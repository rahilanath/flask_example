import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/chinook.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Invoices = Base.classes.invoices
Items = Base.classes.invoice_items

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/billingcountry'>billingcountry</a><br/>"
        f"<a href='/api/v1.0/countrytotal'>countrytotal</a><br/>"
        f"<a href='/api/v1.0/postcodes/USA'>postcodes/USA</a><br/>"
        f"<a href='/api/v1.0/countryitemtotals/USA'>countryitemtotals/USA</a><br/>"
        f"<a href='/api/v1.0/postcodeitemtotals/USA'>postcodeitemtotals/USA</a><br/>"
    )

@app.route("/api/v1.0/billingcountry")
def billingcountry():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    results = session.query(Invoices.BillingCountry).group_by(Invoices.BillingCountry).all()


    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/countrytotal")
def countrytotal():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries' invoice totals
    results = session.query(Invoices.BillingCountry, func.sum(Invoices.Total)).group_by(Invoices.BillingCountry).order_by(func.sum(Invoices.Total).desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_results
    all_results = []
    for item in results:
        item_dict = {}
        item_dict["country"] = item[0]
        item_dict["total"] = float(item[1])
        all_results.append(item_dict)

    return jsonify(all_results)

@app.route("/api/v1.0/postcodes/<value>")
def postcodes(value):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    results = session.query(Invoices.BillingPostalCode).filter(Invoices.BillingCountry == value).group_by(Invoices.BillingPostalCode).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/countryitemtotals/<value>")
def countryitemtotals(value):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries' invoice totals
    results = session.query(func.sum(Items.UnitPrice * Items.Quantity)).filter(Invoices.InvoiceId == Items.InvoiceId).filter(Invoices.BillingCountry == value).scalar()

    session.close()

    # Create a dictionary from the results
    item_dict = {'country':value, 'total':float(results)}

    return jsonify([item_dict])

@app.route("/api/v1.0/postcodeitemtotals/<value>")
def postcodeitemtotals(value):
    session = Session(engine)
    results = session.query(Invoices.BillingPostalCode, func.sum(Items.UnitPrice * Items.Quantity)).filter(Invoices.InvoiceId == Items.InvoiceId).filter(Invoices.BillingCountry == value).group_by(Invoices.BillingPostalCode).order_by(func.sum(Items.UnitPrice * Items.Quantity).desc()).all()
    session.close()
    all_results = []
    for item in results:
        item_dict = {}
        item_dict["postcode"] = item[0]
        item_dict["total"] = float(item[1])
        all_results.append(item_dict)

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)
