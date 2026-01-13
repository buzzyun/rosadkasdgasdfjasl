import requests
import datetime
import random
import socket
import socks
import http.client
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib
import time
import uuid
import os
import re
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

global g_exchange_rate
exchange_rate = "1350"

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

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

# def connectDriver(tool):
#     global set_browser

#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#     driver_path = f'./{chrome_ver}/chromedriver.exe'
#     if os.path.exists(driver_path):
#         print(f"chrom driver is insatlled: {driver_path}")
#     else:
#         print(f"install the chrome driver(ver: {chrome_ver})")
#         chromedriver_autoinstaller.install(True)

#     if tool == 'chrome':
#         time.sleep(1)
#         username = os.getenv("USERNAME")
#         userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
#         #options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
#         options.add_argument("user-data-dir={}".format(userProfile))
#         options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://www.ebay.com/'")
#         browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

#     elif tool == 'chrome_secret':
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         options.add_argument('--no-sandbox')  
#         options.add_argument("--incognito") # 시크릿 모드
#         ##options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
#                 random.random()) + " Safari/537.36, 'Referer': 'https://www.ebay.com/'")
#         browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

#     elif tool == 'brave':
#         path = "C:\\Project\\chromedriver.exe"
#         username = os.getenv("USERNAME")
#         userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#         options = webdriver.ChromeOptions()
#         brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         options.add_argument("user-data-dir={}".format(userProfile))
#         options.binary_location = brave_path
#         browser = webdriver.Chrome(executable_path=path, chrome_options=options)

#     elif tool == 'Firefox':

#         path = "C:\Project\cgeckodriver.exe"
#         profile = webdriver.FirefoxProfile()
#         profile.set_preference('network.proxy.type', 1)
#         profile.set_preference('network.proxy.socks', '127.0.0.1')
#         profile.set_preference('network.proxy.socks_port', 9150)
#         profile.update_preferences()
#         browser = webdriver.Firefox(profile, executable_path=path)

#     return browser

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    # checkIP()
    print(">> sql : {}".format(sql))
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip :', response.read())
    print('>> mac_addr :', mac_addr())

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

def setShipContry(browser):
    selRtn = "0"
    time.sleep(1)

    try:
        if browser.find_element(By.CSS_SELECTOR, '#DESCRIPTION_VHR_SHIPPING_TABS0-0-1-tabs-1 > span'):
            browser.find_element(By.CSS_SELECTOR, '#DESCRIPTION_VHR_SHIPPING_TABS0-0-1-tabs-1 > span').click()
            if browser.find_element(By.CSS_SELECTOR, '#shCountry'):
                curbtn= browser.find_element(By.CSS_SELECTOR, '#shCountry')
                curbtn.click()
                time.sleep(3)
                # itemscurrSel = curbtn.find_elements_by_tag_name('option')
                itemscurrSel = curbtn.find_elements(By.TAG_NAME, 'option')
                comments_text = {}
                for num, comment in enumerate(itemscurrSel):
                    comments_text[num] = comment
                    txtShip = str(comment.get_attribute('value'))
                    if txtShip == '1': # "United States"
                        comments_text[num].click()
                        print("United States Click ")
                        selRtn = "1"
                        break
                if selRtn != "1":
                    selRtn = "2"
                    print(">> United States 없음")
                else:
                    print(" {} 선택 OK ".format("United States"))
                    if browser.find_element(By.CSS_SELECTOR, '#shipping-calculator-form > div.ux-shipping-calculator__getRates > button'):
                        browser.find_element(By.CSS_SELECTOR, '#shipping-calculator-form > div.ux-shipping-calculator__getRates > button').click()
                        time.sleep(2)

    except Exception as ex:
        print('>> Exception :', ex)
        selRtn = "0"

    return selRtn

def getDescript(driver, desc_url):
    ### descript ###
    descript = ""
    descript_str = ""
    descript_url = str(desc_url).replace('amp;','')
    print('>> descript_url : {} '.format(descript_url))
    try:
        descript_result = requests.get(descript_url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        time.sleep(4)
        descript_str = descript_result.text
        #with open("result_descript.html","w",encoding="utf8") as f: 
        #    f.write(str(descript_str))
    except Exception as ex:
        print('>> Exception :', ex)
        print('>> No check')
        descript_str = ""
    else:
        time.sleep(0.5)
        #print(">> descript_str : {} ".format(str(descript_str)[:200]))
        soup_descript = BeautifulSoup(descript_str, 'html.parser')
        print('>> soup_descript : {}'.format(soup_descript.text[:100].replace("\n","")))

        if str(descript_str).find('<div class="page_out pageOut" id="simple">') > -1:
            descript_str = getparse(str(descript_str),'<div class="page_out pageOut" id="simple">','')
            if str(descript_str).find('<div class="layout footer_content"') > -1:
                descript_str = getparse(descript_str,'','<div class="layout footer_content"')

    return str(descript_str)

def get_imgoption_replace(img_str): #str.decode("utf8") 
    img_str = str(img_str).replace('u002F','').replace('\\','/').replace('"','').replace("s-l64.jpg","s-l640.jpg").replace("s-l64.png","s-l640.png").strip()
    return str(img_str)

def check_condtion(condition):
    refurb_value = ""
    if str(condition).find("Certified - Refurbished") > -1:
        print(">> Certified - Refurbished ")
        refurb_value = "1"
    elif str(condition).find("without ") > -1: # New without tags
        print(">> New without tags ")
        refurb_value = "2"
    elif str(condition).find("New—open box") > -1:
        print(">> New—open box ")
        refurb_value = "2"
    elif str(condition).find("New") > -1 or str(condition).find("New with tags") > -1 or str(condition).find("New with box") > -1 or str(condition).find("Brand new") > -1 or str(condition).find("New other") > -1: 
        print(">> New goods ")
        refurb_value = "0"
    else:
        print(">> check goods : {}".format(condition))
        refurb_value = "2"

    return str(refurb_value)

def getMemo(in_code):
    in_code_no = ""
    in_code_no = str(in_code[:3])
    rtnMemo = ""
    if in_code_no == "D01":
        rtnMemo = str(in_code) + ' : (Sold Out) Unsellable product'
    elif in_code_no == "D02":
        rtnMemo = str(in_code) + ' : (No Title) nsellable product'
    elif in_code_no == "D03":
        rtnMemo = str(in_code) + ' : (Fobidden) Unsellable product'
    elif in_code_no == "D04":
        rtnMemo = str(in_code) + ' : (Buy used) Unsellable product'
    elif in_code_no == "D44":
        rtnMemo = str(in_code) + ' : (New goods) Unsellable product'
    elif in_code_no == "D05":
        rtnMemo = str(in_code) + ' : (Add-on Item) Unsellable product'
    elif in_code_no == "D06":
        rtnMemo = str(in_code) + ' : (Temporarily out of stock) Unsellable product'
    elif in_code_no == "D46":
        rtnMemo = str(in_code) + ' : (more than stock) Unsellable product'
    elif in_code_no == "D07":
        rtnMemo = str(in_code) + ' : (option check) Unsellable product'
    elif in_code_no == "D47":
        rtnMemo = str(in_code) + ' : (option check) Unsellable option word'
    elif in_code_no == "D20":
        rtnMemo = str(in_code) + ' : (option check) 2 option price check'
    elif in_code_no == "D08":
        rtnMemo = str(in_code) + ' : (option price check) Unsellable product'
    elif in_code_no == "D48":
        rtnMemo = str(in_code) + ' : (goods price check) Unsellable product'
    elif in_code_no == "D49":
        rtnMemo = str(in_code) + ' : (shipping) Does not ship to US'
    elif in_code_no == "D09":
        rtnMemo = str(in_code) + ' : (max price over) Unsellable product'
    elif in_code_no == "D10":
        rtnMemo = str(in_code) + ' : (Pre-order) Unsellable product'
    elif in_code_no == "D11":
        rtnMemo = str(in_code) + ' : (shipping price over) Unsellable product'
    elif in_code_no == "D12":
        rtnMemo = str(in_code) + ' : (min price) Unsellable product'
    elif in_code_no == "D13":
        rtnMemo = str(in_code) + ' : (Pantry Goods) Unsellable product'
    elif in_code_no == "D17":
        rtnMemo = str(in_code) + ' : (No goodscode) Unsellable product'
    elif in_code_no == "T01":
        rtnMemo = str(in_code) + ' : tmall product'
    elif in_code_no == "D18":
        rtnMemo = str(in_code) + ' : (black-curtain-redirect) Unsellable product'
    elif in_code_no == "D19":
        rtnMemo = str(in_code) + ' : (No img) Unsellable product'
    elif in_code_no == "C01":
        rtnMemo = str(in_code) + ' : (Connection aborted(goods)) Url Connect Error'
    elif in_code_no == "C02":
        rtnMemo = str(in_code) + ' : (Connection aborted(option)) Url Connect Error'
    elif in_code_no == "C04":
        rtnMemo = str(in_code) + ' : blocked (captcha) Url blocked '
    elif in_code_no == "C05":
        rtnMemo = str(in_code) + ' : blocked  Url blocked '
    elif in_code_no == "C06":
        rtnMemo = str(in_code) + ' : Deliver to check '
    elif in_code_no == "C07":
        rtnMemo = str(in_code) + ' : (Title cannot be translated) Japanese included'        
    elif in_code_no == "E99":
        rtnMemo = str(in_code) + ' : error exit '
    elif in_code_no == "E01":
        rtnMemo = str(in_code) + ' : error check '
    elif in_code_no == "E02":
        rtnMemo = str(in_code) + ' : margin set error '
    elif in_code_no == "S01":
        rtnMemo = str(in_code) + ' : update stop goods (SKIP)'
    elif in_code_no == "S02":
        rtnMemo = str(in_code) + ' : naver noclick goods (SKIP)'
    elif in_code_no == "Q01":
        rtnMemo = str(in_code) + ' : setDB (Insert error)'
    elif in_code_no == "Q02":
        rtnMemo = str(in_code) + ' : setDB (Update error)'
    return rtnMemo

def get_replace_title(str_title):

    tmp_title = str(str_title).strip()
    tmp_title = tmp_title.replace("💥","").replace("✅","")
    tmp_title = tmp_title.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ').replace("&lt;","<").replace("&gt;",">")
    tmp_title = tmp_title.replace("&ndash;","-").replace("&times;"," x ").replace("&rdquo;","").replace('–','-').replace('「',' ').replace('」',' ')
    tmp_title = tmp_title.replace("&quot;","`").replace("\\", "").replace("★","").replace("◆","").replace('"', '').replace(',', ' ').replace('  ', ' ').strip()

    return tmp_title

# 특수단어 제거
def replaceQueryString(in_word) :
    result = in_word.replace("'","")
    result = result.replace("💥","").replace("✅","")
    result = result.replace("★","").replace("💥","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ").replace("–","-")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","").replace("  "," ")

    return result

def replaceOptionValue(in_word) :
    result = str(in_word)
    if result[:1] == '"':
        result = result[1:]
    if result[-1:] == '"':
        result = result[:-1]
    result = result.replace("'","").replace('"','`').replace('``','`')
    result = result.replace("★","").replace("◆","").replace("/"," . ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ").replace("–","-").replace('}','').replace('{','')
    result = result.replace("&#39;","`").replace("&#34;","`").replace("&quot;","").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")
    result = result.replace('\\u002F','').replace('u002F','').replace("\\", "").replace("  "," ").strip()

    return result

def getAddpirce(in_price, dic):
    f_price = 0
    f_price = float(in_price)

    if dic['exchange_rate'] == "" or dic['exchange_rate'] == "0":
        print(">> getAddpirce 오류 ")
        return "E02"
    else:
        wonprice = f_price * float(dic['rate_margin']) * float(dic['exchange_rate'])

    return int(round(wonprice, -2))

# mssql null
def getQueryValue(in_value):
    if in_value == None:
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

#옵션처리
def generateOptionString(dic):
    print(">> DB Option (generateOptionString)")
    #print(dic['subasin'])
    #print(str(len(dic['subasin'])))

    #print(dic['option_price'])
    #print(str(len(dic['option_price'])))

    minus_optflg = ""
    minus_optflg = dic['minus_opt']
    print(">> minus_optflg :"+str(minus_optflg))

    option_item = []
    for low in dic['subasin']:
        option_item_str = []

        if dic['option_price'].get(low):
            option_price_diff = getAddpirce(dic['option_price'][low],dic) - getAddpirce(dic['price'],dic)
            option_price_diff = int(round(option_price_diff, -2))
            print(str(low) + " : " + str(option_price_diff) + " = " + str(getAddpirce(dic['option_price'][low],dic)) + str(' - ') + str(getAddpirce(dic['price'],dic)))

            if minus_optflg == "1":
                if option_price_diff > 0:
                    option_price_diff = 0
                # if option_price_diff < 0:
                #     option_price_diff = int(round(option_price_diff / 2, -2))
            else:
                if option_price_diff < 0:
                    option_price_diff = 0    

            option_value = replaceQueryString(dic['option_value'][low])
            option_item_str.append(option_value)
            option_item_str.append(str(option_price_diff))
            option_item.append("/".join(option_item_str))

    return ",".join(option_item)

# replace
def replaceTitle(in_word, replace_title_list):
    target = str(in_word).upper()

    for rs in replace_title_list:
        replace_ban_title = rs[0]
        replace_title = rs[1]
        if str(replace_ban_title) != '' and replace_ban_title != None:

            if target.find(replace_ban_title.upper()) >= 0:
                target = target.replace(replace_ban_title.upper()," " + replace_title + " ")
                print('>> [replace (1)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.lower()) >= 0:
                target = target.replace(replace_ban_title.lower(), " " + replace_title + " ")
                print('>> [replace (2)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.capitalize()) >= 0 :
                target = target.replace(replace_ban_title.capitalize(), " " + replace_title + " ")
                print('>> [replace (3)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

    #print('[replace)] :' + str(target))
    return target

# (사이트DB 체크) 사이트내 금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_site(target, cate_idx, replace_site_title_list):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'

    for rs in replace_site_title_list:
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        ban_cate_idx = (rs[4]).strip()
        if ban_title_inner == None or ban_title_inner == '' : #case 1
            if ban_check == '1' :
                if target.lower().find(ban_title_gubun.lower()) == 0 :
                    result = "1"
                    print('>> [Forbidden (1) 1 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 1  : " + str(ban_title_gubun)
                    break
                elif target.lower().find(ban_title_gubun.lower()) > 0 :
                    forward_index = target.lower().find(ban_title_gubun.lower())
                    backward_index = target.lower().rfind(ban_title_gubun.lower())
                    if forward_index == backward_index :                        
                        check_str = target[forward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-1 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-1  : " + str(ban_title_gubun)                            
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-2 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-2  : " + str(ban_title_gubun)  
                                break                       
                    else:
                        check_str = target[forward_index-1]
                        backward_str = target[backward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-3 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-3  : " + str(ban_title_gubun)  
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-5 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-5  : " + str(ban_title_gubun)  
                                break
                        if backward_str == '' or backward_str ==' ' or backward_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-4 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-4  : " + str(ban_title_gubun) 
                            break
                        else:
                            backward_check_symbol = len(re.sub(parttern,'',backward_str))
                            if backward_check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-6 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-6  : " + str(ban_title_gubun)  
                                break  
            else :
                if target.lower().find(ban_title_gubun.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (1) 0 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 0 : " + str(ban_title_gubun)                    
                    break
        else:
            if ban_title_gubun_2 == None or ban_title_gubun_2 == '' : #case 2
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                    ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                    break
            else: #case 3
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 and target.lower().find(ban_title_gubun_2.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (3)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2))
                    ban_str = "Forbidden (3) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2)
                    break

    if result == "1":
        if ban_cate_idx != "":
            if str(ban_cate_idx) == str(cate_idx):
                result = result + '@' + ban_str
            else:
                result = "0"
                print(">> 금지어 제외안함 카테고리 다름 : (db){} (cateidx){}".format(ban_cate_idx, cate_idx))
        else:
            result = result + '@' + ban_str

    return result

#금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_new(target, ban_title_list):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'

    for rs in ban_title_list:
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        
        if ban_title_inner == None or ban_title_inner == '' : #case 1
            if ban_check == '1' :
                if target.lower().find(ban_title_gubun.lower()) == 0 :
                    result = "1"
                    print('>> [Forbidden (1) 1 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 1  : " + str(ban_title_gubun)
                    break
                elif target.lower().find(ban_title_gubun.lower()) > 0 :
                    forward_index = target.lower().find(ban_title_gubun.lower())
                    backward_index = target.lower().rfind(ban_title_gubun.lower())
                    
                    if forward_index == backward_index :                        
                        check_str = target[forward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-1 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-1  : " + str(ban_title_gubun)                            
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-2 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-2  : " + str(ban_title_gubun)  
                                break                            
                    else:
                        check_str = target[forward_index-1]
                        backward_str = target[backward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-3 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-3  : " + str(ban_title_gubun)  
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-5 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-5  : " + str(ban_title_gubun)  
                                break    
                        
                        if backward_str == '' or backward_str ==' ' or backward_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-4 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-4  : " + str(ban_title_gubun) 
                            break
                        else:
                            backward_check_symbol = len(re.sub(parttern,'',backward_str))
                            if backward_check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-6 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-6  : " + str(ban_title_gubun)  
                                break  
            else :
                if target.lower().find(ban_title_gubun.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (1) 0 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 0 : " + str(ban_title_gubun)                    
                    break
        else:
            if ban_title_gubun_2 == None or ban_title_gubun_2 == '' : #case 2
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                    ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                    break
            else: #case 3
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 and target.lower().find(ban_title_gubun_2.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (3)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2))
                    ban_str = "Forbidden (3) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2)
                    break

    if result == "1":
        result = result + '@' + ban_str

    return result

#reg 한글 체크
def regKrStrChk(in_str):
    result = ""
    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)
    if (regStr):
        result = "1"
    else:
        result = "0"
    return result

#reg 숫자점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9]', '', in_str)
    return result

def rep_option_price(in_str):
    valStr = str(in_str).replace(' ','')
    valStr = str(valStr).replace(',','').replace('US','').replace('$','').strip()
    return valStr

def setGoodsdelProc(db_con, in_DUid, in_DIsDisplay, in_DOptionKind):
    db_con.delete('t_goods_sub', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_category', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_option', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_content', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods', "uid = '{0}'".format(in_DUid))
    print('>> (setGoodsdelProc) t_goods (delete ok) : {}'.format(in_DUid))

    return "0"

def changeImgSize(ea_img):
    img_tmp = ""
    img_size = ""
    rtn_img = ea_img
    if str(rtn_img).find('i.ebayimg.com') > -1:
        img_tmp = getparseR(str(rtn_img),'/','')
        if img_tmp.find('s-l') > -1:
            img_size = getparse(str(img_tmp),'s-l','.')
            if int(img_size) < 640:
                rtn_img = str(rtn_img).replace('/s-l'+str(img_size)+str('.'), '/s-l640.')
                #print(">> size Edit ea_img : {}".format(ea_img))    

    return rtn_img

def getCondition(result):
    condition = ""
    if result.find('itemCondition">') > -1:
        condition = getparse(str(result),'itemCondition">','</div>')
        #print(">> itemCondition : {}".format(condition))
    elif result.find('d-item-condition-label') > -1:
        condition = getparse(str(result),'d-item-condition-label','')
        if condition.find('Quantity:') > -1:
            condition = getparse(str(condition),'','Quantity:')
        else:
            condition = getparse(str(condition),'','<div class="u-cb spcr ">')
        if str(condition).find("Condition:") > -1:
            condition = getparse(str(condition),'Condition:','')
        if str(condition).find('<span class="ux-textspans">') > -1:
            condition = getparse(str(condition),'<span class="ux-textspans">','</span>')
    elif result.find('-item-condition-label') > -1:
        condition = getparse(str(result),'-item-condition-label','')
        if condition.find('Quantity:') > -1:
            condition = getparse(str(condition),'','Quantity:')
        else:
            condition = getparse(str(condition),'','<div class="u-cb spcr ">')
        if str(condition).find("Condition:") > -1:
            condition = getparse(str(condition),'Condition:','')
        if str(condition).find('<span class="ux-textspans">') > -1:
            condition = getparse(str(condition),'<span class="ux-textspans">','</span>')
    return str(condition)


def getOptDisPlayName(optDic, optValue, optCnt):
    cnt = 0
    optionValue = ""
    for key, value in optDic.items():
        if value.find(optValue) > -1:
            dipMName = getparse(value,'"displayName":"','"')
            dipMName = dipMName.replace(":"," . ").replace(","," . ").replace("'","").replace("  "," ").strip()
            if dipMName != "":
                cnt = cnt + 1
            if optionValue == "":
                optionValue = dipMName
            else:
                optionValue = optionValue + " | " + dipMName

    if cnt != optCnt:
        print(">> Option Count Check Please : {}".format(cnt))
    return optionValue


def proc_asin_parse_brower(db_con, db_price, browser, asin_item, manage_dic):
    in_pg = manage_dic['pgName']
    sp_asin = asin_item.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    display_price = sp_asin[2]
    guid = ""
    guid = sp_asin[3]
    db_goodscode = ""

    goods = dict()
    goods['guid'] = guid
    goods['catecode'] = cateidx
    goods['asin'] = asin

    now_url = "https://www.ebay.com/itm/" + str(asin) 
    #now_url = "https://www.ebay.com/itm/" + str(asin) + "?country=111"
    print('\n\n>> now_url : ' + str(now_url)) 
    time.sleep(1)
    try:
        browser.get(now_url)
    except Exception as e:
        print(">> browser.get Except ")
        browser.refresh()
        time.sleep(10)
        return "C02"

    time.sleep(random.uniform(4,6))
    result = ""
    result = str(browser.page_source)
    # soup = BeautifulSoup(result, 'html.parser')
    time.sleep(1)
    # with open("result_ebay_" +str(asin)+ ".html","w",encoding="utf8") as f: 
    #     f.write(str(result))

    result = str(browser.page_source)
    if result.find('id="vi_main_img_fs"') == -1 and result.find('og:image" content="') == -1:
        time.sleep(4)

    result = str(browser.page_source)
    # 품절 체크
    rtn_sold = soldout_check(result)
    if str(rtn_sold) != "0":
        return rtn_sold

    if result.find('id="gh-eb-Geo-a-default"') > -1:
        if result.find('Current language English') == -1:
            print(">> 언어 설정 필요 ")
            try:
                browser.find_element(By.XPATH, '//*[@id="gh-eb-Geo-a-default"]/span[2]').click()
                time.sleep(1)
                browser.find_element(By.XPATH, '//*[@id="gh-eb-Geo-a-en"]/span[2]').click()
                time.sleep(2)
            except Exception as e:
                print(">> 언어 설정 Except ")

        result = browser.page_source
        if result.find('Current language English') == -1:
            print(">> 언어 설정 필요 (2)")
            return "E99"

    result = str(browser.page_source)
    # 품절 체크
    rtn_sold = soldout_check(result)
    if str(rtn_sold) != "0":
        return rtn_sold

    if result.find('id="binBtn_btn') == -1:
        print(">> No Button : Buy It Now (sold)")
        return "D01"

    if result.find('data-testid=x-bin-action') > -1 or result.find('data-testid="x-bin-action"') > -1:
        print(">> Buy It Now OK")
    else:
        print(">> No Button : Buy It Now (sold)")
        return "D01"

    if str(browser.page_source).find("Ship to United States") > -1:
            print(">> Ship to United States OK")
    elif str(browser.page_source).find('<span>Ship to</span>') > -1:
        # currContry = getparse(result,'ux-shipping-calculator__country','ux-shipping-calculator__getRates')
        # currContry = getparse(str(currContry),'<option value="1" selected="">','</option>')
        if str(browser.page_source).find('United States') > -1:
            print(">> shipping country : United States")
        else:
            print(">> shipping country : ")
            rtnFlg = setShipContry(browser)
            if rtnFlg == "0":
                input(">> shipping country 설정 필요 :")
            elif rtnFlg == "2":
                print('>> No United States (D48)')
                return "D48"                

    print(">> -------------------------------------- {} --------------------------------------  ".format(asin))
    result = str(result)
    title = ""
    if result.find('id="itemTitle"') > -1:
        title = getparse(result,'id="itemTitle"','</h1>')
        if str(title).find('>Details about  &nbsp;</span>') > -1: title = getparse(title,'>Details about  &nbsp;</span>','')
        if str(title).find('<span style="white-space: nowrap;">') > -1: title = getparse(title,'','<span style="white-space: nowrap;">')
        print(">> title (itemTitle) : {}".format(title))
    elif result.find('"og:title" content="') > -1:
        title = getparse(result,'"og:title" content="','">').replace('| eBay','')
        print(">> title (og:title) : {}".format(title))
    else: 
        print(">> No title : {}".format(asin))
    if title == "":
        if result.find('mainTitle') > -1:
            title = getparse(result,'mainTitle','</h1>')
            title = getparse(title,'--BOLD">','</span>').replace('| eBay','').replace('<!--F#f_7[0]-->','').replace('<!--F/-->','')
            print(">> title (mainTitle) : {}".format(title))

    title = get_replace_title(title)
    print(">> title : {}".format(title))
    # Access Denied  ---> 체크하기 
    if str(title).strip() == "":
        print('>> title NO ( Url Connect Error ) ')
        return "C01"

    if len(title) < 4:
        print('>> title len < 4 ')
        return "D02"

    db_OriginalPrice = 0
    db_org_title = ''
    db_old_title = ''
    db_Weight = '0'
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        db_org_title = ''
        db_old_title = ''
        db_Weight = '0'
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, order_ck, isnull(OriginalPrice,0) from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, order_ck, isnull(OriginalPrice,0) from t_goods where uid = '{0}'".format(guid)
    # checkIP()
    # print(">> sql : {}".format(sql))   
    try:
        rowUP = db_con.selectone(sql)
    except Exception as e:
        print('>> exception 1-2 (sql) : {}'.format(sql))
        # checkIP()
        time.sleep(30)
        # procLogSet(db_con, in_pg, " ( exception 1-2  ) exit - asin_item: " + str(asin_item))
        procEnd(db_con, browser)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_old_title = rowUP[6]
        db_order_ck = rowUP[7]
        db_OriginalPrice = rowUP[8]
        goods['guid'] = db_uid
        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid

        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"
        if str(db_Del_Naver) == "1":
            print('>> Del_Naver 1 (네이버 미노출상품) : ' + str(asin))
        if str(DB_stop_update) == "1":
            print('>> stop_update goods : ' + str(asin))
            return "S01"

    ########### title ###########
    goods_title = title.replace(r'\x26', ' & ').replace("'", "`").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('–','-').replace('・','.')
    goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '').replace('  ',' ')
    goods_title = replaceQueryString(goods_title)

    replace_title_list = manage_dic['replace_title_list']
    goods_title = replaceTitle(goods_title, replace_title_list)
    if goods_title == "E":
        print(">> ( exception replaceTitle  ) exit : " + str(asin))
        time.sleep(10)
        # checkIP()
        # procLogSet(db_con, in_pg, " ( exception replaceTitle ) exit - asin: " + str(asin))
        procEnd(db_con, browser)

    if goods_title[-1:] == ".":
        goods_title = goods_title[:-1]
    if goods_title[-1:] == "|":
        goods_title = goods_title[:-1]
    goods_title = str(goods_title).replace("  ", " ").strip()

    print('>> goods_title (final) : ' + str(goods_title[:80]))
    if str(goods_title).strip() == "" or len(goods_title) < 5:
        print('>> no title ')
        return "D02"

    ########### title (checkForbidden_new) ###########
    ban_title_list = manage_dic['ban_title_list']
    forbidden_flag = checkForbidden_new(title, ban_title_list)
    if forbidden_flag == "E":
        print(">> ( exception checkForbidden_new  ) exit : " + str(asin))
        time.sleep(10)
        # procLogSet(db_con, in_pg, " ( exception checkForbidden_new  ) exit - asin: " + str(asin))
        procEnd(db_con, browser)

    if str(forbidden_flag) == "0":
        pass
        #print('>> No checkForbidden_new: ' + str(forbidden_flag))
    else:
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # (사이트 DB) title 금지어 체크 ###########
    replace_site_title_list = manage_dic['replace_site_title_list']
    forbidden_flag_site = checkForbidden_site(title, cateidx, replace_site_title_list)
    if str(forbidden_flag_site) != "0":
        print('>> checkForbidden_site : '+str(forbidden_flag_site))
        return "D03 :" + " ( site: " + forbidden_flag_site[2:] + " ) "

    goods['forbidden'] = 'F'
    goods['goods_title'] = goods_title

    db_org_title = str(db_org_title).replace(",","").upper()
    if db_org_title == goods_title: # 기존 org title 과 파싱 title 비교
        print(">> 타이틀 변화없음 ")
        goods['goods_title'] = db_old_title # 기존 DB title 그대로 반영 

    goods['IT_title'] = goods_title
    goods['db_goodscode'] = str(db_goodscode)

    ### image ###
    imgB = ""
    other_img_set = []
    img_low = 0
    img_str_tmp = ""
    other_img_list = ""

    if result.find('ux-image-carousel zoom img-transition-medium') > -1 :
        img_str_tmp = getparse(str(result),'ux-image-carousel zoom img-transition-medium','')
        if img_str_tmp.find('Similar Items') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'','Similar Items')
        if img_str_tmp.find('id="RightSummaryPanel"') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'','id="RightSummaryPanel"')
        if img_str_tmp.find('<img alt=') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'<img alt=','')
        if img_str_tmp.find('"Opens image gallery"') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'','"Opens image gallery"')
        other_img_list = str(img_str_tmp).split('<img alt=')

    elif result.find('ux-image-carousel-item image') > -1 :
        img_str_tmp = getparse(str(result),'ux-image-carousel-item image','</>')
        if img_str_tmp.find('Similar Items') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'','Similar Items')
        if img_str_tmp.find('id="RightSummaryPanel"') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'','id="RightSummaryPanel"')
        if img_str_tmp.find('data-src=') > -1 :
            img_str_tmp = getparse(str(img_str_tmp),'data-src=','')
        other_img_list = str(img_str_tmp).split('data-src=')

    elif result.find('id="vi_main_img_fs"') > -1 :
        img_str_tmp = getparse(result,'id="vi_main_img_fs"','id="RightSummaryPanel"')
        if str(img_str_tmp).find('class="tdThumb"') > -1:
            img_str_tmp = getparse(img_str_tmp,'class="tdThumb"','')
            other_img_list = str(img_str_tmp).split('class="tdThumb"')
        elif str(img_str_tmp).find('img src=') > -1:
            img_str_tmp = getparse(img_str_tmp,'img src=','')
            if img_str_tmp.find('</div>') > -1:
                img_str_tmp = getparse(img_str_tmp,'','</div>')
            other_img_list = str(img_str_tmp).split('img src=')
        elif str(img_str_tmp).find('data-src=') > -1:
            img_str_tmp = getparse(img_str_tmp,'data-src=','')
            other_img_list = str(img_str_tmp).split('data-src=')

    elif result.find('class="ux-image-filmstrip-carousel"') > -1 :
        img_str_tmp = getparse(result,'class="ux-image-filmstrip-carousel"','</div>')
        img_str_tmp = getparse(img_str_tmp,'img src=','')
        other_img_list = str(img_str_tmp).split('img src=')

    ea_img = ""
    if img_str_tmp != "":
        for ea_other_img in other_img_list:
            if ea_other_img.find('src="') > -1:
                ea_img = getparse(ea_other_img, 'src="', '"')
            else:
                ea_img = getparse(ea_other_img, '"', '"')
            ea_img = str(ea_img).replace("}","").replace("{","")
            # print(">> [{}] ea_img : {}".format(img_low, ea_img))
            if (str(ea_img).find('i.ebayimg.com') > -1 or str(ea_img).find('//i3.') > -1 or str(ea_img).lower().find('.jpg') > -1 or str(ea_img).lower().find('.png') > -1 or str(ea_img).lower().find('.gif') > -1 ):
                ea_img = changeImgSize(ea_img)
                if ea_img != "":
                    img_low = img_low + 1
                    # dupcnt = other_img_set.count(ea_img)
                    # print(">> dupcnt : {} | ea_img : {}".format(dupcnt, ea_img))
                    other_img_set.append(ea_img)
                    if imgB == "" :
                        imgB = ea_img
                        print(">> imgB : {}".format(imgB))
                if img_low > 4:
                    break

    if str(imgB).strip() == "":
        if result.find('active image"') > -1:
            imgB = getparse(result,'active image"','</div>')
            if str(imgB).find('image.src =') > -1:
                imgB = getparse(imgB,'image.src =','"')
            else:
                imgB = getparse(imgB,' src="','"')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    if str(imgB).strip() == "":
        if result.find('id="icImg"') > -1:
            imgB = getparse(result,'id="icImg"','')
            imgB = getparse(imgB,'src="','"')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    if str(imgB).strip() == "":
        if result.find('"image":"') > -1:
            imgB = getparse(result,'"image":"','"')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    if str(imgB).strip() == "":
        if result.find('itemprop="image"') > -1:
            imgB = getparse(result,'itemprop="image"','')
            imgB = getparse(imgB,'src="','"')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    if str(imgB).strip() == "":
        if result.find('style="background-image: url') > -1:
            imgB = getparse(result,'style="background-image: url','')
            imgB = getparse(imgB,'(',')')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    if str(imgB).lower().find('.jpg') > -1 or str(imgB).lower().find('.jpeg') > -1 or str(imgB).lower().find('.png') > -1:
        pass
    else:
        if result.find('"image":"') > -1:
            imgB = getparse(result,'"image":"','"')
            imgB = changeImgSize(imgB)
            print(">> imgB : {}".format(imgB))

    ####### imgB 없으면  No img
    if str(imgB).strip() == "":
        print(">> No imag : {}".format(asin))
        print(">> (No img) Unsellable product : {}".format(asin))
        return "D19"

    if str(imgB).lower().find('.jpg') > -1 or str(imgB).lower().find('.jpeg') > -1 or str(imgB).lower().find('.png') > -1:
        pass
    else:
        print(">> No imag (.jpg .png 없음) : {}".format(asin))
        return "D19"
    imgB = str(imgB).replace("}","").replace("{","")

    sql = " select exchange_rate, coupon, rate_margin, withbuy_cost, price_min, price_min_plus,price_middle_from, price_middle_to, price_middle_plus, price_max, price_max_plus, price_plus, withbuy_cost_plus, price_middle_from2, price_middle_to2, price_middle_plus2 from python_version_manage where name = 'goods' "
    # checkIP()
    print(">> sql : {}".format(sql))
    try:
        row = db_con.selectone(sql)
    except Exception as e:
        print('>> exception 1-22 (sql) : {}'.format(sql))
        ## checkIP()
        time.sleep(30)
        # procLogSet(db_con, in_pg, " ( exception 1-2  ) exit - asin_item: " + str(asin_item))
        procEnd(db_con, browser)

    if not row:
        print(">> python_version_manage 오류 ")
        return "E02"
    else:
        exchange_rate = row[0]
        py_coupom = row[1]
        rate_margin = row[2]
        withbuy_cost = row[3]
        price_min = row[4]
        price_min_plus = row[5]
        price_middle_from = row[6]
        price_middle_to = row[7]
        price_middle_plus = row[8]
        price_max = row[9]
        price_max_plus = row[10]
        price_plus = row[11]
        withbuy_cost_plus = row[12]
        price_middle_from2 = row[13]
        price_middle_to2 = row[14]
        price_middle_plus2 = row[15]

    goods['exchange_rate'] = exchange_rate    
    goods['rate_margin'] = rate_margin
    goods['withbuy_cost'] = withbuy_cost
    goods['price_min'] = price_min    
    goods['price_min_plus'] = price_min_plus  
    goods['price_middle_from'] = price_middle_from 
    goods['price_middle_to'] = price_middle_to 
    goods['price_middle_plus'] = price_middle_plus 
    goods['price_max'] = price_max 
    goods['price_max_plus'] = price_max_plus 
    goods['price_plus'] = price_plus 
    goods['withbuy_cost_plus'] = withbuy_cost_plus
    goods['price_middle_from2'] = price_middle_from2
    goods['price_middle_to2'] = price_middle_to2 
    goods['price_middle_plus2'] = price_middle_plus2 

    condition = getCondition(result)
    if condition == "":
        print(">> condition 확인필요 : {}".format(condition))
        input(">> ")
    #print(">> condition-label : {}".format(condition))

    stock_check = ""
    stock_quantity = ""
    if result.find('id="qtySubTxt"') > -1:
        stock_quantity = getparse(str(result),'id="qtySubTxt"','</span>')
        stock_quantity = getparse(str(stock_quantity),'>','available').replace('More than','').replace('<span class="">','').strip()
        print(">> stock_quantity : {}".format(stock_quantity))
        stock_check = regRemoveText(stock_quantity).strip()
        if stock_check != "":
            if int(stock_check) < 1:
                print('>> More than {} '.format(stock_check))
                return "D46"  
        print(">> stock_check : {}".format(stock_check))

    flg_ref = ""
    goods['flg_ref'] = ''
    refurb_check = check_condtion(condition)
    if refurb_check == "1":
        flg_ref = "1"
        goods['flg_ref'] = '1'
        print(">> Certified - Refurbished Ok : {}".format(condition))
    else:
        if refurb_check == "0":
            flg_ref = "0"
            print(">> New (Skip) : {}".format(condition))
            #return "D44"
        else:
            print(">> (Buy used) condition no check : {}".format(condition))
            return "D04"

    sale_price = ""
    mainPrice_tmp = ""
    mainCur_price = ""
    origin_price = ""
    main_price = ""
    priceCurrency = ""

    if result.find('class="mainPrice"') > -1:
        mainPrice_tmp = getparse(str(result),'class="mainPrice"','</div>')
    elif result.find('itemprop="price"') > -1:
        mainPrice_tmp = getparse(str(result),'itemprop="price"','</div>')
    mainCur_price = getparse(str(mainPrice_tmp),'content="','</span>')
    mainCur_price = getparse(str(mainCur_price),'">','')
    if mainCur_price == "":
        mainPrice_tmp = getparse(str(result),'"priceCurrency":"','}')
        priceCurrency = getparse(str(mainPrice_tmp),'','"')
        if mainPrice_tmp.find('"price":"') > -1 and str(priceCurrency) == "USD":
            mainCur_price = getparse(str(mainPrice_tmp),'"price":"','"')

    if mainCur_price.find('US') > -1:
        main_price = getparse(str(mainPrice_tmp),'content="','"').replace(',','').strip()
    elif mainCur_price.find('GBP') > -1 or mainCur_price.find('AU') > -1 or mainCur_price.find('EUR') > -1 or mainCur_price.find('C') > -1: 
        print('>> No US price (D48)')
        return "D48" 
    elif priceCurrency == "USD" and mainCur_price != "":
        main_price = mainCur_price.replace(',','').strip()
    else:
        if result.find('"convertedBinPrice":"US $') > -1:
            convert_price = getparse(str(result),'"convertedBinPrice":"US $','"').replace(',','').strip()
            print(">> convert_price : {}".format(convert_price))
            main_price = convert_price
        elif result.find('convertedFromValue":') > -1:
            convert_price = getparse(str(result),'convertedFromValue":',',').replace(',','').strip()
            convert_curr = getparse(str(result),'convertedFromValue":','}')
            convert_curr = getparse(str(convert_curr),'convertedFromCurrency":"','"')
            if convert_curr == "USD" and convert_price != "":
                main_price = convert_price
            else:
                print('>> No main_price ')
                return "D01"            
        else:
            print('>> No main_price ')
            return "D01"                
    print(">> main_price : {}".format(main_price))
    if main_price == "":
        if result.find('discountedPrice":"') > -1:
            discountedPrice = getparse(str(result),'discountedPrice":"','"')
            print(">> discountedPrice : {}".format(discountedPrice))

    if result.find('id="vi-priceDetails"') > -1:
        origin_price = getparse(str(result),'id="vi-priceDetails"','</div>')
        origin_price = getparse(str(origin_price),'US $','</span>').replace(',','').strip()
        print(">> origin_price : {}".format(origin_price))
    if origin_price == "":
        if result.find('originalPrice":"') > -1:
            origin_price = getparse(str(result),'originalPrice":"','"').replace(',','').strip()
            print(">> origin_price (originalPrice) : {}".format(origin_price))

    if origin_price.find('US $') > -1 or origin_price.find('EUR') > -1:
        origin_price = getparse(str(origin_price),'US $','').replace(',','').replace("EUR","").strip()
        if main_price == "":
            main_price = origin_price
            print(">> origin_price -> main_price (1) : {}".format(main_price))

    if origin_price != "":
        if float(main_price) < float(origin_price):
            # 할인전 가격으로 수정 (List Price)
            main_price = origin_price
            print(">> origin_price -> main_price (3) : {}".format(main_price))

    if main_price == "":
        print('>> No main_price ')
        return "D01"

    if float(main_price) < 1:
        print('>> 1 달러 미만 (skip)')
        return "D12" + " ( " + str(main_price) + " ) "

    if float(main_price) > 1100:
        print('>> 1100 달러 over (skip)')
        return "D09" + " ( " + str(main_price) + " ) "

    base_min_price = float(main_price)
    base_top_price = float(main_price)
    goods['price'] = float(base_min_price)
    goods['price_tmp'] = float(base_min_price)  

    if result.find('qtyTextBox">') > -1:
        print(">> Quantity Ok ")

    # if result.find('Does not ship to Korea') > -1:
    #     print(">> Does not ship to Korea")
    #     return "D49"

    # 경매 상품 체크
    if result.find('Starting bid:') > -1 or  result.find('Current bid:') > -1 :
        print(">> 경매 상품 SKIP : {}".format(asin))
        print(">> (Buy used) Unsellable product : {}".format(condition))
        return "D04"

    # 경매 상품 체크
    if result.find('title="Auction:') > -1:
        print(">> 경매 상품 (Auction) SKIP : {}".format(asin))
        print(">> (Buy used) Unsellable product : {}".format(condition))
        return "D04"

    # Shipping: Free 체크

    ship_check_sour = getparse(str(result),'class="vim d-shipping-minview','<div class="u-cb spcr">')
    ship_check = str(ship_check_sour)
    if str(ship_check_sour).find('Shipping:') > -1:
        ship_check = getparse(str(ship_check_sour),'Shipping:','')
    if str(ship_check_sour).find('배송:') > -1:
        ship_check = getparse(str(ship_check_sour),'배송:','')

    if str(ship_check).find('not ship to United States') > -1:
        print(">> not ship to United States : {}".format(asin))
        return "D49"
    if str(ship_check).find('미국 배송 불가') > -1:
        print(">> 미국 배송 불가 : {}".format(asin))
        return "D49"
    if str(ship_check).find('United States') > -1 or str(ship_check).find('미국') > -1:
        pass
    else:
        print(">> not ship to United States : {}".format(asin))
        return "D49"
    ship_price = "0"
    goods['shipping_fee'] = 0
    if str(ship_check).find('class="ux-textspans ux-textspans--POSITIVE ux-textspans--BOLD">') > -1:
        ship_check = getparse(str(ship_check),'class="ux-textspans ux-textspans--POSITIVE ux-textspans--BOLD">','</span>')
    if str(ship_check).find('class="ux-textspans ux-textspans--BOLD">') > -1:
        ship_check = getparse(str(ship_check),'class="ux-textspans ux-textspans--BOLD">','</span>')
    if str(ship_check).find('FREE') > -1 or str(ship_check).find('Free') > -1 or str(ship_check).find('무료') > -1:
        print(">> 무료 배송 상품 OK ")
    else:
        print(">> 유료 배송 상품 OK ")
        ship_price = getparse(str(ship_check),'US $','</span>').strip()
        ship_price = ship_price.replace(",","")
        if ship_price != "" and ship_check_sour.find('to Korea, South via Global') > -1:
            print(">> 유료 배송 to Korea, South via Globa -> free ")
            ship_price = 0
            pass
        elif ship_price != "" and ship_check_sour.find(' Priority Shipping to Korea, South') > -1:
            print(">> 유료 배송  Priority Shipping to Korea, South -> free ")
            ship_price = 0
            pass
        elif ship_price == "":
            ship_price = 0
        else:
            if float(ship_price) > 20:
                print(">> (shipping price over) Unsellable product : {}".format(ship_price))
                return "D11"

    ship_from = ""
    if str(ship_check_sour).find('Located in:') > -1:
        ship_from = getparse(str(ship_check_sour),'Located in:','</span>')
        ship_from = getparseR(ship_from,",","").strip()
        print(">> ship_from : {}".format(ship_from))
    goods['ship_from'] = ship_from[:80]

    feature = ""
    result_feature = str(browser.page_source)
    feature = "<h3>Item specifics</h3>"
    if result_feature.find('data-testid="x-about-this-item">') > -1 :
        feature_tmp = getparse(result_feature,'data-testid="x-about-this-item">','')
        if feature_tmp.find('data-testid="d-item-description') > -1:
            feature_tmp = getparse(feature_tmp,'','data-testid="d-item-description')
        elif feature_tmp.find('role="tabpanel"') > -1:
            feature_tmp = getparse(feature_tmp,'','role="tabpanel"')

        sp_feature = str(feature_tmp).split('class="ux-labels-values__labels-content"')
        for ea_fea in sp_feature:
            if str(ea_fea).find('item--table-view">') > -1:
                continue
            feature_label = getparse(ea_fea,'class="ux-textspans">','</span>').replace("'","")
            feature_value = getparse(ea_fea,'class="ux-labels-values__values-content"','')
            feature_value = getparse(feature_value,'class="ux-textspans">','</span>').replace("'","")
            if feature_value.find('New: A brand-new') > -1:
                feature_value = "New"
            if feature_label != "":
                feature = feature + "<p><b>● " + feature_label + "</b> : " + feature_value + "</p>"

        feature = feature + "<br><br>"
        print(">> feature : {}".format(feature))
    feature = feature.replace("a href=","").replace("https://www.ebay.com","").replace("www.ebay.com","").replace("ebay.com","")
    soup_feature = BeautifulSoup(feature, 'html.parser')
    print(">> soup_feature (Item specifics) : {}".format(soup_feature.text[:100]))
    
    seller_return_ck = "0"
    seller_return_tmp = ""
    seller_return_tmp = getparse(str(result),'id="SRPSection"','Payments:')
    seller_return_tmp = getparse(str(seller_return_tmp),'Returns:','')
    if str(seller_return_tmp).find('Seller does not accept returns') > -1:
        seller_return_ck = "1"

    ########### option ###########    
    goods['minus_opt'] = ""
    goods['coupon'] = "" 
    goods['many_option'] = '0'
    goods['Items'] = ""
    goods['option_type'] = ""
    min_price = 0
    top_price = 0

    d_minus_opt = ""
    opmaxlen = 0
    option_count = 0
    option_kubun = "0"
    option_type_str = ""
    opmaxlen = 0

    ######### shipping_category_weight / catecode의 minus_opt 플래그 확인 #############################
    d_minus_opt = ""
    d_coupon = ""   
    c_weight = "0"
    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(weight,0) from t_category where CateCode = '{0}'".format(cateidx)
    # checkIP()
    # print(">> sql2 : {}".format(sql2))
    try:
        rsCate = db_con.selectone(sql2)
    except Exception as e:
        print('>> exception 1-3 (sql2) : {}'.format(sql2))
        # checkIP()
        time.sleep(30)
        # procLogSet(db_con, in_pg, " ( exception 1-3  ) exit - asin_item: " + str(asin_item))
        procEnd(db_con, browser)
    if rsCate:
        d_minus_opt = rsCate[0]
        d_minus_opt = str(d_minus_opt).strip()
        d_coupon = rsCate[1]
        c_weight = rsCate[2]
        #print('>> (DB) d_minus_opt : '+str(d_minus_opt))
        print('>> (DB) coupon : {}'.format(d_coupon))
    tmp_coupon = int(py_coupom)
    print('>> (set) coupon : {}'.format(tmp_coupon))
    goods['coupon'] = str(tmp_coupon)

    option_item_dic = dict()
    option_image_dic = dict()

    option_item_map = ""
    base_price_tmp = ""
    if str(result).find('"selectMenus"') == -1 :
        print(">> No option Goods : {}".format(asin))     
        option_kubun = "0" # 옵션 없음
        goods['many_option'] = '0'
        option_ck = None   
        base_price_tmp = float(base_min_price)
    else:
        option_ck = "300"
        option_kubun = "1" # 옵션 상품
        goods['many_option'] = '1'

        option_ids_tmp = getparse(result,'"selectMenus"','"menuItemMap"')
        sp_ids = str(option_ids_tmp).split('{"id"')
        option_count = len(sp_ids) -1 
        print(">> option Count : {}".format(option_count))

        menuItemMap = getparse(result,'"menuItemMap"','"variationsMap"')
        variationsMap = getparse(result,'"variationsMap"','"selectedVariationId"')
        if variationsMap.find('"menuItemPictureIndexMap"') > -1:
            variationsMap = getparse(variationsMap,'','"menuItemPictureIndexMap"')

        option_ids_dic = dict()
        option_value_dic = dict()
        option_price_dic = dict()
        option_image_dic = dict()
        subasin_set = []

        ########### option type ###########
        option_type = ""
        option_type = ""
        for ea_label in sp_ids:
            optLabel = getparse(str(ea_label),'displayLabel":"','"')
            if optLabel == "":
                continue
            if option_type == "":
                option_type = optLabel
            else:
                option_type = option_type + " | " + optLabel
        print(">> option_type : {} ".format(option_type))

        i = 0
        spMenu = menuItemMap.split('":{')
        for ea_ids in spMenu:
            if i == 0:
                i = i + 1
                continue
            ea_Id = getparse(str(ea_ids),'"valueId":',',')
            ea_item = getparse(str(ea_ids),'"valueId":','}')
            ea_dpname = getparse(str(ea_ids),'displayName":"',',')
            option_ids_dic[ea_Id] = ea_item
            i = i + 1
        # print(">> option_ids_dic : {}".format(option_ids_dic))

        rowCnt = 0
        spValMap = variationsMap.split('"updateModules":')
        for ea_val in spValMap:
            if rowCnt > 0:
                if str(ea_val).find('[]},"') > -1:
                    ea_valueId = getparse(str(ea_val),'[]},"','"')
                else:
                    ea_valueId = getparse(str(ea_val),'"','"')
            else:
                ea_valueId = getparse(str(ea_val),'"','"')

            if ea_valueId == "":
                continue
            if ea_val.find('value":') == -1:
                continue
            
            rowCnt = rowCnt + 1
            if ea_val.find('"convertedFromValue":') > -1:
                ea_price = getparse(str(ea_val),'"convertedFromValue":',',')
            elif ea_val.find('text":"US') > -1:
                ea_price = getparse(str(ea_val),'text":"US','"')
            else:
                if rowCnt != len(spValMap):
                    print(">> ea_price Check Please : [{}] {}".format(ea_valueId, ea_val))
                # with open(os.getcwd() + "/result_" +str(asin)+ ".html","w",encoding="utf8") as f: 
                #     f.write(str(result))
                # input(">> Key :")

            if len(ea_valueId) != 12 and str(ea_valueId).isdigit() == False:
                print(">> [{}] ea_valueId check please : {}".format(asin, ea_valueId))
                input(">> ea_valueId check please : ")

            ea_price = ea_price.replace('$','').replace(',','').replace('\\','').replace('/','').replace('ea','').replace('Ea','').strip()
            if ea_price != "":
                ea_name = getOptDisPlayName(option_ids_dic, ea_valueId, option_count)
                ea_name = replaceOptionValue(ea_name)
                ea_img = getparse(str(ea_val),'"thumbnailUrl":',',').replace('null','')
                if ea_img != "":
                    ea_img = get_imgoption_replace(ea_img)
                    option_image_dic[ea_name] = ea_img
                if ea_name == "":
                    #print(">> (Skip) No name [{}] {} | {} | {} ".format(rowCnt, ea_valueId, ea_name, ea_price))
                    pass
                elif ea_val.find('outOfStock":true') > -1:
                    print(">> (SoldOut) [{}] {} | {} | {} ".format(rowCnt, ea_valueId, ea_name, ea_price))
                else:
                    option_value_dic[ea_valueId] = ea_name
                    option_price_dic[ea_valueId] = ea_price
                    subasin_set.append(ea_valueId)
                    opmaxlen = opmaxlen + 1
                    print(">> [{}] {} | {} | {} ".format(rowCnt, ea_valueId, ea_name, ea_price))

        # print(">> option_value_dic : {}".format(option_value_dic))
        # print(">> option_price_dic : {}".format(option_price_dic))
        # print(">> subasin_set : {}".format(subasin_set))

        if option_count > 0 and opmaxlen == 0:
            # No Option
            print(">> Option Goods - opmaxlen :0 : {}".format(asin))
            print('>> option_value check .')

            # with open(os.getcwd() + "/result_" +str(asin)+ ".html","w",encoding="utf8") as f: 
            #     f.write(str(result))
            # with open(os.getcwd() + "/menuItemMap_" +str(asin)+ ".html","w",encoding="utf8") as f: 
            #     f.write(str(menuItemMap))
            # with open(os.getcwd() + "/variationsMap_" +str(asin)+ ".html","w",encoding="utf8") as f: 
            #     f.write(str(variationsMap))
            return "D07"

        opt_val_cnt = 0
        opt_price_cnt = 0
        if opmaxlen > 0:
            opt_val_cnt = len(option_value_dic)
            opt_price_cnt = len(option_price_dic)
            print('>> opt_val_cnt : {} | opt_price_cnt : {}'.format(opt_val_cnt,opt_price_cnt))
            if opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt == opt_price_cnt:
                print('>> option OK')
            elif opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt > opt_price_cnt:
                print('>> option_cnt  option_cnt  unmatch (Progress)')
            else:
                #procLogSet(db_con, in_pg, " {} : option (D07) : opt_val : {}  | opt_price : {} ").format(in_asin,opt_val_cnt,opt_price_cnt)
                print('>> option_value check (2) - opt_val_cnt : {} | opt_price_cnt : {}'.format(opt_val_cnt,opt_price_cnt))
                return "D07"

        # dic_price = option_price_dic.values()
        # min_price = min(dic_price)
        # top_price = max(dic_price)

        rcnt = 0
        for k, v in option_price_dic.items():
            if rcnt == 0:
                min_price = float(v)
                top_price = float(v)
            else:
                if float(v) > float(top_price):
                    top_price = float(v)
                if float(v) < float(min_price):
                    min_price = float(v)
            rcnt = rcnt + 1 

        print(">> min_price : {} top_price: {}".format(min_price, top_price))

        if min_price == 0 or min_price == 0.0:
            print(">> Option Min Price : 0 ")
        else:
            base_min_price = min_price
        if top_price == 0 or top_price == 0.0:
            print(">> Option Max Price : 0 ")
        else:
            base_top_price = top_price
        print(">> Option Max Price : {} | Option Min Price : {} ".format(base_top_price, base_min_price))
        if base_min_price == "" and base_top_price == "":
            base_min_price = goods['price']
            base_top_price = goods['price']
            print(">> Option Pirce No - price로 변경 Max Price : {} | Min Price : {} ".format(base_top_price, base_min_price))

        if d_minus_opt == "1": # 마이너스 옵션으로 set
            base_price_tmp = float(base_top_price)
            goods['price'] = float(base_top_price)
            goods['price_tmp'] = float(base_top_price)        
            print('>> 마이너스 옵션 set :' +str(base_price_tmp))
        else:
            base_price_tmp = float(base_min_price)
            goods['price'] = float(base_min_price)
            goods['price_tmp'] = float(base_min_price)        
            print('>> 플러스 옵션 set :' +str(base_price_tmp))

        goods['base_price'] = float(base_min_price)
        goods['base_tmp_price'] = float(base_top_price)

        #if d_coupon is None or d_coupon == "" or d_coupon == 0:
        tmp_coupon = int(py_coupom)

        goods['minus_opt'] = str(d_minus_opt)
        goods['coupon'] = str(tmp_coupon)
        print('>> (DB) goods minus_opt : '+str(goods['minus_opt']))

        goods['subasin'] = subasin_set
        goods['option_value'] = option_value_dic
        goods['option_price'] = option_price_dic
        goods['option_image'] = option_image_dic

        ########### option Item / option type ###########
        if option_count == 0:
            print('>>option_count : 0 ')
        else:
            goods['Items'] = getQueryValue(generateOptionString(goods))
            goods['option_type'] = option_type
            print('>> Items :  ' + str(goods['Items']))
            print('>> option_type :  ' + str(option_type))

            ##### price check #####
            if float(base_min_price) < 1 or str(base_min_price) == "":
                print('>> 1 달러 미만 (skip)')
                return "D12" + " ( " + str(base_min_price) + " ) "  # 1 달러 미만
            if float(base_top_price) > 1100:
                print('>> 1100 달러 over (skip)')
                return "D09" + " ( " + str(base_top_price) + " ) "  # 1100 달러 over

    descript = ""
    if result.find('data-testid="d-item-description">') > -1:
        descript = getparse(result,'data-testid="d-item-description">','')
        if descript.find('<div class="tab-pane "') > -1:
            descript = getparse(str(descript),'','<div class="tab-pane "')
        if descript.find('<div id="promotionsCntr"') > -1:
            descript = getparse(str(descript),'','<div id="promotionsCntr"')
        if descript.find('<div id="desc_wrapper_ctr">') > -1:
            descript = getparse(str(descript),'<div id="desc_wrapper_ctr">','')
        descript_url = getparse(descript,'src="','"')
        if str(descript_url) != "":
            descript = getDescript(browser, descript_url)

    if descript == "" and result.find('id="desc_div"') > -1:
        #descript = getparse(result,'id="desc_div"','</div>')
        descript = getparse(result,'id="desc_div"','<div id="FootPanel">')
        if descript.find('<div class="tab-pane "') > -1:
            descript = getparse(str(descript),'','<div class="tab-pane "')
        if descript.find('<div id="promotionsCntr"') > -1:
            descript = getparse(str(descript),'','<div id="promotionsCntr"')
        if descript.find('<div id="desc_wrapper_ctr">') > -1:
            descript = getparse(str(descript),'<div id="desc_wrapper_ctr">','')
        descript_url = getparse(descript,'src="','"')
        descript = getDescript(browser, descript_url)

    if descript == "" and result.find('<div class="tab-content-m ">') > -1:
        descript = getparse(str(result),'<div class="tab-content-m ">','<div id="FootPanel">')
        if descript.find('<div class="tab-pane "') > -1:
            descript = getparse(str(descript),'','<div class="tab-pane "')
        if descript.find('<div id="promotionsCntr"') > -1:
            descript = getparse(str(descript),'','<div id="promotionsCntr"')
        if descript.find('<div id="desc_wrapper_ctr">') > -1:
            descript = getparse(str(descript),'<div id="desc_wrapper_ctr">','')
        #with open("result_ebay_descript.html","w",encoding="utf8") as f: 
        #    f.write(str(descript))

        if str(descript).find('<div class="page_out pageOut" id="simple">') > -1:
            descript = getparse(str(descript),'<div class="page_out pageOut" id="simple">','')
            if str(descript).find('<div class="layout footer_content"') > -1:
                descript = getparse(descript,'','<div class="layout footer_content"')
    else:
        print(">> No descript : {}".format(asin))
    #descript = str(descript).replace("a href=","").replace("href=","").replace("https://www.ebay.com","").replace("https://i.ebayimg.com","").replace("https://pages.ebay.com","").replace("https://stores.ebay.com","").replace("www.ebay.com","").replace("stores.ebay.com","").replace("i.ebayimg.com","").replace("pages.ebay.com","").replace("ebay.com","")
    descript = str(descript).replace("https://www.ebay.com","").replace("https://pages.ebay.com","").replace("https://stores.ebay.com","").replace("www.ebay.com","").replace("stores.ebay.com","").replace("pages.ebay.com","")
    descript = str(descript).replace('a href="','a href="##').replace('target="_blank"','')
    descript = str(descript).replace('id="csgGalleryContainer"','id="csgGalleryContainer" style="display: none"')

    goods['naver_img'] = None
    goods['mainimage'] = imgB
    goods['image'] = other_img_set

    goods['db_Weight'] = db_Weight
    goods['feature'] = feature
    goods['description'] = descript
    goods['stock_tmp'] = stock_check
    goods['optionkind'] = option_ck

    ########### shipping_weight ###########
    shipping_weight = "0"
    print('>> shipping_weight : ' + str(shipping_weight))
    print('>> db_Weight : ' + str(db_Weight))

    # DB 무게 입력이 있을경우 
    if float(shipping_weight) < float(db_Weight):
        shipping_weight = db_Weight
    # 카테고리 무게 입력이 있을경우 
    if float(shipping_weight) < float(c_weight):
        shipping_weight = c_weight

    goods['shipping_weight'] = shipping_weight
    # withbuy
    shipping_withbuy = getWithbuyFee(goods['shipping_weight'], withbuy_cost, withbuy_cost_plus, tmp_coupon)
    print('>> shipping_withbuy  : ' + str(shipping_withbuy))
    if str(shipping_withbuy) == "" or str(shipping_withbuy) == "0" or str(shipping_withbuy) == "0.0":
        shipping_withbuy = withbuy_cost / ((100-tmp_coupon)/100)
        print('>> withbuy_cost 플러스 : ' + str(shipping_withbuy))
        if str(shipping_withbuy) == "":
            shipping_withbuy = 18500
            print('>> shipping_withbuy 없음 18,500원 설정 : ' + str(shipping_withbuy))

    # ref 유료배송비
    goods['shipping_fee_tmp'] = str(ship_price)[:10]
    ref_shipping_fee = float(ship_price) * float(exchange_rate)
    print(">> ref_shipping_fee : {} ".format(ref_shipping_fee))

    shipping_fee = float(ref_shipping_fee) / ((100-tmp_coupon)/100)
    goods['shipping_fee'] = int(round(shipping_fee, -2))

    # 유료배송비 (ebay local 배송비)
    shipping_fee = goods['shipping_fee']
    print('>> 유료배송비 (ebay local 배송비) : ' + str(shipping_fee))

    ########### goodsmoney ###########
    goodsmoney = 0
    goodsmoney = getAddpirce_plus(goods, goods['price'], base_price_tmp) + int(shipping_fee) + int(shipping_withbuy)
    goodsmoney = int(round(goodsmoney, -2))
    print(">> goodsmoney (Sum) : {} ".format(goodsmoney))

    if int(goodsmoney) > 5000000:
        print('>> 5백만원 over (skip)')
        return "D09" + " ( " + str(goodsmoney) + " ) "  # 500백만원 over

    if goods['minus_opt'] == "1":
        diff_plus = 0
        diff_plus = float(goods['base_tmp_price']) - float(goods['base_price'])
        print('>> diff_plus : ' + str(diff_plus) + " = " + str(goods['base_tmp_price']) + " - " + str(goods['base_price']))
        diff_plus = (diff_plus * float(goods['exchange_rate']) * float(goods['rate_margin'])) * (tmp_coupon / 100) * (100 / (100-tmp_coupon))
        print('>> diff_plus (2) : ' + str(diff_plus))

        goodsmoney = goodsmoney + float(diff_plus)
        goodsmoney = int(round(goodsmoney, -2))
        print('>> goodsmoney (after) : ' + str(goodsmoney))
        
        sale_price = str(int(goodsmoney) * (100-tmp_coupon) / 100)
        print('>> (sale price) : {}'.format(sale_price))
    else:
        sale_price = str(int(goodsmoney) * (100-tmp_coupon) / 100)
        print('>> (sale price) : {}'.format(sale_price))

    goods['goodsmoney'] = goodsmoney
    print('>> goodsmoney : ' + str(goodsmoney))
    sale_price = str(int(goodsmoney) * (100-tmp_coupon) / 100)
    print('>> (sale price) : {}'.format(sale_price)) 

    low_price = float(goods['price']) * float(exchange_rate) + (int(shipping_fee) * (100-tmp_coupon) / 100)  + (int(shipping_withbuy) * (100-tmp_coupon) / 100)
    print('>> low_price : {} (환율 {}) + {} + {} = {}'.format(float(goods['price']) * float(exchange_rate), exchange_rate, (int(shipping_fee) * (100-tmp_coupon) / 100), (int(shipping_withbuy) * (100-tmp_coupon) / 100), int(low_price)))
    low_price = int(low_price)
    print('>> low_price (최저원가) : ' + str(low_price))
    goods['low_price'] = low_price
    goods['shipping_withbuy'] = shipping_withbuy
    goods['seller_return_ck'] = seller_return_ck
    goods['db_OriginalPrice'] = float(db_OriginalPrice)

    #DB set
    rtnDBflg = setDB_proc(asin, goods, db_con, db_price, in_pg, guid)
    sel_goodscode = ""
    if rtnDBflg[:2] != "0@":
        if rtnDBflg == "D01":
            print(">> ## t_goods Option /0 없음 에러 (품절처리 필요)  ##")
            return "D01"
        else:
            print('>> setDB error --> DB check Rollback ')
            sql = "select top 1 uid,IsDisplay,OptionKind from t_goods where ali_no = '{0}'".format(asin)
            # checkIP()
            print(">> sql : {}".format(sql))
            row = db_con.selectone(sql)
            if not row:
                print(">> ## t_goods Insert No goods (OK) ##")
            else:
                DUid = row[0]
                DIsDisplay = row[1]
                DOptionKind = row[2]
                # 상품 삭제처리 
                setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
                # print('\n >> t_goods Insert (delete)')
            return str(rtnDBflg) # exit
    else:
        sel_goodscode = getparse(rtnDBflg,"0@","")
        sql_i = "insert into goods_title_tran (goodscode, asin_no, Title) values ('{}', '{}',dbo.GetCutStr('{}',240,'...'))".format(sel_goodscode, asin, goods_title)
        db_org_title = str(db_org_title).replace(",","").upper()
        if db_org_title == goods_title: # 기존 org title 과 파싱 title 비교
            print(">> 타이틀 변화없음 ")
            if regKrStrChk(db_old_title) == "0": # 기존 DB title 한글번역 없을경우 번역 대상
                print(">> 한글 없음 번역 Insert : {} ".format(asin))
                db_con.execute(sql_i)
        else:
            print(">> 타이틀 번역 Insert : {} ".format(asin))
            db_con.execute(sql_i)


    return "0"


def getAddpirce_plus(dic, in_price, in_base_price):
    f_price = 0
    f_base_price = 0
    f_price = float(in_price)
    f_base_price = float(in_base_price)

    if dic['exchange_rate'] == "" or dic['rate_margin'] == "0":
        print(">> getAddpirce 오류 ")
        return "E02"
    else:
        add_plus = dic['price_plus']
        if f_base_price <= dic['price_min']:
            add_plus = dic['price_min_plus']
        elif f_base_price > dic['price_middle_from'] and f_base_price <= dic['price_middle_to']:
            add_plus = dic['price_middle_plus']
        elif f_base_price > dic['price_middle_from2'] and f_base_price <= dic['price_middle_to2']:
            add_plus = dic['price_middle_plus2']
        elif f_base_price > dic['price_max']:
            add_plus = dic['price_max_plus']

        wonprice = f_price * float(dic['rate_margin']) * float(dic['exchange_rate']) + add_plus
        print(">> " + str(wonprice) + " : " + str(f_price) + " * (g_rate_margin : " + str(dic['rate_margin']) + " * (g_exchange_rate) : " + str(dic['exchange_rate']) + " + (add_plus) : "+str(add_plus))

    return int(round(wonprice, -2))

#withbuy
def getWithbuyFee(in_weight, withbuy_base, withbuy_base_plus, in_coupon):
    withbuy_shipping_fee = 0
    # 추가요금 : 일본 2,000원 / 독일 2,400원 / 영국 2,700원 / 미국 2,500원 
    # 기본요금 (1키로): 일본 10,000원 / 독일 14,900원 / 영국 14,000원 / 미국 9,000원 
    base_fee = withbuy_base / ((100-in_coupon)/100)
    #print('>>Withbuy (base_fee) : {}'.format(base_fee)) 
    if float(in_weight) > 1:
        plus_fee = float(withbuy_base_plus) / ((100-in_coupon)/100)
        add_shipping_fee = ((float(in_weight) / 0.5) - 2 ) * plus_fee 
        withbuy_shipping_fee = base_fee + add_shipping_fee
        if float(in_weight) > 10:
            withbuy_shipping_fee = withbuy_shipping_fee + 20000 + plus_fee
    else:
        withbuy_shipping_fee = base_fee

    return int(round(withbuy_shipping_fee, -2))

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(currIp) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

#goodscode
def getGoodsCode(uid,goodshead):
    result = goodshead+str(uid).zfill(10)
    return result

# contents
def generateContent(dic):
    feature_item = []
    description_item = []
    content_item = []
    description = []
    feature = []

    #feature_item.append('<br><br><font color="orange"><b>Item specifics</b></font><br><br><br><br>')
    #description_item.append('<br><br><br><font color="red"><b>Description</b></font><br><br><br>')
    feature_item.append('<br><br><br><font color="red"><b>Description</b></font><br><br><br>')

    feature_item.append("".join(dic['feature']))
    feature = "".join(feature_item)
    description_item.append(dic['description'].replace("'","").replace("Description",""))
    description = "".join(description_item)

    if dic['optionkind'] == '300' or dic['optionkind'] == 300:
        option_img_set = []
        for key,values in dic['option_image'].items():
            if str(values) == '<br>' or str(values) == '':
                print(">> option_image values 없음 : "+str(values))
            else:
                option_img_set.append('<Font color=blue><pre><b>[ {0} ]</b></pre></FONT><br><img src="{1}"><br><br>'.format(key,values))
        opt_img_item = "".join(option_img_set)
        content_item.append(opt_img_item.replace("'",""))
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(description.replace("'","").replace("・","·"))
    else:
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(description.replace("'",""))        

    return "".join(content_item)

#DB set
def setDB_proc(in_asin, dic, db_con, db_price, in_pg, in_guid):
    global g_exchange_rate
    err_flg = "0"
    rtn_goodscode = ""
    print('>> setDB in_guid : {} '.format(in_guid))
    print('>> setDB start : {} '.format(in_pg))
    print('>> [asin] : {} '.format(in_asin))

    goods_title = dic['goods_title']
    dic['ali_no'] = in_asin
    originalprice = float(dic['price']) * float(dic['exchange_rate'])
    originalprice = int(originalprice)
    print('>> price : ' + str(dic['price']))
    print('>> originalprice (rate:' +str(dic['exchange_rate'])+ ') : ' + str(originalprice))

    ##### price check #####
    if float(dic['price']) < 1:
        print('>> 1 달러 미만 (skip)')
        return "D12" + " ( " + str(dic['price']) + " ) "  # 1 달러 미만

    # DB query
    goodsinfo_dic = dict()
    goodsinfo_dic['SiteID'] = "'rental'"
    goodsinfo_dic['DealerID'] = "'rental'"
    goodsinfo_dic['GoodsType'] = "'N'"
    goodsinfo_dic['Title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['IT_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['IT_title'])

    goodsinfo_dic['ImgB'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgM'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgS'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['naver_img'] = getQueryValue(dic['naver_img'])
    goodsinfo_dic['OptionKind'] = getQueryValue(dic['optionkind'])
    goodsinfo_dic['DeliveryPolicy'] = "'990'"
    goodsinfo_dic['State'] = "'100'"
    #########################goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
    goodsinfo_dic['price_tmp'] = getQueryValue(dic['price_tmp'])
    goodsinfo_dic['withbuy_price_tmp'] = getQueryValue(dic['shipping_withbuy'])
    goodsinfo_dic['OriginalPrice'] = originalprice
    goodsinfo_dic['ali_no'] = getQueryValue(dic['ali_no'])
    goodsinfo_dic['cate_idx'] = dic['catecode']
    goodsinfo_dic['E_title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['shipping_fee'] = getQueryValue(dic['shipping_fee'])
    goodsinfo_dic['shipping_fee_tmp'] = getQueryValue(dic['shipping_fee_tmp'])
    goodsinfo_dic['shipping_weight'] = getQueryValue(dic['shipping_weight'])
    goodsinfo_dic['stock_tmp'] = getQueryValue(dic['stock_tmp'])
    goodsinfo_dic['ship_from'] = getQueryValue(dic['ship_from'])
    goodsinfo_dic['flg_ref'] = getQueryValue(dic['flg_ref'])
    goodsinfo_dic['seller_return_ck'] = getQueryValue(dic['seller_return_ck'])

    many_option_ck = dic['many_option']
    if many_option_ck == '1' :
        goodsinfo_dic['many_option'] = "'1'"

    #other img
    otherimg_low = 1
    for otherimg in dic['image']:
        if otherimg_low <= 5:
            goodsinfo_dic['other_img_chk_'+str(otherimg_low)] = "'1'"
            goodsinfo_dic['other_img'+str(otherimg_low)] = getQueryValue(otherimg)
        otherimg_low += 1

    ##############################################
    #option (goodsinfo_option_dic)
    ##############################################
    goodsinfo_option_dic = dict()
    if dic['optionkind'] == '300' or dic['optionkind'] == 300:
        goodsinfo_option_dic['Title'] = getQueryValue(replaceQueryString(dic['option_type']))
        goodsinfo_option_dic['Items'] = dic['Items']

        if str(goodsinfo_option_dic['Items']).find('/0') > -1:
            print('>> Opt 기본옵션 /0 포함 ')
        else:
            print('>> Opt 기본옵션 /0 없음 (SKIP) ')
            print(dic['Items'])
            return "D01"

        print('>> option (type) : '+str(dic['option_type']))
        print('>> option (final) : ')
        print(goodsinfo_option_dic['Items'])

        goodsinfo_option_dic['Sort'] = 1
        goodsinfo_option_dic['ali_no'] = getQueryValue(dic['ali_no'])

    ##############################################
    #t_goods_content
    ##############################################
    goodsinfo_content_dic = dict()
    goodsinfo_content_dic['Content'] = "N" + getQueryValue(generateContent(dic))

    ##############################################
    #t_goods_sub
    ##############################################
    goodsinfo_sub_dic = dict()
    goodsinfo_sub_dic['Product'] = "'US'"

    ##############################################
    # t_goods_category
    ##############################################
    goodsinfo_cate_dic = dict()
    goodsinfo_cate_dic['CateCode'] = dic['catecode']
    goodsinfo_cate_dic['Sort'] = 1

    #input("Key input setDB : ")
    ck_isdisplay = ""
    ck_delnaver = ""
    searchFlg = "0"
    D_ali_no = ""
    D_naver_in = ""
    procFlg = ""
    if str(in_guid) == '' or in_guid is None or in_guid == 'None':
        procFlg = "N"

        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where ali_no = '{0}' ".format(dic['ali_no'])
        print('>> ## t_goods table 검색 (1) (ali_no) : {}'.format(dic['ali_no']))
        rows = db_con.selectone(sql)

        if not rows:
            procFlg = "N"          
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): {}".format(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"
        print(' procFlg : '+str(procFlg))  
    else:
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where uid = {0} ".format(in_guid)
        print('>> ## t_goods table 검색 (2) (no asin) ')  
        rows = db_con.selectone(sql)

        if rows:
            procFlg = "U" 
            old_guid = rows[0]
            ck_isdisplay = rows[1]
            ck_delnaver = rows[2]
            D_ali_no = rows[3]
            D_goodscode = rows[4]
            D_naver_in = rows[5]
            rtn_goodscode = D_goodscode    
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"

    if procFlg == "N":
        if dic['goodsmoney'] < 18000:
            dic['goodsmoney'] = 18000
        goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])        
        goodsinfo_dic['confirm_goods'] = 1 
        goodsinfo_dic['naver_price_ck'] = "'0'"
        #####################################################################
        print(">> ## setDB New Insert : " + str(in_asin))
        #####################################################################
        #insert t_goods
        try:
            db_con.insert('t_goods',goodsinfo_dic)
            print('>> ## t_goods  insert ')
        except Exception as e:
            print('>> Exception [t_goods]', e)
            err_flg = "1"
            return "Q01"

        time.sleep(1)
        #goodscode #######################
        sql = "select top 1 uid from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        coderow = db_con.selectone(sql)
        now_guid = coderow[0]         
        new_goodscode = getGoodsCode(now_guid, 'R')
        print('>> new_goodscode : '+str(new_goodscode))
        rtn_goodscode = new_goodscode
        err_flg = "0"

        if str(new_goodscode) == "":
            print('>> goodscode 생성 오류 (Q01) : '+str(new_goodscode))
            err_flg = "1"
            return "Q01"

        if str(new_goodscode).find(str(now_guid)) == -1:
            print('>> goodscode가 unmatch (Q01) : '+str(new_goodscode))
            err_flg = "1"
            return "Q01"

        try:
            sql = "update t_goods set goodscode = '{0}' where uid = {1}".format(new_goodscode,now_guid)
            db_con.execute(sql)
            print('>> t_goods table goodscode update')
        except Exception as e:
            print('>> Exception [#goodscode]', e)
            err_flg = "1"
            return "Q01"

        #option #######################
        option_where_condition = "GOODSUID = '{0}'".format(now_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]', e)
            return "Q02"

        if dic['optionkind'] == 300 or dic['optionkind'] == "300":
            goodsinfo_option_dic['GOODSUID'] = now_guid
            print('>> t_goods_option Insert')
            #print(goodsinfo_option_dic)
            try:
                db_con.insert('t_goods_option',goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_content #######################
        sql = "select * from t_goods_content where uid = {0}".format(now_guid)
        contentrow = db_con.selectone(sql)

        print('>> t_goods_content Insert')
        if not contentrow:
            goodsinfo_content_dic['Uid'] = now_guid
            try:
                db_con.insert('t_goods_content', goodsinfo_content_dic)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q01"
        else:
            content_where_condition = "uid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_sub #######################
        sql = "select * from t_goods_sub where uid={0}".format(now_guid)
        goodssubrow = db_con.selectone(sql)
        print('>> t_goods_sub Insert')
        if not goodssubrow:
            goodsinfo_sub_dic['Uid'] = now_guid
            try:
                db_con.insert('t_goods_sub', goodsinfo_sub_dic)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q01"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(now_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_category #######################
        sql = "select * from t_goods_category where GoodsUid = '{0}'".format(now_guid)
        categoryrow = db_con.selectone(sql)
        print('>> t_goods_category Insert')
        if not categoryrow :
            goodsinfo_cate_dic['GoodsUid'] = now_guid
            try:
                db_con.insert('t_goods_category', goodsinfo_cate_dic)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q01"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q01"

        print(">> 신규 상품 insert goods Ok : {}".format(rtn_goodscode))
    else:
        #####################################################################
        print(">> ## setDB Update ")
        #####################################################################
        goodsinfo_dic['naver_price_ck'] = "'0'"
        if dic['db_goodscode'] != "" or D_goodscode != "":
            if D_goodscode == "":
                D_goodscode = dic['db_goodscode']
            ## [naver_price 테이블 ] change_price 최저가 확인후 처리  
            sql_price = "select price, DATEDIFF(dd,isnull(update_date, regdate), getdate()) as diff_day from change_price where flag = '4' and goodscode = '{}'".format(D_goodscode)
            # checkIP()
            print(">> sql_price : {}".format(sql_price))
            row = db_price.selectone(sql_price)
            if row:
                naver_rowprice = row[0]
                diff_day = row[1]
                print(">> [{}] | low_price : {} | naver_rowprice : {} | diff_day : {}".format(D_goodscode, dic['low_price'], naver_rowprice, diff_day))
                # change_price 최저가 비교
                if int(dic['low_price']) > int(naver_rowprice):
                    if diff_day > 90:
                        print(">> change_price 업데이트가 90일 이상지난 상품으로 실제 가격 Update : {}".format(diff_day))
                    elif int(dic['low_price']) * 0.85 > int(naver_rowprice):
                        print(">> change_price 최저가 15프로 이상 차액으로 실제 가격 Update : {} ".format(int(dic['low_price']) * 0.85))
                    else:
                        ## change_price --->  minus_check = 1  update  처리 
                        slq_price_up = "update change_price set minus_check = '1' where goodscode = '{}'".format(D_goodscode)
                        print(">> [naver_price 테이블 ] change_price --->  minus_check = 1 update  처리 : {}".format(D_goodscode))
                        print(">> [t_goods 테이블 ] pirce 변경 (SKIP) : {}".format(D_goodscode))
                        db_price.execute(slq_price_up)
                        goodsinfo_dic['naver_price_ck'] = "'1'"

        if goodsinfo_dic['naver_price_ck'] == "'0'":
            # change_price 최저가 없음
            if dic['goodsmoney'] < 18000:
                dic['goodsmoney'] = 18000
            goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
            goodsinfo_dic['naver_price_ck'] = "'0'"

        goodsinfo_dic['UpdateDate'] = 'getdate()'
        arr_where_condition = "uid = {0}".format(old_guid)
        print(">> old_guid : " +str(old_guid) + " | ck_isdisplay : "+str(ck_isdisplay) + " | ck_delnaver : " + str(ck_delnaver))
        ### Test ############################
        #print(goodsinfo_dic)
        try:
            db_con.update('t_goods', goodsinfo_dic, arr_where_condition)
            print('>> t_goods Update ')
        except Exception as e:
            print('>> Exception [t_goods]', e)
            err_flg = "1"
            return "Q02"

        # option #######################
        option_where_condition = "GOODSUID = '{0}'".format(old_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]', e)
            return "Q02"

        if dic['optionkind'] == 300 or dic['optionkind'] == "300":
            goodsinfo_option_dic['GOODSUID'] = old_guid
            print('>> t_goods_option UPdate:')
            #print(goodsinfo_option_dic)

            try:
                db_con.insert('t_goods_option', goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]', e)
                return "Q02"

        #t_goods_content #######################
        sql = "select * from t_goods_content where uid = {0}".format(old_guid)
        contentrow = db_con.selectone(sql)

        print('>> t_goods_content Update')
        if not contentrow:
            goodsinfo_content_dic['Uid'] = old_guid
            try:
                db_con.insert('t_goods_content', goodsinfo_content_dic)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q02"
        else:
            content_where_condition = "uid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q02"

        #t_goods_category #######################
        sql = "select * from t_goods_category where GoodsUid = '{0}'".format(old_guid)
        categoryrow = db_con.selectone(sql)
        print('>> t_goods_category Update')

        if not categoryrow :
            goodsinfo_cate_dic['GoodsUid'] = old_guid
            try:
                db_con.insert('t_goods_category', goodsinfo_cate_dic)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q02"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q02"

        #t_goods_sub #######################
        sql = "select * from t_goods_sub where uid={0}".format(old_guid)
        goodssubrow = db_con.selectone(sql)
        print('>> t_goods_sub Update')
        #print(goodsinfo_sub_dic)
        if not goodssubrow:
            goodsinfo_sub_dic['Uid'] = old_guid
            try:
                db_con.insert('t_goods_sub', goodsinfo_sub_dic)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q02"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(old_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q02"

        # 품절/진열 변경 #######################
        if ck_isdisplay == "F": # 품절상태의 경우
            #if ck_delnaver == 0:
            print('>> IsDisplay Update (품절 -> 노출)')
            sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = null, stock_ck_cnt = '0', UpdateDate=getdate() where uid = {0}".format(old_guid)
            #print('>> setDisplay : ' + str(sql))
            try:
                db_con.execute(sql)
                print('>> ## update_execute ')
            except Exception as e:
                print('>> Exception [t_goods]', e)
                return "Q02"

        # 네이버 노출 상품이고, change_price 최저가 없고, OriginalPrice 가 변경되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : U)
        if str(D_naver_in) == "1" and goodsinfo_dic['naver_price_ck'] == "'0'" and ( int(dic['db_OriginalPrice']) != int(goodsinfo_dic['OriginalPrice']) ):
            proc_ep_insert(D_goodscode,'U')

        print(">> 기존 상품 update goods Ok ")

    dic.clear()
    goodsinfo_dic.clear()
    goodsinfo_content_dic.clear()
    goodsinfo_option_dic.clear()
    goodsinfo_sub_dic.clear()
    goodsinfo_cate_dic.clear()

    print(">> SetDB OK ASIN : " + str(in_asin))

    return "0@" + str(rtn_goodscode)


def get_asinset(in_catecode,db_con,list_name):
    asinset = []

    if list_name == "list":
        sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
    else:
        sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsinRef as a left join t_goods as t on t.ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
    rs_row = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rs_row:
        print('>> category complete! change catecode :' +str(in_catecode))
        where_condition = " catecode = '{0}'".format(in_catecode)
        db_con.delete('update_list2', where_condition)
        return 0

    for ea_asin in rs_row:
        Duid = ""
        asin = ea_asin[0]
        price = ea_asin[1]
        Duid = ea_asin[2]
        if (price is None) or (price == ''):
            price = 'null'
        if (asin is None) or (asin == '') or asin == None:
            pass
        else:
            asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(price) + '@' + str(Duid))

    return asinset

def procWork(db_con, in_ip):
    print('>> procWork : ' + str(datetime.datetime.now()))

    ip_catecode = ""
    sql = "select catecode from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] Catecode No. ")

    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] Catecode : " + str(ip_catecode))

        sql = "update update_list2 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list2 (getdate) ")
        db_con.execute(sql)

    return "0"

def version_check(db_con, in_drive, manage_dic):

    in_ver = manage_dic['ver']
    in_pgFilename = manage_dic['pgFilename'] 
    in_pgKbn = manage_dic['pgKbn']
    
    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")

    sql = "select version,url from python_version_manage where name = '" +str(in_pgKbn)+ "'"
    print(">> sql:" + sql)

    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        print(">> (DB) version :" +str(version))

        if str(in_ver) != str(version):
            db_con.close()            
            in_drive.quit()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 10000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")
                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 10000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")
            time.sleep(2)

            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception (1)')
            else:
                pass

            try:
                fname = os.path.abspath( __file__ )
                fname = getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 

                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')
            else:
                pass

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

def version_check_2(db_con, manage_dic):

    in_ver = manage_dic['ver']
    in_pgFilename = manage_dic['pgFilename'] 
    in_pgKbn = manage_dic['pgKbn']

    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")

    sql = "select version,url from python_version_manage where name = '" +str(in_pgKbn)+ "'"
    print(">> sql:" + sql)

    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        print(">> (DB) version :" +str(version))

        if str(in_ver) != str(version):
            db_con.close()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 1000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")

                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 1000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")

            time.sleep(3)
            
            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception ')
            else:
                pass

            try:
                fname = os.path.abspath( __file__ )
                fname = getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 

                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')
            else:
                pass

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

def procEnd(db_con, in_drive):
    time.sleep(1)
    print(">> procEnd : " + str(datetime.datetime.now()))
    db_con.close()
    in_drive.quit()
    time.sleep(2)
    os._exit(0)

def newlist(db_con, in_drive, in_pg, in_ip):
    cateidx = ""
    sql = "select * from update_list2 where flg_ref is null and proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        sql = "select top 1 cate_idx from T_Category_BestAsin where cate_idx not in (select catecode from update_list2 where flg_ref is null ) order by up_date"
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> Error : '+str(e))
                # proc end
                procEnd(db_con, in_drive)
    else:
        sql = "select count(*) from update_list2 where flg_ref is null and proc_ip = '{0}'".format(in_ip)
        rows = db_con.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list2 where flg_ref is null and proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list2 where flg_ref is null and proc_ip='{0}' order by regdate desc)".format(in_ip)
            db_con.execute(sql)

        sql = "select catecode, now_page from update_list2 where flg_ref is null and proc_ip = '{0}'".format(in_ip)
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            now_page = row[1]
            if now_page > 2:
                now_page = 2
            sql = "update update_list2 set now_page = {0} ,regdate=getdate() where flg_ref is null and proc_ip='{1}'".format(now_page, in_ip)
            db_con.execute(sql)

    return cateidx

def newlist_ref(db_con, in_drive, in_pg, in_ip):
    cateidx = ""
    sql = "select * from update_list2 where flg_ref = '1' and proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        sql = "select top 1 cate_idx from T_Category_BestAsinRef where cate_idx not in (select catecode from update_list2 where flg_ref = '1' ) order by up_date"

        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> Error : '+str(e))
                # proc end
                procEnd(db_con, in_drive)
    else:
        sql = "select count(*) from update_list2 where flg_ref = '1' and proc_ip = '{0}'".format(in_ip)
        rows = db_con.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list2 where flg_ref = '1' and proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list2 where flg_ref = '1' and proc_ip='{0}' order by regdate desc)".format(in_ip)
            db_con.execute(sql)

        sql = "select catecode, now_page from update_list2 where flg_ref = '1' and proc_ip = '{0}'".format(in_ip)
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            now_page = row[1]
            if now_page > 2:
                now_page = 2
            sql = "update update_list2 set now_page = {0} ,regdate=getdate() where flg_ref = '1' and proc_ip='{1}'".format(now_page, in_ip)
            db_con.execute(sql)

    return cateidx

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

def rtn_msg_print(rtnChk):
    rtnChk_no = ""
    rtnChk_no = str(rtnChk[:3])

    if rtnChk_no[:1] == "D":
        print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
    elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
        print('>> # Url Connect Error : ' + str(rtnChk))
    elif rtnChk_no == "C04" or rtnChk_no == "C05":  # blocked
        print('>> # blocked error : ' + str(rtnChk))
    elif rtnChk_no == "S01":
        print('>> # stop upadte (SKIP) : ' + str(rtnChk))
    elif rtnChk_no == "S02":
        print('>> # naver noclick goods (SKIP) : ' + str(rtnChk))
    elif rtnChk_no == "Q01":  # setDB ( Insert )
        print('>> # SetDB  Insert  : ' + str(rtnChk))
    elif rtnChk_no == "Q02":  # setDB ( Update )
        print('>> # SetDB  Update  : ' + str(rtnChk))
    elif rtnChk_no == "E01":
        print('>> # error : ' + str(rtnChk))
    elif rtnChk_no == "0":
        print('>> # SetDB Ok : ' + str(rtnChk))
    else:
        print('>> # rtnChk_no : ' + str(rtnChk))

def set_multi(db_con, db_price, browser, manage_dic):

    in_pg = manage_dic['pgName']
    currIp = manage_dic['currIp']
    list_name = manage_dic['list_name']
    pgFilename = manage_dic['pgName']
    ver = manage_dic['ver']
    # 새상품 : LH_ItemCondition=1000 / 무료배송상품 : LH_FS=1 / Item Location : H_PrefLoc=1 (US Only)
    # https://www.ebay.com/itm/174400017335?LH_ItemCondition=1000 (New Goods )
    # https://www.ebay.com/itm/402819574928?_nkw=refurbished
    # https://www.ebay.com/b/45462?rt=nc&mag=1&LH_ItemCondition=1000|2000&LH_FS=1&H_PrefLoc=1
    # cate_no = "22691" # '34386'

    if list_name == "list":
        cateidx = newlist(db_con, browser, in_pg, mac_addr())
    else:
        cateidx = newlist_ref(db_con, browser, in_pg, mac_addr())
    if cateidx == "":
        print('>> catecode parsing complete : ' + str(cateidx))
        return "0"

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, browser, manage_dic)

    # asin get
    get_asin_list = []
    get_asin_list = get_asinset(cateidx, db_con, list_name)
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(cateidx))
        return "1"

    allCnt = 0
    c_Errcnt = 0
    d19_Errcnt = 0 
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))
    rtnChk_no = ""

    for asin_item in get_asin_list:
        print('>> version : '+str(ver))
        # checkIP()
        time.sleep(2)
        allCnt = allCnt + 1
        if allCnt % 10 == 0:
            procWork(db_con, mac_addr())
        time.sleep(1)
        print(str(datetime.datetime.now()))
        print('>> ----------------- < set_multi [' + str(allCnt) + ' ] >  catecode : ' + str(cateidx) + ' | goodscode : ' + str(asin_item) + ' -------------------------------------')
        rtnChk = proc_asin_parse_brower(db_con, db_price, browser, asin_item, manage_dic)  
        print('>> [ rtnChk ] : ' + str(rtnChk))
        spm_asin = asin_item.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        allCnt = allCnt + 1

        # return msg print 
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        rtn_msg_print(rtnChk)
        if rtnChk_no[:1] == "C":
            c_Errcnt = c_Errcnt + 1
        elif rtnChk_no[:3] == "D19":
            d19_Errcnt = d19_Errcnt + 1
        elif rtnChk_no[:1] == "D" or rtnChk_no[:1] == "0":
            c_Errcnt = 0
            d19_Errcnt = 0

        dic_b = dict()
        dic_b['asin'] = "'" + rtn_asin + "'"
        dic_b['cate_idx'] = cateidx
        dic_b['memo'] = "'" + getMemo(rtnChk.replace("'","`")) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "

        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "E":
            print('>> proc_asin_parse_brower (OK) ')
            if rtnChk == "E99":
                break
            if rtnChk_no[:1] == "D":
                D_naver_in = ""
                D_goodscode = ""
                if str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where ali_no = '{0}'".format(rtn_asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where uid = '{0}'".format(rtn_uid)                    
                # print(">> sql : {}".format(sql))
                try:
                    rs = db_con.selectone(sql)
                except Exception as e:
                    print('>> exception 1-1 (sql) : {}'.format(sql))
                    # checkIP()
                    time.sleep(30)
                    # procLogSet(db_con, in_pg, " ( exception 1-1  ) exit - rtn_asin: " + str(rtn_asin))
                    procEnd(db_con, browser)

                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    DDel_Naver = rs[2]
                    D_naver_in = rs[5]
                    D_goodscode = rs[6]

                    # T_goods sold out
                    if DIsDisplay == 'T':
                        if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                            sql_u1 = "update t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1' where uid = {0}".format(Duid)
                            db_con.execute(sql_u1)

                            sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
                            db_con.execute(sql_u2)
                        else:
                            print('>> [' + str(rtn_asin) + '] setDisplay (품절 처리) :' + str(Duid))                              
                            sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate() where uid='{0}'".format(Duid)
                            print(">> sql : " + str(sql))
                            print(">> 품절 처리 OK : " + str(asin_item))
                            db_con.execute(sql)
                        # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                        if str(D_naver_in) == "1":
                            proc_ep_insert(D_goodscode,'D')

            if rtnChk != "0":  
                sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(rtn_asin)
                db_con.execute(sql)
                db_con.insert('T_Category_BestAsin_del', dic_b)  # insert
                print('>> ##insert## : T_Category_BestAsin_del')

        else:
            rtnChk = "E99"
            break
        if list_name == "list":
            sql = "delete from T_Category_BestAsin where asin ='{0}'".format(rtn_asin)
        else:
            sql = "delete from T_Category_BestAsinRef where asin ='{0}'".format(rtn_asin)            
        db_con.execute(sql)

        if rtnChk_no[:1] == "C":
            time.sleep(2)
            if c_Errcnt > 7:
                print('>> ( c_Errcnt 7 over ) exit - catecode :' + str(cateidx))
                procLogSet(db_con, in_pg, " ( c_Errcnt 7 over ) exit - catecode: " + str(cateidx))
                procEnd(db_con, browser)
        if d19_Errcnt > 7:
            print('>> ( d19_Errcnt 7 over ) exit - catecode :' + str(cateidx))
            procLogSet(db_con, in_pg, " ( d19_Errcnt 7 over ) exit - catecode: " + str(cateidx))
            procEnd(db_con, browser)

    if rtnChk == "E99":
        return "E99"

    return "0"

# Stock ###################################################################################
def set_stock_multi(db_con, db_price, browser, manage_dic):
###########################################################################################
    in_ver = manage_dic['ver']
    in_pg = manage_dic['pgName']
    print('>> set_stock_multi ')

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, browser, manage_dic)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, manage_dic)
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(currIp))
        return "11"

    allCnt = 0
    c_Errcnt = 0
    d19_Errcnt = 0 
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))
    rtnChk_no = ""

    for asin_item in get_asin_list:
        print('>> version : '+str(in_ver))
        #checkIP()
        allCnt = allCnt + 1
        if allCnt % 10 == 0:
            procWork(db_con, mac_addr())
        time.sleep(1)
        print(str(datetime.datetime.now()))
        print('>> ----------------- < set_stock_multi [' + str(allCnt) + ' ] goodscode : ' + str(asin_item) + ' -------------------------------------')
        rtnChk = proc_asin_parse_brower(db_con, db_price, browser, asin_item, manage_dic)  
        print('>> [ rtnChk ] : ' + str(rtnChk))
        spm_asin = asin_item.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        allCnt = allCnt + 1

        # return msg print 
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        rtn_msg_print(rtnChk)

        if rtnChk_no[:1] == "C":
            c_Errcnt = c_Errcnt + 1
        elif rtnChk_no[:3] == "D19":
            d19_Errcnt = d19_Errcnt + 1
        elif rtnChk_no[:1] == "D" or rtnChk_no[:1] == "0":
            c_Errcnt = 0
            d19_Errcnt = 0        

        dic_b = dict()
        dic_b['asin'] = "'" + rtn_asin + "'"
        dic_b['memo'] = "'" + getMemo(rtnChk) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "

        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "E":
            print('>> proc_asin_parse_brower (OK) ')
            if rtnChk == "E99":
                break

        # checkIP()
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        # print('>> ##selectone## sql :' + str(sql))
        try:
            rs_row = db_con.selectone(sql)
        except Exception as e:
            print('>> exception 2-1 (sql) : {}'.format(sql))
            # checkIP()
            time.sleep(30)
            # procLogSet(db_con, in_pg, " ( exception 2-1  ) exit - rtn_asin: " + str(rtn_asin))
            procEnd(db_con, browser)

        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_item))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_naver_in = rs_row[8]	

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        print('>> Forbidden 금지어일 경우 판매불가 상품처리 ')
                        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {}".format(            rtn_uid)
                        db_con.execute(sql_u1)
                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {}".format(rtn_uid)
                        db_con.execute(sql_u2)
                    else:
                        print('>> IsDisplay Update (F) 품절처리 ')
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{}'".format(rtn_uid)
                        print(">> sql : " + str(sql))
                        print(">> sold out OK : " + str(d_GoodsCode))
                        db_con.execute(sql)
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)
            elif rtnChk_no == "0":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)
            else:  # blocked
                sql = "update T_goods set stock_ck = '1', UpdateDate = UpdateDate - 3 where uid='{}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)
        print(">> Errcnt : {} ".format(c_Errcnt))

        if rtnChk_no[:1] == "C":
            time.sleep(2)
            if c_Errcnt > 7:
                print('>> ( c_Errcnt 7 over ) exit  :' + str(asin_item))
                procLogSet(db_con, in_pg, " ( c_Errcnt 7 over ) exit : " + str(asin_item))
                procEnd(db_con, browser)

        if d19_Errcnt > 7:
            print('>> ( d19_Errcnt 7 over ) exit  :' + str(asin_item))
            procLogSet(db_con, in_pg, " ( d19_Errcnt 7 over ) exit : " + str(asin_item))
            procEnd(db_con, browser)

    if rtnChk == "E99":
        return "E99"

    return "0"


def get_update_goods(in_site, db_FS, db_con):
    asinset = []
    tmp_guid = ""
    chk_data = ""

    sql = " select top 100  guid, sitecate,  display_ali_no, regdate, upddate, flg_chk "
    sql = sql + " from amazon_goods_update "
    sql = sql + " where flg_chk ='0' and sitecate = '" + str(in_site) + "'"
    sql = sql + " order by RegDate asc "
    rs_row = db_FS.select(sql)
    #print('>> ##select all## sql :' + str(sql))

    rowCnt = 0
    if rs_row:
        print('>> (amazon_goods_update) top 100 guid ')
        for ea_item in rs_row:
            rowCnt = rowCnt + 1
            d_guid = ea_item[0]
            if rowCnt == 1:
                tmp_guid = " ( " + "'" + str(d_guid) + "'"
            tmp_guid = tmp_guid + ",'" + str(d_guid) + "'"
        if tmp_guid != "":
            tmp_guid = tmp_guid + " ) "
        print('>> tmp_guid :' + str(tmp_guid))

        # 우선 업데이트 대상 상품 업데이트 
        sql = "select top 25 ali_no, price, cate_idx, uid from t_goods where uid in " + str(tmp_guid) 
        rs_row2 = db_con.select(sql)
        print('>> ##select all## sql :' + str(sql))

        if not rs_row2:
            print('>> (UpdateDate) Date No ! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_asin in rs_row2:
                asin = ea_asin[0]
                price = ea_asin[1]
                cate_idx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cate_idx) + '@' + str(price) + '@' + str(uid))
        if chk_data == "0":
            return ""
    return asinset

# Stock ###################################################################################
def set_updatelist(db_FS, db_con, db_price, browser, manage_dic):
###########################################################################################
    print('>> set_updatelist ')

    in_pg = manage_dic['pgName']
    in_pgsite = manage_dic['pgSite']
    in_ver = manage_dic['ver']

    # asin get
    get_asin_list2 = []
    get_asin_list2 = get_update_goods(in_pgsite, db_FS, db_con)
    print(get_asin_list2)
    if str(get_asin_list2).rfind('@') == -1:
        print('>> 우선 없데이트 처리 대상 없음. (완료)')
        return "1"

    allCnt = 0
    c_Errcnt = 0
    d19_Errcnt = 0 
    cnt_asinlist2 = 0
    cnt_asinlist2 = len(get_asin_list2)
    rtnChk = ""
    print('>> (get_asin_list2) len :' + str(cnt_asinlist2))

    for asin_low in get_asin_list2:
        print('>> version : '+str(in_ver))
        #checkIP()
        allCnt = allCnt + 1
        if allCnt % 10 == 0:
            procWork(db_con, mac_addr())
        time.sleep(1)
        print(str(datetime.datetime.now()))
        print('\n\n ----------------- < (stock check) set_updatelist [' + str(cnt_asinlist2) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(db_con, db_price, browser, asin_low, manage_dic)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_updatelist Exception Error : ' + str(ex))
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "":
                print('>> error : ' + str(rtnChk))
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_parse_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        # return msg print 
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        rtn_msg_print(rtnChk)
        if rtnChk_no[:1] == "C":
            c_Errcnt = c_Errcnt + 1
        elif rtnChk_no[:3] == "D19":
            d19_Errcnt = d19_Errcnt + 1
        elif rtnChk_no[:1] == "D" or rtnChk_no[:1] == "0":
            c_Errcnt = 0
            d19_Errcnt = 0 

        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "E":
            print('>> proc_asin_parse_brower (OK) ')
            if rtnChk == "E99":
                break

        # checkIP()
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        #print('>> ##selectone## sql :' + str(sql))
        try:
            rs_row = db_con.selectone(sql)
        except Exception as e:
            print('>> exception 2-2 (sql) : {}'.format(sql))
            # checkIP()
            time.sleep(30)
            # procLogSet(db_con, in_pg, " ( exception 2-2  ) exit - rtn_asin: " + str(rtn_asin))
            procEnd(db_con, browser)

        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_naver_in = rs_row[8]	

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        print('>> Forbidden 금지어일 경우 판매불가 상품처리 ')
                        sql_u1 = "update t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1', NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid='{}'".format(rtn_uid)
                        db_con.execute(sql_u1)

                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {}".format(rtn_uid)
                        db_con.execute(sql_u2)
                    else:
                        print('>> [' + str(rtn_asin) + '] setDisplay (품절 처리) :' + str(rtn_uid))
                        #setDisplay(rtn_uid, 'F', '', db_con)      
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{}'".format(rtn_uid)
                        print(">> sql : " + str(sql))
                        print(">> 품절 처리 OK : " + str(d_GoodsCode))
                        db_con.execute(sql)
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no == "0":
                # ep 반영될수 있도록 update_price = '1' 추가
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date = getdate(), stock_ck_cnt = '0', update_price = '1' where uid='{}'".format(rtn_uid)
                print(">> ep 반영될수 있도록 update_price = '1' 추가 sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

                sql_ch = " select * from naver_del where goodscode = '{}'".format(d_GoodsCode)
                row_ch = db_FS.selectone(sql_ch)
                if not row_ch:
                    sql_i = "insert into naver_del (goodscode,deldate,ep_mode) values ('{}',getdate(),'U')".format(d_GoodsCode)
                    print(">> ep 반영될수 있도록 naver_del 추가 : {} ".format(sql_i))
                    db_FS.execute(sql_i)

            # blocked 경우 amazon_goods_update 테이블 regdate + 1 다음에 다시 시도
            if rtnChk_no[:1] == "C" or rtnChk_no[:1] == "Q" or rtnChk_no[:1] == "E":
                sql = "update amazon_goods_update set flg_chk = '0', regdate = regdate + 1 where guid='{}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)
            elif rtnChk_no == "0" or rtnChk_no[:1] == "D":
                sql = "update amazon_goods_update set flg_chk = '1', upddate = getdate() where guid='{}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)

        print(">> Errcnt : {} ".format(c_Errcnt))

        if rtnChk_no[:1] == "C":
            time.sleep(2)
            if c_Errcnt > 7:
                print('>> ( c_Errcnt 7 over ) exit  :' + str(asin_low))
                procLogSet(db_con, in_pg, " ( c_Errcnt 7 over ) exit : " + str(asin_low))
                procEnd(db_con, browser)
        if d19_Errcnt > 7:
            print('>> ( d19_Errcnt 7 over ) exit  :' + str(asin_low))
            procLogSet(db_con, in_pg, " ( d19_Errcnt 7 over ) exit : " + str(asin_low))
            procEnd(db_con, browser)

    if rtnChk == "E99":
        return "E99"

    return "0"

def procStockWork(db_con, in_pg, in_ip):
    print('>> procStockWork : ' + str(datetime.datetime.now()))

    ip_catecode = ""
    sql = "select proc_ip from update_list3 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] proc_ip No : " + str(in_ip))
        sql = "insert into update_list3 (regdate, proc_ip) values (getdate(),'{0}')".format(in_ip)
        print(">> insert update_list3 (getdate) ")
        db_con.execute(sql)
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] proc_ip : " + str(ip_catecode))
        sql = "update update_list3 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update update_list3 (getdate) ")
        db_con.execute(sql)

# Stock ###################################################################################
def get_stock_asin(db_con, manage_dic):
###########################################################################################
    in_sql1 = manage_dic['sql1']
    in_sql2 = manage_dic['sql2']
    in_sql3 = manage_dic['sql3']

    asinset = []
    chk_data = "0"
    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_asin in rs_row:
            asin = ea_asin[0]
            price = ea_asin[1]
            cateidx = ea_asin[2]
            uid = ea_asin[3]
            if (price is None) or (price == ''):
                price = 'null'
            if (asin is None) or (asin == '') or asin == None:
                pass
            else:
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if in_sql2 != "":
        rs_row2 = db_con.select(in_sql2)
        print('>> ##select all## in_sql2 :' + str(in_sql2))

        if not rs_row2:
            print('>> (UpdateDate) Stock Check complete! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_asin in rs_row2:
                asin = ea_asin[0]
                price = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                if (asin is None) or (asin == '') or asin == None:
                    pass
                else:
                    asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if in_sql3 != "":
        rs_row3 = db_con.select(in_sql3)
        print('>> ##select all## in_sql3 :' + str(in_sql3))

        if not rs_row3:
            print('>> ( stock_ck = 9) Check complete! ')
        else:
            print('>> (stock_ck = 9) len :' + str(len(rs_row3)))
            chk_data = "1"
            for ea_asin in rs_row3:
                asin = ea_asin[0]
                price = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                if (asin is None) or (asin == '') or asin == None:
                    pass
                else:
                    asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))
    if chk_data == "0":
        return ""

    return asinset


# stock_out ###################################################################################
def set_stock_out(db_con, db_price, in_drive, manage_dic):
###########################################################################################
    print('>> set_stock_out ')
    in_pg = manage_dic['pgName']
    in_ver = manage_dic['ver']
    in_pgsite = manage_dic['pgSite']

    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, in_drive, manage_dic)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, manage_dic)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> get_asin_list parsing complete : ' + str(currIp))
        return "11"

    c_Errcnt = 0
    d19_Errcnt = 0 
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        tmp_msg = ""
        allCnt = allCnt + 1
        if allCnt % 10 == 0:
            procStockWork(db_con, in_pg, mac_addr())
        time.sleep(1)

        print('\n\n')
        print('>> version : '+str(in_ver))
        #checkIP()
        print('>> ----------------- < (set_stock_out) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_out_brower(asin_low,db_con,db_price,in_drive,manage_dic)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_stock_out Exception Error : ' + str(ex))
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "":
                print('>> error : ' + str(rtnChk))
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_out_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        # return msg print 
        rtn_msg_print(rtnChk)
        if rtnChk_no[:1] == "C":
            c_Errcnt = c_Errcnt + 1
        elif rtnChk_no[:3] == "D19":
            d19_Errcnt = d19_Errcnt + 1
        elif rtnChk_no[:1] == "D" or rtnChk_no[:1] == "0":
            c_Errcnt = 0
            d19_Errcnt = 0 

        # checkIP()
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        # print('>> ##selectone## sql :' + str(sql))

        try:
            rs_row = db_con.selectone(sql)
        except Exception as e:
            print('>> exception 3-1 (sql) : {}'.format(sql))
            # checkIP()
            time.sleep(30)
            #procLogSet(db_con, in_pg, " ( exception 3-1  ) exit - rtn_asin: " + str(rtn_asin))
            procEnd(db_con, in_drive)

        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_naver_in = rs_row[8]	

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    print('>> IsDisplay Update (F) 품절처리 ')
                    #setDisplay(rtn_uid, 'F','1', db_con)
                    sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> Ok stock_ck update : " + str(d_GoodsCode))
                    db_con.execute(sql)
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

            elif rtnChk_no == "0":
                sql = "update T_goods set stock_ck = '2' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            else:  # blocked
                sql = "update T_goods set stock_ck = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)

        print(">> Errcnt : {0} ".format(c_Errcnt))

        if rtnChk_no[:1] == "C":
            time.sleep(3)
            if c_Errcnt > 5:
                print('>> ( c_Errcnt 5 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, in_pg, " c_Errcnt 5 over exit : " + str(asin_low))
                procEnd(db_con, in_drive)
        if d19_Errcnt > 7:
            print('>> ( d19_Errcnt 7 over ) exit  :' + str(asin_low))
            procLogSet(db_con, in_pg, " ( d19_Errcnt 7 over ) exit : " + str(asin_low))
            procEnd(db_con, in_drive)

    return "0"


def soldout_check(result):
    if str(result).find('have permission to access') > -1:
        print('>> Connect Error ')
        return "E99"
    if str(result).find('HTTP ERROR 429') > -1:
        print('>> Connect Error ')
        return "C02"
    if str(result).find('Looks like this page is missing') > -1:
        print('>> Looks like this page is missing (D17)')
        return "D17"
    if str(result).find(' this item is not available.') > -1:
        print('>> this item is not available. (D17)')
        return "D17"
    if str(result).find('This listing was ended by the seller') > -1:
        print('>> This listing was ended by the seller')
        return "D01"
    if str(result).find('This listing has ended.') > -1:
        print('>> This listing has ended.')
        return "D01"
    if str(result).find('This item is out of stock.') > -1:
        print('>> This item is out of stock.')
        return "D01"
    if str(result).find('Bidding has ended on this item.') > -1:
        print('>> Bidding has ended on this item.')
        return "D01"
    if str(result).find('Add this item to your watchlist to keep') > -1:
        print('>> Add this item to your watchlist to keep')
        return "D06"
    # if str(result).find('class="msgTextAlign"') > -1:
    #     strTmp = getparse(str(result),'class="msgTextAlign"','</span>')
    #     if strTmp.lower().find('this') > -1:
    #         print('>> class="msgTextAlign"')
    #         return "D01"

    return "0"

# 재고 체크
def proc_asin_out_brower(asin_item, db_con, db_price, browser, manage_dic): 
    sp_asin = asin_item.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    guid = ""
    guid = sp_asin[3]
    db_goodscode = ""
    db_Del_Naver = ""
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    now_url = "https://www.ebay.com/itm/" + str(asin) 
    print('\n\n>> now_url : ' + str(now_url)) 
    time.sleep(1)
    # browser.get(now_url)
    try:
        browser.get(now_url)
    except Exception as e:
        print(">> browser.get Except ")
        browser.refresh()
        time.sleep(10)
        return "C02"

    time.sleep(random.uniform(4,5))
    result = ""
    result = str(browser.page_source)
    time.sleep(2)
    if result.find('id="gh-eb-Geo-a-default"') > -1:
        print(">> 언어 설정 필요 (0)")
        #return "E99"

    result = str(browser.page_source)
    # 품절 체크
    rtn_sold = soldout_check(result)
    if  str(rtn_sold) != "0":
        return rtn_sold

    if result.find('id="binBtn_btn') == -1:
        print(">> No Button : Buy It Now (sold)")
        return "D01"

    if result.find('data-testid=x-bin-action') > -1 or result.find('data-testid="x-bin-action"') > -1:
        print(">> Buy It Now OK")
    else:
        print(">> No Button : Buy It Now (sold)")
        return "D01"   

    # if result.find('ux-shipping-calculator__country') > -1:
    #     currContry = getparse(result,'ux-shipping-calculator__country','ux-shipping-calculator__getRates')
    #     currContry = getparse(str(currContry),'<option value="1" selected="">','</option>')
    #     if currContry.find('United States') > -1:
    #         print(">> shipping country : United States")
    #     else:
    #         print(">> shipping country : {}".format(currContry))
    #         rtnFlg = setShipContry(browser)
    #         if rtnFlg == "0":
    #             input(">> shipping country 설정 필요 :")
    #         elif rtnFlg == "2":
    #             print('>> No United States (D48)')
    #             return "D48"      

    if str(browser.page_source).find("Ship to United States") > -1:
            print(">> Ship to United States OK")
    elif str(browser.page_source).find('<span>Ship to</span>') > -1:
        # currContry = getparse(result,'ux-shipping-calculator__country','ux-shipping-calculator__getRates')
        # currContry = getparse(str(currContry),'<option value="1" selected="">','</option>')
        if str(browser.page_source).find('United States') > -1:
            print(">> shipping country : United States")
        else:
            print(">> shipping country : ")
            rtnFlg = setShipContry(browser)
            if rtnFlg == "0":
                input(">> shipping country 설정 필요 :")
            elif rtnFlg == "2":
                print('>> No United States (D48)')
                return "D48"  

    condition = getCondition(result)
    if condition == "":
        print(">> condition 확인필요 : {}".format(condition))
        input(">> ")
    #print(">> condition-label : {}".format(condition))

    stock_check = ""
    stock_quantity = ""
    if result.find('id="qtySubTxt"') > -1:
        stock_quantity = getparse(str(result),'id="qtySubTxt"','</span>')
        stock_quantity = getparse(str(stock_quantity),'>','available').replace('More than','').replace('<span class="">','').strip()
        print(">> stock_quantity : {}".format(stock_quantity))
        stock_check = regRemoveText(stock_quantity).strip()
        if stock_check != "":
            if int(stock_check) < 1: # 0개일 경우 품절처리
                print('>> More than {} '.format(stock_check))
                return "D46"  
        print(">> stock_check : {}".format(stock_check))

    refurb_check = check_condtion(condition)
    if refurb_check == "1":
        print(">> Certified - Refurbished Ok : {}".format(condition))
    else:
        if refurb_check == "0":
            print(">> New (Skip) : {}".format(condition))
        else:
            print(">> (Buy used) condition no check : {}".format(condition))
            return "D04"

    sale_price = ""
    mainPrice_tmp = ""
    mainCur_price = ""
    origin_price = ""
    main_price = ""
    priceCurrency = ""

    if result.find('class="mainPrice"') > -1:
        mainPrice_tmp = getparse(str(result),'class="mainPrice"','</div>')
    elif result.find('itemprop="price"') > -1:
        mainPrice_tmp = getparse(str(result),'itemprop="price"','</div>')
    mainCur_price = getparse(str(mainPrice_tmp),'content="','</span>')
    mainCur_price = getparse(str(mainCur_price),'">','')
    if mainCur_price == "":
        mainPrice_tmp = getparse(str(result),'"priceCurrency":"','}')
        priceCurrency = getparse(str(mainPrice_tmp),'','"')
        if mainPrice_tmp.find('"price":"') > -1 and str(priceCurrency) == "USD":
            mainCur_price = getparse(str(mainPrice_tmp),'"price":"','"')

    if mainCur_price.find('US') > -1:
        main_price = getparse(str(mainPrice_tmp),'content="','"').replace(',','').strip()
    elif mainCur_price.find('GBP') > -1 or mainCur_price.find('AU') > -1 or mainCur_price.find('EUR') > -1 or mainCur_price.find('C') > -1: 
        print('>> No US price (D48)')
        return "D48" 
    elif priceCurrency == "USD" and mainCur_price != "":
        main_price = mainCur_price.replace(',','').strip()
    else:
        if result.find('"convertedBinPrice":"US $') > -1:
            convert_price = getparse(str(result),'"convertedBinPrice":"US $','"').replace(',','').strip()
            print(">> convert_price : {}".format(convert_price))
            main_price = convert_price
        elif result.find('convertedFromValue":') > -1:
            convert_price = getparse(str(result),'convertedFromValue":',',').replace(',','').strip()
            convert_curr = getparse(str(result),'convertedFromValue":','}')
            convert_curr = getparse(str(convert_curr),'convertedFromCurrency":"','"')
            if convert_curr == "USD" and convert_price != "":
                main_price = convert_price
            else:
                print('>> No main_price ')
                return "D01"            
        else:
            print('>> No main_price ')
            return "D01"                
    print(">> main_price : {}".format(main_price))
    if main_price == "":
        if result.find('discountedPrice":"') > -1:
            discountedPrice = getparse(str(result),'discountedPrice":"','"')
            print(">> discountedPrice : {}".format(discountedPrice))

    if result.find('id="vi-priceDetails"') > -1:
        origin_price = getparse(str(result),'id="vi-priceDetails"','</div>')
        origin_price = getparse(str(origin_price),'US $','</span>').replace(',','').strip()
        print(">> origin_price : {}".format(origin_price))
    if origin_price == "":
        if result.find('originalPrice":"') > -1:
            origin_price = getparse(str(result),'originalPrice":"','"').replace(',','').strip()
            print(">> origin_price (originalPrice) : {}".format(origin_price))

    if origin_price.find('US $') > -1 or origin_price.find('EUR') > -1:
        origin_price = getparse(str(origin_price),'US $','').replace(',','').replace("EUR","").strip()
        if main_price == "":
            main_price = origin_price
            print(">> origin_price -> main_price (1) : {}".format(main_price))

    if origin_price != "":
        if float(main_price) < float(origin_price):
            # 할인전 가격으로 수정 (List Price)
            main_price = origin_price
            print(">> origin_price -> main_price (3) : {}".format(main_price))

    if main_price == "":
        print('>> No main_price ')
        return "D01"

    if float(main_price) < 1:
        print('>> 1 달러 미만 (skip)')
        return "D12" + " ( " + str(main_price) + " ) "

    if float(main_price) > 1100:
        print('>> 1100 달러 over (skip)')
        return "D09" + " ( " + str(main_price) + " ) "
    
    # 경매 상품 체크
    if result.find('Starting bid:') > -1 or  result.find('Current bid:') > -1 :
        print(">> 경매 상품 SKIP : {}".format(asin))
        print(">> (Buy used) Unsellable product : {}".format(condition))
        return "D04"

    # 경매 상품 체크
    if result.find('title="Auction:') > -1:
        print(">> 경매 상품 (Auction) SKIP : {}".format(asin))
        print(">> (Buy used) Unsellable product : {}".format(condition))
        return "D04"

    db_Weight = "0"
    DB_stop_update = "0"
    # checkIP()
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where uid = {0}".format(guid)
    # print(">> sql : {}".format(sql))

    try:
        rowUP = db_con.selectone(sql)
    except Exception as e:
        print('>> exception 1.1.1 (sql) : {}'.format(sql))
        # checkIP()
        time.sleep(30)
        # procLogSet(db_con, in_pg, " ( exception 1.1.1  ) exit - asin: " + str(asin))
        procEnd(db_con, browser)

    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]

        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid
        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"
        if str(db_Del_Naver) == "1":
            print('>> Del_Naver 1 (네이버 미노출상품) : ' + str(asin))
        if str(DB_stop_update) == "1":
            print('>> stop_update goods : ' + str(asin))
            return "S01"

    return "0"
