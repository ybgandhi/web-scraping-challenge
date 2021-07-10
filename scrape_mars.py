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
    return Browser('chrome', **executable_path)
    #return Browser('chrome', **executable_path, headless=False)

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
    soup = bs(html, 'html_parser')

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

    fact_table_html=mars_fact.to_html()
    fact_table_html

    fact_table_html.replace('\n','')
    #print(fact_table_html)



