import os
os.system('pip install --upgrade selenium')
import datetime
import time
from sys import exit
from selenium import webdriver
import selenium.webdriver.chrome.service as Service 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
import subprocess
import pyperclip
import random
import socket
import socks
import sys
import DBmodule_FR
import func_user

global gProc_no
global taobaoIdpip 
global upd_cnt
global err_cnt
global gLogFileName
log_now = datetime.datetime.now()

db_con = DBmodule_FR.Database('freeship')
print(">> Ver : 1.00 | edit : 24-04-25 ")

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
        #path = "C:\project\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--incognito") # 시크릿 모드
        options.add_argument("user-data-dir={}".format(userProfile))
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    if tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
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
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2})
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

    elif tool == 'brave':
        path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return browser

def moveSlide(browser):
    print('slide proc')
    #//*[@id="nc_1_n1z"]
    #slider = browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]')
    slider = browser.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
    #slider = None
    if slider:
        move = ActionChains(browser)
        move.click_and_hold(slider).perform()
        browser.implicitly_wait(5)
        xval = 0
        try:
            move.move_by_offset(10, 1).perform()
            time.sleep(0.1)
            move.move_by_offset(20, 1).perform()
            move.move_by_offset(60, 1).perform()
            move.move_by_offset(80, 1).perform()
            move.move_by_offset(120, 1).perform()
            move.move_by_offset(180, 1).perform()
            move.move_by_offset(250, 1).perform()
            time.sleep(4)
            #main_result = browser.page_source
            if str(browser.page_source).find('class="scale_text slidetounlock"') > -1:
                browser.find_element(By.XPATH,'//*[@id="nc_1__scale_text"]').click()
                time.sleep(1)
        except Exception as e:
            print(">> moveSlide Exception ")
        else:
            move.reset_actions()
            time.sleep(0.1)
        time.sleep(random.uniform(3,5))

def checkSlide(browser):
    #browser.delete_all_cookies()
    flg = "1"
    count = 0
    #main_result = browser.page_source
    if str(browser.page_source).find('class="scale_text slidetounlock"') > -1:
        print(">> slidetounlock (SKIP) ")
        time.sleep(2)
        flg = "0"
        while flg == "0":
            count = count + 1
            #browser.refresh()
            print('slide click : {}'.format(count))
            moveSlide(browser)
            time.sleep(random.uniform(4,5))
            #main_result = browser.page_source
            if str(browser.page_source).find('class="scale_text slidetounlock"') > -1:
                print(">> slidetounlock (SKIP)  ")
                flg == "0"
            else:
                flg == "1"
                break
            if count > 5:
                flg == "E"
                break
    return flg


def loginProc(browser, in_login_id, in_password, auto_set):
    #로그인 복사 붙여넣기로 구현
    # browser.execute_script("window.scrollBy(0, 500)")
    # time.sleep(2)
    browser.implicitly_wait(5)
    pyperclip.copy(in_login_id)
    time.sleep(1)
    elemId = browser.find_element(By.ID,'fm-login-id')
    elemId.send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    elemId.send_keys(Keys.DELETE)
    print('>> fm-login-id (clear)')
    
    elempw = browser.find_element(By.ID,'fm-login-password')
    elempw.send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    elempw.send_keys(Keys.DELETE)
    print('>> fm-login-password (clear)')
    time.sleep(1)

    elemId.click()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    pyperclip.copy(in_password)
    elempw.click()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(3)
    
    if auto_set == "1":
        input("After Login Key Press: ")
    else:
        try:
            browser.find_element(By.XPATH,'//*[@id="login-form"]/div[5]/button').click()
            #browser.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
        except Exception as e:
            print(">> exception check ")
            time.sleep(5)
        else:
            time.sleep(3)
    time.sleep(1)


def procSlideCheck(in_drive):
    result = ""

    time.sleep(2)
    result = in_drive.page_source

    if str(result).find('id="nocaptcha"') > -1:
        print(" nocaptcha slide ( 접속 불가 ) ")

        wCnt = 30
        while wCnt > 0:
            time.sleep(1)
            print(" time.sleep(" + str(wCnt) + ")")
            wCnt = wCnt - 1

        time.sleep(2)
        print(" time.sleep(2)")

        result = in_drive.page_source
        time.sleep(1)
        print(" time.sleep(1)")

        if str(result).find('id="nocaptcha"') > -1:
            return "1"

    return "0"

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):

    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)

    return "0"

def setDB_CheckOrder(in_uid, in_infouid, in_orderno, in_ali_orderno, in_Reason, in_taobaoId):
    print(" setDB_CheckOrder Proc ")

    sql_s = " select OrderNo from freeship_tracking_check where Infouid = '" + str(in_infouid) + "' "
    print(" sql_s : " + str(sql_s))
    row = db_con.selectone(sql_s)

    if not row:
        # 타오바오 취소 및 배송사고건 freeship_tracking_check 테이블에 입력
        iSql = " insert into freeship_tracking_check ( ProcDate, OrderNo, ali_orderno, ali_id, Reason, ouid, Infouid ) "
        iSql = iSql + " values ( getdate(), '" + str(in_orderno) + "','" + str(in_ali_orderno) + "','" +str(in_taobaoId)+ "', '" + str(in_Reason) + "', '" + str(in_uid) + "', '" + str(in_infouid) + "' )"
        print(" cancel order DB table insert : " + str(in_ali_orderno))
        print(" iSql : " + str(iSql))
        db_con.execute(iSql)

    # T_ORDER_DELIVERY 테이블 tracking_china_state 변경
    up_sql = "update T_ORDER_DELIVERY set tracking_china_state = 'F' where Uid = '" + str(in_infouid) + "' "
    print('>> up_sql : ' + str(up_sql))
    db_con.execute(up_sql)

    return "0"

def do_proc(in_driver, in_Proc_no, in_taobaoId):

    upd_cnt = 0
    in_driver.set_window_size(1100, 750)
    in_driver.implicitly_wait(3)

    try:
        in_driver.get('http://trade.taobao.com/trade/itemlist/list_bought_items.htm')
    except Exception as e:
        print('taobao 접속 에러 (종료) ')
        procLogSet(in_Proc_no, "E", "0", str(in_taobaoId) + " | taobao 접속 에러 (종료)")
        time.sleep(30)
        in_driver.quit()
        os._exit(1)

    else:
        print('taobao Connect Ok ')

    time.sleep(2)
    result = in_driver.page_source
    time.sleep(2)

    if str(in_driver.current_url).find("/login.jhtml") > -1:
        procLogSet(in_Proc_no, "E", "0", " 로그인 불가 (종료) ")
        time.sleep(30)
        return "1"

    if str(result).find('id="nocaptcha"') > -1:
        print(" nocaptcha slide ( 접속 불가 ) ")
        procLogSet(in_Proc_no, "E", "0", str(in_taobaoId) + " | nocaptcha slide ( 접속 불가 )")
        time.sleep(30)
        in_driver.quit()
        os._exit(1)

    else:
        print(" Connect OK ")

    time.sleep(3)
    print("-----------------------------------------------")

    # 주문 아이디별 트래킹 번호 미입력 리스트 검색
    sql = " SELECT I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel "
    sql = sql + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    sql = sql + " where I.ali_chk = '0' and D.DeliveryNo is null and D.DeliveryDate is null and O.state in ('201','301','421') "
    sql = sql + " and tracking_china is null AND I.ali_id='" +str(in_taobaoId)+ "' "
    sql = sql + " and tracking_china_state is null "
    sql = sql + " order by ali_ord_date asc "
    print("sql : " + str(sql))
    print("-----------------------------------------------")

    rows = db_con.select(sql)
    low = 1
    lenRows = 0
    if rows:
        lenRows = str(len(rows))
        print(str(in_taobaoId) + " | 리스트 Cnt : " + str(len(rows)))
        procLogSet(in_Proc_no, "P", "0", str(in_taobaoId) + " | 리스트 Cnt : " + str(len(rows)))

        for ea_row in rows:
            tracking_no = ""
            trackNo = ""
            trackSuccess = ""

            ali_orderno = ea_row[0]
            orderNo = ea_row[1]
            state = ea_row[2]
            RegDate = ea_row[3]
            ChkDate = ea_row[4]
            DUid = ea_row[5]
            DInfoUid = ea_row[6]

            # ea_url = 'https://buyertrade.taobao.com/trade/json/transit_step.do?bizOrderId='+str(ali_orderno)
            ea_url = 'https://market.m.taobao.com/app/dinamic/pc-trade-logistics/home.html?orderId='+str(ali_orderno)
            print(" [" + str(low) + "] " + str(orderNo) + " | " + str(DUid) + " | " + str(DInfoUid) + " | " + str(ali_orderno))
            # print(">> url : {}".format(ea_url))
            time.sleep(0.5)
            in_driver.get(ea_url)
            time.sleep(random.uniform(2,4))
            res = in_driver.page_source

            if str(res).find('id="nocaptcha"') > -1:
                print(" nocaptcha slide ( 접속 불가 (transit_step)) ")
                procLogSet(in_Proc_no, "E", "0", str(in_taobaoId) + " | nocaptcha slide ( 접속 불가 (transit_step))")
                in_driver.quit()
                os._exit(1)

            #if str(res).find('{"isSuccess":"false"}') > -1: # 타오바오 거래종료
            #    print(">> res : {}".format(res))
                procLogSet(in_Proc_no, "C", "0", str(in_taobaoId) + " | 취소 확인필요 (taobao_cancel) : " + str(ali_orderno))
            #    setDB_CheckOrder(DUid, DInfoUid, orderNo, ali_orderno, "taobao_cancel",in_taobaoId)
            #else:
            trackTmp = func_user.getparse(str(res),'flexRow pc-company-wrapper">','')
            trackNo = func_user.getparse(str(res),'<span class="rax-text-v2 desc">','</span>').strip()

            if str(trackNo) != "":
                print(str(ali_orderno) + " ( " + str(DInfoUid) + " ) | Delivery No : " +str(trackNo))
                up_sql = "update T_ORDER_DELIVERY set tracking_china = '" + str(trackNo) + "', tracking_china_date = getdate() where Uid = '" + str(DInfoUid) + "'"
                print(" (DB) Update : "+str(trackNo))
                db_con.execute(up_sql)
                upd_cnt = upd_cnt + 1
            else:
                print(str(ali_orderno) + " | No Tracking (Skip) ")
                if trackTmp.find('已下单') > -1: # 주문완료 확인
                    print(">> 주문완료 (已下单) State : {}".format(ali_orderno))
                else:
                    print(">> 주문완료 확인불가 ")
                    cancel_check_url = 'https://trade.taobao.com/trade/detail/trade_order_detail.htm?biz_order_id='+str(ali_orderno)
                    print(">> cancel_check_url : {}".format(cancel_check_url))
                    in_driver.get(cancel_check_url)
                    time.sleep(random.uniform(2,4))
                    cancel_res = in_driver.page_source
                    if str(cancel_res).find(ali_orderno) > -1:
                        print(">> 주문번호 있는지 확인OK : {}".format(ali_orderno))
                        if str(cancel_res).find('交易关闭') > -1:
                            print(">> 타오바오 거래종료 (交易关闭) 확인 OK (취소 등록) : {}".format(ali_orderno))
                            setDB_CheckOrder(DUid, DInfoUid, orderNo, ali_orderno, "taobao_cancel",in_taobaoId) # 타오바오 거래종료
                            procLogSet(in_Proc_no, "C", "0", str(in_taobaoId) + " | 주문취소 : " + str(ali_orderno))
            #input("Key Press : ")

            time.sleep(1)

            low = low + 1
    else:
        print(str(in_taobaoId) + " | 처리 대상 없음 0 ")
        procLogSet(in_Proc_no, "P", "0", str(in_taobaoId) + " : 처리 대상 없음 0 ")

    print(str(in_taobaoId) + " | 실행 cnt  : " + str(lenRows) + " | 테이블 tracking_china 입력 : " + str(upd_cnt))
    procLogSet(in_Proc_no, "F", str(upd_cnt), str(in_taobaoId) + " | 실행 cnt  " + str(lenRows) + " | 테이블 tracking_china 입력 : " + str(upd_cnt))

    return "0"

if __name__ == '__main__':

    print('>> Taobao Delivery Proc ')
    print('>> [--- main start ---] ' + str(datetime.datetime.now()))

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

    upd_cnt = 0
    nodata_cnt = 0
    taobaoId = ""
    login_id = ""
    password = ""
    auto_set = ""
    connect_mode = ""

    gProc_no = "DEV_TAO"
    cur_Ip = socket.gethostbyname(socket.gethostname())
    print(">> cur_Ip : {}".format(cur_Ip))
    print(">> gProc_no : {}".format(gProc_no))

    proc_name = ""
    if cur_Ip == "222.104.189.249":
        proc_name = "tao_249"
    elif cur_Ip == "222.104.189.229":
        proc_name = "tao_229"
    elif cur_Ip == "222.104.189.40":
        proc_name = "tao_40"
    elif cur_Ip == "222.104.189.18":
        proc_name = "tao_40"

    if proc_name != "":
        sql = " select ali_id, login_id, login_pw, auto_set, connect_mode from ali_order_auto_set where proc_name = '{}'".format(proc_name)
        rs = db_con.selectone(sql)
        if rs:
            taobaoId = str(rs[0]).strip()
            login_id = str(rs[1]).strip()
            password = str(rs[2]).strip()
            auto_set = str(rs[3]).strip()
            connect_mode = str(rs[4]).strip()

    if taobaoId == "" or login_id == "" or password == "":
        print(">> 로그인 정보 확인불가 : {} ".format(cur_Ip))
        procLogSet(gProc_no, "E", "0", str(cur_Ip) + " | 로그인 정보 확인불가 (종료)")
        print(">> Main End : " + str(datetime.datetime.now()))
        db_con.close()
        os._exit(1)

    # try:
    #     if connect_mode == "chrome_service_secret":
    #         browser = func_user.connectDriverNew("https://s.taobao.com", "S")
    #     else:
    #         browser = func_user.connectDriverNew("https://s.taobao.com", "")
    # except Exception as e:
    #     try:
    #         if connect_mode == "chrome_service_secret":
    #             browser = func_user.connectDriverOld("https://s.taobao.com", "S")
    #         else:
    #             browser = func_user.connectDriverOld("https://s.taobao.com", "")
    #     except Exception as e:
    #         print('>> connectDriver 접속 에러 (종료) : ', e)
    #         procLogSet(gProc_no, "E", "0", str(taobaoId) + " | connectDriver 접속 에러 (종료)")
    #         time.sleep(10)
    #         print('>> time.sleep(20) ')
    # else:
    #     time.sleep(2)
    #     print('>> connectDriver Ok ')
    # browser.delete_all_cookies()
    # browser.set_window_size(1300, 750)
    # browser.implicitly_wait(3)
    try:
        proc_id, browser = func_user.connectSubProcess()
        print('>> connectSubProcess proc_id : {}'.format(proc_id))
    except Exception as e:
        print('>> connectSubProcess except : {}'.format(e))
        try:
            if connect_mode == "chrome_service_secret":
                browser = func_user.connectDriverOld("https://s.taobao.com", "S")
            else:
                browser = func_user.connectDriverOld("https://s.taobao.com", "")
        except Exception as e:
            print('>> connectDriver 접속 에러 (종료) : ', e)
            procLogSet(gProc_no, "E", "0", str(taobaoId) + " | connectDriver 접속 에러 (종료)")
            time.sleep(10)
            print('>> time.sleep(20) ')
    else:
        time.sleep(2)
        print('>> connectDriver Ok ')

    time.sleep(2)

    if connect_mode == "manual":
        now_url = "http://trade.taobao.com/trade/itemlist/list_bought_items.htm"
    else:
        now_url = "http://login.taobao.com"
    try:
        browser.get(now_url)
    except Exception as e:
        print(">> browser.get except ")

    time.sleep(random.uniform(4,6))
    main = browser.window_handles

    if str(main).find('已买到的宝贝') > -1:
        print(">> Order List pase ")
    else:
        if connect_mode == "manual":
            input(">> After Login Manual Key Press : ")
            print(">> ID / PASS 입력 OK (Manual) ")

        if str(browser.current_url).find("member/login_unusual.htm") > -1 or str(browser.current_url).find('login.jhtml') > -1:
            print('>> time.sleep(10)  ')
            time.sleep(10)

        if str(browser.current_url).find("member/login_unusual.htm") > -1 or str(browser.current_url).find('login.jhtml') > -1:
            print('>> 인증 및 로그인 해주세요. (30)')
            #input(">> After Key Press : ")
            time.sleep(60)

        if str(browser.current_url).find("member/login_unusual.htm") > -1 or str(browser.current_url).find('login.jhtml') > -1:
            print('>> 로그인해 주세요. (60) ')
            input(">> After Key Press : ")
            time.sleep(60)

    if str(browser.current_url).find("/login.jhtml") == -1:
        print('>> PROC START ')

        # 현지 송장 가져오기 
        do_proc(browser, gProc_no, taobaoId)
    else:
        print('>> 로그인 불가 (종료) ')
        procLogSet(gProc_no, "E", "0", str(cur_Ip) + " | 로그인 불가 (종료)")

    db_con.close()
    time.sleep(5)
    print(">> time.sleep(5) ")

    try:
        browser.quit()
        print("proc_id.pid:{}".proc_id.pid)
        subprocess.Popen.kill(proc_id)
    except Exception as e:
        print(">> subprocess.Popen.kill except")
    os._exit(0)

