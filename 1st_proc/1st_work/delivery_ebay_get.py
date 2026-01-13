
import time
import os
import datetime
import random
import socket
from sys import exit
import subprocess
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import DBmodule_FR
import func_user

db_con = DBmodule_FR.Database('freeship')

########################################################################################
# ebay 송장번호 처리 
########################################################################################
global gProc_no
global upd_cnt
gProc_no = "DEV_SEL_EBAY_GET"

def proc_login(browser):
    loginTmp = func_user.getparse(str(browser.page_source), 'id="signin-form"', 'id="signin-continue-btn"')
    if loginTmp.find('id="userid"') > -1:
        print(">> Login ID 입력 ")
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="userid"]').send_keys('bugeon151@gmail.com')
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="signin-continue-btn"]').click()

    if str(browser.page_source).find('for="pass"') > -1:
        print(">> Login Pass 입력 ")
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="pass"]').send_keys('moohan7243@')
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="sgnBt"]').click()
        time.sleep(5)

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

def procDelievey(browser):
    upd_cnt = 0
    time.sleep(1)
    if str(browser.page_source).find('class="m-container-items">') == -1:
        time.sleep(5)

    orderResult = func_user.getparse(str(browser.page_source), 'class="m-container-items">', 'class="m-container__footer"')     
    orderSP = orderResult.split('<div class="m-order-card">')
    print(">> orderSP : {}".format(len(orderSP)))
    ordCnt = 0
    for ea_order in orderSP:
        if ea_order != "":
            ordCnt = ordCnt + 1
            orderEbayNo = func_user.getparse(ea_order, '<dt>ORDER NUMBER</dt>', '</div>')
            orderEbayNo = func_user.getparse(orderEbayNo, '<dd>', '</dd>').strip()
            orderGoodNo = func_user.getparse(ea_order, 'info-item-info-listingId">(', ')').strip()
            orderTrackNo = func_user.getparse(ea_order, 'Tracking number:', '</p>')
            orderTrackNo = func_user.getparse(orderTrackNo, '<span class="PSEUDOLINK">', '</span>').strip()
            if orderTrackNo == "":
                print(">> {} : {} ( 상품코드: {} ) | trackNo : No ".format(ordCnt, orderEbayNo, orderGoodNo))
            else:
                print(">> {} : {} ( 상품코드: {} ) | trackNo : {}".format(ordCnt, orderEbayNo, orderGoodNo, orderTrackNo))

                sql = "select i.uid, o.uid, o.orderno, o.state, isnull(d.tracking_china,''), d.tracking_china_date, tracking_china_state from t_order as o inner join t_order_info as i on i.OrderUid = o.uid join T_ORDER_DELIVERY as d on d.uid = i.uid \
                    where state in ('201','301','421') and ali_id = 'ref' and tracking_china_state is null and ali_orderno = '{}' and order_ali_no = '{}' ".format(orderEbayNo, orderGoodNo)
                rows = db_con.select(sql)
                if rows:
                    for row in rows:
                        db_InfoUid = row[0]
                        db_Ouid = row[1]
                        db_orderNo = row[2]
                        db_state = row[3]
                        db_tracking_china = row[4]
                        db_tracking_china_date = row[5]
                        db_tracking_china_state = row[6]
                        if str(db_tracking_china).strip() == orderTrackNo:
                            print(">> -------- DB (Skip): {} | {} | {} [new:{} | DB:{}]".format(db_orderNo, orderEbayNo, db_state, orderTrackNo, db_tracking_china))
                        else:
                            print(">> -------- DB Update : {} | {} | {} [new:{} | DB:{}]".format(db_orderNo, orderEbayNo, db_state, orderTrackNo, db_tracking_china))
                            sql_u = " update T_ORDER_DELIVERY set tracking_china = '{}', tracking_china_date = getdate() where uid = '{}'".format(orderTrackNo, db_InfoUid)
                            #print(">> sql_u : {}".format(sql_u))
                            db_con.execute(sql_u)
                            upd_cnt = upd_cnt + 1

    return upd_cnt



def procDelieveyPage(browser):
    time.sleep(1)
    browser.get("https://www.ebay.com/mye/myebay/v2/purchase?page=1&moduleId=122169")
    time.sleep(5)
    if str(browser.page_source).find('>Orders</h2>') == -1:
        time.sleep(5)

    upd_cnt = 0
    if str(browser.page_source).find('class="m-container-items">') == -1:
        time.sleep(5)

    if str(browser.page_source).find('<ol class="pagination__items"') > -1:
        orderPageTmp = func_user.getparse(str(browser.page_source), '<ol class="pagination__items"', '</ol>')
        orderPageTmp = func_user.getparseR(orderPageTmp, 'class="pagination__item"', '</button>')
        orderPageEnd = func_user.getparse(orderPageTmp, '>', '').replace('"','')
        print(">> orderPageEnd : {}".format(orderPageEnd))

    procPage = 0
    if int(orderPageEnd) > 12:
        procPage = 12
    else:
        procPage = int(orderPageEnd)

    for page in range(1,procPage+1):
        print("\n\n----------------------------------------------------------------------")
        print(">> CurrPage : {}".format(page))

        linkUrl = 'https://www.ebay.com/mye/myebay/v2/purchase?page=' +str(page)+ '&moduleId=122169&mp=purchase-module-v2&type=v2&pg=purchase'
        print(">> linkUrl : {}".format(linkUrl))
        browser.get(linkUrl)
        time.sleep(5)
        if str(browser.page_source).find('>Shipped</h2>') == -1:
            time.sleep(5)

        orderResult = func_user.getparse(str(browser.page_source), '>Shipped</', 'class="m-container__footer"')
        orderSP = orderResult.split('<div class="m-ph-card m-order-card">')
        print(">> orderSP : {}".format(len(orderSP)))
        ordCnt = 0
        for ea_order in orderSP:
            if ea_order != "":
                orderTrackNo = ""
                ea_result = ""
                orderEbayNo = func_user.getparse(ea_order, 'Order number:</span>', '</div>')
                orderEbayNo = func_user.getparse(orderEbayNo, 'item-text">', '</span>').strip()
                if orderEbayNo == "":
                    continue
                ordCnt = ordCnt + 1
                print("\n\n -----------------------------------------------------------")
                orderGoodNo = func_user.getparse(ea_order, 'item-info-title">', '</div>').strip()
                orderGoodNo = func_user.getparse(str(orderGoodNo), 'ebay.com/itm/', '"').strip()
                if str(orderGoodNo).find('?') > -1:
                    orderGoodNo = func_user.getparse(orderGoodNo, '', '?').strip()

                print(">>[{} page] ({}) : {} ( 상품코드: {} ) ".format(page, ordCnt, orderEbayNo, orderGoodNo))
                if ea_order.find('/ship/trk/tracking-details?') == -1:
                    print(">> ({}) (Track Package No) trackNo : No".format(orderEbayNo))
                else:
                    tractInfo = func_user.getparse(ea_order, '/ship/trk/tracking-details?', '"')
                    transid = func_user.getparse(tractInfo, 'transid=', '&')
                    itemid = func_user.getparse(tractInfo, 'itemid=', '')

                    searchurl = "https://www.ebay.com/ship/trk/tracking-details?transid={}&itemid={}".format(transid, itemid)
                    # print(">> searchurl : {}".format(searchurl))
                    browser.get(searchurl)
                    time.sleep(2)
                    ea_result = str(browser.page_source)
                    orderTrackNo = func_user.getparse(ea_result, 'class="tracking-details"', '</div>')
                    if orderTrackNo.find("strOrigTrackNum=") > -1:
                        orderTrackNo = func_user.getparse(orderTrackNo, 'strOrigTrackNum=', '&').strip()
                    elif orderTrackNo.find("InquiryNumber1=") > -1:
                        orderTrackNo = func_user.getparse(orderTrackNo, 'InquiryNumber1=', '"').strip()
                    else:
                        orderTrackNo = func_user.getparse(ea_result, 'title-container__trackingNumber"', '<').strip()
                        if orderTrackNo.find('>') > -1:
                            orderTrackNo = func_user.getparse(orderTrackNo, '>', '').strip()
                    if orderTrackNo == "":
                        if ea_result.find('"trackingNumber":"') > -1:
                            orderTrackNo = func_user.getparse(ea_result, '"trackingNumber":"', '"').strip()

                    if orderTrackNo == "":
                        print(">> ({}) trackNo : No".format(orderEbayNo))
                    else:
                        print(">> ({}) trackNo : {}".format(orderEbayNo, orderTrackNo))

                        if orderGoodNo == "":
                            sql = "select i.uid, o.uid, o.orderno, o.state, isnull(d.tracking_china,''), d.tracking_china_date, tracking_china_state, i.ali_id from t_order as o inner join t_order_info as i on i.OrderUid = o.uid join T_ORDER_DELIVERY as d on d.uid = i.uid \
                            where state in ('201','301','421') and ali_id in ('ref','ref2') and tracking_china_state is null and ali_orderno = '{}'".format(orderEbayNo)
                        else:
                            sql = "select i.uid, o.uid, o.orderno, o.state, isnull(d.tracking_china,''), d.tracking_china_date, tracking_china_state, i.ali_id from t_order as o inner join t_order_info as i on i.OrderUid = o.uid join T_ORDER_DELIVERY as d on d.uid = i.uid \
                            where state in ('201','301','421') and ali_id in ('ref','ref2') and tracking_china_state is null and ali_orderno = '{}' and order_ali_no = '{}' ".format(orderEbayNo, orderGoodNo)
                        # sql = "select i.uid, o.uid, o.orderno, o.state, isnull(d.tracking_china,''), d.tracking_china_date, tracking_china_state from t_order as o inner join t_order_info as i on i.OrderUid = o.uid join T_ORDER_DELIVERY as d on d.uid = i.uid \
                        #     where state in ('201','301','421') and ali_id in ('ref','ref2') and tracking_china_state is null and ali_orderno = '{}'".format(orderEbayNo)
                        rows = db_con.select(sql)
                        if rows:
                            for row in rows:
                                db_InfoUid = row[0]
                                db_Ouid = row[1]
                                db_orderNo = row[2]
                                db_state = row[3]
                                db_tracking_china = row[4]
                                db_tracking_china_date = row[5]
                                db_tracking_china_state = row[6]
                                db_ali_id = row[7]
                                if str(db_tracking_china).strip() == str(orderTrackNo):
                                    print(">> -------- DB (Skip): {} | {} | {} [new:{} | DB:{}]".format(db_orderNo, orderEbayNo, db_state, orderTrackNo, db_tracking_china))
                                    pass
                                else:
                                    print(">> -------- DB Update : {} | {} | {} [new:{} | DB:{}]".format(db_orderNo, orderEbayNo, db_state, orderTrackNo, db_tracking_china))
                                    sql_u = " update T_ORDER_DELIVERY set tracking_china = '{}', tracking_china_date = getdate() where uid = '{}'".format(orderTrackNo, db_InfoUid)
                                    print(">> update T_ORDER_DELIVERY (tracking_china) : {}".format(orderEbayNo))
                                    db_con.execute(sql_u)
                                    upd_cnt = upd_cnt + 1

    return upd_cnt


# 취소 및 환불처리 
def procReturnCancelPage(browser):
    time.sleep(1)
    browser.get("https://www.ebay.com/mye/myebay/v2/purchase?page=1&moduleId=122166")
    time.sleep(5)
    if str(browser.page_source).find('>Returns & Canceled</') == -1:
        time.sleep(5)

    rtnCnt = 0
    if str(browser.page_source).find('class="m-container-items">') == -1:
        time.sleep(5)

    if str(browser.page_source).find('<ol class="pagination__items"') > -1:
        orderPageTmp = func_user.getparse(str(browser.page_source), '<ol class="pagination__items"', '</ol>')
        orderPageTmp = func_user.getparseR(orderPageTmp, 'class="pagination__item"', '</button>')
        orderPageEnd = func_user.getparse(orderPageTmp, '>', '').replace('"','')
        print(">> orderPageEnd : {}".format(orderPageEnd))

    procPage = 0
    if int(orderPageEnd) > 5:
        procPage = 5
    else:
        procPage = int(orderPageEnd)

    for page in range(1,procPage+1):
        print("\n\n----------------------------------------------------------------------")
        print(">> CurrPage : {}".format(page))

        linkUrl = 'https://www.ebay.com/mye/myebay/v2/purchase?page=' +str(page)+ '&moduleId=122166&mp=purchase-module-v2&type=v2&pg=purchase'
        print(">> linkUrl : {}".format(linkUrl))
        browser.get(linkUrl)
        time.sleep(5)
        if str(browser.page_source).find(' Canceled</h') == -1:
            time.sleep(5)
        func_user.getparse(str(browser.page_source), 'title-container', 'class="m-container__footer"')
        orderResult = func_user.getparse(str(browser.page_source), ' Canceled</h', 'class="m-container__footer"')
        orderSP = orderResult.split('<div class="m-ph-card m-order-card">')
        print(">> orderSP : {}".format(len(orderSP)))
        ordCnt = 0
        for ea_item in orderSP:
            if ea_item != "":
                stateTmp = func_user.getparse(ea_item, 'class="section-notice__main">', '</div>')
                stateTmp = func_user.getparse(stateTmp, 'item-text">', '</span>').strip()
                cancelOrderNo = func_user.getparse(ea_item, 'Order number:</span>', '</div>')
                cancelOrderNo = func_user.getparse(cancelOrderNo, 'item-text">', '</span>').strip()
                if cancelOrderNo == "":
                    continue
                ordCnt = ordCnt + 1
                cancelGoodNo = func_user.getparse(ea_item, 'item-info-title">', '</div>').strip()
                cancelGoodNo = func_user.getparse(cancelGoodNo, 'ebay.com/itm/', '"').strip()
                if str(cancelGoodNo).find('?') > -1:
                    cancelGoodNo = func_user.getparse(cancelGoodNo, '', '?').strip()
                print(">> [{}] {} | {} | {} ".format(ordCnt, cancelOrderNo, cancelGoodNo, stateTmp))

                if str(stateTmp) == "Order canceled" or str(stateTmp).find("Refunded") > -1 or str(stateTmp).find("Canceled") > -1:
                    print(" >> {} proc ".format(stateTmp))
                    if ea_item.find('The item has been cancele') > -1:
                        reason = "ebay_cancel"
                    elif str(stateTmp).find("Refunded") > -1: 
                        reason = "ebay_returncancel"
                    else:
                        reason = "ebay_cancel"
                    if str(cancelOrderNo) != "":
                        sql_q = " SELECT O.orderno, O.Uid , I.Uid, O.state, I.ali_id from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid \
                            inner join T_ORDER O on O.uid=D.OrderUid where O.state in ('201','301') and ali_orderno = '{}' and order_ali_no = '{}' ".format(cancelOrderNo, cancelGoodNo)
                        #print(" sql_q : " + str(sql_q))
                        row_q = db_con.selectone(sql_q)
                        if not row_q:
                            pass #print(">> DB Order 체크 ( SKIP ) : {} | {} | {} ".format(cancelOrderNo, cancelGoodNo, "ebay_cancel"))
                        else:
                            db_orderno = row_q[0]
                            db_Ouid = row_q[1]
                            db_InfoUid = row_q[2]
                            db_state = row_q[3]
                            db_ali_id = row_q[4]
                            print(">> DB Order 체크 : {} | {} | {} ".format(cancelOrderNo, cancelGoodNo, reason))

                            sql_s = " select OrderNo from freeship_tracking_check where Infouid = '{}'".format(db_InfoUid)
                            #print(" sql_s : " + str(sql_s))
                            row = db_con.selectone(sql_s)
                            if not row:
                                # ebay 취소 및 배송사고건 freeship_tracking_check 테이블에 입력
                                iSql = " insert into freeship_tracking_check ( ProcDate, OrderNo, ali_orderno, ali_id, Reason, ouid, Infouid ) "
                                iSql = iSql + " values ( getdate(), '" + str(db_orderno) + "','" + str(cancelOrderNo) + "','" + str(db_ali_id) + "', '" + str(reason) + "', '" + str(db_Ouid) + "', '" + str(db_InfoUid) + "' )"
                                print(" cancel order DB table ( Insert ) : " + str(cancelOrderNo))
                                db_con.execute(iSql)

                            # T_ORDER_DELIVERY 테이블 tracking_china_state 변경
                            up_sql = "update T_ORDER_DELIVERY set tracking_china_state = 'F' where Uid = '" + str(db_InfoUid) + "' "
                            print(">> cancel order DB table ( Update ) (tracking_china_state:F) : " + str(cancelOrderNo))
                            #print('>> up_sql : ' + str(up_sql))
                            db_con.execute(up_sql)
                            rtnCnt = rtnCnt + 1
                else:
                    print(" >> {} (Skip) ".format(stateTmp))

    return rtnCnt

# 트래킹 파싱
def procTracking(browser,db_con):
    time.sleep(1)
    
    sql = "select i.uid, o.uid, o.orderno, o.state, isnull(d.tracking_china,''), d.tracking_china_date, tracking_china_state from t_order as o inner join t_order_info as i on i.OrderUid = o.uid join T_ORDER_DELIVERY as d on d.uid = i.uid where  ali_orderno = '{}'"
    
    
    time.sleep(1)
    browser.get("https://www.ebay.com/mye/myebay/v2/purchase?page=1&moduleId=122169")
    time.sleep(5)
    if str(browser.page_source).find('>Returns & Canceled</h2>') == -1:
        time.sleep(5)

    rtnCnt = 0
    if str(browser.page_source).find('class="m-container-items">') == -1:
        time.sleep(5)

    if str(browser.page_source).find('<ol class="pagination__items"') > -1:
        orderPageTmp = func_user.getparse(str(browser.page_source), '<ol class="pagination__items"', '</ol>')
        orderPageTmp = func_user.getparseR(orderPageTmp, 'class="pagination__item"', '</button>')
        orderPageEnd = func_user.getparse(orderPageTmp, '>', '').replace('"','')
        print(">> orderPageEnd : {}".format(orderPageEnd))

    procPage = 0
    if int(orderPageEnd) > 8:
        procPage = 8
    else:
        procPage = int(orderPageEnd)
    procPage = 2
    for page in range(1,procPage+1):
        print("\n\n----------------------------------------------------------------------")
        print(">> CurrPage : {}".format(page))

        linkUrl = 'https://www.ebay.com/mye/myebay/v2/purchase?page=' +str(page)+ '&moduleId=122169&mp=purchase-module-v2&type=v2&pg=purchase'
        print(">> linkUrl : {}".format(linkUrl))
        browser.get(linkUrl)
        time.sleep(5)
        if str(browser.page_source).find('Shipped</h2>') == -1:
            time.sleep(5)
        func_user.getparse(str(browser.page_source), 'title-container', 'class="m-container__footer"')
        orderResult = func_user.getparse(str(browser.page_source), 'Shipped</h2>', 'class="m-container__footer"')
        orderSP = orderResult.split('<div class="m-ph-card m-order-card">')
        print(">> orderSP : {}".format(len(orderSP)))
        ordCnt = 0
        for ea_item in orderSP:
            time.sleep(5)
            if ea_item != "":
                stateTmp = func_user.getparse(ea_item, 'class="section-notice__main">', '</div>')
                stateTmp = func_user.getparse(stateTmp, 'item-text">', '</span>').strip()
                OrderNo = func_user.getparse(ea_item, 'Order number:</span>', '</div>')
                OrderNo = func_user.getparse(OrderNo, 'item-text">', '</span>').strip()                
                if OrderNo == "":
                    print("OrderNo 없음")
                    continue
                print("OrderNo : "+OrderNo)
                rs = db_con.selectone(sql.format(OrderNo))
                if rs:
                    db_InfoUid = rs[0]
                    browser.get("https://order.ebay.com/ord/show?orderId={}#/".format(OrderNo))
                    now_url = browser.current_url
                    if now_url.find("limitexceeded") > -1:
                        input("리퀘스트 제한")
                    track_source = browser.page_source
                    if track_source.find('<span class="SECONDARY">Number</span>') > -1:
                        stateTmp = func_user.getparse(track_source, 'class="inner-tracking-box">', '</div>')
                        stateTmp = func_user.getparse(stateTmp, '<dd>', '</dd>').strip()
                        stateTmp = func_user.getparse(stateTmp, 'class="eui-text-span">', '</span>').strip()
                        tracking_no = stateTmp.replace('<span class="">',"")
                        sql_u = " update T_ORDER_DELIVERY set tracking_china = '{}', tracking_china_date = getdate(), tracking_china_state = 'T' where uid = '{}'".format(tracking_no, db_InfoUid)
                        print("tracking_no : "+tracking_no)
                        print(">> sql_u : {}".format(sql_u))
                        db_con.execute(sql_u)
                    else:
                        print("No trackingNo")

                else:
                    print("db없음")


    # sql_u = " update T_ORDER_DELIVERY set tracking_china = '{}', tracking_china_date = getdate() where uid = '{}'".format(orderTrackNo, db_InfoUid)
    #print(">> sql_u : {}".format(sql_u))
    # db_con.execute(sql_u)

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
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)

    return browser

if __name__ == '__main__':
    
    pgSite="https://www.ebay.com"

    upd_cnt = 0
    print('>> ebay Delivery Get Proc (ebay 송장 번호 --> 프리쉽 또는 배대지 송장 입력 처리) ')
    print('>> [--- main start ---] ' + str(datetime.datetime.now()))

    cur_Ip = socket.gethostbyname(socket.gethostname())
    func_user.procLogSet(db_con, gProc_no, "S", "0", "ebay 현지 송장 가져오기 : "+str(cur_Ip))

    try:
        proc_con, browser = func_user.connectSubProcess()
    except Exception as e:
        try:
            browser = func_user.connectDriverOld(pgSite,'S')
        except Exception as e:
            print('예외가 발생 (종료) : ', e)
            procLogSet(gProc_no, "E", "0", "connectDriver 접속 에러 (종료)")
            time.sleep(20)
            print('>> time.sleep(20) ')
            os._exit(1)
    # browser = connectDriver("https://www.ebay.com")
    browser.set_window_size(1300, 1000)
    time.sleep(2)

    now_url = "https://www.ebay.com/"
    browser.get(now_url)
    time.sleep(5)
    tmpStr = func_user.getparse(str(browser.page_source), '<button id="gh-ug"', '</button>')
    if tmpStr.find('>Hi <b>') > -1:
        tmpStr = func_user.getparse(str(browser.page_source), '<button id="gh-ug"', '</button>')
        print(">> 로그인 된 상태 ")
        time.sleep(2)
    else:
        now_url = "https://signin.ebay.com"
        browser.get(now_url)
        time.sleep(5)
        if str(browser.page_source).find('hCaptcha') > -1:
            print(">> hCaptcha 해제해 주세요. ")
            func_user.procLogSet(db_con, gProc_no, "E", "0", "hCaptcha 해제해 주세요")
            input(">> Input : ")
            time.sleep(2)
        # 로그인 처리 
        proc_login(browser)

    ###input(">> Input : ")

    if str(browser.page_source).find('href="https://www.ebay.com/mys/home') > -1:
        print(">> Login OK ")

        print("\n\n>> ------- Delivery Proc -------")
        # delivery proc
        rtn_cnt = 0
        rtn_cnt = procDelieveyPage(browser)
        print(">> Update Count : {}".format(rtn_cnt))
        time.sleep(1)

        print("\n\n>> ------- ReturnCancel Proc -------")
        # returncancel proc
        rtn_returncancel_cnt = 0
        rtn_returncancel_cnt = procReturnCancelPage(browser)
        print(">> ReturnCancel Count : {}".format(rtn_returncancel_cnt))
        procTracking(browser,db_con)
        func_user.procLogSet(db_con, gProc_no, "P", rtn_cnt, "프리쉽 (ebay) 송장 처리 : " +str(rtn_cnt)+ " | Return & Cancel : " +str(rtn_returncancel_cnt))
        time.sleep(3)

    else:
        print(">> Login Error (종료)")
        procLogSet(gProc_no, "E", "0", " 로그인 에러 (종료)")
        time.sleep(10)

    func_user.procLogSet(db_con, gProc_no, "F", "0", "END ebay 현지 송장 가져오기 : "+str(cur_Ip))
    print('>> [--- main End ---] ' + str(datetime.datetime.now()))
    db_con.close()
    time.sleep(2)
    browser.quit()
    try:
        print(">>proc_con.pid : {}".format(proc_con.pid))
        subprocess.Popen.kill(proc_con)
    except:
        pass
    os._exit(0)


