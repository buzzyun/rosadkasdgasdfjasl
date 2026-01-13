# -*- coding: utf-8 -*-
import datetime
import os
import time
import sys
import random
import socket
import socks
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import threading
import re
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

db_ali = DBmodule_FR.Database('aliexpress')

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

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace(',','|').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp

def do_proc(db_con, browser, proc_name):

    sql = "select top 50 catecode, name from t_category where tran_check is null order by catecode asc"
    rows= db_con.select(sql)
    print('##select ## sql :' + str(sql))
    if not rows:
        print('>> 대상 없음 (exit) ')
        return "1"
    print(len(rows))

    url_link = "https://dev.freeship.co.kr/_GoodsUpdate/" + str(proc_name)
    print('>> url_link : ' + str(url_link))
    browser.get(url_link)
    time.sleep(4)
    result2 = browser.page_source
    time.sleep(2)
    if str(result2).find('<div class="skiptranslate') == -1:
        print('>> 대상 없음 ' )
        return "1" 

    tran_result = getparse(str(result2), 'id="google_translate_element">','<div class="skiptranslate goog-te-gadget"')
    sp_item = str(tran_result).split('<input type="hidden"')
    lowCnt = 0
    cnt = 0
    unmatch_cnt = 0
    for rs in rows:
        cnt = cnt + 1
        tran_catename = ""
        db_catecode = ""
        db_catecode = rs[0]
        db_catename = rs[1]
        if str(result2).find(' value="{}">'.format(db_catecode)):
            tmp_item = getparse(str(result2),' value="' +str(db_catecode)+ '">','</pre>')
            tran_catename = getparse(str(tmp_item),'<font style="vertical-align: inherit;">','</font>')
            tran_catename = tran_catename.replace('<font style="vertical-align: inherit;">','').replace("'","").strip()
            tran_catename = replace_str(tran_catename)
        if str(tran_catename).strip() == "":
            print(">> No Catename (skip) : {}".format(tran_catename))
        else:
            print(">> {} | {} | {} ".format(db_catecode, db_catename, tran_catename))
            uSql = " update t_category set kor_name = '{}', tran_check = '1' where catecode = '{}'".format(tran_catename, db_catecode)
            #print(">> {} | Update ".format(db_catecode))
            db_con.execute(uSql)
        lowCnt = lowCnt + 1

    return "0"


if __name__ == '__main__':
    print(">> Start etsy_title_tran ")
    print(str(datetime.datetime.now()))

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    #path = "C:\\project\\chromedriver.exe"
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    options = webdriver.ChromeOptions()
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    #options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.binary_location = brave_path
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    browser.implicitly_wait(3)

    db_con = DBmodule_FR.Database("REF")

    proc_name = "title_tran_ref_cate.asp"
    rtn_flg = "0"
    while( rtn_flg == "0"):
        try:
            rtn_flg = do_proc(db_con, browser, proc_name)
        except Exception as e:
            print('>> 예외가 발생 (종료) : ', e)
            time.sleep(5)
            break
        else:
            time.sleep(1)
        if rtn_flg != "0":
            print(">> Error Exit ")
            break
        time.sleep(random.uniform(5,15))

    db_con.close()
    browser.quit()
    print(str(datetime.datetime.now()))
    print(">> End ebay category tran end ")
    os._exit(0)

