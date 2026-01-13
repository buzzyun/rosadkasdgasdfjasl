import time
import os
import random
import urllib
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium import webdriver
import socket
import socks
import http.client
import time
from datetime import datetime
from stem import Signal
from stem.control import Controller
import subprocess


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

def connectDriverSub():
    filePath = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeTEMP"') # 디버거 크롬 구동
    subprocess.Popen(filePath) # 디버거 크롬 구동

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    browser = webdriver.Chrome(options=option)

    return browser

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'

    proc = ""
    try:
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
        print(">> C:\Program Files (x86)\Google\Chrome ")
    except FileNotFoundError:
        print(">> C:\Program Files\Google\Chrome ")
        proc = subprocess.Popen(filePath)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(options=option)

    return proc, browser

def connectDriverOld(pgSite, mode):
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
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    if str(pgSite).find('etsy') == -1:
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")

    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    if str(pgSite).find('etsy') == -1:
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver
    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser


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
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
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
    elif gHead == "K":
        sitename = "uk"
    elif gHead == "L":
        sitename = "cn"
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

def elem_clear(elem):
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)

def naver_login_in(driver):

    # 로그인 ID/PASS 입력
    elem11 = driver.find_element(By.ID,'login_username')
    elem_clear(elem11)
    elem11.send_keys('freeshipcps')
    time.sleep(0.5)
    elem22 = driver.find_element(By.ID,'login_password')
    elem_clear(elem22)
    elem22.send_keys('@allin#am1071')
    time.sleep(1)
    # 로그인 버튼 클릭
    alogin = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "login_button")))
    alogin.click()
    print('>> 로그인 버튼 클릭 Ok')

    return "0"


def getDatetime(type):

    now = datetime.now()
    if type == "0":
        # print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        # 문자열 변환 :  2021-12-22 15:46:26
        return now.strftime('%Y-%m-%d %H:%M:%S')
    elif type == "1":
        # print("현재 : ", now)
        # 현재 :  2021-12-22 15:46:26.695840
        return now
    elif type == "2":
        # print("현재 날짜 : ", now.date())
        # 현재 날짜 :  2021-12-22
        return now.date()
    elif type == "3":
        # print("현재 시간 : ", now.time())
        # 현재 시간 :  15:46:26.695840
        return now.time()
    elif type == "4":
        # print("timestamp : ", now.timestamp())
        # timestamp :  1640155586.69584
        return now.timestamp()
    elif type == "5":
        # print("년 : ", now.year)
        # 년 :  2021
        return now.year
    elif type == "6":
        # print("월 : ", now.month)
        # 월 :  12
        return now.month
    elif type == "7":
        # print("일 : ", now.day)
        # 일 :  22
        return now.day
    elif type == "8":
        # print("시 : ", now.hour)
        # 시 :  15
        return now.hour
    elif type == "9":
        # print("분 : ", now.minute)
        # 분 :  46
        return now.minute
    elif type == "10":
        # print("초 : ", now.second)
        # 초 :  26
        return now.second
    elif type == "11":
        # print("마이크로초 : ", now.microsecond)
        # 마이크로초 :  695840
        return now.microsecond
