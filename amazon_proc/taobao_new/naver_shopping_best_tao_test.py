
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
    try:
        proc_id, browser = connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    naver_url = "https://search.shopping.naver.com/search/category/100011132?adQuery&catId=50000807&origQuery&pagingIndex=1&pagingSize=106&productSet=overseas&query&sort=rel&spec=M10013382%7CM10731145%20M10012485%7CM10032139%20M10012485%7CM10588283%20M10012485%7CM10669979%20M10012485%7CM10574793&timestamp=&viewType=list"
    naver_url2 = "https://shopping-phinf.pstatic.net/main_8850774/88507744596.jpg"

    # wait = WebDriverWait(browser, 10)
    # browser.implicitly_wait(10)  # seconds
    # # driver.get(naver_url2)
    # browser.get(naver_url)
    # time.sleep(3)
    # result = browser.page_source

    wait = WebDriverWait(browser, 10)
    browser.implicitly_wait(10)  # seconds
    # driver.get(naver_url2)
    browser.get(naver_url)
    time.sleep(random.uniform(3,5))
    moveScroll(browser, 5)

    result = browser.page_source
    dic_imgs = dict()
    ## browser.find_elements(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div[1]/div')[1]
    ## browser.find_elements(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div[1]/div')[1].find_element(By.XPATH,'div/div/div').get_attribute('innerHTML')
        
    required_images = browser.find_elements(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div[1]/div')
    for ea_img in required_images:
        text_html = ea_img.get_attribute('innerHTML')
        # print(">> text_html : {}".format(text_html))

        goods_url = getparse(text_html,'href="','"').replace('amp;', '').strip()
        img_url = getparse(text_html,'src="','"').replace('http://', 'https://').strip()
        if img_url.find("?") > -1: img_url = getparse(img_url,'','?')
        data_contents_id = getparse(text_html,'data-i="','"').strip()
        data_provider_id = getparse(text_html,'data-ms="','"').strip()
        data_title = getparse(text_html,'data-shp-contents-dtl','}')
        data_title = getparse(data_title,'value&quot;:&quot;','').replace('&quot;', '').strip()
        print(">> img_url : {} | goods_url : {}".format(img_url, goods_url))
        print(">> data_contents_id : {} | data_provider_id : {} | data_title : {}".format(data_contents_id, data_provider_id, data_title))

        if str(text_html).find('detail.tmall.com') > 0:
            print(">> detail.tmall.com (0) ")
        elif str(text_html).find('item.taobao.com') > 0:
            print(">> item.taobao.com (0) ")
        else:
            print(">> No src (0) ")

        dic_imgs[str(data_contents_id)] = img_url
        # browser.get(img_url)
        # time.sleep(random.uniform(3,5))
        # result_img = browser.page_source
        # #print(">> result_img : {}".format(result_img))

        # print(">> result_img ... ")
        # if str(result_img).find('detail.tmall.com') > 0:
        #     print(">> detail.tmall.com (1) ")
        # elif str(result_img).find('item.taobao.com') > 0:
        #     print(">> item.taobao.com (1) ")
        # else:
        #     print(">> No src (1) ")

        print(">> ")




    # dic_imgs = dict()
    # img_list = getparse(result,'class="basicList_list_basis__','class="searchList_notice__')
    # sp_imgs = img_list.split('product_img_area__')
    # print(">> sp_imgs : {}".format(sp_imgs))
    # for ea_img in sp_imgs:
    #     goods_url = getparse(ea_img,'href="','"').replace('amp;', '').strip()
    #     img_url = getparse(ea_img,'src="','"').replace('http://', 'https://').strip()
    #     if img_url.find("?") > -1: img_url = getparse(ea_img,'','?')
        
    #     data_contents_id = getparse(ea_img,'data-i="','"').strip()
    #     data_provider_id = getparse(ea_img,'data-ms="','"').strip()
    #     data_title = getparse(ea_img,'data-shp-contents-dtl','}')
    #     data_title = getparse(data_title,'value&quot;:&quot;','').replace('&quot;', '').strip()
    #     print(">> img_url : {} | goods_url : {}".format(img_url, goods_url))
    #     print(">> data_contents_id : {} | data_provider_id : {} | data_title : {}".format(data_contents_id, data_provider_id, data_title))

    #     dic_imgs[str(data_contents_id)] = img_url



    print(">> ")