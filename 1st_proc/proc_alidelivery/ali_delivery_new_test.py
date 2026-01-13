import subprocess
import time, random
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import webbrowser
import socket
import os
import DBmodule_FR

global ver
ver = "3.0"
print(">> ver : {}".format(ver))
global gProc_no
global timecount
global cur_Ip
cur_Ip = socket.gethostbyname(socket.gethostname())  

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


# 파싱함수 (뒤에서 부터 찾아서 파싱)
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

# import clipboard
def chrom_drive():
    proc_id = ""
    try:
        proc_id = subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        proc_id = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
    option = webdriver.ChromeOptions()
    # option.add_argument("--incognito")
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
    return driver, proc_id 

def connectDriverOld(pgSite, mode):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    if str(pgSite).find('etsy') == -1:
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")

    browser = webdriver.Chrome(options=option)

    return browser

# 1분 마다 timecount 증가 (1시간 이후 종료)
def fun_timer():
    global timecount
    print(">> fun_timer ")
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 60):
        print('>> 타임아웃 종료 ')

        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)

            time.sleep(5)
            taskstr2 = "taskkill /f /im cmd.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr2 : {}".format(taskstr2))  
            os.system(taskstr2)
        except Exception as e:
            print('>> taskkill Exception (2)')

        time.sleep(5)
        os._exit(1)

def chrom_click(selector, driver):
    print(selector,"클릭(before)")
    driver.find_element(By.CSS_SELECTOR,selector).click()
    time.sleep(1)
    print(selector,"클릭")
    
def chrom_write(selector, driver, write):
    lst = list(write)
    for i in lst:
        driver.find_element(By.CSS_SELECTOR,selector).send_keys(i)
        time.sleep(0.25)
    time.sleep(1)

def PopUpChk(className):
    try:
        chk_pop = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, className))
        )
    except:
        print(className + "없음")
        chk_pop = ""
    return chk_pop  

def scrollDwon(driver):
    try:         
        chrom_click('#root > div > div.order-main > div.order-more > button > span', driver)
    except:
        driver.execute_script("document.getElementsByClassName('comet-btn comet-btn-large comet-btn-borderless')[0].click();")
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("pwnbit.kr", 443))
# ip = sock.getsockname()[0]


def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo, ali_id):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo, ali_id) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "','" + str(ali_id) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "','" + str(ali_id) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "','" + str(ali_id) + "')"

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)

def procLogSetAli(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo, ali_id):
    today = str(datetime.now())[:10]
    sql = "select idx from auto_proc_log_ali where regdate > '{} 00:00:00' and ali_id = '{}'".format(today, ali_id)
    row = db_con.selectone(sql)
    if row:
        idx = row[0]
        sql = "update auto_proc_log_ali set proc_state = '{}', proc_memo = '{}', updatedate = getdate() where idx = '{}'".format(in_proc_state, in_proc_memo, idx)
    else:
        sql = " insert into auto_proc_log_ali (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo, ali_id) "
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "','" + str(ali_id) + "')"
    print(" setLogProcAli : " + str(sql))
    db_con.execute(sql)

def db_save(db_fs, statuses, orderDates, orderNos, proc_name):
    ins = 0
    # db 저장
    for a_status, b_date, c_orderno in zip(statuses,orderDates,orderNos):
        if a_status == "완료":
            print(">> statuses : {} | orderNos : {} 완료상태 스킵".format(a_status, c_orderno))
            continue

        ins = ins + 1
        sql2 = "select ali_orderNO from ali_orderCancel where ali_orderNO = '{}'".format(c_orderno)
        row = db_fs.selectone(sql2)
        if not row:
            sql = "insert into ali_orderCancel(status, orderDate, ali_orderNo, regdate, ali_id, proc_name) values('{}', '{}', '{}', getdate(), '{}', '{}')".format(a_status, b_date, c_orderno, ali_id, proc_name)
            db_fs.execute(sql)
            print(">> statuses : {} | orderNos : {} 저장 완료".format(a_status, c_orderno))
        else:
            sql = "update ali_orderCancel set status = '{}', orderDate = '{}', regdate = getdate(), ali_id = '{}', proc_name = '{}' where ali_orderNo = '{}'".format(a_status, b_date, ali_id, proc_name, c_orderno)
            db_fs.execute(sql)
            print(">> statuses : {} | orderNos : {} 업데이트 완료".format(a_status, c_orderno))

    return ins

def login_set_proc(driver, input_id, input_pw):

    result = driver.page_source
    print("팝업 확인")
    chk_pop = PopUpChk("pop-close-btn")
    if chk_pop == "":
        chk_pop = PopUpChk("btn-close")
    if chk_pop:
        print("팝업 닫기")
        chk_pop.click()
    time.sleep(1)

    # 마우스 커서 어카운트에 위치
    print(">> login proc ")
    try:
        print(">> #nav-user-account > span > a (before) ")
        some_tag=driver.find_element(By.CSS_SELECTOR,"#nav-user-account > span > a")
        ActionChains(driver).move_to_element(some_tag).perform()
    except:
        try:
            print(">> div.my-account--menuItem--1GDZChA > div (before) ")
            some_tag=driver.find_element(By.CSS_SELECTOR,"#_global_header_23_ > div > div > div.pc-header--right--2cV7LB8 > div.pc-header--rightWrap--HYqeULJ > div.pc-header--items--tL_sfQ4 > div.my-account--menuItem--1GDZChA > div")    
            ActionChains(driver).move_to_element(some_tag).perform()
        except:
            print(">> div.my-account--menuItem--1GDZChA > div --- except")

    # sign in 클릭
    time.sleep(1)
    try:
        print(">> sign in 클릭 (before)")
        try:
            print(">> a.sign-btn   click (before)")
            chrom_click("#nav-user-account > div > div > p.flyout-bottons > a.sign-btn", driver)#error
        except:
            print(">> signin--RiPQVPB  click (before)")
            chrom_click("button.my-account--signin--RiPQVPB", driver)#error

        # 아이디, 패스워드 입력
        print(">> id input (before)")
        chrom_click("#fm-login-id", driver)    
        chrom_write("#fm-login-id", driver, input_id)
        chrom_write("#fm-login-password", driver, input_pw)
        print(">> id input (after)")
        try:
            print(">> login-submit > span (before)")
            chrom_click("#batman-dialog-wrap > div > div > div.cosmos-tabs > div.cosmos-tabs-container > div > div > button.cosmos-btn.cosmos-btn-primary.cosmos-btn-large.cosmos-btn-block.login-submit > span", driver)
        except:
            print(">> div.fm-tabs-content > div > div > button (before)")
            chrom_click("#batman-dialog-wrap > div > div.fm-tabs-content > div > div > button", driver)
    except:
        print(">> 로그인 중 except ")

    time.sleep(1)
    try:
        chk_pop = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.btn-close")))
        chk_pop = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(17) > div > div > img.btn-close")))        
    except:
        print(">> chk_pop 없음")
        chk_pop=""

    if chk_pop:
        chk_pop.click()
    time.sleep(2)   

    if str(result).find('"currency":"USD"') > -1:
        print(">> USD OK")
    else:
        print(">> USD SET (before)")
        input(">> After USD set : ")

# 주문내역 이동 
def order_list1(driver):

    url="https://www.aliexpress.com/p/order/index.html"
    print("url: {}".format(url))
    try:
        driver.get(url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item")))
    except:
        driver.get("https://ko.aliexpress.com/")
        time.sleep(1)
        driver.get("https://trade.aliexpress.com/orderList.htm")
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item")))

    ## 알리주문내역 
    print(">> 알리주문내역 (완료) 클릭전 ")
    elem_finished = "#root > div.order-wrap > div.order-header > div.order-nav > div.comet-tabs > div > div > div:nth-child(5)"
    chrom_click(elem_finished, driver)
    time.sleep(5)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
    time.sleep(1)

    if str(driver.page_source).find('class="order-main"') == 0:
        input(">> After login order_page(1) : ")
        time.sleep(1)
        try:
            chrom_click(elem_finished, driver)
            time.sleep(5)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
        except:
            print(">> order page except (1) .. ")

# 주문내역 이동 
def order_list2(driver):

    elem_finished = "#root > div.order-wrap > div.order-header > div.order-nav > div.comet-tabs > div > div > div:nth-child(5)"
    try:
        chrom_click(elem_finished, driver)
        time.sleep(5)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
    except:
        print(">> order page except (2-1) .. ")
    time.sleep(2)
    if str(driver.page_source).find('class="order-main"') == 0:
        input(">> After login order_page(2-1) : ")
        time.sleep(1)
        try:
            chrom_click(elem_finished, driver)
            time.sleep(5)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
        except:
            print(">> order page except (2-2) .. ")
            input(">> After login order_page(2-2) : ")
            time.sleep(1)

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


# 송장 번호 파싱해서 DB 테이블 임시 저장 후 asp 페이지 호출 (asp페이지에서 프리쉽 발송처리 및 네이버페이 송장발송처리)
def proc_delivery(driver, db_fs, ali_id):
    procLogSet(db_fs, gProc_no, "S", "0", "[ " +str(ali_id)+ " ] 송장처리 시작 : " +str(cur_Ip), ali_id)

    sql = "SELECT I.uid, I.ali_id, I.ali_orderno, O.Uid , O.naver_pay_product_code,O.RegDate,O.naver_pay_cancel,O.orderno, O.state, O.ChkDate, O.PAYWAY, I.ali_reorder_chk, D.DeliveryNo \
        from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid \
        where I.ali_chk = '0' and D.DeliveryName is null and D.DeliveryNo is null and D.DeliveryDate is null and O.state in ('201','301','421') \
        AND I.ali_id='" +str(ali_id)+ "'\
        AND DATEDIFF(day,O.RegDate,getdate()) < 60 "

    ins = 0
    cnt = 0
    all_cnt = 0
    proc_rows = db_fs.select(sql)
    if not proc_rows:
        procLogSet(db_fs, gProc_no, "P", ins, "[ " +str(ali_id)+ " ] 송장DB처리 : " +str(cur_Ip), ali_id)
        print(">> (송장) 처리할 데이터가 없습니다. ")
    else:
        all_cnt = len(proc_rows)
        print(">> (송장) 처리할 데이터 : {}".format(all_cnt))

        for ea_ord in proc_rows:
            Iuid = ea_ord[0]
            ali_id = ea_ord[1]
            ali_orderno = ea_ord[2]
            Ouid = ea_ord[3]
            naver_pay_product_code = ea_ord[4]
            RegDate = ea_ord[5]
            naver_pay_cancel = ea_ord[6]
            orderno = ea_ord[7]
            state = ea_ord[8]
            ChkDate = ea_ord[9]
            PAYWAY = ea_ord[10]
            ali_reorder_chk = ea_ord[11]
            db_DeliveryNo = ea_ord[12]
            Pay_orderno = ""
            if naver_pay_product_code is None or naver_pay_product_code == "":
                Pay_orderno = ""
            else:
                Pay_orderno = naver_pay_product_code

            cnt = cnt + 1
            ea_url = "https://www.aliexpress.com/p/tracking/index.html?tradeOrderId=" + str(ali_orderno)

            try:
                driver.get(ea_url)
            except Exception as ex:
                print(">> ea_url Exception : {}".format(ali_orderno))
                # input(">> ")
            else:
                time.sleep(random.uniform(2, 2.5))
                ea_source = driver.page_source
                ea_soup = BeautifulSoup(ea_source,'html.parser')
                if ea_source.find('운송장 번호') > -1:
                    ea_tmp = getparse(ea_source,'운송장 번호','</span>')
                elif ea_source.find('Tracking number') > -1:
                    ea_tmp = getparse(ea_source,'Tracking number','</span>')
                else:
                    if ea_source.find('Haven’t found any thing to follow?') > -1:
                        print(">>({}) (skip) No tracking no : {}".format(cnt, ali_orderno))
                        continue
                    else:
                        print(">>({}) Check Please : {}".format(cnt, ali_orderno))
                        input(">> After Check Input : ")
                        continue

                ea_track = getparse(ea_tmp,'<span>','').strip()
                print(">>({}/{}) [{}] {} ".format(cnt, all_cnt, ali_orderno, ea_track))

                # track no 
                if ea_track == "":
                    try:
                        ea_track = ea_soup.select_one('#root > div > div:nth-child(3) > div:nth-child(2) > div > div > span').get_text()
                    except Exception as ex:
                        print(">>({}) Exception : {}".format(cnt, ali_orderno))
                    else:
                        time.sleep(1)
                        ea_track = ea_track.strip()
                        print(">>({}) [{}] (soup) {} ".format(cnt, ali_orderno, ea_track))

                if ea_track != "":
                    delicode = ea_track
                    # track info (1)
                    track_info = getparse(ea_source,'class="logistic-info--trackWrap--','<div class="tracking-wrap">')
                    track_info = getparse(track_info,'">','')
                    track_info = track_info[:2000].replace("'","")
                    #print(">> [{}] track_info : {} ".format(ali_orderno, track_info))

                    # 송장번호 매칭 택배사명 가져오기 DeliveryUid, DeliveryName, delivery_company 
                    DeliveryUid, DeliveryName, delivery_company = get_track_name(delicode)

                    print(">>({}) [{}] {} | ( {} ) {} | {}".format(cnt, ali_orderno, delicode, DeliveryUid, delivery_company, DeliveryName))
                    if DeliveryUid == "":
                        print(">> No DeliveryUid Check : {}".format(ali_orderno))
                        input(">> No DeliveryUid Check : ")
                    else:
                        dic = dict()
                        dic['ali_orderno'] = "'" + ali_orderno + "'"
                        if naver_pay_product_code is None or naver_pay_product_code == "":
                            pass
                        else:
                            dic['naver_pay_product_code'] = "'" + naver_pay_product_code + "'"
                        dic['DeliveryUid'] = "'" + DeliveryUid + "'"
                        dic['DeliveryNo'] = "'" + delicode + "'"
                        dic['DeliveryName'] = "'" + DeliveryName + "'"
                        dic['delivery_company'] = "'" + delivery_company + "'"
                        dic['updatedate'] = "getdate()"
                        dic['DeliveryContent'] = "'" + track_info + "'"
                        dic['ali_id'] = "'" + ali_id + "'"                     

                        # DB save 
                        sql_g = "select Iuid, isnull(DeliveryNo,''), isnull(flg,'') from ali_delivery_temp where Iuid = '{}'".format(Iuid)
                        row_g = db_fs.selectone(sql_g)
                        if row_g:
                            # DB update 
                            db_iuid = row_g[0]
                            db_DeliveryNo = row_g[1].strip()
                            db_flg = row_g[2].strip()
                            if db_flg == "":
                                if db_DeliveryNo != "":
                                    dic['pre_DeliveryNo'] = "'" + db_DeliveryNo + "'"
                                    dic['pre_DeliveryDate'] = "getdate()"

                                sql_where = " Iuid = '" + str(Iuid) + "'"
                                db_fs.update('ali_delivery_temp', dic, sql_where)  # update       
                            else:
                                print(">>({}) db_DeliveryNo check : {}".format(cnt, ali_orderno))                    
                        else:
                            # DB insert 
                            dic['Iuid'] = Iuid 
                            dic['Ouid'] = Ouid 
                            dic['orderno'] = "'" + orderno + "'"                        

                            db_fs.insert('ali_delivery_temp', dic)  # insert
                            print('##insert## : ali_delivery_temp')
                            ins = ins + 1

        run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/ali_order_delivery_insert_proc_v5.asp?ali_id=" + str(ali_id)
        print(">> 송장처리 asp url 리스트 : {}".format(run_url))
        #chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s"
        webbrowser.open_new_tab(run_url)
        time.sleep(10)

    ### procLogSet(db_fs, gProc_no, "F", ins, "[ " +str(ali_id)+ " ] 송장처리 완료 : " +str(cur_Ip), ali_id)
    return ins

def proc_cancel(driver, db_fs, ali_id, proc_name, set_diff_day):

    # 주문내역 이동 
    order_list1(driver)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    ins = 0
    first_item = 0
    last_item = 10
    add_num = 10
    num = 0
    date_diff_days = 0

    now = datetime.now()
    print(">> Parsing Start --------------------------- ")
    chrom_click('#root > div > div.order-main > div.order-more > button > span', driver)
    print(">> set_diff_day : {}".format(set_diff_day))
    while date_diff_days < set_diff_day:
        time.sleep(2)
        html=driver.page_source
        soup = BeautifulSoup(html,'html.parser')        
        items = soup.select('#root > div > div.order-main > div.order-content > div > div.order-item')[first_item:last_item]
        print(first_item,"~",last_item,">> date diff : ",date_diff_days)
        first_item = first_item + add_num
        last_item = last_item + add_num
        # 10개씩 db 입력
        statuses = []
        orderNos = []
        orderDates = []

        print(">> window.scrollTo  click ")
        try:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight-1300);')
        except:
            print(">> window.scrollTo except .. ")

        time.sleep(2)
        if len(items) == 0:
            break

        for i in items:
            # 상태
            status = i.find('div').find('div').find('span').get_text()

            # 주문번호
            temp0 = i.select_one('div.order-item-header > div.order-item-header-right > div > div:nth-child(2)').get_text()
            cut_position = temp0.find(':')
            orderNo = temp0[cut_position+1:]
            orderNo = orderNo.replace("복사","")
            orderNo = orderNo.replace("copy","")
            orderNo = orderNo.strip()    

            # 주문날짜
            temp = i.select_one('div.order-item-header > div.order-item-header-right > div > div:nth-child(1)').get_text()
            cut_position = temp.find(':')
            orderDate = temp[cut_position+1:]
            orderDate = orderDate.strip()
            if orderDate.find('년') > 0:
                date_to_compare = datetime.strptime(orderDate, '%Y년 %m월 %d일')
            else:
                date_to_compare = datetime.strptime(orderDate, '%b %d, %Y')
            orderDate = date_to_compare.strftime('%Y-%m-%d')
            date_diff = now - date_to_compare

            statuses.append(status)
            orderNos.append(orderNo)
            orderDates.append(orderDate)
            date_diff_days = date_diff.days
            print(">> {} ({}) {} [{}]".format(orderNo, status, orderDate, date_diff_days))

        if len(statuses) < 1:
            print(">> chrom_click (1)")
            elem_finished = "#root > div.order-wrap > div.order-header > div.order-nav > div.comet-tabs > div > div > div:nth-child(5)"
            chrom_click(elem_finished, driver)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
            time.sleep(3)
            continue

        print("\n\n>> db save ")
        # db 저장
        try:
            ins = db_save(db_fs, statuses, orderDates, orderNos, proc_name)
        except Exception as ex:
            print(">> db_save except : ".format(ex))
            input(">> DB save error Check please : ")

        num = num + 1
        try:
            scrollDwon(driver)
        except Exception as ex:
            time.sleep(5)
            print(">> scrollDwon except(1) : ".format(ex))
            try:
                scrollDwon()
            except Exception as ex:
                print(">> scrollDwon except(2) break : ".format(ex))
                break

        time.sleep(1)

    procLogSet(db_fs, gProc_no, "C", ins, "[ " +str(ali_id)+ " ] 송장취소리스트 : " +str(cur_Ip), ali_id)

def track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state):
    if delivery_finish == "1":
        sql_u = "update T_ORDER_DELIVERY set tracking_memo = '{}', delivery_finish = '1', delivery_finish_date = getdate(), tracking_state = '{}' where uid = '{}'".format(track_info, tracking_state, Iuid)
        print(">>({}) [{}] {} : track_info update (배송완료)".format(cnt, ali_orderno, delicode))
    else:
        sql_u = "update T_ORDER_DELIVERY set tracking_memo = '{}', tracking_state = '{}' where uid = '{}'".format(track_info, tracking_state, Iuid)
        print(">>({}) [{}] {} : track_info update (배송중)".format(cnt, ali_orderno, delicode))
    db_fs.execute(sql_u)  # update

# 배송완료(302)로 변경
def delivery_state_change(db_fs, ali_orderno, Ouid):
    ordCnt = 0
    devCnt = 0
    sql_o = " SELECT count(*) as ordCnt from T_ORDER_info as I inner join T_ORDER as O on O.uid=I.OrderUid where O.state='301' and I.OrderUid = '{}'".format(Ouid)
    row_cnt_ord = db_fs.selectone(sql_o)
    if row_cnt_ord:
        ordCnt = row_cnt_ord[0]
    sql_d = " select count(*) as devCnt from T_ORDER_DELIVERY where OrderUid = '{}' and DeliveryNo is not null and delivery_finish = '1' ".format(Ouid)
    row_cnt_dev = db_fs.selectone(sql_d)
    if row_cnt_dev:
        devCnt = row_cnt_dev[0]
    print(">> ordCnt : {} | devCnt : {}".format(ordCnt, devCnt))
    if ordCnt > 0 and ordCnt == devCnt:
        print(">> 배송완료(302)로 변경 : {}".format(ali_orderno))
        sql_u3 = "UPDATE T_ORDER SET state = '302' where uid = '{}' and PAYWAY not in ('Coupang','NaverPay') and state = '301'".format(Ouid)
        print(">> sql_u3 : {} ".format(sql_u3))
        db_fs.execute(sql_u3)
    else:
        print(">> 배송완료(302)로 변경불가 (Skip) : {}".format(ali_orderno))

def tracking_check_log(db_fs, Iuid, Ouid, Reason, ali_orderno, db_DeliveryNo, delicode, RegDate, orderno, PAYWAY, Pay_orderno):

    sql_s = "select OrderNo, reason, proc_state from freeship_tracking_check where InfoUid = '{}'".format(Iuid)
    row_s = db_fs.selectone(sql_s)
    if row_s:
        curr_reason = row_s[1]
        proc_state = row_s[2]
        print(">>curr_reason: {} - Reason : {} | proc_state : {}".format(curr_reason, Reason, proc_state))

        sql_r = " update freeship_tracking_check \
        set ProcDate = getdate(), ali_orderno = '{}', ali_id = '{}', Reason = '{}', pre_trackno = '{}', now_trackno = '{}' \
        where InfoUid = '{}'".format(ali_orderno, ali_id, Reason, db_DeliveryNo, delicode, Iuid )
        print(">> Reson :({}) 변경 : {}".format(Reason, ali_orderno))
        db_fs.execute(sql_r)
    else:
        sql_r = " insert into freeship_tracking_check \
            ( ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, InfoUid, pre_trackno, now_trackno ) \
            values ( getdate(),'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(RegDate, orderno, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, Iuid, db_DeliveryNo, delicode)
        print(">> Reson :({}) 추가 : {}".format(Reason, ali_orderno))
        db_fs.execute(sql_r)


def proc_finishCheck(driver, db_fs, ali_id, sel_kbn):
    if sel_kbn == "1":
        sql = "SELECT I.uid, I.ali_id, I.ali_orderno, O.Uid , O.naver_pay_product_code,O.RegDate,O.naver_pay_cancel,O.orderno, O.state, O.ChkDate, O.PAYWAY, I.ali_reorder_chk, D.DeliveryNo, isnull(D.after_trackno,''), D.DeliveryUid \
        from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid \
        where I.ali_chk = '1' and D.DeliveryNo is not null and D.DeliveryDate >= getdate() - 6 and D.DeliveryDate < getdate() - 2 and O.state = '301' \
        AND delivery_finish is null and I.ali_id='" +str(ali_id)+ " and O.payway = 'NaverPay' and left(D.DeliveryNo,3) = 'CNG' and isnull(D.after_trackno,'') = '''\
        order by D.DeliveryDate asc "
    else:
        sql = "SELECT I.uid, I.ali_id, I.ali_orderno, O.Uid , O.naver_pay_product_code,O.RegDate,O.naver_pay_cancel,O.orderno, O.state, O.ChkDate, O.PAYWAY, I.ali_reorder_chk, D.DeliveryNo, isnull(D.after_trackno,''), D.DeliveryUid \
        from T_ORDER_info I inner join T_ORDER_DELIVERY D on I.Uid=D.Uid inner join T_ORDER O on O.uid=D.OrderUid \
        where I.ali_chk = '1' and D.DeliveryNo is not null and D.DeliveryDate > getdate() - 60 and D.DeliveryDate < getdate() - 5 and O.state = '301' \
        AND delivery_finish is null and I.ali_id='" +str(ali_id)+ "'\
        order by D.DeliveryDate asc "

    ins = 0
    cnt = 0
    all_cnt = 0
    proc_rows = db_fs.select(sql)
    if not proc_rows:
        print(">> (송장 배송중상태 주문건) 처리할 데이터가 없습니다. (sel_kbn:"+str(sel_kbn)+")")
        finish_flg = "1"
    else:
        all_cnt = len(proc_rows)
        print(">> (송장 배송중상태 주문건) 처리할 데이터 (sel_kbn:"+str(sel_kbn)+"): {}".format(all_cnt))

        for ea_ord in proc_rows:
            Iuid = ea_ord[0]
            ali_id = ea_ord[1]
            ali_orderno = ea_ord[2]
            Ouid = ea_ord[3]
            naver_pay_product_code = ea_ord[4]
            RegDate = ea_ord[5]
            naver_pay_cancel = ea_ord[6]
            orderno = ea_ord[7]
            state = ea_ord[8]
            ChkDate = ea_ord[9]
            PAYWAY = ea_ord[10]
            ali_reorder_chk = ea_ord[11]
            db_DeliveryNo = ea_ord[12]
            after_trackno = ea_ord[13]
            db_DeliveryUid= ea_ord[14]

            delivery_finish = "0"
            delivery_cancel = "0"
            Pay_orderno = ""
            if naver_pay_product_code is None or naver_pay_product_code == "":
                Pay_orderno = ""
            else:
                Pay_orderno = naver_pay_product_code

            cnt = cnt + 1
            ea_url = "https://www.aliexpress.com/p/tracking/index.html?tradeOrderId=" + str(ali_orderno)

            try:
                driver.get(ea_url)
            except Exception as ex:
                print(">> Exception : {}".format(ali_orderno))
                # input(">> ")
            else:
                time.sleep(random.uniform(2.5, 4))
                ea_source = driver.page_source
                ea_soup = BeautifulSoup(ea_source,'html.parser')
                if ea_source.find('운송장 번호') > -1:
                    ea_tmp = getparse(ea_source,'운송장 번호','</span>')
                elif ea_source.find('Tracking number') > -1:
                    ea_tmp = getparse(ea_source,'Tracking number','</span>')
                else:
                    if ea_source.find('Haven’t found any thing to follow?') > -1:
                        print(">>({}) (skip) No tracking no : {}".format(cnt, ali_orderno))
                        continue
                    else:
                        print(">>({}) Check Please : {}".format(cnt, ali_orderno))
                        # input(">> After Check Input : ")
                        continue

                track_info = ""
                ea_track = getparse(ea_tmp,'<span>','').strip()
                print(">>({}/{}) [{}] {} ".format(cnt, all_cnt, ali_orderno, ea_track))

                # track no 
                if ea_track == "":
                    try:
                        ea_track = ea_soup.select_one('#root > div > div:nth-child(3) > div:nth-child(2) > div > div > span').get_text()
                    except Exception as ex:
                        print(">>({}) Exception : {}".format(cnt, ali_orderno))
                    else:
                        time.sleep(1)
                        ea_track = ea_track.strip()
                        print(">>({}) [{}] (soup) {} ".format(cnt, ali_orderno, ea_track))

                if ea_track != "":
                    delicode = ea_track
                    # track info (1)
                    tracking_state = ""
                    track_info = getparse(ea_source,'class="logistic-info--trackWrap--','<div class="tracking-wrap">')
                    track_info = getparse(track_info,'">','')
                    track_info = track_info[:2000].replace("'","")
                    #print(">> [{}] track_info : {} ".format(ali_orderno, track_info))
                    if track_info.find('상품 배송 완료') > -1:
                        delivery_finish = "1"
                        tracking_state = "배송완료"
                    elif track_info.find('발송이 취소') > -1:
                        delivery_cancel = "1"
                        tracking_state = "발송취소" 
                    elif track_info.find('통관') > -1:
                        tracking_state = "통관중"
                    else:
                        tracking_state = "배송중"
    
                    if delivery_cancel == "1":
                        # freeship_tracking_check 로그 기록 
                        Reason = "shipping_accident" # 배송취소
                        tracking_check_log(db_fs, Iuid, Ouid, Reason, ali_orderno, db_DeliveryNo, delicode, RegDate, orderno, PAYWAY, Pay_orderno)                                           

                        track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state)
                        print(">>({}) [{}] {} : 발송 취소 ".format(cnt, ali_orderno, delicode))
                    elif str(db_DeliveryNo).strip() == str(delicode).strip():
                        # 트래킹번호 같음 (정상)
                        track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state)
                        print(">>({}) [{}] {} : 송장 변경없음 ".format(cnt, ali_orderno, delicode))
                    else:
                        ins = ins + 1
                        if str(after_trackno).strip() == str(delicode).strip():
                            print(">>({}) 송장 변경 [{}] after_trackno 같음 (skip) : {} | {}".format(cnt, ali_orderno, after_trackno, delicode))
                            track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state)
                        elif after_trackno != "":
                            print(">>({}) 송장 변경 [{}] after_trackno 있음 (skip) : {} | {}".format(cnt, ali_orderno, after_trackno, delicode))
                            track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state)
                        else:
                            # (변경) 송장번호 매칭 택배사명 가져오기 DeliveryUid, DeliveryName, delivery_company 
                            DeliveryUid, DeliveryName, delivery_company = get_track_name(delicode)

                            if DeliveryUid == "":
                                print(">> (변경 송장) No DeliveryUid Check : {}".format(ali_orderno))
                            elif str(db_DeliveryUid) != "29" and str(DeliveryUid) == "29":
                                print(">>({}) 송장 변경 [{}] 일반우편이 아닌송장에서 일반우편으로 변경불가 (skip) : {} | {}".format(cnt, ali_orderno, after_trackno, delicode))
                                track_info_change(db_fs, cnt, ali_orderno, delicode, track_info, Iuid, delivery_finish, tracking_state)
                            else:
                                if delivery_finish == "1":
                                    # DB (T_ORDER_DELIVERY) Update
                                    sql_u2 = "update T_ORDER_DELIVERY set pre_trackno = '{}', DeliveryNoChangeDate = getdate(), \
                                        DeliveryNo = '{}', DeliveryUid = '{}', DeliveryName = '{}', tracking_memo = '{}', delivery_finish = '1', delivery_finish_date = getdate() \
                                        where uid = '{}'".format(db_DeliveryNo, delicode, DeliveryUid, DeliveryName, track_info, Iuid)
                                    #print(">> sql_u2 : {}".format(sql_u2))
                                    print(">>({}) 송장 변경 [{}] {} ==> {} | ( {} ) {} | {} (배송완료)".format(cnt, ali_orderno, db_DeliveryNo, delicode, DeliveryUid, delivery_company, DeliveryName))
                                    db_fs.execute(sql_u2)  # update
                                else:
                                    # DB (T_ORDER_DELIVERY) Update
                                    sql_u2 = "update T_ORDER_DELIVERY set pre_trackno = '{}', DeliveryNoChangeDate = getdate(), \
                                        DeliveryNo = '{}', DeliveryUid = '{}', DeliveryName = '{}', tracking_memo = '{}' \
                                        where uid = '{}'".format(db_DeliveryNo, delicode, DeliveryUid, DeliveryName, track_info, Iuid)
                                    #print(">> sql_u2 : {}".format(sql_u2))
                                    print(">>({}) 송장 변경 [{}] {} ==> {} | ( {} ) {} | {} (배송중)".format(cnt, ali_orderno, db_DeliveryNo, delicode, DeliveryUid, delivery_company, DeliveryName))
                                    db_fs.execute(sql_u2)  # update

                                # freeship_tracking_check 로그 기록 
                                if ali_reorder_chk == "1" and PAYWAY == "NaverPay":
                                    Reason = "re_order" # 재주문
                                    tracking_check_log(db_fs, Iuid, Ouid, Reason, ali_orderno, db_DeliveryNo, delicode, RegDate, orderno, PAYWAY, Pay_orderno)
                                else:
                                    Reason = "mismatchtracking" # 송장 변경
                                    tracking_check_log(db_fs, Iuid, Ouid, Reason, ali_orderno, db_DeliveryNo, delicode, RegDate, orderno, PAYWAY, Pay_orderno)

                    if delivery_finish == "1":
                        if PAYWAY == "NaverPay" or PAYWAY == "Coupang":
                            print(">> {} 배송완료처리 (skip) : {}".format(PAYWAY, ali_orderno))
                        else:
                            delivery_state_change(db_fs, ali_orderno, Ouid)

    procLogSet(db_fs, gProc_no, "D", ins, "[ " +str(ali_id)+ " ] 송장(배송중)체크 완료 (sel_kbn:" +str(sel_kbn)+ ") : " +str(cur_Ip), ali_id)


if __name__ == '__main__':

    print('\n [--- main start ---] ' + str(datetime.now()))
    ip = socket.gethostbyname(socket.getfqdn())
    ip_pos = ip.rfind(".")
    print(ip[ip_pos+1:])

    gProc_no = "delivery"
    db_fs = DBmodule_FR.Database('freeship')
    proc_cnt = 0

    if str(cur_Ip).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')

    # 설정 시간후 종료 fun_timer
    # timecount = 0
    # print(">> fun_timer Start ")
    # fun_timer()

    delivery_flg = "0"
    row = db_fs.selectone("select top 1 proc_name, ali_id, login_id, login_pw, isnull(set_diff_day,0) from ali_order_auto_set where login_ip = '{}'".format(ip))
    if not row:
        procLogSet(db_fs, gProc_no, "E", "0", " 송장처리 설정 정보 확인필요 : " +str(cur_Ip), "")
    else:
        proc_name = row[0]
        ali_id = row[1]
        input_id = row[2]
        input_pw = row[3]
        set_diff_day = row[4]
        procLogSet(db_fs, gProc_no, "A", "0", "[ " +str(ali_id)+ " ] 송장 처리 : " +str(cur_Ip), ali_id)

    procLogSetAli(db_fs, gProc_no, "S", "0", "[ " +str(ali_id)+ " ] 시작 : " +str(cur_Ip), ali_id)
    proc_id = ""
    url="https://ko.aliexpress.com/"
    try:

        try:
            print(">> chrom_drive ...")
            driver, proc_id = chrom_drive()
            driver.get(url)
            time.sleep(3)
        except Exception as ex:
            print(">> connectDriverOld ...")
            driver = connectDriverOld(url, "")
            driver.get(url)
            time.sleep(3)

        # 로그인 및 KRW Set
        # 로그인 및 USD Set 
        login_set_proc(driver, input_id, input_pw)

        time.sleep(1)
        # 주문내역 이동 
        order_list1(driver)

    except Exception as ex:
        print(ex)
        log = traceback.format_exc()
        print(traceback.format_exc())
        f = open("error_log.txt","w")
        f.write(log)
        f.close()

        input(">> After login order_page(2) : ")
        # 주문내역 이동 
        order_list2(driver)

    now = datetime.now()
    print(">> Parsing Start --------------------------- ")
    chrom_click('#root > div > div.order-main > div.order-more > button > span', driver)

    ####################################################################
    deliveryIns = 0
    print('\n\n>> 송장 작업 시작 --------------------------------')
    deliveryIns = proc_delivery(driver, db_fs, ali_id)
    print('>> 송장 작업 완료 --------------------------------')

    ####################################################################
    print('\n\n>> 송장 배송중상태 주문건 체크 시작 --------------------------------')
    print('\n\n>> 송장 배송중상태 주문건 체크 (1)')
    proc_finishCheck(driver, db_fs, ali_id, "1")
    print('\n\n>> 송장 배송중상태 주문건 체크 (2)')
    proc_finishCheck(driver, db_fs, ali_id, "2")
    print('>> 송장 배송중상태 주문건 체크 종료 --------------------------------')

    ####################################################################
    print('\n\n>> 송장 취소 및 환불건 작업 시작 --------------------------------')
    if set_diff_day == 0 or set_diff_day is None:   set_diff_day = 30
    proc_cancel(driver, db_fs, ali_id, proc_name, set_diff_day)
    print('>> 주문 취소리스트 작업 완료 --------------------------------')
    ####################################################################

    procLogSet(db_fs, gProc_no, "F", deliveryIns, "[ " +str(ali_id)+ " ] 송장처리 완료 : " +str(cur_Ip), ali_id)
    print("\n\n>> 작업 완료 ")
    now = datetime.now()
    print(now)

    time.sleep(10)
    try:
        driver.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")

    procLogSetAli(db_fs, gProc_no, "F", "0", "[ " +str(ali_id)+ " ] 종료 : " +str(cur_Ip), ali_id)
    db_fs.close()
    os._exit(0)


