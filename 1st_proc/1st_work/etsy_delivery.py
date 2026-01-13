import time
import os
import datetime
import socket
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import func_user
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

db_con = DBmodule_FR.Database('freeship')
global gProc_no
global orderId
global upd_cnt
global err_cnt
global ver
ver = "2.0"
print(">> ver : {}".format(ver))

########################################################################################
# handmade 에서 배대지로 발송된 송장(중국) 가져오기
# - T_ORDER_DELIVERY 테이블 tracking_china / tracking_china_date 컬럼에 입력
########################################################################################

# 파싱 함수
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

def delieveyLogSet(infoUid, in_reason, Old_DeliveryNo, delivery_no):

    sql = " SELECT O.uid, I.uid, O.RegDate, O.orderNo, I.ali_orderno, I.ali_id, O.PAYWAY, isnull(O.naver_pay_product_code,''), O.naver_pay_cancel, I.ali_reorder_chk from T_ORDER_info I inner join T_ORDER O on O.uid = I.OrderUid where I.uid ='" + str(infoUid) + "'"   
    row_f = db_con.selectone(sql)
    if row_f:
        D_uid = row_f[0]
        D_infoUid = row_f[1]
        D_RegDate = row_f[2]
        D_orderNo = row_f[3]
        D_ali_orderno = row_f[4]
        D_ali_id = row_f[5]
        D_PAYWAY = row_f[6]
        D_Pay_orderno = row_f[7]
        D_ali_reorder_chk = row_f[8]

        sql_s = "select OrderNo from freeship_tracking_check where infoUid = '" + str(infoUid) + "' and Reason = '" + in_reason + "'"
        row = db_con.selectone(sql_s)
        if not row:
            if in_reason == "mismatchtracking":
                sql_i = " insert into freeship_tracking_check ( ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, InfoUid, pre_trackno, now_trackno ) values(getdate(),'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(D_RegDate, D_orderNo, D_ali_orderno, D_ali_id, D_PAYWAY, D_Pay_orderno, in_reason, D_uid, D_infoUid, Old_DeliveryNo, delivery_no)
            else:
                sql_i = " insert into freeship_tracking_check ( ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, InfoUid ) values(getdate(),'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(D_RegDate, D_orderNo, D_ali_orderno, D_ali_id, D_PAYWAY, D_Pay_orderno, in_reason, D_uid, D_infoUid)
            print(">> delieveyLogSet : " + str(sql_i))
            db_con.execute(sql_i)

            if in_reason == "mismatchtracking":
                sql_d = "delete from freeship_tracking_check where infoUid = '" + str(infoUid) + "' and Reason = 'handmade_notracking'"
                print(">> sql_d : " + str(sql_d))
                db_con.execute(sql_d)

    return "0"

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):

    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    #print(">> setLogProc : " + str(sql))
    db_con.execute(sql)

    return "0"

def loginProc(in_driver, in_login_id, in_password):
    #로그인 복사 붙여넣기로 구현
    in_driver.implicitly_wait(5)
    currIp = socket.gethostbyname(socket.gethostname())
    time.sleep(2)

    if in_driver.find_element(By.CSS_SELECTOR,'#gnav-header-inner > div.wt-flex-shrink-xs-0 > nav > ul > li:nth-child(1) > button'):
        in_driver.find_element(By.CSS_SELECTOR,'#gnav-header-inner > div.wt-flex-shrink-xs-0 > nav > ul > li:nth-child(1) > button').click()

    time.sleep(3)

    pyperclip.copy(in_login_id)
    in_driver.find_element(By.XPATH,'//*[@id="join_neu_email_field"]').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    pyperclip.copy(in_password)
    in_driver.find_element(By.XPATH,'//*[@id="join_neu_password_field"]').click()
    ActionChains(in_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    in_driver.find_element(By.XPATH,'//*[@id="join-neu-form"]/div[1]/div/div[7]/div/button').click()
    time.sleep(3)

    return "0"

def procDelivery(in_url, in_drive, in_Uid, in_InfoUid, in_ali_orderno, in_orderNo, in_orderId):
    global upd_cnt
    delivery_no = ""
    delivery_name = ""
    delivery_state = ""
    
####### Test ###########################
    #in_url = "https://www.etsy.com/your/purchases/2290942217?ref=yr_purchases"
    #in_url = "https://www.etsy.com/your/purchases/2201155054?ref=yr_purchases"
########################################
    in_drive.get(in_url)
    time.sleep(2)
    print(" in_url : " + str(in_url) + "1")

    result_sour = in_drive.page_source
    time.sleep(0.5)
    # print("result2 : "+str(result2))
    if str(result_sour).strip() == "":
        print(" URL 접속 에러 : {}".format(in_ali_orderno))
        return "E"

    if str(result_sour).find('class="order-actions-summary') == -1:
        print(" 처리 대상 없음 (SKIP) : {}".format(in_ali_orderno))
        return "1"
    
    state_check = getparse(str(result_sour),'class="order-actions-summary','</div>')
    if str(state_check).find("Canceled") > -1:
        print(">> Canceled : {}".format(in_ali_orderno))
        delieveyLogSet(in_InfoUid, "handmade_cancel","","")
        return "1"

    delivery_state = getparse(str(result_sour),'data-event="shipment-link">','</div>')
    delivery_state = getparse(str(delivery_state),'','</a>').replace("\n","").strip()

    print(">> delivery_state : {}".format(delivery_state))
    if delivery_state == "":
        print(">> delivery_state Error : {}".format(in_url))
        print(" 처리 대상 없음 (SKIP) : {}".format(in_ali_orderno))
        return "1"

    if delivery_state == "Not Shipped":
        print(">> delivery_state : Not Shipped")
    else:
        print(">> delivery_state : Delivered")
        delivery_no = getparse(str(result_sour),'class="ss-icon ss-delivery"></span>','</div>').strip()
        if str(delivery_no).find('target="_blank">') > -1:
            delivery_no = getparse(str(delivery_no),'target="_blank">','</a>').strip()
        delivery_name = getparse(str(result_sour),'shipment-details-body-carrier clearfix">','<div class="shipment-carrier-tracking-code">').strip()
        if str(delivery_name).find(':') > -1:
            delivery_name = getparse(str(delivery_name),':','').strip()
        if str(delivery_name).find('with ') > -1:
            delivery_name = getparse(str(delivery_name),'with ','').strip()
            
        if len(delivery_no) < 8 and (delivery_state == "Shipped" or delivery_state.find("transit") > -1 ):
            print(">> delivery no 가송장 (SKIP) : " + str(ali_orderno))
            return "1"
            # delieveyLogSet(in_InfoUid, "handmade_notracking","","")
            # delivery_no = str(ali_orderno)
            # delivery_name = "temp"

        if str(delivery_no).find("Etsy") > -1 and (delivery_state == "Shipped" or delivery_state.find("transit") > -1 ):
            print(">> delivery no 가송장 (SKIP) : " + str(ali_orderno))
            return "1"
            # delieveyLogSet(in_InfoUid, "handmade_notracking","","")
            # delivery_no = str(ali_orderno)
            # delivery_name = "temp"

        print(" delivery no : {} | {} ".format(delivery_no, delivery_name))
        if len(delivery_no) > 7:
            if str(delivery_no[:2]) == "SF":
                delivery_name = "SFexpress"

            sql = "select * from handmade_tracking where infouid = '{}'".format(in_InfoUid)
            row = db_con.selectone(sql)
            if not row:
                sql = "insert into handmade_tracking (delivery_id, delicode, delivery_price, orderno, handmade_orderno, ouid, infouid) values ('{}','{}','{}','{}','{}','{}','{}')".format(delivery_name, delivery_no, '0', in_orderNo, in_ali_orderno, in_Uid, in_InfoUid)	
                print(">> sql : {}".format(sql))
                db_con.execute(sql)
            else:
                sql = "update handmade_tracking set delivery_id = '{}', delicode = '{}', orderno ='{}', handmade_orderno = '{}' where infouid = '{}'".format(delivery_name, delivery_no, in_orderNo, in_ali_orderno, in_InfoUid)	
                print(">> sql : {}".format(sql))
                db_con.execute(sql)

            upd_cnt = upd_cnt + 1
        else:
            print(">> delivery no 확인필요 : " + str(ali_orderno))
            procLogSet(gProc_no, "F", "0", "[" +str(orderId)+ "] delivery no 확인필요 : " + str(delivery_name) + str(" | ") + str(delivery_no) + str(" | ") + str(ali_orderno))

    return "0"


def procDelivery_Re(in_url, in_drive, in_Uid, in_InfoUid, in_ali_orderno, in_orderNo, in_orderId, Old_DeliveryNo, payway):
    global upd_cnt
    delivery_no = ""
    delivery_name = ""
    delivery_state = ""
    
    in_drive.get(in_url)
    time.sleep(2.5)
    print(" in_url : " + str(in_url) + "1")

    result_sour = in_drive.page_source
    # print("result2 : "+str(result2))
    current_url = browser.current_url
    if str(current_url).find('https://www.etsy.com/your/purchases') == -1:
        print(" URL 접속 에러 : {}".format(in_ali_orderno))
        return "E"
        
    if str(result_sour).strip() == "":
        print(" URL 접속 에러  : {}".format(in_ali_orderno))
        return "E"

    if str(result_sour).find('trying to view a receipt that does not belong to you') > -1:
        print(" 해당 주문내역 없음 (SKIP) : {}".format(in_ali_orderno))
        return "1"

    if str(result_sour).find('class="order-actions-summary') == -1:
        print(" 처리 대상 없음 (SKIP) : {}".format(in_ali_orderno))
        return "1"

    state_check = getparse(str(result_sour),'class="order-actions-summary','</div>')
    if str(state_check).find("Canceled") > -1:
        print(">> Canceled : {}".format(in_ali_orderno))
        delieveyLogSet(in_InfoUid, "handmade_cancel","","")
        return "1"

    delivery_state = getparse(str(result_sour),'data-event="shipment-link">','</div>')
    delivery_state = getparse(str(delivery_state),'','</a>').replace("\n","").strip()

    print(">> delivery_state : {}".format(delivery_state))
    if delivery_state == "":
        print(">> delivery_state Error : {}".format(in_url))
        print(" 처리 대상 없음 (SKIP) ")
        return "1"

    ############ test ###########################################
    # print(">> delivery_no : {}".format(delivery_no))
    # input(">> Input Key (1) : ")
    ############ test ###########################################

    # print(">> delivery_state : {}".format(delivery_state))
    if delivery_state == "Not Shipped":
        print(">> delivery_state : Not Shipped")
    else:
        print(">> delivery_state : Delivered")
        delivery_no = getparse(str(result_sour),'class="ss-icon ss-delivery"></span>','</div>').strip()

        ############ test ###########################################
        # print(">> delivery_no : {}".format(delivery_no))
        # keyTmp2 = ""
        # keyTmp2 = input(">> Input Key (1) : ")
        # if keyTmp2 == "Y":
        #     print(">> shipment : {}".format(getparse(str(result_sour),'shipment-details-body-carrier clearfix">','<div class="shipment-details clearfix">')))
        ############ test ###########################################

        if str(delivery_no).find('target="_blank">') > -1:
            delivery_no = getparse(str(delivery_no),'target="_blank">','</a>').strip()
        
        if str(result_sour).find('<div class="shipment-carrier-name">') > -1:
            delivery_name = getparse(str(result_sour),'<div class="shipment-carrier-name">','</div>').strip()
            if str(delivery_name).find('target="_blank">') > -1:
                delivery_name = getparse(str(delivery_name),'target="_blank">','</a>').strip()
        else:
            delivery_name = getparse(str(result_sour),'shipment-details-body-carrier clearfix">','<div class="shipment-carrier-tracking-code">').strip()

        if str(delivery_name).find(':') > -1:
            delivery_name = getparse(str(delivery_name),':','').strip()
        if str(delivery_name).find('with ') > -1:
            delivery_name = getparse(str(delivery_name),'with ','').strip()
            
        if len(delivery_no) < 8 and (delivery_state == "Shipped" or delivery_state.find("transit") > -1 ):
            print(">> delivery no 가송장 : " + str(ali_orderno))
            return "1"

        if str(delivery_no).find("Etsy") > -1 and (delivery_state == "Shipped" or delivery_state.find("transit") > -1 ):
            print(">> delivery no 가송장 : " + str(ali_orderno))
            return "1"

        print(" delivery no : {} | {} ".format(delivery_no, delivery_name))
        DeliveryUid = ""
        DeliveryName = ""
        if len(delivery_no) > 7:
            if str(delivery_no[:2]) == "SF":
                DeliveryUid = "19"
                DeliveryName = "SFexpress"               
            elif str(delivery_name).find('DHL') > -1:
                DeliveryUid = "5"
                DeliveryName = "DHL"    
            elif str(delivery_name).find('FEDEX') > -1 or str(delivery_name).find('FedexIP') > -1:
                DeliveryUid = "6"
                DeliveryName = "FEDEX"    
            elif str(delivery_name).find('CJ-IPS"') > -1:
                DeliveryUid = "4"
                DeliveryName = "CJ대한통운(국제택배)"    
            elif str(delivery_name).find('UPS') > -1:
                DeliveryUid = "7"
                DeliveryName = "UPS"    
            elif str(delivery_name).find('TNT') > -1:
                DeliveryUid = "15"
                DeliveryName = "TNT" 
            else:
                if len(delivery_no) == 13 and str(delivery_no[:1]) != "S" and str(delivery_no[:1]) != "M" and str(delivery_no[:3]) != "ETH" and str(delivery_no[:1]) != "B" and str(delivery_no[:1]) != "Q" and str(delivery_no[:3]) != "FTL"and str(delivery_no[:2]) != "ET" and str(delivery_no[:2]) != "MP" and str(delivery_no[:2]) != "60":
                    DeliveryUid = "2"
                    DeliveryName = "국제등기" 
                elif str(delivery_no[:2]) != "60":
                    DeliveryUid = "12"
                    DeliveryName = "우체국택배" 
                else:
                    DeliveryUid = "16"
                    DeliveryName = "기타택배"
                    print(">> 새로운 택배사 등록 확인바람 : " + str(ali_orderno))
                    procLogSet(gProc_no, "F", "0", "[" +str(orderId)+ "] (가송장) 새로운 택배사 확인필요 : " + str(delivery_name) + str(" | ") + str(ali_orderno))

            ############ test ###########################################
            # print(">> delivery_no : {}".format(delivery_no))
            # KeyTmp = ""
            # keyTmp = input(">> Input Key (2) : ")
            # if KeyTmp == "Y":
            #     print(">> result_sour : {}".format(result_sour))
            ############ test ###########################################

            if str(Old_DeliveryNo) == str(delivery_no):
                print(">> 이전 트래킹번호랑 같음 (Skip) : {}".format(in_orderNo))
            else:
                if payway == "NaverPay":
                    delieveyLogSet(in_InfoUid, "mismatchtracking", Old_DeliveryNo, delivery_no)
                else:
                    sql_d = "delete from freeship_tracking_check where infoUid = '" + str(in_InfoUid) + "' and Reason = 'handmade_notracking'"
                    print(">> sql_d : " + str(sql_d))
                    db_con.execute(sql_d)

                u_sql = "update T_ORDER_DELIVERY set DeliveryUid = '{}', DeliveryName = '{}', DeliveryNo = '{}', DeliveryNoChangeDate = getdate(), pre_trackno = '{}', tracking_china_date = getdate(), tracking_china_state = 'T' where uid = '{}'".format(DeliveryUid, DeliveryName, delivery_no, Old_DeliveryNo, in_InfoUid)
                print(">> (가송장) u_sql : " + str(u_sql))
                db_con.execute(u_sql)

                upd_cnt = upd_cnt + 1
        else:
            print(">> (가송장) delivery no 확인필요 : " + str(ali_orderno))
            procLogSet(gProc_no, "F", "0", "[" +str(orderId)+ "] (가송장) delivery no 확인필요 : " + str(delivery_name) + str(" | ") + str(ali_orderno))

        ############ test ###########################################
        # input(">> Input Key (3) : ")
        ############ test ###########################################

    return "0"

def connectDriver(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    if mode == "S":
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

    return browser


if __name__ == '__main__':

    upd_cnt = 0
    err_cnt = 0

    print('>> Handmade Delivery Proc ')
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))
    print(">> ver : {}".format(ver))

    try:
        taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
        print(">> taskstr : {}".format(taskstr))  
        os.system(taskstr)
    except Exception as e:
        print('>> taskkill Exception (1)')
    else:
        pass

    ip = socket.gethostbyname(socket.gethostname())
    gProc_no = "DEV_HANDMADE"
    orderId = "handmade"
    cur_Ip = socket.gethostbyname(socket.gethostname())
    proc_name = "etsy_" + func_user.getparseR(cur_Ip,".","")

    # if str(cur_Ip).strip() == "222.104.189.18":
    #     proc_name = "etsy_30"

    time.sleep(1)
    if proc_name != "":
        sql = " select ali_id, login_id, login_pw, auto_set, connect_mode from ali_order_auto_set where proc_name = '{}'".format(proc_name)
        rs = db_con.selectone(sql)
        if rs:
            orderId = str(rs[0]).strip()
            login_id = str(rs[1]).strip()
            password = str(rs[2]).strip()

    procLogSet(gProc_no, "S", "0", "[" +str(orderId)+ "] 송장처리 Start : " + str(ip))

    if orderId == "" or login_id == "" or password == "":
        print(">> 로그인 정보 확인불가 : {} ".format(cur_Ip))
        func_user.procLogSet(gProc_no, "E", "0", str(cur_Ip) + " | 로그인 정보 확인불가 (종료)[" + str(orderId)+"]")
        print(">> Main End : " + str(datetime.datetime.now()))
        db_con.close()
        os._exit(1)

    set_browser = "chrome"
    ip = socket.gethostbyname(socket.gethostname())
    now_url = "https://www.etsy.com"
    # browser = connectDriver(now_url,'')
    try:
        print(">> connectSubProcess ")
        proc, browser = func_user.connectSubProcess()
    except Exception as e:
        print(">> connectDriverNew set ")
        browser = func_user.connectDriverNew(now_url, "")

    time.sleep(3)
    browser.get(now_url)
    time.sleep(2)
    #browser.set_window_size(1100, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    print(">> Browser Count : {}".format(len(browser.window_handles)))
    main = browser.window_handles
    last_tab = browser.window_handles[len(main) - 1]
    if str(len(main)) != "1":
        for handle in main:
            if handle != last_tab:
                browser.switch_to.window(window_name=last_tab)
                browser.close()
            browser.switch_to.window(window_name=handle)
        print(">> Browser Close : {}".format(len(browser.window_handles)))
        procLogSet(db_con, "etsy_delivery", ">> ( OpenBrowser Close proc) ") 

    time.sleep(2)

    try:
        now_url = "https://www.etsy.com/your/purchases?ref=hdr_user_menu-txs"
        browser.get(now_url)        
    except Exception as e:
        print('handmade 접속 에러 (종료) : ', e)
        procLogSet(gProc_no, "E", "0", "[" + str(orderId)+"] 접속 에러 (종료)")
        time.sleep(10)
        print('>> time.sleep(10) ')
        browser.quit()
    else:
        time.sleep(4)
        if str(browser.current_url).find('etsy.com/your/purchases') == -1:
            print('handmade Connect Error ')
            procLogSet(gProc_no, "E", "0", "[" + str(orderId)+"] 접속 (로그인) 에러 (종료)")
            input(">> 로그인 처리후 아무키나 입력 해주세요. :")
        else:
            print('handmade Connect Ok ')

    if str(browser.page_source).find('class="order-details-body') > -1:
        print(">> Logined Ok ")
    else:
        # loginProc(browser, login_id, password)
        input("로그인 처리후 아무키나 입력 해주세요. : ")

    # input("Login Key : ")
    print(" ID / PASS 입력 OK ")

    time.sleep(3)
    # print('>> time.sleep(1) ')
    # browser.refresh()
    # time.sleep(1)

    ######################################################
    # 주문 아이디별 가송장 트래킹 재확인후 업데이트처리
    ######################################################
    # sql_2 = " SELECT I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel "
    # sql_2 = sql_2 + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    # sql_2 = sql_2 + " where I.ali_chk = '1' and tracking_china_state = 'F' and O.state in ('201','301','421') and Payway = 'NaverPay' "
    # sql_2 = sql_2 + " AND I.ali_id = '" +str(orderId)+ "' "

    sql_2 = " select I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel, D.DeliveryNo, O.payway "
    sql_2 = sql_2 + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    sql_2 = sql_2 + " where I.ali_chk = '1' and tracking_china_state = 'F' and O.state in ('201','301','421') "
    sql_2 = sql_2 + " AND I.ali_id = '" +str(orderId)+ "' and d.DeliveryDate > getdate() - 90 "
    print("sql_2 : " + str(sql_2))

    # sql_2 = " SELECT I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel "
    # sql_2 = sql_2 + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    # sql_2 = sql_2 + " where orderno = 'H2305211819CNQ' "
    # print("sql_2 : " + str(sql_2))

    rows = db_con.select(sql_2)
    low = 0
    lenRows = 0
    if rows:
        lenRows = str(len(rows))
        print("(가송장) 리스트 Cnt : " + str(len(rows)))
        procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] (가송장) 리스트 Cnt : " + str(len(rows)))

        for ea_row in rows:
            tracking_no = ""
            ali_orderno = ea_row[0]
            orderNo = ea_row[1]
            state = ea_row[2]
            RegDate = ea_row[3]
            ChkDate = ea_row[4]
            DUid = ea_row[5]
            DInfoUid = ea_row[6]
            Old_DeliveryNo = ea_row[9]
            payway = ea_row[10]

            ea_url = 'https://www.etsy.com/your/purchases/' + str(ali_orderno) + "?ref=yr_purchases"
            print(" [" + str(low) + "] " + str(orderNo) + " | " + str(DUid) + " | " + str(DInfoUid) + " | " + str(ali_orderno))

            time.sleep(1)
            rtn_Flg = procDelivery_Re(ea_url, browser, DUid, DInfoUid, ali_orderno, orderNo, orderId, Old_DeliveryNo, payway)
            if rtn_Flg == "E":
                print(" Error Exit : " + str(rtn_Flg))
                procLogSet(gProc_no, "E", "0", "Error Exit : " + str(ali_orderno))
                db_con.close
                browser.quit()
                os._exit(1)
            elif rtn_Flg == "1":
                print(">> SKIP : " + str(rtn_Flg))

            low = low + 1
    else:
        print("(가송장) 리스트 없음 " )
        procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] (가송장) 리스트 없음 ")

    print(" 실행 cnt  " + str(lenRows) + " | (가송장) 테이블 tracking 입력 : " + str(upd_cnt))
    procLogSet(gProc_no, "F", str(upd_cnt), "[" + str(orderId)+"] (가송장) 실행 cnt  " + str(lenRows) + " | (가송장) 테이블 tracking 입력 : " + str(upd_cnt))
    # procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] 프리쉽 가송장처리 완료 ")
    time.sleep(1)
    
    ######################################################
    # 주문 아이디별 송장 트래킹 처리
    ######################################################
    upd_cnt = 0
    sql_d = " delete from handmade_tracking "
    print(">> delete table : " + str(sql_d))
    db_con.execute(sql_d)

    # 주문 아이디별 트래킹 번호 미입력 리스트 검색
    sql = " SELECT I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel "
    sql = sql + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    sql = sql + " where I.ali_chk = '0' and D.DeliveryNo is null and D.DeliveryDate is null and O.state in ('201','301','421') "
    sql = sql + " AND I.ali_id = '" +str(orderId)+ "' "
    sql = sql + " order by ali_ord_date asc "
    print("sql : " + str(sql))

    rows = db_con.select(sql)
    low = 0
    lenRows = 0
    if rows:
        lenRows = str(len(rows))
        print("송장 대상 리스트 Cnt : " + str(len(rows)))
        procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] 송장 대상 리스트 Cnt : " + str(len(rows)))

        for ea_row in rows:
            tracking_no = ""
            ali_orderno = ea_row[0]
            orderNo = ea_row[1]
            state = ea_row[2]
            RegDate = ea_row[3]
            ChkDate = ea_row[4]
            DUid = ea_row[5]
            DInfoUid = ea_row[6]

            ea_url = 'https://www.etsy.com/your/purchases/' + str(ali_orderno) + "?ref=yr_purchases"
            print(" [" + str(low) + "] " + str(orderNo) + " | " + str(DUid) + " | " + str(DInfoUid) + " | " + str(ali_orderno))

            time.sleep(1)
            rtn_Flg = procDelivery(ea_url, browser, DUid, DInfoUid, ali_orderno, orderNo, orderId)
            if rtn_Flg == "E":
                print(" Error Exit : " + str(rtn_Flg))
                procLogSet(gProc_no, "E", "0", "Error Exit : " + str(ali_orderno))
                db_con.close
                browser.quit()
                os._exit(1)
            elif rtn_Flg == "1":
                print(">> SKIP : " + str(rtn_Flg))
                #procLogSet(gProc_no, "F", "0", "처리 대상 없음 : " + str(ali_orderno))
                #break

            low = low + 1
    else:
        print("리스트 없음 " + str(sql))
        procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] 송장 대상 리스트 없음 ")

    print(" 실행 cnt  " + str(lenRows) + " | 테이블 tracking 입력 : " + str(upd_cnt))
    procLogSet(gProc_no, "F", str(upd_cnt), "[" + str(orderId)+"] 실행 cnt  " + str(lenRows) + " | 테이블 tracking 입력 : " + str(upd_cnt))
    print('\n [--- main end ---] ' + str(datetime.datetime.now()))

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/handmade_tracking_proc.asp?mode=del"
    print(" >> Next Proc 실행 (HANDMADE) 프리쉽 송장처리 : handmade_tracking_proc.asp?mode=del : " + str(run_url))

    browser.get(run_url)
    time.sleep(5)
    print(" time.sleep(5) ")
    procLogSet(gProc_no, "P", "0", "[" + str(orderId)+"] 프리쉽 송장처리 완료 " + str(run_url))

###########################
    time.sleep(1)
    db_con.close()
    browser.quit()
    os._exit(0)

