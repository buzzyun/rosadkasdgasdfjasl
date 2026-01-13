import os
os.system('pip install --upgrade selenium')
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
from selenium.webdriver.chrome.options import Options
import subprocess
import os
import util_func

def connectSubProcess():
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    option.add_argument("--hide-console")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=Service(executable_path='C:\\project\\chromedriver.exe'),options=option)

    return driver 

def connectSubProcess2():    
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'

    proc = ""
    try:
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
        print(">> C:\Program Files (x86)\Google\Chrome ")
    except FileNotFoundError:
        print(">> C:\Program Files\Google\Chrome ")
        proc = subprocess.Popen(filePath)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(options=option)

    return proc, browser
def changeLang(driver):
    print("한국어로 변경")
    time.sleep(1)
    try:
        chrom_click("i[class='iconfont icon-close she-close']", driver)
    except:
        print("팝업 없음")
    chrom_click("i[class='sh_pc_sui_icon_nav_global_24px_shein']", driver)
    chrom_click("a[data-lang='asiako']", driver) 
    
def chrom_click(selector, driver):
    try:
        driver.find_element(By.CSS_SELECTOR,selector).click()
    except:
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,selector))
    time.sleep(1)

def getPrdData(html):
    start_index = html.find('"productIntroData":{')
    end_index = html.find(',"defaultMallCode"',start_index)
    html = html[start_index+19:end_index].strip()
    json_data = json.loads(html)
    
    return json_data

def getReviewData(html):
    start_index = html.find('<pre>')
    end_index = html.find('</pre>',start_index)
    html = html[start_index+5:end_index].strip()
    json_data = json.loads(html)
    
    return json_data

limit = 20
product_url = "https://asia.shein.com/item-p-{}.html"
review_url = "https://asia.shein.com/api/comment/abcCommentInfo/query?_ver=1.1.8&_lang=ko&spu={}&goods_id=&page=1&limit="+str(limit)+"&offset=3&sort=&size=&is_picture=&rule_id=recsrch_sort:A&tag_id=&local_site_abt_flag=&shop_id=&query_rank=0&same_query_flag=1&not_need_img=1"
db_con = DBmodule_NEW.Database("trend")


proc,driver = connectSubProcess2()
try:
    while True:
        sql = "select top 1 ali_no, uid from t_goods where uid not in (select GoodsUid from t_goods_review) and isDisplay='T' and isSoldOut='F' order by uid"
        rs = db_con.selectone(sql)
        if rs:
            dic = dict()
            uid = rs[1]
            ali_no = rs[0]
            dic["GoodsUid"] = uid
            driver.get(product_url.format(ali_no))
            html = driver.page_source
            json_data = getPrdData(html)
            try:
                spu = json_data["commentInfo"]["spu"]
            except:
                # review_chk, 1: 리뷰 있음, 0: 리뷰 없음
                dic["review_chk"] = 0
                db_con.insert("t_goods_review", dic)
                db_con.commit()
                print("GoodsUid : {} 리뷰 없음".format(uid))
                continue
            driver.get(review_url.format(spu))
            now_url = driver.current_url
            if now_url.find("/risk/") > -1:
                input("캡챠 확인")
            html = driver.page_source
            json_data = getReviewData(html)
            review_data = json_data["info"]["commentInfo"]
            
            review_list = []
            for review in review_data:
                review_dic = dict()
                review_img_list = []
                review_dic["content"] = review["content"]
                review_dic["comment_rank"] = review["comment_rank"]
                if "goods_attr_list" in review:
                    review_dic["option"] = review["goods_attr_list"]
                else:
                    review_dic["option"] = review["color"]
                for review_img in review["comment_image"]:
                    review_img_list.append(review_img["member_image_original"])
                review_dic["review_img_list"] = review_img_list
                
                review_list.append(review_dic)
                    

            review_data = str(review_list).replace("'", '"').replace("\n","")
            dic["review_chk"] = 1
            dic["review_json"] = "N'"+review_data+"'"
            db_con.insert("t_goods_review", dic)
            print("GoodsUid : {} 리뷰 입력 완료".format(uid))
            db_con.commit()
            break
        else:
            print("작업 완료")
            break
except Exception as ex:
    print(ex)
    traceback.print_exc()


db_con.close()
driver.quit()