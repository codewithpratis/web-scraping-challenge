#import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


    
    # Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

    
    # create dictinary
    scrape_mars = {}

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
    articles = soup.find('div', class_='image_and_description_container')
    #try:
     #   scrape_mars['news_title'] = articles.find('div', class_='content_title').get_text()
      #  scrape_mars['news_p'] = articles.find('div', class_='article_teaser_body').get_text()
    #except AttributeError:
        #print ("news: -")
    scrape_mars['news_title'] = articles.find('div', class_='content_title').get_text()
    scrape_mars['news_p'] = articles.find('div', class_='article_teaser_body').get_text()

    # Dictionary entry from MARS NEWS
    scrape_mars
    
     # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)
    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    scrape_mars['featured_image_url'] = main_url + featured_image_url

    # Display full link to featured image
    print(scrape_mars)

        

# Mars Weather 
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            scrape_mars['mars_weather'] = latest_tweets
            break
        else: 
            pass
    latest_tweets

        


# Mars Facts
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    scrape_mars['mars_df'] = mars_df
    scrape_mars['mars_df']

  


# MARS HEMISPHERES
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hiu = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
            
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
            
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
            
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
            
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
        # Append the retreived information into a list of dictionaries 
        hiu.append({"title" : title, "img_url" : img_url})
        
        browser.back()

    scrape_mars['hiu'] = hiu

    alt_url_list = {'Cerberus Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg',
 'Schiaparelli Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg',
 'Syrtis Major Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg',
 'Valles Marineris Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}

    alt_image_url_list = []

    for title,url in alt_url_list.items():
        alt_image_url_list.append({'title':title,'url':url})

    scrape_mars['alt_img_url']=alt_image_url_list




    browser.quit()

    return scrape_mars