# -*- coding: utf-8 -*-
import os
os.system('pip install --upgrade selenium')
import datetime
import os, random
import time
import sys
import socket
import threading
import multiprocessing
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium import webdriver
import handmade_func
import DBmodule_py

global proc_id
global timecount
global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

ver = "02.31"

# 1분 마다 timecount 증가 (2시간 이후 종료)
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

        time.sleep(5)
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

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    proc = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
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
    return proc, browser

def option_parse(in_sour):
    sp_opt_val = str(in_sour).split('<option value="')
    for ea_opt_val in sp_opt_val:
        opt_val = ""
        opt_name = ""
        if str(ea_opt_val).find('selected="">') > -1:
            print(">> option Skip ")
        else:
            #print("ea_opt_val : {}".format(ea_opt_val))
            opt_val = getparse(str(ea_opt_val),'','"')
            opt_name = getparse(str(ea_opt_val),'">','</option>')
            print(">> option : {} | {}".format(opt_val, opt_name))
    return ""

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

def doTestProc(db_con, db_ali, db_price, asin_low, input_Site):
    
    print('[Test] asin_low : ' + str(asin_low))
    now_url = "https://www.etsy.com"

    set_browser = "chrome"
    setSite = "https://etsy.com"

    #browser = handmade_func.connectDriver(set_browser, 'etsy.com')
    # try:
    #     browser = handmade_func.connectDriverNew(setSite,"Y","N")
    # except Exception as e:
    #     print(">> connectDriverOld set ")
    #     browser = handmade_func.connectDriverOld(setSite,"Y","N")
    #     print(">> connectDriverOld set OK ")
    # browser.set_window_size(1100, 900)
    # browser.set_window_position(140, 0, windowHandle='current')

    now_url = 'https://www.etsy.com/'
    try:
        proc, browser = connectSubProcess()
    except Exception as e:
        print('예외가 발생 (종료) : ', e)
    else:
        print('connectDriver 연결 OK')

    #browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    #handmade_func.procIpChange(1,"Y")
    time.sleep(1)
    browser.get(now_url)
    time.sleep(4)

    print('< Test Main | 상품코드 : ' + str(asin_low))
    # in_asin_str,db_con, db_ali, db_ali2, in_drive, in_pg, in_pgsite
    rtnChk = handmade_func.proc_asin_parse_brower(asin_low, db_con, db_ali, db_ali2, db_price, browser, "goods", input_Site)
    rtnChk = rtnChk[:3]
    spm_asin = asin_low.split('@')
    rtn_asin = spm_asin[0]

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


if __name__ == '__main__':

    multiprocessing.freeze_support()
    print(str(datetime.datetime.now()))
    timecount = 0

    currIp = socket.gethostbyname(socket.gethostname())
    # if str(currIp).strip() != "222.104.189.18":
    #     try:
    #         taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
    #         print(">> taskstr : {}".format(taskstr))  
    #         os.system(taskstr)
    #     except Exception as e:
    #         print('>> taskkill Exception (1)')
    #     else:
    #         pass
    #     time.sleep(4)

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    input_Site = str(sys.argv[1]).strip()
    input_pgKbn = str(sys.argv[2]).strip()
    input_tor = str(sys.argv[3]).strip()
    input_type = str(sys.argv[4]).strip()
    print(">> SITE : {} | PG NAME : {} | Tor : {} | Type : {}".format(input_Site,input_pgKbn,input_tor,input_type))

    if input_Site == "" and input_pgKbn == "" and input_tor == "":
        print(">> 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if input_Site != 'handmade':
        print(">> 사이트 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)     

    db_price = DBmodule_py.Database('naver_price')
    db_ali2 = DBmodule_py.Database('aliexpress', True)
    db_ali = DBmodule_py.Database('aliexpress')
    db_FS = DBmodule_py.Database('freeship')
    db_con = DBmodule_py.Database(input_Site.upper())

    # Test Proc 
    if input_pgKbn == "test":
        # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
        asin_list = input(" asin@cate_idx@0@guid : ")
        print(" input asin_list : " + str(asin_list))

        doTestProc(db_con, db_ali, db_price, asin_list, "handmade")
        # proc end
        db_con.close()
        db_ali.close()
        os._exit(0) 

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

    if now_url == "" or now_url2 == "":
        print(">> 사이트 값을 확인하세요. {} | {} ".format(now_url, now_url2))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)        

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

    if str(currIp).strip() != "222.104.189.18":
        handmade_func.version_check_2(db_con, ver, pgFilename, pgKbn)
    time.sleep(1)

    # set_browser = "chrome"
    # setSite = "https://etsy.com"
    #browser = handmade_func.connectDriver(set_browser, 'etsy.com')
    # try:
    #     browser = handmade_func.connectDriverNew(setSite,input_tor,input_type)
    # except Exception as e:
    #     print(">> connectDriverOld set ")
    #     browser = handmade_func.connectDriverOld(setSite,input_tor,input_type)
    #     print(">> connectDriverOld set OK ")
    # browser.set_window_size(1100, 900)
    # browser.set_window_position(140, 0, windowHandle='current')
    # browser.implicitly_wait(3)

    # handmade_func.procIpChange(3, input_tor)
    # time.sleep(1)
    # browser.get(setSite)
    # time.sleep(4)
    # browser.implicitly_wait(3)
    # time.sleep(2)

    pgSite = 'https://www.etsy.com/'
    try:
        proc_id, browser = connectSubProcess()
        print("proc_id(pid) = {}".format(proc_id.pid))
    except Exception as e:
        print('예외가 발생 (종료) : ', e)
    else:
        print('connectDriver 연결 OK')

    time.sleep(random.uniform(4,7))
    if input_tor == "Y":
        handmade_func.checkIP()
        time.sleep(1)
        wCnt = 0 
        while wCnt < 3 :
            handmade_func.set_new_tor_ip(input_tor)
            handmade_func.checkCurrIP_new(input_tor)
            time.sleep(5)
            wCnt = wCnt + 1

    # setSite = "https://www.etsy.com/featured/hub/sales?ref=Deals24_cat_nav"
    # print('>> main_url : ' + str(setSite)) 
    # try:
    #     browser.get(setSite)
    # except Exception as e:
    #     print('>> exception browser.get ')
    #     time.sleep(10)
    #     # print("proc_id(pid) = ", proc_id.pid)
    #     # subprocess.Popen.kill(proc_id)
    #     handmade_func.procEnd(db_con, db_ali, browser, '')

    #time.sleep(random.uniform(5,7))     
    main_result = ""
    main_result = str(browser.page_source)
    list_name = "list"
    ### check_browser(browser)
    time.sleep(1)

    result = browser.page_source
    time.sleep(2)

    if str(result).find('data-id="gnav-search-submit-button"') == -1:
        print('>> data-id="gnav-search-submit-button" ')
        time.sleep(3)

        try:
            browser.get(now_url2)
        except Exception as e:
            print('>> now_url Connect Exception Error ')
        else:
            time.sleep(4)

    flg_multi = ""
    flg_m = "0"
    low_l = 0
    mainLow = 0
    while flg_m == "0":
        print(">> (Main) start  : " + str(low_l) + " : " + str(datetime.datetime.now()))
        time.sleep(1)

        if input_pgKbn == "goods":
            flg_multi = handmade_func.set_multi(browser, pgName, pgFilename, pgKbn, pgSite, ver, db_con, db_ali, db_ali2, db_price, input_tor)
        elif str(input_pgKbn).find('stock_out') > -1:
            flg_multi = handmade_func.set_stock_out(db_con, db_ali, db_price, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3, input_tor)
        elif input_pgKbn == "stock":
            flg_list = handmade_func.set_updatelist(db_FS, db_con, db_ali, db_ali2, db_price, browser, pgName, pgSite, ver, input_tor)
            flg_multi = handmade_func.set_stock_multi(db_con, db_ali, db_ali2, db_price, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3, input_tor)
        elif str(input_pgKbn).find('stock_check') > -1:
            flg_multi = handmade_func.set_stock_multi(db_con, db_ali, db_ali2, db_price, browser, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2, sql3, input_tor)
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

        low_l = low_l + 1

    #########################################################################
    print(">> Main End : " + str(datetime.datetime.now()))

    # proc end
    db_con.close()
    db_ali.close()
    db_ali2.close()
    browser.quit()
    try:
        subprocess.Popen.kill(proc_id)
    except Exception as e:
        print(">> subprocess.Popen.kill(proc_id) exception")
    if flg_multi == "E99" or flg_multi == "E":
        os._exit(1)
    else:
        os._exit(0)





