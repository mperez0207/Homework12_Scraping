# Import our scraping script
import scrape_mars

# Import flask
from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Set route
@app.route('/')
def index():
    # Scrape data
    scrape()

    # Retrieve scraped data
    client = pymongo.MongoClient()
    db = client["mars"]
    collection = db["mars_data"]
    
    mars_data = collection.find_one()

    client.close()

    # Render html page with scraped data
    return render_template("index.html", news_title=mars_data["news_title"], news_paragraph=mars_data["news_paragraph"],
                           feat_image_url=mars_data["feat_image_url"], weather_tweet=mars_data["weather_tweet"],
                           facts_html_table=mars_data["facts_html_table"], 
                           valles_marineris_url=mars_data["hemisphere_urls"][3]["img_url"], valles_marineris_title=mars_data["hemisphere_urls"][3]["title"],
                           cerberus_url=mars_data["hemisphere_urls"][0]["img_url"], cerberus_title=mars_data["hemisphere_urls"][0]["title"],
                           schiaparelli_url=mars_data["hemisphere_urls"][1]["img_url"], schiaparelli_title=mars_data["hemisphere_urls"][1]["title"],
                           syrtis_major_url=mars_data["hemisphere_urls"][2]["img_url"], syrtis_major_title=mars_data["hemisphere_urls"][2]["title"])

@app.route('/scrape')
def scrape():
    # Create pymongo instance
    client = pymongo.MongoClient()

    # Connect to a database. Will create one if not already available.
    db = client["mars"]
    collection = db["mars_data"]

    # Insert scraped data
    collection.delete_many({})
    collection.insert_one(scrape_mars.scrape())

    client.close()

    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
