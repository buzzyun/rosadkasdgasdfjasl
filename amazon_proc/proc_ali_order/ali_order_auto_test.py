# library to launch and kill Tor process
import random
# library for Tor connection
import socket
import socks
import http.client
# library for scraping
import urllib
from urllib.request import Request, urlopen
from multiprocessing import Pool,freeze_support,Manager,Process
import pyodbc
from stem import Signal
from stem.control import Controller
import time
import lxml
import requests
import threading
import sys
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from io import BytesIO
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import os
#from phpserialize import serialize, unserialize
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import datetime

global st_now
global fileName
st_now = datetime.datetime.now()
#fileName = "C:/python_log/python_log_" + str(str(st_now)[:10] + "_" + str(st_now)[11:-7].replace(":","")) + ".txt"
fileName = "C:/python_log/python_log_" + str(str(st_now)[:10] + "_" + str(st_now)[11:-7].replace(":","")) + ".txt"
print('\n global fileName: ' +str(fileName))


# DB연결
def connectDB(server, database, username, password):
    print('\n [--- connectDB ---]')
    con = pyodbc.connect(
        'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server, database, username, password),
        autocommit=True)
    return con


def closeDB(db):
    print('\n [--- closeDB ---]')
    db.close()

# DB
server = '59.23.231.194,14103'
database = 'freeship'
username = 'sa'
password = '@allin#am1071'
con = connectDB(server, database, username, password)
db = con.cursor()
db2 = con.cursor()

global exchangeRate
exchangeRate = 1350

def checkIP():
	conn = http.client.HTTPConnection("icanhazip.com")
	conn.request("GET", "/")
	time.sleep(3)
	response = conn.getresponse()
	print('current ip address :', response.read())


# 파싱 함수
def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos + len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result.strip()


#영문 이름 변환
def getEngName(rcvKname):
    name_item = rcvKname
    qName = urllib.parse.quote_plus(name_item)
    linkSite = 'https://s.search.naver.com/n/name.krdic/translation/?_callback=window.__jindo2_callback._2069&query=' + qName + '&where=name&output=json&charset=euc-k'
    webpage = requests.get(linkSite)
    soupNm = BeautifulSoup(webpage.content, "html.parser")
    resultStr = soupNm.text
    #print('\n resultStr:' + str(resultStr))
    eng_name = ""

    if resultStr != "":
        if resultStr.find('"name":') > 0:
            en_name_item = resultStr.split('"name":')
            eng_name = getparse(en_name_item[1],'"','"')
            print('\n eng_name (1):' + str(eng_name))
            if eng_name[:4] == "Gim ":
                eng_name = eng_name[:4].replace('Gim ','Kim ') + eng_name[4:]
                print('\n eng_name (2):' + eng_name)
            if eng_name[:2] == "I ":
                eng_name = eng_name[:2].replace('I ','Lee ') + eng_name[2:]
                print('\n eng_name (2):' + eng_name)
        else:
            print('\n 영문 변역 불가한 이름 :' + str(rcvKname))

    return eng_name

#영문 주소 변환
def getEngJuso(rcvJuso, rcvPost):
    find_juso = ""

    rcvJuso = rcvJuso.replace(" ", "").strip()
    qJuso = urllib.parse.quote_plus(rcvJuso)
    qStr = urllib.parse.quote_plus("영문주소")

    linkSite2 = 'http://csearch.naver.com/content/eprender.nhn?where=nexearch&pkid=252&q=' + qJuso + '%20' + qStr + '&key=address_eng'
    print('\n linkSite2:' + str(linkSite2))

    req2 = Request(linkSite2)
    connection2 = urlopen(req2)
    soupNm2 = BeautifulSoup(connection2, "html.parser")

    addr_items = ""
    addr_items = str(soupNm2).split("<strong>")

    for addr_ea in addr_items:
        zip_str = getparse(addr_ea, '<td class="tc">','</td>')

        if rcvPost == zip_str:
            find_juso = getparse(addr_ea,'','</strong>')
            find_zip = zip_str
            print('\n 영문주소 : ' + str(find_juso))
            break

    return find_juso


#주소 앞 한단어 자르기
def getWordCut(orgName_item):
    name_item_word = ""
    indexNo = orgName_item.find(" ")

    # 주소 앞 한단어 자르기 (1)
    name_item_word = orgName_item[indexNo:].strip()

    if name_item_word.find("(") > 0:
        f_fos = name_item_word.find("(")
        name_item_word = name_item_word[:f_fos].strip()

    return name_item_word


#영문 주소변환
def chgEngJusoProc(strJuso, strJuso2, strPost):
    engNameJuso = ""

    post_val = strPost.replace("-", "")
    check_front_number = strJuso[-1:]
    check_bottom_number = strJuso2[:1]

    if check_front_number.isnumeric() and check_bottom_number.isnumeric():
        name_item = strJuso
    elif check_front_number.isnumeric() and not check_bottom_number.isnumeric():
        name_item = strJuso
    else:
        name_item = strJuso + " " + strJuso2
    print('\n 변환할 주소 : ' + str(name_item))

    name_item_org = ""
    # 주소앞 한단어 자르기[1]
    name_item_val = getWordCut(name_item)
    name_item_org = name_item_val
    engNameJuso = getEngJuso(name_item_val, post_val)

    if engNameJuso == "":
        # 주소앞 한단어 자르기[2]
        name_item_val = getWordCut(name_item_org)
        name_item_org = ""
        name_item_org = name_item_val
        engNameJuso = getEngJuso(name_item_val, post_val)

        if engNameJuso == "":
            # 주소앞 한단어 자르기[3]
            name_item_val = getWordCut(name_item_org)
            name_item_org = ""
            name_item_org = name_item_val

            engNameJuso = getEngJuso(name_item_val, post_val)

            if engNameJuso == "":
                # 주소앞 한단어 자르기[4]
                name_item_val = name_item_val.replace(" ", "").strip()
                engNameJuso = getEngJuso(name_item_val, post_val)

                if engNameJuso == "":
                    print('\n 주소변환불가 : ', str(name_item_val))

    return engNameJuso


def login_Proc(in_driver):
    print('\n [--- login_Proc ---]')
    wait = WebDriverWait(in_driver, 20)

    #로그인 ID/PASS 입력
    in_driver.find_element_by_name('fm-login-id').send_keys('koiforever0526@gmail.com')
    in_driver.find_element_by_name('fm-login-password').send_keys('uiop7890')

    # 로그인 버튼 클릭
    #alogin = WebDriverWait(in_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fm-btn")))
    alogin = WebDriverWait(in_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.fm-button")))
    alogin.click()

    return "0"

def chk_CouponPop(in_driver):
    print('\n [--- chk_CouponPop ---]')

    chkFlag = "0"

    try:
        wait = WebDriverWait(in_driver, 10)
        # 쿠폰 팝업창 1
        aPopClose = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.close-layer")))
        #aPopClose = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.close-layer")))
        aPopClose.click()

    except NoSuchElementException:
        print('NoSuchElementException')
        chkFlag = "1"
    except TimeoutException:
        print('TimeoutException')
        chkFlag = "1"
    finally:
        print("finally : ---SKIP---")

    return chkFlag


def shipping_price(itemcode, inPrice):
    print('\n [--- shipping_price ---]')

    #url = "http://freight.aliexpress.com/ajaxFreightCalculateService.htm?callback=jQuery18309705440334510058_1375336224186&productid=" + str(
    #    itemcode) + "&country=KR&count=1&f=d&_=1375336244868"

    url = "https://www.aliexpress.com/aeglodetailweb/api/logistics/freight?productId=" + str(
        itemcode) + "&count=1&minPrice="+str(inPrice)+"&country=KR&provinceCode=&cityCode=&tradeCurrency=USD"

    print('\n url:' + str(url))

    req2: Request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
            random.random()) + ' Safari/537.36', 'Referer': 'https://www.aliexpress.com'})
    connection2 = urlopen(req2)
    soup3 = BeautifulSoup(connection2, "html.parser")

    # print('\n soup3:' + str(soup3))
    items = str(soup3).split('"company":')
    print('\n len(items):' + str(len(items) - 1))

    delivery_price = ""
    delivery_nm = ""
    delivery_time = "0"
    delivery_sel = 1
    delivery_istrack = "false"

    low = 1
    while low < len(items):
        shipping_ea = items[low]
        # print('\n shipping_ea:' + str(shipping_ea))

        istrack = ""
        istrack = getparse(shipping_ea, '"tracking":', '}')
        shipping_val = getparse(shipping_ea, '"value":', "}")
        shipping_company = getparse(shipping_ea, '"', '"')
        shipping_time = getparse(shipping_ea, '"time":"', '"')

        epos = shipping_time.rfind('-')
        shipping_time = shipping_time[epos + 1:]
        print('\n ({0}) {1} | {2} | {3} | {4} '.format(str(low), str(istrack), str(shipping_val), str(shipping_company),
                                                       str(shipping_time)))
        if istrack == "true":
            if delivery_price == "":
                delivery_istrack = istrack
                delivery_price = str(float(shipping_val))
                delivery_nm = shipping_company
                delivery_time = shipping_time
            elif float(delivery_price) > float(shipping_val):
                delivery_istrack = istrack
                delivery_price = str(float(shipping_val))
                delivery_nm = shipping_company
                delivery_time = shipping_time

        low = low + 1

    print('\n 최저 배송비:' + str(delivery_price))
    return str(istrack) + '@' + str(delivery_price) + '@' + str(delivery_nm) + '@' + str(delivery_time)


def goodsSoldOutChk(in_driver2, gCode):
    print('\n [--- orderGoodsChk ---]')
    print('\n gCode : ' + str(gCode))
    chkFlag = "0"

    time.sleep(5)
    in_driver2.refresh()
    wait = WebDriverWait(in_driver2, 20)

    try:
        # 품절상품 체크
        strPrice = in_driver2.find_element_by_class_name('product-price-value')
        print('\n [품절체크] 화면 알리가격 : ' + str(strPrice.text))
    except NoSuchElementException:
        print('NoSuchElementException')
        chkFlag = "1"
    except TimeoutException:
        print('TimeoutException')
        chkFlag = "1"
    finally:
        print("--- 품절상품 체크 완료 ---")

    return chkFlag

def goodsDeliveryChk(in_driver2, gCode):
    print('\n [--- goodsDeliveryChk ---]')
    print('\n gCode : ' + str(gCode))
    chkFlag = "0"

    time.sleep(5)
    in_driver2.refresh()
    wait = WebDriverWait(in_driver2, 20)

    try:
        # 품절상품 체크
        strPrice = in_driver2.find_element_by_class_name('product-shipping')
        print('\n [한국 배송체크] 화면 문구 : ' + str(strPrice.text))
    except NoSuchElementException:
        print('NoSuchElementException')
        chkFlag = "1"
    except TimeoutException:
        print('TimeoutException')
        chkFlag = "1"
    finally:
        print("--- 한국 배송체크 완료 ---")
        if str(strPrice.text) == "Can not deliver to Korea":
            chkFlag = "1"
            print("--- 한국 배송 불가 [ " + str(strPrice.text) + " ] ---")
            fileWt("--- 한국 배송 불가 [ " + str(strPrice.text) + " ] ---")


    return chkFlag


def goodsOptionChk(in_driver2, gCode):
    print('\n [--- goodsOptionChk ---]')
    print('\n gCode : ' + str(gCode))
    chkFlag = "0"

    time.sleep(5)
    in_driver2.refresh()
    wait = WebDriverWait(in_driver2, 20)
    strOption = ""

    try:
        # 옶션 있는 상품인지 체크
        strOption = in_driver2.find_element_by_class_name('product-sku')
        print('\n [옵션내용] : ' + str(strOption.text))
    except NoSuchElementException:
        print('NoSuchElementException')
        chkFlag = "0"
    except TimeoutException:
        print('TimeoutException')
        chkFlag = "0"
    finally:
        print("--- 옶션 있는 상품인지 체크 완료 ---")
        if strOption.text == "":
            chkFlag = "0"
        else:
            chkFlag = "1"

    return chkFlag

def orderProc(in_driver, aliCode, orderNo):

    orderProcRtn = "0"


    print('\n {0} | {1}'.format(str(orderNo),str(aliCode)))
    fileWt("\n 알리 상품코드 " + str(orderNo)+" | "+str(aliCode))

    # time.sleep(5)
    # wait = WebDriverWait(in_driver, 20)
    # # 알리 상품코드 입력
    # in_driver.find_element_by_name('SearchText').send_keys(aliCode)
    #
    # # 상품코드 검색창 버튼 클릭
    # wait = WebDriverWait(in_driver, 20)
    # aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-button")))
    # aSearchBtn.click()

###################



    # 알리 상품코드 입력
    # in_driver.find_element_by_name('SearchText').send_keys(aliCode)
    in_driver.find_element_by_xpath('//*[@id="search-key"]').send_keys(aliCode)

    print('\n >>상품코드 검색창 : 알리 상품코드 입력')
    fileWt('\n\n >>상품코드 검색창 : 알리 상품코드 입력')

    # 상품코드 검색창 버튼 클릭
    wait = WebDriverWait(in_driver, 20)
    aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-button")))
    #aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.search-in-aliexpress")))
    aSearchBtn.click()

###################


    time.sleep(5)
    #in_driver.refresh()
    wait = WebDriverWait(in_driver, 20)

    #### 상품 품절 체크 ###
    if goodsSoldOutChk(in_driver, aliCode) == "1": ## 주문불가##
        print('\n 주문불가 {0} 알리 상품 품절 (상품코드) {1} '.format(str(orderNo), str(aliCode)))
        fileWt("\n 주문불가 알리 상품 품절 (상품코드)" + str(orderNo) + " | " + str(aliCode))

        # 알리 Home 이동
        in_driver.refresh()
        wait = WebDriverWait(in_driver, 20)
        aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
        aHomebtn.click()
        print('\n 알리 Home 이동')

        orderProcRtn = "1"
        return orderProcRtn

    time.sleep(5)

    # #### 상품 한국배송가능 체크 ###
    # if goodsDeliveryChk(in_driver, aliCode) == "1": ## 주문불가##
    #     print('\n 한국배송가능 체크 {0} 배송불가 (상품코드) {1} '.format(str(orderNo), str(aliCode)))
    #     fileWt("\n 한국배송가능 체크 : 배송불가 (상품코드)" + str(orderNo) + " | " + str(aliCode))
    #
    #     # 알리 Home 이동
    #     in_driver.refresh()
    #     wait = WebDriverWait(in_driver, 20)
    #     aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
    #     aHomebtn.click()
    #     print('\n 알리 Home 이동')
    #
    #     orderProcRtn = "1"
    #     return orderProcRtn
    #
    # time.sleep(5)

    #### 알리 상품 옵션있는지 체크 ####
    # if goodsOptionChk(in_driver, aliCode) == "1": ## 주문불가##
    #     print('\n 주문불가 {0} 알리 옵션 존재상품 (상품코드) {1} '.format(str(orderNo), str(aliCode)))
    #     fileWt("\n 주문불가  알리 옵션 존재상품 (상품코드)" + str(orderNo) + " | " + str(aliCode))
    #
    #     # 알리 Home 이동
    #     in_driver.refresh()
    #     wait = WebDriverWait(in_driver, 20)
    #     aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
    #     aHomebtn.click()
    #     print('\n 알리 Home 이동')
    #
    #     orderProcRtn = "1"
    #     return orderProcRtn
    #
    #
    # time.sleep(5)
    # in_driver.refresh()
    # wait = WebDriverWait(in_driver, 20)


    scrPrice = in_driver.find_element_by_class_name('product-price-value').text
    print('\n [화면 알리가격] : ' + scrPrice)

    miniPrice = str(scrPrice)
    if miniPrice.find("-") > 0:
        eaPrice = miniPrice.split("-")
        miniPrice = eaPrice[0]

    scrMiniPrice = miniPrice.replace("US","")
    scrMiniPrice = scrMiniPrice.replace("$", "")
    scrMiniPrice = scrMiniPrice.strip()
    print('\n scrMiniPrice : ' + str(scrMiniPrice))

    # 배송일 클릭
    wait = WebDriverWait(in_driver, 20)
    aDevDate = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.product-shipping-info.black-link")))
    aDevDate.click()
    print('\n >>배송일 : 버튼 클릭')
    fileWt('\n\n >>배송일 : 버튼 클릭')

    time.sleep(1)
    print('\n time.sleep(1)')

    wait = WebDriverWait(in_driver, 20)
    req = in_driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    print('\n 배송일 추출 (soup)')
    fileWt('\n 배송일 추출 (soup)')

    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    dev_price = "0"
######################################
    in_ea = "1"
######################################

    # 배송일 추출
    shipMiniPrice = float(scrMiniPrice) * float(in_ea)
    print('\n shipMiniPrice : ' + str(shipMiniPrice))

    dev_price_val = str(shipping_price(aliCode, shipMiniPrice))
    dev_price_items = dev_price_val.split('@')
    print('\n 배송일 추출 내용 : ' + str(dev_price_items))


    dev_track = dev_price_items[0].strip()
    dev_price = dev_price_items[1].strip()
    dev_name = dev_price_items[2].strip()
    dev_time = dev_price_items[3].strip()
    # print('\n dev_track : '+str(str(dev_track)))

    # 배송일 체크
    wait = WebDriverWait(in_driver, 20)
    listName = in_driver.find_elements_by_css_selector('div.service-name')


    listRadio = in_driver.find_elements_by_css_selector('input.next-radio-input')
    print('\n listRadio (len) : ' + str(len(listRadio)))




    dev_sel = "2"
    j = 1
    for iea in listName:
        j = j + 1
        # print('\n {0} : {1} '.format(j,str(iea.text)))
        if iea.text == dev_name:
            dev_sel = j
            break
    print('\n 선택 : ' + str(dev_sel))


    if str(dev_sel) != "2":
        wait = WebDriverWait(in_driver, 20)
        strSHiptxt = in_driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div/div/div/div[' + str(dev_sel) + ']/div[5]/div[1]').text

        # print('\n 선택배송사 : ' + str(strSHiptxt))
        # fileWt('\n 선택배송사 : ' + str(strSHiptxt))

        wait = WebDriverWait(in_driver, 20)
        # 배송일 선택 라디오버튼 클릭
        in_driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div/div/div/div[' + str(dev_sel) + ']/div[1]/label/span/input').click()
    else:
        strSHiptxt = dev_name

    print('\n (선택 버튼) 배송사 : ' + str(strSHiptxt))


    time.sleep(1)
    print('\n time.sleep(1)')

    # 배송일 적용버튼 클릭
    wait = WebDriverWait(in_driver, 20)
    aDevDatebtn = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-btn.next-medium.next-btn-primary")))
    aDevDatebtn.click()
    print('\n >>배송일 : 적용 버튼 클릭')


    time.sleep(1)
    print('\n time.sleep(1)')

    # 화면에서 적용 배송비용 날짜 부분 가져오기 #
    wait = WebDriverWait(in_driver, 30)
    strShipping = in_driver.find_element_by_class_name('product-shipping').text
    print('\n [화면:배송] : ' + str(strShipping))





    ### 배송비 배송날짜 체크 - 주문 가능 여부 판단 ###
    if str(dev_track) == "false":
        print('\n 트래킹 포함하는 배송사 없음 [주문불가]')
        fileWt('\n 트래킹 포함하는 배송사 없음 [주문불가]')
        orderProcRtn = "1"
    else:
        if strShipping.find(dev_name) < 0:
            print('\n 배송사명 match Error'+ str(dev_name))
            fileWt('\n 배송사명 match Error' + str(dev_name))
            orderProcRtn = "1"
        if float(dev_price) > 6.0:
            print('\n 배송비 6달러 이상 [주문불가] :' + str(dev_price))
            fileWt('\n 배송비 6달러 이상 [주문불가] :' + str(dev_price))
            orderProcRtn = "1"
        if int(dev_time) > 24:
            print('\n 배송기간 24일 이상 [delay]:' + str(dev_time))
            fileWt('\n 배송기간 24일 이상 [delay]:' + str(dev_time))
            orderProcRtn = "1"


    if orderProcRtn == "1": ## 주문불가##
        # 알리 Home 이동
        wait = WebDriverWait(in_driver, 20)
        aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
        aHomebtn.click()
        print('\n 알리 Home 이동')
        return orderProcRtn

    else:

        wait = WebDriverWait(in_driver, 30)
        # 즉시구매 버튼 클릭
        aBuyBtn = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-btn.next-large.next-btn-primary.buynow")))
        aBuyBtn.click()

        # 주소선택 Down 화살표 클릭
        aJusoChk = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.arrow-content.arrow-down")))
        aJusoChk.click()

        # 주소 Edit 클릭
        aJusoEdit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-btn.next-medium.next-btn-primary.next-btn-text")))
        aJusoEdit.click()

        time.sleep(2)

        # sql = " select top 1 t.uid, OrderNo, SettlePrice, OrdName, state, RegDate, ConfirmDate,optionKind, OptionTxt,"
        # sql = sql + " rcvName, RcvTel, RcvMobile, RcvPost, RcvAddr, RcvAddrDetail, soc_no, i.ali_seller, optionKind, OptionTxt, i.ea "
        # sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.uid "
        # sql = sql + " where state = '200' and naver_pay_cancel_wait is null and cancel_cate is null and cancel_reason is null "
        # sql = sql + " and OrderMemo is null and AdminMemo is null and cancel_cate is null and cancel_reason is null "
        # sql = sql + " and t.OrderNo = '" + str(orderNo) + "'"

########################################
        sql = " select top 1 t.uid, OrderNo, SettlePrice, OrdName, state, RegDate, ConfirmDate,optionKind, OptionTxt,"
        sql = sql + " rcvName, RcvTel, RcvMobile, RcvPost, RcvAddr, RcvAddrDetail, soc_no, i.ali_seller, optionKind, OptionTxt, i.ea "
        sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.uid "
        sql = sql + " where t.OrderNo = '" + str(orderNo) + "'"
########################################

        print('\n sql:' + str(sql))
        fileWt('\n\n sql:' + str(sql))
        db.execute(sql)
        row = db.fetchone()
        cnt = 0

        if not row:
            # 해당 주문번호가 배송준비중 상태가 아니거나 1개이상의 주문일 경우 주문불가
            # 알리 Home 이동
            print('\n 해당 주문번호가 배송준비중 상태가 아니거나 1개이상의 주문일 경우 주문불가 :'+str(orderNo))
            fileWt("\n 해당 주문번호가 배송준비중 상태가 아니거나 1개이상의 주문일 경우 주문불가" + str(orderNo))

            wait = WebDriverWait(in_driver, 20)
            aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.ae-logo")))
            aHomebtn.click()
            print('\n 알리 Home 이동')
            orderProcRtn = "1"
            return orderProcRtn

        else:
            cnt = cnt + 1
            d_uid = row[0]
            d_OrderNo = row[1]
            d_SettlePrice = row[2]
            d_rcvName = row[9]
            d_RcvTel = row[10]
            d_RcvMobile = row[11]
            d_RcvPost = row[12]
            d_RcvAddr = row[13]
            d_RcvAddrDetail = row[14]
            d_soc_no = row[15]
            d_ali_seller = row[16]

            strTemp = str(d_OrderNo) + " | " + str(format(d_SettlePrice, ',')) + "원 | " + str(d_rcvName) + " | " + str(d_RcvTel) + " | " + str(d_RcvMobile) + " | " + str(d_RcvPost) + " | "  + str(d_RcvAddr) + " | " + str(d_RcvAddrDetail) + " | " + str(d_soc_no)
            print("\n [프리쉽 주문내역] " + strTemp)
            fileWt("\n\n [프리쉽 주문내역] " + strTemp)

            d_RcvPost = d_RcvPost.replace("-", "")
            d_RcvMobile = d_RcvMobile.replace("-","")
            if d_RcvMobile == "":
                d_RcvMobile = d_RcvTel.replace("-","")

            # 주소 입력
            in_driver.implicitly_wait(5)

            in_driver.find_element_by_id('contactPerson').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('contactPerson').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('mobileNo').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('mobileNo').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('address').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('address').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('address2').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('address2').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('city').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('city').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('zip').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('zip').send_keys(Keys.DELETE)
            in_driver.find_element_by_id('passportNo').send_keys(Keys.CONTROL + "a")
            in_driver.find_element_by_id('passportNo').send_keys(Keys.DELETE)

            wait = WebDriverWait(in_driver, 20)
            time.sleep(3)

            ########### 이름 주소 영문 번역 ###################
            #
            # # 변환할 이름
            # engName = getEngName(d_rcvName)
            # print('\n engName : ' + str(engName))
            #
            # if engName == "":
            #     # 알리 Home 이동
            #     print('\n 영문 이름 번역 불가 :' + str(d_rcvName))
            #     fileWt("\n 영문 이름 번역 불가" + str(d_rcvName))
            #
            #     wait = WebDriverWait(in_driver, 20)
            #     aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.ae-logo")))
            #     aHomebtn.click()
            #     print('\n 알리 Home 이동')
            #     orderProcRtn = "1"
            #     return orderProcRtn
            #
            # time.sleep(3)
            #
            # # 변환할 주소
            # engJuso = chgEngJusoProc(d_RcvAddr, d_RcvAddrDetail, d_RcvPost)
            # engJuso_0 = engJuso.replace(", Republic of Korea", "")
            #
            # fpos2 = engJuso_0.rfind(",")
            # if fpos2 > 0:
            #     engJuso_2 = engJuso_0[:fpos2].strip()
            #     engJuso_1 = engJuso_0[fpos2 + 1:].strip()
            #
            # #print('\n 영문 변환 전체주소 : ' + str(engJuso))
            # print('\n 영문 변환 주소 2 : ' + str(engJuso_2))
            # print('\n 영문 변환 주소 1 : ' + str(engJuso_1))
            #
            # if engJuso_1 == "" or engJuso_2 == "":
            #     # 알리 Home 이동
            #     print('\n 영문 주소 번역 불가 :' + str(d_RcvAddr))
            #     print('\n 영문 주소 번역 불가 :' + str(d_RcvAddrDetail))
            #     fileWt("\n 영문 주소 번역 불가: " + str(d_RcvAddr) + " " + str(d_RcvAddrDetail))
            #
            #     wait = WebDriverWait(in_driver, 20)
            #     aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.ae-logo")))
            #     aHomebtn.click()
            #     print('\n 알리 Home 이동')
            #     orderProcRtn = "1"
            #     return orderProcRtn


####################################
            #38, Innovalley-ro, Dong-gu, Daegu, Republic of Korea   41065
            time.sleep(5)

            in_driver.find_element_by_id('contactPerson').send_keys('Kim Yujin')
            in_driver.find_element_by_id('mobileNo').send_keys('01090467616')
            in_driver.find_element_by_id('address').send_keys('38, Innovalley-ro, Dong-gu')
            in_driver.find_element_by_id('address2').send_keys('2F')
            in_driver.find_element_by_id('city').send_keys('Daegu')
            in_driver.find_element_by_id('zip').send_keys('41065')
            in_driver.find_element_by_id('passportNo').send_keys('19780701')

####################################
            ########### 이름 주소 영문 번역 ###################
            # time.sleep(5)
            #
            # in_driver.find_element_by_id('contactPerson').send_keys(engName + '(' + d_OrderNo + ')')
            # in_driver.find_element_by_id('mobileNo').send_keys(d_RcvMobile)
            # in_driver.find_element_by_id('address').send_keys(engJuso_2)
            # in_driver.find_element_by_id('address2').send_keys(d_RcvAddrDetail)
            # in_driver.find_element_by_id('city').send_keys(engJuso_1)
            # in_driver.find_element_by_id('zip').send_keys(d_RcvPost)
            # in_driver.find_element_by_id('passportNo').send_keys(d_soc_no)

            time.sleep(3)

            # Confirm 버튼 클릭
            wait = WebDriverWait(in_driver, 20)
            aJusoEdit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-btn.next-large.next-btn-primary")))
            aJusoEdit.click()
            print('\n Confirm 버튼 클릭 완료')

            time.sleep(5)
            ####################### 주문 내용 확인 #######################

            #주소 이름 연락처 우편번호
            orderNameChk = in_driver.find_element_by_class_name('address-item').text
            print('\n [수령지] :'+str(orderNameChk))
            fileWt('\n\n [수령지] :'+str(orderNameChk))

            #배송비
            orderShipPrice = in_driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/div/div/div/div[3]/div/div[2]/div[2]').text
            orderShipPrice = orderShipPrice.replace("US", "")
            orderShipPrice = orderShipPrice.replace("$", "")
            print('\n [결제화면] 배송비 :'+str(orderShipPrice))
            fileWt('\n\n [결제화면] 배송비 :' + str(orderShipPrice))

            #합계 결제금액
            orderTotalPrice = in_driver.find_element_by_class_name('total-cost').text
            print('\n [결제화면] 합계 결제금액 :'+str(orderTotalPrice))
            fileWt('\n [결제화면] 알리 결제금액 :'+str(orderTotalPrice))

            orderTotalPrice = orderTotalPrice.replace("US", "")
            orderTotalPrice = orderTotalPrice.replace("$", "")
            ori_cost = float(orderTotalPrice) * exchangeRate
            ori_cost = round(ori_cost)
            margin = int(d_SettlePrice) - int(ori_cost)
            print('\n 프리쉽 판매가격 :' + format(d_SettlePrice, ','))
            print('\n 원가 :'+ format(ori_cost, ','))
            print('\n 예상 마진 :'+ format(margin, ','))

            fileWt("\n 프리쉽 판매가격 " + str(format(d_SettlePrice, ',')))
            fileWt("\n 원가 " + str(format(ori_cost, ',')))
            fileWt("\n 예상 마진 " + str(format(margin, ',')))

            # if orderNameChk.find(d_OrderNo) < 0:
            #     print('\n 주문번호 없음 확인필요: ' + str(d_OrderNo))
            #     fileWt('\n 주문번호 없음 확인필요: ' + str(d_OrderNo))
            #     orderProcRtn = "1"
            # if orderNameChk.find(d_RcvMobile) < 0:
            #     print('\n 연락처 없음 확인필요: ' + str(d_RcvMobile))
            #     fileWt('\n 연락처 없음 확인필요: ' + str(d_RcvMobile))
            #     orderProcRtn = "1"
            # if orderNameChk.find(d_RcvPost) < 0:
            #     print('\n 우편번호 없음 확인필요: ' + str(d_RcvPost))
            #     fileWt('\n 우편번호 없음 확인필요: ' + str(d_RcvPost))
            #     orderProcRtn = "1"
            #
            # if float(orderShipPrice) > 6.0:
            #     print('\n 배송비 6달러 초과: ' + str(orderShipPrice))
            #     fileWt('\n 배송비 6달러 초과: ' + str(orderShipPrice))
            #     orderProcRtn = "1"
            # if float(d_SettlePrice) <= float(ori_cost):
            #     #print('\n 가격초과 ( 알리가격: {0} * 환율({1}) = : {2}'.format(str(d_SettlePrice),str(exchangeRate),str(ori_cost)))
            #     pmsg = '\n 가격초과 [ 알리 가격: ' + str(d_SettlePrice) + '* 환율(' + str(exchangeRate) + ') = : ' + str(ori_cost) + ' ]'
            #     print(pmsg)
            #     fileWt(pmsg)
            #     orderProcRtn = "1"

            cur_url = in_driver.current_url
            print('\n cur_url : '+str(cur_url))
            fileWt('\n cur_url : ' + str(cur_url))
            # if cur_url != "":
            #     itemno_chk = getparse(cur_url,"objectId=","&")
            #     if itemno_chk == str(d_ali_seller).strip():
            #         print('\n [화면] 상품코드 일치 : ' + str(itemno_chk))
            #         fileWt('\n [화면] 상품코드 일치 : ' + str(itemno_chk))
            #     else:
            #         print('\n 알리 상품코드 불일치 : ' + str(itemno_chk))
            #         orderProcRtn = "1"
            # else:
            #     print('\n 알리 상품코드 확인불가 cur_url : ' + str(cur_url))
            #     fileWt('\n\n 알리 상품코드 확인불가 cur_url : ' + str(cur_url))
            #     orderProcRtn = "1"

            ####################### 주문 내용 확인 #######################
            time.sleep(3)
            wait = WebDriverWait(in_driver, 20)
            input('아무거나 입력하세요.[1]')

            # 주문 버튼 클릭
            wait = WebDriverWait(in_driver, 20)
            aOkbtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.order-btn-holder")))
            aOkbtn.click()
            print('\n 주문 완료')


            time.sleep(3)
            # # 주문완료 체크
            # pageChk = in_driver.find_element_by_class_name('next-message-title').text
            # print('\n [주문완료 체크] :' + str(pageChk))
            # fileWt('\n\n [주문완료 체크] :' + str(pageChk))


            # # 옶션 있는 상품인지 체크
            # strOption_box = mainDriver.find_element_by_css_selector('div.operation-container')
            # comments = strOption_box.find_elements_by_tag_name("a")
            # comments_text = {}
            #
            # for num, comment in enumerate(comments):
            #     comments_text[num] = comment.find_element_by_css_selector("div.sku-property-text")
            #     print('\n [옵션내용 3] num : ' + str(num))
            #     print('\n [옵션내용 3] : ' + str(comments_text[num].text))
            #
            #     txtShip = str(comments_text[num].text).strip()
            #     if txtShip == "CHINA" or txtShip == "china" or txtShip == "중국" or txtShip == "CN" or txtShip == "cn":
            #         comments_text[num].click()
            #         print("CHINA Click ")
            #         break
            #
            # print('\n 옵션 선택완료 ')

            strCheckMyOrder = mainDriver.find_element_by_css_selector('div.operation-container')
            comments = strCheckMyOrder.find_elements_by_tag_name("a")
            comments[1].click()


            # myorderbtn = in_driver.find_element_by_xpath('//*[@id="container"]/div/div/div[4]/a[2]').text
            # print('\n [myorderbtn] :' + str(myorderbtn))
            # fileWt('\n\n [myorderbtn] :' + str(myorderbtn))
            input('아무거나 입력하세요.[주문 완료][2]')




            in_driver.find_element_by_xpath('//*[@id="container"]/div/div/div[4]/a[2]').click()
            time.sleep(3)
            wait = WebDriverWait(in_driver, 20)
            input('아무거나 입력하세요.[ Check my order ][3]')

                        # ################################################################################
                        # ##주문이력 화면으로 이동후 주문번호 확인하기
                        #
                        # wait = WebDriverWait(in_driver, 20)
                        # strorderInfo = in_driver.find_element_by_class_name('order-info').text
                        # print('\n [strorderInfo] :' + str(strorderInfo))
                        # fileWt('\n [strorderInfo] :' + str(strorderInfo))
                        #
                        # newOrderNo = getparse(strorderInfo, "Order ID:", "View Detail")
                        # newOrderNo = newOrderNo.strip()
                        # print('\n [newOrderNo] :' + str(newOrderNo))
                        # fileWt('\n [newOrderNo] :' + str(newOrderNo))
                        #
                        # ########### 주문 내역 검증 필요
                        #
                        # time.sleep(3)
                        # wait = WebDriverWait(in_driver, 20)
                        #
                        # #pUrl = "https://trade.aliexpress.com/order_detail.htm?orderId=8015724942157399"
                        # pUrl = "https://trade.aliexpress.com/order_detail.htm?orderId="+str(newOrderNo)
                        # print('\n pUrl :' + str(pUrl))
                        # fileWt('\n pUrl :' + str(pUrl))
                        #
                        # ### 주문내역 확인 ###
                        # req2: Request = Request(pUrl, headers={
                        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                        #         random.random()) + ' Safari/537.36', 'Referer': 'https://www.aliexpress.com'})
                        # connection2 = urlopen(req2)
                        # print('\n - OK - ')
                        # last_chk_pos = 0
                        # soup2 = BeautifulSoup(connection2, "html.parser")
                        #
                        # str_sItemno = getparse(str(soup2), 'productId="', '" ')
                        # print('\n str_sItemno :' + str(str_sItemno))
                        # fileWt('\n str_sItemno :' + str(str_sItemno))
                        #
                        # str_patxt = getparse(str(soup2), "'Zip Code'","</li>")
                        # str_sZip = getparse(str_patxt, '"i18ncopy">','</span>')
                        # print('\n str_sZip :' + str(str_sZip))
                        # fileWt('\n str_sZip :' + str(str_sZip))
                        #
                        # time.sleep(3)
                        # ################################################################################
                        # wait = WebDriverWait(in_driver, 20)
                        # input('아무거나 입력하세요.[newOrderNo][4]')
                        #
                        # # 주문완료 화면에서 알리 Home 이동
                        # wait = WebDriverWait(in_driver, 20)
                        # aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
                        # aHomebtn.click()
                        # print('\n 알리 Home 이동')
                        #
                        # return "0"

                        #
                        # #if str_sZip.strip() == d_RcvPost and str_sItemno.strip() == str(d_ali_seller).strip():
                        # if str_sZip.strip() == "41065" and str_sItemno.strip() == "32326259904":
                        #     print('\n 주문내역 확인완료 | str_sItemno: ' + str(str_sItemno) + ' | str_sZip : ' + str(str_sZip))
                        #     fileWt('\n 주문내역 확인완료 | str_sItemno: ' + str(str_sItemno) + ' | str_sZip : ' + str(str_sZip))
                        #
                        #     time.sleep(3)
                        #     ################################################################################
                        #     wait = WebDriverWait(in_driver, 20)
                        #     input('아무거나 입력하세요.[newOrderNo][4]')
                        #
                        #     # 주문완료 화면에서 알리 Home 이동
                        #     wait = WebDriverWait(in_driver, 20)
                        #     aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
                        #     aHomebtn.click()
                        #     print('\n 알리 Home 이동')
                        #
                        #     return "0"
                        #     ################################################################################
                        #
                        # else:
                        #     print('\n 주문 실패 myorderbtn :' + str(myorderbtn))
                        #     fileWt('\n 주문 실패 myorderbtn :' + str(myorderbtn))
################################################################################
#    Payment Successful 이 아닐경우  프로그램 종료 코드 추가 필요
# ################################################################################
#                     else:
#                         print('\n 주문 실패 myorderbtn :' + str(myorderbtn))
#                         fileWt('\n 주문 실패 myorderbtn :' + str(myorderbtn))
# ################################################################################
# #    Payment Successful 이 아닐경우  프로그램 종료 코드 추가 필요
# ################################################################################
#
#                 else:
#                     print('\n 주문 실패 pageChk :' + str(pageChk))
#                     fileWt('\n 주문 실패 pageChk :' + str(pageChk))
# ################################################################################
# #    Payment Successful 이 아닐경우  프로그램 종료 코드 추가 필요
# ################################################################################
#                     return "1"


def fileWt(strMsg):
    global st_now
    global fileName

    f = open(fileName, 'a')
    f.write(str(strMsg))
    f.close()


def procStart(driver):
    global st_now
    global fileName

    now = datetime.datetime.now()
    Year = str(now)[:4]
    nowDate = now.strftime('%Y-%m-%d')

    strDate = str(now)[:10]
    strTime = str(now)[11:-7]
    strHH = strTime[:2]

    before1h = int(strHH) - 1
    sDate = strDate + " 00:00:00"
    eEate = strDate + " " + str(before1h) + ":00:00"

    print('\n sDate: ' + str(sDate))
    print('\n eEate: ' + str(eEate))

    print("\n [--- procStart ---] ------------------------------------- "+str(now))
    fileWt("\n [--- procStart ---] ------------------------------------- "+str(now))

    #orderList = ['32972721404','32869770621','32766472920','4000739579155']
    #orderList = ['32854052487']

    # sql = " select top 10 t.uid, OrderNo, SettlePrice, i.GoodsCode, i.ali_seller, i.sitecate, RcvPost, soc_no, rcvName "
    # sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.uid "
    # sql = sql + " where t.state = '200' and i.optionKind <> '300' and i.ea = 1 and soc_no is not null and ali_seller is not null"
    # sql = sql + " and OrderMemo is null and AdminMemo is null and cancel_cate is null and cancel_reason is null "
    # sql = sql + " and naver_pay_cancel_wait is null "
    # sql = sql + " and i.sitecate in ('fashion','electron','baby','furniture','beauty','jewelry','auto','sports','office','industry','fashion2','electron2','baby2','furniture2','beauty2','jewelry2','auto2','sports2','office2','industry2') "
    # #sql = sql + " and ConfirmDate between '" + str(nowDate) + " 00:00:00' and getdate()"
    # sql = sql + " and ConfirmDate between '" + str(sDate) + "' and '" + str(eEate) + "'"
    #
    # #### 10만원 이하 상품 ####
    # sql = sql + " and t.SettlePrice < 100000 "
    # #### 10만원 이하 상품 ####
    # sql = sql + " order by t.uid desc"
    #
    # print('\n sql:' + str(sql))
    # fileWt('\n sql:' + str(sql))
    #
    # db.execute(sql)
    # ord_rows = db.fetchall()
    # print('\n 처리할 주문 CNT :' + str(len(ord_rows)))
    # fileWt('\n 처리할 주문 CNT :' + str(len(ord_rows)))
    #
    # orderProc(driver, m_ali_code, m_OrderNo)
    #
    # icnt = 0
    # if ord_rows:
    #     for rs in ord_rows:
    #         procCheckFlag = "0"
    #         icnt = icnt + 1
    #         m_uid = rs[0]
    #         m_OrderNo = rs[1]
    #         m_SettlePrice = rs[2]
    #         m_GoodsCode = rs[3]
    #         m_ali_code = rs[4]
    #         m_site = rs[5]
    #         m_RcvPost = rs[6]
    #         m_soc_no = rs[7]
    #         m_rcvName = rs[8]
    #         print('\n ------------------------------------------------------------------------')
    #         print(
    #             '\n [{0}] {1} | {2} | {3} | {4} | {5} | {6}'.format(icnt, m_uid, m_OrderNo, m_SettlePrice, m_GoodsCode, m_ali_code, m_rcvName))
    #         fileWt("\n\n 카운트 ----------------------------------------------------  " + str(icnt))
    #         fileWt("\n 주문번호" + str(m_OrderNo))
    #
    #         ## t_order_info 주문건수 1개 이상인지 체크 ##
    #         sql_r = " select * from t_order_info where OrderUid ='" + str(m_uid) + "'"
    #         print('\n sql_r:' + str(sql_r))
    #         db2.execute(sql_r)
    #         ord_info_rows = db2.fetchall()
    #         #print('\n t_order_info (CNT):' + str(len(ord_info_rows)))
    #         #fileWt("\n 주문건수 1개인지 체크: " + str(len(ord_info_rows)))
    #
    #         #if int(m_SettlePrice) < 50000:
    #         #    print('\n 결제 금액 5만원 이상 자동주문처리 불가 (SKIP) : '+str(m_SettlePrice))
    #         #    procCheckFlag = "1"
    #
    #         if str(len(ord_info_rows)) != "1":
    #             print('\n 주문번호당 1개 이상의 주문 (SKIP) : '+str(m_OrderNo))
    #             fileWt('\n 주문번호당 1개 이상의 주문 (SKIP) : '+str(m_OrderNo))
    #             procCheckFlag = "1"
    #
    #         if len(m_RcvPost) > 5:
    #             print('\n 우편번호 5자리 이상 확인필요 (SKIP) : '+str(m_RcvPost))
    #             fileWt('\n 우편번호 5자리 이상 확인필요 (SKIP) : '+str(m_RcvPost))
    #             procCheckFlag = "1"
    #
    #         if len(m_rcvName) > 3:
    #             print('\n 수령인명 3자리 이상 확인필요 (SKIP) : '+str(m_rcvName))
    #             fileWt('\n 수령인명 3자리 이상 확인필요 (SKIP) : ' + str(m_rcvName))
    #             procCheckFlag = "1"
    #
    #         if m_rcvName == "우리집":
    #             print('\n 수령인명 불가한이름 포함 확인필요 (SKIP) : '+str(m_rcvName))
    #             fileWt('\n 수령인명 불가한이름 포함 확인필요 (SKIP) : ' + str(m_rcvName))
    #             procCheckFlag = "1"
    #
    #         if len(m_soc_no) == 8:
    #             if not m_soc_no.isdigit():
    #                 print('\n 통관번호 숫자아님 확인필요 (SKIP) : '+str(m_soc_no))
    #                 fileWt('\n 통관번호 숫자아님 확인필요 (SKIP) : ' + str(m_soc_no))
    #                 procCheckFlag = "1"
    #             else:
    #                 strY = m_soc_no[:4]
    #                 strM = m_soc_no[4:-2]
    #                 strD = m_soc_no[6:]
    #                 if int(strY) < int(Year) - 100 or int(strM) > 12 or int(strD) > 31:
    #                     print('\n 통관번호 생년월일 오류 (SKIP) : ' + str(m_soc_no))
    #                     fileWt('\n 통관번호 생년월일 오류 (SKIP) : ' + str(m_soc_no))
    #                     procCheckFlag = "1"
    #         elif len(m_soc_no) == 13:
    #             if not (m_soc_no[:1].upper() == "P" and m_soc_no[1:].isdigit() ):
    #                 print('\n 통관번호 오류 (SKIP) : ' + str(m_soc_no))
    #                 fileWt('\n 통관번호 오류 (SKIP) : ' + str(m_soc_no))
    #                 procCheckFlag = "1"
    #         else:
    #             print('\n 통관번호 확인필요 (SKIP) : ' + str(m_soc_no))
    #             fileWt('\n 통관번호 확인필요 (SKIP) : ' + str(m_soc_no))
    #             procCheckFlag = "1"
    #
    #         if procCheckFlag == "0":
    #             main = driver.window_handles
    #             last_tab = driver.window_handles[len(main) - 1]
    #             # print('\n last_tab: ' + str(last_tab))
    #             if str(len(main)) != "1":
    #                 for handle in main:
    #                     if handle != last_tab:
    #                         driver.switch_to.window(window_name=handle)
    #                         driver.close()
    #                     driver.switch_to.window(window_name=last_tab)
    #
    #             pmsg = '\n [--- orderProc ---] ' + str(datetime.datetime.now())
    #             print(pmsg)
    #             fileWt(pmsg)
    #
    #             if orderProc(driver, m_ali_code, m_OrderNo) == "1":
    #                 print('\n Order fail : ' + str(m_OrderNo))
    #                 fileWt("\n 주문 실패 " + str(m_OrderNo))
    #             else:
    #                 print('\n Order success : ' + str(m_OrderNo))
    #                 fileWt("\n 주문 성공 " + str(m_OrderNo))
    #
    #             pmsg = '\n [--- orderProc ---] ' + str(datetime.datetime.now())
    #             print(pmsg)
    #             fileWt(pmsg)
    #
    #             driver.refresh()
    #             wait = WebDriverWait(driver, 20)
    #             print('\n ------------------------------------------------------------------------')
    #
    #         else:
    #             print('\n 주문 불가 : ' + str(m_OrderNo))
    #             fileWt('\n 주문 불가 : ' + str(m_OrderNo))

#####################

    m_ali_code = "4001278493498"
    m_OrderNo = "P2026102524808"
    orderProc(driver, m_ali_code, m_OrderNo)

#####################
    e_now = datetime.datetime.now()
    fileWt("\n [--- procEnd ---] -------------------------------------" + str(e_now))

if __name__=='__main__':

    now = datetime.datetime.now()
    print('\n [--- main Proc start ---] ' + str(now))
    fileWt('\n [--- main Proc start ---] ' + str(now))

    path = "C:\\util\\chromedriver.exe"
    mainDriver = webdriver.Chrome(path)
    mainDriver.get('https://login.aliexpress.com/')

    # 로그인 버튼 클릭
    login_Proc(mainDriver)
    time.sleep(2)

    # 쿠폰 파업창 확인
    if chk_CouponPop(mainDriver) == "1":
        print('\n 쿠폰팝업 없음')
    else:
        print('\n 쿠폰팝업 닫기 완료')

    procStart(mainDriver)

    now = datetime.datetime.now()
    print('\n [--- main Proc end ---] ' + str(now))
    fileWt('\n [--- main Proc end ---] ' + str(now))
