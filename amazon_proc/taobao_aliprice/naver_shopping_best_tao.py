import os
import sys
import pyodbc
import threading
import http.client
import time
import pyautogui
import requests
from sys import exit
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import selenium
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
import multiprocessing
import certifi
import json
import datetime
import socket
import socks
from stem import Signal
from stem.control import Controller
from common import DBmodule as DB
import pyautogui
import urllib.parse

#https://search.shopping.naver.com/search/all?adQuery=%EC%9B%90%ED%94%BC%EC%8A%A4&origQuery=%EC%9B%90%ED%94%BC%EC%8A%A4&pagingIndex=1&pagingSize=40&productSet=overseas&query=%EC%9B%90%ED%94%BC%EC%8A%A4&sort=review&timestamp=&viewType=list



ver = "2.386"
ip = socket.gethostbyname(socket.gethostname())

server = '59.23.231.194,14103'
database = 'aliexpress'
username = '1stplatfor_sql'
password = '@allin#am1071'
con = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
    autocommit=True)
cursor = con.cursor()


def isHangul(text):
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

def killTor(sproc):
	sproc.kill()

#파싱 함수
def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result.strip()

def connectTor():
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	socket.socket = socks.socksocket
	print("Connected to Tor")


def set_new_ip():
	# disable socks server and enabling again
	socks.setdefaultproxy()
	"""Change IP using TOR"""
	with Controller.from_port(port=9151) as controller:
		controller.authenticate()
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
		socket.socket = socks.socksocket
		controller.signal(Signal.NEWNYM)


def checkIP():
	conn = http.client.HTTPConnection("icanhazip.com")
	conn.request("GET", "/")
	time.sleep(3)
	response = conn.getresponse()
	print('current ip address :', response.read())


def getSiteDB(goodscode):
	head = "".join(re.findall("[a-zA-Z]+", goodscode))

	site_list = {
		"G": "fashion", "A": "auto", "Y": "baby", "E": "electron", "F": "furniture", "I": "industry", "J": "jewelry",
		"O": "office", "S": "sports", "B": "beauty",
		"CG": "fashion2", "CA": "auto2", "CY": "baby2", "CE": "electron2", "CF": "furniture2", "CI": "industry2",
		"CJ": "jewelry2", "CO": "office2", "CS": "sports2", "CB": "beauty2", "pri": "nprice", "free": "freeship"
	}

	site = site_list[head]

	db = DB.Database(site)
	print(site)
	return db


def getSearchEngine(goodscode):
    head = "".join(re.findall("[a-zA-Z]+", goodscode))
    guid = "".join(re.findall("\d+", goodscode))
    guid = guid.lstrip("0")


    site_list = {
        "G": "fashion", "A": "auto", "Y": "baby", "E": "electron", "F": "furniture", "I": "industry", "J": "jewelry",
        "O": "office", "S": "sports", "B": "beauty",
        "CG": "fashion2", "CA": "auto2", "CY": "baby2", "CE": "electron2", "CF": "furniture2", "CI": "industry2",
        "CJ": "jewelry2", "CO": "office2", "CS": "sports2", "CB": "beauty2"
    }

    site = site_list[head]
    print(head)

    url = "http://59.23.231.204:8090/service/search.json"
    search_str = "{{goodscode:ALL({0}):100:15}}".format(goodscode)
    params = {"cn": site, "fl": "uid,title,imgb,price,naver_catecode,catecode,ali_no,originalprice,coupon,withbuy,SHIPPING", "se": search_str, "sn": 1, "ln": 10}

    try:
        res = requests.get(url, params=params)
        result = res.text
        return result

    except Exception as swear:
	    price_low()


def fun_item():
    timer = threading.Timer(1, fun_item)


    service = Service()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument("user-data-dir={}".format(userProfile))
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
            random.random()) + " Safari/537.36, 'Referer': 'https://ko.aliexpress.com/'")

    driver = webdriver.Chrome(service=service, options=options)



    naver_url = "https://search.shopping.naver.com/search/category/100011132?adQuery&catId=50000807&origQuery&pagingIndex=1&pagingSize=106&productSet=overseas&query&sort=rel&spec=M10013382%7CM10731145%20M10012485%7CM10032139%20M10012485%7CM10588283%20M10012485%7CM10669979%20M10012485%7CM10574793&timestamp=&viewType=list"
    naver_url2 = "https://shopping-phinf.pstatic.net/main_8850774/88507744596.jpg"
    #//*[@id="ap-sbi-alipriceTaobao-result"]/div/div[1]/div/div/button
    #/html/body/div[2]/div/div[1]/div[1]/div[1]
    #/html/body/div[2]/div/div[1]/div[1]/div[1]
    #body > div.ap-ext.ap-ext-taobao_search_by_image > div > div:nth-child(1) > div.ap-sbi
    #body > div.ap-ext.ap-ext-taobao_search_by_image > div > div:nth-child(1) > div.ap-sbi > div.ap-sbi-btn-search-wrapper.ap-is-expanded
    #body > div.ap-ext.ap-ext-taobao_search_by_image > div > div:nth-child(1) > div.ap-sbi > div.ap-sbi-btn-search-wrapper.ap-is-expanded
    #// *[ @ id = "content"] / div[1] / div[2] / div / div[1] / div / div[1] / div / a
    #// *[ @ id = "content"] / div[1] / div[2] / div / div[2] / div / div[1] / div / a / img
    #/ html / body / div[2] / div / div[1] / div[1] / div[1]
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(10)  # seconds
    driver.get(naver_url2)

    required_image = driver.find_element(By.XPATH,'/html/body/img')
    hidden_submenu = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[1]/div[1]/div[1]/i')

    menu = driver.find_element(By.CSS_SELECTOR, "body > img")
    hidden_submenu = driver.find_element(By.CSS_SELECTOR, "body > div > div > div:nth-child(2) > div.ap-sbi > div.ap-sbi-btn-search-wrapper > div.ap-sbi-btn-search > i")

    actions = ActionChains(driver)
    actions.move_to_element(menu)
    actions.click(hidden_submenu)
    actions.perform()

    loadcon2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ap-sbi-alipriceTaobao-result > div > div.ap-list.ap-list--gallery > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > div > div:nth-child(1) > div > div.ap-is-link.ap-product-image')))
    actions.click(loadcon2)
    actions.perform()
    while 1:
        driver.switch_to.window(driver.window_handles[-1])
        tao_url = driver.current_url
        if str(tao_url).find('detail.tmall.com') > 0:
            item_id = getparse(tao_url, 'id=', '&')
            print(tao_url)
            break
        elif str(tao_url).find('item.taobao.com') > 0:
            item_id = getparse(tao_url, 'id=', '&')
            print(tao_url)
            break
        else:
            print('loading')

    driver.close()
    print(item_id)

    exit()




    #print(items_con)
    for loadp in range(1, 50):


        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    items_con = soup.find('div', attrs={'class': 'basicList_list_basis__uNBZx'})
    items = items_con.find_all('img')

    for item in items:
        naver_img = getparse(str(item), 'shopping-phinf.pstatic.net', '?')
        #print(naver_img)
        if str(naver_img).find('main_') > 0:

            print(naver_img)



fun_item()