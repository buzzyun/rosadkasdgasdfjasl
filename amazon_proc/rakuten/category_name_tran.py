# -*- coding: utf-8 -*-
import datetime
import os
import time
import sys
import random
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

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


def get_replace_title(str_title):

    tmp_title = str(str_title).strip()
    tmp_title = tmp_title.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ').replace("&lt;","<").replace("&gt;",">")
    tmp_title = tmp_title.replace("&ndash;","-").replace("&times;"," x ").replace("&rdquo;","").replace('–','-').replace('「',' ').replace('」',' ')
    tmp_title = tmp_title.replace("&quot;","").replace("\\", "").replace("★","").replace("◆","").replace('"', '').replace('  ', ' ')

    return tmp_title

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

#reg 일본어 체크
def regJpStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+",chkStr) #일본어(Katakana/Hiragana/Kanji)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

#reg 일본어 체크
def replace_regJpStrChk(in_str):
    result = ""
    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+",chkStr) #일본어(Katakana/Hiragana/Kanji)
    result = in_str.replace(regStr[0],' ')
    if len(result) == "":
        result = in_str

    return str(result).replace('  ',' ').strip()

# 상품 guid 가져오기 (goodscode --> guid)
def getGuid(gCode):
    rtn_guid = ""
    tmpGuid = str(gCode)[2:]
    tmpGuid = str(tmpGuid).lstrip("0")
    rtn_guid = str(tmpGuid).replace("N", "")

    return str(rtn_guid)

###############################################

def replace_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").replace("<hr>","").strip()
    
    return result_str

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()

    return result_str

def connectDriver(pgSite):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    # option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)

    return browser


def connectDriverNew(pgSite):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument("--disable-gpu")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)

    return browser


def do_proc(db_con, browser):
    time.sleep(1)
    sql = "select top 100 catecode, name from T_CATEGORY where tran_check is null order by catecode asc"
    rows= db_con.select(sql)
    print('##select ## sql :' + str(sql))
    if not rows:
        print('>> 대상 없음 (exit) ')
        return "1"

    url_link = "https://dev.freeship.co.kr/_GoodsUpdate/rakuten_catecode_name_tran.asp" 
    print('>> url_link : ' + str(url_link))
    browser.get(url_link)
    time.sleep(4)
    result2 = browser.page_source
    time.sleep(1)

    if str(result2).find('<div class="skiptranslate') == -1:
        print('>> 대상 없음 ' )
        return "1" 

    lowCnt = 0
    tran_source = getparse(str(result2),'<div id="google_translate_element">','')
    if str(tran_source).find('<pre>') > -1:
        tran_source = getparse(str(tran_source),'<pre>','')
    if str(tran_source).find('</pre>') > -1:
        tran_source = getparse(str(tran_source),'','</pre>')
    sp_tran = tran_source.split('<input type="hidden"')
    for ea_item in sp_tran:
        time.sleep(0.1)
        tran_title = ""
        #print(">> ea_item : {}".format(ea_item))
        ea_tmp = getparse(ea_item,'value="','')
        ea_catecode = getparse(ea_tmp,'','"')
        ea_catecode = str(ea_catecode).replace("\u200b","").replace(",","").replace(" ","").replace("'","").strip()
        if ea_tmp.find('<div>') > -1:
            ea_tmp = str(ea_tmp).replace("<div>","").replace("</div>","").replace("'","").strip()
        tran_title = getparse(ea_tmp,'>','')
        tran_title = replace_main_str(tran_title).replace('<hr>','')
        tran_title = tran_title.replace("?"," ").replace("  "," ").strip() # ? 제거하기
        if str(ea_catecode) == "":
            print(">> [{}] No ea_catecode or check ea_catecode : {}".format(lowCnt, ea_tmp))
        else:
            print('>> [{}] {} | {}'.format(lowCnt, ea_catecode, tran_title))
            tran_title = tran_title.replace("'","").strip()

            if str(tran_title).find('inherit;">') > -1:
                tran_title = getparse(str(tran_title),'inherit;">','')
            print("[{}] {} | {}".format(lowCnt, ea_catecode, tran_title))
            
            if str(tran_title) != "":
                sqlu = "update t_category set kor_name = '{}', tran_check = '1' where catecode = '{}'".format(tran_title, ea_catecode)
                print(">> update : {}".format(ea_catecode))
                db_con.execute(sqlu)

        lowCnt = lowCnt + 1

    return "0"

if __name__ == '__main__':

    print(">> Start etsy_title_tran ")
    print(str(datetime.datetime.now()))

    browser = connectDriverNew('https://dev.freeship.co.kr')
    browser.set_window_size(1100, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    db_con = DBmodule_FR.Database('shop') #rakuten

    proc_flg = "0"
    while proc_flg == "0":
        sql = "select top 1 catecode, name from T_CATEGORY where tran_check is null "
        rows= db_con.select(sql)
        print('##select ## sql :' + str(sql))
        if not rows:
            print('>> 대상 없음 (exit) ')
            proc_flg = "1"
        else:
            do_proc(db_con, browser)

    db_con.close()
    browser.quit()
    print(str(datetime.datetime.now()))
    print(">> End etsy_title_tran ")
    os._exit(0)
