import datetime
import os
import random
import socket
import socks
import http.client
import urllib
from urllib.request import Request, urlopen
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import chromedriver_autoinstaller
import time
from dbCon import DBmodule_FR

global page
global ip
global pagecount
global timecount
global chkTime
global ver
global endpage
global errCnt

ver = "1.0"

ip = socket.gethostbyname(socket.gethostname())
amzurl = ""
timecount = 0
db_con = DBmodule_FR.Database('shop')
chkTime = time.time()
print("chkTime : "+str(chkTime))

def connectDriver(tool):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    if tool == 'chrome':
        time.sleep(1)
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        # 크롤링 방지 설정을 undefined로 변경 
        #browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 
    elif tool == 'brave':
        #path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("window-size=1400x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    elif tool == 'Firefox':
        path = "C:\Project\cgeckodriver.exe"
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9150)
        profile.update_preferences()
        browser = webdriver.Firefox(profile, executable_path=path)
    return browser

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

#rfind 파싱함수
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

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip address :', response.read())

def set_new_ip():
    print('>> set_new_ip')
    # disable socks server and enabling again
    socks.setdefaultproxy()
    # """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)

def version_check(in_drive):
    global ver
    print("version:" + ver)
    file_path = r"c:/project/"
    file_name = "new_shop_asin.exe"
    sql = "select version, url from python_version_manage where name = 'list'"
    print("sql:" + sql)
    rows = db_con.selectone(sql)
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        print("New version Download :" + str(version_url) + " | "+ str(file_path + file_name))
        time.sleep(30)
        print("time.sleep(30)")
        print("New version update exit")

        db_con.close()
        in_drive.quit()
        time.sleep(2)
        os._exit(1)

def moveScroll(driver):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 1200
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(1)
        # 끝까지 스크롤 다운
        print(">> moveScroll : {}".format(sroll_cnt))
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > 9:
            break
        last_height = new_height

def loginProc_new(in_driver, in_login_id, in_password):
    time.sleep(1)
    print('>> loginProc_new ')

    wait = WebDriverWait(in_driver, 30)
    id_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id"))) 
    id_input.send_keys(in_login_id) 
    print('>> ID OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    pw_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-password"))) 
    pw_input.send_keys(in_password) 
    print('>> pass OK ')
    time.sleep(2)
    wait = WebDriverWait(in_driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fm-button"))).click()
    print('>> click OK ')
    time.sleep(4)


def procDbSet(in_asin, in_cateidx, in_price, db_con):
    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        #sql = "insert into T_Category_BestAsin (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(in_cateidx) + "','" + str(in_price) + "',getdate()) "
        sql = "insert into T_Category_BestAsin (asin, cate_idx, reg_date) values ('{}', '{}', getdate())".format(in_asin,in_cateidx)
        # print('sql :'+str(sql))
        db_con.execute(sql)

    else:
        print('>> T_Category_BestAsin (Update)')
        #sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(in_asin) + "'"
        sql = "update T_Category_BestAsin set up_date = GETDATE() where asin='" + str(in_asin) + "'"
        # print('sql :'+str(sql))
        db_con.execute(sql)

    return "0"

def proc_asin(browser, catecode):
    cnt = 0
    rtn_value = "0"
    result = browser.page_source
    result_source_tmp = getparse(str(result),'class="cate1688-offer','class="channel-common-footer"')
    sp_list_tmp = str(result_source_tmp).split('class="cate1688-offer')
    if len(sp_list_tmp) > 20:
        moveScroll(browser)
        time.sleep(3)
        print('>> time.sleep(3) ')
    else:
        if str(result_source_tmp).find('<span class="alife-bc-uc-number">') > -1:
            print('>> Show 1688 Parsing 20이하 ')
        else:
            print('>> Show 1688 Parsing Check Please. ')

    result = browser.page_source
    time.sleep(3)
    print('>> time.sleep(3) ')
    #with open("soup_asin_1688.html","w",encoding="utf8") as f: 
    #    f.write(str(result))

    if str(result).find('class="cate1688-offer') > -1:
        print('>> Show 1688 Parsing ')
        result_source = getparse(str(result),'class="cate1688-offer','class="channel-common-footer"')
        if str(result_source).find('class="cate1688-offer') > -1:
            sp_list = str(result_source).split('class="cate1688-offer')
            for ea_item in sp_list:
                if str(ea_item).find('id="') > -1:
                    asin = getparse(str(ea_item),'id="','"')
                    price = getparse(str(ea_item),'<span class="alife-bc-uc-number">','</span>')
                    price = str(price).replace('￥','').replace(',','').strip()
                    if asin != "" and price != "":
                        cnt = cnt + 1
                    if str(asin) == "":
                        print('>> no asin (Skip) ' + str(asin))
                    elif len(asin) > 13:
                        print('>> over len(asin) (Skip) ' + str(price))
                    elif str(price) == "" or str(price) == "0":
                        print('>> no price (Skip) ' + str(price))
                    else:
                        price = str(price).replace('&nbsp;', '').replace('$', '').replace('USD', '').replace('+', '').replace('-', '').replace(',', '').replace('\xa0','').replace("'", '').strip()
                        print(">> ({}) [catecode : {}] {} | {} | (DB In) ".format(cnt, catecode, asin, price))
                        # DB 입력
                        procDbSet(asin, catecode, price, db_con)
    else:
        print('>> Show 1688 Parsing ( No Parsing )')
        rtn_value = "1"

    return rtn_value

def doProcDetail(browser, catecode, endPage):
    cnt = 0
    time.sleep(1)
    print('>> time.sleep(1) ')
    price_from = 1
    price_to = 20
    endprice = 300 # default
    endprice = int(endPage)
    check_cnt = 0
    while price_to <= endprice:
        if price_to == endprice:
            price_to = price_to + 200
        print(">> catecode : {} | price_from : {} | price_to : {}".format(catecode, price_from,price_to))
        browser.find_element_by_css_selector('li.price > div.price-from > span > input[type=text]').send_keys(str(price_from))
        time.sleep(1)
        browser.find_element_by_css_selector('li.price > div.price-end > span > input[type=text]').send_keys(str(price_to))
        time.sleep(2)
        browser.find_element_by_css_selector('li.price > div.price-confirmBtns > button.next-btn.next-btn-warning.next-btn-normal.next-btn-medium.confirm').click()
        time.sleep(6)

        result = browser.page_source
        if str(result).find('TB14rnLDgHqK1RjSZFkXXX.WFXa-340-308.png') > -1:
            print(">> Page View Error : TB14rnLDgHqK1RjSZFkXXX.WFXa-340-308.png ")
            check_cnt = check_cnt + 1
            browser.find_element_by_css_selector('li:nth-child(2) > button').click()
            time.sleep(6)
        else:
            check_cnt = 0

        if check_cnt > 3:
            print(">> check_cnt 3 over (End) ")
            break
        proc_asin(browser, catecode)

        price_from = price_from + 20
        price_to = price_to + 20
        time.sleep(1)
        browser.find_element_by_css_selector('li.price > div.price-from > span > input[type=text]').send_keys(Keys.CONTROL + "a")
        time.sleep(1)
        browser.find_element_by_css_selector('li.price > div.price-from > span > input[type=text]').send_keys(Keys.DELETE)
        time.sleep(1)
        browser.find_element_by_css_selector('li.price > div.price-end > span > input[type=text]').send_keys(Keys.CONTROL + "a")
        time.sleep(1)
        browser.find_element_by_css_selector('li.price > div.price-end > span > input[type=text]').send_keys(Keys.DELETE)
        time.sleep(5)
        cnt = cnt + 1

    return str(cnt)

def doProcShow(browser, endPage):
    catecode = ""
    rtn_value = "0"
    rtnCnt = 0
    sql = "SELECT top 1 a.catecode, kor_name, a.amz_cateurl, cate_kbn FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate='1' and cate_kbn is null and b.catecode is null order by up_date asc "
    row = db_con.selectone(sql)
    if row:
        catecode = row[0]
        kor_name = row[1]
        amz_cateurl = row[2]
        cate_kbn = row[3]
        print("\n\n")
        print(">>--------------------------------------------------------------------------------------------------------------------------------------------")
        print(">> ( {} ) {} | {} | {}".format(catecode, kor_name, amz_cateurl, cate_kbn))
        print(">>--------------------------------------------------------------------------------------------------------------------------------------------")

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        rowUP = db_con.selectone(sql)
        if rowUP:
            sql = " update update_list set catecode = '{}', amz_cateurl = '{}', regdate = getdate() where proc_ip = '{}'".format(catecode, amz_cateurl, ip)
        else:
            sql = " insert into update_list (proc_ip, catecode, amz_cateurl, regdate) value ('{}','{}','{}',getdate())".format(ip, catecode, amz_cateurl)
        db_con.execute(sql)

        time.sleep(1)
        print('>> time.sleep(1) ')
        print(">> ea_list : {}".format(amz_cateurl))
        browser.get(amz_cateurl)
        browser.add_cookie({'name':'hng','value':'CN%7Czh-CN%7CCNY%7C156'})
        time.sleep(7)
        print('>> time.sleep(7) ')
        #input(">> Key : ")

        cur_url = browser.current_url
        if str(cur_url).find('/home.html') > -1:
            print(">> Net Work Error (skip) : {}".format(cur_url))
            time.sleep(3)
            return "E"

        proc_asin(browser, catecode)
        time.sleep(2)
        try:
            rtnCnt = doProcDetail(browser, catecode, endPage)
        except Exception as ex:
            print('>> doProcDetail Error (Skip) : ', ex)
        else:                    
            time.sleep(3)
            print('>> time.sleep(3) ')           

    if float(rtnCnt) > 0:
        sql_u = "update t_category set list_in = '2', up_date = getdate() where catecode = '{}'".format(catecode)
    else:
        sql_u = "update t_category set list_in = '1', up_date = getdate() where catecode = '{}'".format(catecode)
    print('>> sql_u : {}'.format(sql_u))
    db_con.execute(sql_u)

    return rtn_value


def procBlockGoods():
    
    print('Blocked Goods --> Insert')
    sql = "select asin, cate_idx, DATEADD(day,-3,reg_date) from T_Category_BestAsin_del where reg_date < DATEADD(hh,-2,getdate()) and left(code ,1) = 'C'"
    rows = db_con.select(sql)
    print('procBlockGoods (sql) :' + str(sql))

    if not rows:
        print('(2시간전) Blocked Goods No ')
    else:
        for rs in rows:
            Dasin = rs[0]
            Dcate_idx = rs[1]
            Dreg_date = rs[2] #생성일 -3일
            print("Blocked Goods : " + str(Dcate_idx) + " | " + str(Dasin))

            sql2 = "select * from T_Category_BestAsin where asin = '{0}'".format(Dasin)
            rs2 = db_con.selectone(sql2)
            #print('##select one## sql2 :' + str(sql2))

            if not rs2:  # rs2 is None
                print('New T_Category_BestAsin')

                sql = "insert into T_Category_BestAsin (cate_idx,price,asin,reg_date) values (" + str(Dcate_idx) + ",0,'" + str(Dasin) + "', getdate()-3)"
                db_con.execute(sql)  # insert
                #print('##insert## (sql):'+str(sql))
                print('##insert## : T_Category_BestAsin : '+str(Dasin))

                sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(Dasin)
                db_con.execute(sql)
                print('##delete## : T_Category_BestAsin_del : '+str(Dasin))

    return "0"

def getEndpage(db_con):
    rtnPage = 30

    sql = " select endpage from python_version_manage where name = 'list' "
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]

    print("getEndpage : "+str(rtnPage))

    return rtnPage

def getEndasin(db_con):
    rtnAsin = 30000

    sql = " select endasin from python_version_manage where name = 'list' "
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]

    print("getEndasin : "+str(rtnAsin))

    return rtnAsin

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

if __name__ == '__main__':
    global goods

    errCnt = 0
    errFlg = ""
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))

    set_browser = "chrome"
    set_browser = "brave"
    browser = connectDriver(set_browser)
    browser.set_window_size(1400, 1000)
    browser.implicitly_wait(3)

    time.sleep(2)
    print('>> time.sleep(2)')

    endpage = 0
    endpage = getEndpage(db_con)
    if endpage > 9 and endpage < 300:
        print('getEndpage OK')
    else:
        print('getEndpage Check')

    endasin = 0
    endasin = getEndasin(db_con)
    if endasin > 0:
        print('getEndasin OK' + str(endasin))
    else:
        print('getEndasin Check')

    mainLow = 1
    mainStop = "0"
    while mainLow < 50:
        sql_cnt = " select count(*) from T_Category_BestAsin "
        rowCnt = db_con.selectone(sql_cnt)
        if not rowCnt:
            print('asinCnt 확인불가')
            db_con.close()
            browser.quit()
            time.sleep(1)
            os._exit(0)
        else:
            asinCnt = rowCnt[0]
            if asinCnt > endasin:
                print('(SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
                procLogSet(db_con, "shop_list", " asinCnt : " + str(asinCnt)+' 건)')
                db_con.close()
                browser.quit()
                time.sleep(1)
                os._exit(0)
        print('\n ------------- mainLow : ' + str(mainLow) + ' -------------')

        rtn_flg = doProcShow(browser, endpage)
        if rtn_flg == "E":
            break

        mainLow = mainLow + 1

    print('\n [--- main end ---] ' + str(datetime.datetime.now()))
    print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간

    db_con.close()
    time.sleep(2)
    browser.quit()
    time.sleep(2)
    os._exit(0)

