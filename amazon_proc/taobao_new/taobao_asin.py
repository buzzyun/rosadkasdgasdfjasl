import os
os.system('pip install --upgrade selenium')
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.chrome.service as Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import subprocess
import pyperclip
import time
import socket
import os
import urllib
import threading
import sys
import DBmodule_FR

global endpage
global ver
global glogin_id
global glogin_pass
ver = "01.15"

glogin_id = "1stplatform_jin"
glogin_pass = "Order1071tao*"

def version_check(cursor):
    global browser
    print("version:" + ver)
    file_path = r"c:/project/"
    file_name = "new_taobao_asin.exe"
    sql = "select version,url from python_version_manage where name = 'list'"
    rows = cursor.selectone(sql)
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        # os.system("taskkill /f /im geckodriver.exe")
        time.sleep(10)
        return False
    else:
        return True

def connectDriverOld(pgSite, mode, type):
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
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser


# def connectDriverOld(pgSite, kbn):
#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#     driver_path = f'./{chrome_ver}/chromedriver.exe'
#     if os.path.exists(driver_path):
#         print(f"chrom driver is insatlled: {driver_path}")
#     else:
#         print(f"install the chrome driver(ver: {chrome_ver})")
#         chromedriver_autoinstaller.install(True)
#     time.sleep(1)
#     option = Options()
#     username = os.getenv("USERNAME")
#     userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#     option.add_experimental_option('excludeSwitches', ['enable-logging'])
#     option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
#     option.add_experimental_option("useAutomationExtension", False) 
#     option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#     option.add_argument("--disable-blink-features=AutomationControlled") 
#     option.add_argument("--disable-features=VizDisplayCompositor")
#     option.add_argument("--disable-gpu")
#     if str(kbn) == "Y":
#         option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
#     option.add_argument("user-data-dir={}".format(userProfile))
#     option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
#     browser = webdriver.Chrome(options=option)

#     return browser

# def connectDriverNew(pgSite, kbn):
#     option = Options()
#     username = os.getenv("USERNAME")
#     userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#     option.add_experimental_option('excludeSwitches', ['enable-logging'])
#     option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
#     option.add_experimental_option("useAutomationExtension", False) 
#     option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#     option.add_argument("--disable-blink-features=AutomationControlled") 
#     option.add_argument("--disable-features=VizDisplayCompositor")
#     option.add_argument("--disable-gpu")
#     if str(kbn) == "Y":
#         option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
#     option.add_argument("user-data-dir={}".format(userProfile))
#     option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")

#     browser = ""
#     try:
#         s = Service(ChromeDriverManager().install())
#         browser = webdriver.Chrome(service=s, options=option)
#     except Exception as e:
#         print(e)
#         # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
#         # browser = webdriver.Chrome(service=s, options=option)
#         latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
#         latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
#         service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
#         browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
#         driver_executable_path = service.path
#     return browser

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
        # options = webdriver.ChromeOptions() 
        # options.add_argument("--disable-blink-features=AutomationControlled") 
        # user_ag = UserAgent().random 
        # options.add_argument('--no-sandbox')
        # options.add_argument('user-agent=%s'%user_ag) 
        # options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        # options.add_experimental_option("useAutomationExtension", False) 
        # options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        # #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        # browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        # #크롤링 방지 설정을 undefined로 변경 
        # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

        options = webdriver.ChromeOptions() 
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_argument("user-data-dir={}".format(userProfile))
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        #크롤링 방지 설정을 undefined로 변경 
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

    elif tool == 'chrome_debug':
        try:
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동
        except:
            subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        #options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
        #browser.implicitly_wait(20)

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')  
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        
    elif tool == 'chrome_service':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        #user_ag = UserAgent().random 
        #options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")

        #desired_capabilities = options.to_capabilities()
        #desired_capabilities['pageLoadStrategy'] = 'none'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

    elif tool == 'chrome_service_secret':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        #user_ag = UserAgent().random 
        #options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2})
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")

        #desired_capabilities = options.to_capabilities()
        #desired_capabilities['pageLoadStrategy'] = 'none'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

    elif tool == 'brave':
        #path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_argument("window-size=1400x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

        # brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        # options = webdriver.ChromeOptions()
        # options.binary_location = brave_path

        # # Create new automated instance of Brave
        # browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'Firefox':
        path = "C:\Project\cgeckodriver.exe"
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9150)
        profile.update_preferences()
        browser = webdriver.Firefox(profile, executable_path=path)

    return browser


def getLoginInfo():
    random_num = random.randrange(1,5)
    random_num = 2
    # if random_num == 1:
    #     id = "kimbyeongwan20"
    #     password = "order1071tao*"
    # elif random_num == 2:
    #     id = "kimbyeongwan21"
    #     password = "order1071tao*"
    # elif random_num == 3:
    #     id = "1stplatform_jin"
    #     password = "order1071tao*"
    # elif random_num == 4:
    #     id = "kimbyeongwan31"
    #     password = "order1071tao*"
    id = "buyngwankim"
    password = "Order1071tao*"
    
    result = {"id": id, "password": password}
    return result


def elem_clear(browser, elem):
    time.sleep(0.2)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.2)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.2)
    elem.clear()
    time.sleep(0.5)
    return

def loginProc(driver):
    #로그인 복사 붙여넣기로 구현
    login_info = getLoginInfo()
    driver.implicitly_wait(5)
    pyperclip.copy(login_info['id'])
    driver.find_element_by_name('fm-login-id').click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    pyperclip.copy(login_info['password'])
    driver.find_element_by_name('fm-login-password').click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()

def loginProc_new(in_driver, in_login_id, in_password):
    time.sleep(1)
    print('>> loginProc_new ')

    wait = WebDriverWait(in_driver, 30)
    id_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id"))) 
    elem_clear(in_driver, id_input)
    id_input.send_keys(in_login_id) 
    print('>> ID OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    pw_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-password"))) 
    elem_clear(in_driver, pw_input)
    pw_input.send_keys(in_password) 
    print('>> pass OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-form > div.fm-btn > button"))).click()
    print('>> click OK ')
    time.sleep(4)


def moveScroll(driver):
    SCROLL_PAUSE_SEC = 1
    time.sleep(1)
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def moveSlide(driver):
    print('slide proc')
    #//*[@id="nc_1_n1z"]
    #slider = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
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

def clickNextPage(driver):
    result = None
    SCROLL_PAUSE_SEC = 1
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="listsrp-pager"]/div/div/div/div[2]/span[3]').click()
    driver.implicitly_wait(5)
    result = driver.page_source
    return result

#파싱 함수
def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result.strip()

def newlist(cursor,ip):

    sql = "select top 1 * from update_list where proc_ip = '{0}'".format(ip)
    rows = cursor.selectone(sql)
    if not rows:
        page = 1
        sql = "SELECT top 1 a.amz_cateurl,a.catecode,a.update_cnt,a.bcate FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate = 1 and b.catecode is null and a.CateCode < 3000  and sale_ck_new = '1' order by up_date asc"
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        update_cnt = row[2]
        bcate = row[3]
        goodscnt = None
        if str(bcate) == '1044' or str(bcate) == '1038' or str(bcate) == '1033' :
            max_price = 'T'
        else :
            max_price = 'F'
        cursor.execute("update T_CATEGORY set up_date = GETDATE() where catecode='{0}'".format(cateidx))

        sql = "insert into update_list (catecode,now_page,proc_ip,amz_cateurl,regdate,update_cnt,max_price) values ('{0}','{1}','{2}','{3}',getdate(),'{4}','{5}')".format(cateidx, page, ip,amzurl,update_cnt,max_price)
        try:
            cursor.execute(sql)
        except Exception as e:
            os._exit(1)

    else:
        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        rows = cursor.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            cursor.execute(sql)

        sql = "select amz_cateurl,catecode,now_page,update_cnt,max_price,goodscnt from update_list where proc_ip = '{0}'".format(ip)
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        update_cnt = row[3]
        max_price = row[4]
        goodscnt = row[5]

    result = {"catecode": cateidx, "page": int(page),"url":amzurl,"update_cnt":update_cnt,"max_price":max_price,"goodscnt":goodscnt}
    return result

def confirmHtmlSource(source,flag):
    if flag == 'login' :
        check = source.find('login-newbg')
    elif flag == 'captcha' :
        check = source.find('id="nocaptcha"')

    if check > -1 :
        return True
    else :
        return False

#로그인 캡챠 처리
def preProc(result,now_url):
    global browser
    global glogin_id
    global glogin_pass
    # 로그인 처리
    if confirmHtmlSource(result, 'login') == True:
        print('need login')
        #loginProc(browser)
        loginProc_new(browser,glogin_id,glogin_pass)
        print(">> ID / PASS 입력 OK ")
        time.sleep(10)
        print('>> time.sleep(10) ')
        curr_url = str(browser.current_url)[:40]
        print('>> curr_url : {} '.format(curr_url))
        if str(curr_url).find('login.taobao.com') > -1:
            print('>> login Error (60) : {} '.format(curr_url))
            time.sleep(60)
        curr_url = str(browser.current_url)[:40]
        print('>> curr_url : {} '.format(curr_url))
        if str(curr_url).find('login.taobao.com') > -1:
            print('>> please login : {} '.format(curr_url))
            # time.sleep(300)
            input(">> After login : ")

        time.sleep(3)
        result = browser.page_source
        login_flag = True
        login_flag_count = 1
        if confirmHtmlSource(result, 'login') == True:
            print('login again')
            while login_flag:
                browser.get(now_url)
                print(">> now_url : {}".format(now_url))
                time.sleep(2)
                browser.add_cookie({'name':'hng','value':'CN%7Czh-CN%7CCNY%7C156'})
                print(">>time.sleep(10)")
                time.sleep(10)

                result = browser.page_source
                if confirmHtmlSource(result, 'login') == False:
                    #sql = "update update_list set login = 'T' where catecode = '{0}'".format(cate_info['catecode'])
                    #db.execute(sql)
                    login_flag = False
                    break
                elif confirmHtmlSource(result, 'login') == True:
                    #loginProc(browser)
                    loginProc_new(browser,glogin_id,glogin_pass)
                    print(">> ID / PASS 입력 OK ")
                    time.sleep(2)
                    print('>> time.sleep(2) ')
                    curr_url = browser.current_url
                    print('>> curr_url : {} '.format(curr_url))
                    if str(curr_url).find('login.taobao.com') > -1:
                        print('>> login Error : {} '.format(curr_url))
                        time.sleep(300)                    

                else:
                    if confirmHtmlSource(result, 'captcha') == True:
                        print(result)
                        sys.exit('check captcha')
                    else:
                        sys.exit('another error')

                if login_flag_count > 3:
                    sys.exit('login count over')

                login_flag_count += 1

    # 캡챠 확인
    if confirmHtmlSource(result, 'captcha') == True:
        print('need captcha')
        #print(result)
        #time.sleep(3)
        #browser.get(now_url)
        captcha_flag = True
        captcha_flag_count = 1
        while captcha_flag:
            #moveSlide(browser)
            print(">> Slide Captcha Check")
            input(">> Input Key : ")
            time.sleep(5)
            result = browser.page_source
            if confirmHtmlSource(result, 'captcha') == False:
                captcha_flag = False
            else :
                captcha_flag_count += 1

            if captcha_flag_count > 10:
                sys.exit('captcha count 10 over')
            #browser = connectDriver('else')
            #browser.get(now_url)
            #result = browser.page_source

            #loginProc(browser)

            #if confirmHtmlSource(result, 'captcha') == False :
                #captcha_flag = False
                #break
            #else :
                #captcha_flag_count += 1

            #if captcha_flag_count > 3:
                #sys.exit('captcha count over')

    return result

def getMaxPage(target):
    if int(target)==0 or target == None:
        result = 5
    elif int(target) >=1 and int(target) <= 2 :
        result = 10
    elif int(target) >=3 and int(target) <= 30 :
        result = 30
    else :
        result = 5

    return result

def replaceTitle(title):
    title = str(title)
    title = title.replace('\u003cspan class\u003dH\u003e','').replace('\u003c/span\u003e','')
    title = title.replace('\u003c','').replace('\u003dH','').replace('\u003e','').replace('\u003d','').strip()
    return title


def procGet(now_url):
    try:
        browser.get(now_url)
        print(">> now_url : {}".format(now_url))
        print(">> time.sleep(4.0-5.5)")
        time.sleep(random.uniform(4.0,5.5))
        browser.add_cookie({'name':'hng','value':'CN%7Czh-CN%7CCNY%7C156'})
        result = browser.page_source
    except Exception as e:
        print(">> now_url : {}".format(now_url))
        input(">> Key : ")
        time.sleep(3)
        result = ""
    time.sleep(1)
    return result

def procList():
    print(">> procList Start ")
    global timecount
    global db
    global browser
    global start_check
    global endpage
    timecount = 0
    cate_info = newlist(db, ip)

    endasin = 0
    sql = " select endasin from python_version_manage where name = 'list'"
    rowCnt1 = db.selectone(sql)
    if rowCnt1:
        endasin = rowCnt1[0]
    print(">> end asin count : "+str(endasin))
    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin where catecode < 3000 "
    rowCnt2 = db.selectone(sql_cnt)
    print(">> asin count : "+str(asinCnt))
    if rowCnt2:
        asinCnt = rowCnt2[0]
    if asinCnt > endasin:
        print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
        db.close()
        browser.close()
        browser.quit()
        os._exit(1)

    if version_check(db) == False :
        db.close()
        browser.close()
        browser.quit()
        os.system("taskkill /f /im taobao_asin.exe")
        os._exit(1)
    else :
        timecount = 0
        timer = threading.Timer(0, procList)

        print('>> start ')
        now_url = cate_info['url']
        if now_url.find('&seller_type=taobao') > -1:
            now_url = now_url.replace('&seller_type=taobao', '')

        if cate_info['page'] > 1:
            now_page = cate_info['page']
            goodscnt = cate_info['goodscnt']
            if goodscnt != None :
                now_goods_count = (now_page - 1) * int(goodscnt)
            else:
                now_goods_count = (now_page - 1) * 60
            now_url = now_url + '&bcoffset=0&s=' + str(now_goods_count)
        #print(now_url)
        print(">> catecode : {} :  max_price : {} ".format(cate_info['catecode'], cate_info['max_price']))
        print(">> now_url : {} ".format(now_url))

        start_check = True
        if start_check == True :
            result = procGet(now_url)
        else :
            result = clickNextPage(browser)
            browser.implicitly_wait(5)
            time.sleep(random.uniform(5.0,7.5))

        if str(result).find('id="listsrp-itemlist"') > -1:
            print(">> List (listsrp-itemlist) (1) Ok ")
        elif str(result).find('id="minisrp-itemlist"') > -1:
            print(">> List (minisrp-itemlist) (2) Ok ")
        elif str(result).find('class="m-itemlist"') > -1:
            print(">> List (m-itemlist) (3) Ok ")
        elif str(result).find('class="Content--content--') > -1:
            print(">> List (Content--content) (4) Ok ")
        else:
            print(">> List (No) preProc ")
            result = preProc(result,now_url)
        time.sleep(1)
        try:
            moveScroll(browser)
        except Exception as e:
            print(">> moveScroll Exception ")
            time.sleep(2)

        max_price = cate_info['max_price']
        total_page = getparse(result,'"totalPage":',',')
        if str(total_page).isdigit() == True:
            print(">> total_page : {}".format(total_page))
        else:
            total_page = cate_info['page']
            print(">> total_page error -> cate_info page update: {}".format(total_page))

        if result.find('"nid":"') == -1:
            print(">> total_page check error ")
            #browser.refresh()
            time.sleep(4)
            
            result = procGet(now_url)
            if result.find('"nid":"') == -1:
                print(">> total_page check error (2)")
                # input(">> Key Input : ")
                result = procGet(now_url)
            # if result.find('"nid":"') == -1:
            #     print(">> total_page check error (2-2)")
            #     input(">> Key Input : ")
            #     result = procGet(now_url)
            # if result.find('"nid":"') == -1:
            #     print(">> total_page check error (2-3)")
            #     input(">> Key Input : ")
            #     result = procGet(now_url)

        if result.find('"nid":"') == -1:
            print(">> total_page check error (3)")
            # sql = "delete from update_list where proc_ip = '{0}'".format(ip)
            # print(">> sql : {}".format(sql))
            # db.execute(sql)
            # db.close()
            # browser.close()
            # browser.quit()
            # os._exit(1)
            print('>> next catecode ')
            sql = "update T_CATEGORY set up_date = GETDATE() where catecode='{0}'".format(cate_info['catecode'])
            db.execute(sql)
            sql = "delete from update_list where catecode ='{0}'".format(cate_info['catecode'])
            db.execute(sql)

            start_check = True
            time.sleep(10)
            timer.start()
        else:
            current_page = getparse(result,'"currentPage":',',')
            print(">> current_page : {}".format(current_page))
            max_page = getMaxPage(cate_info['update_cnt'])
            if float(max_page) > float(endpage):
                max_page = endpage
                print(">> max_page (endpage update) : {}".format(max_page))
            else:
                print(">> max_page : {}".format(max_page))
            if cate_info['page'] != current_page :
                sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(cate_info['page'],cate_info['catecode'])
                db.execute(sql)
                cate_info['page'] = current_page
                print(">> current_page : ( {} ) -------------------- ".format(current_page))

            #상품코드 가져오기
            if result.find('"nid":"') > 0 :
                print(">> goods list ")
                asin_list = result.split('"nid":"')
                low = 1
                update_goods_count = 0
                tmall_skip_cnt = 0
                while low < len(asin_list):
                    asin = getparse(asin_list[low], None, '"')
                    istmall_ck = getparse(asin_list[low], '"isTmall":', ',')
                    if istmall_ck == 'false':
                        istmall = 'F'
                    elif istmall_ck == 'true' :
                        istmall = 'T'
                    else:
                        print(istmall_ck)
                        istmall = 'F'
                    title = getparse(asin_list[low],'"title":"','"')
                    title = replaceTitle(title)
                    pic_url = getparse(asin_list[low], '"pic_url":"', '"')
                    view_price = getparse(asin_list[low], '"view_price":"', '"')
                    seller_id = getparse(asin_list[low], '"user_id":"', '"')
                    view_price = view_price.replace('"','').replace("'",'').replace(",",'')

                    if istmall == 'T':
                        print(">> [{}] (Tmall Skip) {} | {}".format(low,asin,view_price))
                        tmall_skip_cnt = tmall_skip_cnt + 1

                    ##### price check #####
                    if float(view_price) < 1:
                        print(">> [{}] (1 위안 미만 (skip)) {} | {} ".format(low, asin, view_price))
                    elif float(view_price) > 8000:
                        print(">> [{}] (8000 위안 (150만원) over (skip)) {} | {} ".format(low, asin, view_price))
                    elif max_price == 'T' and float(view_price) > 1000 :
                        print(">> [{}] (max price 1000 over) {} | {} ".format(low, asin, view_price))
                    else:
                        sql = "select * from T_Category_BestAsin where asin = '{0}'".format(asin)
                        row = db.selectone(sql)
                        if not row :
                            sql = "insert into T_Category_BestAsin (asin,catecode,up_date,img,price,isTmall,title,seller_id) values('{0}','{1}',getdate(),'{2}','{3}','{4}',N'{5}','{6}')".format(asin,cate_info['catecode'],pic_url,view_price,istmall,title,seller_id)
                            db.execute(sql)
                            print(">> [{}] (insert) {} | {}".format(low,asin,view_price))
                        else :
                            sql = "update T_Category_BestAsin set up_date = getdate() where asin = '{0}'".format(asin)
                            db.execute(sql)
                            print(">> [{}] (update) {} | {}".format(low,asin,view_price))
                            update_goods_count += 1

                    low += 1

                print(">> tmall_cnt : {} ".format(tmall_skip_cnt))
                # page 업데이트
                #if int(cate_info['page']) < int(total_page):
                #if int(cate_info['page']) < max_page and int(cate_info['page']) < int(total_page) :
                print(">> total_page : {} | max_page : {} ".format(total_page, max_page))
                print(">> cate_info['page'] : {}".format(cate_info['page']))
                if str(cate_info['page']).isdigit() == True:
                    cate_info_page = int(cate_info['page'])
                else:
                    print(">> cate_info['page'] Error --> max_page 입력하고 SKIP 처리 : {} ".format(max_page))
                    cate_info_page = max_page
                
                if cate_info_page < max_page and cate_info_page < int(total_page):
                    next_page = int(cate_info['page']) + 1
                    print(next_page)
                    if cate_info_page == 1 :
                        sql = "update update_list set now_page = '{0}',goodscnt = '{2}' where catecode = '{1}'".format(next_page, cate_info['catecode'],low-1)
                    else:
                        sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(next_page, cate_info['catecode'])
                    db.execute(sql)
                    print('>> next page : {}'.format(next_page))
                    start_check = False
                    time.sleep(10)
                else:
                    print('>> next catecode')
                    sql = "update T_CATEGORY set up_date = GETDATE(),update_cnt = update_cnt + 1 where catecode='{0}'".format(cate_info['catecode'])
                    db.execute(sql)
                    sql = "delete from update_list where catecode ='{0}'".format(cate_info['catecode'])
                    db.execute(sql)
                    start_check = True
                    time.sleep(10)

                timer.start()

def fun_timer():
    global timecount
    global browser
    global db
    timecount += 1
    proces_timer = threading.Timer(1, fun_timer)
    proces_timer.start()
    if (timecount == 200000):
        browser.close()
        browser.quit()
        os.system("taskkill /f /im taobao_asin.exe")
        os._exit(1)

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def getEndpage(db_con):
    rtnPage = 30
    sql = " select endpage from python_version_manage where name = 'list'"
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]
    print(">> getEndpage : "+str(rtnPage))

    return rtnPage

def getEndasin(db_con):
    rtnAsin = 200000
    sql = " select endasin from python_version_manage where name = 'list'"
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]
    print(">> getEndasin : "+str(rtnAsin))

    return rtnAsin

if __name__ == '__main__':
    print(str(datetime.datetime.now()))

    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
    time.sleep(3)

    start_check = True
    set_browser = "chrome"
    ip = socket.gethostbyname(socket.gethostname())
    #db = DBmodule_FR.Database('taobao')
    db = DBmodule_FR.Database('taobao')

    if str(currIp).strip() != "222.104.189.18":
        version_check(db)

    dSql = "delete from T_Category_BestAsin where asin in (select g.ali_no from T_Category_BestAsin as a inner join t_goods as g on g.ali_no = a.asin and g.stop_update = '1')"
    print('>>  (DEL) stop_update goods (dSql) :' + str(dSql))
    db.execute(dSql)

    dSql = "delete from T_Category_BestAsin where catecode in (select a.catecode from T_Category_BestAsin as a inner join T_CATEGORY as c on c.CateCode = a.catecode and c.IsHidden = 'T')"
    print('>> (DEL) IsHidden T Category (dSql) :' + str(dSql))
    db.execute(dSql)

    endpage = 0
    endpage = getEndpage(db)
    if endpage > 9 and endpage < 300:
        print('>> getEndpage OK')
    else:
        print('>> getEndpage Check')

    endasin = 0
    endasin = getEndasin(db)
    if endasin > 0:
        print('>> getEndasin OK' + str(endasin))
    else:
        print('>> getEndasin Check')

    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin where catecode < 3000 "
    rowCnt = db.selectone(sql_cnt)
    if not rowCnt:
        print('>> asinCnt 확인불가')
        db.close()
        time.sleep(1)
        os._exit(0)
    else:
        asinCnt = rowCnt[0]
        if asinCnt > endasin:
            print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
            procLogSet(db, "asin_list", " asinCnt : " + str(asinCnt)+' 건)')
            db.close()
            time.sleep(1)
            os._exit(0)

    #browser = connectDriver("chrome")
    # browser = connectDriver("chrome_service_secret")
    main_url = "https://www.taobao.com"
    try:
        browser = connectDriverNew(main_url,"","")
        print(">> connectDriverNew ")
    except Exception as e:
        browser = connectDriverOld(main_url,"","")
        print(">> connectDriverOld set OK ")

    time.sleep(4)
    timecount = 0
    # input(">> After Login Input : ")
    time.sleep(2)
    # fun_timer()
    procList()





