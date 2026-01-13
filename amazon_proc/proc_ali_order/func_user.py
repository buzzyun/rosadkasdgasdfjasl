import datetime
import time
import os
import random
import requests
import re
from selenium import webdriver
import chromedriver_autoinstaller
import socket
import socks
import http.client
import time
from stem import Signal
from stem.control import Controller

# 파싱함수
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

# 파싱함수 (뒤에서 부터 찾아서 파싱)
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

def connectDriver(tool, mode, site):
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
        #path = "C:\project\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        if mode == "S":
            options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': '" +str(site)+ "'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        #browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

    elif tool == 'chrome_secret':
        #path = "C:\project\chromedriver.exe"
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
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        #browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

    elif tool == 'brave':
        path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return browser


def set_new_ip():
    # disable socks server and enabling again
    socks.setdefaultproxy()
    """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(3)
    response = conn.getresponse()
    print('current ip address :', response.read())

def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)


def getQueryValue(in_value):
    if in_value == None:
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

# 정규식 체크 : 특수문자/숫자/영문/한글
def regStrChk(in_str):
    result = ""
    chkStr = str(in_str).replace(' ', '')
    chkStr = chkStr.strip()
    regStr = re.search('[^. %–|<>&`()+A-Za-z0-9가-힣]+', chkStr)
    if (regStr):
        result = "1"
    else:
        result = "0"
    return result

# 정규식 체크 : 일본어 체크 (Katakana/Hiragana/Kanji)
def regJpStrChk(in_str):
    result = ""
    chkStr = str(in_str).replace(' ', '')
    chkStr = chkStr.strip()

    # 일본어(Katakana/Hiragana/Kanji)
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+", chkStr)
    if (regStr):
        result = "1"  # 일본어 포함
    else:
        result = "0"  # 일본어 없음

    return result

# 특수문자 replace
def replaceQueryString(in_word):
    result = in_word.replace("'", "`")
    result = result.replace("★", "").replace("◆", "").replace(
        "/", " | ").replace(",", " ").replace("&lt;", "<").replace("&gt;", ">")
    result = result.replace(r'\x26', ' ').replace('&amp;', ' & ').replace(
        '&AMP;', ' & ').replace('&nbsp;', ' ').replace('&NBSP;', ' ')
    result = result.replace(
        "&ndash;", "-").replace("&times;", " x ").replace("–", "-")
    result = result.replace("&#39;", "`").replace(
        "&quot;", "").replace("\\", "").replace("®", "")
    result = result.replace("【", "(").replace("】", ")").replace(
        "()", "").replace("[]", "").replace(";", "")

    return result

# 상품코드 생성 goodscode
def getGoodsCode(uid, goodshead):
    result = goodshead+str(uid).zfill(10)
    return result

# 상품 guid 가져오기 (goodscode --> guid)
def getGuid(gCode):
    rtn_guid = ""
    tmpGuid = str(gCode)[2:]
    tmpGuid = str(tmpGuid).lstrip("0")
    rtn_guid = str(tmpGuid).replace("N", "")
    return str(rtn_guid)

# 상품코드의 사이트명 가져오기
def getSiteName(gCode):
    sitename = ""
    gHead = str(gCode)[:1]
    if gHead == "G":
        sitename = "fashion"
    elif gHead == "A":
        sitename = "auto"
    elif gHead == "B":
        sitename = "beauty"
    elif gHead == "Y":
        sitename = "baby"
    elif gHead == "E":
        sitename = "electron"
    elif gHead == "F":
        sitename = "furniture"
    elif gHead == "I":
        sitename = "industry"
    elif gHead == "J":
        sitename = "jewelry"
    elif gHead == "O":
        sitename = "office"
    elif gHead == "S":
        sitename = "sports"
    elif gHead == "Q":
        sitename = "usa"
    elif gHead == "X":
        sitename = "best"
    elif gHead == "V":
        sitename = "global"
    elif gHead == "D":
        sitename = "de"
    elif gHead == "N":
        sitename = "mall"
    elif gHead == "L":
        sitename = "cn"
    elif gHead == "K":
        sitename = "uk"
    elif gHead == "H":
        sitename = "handmade"
    elif gHead == "Z":
        sitename = "red"
    elif gHead == "W":
        sitename = "mini"
    elif gHead == "P":
        sitename = "shop"
    elif gHead == "T":
        sitename = "trend"
    elif gHead == "R":
        sitename = "ref"
    elif gHead == "C":
        gHead_2 = str(gCode)[:2]
        if gHead_2 == "CG":
            sitename = "fashion2"
        elif gHead_2 == "CA":
            sitename = "auto2"
        elif gHead_2 == "CY":
            sitename = "baby2"
        elif gHead_2 == "CE":
            sitename = "electron2"
        elif gHead_2 == "CF":
            sitename = "furniture2"
        elif gHead_2 == "CI":
            sitename = "industry2"
        elif gHead_2 == "CJ":
            sitename = "jewelry2"
        elif gHead_2 == "CO":
            sitename = "office2"
        elif gHead_2 == "CS":
            sitename = "sports2"
        elif gHead_2 == "CB":
            sitename = "beauty2"

    return sitename
