
import os
os.system('pip install --upgrade selenium')
import time
import datetime
import random
import socket
import urllib
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import subprocess
import uuid
import taobao_func
import DBmodule_FR

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

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
    proc = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)
    return proc, browser

def moveScroll(driver, max_scroll_cnt):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 1000
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(random.uniform(1,3))
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > max_scroll_cnt:
            break
        last_height = new_height

if __name__ == '__main__':

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    currIp = socket.gethostbyname(socket.gethostname())
    proc_id = ""
    # try:
    #     proc_id, browser = connectSubProcess()
    # except Exception as e:
    #     print(">> connectSubProcess Exception ")

    naver_url = "https://search.shopping.naver.com/search/category/100011132?adQuery&catId=50000807&origQuery&pagingIndex=1&pagingSize=106&productSet=overseas&query&sort=rel&spec=M10013382%7CM10731145%20M10012485%7CM10032139%20M10012485%7CM10588283%20M10012485%7CM10669979%20M10012485%7CM10574793&timestamp=&viewType=list"
    naver_url2 = "https://shopping-phinf.pstatic.net/main_8850774/88507744596.jpg"

    option = Options()
    #option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    option.page_load_strategy = 'eager' # 옵션에 지정함으로써 전체 사이트 다 뜰때까지 로딩을 기다릴 필요가 없어집니다.
    # option.add_argument("--blink-settings=imagesEnabled=false") # 셀레니움 드라이브옵션에 이미지를 안불러 오도록 설정하면 속도 향상에 도음이 됩니다.

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)
    #wait = WebDriverWait(browser, 10)
    #browser.implicitly_wait(10)  # seconds
    
    naver_url3 = "https://search.shopping.naver.com/search/category/100011379"
    browser.get(naver_url3)


    #필요한 부분까지의 로딩을 
    while 1:
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        if str(soup).find('title--text--Otu0bLr') > 0:
            print(">> title--text--Otu0bLr")

        if str(soup).find('detail.tmall.com') > 0:
            print(">> detail.tmall.com (0) ")
        elif str(soup).find('item.taobao.com') > 0:
            print(">> item.taobao.com (0) ")
        elif str(soup).find('AliExpress') > 0:
            print(">> item.taobao.com (0) ")
        else:
            print(">> No src (0) ")

        if str(html).find('detail.tmall.com') > 0:
            print(">> html detail.tmall.com (0) ")
        elif str(html).find('item.taobao.com') > 0:
            print(">> html item.taobao.com (0) ")
        elif str(html).find('AliExpress') > 0:
            print(">> html item.taobao.com (0) ")
        else:
            print(">> html No src (0) ")

    print(">> ")
    input(">>")