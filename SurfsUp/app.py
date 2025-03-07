# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta  # Import these here!

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`

Base = automap_base()

# Use the Base class to reflect the database tables

Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation - Last 12 months of precipitation <br/>"
        f"/api/v1.0/stations - List of stations <br/>"
        f"/api/v1.0/tobs - List of table observations for the previous year <br/>"
        f"/api/v1.0/<start> - Min, Avg, & Max Teps for specific dates <br/>"
        f"/api/v1.0/<start>/<end> - Min, Avg, Max temps for start to end dates <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    l12_mos = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= l12_mos).all()
    prcp_data = {date: prcp for date, prcp in results}
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = [station[0] for station in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_yr = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
        .filter(Measurement.date >= last_yr)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()[0]
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= last_yr).all()
    tobs_data = [temp for _, temp in results]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    temps = results[0] 
    return jsonify({
        "TMIN": temps[0],
        "TAVG": temps[1],
        "TMAX": temps[2]
    })

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()
    temps = results[0] 
    return jsonify({
        "TMIN": temps[0],
        "TAVG": temps[1],
        "TMAX": temps[2]
    })

if __name__ == '__main__':
    app.run(debug=True)