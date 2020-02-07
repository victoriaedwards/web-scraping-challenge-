from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests

def scrape():
    
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()
    return final_data


def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    return mars_info

def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    image_html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    mars_info['featured_image_url'] = featured_image_url 
    return mars_info

def marsWeather():
    twitter_response = requests.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = bs(twitter_response.text, 'html.parser')
    tweet_list= twitter_soup.find_all('div', class_="js-tweet-text-container")
    
    for i in range(100):
    weather_tweet = tweet_list[i].text
    if "Sol " and "pressure" in weather_tweet:
        print(weather_tweet)
        break
    mars_weather['weather_tweet'] = weather_tweet
    return mars_weather
def marFacts():
    facts_url='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Description','Value']
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    return marsFacts
def marsHemispheres():
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html=browser.html
    soup = bs(hemisphere_html, 'html.parser')
    hemisphere_items = soup.find_all('div', class_='item')
    mars_hemispheres = []
    hemisphere_main_url = 'https://astrogeology.usgs.gov'
   
    
    for item in hemisphere_items: 
        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']    
        browser.visit(hemisphere_main_url + partial_img_url) 
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']
        mars_hemispheres.append({"title" : title, "img_url" : img_url})
    
    return mars_hemispheres
        