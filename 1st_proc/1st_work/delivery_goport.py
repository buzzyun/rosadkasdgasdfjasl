import os
import time
import socket
import datetime
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            # da = Alert(browser)
            # time.sleep(0.5)
            # if str(da.text).find('완료') > -1:
            #     check_flg = "0"
            #     print(da.text)
            # da.accept()
            # time.sleep(1)
            # Alert 대기 및 확인 예시
            wait = WebDriverWait(browser, 10)
            wait.until(EC.alert_is_present())
            alert = Alert(browser)
            time.sleep(0.5)
            if str(alert.text).find('완료') > -1 or str(alert.text).find('정상') > -1:
                check_flg = "0"
                print(alert.text)
            alert.accept()  # 경고창 확인
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
    sql = sql + " and tracking_china is not null and tracking_china_state is null AND I.ali_id in ('taobao','taobao1','red2') and amazon_price_date > '2023-07-04 00:00:00' "
    print("sql : " + str(sql))

    rows = db_con.select(sql)
    low = 0
    lenRows = ""
    if rows:
        lenRows = str(len(rows))
        print(">> 리스트 Count : " + str(lenRows))
        # func_user.procLogSet(db_con,gProc_no, "P", "0", '[' +str(in_taobaoId)+ '] 주문 트래킹 번호 미입력 리스트 : '+str(len(rows)))

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


def proc_get(db_con, browser, menu, diffday):
    global upd_cnt
    print(">> ")

    # 기간 : 30일전부터 오늘까지
    today = date.today()
    week_diff = date.today() - timedelta(diffday)
    strFrom = str(week_diff).replace("-", "")
    strTo = str(today).replace("-", "")
    itemResult = ""

    proc_url = "https://goport.kr/agency/order?status="+str(menu)+"&s=referCode&k=&orderType=&customsInfoValid=&deliveryLock=&date1="+str(strFrom)+"&date2=" + str(strTo)
    browser.get(proc_url)
    source = str(browser.page_source)
    itemResult = func_user.getparse(source, 'class="table-list order-item-list"','</table>')
    if str(itemResult).find('데이타가 없습니다') > -1:
        print(">> 데이타가 없습니다 : {}".format(menu))
        return "0"

    pageResult = func_user.getparse(source, '<div class="pagination a1">','</div>')
    endPage = func_user.getparse(pageResult, 'class="direction next last">','</span>')
    endPage = int(func_user.getparse(endPage, 'pageNo/','"'))
    print(">> endPage : {}".format(endPage))
    time.sleep(2)

    page = 1
    while page <= int(endPage):
        print("\n\n>> ---------------------- curPage : {}".format(page))

        if page > 1:
            proc_url = "https://goport.kr/agency/order/status/"+str(menu)+"/date1/" +str(strFrom)+ "/date2/" +str(strTo)+ "/pageNo/" + str(page)
            browser.get(proc_url)
            source = str(browser.page_source)
            itemResult = func_user.getparse(source, 'class="table-list order-item-list"','</table>')

        if itemResult == "" or itemResult.find("데이타가 없습니다") > -1:
            print(">> 데이터 없음 ")
        else:
            rowCnt = 0
            spItem = itemResult.split('</tr>')
            for item in spItem:
                itemNo = ""
                chinaOrderno = ""
                delieveyNo = ""
                delivery_price = ""
                rowCnt = rowCnt + 1

                status = func_user.getparse(str(item), '<span class="status">', '</span>').strip()
                if status.find('발송완료') > -1 or status.find('통관중') > -1 or status.find('통관완료') > -1 or status.find('배송완료') > -1:
                    itemNo = func_user.getparse(item, '"itemId">아이템번호:','</span>').strip()
                    if str(itemNo).find('"')>-1:
                      itemNo = func_user.getparse(itemNo,None,'"')
                    pkgNo = func_user.getparse(item, '묶음번호:','</span>').strip()
                    chinaOrderno = func_user.getparse(item, 'class="item-option item-option-order">','</span>').strip()
                    delieveyNo = func_user.getparse(item, '운송장번호:','</span>').strip()
                    delivery_price = func_user.getparse(item, '결제금액 :','</span>').replace("원","").replace(",","").strip()
                    item_ea = func_user.getparse(item, 'class="quantity">','</span>').replace("개","").strip()
                    # if delieveyNo.find('EXT') > -1:
                    #     print(">> 묶음 송장번호 ")
                    #     delieveyNo = func_user.getparse(item, 'btn btn-default btn-xs','</div>') 
                    #     if delieveyNo.find('invc_no=') > -1:
                    #         delieveyNo = func_user.getparse(delieveyNo, 'invc_no=','"')
                    #     if len(delieveyNo) > 14:
                    #         delieveyNo = func_user.getparse(delieveyNo, '',' ').strip()

                    if delieveyNo.find('EXT') > -1:
                        print(">> 묶음 송장번호 ")
                        if str(item).find('배송현황') > -1:
                            deliverMemo = func_user.getparseR(str(item), '배송현황', 'class="order-buttons"')
                            deliverMemo = func_user.getparseR(str(deliverMemo), 'InvNo=', '"')
                            print(">> 송장번호 여러개 : {}".format(deliverMemo))
                        if deliverMemo != "":
                            delieveyNo = func_user.getparseR(str(deliverMemo), '', ' ')
                            updDateMemo = str(datetime.datetime.now())[5:10].replace('-','/') + " 송장번호 : " + str(deliverMemo) + " [adminauto] "
                            sql = "select isnull(adminmemo,''), orderno from t_order as o inner join t_order_info as i on i.orderuid = o.uid where ali_orderno = '{}'".format(chinaOrderno)
                            row_a = db_con.selectone(sql)
                            if row_a:
                                db_adminmemo = row_a[0]
                                db_orderno = row_a[1]
                                if db_adminmemo.find('[adminauto]') == -1:
                                    uSql = " update t_order set adminmemo = isnull(adminmemo,'') + '{}' where orderno = '{}'".format(updDateMemo, db_orderno)
                                    print(">> adminmemo update : {}".format(updDateMemo))
                                    db_con.execute(uSql)

                    if delieveyNo.find('target="_blank">') > -1:
                        delieveyNo = func_user.getparse(delieveyNo, 'target="_blank">','</a>').strip()
                    if itemNo != "":
                        print(">> [{}] 신청서번호 : {} ({}) | 운송장번호 : {} | 결제금액 : {}원 |  수량: {}개".format(chinaOrderno, itemNo, pkgNo, delieveyNo, delivery_price, item_ea))

                    if str(delieveyNo)[:1] == "3" or str(delieveyNo)[:2] == "55" or str(delieveyNo)[:2] == "56" or str(delieveyNo)[:2] == "57" or str(delieveyNo)[:2] == "58" or str(delieveyNo)[:2] == "59":
                        if len(delieveyNo) > 12:
                            func_user.procLogSet(gProc_no, "E", "0", "송장번호12자리 이상 확인필요:"+str(chinaOrderno)+":"+str(delieveyNo)+" ")
                            time.sleep(1)
                            delieveyNo = delieveyNo[:12].strip()

                        if len(delieveyNo) == 12 and str(delieveyNo)[:2] == "31":
                            delivery_id = "HYUNDAI"
                            delivery_company = "HYUNDAI"
                            DeliveryUid = "26"
                            DeliveryName = "롯데택배"
                        else:
                            delivery_id = "CJ-IPS"
                            delivery_company = "CJGLS"
                            DeliveryUid = "4"
                            DeliveryName = "CJ대한통운"
                        print("(" + str(rowCnt) + ") 송장번호 : " + str(delieveyNo) + " (" + str(DeliveryName) + ") [" + str(delivery_id) + "] | " + str(chinaOrderno))

                        sql = "select amazon_orderno from sellermaker_tracking where amazon_orderno = '" + str(chinaOrderno) + "' "
                        row = db_con.selectone(sql)
                        if not row:
                            sql = "insert into sellermaker_tracking (delivery_id,delicode,amazon_orderno, itemNo, pkgNo, delivery_price, item_ea) values ('" + str( delivery_id) + "','" + str(delieveyNo) + "','" + str(chinaOrderno) + "','" + str(itemNo) + "','" + str(pkgNo) + "','" + str(delivery_price) + "','" + str(item_ea) + "')"
                            print("Insert table : sellermaker_tracking ")
                            upd_cnt = upd_cnt + 1
                            print(sql)
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
                                    print(" 새로운 택배사 등록필요 - 타오바오 : " + str(chinaOrderno) + " | 송장번호 : " + str(delieveyNo))
                                    func_user.procLogSet(db_con,gProc_no, "E", "0", "새로운 택배사 등록필요 - 타오바오 : " + str(chinaOrderno)+ " | 송장번호 : " + str(delieveyNo))
                                    procLogTracking(chinaOrderno, delieveyNo)
                                    # return "1"
                                else:
                                    print(" 새로운 택배사 : {} (state: {})".format(chinaOrderno, db_state))

        page = page + 1
        time.sleep(2)

    return "0"



if __name__ == '__main__':

    print('>> goport Delivery Put (타오바오 트래킹 번호 --> 고포트 입력) Proc ')
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))
    ip = socket.gethostbyname(socket.gethostname())
    gProc_no = "DEV_GOPORT_TAO"
    in_taobaoId = "taobao1"
    db_con = DBmodule_FR.Database('freeship')

    loginid = ""
    loginpass = ""
    sql = "select login_id, login_pw from ali_order_auto_set where proc_name = 'goport'"
    row = db_con.selectone(sql)
    if row:
        loginid = str(row[0])
        loginpass = str(row[1])
        print(">> loginid : {}".format(loginid))

    set_browser = "chrome"

    time.sleep(1)
    func_user.procLogSet(db_con,gProc_no, "S", 0, '타오바오 트래킹 번호 --> 고포트 (goport) 입력 : ' +str(ip))
    proc_id = ""
    try:
        proc_id, browser = func_user.connectSubProcess()
    except Exception as e:
        try:
            browser = func_user.connectDriverOld("https://goport.kr", "")
        except Exception as e:
            print('예외가 발생 (종료) : ', e)
            func_user.procLogSet(db_con,gProc_no, "E", "0", 'connectDriver 접속 에러 (종료)')
            time.sleep(5)
            print('>> time.sleep(5) ')
            os._exit(1)
    else:
        print('connectDriver Ok ')

    time.sleep(3)
    browser.set_window_size(1920, 1000)
    browser.implicitly_wait(3)

    timecount = 0
    now_url = "https://goport.kr"
    browser.get(now_url)
    #browser.maximize_window()
    time.sleep(2)
    browser.set_window_size(1920, 1400)
    time.sleep(5)
    result = str(browser.page_source)
    #print("result : "+str(result))

    try:
        browser.find_element(By.CSS_SELECTOR,'#ch-shadow-root-wrapper > article > div > div > div.VideoPreviewCloseBtn__CloseButtonArea-ch-front__sc-1r76upb-2.jQDfTd > button > svg').click()
    except Exception as e:
        print('>> 팝업 닫기 (1) except: ', e)
    time.sleep(1.5)

    mainResult = func_user.getparse(result, '<ul class="ul pull-right">','</ul>')
    if mainResult.find('/member/logout') > -1:
        print(">> 로그인 되어있음 ")
    else:
        print(">> 로그인 처리 ")
        if str(browser.current_url).find("member/login/targetUrl/") > -1:
            elem_input1 = "#member-login > form > div.form-group > input:nth-child(1)"
            elem_input2 = "#member-login > form > div.form-group > input:nth-child(2)"
            elem_btn = "#member-login > form > button"
        elif str(browser.current_url).find("goport.kr") > -1:
            elem_input1 = "div.widget.widget-login-info > form > div.login-form > input:nth-child(1)"
            elem_input2 = "div.widget.widget-login-info > form > div.login-form > input:nth-child(2)"
            elem_btn = "div.widget.widget-login-info > form > button"
        else:
            elem_input1 = "div.login-form > input:nth-child(1)"
            elem_input2 = "div.login-form > input:nth-child(2)"
            elem_btn = "div.widget.widget-login-info > form > button"
        try:
            elem = browser.find_element(By.CSS_SELECTOR,elem_input1)
            elem_clear(browser, elem)
            elem.send_keys(loginid)
            elem = browser.find_element(By.CSS_SELECTOR,elem_input2)
            elem_clear(browser, elem)
            elem.send_keys(loginpass)
            browser.find_element(By.CSS_SELECTOR,elem_btn).click()
            time.sleep(2)
        except Exception as e:
            print(">> Exception Login_proc ")
            func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
            input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")

    try:
        browser.find_element(By.CSS_SELECTOR,'#ch-shadow-root-wrapper > article > div > div > div.VideoPreviewCloseBtn__CloseButtonArea-ch-front__sc-1r76upb-2.jQDfTd > button > svg').click()
    except Exception as e:
        print('>> 팝업 닫기 (2) except: ', e)
    time.sleep(1.5)

    time.sleep(2)

    # 중국송장번호 -> 고포트에 트래킹번호 입력 처리
    upd_cnt = 0
    proc_put(db_con, browser)
    func_user.procLogSet(db_con,gProc_no, "F", upd_cnt, '[' +str(ip)+ '] 타오바오 트래킹 번호 --> 고포트 (goport) 입력완료 : '+str(upd_cnt))

    sql = "delete from sellermaker_tracking "
    print("Delete : " + str(sql))
    db_con.execute(sql)

    print('>> goport Delivery Put (고포트 트래킹 번호 --> 프리쉽 배송처리) Proc ')
    # 고포트 -> 한국 배송 트래킹번호 프리쉽 반영
    func_user.procLogSet(db_con,gProc_no, "S", 0, '고포트 트래킹 번호 --> 프리쉽 배송처리 : ' +str(ip))

    upd_cnt = 0
    proc_get(db_con, browser, "ADAA", 30) # 발송완료
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(ip)+ '] 고포트 (goport) --> 프리쉽 배송처리 (발송완료) : '+str(upd_cnt))

    upd_cnt = 0
    proc_get(db_con, browser, "ADCA", 30) # 통관중
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(ip)+ '] 고포트 (goport) --> 프리쉽 배송처리 (통관중) : '+str(upd_cnt))

    upd_cnt = 0
    proc_get(db_con, browser, "ADDA", 30) # 통관완료
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(ip)+ '] 고포트 (goport) --> 프리쉽 배송처리 (통관완료) : '+str(upd_cnt))

    upd_cnt = 0
    proc_get(db_con, browser, "AXAA", 30) # 배송완료
    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, '[' +str(ip)+ '] 고포트 (goport) --> 프리쉽 배송처리 (배송완료) : '+str(upd_cnt))

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/taobao_sellermaker_tracking_proc.asp"
    print(" >> Next Proc 실행 (프리쉽 송장처리 : taobao_sellermaker_tracking_proc.asp) : " + str(run_url))

    browser.get(run_url)
    time.sleep(5)
    print(" time.sleep(5) ")

    func_user.procLogSet(db_con, gProc_no, "F", "0", "타오바오 프리쉽 송장처리 " + str(run_url))

    db_con.close()
    print(">> time.sleep(180) ")
    time.sleep(180)
    print('\n [--- main End ---] ' + str(datetime.datetime.now()))
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)