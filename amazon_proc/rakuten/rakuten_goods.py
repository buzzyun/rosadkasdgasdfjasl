import os
os.system('pip install --upgrade selenium')
import sys
import datetime
import random
import socket
from selenium import webdriver
import threading
import multiprocessing
import time
import socket
import urllib
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import subprocess
import rakuten_func
import sys
import DBmodule_FR

ver = "02.11"
print('>> ver : '+str(ver))

# 1분 마다 timecount 증가 (2시간 이후 종료)
def fun_timer():
    global timecount
    print(">> Timer : {}".format(datetime.datetime.now()))
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 90):
        print('>> 타임아웃 종료 : {}'.format(datetime.datetime.now()))
        #print(os.system('tasklist')) #프로세스 목록 출력

        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)

            fname = os.path.abspath( __file__ )
            fname = rakuten_func.getparseR(fname,"\\","")
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

def doTestProc(db_con, db_price, browser, asin_item, manage_dic):
    time.sleep(2)
    print('[Test] asin_low : ' + str(asin_item))
    print('< Test Main | 상품코드 : ' + str(asin_item))

    rtnChk = rakuten_func.proc_asin_parse_brower(db_con, db_price, browser, asin_item, manage_dic)  
    spm_asin = asin_item.split('@')
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
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        browser = webdriver.Chrome(service=s, options=option)
    return browser

def connectDriverOld(pgSite, kbn, type):
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
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(type) == "H":
        option.add_argument("--headless") # headless 
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
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
    if str(type) == "H":
        option.add_argument("--headless") # headless 
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

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

def check_browser(browser):
    print(">> Browser Count : {}".format(len(browser.window_handles)))
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
        time.sleep(4)


def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    proc_id = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc_id = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc_id = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    option.add_argument("--incognito") ## 시크릿 모드 추가
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    print(f" >> driver_path: {driver_path}")
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)
    return browser, proc_id

if __name__ == '__main__':

    print(">> start ")
    multiprocessing.freeze_support()
    print(str(datetime.datetime.now()))
    timecount = 0
    list_name = "list"
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

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    time.sleep(1)
    input_Site = str(sys.argv[1]).strip()
    input_pgKbn = str(sys.argv[2]).strip()
    input_tor = str(sys.argv[3]).strip()
    input_type = str(sys.argv[4]).strip().upper()
    print(">> SITE : {} | PG NAME : {} | Tor : {} | Type : {} ".format(input_Site, input_pgKbn, input_tor, input_type))
    if input_Site == "" or input_pgKbn == "" or input_tor == "" or input_type == "":
        print(">> 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    time.sleep(2)
    db_con = DBmodule_FR.Database('shop')
    db_price = DBmodule_FR.Database('naver_price')
    db_FS = DBmodule_FR.Database('freeship')

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

    if pgFilename is None or pgFilename == "":
        pgFilename = "new_" + str(pgName) + ".exe"

    if pgName is None or pgName == "":
        pgName = pgKbn

    db_ali = DBmodule_FR.Database('aliexpress')
    # 194 aliexpress 금지어 리스트
    sql_ali2 = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
    # 194 aliexpress replace 리스트
    sql_ali3 = "select replace_ban_title,replace_title from Replace_Title"
    ban_title_list = db_ali.select(sql_ali2)
    replace_title_list = db_ali.select(sql_ali3)
    db_ali.close()

    # 사이트별 금지어 리스트
    sql_site_ban = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
    replace_site_title_list = db_con.select(sql_site_ban)

    manage_dic = dict()
    manage_dic['pgName'] = pgName
    manage_dic['currIp'] = currIp
    manage_dic['list_name'] = list_name
    manage_dic['pgFilename'] = pgFilename
    manage_dic['pgKbn'] = pgKbn
    manage_dic['pgSite'] = pgSite
    manage_dic['sql1'] = sql1
    manage_dic['sql2'] = sql2
    manage_dic['sql3'] = sql3
    manage_dic['ver'] = ver
    manage_dic['tor'] = input_tor
    manage_dic['ban_title_list'] = ban_title_list
    manage_dic['replace_title_list'] = replace_title_list
    manage_dic['replace_site_title_list'] = replace_site_title_list


    if str(currIp).strip() != "222.104.189.18":
        rakuten_func.version_check_2(db_con, manage_dic)
    time.sleep(1)

    # main_url = "https://www.rakuten.co.jp"
    # #browser = connectDriver(main_url)
    # if input_tor == "Y":
    #     # browser = connectDriverNew(main_url, "Y") #tor 사용
    #     try:
    #         print(">> connectDriverOld set ")
    #         browser = connectDriverOld(main_url, "Y", input_type)
    #     except Exception as e:
    #         print(">> connectDriverNew set ")
    #         try:
    #             browser = connectDriverNew(main_url, "Y", input_type)
    #         except Exception as e:
    #             print(">> connectDriverNew Exception : {}".format(e))
    # else:
    #     # browser = connectDriverNew(main_url, "") #tor 미사용
    #     try:
    #         print(">> connectDriverOld set ")
    #         browser = connectDriverOld(main_url, "", input_type)
    #     except Exception as e:
    #         print(">> connectDriverNew set ")
    #         browser = connectDriverNew(main_url, "", input_type)

    main_url = "https://www.rakuten.co.jp"
    proc_id = ""
    try:
        browser, proc_id = connectSubProcess()
        print(">> connectSubProcess OK ")
    except Exception as e:
        print(">> Exception : {}".format(e))
        try:
            print(">> connectDriverOld set ")
            browser = connectDriverOld(main_url,"", input_type)
        except Exception as e:
            print(">> connectDriverOld except")

    time.sleep(1)
    now_url = "https://www.rakuten.co.jp"
    browser.get(now_url)
    browser.set_window_size(1400, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(3)
    # time.sleep(random.uniform(4,5))

    if input_tor == "Y":
        rakuten_func.checkIP()
        time.sleep(1)
        wCnt = 0 
        while wCnt < 3 :
            rakuten_func.set_new_tor_ip()
            rakuten_func.checkCurrIP_new()
            time.sleep(random.uniform(2,4))
            wCnt = wCnt + 1

    # print('>> main_url : ' + str(main_url)) 
    # try:
    #     browser.get(main_url)
    # except Exception as e:
    #     print('>> exception browser.get ')
    #     time.sleep(random.uniform(2,4))
    #     rakuten_func.procEnd(db_con, browser)

    time.sleep(random.uniform(5,7))
    main_result = ""
    main_result = str(browser.page_source)

    check_browser(browser)

    flg_m = "0"
    low_l = 0
    flg_multi = "0"
    flg_list = ""
    while flg_m == "0":
        time.sleep(2)
        if input_pgKbn == "test":
            # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
            asin_list = input(">> asin@cate_idx@0@guid : ")
            print(" input asin_list : " + str(asin_list))
            flg_multi = doTestProc(db_con, db_price, browser, asin_list, manage_dic)
            # proc end1
        else:
            try:
                if input_pgKbn == "goods":
                    flg_multi = rakuten_func.set_multi(db_con, db_price, browser, manage_dic)
                elif input_pgKbn == "stock":
                    flg_list = rakuten_func.set_updatelist(db_FS, db_con, db_price, browser, manage_dic)
                    flg_multi = rakuten_func.set_stock_multi(db_con, db_price, browser, manage_dic)
                elif str(input_pgKbn).find('stock_out') > -1:
                    flg_multi = rakuten_func.set_stock_out(db_con, db_price, browser, manage_dic)
                elif input_pgKbn.find('stock_check') > -1:
                    flg_list = rakuten_func.set_updatelist(db_FS, db_con, db_price, manage_dic)
                    flg_multi = rakuten_func.set_stock_multi(db_con, db_price, browser, manage_dic)
                else:
                    print(">> input_pgKbn 값을 확인하세요 : {} ".format(input_pgKbn))
                    break
            except Exception as e:
                print('>> exception main ')
                rakuten_func.procEnd(db_con, browser)

        if flg_multi == "1":
            print('>> Complete ')
            time.sleep(2)
        elif flg_multi == "11":
            print('>> (stock) Complete ')
            break
        elif flg_multi == "E":
            print('>> Error (Exit)')
            break
        elif flg_multi == "E99":
            print('>> Error E99 (Exit)')
            break
        time.sleep(1)
        if low_l > 500:
            print('>> mainrow 500 Over (Exit)')
            break
        low_l = low_l + 1

    db_FS.close()
    db_con.close()
    db_price.close()
    browser.delete_all_cookies()
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
        db_ali.close()
    except:
        print(">> subprocess.Popen.kill except")
    if flg_multi == "E99":
        os._exit(1)
    else:
        os._exit(0)