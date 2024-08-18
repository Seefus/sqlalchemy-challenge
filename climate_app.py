# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement=Base.classes.measurement
Station=Base.classes.station
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        "Welcome to my 'Home' page!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).\
    order_by(Measurement.date).all()
    session.close()
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    session = Session(engine)
    results = session.query(Station.station).group_by(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()
    session.close()
    tobs = {date: tobs for date, tobs in results}
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    print(f"Server received request for data starting from {start}...")
    session = Session(engine)
    results = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')
    ).filter(Measurement.date >= start).all()
    session.close()
    temps = {
        "TMIN": results[0].TMIN,
        "TAVG": results[0].TAVG,
        "TMAX": results[0].TMAX
    }
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print(f"Server received request for data from {start} to {end}...")
    session = Session(engine)
    results = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')
    ).filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    session.close()
    temps = {
        "TMIN": results[0].TMIN,
        "TAVG": results[0].TAVG,
        "TMAX": results[0].TMAX
    }
    return jsonify(temps)
if __name__ == "__main__":
    app.run(debug=True)

http://127.0.0.1:5000/
http://127.0.0.1:5000/api/v1.0/precipitation
http://127.0.0.1:5000/api/v1.0/stations
http://127.0.0.1:5000/api/v1.0/tobs
http://127.0.0.1:5000/api/v1.0/2016-08-24
http://127.0.0.1:5000/api/v1.0/2016-09-08/2016-11-01