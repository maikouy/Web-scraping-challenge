from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Route to render index.html template using data from Mongo
@app.route("/")
def index():

    #Find record of data from the mongo database
    listing = mongo.db.listing.find_one()
    #Return template and data
    return render_template("index.html", listing=listing)


@app.route("/scrape")
def scraper():
    listing = mongo.db.listing
    listing_data = scrape_mars.scrape()
    listing.update({}, listing_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
