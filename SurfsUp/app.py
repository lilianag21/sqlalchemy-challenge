# Import the dependencies.

import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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


#################################################
# Flask Setup
#################################################

app = Flask(__name__)
session = Session(engine)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 months of precipitation data<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations from the most active station<br/>"
        f"/api/v1.0/{{start}} - Min, Avg, Max temperature from a start date<br/>"
        f"/api/v1.0/{{start}}/{{end}} - Min, Avg, Max temperature for a date range"
    )