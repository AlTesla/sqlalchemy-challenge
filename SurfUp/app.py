# Import the dependencies.
from flask import Flask, render_template, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    """List all avilable api routes"""
    return render_template('routes.html')


@app.route("/api/v1.0/precipitation")
def precipitation():
    #query the last 12 months of data 
    data = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date >= '2016-08-23').all()
    #convert the query result to a dictionary
    result = {date: prcp for date, prcp in data}
    #return the Json representation of the dictionary
    return jsonify(result)


@app.route("/api/v1.0/stations")
def stations():
    #query the station column from the dataset
    data = session.query(Station.station).all()
    #convert the query result to a list
    result = [station for station, in data]
    #return the JSON representaion of the list
    return jsonify(result)
 

@app.route("/api/v1.0/tobs")   
def tobs():
    #calculate the previous year date 
    prev_year = dt.date(last_date) - dt.timedelta(days=365)
    #query the most atctive station 
    most_active_station = session.query(Measurement.station, \
        func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0] 
    #query the dates and temperature observations of the most active#
    #   station for the previous yer                                #
    data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= prev_year).all()
    #convert the query result to a list
    result = [tobs for date, tobs in data]
    #return the JSON representation of the list
    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True, port=5003)