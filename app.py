# importing the dependencies:
import datetime as dt
import numpy as np
import pandas as pd
# SQLAlchemy dependencies:
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Importing flask dependency:
from flask import Flask, jsonify


# Setting up the Database
# setup the engine to access the date:
engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

# Saving reference to each table in the database

Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating the session link from Python to the database

session = Session(engine)


# Creating a New Flask App Instance
# instance is a general term in programming referring to a singular version of something.

app = Flask(__name__)
# here, the __name__ is a magic method that denotes the name of the current function. 
# can use the __name__ function if code is run from command line or important from another piece of code.

# Creating the Flask Routes
# First define the starting point called the route
# use the following function:
# The / indicates that we want to put our data at the root of our routes
# The / is commonly known as the highest level of hierarchy in any computer system.

@app.route('/')

def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/percipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''') 
# Convention when creating rows is the /api/v1.0/ followed by the name of the route
# This signals this is the first version of the app

# Note that every time you create a new route, code should be aligned to left to avoid errors

@app.route('/api/v1.0/percipitation')

def percipitation():
    # This code will look very similar to climate_analysis.ipynb
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Creating a dict with date as key and prcp as value
    # Also using the jsonify() function to convert dict to JSON file
    # Recall that JSON files are good for cleaning, filtering, sorting, vis data
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip) 

# Creating the stations route

@app.route('/api/v1.0/stations')

def stations():
    # Creating the query to get stations 
    results = session.query(Station.station).all()
    # Now using the np.ravel() function to unravel results into one dimensional array
    # Then convert unraveled results to a list.
    # Then jsonify
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Creating the Monthly Temperature Route

@app.route('/api/v1.0/tobs')

def temp_month():
    # Calculating the previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(365)
    # Query the primary station for all temp observations
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Creating the Statistics Route

@app.route('/api/v1.0/temp/<start>')

@app.route('/api/v1.0/temp/<start>/<end>')

def stats(start=None, end=None):
    # When function is declared, create a query to select min, avg, and max temps from SQLite database
    # Using the func class to populate a list
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Using if-not statement to determin the start and ending date
    # Run a query using the constructed list
    # unravel results and jsonify

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list (np.ravel(results))

        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# to run the app, use environment variable by putting export FLASK_APP=app.py
# do this after navigating the directory where app.py is saved.