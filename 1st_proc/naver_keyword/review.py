# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:58:45 2022

@author: allin
"""
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, subprocess, socket
import requests
import json, random
from pymssql import _mssql
from pymssql import _pymssql
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import func_user
import DBmodule_FR


def chrom_click(selector, driver):
    driver.find_element(By.CSS_SELECTOR,selector).click()
    time.sleep(1)
    
def chrom_write(selector, driver, write):  
    driver.find_element(By.CSS_SELECTOR,selector).send_keys(write)    
    time.sleep(1)


def connectSubProcess():
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

def screen_check(driver):
    time.sleep(1)
    try:
        main = driver.window_handles
        print(">> Browser Count : {}".format(len(main)))
        last_tab = driver.window_handles[len(main) - 1]
        if str(len(main)) != "1":
            for handle in main:
                if handle != last_tab:
                    driver.switch_to.window(window_name=last_tab)
                    driver.close()
                    driver.switch_to.window(window_name=handle)
            print(">> Browser Close : {}".format(len(driver.window_handles)))

    except Exception as e:
        print('>> Popup Close Exception ')

    time.sleep(0.5)

def elem_clear(elem):
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)

if __name__ == '__main__':

    print(">> 네이버 리뷰 가져오기 (review) ")
    db_con = DBmodule_FR.Database('naver_price')

    now_url = 'https://admin.pay.naver.com'
    # driver = func_user.connectDriverNew('https://admin.pay.naver.com','')
    try:
        print(">> connectDriverNew set ")
        driver = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        driver = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    driver.set_window_size(1400, 1000)

    print('connectDriver 연결 OK')
    driver.implicitly_wait(3)
    #now_url = "https://nid.naver.com/nidlogin.login?url=https://admin.pay.naver.com/nid/check"
    now_url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fadmin.pay.naver.com%2Fnid%2Fcheck&locale=ko_KR&svctype=1"
    driver.get(now_url)
    time.sleep(2)

    currIp = socket.gethostbyname(socket.gethostname())
    print('>> currIp : '+str(currIp))
    loginId = 'kbw4798'
    loginPw = 'bw007583@1011'

    elem11 = driver.find_element(By.XPATH,'//*[@id="id"]')
    elem_clear(elem11)
    elem11.send_keys(loginId)
    time.sleep(0.5)
    elem22 = driver.find_element(By.XPATH,'//*[@id="pw"]')
    elem_clear(elem22)
    elem22.send_keys(loginPw)
    time.sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="log.login"]').click()
    time.sleep(2)

    if str(driver.current_url).find('managementlist') > -1:
        print(">> 가맹점정보 선택하기 ")
        time.sleep(1)
        chkBtn = driver.find_element(By.CSS_SELECTOR, "#store_item_freeship > label > span.name_area")
        if chkBtn:
            chkBtn.click()
            driver.find_element(By.CSS_SELECTOR,"#btnConfirm").click()
            time.sleep(3)

    if str(driver.current_url).find('admin.pay.naver.com/home') > -1:
        print(">> 로그인 OK ")
        time.sleep(1)
    else:
        print(">> 로그인 불가 ")
        input(">> 로그인 처리후 (네이버페이센터홈) 아무키나 눌러주세요 :")
        time.sleep(2)

    if str(driver.current_url).find('admin.pay.naver.com/home') == -1:
        print(">> 로그인 불가 exit ")
        time.sleep(2)
        driver.quit()
        os._exit(1)

    # 팝업 공지 확인후 닫기
    screen_check(driver)
    time.sleep(5)
    # 팝업 공지 확인후 닫기
    screen_check(driver)

    time.sleep(1)

    now = datetime.now()
    print(">> 현재 :", now)	# 현재 : 2021-01-09 21:51:33.170644

    driver.get("https://admin.pay.naver.com/o/reviewManage")

    diff = timedelta(days=2)
    yesterday = now - diff
    yesterday = yesterday.strftime("%Y.%m.%d")
    print(">> diff( {} ) yesterday : {}".format(diff, yesterday))
    sDate = yesterday
    eDate = yesterday

    url = "https://admin.pay.naver.com/o/reviewManage/json?range.fromDate={}&range.toDate={}&detailSearch.type=&detailSearch.keyword=&reviewType=&reviewContentClassType=&reviewScore=&paging.current=1&paging.rowsPerPage=500".format(sDate,eDate)
    print(url)
    driver.get("https://admin.pay.naver.com/o/reviewManage/json?range.fromDate={}&range.toDate={}&detailSearch.type=&detailSearch.keyword=&reviewType=&reviewContentClassType=&reviewScore=&paging.current=1&paging.rowsPerPage=500".format(sDate,eDate))

    p_source = driver.page_source
    p_source = p_source.replace("</body></html>","")
    p_source = p_source.replace("<html><head></head><body>","")

    # p_source = input("소스 집어넣기")
    json_data = json.loads(p_source)

    review_url = "https://order.pay.naver.com/review/"

    # "REVIEW_CONTENT_DISPLAY_STATUS": "BLIND" : 제외된 리뷰 - 제거 처리
    totalElements = json_data["htReturnValue"]["pagedResult"]["totalElements"]
    print("리뷰 총 {}개".format(totalElements))
    for item in json_data["htReturnValue"]["pagedResult"]["content"]:
        review_media = ""
        status = item["REVIEW_CONTENT_DISPLAY_STATUS"] == "BLIND"

        review_id = item["REVIEW_CONTENT_ID"]
        product_id = item["REVIEW_CONTENT_PRODUCT_NO"]
        product_title = item["REVIEW_CONTENT_PRODUCT_NAME"]
        review_chk = item["REVIEW_CONTENT_TYPE"]
        order_id = item["REVIEW_CONTENT_PRODUCT_ORDER_ID"]
        detail_chk = item["REVIEW_CONTENT_CLASS_TYPE"]
        score = item["REVIEW_CONTENT_SCORE"]
        review_content = item["REVIEW_CONTENT_CONTENT"]
        writer = item["REVIEW_CONTENT_WRITER_MEMBER_ID"]
        reviewdate = item["REVIEW_CONTENT_CREATE_YMDT"]
            
        res = requests.get(review_url+str(review_id))
        soup = BeautifulSoup(res.text, "html.parser")    
        try:
            element = soup.select_one(".option")
            product_option = element.text
            if product_option == "":
                product_option = "NULL"
        except:
            product_option = "NULL"
            
        try:
            element = soup.select_one(".word")
            review_content = element.text
        except:
            review_content = ""  
            
        try:
            element = soup.select(".photo")
            for i in element:
                if review_media == "":
                    review_media = i["src"]
                else:
                    review_media = review_media + "," + i["src"]
        except:
            review_media = ""        
        
        # review_chk : AFTER_USE = 한달리뷰  NORMAL = 상품리뷰
        # detail_chk : TEXT = 텍스트  PHOTO = 포토
        
        if product_id.find("_") > -1:
            str_pos = product_id.find("_")
            product_id = product_id[:str_pos]
        if product_id.find(",") > -1:
            str_pos = product_id.find(",")
            product_id = product_id[:str_pos]
            
        if review_chk == "AFTER_USE":
            review_chk = "한달리뷰"
        elif review_chk == "NORMAL":
            review_chk = "상품리뷰"
        
        if detail_chk == "TEXT":
            detail_chk = "텍스트"
        elif detail_chk == "PHOTO":
            detail_chk = "포토"
            
        score = score.replace("POINT","")
        
        review_content = review_content.replace("'","")
        
        regdate = datetime.fromtimestamp(reviewdate / 1e3).strftime("%Y-%m-%d %H:%M:%S")
        
        if status == "BLIND":
            if product_option == "NULL":
                sql = "insert into review (review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate, blind) values({}, N'{}', N'{}', {}, N'{}', N'{}', N'{}', N'{}', {}, N'{}', N'{}', '{}', '1')".format(review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate)
            else:
                sql = "insert into review (review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate, blind) values({}, N'{}', N'{}', '{}', N'{}', N'{}', N'{}', N'{}', {}, N'{}', N'{}', '{}', '1')".format(review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate)
        else:
            if product_option == "NULL":
                sql = "insert into review (review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate) values({}, N'{}', N'{}', {}, N'{}', N'{}', N'{}', N'{}', {}, N'{}', N'{}', '{}')".format(review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate)
            else:
                sql = "insert into review (review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate) values({}, N'{}', N'{}', '{}', N'{}', N'{}', N'{}', N'{}', {}, N'{}', N'{}', '{}')".format(review_id, product_id, product_title, product_option, order_id, review_chk, detail_chk, review_media, score, review_content, writer, regdate)
        
        print("======================================")
        # print("review_id : ",review_id)
        # print("product_id : ",product_id)
        # print("product_title : ",product_title)
        # print("product_option : ",product_option)
        # print("order_id : ",order_id)
        # print("review_chk : ",review_chk)
        # print("detail_chk : ",detail_chk)
        # print("review_media : ",review_media)
        # print("score : ",score)
        # print("review_content : ",review_content)
        # print("writer : ",writer)
        # print("regdate : ",regdate)
        print(sql)
        db_con.execute(sql)
        print("DB입력 완료")
        print("======================================")

    db_con.close()
    print("작업 끝")
    driver.quit()
    os._exit(0)


