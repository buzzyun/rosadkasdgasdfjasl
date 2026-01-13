# -*- coding: utf-8 -*-
import datetime
import os
import time
import sys
import random
import socket
#import socks
from selenium import webdriver
import selenium.webdriver.chrome.service as Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from fake_useragent import UserAgent
import subprocess
import threading
import shop_func
from dbCon import DBmodule_FR

global timecount
global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

ver = "21.00"

# 1분 마다 timecount 증가 (3시간 이후 종료)
def fun_timer():
    global timecount
    print(">> Timer : {}".format(datetime.datetime.now()))
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 120):
        print('>> 타임아웃 종료 : {}'.format(datetime.datetime.now()))
        #print(os.system('tasklist')) #프로세스 목록 출력

        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
            
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

        time.sleep(2)
        os._exit(1)

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


def doTestProc(db_con, db_ali, asin_low, input_Site, goods_dic):
    print('[Test] asin_low : ' + str(asin_low))
    sp_asin = asin_low.split('@')
    in_asin = sp_asin[0]
    catecode = sp_asin[1]
    in_price = sp_asin[2]
    guid = sp_asin[3]

    browser = connectDriver("chrome_service")
    wait = WebDriverWait(browser, 20)

    time.sleep(2)     
    main_url = "https://detail.1688.com/offer/" +str(in_asin)+ ".html"
    print('>> main_url : ' + str(main_url))     
    browser.get(main_url)
    browser.set_window_size(1400, 1000)
    browser.implicitly_wait(3)
    time.sleep(4)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alisearch-keywords')))

    pgName = "shop_goods"
    goods_dic['asin'] = str(in_asin)
    goods_dic['catecode'] = str(catecode)
    goods_dic['guid'] = str(guid)

    print('< Test Main | 상품코드 : ' + str(asin_low))
    # in_asin_str,db_con, db_ali, db_ali2, in_drive, in_pg, in_pgsite
    rtnChk = shop_func.proc_asin_parse_brower(goods_dic, db_con, db_ali, browser, pgName, "shop")  

    if rtnChk == "D01" or rtnChk == "D02" or rtnChk == "D03" or rtnChk == "D04" or rtnChk == "D05" or rtnChk == "D06" or rtnChk == "D07" or rtnChk == "D20":
        print('# Unsellable product (asin delete) : '+str(rtnChk))
    elif rtnChk == "C01" or rtnChk == "C02": # Connection Error
        print('# Url Connect Error : ' + str(rtnChk))
    elif rtnChk == "S01": # 업데이트 금지 상품
        print(' # 업데이트 금지 상품 (SKIP) : ' + str(rtnChk))
    elif rtnChk == "Q01": # setDB (상품 Insert 에러)
        print(' # SetDB 상품 Insert 에러 : ' + str(rtnChk))
    elif rtnChk == "Q02": # setDB (상품 Update 에러)
        print(' # SetDB 상품 Update 에러 : ' + str(rtnChk))
    elif rtnChk == "E01": # 처리중 에러
        print(' # SetDB 상품 Update 에러 : ' + str(rtnChk))
    elif rtnChk == "0":  # 처리 완료
        print(' # SetDB 상품 정상처리 : ' + str(rtnChk))
    else:
        print(' # 그외 rtnChk : ' + str(rtnChk))

    return "0"

def connectDriver(tool):
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
                random.random()) + " Safari/537.36, 'Referer': 'https://www.1688.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        
    elif tool == 'chrome_service':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://www.1688.com/'")

        #desired_capabilities = options.to_capabilities()
        #desired_capabilities['pageLoadStrategy'] = 'none'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

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

    elif tool == 'chrome_service_secret':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2})
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://www.1688.com/'")

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

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    timecount = 0    

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
    time.sleep(4)

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    input_Site = sys.argv[1]
    input_pgKbn = sys.argv[2]
    input_Site = str(input_Site).strip()
    input_pgKbn = str(input_pgKbn).strip()

    #print(">> SITE : {}".format(input_Site))
    #print(">> PG NAME : {}".format(input_pgKbn))

    if input_Site == "" and input_pgKbn == "":
        print(">> 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if input_Site == 'shop':
        pass
    else:
        print(">> 사이트 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)     

    db_ali = DBmodule_FR.Database('aliexpress')
    db_FS = DBmodule_FR.Database('freeship')
    db_con = DBmodule_FR.Database('SHOP')

    connect_mode = "chrome"
    goods_dic = dict()
    sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon, connect_mode from python_version_manage where name = '{}'".format(input_pgKbn)
    rs = db_con.selectone(sql)
    if rs:
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        goods_dic['py_now_url'] = str(rs[2]).strip()
        goods_dic['py_now_url2'] = str(rs[3]).strip()
        goods_dic['py_sql1'] = str(rs[4]).replace("`","'")
        goods_dic['py_sql2'] = str(rs[5]).replace("`","'")
        goods_dic['py_sql3'] = str(rs[6]).replace("`","'")
        goods_dic['py_exchange_Rate'] = str(rs[7]).strip()
        goods_dic['py_dollar_exchange'] = str(rs[8]).strip()
        goods_dic['py_withbuy_cost'] = str(rs[9]).strip()
        goods_dic['py_coupon'] = str(rs[10]).strip()

        connect_mode = str(rs[11]).strip()
        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName

    sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,'') from python_version_manage where name = '{}'".format(input_pgKbn)
    rs = db_con.selectone(sql)
    if not rs:
        print(">> pgKbn 값을 확인하세요 : {} ".format(input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)            
    else:
        pgKbn = input_pgKbn
        pgSite = input_Site
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        now_url = str(rs[2]).strip()
        now_url2 = str(rs[3]).strip()
        sql1 = str(rs[4]).replace("`","'")
        sql2 = str(rs[5]).replace("`","'")
        sql3 = str(rs[6]).replace("`","'")

    # Test Proc 
    if input_pgKbn == "test":
        # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
        asin_list = input(" asin@cate_idx@0@guid : ")
        print(" input asin_list : " + str(asin_list))

        doTestProc(db_con, db_ali, asin_list, "shop", goods_dic)
        # proc end
        db_con.close()
        db_ali.close()
        os._exit(0) 

    if pgFilename is None or pgFilename == "":
        pgFilename = "new_" + str(pgName) + ".exe"
    if pgName is None or pgName == "":
        pgName = pgKbn
    if sql1 == "":
        print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        os._exit(1)
    print('>> [--- ' + str(pgName) + ' main start ---] ' + str(datetime.datetime.now()))

    sql = " select target_sql1, isnull(target_sql2,''), isnull(target_sql3,'') from python_version_manage where name = '{}'".format(pgKbn)
    rs = db_con.selectone(sql)
    if rs:
        sql1 = str(rs[0]).replace("`","'")
        sql2 = str(rs[1]).replace("`","'")
        sql3 = str(rs[2]).replace("`","'")

    if pgKbn != "goods" and sql1 == "":
        print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        os._exit(1)

    print('>> [--- ' + str(pgName) + ' main start ---] ' + str(datetime.datetime.now()))
    print('>> pgName : {} | pgSite : {} | pgFilename : {} | pgKbn : {} | now_url : {} '.format(pgName,pgSite,pgFilename,pgKbn,now_url))

    flg_multi = ""
    flg_m = "0"
    low_l = 0
    mainLow = 0
    #browser = connectDriver("chrome_secret")
    browser = connectDriver(connect_mode)
    
    time.sleep(2)     
    main_url = "https://www.1688.com"
    print('>> main_url : ' + str(main_url))     
    browser.get(main_url)
    time.sleep(2)
    browser.set_window_size(1400, 1000)
    browser.implicitly_wait(5)
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alisearch-keywords')))
    time.sleep(2)

    #input("Key : ")
    #print(">> Browser Count : {}".format(len(browser.window_handles)))
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
        browser.get(now_url)
        time.sleep(2)

    time.sleep(1)
    while flg_m == "0":
        print(">> (Main) start  : " + str(low_l) + " : " + str(datetime.datetime.now()))
        time.sleep(1)

        if input_pgKbn == "goods":
            flg_multi = shop_func.set_multi(browser, db_con, db_ali, pgKbn, ver, goods_dic)
        # elif str(input_pgKbn).find('stock_out') > -1:
        #     flg_multi = shop_func.set_stock_out(db_con, db_ali, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3)
        # elif input_pgKbn == "stock":
        #     flg_list = shop_func.set_updatelist(db_FS, db_con, db_ali, browser, pgName, pgSite, ver)
        #     flg_multi = shop_func.set_stock_multi(db_con, db_ali, db_ali2, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3)
        # elif str(input_pgKbn).find('stock_check') > -1:
        #     flg_multi = shop_func.set_stock_multi(db_con, db_ali, db_ali2, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3)
        else:
            print(">> input_pgKbn 값을 확인하세요 : {} ".format(input_pgKbn))
            break    
        if flg_multi == "11":
            print('>> (stock) Complete ')
            break
        elif flg_multi == "1":
            print('>> Complete ')
            #break
        elif flg_multi == "E":
            print('>> Error (Exit)')
            break
        elif flg_multi == "E99":
            print('>> Error E99 (Exit)')
            break
        if low_l > 200:
            print('>> mainrow 200 Over (Exit)')
            break
        time.sleep(1)
        #print("time.sleep(1)")

        low_l = low_l + 1

    #########################################################################
    print(">> Main End : " + str(datetime.datetime.now()))

    # proc end
    db_con.close()
    db_ali.close()
    browser.quit()
    if flg_multi == "E99" or flg_multi == "E":
        os._exit(1)
    else:
        os._exit(0)





