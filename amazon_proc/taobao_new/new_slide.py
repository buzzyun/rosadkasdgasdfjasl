# library to launch and kill Tor process
import os
import subprocess
import random
import sys
import pyodbc
import threading
from multiprocessing import Pool
# library for Tor connection
import socket
import socks
import http.client
import time
import requests
from stem import Signal
from stem.control import Controller
from sys import exit

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

import re
import random
import pyautogui
from datetime import datetime

ver = "1.16"

server = '59.23.231.194,14103'
database = 'freeship'
username = '1stplatfor_sql'
password = '@allin#am1071'
con = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
    autocommit=True)
cursor = con.cursor()

ip = socket.gethostbyname(socket.gethostname())
cursor.execute("update update_list set regdate = GETDATE() where proc_ip = '{0}'".format(ip))


def version_check():
    global ver
    print("version:" + ver)
    file_path = r"c:/project/"
    file_name = "new_slide.exe"
    sql = "select version,url from python_version_manage where name = 'slide'"
    cursor.execute(sql)
    rows = cursor.fetchone()
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        os.system("taskkill /im slide.exe")


service = Service()
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("user-data-dir={}".format(userProfile))
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://ko.aliexpress.com/'")

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)  # seconds
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")


def mouse_slid():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    mydivs = soup.find_all("div", {"class": "baxia-dialog auto"})
    #print(str(mydivs))


    if str(mydivs).find('display: block;') > 1:
        print('okslide')
        SLEEPTIME = random.uniform(3.5, 5.5)
        pyautogui.click(x=7, y=709)
        XRND = random.randrange(365, 385)
        YRND = random.randrange(445, 465)

        XRND2 = random.randrange(655, 700)
        YRND2 =  random.randrange(445, 465)
        FAST = random.uniform(1.35, 3.9)
        pyautogui.moveTo(XRND, YRND)
        pyautogui.dragTo(XRND2, YRND2,FAST, pyautogui.easeInOutBounce)
        pyautogui.press('SPACE')

def mouse_slid2():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #if str(soup).find('J_MIDDLEWARE_FRAME_WIDGET') > 1:
    #    print('okslide2')
    #    time.sleep(5)
    #    SLEEPTIME = random.uniform(3.5, 5.5)
    #    pyautogui.click(x=7, y=709)
    #    XRND = random.randrange(365, 385)
    #    YRND = random.randrange(453, 473)

    #    XRND2 = random.randrange(655, 700)
    #    YRND2 =  random.randrange(453, 473)
    #    FAST = random.uniform(1.35, 3.9)
    #    pyautogui.moveTo(XRND, YRND)
    #    pyautogui.dragTo(XRND2, YRND2,FAST, pyautogui.easeInOutBounce)
    #    pyautogui.press('SPACE')

def shutdownck():
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    sql = "select regdate from update_list where proc_ip = '{0}'".format(ip)
    cursor.execute(sql)
    rows = cursor.fetchone()
    if rows:
        regdate = rows[0]

        now = datetime.now()
        diff = now - regdate

        print(diff.seconds)
        if diff.seconds > 10800:
            print('stop')
            #cursor.execute("update update_list set regdate = GETDATE() where proc_ip = '{0}'".format(ip))
            #os.system("shutdown -r -t 0")
            #time.sleep(30)

while True:
    version_check()
    mouse_slid()
    mouse_slid2()
    SLEEPTIME2 = random.uniform(3.5, 5.5)
    time.sleep(SLEEPTIME2)
    #shutdownck()
