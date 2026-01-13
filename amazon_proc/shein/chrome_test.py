# library to launch and kill Tor process
import os
import subprocess
import random
import sys
import pyodbc
import threading

# library for scraping
import csv
import urllib
from urllib.request import Request, urlopen
import time
import certifi
import hashlib
import uuid
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver  # Import from seleniumwire

import re
import random
from seleniumwire import webdriver  # Import from seleniumwire

service = Service()
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options = webdriver.ChromeOptions()

options.add_argument("user-data-dir={}".format(userProfile))
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://ko.aliexpress.com/'")

driver = webdriver.Chrome(service=service, options=options)

onurl = "https://google.com"
driver.get(onurl)


print(">> ")