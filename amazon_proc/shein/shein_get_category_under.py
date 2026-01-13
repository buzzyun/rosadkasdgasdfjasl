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
def getgbRawDate(html):
    first_wort = "var gbRawData = "
    start_index = html.find(first_wort)
    end_index = html.find("document.dispatchEvent",start_index)
    json_data = json.loads(html[start_index+len(first_wort):end_index])
    
    return json_data
def getCateInfo(json_data,depth,sort,parent,url,lastcate,big=True,bcate=True,middle=True,mcate=True,small=True,scate=True,little=True,dcate=True,last=True,ecate=True):
    dic = dict()
    code = json_data["cat_id"]
    name = json_data["cat_name"]
    name = "'"+name.replace("&nbsp","")+"'"
    amz_cateurl = url+"?child_cat_id="+code
    dic["siteID"]="'rental'"
    dic["isHidden"]="'F'"
    dic["IsDisplayMain"]="'F'"
    dic["SubmainPos"]=0
    dic["Cms"]=0
    dic["CmsGonggu"]=0
    dic["CmsAuction"]=0
    dic["RegDate"]="GETDATE()"
    dic["lastcate"]=lastcate
    dic["list_in"]=0
    dic["up_date"]="GETDATE()"
    dic["name"]=name
    dic["kor_name"]=name
    dic["depth"]=depth
    dic["sort"]=sort
    dic["parent"]=parent
    dic["amz_cateurl"]="'"+amz_cateurl+"'"
    dic["cate_code2"]="'"+code+"'"
    if depth==2:
        dic["bcate"]=bcate
        dic["big"]=big
        dic["middle"]=name     
    if depth==3:
        dic["bcate"]=bcate
        dic["big"]=big
        dic["mcate"]=mcate
        dic["middle"]=middle
        dic["small"]=name
    elif depth==4:
        dic["bcate"]=bcate
        dic["big"]=big
        dic["mcate"]=mcate
        dic["middle"]=middle
        dic["scate"]=scate
        dic["small"]=small
        dic["little"]=name
    elif depth==5:
        dic["bcate"]=bcate
        dic["big"]=big
        dic["mcate"]=mcate
        dic["middle"]=middle
        dic["scate"]=scate
        dic["small"]=small
        dic["dcate"]=dcate
        dic["little"]=little
        dic["last"]=name
    elif depth==6:
        dic["bcate"]=bcate
        dic["big"]=big
        dic["mcate"]=mcate
        dic["middle"]=middle
        dic["scate"]=scate
        dic["small"]=small
        dic["dcate"]=dcate
        dic["little"]=little
        dic["ecate"]=ecate
        dic["last"]=last
        dic["final"]=name
        
    return dic

db_con = DBmodule_NEW.Database('trend')
driver = chrom_drive()
sql = "select CateCode, name, kor_name, amz_cateurl from t_category where depth=1 and RegDate >= '2024-03-20' and RegDate < '2024-03-21'"

rs = db_con.select(sql)
for row in rs:
    CateCode = row[0]
    name = row[1]
    kor_name = row[2]
    amz_cateurl = row[3]
    
    big = "'"+kor_name+"'"
    bcate = CateCode
    driver.get(amz_cateurl)
    html = driver.page_source
    
    json_data = getgbRawDate(html)
    depth2 = json_data["results"]["filterCates"]["children"]
    sort_depth2 = 0
    for depth2_item in depth2: #depth2 insert
        if "children" in depth2_item.keys():
            lastcate = 0
        else:
            lastcate = 1
        sort_depth2 =+ 1
        dic_depth2 = getCateInfo(depth2_item,2,sort_depth2,bcate,amz_cateurl,lastcate,big,bcate)
        middle = dic_depth2["middle"]
        mcate = db_con.insertReturnIdx("t_category", dic_depth2) 
        
        if lastcate == 0:
            depth3 = depth2_item["children"]
            sort_depth3 = 0
            for depth3_item in depth3: #depth3 insert
                if "children" in depth3_item.keys():
                    lastcate = 0
                else:
                    lastcate = 1
                sort_depth3 =+ 1
                dic_depth3 = getCateInfo(depth3_item,3,sort_depth3,bcate,amz_cateurl,lastcate,big,bcate,middle,mcate)
                small = dic_depth3["small"]
                scate = db_con.insertReturnIdx("t_category", dic_depth3)
                
                if lastcate == 0:
                    depth4 = depth3_item["children"]
                    sort_depth4 = 0
                    for depth4_item in depth4: #depth4 insert
                        if "children" in depth4_item.keys():
                            lastcate = 0
                        else:
                            lastcate = 1
                        sort_depth4 =+ 1
                        dic_depth4 = getCateInfo(depth4_item,4,sort_depth4,bcate,amz_cateurl,lastcate,big,bcate,middle,mcate,small,scate)
                        little = dic_depth4["little"]
                        dcate = db_con.insertReturnIdx("t_category", dic_depth4)
    
                        if lastcate == 0:
                            depth5 = depth4_item["children"]
                            sort_depth5 = 0
                            for depth5_item in depth5: #depth5 insert
                                if "children" in depth5_item.keys():
                                    lastcate = 0
                                else:
                                    lastcate = 1
                                sort_depth5 =+ 1
                                dic_depth5 = getCateInfo(depth5_item,5,sort_depth5,bcate,amz_cateurl,lastcate,big,bcate,middle,mcate,small,scate,little,dcate)
                                last = dic_depth5["last"]
                                ecate = db_con.insertReturnIdx("t_category", dic_depth5)
                                
                                if lastcate == 0:
                                    depth6 = depth5_item["children"]
                                    sort_depth6 = 0
                                    for depth6_item in depth6: #depth6 insert
                                        if "children" in depth6_item.keys():
                                            lastcate = 0
                                            input("depth6 이상 더 있음")
                                        else:
                                            lastcate = 1
                                        sort_depth6 =+ 1
                                        dic_depth6 = getCateInfo(depth6_item,6,sort_depth6,bcate,amz_cateurl,lastcate,big,bcate,middle,mcate,small,scate,little,dcate,last,ecate)
                                        fcate = db_con.insertReturnIdx("t_category", dic_depth6)
    db_con.commit()

db_con.close()


