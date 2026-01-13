import os
os.system('pip install --upgrade selenium')
import datetime
import subprocess
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
import chromedriver_autoinstaller
import urllib
import threading
import red_func
import DBmodule_FR

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp  : '+str(currIp))

ver = "01.27"
db_con = DBmodule_FR.Database("red")

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
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

def doTestProc(browser, db_con, db_price, in_pgKbn, in_ver, goods_dic, asin_low): #goods_dic, db_con, asin_low, connect_mode):

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

    print('>> set_updatelist ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    pgName = goods_dic['py_pgFilename']

    # update test 
    print('\n\n ----------------- < (test) proc_asin_parse_brower | goodscode : ' + str(asin_low) + ' -------------------------------------')

    # goods test 
    rtnChk = red_func.proc_asin_parse_brower(browser, goods_dic, db_con, pgName, "red", db_price)
    print('>> [ rtnChk ] : ' + str(rtnChk))
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

    input_Site = str(sys.argv[1]).lower().strip()
    input_pgKbn = str(sys.argv[2]).lower().strip()
    input_login = str(sys.argv[3]).lower().strip()
    input_type = str(sys.argv[4]).upper().strip() # headless type 여부 : H - headless 
    print(">> SITE : {} | PG NAME : {} | LOGIN NAME : {} | Type : {} ".format(input_Site, input_pgKbn, input_login, input_type))

    if input_Site == "" and input_pgKbn == "" and input_login == "" and input_type == "":
        print(">> 사이트 값을 확인하세요. {} | {} | {} | {}".format(input_Site, input_pgKbn, input_login, input_type))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if input_Site == 'red':
        pass
    else:
        print(">> 사이트 값을 확인하세요. {} | {} | {} | {}".format(input_Site, input_pgKbn, input_login, input_type))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)     

    db_FS = DBmodule_FR.Database('freeship')
    db_con = DBmodule_FR.Database('red')
    db_price = DBmodule_FR.Database('naver_price')

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

    curr_id = ""
    curr_pass = ""
    connect_mode = "chrome"
    sql = " select login_id, password, connect_mode from python_version_manage where name = '{}'".format(input_login)
    rs = db_con.selectone(sql)
    if rs:
        curr_id = str(rs[0]).strip()
        curr_pass = str(rs[1]).strip()
        connect_mode = str(rs[2]).strip()

    goods_dic = dict()
    if input_pgKbn == "test":
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon, min_qty_order from python_version_manage where name = 'goods'"
    else:
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon, min_qty_order from python_version_manage where name = '{}'".format(input_pgKbn)
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
        goods_dic['min_qty_order'] = str(rs[11]).strip()

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName

        goods_dic['ver'] = ver
        goods_dic['ban_title_list'] = ban_title_list
        goods_dic['replace_title_list'] = replace_title_list
        goods_dic['replace_site_title_list'] = replace_site_title_list

    if input_pgKbn != "test":
        if input_pgKbn != "goods" and str(goods_dic['py_sql1']) == "":
            print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
            time.sleep(5)
            os._exit(1)

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        red_func.version_check_2(db_con, ver, pgFilename, input_pgKbn)

    time.sleep(random.uniform(4,5))
    main_url = "https://www.dcbuy.co.kr"
    proc_id = ""
    #proc, driver = connectSubProcess()
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
    browser.get(main_url)
    browser.set_window_size(1400, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(3)
    time.sleep(random.uniform(4,5))

    roofCnt = 0
    rtnFlg = ""
    while roofCnt < 5000:
        # Test Proc 
        if input_pgKbn == "test":
            asin_list = input(" asin@cate_idx@istmall@guid : ")
            print(" input asin_list : " + str(asin_list))
            rtnFlg = doTestProc(browser, db_con, db_price, input_pgKbn, ver, goods_dic, asin_list)
        elif input_pgKbn == "goods":
            rtnFlg = red_func.set_multi(browser, db_con, input_pgKbn, ver, goods_dic, db_price)
        elif str(input_pgKbn).find('stock_out') > -1:
            rtnFlg = red_func.set_stock_out(browser, db_con, input_pgKbn, ver, goods_dic)
        elif input_pgKbn == "stock" or input_pgKbn.find("stock_check") > -1:
            rtnFlg = red_func.set_updatelist(browser, db_FS, db_con, input_pgKbn, ver, goods_dic, db_price, input_Site)
            rtnFlg = red_func.set_stock_multi(browser, db_con, input_pgKbn, ver, goods_dic, db_price)

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

    db_FS.close()
    db_con.close()
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    if rtnFlg == "E99":
        os._exit(1)
    else:
        os._exit(0)
