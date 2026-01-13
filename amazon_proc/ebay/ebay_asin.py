import datetime
import os
import random
import socket
import socks
import http.client
import urllib
import chromedriver_autoinstaller
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
import re
import sys
import DBmodule_FR

global page
global ip
global pagecount
global timecount
global chkTime
global ver
global endpage
global errCnt

ver = "7.0"

ip = socket.gethostbyname(socket.gethostname())
amzurl = ""
timecount = 0
db_con = DBmodule_FR.Database('REF')

chkTime = time.time()
print("chkTime : "+str(chkTime))

def connectDriverOld(pgSite):
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
    # option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite):
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
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)

        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path

    return browser

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
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        browser = webdriver.Chrome(service=s, options=option)
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

def version_check(in_drive, name):
    global ver
    print("version:" + ver)
    file_path = r"c:/project/"
    file_name = "new_ebay_asin.exe"
    #sql = "select version,url from python_version_manage where name = 'list'"
    sql = "select version,url from python_version_manage where name = '{}'".format(name)
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
    time.sleep(1)
    proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    print('>> Tor Current IP:', res.text)

def getSource(in_url, in_drive, in_cateidx):

    time.sleep(2)
    print('>> time.sleep(2) ')
    print('url :'+str(in_url))

    result = ""
    try:
        in_drive.get(in_url)
        time.sleep(random.uniform(5,6))  
    except Exception as ex:
        print('test_asin Get Error Skip : ', ex)
    else:                    
        print('>> connect ok ')

    result = in_drive.page_source
    #print("result : "+str(result))
    time.sleep(2)
    print('>> time.sleep(2) ')

    tmp_result = ""
    if str(result).find('b-list__items_nofooter') > -1 or str(result).find('item-card--list') > -1:
        print('>> getSource Ok (1) - ')
    elif str(result).find('It’s not you. It’s us.') > -1:
        print('>> getSource : It’s not you. It’s us.')
        return "2"
    elif str(result).find('0 results found') > -1:
        print('>> getSource : 0 results found')
        return "2"
    elif str(result).find('Looks like this page is missing') > -1:
        print('>> getSource : Looks like this page is missing')
        return "1"
    else:
        time.sleep(2)
        print('>> time.sleep(2) ')
        # set_new_ip()
        # checkIP()     
        # time.sleep(1)   
        print('>> getSource block retry (1) - ')
        return "E"

    return str(result)


def newlist():
    global ip
    global endpage

    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print(' -- newlist() -- work ip : '+str(ip))
    sql = "select * from update_list where flg_ref is null and proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)
    if not rows:
        print('update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1
        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on a.CateCode = b.catecode and b.flg_ref is null where IsHidden='F' and lastcate=1 and b.catecode is null order by up_date asc "
        #sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and minus_opt = '1' and lastcate=1 and b.catecode is null order by up_date asc "

        if page > endpage:
            page = endpage

        row = db_con.selectone(sql)
        if not row:
            print('work ip 데이터 등록 ')
            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('##insert## : update_list ( catecode | now_page | proc_ip )')
        else:
            amzurl = row[0]
            cateidx = row[1]
            print('[new] cateidx : '+str(cateidx))

            dic_up = dict()
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')
    else:
        print('update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where flg_ref is null and proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where flg_ref is null and proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where flg_ref is null and proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.flg_ref is null and u.proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr


def newlist_ref():
    global ip
    global endpage

    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print(' -- newlist() -- work ip : '+str(ip))

    sql = "select * from update_list where flg_ref = '1' and proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1

        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on a.CateCode=b.catecode and b.flg_ref = '1' where IsHidden='F' and lastcate=1 and b.catecode is null order by up_date_ref asc  "

        if page > endpage:
            page = endpage

        row = db_con.selectone(sql)
        if not row:
            print('work ip 데이터 등록 ')
        else:
            amzurl = row[0]
            cateidx = row[1]
            print('[new] cateidx : '+str(cateidx))

            dic_up = dict()
            dic_up['up_date_ref'] = "getdate()"
            dic_up['list_in_ref'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('##update## : T_CATEGORY (up_date_ref 변경 및 list_in_ref = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"
            dic_in['flg_ref'] = "'1'"

            db_con.insert('update_list', dic_in)  # insert
            print('##insert## : update_list ( catecode | now_page | proc_ip | flg_ref)')

    else:
        print('update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where flg_ref = '1' and proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where flg_ref = '1' and proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where flg_ref = '1' and proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.flg_ref = '1' and u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr

def procLastpage(in_cateidx, in_flg, db_con, list_name):

    if list_name == "list":
        if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
            print('마지막 page')
            sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2 where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        elif in_flg == "no_connect":
            sql = "update T_CATEGORY set up_date = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        elif in_flg == "no_data":
            sql = "update T_CATEGORY set up_date = GETDATE()-1,list_in=2 where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        print('sql : ' + str(sql))
        if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
            sql = "delete from update_list where flg_ref is null and catecode ='" + str(in_cateidx) + "'"
            db_con.execute(sql)
            print('sql : ' + str(sql))
    else:
        if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
            print('마지막 page')
            sql = "update T_CATEGORY set up_date_ref = GETDATE(), list_in_ref=2 where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        elif in_flg == "no_connect":
            sql = "update T_CATEGORY set up_date_ref = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        elif in_flg == "no_data":
            sql = "update T_CATEGORY set up_date_ref = GETDATE()-1,list_in_ref=2 where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

        print('sql : ' + str(sql))
        if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
            sql = "delete from update_list where flg_ref = '1' and catecode ='" + str(in_cateidx) + "'"
            db_con.execute(sql)
            print('sql : ' + str(sql))

    return "0"

# def procDbSet(in_asin, in_cateidx, in_price, db_con, list_name):
#     if list_name == "list":
#         sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
#         rs = db_con.selectone(sql)
#         # print('##select one## sql :' + str(sql))

#         if not rs:  # rs is None
#             print('T_Category_BestAsin (New)')
#             sql = "insert into T_Category_BestAsin (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(
#                 in_cateidx) + "','" + str(in_price) + "',getdate()) "
#             # print('sql :'+str(sql))
#             db_con.execute(sql)
#         else:
#             print('T_Category_BestAsin (Update)')
#             sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(
#                 in_asin) + "'"
#             # print('sql :'+str(sql))
#             db_con.execute(sql)
#     else:
#         sql = "select * from T_Category_BestAsinRef where asin = '{0}'".format(in_asin)
#         rs = db_con.selectone(sql)
#         # print('##select one## sql :' + str(sql))

#         if not rs:  # rs is None
#             print('T_Category_BestAsinRef (New)')
#             sql = "insert into T_Category_BestAsinRef (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(
#                 in_cateidx) + "','" + str(in_price) + "',getdate()) "
#             # print('sql :'+str(sql))
#             db_con.execute(sql)
#         else:
#             print('T_Category_BestAsinRef (Update)')
#             sql = "update T_Category_BestAsinRef set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(
#                 in_asin) + "'"
#             # print('sql :'+str(sql))
#             db_con.execute(sql)

#     return "0"

#reg 숫자만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9]', '', in_str)
    return result

def procDbSet(in_asin, in_cateidx, in_price, db_con, list_name):
    if list_name == "list":
        sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
        rs = db_con.selectone(sql)
        # print('##select one## sql :' + str(sql))

        if not rs:  # rs is None
            print('T_Category_BestAsin (New)')
            sql = "insert into T_Category_BestAsin (asin, cate_idx, reg_date) values ('" + str(in_asin) + "','" + str(
                in_cateidx) + "',getdate()) "
            # print('sql :'+str(sql))
            db_con.execute(sql)
        else:
            print('T_Category_BestAsin (Update)')
            sql = "update T_Category_BestAsin set up_date = GETDATE() where asin='" + str(in_asin) + "'"
            # print('sql :'+str(sql))
            db_con.execute(sql)
    else:
        sql = "select * from T_Category_BestAsinRef where asin = '{0}'".format(in_asin)
        rs = db_con.selectone(sql)
        # print('##select one## sql :' + str(sql))

        if not rs:  # rs is None
            print('T_Category_BestAsinRef (New)')
            sql = "insert into T_Category_BestAsinRef (asin, cate_idx, reg_date) values ('" + str(in_asin) + "','" + str(in_cateidx) + "',getdate()) "
            # print('sql :'+str(sql))
            db_con.execute(sql)
        else:
            print('T_Category_BestAsinRef (Update)')
            sql = "update T_Category_BestAsinRef set up_date = GETDATE() where asin='" + str(in_asin) + "'"
            # print('sql :'+str(sql))
            db_con.execute(sql)

    return "0"

def fun_chart(in_catetmp, in_drive, list_name):
    global errCnt
    global ip
    global endpage
    global timecount
    strSoup1 = ""
    strSoup2 = ""
    baseRH = ""
    next_page = endpage

    curpage = ""
    print('\n fun_chart() ')

    if str(ip).strip() == "222.104.189.18":
        print(' version_check (Skip) local : ' + str(ip))
    else:
        # version 체크
        version_check(in_drive, list_name)

    # https://www.ebay.com/c/accessories/hand-fans?explicit=1&page_type=category&order=highest_reviews&ship_to=KR&max_processing_days=3&max=1000&ref=pagination&page=2
    # FREE shipping / 1000달러 이하 / 1–3 business days / Shop location : Anywhere / ship_to=KR / highest_reviews (정렬)
    # https://www.ebay.com/c/accessories/hand-fans?explicit=1&page_type=category&order=highest_reviews&ship_to=KR&max_processing_days=3&max=1000&free_shipping=true&ref=pagination&page=2
    # id="search-results-top"
    # https://www.ebay.com/b/169291
    # https://www.ebay.com/b/169291?LH_BIN=1&LH_FS=1&LH_ItemCondition=1000|2000&LH_PrefLoc=1&mag=1&rt=nc&_udhi=1400&_udlo=1
    # https://www.ebay.com/b/Womens-Bags-Handbags/169291/bn_738272?LH_BIN=1&LH_FS=1&LH_ItemCondition=1000%7C2000&LH_PrefLoc=1&mag=1&rt=nc&_pgn=1&_udhi=1400&_udlo=1
    # https://www.ebay.com/b/Womens-Bags-Handbags/169291/bn_738272?LH_BIN=1&LH_FS=1&LH_ItemCondition=1000%7C2000&LH_PrefLoc=1&mag=1&rt=nc&_pgn=4&_udhi=1400&_udlo=1
    sp_tmp = str(in_catetmp).split('@')
    cateidx = sp_tmp[0]
    page = sp_tmp[1]
    if str(page) == "":
        page = "1"

    pglow = int(page)

    while pglow <= endpage:
        time.sleep(1)
        print('time.sleep(1)')
        cate_code2 = ""
        amzurl = ""
        soup_view = ""
        page1type = "1"
        print('pglow :' + str(pglow))
        print('page : ' + str(page))
        print('errCnt : ' + str(errCnt))

        result_sour = str(in_drive.page_source)
        if result_sour.find('id="gh-eb-Geo-a-default"') > -1:
            if result_sour.find('Current language English') == -1:
                print(">> 언어 설정 필요 ")
                in_drive.find_element(By.XPATH,'//*[@id="gh-eb-Geo-a-default"]/span[2]').click()
                time.sleep(1)
                in_drive.find_element(By.XPATH,'//*[@id="gh-eb-Geo-a-en"]/span[2]').click()
                time.sleep(2)
            result_sour = in_drive.page_source
            if result_sour.find('Current language English') == -1:
                print(">> 언어 설정 필요 (2)")
                return "E99"

        time.sleep(1)

        if errCnt > 10:
            print('errCnt 10개 이상 강제종료 : ' + str(errCnt))
            procLogSet(db_con, "usa_list", " errCnt 10개 이상 강제종료 : " + str(errCnt))

            db_con.close()
            in_drive.quit()
            os._exit(0)

        list_in_chk_cnt = 0
        sql = "select cate_code2, name, isnull(list_in_chk_cnt,0), isnull(sale_ck_new,''), bcate from t_category where catecode = '{0}'".format(cateidx)
        rs = db_con.selectone(sql)
        print('## ' + str(pglow) + ' ####(fun_chart) select one## sql :' + str(sql))

        if not rs:
            print(" 해당 카테고리코드 없음 : " + str(cateidx))
            procLastpage(cateidx, "no_cateidx", db_con, list_name)
            break

        cate_code2 = rs[0]
        cate_name = rs[1]
        list_in_chk_cnt = rs[2]
        sale_ck_new = str(rs[3]).strip()
        bcate = rs[4]

        #onurl = "https://www.ebay.com/b/177?rt=nc&LH_BIN=1&LH_FS=1&LH_PrefLoc=1&mag=1&_pgn=" +str(page)+ "&_udhi=1400&LH_ItemCondition=2000&_udlo=1"
        #onurl = "https://www.ebay.com/b/" +str(cate_code2)+ "?rt=nc&LH_BIN=1&LH_FS=1&LH_PrefLoc=1&mag=1&_pgn=" +str(page)+ "&_udhi=1400&LH_ItemCondition=1000|2000&_udlo=1"
        if list_name == "list":
            onurl = "https://www.ebay.com/b/" +str(cate_code2)+ "?rt=nc&LH_BIN=1&LH_FS=1&LH_PrefLoc=1&mag=1&_pgn=" +str(page)+ "&_udhi=1400&LH_ItemCondition=1000&_udlo=1"
        else:
            onurl = "https://www.ebay.com/b/" +str(cate_code2)+ "?rt=nc&LH_BIN=1&LH_FS=1&LH_PrefLoc=1&mag=1&_pgn=" +str(page)+ "&_udhi=1400&LH_ItemCondition=2000&_udlo=1"
        print('[' + str(cateidx) + '] page: ' + str(page) + ' | ' + str(cate_code2) + ' | ' + str(cate_name))

        print('page (1) url : ' + str(onurl))
        soup = getSource(str(onurl),in_drive,cateidx)
        if soup == "E":
            errCnt = errCnt + 1
            print('>> Data를 가져올수없음 (SKIP) : ' + str(in_catetmp) + ' | ' + str(onurl))
            procLastpage(cateidx, "no_page", db_con, list_name)
            break
        elif soup == "1" or soup == "2":
            errCnt = 0
            if soup == "2": 
                print('>> 결과가 0 입니다. ')
                # DB에 ishidden 값 변경 list_in_chk_cnt 증가
                sqlu = "update t_category set list_in_chk_cnt = list_in_chk_cnt + 1 where catecode = '{0}'".format(cateidx)
                print(">> t_category : list_in_chk_cnt 증가 ")
                db_con.execute(sqlu)

                if sale_ck_new == "" and bcate == "126":
                    print(">> sale_ck_new 없는 (bcate:126) 카테고리 : {}".format(cateidx))
                    sqlu = "update t_category set ishidden = 'T' where catecode = '{0}'".format(cateidx)
                    print(">> t_category : ishidden  T 변경")
                    db_con.execute(sqlu)

            if soup == "1": print('>> Looks like this page is missing')
            orgSoup = ""
            procLastpage(cateidx, "no_page", db_con, list_name)
            break
        else:
            print('>> get Data Ok (1)')
            orgSoup = str(soup)
            if str(soup).find('s-item s-item--large') > -1 or str(soup).find('item-card--list') > -1:  # 유효한 페이지인지 체크
                orgSoup = str(soup)
            else:
                print('>> 유효한 페이지가 아닙니다.(1) ')
                orgSoup = ""
                procLastpage(cateidx, "no_page", db_con, list_name)
                break

        print('>> Current Page : ' + str(page))
        if str(soup) != "":
            if str(soup).find('s-item s-item--large') > -1:
                print(">>(sp_items) s-item s-item--large")
                sp_items = str(soup).split('s-item s-item--large')
            elif str(soup).find('item-card--list') > -1:
                print(">>(sp_items) item-card--list")
                sp_items = str(soup).split('item-card--list')
            print('>> len(sp_items):' + str(len(sp_items) - 1))

            if len(sp_items) == 0:
                print('>> 해당 페이지에 데이터가 0개.')
                procLastpage(cateidx, "no_page", db_con, list_name)
                break

            itemCnt = len(sp_items)
            itemTmp = "0"
            if str(soup).find('srp-controls__count-heading') > -1:
                itemTmp = getparse(str(soup), 'srp-controls__count-heading', 'Results').replace('"','').replace('>','').replace(',','').strip()
                if int(itemTmp) > 48:
                    itemTmp = "48"
            elif str(soup).find('textual-display brw-controls__count">') > -1:
                itemTmp = getparse(str(soup), 'textual-display brw-controls__count">', 'Results').replace('"','').replace('>','').replace(',','').strip()
                if int(itemTmp) > 48:
                    itemTmp = "48"

            if itemTmp != "0" and len(sp_items) > int(itemTmp):
                itemCnt = int(itemTmp) + 1
                print('>> itemCnt : {}'.format(itemCnt))
            i=1
            while i < itemCnt:
                ea_item = sp_items[i]
                price = "0"
                asin = ""
                #asin = getparse(ea_item, 'www.ebay.com/itm/', '?')
                asin = getparse(ea_item, 'www.ebay.com/itm/', '"')
                if str(asin).find("?") > -1:
                    asin = getparse(asin, '', '?')
                if str(asin).find(">") > -1:
                    asin = getparse(asin, '', '>').replace('"',"")
                if str(ea_item).find('price--displayprice">') > -1:
                    price = getparse(str(ea_item), 'price--displayprice">', '</span>')
                else:
                    price = getparse(str(ea_item), 's-item__price">', '</span>')
                if str(price).find('$') > -1:
                    price = getparse(str(price), '$', '')
                else:
                    print(">> $ 없음 (skip) : {}".format(price))
                    price = ""
                #print('>> asin : ' + str(asin) + ' | ' + str(price))

                ea_stock = ""
                if str(asin) != "" and str(ea_item).find('class="s-item__hotness-nib-corner"') > -1:
                    ea_stock = getparse(str(ea_item),'class="NEGATIVE">','</span>')
                    if ea_stock.find('left') > -1:
                        ea_stock = regRemoveText(ea_stock)
                        print('>> ( {0} ) No Stock only : {1} | {2}'.format(i, ea_stock, asin))
                        i = i + 1
                        continue
                    else:
                        print('>> ( {0} ) Stock : {1} | {2}'.format(i, ea_stock, asin))

                if str(asin) == "":
                    print('>> ( {0} ) No asin : {1} '.format(i, asin))
                elif len(asin) > 13:
                    print('>> ( {0} ) over asin : {1} '.format(i, asin))
                elif str(price) == "" or str(price) == "0":
                    print('>> ( {0} ) No price : {1} '.format(i, asin))
                else:
                    if str(price).find('-') > -1:
                        price = getparse(str(price),'','-')
                    elif str(price).find('<span') > -1:
                        price = getparse(str(price),'','<span')

                    price = str(price).replace('&nbsp;', '').replace('JPY', '').replace('¥', '').replace('$', '').replace('€', '').replace('USD', '').replace(',', '').replace('\xa0','').replace("<", '').replace(">", '').replace("!", '').replace("'", '').strip()
                    price = str(price)[:8]
                    #print(str(asin) + " | " + str(price) + " | DB Insert ")

                    # DB 입력
                    procDbSet(asin, cateidx, price, db_con, list_name)

                    print('>> ( {0} ) : {1}  | {2} [ {3} ] DB Insert '.format(i, cateidx, asin, price))
                    if str(ea_item).find('</section>') > -1:
                        print(">> list End ")
                        break
                i = i + 1

        print('page : '+str(page))
        page = int(page)

        nav_page = getparse(str(soup),'role="navigation"','')
        if str(nav_page).find('class="icon icon--pagination-next"') > -1:
            next_page = getparse(str(soup),'class="pagination__items"','</ol>')
            next_page = getparseR(str(next_page),'pagination__item','</a>')
            next_page = str(next_page).replace('">','')
            if str(next_page).isdigit() == True:
                print('>> page : {} | next_page : {} | 마지막 page: {}'.format(page, next_page, endpage))
                if int(next_page) > int(endpage):
                    next_page = endpage
                    print('>> next_page > endpage ')
                if int(page) > int(next_page):
                    print('>> page > next_page  | 마지막 page: {}'.format(endpage))
                    procLastpage(cateidx, "end", db_con, list_name)
                    break
        if itemCnt < 48:
            print('>> 마지막 page'+str(endpage))
            procLastpage(cateidx, "end", db_con, list_name)
            break
        if int(page) >= int(endpage):
            print('>> 마지막 page'+str(endpage))
            procLastpage(cateidx, "end", db_con, list_name)
            break
        else:
            page += 1
            if page > endpage:
                page = endpage
            print('>> Next page : '+str(page))
            errCnt = 0

            if list_name == "list":
                sql = "update update_list set now_page = '{0}' where flg_ref is null and catecode = '{1}'".format(page, cateidx)
            else:
                sql = "update update_list set now_page = '{0}' where flg_ref = '1' and catecode = '{1}'".format(page, cateidx)
            db_con.execute(sql)
            print('sql : ' + str(sql))

        pglow = pglow + 1
        print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간

    return "0"

def getEndpage(db_con, list_name):
    rtnPage = 30

    sql = " select endpage from python_version_manage where name = '{}'".format(list_name)
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]

    print(">> getEndpage : "+str(rtnPage))

    return rtnPage

def getEndasin(db_con, list_name):
    rtnAsin = 30000

    sql = " select endasin from python_version_manage where name = '{}'".format(list_name)
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]

    print(">> getEndasin : "+str(rtnAsin))

    return rtnAsin


def procBlockGoods(list_name):

    if list_name == "list":
        tableNmae = "T_Category_BestAsin"
        tableNmae_del = "T_Category_BestAsin_del"
    else:
        tableNmae = "T_Category_BestAsinRef"
        tableNmae_del = "T_Category_BestAsinRef_del"

    print('Blocked Goods --> Insert')
    sql = "select asin, cate_idx, DATEADD(day,-3,reg_date) from {} where reg_date < DATEADD(hh,-2,getdate()) and left(code ,1) = 'C'".format(tableNmae_del)
    rows = db_con.select(sql)
    print('>> procBlockGoods (sql) :' + str(sql))

    if not rows:
        print('>> (2시간전) Blocked Goods No ')
    else:
        for rs in rows:
            Dasin = rs[0]
            Dcate_idx = rs[1]
            Dreg_date = rs[2] #생성일 -3일
            print(">> Blocked Goods : " + str(Dcate_idx) + " | " + str(Dasin))

            sql2 = "select * from {} where asin = '{}'".format(tableNmae, Dasin)
            rs2 = db_con.selectone(sql2)
            #print('##select one## sql2 :' + str(sql2))

            if not rs2:  # rs2 is None
                print('>> New T_Category_BestAsin')

                sql = "insert into {} (cate_idx,price,asin,reg_date) values ('{}',0,'{}', getdate()-3)".format(tableNmae, Dcate_idx, Dasin)
                db_con.execute(sql)  # insert
                #print('##insert## (sql):'+str(sql))
                print('##insert## : T_Category_BestAsin : '+str(Dasin))

                sql = "delete from {} where asin ='{}'".format(tableNmae_del, Dasin)
                db_con.execute(sql)
                print('##delete## : T_Category_BestAsin_del : '+str(Dasin))

    return "0"


def doScrollDown(whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break


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

    # list_name = str(sys.argv[1]).strip()
    # print(">> list_name : {}".format(list_name))
    # if list_name == "":
    #     print(">> 입력 값이 없습니다. list로 진행")
    #     list_name = "list"
    list_name = "list"

    # Block Goods --> T_Category_BestAsin 이동
    # procBlockGoods(list_name)
    # time.sleep(2)
    # print('>> time.sleep(2) ')

    now_url = "https://www.ebay.com/"
    # browser = connectDriver(now_url)
    try:
        browser = connectDriverNew(now_url)
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(now_url)
        print(">> connectDriverOld set OK ")
    browser.set_window_size(1200, 900)
    browser.implicitly_wait(3)
    time.sleep(3)
    print('>> time.sleep(3) ')

    browser.get(now_url)
    time.sleep(random.uniform(5,6))

    result = str(browser.page_source)
    if result.find('id="gh-eb-Geo-a-default"') > -1:
        if result.find('Current language English') == -1:
            print(">> 언어 설정 필요 ")
            browser.find_element(By.XPATH,'//*[@id="gh-eb-Geo-a-default"]/span[2]').click()
            time.sleep(1)
            browser.find_element(By.XPATH,'//*[@id="gh-eb-Geo-a-en"]/span[2]').click()
            time.sleep(2)
        result = browser.page_source
        if result.find('Current language English') == -1:
            print(">> 언어 설정 필요 (2)")

    time.sleep(1)
    endpage = 0
    endpage = getEndpage(db_con, list_name)
    if endpage > 9 and endpage < 300:
        print('getEndpage OK')
    else:
        print('getEndpage Check')

    endasin = 0
    endasin = getEndasin(db_con, list_name)
    if endasin > 0:
        print('getEndasin OK' + str(endasin))
    else:
        print('getEndasin Check')

    mainLow = 1
    mainStop = "0"
    while mainLow < 100:
        if list_name == "list":
            sql_cnt = " select count(*) from T_Category_BestAsin "
        else:
            sql_cnt = " select count(*) from T_Category_BestAsinRef "

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
                procLogSet(db_con, "list", " asinCnt : " + str(asinCnt)+' 건)')
                db_con.close()
                browser.quit()
                time.sleep(1)
                os._exit(0)
        print('\n ------------- mainLow : ' + str(mainLow) + ' -------------')

        if list_name == "list":
            rCate = newlist()
        else:
            rCate = newlist_ref()
        if rCate == "1":
            print(" rCate : " + str(rCate))
        else:
            try:
                fun_chart(rCate, browser, list_name)
            except Exception as e:
                print("Exception:{}".format(e))
                print('(SKIP) Exception Error ebay asin ')
                break
        mainLow = mainLow + 1

    print('\n [--- main end ---] ' + str(datetime.datetime.now()))
    print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간
    procLogSet(db_con, "usa_list", " procEnd : " + str(datetime.datetime.now()))

    db_con.close()
    time.sleep(2)
    browser.quit()
    time.sleep(2)
    os._exit(0)

