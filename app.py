# import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database
# create the link to sql file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# set up flask
app = Flask(__name__)

# flask route
@app.route("/")
def welcome():
    #list all API routes
    return (
        f"Welcome to hawaii<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # get the last date in the data set
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_12_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()

    prcp_list = []

    for row in last_12_prcp:
        date = str(last_12_prcp[0])
        row = {date:last_12_prcp[1]}
        prcp_list.append(row)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    station_location = session.query(Station.station).all()
    stations = list(np.ravel(station_location))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # get the last date in the data set
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_12_tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).order_by(Measurement.date).all()

    tobs_list = []

    for row in last_12_tobs:
        date = str(last_12_tobs[0])
        row = {date:last_12_tobs[1]}
        tobs_list.append(row)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def trip1(start):

    # find out the start time 
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    # find out tmin tavg tmax
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


if __name__ == "__main__":
    app.run(debug=True)




