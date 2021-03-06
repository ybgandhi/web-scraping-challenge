# import all dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def chrome_browser():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #return Browser('chrome', **executable_path)
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = chrome_browser()
    #************************************************
    ## NASA Mars News
    #************************************************

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # set timer for processing break
    time.sleep(1)

    # scrape using soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # retrieve title
    news_title = soup.find_all('div', class_='content_title')[0].text
    #title
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text
    news_p

    #************************************************
    ## JPL Mars Space Images
    #************************************************

    #JPL url
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)

    #beautifil soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # find image
    image_url = soup.find('img', class_='thumbimg')['src']
    print(image_url)

    featured_image_url = f"{jpl_url}{image_url}"

    #************************************************
    ## Mars Facts
    #************************************************
    mars_facts_url = "https://galaxyfacts-mars.com/"

    tables = pd.read_html(mars_facts_url)

    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_fact.set_index("Profile",inplace=True)
    mars_fact

    fact_table_html=mars_fact.to_html(classes="table table-striped")
    fact_table_html

    fact_table_html.replace('\n','')
    #print(fact_table_html)

    #************************************************
    ## Mars Hemipheres
    #************************************************

    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # scrape hemisphere website
    hemisphere_url = "https://marshemispheres.com"
    browser.visit(hemisphere_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')

    # extract hemispheres item elements
    hemisphere = hemi_soup.find_all('div', class_='description')
    print(hemisphere)
    
    # set up empty list to store all image and url string
    hemisphere_list = []

    # loop through each hemisphere that are on Mars
    for item in range(len(hemisphere)):
        hemisphere_link = browser.find_by_css('a.product-item h3')
        hemisphere_link[item].click()
        time.sleep(1)
        #print(hemisphere_link)
        
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        
        img_title = img_soup.find('h2',class_='title').text
        
        img_find_class = img_soup.find('div', class_="downloads")
        img_find_click = img_find_class.find('li')
        img_find = img_find_click.find('a')['href']
        
        img_url = f"{hemisphere_url}/{img_find}"
        
        hemisphere_list.append({"title":img_title,
                        "img_url":img_url})
        browser.back()

    hemisphere_list
    browser.quit()

    #************************************************
    ## store in dictionary
    #************************************************
    scraped_data = {
        "title_part": news_title,
        "news": news_p,
        "featured_image": featured_image_url,
        "mars_table": fact_table_html,
        "hemisphere_images": hemisphere_list 
    }
    return scraped_data