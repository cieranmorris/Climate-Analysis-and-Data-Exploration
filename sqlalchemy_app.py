
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





#Define 'main' behavior
if __name__ == '__main__':
    app.run(debug = True)