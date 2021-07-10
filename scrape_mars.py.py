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
     