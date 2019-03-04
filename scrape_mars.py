
# Ran script to convert the jupyter notebook "mission_to_mars" into a Python script called scrape_mars_py
# ipython nbconvert --to script notebook.ipynb

# # Mission to Mars
# Import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import numpy as np
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Various websites containing information on Planet Mars will be visited and certain data will be scraped
# The script will collect all data in a Python dictionary

def scrape():

    browser = init_browser()
    mars_data = {}

# NASA Mars News
# Go to https://mars.nasa.gov/news NASA Mars News

    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)

#Pause Python Code
    time.sleep(1)

# Scrape page into Soup
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "html.parser")


# Collect latest news title and paragragh text
    nasa_news_title = nasa_soup.find('div', class_='content_title').text
    nasa_news_p = nasa_soup.find('div', class_='article_teaser_body').text
    
    mars_data["nasa_news_title"] = nasa_news_title
    mars_data["nasa_news_p"] = nasa_news_p


# # JPL  Mars Space Images - Featured Image
# Go to https://www.jpl.nasa.gov

    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')      

    image_url = jpl_soup.find('img', class_='main_image')
    end_image_url = image_url.get('src')
    mars_image_url = "https://www.jpl.nasa.gov" + end_image_url
    mars_data["mars_image_url"] = mars_image_url

  

# # Mars Weather
# Mars Weather twitter account
# Go to "https://twitter.com/marswxreport?lang=en"

    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)

# Scrape the latest Mars weather tweet from the page
    weather_html = browser.html
    weather_soup = bs(weather_html, "html.parser")
   
    tweets= weather_soup.find_all('div', class_="js-tweet-text-container")

    for tweet in tweets:
        mars_weather = tweet.find('p').text
        if 'InSight' in mars_weather:
            print(mars_weather)
            break
        else:
            pass
        
    mars_data["mars_weather"] = mars_weather


# # Mars Facts
# Go to "https://space-facts.com/mars/"

    url_mars_facts = "https://space-facts.com/mars/"


# Scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_fact_table = pd.read_html(url_mars_facts)


# Create dataframe from table
    mars_fact_df = mars_fact_table[0]
    mars_fact_df.columns = ['Measurement', 'Fact']
 
# Set the index to the first column
    mars_fact_df.set_index('Measurement', inplace=True)

    mars_html_table = mars_fact_df.to_html()

# Strip unwanted newlines to clean up the table.
    mars_html_table.replace('\n', '')
 
    mars_facts = mars_html_table

# Save data to dictionary
    mars_data["mars_facts"] = mars_facts


# # Mars Hemispheres - USGS Astrogeology site
# Go to "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_usgs)


# Parse HTML with Beautiful Soup
    hemisphere_html = browser.html
    hemi_soup = bs(hemisphere_html, "html.parser")

# Save the url strings in list  
    hemi_urls = []
    
# Retrieve all items that contain mars hemispheres information
    items = hemi_soup.find_all('div', class_='item')

# Store the base url for the website
    hemispheres_base_url = 'https://astrogeology.usgs.gov'


# Loop through the items previously stored
    for i in items: 
    
    # Store title
        title = i.find('h3').text
    
    # Store link that leads to full image website
        relative_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
        browser.visit(hemispheres_base_url + relative_img_url)
    
    # HTML Object of individual hemisphere information website 
        relative_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        hemi_soup = bs(relative_img_html, 'html.parser')
    
    # Retrieve full image source 
        img_url = hemispheres_base_url + hemi_soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
        hemi_urls.append({"title" : title, "img_url" : img_url})   

    mars_data["hemisphere_images"] = hemi_urls

    return mars_data

     # Close the browser after scraping
    browser.quit()