# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create our session (link) from Python to the DB




#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > prev_year).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_year = {date:prcp for date, prcp in precipitation}

    return jsonify(prcp_year)

@app.route("/api/v1.0/stations")
def allstations():
    
    stations = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    stn = {station: name for station, name in stations}

    return jsonify(stn)

@app.route("/api/v1.0/tobs")
def temperature():
    
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)

    measure = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > prev_year).all()

    session.close()

    # Convert list of tuples into normal list
    temp = {date: tobs for date, tobs in measure}
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def startdate(start=None):
    
    print(start)
    temp_summary= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                                .filter(Measurement.date == start).all()


    session.close()

    # Convert list of tuples into normal list
    tsum = list(np.ravel(temp_summary))

    return jsonify(tsum)




if __name__ == '__main__':
    app.run(debug=True)