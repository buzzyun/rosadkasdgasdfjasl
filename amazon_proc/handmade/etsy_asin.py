import datetime
import os
import random
import socket
import urllib
from urllib.request import Request, urlopen
from stem import Signal
from selenium import webdriver
from stem.control import Controller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
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
ver = "11.0"

ip = socket.gethostbyname(socket.gethostname())
amzurl = ""
timecount = 0
db_con = DBmodule_FR.Database('handmade')

chkTime = time.time()
print("chkTime : "+str(chkTime))

def connectDriverOld(pgSite):
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
    # option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

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
    # option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
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

def version_check(in_drive):
    global ver
    print("version:" + ver)
    file_path = r"c:/project/"
    file_name = "new_etsy_asin.exe"
    sql = "select version,url from python_version_manage where name = 'list'"
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

def getParserSoup(in_url):

    try:
        print('\n try(1) getParserSoup(in_url)')
        source_code = requests.get(in_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + ' Safari/537.36', 'Referer': 'https://www.etsy.com'})

    except Exception as ex:  # 에러 종류
        if (ex.code == 503):
            print('try(1) 503 에러 해당 :', ex)

            time.sleep(2)
            print('time.sleep(2)')
            # set_new_tor_ip()
            # checkCurrIP()
            # time.sleep(2)

            try:
                print('\n try(2) getParserSoup(in_url)')
                source_code = requests.get(in_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                    random.random()) + ' Safari/537.36', 'Referer': 'https://www.etsy.com'})

            except Exception as ex:  # 에러 종류
                print('try (2) 에러 발생 (skip) ', ex)
                return "1"

            else:
                print('-- try (2) OK --', ex)

        elif (ex.code == 404):
            print('try(1) 404 에러가 발생 (SKIP)', ex)
            return "1"

        else:
            print('try (1) 에러가 발생 (SKIP)', ex)
            return "1"

    else:
        print('try (1) OK ')
        resultSoup = source_code.text

        if str(resultSoup).find('id="fst-hybrid-dynamic-h1"') > -1 or str(resultSoup).find('class="a-section a-text-center"') > -1:
            print('\n - resultSoup Ok (1) - ')
        else:
            print('\n - block retry (1) - ')


            try:
                source_code = requests.get(in_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                        random.random()) + ' Safari/537.36', 'Referer': 'https://www.etsy.com'})

            except Exception as ex:  # 에러 종류
                print('에러가 발생 (3) (SKIP)', ex)
                return "1"
            else:
                resultSoup = source_code.text
                if str(resultSoup).find('id="fst-hybrid-dynamic-h1"') > -1 or str(resultSoup).find('class="a-section a-text-center"') > -1:
                    print('\n - resultSoup Ok (2) - ')
                else:
                    print('\n - block end (2) - ')
                    return "1"

    return str(resultSoup)



def reDoProc(in_drive, in_url):
    result = ""

    time.sleep(1)
    print('>> time.sleep(1) ')
    # set_new_tor_ip()
    # checkCurrIP()
    # time.sleep(3)
    # print('>> time.sleep(3) ')

    print("Test site Connect ")
    result = ""
    try:
        in_drive.get("https://www.etsy.com/")
    except Exception as ex:
        print(' reDoProc url Get Error Skip : ', ex)
    else:                    
        time.sleep(3)
        print('time.sleep(3)')
        result = in_drive.page_source

    in_drive.refresh()
    time.sleep(3)

    print('url :'+str(in_url))
    in_drive.get(in_url)
    time.sleep(3)
    print('time.sleep(3)')

    result = browser.page_source
    #print("result : "+str(result))
    time.sleep(2)
    print('>> time.sleep(2) ')

    return result


def getSource(in_url, in_drive, in_cateidx):

    time.sleep(2)
    print('>> time.sleep(2) ')
    print('url :'+str(in_url))

    result = ""
    try:
        in_drive.get(in_url)
    except Exception as ex:
        print('test_asin Get Error Skip : ', ex)
    else:                    
        time.sleep(4)
        print('time.sleep(4)')

    result = in_drive.page_source
    #print("result : "+str(result))
    time.sleep(4)
    print('>> time.sleep(4) ')

    tmp_result = ""
    if str(result).find('data-search-results-container') > -1 or str(result).find('Search results') > -1:
        print('\n - getSource Ok (1) - ')
    elif str(result).find('Try searching for something else') > -1:
        print('>> Try searching for something else ... (No category) (Skip)')
        # set_new_tor_ip()
        # time.sleep(3)   
        return "2"
    else:
        time.sleep(2)
        print('>> time.sleep(2) ')
        # set_new_tor_ip()
        #checkCurrIP()     
        # time.sleep(3)   
        print('\n - getSource block retry (1) - ')
        return "1"

    return str(result)


def newlist():
    global ip
    global endpage

    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print(' -- newlist() -- work ip : '+str(ip))

    sql = "select * from update_list where proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1

        ## cate_kubun = de 
        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null order by up_date asc "
        #sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and minus_opt = '1' and lastcate=1 and b.catecode is null order by up_date asc "

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
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('##insert## : update_list ( catecode | now_page | proc_ip )')

    else:
        print('update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('cateidx : '+str(cateidx)+ ' | page : ' + str(page))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr


def procLastpage(in_cateidx, in_flg, db_con):

    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
        print('마지막 page')
        sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_connect":
        sql = "update T_CATEGORY set up_date = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_data":
        sql = "update T_CATEGORY set up_date = GETDATE()-1 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    #print('sql : ' + str(sql))
    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
        sql = "delete from update_list where catecode ='" + str(in_cateidx) + "'"
        db_con.execute(sql)
        #print('sql : ' + str(sql))

    return "0"


def procDbSet(in_asin, in_cateidx, in_price, asin_url, db_con):

    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        #sql = "insert into T_Category_BestAsin (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(in_cateidx) + "','" + str(in_price) + "',getdate()) "
        sql = "insert into T_Category_BestAsin (asin, cate_idx, reg_date, asin_url) values ('{}', '{}', getdate(), '{}')".format(in_asin,in_cateidx, asin_url)
        # print('sql :'+str(sql))
        db_con.execute(sql)

    else:
        print('>> T_Category_BestAsin (Update)')
        #sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(in_asin) + "'"
        sql = "update T_Category_BestAsin set up_date = GETDATE() where asin='" + str(in_asin) + "'"
        # print('sql :'+str(sql))
        db_con.execute(sql)

    return "0"


def fun_chart(in_catetmp, in_drive):
    global errCnt
    global ip
    global endpage
    global timecount
    strSoup1 = ""
    strSoup2 = ""
    baseRH = ""

    curpage = ""
    print('\n fun_chart() ')

    if str(ip).strip() == "222.104.189.18":
        print(' version_check (Skip) local : ' + str(ip))
    else:
        # version 체크
        version_check(in_drive)

    # https://www.etsy.com/c/accessories/hand-fans?explicit=1&page_type=category&order=highest_reviews&ship_to=KR&max_processing_days=3&max=1000&ref=pagination&page=2
    # FREE shipping / 1000달러 이하 / 1–3 business days / Shop location : Anywhere / ship_to=KR / highest_reviews (정렬)
    # https://www.etsy.com/c/accessories/hand-fans?explicit=1&page_type=category&order=highest_reviews&ship_to=KR&max_processing_days=3&max=1000&free_shipping=true&ref=pagination&page=2
    # id="search-results-top"

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

        if errCnt > 5:
            print('errCnt 5개 이상 강제종료 : ' + str(errCnt))
            procLogSet(db_con, "usa_list", " errCnt 5개 이상 강제종료 : " + str(errCnt))

            return "1"

        sql = "select amz_cateurl from t_category where catecode = '{0}'".format(cateidx)
        rs = db_con.selectone(sql)
        print('## ' + str(pglow) + ' ####(fun_chart) select one## sql :' + str(sql))

        if not rs:
            print(" 해당 카테고리코드 없음 : " + str(cateidx))
            procLastpage(cateidx, "no_cateidx", db_con)
            break

        amzurl = rs[0]
        if str(amzurl).find('www.etsy.com') > -1:
            # FREE shipping / 1000달러 이하 / 1–3 business days / Shop location : Anywhere / ship_to=KR / highest_reviews (정렬)
            amzurl = str(amzurl) + "&page_type=category&order=highest_reviews&ship_to=KR&max_processing_days=3&max=1000&free_shipping=true&ref=pagination&page=" + str(page)
        # print('[' + str(cateidx) + '] page: ' + str(page) + ' | ' + str(amzurl))
        print('[' + str(cateidx) + '] page: ' + str(page))

        onurl = amzurl
        print('page (1) url : ' + str(onurl))
        soup = getSource(str(onurl),in_drive,cateidx)
        if soup == "1":
            errCnt = errCnt + 1
            print('>> Data를 가져올수없음 (SKIP) : ' + str(in_catetmp) + ' | ' + str(onurl))
            procLastpage(cateidx, "no_data", db_con)
            break
        elif soup == "2":
            errCnt = errCnt + 1
            print('>> No page (category no goods)(SKIP) : ' + str(in_catetmp) + ' | ' + str(onurl))
            procLastpage(cateidx, "end", db_con)
            break
        else:
            print('>> get Data Ok (1)')
            orgSoup = str(soup)
            if str(soup).find('id="search-results-top"') > -1 or str(soup).find('data-result-info') > -1:  # 유효한 페이지인지 체크
                orgSoup = str(soup)
            else:
                print('>> 유효한 페이지가 아닙니다.(1) ')
                orgSoup = ""
                procLastpage(cateidx, "no_page", db_con)
                break

        print(' Current Page : ' + str(page))
        if str(soup) != "":
            if str(soup).find('data-palette-listing-id=') > -1:
                sp_items = str(soup).split('data-palette-listing-id=')
            print('len(sp_items):' + str(len(sp_items) - 1))

            if len(sp_items) == 0:
                print('>> 해당 페이지에 데이터가 0개.')
                procLastpage(cateidx, "no_page", db_con)
                break

            i=0
            while i < len(sp_items):

                ea_item = sp_items[i]
                price = "0"
                asin = ""
                asin = getparse(ea_item, '"', '"')
                # if str(ea_item).find('data-shop-id') == -1:
                #     print('>> ( {0} ) No asin : {1} '.format(i, asin))
                #     i = i + 1
                #     continue
                asin_url = getparse(str(ea_item), 'class="listing-link', '</div>')
                asin_url = getparse(str(asin_url), 'href="', '"').replace('amp;','').strip()
                if asin_url.find(asin) == -1:
                    asin_url = ""
                if str(ea_item).find('class="currency-value">') > -1:
                    price = getparse(str(ea_item), 'class="currency-value">', '</span>')
                else:
                    price = getparse(str(ea_item), "class='currency-value'>", "</span>")
                #print('>> asin : ' + str(asin) + ' | ' + str(price))

                if str(asin) == "":
                    print('>> ( {0} ) No asin : {1} '.format(i, asin))
                elif len(asin) > 11:
                    print('>> ( {0} ) over len : {1} '.format(i, asin))
                elif str(price) == "" or str(price) == "0":
                    print('>> ( {0} ) No price : {1} '.format(i, asin))
                else:
                    if str(price).find('-') > -1:
                        price = getparse(str(price),'','-')
                    price = str(price).replace('&nbsp;', '').replace('JPY', '').replace('¥', '').replace('$', '').replace('€', '').replace('USD', '').replace(',', '').replace('\xa0','').replace("'", '').strip()
                    print(str(asin) + " | " + str(price) + " | DB Insert ")

                    # DB 입력
                    procDbSet(asin, cateidx, price, asin_url, db_con)

                    print('>> ( {0} ) : {1}  | {2} [ {3} ] '.format(i, cateidx, asin, price))

                i = i + 1

        print('\n\n>> page : '+str(page))
        page = int(page)

        nav_page = getparse(str(soup),'"search_pagination"','</nav>')
        # if str(nav_page).find('wt-btn wt-btn--small wt-action-group__item wt-btn--icon wt-is-disabled') > -1:
        if str(nav_page).find('wt-action-group__item wt-btn--icon wt-is-disabled') > -1 or str(nav_page).find('wt-action-group__item.wt-btn--icon.wt-is-disabled') > -1:
            if str(page) <= str(endpage):
                print("Change endpage : {}".format(endpage))
                procLastpage(cateidx, "end", db_con)
                break

        if int(page) >= int(endpage):
            print('>> 마지막 page'+str(endpage))
            procLastpage(cateidx, "end", db_con)
            break
        else:
            page += 1
            if page > int(endpage):
                page = int(endpage)
            print('Next page : '+str(page))
            errCnt = 0

            sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(page, cateidx)
            db_con.execute(sql)
            print('sql : ' + str(sql))

        pglow = pglow + 1
        print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간

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


def doScrollDown(whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break


def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into etsy_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def getAsinCnt(db_con):
    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

if __name__ == '__main__':
    global goods

    errCnt = 0
    errFlg = ""
    print('\n [--- main start ---] ' + str(datetime.datetime.now()))

    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
    time.sleep(4)

    # Block Goods --> T_Category_BestAsin 이동
    procBlockGoods()
    time.sleep(2)
    # print('>> time.sleep(2) ')

    endasin = 0
    endasin = getEndasin(db_con)
    if endasin > 0:
        print('getEndasin OK' + str(endasin))
    else:
        print('getEndasin Check')

    asinCnt = getAsinCnt(db_con)
    if asinCnt > endasin:
        print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
        procLogSet(db_con, "asin_list", " asinCnt : " + str(asinCnt)+' 건)', ip)
        db_con.close()
        time.sleep(1)
        #os._exit(0)

    now_url = "https://www.etsy.com"
    # browser = connectDriver(now_url)
    try:
        browser = connectDriverNew(now_url)
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(now_url)
        print(">> connectDriverOld set OK ")

    browser.set_window_size(1200, 900)
    browser.implicitly_wait(3)

    time.sleep(1)
    print('>> time.sleep(1) ')
    #set_new_tor_ip()
    #checkCurrIP_new()
    #time.sleep(3)
    #print('>> time.sleep(3) ')

    browser.get(now_url)
    time.sleep(3)
    print('>> time.sleep(3) ')

    result = browser.page_source
    # print("result : "+str(result))
    time.sleep(2)
    print('>> time.sleep(2) ')

    if str(result).find('validateCaptcha') > -1:
        print('>> validateCaptcha (auto) ')

        time.sleep(1)
        print('>> time.sleep(1) ')
        # set_new_tor_ip()
        # checkCurrIP()
        # time.sleep(3)
        # print('>> time.sleep(3) ')

        now_url = "https://www.etsy.com/"
        try:
            browser.get(now_url)
        except Exception as ex:
            print('now_url Get Error Skip : ', ex)
        else:                    
            time.sleep(3)
            print('>> time.sleep(3) ')

    endpage = 0
    endpage = getEndpage(db_con)
    if endpage > 9 and endpage < 300:
        print('getEndpage OK')
    else:
        print('getEndpage Check')

    mainLow = 1
    mainStop = "0"
    while mainLow < 100:
        asinCnt = getAsinCnt(db_con)
        if asinCnt > endasin:
            #print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
            procLogSet(db_con, "asin_list", " asinCnt : " + str(asinCnt)+' 건)')
            db_con.close()
            browser.quit()
            time.sleep(1)
            os._exit(0)

        print('\n ------------- mainLow : ' + str(mainLow) + ' -------------')

        rCate = newlist()
        if rCate == "1":
            print(" rCate : " + str(rCate))
        else:
            rtn_Flg = fun_chart(rCate, browser)
            if rtn_Flg == "1":
                db_con.close()
                browser.quit()
                time.sleep(1)
                os._exit(0)

        # if mainLow % 10 == 0:
        #     set_new_tor_ip()
        #     checkCurrIP()
        #     time.sleep(2)

        mainLow = mainLow + 1

    print('\n [--- main end ---] ' + str(datetime.datetime.now()))
    print(" (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간
    procLogSet(db_con, "usa_list", " procEnd : " + str(datetime.datetime.now()))

    db_con.close()
    time.sleep(2)
    browser.quit()
    time.sleep(2)
    os._exit(0)

