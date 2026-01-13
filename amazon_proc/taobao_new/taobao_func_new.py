# -*- coding: utf-8 -*-
import datetime
import os
import random
import socket
import urllib
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import requests
import re
import pyperclip
import uuid
import DBmodule_py
import DBmodule_FR

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

global cnt_title_tran
global EX_PRICE
global gTWOCAPTCHA_API_KEY
gTWOCAPTCHA_API_KEY = "decc2c5553302ce2df33ddb9cf1f4846"

EX_PRICE = 12
EX_PRICE_US = 1300

ip = socket.gethostbyname(socket.gethostname())
#print('>> IP : '+str(ip))
#translator = googletrans.Translator()

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

def loginProc(in_driver, in_login_id, in_password):
    #로그인 복사 붙여넣기로 구현

    in_driver.implicitly_wait(5)
    pyperclip.copy(in_login_id)

    in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.DELETE)
    print('>> fm-login-id (clear)')
    in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.DELETE)
    print('>> fm-login-password (clear)')
    time.sleep(1)

    in_driver.find_element(By.NAME,'fm-login-id').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    pyperclip.copy(in_password)
    in_driver.find_element(By.NAME,'fm-login-password').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    in_driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
    time.sleep(1)


def loginProc_new(in_driver, in_login_id, in_password):
    time.sleep(1)
    print('>> loginProc_new ')

    wait = WebDriverWait(in_driver, 30)
    id_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id"))) 
    id_input.send_keys(in_login_id) 
    print('>> ID OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    pw_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-password"))) 
    pw_input.send_keys(in_password) 
    print('>> pass OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fm-button"))).click()
    print('>> click OK ')
    time.sleep(4)

    # in_driver.find_element(By.NAME,'fm-login-id').click()
    # in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.CONTROL + "a")
    # time.sleep(1)
    # in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.DELETE)
    # print('>> fm-login-id (clear)')
    # time.sleep(0.5)
    # for i in list(in_login_id):
    #     in_driver.find_element_by_css_selector('#fm-login-id').send_keys(i)
    #     time.sleep(0.25)
    # print('>> ID OK ')
    # in_driver.find_element(By.NAME,'fm-login-password').click()
    # in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.CONTROL + "a")
    # time.sleep(1)
    # in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.DELETE)
    # print('>> fm-login-password (clear)')
    # time.sleep(0.5)
    # for i in list(in_password):
    #     in_driver.find_element_by_css_selector('#fm-login-password').send_keys(i)
    #     time.sleep(0.25)
    # print('>> pass OK ')

    # time.sleep(2)
    # ActionChains(in_driver).key_up(Keys.ENTER).perform()
    # print('>> enter click ')
    # # in_driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
    # time.sleep(2)
    # try:
    #     in_driver.find_element_by_css_selector('#login-form > div.fm-btn > button').click()
    #     print('>> more click OK ')
    # except Exception as e:
    #     print('>> login except ')

    # in_driver.find_element(By.NAME,'fm-login-id').click()
    # in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.CONTROL + "a")
    # time.sleep(1)
    # in_driver.find_element(By.NAME,'fm-login-id').send_keys(Keys.DELETE)
    # print('>> fm-login-id (clear)')
    # time.sleep(0.5)
    # for i in list(in_login_id):
    #     in_driver.find_element_by_css_selector('#fm-login-id').send_keys(i)
    #     time.sleep(0.25)
    # print('>> ID OK ')
    # in_driver.find_element(By.NAME,'fm-login-password').click()
    # in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.CONTROL + "a")
    # time.sleep(1)
    # in_driver.find_element(By.NAME,'fm-login-password').send_keys(Keys.DELETE)
    # print('>> fm-login-password (clear)')
    # time.sleep(0.5)
    # for i in list(in_password):
    #     in_driver.find_element_by_css_selector('#fm-login-password').send_keys(i)
    #     time.sleep(0.25)
    # print('>> pass OK ')
    # time.sleep(2)
    # #in_driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
    # in_driver.find_element_by_css_selector('#login-form > div.fm-btn > button').click()
    # try:
    #     in_driver.find_element_by_css_selector('#login-form > div.fm-btn > button').click()
    #     print('>> more click OK ')
    # except Exception as e:
    #     print('>> login except ')



def elem_clear(browser, elem):

    time.sleep(0.2)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.2)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.2)
    elem.clear()
    time.sleep(0.5)

    return

## https://open-demo.otcommerce.com/ik.php 로그인처리
def demo_login_new(browser):
    print(">> login proc ")
    if browser.find_element(By.XPATH,'//*[@id="ot_auth_login"]'):
        elem = browser.find_element(By.XPATH,'//*[@id="ot_auth_login"]')
        elem_clear(browser, elem)
        elem.send_keys('1a8389aa-f246-4e24-8e87-de6f89806c6e')
        time.sleep(1)
        if browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[4]/div/button'):
            browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[4]/div/button').click()
            time.sleep(1)
        if str(browser.current_url).find('?cmd=Login') > -1:
            if browser.find_element(By.XPATH,'//*[@id="ot_auth_login"]'):
                elem = browser.find_element(By.XPATH,'//*[@id="ot_auth_login"]')
                elem_clear(browser, elem)
                elem.send_keys('root')
                elem = browser.find_element(By.XPATH,'//*[@id="ot_auth_password"]')
                elem_clear(browser, elem)
                elem.send_keys('38w7sg9BSXgv')
                time.sleep(1)
                if browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[3]/div/button'):
                    browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[3]/div/button').click()
                    time.sleep(1)

    return "0"

def check_browser(browser):
    print(">> Browser Count : {}".format(len(browser.window_handles)))
    if len(browser.window_handles) != 1:
        print(">> Browser Close : {}".format(len(browser.window_handles)))
        time.sleep(1)
        main = browser.window_handles
        last_tab = browser.window_handles[len(main) - 1]
        print('>> last_tab: ' + str(last_tab))
        if str(len(main)) != "1":
            for handle in main:
                if handle != last_tab:
                    browser.switch_to.window(window_name=handle)
                    browser.close()
                browser.switch_to.window(window_name=last_tab)
            time.sleep(2)
        print(">> Browser Close (after) : {}".format(len(browser.window_handles)))
        time.sleep(1)

#중국어 찾기
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

#db 특수단어 제거
def replaceQueryString(target) :
    result = target.replace("'","")
    result = result.replace("★","").replace("◆","").replace("/","|").replace(","," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("【","[").replace("】","]").replace('"', '').replace("「","[").replace("」","]").replace("(","[").replace(")","]").replace("（","[").replace("）","]")
    return str(result).strip()

#db 특수단어 제거
def replaceQueryStringOption(target) :
    result = target.replace("'","`").replace(","," ").replace("正品","").replace("정품"," ").replace("、",".").replace("\xa0"," ")
    result = result.replace("★","").replace("◆","").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("--","-").replace('"', '`')
    result = result.replace("{","[").replace("}","]").replace("/"," | ").replace("【","[").replace("】","]").replace("「","").replace("」","").replace("(","[").replace(")","]").replace("（","[").replace("）","]")
    return str(result).strip()

def replaceQueryStringTitle(target) :
    result = target.replace("'","").replace("- Taobao","").replace("Taobao","").replace("taobao","").replace("TAOBAO","").replace("tmall.com","").replace("- ChinaglobalMall","").replace("- CHINAGLOBALMALL","").replace('�','')
    result = result.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("【","(").replace("】",")").replace('"', '').replace("「","(").replace("」",")")
    return str(result).strip()

def replaceDescription(target):
    result = target.replace("'","")
    result = result.replace('&NBSP;', ' ').replace('&nbsp;', ' ').replace('&amp;NBSP;', ' ').replace('&amp;nbsp;', ' ')
    result = result.replace('&ldquo; Alipay&rdquo;','').replace('&ldquo; Alipay&rdquo;','')
    result = result.replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","")
    result = result.replace('//amos1.taobao.com/online.ww/online.aw?v=2&uid=%E6%AD%A6%E7%BC%98_%E5%B0%8F%E7%BD%97&s=2&site=cntaobao&s=2&charset=utf-8','')
    result = result.replace('amos1.taobao.com','').replace('//amos1.taobao.com/online.ww','')
    result = result.replace('https://img.alicdn.com/imgextra/i4/88672451/T2kLxyXihaXXXXXXXX_!!88672451.jpg','')
    result = result.replace('https://item.taobao.com/item.htm', '').replace('http://item.taobao.com/item.htm', '').replace('?id=','')
    result = result.replace('https://gdp.alicdn.com/imgextra/i2/113315203/T2cPlQXvFaXXXXXXXX_!!113315203.jpg', '')
    result = result.replace('//gdp.alicdn.com/imgextra/i2/113315203/T2cPlQXvFaXXXXXXXX_!!113315203.jpg', '')
    return result

def soldoutCheck(html_str,istmall):
    result = False
    if istmall == 'F' :
        if html_str.find('"error-notice"') > -1 :
            print(">> Sold Out : error-notice ")
            result = True
    else :
        if html_str.find('"errorAdvice"') > -1 :
            print(">> Sold Out : errorAdvice ")
            result = True
        elif html_str.find('"sold-out-info"') > -1 :
            result = True
    if html_str.find('该宝贝在您所选地区限制购买') > -1 :
        print(">> Sold Out : 该宝贝在您所选地区限制购买 (선택지역 구매불가) ")
        result = True
    return result

#mssql 쿼리 문 null처리
def getQueryValue(target):
    if target == None :
        result = "NULL"
    else :
        result = "'{0}'".format(target)
    return result

def get_cookies(driver):
    cookies = {}
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()
    return result_str

def getDescript(driver, result_goods, istmall):

    cookies = get_cookies(driver)
    ### descript ###
    descript = ""
    descript_str = ""
    descript_str2 = ""
    descript_result = ""
    descript_result2 = ""
    if istmall == "T":
        descript_url_str = getparse(result_goods,'"descUrl":"','"')
        descript_url = 'https:' + descript_url_str
    else:
        descript_url_str = getparse(result_goods, "descUrl          :", "counterApi")
        descript_url = getparse(descript_url_str, "//", "'")
        descript_url = 'https://' + descript_url
    print('>> descript_url : {} '.format(descript_url))
    try:
        #descript_result = requests.get(descript_url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        descript_result = requests.get(descript_url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, cookies=cookies)
        time.sleep(1)
        descript_str = descript_result.text
    except Exception as ex:
        print('>> descript_result Exception ')
        print('>> No check')
        descript_str = ""
    else:
        time.sleep(0.5)
        print(">> descript_str : {} ".format(str(descript_str)[:20]))

    if descript_str.find("var desc='") > -1:
        descript = getparse(descript_str, "var desc='", "';")
    else:
        if istmall == "T":
            descript_url2_str = getparse(result_goods, '"httpsDescUrl":"', '"')
            descript_url2 = 'https:' + descript_url2_str
        else:
            descript_url2_str = getparseR(descript_url_str, '//', None)
            descript_url2 = getparse(descript_url2_str, None, "'")
            descript_url2 = 'https://' + descript_url2
        print('>> descript_url2 : {} '.format(descript_url2))
        time.sleep(1)
        try:
            #descript_result2 = requests.get(descript_url2, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            descript_result2 = requests.get(descript_url2, headers={'Content-Type': 'application/x-www-form-urlencoded'}, cookies=cookies)
            time.sleep(1)
            descript_str2 = descript_result2.text  
        except Exception as ex:
            print('>> descript_result2 Exception ')
            print('>> No check')
            descript_str2 = ""
        else:
            time.sleep(0.5)
            print(">> descript_str2 : {} ".format(str(descript_str2)[:100]))
        
        if descript_str2.find("var desc='") > -1:
            descript = getparse(descript_str2, "var desc='", "';")

        # if descript == "":
        #     driver.get(descript_url)
        #     time.sleep(3)
        #     desc_result = driver.page_source
        #     path_file = os.getcwd()
        #     with open(path_file + "/log/desc_result.html","w",encoding="utf8") as f: 
        #         f.write(str(desc_result))
    return str(descript)

def moveScroll(driver):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 700
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > 5:
            break
        last_height = new_height

def procTranConect(browser, in_asin, option_max_count):
    result_tran = ""
    try:
        tran_url = 'https://cn.freeship.co.kr/_GoodsUpdate/title_tran_taobao.asp?asin={0}'.format(in_asin)
        print(">> tran_url : {}".format(tran_url))
        browser.get(tran_url)
    except Exception as e:
        print(">> procTranConect Exception : {}".format(e))
    else:
        time.sleep(random.uniform(3,4))
        if option_max_count > 25:
            moveScroll(browser)
        time.sleep(1)
        result_tran = str(browser.page_source)
        #print(">> result_tran : {}".format(result_tran))
    return result_tran

def getTranTitle(result_tmp, in_asin):
    tran_title = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_title = getparse(result_tmp,'<div id="google_translate_element">','<hr>')
        tran_title = getparse(tran_title,'<input type="hidden"','')
        tran_title = getparse(tran_title,'">','')
        tran_title = replace_main_str(tran_title)
        tran_title = tran_title.replace("- ChinaglobalMall","").strip()
    return str(tran_title)

def getTranOption(result_tmp, in_asin):
    tran_option = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_option = getparse(result_tmp,'<div id="google_translate_element">','<div class="skiptranslate ')
        tran_option = getparse(tran_option,'<hr>','')
        tran_option = replace_main_str(tran_option)
    return str(tran_option)

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

def getWonpirce(gDic, price):
    dollar_exchange = float(gDic['py_dollar_exchange']) # 0.16
    won_exchange = float(gDic['py_exchange_Rate']) # 180 -> 210
    final_price = 0
    price = float(price)
    dollar_price = price * dollar_exchange
    dollar_price = abs(dollar_price)
    won_price = price * won_exchange

    db_ali2 = DBmodule_py.Database('aliexpress', True)
    sql = "select * from ali_price_ck where cate_code = 'MAIN'"
    rs = db_ali2.selectone(sql)
    db_ali2.close()
    start_arr = []
    end_arr = []
    uppr_arr = []
    add_arr = []

    for i in range(0,30):
        pre_fix = str(i+1)
        start_arr.append(rs[str('st_'+pre_fix+'p')])
        end_arr.append(rs[str('ed_'+pre_fix+'p')])
        uppr_arr.append( rs[str('p_'+pre_fix+'uppr')])
        add_arr.append(rs[str('plus_'+pre_fix+'p')])

        if final_price == 0:
            if i == 0 :
                if dollar_price > 0 and dollar_price <= end_arr[i] :
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])
            elif i == 29 :
                if dollar_price > start_arr[i] :
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])
            else :
                if dollar_price > start_arr[i] and dollar_price <= end_arr[i]:
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])

        if final_price != 0:
            #print(" [{}] : {} * {} + {} = {}".format(price, round(won_price), uppr_arr[i], add_arr[i], round(final_price)))
            return round(final_price, 2)

    #print(">> final_price : [{}] {} | sale : {}".format(price, final_price, (final_price*0.5)))
    return round(final_price, 2)

def getMemo(in_code):
    in_code_no = ""
    in_code_no = str(in_code[:3])
    rtnMemo = ""
    if in_code_no == "D01":
        rtnMemo = str(in_code) + ' : (Sold Out) Unsellable product'
    elif in_code_no == "D02":
        rtnMemo = str(in_code) + ' : (No Title) nsellable product'
    elif in_code_no == "D22":
        rtnMemo = str(in_code) + ' : (No Price) nsellable product'
    elif in_code_no == "D71":
        rtnMemo = str(in_code) + ' : (sell not allowed) Unsellable product'
    elif in_code_no == "D03":
        rtnMemo = str(in_code) + ' : (Fobidden) Unsellable product'
    elif in_code_no == "D04":
        rtnMemo = str(in_code) + ' : (Buy used) Unsellable product'
    elif in_code_no == "D05":
        rtnMemo = str(in_code) + ' : (Add-on Item) Unsellable product'
    elif in_code_no == "D06":
        rtnMemo = str(in_code) + ' : (Temporarily out of stock) Unsellable product'
    elif in_code_no == "D07":
        rtnMemo = str(in_code) + ' : (option check) Unsellable product'
    elif in_code_no == "D57":
            rtnMemo = str(in_code) + ' : (option check) no option base 0 '
    elif in_code_no == "D47":
        rtnMemo = str(in_code) + ' : (option check) Unsellable option word'
    elif in_code_no == "D20":
        rtnMemo = str(in_code) + ' : (option check) 2 option price check'
    elif in_code_no == "D08":
        rtnMemo = str(in_code) + ' : (option price check) Unsellable product'
    elif in_code_no == "D09":
        rtnMemo = str(in_code) + ' : (max price over) Unsellable product'
    elif in_code_no == "D49":
        rtnMemo = str(in_code) + ' : (deposit_price) Unsellable product'
    elif in_code_no == "D49":  # 1044, 1038, 1033 카테고리 max over
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
    elif in_code_no == "T02":
        rtnMemo = str(in_code) + ' : tmall Sold out'
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
    elif in_code_no == "P01":
        rtnMemo = str(in_code) + ' : Check (Url No item)'

    return rtnMemo

#옵션처리
def generateOptionString(gDic, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, coupon):
    #################################################################
    klow = 0
    option_item = []
    option_marzin_price_sale_dic = dict()
    for key, value in option_price_dic.items():
        option_item_str = []
        klow = klow + 1
        diff_sale_price = 0
        option_marzin_price = 0
        option_marzin_sale_price = 0
        base_price_marzin = 0
        value_price_marzin = 0

        if str(value) == '0' or str(value) == '0.0':
            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            option_value = option_value_dic[key]
            option_value_str = "(" + str(key) + ")" + option_value
            option_item_str.append(option_value_str)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))
        else:
            diff_sale_price = float(value)-float(base_price_tmp)
            base_price_marzin = getWonpirce(gDic,float(base_price_tmp))
            value_price_marzin = getWonpirce(gDic, float(value))
            option_marzin_price = value_price_marzin - base_price_marzin  
            option_marzin_price = option_marzin_price
            #option_marzin_sale_price = option_marzin_price * ((100-coupon) / 100)
            option_marzin_sale_price = option_marzin_price
            option_marzin_sale_price = int(round(option_marzin_sale_price, -2))
            
            if d_minus_opt == "1":
                if option_marzin_sale_price >= 0:
                    option_marzin_sale_price = 0
                option_marzin_sale_price = option_marzin_sale_price / 2
            else:
                if option_marzin_sale_price < 0:
                    option_marzin_sale_price = 0

            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            option_value = option_value_dic[key]
            option_value_str = "(" + str(key) + ")" + option_value
            option_item_str.append(option_value_str)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))

    #print(">> option_marzin_price_sale_dic : {} ".format(option_marzin_price_sale_dic))    return ",".join(option_item) 
    return ",".join(option_item)


def getDeliveryFee(gDic, in_weight):
    deliveryFee = gDic['py_withbuy_cost']
    deliveryFee = float(deliveryFee)

    weight = in_weight
    if weight == None or weight == 0 or weight == 0.0 or weight == '' :
        pass
    else:
        if weight <= 15 :
            deliveryFee = deliveryFee + (weight*500)
        else:
            deliveryFee = (deliveryFee + 14000) + ((weight-15)*3000)

    result = deliveryFee * 2
    print(">> getDeliveryFee : {}".format(result))
    return int(round(result, -2))

def setGoodsdelProc(db_con, in_DUid, in_DIsDisplay, in_DOptionKind):
    
    db_con.delete('t_goods_sub', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_category', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_option', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_content', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods', "uid = '{0}'".format(in_DUid))

    print('>> (setGoodsdelProc) t_goods (delete ok) : {}'.format(in_DUid))

    return "0"

#goodscode
def getGoodsCode(uid,goodshead):
    result = goodshead+str(uid).zfill(10)
    return result

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(currIp) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

# contents
def generateContent(dic):
    feature_item = []
    description_item = []
    content_item = []
    description = []
    feature = []

    feature_item.append('<br><br><font color="orange"><b>Highlights</b></font><br><br><br><br>')
    feature_item.append("".join(dic['feature']))
    feature = "".join(feature_item)
    description_item.append('<br><br><br><font color="red"><b>Description</b></font><br><br><br>')
    description_item.append(dic['description'].replace("Description","").replace('&NBSP;', ' ').replace('&nbsp;', ' '))
    description = "".join(description_item)

    if dic['OptionKind'] == '300' or dic['OptionKind'] == 300:
        option_img_set = []
        for key,values in dic['option_img_dic'].items():
            if str(values) == '<br>' or str(values) == '':
                print(">> option_image values 없음 : "+str(values))
            else:
                values = replaceQueryStringOption(values)
                option_img_set.append('<Font color=blue><pre><b>[ {0} ]</b></pre></FONT><br><img src="{1}"><br><br>'.format(values, key))
        opt_img_item = "".join(option_img_set)
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(opt_img_item.replace("'",""))
        content_item.append(description.replace("'","").replace("・","·"))
    else:
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(description.replace("'",""))        

    return "".join(content_item)

#DB set
def setDB_proc(in_asin, dic, db_con, in_pg, in_guid, db_price):

    err_flg = "0"
    rtn_goodscode = ""
    print('>> setDB in_guid :' + str(in_guid))
    print('>> setDB start : ' +str(in_pg))
    print('>> [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_asin))

    goods_title = dic['goods_title']
    
    ##### price check #####
    if float(dic['price']) < 1:
        print('>> 1 달러 미만 (skip)')
        return "D12" + " ( " + str(dic['price']) + " ) "  # 1 달러 미만 

    # DB query
    goodsinfo_dic = dict()
    goodsinfo_dic['SiteID'] = "'rental'"
    goodsinfo_dic['DealerID'] = "'rental'"
    goodsinfo_dic['GoodsType'] = "'N'"
    goodsinfo_dic['api_flg'] = getQueryValue(dic['api_flg'])
    if dic['api_flg'] == '1':
        goodsinfo_dic['api_date'] = 'getdate()'
        goodsinfo_dic['api_InternalId'] = getQueryValue(dic['api_InternalId'])
        goodsinfo_dic['api_ExternalId'] = getQueryValue(dic['api_ExternalId'])
        goodsinfo_dic['api_categoryInfo'] = getQueryValue(dic['api_categoryInfo'])
        goodsinfo_dic['api_UpdatedTime'] = getQueryValue(dic['api_UpdatedTime'])
        goodsinfo_dic['api_CreatedTime'] = getQueryValue(dic['api_CreatedTime'])
        goodsinfo_dic['api_sell_reason'] = getQueryValue(dic['api_sell_reason'])
    else:
        goodsinfo_dic['api_date'] = getQueryValue(None)
    goodsinfo_dic['Title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['istmall'] = getQueryValue(dic['istmall'])
    goodsinfo_dic['ImgB'] = getQueryValue(dic['imgB'])
    goodsinfo_dic['ImgM'] = getQueryValue(dic['imgB'])
    goodsinfo_dic['ImgS'] = getQueryValue(dic['imgB'])
    #goodsinfo_dic['naver_img'] = getQueryValue(dic['naver_img'])
    goodsinfo_dic['OptionKind'] = getQueryValue(dic['OptionKind'])
    goodsinfo_dic['DeliveryPolicy'] = "'990'"
    goodsinfo_dic['State'] = "'100'"
    ### goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
    goodsinfo_dic['price_tmp'] = getQueryValue(dic['price_tmp'])
    goodsinfo_dic['OriginalPrice'] = dic['OriginalPrice']
    goodsinfo_dic['ali_no'] = getQueryValue(dic['ali_no'])
    goodsinfo_dic['cate_idx'] = dic['catecode']
    goodsinfo_dic['E_title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['DE_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['DE_title'])
    goodsinfo_dic['shipping_fee'] = getQueryValue(dic['taobao_shipping_fee'])
    goodsinfo_dic['shipping_weight'] = getQueryValue(dic['shipping_weight'])
    goodsinfo_dic['origin_dollar'] = getQueryValue(dic['price'])
    goodsinfo_dic['istmall'] = getQueryValue(dic['istmall'])
    goodsinfo_dic['withbuy_price_tmp'] = getQueryValue(dic['delivery_fee'])
    goodsinfo_dic['imgb_update_flg'] = getQueryValue(dic['imgb_update_flg'])

    if dic['taobao_shipping'] != "":
        goodsinfo_dic['taobao_shipping'] = getQueryValue(dic['taobao_shipping'])

    many_option_ck = dic['many_option']
    if many_option_ck == '1' :
        goodsinfo_dic['many_option'] = "'1'"

    #other img
    otherimg_low = 1
    for otherimg in dic['other_img_set']:
        if otherimg_low <= 5:
            goodsinfo_dic['other_img_chk_'+str(otherimg_low)] = "'1'"
            goodsinfo_dic['other_img'+str(otherimg_low)] = getQueryValue(otherimg)
        otherimg_low += 1

    ##############################################
    #option (goodsinfo_option_dic)
    ##############################################
    goodsinfo_option_dic = dict()
    if dic['OptionKind'] == '300' or dic['OptionKind'] == 300:
        goodsinfo_option_dic['Title'] = "'옵션선택'"
        goodsinfo_option_dic['Items'] = dic['Items']

        goodsinfo_option_dic['Items_org'] = "'N'+'" + str(dic['option_value_dic_org']).replace("'",'') + "'"
        goodsinfo_option_dic['Items_tran'] = "'N'+'" + str(dic['option_value_dic']).replace("'",'') + "'"
        goodsinfo_option_dic['Items_img_org'] = "'N'+'" + str(dic['option_img_dic_org']).replace("'",'') + "'"

        if str(goodsinfo_option_dic['Items']).find('/0') > -1:
            print('>> Opt 기본옵션 /0 포함 ')
        else:
            print('>> Opt 기본옵션 /0 없음 (SKIP) ')
            print(dic['Items'])
            return "D57"

        print('>> option (final) ')
        #print(goodsinfo_option_dic['Items'])

        goodsinfo_option_dic['Sort'] = 1
        goodsinfo_option_dic['ali_no'] = getQueryValue(dic['ali_no'])

    ##############################################
    #t_goods_content
    ##############################################
    goodsinfo_content_dic = dict()
    goodsinfo_content_dic['Content'] = "N" + getQueryValue(generateContent(dic))

    goodsreview = dic['review']
    goodsreview = str(goodsreview).replace("'",'"')
    goodsinfo_content_dic['ReviewContent'] = getQueryValue(goodsreview)
    goodsinfo_content_dic['ReviewRegDate'] = 'getdate()'

    ##############################################
    #t_goods_sub
    ##############################################
    goodsinfo_sub_dic = dict()
    goodsinfo_sub_dic['Product'] = "'CHINA'"

    if dic['api_flg'] == '1':
        goodsinfo_sub_dic['gall_list'] = getQueryValue(dic['gallery'])

    ##############################################
    # t_goods_category
    ##############################################
    goodsinfo_cate_dic = dict()
    goodsinfo_cate_dic['CateCode'] = dic['catecode']
    goodsinfo_cate_dic['Sort'] = 1
    
    ck_isdisplay = ""
    ck_delnaver = ""
    searchFlg = "0"
    D_ali_no = ""
    procFlg = ""
    D_naver_in = ""

    if str(in_guid) == '' or in_guid is None or in_guid == 'None':
        procFlg = "N"
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (ali_no) : {}'.format(dic['ali_no']))

        if not rows:
            procFlg = "N"
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"

        print(' procFlg : '+str(procFlg))  
    else:
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where uid = {0} ".format(in_guid)
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (2) (parentali_noasin) ')  

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
        goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])        
        goodsinfo_dic['naver_price_ck'] = "'0'"
        # if dic['api_flg'] == '1': # api의 경우 confirm_goods = 1 설정
        goodsinfo_dic['confirm_goods'] = 1 # img_url 이후처리 (이미지 컨버팅 이후 confirm_goods -> null 변경처리 23.11.24)
        #####################################################################
        print(">> ## setDB New Insert : " + str(in_asin))
        #####################################################################
        #insert t_goods
        try:
            db_con.insert('t_goods',goodsinfo_dic)
            print('>> ## t_goods  insert ')
        except Exception as e:
            print('>> Exception [t_goods]')
            err_flg = "1"
            return "Q01"

        time.sleep(1)
        #goodscode #######################
        sql = "select top 1 uid from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        coderow = db_con.selectone(sql)
        now_guid = coderow[0]         

        new_goodscode = getGoodsCode(now_guid, 'L')
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
            print('>> Exception [#goodscode]')
            err_flg = "1"
            return "Q01"

        #option #######################
        option_where_condition = "GOODSUID = '{0}'".format(now_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]')
            return "Q02"

        if dic['OptionKind'] == '300' or dic['OptionKind'] == 300 :
            goodsinfo_option_dic['GOODSUID'] = now_guid
            print('>> t_goods_option Insert')
            #print(goodsinfo_option_dic)
            try:
                db_con.insert('t_goods_option',goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]')
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
                print('>> Exception [t_goods_content]')
                err_flg = "1"
                return "Q01"
        else:
            content_where_condition = "uid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]')
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
                print('>> Exception [t_goods_sub]')
                err_flg = "1"
                return "Q01"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(now_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]')
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
                print('>> Exception [t_goods_category]')
                err_flg = "1"
                return "Q01"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]')
                err_flg = "1"
                return "Q01"
        
        print(">> 신규 상품 insert goods Ok : {}".format(rtn_goodscode))
    else:
        #####################################################################
        print(">> ## setDB Update ")
        #####################################################################
        goodsinfo_dic['naver_price_ck'] = "'0'"
        if str(dic['db_goodscode']) != "" or D_goodscode != "":
            if D_goodscode == "":
                D_goodscode = dic['db_goodscode']
            ## [naver_price 테이블 ] change_price 최저가 확인후 처리  
            sql_price = "select price, DATEDIFF(dd,isnull(update_date, regdate), getdate()) as diff_day from change_price where flag = '4' and goodscode = '{}'".format(D_goodscode)
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
            goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])

        if str(dic['del_naver']) == "7" :
            # 네이버에서 이미지 오류로 빠진 상품 -> del_naver -> null 로 변경
            goodsinfo_dic['del_naver'] = getQueryValue(None)
            goodsinfo_dic['before_del_naver'] = getQueryValue("7")
            print(">> del_naver 7 -> null 처리 : {}".format(dic['db_goodscode']))
        elif str(dic['del_naver']) == "5" :
            # 네이버에서 오래된 날짜 상품 (제외상품 다시 추가) -> del_naver -> null 로 변경
            goodsinfo_dic['del_naver'] = getQueryValue(None)
            goodsinfo_dic['before_del_naver'] = getQueryValue("5")
            print(">> del_naver 5 -> null 처리 : {}".format(dic['db_goodscode']))

        goodsinfo_dic['UpdateDate'] = 'getdate()'
        arr_where_condition = "uid = {0}".format(old_guid)
        print(">> old_guid : " +str(old_guid) + " | ck_isdisplay : "+str(ck_isdisplay) + " | ck_delnaver : " + str(ck_delnaver))
        ### Test ############################
        #print(goodsinfo_dic)
        try:
            db_con.update('t_goods', goodsinfo_dic, arr_where_condition)
            print('>> t_goods Update ')
        except Exception as e:
            print('>> Exception [t_goods]')
            err_flg = "1"
            return "Q02"

        # option #######################
        option_where_condition = "GOODSUID = '{0}'".format(old_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]')
            return "Q02"

        if dic['OptionKind'] == 300 or dic['OptionKind'] == '300':
            goodsinfo_option_dic['GOODSUID'] = old_guid
            print('>> t_goods_option UPdate:')
            #print(goodsinfo_option_dic)

            try:
                db_con.insert('t_goods_option', goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]')
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
                print('>> Exception [t_goods_content]')
                err_flg = "1"
                return "Q02"
        else:
            content_where_condition = "uid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]')
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
                print('>> Exception [t_goods_category]')
                err_flg = "1"
                return "Q02"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]')
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
                print('>> Exception [t_goods_sub]')
                err_flg = "1"
                return "Q02"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(old_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]')
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
                print('>> Exception [t_goods]')
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


# def getDesc(result_goods):
#     descript = result_goods
#     descript = getparse(result_goods,'shadow.innerHTML = "','[...shadow')
#     if descript.find('<div id="view-guide">') > -1: descript = getparse(descript,'','<div id="view-guide">')
#     if descript.find('<img src="/views/ali/imgs/attention.jpg') > -1: 
#         descript = getparse(descript,'','<img src="/views/ali/imgs/attention.jpg')
#     descript = descript.replace(";","").replace("<div style=>","").strip()
#     if descript.find('\\u') > -1:
#         descript = descript.replace('\\u', '/u')
#         descript = descript.replace('\\','').strip()
#         descript = descript.replace(r'/u', r'\u')
#         try:
#             descript = descript.encode('utf-8')
#             descript = descript.decode('unicode_escape')
#         except Exception as e:
#             print(">> descript decode Exception ...")
#             descript = descript.replace('\\','').strip()
#             descript = descript.replace("'","")
#             return descript
#     else:
#         descript = descript.replace('\\','').strip()
#     descript = descript.replace("'","")
#     return descript

def get_goods_title(result_goods, manage_dic, asin):

    title = getparse(str(result_goods),'<div class="title-area">','</div>')
    goods_title = getparse(str(title),'<h3 class="need-trans">','</h3>')
    if findChinese(goods_title): 
        goods_title = replaceQueryStringTitle(goods_title)
    org_url = getparse(str(title),'<a href="','"')
    print(">> goods_title : {}".format(goods_title))

    ########### title ###########
    goods_title = goods_title.replace(r'\x26', ' & ').replace("'", "").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('–','-').replace('・','.')
    goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '').replace('  ',' ')
    goods_title = replaceQueryString(goods_title)

    replace_title_list = manage_dic['replace_title_list']
    goods_title = replaceTitle(goods_title, replace_title_list)
    if goods_title == "E":
        print(">> ( exception replaceTitle  ) exit : " + str(asin))
        return "C01"

    if goods_title[-1:] == ".":
        goods_title = goods_title[:-1]
    if goods_title[-1:] == "|":
        goods_title = goods_title[:-1]
    goods_title = str(goods_title).replace("  ", " ").strip()

    print('>> goods_title (final) : ' + str(goods_title[:80]))
    if str(goods_title).strip() == "" or len(goods_title) < 5:
        print('>> no title ')
        return "D02"

    return goods_title

def proc_asin_parse_brower(gDic, db_con, db_ali, browser, in_pg, in_pgsite, db_price, manage_dic):
    
    guid = ""
    asin = gDic['asin']
    catecode = gDic['catecode']
    istmall = gDic['istmall']
    guid = gDic['guid']
    result_goods = ""
    path_file = os.getcwd()
    page_info_tmp = ""

    time.sleep(random.uniform(1,2))
    ## https://sharkda.kr/ali/view/code/taobao/itemId/782462164175/categoryNo/1276/pageNo/1
    goods_url = "https://sharkda.kr/ali/view/code/taobao/itemId/{}/categoryNo/{}/pageNo/1".format(asin, catecode)
    print(">> goods_url : {}".format(goods_url))

    try:
        browser.get(goods_url)
        print(">> browser.get ")
    except Exception as e:
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"
    time.sleep(random.uniform(5,8))
    proc = 0
    while(proc < 5):
        if str(browser.page_source).find('/imgs/system/error.png') > -1:
            print(">> 잠시만 기다려주세요...({})".format(proc))
            time.sleep(random.uniform(4,6))
        elif str(browser.page_source).find('503 Service Temporarily Unavailable') > -1:
            print(">> 잠시만 기다려주세요...(503 Temporarily)({})".format(proc))
            time.sleep(random.uniform(20,30))
            return "E99"
        else:
            break
        proc = proc + 1

    if str(browser.page_source).find('503 Service Temporarily Unavailable') > -1:
        print(">> 잠시만 기다려주세요...(503 Temporarily) (종료)")
        time.sleep(random.uniform(20,30))
        return "E99"

    result_goods = browser.page_source
    time.sleep(1)
    result_soup = BeautifulSoup(result_goods, 'html.parser')
    # print("result_goods : "+str(result_goods))
    option_item = ""
    title = ""
    descript = ""
    tran_title = ""
    tran_option = ""
    base_min_price = 0
    base_top_price = 0
    option_val_count = 0
    option_max_count = 100
    time.sleep(2)

    if str(browser.page_source) == "":
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"

    # 품절 체크
    if str(browser.page_source).find('타오바오내 재고가 없는 상품') > -1: # 품절 체크
        print('>> sold out : 此宝贝已下架 (품절) {}'.format(asin))
        return "D01"

    result_goods = str(browser.page_source)
    title = getparse(getparse(str(browser.page_source),'<div class="title-area">','</div>'),'<h3 class="need-trans">','</h3>')
    if findChinese(title):
        print(">> 중국어 발견 skip ")
        time.sleep(random.uniform(5,8))
        result_goods = browser.page_source
        title = getparse(getparse(str(browser.page_source),'<div class="title-area">','</div>'),'<h3 class="need-trans">','</h3>')
        if findChinese(title):
            print(">> 중국어 발견 skip ")
            return "C02"

    goods_title = get_goods_title((result_goods), manage_dic, asin)
    if goods_title == "C01":
        return "C01"
    elif goods_title == "D01":
        time.sleep(random.uniform(3,4))
        ## https://sharkda.kr/ali/view/code/taobao/itemId/782462164175/categoryNo/1276/pageNo/1
        goods_url = "https://sharkda.kr/ali/view/code/taobao/itemId/{}/categoryNo/{}/pageNo/1".format(asin, catecode)
        print(">> goods_url : {}".format(goods_url))
        try:
            browser.get(goods_url)
            print(">> browser.get (2) ")
        except Exception as e:
            print(">> Connect Error (SKIP): {}".format(goods_url))
            return "C01"
        time.sleep(random.uniform(5,8))
        goods_title = get_goods_title((result_goods), manage_dic, asin)
        if goods_title == "D01":
            return "D01"

    db_Weight = "0"
    DB_stop_update = "0"
    shipping_weight = 0
    db_OriginalPrice = 0
    db_Del_Naver = ""
    db_goodscode = ""
    db_imgB = ""
    db_isDisplay = ""
    # stop_update check
    if str(guid) == '' or guid is None:
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title, isnull(OriginalPrice,0), imgB, IsDisplay from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title, isnull(OriginalPrice,0), imgB, IsDisplay  from t_goods where uid = {0}".format(guid)

    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_title = rowUP[6]
        db_OriginalPrice = rowUP[7]
        db_imgB = rowUP[8]
        db_isDisplay = rowUP[9]
        shipping_weight = float(db_Weight)

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
    result_dic = dict()
    
    # title = getparse(str(result_goods),'<div class="title-area">','</div>')
    # goods_title = getparse(str(title),'<h3 class="need-trans">','</h3>')
    # if findChinese(goods_title): 
    #     goods_title = replaceQueryStringTitle(goods_title)
    # org_url = getparse(str(title),'<a href="','"')
    # print(">> goods_title : {}".format(goods_title))

    # ########### title ###########
    # goods_title = goods_title.replace(r'\x26', ' & ').replace("'", "").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('–','-').replace('・','.')
    # goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '').replace('  ',' ')
    # goods_title = replaceQueryString(goods_title)

    # replace_title_list = manage_dic['replace_title_list']
    # goods_title = replaceTitle(goods_title, replace_title_list)
    # if goods_title == "E":
    #     print(">> ( exception replaceTitle  ) exit : " + str(asin))
    #     return "C01"

    # if goods_title[-1:] == ".":
    #     goods_title = goods_title[:-1]
    # if goods_title[-1:] == "|":
    #     goods_title = goods_title[:-1]
    # goods_title = str(goods_title).replace("  ", " ").strip()

    # print('>> goods_title (final) : ' + str(goods_title[:80]))
    # if str(goods_title).strip() == "" or len(goods_title) < 5:
    #     print('>> no title ')

    #     return "D02"
    
    

    ########### title (checkForbidden_new) ###########
    ban_title_list = manage_dic['ban_title_list']
    forbidden_flag = checkForbidden_new(title, ban_title_list)
    if forbidden_flag == "E":
        print(">> ( exception checkForbidden_new  ) exit : " + str(asin))
        time.sleep(10)

        procEnd(db_con, browser)

    if str(forbidden_flag) == "0":
        pass
    else:
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # (사이트 DB) title 금지어 체크 ###########
    replace_site_title_list = manage_dic['replace_site_title_list']
    forbidden_flag_site = checkForbidden_site(title, catecode, replace_site_title_list)
    if str(forbidden_flag_site) != "0":
        print('>> checkForbidden_site : '+str(forbidden_flag_site))
        return "D03 :" + " ( site: " + forbidden_flag_site[2:] + " ) "


    result_json = getparse(str(result_goods),'var jsonData =','property="og:title"')

    ##### price #####
    price_kr = getparse(str(result_goods),'<strong class="price">','</strong>').strip()
    price_kr = price_kr.replace('원','').replace(',','')
    print(">> price_kr : {}".format(price_kr))

    price = getparse(str(result_json),'"price":',',').replace(',','').strip()
    print(">> price : {}".format(price))
    if str(price) == "0" or str(price) == "":
        print('>> No price Sold Out')
        return "D22"

    ######### shipping_category_weight / catecode의 minus_opt 플래그 확인 #############################
    d_minus_opt = ""
    d_coupon = ""   
    cate_weight = 0

    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(weight,0), bcate from t_category where CateCode = '{0}'".format(catecode)
    rsCate = db_con.selectone(sql2)
    if rsCate:
        d_minus_opt = rsCate[0]
        d_coupon = rsCate[1]
        cate_weight = rsCate[2]
        d_bcate = rsCate[3]
        d_minus_opt = str(d_minus_opt).strip()

    # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
    if str(d_bcate) == '1044' or str(d_bcate) == '1038' or str(d_bcate) == '1033':
        max_price = 'T'
        if float(price) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
            print('>> 1000 위안 (15만원) over (skip)')
            return "D49" + " ( " + str(price) + " ) "  # 800 위안 over
    else:
        max_price = 'F'

    ##### price check #####
    if float(price) < 1:
        print('>> 1 위안 미만 (skip)')
        return "D12" + " ( " + str(price) + " ) "  # 1 위안 미만

    if float(price) > 8000:
        print('>> 8000 위안 (150만원) over (skip)')
        return "D09" + " ( " + str(price) + " 위안) "  # 8000 위안 over

    if float(shipping_weight) < float(cate_weight):
        shipping_weight = cate_weight

    deposit_price = ""
    deposit_price = getparse(result_goods,'tb-service-items-option','</div>')
    if str(deposit_price).find('延长保修') > -1:
        deposit_price = getparse(deposit_price,'¥','')
        print('>> 연장보증금 (skip)')
        return "D49" + " ( " + str(deposit_price) + " ) " 

    ### image ###
    imgB = getparse(str(result_goods),'id="main-thumb"','</div>')
    imgB = getparse(imgB,'src="','"')
    print(">> imgB : {}".format(imgB))

    other_img_set = []
    if result_goods.find('id="sub-thumb"') > -1 :
        img_str = getparse(str(result_goods),'id="sub-thumb"','class="info-wrap"')
        other_img_list = img_str.split('<img ')
        for ea_other_img in other_img_list:
            ea_other_img = getparse(ea_other_img,' src="','"')
            if ea_other_img.find(".jpg") > -1:
                ea_other_img = getparse(ea_other_img, '', '.jpg') + str('.jpg')
            print(">> ea_other_img : {}".format(ea_other_img))
            if imgB == "" :
                imgB = ea_other_img
            else:
                other_img_set.append(ea_other_img)
        print(">> imgB : {}".format(imgB))

    ####### imgB 없으면  No img
    if str(imgB).strip() == "":
        print(">> No imag : {}".format(asin))
        if db_isDisplay == "T":
            return "C02"
        return "D19"

    if str(imgB)[:2] == "//":
        imgB = "https:" + str(imgB)
        print(">> imgB : {}".format(imgB))

    if str(db_imgB).strip() == "":
        print(">> 신규 이미지 ")
        result_dic['imgb_update_flg'] = None
    elif str(db_imgB).strip() == str(imgB).strip():
        print(">> 이미지 변경 없음 ")
        result_dic['imgb_update_flg'] = None
    else:
        print(">> 이미지 변경됨 ")
        result_dic['imgb_update_flg'] = '1'

    ShopId = ""
    print(">> ShopId : {}".format(ShopId))

    ### feature ###
    feature = ""

    #################################################################################
    ### descript ###
    #################################################################################
    descript = ""
    descript = getparse(result_goods,'shadow.innerHTML = "','[...shadow')
    if descript.find('<div id="view-guide">') > -1: descript = getparse(descript,'','<div id="view-guide">')
    if descript.find('<img src="/views/ali/imgs/attention.jpg') > -1: 
        descript = getparse(descript,'','<img src="/views/ali/imgs/attention.jpg')
    descript = descript.replace(";","").replace("<div style=>","").strip()

    if descript.replace('\\u00a0','').find('\\u') > -1:
        descript = descript.replace('\\u', '/u')
        descript = descript.replace('\\','').strip()
        descript = descript.replace(r'/u', r'\u')
        try:
            descript = descript.encode('utf-8')
            descript = descript.decode('unicode_escape')
        except Exception as e:
            print(">> descript decode Exception ...")
            return "C04"
    else:
        descript = descript.replace('\\','').strip()
    descript = descript.replace("'","").replace('"','')

    # with open(os.getcwd() + "/log/1688_desc_"+str(asin)+".html","w",encoding="utf8") as f: 
    #     f.write(str(descript))

    # if findChinese(descript):
    #     print(">> 중국어 발견 skip ")
    #     return "C02"
    #################################################################################

    result_dic['ali_no'] = asin
    result_dic['catecode'] = catecode
    result_dic['istmall'] = istmall
    result_dic['api_flg'] = None
    result_dic['api_date'] = None
    result_dic['title'] = title
    result_dic['price'] = price
    result_dic['price_tmp'] = float(price)
    result_dic['imgB'] = imgB
    result_dic['other_img_set'] = other_img_set
    result_dic['feature'] = feature
    result_dic['description'] = descript
    result_dic['shipping_weight'] = shipping_weight
    rtn_reviews_arr = []
    result_dic['review'] = rtn_reviews_arr
    result_dic['db_goodscode'] = db_goodscode
    result_dic['del_naver'] = db_Del_Naver
    result_dic['forbidden'] = 'F'
    result_dic['goods_title'] = goods_title
    result_dic['DE_title'] = goods_title
    result_dic['IT_title'] = goods_title

    base_min_price = price
    base_top_price = price

    ### 무료 배송 ###  
    taobao_shipping_fee = 0
    result_dic['taobao_shipping'] = ''

    ### option ###  
    option_area = getparse(str(result_goods),'id="option-area"','id="option-result-area"')
    result_options = getparse(str(result_json),'"skus":{','"props":')
    sp_option_kind = option_area.split('<div class="option-list')
    option_kind_name = ""
    for ea_kind in sp_option_kind:
        if ea_kind.find('class="need-trans title">') > -1:
            ea_kind_name = getparse(ea_kind,'class="need-trans title">','</div>') ##
            if option_kind_name.strip() == "":
                option_kind_name = ea_kind_name
            else:
                option_kind_name = option_kind_name + ' | ' + ea_kind_name
    print(">> option_kind_name : {}".format(option_kind_name))

    option_check = "" # 0 : No Option, 1 : Option Ok, X = Option Skip 
    if result_goods.find('var jsonData =') == -1:
        option_check = "0"
        print('No Option goods : {} '.format(asin))
        result_dic['OptionKind'] = None
        result_dic['many_option'] = '0'
    elif result_json.find('"skus":[]') > -1:
        option_check = "0"
        print('No Option goods : {} '.format(asin))
        result_dic['OptionKind'] = None
        result_dic['many_option'] = '0'
    else:
        option_check = "1"
        sp_options = result_options.split('},')
        sp_option_cnt = len(sp_options) -1
        print(">> Option Cnt : {}".format(sp_option_cnt))

        if sp_option_cnt > 300:
            option_max_count = 100
            print(">> Option Cnt 300 over ")

        if option_max_count > sp_option_cnt:
            option_max_count = sp_option_cnt
            ################ option max 값 한정하기 

    if option_check == "1":
        print('option item')
        result_dic['OptionKind'] = '300'
        result_dic['many_option'] = '1'
        option_code_dic = dict()
        option_value_dic = dict()
        option_value_org_dic = dict()
        option_price_dic = dict()
        option_img_dic = dict()

        option_min_price = 0
        option_max_price = 0
        option_val_count = 0
        opt_tran_cnt = 0
        option_ea_cnt = 0

        for option_ea in sp_options:
            option_ea_cnt = option_ea_cnt + 1
            if option_ea_cnt > option_max_count:
                break
            option_code = getparse(str(option_ea),'"sku_id":',',')
            option_id = getparse(str(option_ea),'"','":')
            option_price = getparse(str(option_ea),'"price":',',')
            option_price_won = getparse(str(option_ea),'"getPrice":',',')
            if option_price == "": 
                option_price = 0

            #옵션 가격 처리
            if option_min_price == 0 :
                option_min_price = option_price
            else:
                if option_min_price > option_price :
                    option_min_price = option_price
            if option_max_price == 0 :
                option_max_price = option_price
            else:
                if option_max_price < option_price :
                    option_max_price = option_price

            option_qty = getparse(str(option_ea),'"quantity":',',')
            option_img = getparse(str(option_ea),'"pic_url":"','"')
            print(">> ({}) {} : {} => {} ( {}원) stock: {} ".format(option_ea_cnt, option_id, option_code, option_price, option_price_won, option_qty))
            print(">> img : {}".format(option_img))

            if option_code == "":
                pass
            elif option_qty == "" or option_qty == "0":
                print(">> Option ({}) (Sold) : [{}] {} | {} ".format(option_ea_cnt, option_id, option_code, option_price))
            else:
                opt_set_cnt = 0
                sp_skdid = option_id.split(';')
                option_value = ""
                opt_val_tmp = ""
                for ea_sku in sp_skdid:
                    option_str = getparseR(str(option_area), '','data-prop="' +str(ea_sku)+ '"')
                    option_value = getparseR(option_str, 'value="','"').strip()
                    option_value = option_value.replace(r'\x26', '&').replace('\xa0', ' ').replace('&#39;', '`').replace('&amp;', '&').replace('&quot;', '').replace("'", "`").replace('"', '')
                    option_value = replaceQueryStringOption(option_value)
                    if opt_val_tmp == "":
                        opt_val_tmp = opt_val_tmp + option_value
                    else:
                        opt_val_tmp = opt_val_tmp + " | " + option_value

                if opt_val_tmp == "":
                    print(">> Option value Check Please : {}".format(opt_val_tmp))
                elif str(opt_val_tmp).find("사전판매") > -1 or str(opt_val_tmp).find("예약") > -1:
                    print(">> Option ({}) (사전판매/예약) Skip : [{}] {} | {} ".format(option_ea_cnt, option_id, option_code, option_price))
                elif str(opt_val_tmp).find("보증") > -1:
                    print(">> Option ({}) (보증) Skip : [{}] {} | {} ".format(option_ea_cnt, option_id, option_code, option_price))
                else:
                    print(">> Option ({}) [{}] {}  (price: {}) ".format(option_ea_cnt, option_code, opt_val_tmp, option_price))
                    opt_set_cnt = opt_set_cnt + 1
                    option_val_count = option_val_count + 1
                    option_value = option_value.replace(r'\x26', '&').replace('\xa0', ' ').replace('&#39;', '`').replace('&amp;', '&').replace('&quot;', '').replace("'", "`").replace('"', '')
                    option_value = replaceQueryStringOption(option_value)
                    option_code_dic[option_code] = option_id
                    option_price_dic[option_code] = float(option_price)
                    option_value_dic[option_code] = opt_val_tmp
                    option_value_org_dic[option_code] = option_value

                    # 옵션 이미지
                    sp_opt_img = option_area.split('class="need-trans-option option-select"')
                    for ea_img in sp_opt_img:
                        opt_img_txt = getparse(str(ea_img),'value="','"')
                        opt_img_txt = opt_img_txt.replace(r'\x26', '&').replace('\xa0', ' ').replace('&#39;', '`').replace('&amp;', '&').replace('&quot;', '').replace("'", "`").replace('"', '')
                        opt_img_txt = replaceQueryStringOption(opt_img_txt)
                        if str(ea_img).find('<img') > -1:
                            opt_img_url = getparse(str(ea_img),'src="','"')
                            if opt_img_url != "":
                                #print(">> {} : {}".format(opt_img_txt, opt_img_url))
                                option_img_dic[opt_img_url] = opt_img_txt


        print(">> option_value_dic : {}".format(option_value_dic))
        print(">> option_price_dic : {}".format(option_price_dic))
        print(">> option_img_dic : {}".format(option_img_dic))
        result_dic['option_value_dic_org'] = option_value_org_dic
        result_dic['option_img_dic_org'] = option_img_dic

        if option_val_count == 0:
            # No Option
            print(">> Option Goods - opmaxlen 0 : {}".format(asin))
            print('>> Option_value check .')
            return "D07"

        # min_price = min(option_price_dic.values())
        # top_price = max(option_price_dic.values())
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
            #print(">> Option Min Price : 0 ")
            pass
        else:
            base_min_price = min_price
        if top_price == 0 or top_price == 0.0:
            #print(">> Option Max Price : 0 ")
            pass
        else:
            base_top_price = top_price
        
        #print(">> Option Max Price : {} ({}) | Option Min Price : {} ( {} ) ".format(base_top_price, getWonpirce(db_ali2,base_top_price,exchange_rate), base_min_price, getWonpirce(db_ali2,base_min_price,exchange_rate)))
        print(">> Option Max Price : {} | Option Min Price : {} ".format(base_top_price, base_min_price))

    if option_check == "1" and option_val_count == 0:
        # No Option
        print(">> Option Goods - opmaxlen 0 : {}".format(asin))
        print('>> Option_value check .')
        return "D07"
    print(">> Option_val_count : {}".format(option_val_count))
    
    ##################################
    #d_minus_opt = "1"
    ##################################

    if d_minus_opt == "1": # 마이너스 옵션으로 set
        base_price_tmp = float(base_top_price)
        result_dic['price'] = float(base_top_price)
        result_dic['price_tmp'] = float(base_top_price)        
        print('>> 마이너스 옵션 set :' +str(base_price_tmp))
    else:
        base_price_tmp = float(base_min_price)
        result_dic['price'] = float(base_min_price)
        result_dic['price_tmp'] = float(base_min_price)        
        print('>> 플러스 옵션 set :' +str(base_price_tmp))

    deposit_price = "0"
    deposit_price = getparse(result_goods,'延长保修','"')
    if str(deposit_price) != "":
        deposit_price = getparse(deposit_price,'¥','')
        if deposit_price.isdigit():
            base_price_tmp = base_price_tmp + float(deposit_price)
            print('>> 보증연장금 추가 : ' +str(deposit_price))
            print('>> base_price_tmp 변경 : ' +str(base_price_tmp))

    tmp_coupon = gDic['py_coupon']
    tmp_coupon = int(tmp_coupon)
    result_dic['minus_opt'] = str(d_minus_opt)
    result_dic['coupon'] = str(tmp_coupon)
    print('>> (DB) goods minus_opt : '+str(result_dic['minus_opt']))

    if option_check == "":
        print(">> Goods option_check : {}".format(asin))
        return "D07"            
    else:
        # originalprice
        if d_minus_opt == '1':
            originalprice = float(result_dic['price']) * float(gDic['py_exchange_Rate'])
            print(">> originalprice ( {} * {} ) : {}".format(result_dic['price'],gDic['py_exchange_Rate'],originalprice))
        else:
            originalprice = float(result_dic['price_tmp']) * float(gDic['py_exchange_Rate'])
            print(">> originalprice ( {} * {} ) : {}".format(result_dic['price_tmp'],gDic['py_exchange_Rate'],originalprice))
        originalprice = int(originalprice)

        # 배대지 배송비
        delievey_fee = 5900 #
        delievey_fee = float(getDeliveryFee(gDic, shipping_weight))
        #print(">> delievey_fee : {} ".format(delievey_fee))

        # 타오바오 유료배송비
        taobao_shipping_fee = taobao_shipping_fee * float(gDic['py_exchange_Rate']) * 2
        result_dic['taobao_shipping_fee'] = taobao_shipping_fee      
        #print(">> taobao_shipping_fee : {} ".format(taobao_shipping_fee))

        ########### goodsmoney ###########
        goodsmoney = 0
        goodsmoney = getWonpirce(gDic, base_price_tmp)
        print(">> goodsmoney (마진플러스): {} + (배대지) {} + (유료배송) {} ".format(goodsmoney, delievey_fee, taobao_shipping_fee))
        goodsmoney = goodsmoney + delievey_fee + taobao_shipping_fee
        goodsmoney = int(round(goodsmoney, -2))
        print(">> goodsmoney (Sum) ({}) ".format(goodsmoney))

        if float(goodsmoney) < 23000:
            goodsmoney = 23000
            print('>> goodsmoney 23,000원 이하 -> 23,000 set: ' + str(goodsmoney)) 
        sale_goodsmoney = int(goodsmoney) * ((100-tmp_coupon) / 100)
        print('>> (sale price) : ' + str(sale_goodsmoney)) 
        marjin = sale_goodsmoney - (originalprice + (delievey_fee/2))
        print('>> (sale marjin) : {} ( {} %)'.format(marjin, (marjin/sale_goodsmoney * 100)))    

        if goodsmoney >= 3000000:
            print('>> goodsmoney Over : '+str(goodsmoney))
            return "D09 :" + " ( " + str(goodsmoney) + "원)"

        low_price = float(result_dic['price']) * float(gDic['py_exchange_Rate']) + (int(taobao_shipping_fee) * (100-tmp_coupon) / 100) + (int(delievey_fee) * (100-tmp_coupon) / 100)
        print('>> low_price : {} (환율 {}) '.format(float(result_dic['price']) * float(gDic['py_exchange_Rate']), float(gDic['py_exchange_Rate'])))
        print('>> taobao_shipping_fee : {} | 배대지 : {} '.format((int(taobao_shipping_fee) * (100-tmp_coupon) / 100),(int(delievey_fee) * (100-tmp_coupon) / 100)))
        low_price = int(low_price)
        print('>> low_price (최저원가) : ' + str(low_price))
        result_dic['low_price'] = low_price

        result_dic['forbidden'] = 'F'                    
        result_dic['title'] = tran_title
        result_dic['OriginalPrice'] = originalprice
        result_dic['delivery_fee'] = delievey_fee
        result_dic['goodsmoney'] = goodsmoney
        result_dic['db_OriginalPrice'] = float(db_OriginalPrice)

        if option_check == "1":
            result_dic['option_code_dic'] = option_code_dic
            result_dic['option_price_dic'] = option_price_dic
            result_dic['option_value_dic'] = option_value_dic
            result_dic['option_img_dic'] = option_img_dic
            result_dic['option_max_min_diff'] = float(option_max_price) - float(option_min_price)

            # 옵션 조합 
            option_item = generateOptionString(gDic, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, tmp_coupon)
            print(">> Option_item : {}".format(option_item))
            if option_item.find("/0") == -1:
                print('>> option_value check (0원 옵션 없음) : {}'.format(asin))
                return "D07"
            if option_item.find("화물") > -1 or option_item.find("계약") > -1 or option_item.find("보증") > -1 or option_item.find("예약") > -1 or option_item.find("경매") > -1 or option_item.find("교환") > -1 or \
                option_item.find("무료배송") > -1 or option_item.find("무료 배송") > -1 or option_item.find("환불 불가") > -1 or option_item.find("환불불가") > -1 or option_item.find("파손") > -1 or \
                option_item.find("반품 불가") > -1 or option_item.find("반품불가") > -1 or option_item.find("선주문") > -1 or option_item.find("도착 예정") > -1 or option_item.find("보상") > -1 or \
                option_item.find("위안") > -1 or option_item.find("보증") > -1 or option_item.find("사전 판매") > -1 or option_item.find("인증서") > -1 or option_item.find("맞춤") > -1 \
                or option_item.find("본인 부담") > -1 or option_item.find("배송 불가") > -1 or option_item.find("문의") > -1 or option_item.find("가격 변경") > -1:
                print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(asin))
                return "D47"

            if findChinese(option_item):
                print(">> (옵션) 중국어 발견 skip ")
                return "C02"

            option_item = option_item.replace("`","")
            result_dic['Items'] = getQueryValue(option_item)

        ###### ######################################################################
        rtnFlg = setDB_proc(asin, result_dic, db_con, in_pg, guid, db_price)
        #rtnFlg = "0@"
        ####### ######################################################################
        if rtnFlg[:2] != "0@":
            if rtnFlg == "D01":
                print(">> ## t_goods Option /0 없음 에러 (품절처리 필요)  ##")
                return "D57"
            else:
                print('>> setDB error --> DB check Rollback ')
                sql = "select top 1 uid,IsDisplay,OptionKind from t_goods where ali_no = '{0}'".format(asin)
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
                return str(rtnFlg) # exit


    return "0"


def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

def version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn):

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
            db_ali.close()            
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


def version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn):
    
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

def procEnd(db_con, in_drive):
    time.sleep(1)
    print(">> procEnd : " + str(datetime.datetime.now()))
    db_con.close()
    in_drive.quit()
    time.sleep(2)
    os._exit(0)

def procWork(db_con, db_ali, in_drive, in_pg, in_ip):
    print('>> procWork : ' + str(datetime.datetime.now()))
    ip_catecode = ""
    sql = "select catecode from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(ip) + " ] Catecode No. ")
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(ip) + " ] Catecode : " + str(ip_catecode))

        sql = "update update_list2 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list2 (getdate) ")
        db_con.execute(sql)
    return "0"


def newlist(db_con, db_ali, in_drive, in_pg, in_ip):
    cateidx = ""
    sql = "select * from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        # sql = "select top 1 catecode from T_Category_BestAsin where isTmall = 'F' and catecode not in (select catecode from update_list2) order by up_date"
        # sql = "select top 1 catecode from T_Category_BestAsin as a left join t_goods as g on g.ali_no = a.asin where a.isTmall = 'F' and a.del_flg is null and g.ali_no is not null and g.api_flg is null and catecode not in (select catecode from update_list2) order by up_date "
        # sql = "select top 1 catecode from T_Category_BestAsin as a left join t_goods as g on g.ali_no = a.asin where a.isTmall = 'F' and a.del_flg is null and catecode not in (select catecode from update_list2) order by up_date "
        sql = "select top 1 catecode from T_Category_BestAsin as a left join t_goods as g on g.ali_no = a.asin where a.del_flg is null and catecode not in (select catecode from update_list2) order by up_date "
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> Error newlist ')
                # proc end
                procEnd(db_con, in_drive)
    else:
        sql = "select count(*) from update_list2 where proc_ip = '{0}'".format(in_ip)
        rows = db_con.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list2 where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list2 where proc_ip='{0}' order by regdate desc)".format(in_ip)
            db_con.execute(sql)

        sql = "select catecode, now_page from update_list2  where proc_ip = '{0}'".format(in_ip)
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            now_page = row[1]
            if now_page > 2:
                now_page = 2

            sql = "update update_list2 set now_page = {0} ,regdate=getdate() where proc_ip='{1}'".format(now_page, in_ip)
            db_con.execute(sql)

    return cateidx

def get_asinset(in_catecode,db_con):
    asinset = []
    #sql = "select top 100 asin, a.isTmall, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.isTmall = 'F' and a.catecode = '{0}' order by newid()".format(in_catecode)
    #sql = "select top 100 asin, a.isTmall, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.isTmall = 'F' and a.del_flg is null and t.ali_no is not null and t.api_flg is null and a.catecode = '{0}' order by newid()".format(in_catecode)
    #sql = "select top 100 asin, a.isTmall, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.isTmall = 'F' and a.del_flg is null and t.api_flg is null and a.catecode = '{0}' order by newid()".format(in_catecode)
    #sql = "select top 100 asin, a.isTmall, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.del_flg is null and a.catecode = '{0}' order by newid()".format(in_catecode)
    sql = "select top 100 asin, a.isTmall, t.Uid from T_Category_BestAsin as a left join ( select uid, cate_idx, ali_no from t_goods where cate_idx = '" +str(in_catecode)+ "' ) as t on t.ali_no = a.asin where a.catecode = '" +str(in_catecode)+ "' "        
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
        isTmall = ea_asin[1]
        Duid = ea_asin[2]
        if Duid is None or Duid == "" or Duid == None:
            Duid = ""
        if asin is None or asin == "" or asin == None:
            pass
        else:
            asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(isTmall) + '@' + str(Duid))
    return asinset

# Stock ###################################################################################
def get_stock_asin(db_con, in_sql1, in_sql2, in_sql3):
###########################################################################################
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
            isTmall = ea_asin[1]
            cateidx = ea_asin[2]
            uid = ea_asin[3]
            if uid is None or uid == "" or uid == None:
                uid = ""
            if asin is None or asin == "" or asin == None:
                pass
            else:
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(isTmall) + '@' + str(uid))

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
                isTmall = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if uid is None or uid == "" or uid == None:
                    uid = ""
                if asin is None or asin == "" or asin == None:
                    pass
                else:
                    asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(isTmall) + '@' + str(uid))


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
                isTmall = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if uid is None or uid == "" or uid == None:
                    uid = ""
                if asin is None or asin == "" or asin == None:
                    pass
                else:
                    asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(isTmall) + '@' + str(uid))

    if chk_data == "0":
        return ""

    return asinset

def moveSlide(driver):
    print('slide proc')
    #//*[@id="nc_1_n1z"]
    slider = driver.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
    slider = None
    if slider != None:
        move = ActionChains(driver)
        move.click_and_hold(slider).perform()
        print('slide click hold')
        driver.implicitly_wait(2)
        move.move_by_offset(20, 1).perform()
        driver.implicitly_wait(1)
        move.move_by_offset(250, 0).perform()
        time.sleep(1)

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def set_multi(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic, db_price, manage_dic):
    if str(manage_dic['ip_vpn']).upper() == "V":
        in_ip = mac_addr()
    else:
        in_ip = currIp
    pgName = goods_dic['py_pgFilename']
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, db_ali, browser, in_ver, pgName, in_pgKbn)

    cateidx = newlist(db_con, db_ali, browser, pgName, in_ip)
    print('>> newlist() catecode : {} | in_ip : {}'.format(cateidx, in_ip))
    if cateidx == "":
        print('>> catecode parsing complete : ' + str(cateidx))
        return "11"

    # asin get
    get_asin_list = []
    get_asin_list = get_asinset(cateidx, db_con)
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(cateidx))
        return "11"

    allCnt = 0
    c_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        time.sleep(1)
        sp_asin = asin_low.split('@')
        asin = sp_asin[0]
        catecode = sp_asin[1]
        istmall = sp_asin[2]
        guid = sp_asin[3]
        print("\n\n\n### {} : ### [ {} ] (catecode : {}) #################################################".format(allCnt, asin, catecode))
        if allCnt == 1 or allCnt == 50:
            procWork(db_con, db_ali, browser, "", in_ip)
        print('>> version : '+str(in_ver))

        goods_dic['asin'] = str(asin)
        goods_dic['catecode'] = str(catecode)
        goods_dic['istmall'] = str(istmall)
        goods_dic['guid'] = str(guid)

        rtnChk = proc_asin_parse_brower(goods_dic, db_con, db_ali, browser, pgName, "taobao", db_price, manage_dic)  
        print('>> [ rtnChk ] : ' + str(rtnChk))
        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "T" or rtnChk[:1] == "E" or rtnChk[:1] == "P":
            print('>> proc_asin_parse_brower (OK) ')
        else:
            rtnChk = "E01"

        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            procLogSet(db_con, pgName, " ( E99 ) exit - asin: " + str(asin))
            rtnChk = "E99"
            break

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05":  # blocked
            c_Errcnt = c_Errcnt + 1
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
        elif rtnChk_no == "T01" or rtnChk_no == "T02":
            print('>> # Tmall Goods : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        dic_b = dict()
        dic_b['asin'] = "'" + asin + "'"
        dic_b['cate_idx'] = catecode
        dic_b['memo'] = "'" + getMemo(rtnChk) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "
        dic_b['isTmall'] = "'" + istmall + "'"

        if rtnChk != "0":  
            if rtnChk_no[:1] == "D" or rtnChk_no == "T02" or rtnChk_no == "T01" or rtnChk_no == "P01":
                D_naver_in = ""
                D_goodscode = ""
                if str(guid) == '' or guid is None or guid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where ali_no = '{0}'".format(asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where uid = '{0}'".format(guid)                    
                rs = db_con.selectone(sql)
                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    DDel_Naver = rs[2]
                    D_regdate = rs[3]
                    D_UpdateDate = rs[4]
                    D_naver_in = rs[5]
                    D_goodscode = rs[6]
                    print(">> [{}] regdate : {} | UpdateDate : {}".format(D_goodscode, D_regdate, D_UpdateDate))
                    # T_goods sold out
                    if DIsDisplay == 'T':
                        if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                            sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1' where uid = {0}".format(Duid)
                            db_con.execute(sql_u1)
                            sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
                            db_con.execute(sql_u2)
                            print(">> Forbidden 금지어 판매불가 상품처리: " + str(asin_low))
                        elif rtnChk_no == "T02":
                            sql = "update T_goods set istmall = 'T', IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
                            print(">> sql : " + str(sql))
                            print(">> Tmall 품절 stock_ck update: " + str(asin_low))
                            db_con.execute(sql)
                        else:
                            if rtnChk_no == "P01":
                                print('>> [' + str(asin) + '] setDisplay ((T) 품절 처리 보류 - skip) :' + str(Duid))                               
                                sql = "update T_goods set stock_ck = '7', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(Duid)
                                print(">> sql : " + str(sql))
                                print(">> 품절 처리 보류 (P01) : " + str(asin_low))
                                db_con.execute(sql)
                            else:
                                print('>> [' + str(asin) + '] setDisplay (품절 처리) :' + str(Duid))
                                #setDisplay(Duid, 'F', '', db_con)                                
                                sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate() where uid='{0}'".format(Duid)
                                print(">> sql : " + str(sql))
                                print(">> 품절 처리 OK : " + str(asin_low))
                                db_con.execute(sql)

                        # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                        if rtnChk_no[:1] == "D" and str(D_naver_in) == "1":
                            proc_ep_insert(D_goodscode,'D')

                    if DIsDisplay == 'F' and rtnChk_no == "P01":
                        print('>> [' + str(asin) + '] setDisplay ((F) 품절 처리 보류 - skip) :' + str(Duid))                          
                        sql = "update T_goods set stock_ck = '7', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(Duid)
                        print(">> sql : " + str(sql))
                        print(">> 품절 처리 보류 (P01) : " + str(asin_low))
                        db_con.execute(sql)

                    if rtnChk_no == "T01":
                        sql = "update T_goods set istmall = 'T', stock_ck = '5', UpdateDate=getdate() where uid='{0}'".format(Duid)
                        print(">> sql : " + str(sql))
                        print(">> Ok stock_ck update : " + str(asin_low))
                        db_con.execute(sql)

                    # elif rtnChk_no == "P01":
                    #     sql = "update T_goods set UpdateDate=getdate() where uid='{0}'".format(Duid)
                    #     print(">> sql : " + str(sql))
                    #     print(">> Ok stock_ck update : " + str(asin_low))
                    #     db_con.execute(sql)
                

            # elif rtnChk_no == "T01":
            #     sql = "update T_goods set istmall = 'T', stock_ck = '5', UpdateDate=getdate() where asin='{0}'".format(asin)
            #     print(">> sql : " + str(sql))
            #     print(">> Ok stock_ck update : " + str(asin_low))
            #     db_con.execute(sql)

            # elif rtnChk_no == "T02":
            #     sql = "update T_goods set istmall = 'T', IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
            #     print(">> sql : " + str(sql))
            #     print(">> Ok stock_ck update : " + str(asin_low))
            #     db_con.execute(sql)

            sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(asin)
            db_con.execute(sql)
            db_con.insert('T_Category_BestAsin_del', dic_b)  # insert
            print('>> ##insert## : T_Category_BestAsin_del')

        sql = "delete from T_Category_BestAsin where asin ='{0}'".format(asin)
        db_con.execute(sql)
        print(">> Errcnt : {0}".format(c_Errcnt))

        if rtnChk_no[:1] == "C":
            time.sleep(2)
            if c_Errcnt > 20:
                print('>> ( c_Errcnt 15 over ) exit - catecode :' + str(cateidx))
                procLogSet(db_con, pgName, " ( c_Errcnt 20 over ) exit - catecode: " + str(cateidx))
                procEnd(db_con, browser)

    if rtnChk == "E99":
        return rtnChk

    return "0"


def get_update_goods(in_site, db_FS, db_con):
    asinset = []
    tmp_guid = ""
    chk_data = ""

    sql = " select top 100  guid, sitecate, display_ali_no, regdate, upddate, flg_chk "
    sql = sql + " from amazon_goods_update "
    # ql = sql + " where flg_chk ='0' and sitecate = 'cn' and isnull(istmall,'') <> 'T' "
    sql = sql + " where flg_chk ='0' and sitecate = 'cn' "
    sql = sql + " order by RegDate asc "

    rs_row = db_FS.select(sql)
    print('>> ##select all## sql :' + str(sql))

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
        sql = "select top 25 ali_no, price, cate_idx, uid, isTmall from t_goods where uid in " + str(tmp_guid) 
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
                isTmall = ea_asin[4]
                if (price is None) or (price == ''):
                    price = 'null'
                if asin == "" or asin is None or asin == None:
                    pass
                else:
                    asinset.append(str(asin) + '@' + str(cate_idx) + '@' + str(isTmall) + '@' + str(uid))

        if chk_data == "0":
            return ""

    return asinset

# Stock ###################################################################################
def set_updatelist(db_FS, db_con, db_ali, in_drive, in_pgsite, in_ver, goods_dic, db_price, manage_dic):
###########################################################################################
    print('>> set_updatelist ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    pgName = goods_dic['py_pgFilename']
    if str(manage_dic['ip_vpn']).upper() == "V":
        in_ip = mac_addr()
    else:
        in_ip = currIp 

    # asin get
    get_asin_list2 = []
    get_asin_list2 = get_update_goods(in_pgsite, db_FS, db_con)
    print(get_asin_list2)

    if str(get_asin_list2).rfind('@') == -1:
        print('>> 우선 없데이트 처리 대상 없음. (완료)')
        return "0"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist2 = 0
    cnt_asinlist2 = len(get_asin_list2)
    rtnChk = ""
    print('>> (get_asin_list2) len :' + str(cnt_asinlist2))

    for asin_low in get_asin_list2:
        tmp_msg = ""
        allCnt = allCnt + 1

        sp_asin = asin_low.split('@')
        asin = sp_asin[0]
        catecode = sp_asin[1]
        istmall = sp_asin[2]
        guid = sp_asin[3]

        print('\n\n ----------------- < (stock check) set_updatelist [' + str(cnt_asinlist2) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')
        if allCnt == 1 or allCnt == 50:
            procWork(db_con, db_ali, in_drive, "", in_ip)
        print('>> version : '+str(in_ver))

        goods_dic['asin'] = str(asin)
        goods_dic['catecode'] = str(catecode)
        goods_dic['istmall'] = str(istmall)
        goods_dic['guid'] = str(guid)

        try:
            rtnChk = proc_asin_parse_brower(goods_dic, db_con, db_ali, in_drive, pgName, "taobao", db_price, manage_dic)  
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_updatelist Exception Error ' )
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

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            return "E99"

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05":  # blocked
            c_Errcnt = c_Errcnt + 1
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
        elif rtnChk_no == "T01":
            print('>> # Tmall Goods : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))
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
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]
            d_naver_in = rs_row[8]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))
            print(">> d_naver_in : " + str(d_naver_in))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        print('>> Forbidden 금지어일 경우 판매불가 상품처리 ')
                        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1', NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(
                            rtn_uid)
                        db_con.execute(sql_u1)

                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(rtn_uid)
                        db_con.execute(sql_u2)
                    else:
                        print('>> [' + str(rtn_asin) + '] setDisplay (품절 처리) :' + str(rtn_uid))
                        #setDisplay(rtn_uid, 'F', '', db_con)      
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                        print(">> sql : " + str(sql))
                        print(">> 품절 처리 OK : " + str(d_GoodsCode))
                        db_con.execute(sql)

                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no == "T01":
                sql = "update T_goods set istmall = 'T', stock_ck = '5', UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "P01":
                sql = "update T_goods set stock_ck = '7', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> 품절 처리 보류 (P01) : " + str(asin_low))
                db_con.execute(sql)

            elif rtnChk_no == "0":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            # blocked 경우 amazon_goods_update 테이블 regdate + 1 다음에 다시 시도
            if rtnChk_no == "P01" or rtnChk_no[:1] == "C" or rtnChk_no[:1] == "Q" or rtnChk_no[:1] == "E":
                sql = "update amazon_goods_update set flg_chk = '0', regdate = regdate + 1 where guid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)
            else:
                if rtnChk_no == "T01":
                    sql = "update amazon_goods_update set istmall = 'T', memo = 'Tmall goods ' where guid = '{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> amazon_goods_update update : " + str(d_GoodsCode))
                    db_FS.execute(sql)
                else:
                    sql = "update amazon_goods_update set flg_chk = '1', upddate = getdate() where guid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> amazon_goods_update  : " + str(rtn_uid))
                    db_FS.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))

        if rtnChk_no[:1] == "C":
            if c_Errcnt > 15:
                print('>> ( 접속불가 ) exit -  :' + str(asin_low))
                time.sleep(1)
                #print('\n time.sleep(1)')
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, pgName, " 접속불가 또는 에러발생 : " + str(asin_low))
                # proc end
                procEnd(db_con, in_drive)

    if rtnChk_no == "E99":
        print('>> E99 Exit : ' + str(rtnChk_no))
        return rtnChk_no

    return "F"

# Stock ##################################################################################################
def set_stock_multi(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic, db_price, manage_dic):
##########################################################################################################
    print('>> set_stock_multi ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0

    pgName = goods_dic['py_pgFilename']
    sql1 = goods_dic['py_sql1']
    sql2 = goods_dic['py_sql2']
    sql3 = goods_dic['py_sql3']
    if str(manage_dic['ip_vpn']).upper() == "V":
        in_ip = mac_addr()
    else:
        in_ip = currIp 

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, db_ali, browser, in_ver, pgName, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, sql1, sql2, sql3)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(in_ip))
        return "11"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        time.sleep(1)
        sp_asin = asin_low.split('@')
        asin = sp_asin[0]
        catecode = sp_asin[1]
        istmall = sp_asin[2]
        guid = sp_asin[3]

        goods_dic['asin'] = str(asin)
        goods_dic['catecode'] = str(catecode)
        goods_dic['istmall'] = str(istmall)
        goods_dic['guid'] = str(guid)

        print("\n\n\n### {} : ### [ {} ] (catecode : {}) #################################################".format(allCnt, asin, catecode))
        if allCnt == 1 or allCnt == 50:
            procStockWork(db_con, "", in_ip)
        print('>> version : '+str(in_ver))
        print('\n\n')
        print('>> version : '+str(in_ver))

        try:
            rtnChk = proc_asin_parse_brower(goods_dic, db_con, db_ali, browser, pgName, "taobao", db_price, manage_dic)  
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_multi Exception Error (asin_low) : ' + str(asin_low))
            if rtnChk == "":
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_parse_brower (OK) -- ')

        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            procLogSet(db_con, pgName, " ( E99 ) exit - asin: " + str(asin))
            return "E99"

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05":  # blocked
            c_Errcnt = c_Errcnt + 1
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
        elif rtnChk_no == "T01" or rtnChk_no == "T02":
            print('>> # Tmall Goods : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(guid) + "'"
        print('>> ##selectone## sql :' + str(sql))
        rs_row = db_con.selectone(sql)

        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]
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
                        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', stock_ck = '1' where uid = {0}".format(guid)
                        db_con.execute(sql_u1)
                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(guid)
                        db_con.execute(sql_u2)
                        print(">> Forbidden 금지어 판매불가 상품처리: " + str(asin_low))
                    else:
                        print('>> [' + str(asin) + '] setDisplay (품절 처리) :' + str(guid))                              
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(guid)
                        print(">> sql : " + str(sql))
                        print(">> 품절 처리 OK : " + str(asin_low))
                        db_con.execute(sql)

                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(guid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no == "T01":
                sql = "update T_goods set istmall = 'T', stock_ck = '5', UpdateDate=getdate() where uid='{0}'".format(guid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "T02":
                sql = "update T_goods set istmall = 'T', IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(guid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "P01":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = '7' where uid='{0}'".format(guid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "0":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{0}'".format(guid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            else:  # blocked
                sql = "update T_goods set stock_ck = '1', UpdateDate = UpdateDate - 3 where uid='{0}'".format(guid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        if rtnChk_no[:1] == "C":
            if c_Errcnt > 15:
                print('>> ( c_Errcnt 15 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, pgName, " c_Errcnt 15 over exit : " + str(asin_low))
                procEnd(db_con, browser)

    if rtnChk_no == "E99":
        print('>> E99 Exit : ' + str(rtnChk_no))
        return rtnChk_no

    return "0"

def procStockWork(db_con, in_pg, in_ip):
    
    print('>> procStockWork : ' + str(datetime.datetime.now()))
    ip_catecode = ""
    sql = "select proc_ip from update_list3 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] proc_ip No : " + str(ip))
        sql = "insert into update_list3 (regdate, proc_ip) values (getdate(),'{0}')".format(in_ip)
        print(">> insert update_list3 (getdate) ")
        db_con.execute(sql)
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] proc_ip : " + str(ip_catecode))
        sql = "update update_list3 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update update_list3 (getdate) ")
        db_con.execute(sql)

    return "0"

# stock_out ###############################################################################
def set_stock_out(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic, manage_dic):
    print('>> set_stock_out ')
    if str(manage_dic['ip_vpn']).upper() == "V":
        in_ip = mac_addr()
    else:
        in_ip = currIp 
    pgName = goods_dic['py_pgFilename']

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, db_ali, browser, in_ver, pgName, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, goods_dic['py_sql1'], goods_dic['py_sql2'], goods_dic['py_sql3'])
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> get_asin_list parsing complete : ' + str(ip))
        return "1"

    allCnt = 0
    c_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt == 1 or allCnt == 50:
            procStockWork(db_con, pgName, ip)
            time.sleep(1)

        spm_asin = asin_low.split('@')
        goods_dic['asin'] = spm_asin[0]
        goods_dic['catecode'] = spm_asin[1]
        goods_dic['istmall'] = spm_asin[2]
        goods_dic['guid'] = spm_asin[3]

        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> --- < (set_stock_out) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' ---')

        rtnChk = proc_asin_out_brower(goods_dic, db_con, db_ali, browser, manage_dic)
        print('>> [ rtnChk ] : ' + str(rtnChk))
        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "T" or rtnChk[:1] == "E" or rtnChk[:1] == "P01":
            print('>> proc_asin_out_brower (OK) ')
        else:
            rtnChk = "E01"

        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            return "E99"

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06":  # blocked
            c_Errcnt = c_Errcnt + 1
            print('>> # blocked 에러 : ' + str(rtnChk))
        elif rtnChk_no == "S01":
            print('>> # update stop goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "S02":
            print('>> # naver noclick goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB
            print('>> # SetDB Insert error : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB
            print('>> # SetDB Update error : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            print('>> # Error E99: ' + str(rtnChk))
        elif rtnChk_no == "E01":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "T01" or rtnChk_no == "T02":
            print('>> # Tmall goods : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
            print('>> # SetDB OK (완료) : ' + str(rtnChk))
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))
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
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]
            d_naver_in = rs_row[8]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))
            print(">> d_naver_in : " + str(d_naver_in))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    print('>> IsDisplay Update (F) 품절처리 ')
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

            elif rtnChk_no == "T01":
                sql = "update T_goods set istmall = 'T', stock_ck = '5', UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "T02":
                sql = "update T_goods set istmall = 'T', IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)
                if d_IsDisplay == 'T':
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

            elif rtnChk_no == "P01":
                sql = "update T_goods set UpdateDate=getdate(), stock_ck = '7' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok UpdateDate update : " + str(d_GoodsCode))
                db_con.execute(sql)

            else:  # blocked
                sql = "update T_goods set stock_ck = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)

        print(">> Errcnt : {0} ".format(c_Errcnt))
        if rtnChk_no[:1] == "C":
            time.sleep(2)
            if c_Errcnt > 15:
                print('>> ( c_Errcnt 15 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, pgName, " c_Errcnt 15 over exit : " + str(asin_low))
                procEnd(db_con, browser)

    return "0"



# 재고 체크
def proc_asin_out_brower(gDic, db_con, db_ali, browser, manage_dic):
    print('>> proc_asin_out_brower ')
    guid = ""
    asin = gDic['asin']
    catecode = gDic['catecode']
    istmall = gDic['istmall']
    guid = gDic['guid']
    result_goods = ""
    time.sleep(3)

    time.sleep(random.uniform(1,2))
    goods_url = "https://sharkda.kr/ali/view/code/taobao/itemId/{}/categoryNo/{}/pageNo/1".format(asin, catecode)
    print(">> goods_url : {}".format(goods_url))

    try:
        browser.get(goods_url)
        print(">> browser.get ")
    except Exception as e:
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"
    time.sleep(random.uniform(5,8))
    proc = 0
    while(proc < 5):
        if str(browser.page_source).find('/imgs/system/error.png') > -1:
            print(">> 잠시만 기다려주세요...({})".format(proc))
            time.sleep(random.uniform(4,6))
        elif str(browser.page_source).find('503 Service Temporarily Unavailable') > -1:
            print(">> 잠시만 기다려주세요...(503 Temporarily)({})".format(proc))
            time.sleep(random.uniform(20,30))
            return "E99"
        else:
            break
        proc = proc + 1

    if str(browser.page_source).find('503 Service Temporarily Unavailable') > -1:
        print(">> 잠시만 기다려주세요...(503 Temporarily) (종료)")
        time.sleep(random.uniform(20,30))
        return "E99"

    result_goods = browser.page_source
    title = getparse(getparse(str(browser.page_source),'<div class="title-area">','</div>'),'<h3 class="need-trans">','</h3>')
    if findChinese(title):
        print(">> 중국어 발견 skip ")
        time.sleep(random.uniform(5,8))
        result_goods = browser.page_source
        title = getparse(getparse(str(browser.page_source),'<div class="title-area">','</div>'),'<h3 class="need-trans">','</h3>')
        if findChinese(title):
            print(">> 중국어 발견 skip ")
            return "C02"

    time.sleep(1)
    result_soup = BeautifulSoup(result_goods, 'html.parser')
    title = ""
    time.sleep(2)

    if browser.page_source == "":
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"

    # 품절 체크
    if str(browser.page_source).find('타오바오내 재고가 없는 상품') > -1: # 품절 체크
        print('>> sold out : 此宝贝已下架 (품절) {}'.format(asin))
        return "D01"

    db_Weight = "0"
    DB_stop_update = "0"
    shipping_weight = 0
    db_Del_Naver = ""
    db_goodscode = ""
    db_isDisplay = ""
    # stop_update check
    if str(guid) == '' or guid is None:
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title, isnull(OriginalPrice,0), imgB, IsDisplay from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title, isnull(OriginalPrice,0), imgB, IsDisplay  from t_goods where uid = {0}".format(guid)

    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_title = rowUP[6]
        db_OriginalPrice = rowUP[7]
        db_imgB = rowUP[8]
        db_isDisplay = rowUP[9]
        shipping_weight = float(db_Weight)

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
    result_dic = dict()
    result_goods = str(result_goods)
    title = getparse(str(result_goods),'<div class="title-area">','</div>')
    goods_title = getparse(str(title),'<h3 class="need-trans">','</h3>')
    if findChinese(goods_title): 
        goods_title = replaceQueryStringTitle(goods_title)
    org_url = getparse(str(title),'<a href="','"')
    print(">> goods_title : {}".format(goods_title))

    ########### title ###########
    goods_title = goods_title.replace(r'\x26', ' & ').replace("'", "").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('–','-').replace('・','.')
    goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '').replace('  ',' ')
    goods_title = replaceQueryString(goods_title)

    replace_title_list = manage_dic['replace_title_list']
    goods_title = replaceTitle(goods_title, replace_title_list)
    if goods_title == "E":
        print(">> ( exception replaceTitle  ) exit : " + str(asin))
        time.sleep(10)
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
        procEnd(db_con, browser)

    if str(forbidden_flag) == "0":
        pass
    else:
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # (사이트 DB) title 금지어 체크 ###########
    replace_site_title_list = manage_dic['replace_site_title_list']
    forbidden_flag_site = checkForbidden_site(title, catecode, replace_site_title_list)
    if str(forbidden_flag_site) != "0":
        print('>> checkForbidden_site : '+str(forbidden_flag_site))
        return "D03 :" + " ( site: " + forbidden_flag_site[2:] + " ) "

    result_json = getparse(str(result_goods),'var jsonData =','property="og:title"')

    ##### price #####
    price_kr = getparse(str(result_goods),'<strong class="price">','</strong>').strip()
    price_kr = price_kr.replace('원','').replace(',','')
    print(">> price_kr : {}".format(price_kr))

    price = getparse(str(result_json),'"price":',',').replace(',','').strip()
    print(">> price : {}".format(price))
    if str(price) == "0" or str(price) == "":
        print('>> No price Sold Out')
        return "D22"

    ######### shipping_category_weight / catecode의 minus_opt 플래그 확인 #############################
    d_minus_opt = ""
    cate_weight = 0

    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(weight,0), bcate from t_category where CateCode = '{0}'".format(catecode)
    rsCate = db_con.selectone(sql2)
    if rsCate:
        d_minus_opt = rsCate[0]
        d_coupon = rsCate[1]
        cate_weight = rsCate[2]
        d_bcate = rsCate[3]
        d_minus_opt = str(d_minus_opt).strip()

    # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
    if str(d_bcate) == '1044' or str(d_bcate) == '1038' or str(d_bcate) == '1033':
        max_price = 'T'
        if float(price) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
            print('>> 1000 위안 (15만원) over (skip)')
            return "D49" + " ( " + str(price) + " ) "  # 800 위안 over
    else:
        max_price = 'F'

    ##### price check #####
    if float(price) < 1:
        print('>> 1 위안 미만 (skip)')
        return "D12" + " ( " + str(price) + " ) "  # 1 위안 미만

    if float(price) > 8000:
        print('>> 8000 위안 (150만원) over (skip)')
        return "D09" + " ( " + str(price) + " 위안) "  # 8000 위안 over

    if float(shipping_weight) < float(cate_weight):
        shipping_weight = cate_weight

    deposit_price = ""
    deposit_price = getparse(result_goods,'tb-service-items-option','</div>')
    if str(deposit_price).find('延长保修') > -1:
        deposit_price = getparse(deposit_price,'¥','')
        print('>> 연장보증금 (skip)')
        return "D49" + " ( " + str(deposit_price) + " ) " 

    ### image ###
    imgB = getparse(str(result_goods),'id="main-thumb"','</div>')
    imgB = getparse(imgB,'src="','"')
    print(">> imgB : {}".format(imgB))

    other_img_set = []
    if result_goods.find('id="sub-thumb"') > -1 :
        img_str = getparse(str(result_goods),'id="sub-thumb"','class="info-wrap"')
        other_img_list = img_str.split('<img ')
        for ea_other_img in other_img_list:
            ea_other_img = getparse(ea_other_img,' src="','"')
            if ea_other_img.find(".jpg") > -1:
                ea_other_img = getparse(ea_other_img, '', '.jpg') + str('.jpg')
            print(">> ea_other_img : {}".format(ea_other_img))
            if imgB == "" :
                imgB = ea_other_img
            else:
                other_img_set.append(ea_other_img)
        print(">> imgB : {}".format(imgB))

    ####### imgB 없으면  No img
    if str(imgB).strip() == "":
        print(">> No imag : {}".format(asin))
        if db_isDisplay == "T":
            return "C02"
        return "D19"


    return "0"


# 재고 체크
def proc_asin_out_brower_new(gDic, db_con, db_ali, browser):
    print('>> proc_asin_out_brower_new ')
    guid = ""
    asin = gDic['asin']
    catecode = gDic['catecode']
    istmall = gDic['istmall']
    guid = gDic['guid']
    result_goods = ""
    time.sleep(3)
    goods_url = 'https://open-demo.otcommerce.com/?p=item&id=' +str(asin)
    print(">> goods_url : {}".format(goods_url))

    try:
        browser.get(goods_url)
        time.sleep(random.uniform(2.5,3))
        result_goods = str(browser.page_source)
        print(">> page_source ")
    except Exception as e:
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"    
    time.sleep(1)

    if str(result_goods).find('Quantity:') == -1:
        print(">> 품절 (No Quantity) : {}".format(asin))
        return "D01"

    if str(result_goods).find('does not exist or it has been removed') > -1:
        print(">> 품절 (removed) : {}".format(asin))
        return "D01"

    if result_goods == "":
        print(">> Connect Error (SKIP): {}".format(goods_url))
        return "C01"
    else:
        curr_page = ""
        curr_page = browser.current_url
        if str(curr_page).find('/member/login') > -1:
            print(">> Connect page Error (E99) : {}".format(curr_page))
            return "E99"

        db_Weight = "0"
        DB_stop_update = "0"
        db_goodscode = ""
        if str(guid) == '' or guid is None:
            guid = ''
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title from t_goods where ali_no = '{0}'".format(asin)
        else:
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title from t_goods where uid = {0}".format(guid)

        rowUP = db_con.selectone(sql)
        if rowUP:
            DB_stop_update = rowUP[0]
            db_Weight = rowUP[1]
            db_uid = rowUP[2]
            db_Del_Naver = rowUP[3]
            db_goodscode = rowUP[4]
            db_org_title = rowUP[5]
            db_title = rowUP[6]
            shipping_weight = float(db_Weight)

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

        print('>> stop_update No goods : ' + str(asin))
        if str(guid) == '':
            print('>>>>>>>>>>>>>>>>>>>>> no guid (신규) ')
        else:
            print('>>>>>>>>>>>>>>>>>>>>> guid (존재) : ' + str(guid))

        # 품절 체크
        if str(result_goods).find('Item not allowed') > -1:
            print('>> Item not allowe : {}'.format(asin))
            if str(result_goods).find('deleted by vendor') > -1:
                print('>> deleted by vendor : {}'.format(asin))
                return "D01"
        else:
            if str(result_goods).find('js-panel-buttons panel-buttons') > -1:
                print(">> Buy now Ok : {} ".format(asin))
            else:
                print('>> No Buy now (품절) {}'.format(asin))
                return "D01"

        if str(browser.current_url).find('/member/login.jhtml') > -1:
            print('>> login.jhtml : {}'.format(asin))
            return "E99"

    if str(result_goods).find("we have detected unusual traffic from your network") > -1:
        print(">> we have detected unusual traffic from your network : {}".format(asin))
        return "E99"

    return "0"


# set_stock_out_new ###############################################################################
def set_stock_out_new(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic):
    print('>> set_stock_out_new ')
    pgName = goods_dic['py_pgFilename']
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, db_ali, browser, in_ver, pgName, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, goods_dic['py_sql1'], goods_dic['py_sql2'], goods_dic['py_sql3'])
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> get_asin_list parsing complete : ' + str(ip))
        return "1"

    allCnt = 0
    c_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt == 1 or allCnt == 50:
            procStockWork(db_con, pgName, ip)
            time.sleep(1)

        spm_asin = asin_low.split('@')
        goods_dic['asin'] = spm_asin[0]
        goods_dic['catecode'] = spm_asin[1]
        goods_dic['istmall'] = spm_asin[2]
        goods_dic['guid'] = spm_asin[3]

        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> --- < (set_stock_out_new) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' ---')

        rtnChk = proc_asin_out_brower_new(goods_dic, db_con, db_ali, browser)
        print('>> [ rtnChk ] : ' + str(rtnChk))
        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "T" or rtnChk[:1] == "E":
            print('>> proc_asin_out_brower_new (OK) ')
        else:
            rtnChk = "E01"

        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            return "E99"

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06":  # blocked
            c_Errcnt = c_Errcnt + 1
            print('>> # blocked 에러 : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
            print('>> # SetDB OK (완료) : ' + str(rtnChk))
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))
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
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]
            d_naver_in = rs_row[8]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))
            print(">> d_naver_in : " + str(d_naver_in))

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    print('>> IsDisplay Update (F) 품절처리 ')
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
            time.sleep(2)
            if c_Errcnt > 15:
                print('>> ( c_Errcnt 15 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, pgName, " c_Errcnt 15 over exit : " + str(asin_low))
                procEnd(db_con, browser)

    return "0"
