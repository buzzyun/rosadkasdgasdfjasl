import requests
import datetime
import random
import socket
import socks
import http.client
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup 
import pyperclip
import time
import socket
import os
import urllib
import chromedriver_autoinstaller
import subprocess
import threading
import sys
from dbCon import DBmodule_FR

global exchange_rate
exchange_rate = "1350"

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))
db_con = DBmodule_FR.Database('shop')

def getparse(target, findstr, laststr):
    result = ""
    if findstr:
        pos = target.find(findstr)
        if pos > -1:
            result = target[pos + len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        if lastpos > -1:
            result = result[:lastpos]
    else:
        result = result

    return result.strip()

#rfind 파싱함수
def getparseR(target, findstr, laststr):
    if findstr:
        pos = target.rfind(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result

def connectDriver(tool):
    if tool == 'chrome':
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        driver_path = f'./{chrome_ver}/chromedriver.exe'
        if os.path.exists(driver_path):
            print(f"chrom driver is insatlled: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver})")
            chromedriver_autoinstaller.install(True)
        time.sleep(1)
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 

        #크롤링 방지 설정을 undefined로 변경 
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

    if tool == 'chrome_secret':
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        driver_path = f'./{chrome_ver}/chromedriver.exe'
        if os.path.exists(driver_path):
            print(f"chrom driver is insatlled: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver})")
            chromedriver_autoinstaller.install(True)
        time.sleep(1)
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://www.1688.com//'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'brave':
        path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("window-size=1400x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=path, chrome_options=options)
    elif tool == 'Firefox':
        path = "C:\Project\cgeckodriver.exe"
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9150)
        profile.update_preferences()
        browser = webdriver.Firefox(profile, executable_path=path)
    return browser

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip :', response.read())

def checkIP2():
    print(" checkIP2 : ",socket.gethostbyname(socket.gethostname()))
    #print("IP Address(External) : ",socket.gethostbyname(socket.getfqdn()))

def set_new_ip():
    #print("set_new_ip()")
    # disable socks server and enabling again
    socks.setdefaultproxy()
    # """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)


def moveSlide(driver):
    print('slide proc')
    #//*[@id="nc_1_n1z"]
    slider = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    #slider = None
    if slider:
        move = ActionChains(driver)
        move.click_and_hold(slider).perform()
        driver.implicitly_wait(5)
        xval = 0
        try:
            move.move_by_offset(10, 1).perform()
            time.sleep(0.1)
            move.move_by_offset(20, 1).perform()
            move.move_by_offset(60, 1).perform()
            move.move_by_offset(80, 1).perform()
            move.move_by_offset(120, 1).perform()
            move.move_by_offset(180, 1).perform()
            move.move_by_offset(250, 1).perform()
            time.sleep(4)
            main_result = driver.page_source
            if str(main_result).find('Please refresh and try again') > -1:
                driver.find_element_by_xpath('//*[@id="`nc_1_refresh1`"]').click()
                time.sleep(1)
        except UnexpectedAlertPresentException:
            print("UnexpectedAlertPresentException")
        else:
            move.reset_actions()
            time.sleep(0.1)
        time.sleep(random.uniform(3,5))

def checkSlide(driver):
    driver.delete_all_cookies()
    flg = "1"
    count = 0
    main_result = driver.page_source
    if str(main_result).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network (SKIP) ")
        time.sleep(2)
        flg = "0"
        while flg == "0":
            count = count + 1
            driver.refresh()
            print('slide click : {}'.format(count))
            moveSlide(browser)
            time.sleep(random.uniform(4,5))
            main_result = driver.page_source
            if str(main_result).find('we have detected unusual traffic from your network.') > -1:
                print(">> detected unusual traffic from your network (SKIP) ")
                flg == "0"
            else:
                flg == "1"
                break
            if count > 5:
                flg == "E"
                break
    return flg

if __name__ == '__main__':
    print(">> start ")
    browser = connectDriver("chrome_secret")
    #path = "C:\\util\\chromedriver.exe"
    #browser = webdriver.Chrome(path)
    time.sleep(1) 
    browser.delete_all_cookies()
    
    time.sleep(2)     
    main_url = "https://detail.1688.com"
    print('>> main_url : ' + str(main_url))     
    browser.get(main_url)
    browser.set_window_size(1400, 1000)
    browser.implicitly_wait(3)
    time.sleep(2)
    ## 644058906392 --> 가격  00 ~ 00 
    ## 623946836990 --> 가격  00  |  00  |  00
    # asin_list = ['625245411405','670452319805','669931579641','644058906392','653365322787','625144776971','648374157153','623946836990']
    # random.shuffle(asin_list)
    
    ea_asin = ""
    error_cnt = 0
    sql = " select top 30 asin, cate_idx from T_Category_BestAsin "
    rows = db_con.select(sql)
    if rows:
        main_cnt = 0
        for row in rows:
            time.sleep(random.uniform(4,6))
            ea_asin = row[0]
            ea_cate_idx = row[1]
            main_cnt = main_cnt + 1
            print()
            print(">> ----------------------------------------------------------------------------------------")
            main_url = "https://detail.1688.com/offer/{}.html".format(ea_asin)
            print(">> [{}] {} | {}".format(main_cnt, ea_cate_idx, main_url))
            browser.get(main_url)

            time.sleep(random.uniform(5,7))
            main_result = ""
            main_result = browser.page_source

            soup_result = BeautifulSoup(main_result, 'html.parser')
            time.sleep(2)
            # with open("soup_result_1688" +str(ea_asin)+ ".html","w",encoding="utf8") as f: 
            #     f.write(str(soup_result))

            if str(main_result).find('we have detected unusual traffic from your network.') > -1:
                print(">> detected unusual traffic from your network (SKIP) ")
                time.sleep(2)
                rtnFlg = checkSlide(browser)
                if rtnFlg == "1":
                    main_result = browser.page_source
                    print(">> RE page_source Ok")
                    error_cnt = 0
                else:
                    print(">> Slide Error (SKIP) ")
                    time.sleep(3)
                    error_cnt = error_cnt + 1
                    if error_cnt > 5:
                        print(">> error_cnt 5 Over (Exit) ")
                        break
                    continue

            title = getparse(str(main_result),'class="title-text">','</div>')
            print(">> Title : {}".format(title))
            price_head = getparse(str(main_result),'class="price-header">','class="service-content"')
            # with open("soup_price_head_1688.html","w",encoding="utf8") as f: 
            #     f.write(str(price_head))

            if str(price_head).find('class="step-price-item"') > -1:
                print(">> price Select (step-price-item) [1] ")
            elif str(price_head).find('class="price-column"') > -1:
                print(">> price Select (price-column) [2] ")

            disPriceRanges = getparse(str(main_result),'disPriceRanges','skuMapOriginal')
            disPriceRanges = getparse(str(disPriceRanges),'[',']')
            spDisPrice = disPriceRanges.split('},{')
            pRow = 0
            for sItem in spDisPrice:
                pRow = pRow + 1
                beginAmount = getparse(str(sItem),'beginAmount\\":','').replace('}','')
                endAmount = getparse(str(sItem),'endAmount\\":',',').replace('}','')
                sprice = getparse(str(sItem),'price\\":\\"','\\",').replace('}','')
                if endAmount == "0" and int(beginAmount) > int(endAmount):
                    endAmount = int(beginAmount) * 10
                print(">> ({}) {} | {} | {} ".format(pRow, sprice, beginAmount, endAmount))


            price_tap = getparse(str(main_result),'class="od-pc-offer-price-contain"','class="od-pc-offer-discount-contain"')
            sp_price_tap = str(price_tap).split('<div class="price-box">')
            print(">> price_cnt : {}".format(len(sp_price_tap)-1))
            price_cnt = len(sp_price_tap)-1
            if str(main_result).find('<div class="step-price-wrapper"') > -1:
                print(">> price (3) 3개 setp price ")
            elif str(main_result).find('<span class="price-space">~') > -1 and price_cnt == 2:
                print(">> price (2) 2개 from~to ")
            elif str(main_result).find('<div class="price-content">') > -1 and price_cnt == 1:
                print(">> price (1) 1개 price ")
            else:
                print(">> price (4) Check price sytle")

            price = getparse(str(main_result),'class="price-text">','</span>')
            print(">> Price : {}".format(price))
            detail = getparse(str(main_result),'id="detailContentContainer">','<div class="price-info-module">')
            print(">> detail : {}".format(detail[:50]))
            # with open("soup_detail_1688.html","w",encoding="utf8") as f: 
            #     f.write(str(detail))

            skuModel = getparse(str(main_result),"skuModel","skuInfoMap")
            skuInfoMap = getparse(str(main_result),"skuInfoMap","skuInfoMapOriginal")
            # with open("soup_skuInfoMap_1688.html","w",encoding="utf8") as f: 
            #     f.write(str(skuInfoMap))

            sp_skuInfoMap = skuInfoMap.split('"specId"')
            for ea_sku in sp_skuInfoMap:
                item_value = getparse(str(ea_sku), '"specAttrs":"', '"').replace('&gt;',' & ')
                if item_value == "":
                    continue
                item_saleCount = getparse(str(ea_sku), '"saleCount":', ',')
                item_canBookCount = getparse(str(ea_sku), '"canBookCount":', ',')
                item_discountPrice = getparse(str(ea_sku), '"discountPrice":', ',')
                if item_discountPrice == "":
                    item_discountPrice = price
                item_skuId = getparse(str(ea_sku), '"skuId":', ',')
                if item_canBookCount == "0":
                    print(">> ({}) {} | {} 위안 | {} [품절] ".format(item_skuId, item_value, item_discountPrice, item_canBookCount, item_saleCount))
                else:
                    print(">> ({}) {} | {} 위안 | {}".format(item_skuId, item_value, item_discountPrice, item_canBookCount, item_saleCount))

            skuInfoMapOriginal = getparse(str(main_result),"skuInfoMapOriginal","offerBaseInfo")
            #print(">> skuInfoMapOriginal : {}".format(skuInfoMapOriginal))

            if str(main_result).find('class="detail-gallery-img"') > -1:
                img_sorce = getparse(str(main_result),'class="detail-gallery-img"','class="layout-right"')
                sp_img = str(img_sorce).split('class="detail-gallery-img"')
                for ea_img_item in sp_img:
                    ea_img = getparse(str(ea_img_item),'src="','"')
                    print(">> ea_img : {}".format(ea_img))

            sql_d = "delete from T_Category_BestAsin where asin = '{}'".format(ea_asin)
            print(">> Delete Asin : {}".format(ea_asin))
            db_con.execute(sql_d)

        input(">> Input : ")
