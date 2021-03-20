
#Import modules for analysis
import sqlalchemy
import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func, desc, inspect
from flask import Flask, jsonify

#create engine to sqlite file containing data
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")

#Create a base for the new model and reflect tables into this database
Base = automap_base()

Base.prepare(engine, reflect = True)

#Create variables for both measurement and station like in jupyter notebook
measurement = Base.classes.measurement

station = Base.classes.station

#create an app using Flask and pass __name__
app = Flask(__name__)

#create home route for browser
@app.route("/")
def home():
    return (f"Climate Analysis Web Page<br/>"
            f"-------------------------------------------------------<br/>"
            f"<br/>"
            f"Available routes:<br/>"
            f"<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start_date<br/>"
            f"/api/v1.0/start_date/end_date<br/>"
            f"<br/>"
            f"-------------------------------------------------------<br/>"
            f"<br/>")

#create app route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the database
    session = Session(engine)

    # Perform a query to retrieve the precipitation data
    prcp_data = session.query(measurement.date, measurement.prcp).\
                        order_by(measurement.date.desc()).all()

    # Convert query results to a dictionary using date as the key and prcp as the value
    prcp_dictionary = {}
    for date, prcp in prcp_data:
        prcp_dictionary[date] = prcp

    #return a JSON representation of precipitation dictionary
    return jsonify (prcp_dictionary)

    #close session for next app route
    session.close()

#create app route for station data
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the database
    session = Session(engine)

    #Perform query to retrieve station data
    stations_data = session.query(station.id, station.name, station.station).all()

    #return JSON list of stations from dataset
    return jsonify(list(stations_data))

    #close session
    session.close()


#create app route for temperature observance data for the most active station of the year
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the database
    session = Session(engine)

    #Perform query to retrieve temperature observance data
    active_stations = session.query(measurement.station, func.count(measurement.station), station.name).\
                    order_by(func.count(measurement.station).desc()).\
                    group_by(measurement.station).all()

    #Specify most active station
    most_active_station_id = active_stations[0][0]

    #Find latest date, convert to YYYY/MM/DD format and determine date from year previous
    string_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    last_date = (dt.datetime.strptime(string_date, "%Y-%m-%d")).date()

    year_prior_date = last_date - dt.timedelta(days = 365)

    #Perform session query for temperature observations for most active station ID and their associated dates
    temp_observation_data = session.query(measurement.tobs).\
                        filter((measurement.station == most_active_station_id)\
                        & (measurement.date <= last_date)\
                        & (measurement.date >= year_prior_date)).all()

    #Return a JSON of temperature observations (TOBS) for the previous year
    return jsonify(list(temp_observation_data))

    #close session
    session.close()




#Define 'main' behavior
if __name__ == '__main__':
    app.run(debug = True)