# library to launch and kill Tor process
import random
# library for Tor connection
import socket
import socks
import http.client
# library for scraping
import urllib
from urllib.request import Request, urlopen
from multiprocessing import Pool, freeze_support, Manager, Process
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
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import os
#from phpserialize import serialize, unserialize
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import datetime


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


def login_Proc(in_driver):
    print('\n [--- login_Proc ---]')
    wait = WebDriverWait(in_driver, 20)

    # 로그인 ID/PASS 입력
    in_driver.find_element_by_name('fm-login-id').send_keys('koiforever0526@gmail.com')
    in_driver.find_element_by_name('fm-login-password').send_keys('uiop7890')

    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    # 로그인 버튼 클릭
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


def goodsSoldOutChk(in_driver2, gCode):
    print('\n [--- orderGoodsChk ---]')
    print('\n gCode : ' + str(gCode))
    chkFlag = "0"

    time.sleep(1)
    print('\n time.sleep(1)')
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

    time.sleep(1)
    print('\n time.sleep(1)')
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
            #fileWt("--- 한국 배송 불가 [ " + str(strPrice.text) + " ] ---")

    return chkFlag

def shipping_price(in_Driver, itemcode, inPrice):
    print('\n [--- shipping_price ---]')

    # url = "http://freight.aliexpress.com/ajaxFreightCalculateService.htm?callback=jQuery18309705440334510058_1375336224186&productid=" + str(
    #    itemcode) + "&country=KR&count=1&f=d&_=1375336244868"
    url = "https://www.aliexpress.com/aeglodetailweb/api/logistics/freight?productId=" + str(
        itemcode) + "&count=1&minPrice=" + str(inPrice) + "&country=KR&provinceCode=&cityCode=&tradeCurrency=USD"

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

        shipping_time = "0"
        istrack = ""
        istrack = getparse(shipping_ea, '"tracking":', '}')
        shipping_val = getparse(shipping_ea, '"value":', "}")
        shipping_company = getparse(shipping_ea, '"', '"')
        shipping_time = getparse(shipping_ea, '"time":"', '"')

        epos = shipping_time.rfind('-')
        shipping_time = shipping_time[epos + 1:]
        print('\n ({0}) {1} | {2} | {3} | {4} '.format(str(low), str(istrack), str(shipping_val), str(shipping_company),
                                                       str(shipping_time)))
        # print(shipping_company.find("AliExpress Standard"))

        if istrack == "true" and shipping_company.find("China Post") < 0 and int(shipping_time) < 22:
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

    print('\n 최저 배송사 :' + str(delivery_istrack) + " | " + str(delivery_price) + " | " + str(delivery_nm) + " | " + str(
        delivery_time))

    if str(delivery_nm).strip() == "":
        print('\n 선택가능한 배송사 없음 :' + str(delivery_nm))
        return "S001"

    if float(delivery_price) > 4.0:
        print('\n 배송비 4달러 이상 :' + str(delivery_price))
        return "S002"

    if int(delivery_time) > 22:
        print('\n 배송일 22일 이상소요 :' + str(delivery_time))
        return "S003"

    time.sleep(1)
    print('\n time.sleep(1)')
    # 배송내용 부분 클릭
    wait = WebDriverWait(in_Driver, 20)
    btnLogistics = in_Driver.find_element_by_class_name('logistics-company')
    print(btnLogistics)
    btnLogistics.click()
    print('\n >>배송내용 부분 : 클릭')

    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    service_names = in_Driver.find_elements_by_css_selector('div.service-name')
    print('\n 배송사 CNT : ' + str(len(service_names)))

    dev_sel = 0
    j = 0
    for iea in service_names:
        if iea.text == delivery_nm:
            dev_sel = j
            print('\n {0} : {1} '.format(j, str(iea.text)))
            break
        j = j + 1
    print('\n 배송사 선택 : ' + str(dev_sel))

    time.sleep(1)
    print('\n time.sleep(1)')
    radio_cells = in_Driver.find_elements_by_css_selector('div.table-td.radio-cell')
    radio_cells[dev_sel].click()
    print('\n >>배송사 선택 라디오버튼 : 클릭')

    time.sleep(1)
    print('\n time.sleep(1)')

    # 배송일 적용버튼 클릭
    wait = WebDriverWait(in_Driver, 20)
    aDevDatebtn = in_Driver.find_element_by_xpath('/html/body/div/div/div/div/button')
    aDevDatebtn.click()
    print('\n >>배송일 : 적용 버튼 클릭')

    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    logisticSelName = in_Driver.find_element_by_class_name('logistics-company')
    sel_deliver_name = str(logisticSelName.text)
    print('\n [화면 배송] : ' + sel_deliver_name)
    print('\n 선택 배송사 : ' + delivery_nm)

    if sel_deliver_name.find(delivery_nm) < 0:
        print('\n 선택 배송사 불일치')
        return "S004"
    else:
        print('\n 선택 배송사 일치')
        return "0"


def getShipFromOptCode(in_soup_str):
    strTempCut = ""
    shipFromCode = ""
    ch_pos = -1
    ch_pos2 = -1
    in_soup_str = str(in_soup_str)

    # CHINA 또는 CN 검색
    ch_pos = in_soup_str.upper().find('PROPERTYVALUEDISPLAYNAME":"CHINA"')
    print('\n CHINA 위치 검색 (ch_pos) :' + str(ch_pos))

    if ch_pos > -1:
        strTempCut = in_soup_str[ch_pos:]
        print('\n strTempCut :' + str(strTempCut))
        shipFromCode = getparse(strTempCut, 'propertyValueId":', ',"propertyValueIdLong')
        print('\n shipFromCode :' + str(shipFromCode))
    else:
        ch_pos2 = in_soup_str.upper().find('PROPERTYVALUEDISPLAYNAME":"CN"')
        print('\n ch_pos2 :' + str(ch_pos2))
        if ch_pos2 > -1:
            strTempCut = in_soup_str[ch_pos2:]
            print('\n strTempCut :' + str(strTempCut))
            shipFromCode = getparse(strTempCut, 'propertyValueId":', ',"propertyValueIdLong')
            print('\n shipFromCode :' + str(shipFromCode))

    return shipFromCode


# getSkuAttr (skuAttr, skuId 검색)
def getSkuAttr(in_soup, in_opCode):
    ren_flg_search = ""
    tmp_skuAttr = ""
    tmp_skuId = ""
    rtnCodeStr = ""

    tmp_opCode = 'skuPropIds":"' + str(in_opCode)
    print('\n [검색 skuPropIds ] :' + str(tmp_opCode))

    t_fos = str(in_soup).find(tmp_opCode)
    # print('\n f_fos :' + str(f_fos))

    if t_fos == -1:
        ren_flg_search = "X01"
        print('\n [X01] 일치 하는 옵션 없음 : ' + str(ren_flg_search))
    else:
        tmp_string = in_soup[:t_fos]
        # 재고확인 (inventory)
        tmp_string_2 = getparse(str(in_soup), str(in_opCode), '"isActivity":')
        tmp_inventory = getparse(tmp_string_2, '"inventory":', ',')
        # print('\n tmp_string_2 :' + str(tmp_string_2))
        print('\n [ 옵션 재고수량 ] :' + str(tmp_inventory))

        if int(tmp_inventory) == 0:
            ren_flg_search = "X02"
            print('\n [X02] 해당옵션 재고없음 : ' + str(ren_flg_search))
        else:
            sku_fos = str(tmp_string).rfind('"skuAttr":"')
            tmp_val = tmp_string[sku_fos:]
            # print('\n tmp_val :' + str(tmp_val))

            if str(tmp_val) != "":
                tmp_skuAttr = getparse(str(tmp_val), '"skuAttr":"', '","')
                tmp_skuId = getparse(str(tmp_val), '"skuId":', ',"skuIdStr"')
                # print('\n tmp_skuAttr :' + str(tmp_skuAttr))
                # print('\n tmp_skuId :' + str(tmp_skuId))
            else:
                ren_flg_search = "X03"
                print('\n [X03] 옵션코드 확인 불가 : ' + str(ren_flg_search))

    if ren_flg_search == "" and tmp_skuAttr != "" and tmp_skuId != "":
        rtnCodeStr = tmp_skuAttr + "@" + tmp_skuId + "*" + tmp_inventory
        print('\n [OK] rtnCodeStr : ' + str(rtnCodeStr))
        return rtnCodeStr
    else:
        return ren_flg_search


def changeEngStr(in_optStr):

    rtnOptStr = ""
    tgOptStr = str(in_optStr).strip()

    if tgOptStr != "":
        if len(tgOptStr) == 2:
            if tgOptStr == "빨강" or tgOptStr == "빨간":
                rtnOptStr = "red"
            elif tgOptStr == "노랑" or tgOptStr == "노란":
                rtnOptStr = "yellow"
            elif tgOptStr == "파랑" or tgOptStr == "파란":
                rtnOptStr = "blue"
            elif tgOptStr == "분홍" or tgOptStr == "핑크":
                rtnOptStr = "pink"
            elif tgOptStr == "검정":
                rtnOptStr = "black"
            elif tgOptStr == "흰색":
                rtnOptStr = "white"
            elif tgOptStr == "보라":
                rtnOptStr = "puple"
            elif tgOptStr == "주황":
                rtnOptStr = "orange"
            elif tgOptStr == "회색":
                rtnOptStr = "grey"
        elif len(tgOptStr) == 3:
            if tgOptStr == "빨강색" or tgOptStr == "빨간색":
                rtnOptStr = "red"
            elif tgOptStr == "노랑색" or tgOptStr == "노란색":
                rtnOptStr = "yellow"
            elif tgOptStr == "파랑색" or tgOptStr == "파란색":
                rtnOptStr = "blue"
            elif tgOptStr == "분홍색" or tgOptStr == "핑크색":
                rtnOptStr = "pink"
            elif tgOptStr == "검정색":
                rtnOptStr = "black"
            elif tgOptStr == "보라색":
                rtnOptStr = "puple"
            elif tgOptStr == "주황색":
                rtnOptStr = "orange"

    print("\n [changeEngStr] rtnOptStr : " + str(rtnOptStr))
    return rtnOptStr

def isKoreanIncluded(in_word):
    in_word = str(in_word).strip()

    for i in in_word:
        if ord(i) > int('0x1100',16) and ord(i) < int('0x11ff',16) :
            return "1"
        if ord(i) > int('0x3131',16) and ord(i) < int('0x318e',16) :
            return "1"
        if ord(i) > int('0xa960',16) and ord(i) < int('0xa97c',16) :
            return "1"
        if ord(i) > int('0xac00',16) and ord(i) < int('0xd7a3',16) :
            return "1"
        if ord(i) > int('0xd7b0',16) and ord(i) < int('0xd7fb',16) :
            return "1"

    return "0"


def getNextUrl(in_drive, in_aliCode, in_optionTxt, in_ea):
    flg_search = ""
    fs_flg_opt = ""
    flg_opt = ""
    edt_optionstr = ""
    org_optionTxt = ""
    org2_optionTxt = ""
    v_skuAttr_uni = ""
    v_skuAttr = ""
    v_skuId = ""
    v_stock = 0
    find_str = ""
    move_url = ""
    matchFlg = "0"
    flg_Ship_from = ""
    v_ordEa = str(in_ea)
    in_optionTxt = str(in_optionTxt).strip()
    org_optionTxt = in_optionTxt
    print("\n [ORG] 옵션명 : " + str(org_optionTxt))

    if in_optionTxt == "":
        print('\n 옵션 없는 주문 : ' + str(in_optionTxt))
        fs_flg_opt = "0"
    else:
        print('\n 옵션 있는 주문 : ' + str(in_optionTxt))
        fs_flg_opt = "1"

    # 주문 옵션이 있는경우 옵션 코드 추출하기
    if fs_flg_opt == "1":

        # 첫번째 문자가 / 일경우 /제거
        if in_optionTxt[:1] == "/":
            in_optionTxt = in_optionTxt[1:]
            print('\n 첫번째 문자 /(슬러시) 제거 : ' + str(in_optionTxt))

        # / 슬러스 문자 검색 될 경우 : (예전 옵션) 1개이상 옵션 SKIP 대상
        fd_st2_pos = in_optionTxt.find('/')
        if fd_st2_pos > -1:
            flg_search = "S04"  # SKIP
            print("\n * 예전 옵션 (슬러시문자 1개이상) SKIP 대상 : " + str(flg_search))

        # ,수량 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st3_pos = in_optionTxt.find(',수량')
        if fd_st3_pos > -1:
            in_optionTxt = in_optionTxt[:fd_st3_pos]
            print('\n [옵션 ,수량 부분 제거] in_optionTxt : ' + str(in_optionTxt))

        # +( 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st4_pos = in_optionTxt.find('(+')
        if fd_st4_pos > -1:
            in_optionTxt = in_optionTxt[:fd_st4_pos]
            print('\n [옵션 +( 부분 제거] in_optionTxt : ' + str(in_optionTxt))
            org2_optionTxt = str(in_optionTxt)

        # 괄호 있는 옵션 #################################
        if in_optionTxt[:1] == "(":
            print("\n * 괄호 있는 옶션 : " + str(in_optionTxt))
            strPos = in_optionTxt.find(")")
            in_optionTxt = in_optionTxt[0:strPos + 1]
            opt_size = len(in_optionTxt)

            # 해당 옵션명이 중복으로 있는지 확인
            ov_pos = org_optionTxt.find(in_optionTxt)
            org_optionTxt = org_optionTxt[ov_pos + opt_size:]
            # print("\n ov_pos : " + str(ov_pos))
            print("\n [ORG] 옵션명 (코드 제외) : " + str(org_optionTxt))

            if org_optionTxt.find(in_optionTxt) == -1:
                flg_opt = "opt_new"
                in_optionTxt = in_optionTxt.replace("(", "")
                in_optionTxt = in_optionTxt.replace(")", "")
                edt_optionstr = in_optionTxt
                print("\n * NEW 옵션 case : " + str(flg_opt))

            else:  # 옵션명이 중복
                org2_optionTxt = org2_optionTxt.replace(in_optionTxt, "")
                edt_optionstr = org2_optionTxt
                sp_optcnt = edt_optionstr.split(":")
                print('\n 옵션 CNT : ' + str(len(sp_optcnt)))  # skip

                if len(sp_optcnt) == 2:
                    flg_opt = "opt_old"  # SKIP
                    print('\n * 예전 옵션 (괄호) CASE : ' + str(flg_opt))
                else:  # 옵션명이 중복이 2개이상 또는 2개이하의 경우 SKIP
                    flg_search = "S01"  # SKIP
                    print('\n (* 예전 옵션 (괄호 중복) SKIP 대상 : ' + str(flg_search))  # skip

        # 괄호 없는 옵션 #################################
        else:
            #if in_optionTxt[:2].isalpha() or in_optionTxt[:2].isdigit():
            if isKoreanIncluded(in_optionTxt) == "0":
                print("\n 괄호 없는 옵션 (영문자및 숫자) : " + str(in_optionTxt))
                if in_optionTxt.find("As ") == -1 and in_optionTxt.find("as ") == -1 and in_optionTxt.find("AS ") == -1:
                    flg_opt = "opt_old_2"
                    edt_optionstr = in_optionTxt
                    print('\n * 예전 옵션 (괄호 없음) CASE : ' + str(flg_opt))
                else:
                    flg_search = "S02"
                    print("\n * 예전 옵션 (괄호 없음) (As로 시작되는 옵션) SKIP 대상 : " + str(flg_search))
            else:
                print("\n 괄호 없는 옵션 (한글) : " + str(in_optionTxt))
                chgStr = changeEngStr(in_optionTxt)
                if chgStr == "":
                    flg_search = "S03"  # SKIP
                    print("\n * 예전 옵션 (괄호 없음) (한글옵션->영문변환 불가) SKIP 대상 : " + str(flg_search))
                else:
                    flg_opt = "opt_old_2"
                    edt_optionstr = chgStr
                    print('\n [ 한글옵션 -> 옵션 영문변환 ] : ' + str(in_optionTxt) + " -> " + str(chgStr))
                    print('\n * 예전 옵션 (괄호 없음) CASE : ' + str(flg_opt))

        print("\n >옵션 종류 : " + str(flg_opt))
        print("\n >정리한 옵션코드명 : " + str(in_optionTxt))
        print("\n >정리한 옵션명 : " + str(edt_optionstr))

    if flg_search != "":
        print("\n >주문 불가한 옵션 : " + str(flg_search))
        return str(flg_search)

    # 소스 가져오기 ######################################################################
    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')
    req_v = in_drive.page_source
    soup_v = BeautifulSoup(req_v, 'html.parser')
    # print('\n soup_v :' + str(soup_v))

    str_soup_list = ""
    str_soup = ""
    str_soup_list = getparse(str(soup_v), 'productSKUPropertyList":', '"skuPriceList":')
    str_soup = getparse(str(soup_v), '"skuPriceList":[', '"warrantyDetailJson"')
    soup_sp_cnt = 0
    ####################################################################################

    # 옵션 없음 ###############
    if str(str_soup_list) == "":
        if fs_flg_opt == "0":
            flg_opt = "opt_no"
            print('\n * 옵션 없는 CASE : ' + str(flg_opt))
        else:
            flg_search = "X01"
            print('\n [X01] 일치하는 옵션 없음 : ' + str(flg_search))

    # 옵션 있음 ###############
    else:
        soup_sp_cnt = len(str_soup_list.split('"skuPropertyName":')) - 1
        print('\n (소스) 옵션수 :' + str(soup_sp_cnt))

        if fs_flg_opt == "0":
            print('\n * (주문) 옵션은 없고 (소스) 옵션 있는 CASE ')

            sf_fos = str_soup_list.find(':"Ships From"')
            # print('\n sf_fos :' + str(sf_fos))
            if soup_sp_cnt == 1 and sf_fos > -1:
                flg_Ship_from = "1"
                shipFromRtn = getShipFromOptCode(str_soup_list)
                if str(shipFromRtn) != "":
                    print('\n (Ships From) 코드 :' + str(shipFromRtn))

                    # getSkuAttr 호출 (skuAttr, skuId)
                    rtn_Attr = getSkuAttr(str_soup, str(shipFromRtn))
                    if rtn_Attr == "X":
                        flg_search = rtn_Attr
                        print('\n [ 옵션 검색 불가 ] : ' + str(flg_search))
                    else:
                        v_skuAttr = getparse(str(rtn_Attr), '', '@')
                        v_skuId = getparse(str(rtn_Attr), '@', '*')
                        v_stock = getparse(str(rtn_Attr), '*', '')
                else:
                    flg_search = "X04"
                    print('\n [X04] Ship From : China 옵션 선택 불가 : ' + str(flg_search))
            else:
                flg_search = "S05"
                print('\n [S05] 옵션 있는 상품 (옵션 선택 확인필요) SKIP 대상 : ' + str(flg_search))

    # 예전 옵션 : 괄호 없는 옵션 및 괄호있는 예전 옵션 (괄호 제거후 옵션명으로 검색)
    if flg_search == "" and (flg_opt == "opt_old_2" or flg_opt == "opt_old"):
        print('\n >> 예전 옵션 : 괄호 없는 옵션 처리: ' + str(flg_opt))

        # skuPropertyName
        str_soup_old = getparse(str(soup_v), 'skuPropertyName":', '"skuPriceList":')
        # print('\n str_soup_old :' + str(str_soup_old))

        if str(str_soup_old) != "":
            soup_sp = str_soup_old.split('"skuPropertyName":')
            soup_sp_cnt = len(soup_sp)
            # print('\n soup_sp_cnt :' + str(soup_sp_cnt))

            opt_sp = edt_optionstr.split(":")
            opt_sp_cnt = len(opt_sp)
            # print('\n opt_sp :' + str(opt_sp))
            print('\n (주문) 옵션수 :' + str(opt_sp_cnt))

            k = 0
            tmp_sku = ""
            while k < opt_sp_cnt:
                soup_sp_v = str(soup_sp[k])
                #f_fos = soup_sp_v.find('"propertyValueDisplayName":"' + opt_sp[k].strip() + '"')
                f_fos = soup_sp_v.upper().find('"PROPERTYVALUEDISPLAYNAME":"' + opt_sp[k].strip().upper() + '"')
                if f_fos > -1:
                    if k > 0:
                        tmp_sku = tmp_sku + ","
                    tmp_sku = tmp_sku + getparse(soup_sp_v[f_fos:], 'propertyValueId":', ',"propertyValueIdLong')
                    print('\n tmp_sku :' + str(tmp_sku))
                k = k + 1

            if tmp_sku == "":
                flg_search = "X03"
                print('\n [ 옵션코드 확인 불가 ] : ' + str(flg_search))
            else:
                # getSkuAttr 호출 (skuAttr, skuId)
                rtn_Attr = getSkuAttr(str_soup, str(tmp_sku))
                if rtn_Attr == "X":
                    flg_search = rtn_Attr
                    print('\n [ 옵션 검색 불가 ] : ' + str(flg_search))
                else:
                    v_skuAttr = getparse(str(rtn_Attr), '', '@')
                    v_skuId = getparse(str(rtn_Attr), '@', '*')
                    v_stock = getparse(str(rtn_Attr), '*', '')

    # NEW 옵션 (괄호 있음) 경우
    if flg_search == "" and flg_opt == "opt_new":

        str_soup = getparse(str(soup_v), '"skuPriceList":[', '"warrantyDetailJson"')
        # print('\n str_soup :' + str(str_soup))

        find_str = edt_optionstr.replace(":", ",")
        print('\n (주문)옵션코드 :' + str(find_str))
        # print('\n str_soup :' + str(str_soup))

        option_sp = find_str.split(',')
        option_sp_cnt = len(option_sp)
        print('\n (주문) 옵션수 :' + str(option_sp_cnt))

        if str(soup_sp_cnt) != str(option_sp_cnt):
            print('\n 옵션수 불일치 :' + str(option_sp_cnt))

            f_fos2 = str_soup_list.find(':"Ships From"')
            # print('\n f_fos2 :' + str(f_fos2))
            if f_fos2 > -1:
                flg_Ship_from = "1"
                shipFromRtn = getShipFromOptCode(str_soup_list)

                if str(shipFromRtn) != "":
                    find_str = str(shipFromRtn) + "," + find_str
                    print('\n (변경)find_str :' + str(find_str))

        # getSkuAttr 호출 (skuAttr, skuId)
        rtn_Attr = getSkuAttr(str_soup, str(find_str))
        if rtn_Attr == "X":
            flg_search = rtn_Attr
            print('\n [ 옵션 검색 불가 ] : ' + str(flg_search))
        else:
            v_skuAttr = getparse(str(rtn_Attr), '', '@')
            v_skuId = getparse(str(rtn_Attr), '@', '*')
            v_stock = getparse(str(rtn_Attr), '*', '')
            # print('\n [ skuAttr ] :' + str(v_skuAttr))
            # print('\n [ skuId ] :' + str(v_skuId))

    # 옵션 없는 경우
    if flg_search == "" and flg_opt == "opt_no":
        print('\n >> 옵션 없음 : ' + str(flg_opt))
        v_skuId = getparse(str(str_soup), '"skuId":', ',"skuIdStr"')
        v_stock = getparse(str(str_soup), '"inventory":', ',')

    ##############################################################

    print('\n [ skuAttr ] :' + str(v_skuAttr))
    print('\n [ skuId ] :' + str(v_skuId))
    print('\n [ stock ] :' + str(v_stock))

    # 유티코드로 변경\
    if str(v_skuAttr).strip() != "":
        v_skuAttr_uni = str(v_skuAttr).replace(":", "%3A")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(";", "%3B")
        v_skuAttr_uni = str(v_skuAttr_uni).replace("#", "%23")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(" ", "+")
        print('\n [ 유니코드 변환 ] :' + str(v_skuAttr_uni))

    ship_company = "CAINIAO_STANDARD"
    move_url = "https://shoppingcart.aliexpress.com/order/confirm_order.htm?objectId=" + in_aliCode + "&from=aliexpress&countryCode=KR" + \
               "&shippingCompany=" + ship_company + \
               "&provinceCode=&cityCode=&promiseId=&aeOrderFrom=main_detail" + \
               "&skuAttr=" + v_skuAttr_uni + \
               "&skuId=" + v_skuId + \
               "&skucustomAttr=null" + \
               "&quantity=" + v_ordEa

    print("\n >> move_url : " + str(move_url))

    if flg_search == "" and (in_ea) > int(v_stock):
        flg_search = "X02"
        print('\n [X02] 해당옵션 재고부족 : ' + str(flg_search))
        print('\n 주문수량 : ' + str(in_ea) + ' | 재고수량 : ' + str(v_stock))

    ##############################################################

    print("\n [ORG] 옵션명 : " + str(org_optionTxt))
#############################################
    input("[1] Input Key : ")
#############################################

    if flg_search == "" and (flg_opt == "opt_new" or flg_opt == "opt_old" or flg_opt == "opt_old_2" or flg_opt == "opt_no"):
        return str(move_url)
    else:  # SKIP 대상 옵션
        return str(flg_search)


def replaceStr(in_value):
    tmpVal = ""
    tmpVal = str(in_value)
    tmpVal = tmpVal.replace("US", "")
    tmpVal = tmpVal.replace("$", "")
    tmpVal = tmpVal.strip()

    return tmpVal


def nextPageChk(in_drive):
    scrTest = ""
    chkScreenTxt = ""
    chkFlag = "1"

    time.sleep(1)
    print('\n time.sleep(1)')
    try:
        scrTest = in_drive.find_element_by_class_name('next-loading-wrap')
    except NoSuchElementException:
        print('NoSuchElementException')
    except TimeoutException:
        print('TimeoutException')
    finally:
        chkScreenTxt = str(scrTest.text).strip()
        if chkScreenTxt.find("Order Summary") >= 0 or chkScreenTxt.find("주문 내역 요약") >= 0:
            print('\n Next Page OK ')
            chkFlag = "0"
        else:
            # The Internet is not working. 인터넷이 작동하지 않습니다.
            print('\n Next Page Error ')

    return chkFlag


def orderCheck(in_driver, in_aliCode, in_chkFlg):
    rtnCheckCode = "0"

    if in_chkFlg == "SOLD_CHK":
        #### 상품 품절 체크 ###
        if goodsSoldOutChk(in_driver, in_aliCode) == "1":  ## 주문불가##
            print('\n 알리 상품 품절 (상품코드) ' + str(in_aliCode))

            # 알리 Home 이동
            wait = WebDriverWait(in_driver, 20)
            aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
            aHomebtn.click()
            print('\n 알리 Home 이동')
            rtnCheckCode = "S"

    if in_chkFlg == "KOR_DEV_CHK":
        #### 상품 한국배송가능 체크 ###
        if goodsDeliveryChk(in_driver, in_aliCode) == "1":  ## 주문불가##
            print('\n 한국배송 불가 : ' + str(in_aliCode))

            # 알리 Home 이동
            wait = WebDriverWait(in_driver, 20)
            aHomebtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.logo-base")))
            aHomebtn.click()
            print('\n 알리 Home 이동')
            rtnCheckCode = "K"

    return rtnCheckCode

def getSql(in_sql_kbn):

    sql = ""
    sql = sql + " select top 10 t.uid, OrderNo, SettlePrice + TotalDeliveryFee as SettlePrice, i.GoodsCode, isnull(i.ali_seller,''), o.item,i.sitecate, i.ea "
    sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.uid"
    sql = sql + " inner join  t_order_option as o on o.OrderInfoUid = i.uid"
    sql = sql + " where t.state = '200'"
    sql = sql + " and UserID <> 'kbw4798'"
    sql = sql + " and i.sitecate in ('fashion','electron','baby','furniture','beauty','jewelry','auto','sports','office','industry','fashion2','electron2','baby2','furniture2','beauty2','jewelry2','auto2','sports2','office2','industry2') "
    sql = sql + " and i.ali_seller is not null"
    sql = sql + " and t.RegDate >= '2020-08-24 18:00:00' and t.RegDate <= '2020-08-25 09:00:00'"
    sql = sql + " order by t.uid desc"

    print('\n [ sql ] :' + str(sql))

    return sql

def chkGetDrive(in_driver,in_url):
    rtnPageFlg = "0"

    try:
        wait = WebDriverWait(in_driver, 10)
        # my order 실행
        in_driver.get(in_url)
        print('\n [ in_driver.get ] : '+str(in_url))

    except NoSuchElementException:
        print('NoSuchElementException')
        rtnPageFlg = "x"
    except TimeoutException:
        print('TimeoutException')
        rtnPageFlg = "x"
    finally:
        if rtnPageFlg == "x":
            print('Error')
        else:
            print('Ok')

    return rtnPageFlg

def orderProcBase(in_driver, in_aliCode, in_optionstr, in_orderNo, in_ea):
    orderProcRtn = "0"

    print('\n {0} | {1}'.format(str(in_orderNo), str(in_aliCode)))

    # 알리 상품코드 입력
    time.sleep(1)
    print('\n time.sleep(1)')
    wait = WebDriverWait(in_driver, 20)
    in_driver.find_element_by_xpath('//*[@id="search-key"]').send_keys(in_aliCode)

    # 상품코드 검색창 버튼 클릭
    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')
    wait = WebDriverWait(in_driver, 20)
    aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-button")))
    aSearchBtn.click()

    time.sleep(1)
    print('\n time.sleep(1)')

    ####################################################################################################

    rtnCheck = orderCheck(in_driver, str(in_aliCode), "SOLD_CHK")
    if rtnCheck != "0":
        print('\n [ 알리 품절 (SKIP) ] :' + str(rtnCheck))
        return "1"

    rtnCheck = orderCheck(in_driver, str(in_aliCode), "KOR_DEV_CHK")
    if rtnCheck != "0":
        print('\n [ 알리 한국배송 불가 (SKIP) ] :' + str(rtnCheck))
        return "1"

    ####################################################################################################

    # Get : Next Page Url
    next_url = getNextUrl(in_driver, in_aliCode, str(in_optionstr), in_ea)
    print('\n [다음 화면 URL] :' + str(next_url))

    if next_url[:1] == "S" or next_url[:1] == "X":
        print('\n [ 진행불가 (SKIP) ] :' + str(next_url))
        return "1"

    # Next Page Url 실행
    mainDriver.get(next_url)
    print('\n [ NEXT PAGE CHECK ] ')

    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    # Next Page check
    chkNextFlg = nextPageChk(in_driver)
    print('\n chkNextFlg :' + str(chkNextFlg))
#############################################
    #input("[2] Input Key : ")
#############################################

    if chkNextFlg == "1":
        print('\n [ Next Page Error (SKIP) ] :' + str(chkNextFlg))
        return "1"
    ####################################################################################################

    # 결제화면:소계
    time.sleep(1)
    print('\n time.sleep(1)')
    orderPrices = in_driver.find_elements_by_class_name('charge-cost')
    scrMiniPrice = replaceStr(orderPrices[0].text)
    print('\n [결제화면] 소계 :' + scrMiniPrice)

    time.sleep(1)
    print('\n time.sleep(1)')
    # # my order
    myorder_url = "https://trade.aliexpress.com/orderList.htm"
    print('\n [myorder_url] :' + str(myorder_url))

    rtnGDFlg = chkGetDrive(in_driver, myorder_url)
    if rtnGDFlg == "x":
        print('\n 주문 에러 :' + str(rtnGDFlg))
        return rtnGDFlg

    # 소스 가져오기 ######################################################################
    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    req_my = in_driver.page_source
    soup_my = BeautifulSoup(req_my, 'html.parser')
    # print('\n soup_my :' + str(soup_my))
    time.sleep(1)
    print('\n time.sleep(1)')
    print('\n [ my order ] ')

    strSoupTmp = getparse(str(soup_my),'</thead>','</tfoot>')
    spSoupTmp = strSoupTmp.split('Order ID:')

    strNewOrderNo = getparse(str(spSoupTmp[1]), 'order_detail.htm?orderId=', '"')
    strOrderPrice = getparse(str(spSoupTmp[1]), '<p class="amount-num">', '</p>')
    strAliCode = getparse(str(spSoupTmp[1]), 'productid="', '"')

    print('\n strNewOrderNo :' + str(strNewOrderNo))
    print('\n strOrderPrice :' + str(strOrderPrice))
    print('\n strAliCode :' + str(strAliCode))

    # my order view 실행
    myorderview_url = "https://trade.aliexpress.com/order_detail.htm?orderId=" + strNewOrderNo
    print('\n [myorderview_url] :' + str(myorderview_url))

    # my order view 실행
    rtnGD2Flg = chkGetDrive(in_driver, myorderview_url)
    if rtnGD2Flg == "x":
        print('\n 주문 에러 :' + str(rtnGD2Flg))
        return rtnGD2Flg

    print('\n [ my order View ] ')

    # 소스 가져오기 ######################################################################
    time.sleep(1)
    print('\n time.sleep(1)')
    time.sleep(1)
    print('\n time.sleep(2)')

    req_myView = in_driver.page_source
    soup_myView = BeautifulSoup(req_myView, 'html.parser')
    # print('\n soup_myView :' + str(soup_myView))
    time.sleep(1)
    print('\n time.sleep(1)')

    str_sItemno = getparse(str(soup_myView),'productId=', '"')
    str_Zipno = getparse(str(soup_myView),'Zip Code:', 'Mobile:')
    str_Zipno = getparse(str(str_Zipno), 'Zip Code">', '</span>')
    print('\n str_sItemno :' + str(str_sItemno))
    print('\n str_Zipno :' + str(str_Zipno))


    input("[4] Input Key : ")

    return "0"
    ##########################################

# flg_search = "S01" # 예전 옵션 (괄호 중복) SKIP 대상
# flg_search = "S02" # 예전 옵션 (괄호 없음) ( As 로 시작되는 옵션) SKIP 대상
# flg_search = "S03" # 예전 옵션 (괄호 없음) (영문자및 숫자 아님) SKIP 대상
# flg_search = "S04" # 예전 옵션 (슬러시문자 1개이상) SKIP 대상
# flg_search = "S05" # [S05] 옵션 있는 상품 (옵션 선택 확인필요) SKIP 대상
# flg_search = "X01" # 일치하는 옵션 없음
# flg_search = "X02" # 해당옵션 재고부족
# flg_search = "X03" # 옵션코드 확인 불가
# flg_search = "X04" # Ship From : China 옵션 선택 불가
if __name__ == '__main__':

    now = datetime.datetime.now()
    print('\n [--- main Proc start ---] ' + str(now))

    path = "C:\\util\\chromedriver.exe"
    mainDriver = webdriver.Chrome(path)

    mainDriver.get('https://login.aliexpress.com/')
    # mainDriver.get('https://aliexpress.com/')

    # 로그인 ID/PASS 입력
    mainDriver.find_element_by_name('fm-login-id').send_keys('koiforever0526@gmail.com')
    mainDriver.find_element_by_name('fm-login-password').send_keys('uiop7890')

    time.sleep(1)

    # 로그인 버튼 클릭
    alogin = WebDriverWait(mainDriver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.fm-button")))
    alogin.click()

    time.sleep(1)
    print('\n time.sleep(1)')

    mainDriver.set_window_size(1300, 1000)
    time.sleep(1)
    print('\n time.sleep(1)')

    mainDriver.refresh()

    # aliCode = "4000311647220"
    # ord_optionstr = "Black:22mm Fenix5 6 935 (+500원)"  # 괄호 없는 옵션션
    # # aliCode = "4001123173769"  ## 옵션 3개 --> 정상 처리됨
    # # ord_optionstr = "(200141872:200844596:201336100)Yellow Star Mandala:210CM x 230CM:CHINA"
    # # aliCode = "32976778620"  ## 옵션 3개 --> 정상 처리됨
    # # ord_optionstr = "(352061)160315-16930(352061):16mm Grosgrain (+2,300)"
    #
    # aliCode = "32974577325"
    # ord_optionstr = "(193:200012239:201533809:201336100)Blue 5.3:8:오른손:CHINA"
    #
    # aliCode = "4000890788787"
    # ord_optionstr = "2:S"
    #
    # aliCode = "32846045160"
    # ord_optionstr = "(175)Blackish Green(175):8.0 (+8,400원)"
    #
    # aliCode = "33009072845"
    # ord_optionstr = "(200004889)30M X 1.1M X 1.8CM (+6,900) "
    #
    # aliCode = "4000221929931"
    # ord_optionstr = ""
    #
    # # aliCode = "32898037118"
    # # ord_optionstr = "China  "
    #
    # aliCode = "4000580757459"
    # ord_optionstr = "CHINA:Model B"
    #
    # ord_optionstr = str(ord_optionstr).strip()
    # d_ea = "2"  # 수량

    strSql = getSql("1")
    db.execute(strSql)
    ord_rows = db.fetchall()
    print('\n 처리할 주문 CNT :' + str(len(ord_rows)))

    icnt = 0
    if not ord_rows:
        print('\n 처리할 주문이 없습니다.')

    print('\n 처리할 주문 CNT :' + str(len(ord_rows)))
    for rs in ord_rows:
        procCheckFlag = "0"
        icnt = icnt + 1
        m_uid = rs[0]
        m_OrderNo = rs[1]
        m_SettlePrice = rs[2]
        m_GoodsCode = rs[3]
        m_ali_code = rs[4]
        m_ali_option = rs[5]
        m_ali_site= rs[6]
        m_ali_ea = rs[7]

        aliCode = m_ali_code
        ord_optionstr = str(m_ali_option).strip()

        print("\n ############## cnt : " + str(icnt) + "############")
        print("\n [주문] 알리코드 : " + str(aliCode))
        print("\n [주문] 옵션명 : " + str(ord_optionstr))
        print("\n [주문] 수량 : " + str(m_ali_ea))

####################################################################################################

        time.sleep(1)
        print('\n time.sleep(1)')
        mainDriver.refresh()

        # rtnBase = orderProcBase(mainDriver, aliCode, ord_optionstr, m_OrderNo, m_ali_ea)
        # if rtnBase == "0":
        #     print("\n 주문 OK : " + str(rtnBase))
        # else:
        #     print("\n 주문 SKIP : " + str(rtnBase))

        ######## Test ########
        procCheckFlag == "0"
        ######## Test ########

        if procCheckFlag == "0":
            main = mainDriver.window_handles
            last_tab = mainDriver.window_handles[len(main) - 1]
            # print('\n last_tab: ' + str(last_tab))
            if str(len(main)) != "1":
                for handle in main:
                    if handle != last_tab:
                        mainDriver.switch_to.window(window_name=handle)
                        mainDriver.close()
                    mainDriver.switch_to.window(window_name=last_tab)

            pmsg = '\n [--- orderProcBase Call Start ---] ' + str(datetime.datetime.now())
            print(pmsg)

            time.sleep(1)
            print('\n time.sleep(1)')

            rtnProcResult = orderProcBase(mainDriver, aliCode, ord_optionstr, m_OrderNo, m_ali_ea)
            if rtnProcResult == "0":
                print('\n 자동 주문 성공 : ' + str(m_OrderNo))

                # 알리 Home 이동
                wait = WebDriverWait(mainDriver, 20)
                mainDriver.get('https://aliexpress.com/')
                print('\n 알리 Home 이동')

            elif rtnProcResult == "X":
                print('\n 자동 주문 불가 (중단) : ' + str(m_OrderNo))
                print('\n 자동 주문 처리가 중단 되었습니다. [ Error ] ')
                time.sleep(1)
                print('\n time.sleep(1)')
                time.sleep(1)
                print('\n time.sleep(2)')
                mainDriver.quit()

            else:
                print('\n 자동주문 SKIP : ' + str(m_OrderNo))

                # 알리 Home 이동
                wait = WebDriverWait(mainDriver, 20)
                mainDriver.get('https://aliexpress.com/')
                print('\n 알리 Home 이동')


            pmsg = '\n [--- orderProcBase Call End ---] ' + str(datetime.datetime.now())
            print(pmsg)

#######################################################################################################


        # # 배송일 선택
        # time.sleep(1)
        # rtn_ship_code = shipping_price(mainDriver, aliCode, scrMiniPrice)
        # if rtn_ship_code != "0":
        #     print('\n 배송일 선택 불가 : ' + str(rtn_ship_code))
        #     ### 에러 처리 ###
        # else:
        #     print('\n 배송일 선택 완료 : ' + str(rtn_ship_code))
        #
        # ####################################################################################################
        #
        # # 결제화면: 배송비
        # time.sleep(2)
        # orderShipPrices = mainDriver.find_elements_by_class_name('charge-cost')
        # orderShipPrice = replaceStr(orderShipPrices[1].text)
        # print('\n [결제화면] 배송비 :' + orderShipPrice)
        #
        # # 결제화면: 총액
        # time.sleep(1)
        # ali_TotalPrice = mainDriver.find_element_by_class_name('total-cost').text
        # ali_TotalPrice = replaceStr(ali_TotalPrice)
        # print('\n [결제화면] 합계 결제금액 :' + str(ali_TotalPrice))

        ####################################################################################################
        # # my order
        # myorder_url = "https://trade.aliexpress.com/order_detail.htm?orderId=8017118985807399"
        # print('\n [myorder_url] :' + str(myorder_url))
        #
        # # my order 실행
        # mainDriver.get(myorder_url)
        # print('\n [ my order CHECK ] ')

        ####################################################################################################

    now = datetime.datetime.now()
    print('\n [--- main Proc End ---] ' + str(now))

