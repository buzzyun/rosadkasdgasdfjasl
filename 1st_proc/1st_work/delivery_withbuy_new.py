
import os
os.system('pip install --upgrade selenium')

import os.path
from os import path
import datetime
import time
import socket
import time
from urllib.request import Request, urlopen
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date, timedelta
import fnmatch
import subprocess
import DBmodule_FR
import func_user
from selenium.webdriver.chrome.service import Service
print(webdriver.__version__)

global gProc_no
global ins_cnt
log_now = datetime.datetime.now()

db_FS = DBmodule_FR.Database('freeship')

def elem_clear(browser, elem):

    time.sleep(0.2)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.2)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.2)
    elem.clear()
    time.sleep(0.5)

    return

def loginProc(in_driver):
    
    time.sleep(1)

    if str(browser.current_url).find("member/login/targetUrl/") > -1:
        elem_input1 = "#member-login > form > div.form-group > input:nth-child(1)"
        elem_input2 = "#member-login > form > div.form-group > input:nth-child(2)"
        elem_btn = "#member-login > form > button"
        # "#member-login > form > button"
    else:
        elem_input1 = "div.login-form > input:nth-child(1)"
        elem_input2 = "div.login-form > input:nth-child(2)"
        elem_btn = "div.widget.widget-login-info > form > button"

    try:
        elem = browser.find_element(By.CSS_SELECTOR,elem_input1)
        elem_clear(browser, elem)
        elem.send_keys("anmmll")
        elem = browser.find_element(By.CSS_SELECTOR,elem_input2)
        elem_clear(browser, elem)
        elem.send_keys("allin1071")
        browser.find_element(By.CSS_SELECTOR,elem_btn).click()
        time.sleep(2)
    except Exception as e:
        print(">> Exception Login_proc ")
        func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
        input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")

    # try:
    #     in_driver.find_element(By.XPATH,'//*[@name="mb_id"]').send_keys("anmmll")
    # except Exception as e:
    #     print('로그인 접속 에러 (종료) : ', e)
    #     time.sleep(20)
    #     print('>> time.sleep(20) ')
    # else:
    #     print('로그인 화면 OK')

    # time.sleep(1)
    # in_driver.find_element(By.XPATH,'//*[@name="mb_passwd"]').send_keys("allin1071")
    # time.sleep(1)
    # print(" ID / PASS 입력 OK ")

    # in_driver.find_element(By.XPATH,'//*[@id="member-login"]/form/button').click()
    # time.sleep(2)

    return "0"

def proc_alert(in_driver):
    time.sleep(1)
    try:
        da = Alert(in_driver)
        da.accept()
        time.sleep(3)
    except:
        print(" No Alert 2")

    return "0"

def downloadProc(in_driver):

    # 기간 : 60일전부터 오늘까지
    today = date.today()
    day_before = date.today() - timedelta(60)

    startDate = str(day_before).replace("-","")
    endDate = str(today).replace("-","")
    # procList = ['E22','E23','E24','E25','E26'],[발송완료,통관완료,배송완료,통관중,출고완료]
    procList = ['ADAA','ADDA','AXAA','ADCA','E26']


    listCnt = ""
    proc_alert(in_driver)
    time.sleep(3)
    url = ""
    url = "https://www.globalwithbuy.com/agency/order?status=&agencyCode=&dateType=date&date1=" + str(startDate) + "&date2=" + str(endDate)
    print(' url : {}'.format(url))
    try:
        in_driver.get(url)
        time.sleep(3)
        listCnt = in_driver.find_element(By.XPATH,'//*[@class="list-top"]/div[1]/span[1]/strong')
    except Exception as e:
        print(">> error")
        return "1"
    # else:
    #     time.sleep(3)

    #### listCnt = in_driver.find_element(By.XPATH,'//*[@id="mypage-list"]/div[1]/span[1]/strong')

    print(' Cnt list : {}'.format(listCnt.text))
    time.sleep(1)

    try:

        downBtn = in_driver.find_element(By.XPATH,'//*[@name="download"]/button')
        downBtn.click()
        time.sleep(2)
    except:
        print(" No Alert 1")
    else:
        proc_alert(in_driver)

    print(" >> Download 완료 ")
    time.sleep(1)
    print(" >> ----------------------------- ")

    return "0"


def readCsvFile():
    currIp = socket.gethostbyname(socket.gethostname())
    print('>> currIp : '+str(currIp))

    ins_cnt = 0
    del_sql = "delete from withbuy_tracking "
    print(">> del_sql : {}".format(del_sql))
    db_FS.execute(del_sql)
    today = date.today()

    if path.exists("C:\\Users\\allin\\Downloads\\"):
        filePath = "C:\\Users\\allin\\Downloads\\"
    elif path.exists("C:\\Users\\freeship\\Downloads\\"):
        filePath = "C:\\Users\\freeship\\Downloads\\"
    else:
        filePath = "C:\\Users\\user\\Downloads\\"

    findFileList = []
    findname = "download-" + str(today) + "*.txt"
    findCnt = 0
    for file_ea in os.listdir(filePath):
        if fnmatch.fnmatch(file_ea, findname):
            print(file_ea)
            findCnt = findCnt + 1
            findFileList.append(filePath + file_ea)

        if findCnt > 7:
            break

    print(findFileList)

    print("--------------------------------------------------")
    for file in findFileList:
        print(">> FileName : {}".format(file))
        print("--------------------------------------------------")
        lownum = 1
        with open(file, "r", encoding="utf-8", newline="") as f:
            line = ""
            line_tmp = ""
            for line in f:
                if lownum == 1:
                    print(" Title (SKIP) ")
                else:
                    if line.find("\r\n") == -1:
                        line_tmp = line_tmp + line

                    else:
                        line_tmp = line_tmp + line
                        split_data = line_tmp.split('\t',)
                        line_tmp = ""

                        if len(split_data) < 33:
                            print(">> 33개 항목 아님 확인필요 : {}".format(orderno))
                            procLogSet(gProc_no, "E", "0", " 위드바이: 33개 항목 아님 확인필요: "+str(orderno))
                            return "1"

                    col_low = 1
                    orderno = ""
                    amazon_orderno = ""
                    delivery_id = ""
                    delicode = ""
                    delivery_price = ""
                    weight_volume = ""
                    weight_pay = ""
                    weight_unit = ""
                    withbuyNo = ""
                    withbuyRcvName = ""
                    key_flg = "0"
                    for spEa in split_data:
                        spEa = str(spEa)
                        if col_low == 3:
                            #print(" 신청서상태 : " + str(spEa))
                            orderStatus = spEa.replace('"','')
                        elif col_low == 5:
                            #print(" 업체주문번호 : " + str(spEa))
                            orderno = spEa.replace('"','')                            
                        elif col_low == 4:
                            #print(" 신청서번호 : " + str(spEa))
                            withbuyNo = spEa.replace('"','')
                        elif col_low == 8:
                            #print(" 배송업체 : " + str(spEa))
                            delivery_id = spEa.replace('"','')
                        elif col_low == 9:
                            #print(" 송장번호 : " + str(spEa))
                            delicode = spEa.replace('"','')
                        elif col_low == 10:
                            #print("  수령인 : " + str(spEa))
                            withbuyRcvName = spEa.replace('"','')
                        elif col_low == 17:
                            #print(" 아이템수 : " + str(spEa))
                            item_ea = spEa.replace('"','')
                            if len(item_ea) > 4: item_ea = "0"
                        elif col_low == 18:
                            #print(" 총수량 : " + str(spEa))
                            goods_ea = spEa.replace('"','')
                            if len(goods_ea) > 4: goods_ea = "0"
                        elif col_low == 27:
                            #print(" 부피무게 : " + str(spEa)) 
                            weight_volume = spEa.replace('"','')
                            if len(weight_volume) > 20: weight_volume = ""
                        elif col_low == 28:
                            weight_pay = spEa.replace('"','')
                            #print(" 결제무게 : " + str(spEa)) 
                            if len(weight_pay) > 20: weight_pay = ""
                        elif col_low == 29:
                            weight_unit = spEa.replace('"','')
                            #print(" 무게단위 : " + str(spEa)) 
                            if len(weight_unit) > 20: weight_unit = ""
                        elif col_low == 30:
                            #print(" 결제금액 : " + str(spEa)) 
                            delivery_price = spEa.replace('"','')
                            if delivery_price.find('.') > -1:
                                delivery_price = func_user.getparse(str(delivery_price),'','.').strip()
                            if len(delivery_price) > 10: delivery_price = "0"
                        elif col_low == 33:
                            #print(" 오더넘버 : " + str(spEa)) 
                            spEa = spEa.replace('"','').replace('\r','').replace('\n','')
                            amazon_orderno = spEa
                            if str(spEa).find(',') > -1 and len(spEa) > 16:
                                key_flg = "1"
                                # amazon_orderno = func_user.getparse(str(spEa),'',',')

                        col_low = col_low + 1
                        
                    if str(amazon_orderno).strip() == str(orderno).strip():
                        print(">> match : {} | {}".format(amazon_orderno,orderno))
                        sql = "select ali_orderno from t_order as o inner join t_order_info as i on i.orderuid = o.uid where orderno = '{0}' ".format(orderno)
                        rowc = db_FS.selectone(sql)
                        if rowc:
                            amazon_orderno = rowc[0]
                            print(">> ali_orderno -> amazon_orderno charnge  : {} | {}".format(amazon_orderno,orderno))

                    if orderStatus not in ["발송완료","통관완료","배송완료","통관중","출고완료"]:
                        print(" >> 다른 신청서 상태(" + str(lownum-1) + ") {0} {1} {2} {3} {4}".format(orderStatus, orderno, amazon_orderno, delicode, delivery_id))
                        continue
                    print("===")
                    if str(orderno).strip() == "" or len(str(orderno).strip()) > 20:
                        print(">> No orderno 확인 필요 : {0} : {1} ".format(withbuyNo, amazon_orderno))
                        
                        DB_state = ""
                        DB_DeliveryNo = ""
                        sql = "select state, DeliveryNo from t_order as o inner join t_order_info as i on i.orderuid = o.uid inner join T_ORDER_DELIVERY as d on d.uid = i.uid where ali_orderno = '{0}' ".format(amazon_orderno)
                        rowc = db_FS.selectone(sql)
                        if rowc:                        
                            DB_state = rowc[0]
                            DB_DeliveryNo = rowc[1]
                            if DB_state != "201" and DB_state != "421":
                                print(">> orderno 확인 필요 (1) : {0} : {1} | DB_state : {2}".format(withbuyNo, amazon_orderno, DB_state))
                            else:
                                procLogSet(gProc_no, "E", "0", " No orderno 확인 필요 {0} : {1} | DB_state : {2} | DB_DeliveryNo: {3}".format(withbuyNo, amazon_orderno, DB_state, DB_DeliveryNo))
                            #return "1"
                        else:
                            sql = "select state, ali_orderno from t_order as o inner join t_order_info as i on i.orderuid = o.uid inner join T_ORDER_DELIVERY as d on d.uid = i.uid where DeliveryNo = '{0}' ".format(delicode)
                            rowc = db_FS.selectone(sql)
                            if rowc:                        
                                DB_state = rowc[0]
                                if DB_state != "201" and DB_state != "421":
                                    print(">> orderno 확인 필요 (2) : {0} : {1} | DB_state : {2}".format(withbuyNo, amazon_orderno, DB_state))
                                else:
                                    procLogSet(gProc_no, "E", "0", " No orderno 확인 필요 {0} : {1} | DB_state : {2} | DB_DeliveryNo: {3}".format(withbuyNo, amazon_orderno, DB_state, DB_DeliveryNo))
                            else:
                                procLogSet(gProc_no, "E", "0", " No orderno 확인 필요 {0} : {1} | 수령인 : {2}".format(withbuyNo, amazon_orderno, withbuyRcvName))
                    else:
                        if str(delicode).strip() == "":
                            print(">> No delicode 확인필요 : {}".format(orderno))
                            procLogSet(gProc_no, "E", "0", " No delicode 확인필요: "+str(orderno))
                            return "1"

                        delivery_company = ""
                        DeliveryUid = ""
                        DeliveryName = ""
                        if str(delivery_id).find("판토스") > -1:
                            delivery_company = "PANTOS"
                            DeliveryUid = "23"
                            DeliveryName = "LX판토스"
                        elif str(delivery_id).find("CJ-IPS") > -1:
                            delivery_company = "CJGLS"
                            DeliveryUid = "4"
                            DeliveryName = "CJ대한통운(국제택배)"
                        elif str(delivery_id).find("인트라스") > -1:
                            delivery_company = "EPOST"
                            DeliveryUid = "12"
                            DeliveryName = "우체국택배"
                        elif str(delivery_id).find("우체국") > -1:
                            delivery_company = "EPOST"
                            DeliveryUid = "12"
                            DeliveryName = "우체국택배"
                        elif str(delivery_id).find("CR로지텍") > -1:
                            delivery_company = "CRLX"
                            DeliveryUid = "11"
                            DeliveryName = "시알로지텍"
                        elif str(delivery_id).find("NARDA") > -1:
                            delivery_company = "PANTOS"
                            DeliveryUid = "23"
                            DeliveryName = "LX판토스"
                        elif str(delicode)[:2] == "60":
                            delivery_company = "EPOST"
                            DeliveryUid = "12"
                            DeliveryName = "우체국택배"
                        elif str(delivery_id).find("CJ대한통운") > -1:
                            delivery_company = "CJGLS"
                            DeliveryUid = "4"
                            DeliveryName = "CJ대한통운"

                        # elif str(delivery_id).find("FEDEX") > -1:
                        #     delivery_company = "FEDEX"
                        #     DeliveryUid = "6"
                        #     DeliveryName = "FEDEX"
                        # elif str(delivery_id).find("FedexIP") > -1:
                        #     delivery_company = "FEDEX"
                        #     DeliveryUid = "6"
                        #     DeliveryName = "FEDEX"
                        else:
                            print(" >> ( 기타택배 : " + str(lownum-1) + ") {0} {1} {2} {3}".format(orderno, amazon_orderno, delicode, delivery_id))
                            #input(">> Key : ")

                        if key_flg == "1":
                            selsql = "select amazon_orderno from withbuy_tracking where orderno = '{0}' ".format(orderno)
                            selRow = db_FS.selectone(selsql)
                            if selRow:
                                sql = "update withbuy_tracking set delivery_id='{0}', delicode='{1}',delivery_price='{2}', weight_volume='{3}', weight_pay='{4}', weight_unit='{5}', item_ea='{6}', goods_ea='{7}' where orderno = '{8}' ".format(delivery_id,delicode,delivery_price,weight_volume,weight_pay,weight_unit,item_ea,goods_ea,orderno)	
                            else:
                                sql = "insert into withbuy_tracking (delivery_id,delicode,delivery_price,orderno,amazon_orderno,weight_volume,weight_pay,weight_unit,item_ea,goods_ea, itemNo) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(delivery_id,delicode,delivery_price,orderno,amazon_orderno,weight_volume,weight_pay,weight_unit,item_ea,goods_ea, withbuyNo)	
                        else:
                            selsql = "select amazon_orderno from withbuy_tracking where orderno = '{0}' and amazon_orderno = '{1}'".format(orderno,amazon_orderno)
                            selRow = db_FS.selectone(selsql)
                            if selRow:
                                sql = "update withbuy_tracking set delivery_id='{0}', delicode='{1}',delivery_price='{2}', weight_volume='{3}', weight_pay='{4}', weight_unit='{5}', item_ea='{6}', goods_ea='{7}' where orderno = '{8}' and amazon_orderno = '{9}'".format(delivery_id,delicode,delivery_price,weight_volume,weight_pay,weight_unit,item_ea,goods_ea,orderno,amazon_orderno)	
                            else:
                                sql = "insert into withbuy_tracking (delivery_id,delicode,delivery_price,orderno,amazon_orderno,weight_volume,weight_pay,weight_unit,item_ea,goods_ea, itemNo) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(delivery_id,delicode,delivery_price,orderno,amazon_orderno,weight_volume,weight_pay,weight_unit,item_ea,goods_ea, withbuyNo)	
                        try:
                            db_FS.execute(sql)
                        except Exception as e:
                            print(">> Exception sql : {}".format(sql))
                            print(">> ")
                        ins_cnt = ins_cnt + 1
                        print(" >> (" + str(lownum-1) + ") {0} {1} {2} {3}".format(orderno, amazon_orderno, delicode, delivery_id))

                lownum = lownum + 1

        repFileName = file.replace('account2_','back_account_')
        os.rename(file, repFileName)
        print(">> backup - filename change ")

    f.close() 

    return str(ins_cnt)

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)
# 
    return "0"

if __name__ == '__main__':

    upd_cnt = 0
    gProc_no = "DEV_SEL_WITHBUY_GET"
    ip = socket.gethostbyname(socket.gethostname())

    print('>> withbuy Delivery Get Proc (위드바이 송장 번호 --> 프리쉽에 송장 입력 처리) ')
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))
    procLogSet(gProc_no, "S", "0", "위드바이 송장(new) Start : " + str(ip))

    set_browser = "chrome"
    ip = socket.gethostbyname(socket.gethostname())
    db_con = DBmodule_FR.Database('freeship')

    pgSite = 'https://www.globalwithbuy.com/'
    try:
        # browser = func_user.connectDriverNew(pgSite,'S')
        proc, browser = func_user.connectSubProcess()
        # service = Service('C:/Users/allin/Downloads/chromedriver-win64/chromedriver.exe')
        # browser = webdriver.Chrome(service = service)
    except Exception as e:
        try:
            browser = func_user.connectDriverOld(pgSite,'S')
        except Exception as e:
            print('예외가 발생 (종료) : ', e)
            procLogSet(gProc_no, "E", "0", "connectDriver 접속 에러 (종료)")
            time.sleep(20)
            print('>> time.sleep(20) ')
            os._exit(1)
    else:
        print('connectDriver 연결 OK')
    
    # browser.set_window_size(1300, 1000)
    # browser.implicitly_wait(3)

    now_url = "https://www.globalwithbuy.com/agency/order"
    browser.get(now_url)
    browser.maximize_window()
    #result = browser.page_source

    time.sleep(2)

    if str(browser.page_source).find('1stplatform님') == -1:
        # 로그인 처리
        loginProc(browser)
    else:
        print(">> Login Ok ")
    time.sleep(1)

    # CSV 파일 다운로드 처리
    rtnFlg = downloadProc(browser)
    if rtnFlg == "1":
        # CSV 파일 다운로드 Error
        print('>> CSV 파일 다운로드 Error (Exit) ')
        procLogSet(gProc_no, "E", "0", "(CSV 파일 다운로드 Error ) ")
        os._exit(1)
    else:
        print(" >> CSV 파일 다운로드 완료 ")

    time.sleep(1)

    rtnFlg = ""
    rtnFlg = readCsvFile()
    print('>> 파일 Read --> DB Insert OK ')
    procLogSet(gProc_no, "F", rtnFlg, " 위드바이 송장번호 가져오기 : " + str(rtnFlg))

    time.sleep(1)

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/withbuy_tracking_proc_v3.asp?mode=del"
    #run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/withbuy_tracking_proc_v3_test2.asp?mode=del"
    print(" >> Next Proc 실행 (위드바이) 프리쉽 송장처리(new) : withbuy_tracking_proc_v3.asp?mode=del : " + str(run_url))

    browser.get(run_url)
    time.sleep(5)
    print(" time.sleep(5) ")

    procLogSet(gProc_no, "P", "0", " (위드바이) 프리쉽 송장처리(new) 완료 " + str(run_url))

    print('\n [--- main end ---] ' + str(datetime.datetime.now()))

    db_FS.close()
    time.sleep(5)
    print(" time.sleep(5) ")
    browser.quit()
    print("proc1 = ", proc.pid)
    subprocess.Popen.kill(proc)
    os._exit(0)