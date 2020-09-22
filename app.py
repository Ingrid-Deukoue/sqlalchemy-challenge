#Import dependencies
#import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

#Set up the database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

#flask setup
app = Flask(__name__)


#Set FLask routes

@app.route("/")
def main():
    """Lists all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary where the date is the key and the value is 
    the precipitation value"""

    print("Received precipitation api request.")

    #find the last date in the database
    final_date= session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_query = final_date_query[0][0]
    max_date = datetime.datetime.strptime(max_date_query, "%Y-%m-%d")
    #find the first date of the database
    begin_date = max_date - datetime.timedelta(366)
    #find dates and precipitation amounts
    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()
        
    #Dictionnary
    JSON_dict = {}
    for result in precip_data:
        JSON_dict[result[0]] = result[1]

    return jsonify(JSON_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""

    print("Received station api request.")

    #query stations list
    stations_data = session.query(Station).all()

    #create a list of dictionaries
    stations_list = []
    for station in stations_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""

    print("Received tobs api request.")

    #We find temperature data for the last year.  First we find the last date in the database
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")

    #set beginning of search query
    begin_date = max_date - datetime.timedelta(366)

    #get temperature measurements for last year
    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()

    #create list of dictionaries (one for each observation)
    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum, average, and maximum temperatures from the start date until
    the end of the database."""

    print("Received start date api request.")

    #last date in the database
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date = final_date_query[0][0]

    #temperatures
    temps = calc_temps(start, max_date)

    #create a list
    return_list = []
    date_dict = {'start_date': start, 'end_date': max_date}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(return_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a JSON list of the minimum, average, and maximum temperatures from the start date unitl
    the end date."""

    print("Received start date and end date api request.")

    #get the temperatures
    temps = calc_temps(start, end)

    #create a list
    return_list = []
    date_dict = {'start_date': start, 'end_date': end}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(return_list)

#code to actually run
if __name__ == "__main__":
    app.run(debug = True) 










