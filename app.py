from flask import Flask, jsonify, redirect, render_template
from pymongo import MongoClient
import scrape_mars

client = MongoClient('localhost',27017)

app = Flask(__name__)

db = client.mars_data_DB
mars_collection = db.mars_collection

@app.route("/")
def render_index():
    
   
    mars_find =  mars_collection.find_one()

        
    news_title = mars_find['news_data']['news_title']
    paragraph_text_1 = mars_find['news_data']['paragraph_text_1']
    paragraph_text_2 = mars_find['news_data']['paragraph_text_2']
    featured_image_url = mars_find['featured_image_url']
    mars_weather_tweet = mars_find['mars_weather']
    mars_facts_table = mars_find['mars_facts']
    hemisphere_title_1 = mars_find['mars_hemispheres'][0]['title']
    hemisphere_img_1 = mars_find['mars_hemispheres'][0]['img_url']
    hemisphere_title_2 = mars_find['mars_hemispheres'][1]['title']
    hemisphere_img_2 = mars_find['mars_hemispheres'][1]['img_url']
    hemisphere_title_3 = mars_find['mars_hemispheres'][2]['title']
    hemisphere_img_3 = mars_find['mars_hemispheres'][2]['img_url']
    hemisphere_title_4 = mars_find['mars_hemispheres'][3]['title']
    hemisphere_img_4 = mars_find['mars_hemispheres'][3]['img_url']
    
    return render_template("index.html", news_title=news_title,\
                                         paragraph_text_1=paragraph_text_1,\
                                         paragraph_text_2=paragraph_text_2,\
                                         featured_image_url=featured_image_url,\
                                         mars_weather_tweet=mars_weather_tweet,\
                                         mars_facts_table=mars_facts_table,\
                                         hemisphere_title_1=hemisphere_title_1,\
                                         hemisphere_img_1=hemisphere_img_1,\
                                         hemisphere_title_2=hemisphere_title_2,\
                                         hemisphere_img_2=hemisphere_img_2,\
                                         hemisphere_title_3=hemisphere_title_3,\
                                         hemisphere_img_3=hemisphere_img_3,\
                                         hemisphere_title_4=hemisphere_title_4,\
                                         hemisphere_img_4=hemisphere_img_4)

# --------------------------------------------------------------------------
# Initializes scrape route; inserts results into  mars_data_DB in MongoDB
# --------------------------------------------------------------------------
@app.route('/scrape')
def scrape_mars_data():
    scrape_results = scrape_mars.scrape()
    mars_collection.replace_one({}, scrape_results, upsert=True)
    return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run(debug=True, port=1140)