# Import the dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text, desc, and_

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
inspector = inspect(conn)

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model

Base = automap_base()
Base.prepare(autoload_with=engine)
Base.classes.keys()

# reflect the tables
station = Base.classes.station
measurement = Base.classes.measurement
inspector.get_table_names()

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
inspector = inspect(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return """
<a href="http://127.0.0.1:5000/api/v1.0/precipitation">precipitation</a>
<br>
<br>
<a href="http://127.0.0.1:5000/api/v1.0/stations">stations</a>
<br>
<br>
<a href="http://127.0.0.1:5000/api/v1.0/tobs">tobs</a>
<br>
<br>
<a href="http://127.0.0.1:5000/api/v1.0/<start>">start</a>
<br>
<br> 
<a href="http://127.0.0.1:5000/api/v1.0/<start>/<end>">start/end</a>
"""

@app.route('/api/v1.0/precipitation') # returns the date and the precipitation
def precipitation():
    session = Session(engine)
    precip = []
    for x,y in session.query(measurement.date,measurement.prcp).filter(measurement.date >='2016-08-23').all():
        precip.append({x:y}) 
    session.close()
       
    return precip

@app.route('/api/v1.0/stations') # returns all the stations
def stations():
    session = Session(engine)
    stat = []
    for x in session.query(station.station).all():    
        stat.append([x][0][0])
    session.close()   
    
    return jsonify(stat) 
    

@app.route('/api/v1.0/tobs') # returns the tobs for the date
def tobs():
    session = Session(engine)
    tobs ={}
    for x,y in session.query(measurement.date,measurement.tobs).filter(measurement.date >='2016-08-17').filter(measurement.station =="USC00519281" ).all():
        tobs[x]=y
    session.close()
       
    return jsonify(tobs)
    
@app.route('/api/v1.0/<start>') # returns the min, avg, and max for each date with a specific start point
def beginning_of_year(start):
    session = Session(engine)
    
    m=measurement  
        
    min_avg_max = []
    for x in session.query(m.date, func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).filter(m.date >=start).group_by(m.date).all():
        min_avg_max.append({x[0]:{'min':x[1],'avg':x[2],'max':x[3]}})
    session.close()
    
    return jsonify(min_avg_max)

@app.route('/api/v1.0/<start>/<end>')  # returns the min, avg, and max for each date with a specific start and end point
def six_month(start, end):
    session = Session(engine)
    
    m=measurement
    
    tmin_tavg_tmax = []
    for x in session.query(m.date, func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).filter(m.date >=start).filter(m.date <=end).group_by(m.date).all():
        tmin_tavg_tmax.append({x[0]:{'min':x[1],'avg':x[2],'max':x[3]}})
    session.close()  
    
    return jsonify(tmin_tavg_tmax)

if __name__ =='__main__':
    app.run(debug=True)