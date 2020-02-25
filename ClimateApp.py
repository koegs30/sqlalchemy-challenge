import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
import datetime as dt

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Home Page"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end"
    )
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

latest_date = session.query(Measurement.date).order_by(Measurement.date).first()
latest = latest_date[0]
late = latest.split('-')
year = int(late[0])
day = int(late[1])
month = int(late[2])

query_date = dt.date(year, day, month) - dt.timedelta(days=366)
year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>query_date).order_by(Measurement.date.asc()).all()
precip_dict = {sub[0]: sub[1:] for sub in year_precip}


@app.route("/api/v1.0/precipitation")
def precip():
    return (
        jsonify(precip_dict)
    )

stations=session.query(Station.name).group_by(Station.name).all()

stations_list = []
for sublist in stations:
    for item in sublist:
        stations_list.append(item)

@app.route("/api/v1.0/stations")
def station():
    return(
        jsonify(stations_list)
    )

yr_temps = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > query_date).all()
for results in yr_temps:
    yr_temps_dict = {"TOBs":yr_temps[1:]}

@app.route("/api/v1.0/tobs")
def tobs():
    return(
        jsonify(yr_temps_dict)
    )

start_date = dt.date(2016,6,27)
end_date = dt.date(2016,7,4)

sel = [Station.name,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
start = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.station==Station.station).group_by(Station.name).all()
start_dict = {sub[0]: sub[1:] for sub in start}

@app.route("/api/v1.0/start")
def date_temp():
    return(
        jsonify(start_dict)
    )

sel2 = [Station.name,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
start_end = session.query(*sel2).filter(Measurement.date >= start_date, Measurement.date<=end_date).filter(Measurement.station==Station.station).group_by(Station.name).all()
start_end_dict = {sub[0]: sub[1:] for sub in start_end}

@app.route("/api/v1.0/start/end")
def date_temp2():
    return(
        jsonify(start_end_dict)
    )

if __name__ == "__main__":
    app.run(debug=True)