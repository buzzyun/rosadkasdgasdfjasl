import os
os.system('pip install --upgrade selenium')
import re
import time
import datetime
import os
import random
import requests
import urllib
import json
from stem import Signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen
from stem.control import Controller
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

def connectDriverOld(pgSite, kbn, type):
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
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer':'" + str (pgSite) + "'")
    browser = webdriver.Chrome(options=option)
    return browser

def connectDriverNew(pgSite, kbn, type):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
        print(">> ChromeDriverManager install ")
    except Exception as e:
        print(e)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

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


#db 특수단어 제거
def replaceQueryString(in_word) :
    result = in_word.replace("'","`").replace("&rdquo;"," ").replace('”',' ')
    result = result.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")

    return result

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace('/',' . ').replace(',',' . ').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp

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

def billChk(browser, db_con):
    billChk = "https://open-demo.otcommerce.com/admin/?cmd=Reports&do=billing"
    browser.get(billChk)
    print(">> url : {}".format(billChk))
    time.sleep(4)
    if str(browser.page_source).find('Balance:') > -1:
        Billing = getparse(str(browser.page_source),'Balance:','</div>')
        Billing = getparse(Billing,'class="badge weight-normal font-13">','$').strip()
        print(">> Balance: {}".format(Billing))
        time.sleep(2)
        if str(Billing).replace('.','').isdigit():
            uSql = "update python_version_manage set api_balance = {}, api_balance_date = getdate() where name = 'goods_api'".format(Billing)
            print(">> uSql : {}".format(uSql))
            db_con.execute(uSql)
    return "0"

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

def set_language(browser):
    lang_name = ""
    print(">> set_language ")
    if browser.find_element(By.XPATH,'//*[@id="select-language"]/img'):
        time.sleep(0.5)
        lang_name = browser.find_element(By.XPATH,'//*[@id="select-language"]/img').accessible_name
        if str(lang_name).find('Korean') > -1:
            print(">> Korean OK ")
        else:
            browser.find_element(By.XPATH,'//*[@id="select-language"]').click()
            time.sleep(0.5)
            browser.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/div[3]/div/div/div/ul/li[2]').click()
            time.sleep(4)

            if browser.find_element(By.XPATH,'//*[@id="select-language"]/img'):
                lang_name = browser.find_element(By.XPATH,'//*[@id="select-language"]/img').accessible_name

    return str(lang_name)