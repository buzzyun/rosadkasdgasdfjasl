import random
from stem import Signal
from stem.control import Controller
import socket
import time
import lxml
import sys
import selenium
import urllib
import cv2
from PIL import Image
from io import BytesIO
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
import os
#from phpserialize import serialize, unserialize
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from fake_useragent import UserAgent 
import datetime
import pyperclip
import func
from dbCon import DBmodule_FR

db_FS = DBmodule_FR.Database("freeship")

def connectDriver(tool):
    global set_browser

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    if tool == 'chrome':
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://ko.aliexpress.com/'")
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

def loginProc(in_driver, in_login_id, in_password):
    #로그인 복사 붙여넣기로 구현

    in_driver.implicitly_wait(5)
    pyperclip.copy(in_login_id)

    in_driver.find_element_by_name('fm-login-id').send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    in_driver.find_element_by_name('fm-login-id').send_keys(Keys.DELETE)
    print('>> fm-login-id (clear)')
    in_driver.find_element_by_name('fm-login-password').send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    in_driver.find_element_by_name('fm-login-password').send_keys(Keys.DELETE)
    print('>> fm-login-password (clear)')
    time.sleep(1)

    in_driver.find_element_by_name('fm-login-id').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    pyperclip.copy(in_password)
    in_driver.find_element_by_name('fm-login-password').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)


# getSkuAttr (skuAttr, skuId 검색)
def getSkuAttr(in_soup, in_opCode):
    ren_flg_search = ""
    tmp_skuAttr = ""
    tmp_skuId = ""
    rtnCodeStr = ""

    tmp_opCode = 'skuPropIds":"' + str(in_opCode)
    print('>> [검색 skuPropIds ] :' + str(tmp_opCode))

    t_fos = str(in_soup).find(tmp_opCode)
    # print('>> f_fos :' + str(f_fos))

    if t_fos == -1:
        ren_flg_search = "X01"
        print('>> [X01] 일치 하는 옵션 없음 : ' + str(ren_flg_search))
    else:
        tmp_string = in_soup[:t_fos]
        # 재고확인 (inventory)
        tmp_string_2 = func.getparse(str(in_soup), str(in_opCode), '"isActivity":')
        tmp_inventory = func.getparse(tmp_string_2, '"inventory":', ',')
        # print('>> tmp_string_2 :' + str(tmp_string_2))
        print('>> [ 옵션 재고수량 ] :' + str(tmp_inventory))

        if int(tmp_inventory) == 0:
            ren_flg_search = "X02"
            print('>> [X02] 해당옵션 재고없음 : ' + str(ren_flg_search))
        else:
            sku_fos = str(tmp_string).rfind('"skuAttr":"')
            tmp_val = tmp_string[sku_fos:]
            # print('>> tmp_val :' + str(tmp_val))

            if str(tmp_val) != "":
                tmp_skuAttr = func.getparse(str(tmp_val), '"skuAttr":"', '","')
                tmp_skuId = func.getparse(str(tmp_val), '"skuId":', ',"skuIdStr"')
                # print('>> tmp_skuAttr :' + str(tmp_skuAttr))
                # print('>> tmp_skuId :' + str(tmp_skuId))
            else:
                ren_flg_search = "X03"
                print('>> [X03] 옵션코드 확인 불가 : ' + str(ren_flg_search))

    if ren_flg_search == "" and tmp_skuAttr != "" and tmp_skuId != "":
        rtnCodeStr = tmp_skuAttr + "@" + tmp_skuId + "*" + tmp_inventory
        print('>> [OK] rtnCodeStr : ' + str(rtnCodeStr))
        return rtnCodeStr
    else:
        return ren_flg_search


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
    print(">> [ORG] 옵션명 : " + str(org_optionTxt))

    if in_optionTxt == "":
        print('>> 옵션 없는 주문 : ' + str(in_optionTxt))
        fs_flg_opt = "0"
    else:
        print('>> 옵션 있는 주문 : ' + str(in_optionTxt))
        fs_flg_opt = "1"

    # 주문 옵션이 있는경우 옵션 코드 추출하기
    if fs_flg_opt == "1":

        # 첫번째두번째 문자가 /: 일경우 /:제거
        if in_optionTxt[:2] == "/:":
            in_optionTxt = in_optionTxt[2:]
            print('>> 첫번째 문자 /(슬러시) 제거 : ' + str(in_optionTxt))

        # 첫번째 문자가 : 일경우 :제거
        if in_optionTxt[:1] == ":":
            in_optionTxt = in_optionTxt[1:]
            print('>> 첫번째 문자 :(슬러시) 제거 : ' + str(in_optionTxt))

        # 첫번째 문자가 / 일경우 /제거
        if in_optionTxt[:1] == "/":
            in_optionTxt = in_optionTxt[1:]
            print('>> 첫번째 문자 /(슬러시) 제거 : ' + str(in_optionTxt))

        # / 슬러스 문자 검색 될 경우 : (예전 옵션) 1개이상 옵션 SKIP 대상
        fd_st2_pos = in_optionTxt.find('/')
        if fd_st2_pos > -1:
            flg_search = "S04"  # SKIP
            print(">> * 예전 옵션 (슬러시문자 1개이상) SKIP 대상 : " + str(flg_search))

        # ,수량 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st3_pos = in_optionTxt.find(',수량')
        if fd_st3_pos > -1:
            in_optionTxt = in_optionTxt[:fd_st3_pos]
            print('>> [옵션 ,수량 부분 제거] in_optionTxt : ' + str(in_optionTxt))

        # +( 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st4_pos = in_optionTxt.find('(+')
        if fd_st4_pos > -1:
            in_optionTxt = in_optionTxt[:fd_st4_pos]
            print('>> [옵션 +( 부분 제거] in_optionTxt : ' + str(in_optionTxt))
            org2_optionTxt = str(in_optionTxt)

        # 괄호 있는 옵션 #################################
        if in_optionTxt[:1] == "(":
            print(">> * 괄호 있는 옶션 : " + str(in_optionTxt))
            strPos = in_optionTxt.find(")")
            in_optionTxt = in_optionTxt[0:strPos + 1]
            opt_size = len(in_optionTxt)

            # 해당 옵션명이 중복으로 있는지 확인
            ov_pos = org_optionTxt.find(in_optionTxt)
            org_optionTxt = org_optionTxt[ov_pos + opt_size:]
            # print(">> ov_pos : " + str(ov_pos))
            print(">> [ORG] 옵션명 (코드 제외) : " + str(org_optionTxt))

            if org_optionTxt.find(in_optionTxt) == -1:
                flg_opt = "opt_new"
                in_optionTxt = in_optionTxt.replace("(", "")
                in_optionTxt = in_optionTxt.replace(")", "")
                edt_optionstr = in_optionTxt
                print(">> * NEW 옵션 case : " + str(flg_opt))

            else:  # 옵션명이 중복
                org2_optionTxt = org2_optionTxt.replace(in_optionTxt, "")
                edt_optionstr = org2_optionTxt
                sp_optcnt = edt_optionstr.split(":")
                print('>> 옵션 CNT : ' + str(len(sp_optcnt)))  # skip

                if len(sp_optcnt) == 2:
                    flg_opt = "opt_old"  # SKIP
                    print('>> * 예전 옵션 (괄호) CASE : ' + str(flg_opt))
                else:  # 옵션명이 중복이 2개이상 또는 2개이하의 경우 SKIP
                    flg_search = "S01"  # SKIP
                    print('>> (* 예전 옵션 (괄호 중복) SKIP 대상 : ' + str(flg_search))  # skip

    # -----------------------------------------------------------------------------------
        print(">> 옵션 종류 : " + str(flg_opt))
        print(">> 정리한 옵션코드명 : " + str(in_optionTxt))
        print(">> 정리한 옵션명 : " + str(edt_optionstr))

    if flg_search != "":
        print(">> 주문 불가한 옵션 : " + str(flg_search))
        return str(flg_search)

    # 소스 가져오기 ######################################################################
    time.sleep(3)
    req_v = in_drive.page_source
    soup_v = BeautifulSoup(req_v, 'html.parser')
    # print('>> soup_v :' + str(soup_v))

    str_soup_list = ""
    str_soup = ""
    str_soup_list = func.getparse(str(soup_v), 'productSKUPropertyList":', '"skuPriceList":')
    str_soup = func.getparse(str(soup_v), '"skuPriceList":[', '"warrantyDetailJson"')
    soup_sp_cnt = 0
    ####################################################################################

    # 옵션 없음 ###############
    if str(str_soup_list) == "":
        if fs_flg_opt == "0":
            flg_opt = "opt_no"
            print('>> * 옵션 없는 CASE : ' + str(flg_opt))
        else:
            flg_search = "X01"
            print('>> [X01] 일치하는 옵션 없음 : ' + str(flg_search))

    # 옵션 있음 ###############
    else:
        soup_sp_cnt = len(str_soup_list.split('"skuPropertyName":')) - 1
        print('>> (소스) 옵션수 :' + str(soup_sp_cnt))

        if fs_flg_opt == "0":
            print('>> * (주문) 옵션은 없고 (소스) 옵션 있는 CASE ')

            sf_fos = str_soup_list.find(':"Ships From"')
            # print('>> sf_fos :' + str(sf_fos))
            if soup_sp_cnt == 1 and sf_fos > -1:
                flg_Ship_from = "1"
                v_skuAttr = func.getparse(str(rtn_Attr), '', '@')
                v_skuId = func.getparse(str(rtn_Attr), '@', '*')
                v_stock = func.getparse(str(rtn_Attr), '*', '')
            else:
                flg_search = "S05"
                print('>> [S05] 옵션 있는 상품 (옵션 선택 확인필요) SKIP 대상 : ' + str(flg_search))

    # 예전 옵션 : 괄호 없는 옵션 및 괄호있는 예전 옵션 (괄호 제거후 옵션명으로 검색)
    if flg_search == "" and (flg_opt == "opt_old_2" or flg_opt == "opt_old"):
        print('>> >> 예전 옵션 : 괄호 없는 옵션 처리: ' + str(flg_opt))

        # skuPropertyName
        str_soup_old = func.getparse(str(soup_v), 'skuPropertyName":', '"skuPriceList":')
        # print('>> str_soup_old :' + str(str_soup_old))

        if str(str_soup_old) != "":
            soup_sp = str_soup_old.split('"skuPropertyName":')
            soup_sp_cnt = len(soup_sp)
            # print('>> soup_sp_cnt :' + str(soup_sp_cnt))

            opt_sp = edt_optionstr.split(":")
            opt_sp_cnt = len(opt_sp)
            # print('>> opt_sp :' + str(opt_sp))
            print('>> (주문) 옵션수 :' + str(opt_sp_cnt))

            k = 0
            tmp_sku = ""
            while k < opt_sp_cnt:
                soup_sp_v = str(soup_sp[k])
                #f_fos = soup_sp_v.find('"propertyValueDisplayName":"' + opt_sp[k].strip() + '"')
                f_fos = soup_sp_v.upper().find('"PROPERTYVALUEDISPLAYNAME":"' + opt_sp[k].strip().upper() + '"')
                if f_fos > -1:
                    if k > 0:
                        tmp_sku = tmp_sku + ","
                    tmp_sku = tmp_sku + func.getparse(soup_sp_v[f_fos:], 'propertyValueId":', ',"propertyValueIdLong')
                    print('>> tmp_sku :' + str(tmp_sku))
                k = k + 1

            if tmp_sku == "":
                flg_search = "X03"
                print('>> [ 옵션코드 확인 불가 ] : ' + str(flg_search))
            else:
                # getSkuAttr 호출 (skuAttr, skuId)
                rtn_Attr = getSkuAttr(str_soup, str(tmp_sku))
                if rtn_Attr == "X":
                    flg_search = rtn_Attr
                    print('>> [ 옵션 검색 불가 ] : ' + str(flg_search))
                else:
                    v_skuAttr = func.getparse(str(rtn_Attr), '', '@')
                    v_skuId = func.getparse(str(rtn_Attr), '@', '*')
                    v_stock = func.getparse(str(rtn_Attr), '*', '')

    # NEW 옵션 (괄호 있음) 경우
    if flg_search == "" and flg_opt == "opt_new":

        str_soup = func.getparse(str(soup_v), '"skuPriceList":[', '"warrantyDetailJson"')
        # print('>> str_soup :' + str(str_soup))

        find_str = edt_optionstr.replace(":", ",")
        print('>> (주문)옵션코드 :' + str(find_str))
        # print('>> str_soup :' + str(str_soup))

        option_sp = find_str.split(',')
        option_sp_cnt = len(option_sp)
        print('>> (주문) 옵션수 :' + str(option_sp_cnt))

        if str(soup_sp_cnt) != str(option_sp_cnt):
            print('>> 옵션수 불일치 :' + str(option_sp_cnt))

            f_fos2 = str_soup_list.find(':"Ships From"')
            # print('>> f_fos2 :' + str(f_fos2))
            if f_fos2 > -1:
                flg_Ship_from = "1"

        # getSkuAttr 호출 (skuAttr, skuId)
        rtn_Attr = getSkuAttr(str_soup, str(find_str))
        if rtn_Attr == "X":
            flg_search = rtn_Attr
            print('>> [ 옵션 검색 불가 ] : ' + str(flg_search))
        else:
            v_skuAttr = func.getparse(str(rtn_Attr), '', '@')
            v_skuId = func.getparse(str(rtn_Attr), '@', '*')
            v_stock = func.getparse(str(rtn_Attr), '*', '')
            # print('>> [ skuAttr ] :' + str(v_skuAttr))
            # print('>> [ skuId ] :' + str(v_skuId))

    # 옵션 없는 경우
    if flg_search == "" and flg_opt == "opt_no":
        print('>> >> 옵션 없음 : ' + str(flg_opt))
        v_skuId = func.getparse(str(str_soup), '"skuId":', ',"skuIdStr"')
        v_stock = func.getparse(str(str_soup), '"inventory":', ',')

    ##############################################################

    print('>> [ skuAttr ] :' + str(v_skuAttr))
    print('>> [ skuId ] :' + str(v_skuId))
    print('>> [ stock ] :' + str(v_stock))

    # 유티코드로 변경
    if str(v_skuAttr).strip() != "":
        v_skuAttr_uni = str(v_skuAttr).replace(":", "%3A")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(";", "%3B")
        v_skuAttr_uni = str(v_skuAttr_uni).replace("#", "%23")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(" ", "+")
        print('>> [ 유니코드 변환 ] :' + str(v_skuAttr_uni))

    ship_company = "CAINIAO_STANDARD"
    move_url = "https://shoppingcart.aliexpress.com/order/confirm_order.htm?objectId=" + in_aliCode + \
    "&from=aliexpress&countryCode=KR" + \
    "&shippingCompany=" + ship_company + \
    "&provinceCode=&cityCode=&promiseId=&aeOrderFrom=main_detail" + \
    "&skuAttr=" + v_skuAttr_uni + \
    "&skuId=" + v_skuId + \
    "&skucustomAttr=null" + \
    "&quantity=" + v_ordEa

    print(">> >> move_url : " + str(move_url))

    if flg_search == "" and int(in_ea) > int(v_stock):
        flg_search = "X02"
        print('>> [X02] 해당옵션 재고부족 : ' + str(flg_search))
        print('>> 주문수량 : ' + str(in_ea) + ' | 재고수량 : ' + str(v_stock))

    ##############################################################

    print(">> [ORG] 옵션명 : " + str(org_optionTxt))
#############################################
    #input("[1] Input Key : ")
#############################################

    if flg_search == "" and (flg_opt == "opt_new" or flg_opt == "opt_old" or flg_opt == "opt_old_2" or flg_opt == "opt_no"):
        return str(move_url)
    else:  # SKIP 대상 옵션
        return str(flg_search)

def elem_clear(browser, elem):

    time.sleep(1)
    browser.find_elements_by_css_selector(elem)[0].send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    browser.find_elements_by_css_selector(elem)[0].send_keys(Keys.DELETE)
    time.sleep(1)
    browser.find_elements_by_css_selector(elem)[0].clear()
    time.sleep(1)

    return


def proc_order(browser, ali_temp):

    sp_tmp = str(ali_temp).split('@@')
    aliCode = sp_tmp[0]
    ord_optionstr = sp_tmp[1]
    d_ea = sp_tmp[2]
    ############################################
    # order_no 에 해당하는 주문내역 DB 에서 호출
    ############################################

    browser.get('https://aliexpress.com/')
    time.sleep(4)

    # 알리 상품코드 입력
    time.sleep(1)
    print('>> time.sleep(1)')
    wait = WebDriverWait(browser, 20)
    browser.find_element_by_xpath('//*[@id="search-key"]').send_keys(aliCode)

    # 상품코드 검색창 버튼 클릭
    time.sleep(2)
    print('>> time.sleep(2)')
    wait = WebDriverWait(browser, 20)
    aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-button")))
    if aSearchBtn:
        aSearchBtn.click()
    else:
        print(">> 상품코드 검색창 버튼 없음 확인필요. ")
        input(">> After Check Input : ")

    time.sleep(4)
    print('>> time.sleep(4)')

    result = browser.page_source()
    if str(result).find('"productId":'+str(aliCode)) > -1:
        print(">> aliCode Check Ok ")
    else:
        print(">> aliCode Check Error ")

    next_url = getNextUrl(browser, aliCode, str(ord_optionstr), d_ea)
    if next_url[:1] == "S" or next_url[:1] == "X":
        print('>> [ 진행불가 (SKIP) ] :' + str(next_url))
    else:
        # Next Page Url 실행
        browser.get(next_url)
        print('>> [ NEXT PAGE CHECK ] ')
        time.sleep(4)
        curr_source1 = browser.page_source
        time.sleep(1)

        # 주소 수정 버튼 클릭하기 #####################################################################
        if str(curr_source1).find('다른 주소를 선택') > -1:
            try:
                if browser.find_element_by_css_selector('div.address-list-opt > button:nth-child(2)'): #수정하기 버튼
                    browser.find_element_by_css_selector('div.address-list-opt > button:nth-child(2)').click()
            except Exception as e:
                print(">> 주소 수정 버튼 클릭 Exception ")
            else:
                print(">> 주소 수정 버튼 클릭 Ok ")
                    
        elif str(curr_source1).find('Change') > -1:
            try:
                if browser.find_element_by_xpath('//*[@id="placeorder_wrap__inner"]/div/div[1]/div[1]/div/div[2]/span/a'): #Change 버튼
                    browser.find_element_by_xpath('//*[@id="placeorder_wrap__inner"]/div/div[1]/div[1]/div/div[2]/span/a').click()
            except Exception as e:
                print(">> 주소 Change 버튼 클릭 Exception ")
            else:
                print(">> 주소 Change 버튼 클릭 Ok ")

        time.sleep(3)
        curr_source2 = browser.page_source
        time.sleep(1)

        # 배송주소 (기본) 수정하기 버튼 클릭 #####################################################################
        if str(curr_source2).find('수정하기') > -1:
            try:
                if browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/span/a'):
                    browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/span/a').click()
            except Exception as e:
                print(">> 배송주소 (기본) 수정하기 버튼 클릭 Exception ")
            else:
                print(">> 배송주소 (기본) 수정하기 버튼 클릭 Ok ")    
        elif str(curr_source2).find('수정') > -1:
            try:
                if browser.find_element_by_xpath('/html/body/div/div/div/div/div/ul/li[1]/div[2]/button[2]'):
                    browser.find_element_by_xpath('/html/body/div/div/div/div/div/ul/li[1]/div[2]/button[2]').click()
            except Exception as e:
                print(">> 배송주소 (기본) 수정 버튼 클릭 Exception ")
            else:
                print(">> 배송주소 (기본) 수정 버튼 클릭 Ok ")            
        else:
            try:
                if browser.find_elements_by_css_selector("[ae_page_area='Deliver_to_an_address']")[0]:
                    browser.find_elements_by_css_selector("[ae_page_area='Deliver_to_an_address']")[0].click()
            except Exception as e:
                print(">> 배송주소 (기본) change 버튼 클릭 Exception ")
            else:
                print(">> 배송주소 (기본) change 버튼 클릭 Ok ")    

        # 배송주소 입력하기 시작 #####################################################################
        time.sleep(3)
        curr_source3 = browser.page_source
        time.sleep(1)

        elem_clear(browser, "[placeholder='받는 사람']")
        elem_clear(browser, "[placeholder='휴대폰 번호*']")
        elem_clear(browser, "[placeholder='아파트, 사무실, 부서 등']")
        elem_clear(browser, "[placeholder='개인통관고유부호']")
        time.sleep(2)

        browser.find_elements_by_css_selector("[placeholder='받는 사람']")[0].send_keys('이름')
        time.sleep(2)
        browser.find_elements_by_css_selector("[placeholder='휴대폰 번호*']")[0].send_keys('01011112222')
        time.sleep(2)
    
        # 우편번호 검색
        elem = browser.find_element_by_xpath('//*[@id="halo-wrapper-root"]/div/div/form/div[3]/div[2]/div[1]/div/div/div/span/span[1]/input')
        elem.send_keys('47100')
        time.sleep(1)
        elem.send_keys(Keys.ENTER)
        time.sleep(4)
        browser.find_elements_by_css_selector("[placeholder='아파트, 사무실, 부서 등']")[0].send_keys('000동 000호')
        time.sleep(2)
        browser.find_elements_by_css_selector("[placeholder='개인통관고유부호']")[0].send_keys('P123456789123')

        time.sleep(2)
        # 배송 주소 편집  Confirm 클릭
        if browser.find_elements_by_css_selector('span.next-btn-helper')[0]:
            browser.find_elements_by_css_selector('span.next-btn-helper')[0].click()

        # 배송주소 입력하기 완료 #####################################################################

        time.sleep(3)
        curr_source4 = browser.page_source
        time.sleep(1)

        # 배송주소 (기본) 버튼 클릭 #####################################################################
        if str(curr_source4).find('기본') > -1:
            try:
                if browser.find_element_by_css_selector('span.cm-address-item-content-default-tag'):
                    browser.find_element_by_css_selector('span.cm-address-item-content-default-tag').click()
            except Exception as e:
                print(">> 배송주소 기본 버튼 클릭 Exception ")
            else:
                print(">> 배송주소 기본 버튼 클릭 Ok ")    


    print('>> time.sleep(3)')
    ###########################################################################
    #  전체 입력값 및 상품 체크 하기 
    #  상품 / 가격 / 수량 / 주소 / 총 배송비 / 총합계 
    ###########################################################################


    ###########################################################################
    #  주문내역 확인하기  
    #  해외주문번호 / 가격 / 상품정보 체크
    ###########################################################################
    browser.get('https://www.aliexpress.com/p/order/index.html')
    time.sleep(4)
    curr_source5 = browser.page_source
    time.sleep(1)

    if str(curr_source5).find('class="order-item"') > -1:
        print(">> Order List View OK ")
        new_order_no = ""
        sp_ord_list = str(browser.page_source).split('order-item-header-right-info')
        if len(sp_ord_list) > 0:
            ord_item = sp_ord_list[1]
            new_order_no = func.getparse(str(ord_item),'detail.html?orderId=','"')
            new_goods_no = func.getparse(str(ord_item),'aliexpress.com/item/','.html"')
            print(">> New Order No : {} | Goods No : {}".format(new_order_no, new_goods_no))
    else:
        print(">> Order List View Error ")

    input(">> Key Press : ")

    return "0"


def setShipTO(in_driver):
    rtnChkFlg = ""
    time.sleep(1)
    print('>> time.sleep(1)')

    # Currency 설정
    in_driver.find_element_by_css_selector('span.currency').click() #currency 클릭
    time.sleep(2)
    print('>> time.sleep(2)')
    currencyBtns = in_driver.find_elements_by_css_selector('span.select-item')
    currencyBtns[1].click()

    time.sleep(1)
    itemcurrSelUlBtns = in_driver.find_elements_by_css_selector('ul.notranslate')
    itemcurrSelLiBtns = itemcurrSelUlBtns[1].find_elements_by_tag_name('li')

    comments_text_cur = {}
    for num, comment in enumerate(itemcurrSelLiBtns):
        comments_text_cur[num] = comment
        txtShip = str(comments_text_cur[num].text)

        if txtShip.find('USD') == 0:
            comments_text_cur[num].click()
            chkUSDClick = "1"
            print("USD Click ")
            break

    print("Currency : USD 선택 OK ")
    time.sleep(1)
    print('>> time.sleep(1)')

    #Ship to 설정 저장 클릭
    mainDriver.find_element_by_css_selector('button.ui-button.ui-button-primary.go-contiune-btn').click()
    print('>> save button click')

    print('>> 배송국가 설정 및 Currency 설정 : ' +str(rtnChkFlg))

    return rtnChkFlg

def imgComp(fs_url, ali_url):
    
    # 프리쉽 상품 URL 이미지 다운로드
    #url = "https://office2.freeship.co.kr/goodsimg/56403\\2021-03-29/big/4000041507449.jpg"
    urllib.request.urlretrieve(str(fs_url), "test_fs.jpg")
    time.sleep(3)

    # 알리 상품 이미지 다운로드
    urllib.request.urlretrieve(str(ali_url), "test_ali.jpg")
    time.sleep(2)

    # 프리쉽 상품 이미지와 알리 상품 이미지 비교 
    imageA = cv2.imread("test_fs.jpg")
    imageB = cv2.imread("test_ali.jpg")
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    if len(grayA) == 0 or len(grayB) == 0:
        return "-1"

    # 이미지의 구조 비교
    if len(grayA)==len(grayB):
        print(" 이미지 구조 같음 ")
        return "0"
    else:
        print(" 이미지 구조 다름 ")
        return "1"

if __name__ == '__main__':

    now = datetime.datetime.now()
    print('>> [--- main Proc start ---] ' + str(now))
    currIp = socket.gethostbyname(socket.gethostname())
    currIp = str(currIp).strip()
    print(">> currIp : {}".format(currIp))

    loginId = 'koiforever0526@gmail.com'
    loginPass = 'uiop7890'
        
    currIp = "222.104.189.100"
    # 로그인 ID/PASS 입력
    if currIp != "222.104.189.18":
        sql = "select login_id, login_pw from ali_order_auto_set where login_ip = '{}'".format(currIp)
        row = db_FS.selectone(sql)
        if row:
            loginId = row[0]
            loginPass = row[1]

    time.sleep(2)
    mainDriver = connectDriver("chrome_secret")
    mainDriver.get('https://aliexpress.com/')
    #mainDriver.get('https://login.aliexpress.com/')
    time.sleep(3)

    #loginProc(mainDriver, loginId, loginPass)
    #time.sleep(3)

    # 로그인 버튼 클릭
    # alogin = WebDriverWait(mainDriver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.fm-button")))
    # alogin.click()
    #input(">> After login Key :")

    time.sleep(1)
    print('>> time.sleep(1)')

    mainDriver.set_window_size(1300, 1000)
    time.sleep(1)
    mainDriver.refresh()
    time.sleep(2)

    try:
        if mainDriver.find_element_by_css_selector('img.btn-close'):
            mainDriver.find_element_by_css_selector('img.btn-close').click()
    except Exception as e:
        print(">> pop up close Exception ")
    else:
        print(">> pop up close Ok ")

    time.sleep(1)
    setShipTO(mainDriver)




    # ali_temp = ['4000031771209@@(1052:100014065)Rose Red:XL@@2','32732081471@@/:(193)24V 65ML WEBASTO: (+2,450원),수량:1(옵션가:2450)@@1','1005003617224244@@:(361180:201336100)NL15874XL:CHINA:@@3','33003969449@@:(200971939:200004183)FIREBRICK:0.5MM:@@4']
    # for ali_ea in ali_temp:
    #     print(">> Item : {}".format(ali_ea))
    #     proc_order(mainDriver, ali_ea)

    # input(">> Key Press : ")

    db_FS.close()
    now = datetime.datetime.now()
    print('>> [--- main Proc End ---] ' + str(now))

