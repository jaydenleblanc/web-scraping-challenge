from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongodb connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_hemispheres_app"
mongo = PyMongo(app)

#This is the route that will be used for the home page from Mongo
@app.route("/")
def index():
    listings = mongo.db.collection.find_one()
    return render_template("index.html", listings=listings)


#This is the route that will trigger the scrape function
@app.route("/scrape")
def scrapper():
    
    listings_data = scrape_mars.scrape()
    mongo.db.collection.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    