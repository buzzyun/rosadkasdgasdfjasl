from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# import pyautogui as pg
import socket
from pymssql import _mssql
from pymssql import _pymssql
import traceback
from bs4 import BeautifulSoup
import sys,os
p = os.path.abspath('.')
sys.path.insert(1, p)
from dbCon import dbconfig
from datetime import datetime
# import clipboard

def chrom_drive():
    try:
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
    option = Options()
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    driver.implicitly_wait(5) 
    driver.set_page_load_timeout(3600)
    return driver    
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome("C:\\Users\\allin\\Desktop\\ali_login\\chromedriver.exe",
    #                       options=chrome_options)    
    # driver.implicitly_wait(5)
    # driver.set_page_load_timeout(3600)
    # return driver

def chrom_click(selector, driver):
    driver.find_element_by_css_selector(selector).click()
    time.sleep(1)
    print(selector,"클릭")
    
def chrom_write(selector, driver, write):
    lst = list(write)
    for i in lst:
        driver.find_element_by_css_selector(selector).send_keys(i)
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("pwnbit.kr", 443))
ip = sock.getsockname()[0]
ip_pos = ip.rfind(".")
print(ip[ip_pos+1:])

cnxn = dbconfig.DBconnect("freeship","EUC-KR")
cursor = cnxn.cursor()

cursor.execute("select top 1 * from ali_order_auto_set where login_ip = %s",ip)

row = cursor.fetchone()
cursor.close()
cnxn.close()  

try:
    proc_name = row[0]
    ali_id = row[1]
    input_id = row[2]
    input_pw = row[3]
    # input_id = "quwel@naver.com"
    # input_pw = "tnsdhr12"   
    
    driver = chrom_drive()    

    url="https://ko.aliexpress.com/"
    driver.get(url)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "index-page"))
    )
    print("팝업 확인")
    chk_pop = PopUpChk("pop-close-btn")
    if chk_pop == "":
        chk_pop = PopUpChk("btn-close")

    if chk_pop:
        print("팝업 닫기")
        chk_pop.click()
    time.sleep(1)
    # 마우스 커서 어카운트에 위치
    some_tag=driver.find_element_by_css_selector("#nav-user-account > span > a")
    ActionChains(driver).move_to_element(some_tag).perform()
    # sign in 클릭
    # #nav-user-account > div > ul > li:nth-child(1) > a
    time.sleep(1)
    try:
        chrom_click("#nav-user-account > div > div > p.flyout-bottons > a.sign-btn", driver)#error
        
        # 아이디, 패스워드 입력
        chrom_click("#fm-login-id", driver)    
        chrom_write("#fm-login-id", driver, input_id)
        chrom_write("#fm-login-password", driver, input_pw)
        try:
            chrom_click("#batman-dialog-wrap > div > div > div.cosmos-tabs > div.cosmos-tabs-container > div > div > button.cosmos-btn.cosmos-btn-primary.cosmos-btn-large.cosmos-btn-block.login-submit > span", driver)
        except:
            chrom_click("#batman-dialog-wrap > div > div.fm-tabs-content > div > div > button", driver)
    except:
        print("로그인 중")
    # element = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "account-main"))
    # )
    time.sleep(1)
    try:
        chk_pop = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.btn-close"))
        )
        chk_pop = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(17) > div > div > img.btn-close"))
        )        
    except:
        print("없음")
        chk_pop=""

    if chk_pop:
        chk_pop.click()
    time.sleep(1)  
    url="https://www.aliexpress.com/p/order/index.html"
    try:
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item"))
        )
    except:
        driver.get("https://ko.aliexpress.com/")
        time.sleep(1)
        driver.get("https://trade.aliexpress.com/orderList.htm")
        # driver.refresh()
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item"))
        )
        
    chrom_click('#root > div > div.order-header > div.order-nav > div.comet-tabs > div > div > div:nth-child(5)', driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "page-menu-item"))
    )
    time.sleep(1)
    
    first_item = 0
    last_item = 10
    add_num = 10
    
    num = 0
    date_diff_days = 0

    now = datetime.now()
    while date_diff_days < 60:
        html=driver.page_source
        soup = BeautifulSoup(html,'html.parser')        
        items = soup.select('#root > div > div.order-main > div.order-content > div > div.order-item')[first_item:last_item]
        print(first_item,"~",last_item,"date diff : ",date_diff_days)
        first_item = first_item + add_num
        last_item = last_item + add_num
        # 10개씩 db 입력
        statuses = []
        orderNos = []
        orderDates = []
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
        # db 저장
        try:
            cnxn = dbconfig.DBconnect("freeship","UTF-8")
            cursor = cnxn.cursor()
            for a, b, c in zip(statuses,orderDates,orderNos):
                if a=="완료":
                    print("statuses : ",a, "orderNos : ",c," 완료상태 스킵")
                    continue
                cnxn2 = dbconfig.DBconnect("freeship","UTF-8")
                cursor2 = cnxn2.cursor()
                sql2 = "select ali_orderNO from ali_orderCancel where ali_orderNO = %s"
                cursor2.execute(sql2,c)
                row = cursor2.fetchone()
                if not row:
                    sql = "insert into ali_orderCancel(status, orderDate, ali_orderNo, regdate, ali_id, proc_name) values(%s, %s, %s, getdate(), %s, %s)"
                    val = a, b, c, ali_id, proc_name
                    cursor.execute(sql, val)
                    cnxn.commit()
                    print("statuses : ",a, "orderNos : ",c," 저장 완료")
                else:
                    sql = "update ali_orderCancel set status = %s, orderDate = %s, regdate = getdate(), ali_id = %s, proc_name = %s where ali_orderNo = %s"
                    val = a, b, ali_id, proc_name, c
                    cursor.execute(sql, val)
                    cnxn.commit()
                    print("statuses : ",a, "orderNos : ",c," 업데이트 완료")
                cursor2.close()
                cnxn2.close()        
            cursor.close()
            cnxn.close() 
        except Exception as ex:
            print(ex)
            cursor2.close()
            cnxn2.close()            
            cursor.close()
            cnxn.close()

        num = num + 1   
        try:         
            chrom_click('#root > div > div.order-main > div.order-more > button > span', driver)
        except:
            driver.execute_script("document.getElementsByClassName('comet-btn comet-btn-large comet-btn-borderless')[0].click();")
        time.sleep(1)        
    else:
        print('주문 취소리스트 작업 완료')
        time.sleep(1)
        print("주문 페이지 이동")
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
        
        # some_tag=driver.find_element_by_css_selector("#nav-user-account > span > a")
        # ActionChains(driver).move_to_element(some_tag).perform()    
        # chrom_click("#nav-user-account > div > ul > li:nth-child(1) > a", driver)
        # element = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "me-left-menu"))
        # )    
        # time.sleep(1)
        # chrom_click("#page-content > div > div > div.col-xs-12 > div:nth-child(1) > div > div > p:nth-child(2) > a", driver)
    
        # element = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "me-left-menu"))
        # )    
        # time.sleep(1)
        # chrom_click("#page-content > div > div > div.col-xs-12 > div:nth-child(1) > div > div > p:nth-child(1) > a", driver)
    
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
        # url="https://www.naver.com/"
        # clipboard.copy(ali_cookie)
        driver.close()
        driver2 = chrom_drive()
        driver2.get(url)
        time.sleep(3)
        insert_cookie=driver2.find_element_by_css_selector("body > form > textarea")
        insert_cookie.click()
        time.sleep(1)
        driver2.execute_script("document.getElementsByName('cookies')[0].value = '{}';".format(ali_cookie))
        # ActionChains(driver2).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        # insert_cookie.send_keys(ali_cookie)
        print(ali_cookie)
        now = datetime.now()
        print(now)
        time.sleep(1)
        # chrom_click("body > form > input[type=submit]:nth-child(5)", driver2)
        driver2.execute_script("document.querySelector('body > form > input[type=submit]:nth-child(5)').click();")
        print("완료")
        now = datetime.now()
        print(now)
        driver2.close()
except Exception as ex:
    cursor.close()
    cnxn.close()     
    print(ex)
    log = traceback.format_exc()
    print(traceback.format_exc())
    f = open("error_log.txt","w")
    f.write(log)
    f.close()
finally:
    cursor.close()
    cnxn.close()