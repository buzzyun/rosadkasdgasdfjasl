import os
import time
import socket
import datetime
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import subprocess
import DBmodule_FR
import func_user

# load .env
load_dotenv()

global ver
ver = "1.03"
print(">> ver : {}".format(ver))

def proc_trackno(browser, tracking_china):
    try:
        browser.find_element(By.CSS_SELECTOR,'div > a.btn.btn-secondary.btn-xs.btn-block.event-common-click-dialog').click()
        time.sleep(1)
        try:
            browser.find_element(By.CSS_SELECTOR,'#agency-tracking-number-modify > div > form > div.box > div:nth-child(3) > label').click()
            browser.find_element(By.CSS_SELECTOR,'#agency-tracking-number-modify > div > form > div.box > div > input').send_keys(tracking_china)
        except:
            browser.find_element(By.CSS_SELECTOR,'#agency-tracking-number-modify > div > form > div.box > div > input').send_keys(tracking_china)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR,'#agency-tracking-number-modify > div > form > p > button').click()
        try:
            # alert 확인 클릭
            da = Alert(browser)
            time.sleep(0.5)
            if str(da.text).find('완료') > -1:
                check_flg = "0"
                print(da.text)
            da.accept()
            time.sleep(1)
        except:
            print(" No Alert ")
    except:
        print(" 트래킹 번호 입력 처리 except ")

def procLogTracking(in_ali_orderno, tmp_delivery_no):

    Reason = 'delivername_error'
    sql_s = "select OrderNo from freeship_tracking_check where ali_orderno = '{}' and Reason = '{}'".format(in_ali_orderno, Reason)
    rowTk = db_con.selectone(sql_s)
    if not rowTk:
        sql_s2 = " select RegDate, ali_id, PAYWAY, o.naver_pay_product_code, o.uid, i.uid, OrderNo from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where ali_orderno = '{}'".format(in_ali_orderno)
        rowOrd = db_con.selectone(sql_s2)
        if rowOrd:
            RegDate = rowOrd[0]
            ali_id = rowOrd[1]
            PAYWAY = rowOrd[2]
            Pay_orderno = rowOrd[3]
            Ouid = rowOrd[4]
            Iuid = rowOrd[5]
            OrderNo = rowOrd[6]

            sql_i = "insert into freeship_tracking_check  ( ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, InfoUid, tmp_delivery_no ) "
            sql_i = sql_i + " values ( getdate(), '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                RegDate, OrderNo, in_ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, Iuid, tmp_delivery_no)
            print(" delivername_error (sql): {}".format(sql_i))
            db_con.execute(sql_i)

    return "0"


def elem_clear(browser, elem):

    time.sleep(0.2)
    elem.send_keys(Keys.CONTROL + "a")
    time.sleep(0.2)
    elem.send_keys(Keys.DELETE)
    time.sleep(0.2)
    elem.clear()
    time.sleep(0.5)

    return

def proc_put(db_con, browser):
    global upd_cnt

    #주문 아이디별 트래킹 번호 미입력 리스트 검색
    sql = "select I.ali_orderno, O.orderno, D.tracking_china, D.tracking_china_date, D.uid, O.state, O.RegDate, O.ChkDate, O.Uid , O.naver_pay_product_code, O.naver_pay_cancel "
    sql = sql + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid"
    sql = sql + " where I.ali_chk = '0' and D.DeliveryNo is null and D.DeliveryDate is null and O.state in ('201','301','421') "
    sql = sql + " and tracking_china is not null and tracking_china_state is null AND I.ali_id in ('red','red2') and amazon_price_date > '2023-07-04 00:00:00' "
    print("sql : " + str(sql))

    rows = db_con.select(sql)
    low = 0
    lenRows = ""
    if rows:
        lenRows = str(len(rows))
        print(">> 리스트 Count : " + str(lenRows))
        # func_user.procLogSet(db_con,gProc_no, "P", "0", '[' +str(in_aliId)+ '] 주문 트래킹 번호 미입력 리스트 : '+str(len(rows)))

        for ea_row in rows:
            low = low + 1
            itemResult = ""
            itemtracking = ""
            D_ali_orderno = ""
            D_tracking_china = ""
            D_ali_orderno = str(ea_row[0]).strip()
            D_orderno = ea_row[1]
            D_tracking_china = str(ea_row[2]).strip()
            D_tracking_china_date = ea_row[3]
            D_infoUid = ea_row[4]

            print("[ " + str(low) + " ] " + str(D_ali_orderno) + " (" + str(D_orderno) + ") | " + str(D_tracking_china) + " | " + str(D_tracking_china_date) + " | " + str(D_infoUid))

            proc_url = 'https://goport.kr/agency/order?status=AAAA&s=orderNo&k=' +str(D_ali_orderno)+ '&orderType=&customsInfoValid=&deliveryLock=&date1=&date2='
            browser.get(proc_url)
            time.sleep(2)
            source = str(browser.page_source)
            itemResult = func_user.getparse(source, 'class="table-list order-item-list"','</table>')
            if itemResult == "" or itemResult.find("데이타가 없습니다") > -1:
                print(">> [{}] 신청서 없음 : {}".format(D_ali_orderno, D_tracking_china))
            elif D_tracking_china == "":
                print(">> [{}] 트래킹 번호 없음 (확인필요) : {}".format(D_ali_orderno, D_tracking_china))
            else:
                print(">> ")
                chinaOrderno = func_user.getparse(itemResult, 'item-option item-option-order">','</span>').strip()
                if D_ali_orderno != chinaOrderno:
                    print(">> [{}] 주문번호 불일치 (확인필요) : {}".format(D_ali_orderno, chinaOrderno))
                else:
                    itemtracking = func_user.getparse(itemResult, 'class="item-option item-option-tracking">','</span>')
                    if itemtracking.find('target="_blank">') > -1:
                        itemtracking = func_user.getparse(itemtracking, 'target="_blank">','</a>')

                    print(">> [{}] tracking No : {} | chinaOrderno : {} ".format(D_ali_orderno, itemtracking, chinaOrderno))
                    if itemtracking == "":
                        print(">> 트래킹 번호 입력 before : {}".format(D_tracking_china))
                        proc_trackno(browser, D_tracking_china)
                        time.sleep(1)
                        if str(browser.page_source).find(D_tracking_china) > -1:
                            print(">> 트래킹 번호 입력 확인 OK ( 완료상태변경 ) : {}".format(D_tracking_china))
                            up_sql = "update T_ORDER_DELIVERY set tracking_china_state = 'T' where uid = '" + str(D_infoUid) + "' "
                            # print('>> up_sql : ' + str(up_sql))
                            db_con.execute(up_sql)
                            upd_cnt = upd_cnt + 1
                    elif itemtracking != D_tracking_china:
                        print(">> 트래킹 번호 변경됨 확인필요 : 이전 - {} | 현재 - {}".format(itemtracking, D_tracking_china))
                    else:
                        print(">> [{}] 트래킹 번호 있음 (SKIP) : {}".format(chinaOrderno, itemtracking))
                        up_sql = "update T_ORDER_DELIVERY set tracking_china_state = 'T' where uid = '" + str(D_infoUid) + "' "
                        db_con.execute(up_sql)


def get_track_name(delicode):
    delivery_company = ""
    DeliveryUid = ""
    DeliveryName = ""

    # 송장 13자리
    if len(delicode) == 13:
        if delicode[:1] == "S" or delicode[:1] == "M" or delicode[:1] == "B" or delicode[:1] == "Q" or delicode[:2] == "ET" or delicode[:2] == "MP" or delicode[:3] == "ETH" or delicode[:3] == "FTL":
            delivery_company = "GENERALPOST"
            DeliveryUid = "29"
            DeliveryName = "일반우편"
        elif delicode[:2] == "60":
            delivery_company = "EPOST" 
            DeliveryUid = "12"
            DeliveryName = "우체국택배"
        elif delicode[:4] == "8003":
            delivery_company = "HANJIN" 
            DeliveryUid = "18"
            DeliveryName = "한진택배"
        elif delicode[:2] == "75":
            delivery_company = "YUNDA" 
            DeliveryUid = "22"
            DeliveryName = "YUNDAEXPRES"
        elif delicode[:2] == "WL":
            delivery_company = "KOREXG"
            DeliveryUid = "21"
            DeliveryName = "CJ대한통운(국제택배)"
        elif delicode[:2] == "LP":
            delivery_company = "EMS"
            DeliveryUid = "30"
            DeliveryName = "EMS"
        elif delicode[:2] == "WJ":
            delivery_company = "WOOJIN" 
            DeliveryUid = "25"
            DeliveryName = "우진인터로지스"
        else:
            delivery_company = "EMS" 
            DeliveryUid = "30"
            DeliveryName = "EMS"     

    # 송장 12자리일 경우
    elif len(delicode) == 12:
        if delicode[:2] == "31":
            delivery_company = "HYUNDAI"
            DeliveryUid = "26"
            DeliveryName = "롯데택배"
        elif delicode[:2] == "80" or delicode[:2] == "51":
            delivery_company = "HANJIN"
            DeliveryUid = "18"
            DeliveryName = "한진택배"
        elif delicode[:2] == "77":
            delivery_company = "FEDEX"
            DeliveryUid = "6"
            DeliveryName = "FEDEX"                        
        elif delicode[:2] == "56" or delicode[:2] == "57" or delicode[:2] == "58" or delicode[:2] == "59":
            delivery_company = "CJGLS"
            DeliveryUid = "4"
            DeliveryName = "CJ대한통운"

    # 송장 18자리일 경우
    elif len(delicode) == 18:
        if delicode[:2] == "1Z":
            delivery_company = "UPS"
            DeliveryUid = "7"
            DeliveryName = "UPS"

    if DeliveryName == "": # 그외
        delivery_company = "GENERALPOST"
        DeliveryUid = "29"
        DeliveryName = "일반우편"

    return DeliveryUid, DeliveryName, delivery_company

def proc_get(db_con, browser, menu, diffday):
    global upd_cnt

    itemResult = ""
    proc_url = "https://www.ohmyzip.com/list/"+str(menu)
    print(">> proc_url : {}".format(proc_url))
    browser.get(proc_url)
    source = str(browser.page_source)
    itemResult = func_user.getparse(source, '<section id="content"','')
    itemResult = func_user.getparse(itemResult, '창고위치','')
    itemResult = func_user.getparse(itemResult, '<tbody>','</tbody>')
    if str(itemResult).find('데이타가 없습니다') > -1:
        print(">> 데이타가 없습니다 : {}".format(menu))
        return "0"

    endPage = 1
    #print(">> endPage : {}".format(endPage))
    time.sleep(2)

    page = 1
    dic_orderno = dict()
    dic_trackno = dict()
    while page <= int(endPage):
        print("\n\n>> ---------------------- curPage : {}".format(page))
        if itemResult == "" or itemResult.find("데이타가 없습니다") > -1:
            print(">> 데이터 없음 ")
            break
        else:
            spItem = func_user.getparse(itemResult, '<tr>','').split('</tr>')
            for item in spItem:
                itemNo = func_user.getparse(item, 'ship_no=','"').strip()
                if itemNo.find('&') > -1:
                    itemNo = func_user.getparse(itemNo, '','&').strip()
                chinaOrderno = func_user.getparse(item, 'detail.1688.com/offer','</td>')
                chinaOrderno = func_user.getparse(chinaOrderno, '(',')').strip()
                delieveyNo = func_user.getparse(item, '?wbl=','"').strip()
                if len(itemNo) > 0 and len(delieveyNo) > 0:
                    dic_orderno[str(itemNo)] = chinaOrderno
                    dic_trackno[str(itemNo)] = delieveyNo
                    print(">> [{}] {} | {} ".format(itemNo, chinaOrderno, delieveyNo))

        page = page + 1
        time.sleep(2)

    rowCnt = 0
    for key, val in dic_orderno.items():
        delieveyNo = ""
        delivery_price = ""
        rowCnt = rowCnt + 1
        pkgNo = ""
        item_ea = ""
        itemNo = key
        chinaOrderno = val
        delieveyNo = dic_trackno[str(key)]
        proc_url = "https://www.ohmyzip.com/account/invoicePrint?ship_no="+str(itemNo)+"&wbl_no="+str(delieveyNo)
        browser.get(proc_url)

        itemDetail = func_user.getparse(str(browser.page_source), 'class="payTable"','</table>')
        delivery_price = "¥ " + func_user.getparse(itemDetail, 'class="currency_format">','</span>').strip()
        delivery_weight = func_user.getparse(itemDetail, '</strong>','</tr>')
        delivery_weight = func_user.getparse(delivery_weight, '<td>','</td>').strip()
        if delivery_weight.find('적용 무게') > -1:
            delivery_weight = func_user.getparse(delivery_weight, '적용 무게','</span>')
            delivery_weight = func_user.getparse(delivery_weight, '">','').replace('▶','').strip()

        if itemNo != "":
            print(">> [{}] 신청서번호 : {} ({}) | 운송장번호 : {} | 결제금액 : {}원 |  무게: {}개".format(chinaOrderno, itemNo, pkgNo, delieveyNo, delivery_price, delivery_weight))

            # 송장번호 매칭 택배사명 가져오기 DeliveryUid, DeliveryName, delivery_company 
            DeliveryUid, DeliveryName, delivery_company = get_track_name(delieveyNo)
            print("(" + str(rowCnt) + ") 송장번호 : " + str(delieveyNo) + " (" + str(DeliveryName) + ") [" + str(DeliveryUid) + " : " +str(delivery_company)+ " | " + str(chinaOrderno))

            sql = "select amazon_orderno from ohmyzip_tracking where amazon_orderno = '" + str(chinaOrderno) + "' "
            row = db_con.selectone(sql)
            if not row:
                sql = "insert into ohmyzip_tracking (delivery_id,delicode,amazon_orderno, itemNo, pkgNo, delivery_price, item_weight) values ('" + str( DeliveryUid) + "','" + str(delieveyNo) + "','" + str(chinaOrderno) + "','" + str(itemNo) + "','" + str(pkgNo) + "','" + str(delivery_price) + "','" + str(delivery_weight) + "')"
                print("Insert table : ohmyzip_tracking ")
                upd_cnt = upd_cnt + 1
                db_con.execute(sql)
        else:
            if delieveyNo == "":
                pass
            else:
                sql = "select state from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where ali_orderno = '" + str(chinaOrderno) + "'"
                row = db_con.selectone(sql)
                if row:
                    db_state = row[0]
                    if str(db_state) == "201" or str(db_state) == "421":
                        #input(" 확인 필요 ( 시스템 부서에 알려주세요. ) : ")
                        print(" 새로운 택배사 등록필요 - 1688 : " + str(chinaOrderno) + " | 송장번호 : " + str(delieveyNo))
                        func_user.procLogSet(db_con,gProc_no, "E", "0", "새로운 택배사 등록필요 - 1688 : " + str(chinaOrderno)+ " | 송장번호 : " + str(delieveyNo))
                        procLogTracking(chinaOrderno, delieveyNo)

                    else:
                        print(" 새로운 택배사 : {} (state: {})".format(chinaOrderno, db_state))

    return "0"

def get_china_tracking(browser):
    print(">> 중국 현지 송장 ")

    proc_url = "https://www.ohmyzip.com/list/orderList"
    browser.get(proc_url)

    result_tmp = func_user.getparse(str(browser.page_source), 'id="search_area"','</section>')
    result_tmp = func_user.getparse(result_tmp, '창고위치','</table>')
    result_tmp = func_user.getparse(result_tmp, '<tbody>','</tbody>')

    spItem = result_tmp.split('</tr>')
    for item in spItem:
        itemNo = func_user.getparse(item, 'ship_no=','&').strip()
        taobaoNo = func_user.getparse(item, 'detail.1688.com/offer/','</td>').strip()
        taobaoNo = func_user.getparse(taobaoNo, '(',')').strip()
        chinaTrackno = func_user.getparse(item, 'www.baidu.com/s?ie=utf-8&amp;wd=','"')
        if chinaTrackno != "":
            print(">> [{}] {} | {} ".format(itemNo, taobaoNo, chinaTrackno))
            sql = "select isnull(d.tracking_china,''), pkgNo, d.uid from t_order_info as i inner join T_ORDER_DELIVERY as d on d.uid = i.uid where ali_orderno = '{}'".format(taobaoNo)
            row = db_con.selectone(sql)
            if row:
                tracking_china, pkgNo, d_uid = row
                print(">> [{}] (uid:{}) ".format(taobaoNo, d_uid))
                if tracking_china == "":
                    sql = "update T_ORDER_DELIVERY set tracking_china = '{}', tracking_china_date = getdate(), pkgNo = '{}' where uid = '{}'".format(chinaTrackno,itemNo,d_uid)
                    print(">> Update table : tracking_china : {}".format(sql))
                    db_con.execute(sql)
                else:
                    print(">> tracking_china 존재 (skip): " + str(taobaoNo))

    print(">> 현지 중국 송장 ")

if __name__ == '__main__':

    print('>> ohmyzip Delivery Put & Get (1688 트래킹 번호 --> 오마이집 입력 / 오마이집 배송건 --> 프리쉽 발송처리 ) Proc ')
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))

    gProc_no = "DEV_OHMYZIP"
    in_aliId = "red"
    db_con = DBmodule_FR.Database('freeship')

    loginid = ""
    loginpass = ""
    sql = "select login_id, login_pw from ali_order_auto_set where proc_name = 'ohmyzip'"
    row = db_con.selectone(sql)
    if row:
        loginid = str(row[0])
        loginpass = str(row[1])
        print(">> loginid : {}".format(loginid))

    set_browser = "chrome"
    ip = socket.gethostbyname(socket.gethostname())

    time.sleep(1)
    func_user.procLogSet(db_con,gProc_no, "S", 0, '1688 트래킹 번호 --> 오마이집 (ohmyzip) 입력 : ' +str(ip))
    proc_id = ""
    try:
        proc_id, browser = func_user.connectSubProcess()
    except Exception as e:
        try:
            browser = func_user.connectDriverOld("https://www.ohmyzip.com", "S")
        except Exception as e:
            print('예외가 발생 (종료) : ', e)
            func_user.procLogSet(db_con,gProc_no, "E", "0", 'connectDriver 접속 에러 (종료)')
            time.sleep(5)
            print('>> time.sleep(5) ')
            os._exit(1)
    else:
        print('connectDriver Ok ')

    time.sleep(3)
    browser.set_window_size(1600, 1000)
    browser.implicitly_wait(3)

    timecount = 0
    now_url = "https://www.ohmyzip.com"
    browser.get(now_url)
    #browser.maximize_window()
    time.sleep(3)
    browser.set_window_size(1600, 1200)
    time.sleep(1)
    result = str(browser.page_source)
    #print("result : "+str(result))

    if result.find('Hello, ') > -1:
        print(">> 로그인 되어있음 ")
    else:
        print(">> 로그인 처리 ")
        now_url = "https://www.ohmyzip.com/account/signin?ret="
        browser.get(now_url)
        time.sleep(1)

        try:
            elem = browser.find_element(By.CSS_SELECTOR,"#email")
            elem_clear(browser, elem)
            elem.send_keys(loginid)
            elem = browser.find_element(By.CSS_SELECTOR,"#pwd")
            elem_clear(browser, elem)
            elem.send_keys(loginpass)
            time.sleep(1)
            browser.find_element(By.CSS_SELECTOR,"#content > section > span").click()
            time.sleep(2)
        except Exception as e:
            print(">> Exception Login_proc ")
            func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
            input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")
    time.sleep(2)

    if str(browser.page_source).find('Hello, ') == -1:
        input(">> 로그인 처리후 아무숫자나 입력해 주세요(2) : ")
        time.sleep(2)

    # # 중국송장번호 -> 오마이집에 트래킹번호 입력 처리
    # upd_cnt = 0
    # proc_put(db_con, browser)
    # func_user.procLogSet(db_con,gProc_no, "F", upd_cnt, '[' +str(in_aliId)+ '] 1688중국 트래킹 번호 --> 오마이집에 (ohmyzip) 입력완료 : '+str(upd_cnt))

    print(">> 배대지 중국 송장번호 프리쉽 매칭 ")
    get_china_tracking(browser)


    sql = "delete from ohmyzip_tracking "
    print("Delete : " + str(sql))
    db_con.execute(sql)

    print('>> goport Delivery Put (오마이집 트래킹 번호 --> 프리쉽 배송처리) Proc ')
    # 오마이집 -> 한국 배송 트래킹번호 프리쉽 반영
    func_user.procLogSet(db_con,gProc_no, "S", 0, '오마이집 트래킹 번호 --> 프리쉽 배송처리 : ' +str(ip))

    ##############################################
    upd_cnt = 0
    print(">> 국내도착(통관중) ")
    proc_get(db_con, browser, "list_110", 30) # 국내도착(통관중) https://www.ohmyzip.com/list/list_100
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(in_aliId)+ '] 오마이집 (ohmyzip) --> 프리쉽 배송처리 (발송완료) : '+str(upd_cnt))

    upd_cnt = 0
    print(">> 통관완료 ")
    proc_get(db_con, browser, "list150", 30) # 통관완료 https://www.ohmyzip.com/list/list150
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(in_aliId)+ '] 오마이집 (ohmyzip) --> 프리쉽 배송처리 (통관중) : '+str(upd_cnt))

    # 기간 : 30일전부터 오늘까지
    diffday = 45
    today = date.today()
    week_diff = date.today() - timedelta(diffday)
    strFrom = str(week_diff)
    strTo = str(today)

    upd_cnt = 0
    print(">> 국내배송 ")
    proc_menu = "orderList?status_cd=400&date_from="+str(strFrom)+"&date_to="+str(strTo)+"&search_type=product_nm&keyword="
    proc_get(db_con, browser, proc_menu, 30) # 국내배송 # https://www.ohmyzip.com/list/orderList?status_cd=400
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(in_aliId)+ '] 오마이집 (ohmyzip) --> 프리쉽 배송처리 (통관완료) : '+str(upd_cnt))

    upd_cnt = 0
    print(">> 국내배송완료 ")
    proc_menu = "orderList?status_cd=500&date_from="+str(strFrom)+"&date_to="+str(strTo)+"&search_type=product_nm&keyword="
    proc_get(db_con, browser, proc_menu, 30) # 국내배송완료 # https://www.ohmyzip.com/list/orderList?status_cd=500
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(in_aliId)+ '] 오마이집 (ohmyzip) --> 프리쉽 배송처리 (배송완료) : '+str(upd_cnt))
    ##############################################

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/ohmyzip_tracking_proc.asp"
    print(" >> Next Proc 실행 (프리쉽 송장처리 : ohmyzip_tracking_proc.asp) : " + str(run_url))

    browser.get(run_url)
    time.sleep(5)
    print(" time.sleep(5) ")
    ##############################################

    func_user.procLogSet(db_con, gProc_no, "F", "0", "1688 프리쉽 송장처리 " + str(run_url))

    db_con.close()
    print(">> time.sleep(120) ")
    time.sleep(120)
    print('\n [--- main End ---] ' + str(datetime.datetime.now()))
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)