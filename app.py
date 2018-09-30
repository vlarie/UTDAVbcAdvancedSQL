#######################################################
###  Dependencies for functionality inside apps  #####
#####################################################

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, distinct


#######################################################
###  Establishing connection for database queries  ###
#####################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#######################################################
#####  Connection creation for database queries  #####
#####################################################

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return render_template("index.html")

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    qryLD = session.query(func.max(Measurement.date).label("lastDay")).one()
    maxDate = qryLD.lastDay
    lastDay = dt.strptime(maxDate, '%Y-%m-%d')
    pastYear = lastDay - relativedelta(years=1)
    prcpPY = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > pastYear).all()
    return jsonify(dict(prcpPY))


@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' page...")
    qryLD = session.query(func.max(Measurement.date).label("lastDay")).one()
    maxDate = qryLD.lastDay
    lastDay = dt.strptime(maxDate, '%Y-%m-%d')
    pastYear = lastDay - relativedelta(years=1)
    tobsPY = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > pastYear).all()
    return jsonify(dict(tobsPY))


@app.route("/api/v1.0/<start>") 
def start(start):
    print("Server received request for 'Weather Stats (start)' page...")
    startDate = dt.strptime(start, '%Y-%m-%d')
    minTemp = func.min(Measurement.tobs).label("minTemp")
    maxTemp = func.max(Measurement.tobs).label("maxTemp")
    avgTemp = func.avg(Measurement.tobs).label("avgTemp")
    result = session.query(minTemp, maxTemp, avgTemp).filter(Measurement.date >= startDate).one()
    TMIN = result.minTemp
    TMAX = result.maxTemp
    TAVG = result.avgTemp
    return jsonify({"Lowest Temperature": TMIN, "Highest Temperature": TMAX, "Average Temperature": TAVG})


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    print("Server received request for 'Weather Stats (start/end)' page...")
    startDate = dt.strptime(start, '%Y-%m-%d')
    endDate = dt.strptime(end, '%Y-%m-%d')
    minTemp = func.min(Measurement.tobs).label("minTemp")
    maxTemp = func.max(Measurement.tobs).label("maxTemp")
    avgTemp = func.avg(Measurement.tobs).label("avgTemp")
    result = session.query(minTemp, maxTemp, avgTemp).filter(endDate >= startDate).one()
    TMIN = result.minTemp
    TMAX = result.maxTemp
    TAVG = result.avgTemp
    return jsonify({"Lowest Temperature": TMIN, "Highest Temperature": TMAX, "Average Temperature": TAVG})


if __name__ == "__main__":
    app.run(debug=True)