  
# import dependencies
from flask import Flask, jsonify, render_template, request
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import scrape_mars

# Set up FLASK and create an app, being sure to pass __name__
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Define the database and data collection
db = client.mars_db
collection = db.items

# Make sure MongoDB is running on your computer by typing `mongod` in a terminal window

# Flask Routes for Home Page and Data Scraping

@app.route("/")
def home_page():
    # Read the mongo db data
    mars_data = collection.find_one()
    # send it along with the html page under the home `/` route function
    return render_template('index.html', payload=mars_data)

@app.route("/scrape")
def scrape_all():
    scrape_dic = scrape_mars.scrape()
    print('scrape_result:', scrape_dic)
    
    #  Put the data into the Mongo DB derived from the scraping function 
    collection.update({}, scrape_dic, upsert=True)
    return f'Scraping done!'
if __name__ == "__main__":
    app.run(debug=True)
