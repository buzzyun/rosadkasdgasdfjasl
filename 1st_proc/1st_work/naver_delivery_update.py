import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import pyautogui
import random
import socket
import requests
import json
import os
import datetime
import func_user
import func
import sys
import DBmodule_FR

global ver
ver = "1.05"
print(">> ver : {}".format(ver))
global updCnt
global changedCnt
global skipCnt
global check_cnt

def elem_clear(elem):
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.3)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.3)

def getNaverDelieveyNameNew(db_FS, strName):
    naver_Name = ""
    sql = "select naver_Name from T_DELIVERY where Name = '{}'".format(str(strName).strip())
    row = db_FS.selectone(sql)
    if row:
        naver_Name = row[0]
    else:
        print(">> 매칭  네이버 택배사명 없음. ")
    return str(naver_Name).strip()


def getNaverDelieveyName(strName):
    rtnName = ""
    strName = str(strName).strip()
    if strName == "CJ대한통운":
        rtnName = "CJGLS"
    elif strName == "롯데택배":
        rtnName = "HYUNDAI"
    elif strName == "한진택배":
        rtnName = "HANJIN"
    elif strName == "로젠택배":
        rtnName = "KGB"
    elif strName == "우체국택배":
        rtnName = "EPOST"
    elif strName == "DHL":
        rtnName = "DHL"
    elif strName == "CJ대한통운(국제택배)":
        rtnName = "KOREXG"
    elif strName == "국제등기":
        rtnName = "EMS"
    elif strName == "FEDEX":
        rtnName = "FEDEX"
    elif strName == "우진인터로지스":
        rtnName = "WOOJIN"
    elif strName == "UFO로지스":
        rtnName = "LOGISPARTNER"
    elif strName == "UPS":
        rtnName = "UPS"
    elif strName == "USPS":
        rtnName = "USPS"
    elif strName == "TNT":
        rtnName = "TNT"       
    elif strName == "YUNDAEXPRES":
        rtnName = "YUNDA"
    elif strName == "경동택배":
        rtnName = "KDEXP"
    elif strName == "대신택배":
        rtnName = "DAESIN"
    elif strName == "범한판토스" or strName == "LX판토스":
        rtnName = "PANTOS"
    elif strName == "시알로지텍":
        rtnName = "CRLX"
    elif strName == "기타택배":
        rtnName = "CH1"
    elif strName == "일반우편":
        rtnName = "GENERALPOST"
    elif strName == "EMS":
        rtnName = "EMS"

    return rtnName

def dbUpdateFlg(db_FS, Infouid, memo):
    if memo != "":
        uSql = "update freeship_tracking_check set proc_state = '2', memo = '" +str(memo)+ "', memodate = getdate() where InfoUid = '{}'".format(Infouid)
    else:
        uSql = "update freeship_tracking_check set proc_state = '1' where InfoUid = '{}'".format(Infouid)
    print(">> uSql : {}".format(uSql))
    db_FS.execute(uSql)

def proc_alert(in_driver):
    try:
        da = Alert(in_driver)
        da.accept()
        print(da.text)
        time.sleep(1)
    except:
        print(" No Alert ")
        return "1"

    return "0"

def procLogSet(db_FS, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

def procSearchBtn(mainDriver):
    #  검색버튼 클릭
    if mainDriver.find_element(By.CSS_SELECTOR,'#__app_root__ > div > div.napy_sub_content > div:nth-child(2) > div.button_area > button'):
        textStr3 = mainDriver.find_element(By.CSS_SELECTOR,'#__app_root__ > div > div.napy_sub_content > div:nth-child(2) > div.button_area > button')
        if str(textStr3.text).strip() == "검색":
            print(">> 검색버튼 클릭 ")
            textStr3.click()

    time.sleep(1)

def getPayDeliveryNo(mainDriver):
    # 현재 상품주문번호 확인
    currNo = mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-table-container > table > tbody > tr > td:nth-child(2) > div > a')

    return str(currNo.text).strip()

def procDelieveyNoUpdate(db_FS, Ouid, Infouid, pay_orderno, OrderNo, DeliveryName, DeliveryNo):
    global updCnt
    global skipCnt
    global changedCnt
    global check_cnt
    time.sleep(0.5)
    rtnFlg = ""
    delieveyNo = DeliveryNo.strip()
    delieveyNaverValue = getNaverDelieveyNameNew(db_FS, DeliveryName)
    print(">> delieveyNo : {} | delieveyNaverValue : {} | DeliveryName : {} | delieveyNaverValue : {}".format(delieveyNo, delieveyNaverValue,DeliveryName, delieveyNaverValue))

    if delieveyNaverValue == "":
        print(">> 송장번호 변경 불가 상태 (매칭 네이버 택배사명 없음) : {}".format(DeliveryName))
        # DB Update proc_state = 1, memo 
        dbUpdateFlg(db_FS, Infouid, "네이버페이 송장번호 변경 불가상태")
        skipCnt = skipCnt + 1
        time.sleep(0.5)
        return "0"

    # 상품주문번호 입력
    if mainDriver.find_element(By.CSS_SELECTOR,'div.npay_board_area > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2) > input'):
        elem2= mainDriver.find_element(By.CSS_SELECTOR,'div.npay_board_area > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2) > input')
        elem_clear(elem2)
        time.sleep(0.5)
        elem2.send_keys(pay_orderno)
        print(">> 상품주문번호 입력 : {} ".format(pay_orderno))
    time.sleep(0.5)

    #  검색버튼 클릭
    procSearchBtn(mainDriver)
    gridsource = func.getparse(str(mainDriver.page_source),'class="tui-grid-table"','class="grid_bottom_button"')
    if str(gridsource).find('data-row-key="0"') == -1:
        print(">> 현재 상품주문번호 없음 ")
        mainDriver.get_screenshot_as_file('C:/project/log/no_search_'+str(pay_orderno)+'.png')
        dbUpdateFlg(db_FS, Infouid, "네이버페이 송장번호 변경 검색안됨")
        time.sleep(1)
        skipCnt = skipCnt + 1
        time.sleep(0.5)
        return "0"

    # 현재 상품주문번호 확인
    currNaverOdrNo = getPayDeliveryNo(mainDriver)
    print(">> currNaverOdrNo {} :".format(currNaverOdrNo) )
    if str(currNaverOdrNo).strip() == pay_orderno:
        print(">> 상품주문번호 확인 OK ")
    else:
        print(">> 상품주문번호 확인 불가")
        return "0"

    if mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-table-container > table > tbody > tr > td:nth-child(3) > div > span.tui-grid-content-input'):
        naver_state = mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-rside-area > div.tui-grid-body-area > div > div.tui-grid-table-container > table > tbody > tr > td:nth-child(10)')
        if str(naver_state.text).find("배송중") > -1:
            print(">> 네이버 배송중 상태 ")
        else:
            print(">> 송장번호 변경불가 상태({})".format(str(naver_state.text)))
            if str(naver_state.text).find('배송완료') > -1 or str(naver_state.text).find('구매확정') > -1:
                print(">> 네이버 배송완료 상태 : {}".format(str(naver_state.text)))
                dbUpdateFlg(db_FS, Infouid, "")
                skipCnt = skipCnt + 1
                time.sleep(0.5)
                return "0"

            # DB Update proc_state = 1, memo 
            dbUpdateFlg(db_FS, Infouid, "네이버페이 ("+str(naver_state.text)+") 송장번호 변경불가")
            skipCnt = skipCnt + 1
            time.sleep(0.5)
            return "0"

        checkElem = mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-table-container > table > tbody > tr > td:nth-child(3) > div > span.tui-grid-content-input')    
        if str(checkElem.text).find("택배사명") == -1:
            print(">> 송장번호 변경 불가 상태 : {}".format(checkElem.text))
            # DB Update proc_state = 1, memo 
            dbUpdateFlg(db_FS, Infouid, "네이버페이 송장번호 변경 불가상태")
            skipCnt = skipCnt + 1
            time.sleep(0.5)
            return "0"

    ### 송장번호 확인
    if mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text'):
        elem = mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text')       
        oldDelieveyNo = elem.get_attribute('value')
        if oldDelieveyNo == delieveyNo:
            selDeliveryNmae = func.getparse(str(mainDriver.page_source),'<option value="">택배사명 선택','</select>')
            selDeliveryNmae = func.getparse(selDeliveryNmae,'selected="">','<').strip()
            if str(DeliveryName).strip() == selDeliveryNmae:
                print(">> 이미 변경된 송장번호가 있음 (SKIP) ")
                upSql = "update t_order_delivery set naver_trackno_update = getdate(), naver_track_flg = '1' where Uid = '" +str(Infouid)+ "'"
                print(">> upSql : {}".format(upSql))
                db_FS.execute(upSql)

                # DB Update proc_state = 1
                dbUpdateFlg(db_FS, Infouid, "")
                changedCnt = changedCnt + 1
                time.sleep(0.5)
                return "0"
        elif oldDelieveyNo == "": # 발송처리 안된주문 ( 송장변경 x --> 발송 처리 필요한건 Skip 처리 (예림씨 확인했음) )
            # mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-body-area > div > div.tui-grid-table-container > table > tbody > tr > td:nth-child(2) > div > span.tui-grid-content-input > select > option:nth-child(2)').click()
            # time.sleep(0.5)
            # elem = mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-body-area > div > div.tui-grid-table-container > table > tbody > tr > td:nth-child(4) > div > span.tui-grid-content-input > input')
            print(">> 송장번호 변경 불가 상태 (발송 처리 필요한 주문건) : {}".format(OrderNo))
            # DB Update proc_state = 1, memo 
            dbUpdateFlg(db_FS, Infouid, "네이버페이 송장번호 변경 불가상태")
            skipCnt = skipCnt + 1
            time.sleep(0.5)
            return "0"
        else:
            elem_clear(elem)
            elem.send_keys(delieveyNo)
    time.sleep(0.5)

    ### 택배사명 리스트
    dlist = mainDriver.find_elements(By.CSS_SELECTOR,'div > span.tui-grid-content-input')[1]
    deliveryName_list = dlist.find_element(By.TAG_NAME,'select').find_elements(By.TAG_NAME,'option')
    if deliveryName_list:
        comments_list = {}
        flg = "0"
        for num, comment in enumerate(deliveryName_list):
            ea_item = comment.get_attribute('value')
            #print(" {} :".format(ea_item) )
            comments_list[num] = comment

            if ea_item == delieveyNaverValue:
                print(">> 택배 선택 OK : {}".format(delieveyNaverValue) )
                comments_list[num].click()
                print(">> 택배 Click ")
                flg = "1"
                break

        time.sleep(0.5)
        if flg == "1":
            print(">> 택배사 선택값 확인 OK")
            currDelieveyNo = mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text').get_attribute('value')
            if currDelieveyNo == delieveyNo:
                #time.sleep(0.5)
                mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text').click()
                print(">> 송장 입력값 확인 OK ")
                time.sleep(0.5)

                # 선택 체크박스 클릭
                if mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-table-container > table > tbody > tr > td.tui-grid-cell-row-head.tui-grid-cell > div'):
                    mainDriver.find_element(By.CSS_SELECTOR,'div.tui-grid-table-container > table > tbody > tr > td.tui-grid-cell-row-head.tui-grid-cell > div').click()
                time.sleep(0.5)

                try:
                    # 송장수정 버튼 클릭
                    mainDriver.find_element(By.CSS_SELECTOR,'div.npay_board_area > table > tbody > tr:nth-child(2) > td > button:nth-child(5)').click()
                    time.sleep(1)
                    print(">> Browser Count : {}".format(len(mainDriver.window_handles)))
                    # alert 확인 클릭
                    da = Alert(mainDriver)
                    #print(da.text)
                    time.sleep(0.5)
                    da.accept()
                    print(">> Alert accept()")
                    time.sleep(0.5)

                    print(pyautogui.position())
                    ## pyautogui.moveTo(470,150)
                    ## pyautogui.moveTo(random.uniform(472,474),random.uniform(150,152))
                    x = random.uniform(472,474)
                    y = random.uniform(150,152)
                    print(">> x = : {}, y : {}".format(x, y))
                    pyautogui.moveTo(random.uniform(470,475), random.uniform(148,154))
                    pyautogui.dragTo(x, y, duration=0.5)
                    # time.sleep(0.5)
                    print(">> Popup 확인 click (pyautogui)")
                    pyautogui.click(x, y, duration=0.5)#
                    # pyautogui.click()
                    # pyautogui.doubleClick()
                except:
                    print(">> No Alert ")
                    rtnFlg = "E"
                else:
                    time.sleep(1)
                    main = mainDriver.window_handles
                    print(">> Browser Count : {}".format(len(main)))
                    last_tab = mainDriver.window_handles[len(main) - 1]
                    if str(len(main)) != "1":
                        check_cnt = check_cnt + 1 
                        print(">> 송장번호 변경 불가 상태 확인필요 : {}".format(currNaverOdrNo))
                        # DB Update proc_state = 1, memo 
                        dbUpdateFlg(db_FS, Infouid, "네이버페이 송장번호 변경 불가상태")
                        skipCnt = skipCnt + 1

                        for handle in main:
                            if handle != last_tab:
                                mainDriver.switch_to.window(window_name=last_tab)
                                mainDriver.close()
                                mainDriver.switch_to.window(window_name=handle)
                        print(">> Browser Close : {}".format(len(mainDriver.window_handles)))

                        if check_cnt > 4:
                            procLogSet(db_FS,"naver_delivery_update", "E", "0", "네이버 페이 송장변경 송장번호 변경 불가 상태 연속 3개 이상 : " + str(currIp))
                            print(">> 송장번호 변경 불가 상태 연속 3개 이상 확인필요 : {}".format(currNaverOdrNo))
                            mainDriver.get_screenshot_as_file('C:/project/log/E01_count_'+str(check_cnt)+'_over_'+str(currNaverOdrNo)+'.png')
                            return "E"
                    else:
                        check_cnt = 0

                    time.sleep(0.5)
                    #  검색버튼 클릭
                    procSearchBtn(mainDriver)

                    # 현재 상품주문번호 확인
                    currNaverOdrNo = getPayDeliveryNo(mainDriver)
                    print(">> currNaverOdrNo {} :".format(currNaverOdrNo) )
                    if str(currNaverOdrNo).strip() == pay_orderno:
                        print(">> 상품주문번호 확인 OK : {}".format(str(currNaverOdrNo)))
                    else:
                        print(">> 상품주문번호 확인 불가")
                        return "0"

                    ### 송장번호 확인
                    # if mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text'):
                    #     elem = mainDriver.find_element(By.CSS_SELECTOR,'input.tui-grid-content-text')        
                    editDelieveyNo = func.getparse(str(mainDriver.page_source),'class="tui-grid-table"','class="grid_bottom_button"')
                    editDelieveyNo = func.getparse(str(editDelieveyNo),'class="tui-grid-content-text"','class="grid_bottom_button"')
                    editDelieveyNo = func.getparse(str(editDelieveyNo),'value="','"').strip()
                    if str(editDelieveyNo) == str(delieveyNo):
                        print(">> 송장번호 변경 OK : {}".format(editDelieveyNo))
                        upSql = "update t_order_delivery set naver_trackno_update = getdate(), naver_track_flg = '0' where Uid = '" +str(Infouid)+ "'"
                        print(">> upSql : {}".format(upSql))
                        db_FS.execute(upSql)

                        # DB Update proc_state = 1
                        dbUpdateFlg(db_FS, Infouid, "")
                        updCnt = updCnt + 1
                        #time.sleep(0.5)
                        rtnFlg = "1"
                    else:
                        print(">> 송장번호 변경 확인안됨 : {} | {}".format(editDelieveyNo, delieveyNo))
                        rtnFlg = "0"

        else:
            rtnFlg = "0"

    return rtnFlg

def searchBtn(mainDriver):
    time.sleep(2)
    nowurl = 'https://admin.pay.naver.com/o/v3/n/sale/delivery'
    mainDriver.get(nowurl)
    time.sleep(3)
    result = mainDriver.page_source
    elem1 = func.getparse(str(result),'>조회기간<','</div>')
    elem1 = func.getparse(elem1,'<div class="','"')
    
    mainDriver.find_element(By.CSS_SELECTOR,'div.'+str(elem1)+' > div:nth-child(2) > div > ul > li:nth-child(4) > button')

    elem2 = func.getparse(str(result),'>상세조건<','</div>')
    elem2 = func.getparse(elem2,'<div ','')
    elem2 = func.getparse(elem2,'<div class="','"')

    # 3개월
    if mainDriver.find_element(By.CSS_SELECTOR,'div.'+str(elem1)+' > div:nth-child(2) > div > ul > li:nth-child(4) > button'):
        textStr1 = mainDriver.find_element(By.CSS_SELECTOR,'div.'+str(elem1)+' > div:nth-child(2) > div > ul > li:nth-child(4) > button')
        if str(textStr1.text).strip() == "3개월":
            textStr1.click()
    time.sleep(0.5)

    # 상품주문번호
    if mainDriver.find_element(By.CSS_SELECTOR,'div.npay_board_area > table > tbody > tr:nth-child(2) > td > div > div.'+str(elem2)+' > select > option:nth-child(7)'):
        textStr2 = mainDriver.find_element(By.CSS_SELECTOR,'div.npay_board_area > table > tbody > tr:nth-child(2) > td > div > div.'+str(elem2)+' > select > option:nth-child(7)')
        if str(textStr2.text).strip() == "상품주문번호":
            textStr2.click()
    time.sleep(0.5)

def get_new_token_v1():
    auth_server_url = "https://web1.dktechinmsg.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(inOrderNo, inIuid, msg, phone):
    token = get_new_token_v1()
    test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    template_code = "norder1"
    sender_no = "18005086"
    cid_key = "cid_key"
    phone = "01032542652" #예림

    if phone != "":
        print(">> ")
        ordername = "고객팀"
        orderno = "M0000"
        phone_number = str(phone).replace('-','').strip()
        message = msg
        sms_message = message
        message_type = "SM"
        sms_type = "SM"

        param_date = {'client_id': 'C000000440','sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17','message_type': message_type,'message': message
        ,'cid': cid_key,'phone_number': phone_number,'template_code': template_code,'sender_no': sender_no,'sms_message':sms_message, 'sms_type':sms_type,'title': '송장변경관련 안내'}

        jsonString = json.dumps(param_date, indent=4)
        api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
        if api_call_response.status_code !=200:
            print(">> error ")
        else:
            result = json.loads(api_call_response.text)
            rtn_uid =  result['uid']
            rtn_status_code =  result['kko_status_code']
            rtn_code = result['code']
            rtn_message = result['message']
            print(">> rtn_status_code : {} | rtn_message : {}".format(rtn_status_code, rtn_message))
            if rtn_code == "API_200" or rtn_status_code == "0000": 
                result_code = "200"
                result_message = "OK"
            else:
                result_code = rtn_code
                result_message = rtn_message

            iSql = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent, orderno) values\
                ('{}','{}','{}','{}','{}',getdate(),'adminauto','{}','{}','{}')".format(ordername,phone_number,rtn_uid,result_code,result_message,template_code,message,orderno)
            print(">> iSql : {} ".format(iSql))
            db_FS.execute(iSql)

def screen_check(mainDriver):
    time.sleep(1)
    try:
        main = mainDriver.window_handles
        print(">> Browser Count : {}".format(len(main)))
        last_tab = mainDriver.window_handles[len(main) - 1]
        if str(len(main)) != "1":
            for handle in main:
                if handle != last_tab:
                    mainDriver.switch_to.window(window_name=last_tab)
                    mainDriver.close()
                    mainDriver.switch_to.window(window_name=handle)
            print(">> Browser Close : {}".format(len(mainDriver.window_handles)))

    except Exception as e:
        print('>> Popup Close Exception ')

    time.sleep(0.5)


if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> 작업 시작 (네이버 페이 송장변경 처리) :' + str(now))

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

    rowcnt = 0
    check_cnt = 0
    db_FS = DBmodule_FR.Database('freeship')
    procLogSet(db_FS,"naver_delivery_update", "S", "0", "네이버 페이 송장변경 처리 : " + str(currIp))

    sql = "select c.ouid, c.InfoUid, c.pay_orderno, t.OrderNo, d.DeliveryName, d.DeliveryNo, isnull(d.after_trackno,''), isnull(d.after_DeliveryName,'') from freeship_tracking_check as c inner join t_order_info as i on i.uid = c.InfoUid inner join T_ORDER_DELIVERY as d on d.uid = i.uid inner join t_order as t on t.uid = i.OrderUid where t.state in ('201','301','421') and c.reason = 'mismatchtracking' and c.proc_state is null and t.payway = 'NaverPay' order by c.procdate"
    procRows = db_FS.select(sql)
    if not procRows:
        print(">> 송장 변경 대상이 없습니다. (Exit) ")
        procLogSet(db_FS,"naver_delivery_update", "F", "0", "네이버 페이 송장변경 대상 없음")
        db_FS.close()
        os._exit(0)
    time.sleep(1)

    now_url = 'https://admin.pay.naver.com'
    # mainDriver = func_user.connectDriverNew('https://admin.pay.naver.com','')
    try:
        print(">> connectDriverNew set ")
        mainDriver = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        mainDriver = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    mainDriver.set_window_size(1400, 1000)

    print('connectDriver 연결 OK')
    mainDriver.implicitly_wait(3)
    #now_url = "https://nid.naver.com/nidlogin.login?url=https://admin.pay.naver.com/nid/check"
    now_url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fadmin.pay.naver.com%2Fnid%2Fcheck&locale=ko_KR&svctype=1"
    mainDriver.get(now_url)
    time.sleep(2)

    currIp = socket.gethostbyname(socket.gethostname())
    print('>> currIp : '+str(currIp))
    if currIp == "222.104.189.18":
        loginId = 'kbw4798'
        loginPw = 'bw007583@1011'
    else:
        loginId = 'kbw4798'
        loginPw = 'bw007583@1011'

    elem11 = mainDriver.find_element(By.XPATH,'//*[@id="id"]')
    elem_clear(elem11)
    elem11.send_keys(loginId)
    time.sleep(0.5)
    elem22 = mainDriver.find_element(By.XPATH,'//*[@id="pw"]')
    elem_clear(elem22)
    elem22.send_keys(loginPw)
    time.sleep(0.5)
    mainDriver.find_element(By.XPATH,'//*[@id="log.login"]').click()
    time.sleep(2)

    if str(mainDriver.current_url).find('managementlist') > -1:
        print(">> 가맹점정보 선택하기 ")
        time.sleep(1)
        chkBtn = mainDriver.find_element(By.CSS_SELECTOR, "#store_item_freeship > label > span.name_area")
        if chkBtn:
            chkBtn.click()
            mainDriver.find_element(By.CSS_SELECTOR,"#btnConfirm").click()
            time.sleep(3)

    if str(mainDriver.current_url).find('admin.pay.naver.com/home') > -1:
        print(">> 로그인 OK ")
        time.sleep(1)
    else:
        print(">> 로그인 불가 ")
        sms_send_kakao_proc_new("", "", "[확인요청] 송장변경관련 로그인 확인요청 : " + str(datetime.datetime.now())[:19], "") # 담당자에게 알림톡 전송
        time.sleep(1)
        input(">> 로그인 처리후 (네이버페이센터홈) 아무키나 눌러주세요 :")
        time.sleep(2)

    if str(mainDriver.current_url).find('admin.pay.naver.com/home') == -1:
        print(">> 로그인 불가 exit ")
        time.sleep(2)
        procLogSet(db_FS,"naver_delivery_update", "E", "0", "네이버 페이 송장변경 로그인 불가")
        mainDriver.quit()
        os._exit(1)

    # 팝업 공지 확인후 닫기
    screen_check(mainDriver)
    time.sleep(5)
    # 팝업 공지 확인후 닫기
    screen_check(mainDriver)

    allCnt = 0
    allCnt = len(procRows)
    endCnt = allCnt
    if allCnt > 300:
        endCnt = 300
    # if allCnt > 50:
    #     print(">> (네이버페이센터홈) 처리 시작 ")
    #     endCnt = input(">> 총 (" +str(allCnt)+ ")개 입니다. 수행할 갯수를 입력하세요 (숫자만입력가능) : ")
    #     if endCnt == "":
    #         endCnt = print(">> 수행할 갯수가 입력되지 않았습니다. 수행할 갯수를 입력하세요 (숫자만입력가능) : ")
    #     if endCnt == "":
    #         print(">> 수행할 갯수가 입력되지 않았습니다. (Exit) ")
    #         db_FS.close()
    #         mainDriver.quite()
    #         os._exit(0)   
    #     if int(endCnt) > allCnt:
    #         endCnt = allCnt
    # else:
    #     input(">> (네이버페이센터홈) 처리를 시작 합니다. 아무 숫자나 입려후 엔터키를 눌러주세요 : ")

    # 검색조건 입력
    searchBtn(mainDriver)
    updCnt = 0
    skipCnt = 0
    changedCnt = 0
    for row in procRows:
        rowcnt = rowcnt + 1
        Ouid = row[0]
        Infoid = row[1]
        pay_orderno = row[2]
        OrderNo = row[3]
        DeliveryName = row[4]
        DeliveryNo = row[5]
        after_trackno = row[6]
        after_DeliveryName = row[7]

        proc_DeliveryNo = DeliveryNo
        proc_DeliveryName = DeliveryName
        if after_trackno != "" and after_DeliveryName != "": # delivername_error 배송건중 CNG~ / LP~ 송장이 변경된경우 after_trackno 송장반영
            proc_DeliveryNo = after_trackno
            proc_DeliveryName = after_DeliveryName
        print("\n--------------------------------")
        print(">> [{}] {} ({}) | {} | {} | {} -- {} | {}".format(rowcnt, OrderNo, Infoid, pay_orderno, DeliveryName, DeliveryNo, after_trackno, after_DeliveryName))
        time.sleep(0.5)
        if DeliveryNo is None:
            pass
        else:
            # 팝업 공지 확인후 닫기
            screen_check(mainDriver)
            procRtn = procDelieveyNoUpdate(db_FS, Ouid, Infoid, pay_orderno, OrderNo, proc_DeliveryName, proc_DeliveryNo)
            if procRtn == "":
                print(">> return 값 확인불가 ")
                mainDriver.get_screenshot_as_file('C:/project/log/E00_return_null_'+str(check_cnt)+'_'+str(pay_orderno)+'.png')
                procLogSet(db_FS,"naver_delivery_update", "E", "0", "네이버 페이 송장변경 return 값 확인불가 : udpate({}) | skip({}) | changedCnt({}) ".format(updCnt,skipCnt,changedCnt))
                break
            if procRtn == "E":
                print(">> return 값 확인불가 (E) ")
                procLogSet(db_FS,"naver_delivery_update", "E", "0", "네이버 페이 송장변경 return 값 확인불가 (E): udpate({}) | skip({}) | changedCnt({}) ".format(updCnt,skipCnt,changedCnt))
                break

            if rowcnt >= int(endCnt):
                print(">> 수행할 갯수 End : {} ".format(rowcnt))
                procLogSet(db_FS,"naver_delivery_update", "F", "0", "네이버 페이 송장변경 (수행건수:{}) 완료 : udpate({}) | skip({}) | changedCnt({}) ".format(rowcnt, updCnt,skipCnt,changedCnt))
                break

    time.sleep(2)
    now = datetime.datetime.now()
    print('>> 작업 완료 (네이버 페이 송장변경 처리) :' + str(now))
    procLogSet(db_FS,"naver_delivery_update", "F", "0", "네이버 페이 송장변경 처리완료 : udpate({}) | skip({}) | changedCnt({}) ".format(updCnt,skipCnt,changedCnt))
    db_FS.close()
    mainDriver.quit()
    os._exit(0)


























