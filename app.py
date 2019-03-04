# import necessary libraries
import os

from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo

import scrape_mars

# create instance of Flask app - declare the app variable

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route('/')
def home():
    #mars = mongo.db.mars.find_one()
    app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_DB"
    mongo = PyMongo(app)
    mars = mongo.db.mars_collection.find_one()
    return render_template('index.html', mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_DB"
    mongo = PyMongo(app)
    mars_table = mongo.db.mars_collection

    # Run the scrape function
    data = scrape_mars.scrape()
    #data = {"saturn": 4, "jupiter": 6, "sun": "1"}
    # Update the Mongo database using update and upsert=True
    mars_table.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
