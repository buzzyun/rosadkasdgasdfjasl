import random
import os
import re
import requests
import urllib
import cv2
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chromedriver_autoinstaller
import pyperclip


def connectDriverOld(pgSite, mode):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    print(">> connectDriverOld ")
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    print(">> chrome_ver :{} | driver_path : {}".format(chrome_ver, driver_path))
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    option.add_argument("cookie=intl_loc")
    try:
        browser = webdriver.Chrome(options=option)
    except Exception as e:
        print(e)

    return browser

def connectDriverNew(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    option.add_argument("cookie=intl_loc")
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
        try:
            service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
            browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
            driver_executable_path = service.path
        except Exception as e:
            print(e)

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
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        #options.add_argument("--log-level=3")
        options.add_argument("user-data-dir={}".format(userProfile))
        # options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        
    elif tool == 'chrome_service':
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        #options.add_argument("--log-level=3")
        options.add_argument("user-data-dir={}".format(userProfile))
        # Selenium 4.0 - load webdriver
        s = Service(driver_path)
        browser = webdriver.Chrome(service=s, options=options)

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
        # Selenium 4.0 - load webdriver
        s = Service(driver_path)
        browser = webdriver.Chrome(service=s, options=options)
        #browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

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


def chrom_click(selector, driver):
    driver.find_element(By.CSS_SELECTOR,selector).click()
    time.sleep(1)
    print(selector,"클릭")
    
def chrom_write(selector, driver, write):
    lst = list(write)
    for i in lst:
        driver.find_element(By.CSS_SELECTOR,selector).send_keys(i)
        time.sleep(random.uniform(0.2,0.3))
    time.sleep(1)

def loginProcNew(browser, loginId, loginPw):
    time.sleep(0.5)
    try:
        if browser.find_element(By.CSS_SELECTOR,'img._24EHh'):
            browser.find_element(By.CSS_SELECTOR,'img._24EHh').click()
    except Exception as e:
        print(">> pop up (img._24EHh) close Exception ")
    else:
        print(">> pop up close Ok ")

    try:
        if browser.find_element(By.CSS_SELECTOR,'img.btn-close'):
            browser.find_element(By.CSS_SELECTOR,'img.btn-close').click()
    except Exception as e:
        print(">> pop up (img.btn-close) close Exception ")
    else:
        print(">> pop up close Ok ")
    time.sleep(1)

    # 마우스 커서 어카운트 (계정)에 위치
    ActionChains(browser).move_to_element(browser.find_element(By.CSS_SELECTOR,"#nav-user-account > span > a")).perform()
    # sign in 클릭
    time.sleep(1)
    try:
        # 계정 -> 로그인 버튼 클릭
        chrom_click("#nav-user-account > div > div > p.flyout-bottons > a.sign-btn", browser)
        # 아이디, 패스워드 입력
        chrom_click("#fm-login-id", browser)    
        chrom_write("#fm-login-id", browser, loginId)
        chrom_write("#fm-login-password", browser, loginPw)
        try:
            chrom_click("#batman-dialog-wrap > div > div > div.cosmos-tabs > div.cosmos-tabs-container > div > div > button.cosmos-btn.cosmos-btn-primary.cosmos-btn-large.cosmos-btn-block.login-submit > span", browser)
        except:
            chrom_click("#batman-dialog-wrap > div > div.fm-tabs-content > div > div > button", browser)
    except:
        print("로그인 중")
        time.sleep(1)

    order_url="https://www.aliexpress.com/p/order/index.html"
    try:
        browser.get(order_url)
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item")))
        print(">> 주문 내역 Page Ok ")
        time.sleep(1)
    except:
        print(">> 주문 내역 Page Error ")

    browser.get("https://ko.aliexpress.com/")
    time.sleep(2)

    account_check = browser.find_element(By.CLASS_NAME,'account-main')
    if str(account_check.text).find('로그인') > -1 or str(account_check.text).find('Sign in') > -1:
        print(">> 로그인 실패 ")
        return "1"
    else:
        print(">> 로그인 OK ")
        return "0"

def loginProc(in_driver, in_login_id, in_password):
    #로그인 복사 붙여넣기로 구현

    in_driver.implicitly_wait(5)
    pyperclip.copy(in_login_id)

    result_sour = in_driver.page_source
    if str(result_sour).find('class="fm-logined-title"') > -1:
        print(">> 이미 어카운트에 등록하셨습니다.지금 바로 어카운트를 사용하실수 있습니다 ")
        input(">> KEY :")

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
    elif gHead == "K":
        sitename = "uk"
    elif gHead == "N":
        sitename = "mall"
    elif gHead == "L":
        sitename = "cn"
    elif gHead == "Z":
        sitename = "red"
    elif gHead == "R":
        sitename = "ref"
    elif gHead == "T":
        sitename = "trend"
    elif gHead == "P":
        sitename = "shop"
    elif gHead == "W":
        sitename = "mini"
    elif gHead == "B":
        sitename = "beauty"
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

def getOrderIDCount(inID):
    cnt_ali_id = ""

    if inID == "알리H": cnt_ali_id = "ali_H"
    if inID == "알리J": cnt_ali_id = "ali_J"
    if inID == "알리W": cnt_ali_id = "ali_W"
    if inID == "알리B1": cnt_ali_id = "ali_B1"
    if inID == "알리A1": cnt_ali_id = "ali_A1"
    if inID == "알리S": cnt_ali_id = "ali_S"
    if inID == "알리C": cnt_ali_id = "ali_C"
    if inID == "알리P1": cnt_ali_id = "ali_P1"
    if inID == "알리M": cnt_ali_id = "ali_M"
    if inID == "알리DH": cnt_ali_id = "ali_DH"
    if inID == "알리B": cnt_ali_id = "ali_B"
    if inID == "알리P": cnt_ali_id = "ali_P"
    if inID == "알리P2": cnt_ali_id = "ali_P2"
    if inID == "알리M1": cnt_ali_id = "ali_M1"
    if inID == "알리SO": cnt_ali_id = "ali_SO"
    if inID == "알리BO": cnt_ali_id = "ali_BO"
    if inID == "알리SH": cnt_ali_id = "ali_SH"
    if inID == "알리L": cnt_ali_id = "ali_L"
    if inID == "알리K": cnt_ali_id = "ali_K"
    if inID == "알리K2": cnt_ali_id = "ali_K2"
    if inID == "아마존": cnt_ali_id = "ali_amazon"
    if inID == "아마존SO": cnt_ali_id = "ali_amazonSO"
    if inID == "DH": cnt_ali_id = "DH"
    if inID == "알리ebay": cnt_ali_id = "DH"
    if inID == "조마샵(직)": cnt_ali_id = "joma"
    if inID == "조마샵(배)": cnt_ali_id = "joma"
    if inID == "6pm": cnt_ali_id = "sixpm"
    if inID == "알리BG": cnt_ali_id = "ali_BG"
    if inID == "알리PF": cnt_ali_id = "ali_PF"
    if inID == "알리YS": cnt_ali_id = "ali_YS"
    if inID == "알리BS": cnt_ali_id = "ali_BS"
    if inID == "알리GJ": cnt_ali_id = "ali_GJ"
    if inID == "알리GM": cnt_ali_id = "ali_GM"
    if inID == "알리OS": cnt_ali_id = "ali_OS"
    if inID == "mall": cnt_ali_id = "ali_mall"
    if inID == "일본아마존": cnt_ali_id = "ali_amazonJP"
    if inID == "shop": cnt_ali_id = "ali_shop"
    if inID == "알리BW": cnt_ali_id = "ali_BW"
    if inID == "알리BS7": cnt_ali_id = "ali_BS7"
    if inID == "알리MC": cnt_ali_id = "ali_MC"
    if inID == "알리YSK": cnt_ali_id = "ali_YSK"
    if inID == "알리JH": cnt_ali_id = "ali_JH"
    if inID == "임시결제": cnt_ali_id = "ali_temp"
    if inID == "event": cnt_ali_id = "ali_event"
    if inID == "알리HJ": cnt_ali_id = "ali_HJ"
    if inID == "알리BY": cnt_ali_id = "ali_BY"
    if inID == "글로벌": cnt_ali_id = "ali_global"
    if inID == "알리SM": cnt_ali_id = "ali_SM"
    if inID == "알리FC": cnt_ali_id = "ali_FC"
    if inID == "woman": cnt_ali_id = "ali_woman"
    if inID == "de": cnt_ali_id = "ali_de"
    if inID == "알리BWK": cnt_ali_id = "ali_BWK"
    if inID == "알리YS6": cnt_ali_id = "ali_YS6"
    if inID == "알리KB": cnt_ali_id = "ali_KB"
    if inID == "알리BG7": cnt_ali_id = "ali_BG7"
    if inID == "알리IG": cnt_ali_id = "ali_IG"
    if inID == "알리BSK": cnt_ali_id = "ali_BSK"
    if inID == "알리AM": cnt_ali_id = "ali_AM"
    if inID == "trend": cnt_ali_id = "ali_trend"
    if inID == "알리YJ1": cnt_ali_id = "ali_YJ1"
    if inID == "알리KJ1": cnt_ali_id = "ali_KJ1"
    if inID == "알리YH": cnt_ali_id = "ali_YH"
    if inID == "알리IGJ": cnt_ali_id = "ali_IGJ"
    if inID == "cp1": cnt_ali_id = "cp1"
    if inID == "cp2": cnt_ali_id = "cp2"

    return cnt_ali_id

def procInputEa(browser, d_ea, type):
    if str(type) == "2" or str(type) == "3":
        # findClassname2 = getparse(str(browser.page_source),'comet-input-number quantity--picker--','">')
        # findSelectname2 = 'div.comet-input-number.quantity--picker--' +str(findClassname2)+ ' > input' 
        findClassname2 = getparse(str(browser.page_source),'comet-v2-input-number quantity--picker--','">')
        findSelectname2 = 'div.comet-v2-input-number.quantity--picker--' +str(findClassname2)+ ' > input' 
    else:
        findSelectname2 = 'div.product-quantity.clearfix > span > span > span.next-input.next-medium.next-input-group-auto-width > input'

    if browser.find_element(By.CSS_SELECTOR,findSelectname2):
        ea_elm_btn = browser.find_element(By.CSS_SELECTOR,findSelectname2)
        if str(type) == "2" or str(type) == "3":
            print(">> 수량 클릭 (type2)")
            ea_elm_btn.click()
            time.sleep(0.5)
        time.sleep(0.3)
        ea_elm_btn.send_keys(Keys.CONTROL + "a")
        time.sleep(0.3)
        if str(type) == "1":
            ea_elm_btn.send_keys(Keys.DELETE)
            time.sleep(0.3)
            ea_elm_btn.clear()                
            time.sleep(0.3)
        ea_elm_btn.send_keys(d_ea)
        print(">> 수량 입력 : {}".format(d_ea))
        time.sleep(1)

def get_attrId(str_soup, type):
    if str(type) == "2" or str(type) == "3":
        v_skuId = getparse(str(str_soup), '"skuId":', ',')
        if str(v_skuId).find('}') > -1:
            v_skuId = getparse(str(v_skuId), '', '}') 
    else:
        v_skuId = getparse(str(str_soup), '"skuId":', ',"skuIdStr"')
    return str(v_skuId)

def getOtionUrl(in_drive, dic_opt, in_aliCode, in_ea, ali_screen_type):

    option_code = dic_opt['code']
    option_name = dic_opt['name']
    if len(option_code) == 0:
        option_check = "0"
    else:
        option_check = "1"
        print(">> 옵션코드 : {}".format(option_code))
        print(">> 옵션명 : {}".format(option_name))        
    # -----------------------------------------------------------------------------------

    # 소스 가져오기 ######################################################################
    time.sleep(3)
    # req_v = in_drive.page_source
    # soup_v = BeautifulSoup(req_v, 'html.parser')
    soup_v = in_drive.page_source
    # print('>> soup_v :' + str(soup_v))

    sku_chk = ""
    if str(soup_v).find("productSKUPropertyList") == -1:
        print(">> 소스 확인 불가상태 ")
        sku_chk = "1"
    else:
        print(">> 소스 확인 (productSKUPropertyList) OK ")
        sku_chk = "0"

    flg_Ship_from = ""
    str_soup_list = ""
    str_soup = ""
    str_soup_list = getparse(str(soup_v), 'productSKUPropertyList":', '"skuPriceList":')
    if str(ali_screen_type) == "2" or str(ali_screen_type) == "3":
        str_soup = getparse(str(soup_v), '"skuPriceList":[', '')
        if str(str_soup).find('"wishListComponent"') > -1:
            str_soup = getparse(str(str_soup), '', '"wishListComponent"')
        if str(str_soup).find('"StoreModule"') > -1:
            str_soup = getparse(str(str_soup), '', '"StoreModule"')
        #print('>> str_soup (2) :' + str(str_soup))
    else:
        str_soup = getparse(str(soup_v), '"skuPriceList":[', '"warrantyDetailJson"')
    ####################################################################################
    # print('>> str_soup :' + str(str_soup))

    soup_sp_cnt = 0
    soup_sp_cnt = len(str_soup_list.split('"skuPropertyName":')) - 1
    print(">> (소스) 옵션수 (soup_sp_cnt) : {}".format(soup_sp_cnt))

    if soup_sp_cnt > 0:
        # 옵션명 중복체크
        dup_flg = option_dup_check(str_soup_list, dic_opt, soup_sp_cnt)
        if dup_flg != "0":
            print('>> [S06] 중복 옵션명 있음 (확인필요) ')
            return "S06"

    if len(option_code) == 0 and soup_sp_cnt > 0:
        print('>> * (주문) 옵션은 없고 (소스) 옵션 있는 CASE ')
        if soup_sp_cnt == 1 and (str_soup_list.find('skuPropertyName":"배송지"') > -1 or str_soup_list.lower().find('skupropertyname":"ships from"') > -1):
            if str_soup_list.lower().find('"china"') > -1 or str_soup_list.lower().find('"cn"') > -1 or str_soup_list.find('"중국"') > -1:
                flg_Ship_from = "1"
            else:
                print(">> 소스 배송지 china 미포함 ")
                return "S05"
        else:
            print('>> [S05] 옵션 있는 상품 (옵션 선택 확인필요) SKIP 대상 (S05): {}'.format(dic_opt))
            return "S05"

    find_str = option_code.replace(":", ",")
    print('>> (주문) 옵션코드 :' + str(find_str))
    option_sp = find_str.split(',')
    if option_check == "0":
        option_sp_cnt = 0
    else:
        option_sp_cnt = len(option_sp)
    print('>> (주문) 옵션수 : {} | (소스) 옵션수 : {}'.format(option_sp_cnt, soup_sp_cnt))

    if str(soup_sp_cnt) != str(option_sp_cnt):
        print('>> 옵션수 불일치 :' + str(option_sp_cnt))
        if str_soup_list.find('skuPropertyName":"배송지"') > -1 or str_soup_list.lower().find('skupropertyname":"ships from"') > -1:
            if str_soup_list.lower().find('"china"') > -1 or str_soup_list.lower().find('"cn"') > -1 or str_soup_list.find('"중국"') > -1:
                flg_Ship_from = "1"
            else:
                print(">> 소스 배송지 china 미포함 ")
                return "S05"
        else:
            print('>> [X05] 주문옵션수와 소스옵션수 불일치(X05): {}'.format(dic_opt))

            #with open(os.getcwd() + "/log/result_"+str(in_aliCode)+".html","w",encoding="utf8") as f: 
            #        f.write(str(soup_v))
            #input(">> X01 (01) : ")
            if sku_chk == "1":
                return "S077" # 옵션 소스 확인불가
            return "X05" # 주문옵션수와 소스옵션수 불일치

#################################################################
    #input(">> next (1): ")

    v_skuId = ""
    v_stock = "0"
    v_skuAttr = ""
    if option_check == "0":
        v_skuId = get_attrId(str(str_soup), ali_screen_type)
        v_stock = getparse(str(str_soup), '"inventory":', ',')    
    else:
        tmp_opCode = 'skuPropIds":"' + str(find_str) + '"'
        print('>> [검색 skuPropIds ] :' + str(tmp_opCode))
        if str(ali_screen_type) == "2" or str(ali_screen_type) == "3":
            if str(str_soup).find('{"skuVal":') > -1:
                sp_skulist = str(str_soup).split('{"skuVal":')
            elif str(str_soup).find('{"skuIdStr":') > -1:
                sp_skulist = str(str_soup).split('{"skuIdStr":')
            else:
                print('>> [X01] 일치 하는 옵션 없음 111 : {}'.format(find_str))
                return "X01" 
        else:
            sp_skulist = str(str_soup).split('{"freightExt":')

        skucnt = 1
        while skucnt < len(sp_skulist):
            #print(">> {} : {}".format(skucnt, sp_skulist[skucnt]))
            t_fos = str(sp_skulist[skucnt]).find(tmp_opCode)
            if t_fos > -1:
                v_stock = getparse(sp_skulist[skucnt], '"availQuantity":', ',')
                v_skuAttr = getparse(str(sp_skulist[skucnt]), '"skuAttr":"', '","')
                v_skuId = get_attrId(str(sp_skulist[skucnt]), ali_screen_type)
                break
            skucnt = skucnt + 1

        if v_skuAttr == "" or v_skuId == "":
            print('>> [X01] 일치 하는 옵션 없음 : {}'.format(find_str))
            return "X01"       
        if int(v_stock) == 0:
            print('>> [X02] 해당옵션 재고없음 : {}'.format(find_str))
            return "X02"
        if int(in_ea) > int(v_stock):
            print('>> [X02] 해당옵션 재고부족 : {}'.format(dic_opt))
            print('>> 주문수량 : {} | 재고수량 : {}'.format(in_ea, v_stock))
            return "X02"

    print('>> [ skuAttr ] :' + str(v_skuAttr))
    print('>> [ skuId ] :' + str(v_skuId))
    print('>> [ stock ] :' + str(v_stock))

    # 유티코드로 변경
    v_skuAttr_uni = ""
    if str(v_skuAttr).strip() != "":
        v_skuAttr_uni = str(v_skuAttr).replace(":", "%3A")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(";", "%3B")
        v_skuAttr_uni = str(v_skuAttr_uni).replace("#", "%23")
        v_skuAttr_uni = str(v_skuAttr_uni).replace(" ", "%20")
        #print('>> [ 유니코드 변환 ] :' + str(v_skuAttr_uni))

    ship_company = "CAINIAO_STANDARD"
    move_url = "https://shoppingcart.aliexpress.com/order/confirm_order.htm?objectId=" + in_aliCode + \
    "&from=aliexpress&countryCode=KR" + \
    "&shippingCompany=" + ship_company + \
    "&provinceCode=&cityCode=&promiseId=&aeOrderFrom=main_detail" + \
    "&skuAttr=" + v_skuAttr_uni + \
    "&skuId=" + v_skuId + \
    "&skucustomAttr=null" + \
    "&quantity=" + in_ea
    #print(">> >> move_url : " + str(move_url))

    ##############################################################
    print(">> [ORG] 옵션명 : {}".format(dic_opt))

    return move_url

def setShipTO(in_driver, find_txt):
    rtnChkFlg = ""
    time.sleep(2)

    if find_txt == "한국어":
        # Currency 설정
        if in_driver.find_element(By.CSS_SELECTOR,'span.language_txt'):
            in_driver.find_element(By.CSS_SELECTOR,'span.language_txt').click() 
    if find_txt == "USD":
        # Currency 설정
        if in_driver.find_element(By.CSS_SELECTOR,'span.currency'):
            in_driver.find_element(By.CSS_SELECTOR,'span.currency').click() 

    if find_txt != "":
        time.sleep(2)
        print('>> time.sleep(2)')
        currencyBtns = in_driver.find_elements(By.CSS_SELECTOR,'span.select-item')
        currencyBtns[1].click()

        time.sleep(1)
        itemcurrSelUlBtns = in_driver.find_elements(By.CSS_SELECTOR,'ul.notranslate')
        itemcurrSelLiBtns = itemcurrSelUlBtns[1].find_elements(By.TAG_NAME,'li')

        comments_text = {}
        for num, comment in enumerate(itemcurrSelLiBtns):
            comments_text[num] = comment
            txtShip = str(comments_text[num].text)

            if txtShip.find(find_txt) > -1:
                comments_text[num].click()
                print(find_txt + " Click ")
                break

        print(" {} 선택 OK ".format(find_txt))
        time.sleep(2)
        print('>> time.sleep(2)')

        #Ship to 설정 저장 클릭
        in_driver.find_element(By.CSS_SELECTOR,'button.ui-button.ui-button-primary.go-contiune-btn').click()
        print('>> save button click')

        print(" {} 선택 완료 ".format(find_txt))

    return rtnChkFlg

def setLang(in_driver):
    rtnChkFlg = ""
    time.sleep(4)

    # language 설정
    if in_driver.find_element(By.CSS_SELECTOR,'span.language_txt'):
        in_driver.find_element(By.CSS_SELECTOR,'span.language_txt').click() #language_txt 클릭

        time.sleep(2)
        print('>> time.sleep(2)')
        currencyBtns = in_driver.find_elements(By.CSS_SELECTOR,'span.select-item')
        currencyBtns[1].click()

        time.sleep(1)
        itemcurrSelUlBtns = in_driver.find_elements(By.CSS_SELECTOR,'ul.notranslate')
        itemcurrSelLiBtns = itemcurrSelUlBtns[1].find_elements(By.TAG_NAME,'li')

        comments_text = {}
        for num, comment in enumerate(itemcurrSelLiBtns):
            comments_text[num] = comment
            txtItem = str(comments_text[num].text)

            if txtItem.find('한국어') == 0:
                comments_text[num].click()
                print("한국어 Click ")
                break

        print("Lang : 한국어 선택 OK ")
        time.sleep(1)
        print('>> time.sleep(1)')

        # 설정 저장 클릭
        in_driver.find_element(By.CSS_SELECTOR,'button.ui-button.ui-button-primary.go-contiune-btn').click()
        print('>> save button click')

        print('>> 한국어 설정 완료 ' +str(rtnChkFlg))

    return rtnChkFlg

def setTo(in_driver, find_txt):
    
    if find_txt != "":
        time.sleep(2)
        print('>> time.sleep(2)')
        itemBtns = in_driver.find_elements(By.CSS_SELECTOR,'span.select-item')
        itemBtns[1].click()

        time.sleep(1)
        itemSelUlBtns = in_driver.find_elements(By.CSS_SELECTOR,'ul.notranslate')
        itemSelUlBtns = itemSelUlBtns[1].find_elements(By.TAG_NAME,'li')

        comments_text = {}
        for num, comment in enumerate(itemSelUlBtns):
            comments_text[num] = comment
            txtShip = str(comments_text[num].text)

            if txtShip.find(find_txt) == 0:
                comments_text[num].click()
                print(find_txt + " Click ")
                break

        print(" {} 선택 OK ".format(find_txt))
        time.sleep(3)
        print('>> time.sleep(3)')
        return "0"

    return "1"

def set_LangCurr(in_driver):
    rtn = ""
    time.sleep(4)
    
    result = in_driver.page_source
    if str(result).find('class="language_txt">한국어') > -1:
        print(">> 한국어 Ok")
    else:
        # language 설정
        if in_driver.find_element(By.CSS_SELECTOR,'span.language_txt'):
            in_driver.find_element(By.CSS_SELECTOR,'span.language_txt').click() #language_txt 클릭
            rtn = setTo(in_driver, "한국어")

    if str(result).find('class="currency">USD') > -1:
        print(">> USD Ok")
    else:
        # Currency 설정
        if in_driver.find_element(By.CSS_SELECTOR,'span.currency'):
            in_driver.find_element(By.CSS_SELECTOR,'span.currency').click() #currency 클릭
            rtn = setTo(in_driver, "USD")

    if rtn == "0":
        #설정 저장 클릭
        in_driver.find_element(By.CSS_SELECTOR,'button.ui-button.ui-button-primary.go-contiune-btn').click()
        print('>> save button click')
        print('>> 설정 완료  ')

def setAddrOther(browser):
    time.sleep(1)
    addrul = browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner")
    addrul[1].click()
    time.sleep(1)
    itemBtns = browser.find_element(By.CSS_SELECTOR,"[role='listbox']").find_elements(By.TAG_NAME,'li')

    comments_text = {}
    for num, comment in enumerate(itemBtns):
        comments_text[num] = comment
        txtShip = str(comments_text[num].text)
        if txtShip.find('Other') == 0:
            comments_text[num].click()
            print("Other Click ")
            break

    print("주소 : Other 선택 OK ")
    time.sleep(1)
    print('>> time.sleep(1)')

def isEnglishOrKorean(input_str):
    input_str = input_str.replace(" ","")
    skip_count = 0
    for c in input_str:
        if ord('가') <= ord(c) <= ord('힣'):
            pass
        else:
            skip_count = skip_count + 1
    return skip_count

#reg 한글 체크
def regKrStrChk(in_str):
    result = ""

    chkStr = in_str.replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

def curr_replace(curr_str):
    curr_str = str(curr_str).replace(' ','').replace('>','').replace(',','').replace('₩','').replace('US','').replace('$','').strip()
    return curr_str

def soc_check(soc_no, rcvname, rcv_phone):
    rtnFlg = "1"
    api_key = "g210s234u056t149h070p010e0"
    setrurl = "https://unipass.customs.go.kr:38010/ext/rest/persEcmQry/retrievePersEcm?crkyCn="+str(api_key)+"&persEcm=" + soc_no.upper() + "&pltxNm=" + rcvname + "&cralTelno=" + rcv_phone
    #param = {'text': word, 'options': 4}
    source_code = requests.get(setrurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    if source_code.status_code == 200:
        if str(source_code.text).find('<tCnt>1</tCnt>') > -1:
            rtnFlg = "0"
        else:
            rtnFlg = "1"
            print(">> source_code.text : {}".format(source_code.text))

    return rtnFlg

def imgComp(fs_url, ali_url):

    file_path = os.path.dirname(os.path.abspath(__file__)) 
    if os.path.exists(file_path+ "\\img_fs.jpg"):
        os.remove(file_path+ "\\img_fs.jpg")
    if os.path.exists(file_path+ "\\img_ali.jpg"):
        os.remove(file_path+ "\\img_ali.jpg")

    time.sleep(1)
    # 프리쉽 상품 URL 이미지 다운로드
    urllib.request.urlretrieve(str(fs_url), file_path+"\\img_fs.jpg")
    time.sleep(2)

    # 알리 상품 이미지 다운로드
    r = requests.get(ali_url)
    with open(file_path+"\\img_ali.jpg", "wb") as outfile:
        outfile.write(r.content)
    time.sleep(2)

    # 프리쉽 상품 이미지와 알리 상품 이미지 비교 
    imageA = cv2.imread(file_path+"\\img_fs.jpg")
    imageB = cv2.imread(file_path+"\\img_ali.jpg")
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    if len(grayA) == 0 or len(grayB) == 0:
        return "-1"

    # 이미지의 구조 비교
    if len(grayA)==len(grayB):
        #print(" 이미지 구조 같음 ")
        return "0"
    else:
        print(" 이미지 구조 다름 ")
        return "1"

def elem_clear(browser, elem):

    time.sleep(0.1)
    browser.find_elements(By.CSS_SELECTOR,elem)[0].send_keys(Keys.CONTROL + "a")
    time.sleep(0.1)
    browser.find_elements(By.CSS_SELECTOR,elem)[0].send_keys(Keys.DELETE)
    time.sleep(0.1)
    browser.find_elements(By.CSS_SELECTOR,elem)[0].clear()
    time.sleep(0.3)

    return

def optionName(ord_optionstr):

    ord_option_name = ord_optionstr
    # 첫번째두번째 문자가 /: 일경우 /:제거
    if ord_option_name[:2] == "/:":
        ord_option_name = ord_option_name[2:]
        print('>> 첫번째 문자 /(슬러시) 제거 : ' + str(ord_option_name))

    # 첫번째 문자가 : 일경우 :제거
    if ord_option_name[:1] == ":":
        ord_option_name = ord_option_name[1:]
        print('>> 첫번째 문자 :(슬러시) 제거 : ' + str(ord_option_name))

    # 첫번째 문자가 / 일경우 /제거
    if ord_option_name[:1] == "/":
        ord_option_name = ord_option_name[1:]
        print('>> 첫번째 문자 /(슬러시) 제거 : ' + str(ord_option_name))

    fd_st3_pos = ord_option_name.find(',수량')
    if fd_st3_pos > -1:
        ord_option_name = ord_option_name[:fd_st3_pos]
        print('>> [옵션 ,수량 부분 제거]  : ' + str(ord_option_name))

    # +( 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
    fd_st4_pos = ord_option_name.find('(+')
    if fd_st4_pos > -1:
        ord_option_name = getparse(ord_option_name, '','(+').strip()
        print('>> [옵션 +( 부분 제거]  : ' + str(ord_option_name))

    # 괄호 있는 옵션 #################################
    if ord_option_name[:1] == "(":
        ord_option_name = getparse(ord_option_name, ')','').strip()
        print(">> * 괄호 있는 옶션 : " + str(ord_option_name))

    ord_option_name = ord_option_name.replace(":","").strip()
    print(">> ord_option_name : {}".format(ord_option_name))
    return ord_option_name


def selShipOption(browser, type):
    flg = "0"
    # 배송 클릭
    # if browser.find_element(By.CSS_SELECTOR,'div.product-dynamic-shipping > div > div > div:nth-child(2) > span > p > span:nth-child(1)'):
    #     browser.find_element(By.CSS_SELECTOR,'div.product-dynamic-shipping > div > div > div:nth-child(2) > span > p > span:nth-child(1)').click()
    time.sleep(1)
    # if browser.find_element(By.CSS_SELECTOR,'div.dynamic-shipping-line.dynamic-shipping-titleLayout > span > span'):
    #     browser.find_element(By.CSS_SELECTOR,'div.dynamic-shipping-line.dynamic-shipping-titleLayout > span > span').click()    

    # if browser.find_element(By.CSS_SELECTOR,'div.product-info > div.product-dynamic-shipping > button'):
    #     browser.find_element(By.CSS_SELECTOR,'div.product-info > div.product-dynamic-shipping > button').click()

    if str(browser.page_source).find('class="product-info"') > -1:
        if browser.find_element(By.CSS_SELECTOR,'div.product-info > div.product-dynamic-shipping > button'):
            browser.find_element(By.CSS_SELECTOR,'div.product-info > div.product-dynamic-shipping > button').click()
    else:
        if str(browser.page_source).find('class="shipping--wrap--') > -1:
            findClassnameD = getparse(str(browser.page_source),'class="shipping--wrap--','">')
            if str(type) == "3":
                findClassnameD = 'div.shipping--wrap--' +str(findClassnameD)+ ' > div > div > div'
            else:
                findClassnameD = 'div.shipping--wrap--' +str(findClassnameD)+ ' > div > div'
            #print(">> findClassnameD : {}".format(findClassnameD))
            if browser.find_element(By.CSS_SELECTOR, findClassnameD):
                browser.find_element(By.CSS_SELECTOR, findClassnameD).click()
            print(">> selShipOption 1(shipping--wrap--)")
        elif str(browser.page_source).find('class="dynamic-shipping"') > -1:
            print(">> selShipOption 2(dynamic-shipping)")
            if browser.find_element(By.CSS_SELECTOR,'div.dynamic-shipping > button'):
                browser.find_element(By.CSS_SELECTOR,'div.dynamic-shipping > button').click()
        else:
            print(">> selShipOption 3(product-dynamic-shipping)")
            if browser.find_element(By.CSS_SELECTOR,'div.product-dynamic-shipping > button'):
                browser.find_element(By.CSS_SELECTOR,'div.product-dynamic-shipping > button').click()

    time.sleep(1.5)
    if str(type) == "2" or str(type) == "3":
        # elemcbtn = 'span.comet-icon.comet-icon-chevrondown'
        #findClassnameM = getparse(str(browser.page_source),'logistics--modalContent--"','"')
        #print(">> findClassnameM : {}".format(findClassnameM))
        #elemcbtn = 'div.comet-modal-content > div.comet-modal-body.logistics--modalContent--' +str(findClassnameM)+ ' > button'
        #elemcbtn = 'div.comet-modal-body.logistics--modalContent--IGIdSew > button'
        elemcbtn = 'div.comet-v2-modal-body.logistics--modalContent--IGIdSew > button'
        dev_result = getparse(str(browser.page_source),'class="comet-v2-modal-content"','')
        #print(">> elemcbtn : {}".format(elemcbtn))
    else:
        elemcbtn = 'div.comet-modal-body._1yog9 > button'
        dev_result = getparse(str(browser.page_source),'class="comet-modal-content"','')
    # dev_result = getparse(str(browser.page_source),'class="comet-modal-content"','')
    if str(dev_result).find('추가 옵션') > -1 or str(dev_result).find('More options') > -1:
        print(">> 추가 옵션 있음 ")
        if browser.find_element(By.CSS_SELECTOR,elemcbtn):
            browser.find_element(By.CSS_SELECTOR,elemcbtn).click()
    time.sleep(1)
    
    #dev_result = getparse(str(browser.page_source),'class="comet-modal-content"','')
    if str(type) == "2" or str(type) == "3":
        dev_result = getparse(str(browser.page_source),'class="comet-v2-modal-content"','')
    else:
        dev_result = getparse(str(browser.page_source),'class="comet-modal-content"','')
    if str(dev_result).find('추가 옵션') > -1 or str(dev_result).find('More options') > -1:
        print(">> 추가 옵션 있음 (2) ")
        if browser.find_element(By.CSS_SELECTOR,elemcbtn):
            browser.find_element(By.CSS_SELECTOR,elemcbtn).click()
        time.sleep(1)

    # 추적 가능한 옵션 클릭
    shipping_lists = browser.find_elements(By.CSS_SELECTOR,'div.dynamic-shipping-line.dynamic-shipping-additionLayout > span')
    if shipping_lists:
        comments_list = {}
        for num, comment in enumerate(shipping_lists):
            ea_item = str(comment.text)
            #print(" {} :".format(ea_item) )
            comments_list[num] = comment

            if ea_item.find("추적 가능") > -1:
                comments_list[num].click()
                print(">> 추적 가능 Click ")
                flg = "1"
                break
    time.sleep(1)
    
    if flg == "0": # 추적 가능한 배송사 없을경우 닫기 버튼 클릭
        # if browser.find_element(By.CSS_SELECTOR,'body > div:nth-child(43) > div.comet-modal-wrap > div > button'):
        #     browser.find_element(By.CSS_SELECTOR,'body > div:nth-child(43) > div.comet-modal-wrap > div > button').click()
        if str(type) == "3":
            if browser.find_element(By.CSS_SELECTOR,'div.comet-v2-modal-wrap > div > button'):
                browser.find_element(By.CSS_SELECTOR,'div.comet-v2-modal-wrap > div > button').click()
        else:
            if browser.find_element(By.CSS_SELECTOR,'div.comet-modal-wrap > div > button'):
                browser.find_element(By.CSS_SELECTOR,'div.comet-modal-wrap > div > button').click()
            time.sleep(1)

    return flg


def getImgUrl(result_org, type):
    if str(type) == "2": ## type2 : 알리 상품 이미지 
        imgUrl = getparse(str(result_org),'"imagePathList":["','"')
    elif str(type) == "3": ## type2 : 알리 상품 이미지 
        imgUrl = getparse(str(result_org),'"imagePathList":["','"')
    else:
        imgUrl = getparse(str(result_org),'"imagePath":"','"')
    return str(imgUrl)

def selOptionClick_type1(browser, option_name, opt_cnt_sel):
    skip_plg = "0"
    print(">> selOptionClick_type1 ")
    source_tmp = str(browser.page_source)
    source_opt = getparse(str(source_tmp),'<div class="sku-property"','class="product-quantity-title"')
    # print(">> source_opt : {}".format(source_opt))

    sp_sour_opt = source_opt.split('<div class="sku-property"')
    if str(sp_sour_opt[opt_cnt_sel]).find('<li class="sku-property-item') > -1:
        source_inner_opt = getparse(str(sp_sour_opt[opt_cnt_sel]),'<li class="sku-property-item','</ul>')
        sp_sour_inner_opt = source_inner_opt.split('<li class="sku-property-item')
        print(">> sp_sour_inner_opt(1)")
    else:
        sp_sour_inner_opt = sp_sour_opt
        print(">> sp_sour_inner_opt(2)")

    #print(">> sp_sour_inner_opt : {}".format(sp_sour_inner_opt))
    source_opt_sel = ""
    if str(sp_sour_opt[opt_cnt_sel]).find('<li class="sku-property-item selected">') > -1:
        source_opt_sel = getparse(str(sp_sour_opt[opt_cnt_sel]),'<li class="sku-property-item selected">','</li>').lower().strip()
        # print(">> source_opt_sel : {}".format(source_opt_sel))

    if source_tmp.find('class="sku-property-list"') > -1:
        #print(" len(sp_sour_opt) {}".format(len(sp_sour_opt)))
        if opt_cnt_sel == 0:
            sku_ul = browser.find_elements(By.CSS_SELECTOR, 'div.product-sku > div > div > ul')[opt_cnt_sel]
        else:
            # elem_ul = 'div.product-sku > div > div:nth-child('+ str(int(opt_cnt_sel)+1) +') > ul'
            # print(" elem_ul : {} ".format(elem_ul))
            # sku_ul = browser.find_elements(By.CSS_SELECTOR, elem_ul)[0]
            # print(" sku_ul(1) : {} ".format(sku_ul))
            sku_ul = browser.find_elements(By.CSS_SELECTOR, 'div.product-sku > div > div > ul')[opt_cnt_sel]
            #print(" sku_ul(2) : {} ".format(sku_ul))

        # sku_ul = browser.find_elements(By.CSS_SELECTOR, 'div.product-sku > div')[opt_cnt_sel]
        print(" div.product-sku > div ")
        # print(" outerHTML : {} ".format(sku_ul.get_attribute("outerHTML")) )
    else:
        sku_ul = browser.find_elements(By.CSS_SELECTOR, 'div.sku-property')[opt_cnt_sel]
        print(" div.sku-property ")
    # print(" sku_ul : {} ".format(sku_ul) )

    time.sleep(1)
    flg = "0"
    if sku_ul and skip_plg == "0":
        comments_text = {}
        #sku_li_div = sku_ul.find_elements(By.TAG_NAME,'li > div')
        sku_li_div = sku_ul.find_elements(By.CSS_SELECTOR,'li > div')
        print(">> sku_li_div (len) : {} ".format(len(sku_li_div)) )
        for num, comment in enumerate(sku_li_div):
            #print(" [{}] : {} ".format(num,comment) )
            #print(" outerHTML : {} ".format(comment.get_attribute("outerHTML")) )
            if str(comment.get_attribute("outerHTML")).find('img src=') > -1: # 이미지 옵션 선택
                ea_title = str(comment.find_element(By.TAG_NAME,'img').get_attribute("title")).replace("  "," ").lower().strip()  
                comment_elm = comment.find_element(By.TAG_NAME,'img')
            elif str(comment.get_attribute("outerHTML")).find('<span>') > -1: # 텍스트 옵션 선택
                ea_title = str(comment.find_element(By.TAG_NAME,'span').text).replace("  "," ").lower().strip()
                comment_elm = comment.find_element(By.TAG_NAME,'span')
            else: # 텍스트 옵션 선택
                ea_title = str(comment.find_element(By.TAG_NAME,'span').get_attribute('title')).replace("  "," ").lower().strip()
                comment_elm = comment.find_element(By.TAG_NAME,'span')
            # print(" ea_title [{}] : {} ".format(num+1,ea_title) )

            if str(sp_sour_inner_opt[num])[:10].find(' disabled') == -1:
                comments_text[num] = comment_elm
                if ea_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        comments_text[num].click()
                        print(">> 옵션 Click : [{}] {}".format(num+1, option_name))
                    flg = "1"
                    break
            else:
                print(">> option (disabled) 선택불가 (Skip) : {} ".format(ea_title) )

        if flg == "1":
            print(" [{}] 옵션 선택 OK ".format(option_name))
        time.sleep(1)
        comments_text.clear()
    else:
        print(">> 옵션 선택 불가 소스 확인 필요 : {}".format(option_name))

    return flg


def selOptionClick_type2(browser, option_name, opt_cnt_sel):
    skip_plg = "0"
    print(">> selOptionClick_type2 ")
    ## type2 : 옵션 선택
    source_tmp = browser.page_source

    if str(source_tmp).find('<span>더 보기</span>') > -1:
        print(">> Option 더 보기 ")
        if browser.find_element(By.CSS_SELECTOR, 'span.comet-icon.comet-icon-chevrondown'):
            browser.find_element(By.CSS_SELECTOR, 'span.comet-icon.comet-icon-chevrondown').click()
            time.sleep(1)
            source_tmp = browser.page_source

    source_opt = getparse(str(source_tmp),'<div class="sku-item--wrap--','<div class="comet-divider')   
    sp_sour_opt = source_opt.split('<div class="sku-item--property--')
    #print(">> sp_sour_opt : {}".format(sp_sour_opt))

    source_opt_sel = ""
    if str(sp_sour_opt[opt_cnt_sel+1]).find('<div class="sku-item--selected--') > -1:
        source_opt_sel = getparse(str(sp_sour_opt[opt_cnt_sel]),'<div class="sku-item--selected--','</div>')
        if source_opt_sel.find('alt="') > -1:
            source_opt_sel = getparse(source_opt_sel,'lt="','"')
        elif source_opt_sel.find('title="') > -1:
            source_opt_sel = getparse(source_opt_sel,'title="','"')

    findClassnameO = getparse(str(browser.page_source),'class="sku--wrap--','">')
    findClassnameO = 'div.pdp-info-right > div.sku--wrap--' +str(findClassnameO)+ ' > div'
    print(">> findClassnameO : {}".format(findClassnameO))

    elem_sku_wrap = browser.find_element(By.CSS_SELECTOR, findClassnameO)
    ea_sku = sp_sour_opt[opt_cnt_sel+1]
    #print(">> ea_sku : {}".format(ea_sku))

    elem_list = elem_sku_wrap.find_element(By.CSS_SELECTOR, 'div:nth-child(' + str(opt_cnt_sel+1) + ') > div:nth-child(2) > div')
    #print(">> elem_list : {}".format(elem_list))
    #### elem_list.get_attribute('innerHTML') ---> 소스 확인
    elem_list_opt = elem_list.find_elements(By.CSS_SELECTOR, 'div')
    ea_sku_item = ea_sku.split('class="sku-item--skus--')[1]
    sp_opt = ea_sku_item.split('class="sku-item--')

    print(">> ----------------------------------------- ")

    flg = "0"
    col_sp_cnt = len(sp_opt) - 1
    if col_sp_cnt > 0 and skip_plg == "0":
        col = 0
        while col < col_sp_cnt:
            ea_opt = sp_opt[col+1]
            if ea_opt.find('class="product-main"') > -1:
                ea_opt = getparse(str(ea_opt),'','class="product-main"')
            if ea_opt.find('</div>') > -1:
                ea_opt = getparse(str(ea_opt),'','</div>')
            print(">> 옵션 str : {}".format(ea_opt))
            if str(ea_opt).find('soldOut--') > -1:
                opt_name = getparse(str(ea_opt),'alt="','"')
                print(">> [{}] (품절) 옵션 선택불가 (Skip) : {}".format(col, opt_name))

            elif str(ea_opt).find('<img src=') > -1:
                #print(">> 이미지 옵션 아이템 ")
                opt_name = getparse(str(ea_opt),'alt="','"')
                opt_title = elem_list_opt[col].find_element(By.CSS_SELECTOR,'img').get_attribute('alt').lower()
                opt_title = str(opt_title).replace("  "," ").strip()
                if opt_title == "" and opt_name != "":
                    opt_title = opt_name.lower().replace("  "," ").strip()
                print(">> [{}] (이미지 옵션) 옵션명 : {} ".format(col, opt_title))
                if opt_title == "":
                    print(">> (skip) [img] No opt_title : {}".format(opt_title))
                elif opt_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        elem_list_opt[col].click()
                        print(">> 옵션 Click : [{}] {}".format(col+1, option_name))
                    flg = "1"
                    break

            elif str(ea_opt).find('text') > -1:
                opt_name = getparse(str(ea_opt),'title="','"')
                opt_title = str(elem_list_opt[col].text).lower()
                opt_title = str(opt_title).replace("  "," ").strip()
                if opt_title == "" and opt_name != "":
                    opt_title = opt_name.lower().replace("  "," ").strip()
                print(">> [{}] (텍스트 옵션) 옵션명 : {} ".format(col, opt_title))
                if opt_title == "":
                    print(">> (skip) [text] No opt_title : {}".format(opt_title))
                elif opt_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        elem_list_opt[col].click()
                        print(">> 옵션 Click : [{}] {}".format(col+1, option_name))
                    flg = "1"
                    break

            elif str(ea_opt).find('title') > -1:
                opt_name = getparse(str(ea_opt),'title="','"')
                opt_title = str(elem_list_opt[col].text).lower()
                opt_title = str(opt_title).replace("  "," ").strip()
                print(">> [{}] (텍스트 옵션) 옵션명 : {} ".format(col, opt_title))
                if opt_title == "" and opt_name != "":
                    opt_title = opt_name.lower().replace("  "," ").strip()
                if opt_title == "":
                    print(">> (skip) [title] No opt_title : {}".format(opt_title))
                elif opt_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        elem_list_opt[col].click()
                        print(">> 옵션 Click : [{}] {}".format(col+1, option_name))
                    flg = "1"
                    break

            col = col + 1  

        if flg == "1":
            print(" [{}] 옵션 선택 OK ".format(option_name))
        time.sleep(1)
    else:
        print(">> 옵션 선택 불가 소스 확인 필요 : {}".format(option_name))

    return flg



def selOptionClick_type0(browser, option_name, opt_cnt_sel):
    skip_plg = "0"
    print(">> selOptionClick_type0 ")
    ## type2 : 옵션 선택
    source_tmp = browser.page_source

    if str(source_tmp).find('<span>더 보기</span>') > -1:
        print(">> Option 더 보기 ")
        if browser.find_element(By.CSS_SELECTOR, 'span.comet-icon.comet-icon-chevrondown'):
            browser.find_element(By.CSS_SELECTOR, 'span.comet-icon.comet-icon-chevrondown').click()
            time.sleep(1)
            source_tmp = browser.page_source

    source_opt = getparse(str(source_tmp),'<div class="sku-item--wrap--','<div class="comet-divider')   
    sp_sour_opt = source_opt.split('<div class="sku-item--property--')
    #print(">> sp_sour_opt : {}".format(sp_sour_opt))

    source_opt_sel = ""
    if str(sp_sour_opt[opt_cnt_sel+1]).find('<div class="sku-item--selected--') > -1:
        source_opt_sel = getparse(str(sp_sour_opt[opt_cnt_sel]),'<div class="sku-item--selected--','</div>')
        if source_opt_sel.find('alt="') > -1:
            source_opt_sel = getparse(source_opt_sel,'lt="','"')
        elif source_opt_sel.find('title="') > -1:
            source_opt_sel = getparse(source_opt_sel,'title="','"')

    findClassnameO = getparse(str(browser.page_source),'class="sku--wrap--','">')
    findClassnameO = 'div.pdp-info-right > div.sku--wrap--' +str(findClassnameO)+ ' > div'
    print(">> findClassnameO : {}".format(findClassnameO))

    elem_sku_wrap = browser.find_element(By.CSS_SELECTOR, findClassnameO)
    ea_sku = sp_sour_opt[opt_cnt_sel+1]
    #print(">> ea_sku : {}".format(ea_sku))

    opt_num_cnt = 0
    elem_list = elem_sku_wrap.find_element(By.CSS_SELECTOR, 'div:nth-child(' + str(opt_cnt_sel+1) + ') > div:nth-child(2) > div')
    elem_list_opt = elem_list.find_elements(By.CSS_SELECTOR, 'div')
    # ea_sku_item = ea_sku.split('class="sku-item--skus--')[1]
    # sp_opt = ea_sku_item.split('class="sku-item--')

    ######################################################
    #### elem_list.get_attribute('innerHTML') ---> 소스 확인
    elem_result = elem_list.get_attribute('innerHTML')
    elem_opt_tmp = getparse(str(elem_result),'<div data-sku-col','')
    elem_sku_sp = elem_opt_tmp.split('<div data-sku-col') # 해당옵션 옵션 실제 리스트
    elem_div_sp = elem_opt_tmp.split('<div ') # (하위 div 전체를 가져와 실제옵션리스트수와 다를수 있음) <div style="background-color: rgb(255, 0, 0);"> --> skip 

    flg = "0"
    eaCnt = 0
    realOptCnt = 0
    print(">> 옵션종류 [{}] (옵션리스트수) : {} (div Cnt : {})".format(opt_cnt_sel+1, len(elem_sku_sp), len(elem_div_sp)))
    for ea_item in elem_div_sp:
        ## print(">> [{}] 옵션 : {}".format(eaCnt, ea_item))

        item = ""
        if ea_item.find('class=') == -1:
            eaCnt = eaCnt + 1
            continue
        elif ea_item.find('<img src=') > -1:
            item = getparse(ea_item,'alt="','"')
        elif ea_item.find('title="') > -1:
            item = getparse(ea_item,'title="','"')
        item = item.lower().replace("  "," ").strip()
        print(">> [{}] 옵션 : {}".format(eaCnt, item))

        if ea_item.find('soldOut--') > -1:
            print(">> [{}] (품절) 옵션 선택불가 (Skip) : {}".format(eaCnt, item))
        else:
            if item == str(option_name).lower().strip():
                print(">> 옵션 일치 ({}): {} | {}".format(realOptCnt, item, option_name))
                elem_list_opt[eaCnt].click()
                time.sleep(1)
                flg = "1"
                print(">> 옵션 Click Ok : (div index:{}) {}".format(eaCnt, option_name))
                break

        eaCnt = eaCnt + 1
        realOptCnt = realOptCnt + 1

        if flg == "1":
            print(" [{}] 옵션 선택 OK ".format(option_name))
    else:
        print(">> 옵션 선택 불가 소스 확인 필요 : {}".format(option_name))

    return flg


def selOptionClick_type3(browser, option_name, opt_cnt_sel):
    skip_plg = "0"

    ## type2 : 옵션 선택
    source_tmp = browser.page_source
    source_opt = getparse(str(source_tmp),'<div class="sku-item--wrap--','<div class="comet-divider')
    sp_sour_opt = source_opt.split('<div class="sku-item--property--')
    #print(">> sp_sour_opt : {}".format(sp_sour_opt))

    source_opt_sel = ""
    if str(sp_sour_opt[opt_cnt_sel+1]).find('<div class="sku-item--selected--') > -1:
        source_opt_sel = getparse(str(sp_sour_opt[opt_cnt_sel]),'<div class="sku-item--selected--','</div>')
        if source_opt_sel.find('alt="') > -1:
            source_opt_sel = getparse(source_opt_sel,'lt="','"')
        elif source_opt_sel.find('title="') > -1:
            source_opt_sel = getparse(source_opt_sel,'title="','"')


    findClassnameO = getparse(str(browser.page_source),'class="sku--wrap--','">')
    findClassnameO = 'div.pdp-info-right > div.sku--wrap--' +str(findClassnameO)+ ' > div'
    elem_sku_wrap = browser.find_element(By.CSS_SELECTOR, findClassnameO)
    ea_sku = sp_sour_opt[opt_cnt_sel+1]
    elem_list = elem_sku_wrap.find_element(By.CSS_SELECTOR, 'div:nth-child(' + str(opt_cnt_sel+1) + ') > div:nth-child(2) > div')

    if str(source_opt).find('<span>더 보기</span>') > -1:
        spMoreBtn = source_opt.split('<span>더 보기</span>')
        print(">> spMoreBtn : ".format(len(spMoreBtn)))

    elem_list_opt = elem_list.find_elements(By.CSS_SELECTOR, 'div')
    ea_sku_item = ea_sku.split('<div class="sku-item--skus--')[1]
    sp_opt = ea_sku_item.split('<div class="sku-item--')
    print(">> ----------------------------------------- ")

    flg = "0"
    col_sp_cnt = len(sp_opt) - 1
    print(">> col_sp_cnt : {} ".format(col_sp_cnt))

    if col_sp_cnt > 0 and skip_plg == "0":
        col = 0
        while col < col_sp_cnt:
            ea_opt = sp_opt[col+1]
            if str(ea_opt).find('soldOut--') > -1:
                opt_name = getparse(str(ea_opt),'alt="','"')
                print(">> [{}] (품절) 옵션 선택불가 (Skip) : {}".format(col, opt_name))
            elif str(ea_opt).find('<img src=') > -1:
                #print(">> 이미지 옵션 아이템 ")
                opt_name = getparse(str(ea_opt),'alt="','"')
                #opt_url = getparse(str(ea_opt),'img src="','"')
                opt_title = elem_list_opt[col].find_element(By.CSS_SELECTOR,'img').get_attribute('alt').lower()
                opt_title = str(opt_title).replace("  "," ").strip()
                print(">> [{}] (이미지 옵션) 옵션명 : {} ".format(col, opt_title))
                if opt_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        elem_list_opt[col].click()
                        print(">> 옵션 Click : [{}] {}".format(col+1, option_name))
                    flg = "1"
                    break
            elif str(ea_opt).find('text--') > -1:
                #print(">> 텍스트 옵션 아이템 ")
                opt_name = getparse(str(ea_opt),'title="','"')
                opt_title = str(elem_list_opt[col].text).lower()
                opt_title = str(opt_title).replace("  "," ").strip()
                print(">> [{}] (텍스트 옵션) 옵션명 : {} ".format(col, opt_title))
                if opt_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip():
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        elem_list_opt[col].click()
                        print(">> 옵션 Click : [{}] {}".format(col+1, option_name))
                    flg = "1"
                    break

            col = col + 1  

        if flg == "1":
            print(" [{}] 옵션 선택 OK ".format(option_name))
        time.sleep(1)
    else:
        print(">> 옵션 선택 불가 소스 확인 필요 : {}".format(option_name))

    return flg

def selOptionClick(browser, option_name, opt_cnt_sel):
    skip_plg = "0"
    source_tmp = browser.page_source
    source_opt = getparse(str(source_tmp),'<div class="sku-property">','class="product-quantity-title"')
    sp_sour_opt = source_opt.split('<div class="sku-property">')
    #print(">> sp_sour_opt : {}".format(sp_sour_opt))
    #print(">> sp_sour_opt[{}] : {}".format(opt_cnt_sel, sp_sour_opt[opt_cnt_sel]))

    source_opt_sel = ""
    if str(sp_sour_opt[opt_cnt_sel]).find('<li class="sku-property-item selected">') > -1:
        source_opt_sel = getparse(str(sp_sour_opt[opt_cnt_sel]),'<li class="sku-property-item selected">','</li>').lower().strip()

    #############################################

    #sku_ul = browser.find_element(By.CSS_SELECTOR,'div.product-sku > div > div > ul')
    sku_ul = browser.find_elements(By.CSS_SELECTOR,'div.sku-property')[opt_cnt_sel]
    flg = "0"
    if sku_ul and skip_plg == "0":
        comments_text = {}
        if str(sp_sour_opt[opt_cnt_sel]).find('img src=') > -1:
            # 이미지 옵션 선택
            sku_li = sku_ul.find_elements(By.TAG_NAME,'li > div > img')
            for num, comment in enumerate(sku_li):
                ea_title = str(comment.get_attribute("title")).replace("  "," ").lower().strip()
                #print(" {} :".format(ea_title) )
                comments_text[num] = comment

                #if ea_title.find(option_name.lower()) > -1:
                if ea_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip:
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:                    
                        comments_text[num].click()
                        print(option_name + ">> 옵션 (img) Click ")
                    flg = "1"
                    break
        else:
            # 텍스트 옵션 선택
            sku_li = sku_ul.find_elements(By.TAG_NAME,'li > div > span')
            for num, comment in enumerate(sku_li):
                ea_title = str(comment.text).replace("  "," ").lower().strip()
                #print(" {} :".format(ea_title) )
                comments_text[num] = comment

                if ea_title == str(option_name).lower().strip():
                    if source_opt_sel != "" and source_opt_sel == option_name.lower().strip:
                        print(">> 이미 선택된 옵션 : {}".format(option_name))
                    else:
                        comments_text[num].click()
                        print(option_name + ">> 옵션 Click ")
                    flg = "1"
                    break

        print(" [{}] 옵션 선택  ".format(option_name))
        time.sleep(2)
        #print('>> time.sleep(2)')
    else:
        print(">> 옵션 선택 불가 소스 확인 필요 : {}".format(option_name))

    return flg




# 주소 잘르기 
def cut_address(db_con, address):
    addr1_result = ""
    addr2_result = ""
    addr3_result = ""
    address = str(address).lstrip().rstrip()
    addr1 = address.split(' ')[0]
    addr2_other = address.replace(addr1,'')
    addr2 = addr2_other[:10]
    print(">> (before) {} ".format(address))

    if addr1 == "대구시":
        addr1_re = "대구광역시"
    elif addr1 == "세종시" :
        addr1_re = "세종특별자치시"
    elif addr1 == "충북" :
        addr1_re = "충청북도"
    elif addr1 == "충남" :
        addr1_re = "충청남도"
    elif addr1 == "전북" :
        addr1_re = "전라북도"
    elif addr1 == "전남" :
        addr1_re = "전라남도"
    elif addr1 == "경북" :
        addr1_re = "경상북도"
    elif addr1 == "경남" :
        addr1_re = "경상남도"
    elif addr1 == "광주시" :
        addr1_re = "광주광역시"
    elif addr1 == "대전시" :
        addr1_re = "대전광역시"
    elif addr1 == "부산시" :
        addr1_re = "부산광역시"
    elif addr1 == "서울시" or addr1 == "서울"  :
        addr1_re = "서울특별시"
    elif addr1 == "울산시"  :
        addr1_re = "울산광역시"
    elif addr1 == "인천시"  :
        addr1_re = "인천광역시"
    elif addr1 == "제주도" or addr1 == "제주"  :
        addr1_re = "제주특별자치도"
    elif addr1 == "강원특별자치도":
        addr1_re = "강원도"
    else:
        addr1_re = addr1

    if addr1_re == "세종특별자치시":
        addr1_result = "Sejong-si"
        addr2_result = "Other"
        addr3_result = str(addr2_other).replace('  ',' ').lstrip().rstrip()
    else:
        # addr1 영문주소 검색
        sql = " select top 1 addr1, addr1_eng from address_info where addr1 = '{}'".format(addr1_re)
        row = db_con.selectone(sql)
        if row:
            addr1_result = row[1]

        if addr1_result != "":
            # addr2 검색
            sql = "select addr1, addr2 from address_info where addr1 = '{}' order by addr1, len(addr2) desc".format(addr1_re)
            rows = db_con.select(sql)
            if rows:
                for row2 in rows:
                    db_addr1 = row2[0]
                    db_addr2 = row2[1]
                    if addr2.find(db_addr2) > -1:
                        addr2_result = db_addr2
                        break

                addr3_result = str(addr2_other).replace(db_addr2,'')
                addr3_result = str(addr3_result).replace('  ',' ').lstrip().rstrip()
                print(">> addr3_result : {} ".format(addr3_result))

    print(">>after : {} | {} | {} ".format(addr1_result, addr2_result, addr3_result))

    return addr1_result, addr2_result, addr3_result

def option_dist(opt_text):
    print(">> (주문) 옵션명 : {}".format(opt_text))
    opt_text = opt_text.strip()
    org_optionTxt = opt_text

    if opt_text == "":
        #print(">>  옵션 없는 주문 : {}".format(opt_text))
        fs_flg_opt = "0"
    else:
        #print(">>  옵션 있는 주문 : {}".format(opt_text))
        fs_flg_opt = "1"

    # 주문 옵션이 있는경우 옵션 코드 추출하기
    if fs_flg_opt == "1":
        if opt_text[:1] == " ":
            opt_text = opt_text[1:]
        if opt_text[:3] == "/ :":
            opt_text = opt_text[3:]
        if opt_text[:2] == "/:":
            opt_text = opt_text[2:]
        if opt_text[:1] == "/":
            opt_text = opt_text[1:]
        if opt_text[:1] == " ":
            opt_text = opt_text[1:]
        if opt_text[:1] == ":":
            opt_text = opt_text[1:]

        if opt_text.find('/') > -1:
            flg_search = "S04"  # SKIP
            print(">>  예전 옵션 (옵션 1개이상 : S04) SKIP 대상: {}".format(opt_text))
            return flg_search

        # ,수량 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st3_pos = opt_text.find(',수량')
        if fd_st3_pos > -1:
            opt_text = opt_text[:fd_st3_pos]
            #print(">> 옵션 ( ),수량 )  CUT: {}".format(opt_text))

        # +( 문자 검색 : 해당 문자 있을경우 그앞부분만 cut
        fd_st4_pos = opt_text.find('(+')
        if fd_st4_pos > -1:
            opt_text = opt_text[:fd_st4_pos]
            #print(">> 옵션 ( +( ) CUT: {}".format(opt_text))

        opt_text = opt_text.strip()
        if opt_text[-1:] == ":":
            opt_text = opt_text[:-1]
            #print(">> 옵션 ( : 제거 ) CUT: {}".format(opt_text))

    return str(opt_text).strip()


def moveScroll(driver, max_scroll_cnt):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 700
    while True:
        sroll_cnt = sroll_cnt + 1
        print(">> sroll_cnt : {}".format(sroll_cnt))
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        if sroll_cnt > max_scroll_cnt:
            break
        last_height = new_height

### 옵션명 중복체크 ( 옵션명 같은것이 여러개 있을경우 true )
def has_duplicates(seq):
    return len(seq) != len(set(seq))

### 옵션명 중복체크 ( 옵션명 같은것이 여러개 있을경우 체크 )
def option_dup_check(source_tmp, dic_opt, soup_sp_cnt):
    dup_flg = "0"
    ea_dis_name = ""
    str_soup_prt_tmp = getparse(str(source_tmp), '"skuPropertyValues":', '')
    sp_sour_prt = str_soup_prt_tmp.split('"skuPropertyValues":') # 옵션 종류

    for ea_prt in sp_sour_prt:
        ea_prt = getparse(str(ea_prt), '"propertyValueDisplayName":', '')
        sp_val_disname = ea_prt.split('"propertyValueDisplayName":') # 옵션명
        cnt_sp_name = len(sp_val_disname)
        print(">> cnt_sp_name : {}".format(cnt_sp_name))
        array_list = []
        for ea_dname in sp_val_disname:
            ea_dis_name = getparse(ea_dname,'"','"')
            ea_dis_value = getparse(ea_dname,'"propertyValueId":',',')
            #print(">> ({}) : {} ".format(ea_dis_value, ea_dis_name))

            # if soup_sp_cnt == 1:
            #     if str(dic_opt['name']) == str(ea_dis_name) and str(dic_opt['code']) == str(ea_dis_value):
            #         array_list.append(str(ea_dis_name) + str('@@') + str(ea_dis_value))
            #     if len(array_list) > 1:
            #         if array_list.count(ea_dis_name) > 1:
            #             print(">> 중복 옵션 있음 : {} ".format(ea_dis_name))
            #             dup_flg = "1"
            #             break

            array_list.append(ea_dis_name)
            #print(">> array_list : {}".format(array_list))
            if len(array_list) > 1:
                if array_list.count(ea_dis_name) > 1:
                    print(">> 중복 옵션 있음 : {} ".format(ea_dis_name))
                    dup_flg = "1"
                    break
        print(">> array_list : {}".format(array_list))
    return dup_flg

#금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_new(target, db_ali):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check from Ban_Title where ban_title = 'title' and isnull(ban_cate_idx,'') = '' "
    prs = db_ali.select(sql)
    for rs in prs:
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

# 타이틀 자동주문 확인 단어 체크 "0":정상단어, "1":금지단어
def checkTitle_new(target, db_FS):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check from ali_order_auto_bantitle where ban_title = 'title' and isnull(ban_cate_idx,'') = '' "
    prs = db_FS.select(sql)
    for rs in prs:
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



def get_codeMsg(code):
    rtnMsg = ""
    if code == "S001":
        rtnMsg = "[S001] 묶음주문건 "
    elif code == "S002":
        rtnMsg = "[S002] 수령인3자리이상 "
    elif code == "S003":
        rtnMsg = "[S003] 수령인 한글아님 "
    elif code == "S004":
        rtnMsg = "[S004] 수량 3개이상 "
    elif code == "S005":
        rtnMsg = "[S005] 우편번호5자리이상 "
    elif code == "S006":
        rtnMsg = "[S006] 취소사유있음 "
    elif code == "S007":
        rtnMsg = "[S007] 통관번호 불일치 "
    elif code == "S008":
        rtnMsg = "[S008] 통관번호 불일치 "
    elif code == "S009":
        rtnMsg = "[S009] 알리 상품코드 없음 "
    elif code == "S010":
        rtnMsg = "[S010] 알리 상품이미지 없음 "
    elif code == "S011":
        rtnMsg = "[S011] 알리 상품이미지 다름 "
    elif code == "S015":
        rtnMsg = "[S015] 상세주소 특수문자포함 "
    elif code == "S016":
        rtnMsg = "[S016] 배송준비중 상태아님 "
    elif code == "S017":
        rtnMsg = "[S017] 수령인명 확인필요 "
    elif code == "S019":
        rtnMsg = "[S019] 배송정보 입력오류 "
    elif code == "S020":
        rtnMsg = "[S020] 상품금액 확인불가"
    elif code == "S021":
        rtnMsg = "[S021] 배송비 4달러초과 "
    elif code == "S022":
        rtnMsg = "[S022] 가격초과 "
    elif code == "S023":
        rtnMsg = "[S023] 마진율 10%이하 "
    elif code == "S024":
        rtnMsg = "추적가능 배송사 없음"
    elif code == "S025":
        rtnMsg = "옵션선택 불가"
    elif code == "S026":
        rtnMsg = "수량선택 불가"
    elif code == "S027":
        rtnMsg = "옵션선택 불일치"
    elif code == "S028":
        rtnMsg = "수량선택 불일치"
    elif code == "S029":
        rtnMsg = "[S029] 어드민메모 있음 "
    elif code == "S030":
        rtnMsg = "[S030] 타이틀 확인필요 "
    elif code == "S031":
        rtnMsg = "[S031] 자동주문 대상에서 제외 "
    elif code == "S050":
        rtnMsg = "[S050] 자동주소 변환불가 "
    elif code == "S060":
        rtnMsg = "[S060] 배송정보 입력오류 "
    elif code == "S077":
        rtnMsg = "[S077] 옵션 소스 확인불가 "
    elif code == "S088":
        rtnMsg = "[S088] 초이스상품 결제 실패 "
    elif code == "S099":
        rtnMsg = "[S099] 결제 실패 "
    elif code == "D001" or code == "D002" or code == "D003":
        rtnMsg = "[{}] 품절 ".format(code)

    elif code == "X01":
        rtnMsg = "[X01] 옵션코드 불일치 "
    elif code == "X02":
        rtnMsg = "[X02] 옵션 재고부족 "
    elif code == "X03":
        rtnMsg = "[X03] 옵션코드 확인불가 "
    elif code == "X04":
        rtnMsg = "[X04] 알리 신 버젼 상품 자동불가 "
    elif code == "X05":
        rtnMsg = "[X05] 옵션코드 옵션수 불일치 "

    elif code == "S01":
        rtnMsg = "[S01] 옵션형식 구버젼 "
    elif code == "S04":
        rtnMsg = "[S04] 옵션형식 구버젼 "
    elif code == "S05":
        rtnMsg = "[S05] 옵션있는 상품"
    elif code == "S06":
        rtnMsg = "[S06] 중복옵션명 있음"

    elif code == "E01":
        rtnMsg = "[E01] 주소변경 버튼 없음 "
    elif code == "E02":
        rtnMsg = "[E02] 주문내역 연락처 확인불가 "
    elif code == "E03":
        rtnMsg = "[E03] Next page url 확인필요 "
    elif code == "E04":
        rtnMsg = "[E04] 배송정보 및 주문검토 체크불가 "
    elif code == "E05":
        rtnMsg = "[{}] USD 설정 불가 ".format(code)
    elif code == "E06":
        rtnMsg = "[{}] 주문버튼 클릭불가 ".format(code)
    elif code == "E07":
        rtnMsg = "[{}] 해외주문번호 입력불가 ".format(code)
    elif code == "E08":
        rtnMsg = "[{}] 해외주문번호 입력불가 (배송준비중 아님) ".format(code)
    elif code == "E09":
        rtnMsg = "[{}] 해외주문번호 입력불가 (현지주문번호 존재) ".format(code)
    elif code == "E10":
        rtnMsg = "[{}] 해외주문번호 확인불가 (주문내역 확인필요) ".format(code)
    elif code == "E11":
        rtnMsg = "[{}] 한국어 설정 불가 ".format(code)
    elif code == "E12":
        rtnMsg = "[{}] 알리 검색창 버튼없음 ".format(code)
    elif code == "E15":
        rtnMsg = "[{}] 주문내역 페이지 확인불가 ".format(code)
    elif code == "E16":
        rtnMsg = "[{}] 결제완료 확인불가 ".format(code)
    elif code == "E17":
        rtnMsg = "[{}] 해외주문번호가 이미 존재 ".format(code)
    elif code == "0":
        rtnMsg = "[정상] 주문완료 "

    return rtnMsg
