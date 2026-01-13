from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import socket
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
import DBmodule_FR
import os
global ver
ver = "2.0"
print(">> ver : {}".format(ver))
global gProc_no
global timecount

# import clipboard
def chrom_drive():
    proc_id = ""
    try:
        proc_id = subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        proc_id = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
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
    return driver, proc_id 


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


def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)


def db_save(db_fs, statuses, orderDates, orderNos, proc_name):
    # db 저장
    for a_status, b_date, c_orderno in zip(statuses,orderDates,orderNos):
        if a_status == "완료":
            print(">> statuses : {} | orderNos : {} 완료상태 스킵".format(a_status, c_orderno))
            continue

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


if __name__ == '__main__':

    print('>> gmail get test ')
    print('\n [--- main start ---] ' + str(datetime.now()))
    cur_Ip = socket.gethostbyname(socket.gethostname())    
    ip = socket.gethostbyname(socket.getfqdn())
    ip_pos = ip.rfind(".")
    print(ip[ip_pos+1:])

    gProc_no = "ALI_DELIVERY"
    db_fs = DBmodule_FR.Database('freeship')
    proc_cnt = 0
    procLogSet(db_fs, gProc_no, "A", "0", "(알리 송장) 실행 : " +str(cur_Ip))

    if str(cur_Ip).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')

    # 설정 시간후 종료 fun_timer
    timecount = 0
    print(">> fun_timer Start ")
    fun_timer()

    row = db_fs.selectone("select top 1 * from ali_order_auto_set where login_ip = '{}'".format(ip))
    proc_id = ""
    try:
        proc_name = row[0]
        ali_id = row[1]
        input_id = row[2]
        input_pw = row[3]

        driver, proc_id = chrom_drive()    
        url="https://ko.aliexpress.com/"
        driver.get(url)
        time.sleep(3)

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
            # try:
            #     chrom_click('#switcher-info', driver)
            #     time.sleep(1)    
            #     try:
            #         chrom_click('#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div.switcher-sub.notranslate > div > div.switcher-currency.item.util-clearfix > div', driver)
            #     except:
            #         chrom_click('#switcher-info > span.language_txt', driver)
            #         time.sleep(1)    
            #         chrom_click('#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div.switcher-sub.notranslate > div > div.switcher-currency.item.util-clearfix > div', driver)
            #     time.sleep(1)    
            #     chrom_click('a[data-currency="USD"]', driver)
            #     time.sleep(1)
            #     chrom_click('#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div.switcher-sub.notranslate > div > div.switcher-btn.item.util-clearfix > button', driver)
            # except:
            #     chrom_click('ship-to--text--3H_PaoC', driver)
            #     time.sleep(1)
            #     chrom_click('#_global_header_23_ > div > div > div.pc-header--right--2cV7LB8 > div.pc-header--rightWrap--HYqeULJ > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(8) > div', driver)
            #     time.sleep(1)
            #     chrom_click('div[data-spm-anchor-id="a2g0o.home.header.i2.6c2f4430bE401v"]', driver)
            #     time.sleep(1)
            #     chrom_click('#_global_header_23_ > div > div > div.pc-header--right--2cV7LB8 > div.pc-header--rightWrap--HYqeULJ > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div.es--saveBtn--w8EuBuy', driver)

        time.sleep(1)  
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

        ## 알리주문내역 (완료)
        # elem_finished = "#root > div > div.order-header > div.order-nav > div.comet-tabs > div > div > div:nth-child(5)"
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
                print(">> order page except .. ")

    except Exception as ex:
        print(ex)
        log = traceback.format_exc()
        print(traceback.format_exc())
        f = open("error_log.txt","w")
        f.write(log)
        f.close()

        input(">> After login order_page(2) : ")
        try:
            chrom_click(elem_finished, driver)
            time.sleep(5)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
        except:
            print(">> order page except .. ")
        time.sleep(2)
        if str(driver.page_source).find('class="order-main"') == 0:
            input(">> After login order_page(3) : ")
            time.sleep(1)
            try:
                chrom_click(elem_finished, driver)
                time.sleep(5)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
            except:
                print(">> order page except .. ")

    first_item = 0
    last_item = 10
    add_num = 10
    num = 0
    date_diff_days = 0

    now = datetime.now()
    print(">> Parsing Start --------------------------- ")
    chrom_click('#root > div > div.order-main > div.order-more > button > span', driver)
    while date_diff_days < 60:
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
            chrom_click(elem_finished, driver)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item")))
            time.sleep(3)
            continue

        print("\n\n>> db save ")
        # db 저장
        try:
            db_save(db_fs, statuses, orderDates, orderNos, proc_name)
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

    #### else:
    print('>> 주문 취소리스트 작업 완료 --------------------------------')
    time.sleep(1)
    print(">> 주문 페이지 이동 --------------------------------")
    try:
        driver.get("https://trade.aliexpress.com/orderList.htm")
    except:
        driver.refresh()
    time.sleep(1)
    try:
        driver.get("https://trade.aliexpress.com/issue/issue_list.htm")
    except:
        driver.refresh() 
    time.sleep(1)
    driver.get("https://trade.aliexpress.com/orderList.htm")

    # 쿠키 가져오기
    cookies=driver.get_cookies()
    ali_cookie=""
    for cookie in cookies[:-1]:
        ali_cookie=ali_cookie+cookie["name"]
        ali_cookie=ali_cookie+"="
        ali_cookie=ali_cookie+cookie["value"]
        ali_cookie=ali_cookie+";"
    ali_cookie=ali_cookie+cookies[-1]["name"]+"="+cookies[-1]["value"]

    url="http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/ali_order_delivery_insert_page.asp"
    driver.get(url)
    time.sleep(3)
    insert_cookie=driver.find_element(By.CSS_SELECTOR,"body > form > textarea")
    insert_cookie.click()
    time.sleep(1)
    driver.execute_script("document.getElementsByName('cookies')[0].value = '{}';".format(ali_cookie))

    print(ali_cookie)
    now = datetime.now()
    print(now)
    time.sleep(1)
    driver.execute_script("document.querySelector('body > form > input[type=submit]:nth-child(5)').click();")
    print(">> 작업 완료 ")
    now = datetime.now()
    print(now)
    #time.sleep(10)

    db_fs.close()
    end_chk = "0"
    today = str(datetime.now())[:10]
    while end_chk == "0":
        time.sleep(60)
        sql = "select idx from auto_proc_log where ali_id = '{}' and regdate > '{} 00:00:00' and proc_state = 'F'".format(ali_id, today)
        row_log = db_fs.selectone
        if row_log:
            end_chk = "1"
            print(">> {} 송장처리 완료 확인종료 ")
            break

    try:
        driver.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)

