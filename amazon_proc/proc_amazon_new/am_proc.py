import os
os.system('pip install --upgrade selenium')
import datetime
import multiprocessing
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import subprocess
import time
import threading
import socket
import sys
import DBmodule_AM
import am_func

global ver
global set_browser
global browser
global timecount

ver = "14.45"
print('>> ver: '+str(ver))

# 1분 마다 timecount 증가 (2시간 30분 이후 종료)
def fun_timer():
    global timecount
    print(">> Timer : {}".format(datetime.datetime.now()))
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 150):
        print('>> 타임아웃 종료 : {}'.format(datetime.datetime.now()))
        #print(os.system('tasklist')) #프로세스 목록 출력

        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
            fname = os.path.abspath( __file__ )
            fname = am_func.getparseR(fname,"\\","")
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

def doTestProc(browser, db_con, db_price, asin_low, in_Site, manage_dic):
    time.sleep(2)
    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    print('[Test] asin_low : ' + str(asin_low))
    in_pg = manage_dic['py_pgName']
    in_pgFilename = manage_dic['py_pgFilename']
    in_pgKbn = manage_dic['py_pgKbn']
    in_pgsite = manage_dic['py_pgSite']

    if in_Site == "best" or in_Site == "global":
        now_url = "https://www.amazon.co.jp"
    elif in_Site == "mall" or in_Site == "usa":
        now_url = "https://www.amazon.com"
    elif in_Site == "de":
        now_url = "https://www.amazon.de"
    elif in_Site == "uk":
        now_url = "https://www.amazon.co.uk"
    elif in_Site == "fr":
        now_url = "https://www.amazon.fr"

    print('< Test Main | 상품코드 : ' + str(asin_low))
    #rtnChk = am_func.proc_asin_parse_brower(asin_low, db_con, db_ali, db_price, browser, "goods", in_Site)  
    rtnChk = am_func.proc_asin_parse_brower(asin_low, db_con, db_price, browser, "goods", in_Site, manage_dic)

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

    spm_asin = asin_low.split('@')
    rtn_asin = spm_asin[0]
    rtn_uid = spm_asin[3]
    rtnChk_no = str(rtnChk[:3])
    if rtnChk_no[:1] == "D":
        c_Errcnt = 0
        if rtnChk_no != "D17": d17_Errcnt = 0
        elif rtnChk_no == "D17": d17_Errcnt = d17_Errcnt + 1
        if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
    elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1 # Connection Error 
    elif rtnChk_no == "C04" or rtnChk_no == "C05": c_Errcnt = c_Errcnt + 1 # blocked
    elif rtnChk_no == "0":
        print('>> # SetDB OK (완료) : ' + str(rtnChk))
        c_Errcnt = 0
        d17_Errcnt = 0
        d07_Errcnt = 0

    if rtnChk != "0":  
        if rtnChk_no[:1] == "D":
            D_naver_in = ""
            D_goodscode = ""
            if str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None":
                sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where display_ali_no = '{0}'".format(rtn_asin)
            else:
                sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where uid = '{0}'".format(rtn_uid)                    
            # print(">> sql : {}".format(sql))
            try:
                rs = db_con.selectone(sql)
            except Exception as e:
                print('>> exception 1-1 (sql) : {}'.format(sql))

            if rs:
                Duid = rs[0]
                DIsDisplay = rs[1]
                D_naver_in = rs[5]
                D_goodscode = rs[6]
                print(">> [{}] isDisplay : {} | naver_in : {} ".format(D_goodscode, DIsDisplay, D_naver_in))
                # sold out
                if DIsDisplay == 'T':
                    if rtnChk_no == "D03":  # 금지어 처리 : Forbidden 금지어일 경우 판매불가 상품처리
                        am_func.D03_proc(db_con,Duid, D_naver_in, D_goodscode, "goods")
                    elif rtnChk_no == "D07":
                        print(">> D07 - 품절처리안함 (Skip) ")
                        am_func.stock_proc(db_con, rtn_uid, D_naver_in, D_goodscode, "stock_ck_4")
                    else:
                        am_func.sold_proc(db_con, Duid, D_naver_in, D_goodscode, "goods") # 품절처리 ( 68번 ep_proc_amazon 테이블에 Insert 처리)

    return "0"

def infoManage(db_am, pgKbn, in_pgKbn, pgSite):

    if pgSite == "fr":
        table_name = "python_version_manage_fr"
    else:
        table_name = "python_version_manage"

    sql = " select pgFilename, pgName, now_url, now_url2, sitePost, siteCUR, target_sql1, isnull(target_sql2,''), isnull(target_sql3,'')\
            from {} where name = '{}'".format(table_name, pgKbn)
    rs = db_am.selectone(sql)
    if not rs:
        print(">> pgKbn 값을 확인하세요 : {} ".format(in_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)
    else:
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        now_url = str(rs[2]).strip()
        now_url2 = str(rs[3]).strip()
        sitePost = str(rs[4]).replace('&#8204;','').strip()
        siteCUR = str(rs[5]).strip()
        sql1 = str(rs[6]).replace("`","'").replace("None","")
        sql2 = str(rs[7]).replace("`","'").replace("None","")
        sql3 = str(rs[8]).replace("`","'").replace("None","")

        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        manage_dic['py_now_url'] = now_url
        manage_dic['py_now_url2'] = now_url2
        manage_dic['py_sitePost'] = sitePost
        manage_dic['py_siteCUR'] = siteCUR
        manage_dic['py_sql1'] = sql1
        manage_dic['py_sql2'] = sql2
        manage_dic['py_sql3'] = sql3

        sql = "select exchange_rate, rate_margin, price_min, price_min_plus,price_middle_from, price_middle_to, price_middle_plus, \
            price_max, price_max_plus, price_plus, withbuy_cost, coupon, img_down_flg, withbuy_cost_plus, price_middle_from2, price_middle_to2, price_middle_plus2 \
            from {} where name = 'goods'".format(table_name)
        prs = db_am.selectone(sql)
        #print('##select ## sql :' + str(sql))
        if not prs:
            print(">> getAddpirce 오류 ")
            print(">> Main End : " + str(datetime.datetime.now()))
            os._exit(1)
        else:
            manage_dic['py_exchange_rate'] = prs[0]
            manage_dic['py_rate_margin'] = prs[1]
            manage_dic['py_price_min'] = prs[2]
            manage_dic['py_price_min_plus'] = prs[3]
            manage_dic['py_price_middle_from'] = prs[4]
            manage_dic['py_price_middle_to'] = prs[5]
            manage_dic['py_price_middle_plus'] = prs[6]
            manage_dic['py_price_max'] = prs[7]
            manage_dic['py_price_max_plus'] = prs[8]
            manage_dic['py_price_plus'] = prs[9]
            manage_dic['py_withbuy_cost'] = prs[10]
            manage_dic['py_coupon'] = prs[11]
            manage_dic['py_impy_down_flg'] = prs[12]
            manage_dic['py_withbuy_cost_plus'] = prs[13]
            manage_dic['py_price_middle_from2'] = prs[14]
            manage_dic['py_price_middle_to2'] = prs[15]
            manage_dic['py_price_middle_plus2'] = prs[16]

            if str(manage_dic['py_exchange_rate']) == "" or str(manage_dic['py_exchange_rate']) == "0":
                print(">> getAddpirce 오류 ")
                os._exit(1)

    if pgFilename is None or pgFilename == "":
        pgFilename = "new_" + str(pgName) + ".exe"

    if pgName is None or pgName == "":
        pgName = pgKbn

    if now_url == "" or now_url2 == "" or sitePost == "" or siteCUR == "":
        print(">> 사이트 값을 확인하세요. {} | {} | {} | {}".format(now_url, now_url2, sitePost, siteCUR))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)        

    if pgKbn != "goods" and sql1 == "":
        print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        os._exit(1)

    manage_dic['py_pgFilename'] = pgFilename
    manage_dic['py_pgName']  = pgName
    manage_dic['old_goodscode'] = ""
    manage_dic['old_guid'] = ""
    manage_dic['new_goodscode'] =  ""
    manage_dic['new_guid'] =  ""

    print('>> pgName : {} | pgSite : {} | pgFilename : {} | pgKbn : {} | now_url : {} | sitePost : {} | siteCUR : {} '.format(pgName,pgSite,pgFilename,pgKbn,now_url,sitePost,siteCUR))
    print('>> g_exchange_rate  : ' + str(manage_dic['py_exchange_rate']))
    print('>> g_rate_margin  : ' + str(manage_dic['py_rate_margin']))
    print('>> g_withbuy_cost  : ' + str(manage_dic['py_withbuy_cost']))
    print('>> g_withbuy_cost_plus  : ' + str(manage_dic['py_withbuy_cost_plus']))
    print('>> g_coupon  : ' + str(manage_dic['py_coupon']))
    print('>> [--- ' + str(pgName) + ' main start ---] ' + str(datetime.datetime.now()))

    return manage_dic

def procKill(currIp):
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')

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
    # option.add_argument("--incognito") ## 시크릿 모드 추가
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
    return browser, proc_id

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print(str(datetime.datetime.now()))
    timecount = 0
    currIp = socket.gethostbyname(socket.gethostname())
    procKill(currIp)
    time.sleep(4)

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    in_Site = str(sys.argv[1]).lower().strip() # 사이트 구분 
    in_pgKbn = str(sys.argv[2]).lower().strip() # goods, stock, stock_out 등 구분
    in_tor = str(sys.argv[3]).upper().strip()  # tor 토루 사용여부 : Y - 토루사용, V - VPN 사용 
    in_type = str(sys.argv[4]).upper().strip() # headless type 여부 : H - headless 

    print(">> SITE : {} | PG NAME : {} | Tor : {} | Type : {} ".format(in_Site, in_pgKbn, in_tor, in_type))
    if in_Site == "" or in_pgKbn == "" or in_tor == "" or in_type == "":
        print(">> 입력 값을 확인하세요. {} | {} | {} | {} ".format(in_Site, in_pgKbn, in_tor, in_type))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if in_Site == 'best' or in_Site == 'global' or in_Site == 'mall' or in_Site == 'usa' or in_Site == 'de' or in_Site == 'uk' or in_Site == 'fr':
        pass
    else:
        print(">> 사이트 값을 확인하세요. {} | {} ".format(in_Site, in_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    db_price = DBmodule_AM.Database('naver_price')
    db_FS = DBmodule_AM.Database('freeship')
    db_am = DBmodule_AM.Database(in_Site.upper())

    pgKbn = in_pgKbn
    pgSite = in_Site
    # Test Proc 
    if in_pgKbn == "test":
        pgKbn = "goods"

    #########################################################################
    manage_dic = dict()
    manage_dic['py_pgSite'] = pgSite
    manage_dic['py_pgKbn'] = pgKbn
    manage_dic['py_tor'] = in_tor
    manage_dic['py_type'] = in_type

    manage_dic = infoManage(db_am, pgKbn, in_pgKbn, pgSite)
    manage_dic['ver'] = ver

    now_url = manage_dic['py_now_url']
    sitePost = manage_dic['py_sitePost']
    in_pgFilename = manage_dic['py_pgFilename']
    #in_pgKbn = manage_dic['py_pgKbn']

    if str(currIp).strip() != "222.104.189.18":
        am_func.version_check_2(db_am, ver, in_pgFilename, in_pgKbn, pgSite)

    proc_id_no = ""
    set_browser = "chrome"
    
    if in_Site.upper() == "DE":
        try:
            browser, proc_id_no = connectSubProcess()
            print(">> connectSubProcess set ")
        except Exception as e:
            print(">> connectSubProcess Exception ")
    else:
        if in_tor == "Y": # 토루 사용
            try:
                browser = am_func.connectDriverNew(now_url, "Y", in_type)
            except Exception as e:
                print(">> connectDriverOld set ")
                browser = am_func.connectDriverOld(now_url, "Y", in_type)
                print(">> connectDriverOld set OK ")
        else: # 토루 사용안함
            try:
                print(">> connectDriverOld set")
                browser = am_func.connectDriverOld(now_url, "", in_type)
            except Exception as e:
                print(">> connectDriverOld Exception")
                try:
                    browser = am_func.connectDriverNew(now_url, "", in_type)
                except Exception as e:
                    print(">> connectDriverNew Exception")
                    try:
                        browser, proc_id_no = connectSubProcess()
                        print(">> connectSubProcess set ")
                    except Exception as e:
                        print(">> connectSubProcess Exception ")

    time.sleep(1)
    # browser.set_window_size(1200, 900)
    # browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(2)
    if in_tor == "Y":
        am_func.checkIP()

    wCnt = 0 
    if in_pgKbn == "test":
        pass
    else:
        if in_tor == "Y":
            while wCnt < 3 :
                am_func.set_new_tor_ip()
                am_func.checkCurrIP_new()
                time.sleep(5)
                wCnt = wCnt + 1

    time.sleep(2)
    browser.get(now_url)
    time.sleep(4)

    am_func.check_browser(browser, now_url)
    result = browser.page_source
    time.sleep(2)

    if str(result).find('validateCaptcha') > -1:
        print('>> validateCaptcha (auto) ')
        time.sleep(3)
        try:
            browser.get(now_url)
        except Exception as e:
            print('>> now_url Connect Exception Error ')
        else:
            time.sleep(4)

    ########### Deliver to Set #############################
    deliverTo = am_func.procDeliverChk(browser) #Deliver to check
    print('>> deliverTo (before): ' + str(deliverTo))

    tmp_cPost = sitePost
    if pgSite == "uk":
        tmp_cPost = sitePost[:5]
    if str(deliverTo).find(tmp_cPost) == -1:
        if (pgSite == "uk" ) and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif (pgSite == "usa" ) and str(deliverTo).find("97223") > -1:
            print(" usa 97223 OK (SKIP) ")
        elif (pgSite == "mall" ) and str(deliverTo).find("97223") > -1:
            print(" mall 97223 OK (SKIP) ")
        else:
            if in_pgKbn == "test":
                pass
            else:
                am_func.procDelivertoSet(browser, pgSite, sitePost) #Deliver to Set
            time.sleep(3)

    time.sleep(1)
    deliverTo = am_func.procDeliverChk(browser) #Deliver to check 
    print('>> deliverTo (after): ' + str(deliverTo))
    if str(deliverTo).find(tmp_cPost) == -1:
        print('>> deliverTo no set (SKIP) ' + str(deliverTo))
    ########################################################################

    browser.get_screenshot_as_file('C:\\project\\log\\start.png')
    time.sleep(1)

    flg_m = "0"
    low_l = 0
    flg_multi = ""
    while flg_m == "0":
        am_func.check_browser(browser, now_url)
        print(">> (Main) start  : " + str(low_l) + " : " + str(datetime.datetime.now()))
        time.sleep(3)
        
        db_ali = DBmodule_AM.Database('aliexpress')
        # 194 aliexpress 금지어 리스트
        sql_ali2 = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
        # 194 aliexpress replace 리스트
        sql_ali3 = "select replace_ban_title,replace_title from Replace_Title"
        ban_title_list = db_ali.select(sql_ali2)
        replace_title_list = db_ali.select(sql_ali3)
        db_ali.close()

        # 사이트별 금지어 리스트
        sql_site_ban = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
        replace_site_title_list = db_am.select(sql_site_ban)

        manage_dic['ban_title_list'] = ban_title_list
        manage_dic['replace_title_list'] = replace_title_list
        manage_dic['replace_site_title_list'] = replace_site_title_list

        if in_pgKbn == "test":
            asin_list = input(" asin@cate_idx@0@guid : ")
            print(" input asin_list : " + str(asin_list))
            flg_multi = doTestProc(browser, db_am, db_price, asin_list, in_Site, manage_dic)
        elif in_pgKbn == "goods":
            flg_multi = am_func.set_multi(browser, ver, db_am, db_price, manage_dic)
        elif str(in_pgKbn).find('stock_out') > -1:
            flg_multi = am_func.set_stock_out(db_am, db_price, browser, ver, manage_dic)
        elif in_pgKbn == "stock":
            flg_list = am_func.set_updatelist(db_FS, db_am, db_price, browser, ver, manage_dic)
            flg_multi = am_func.set_stock_multi(db_am, db_price, browser, ver, manage_dic)
        elif str(in_pgKbn).find('stock_check') > -1:
            flg_list = am_func.set_updatelist(db_FS, db_am, db_price, browser, ver, manage_dic)
            flg_multi = am_func.set_stock_multi(db_am, db_price, browser, ver, manage_dic)
        # elif str(in_pgKbn).find('old') > -1:
        #     flg_multi = am_func.set_old_multi(db_am, db_price, browser, ver, manage_dic)
        else:
            print(">> pgKbn 값을 확인하세요 : {} ".format(in_pgKbn))
            break
        if flg_multi == "1":
            print('>> Complete ')
            if pgSite != "uk":
                am_func.set_new_tor_ip()
                am_func.checkCurrIP()
                time.sleep(3)
        elif flg_multi == "11":
            print('>> Complete (stock) ')
            break
        elif flg_multi == "E":
            print('>> Error (Exit)')
            break
        elif flg_multi == "E99":
            print('>> Error E99 (Exit)')
            break
        time.sleep(2)
        if low_l > 500:
            print('>> mainrow 500 Over (Exit)')
            break
        low_l = low_l + 1

    #########################################################################\
    print(">> Main End : " + str(datetime.datetime.now()))

    db_am.close()
    db_price.close()
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id_no)
        print(">> subprocess.Popen.kill")
        procKill(currIp)
    except:
        print(">> subprocess.Popen.kill except")
    if flg_multi == "E99":
        os._exit(1)
    else:
        os._exit(0)





