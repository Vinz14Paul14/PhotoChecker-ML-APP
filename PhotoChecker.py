# project-2 Stocker Picker App
# Tanvir Khan, Nicky Pant, Paul Pineda, James Ye, Fabienne Zumbuehl

import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from flask import Flask, render_template, redirect

#################################################
# Database Setup
#################################################
db_uri = ""
try:
    from .config import db_username
    from .config import db_password
    db_uri = f'postgresql://{db_username}:{db_password}@localhost:5432/FinalProject'
except ImportError:
    print("config not found!")
    db_uri = "sqlite:///db.sqlite"

final_db_uri = os.environ.get('DATABASE_URL', '') or db_uri
print(final_db_uri)

engine = create_engine(final_db_uri)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Company = Base.classes.company
Price = Base.classes.price

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template('photochecker.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/v1.0/company")
def getAllCompanies():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # results is a list of tuples
    results = session.query(Company).all()
    session.close()
    companies = []
    for row in results:
        company = {}
        company['ticker'] = row.ticker
        company['name'] = row.name
        company['ranking'] = row.ranking
        company['mkt_cap'] = row.mkt_cap
        company['pe_ratio'] = row.pe_ratio
        company['eps'] = row.eps
        company['dividend_pct'] = row.dividend_pct
        company['exchange'] = row.exchange
        company['esg_score'] = row.esg_score
        company['recom_rating'] = row.recom_rating
        company['sector'] = row.sector
        company['industry'] = row.industry
        company['country'] = row.country
        company['city'] = row.city
        company['latitude'] = row.latitude
        company['longitude'] = row.longitude
        companies.append(company)

    return jsonify(companies)


# this part must be placed at the end of the file!!	
if __name__ == '__main__':
    app.run(debug=True)