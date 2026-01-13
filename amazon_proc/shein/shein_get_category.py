from selenium import webdriver

import chromedriver_autoinstaller
import DBmodule_NEW
import requests
import json
from operator import itemgetter
import re
import traceback
import get_asin_function
import socket
import random
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess

def chrom_drive():
    try:
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(service=f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(5) 
    driver.set_page_load_timeout(3600)
    return driver 

def chrom_click(selector, driver):
    driver.find_element_by_css_selector(selector).click()
    time.sleep(1)
    

def getCccNavData(html):
    start_index = html.find("window.cccNavData")
    end_index = html.find("</script>",start_index)
    json_data = json.loads(html[start_index+20:end_index])
    
    return json_data

def cateNameFilter(catename):
    if catename.lower().find("sale") > -1 or catename.find("세일") > -1 or catename.find("브랜드") > -1 or catename.lower().find("explore") > -1 or catename.lower().find("new in") > -1 or catename.lower().find("신상") > -1 or catename.lower().find("#SHEINss23") > -1 or catename.lower().find("트렌드") > -1:
        return False
    else:
        return True


db_con = DBmodule_NEW.Database('trend')
driver = chrom_drive()
driver.get("https://asia.shein.com/")
html = driver.page_source

json_data = getCccNavData(html)
sort = 0

for json_item in json_data:
    sort = sort+1
    dic = dict()
    cate_name = json_item["name"]
    if cate_name.find("신상품") > -1 or cate_name.find("세일") > -1:
        continue
    cate_en_name = json_item["enName"]
    cate_code = json_item["hrefTarget"]
    relativeUrl = json_item["firstFloorContent"]["props"]["metaData"]["categoryType"]["relativeUrl"]
    cate_url = "https://asia.shein.com"+relativeUrl
    dic["siteID"]="'rental'"
    dic["isHidden"]="'F'"
    dic["IsDisplayMain"]="'F'"
    dic["SubmainPos"]=0
    dic["Cms"]=0
    dic["CmsGonggu"]=0
    dic["CmsAuction"]=0
    dic["RegDate"]="GETDATE()"
    dic["list_in"]=0
    dic["up_date"]="GETDATE()"
    dic["name"]="'"+cate_en_name+"'"
    dic["kor_name"]="'"+cate_name+"'"
    dic["depth"]=1
    dic["sort"]=sort
    dic["parent"]=0
    dic["amz_cateurl"]="'"+cate_url+"'"
    dic["cate_code2"]="'"+cate_code+"'"
    db_con.insert("t_category", dic)
    print("{} insert OK".format(cate_name))
db_con.commit()
db_con.close()
