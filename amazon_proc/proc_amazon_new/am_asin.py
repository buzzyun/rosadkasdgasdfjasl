
import os
os.system('pip install --upgrade selenium')
import datetime
import os
import re
import requests
import random
import socket
import socks
import http.client
import urllib
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time

def version_check(db_con, in_drive, file_name, ver, list_name):

    print("version:" + ver)
    file_path = r"c:/project/"
    
    sql = "select version,url from python_version_manage where name = '{}'".format(list_name)
    print(">> sql:" + sql)
    rows = db_con.selectone(sql)
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        print(">> New version Download :" + str(version_url) + " | "+ str(file_path + file_name))

        time.sleep(30)
        print(">> time.sleep(30)")
        print(">> New version update exit")

        db_con.close()
        in_drive.quit()
        time.sleep(2)
        os._exit(1)

def version_check2(db_con, file_name, ver, list_name):
    
    print("version:" + ver)
    file_path = r"c:/project/"
    
    sql = "select version,url from python_version_manage where name = '{}'".format(list_name)
    print(">> sql:" + sql)
    rows = db_con.selectone(sql)
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        print(">> New version Download :" + str(version_url) + " | "+ str(file_path + file_name))

        time.sleep(30)
        print(">> time.sleep(30)")
        print(">> New version update exit")

        db_con.close()
        time.sleep(2)
        os._exit(1)

def connectDriverOld(pgSite, kbn):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(kbn) == "":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")

    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, kbn):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(kbn) == "":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser


def connectDriver(tool, url):
    global set_browser

    if tool == 'chrome':
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
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
        options.add_argument("user-data-dir={}".format(userProfile))

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': '{}'".format(url))
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'brave':
        path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=path, chrome_options=options)

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

def set_new_tor_ip():
    # """Change IP using TOR"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    print(">> set_new_tor_ip()")

def checkCurrIP():
    time.sleep(2)
    # proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    # res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    # print('>> Tor Current IP:', res.text)

def checkCurrIP_new():
    time.sleep(1)
    proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    print('>> Tor Current IP:', res.text)
    time.sleep(1)

def reDoProc(in_drive, in_url):
    result = ""

    in_drive.refresh()
    time.sleep(3)
    print('>> time.sleep(3) ')

    try:
        in_drive.get(in_url)
    except Exception as ex:
        print('>> reDoProc url Get Error Skip : ', ex)
    else:                    
        time.sleep(2)
        print('>> time.sleep(2)')
        result = in_drive.page_source

    time.sleep(1)
    print('>> time.sleep(1) ')

    return result


def moveScroll(driver):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 700
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.1)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > 2:
            break
        last_height = new_height

def getAsinCnt(db_con):
    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

def getAsinPriorityCnt(db_con, list_name):
    asinCnt = 0
    if list_name == "list_priority":
        sql_cnt = " select count(*) from T_Category_BestAsin as a inner join t_category as c on a.cate_idx = c.CateCode where c.priority_flg = '1' "
    else:
        sql_cnt = " select count(*) from T_Category_BestAsin as a inner join t_category as c on a.cate_idx = c.CateCode where c.priority_flg is null "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

def getSource(in_url, in_drive, in_cateidx):

    time.sleep(2)
    print('>> time.sleep(2) ')
    print('>> url :'+str(in_url))

    result = ""
    try:
        in_drive.get(in_url)
    except Exception as ex:
        print('>> test_asin Get Error Skip : ', ex)
    else:                    
        time.sleep(3)
        print('>> time.sleep(3)')

    result = str(in_drive.page_source)
    time.sleep(1)

    tmp_result = ""
    if str(result).find('validateCaptcha') > -1 or str(result).find('continue-shopping.gif') > -1:
        cwlow = 1
        while cwlow < 6:
            tmp_result = reDoProc(in_drive, in_url)
            if str(tmp_result).find('validateCaptcha') > -1:
                print('>> (' +str(cwlow)+ ') validateCaptcha ')
            elif str(tmp_result).find('continue-shopping.gif') > -1:
                print('>> (' +str(cwlow)+ ') continue-shopping.gif ')
            elif tmp_result == "":
                print('>> tmp_result : no data Skip')
            else:
                print('>> Connect Ok ')
                result = tmp_result
                break

            cwlow = cwlow + 1

    time.sleep(2)
    print('>> time.sleep(2)')
    if str(result).find('validateCaptcha') > -1 or str(result).find('continue-shopping.gif') > -1:
        print('>> Connect Error (SKIP) ')
        return "1"

    # try:
    #     moveScroll(in_drive)
    # except Exception as ex:
    #     print('>> moveScroll Skip ')

    time.sleep(2)
    result = in_drive.page_source
    print('>> page_source >> get ')
    time.sleep(1)

    if str(result).find('data-component-type="s-search-results"') > -1 or str(result).find('<div data-asin="') > -1:
        print('>> getSource Ok (1) - ')

    elif str(result).find('results for') > -1 or str(result).find('asin=') > -1:
        print('>> getSource Ok (2) - ')

    else:
        print('>> getSource block retry (1) - ')
        return "1"

    #input("Key press : ")
    return str(result)


def getSourceNew(in_url, in_drive, in_cateidx, site_url):

    time.sleep(1)
    print('>> url :'+str(in_url))
    result = ""
    try:
        in_drive.get(in_url)
    except Exception as ex:
        print('>> test_asin Get Error Skip : ', ex)
    else:                    
        time.sleep(3)

    result = str(in_drive.page_source)
    tmp_result = ""
    if str(result).find('validateCaptcha') > -1 or str(result).find('continue-shopping.gif') > -1:
        cwlow = 1
        while cwlow < 6:
            tmp_result = reDoProc(in_drive, in_url)
            if str(tmp_result).find('validateCaptcha') > -1:
                print('>> (' +str(cwlow)+ ') validateCaptcha ')
            elif str(tmp_result).find('continue-shopping.gif') > -1:
                print('>> (' +str(cwlow)+ ') continue-shopping.gif ')
            elif tmp_result == "":
                print('>> tmp_result : no data Skip')
            else:
                print('>> Connect Ok ')
                result = tmp_result
                break

            cwlow = cwlow + 1

    if str(result).find('validateCaptcha') > -1 or str(result).find('continue-shopping.gif') > -1:
        print('>> Connect Error (SKIP) ')
        return "1"

    #moveScroll(in_drive)
    try:
        moveScroll(in_drive)
    except Exception as ex:
        print('>> moveScroll Skip ')

    time.sleep(0.5)
    result = in_drive.page_source
    print('>> page_source >> get ')

    if str(result).find('data-component-type="s-search-results"') > -1 or str(result).find('<div data-asin="') > -1:
        print('>> getSource Ok (1) - ')

    elif str(result).find('See all results') > -1:
        seeMore = getparseR(str(result), '', 'See all results')
        seeMore = getparse(str(seeMore), 'href="', '"').replace('amp;','').strip()
        seeMoreUrl = seeMore
        if seeMore.find("amazon.") == -1:
            seeMoreUrl = site_url + seeMore
            print(">> seeMoreUrl : {}".format(seeMoreUrl))
            #soup = getSource(str(seeMoreUrl),in_drive,in_cateidx)
            try:
                in_drive.get(in_url)
            except Exception as ex:
                print('>> test_asin Get Error Skip : ', ex)
            else:                    
                time.sleep(1)

            result = str(in_drive.page_source)
            if str(result).find('data-component-type="s-search-results"') > -1 or str(result).find('<div data-asin="') > -1:
                print('>> getSource Ok (1 - 1) ')
            else:
                return "1"

    elif str(result).find('results for') > -1 or str(result).find('asin=') > -1:
        print('>> getSource Ok (2) ')

    elif str(result).find('class="octopus-pc-item octopus-pc-item-v3"') > -1:
        print('>> getSource Ok (3) ')

    elif str(result).find('id="gridItemRoot"') > -1:
        print('>> getSource Ok (gridItemRoot) ')

    else:
        print('>> getSource block retry (1) ')
        return "1"

    #input("Key press : ")
    return str(result)

# usa / global / uk (all) --> sale_ck_new = '1' 조건 추가 -> 제거 
def newlist_priority(db_con, endpage, ip, listname):

    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print('>> -- newlist_sale() -- work ip : '+str(ip))

    sql = "select * from update_list where proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('>> update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1

        if listname == "list_priority":
            sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and priority_flg = '1' order by up_date asc "
        else:
            sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and priority_flg is null order by up_date asc "

        if page > endpage:
            page = endpage

        row = db_con.selectone(sql)
        if not row:
            print('>> work ip 데이터 등록 ')
        else:
            amzurl = row[0]
            cateidx = row[1]
            print('>> [new] cateidx : '+str(cateidx))

            dic_up = dict()
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('>> ##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('>> ##insert## : update_list ( catecode | now_page | proc_ip )')

    else:
        print('>> update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('>> ##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('>> cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr


# usa / global / uk (all) --> sale_ck_new = '1' 조건 추가
def newlist_sale(db_con, endpage, ip, listname):
    
    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print('>> -- newlist_sale() -- work ip : '+str(ip))

    sql = "select * from update_list where proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('>> update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1

        if listname == "list_all":
            sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and a.cate_kubun is null and sale_ck_new = '1' order by up_date asc "
        else:
            sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and sale_ck_new = '1' order by up_date asc "

        if page > endpage:
            page = endpage

        row = db_con.selectone(sql)
        if not row:
            print('>> work ip 데이터 등록 ')
        else:
            amzurl = row[0]
            cateidx = row[1]
            print('>> [new] cateidx : '+str(cateidx))

            dic_up = dict()
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('>> ##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('>> ##insert## : update_list ( catecode | now_page | proc_ip )')

    else:
        print('>> update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('>> ##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('>> cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr

def newlist(db_con, endpage, ip, listname):
    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print('>> -- newlist() -- work ip : '+str(ip))

    sql = "select * from update_list where proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('>> update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1

        if listname == "list_all":
            sql = " SELECT top 1 a.amz_cateurl,a.catecode, isnull(a.sale_ck_new,0) FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and a.cate_kubun is null order by up_date asc "
        else:
            sql = " SELECT top 1 a.amz_cateurl,a.catecode, isnull(a.sale_ck_new,0) FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null order by up_date asc "

        row = db_con.selectone(sql)
        if not row:
            print('>> work ip 데이터 등록 ')
        else:
            amzurl = row[0]
            cateidx = row[1]
            sale_ck_new = row[2]
            print('>> [new] cateidx : '+str(cateidx))

            if page > endpage:
                page = endpage

            dic_up = dict()
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('>> ##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('>> ##insert## : update_list ( catecode | now_page | proc_ip )')

    else:
        print('>> update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('>> ##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('>> cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr


def procLastpage(in_cateidx, in_flg, db_con):

    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
        print('>> 마지막 page')
        sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_connect":
        sql = "update T_CATEGORY set up_date = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_data":
        sql = "update T_CATEGORY set up_date = GETDATE()-1 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    print('>> sql : ' + str(sql))
    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
        sql = "delete from update_list where catecode ='" + str(in_cateidx) + "'"
        db_con.execute(sql)
        print('>> sql : ' + str(sql))

    return "0"


def procDbSet(in_asin, in_cateidx, in_price, db_con):
    db_flg = ""
    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        #sql = "insert into T_Category_BestAsin (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(in_cateidx) + "','" + str(in_price) + "',getdate()) "
        sql = "insert into T_Category_BestAsin (asin, cate_idx, reg_date) values ('{}', '{}', getdate())".format(in_asin,in_cateidx)
        # print('sql :'+str(sql))
        db_con.execute(sql)
        db_flg = "insert"
    else:
        print('>> T_Category_BestAsin (존재) : {}'.format(in_asin))
        # #sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(in_asin) + "'"
        # sql = "update T_Category_BestAsin set up_date = GETDATE() where asin='" + str(in_asin) + "'"
        # # print('sql :'+str(sql))
        # db_con.execute(sql)
    return db_flg


def fun_chart(db_con, in_drive, in_catetmp, endpage, ip, file_name, ver, errCnt, site_url, list_name):
    curpage = ""
    print('>> fun_chart() ')

    if str(ip).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(ip))
    else:
        # version 체크
        version_check(db_con, in_drive, file_name, ver, list_name)

    sortType = getSortType(db_con, list_name)
    sp_tmp = str(in_catetmp).split('@')
    cateidx = sp_tmp[0]
    page = sp_tmp[1]

    if str(page) == "":
        page = "1"
    pglow = int(page)

    while pglow <= endpage:
        amzurl = ""
        print('>> pglow :' + str(pglow))
        print('>> page : ' + str(page))
        print('>> errCnt : ' + str(errCnt))

        if errCnt > 7:
            print('>> errCnt 7개 이상 강제종료 : ' + str(errCnt))
            procLogSet(db_con, "list_all", " errCnt 7개 이상 강제종료 : " + str(errCnt), ip)
            #set_new_tor_ip()
            #checkCurrIP()
            time.sleep(1)
            db_con.close()
            in_drive.quit()
            os._exit(0)

        sql = "select amz_cateurl from t_category where catecode = '{0}'".format(cateidx)
        rs = db_con.selectone(sql)
        print('>> ## ' + str(pglow) + ' ####(fun_chart) select one## sql :' + str(sql))

        if not rs:
            print(">> 해당 카테고리코드 없음 : " + str(cateidx))
            procLastpage(cateidx, "no_cateidx", db_con)
            break

        amzurl = rs[0]
        if str(amzurl).find('?node=') > -1:
            cuturl1 = getparse(amzurl,'?node=','')
        else:
            cuturl1 = getparse(amzurl,'/-/','')

        print('>> [' + str(cateidx) + '] page: ' + str(page) + ' | ' + str(cuturl1) + ' | ' + str(amzurl))

        dbInsCnt = 0
        break_flg = "0"
        # (최신, 리뷰, 인기순 3번 실행) start -----------------------------------------------------------------
        perform_cnt = 0 
        while perform_cnt < 3:
            onurl = amzurl
            print('\n>>-------------------------------------------------')
            if str(page) == "1":
                if perform_cnt == 0:
                    onurl = onurl + "&s=date-desc-rank" # 최신순
                    print('>> page (1) 최신순 url : ' + str(onurl))
                elif perform_cnt == 1:
                    onurl = onurl + "&s=review-rank" # 리뷰순
                    print('>> page (1) 리뷰순 url : ' + str(onurl))
                else:
                    onurl = onurl + "&s=exact-aware-popularity-rank" # 인기순
                    print('>> page (1) 인기순 url : ' + str(onurl))

                soup = getSourceNew(str(onurl),in_drive,cateidx,site_url)
                if soup == "1":
                    errCnt = errCnt + 1
                    print('>> Data를 가져올수없음 (SKIP) : ' + str(in_catetmp) + ' | ' + str(onurl))
                    procLastpage(cateidx, "no_data", db_con)
                    break_flg = "1"
                    break
                else:
                    errCnt = 0
                    print('>> get Data Ok (1)')
                    orgSoup = str(soup)
                    if str(soup).find('kailey-kitty._CB485935160_.gif') == -1 and str(soup).find('title._TTD_.png') == -1:  # 유효한 페이지인지 체크
                        orgSoup = str(soup)
                    else:
                        print('>> 유효한 페이지가 아닙니다.(1) ')
                        orgSoup = ""
                        procLastpage(cateidx, "no_page", db_con)
                        break_flg = "1"
                        break

            else:
                print('>> page (2~)')
                onurl = str(site_url) + '/s?rh=n%3A{0}&page={1}'.format(cuturl1, page)
                if perform_cnt == 0:
                    onurl = onurl + "&s=date-desc-rank" # 최신순
                    print('>> page (2~) 최신순 url : ' + str(onurl))
                elif perform_cnt == 1:
                    onurl = onurl + "&s=review-rank" # 리뷰순
                    print('>> page (2~) 리뷰순 url : ' + str(onurl))
                else:
                    onurl = onurl + "&s=exact-aware-popularity-rank" # 인기순
                    print('>> page (2~) 인기순 url : ' + str(onurl))

                soup2 = getSourceNew(str(onurl),in_drive,cateidx,site_url)
                if soup2 == "1":
                    errCnt = errCnt + 1
                    print('>> Data를 가져올수없음 (SKIP) : ' + str(soup2))
                    procLastpage(cateidx, "no_data", db_con)
                    break_flg = "1"
                    break

                else:
                    errCnt = 0
                    print('>> get Data Ok (2)')
                    orgSoup = str(soup2)
                    if str(soup2).find('kailey-kitty._CB485935160_.gif') == -1 and str(soup2).find('title._TTD_.png') == -1:  # 유효한 페이지인지 체크

                        if str(soup2).find('data-component-type="s-search-results"') > -1:
                            time.sleep(2)
                            soup2 = in_drive.page_source
                            print('>> page_source >> get ')
                            time.sleep(0.5)
                            orgSoup = str(soup2)
                        else:
                            print('>> 유효한 페이지가 아닙니다.(2) ')
                            orgSoup = ""
                            procLastpage(cateidx, "no_page", db_con)
                            break_flg = "1"
                            break
                    else:
                        print('>> 유효한 페이지가 아닙니다.(2) ')
                        orgSoup = ""
                        procLastpage(cateidx, "no_page", db_con)
                        break_flg = "1"
                        break

            #input("Key press : ")
            soup = ""
            orgSoup = str(orgSoup)
            #print("strSoup1 : " +str(strSoup1))
            #input("key (strSoup2) : ")
            print(str(page)+' Page data-index ------------------ ')

            tmpSoup = ""
            if str(orgSoup).find('data-index="') > -1:
                f_fos = str(orgSoup).find('data-index="')
                f_fos = f_fos - 100
                tmpSoup = orgSoup[f_fos:]
                soup = getparse(str(tmpSoup), '<div data-asin="', 'class="a-pagination"')
            elif str(orgSoup).find('results for') > -1:
                if str(orgSoup).find('See all results') > -1:
                    soup = getparse(str(orgSoup), 'results for', 'See all results')
                else:
                    soup = getparse(str(orgSoup), 'results for', 'class="a-pagination"')
            elif str(orgSoup).find('class="octopus-pc-item octopus-pc-item-v3"') > -1:
                soup = getparse(str(orgSoup), 'class="octopus-pc-item octopus-pc-item-v3"', '')
            elif str(orgSoup).find('id="gridItemRoot"') > -1:
                soup = getparse(str(orgSoup), 'id="gridItemRoot"', '')

            if str(orgSoup).find('Try checking your spelling or use more general terms') > -1:
                print('>> 유효하지 않은 페이지 (마지막 페이지 또는 오류) ')
                procLastpage(cateidx,"end",db_con)
                break_flg = "1"
                break

            if str(orgSoup).find('validateCaptcha') > -1 or str(orgSoup).find('continue-shopping.gif') > -1:
                errCnt = errCnt + 1
                print('>> validateCaptcha (auto) | continue-shopping.gif ')

            strPage = ""
            if str(orgSoup).find('<ul class="a-pagination">') > -1:
                curpage = getparse(str(orgSoup), '<li class="a-selected">', '</li>')
                curpage = getparse(curpage, '">', '</a>')
            elif str(orgSoup).find('<span class="s-pagination-strip">') > -1:
                curpage = getparse(str(orgSoup), 'class="s-pagination-item s-pagination-selected"', '</span>')
                curpage = getparse(curpage, '">', '')            
            elif str(orgSoup).find('results for') > -1 and str(orgSoup).find('See all results') > -1:
                curpage = "1"
            else:
                curpage = "1"

            curpage = curpage.strip()
            print('>> curpage : ' + str(curpage))

            if str(curpage).isdigit():
                if int(curpage) < endpage:
                    naxtpage = int(curpage) + 1
                    print('>> naxtpage (next) : ' + str(naxtpage))
            else:
                print('>> Page Not Found Error !! : ' + str(curpage))
                #if page != "1":
                procLastpage(cateidx,"no_page",db_con)
                break_flg = "1"
                break

            if str(soup) != "":
                if str(soup).find('<div data-asin="') > -1:
                    sp_items = str(soup).split('<div data-asin="')
                elif str(soup).find('class="octopus-pc-item octopus-pc-item-v3"') > -1:
                    sp_items = str(soup).split('class="octopus-pc-item octopus-pc-item-v3"')
                elif str(soup).find('id="gridItemRoot"') > -1:
                    sp_items = str(soup).split('id="gridItemRoot"')
                else:
                    sp_items = str(soup).split('<div class="a-section a-spacing-medium">')
                print('>> len(sp_items):' + str(len(sp_items) - 1))
                if len(sp_items) == 0:
                    print('>> 해당 페이지에 데이터가 0개.')
                    procLastpage(cateidx, "no_page", db_con)
                    break_flg = "1"
                    break
                if int(page) > 2 and len(sp_items) < 10:
                    print('>> 해당 페이지에 데이터가 10개 이하.')
                    procLastpage(cateidx, "no_page", db_con)
                    break_flg = "1"
                    break

                i=0
                updCnt = 0
                while i < len(sp_items):
                    ea_item = sp_items[i]
                    price = "0"
                    asin = ""
                    if str(orgSoup).find('results for') > -1:
                        asin = getparse(ea_item, '/dp/', '/')
                    elif str(orgSoup).find('class="octopus-pc-item octopus-pc-item-v3"') > -1:
                        asin = getparse(ea_item, '/dp/', '')
                        if str(asin).find('?') > -1:
                            asin = getparse(asin, '', '?')
                        if str(asin).find('/') > -1:
                            asin = getparse(asin, '', '/')
                    elif str(orgSoup).find('id="p13n-asin-index') > -1:
                        asin = getparse(ea_item, '/dp/', '')
                        if str(asin).find('?') > -1:
                            asin = getparse(asin, '', '?')
                        if str(asin).find('/') > -1:
                            asin = getparse(asin, '', '/')                     
                    else:
                        asin = getparse(ea_item, '', '"')
                        print(">> else asin : {}" .format(asin))
                    if str(asin).find("?") > -1:
                        asin = getparse(str(asin), '', '?')

                    if str(ea_item).find('<span class="a-price-whole">') > -1:
                        price = getparse(str(ea_item), '<span class="a-price-whole">', "</span>")
                        price = str(price).replace('<span class="a-price-decimal">','')
                        if str(price).find('.') > -1:
                            price = getparse(str(price), '', ".")
                            price = str(price).replace('&nbsp;', '')
                    elif str(ea_item).find('class="a-size-base a-color-price"') > -1:
                        price = getparse(str(ea_item),'class="a-size-base a-color-price">','</span>')
                        if price.find('>') > -1:
                            price = getparse(str(price),'>','')
                    elif str(ea_item).find('<span class="a-offscreen">') > -1:
                        price = getparse(str(ea_item), '<span class="a-offscreen">', "</span>")
                    elif str(ea_item).find('class="p13n-sc-price">') > -1:
                        price = getparse(str(ea_item), 'p13n-sc-price', "</span>")
                        if price.find('>') > -1:
                            price = getparse(str(price), '>', "")
                    else:
                        price = ""

                    #print('>> asin : ' + str(asin) + ' | ' + str(price))
                    price = price.replace('&nbsp;','').replace('USD','').strip()
                    if str(asin) == "":
                        print('>> ( {0} ) : no asin Skip : {1} '.format(i, asin))
                    elif len(asin) < 8 or len(asin) > 12:
                        print('>> ( {0} ) : len over asin Skip : {1} | {2}'.format(i, asin, price))
                    # elif price > 1000:
                    #     print('>> ( {0} ) : len over price Skip : {1} | {2}'.format(i, asin, price))
                    elif str(price) == "" or str(price) == "0":
                        print('>> ( {0} ) : no price Skip : {1} | {2}'.format(i, asin, price))
                    else:
                        if str(price).find('-') > -1:
                            price = getparse(str(price),'','-')
                        price = str(price).replace('&nbsp;', '').replace('JPY', '').replace('¥', '').replace('$', '').replace('€', '').replace('£', '').replace('USD', '').replace(',', '').replace('\xa0','').replace("'", '').strip()
                        price = regRemoveText(price)
                        price = price.replace(",","").strip()
                        #print(str(asin) + " | " + str(price) + " | DB Insert ")
                        updCnt = updCnt + 1

                        insFlg = ""
                        # DB 입력
                        try:
                            insFlg = procDbSet(asin, cateidx, price, db_con)
                        except Exception as e:
                            print(">> DB ins Exception : {}".format(e))
                            errCnt = errCnt + 1
                            input(">> input (1):")
                        if insFlg == "insert":
                            errCnt = 0
                            dbInsCnt = dbInsCnt + 1
                        print('>> ( {0} ) : {1}  | {2} [ {3} ]  {4} '.format(i, cateidx, asin, price, insFlg))
                    i = i + 1

            perform_cnt = perform_cnt + 1 # (리뷰순, 신사품순 2번 실행)
        # (리뷰순, 신사품순 2번 실행) end -----------------------------------------------------------------
        print(">>(page all) dbInsCnt : {}".format(dbInsCnt))
        if break_flg == "1":
            break

        print('>> page : '+str(page))
        page = int(page)

        if int(page) >= int(endpage):
            print('>> 마지막 page'+str(endpage))
            procLastpage(cateidx, "end", db_con)
            break
        else:
            page += 1
            if page > int(endpage):
                page = int(endpage)
            print('>> Next page : '+str(page))
            errCnt = 0
            sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(page, cateidx)
            db_con.execute(sql)
            print('>> sql : ' + str(sql))

        pglow = pglow + 1
        #print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간
        print('>> time : {} '.format(datetime.datetime.now()))

        test_asin = ""
        sql = "select top 1 asin from T_Category_BestAsin where cate_idx = '{0}' order by reg_date desc ".format(cateidx)
        rs_Asin = db_con.selectone(sql)
        if rs_Asin:
            test_asin = rs_Asin[0]
            print('>> [' +str(cateidx)+ '] test_asin :' + str(test_asin))
            if test_asin != "":
                test_url = str(site_url) + "/dp/" + str(test_asin)
                try:
                    in_drive.get(test_url)
                except Exception as ex:
                    print('>> test_asin Get Error Skip : ', ex)
                else:                    
                    time.sleep(1)

    return "0"

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    return result

def procDeliverChk(in_drive):

    ############ Deliver to Check #############################
    deliver_post = ""
    try:
        deliver_post = in_drive.find_element(By.ID,'glow-ingress-line2').text
    except Exception as ex:
        print('>> error : ', ex)
        return "1"
    else:
        print(">> deliver_post : " + str(deliver_post))

    if deliver_post == "":
        print('>> deliver_post no check ')
        return "1"

    return deliver_post


def procDelivertoSet(in_drive, nFlg):
    time.sleep(1)

    try:
        in_drive.find_element(By.ID,'glow-ingress-line2').click()
    except Exception as ex:
        print('>> Error : ', ex)
        return "1"
    else:
        if nFlg == "US" or nFlg == "DE":
            time.sleep(2)
            devSour = in_drive.page_source
            devSourCut = getparse(devSour,'id="glow-ingress-line1">','</span>')
            time.sleep(1)
            if devSourCut.find("Deliver to") > -1:
                # try:
                #     in_drive.find_element(By.XPATH,'//*[@id="GLUXChangePostalCodeLink"]').click()
                #     print(" change click ")
                # except Exception as ex:
                #     print(' Error : ', ex)

                time.sleep(3)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys(Keys.CONTROL + "a")
                time.sleep(1)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys(Keys.DELETE)
                time.sleep(2)

            if nFlg == "US":
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys('97223')
            elif nFlg == "DE":
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys('65843')

            try:
                time.sleep(1)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input').click()
                time.sleep(2)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXConfirmClose"]').click()
            except Exception as ex:
                print('>> Error : ', ex)
            else:
                #//*[@id="GLUXChangePostalCodeLink"]  # //*[@id="a-autoid-3-announce"]
                time.sleep(3)

        elif nFlg == "JP":
            time.sleep(3)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput_0"]').send_keys('542')
            time.sleep(1)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput_1"]').send_keys('0012')
            time.sleep(1)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input').click()
            time.sleep(3)

        time.sleep(2)
        devSourF = in_drive.page_source
        time.sleep(1)
        if devSourF.find("Continue") > -1:
            time.sleep(1)
            try:
                in_drive.find_element(By.XPATH,'//*[@id="GLUXConfirmClose"]').click()
            except Exception as ex:
                print('>> Error : ', ex)
            time.sleep(3)
            print('>> procDelivertoSet OK ')

    return "0"

def getSortType(db_con, listname):
    sort_type = "1"

    sql = " select sort_type from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        sort_type = rs[0]

    print(">> sort_type : "+str(sort_type))

    return sort_type

def getEndpage(db_con, listname):
    rtnPage = 30

    sql = " select endpage from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]

    print(">> getEndpage : "+str(rtnPage))

    return rtnPage

def getEndpage_check(db_con, listname, catecode):
    rtnPage = 0
    sql_s = "select isnull(sale_ck_new,'0') from t_category where catecode = '{}'".format(catecode)
    row = db_con.selectone(sql_s)
    if row:
        sale_ck_new = row[0]
        if sale_ck_new == "0":
            sql = " select isnull(endpage_nosale,'0') from python_version_manage where name = '{}'".format(listname)
            rs = db_con.selectone(sql)
            if rs:
                if str(rs[0]) != "0":
                    rtnPage = rs[0]
                    print(">> getEndpage_nosale : "+str(rtnPage))
    return rtnPage

def getEndasin(db_con, listname):
    rtnAsin = 30000

    sql = " select endasin from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]

    print(">> getEndasin : "+str(rtnAsin))

    return rtnAsin

def del_naver4_remove(db_con):

    print('>> del_naver4_remove --> Insert')
    sql = "select count(*) as cnt from T_Category_BestAsin as a inner join t_goods as g on g.display_ali_no = a.asin where g.Del_naver = '4' "
    rows = db_con.select(sql)
    print('>> del_naver4_remove (sql) :' + str(sql))
    if not rows:
        print('>> del_naver4_remove 대상 없음 ')
    else:
        sql_del = "delete from T_Category_BestAsin where asin in (select display_ali_no from T_Category_BestAsin as a inner join t_goods as g on g.display_ali_no = a.asin where g.Del_naver = '4')"
        print('# sql_del :' + str(sql_del))
        db_con.execute(sql_del)
    return "0"

def procDelStopUpdateGoods(db_con):
    dSql = "delete from T_Category_BestAsin where asin in (select g.display_ali_no from T_Category_BestAsin as a inner join t_goods as g on g.display_ali_no = a.asin and g.stop_update = '1')"
    print('>> procDelStopUpdateGoods (dSql) :' + str(dSql))
    db_con.execute(dSql)

    return "0"

def procBlockGoods(db_con):

    print('>> Blocked Goods --> Insert')
    sql = "select asin, cate_idx, DATEADD(day,-3,reg_date) from T_Category_BestAsin_del where reg_date < DATEADD(hh,-2,getdate()) and left(code ,1) = 'C'"
    rows = db_con.select(sql)
    print('>> procBlockGoods (sql) :' + str(sql))

    if not rows:
        print('(2시간전) Blocked Goods No ')
    else:
        for rs in rows:
            Dasin = rs[0]
            Dcate_idx = rs[1]
            Dreg_date = rs[2] #생성일 -3일
            print(">> Blocked Goods : " + str(Dcate_idx) + " | " + str(Dasin))

            sql2 = "select * from T_Category_BestAsin where asin = '{0}'".format(Dasin)
            rs2 = db_con.selectone(sql2)
            #print('##select one## sql2 :' + str(sql2))

            if not rs2:  # rs2 is None
                print('>> New T_Category_BestAsin')

                sql = "insert into T_Category_BestAsin (cate_idx,price,asin,reg_date) values (" + str(Dcate_idx) + ",0,'" + str(Dasin) + "', getdate()-3)"
                db_con.execute(sql)  # insert
                #print('##insert## (sql):'+str(sql))
                print('>> ##insert## : T_Category_BestAsin : '+str(Dasin))

                sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(Dasin)
                db_con.execute(sql)
                print('>> ##delete## : T_Category_BestAsin_del : '+str(Dasin))

    return "0"


def doScrollDown(browser, whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break


def procLogSet(in_DB, in_proc_no, in_proc_memo, ip):
    sql = " insert into amazon_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"
