import numpy as np
import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests as req
import time
from scraper import scraped

def initBrowser():
    return Browser("chrome", headless=False)


def closeBrowser(browser):
    browser.quit()


def scrape():
    
    mars_data = {}

    mars_data["news_data"] = marsNewsData()

    mars_data["featured_image_url"] = marsFeaturedImageURL()

    mars_data["mars_weather"] = marsWeather()

    mars_data["mars_facts"] = marsFacts()

    mars_data["mars_hemispheres"] = marsHemisphereImageURLs()


    return mars_data



def marsNewsData():

    news_data = {}
    paragraph_text = []

    base_url = "https://mars.nasa.gov/"
    nasa_url = "https://mars.nasa.gov/news/"
    response_1 = req.get(nasa_url)
    time.sleep(5)

    nasa_soup = bs(response_1.text, 'html.parser')
    soup_div = nasa_soup.find(class_="slide")
    soup_news = soup_div.find_all('a')
    news_title = soup_news[1].get_text().strip()
    soup_p = soup_div.find_all('a', href=True)
    soup_p_url = soup_p[0]['href']
    paragraph_url = base_url + soup_p_url
    response_2 = req.get(paragraph_url)
    time.sleep(5)

    para_soup = bs(response_2.text, "html.parser")
    ww_paragraphs = para_soup.find(class_='wysiwyg_content')
    paragraphs = ww_paragraphs.find_all('p')

    for paragraph in paragraphs:
        clean_paragraph = paragraph.get_text().strip()
        paragraph_text.append(clean_paragraph)

    news_data["news_title"] = news_title
    news_data["paragraph_text_1"] = paragraph_text[0]
    news_data["paragraph_text_2"] = paragraph_text[1]

    return news_data


def marsFeaturedImageURL():

    browser = initBrowser()

    jpl_fullsize_url = 'https://photojournal.jpl.nasa.gov/jpeg/'
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    time.sleep(5)

    featured_image_list = []

    for image in jpl_soup.find_all('div',class_="img"):
        featured_image_list.append(image.find('img').get('src'))

    feature_image = featured_image_list[0]
    temp_list_1 = feature_image.split('-')
    temp_list_2 = temp_list_1[0].split('/')
    featured_image_url = jpl_fullsize_url + temp_list_2[-1] + '.jpg'

    closeBrowser(browser)

    return featured_image_url


def marsWeather():

    browser = initBrowser()

    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(5)

    tweet_html = browser.html
    tweet_soup = bs(tweet_html, 'html.parser')
    time.sleep(5)

    weather_info_list = []

    for weather_info in tweet_soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_info_list.append(weather_info.text.strip())

    for value in reversed(weather_info_list):
        if value[:3]=='Sol':
            mars_weather = value

    closeBrowser(browser)

    return mars_weather


def marsFacts():

    facts_url = 'https://space-facts.com/mars/'
    fact_list = pd.read_html(facts_url)
    time.sleep(5)
    facts_df = fact_list[0]
    facts_table = facts_df.to_html(header=False, index=False)

    return facts_table


def marsHemisphereImageURLs():

    browser = initBrowser()

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    time.sleep(5)

    usgs_html = browser.html
    usgs_soup = bs(usgs_html, 'html.parser')
    time.sleep(5)

    hemisphere_image_urls = []

    products = usgs_soup.find('div', class_='result-list')
    time.sleep(5)
    hemispheres = products.find_all('div', class_='item')
    time.sleep(5)

    for hemisphere in hemispheres:
        title = hemisphere.find('div', class_='description')

        title_text = title.a.text
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)

        usgs_html = browser.html
        usgs_soup = bs(usgs_html, 'html.parser')

        image = usgs_soup.find('div', class_='downloads').find('ul').find('li')
        img_url = image.a['href']

        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})

        browser.click_link_by_partial_text('Back')

    closeBrowser(browser)

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())