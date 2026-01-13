import re
import time
import os
import random
import urllib
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

                if str(browser.page_source).find('class="input-prepend"') > -1:
                    print(">> Login input-prepend ... ")
                    input(">> Login prepend Check : ")
                    time.sleep(2)
                else:
                    if browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[3]/div/button'):
                        browser.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/div/form/div[3]/div/button').click()
                        time.sleep(1)

    return "0"

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


def connectDriverOld(pgSite, kbn):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
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
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, mode, type):
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
    if type == "H":
        option.add_argument("--headless") # headless

    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver
    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

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
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_argument("user-data-dir={}".format(userProfile))
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options) 

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')  
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random())\
            + " Safari/537.36, 'Referer': 'https://open-demo.otcommerce.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'brave':
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return browser

def replaceStr(in_word) :
    result = in_word.replace("'","`")
    result = result.replace("★","").replace("◆","").replace("/"," & ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","ー").replace("&times;"," x ").replace("、"," . ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")
    result = result.replace('\ue244','').replace('■','')

    return result

def getEndpage(db_con, listname):
    rtnPage = 30
    sql = " select endpage from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]
    print(">> getEndpage : "+str(rtnPage))
    return rtnPage

def getEndasin(db_con, listname):
    rtnAsin = 30000
    sql = " select endasin from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]
    print(">> getEndasin : "+str(rtnAsin))
    return rtnAsin

def getSortType(db_con, listname):
    rtnType = ''
    sql = " select sort_type from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnType = rs[0]
    print(">> getSortType : "+str(rtnType))
    return rtnType

def getSet(db_con, listname):
    endpage = 30
    endasin = 30000
    sort_type = ""
    min_qty_order = 1
    sql = " select endpage, endasin, sort_type, min_qty_order from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        endpage = rs[0]
        endasin = rs[1]
        sort_type = rs[2]
        min_qty_order = rs[3]
    return endpage, endasin, sort_type, min_qty_order

def getAsinCnt(db_con, list):
    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin where cate_idx > 3000 "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

def has_duplicates(seq):
    len1 = len(seq)
    len2 = len(set(seq))
    dupCnt = len1 - len2
    return dupCnt


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