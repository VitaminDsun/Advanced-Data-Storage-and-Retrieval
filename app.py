import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#create classes
Measurement = Base.classes.measurement
Station = Base.classes.station

def m_r_year():
    session = Session(bind=engine)
    r_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    session.close()
    date_fomt = '%Y-%m-%d'
    dtfomt = dt.datetime.strptime(r_date,date_fomt)
    oldest_dt = dtfomt - pd.DateOffset(months=months)
    oldest_dt = oldest_dt.strftime(date_fomt)
    return((r_date,oldest_dt))

# Flask routes
app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
 #query for precipation in last 12 months of data

def precip():
    session = Session(bind=engine)
    recent_date,start_year = m_r_year()
    precip = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date <= recent_date).filter(Measurement.date > start_year)
    session.close()
     #create lists of dates and precipitation
    precip_data = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        precip_data.append(precip_dict)
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def station():
    session = Session(bind=engine)
    station = session.query(Station.station,Station.name).all()
    session.close()
    station_data = []
    for station, name in station:
        station_dict = {}
        station_dict["station_id"] = station
        station_dict["name"] = name
        station_data.append(station_dict)
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(bind=engine)
    recent_date,start_year = m_r_year()
    tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date <= recent_date).filter(Measurement.date > start_year)
    session.close()
    temp_data = []
    for date, temp in tobs:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temp
        temp_data.append(temp_dict)
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>")
def summary_start(start):
    session = Session(bind=engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    oldest_date = session.query(Measurement.date).order_by(Measurement.date).first()[0]
    stats = session.query(func.min(Measurement.tobs).label("Min Temp"),func.max(Measurement.tobs).label("Max Temp"),func.avg(Measurement.tobs).label("Average Temp")).filter(Measurement.date >= start)
    stat_list = []
    for s_min, s_max, s_avg in stats:
        s_dict = {}
        s_dict['min_temp'] = s_min
        s_dict['max_temp'] = s_max
        s_dict['avg_temp'] = s_avg
        stat_list.append(s_dict)
    return jsonify(stat_list)
    session.close()


@app.route("/api/v1.0/<start>/<end>")
def summary_start_end(start,end):
    session = Session(bind=engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    oldest_date = session.query(Measurement.date).order_by(Measurement.date).first()[0]
    stats = session.query(func.min(Measurement.tobs).label("Min Temp"),func.max(Measurement.tobs).label("Max Temp"),func.avg(Measurement.tobs).label("Average Temp")).filter(Measurement.date >= start).filter(Measurement.date <=end)
    stat_list = []
    for s_min, s_max, s_avg in stats:
        s_dict = {}
        s_dict['min_temp'] = s_min
        s_dict['max_temp'] = s_max
        s_dict['avg_temp'] = s_avg
        stat_list.append(s_dict)
    return jsonify(stat_list)
    session.close()

if __name__ == ("__main__"):
    app.run(debug=True)



#List all available routes.



#  'worked with TA's, tuttors, and Other students to develop code and also looked some stuff up onon stackoverflow to help me find the answers need to get the right idea going'