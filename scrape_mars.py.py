# import all dependencies
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import pymongo
from selenium import webdriver
import time

def chrome_browser():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = chrome_browser()

    ## NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #set timer for processing break
    time.sleep(1)

    #scrape using soup
    html = browser.html
    soup = bs(html, 'html_parser')
