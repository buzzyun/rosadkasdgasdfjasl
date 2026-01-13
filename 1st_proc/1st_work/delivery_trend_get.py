import os
os.system('pip install --upgrade selenium')
import time
import datetime
import random
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import DBmodule_FR
import func_user
import subprocess
import socket

db_con = DBmodule_FR.Database('freeship')

########################################################################################
# ebay 송장번호 처리 
########################################################################################
global gProc_no
global upd_cnt
gProc_no = "DEV_SEL_TREND_GET"

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

def connectDriverNew():
    try:
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(service=f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(5) 
    driver.set_page_load_timeout(3600)
    return driver

def connectDriverNew2(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")

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
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        s = Service(executable_path='C:\\project\\chromedriver.exe')
        browser = webdriver.Chrome(service=s, options=option)

    return browser

def connectChrome():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    options = webdriver.ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    options.add_argument("user-data-dir={}".format(userProfile))
    browser = webdriver.Chrome(executable_path=driver_path, options=options) 
    time.sleep(1)
    browser.set_window_size(1300, 1000)
    time.sleep(2)

    return browser

def login_proc(browser):
    # 로그인 처리 
    browser.get("https://asia.shein.com/user/auth/login?from=navTop")
    time.sleep(3)
    try:
    ## element = browser.find_elements(By.CLASS_NAME, 'sui-input')[0].find_element(By.TAG_NAME, "input")
        element = browser.find_element(By.CSS_SELECTOR, 'div.page__login_mergeLoginItem > div.actions > div:nth-child(1) > button')
        if element:
            element.click()
            time.sleep(3)
            skipElem = browser.find_element(By.CSS_SELECTOR, 'div.sui-dialog__wrapper.sui-dialog__W480 > div.sui-dialog__body > div.con > div.skip > span')
            if skipElem:
                skipElem.click()
                print(">> Skip PopUp Click Ok")

    except Exception as e:
        print(">> Exception")

# 배송처리
def procDelivery(in_drive, in_Uid, in_InfoUid, in_ali_orderno, in_orderNo, in_orderId):
    global upd_cnt
    delivery_no = ""
    delivery_name = ""
    delivery_state = ""

    #proc_url = 'https://asia.shein.com/user/orders/track/' + str(in_ali_orderno)
    proc_url = 'https://kr.shein.com/orders/track?billno=' + str(in_ali_orderno)
    #print(">> proc_url : " + str(proc_url))
    in_drive.get(proc_url)
    time.sleep(4)
    print(">> orderno : " + str(in_orderNo))
    result_sour = str(in_drive.page_source)
    time.sleep(0.5)
    # print("result2 : "+str(result2))
    if str(result_sour).strip() == "":
        print(" URL 접속 에러 : {}".format(in_ali_orderno))
        return "E"

    if str(result_sour).find('div class="track-null"') > -1:
        print(" 처리 대상 없음 (SKIP) : {}".format(in_ali_orderno))
        return "1"

    tmpTrackInfo = func_user.getparse(str(result_sour),'<div class="track-info-wrap">','id="j-emarsys-container-you-may-also-like"')
    if str(result_sour).find('class="logistic-info__base-number"') > -1:
        delivery_no = func_user.getparse(str(result_sour),'class="logistic-info__base-number"','</span>')
        delivery_no = func_user.getparse(str(delivery_no),'>','').strip()  
    # elif str(result_sour).find('배송 조회 번호') > -1:
    #     delivery_no = func_user.getparse(str(result_sour),'배송 조회 번호','</div>')
    #     delivery_no = func_user.getparse(str(delivery_no),'data-clipboard-text="','"').strip()
    elif str(result_sour).find('운송장 번호 :') > -1:
        delivery_no = func_user.getparse(str(result_sour),'span class="logistics-info-card__number-text">','</span>').strip()
        # delivery_no = func_user.getparse(str(delivery_no),'data-clipboard-text="','"').strip()
    elif str(result_sour).find('class="logistic-info__base-track"') > -1:
        delivery_no = func_user.getparse(str(result_sour),'class="logistic-info__base-track"','</div>')
        delivery_no = func_user.getparse(str(delivery_no),'data-clipboard-text="','"').strip()
    else:
        print(">> else delivery_no ")
        #testno = input(">> delivery_no check : ")
        delivery_no = ""
        #if testno == "Y":
        #    print(">> tmpTrackInfo : {}".format(tmpTrackInfo))

    if str(result_sour).find('class="logistics-info-card__title-text"') > -1:
        delivery_name = func_user.getparse(str(result_sour),'class="logistics-info-card__title-text"','</span>').strip()
        delivery_name = func_user.getparse(str(delivery_name),'>','').replace('</span>','').replace('<span>','').strip()
    elif str(result_sour).find('class="track-info__name"') > -1:
        delivery_name = func_user.getparse(str(result_sour),'class="track-info__name"','</div>')
        delivery_name = func_user.getparse(str(delivery_name),'class="name notranslate"','</span>')
        delivery_name = func_user.getparse(str(delivery_name),'>','').replace('</span>','').replace('<span>','').strip()
    else:
        print(">> else delivery_name ")
        #testname = input(">> delivery_name check : ")
        #if testname == "Y":
        #    print(">> tmpTrackInfo : {}".format(tmpTrackInfo))
        delivery_name = ""

    print(">> delivery info : {} | {} ".format(delivery_no, delivery_name))
    # test = input(">> check : ")
    # if test == "Y":
    #     print(">> tmpTrackInfo : {}".format(tmpTrackInfo))

    if delivery_no != "" and delivery_name == "":
        print(">> 송장번호 있고 택배사 없음 : {} | {}".format(delivery_no, delivery_name))
        if delivery_no[:2] == "80" and len(delivery_no) == 12:
            delivery_name = "HANJIN"
            print(">> 택배사 수정: HANJIN ")

    if len(delivery_no) == 0:
        print(">> 미발송 (SKIP) : {} | {} ".format(in_orderNo, in_ali_orderno))
        return "0"
    else:
        sql = "select * from trend_tracking where infouid = '{}'".format(in_InfoUid)
        row = db_con.selectone(sql)
        if not row:
            sql = "insert into trend_tracking (delivery_id, delicode, delivery_price, orderno, trend_orderno, ouid, infouid) values ('{}','{}','{}','{}','{}','{}','{}')".format(delivery_name, delivery_no, '0', in_orderNo, in_ali_orderno, in_Uid, in_InfoUid)	
            #print(">> sql : {}".format(sql))
            db_con.execute(sql)
        else:
            sql = "update trend_tracking set delivery_id = '{}', delicode = '{}', orderno ='{}', trend_orderno = '{}' where infouid = '{}'".format(delivery_name, delivery_no, in_orderNo, in_ali_orderno, in_InfoUid)	
            #print(">> sql : {}".format(sql))
            db_con.execute(sql)
        print(">> 발송 (Ok) : {} ({}) | {} | {} ".format(in_orderNo, in_ali_orderno, delivery_no, delivery_name))
        upd_cnt = upd_cnt + 1

    return "0"

def procRun(browser):
    ######################################################
    # 주문 아이디별 송장 트래킹 처리
    ######################################################
    upd_cnt = 0
    sql_d = " delete from trend_tracking "
    print(">> delete table : " + str(sql_d))
    db_con.execute(sql_d)
    orderId = "trend"

    # 주문 아이디별 트래킹 번호 미입력 리스트 검색
    sql = " SELECT I.ali_orderno, O.orderno, O.state, O.RegDate, O.ChkDate, O.Uid , I.Uid, O.naver_pay_product_code, O.naver_pay_cancel "
    sql = sql + " from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid "
    sql = sql + " where I.ali_chk = '0' and D.DeliveryNo is null and D.DeliveryDate is null and O.state in ('201','301','421') "
    sql = sql + " AND o.regdate > '2023-05-15' and I.ali_id = '" +str(orderId)+ "' and RegDate > getdate() - 90 "
    sql = sql + " order by ali_ord_date asc "
    #print("sql : " + str(sql))

    rows = db_con.select(sql)
    low = 0
    lenRows = 0
    if rows:
        lenRows = str(len(rows))
        print(">> SHEIN 리스트 Cnt : " + str(len(rows)))
        procLogSet(gProc_no, "P", "0", "리스트 Cnt : " + str(len(rows)))

        for ea_row in rows:
            tracking_no = ""
            ali_orderno = ea_row[0]
            orderNo = ea_row[1]
            state = ea_row[2]
            RegDate = ea_row[3]
            ChkDate = ea_row[4]
            DUid = ea_row[5]
            DInfoUid = ea_row[6]

            print(" [" + str(low) + "] " + str(orderNo) + " | " + str(DUid) + " | " + str(DInfoUid) + " | " + str(ali_orderno))

            time.sleep(1)
            if len(ali_orderno) == 0:
                print(">> ali_orderno Check please : {}".format(orderNo))
                low = low + 1
                continue

            if ali_orderno.find('GSH') == -1:
                print(" 잘못된 주문번호 (SKIP) : {}".format(ali_orderno))
                low = low + 1
                continue

            rtn_Flg = procDelivery(browser, DUid, DInfoUid, ali_orderno, orderNo, orderId)
            if rtn_Flg == "E":
                print(" Error Exit : " + str(rtn_Flg))
                procLogSet(gProc_no, "E", "0", "Error Exit : " + str(ali_orderno))
                db_con.close
                browser.quit()
                os._exit(1)
            elif rtn_Flg == "1":
                print(">> SKIP : " + str(rtn_Flg))
                procLogSet(gProc_no, "F", "0", "처리 대상 없음 : " + str(ali_orderno))
                break
            # elif rtn_Flg == "0":
            #     print(">> 미발송 (SKIP) : " + str(orderNo))

            low = low + 1
    else:
        print("리스트 없음 " + str(sql))
        procLogSet(gProc_no, "P", "0", "리스트 없음 ")

    print(" 실행 cnt  " + str(lenRows) + " | 테이블 tracking 입력 : " + str(upd_cnt))
    procLogSet(gProc_no, "P", str(upd_cnt), "SHEIN 실행 cnt  " + str(lenRows) + " | 테이블 tracking 입력 : " + str(upd_cnt))

    time.sleep(1)
    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/trend_tracking_proc.asp?mode=del"
    print(" >> Next Proc 실행 (TREND) 프리쉽 송장처리 : trend_tracking_proc.asp?mode=del : " + str(run_url))

    browser.get(run_url)
    time.sleep(5)
    print(" time.sleep(5) ")
    procLogSet(gProc_no, "F", "0", " (TREND) 프리쉽 송장처리 완료 " + str(run_url))
    print('\n [--- main end ---] ' + str(datetime.datetime.now()))

    return "0"

# 배송처리
def proc_test(browser):
    global upd_cnt
    delivery_no = ""
    delivery_name = ""
    delivery_state = ""

    test_ali_orderno = "GSHNYY13700NWHH"

    proc_url = 'https://asia.shein.com/user/orders/track/' + str(test_ali_orderno)
    browser.get(proc_url)
    time.sleep(3)
    print(">> proc_url : " + str(proc_url))

    result_sour = str(browser.page_source)
    time.sleep(0.5)
    # print("result2 : "+str(result2))
    if str(result_sour).strip() == "":
        print(" URL 접속 에러 : {}".format(test_ali_orderno))
        return "E"

    if str(result_sour).find('class="track-info-wrap"') == -1:
        print(" 처리 대상 없음 (SKIP) : {}".format(test_ali_orderno))
        return "1"

    # if str(result_sour).find('class="track-null"') == -1:
    #     print(">> 미발송 (SKIP) : {} ".format(test_ali_orderno))
    #     return "0"

    delivery_no = func_user.getparse(str(result_sour),'배송 조회 번호','</div>')
    delivery_no = func_user.getparse(str(delivery_no),'data-clipboard-text="','"').strip()
    delivery_name = func_user.getparse(str(result_sour),'class="track-info__name"','</div>')
    delivery_name = func_user.getparse(str(delivery_name),'class="name notranslate"','</span>')
    delivery_name = func_user.getparse(str(delivery_name),'>','').strip()
    print(" delivery no : {} | {} ".format(delivery_no, delivery_name))


# 취소 및 반품 체크
def procCencelRun(browser):
    print(">> ")
    
    time.sleep(1)
    browser.get("https://asia.shein.com/user/orders/list?from=navTop&page=1")
    time.sleep(5)

    rtnCnt = 0
    if str(browser.page_source).find('<ul class="list-body">') == -1:
        time.sleep(5)

    if str(browser.page_source).find('<ul class="list-body">') > -1:
        orderPageTmp = func_user.getparse(str(browser.page_source), 'class="sui-pagination__total"', 'class="sui-pagination__next')
        orderPageEnd = func_user.getparseR(orderPageTmp, 'class="sui-pagination__inner', '</span>').replace('"','')
        orderPageEnd = func_user.getparse(orderPageEnd, '>', '').strip()
        print(">> orderPageEnd : {}".format(orderPageEnd))

    procPage = 0
    if int(orderPageEnd) > 12:
        procPage = 12
    else:
        procPage = int(orderPageEnd)

    for page in range(1,procPage+1):
        print("\n\n----------------------------------------------------------------------")
        print(">> CurrPage : {}".format(page))

        linkUrl = 'https://asia.shein.com/user/orders/list?from=navTop&page=' +str(page)
        print(">> linkUrl : {}".format(linkUrl))
        browser.get(linkUrl)
        time.sleep(5)

        orderResult = func_user.getparse(str(browser.page_source), '<ul class="list-body">', '</ul>')
        orderSP = orderResult.split('<li class="list-item"')
        print(">> orderSP : {}".format(len(orderSP)))
        ordCnt = 0
        for ea_item in orderSP:
            if ea_item != "":
                stateTmp = func_user.getparse(ea_item, 'class="status-text"', '</span>')
                stateTmp = func_user.getparse(stateTmp, '>', '').strip()
                listOrderNo = func_user.getparse(ea_item, '">주문 번호 : ', '</span>').strip()
                if listOrderNo == "":
                    continue
                ordCnt = ordCnt + 1
                # print(">> [{}] {} | {} ".format(ordCnt, listOrderNo, stateTmp))

                if stateTmp.find('취소') > -1:
                    print(">> (Cancel) [{}] {} | {} ".format(ordCnt, listOrderNo, stateTmp))
                elif stateTmp.find('반품') > -1 or stateTmp.find('환불') > -1:
                    print(">> (Refund) [{}] {} | {} ".format(ordCnt, listOrderNo, stateTmp))
                else:
                    print(">> [{}] {} | {} ".format(ordCnt, listOrderNo, stateTmp))

    return "0"


# 배송완료 체크
def procCompletedCheck(browser):
    print(">> ")
    cnt_302 = 0
    sql = "select o.uid, i.uid, orderno, ali_orderno, d.DeliveryDate, d.DeliveryNo, o.payway \
        from t_order as o inner join t_order_info as i on i.OrderUid = o.uid inner join T_ORDER_DELIVERY as d on d.uid = i.uid \
        where ali_chk = '1' and sitecate = 'trend' and ali_id = 'trend' and o.State = '301' \
        and d.DeliveryNo is not null and RegDate > '2023-05-01' and isnull(tracking_state,'') <> '배송완료' and d.DeliveryDate < getdate() - 7 "
    rows = db_con.select(sql)
    low = 0
    if rows:
        print(">> 배송중 리스트 Cnt : " + str(len(rows)))
        # procLogSet(gProc_no, "P", "0", "배송중 리스트 Cnt : " + str(len(rows)))

        for ea_row in rows:
            track_content = ""
            track_state = ""
            low = low + 1
            Ouid = ea_row[0]
            Iuid = ea_row[1]
            orderno = ea_row[2]
            ali_orderno = ea_row[3]
            DeliveryDate = ea_row[4]
            DeliveryNo = ea_row[5].strip()
            payway = ea_row[6]
            print(" [{}] {} | {} | Ouid : {} | Iuid : {} | DeliveryDate : {} | DeliveryNo : {} | payway : {}".format(low, orderno, ali_orderno, Ouid, Iuid, DeliveryDate, DeliveryNo, payway))

            linkUrl = 'https://asia.shein.com/user/orders/track/' +str(ali_orderno)
            # print(">> linkUrl : {}".format(linkUrl))
            browser.get(linkUrl)
            time.sleep(3)
            # if str(browser.page_source).find('class="show-more"') > -1:
            #     elem = browser.find_element(By.CSS_SELECTOR, 'div.track-res.j-track-ctn > div > div.info-ctn > div')
            #     if elem:
            #         elem.click()
            #         time.sleep(3)

            track_info_name = func_user.getparse(str(browser.page_source), 'class="track-info__name"', 'class="track-info"')
            track_info_name = func_user.getparse(track_info_name, 'class="name notranslate"', '</span>')
            track_info_name = func_user.getparse(track_info_name, '>', '')

            track_info_no = func_user.getparse(str(browser.page_source), '배송 조회 번호', 'class="track-info"')
            track_info_no = func_user.getparse(track_info_no, 'class="number"', '</span>')
            track_info_no = func_user.getparse(track_info_no, '>', '')

            track_info_date = func_user.getparse(str(browser.page_source), '예상 배송 시간 :', 'class="track-info"')
            track_info_date = func_user.getparse(track_info_date, 'class="number"', '</span>')
            track_info_date = func_user.getparse(track_info_date, '>', '')
            print(">> {} | {} | {}".format(track_info_no, track_info_name, track_info_date))

            track_state_ctn = func_user.getparse(str(browser.page_source), 'class="track-info">', '</ul>')
            track_state_ctn = func_user.getparse(track_state_ctn, 'class="info-ctn">', '')
            track_state_ctn = func_user.getparse(track_state_ctn, '<li ', '</ul>')
            sp_track = track_state_ctn.split('class="j-info-list"')

            track_content = "<br>배송 조회 번호 : " + track_info_no + " (" + track_info_name + ")<br> 예상 배송 시간 : " + track_info_date + "<br><hr>"
            track_content = track_content + "<ul>"
            for ea_track in sp_track:
                track_date = func_user.getparse(ea_track, 'class="date notranslate"', '</p>') 
                track_date = func_user.getparse(track_date, '>', '')
                if track_date == "":
                    continue
                track_time = func_user.getparse(ea_track, 'class="time"', '</p>')
                track_time = func_user.getparse(track_time, '>', '') 
                track_title = func_user.getparse(ea_track, 'class="title', '</p>') 
                track_title = func_user.getparse(track_title, '>', '') 
                track_detail = func_user.getparse(ea_track, 'class="desc', '</p>')
                track_detail = func_user.getparse(track_detail, '>', '') 
                track_content = track_content + "<li><div>" + track_date + " " + track_time + "<br>" + track_title + "<br>" + track_detail + "</div></li><br>"

            track_content = track_content.replace("'","") + "</ul>"
            # print(">> track_content : {}".format(track_content))
            if track_content.find('서명되었습니다.') > -1:
                track_state = "배송완료"
                if payway != "NaverPay": # 네이버주문건이 아닐경우... 배송중 301 -> 배송완료 302로 변경
                    sql_u1 = "update T_ORDER set state = '302' where uid = '{}'".format(Ouid)
                    print(">> update state : 302 ")
                    db_con.execute(sql_u1)
                    cnt_302 = cnt_302 + 1
            elif track_content.find('배송중') > -1:
                track_state = "배송중"
            else:
                track_state = "배송준비"
            print(">> [{}] {} : {}".format(orderno, ali_orderno, track_state))

            sql_u = "update T_ORDER_DELIVERY set tracking_content = '{}', tracking_memo = '{}', tracking_state = '{}', tracking_content_date = getdate() where uid = '{}'".format(track_content, track_content, track_state, Iuid)
            print(">> update T_ORDER_DELIVERY ")
            db_con.execute(sql_u)

    procLogSet(gProc_no, "P", str(cnt_302), "SHEIN 배송내역 처리 : 전체 " + str(len(rows)) + " | 302 배송완료 : " + str(cnt_302))

    return "0"


if __name__ == '__main__':

    upd_cnt = 0
    print('>> shein Delivery Get Proc (shein 송장 번호 --> 프리쉽 송장 입력 처리) ')
    print('>> [--- main start ---] ' + str(datetime.datetime.now()))

    ip = socket.gethostbyname(socket.gethostname())
    procLogSet(gProc_no, "S", "0", "SHEIN 송장 입력 처리 : " + str(ip))

    if str(ip).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        time.sleep(1)

    # browser = connectChrome()
    now_url = "https://asia.shein.com"
    # browser = connectDriverNew(now_url, "")
    # browser = connectDriverNew()
    proc, browser = func_user.connectSubProcess()
    browser.maximize_window()
    browser.get(now_url)
    time.sleep(5)
    browser.get("https://kr.shein.com/user/orders/list?from=navTop&ref=asia&rep=dir&ret=kr")
    time.sleep(5)

    result = str(browser.page_source)
    if result.find('class="order-list-card"') > -1 and result.find('aria-label="주문 번호 :') > -1:
        first_orderno = func_user.getparse(result, 'aria-label="주문 번호 :', '"').strip()
        if first_orderno == "":
            print(">> 로그인 된 상태 ")
            func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
            try:
                # 로그인 처리 
                login_proc(browser)
            except Exception as e:
                print(">> Exception Login_proc ")
                func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
                input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")
            else:
                func_user.procLogSet(db_con, gProc_no, "P", "0", "Login OK ")
        else:
            print(">> Order List Ok")
    else:
        if result.find('class="header-user-info">') > -1:
            print(">> 로그인 된 상태 ")
            func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
            time.sleep(2)
        else:
            try:
                # 로그인 처리 
                login_proc(browser)
            except Exception as e:
                print(">> Exception Login_proc ")
                func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
                input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")
            else:
                func_user.procLogSet(db_con, gProc_no, "P", "0", "Login OK ")
    time.sleep(2)
    if str(browser.page_source).find('class="header-user-info">') > -1:
        print(">> 로그인 Ok ")
    else:
        func_user.procLogSet(db_con, gProc_no, "E", "0", "Login Error ")
        input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")
        time.sleep(2)
    ### input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")

    # 배송처리 
    procRun(browser)

    print('>> [--- main End ---] ' + str(datetime.datetime.now()))
    db_con.close()
    time.sleep(5)
    browser.quit()


