import datetime
import os
import time
import sys
import random
import socket
from selenium import webdriver
import selenium.webdriver.chrome.service as Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
import subprocess
import threading
import taobao_func
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp  : '+str(currIp))

ver = "45.11"
db_con = DBmodule_FR.Database("taobao")

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

# 1분 마다 timecount 증가 (4시간 이후 종료)
def fun_timer():
    global timecount
    print(">> Timer : {}".format(datetime.datetime.now()))
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 240):
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

        time.sleep(5)
        os._exit(1)

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
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
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

    elif tool == 'chrome_new':

        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")

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

def doTestProc(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic, asin_low): #goods_dic, db_con, db_ali, asin_low, connect_mode):
    
    print('[Test] asin_low : ' + str(asin_low))

    sp_asin = asin_low.split('@')
    asin = sp_asin[0]
    catecode = sp_asin[1]
    istmall = sp_asin[2]
    guid = sp_asin[3]

    goods_dic['asin'] = str(asin)
    goods_dic['catecode'] = str(catecode)
    goods_dic['istmall'] = str(istmall)
    goods_dic['guid'] = str(guid)
    pgName = "taobao_goods.exe"

    rtnChk = taobao_func.proc_asin_parse_brower(goods_dic, db_con, db_ali, browser, pgName, "taobao") 
    spm_asin = asin_low.split('@')
    rtn_asin = spm_asin[0]

    if rtnChk == "D01" or rtnChk == "D02" or rtnChk == "D03" or rtnChk == "D04" or rtnChk == "D05" or rtnChk == "D06" or rtnChk == "D07":
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
    time.sleep(5)

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    input_Site = sys.argv[1]
    input_pgKbn = sys.argv[2]
    input_login = sys.argv[3]
    input_Site = str(input_Site).strip()
    input_pgKbn = str(input_pgKbn).strip()
    input_login = str(input_login).strip()

    print(">> SITE : {}".format(input_Site))
    print(">> PG NAME : {}".format(input_pgKbn))
    print(">> LOGIN NAME : {}".format(input_login))

    if input_Site == "" and input_pgKbn == "" and input_login == "":
        print(">> 입력 값을 확인하세요. {} | {} | {}".format(input_Site, input_pgKbn, input_login))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if input_Site == 'taobao':
        pass
    else:
        print(">> 사이트 값을 확인하세요. {} | {} | {}".format(input_Site, input_pgKbn, input_login))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)     

    db_ali = DBmodule_FR.Database('aliexpress')
    db_FS = DBmodule_FR.Database('freeship')
    db_con = DBmodule_FR.Database('taobao')
    db_price = DBmodule_FR.Database('naver_price')

    curr_id = ""
    curr_pass = ""
    connect_mode = "chrome"
    sql = " select login_id, password, connect_mode from python_version_manage where name = '{}'".format(input_login)
    rs = db_con.selectone(sql)
    if rs:
        curr_id = str(rs[0]).strip()
        curr_pass = str(rs[1]).strip()
        connect_mode = str(rs[2]).strip()

    try:
        #browser = taobao_func.connectDriver("chrome")
        #connect_mode = "chrome_new"
        browser = connectDriver(connect_mode)
        wait = WebDriverWait(browser, 10)
    except Exception as e:
        print('>> 예외가 발생 (종료) : ')
        time.sleep(10)
        print('>> time.sleep(10) ')
        os._exit(1)
    else:
        print('>> connectDriver 연결 OK')
        #browser.delete_all_cookies()

    time.sleep(2)     
    now_url = "https://login.taobao.com/member/login.jhtml"
    browser.get(now_url)
    browser.set_window_size(1200, 800)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(3)
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logo-link')))
    time.sleep(random.uniform(4,5))

    ### login ### 
    #taobao_func.loginProc(browser,curr_id,curr_pass)
    taobao_func.loginProc_new(browser,curr_id,curr_pass)

    print(">> ID / PASS 입력 OK ")
    if input_pgKbn == "test":
        time.sleep(2)
        pass
    else:
        time.sleep(5)
        print('>> time.sleep(5) ')

        if str(browser.current_url).find("member/login_unusual.htm") > -1:
            print('>> 인증해 주세요. (30)')
            #input(">> After Key Press : ")
            time.sleep(30)
        if str(browser.current_url).find("member/login_unusual.htm") > -1:
            print('>> 인증해 주세요. (120) ')
            #input(">> After Key Press : ")
            time.sleep(120)

        if str(browser.current_url).find('login.jhtml') > -1:
            print('>> 로그인해 주세요. (60) ')
            #input(">> After Key Press : ")
            time.sleep(60)

        if str(browser.current_url).find('login.jhtml') > -1:
            print(">> now : " + str(datetime.datetime.now()))
            print('>> 로그인후 아무키나 입력해주세요')
            input(">> After Key Press : ")
            print('>> time.sleep(7)')
            time.sleep(7)

        curr_url = browser.current_url
        if str(browser.current_url).find('my_taobao.htm?') > -1 or str(browser.current_url).find('taobao.com') > -1:
            print('>> login Ok : {} '.format(curr_url))
            time.sleep(10)
        else:
            print('>> login Error : {} '.format(curr_url))
            time.sleep(180)
            #input(">> Input Key : ")

        curr_url = browser.current_url
        if str(curr_url).find('login.jhtml') > -1:
            print('>> login Error : {} '.format(curr_url))
            time.sleep(5)
            browser.delete_all_cookies()
            time.sleep(2)
            db_ali.close()
            db_FS.close()
            db_con.close()
            browser.quit()
            os._exit(1)

    goods_dic = dict()
    if input_pgKbn == "test":
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon from python_version_manage where name = 'goods'"
    else:
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon from python_version_manage where name = '{}'".format(input_pgKbn)
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

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName

    # Test Proc 
    if input_pgKbn == "test":
        # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
        asin_list = input(" asin@cate_idx@0@guid : ")
        print(" input asin_list : " + str(asin_list))
        #doTestProc(goods_dic,db_con, db_ali, asin_list, input_Site)
        doTestProc(browser, db_con, db_ali, input_pgKbn, ver, goods_dic, asin_list)
        db_ali.close()
        db_FS.close()
        db_con.close()
        browser.quit()
        os._exit(0) 

    if input_pgKbn != "goods" and str(goods_dic['py_sql1']) == "":
        print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        browser.quit()
        os._exit(1)

    roofCnt = 0
    rtnFlg = ""
    while roofCnt < 500:
        print(">> Browser Count : {}".format(len(browser.window_handles)))
        if len(browser.window_handles) != 1:
            main = browser.window_handles
            last_tab = browser.window_handles[len(main) - 1]
            if str(len(main)) != "1":
                for handle in main:
                    if handle != last_tab:
                        browser.switch_to.window(window_name=last_tab)
                        browser.close()
                    browser.switch_to.window(window_name=handle)
                print(">> Browser Close : {}".format(len(browser.window_handles)))
            time.sleep(2)

        ### taobao goods ###
        if input_pgKbn == "goods":
            rtnFlg = taobao_func.set_updatelist(db_FS, db_con, db_ali, browser, input_pgKbn, ver, goods_dic, db_price)
            rtnFlg = taobao_func.set_multi(browser, db_con, db_ali, input_pgKbn, ver, goods_dic, db_price)
        elif str(input_pgKbn).find('stock_out') > -1:
            rtnFlg = taobao_func.set_updatelist(db_FS, db_con, db_ali, browser, input_pgKbn, ver, goods_dic, db_price)
            rtnFlg = taobao_func.set_stock_out(browser, db_con, db_ali, input_pgKbn, ver, goods_dic)
        elif input_pgKbn == "stock" or input_pgKbn.find("stock_check") > -1:
            rtnFlg = taobao_func.set_updatelist(db_FS, db_con, db_ali, browser, input_pgKbn, ver, goods_dic, db_price)
            rtnFlg = taobao_func.set_stock_multi(browser, db_con, db_ali, input_pgKbn, ver, goods_dic, db_price)

        if rtnFlg == "E99":
            time.sleep(10)
            print(">> Error Exit ")
            break
        if rtnFlg == "1" or rtnFlg == "F":
            time.sleep(2)
            print(">> complete ")
            break

        time.sleep(2)
        roofCnt = roofCnt + 1

    #########################################################################
    print(">> Main End : " + str(datetime.datetime.now()))

    browser.delete_all_cookies()
    db_ali.close()
    db_FS.close()
    db_con.close()
    browser.quit()
    if rtnFlg == "E99":
        os._exit(1)        
    else:
        os._exit(0)
