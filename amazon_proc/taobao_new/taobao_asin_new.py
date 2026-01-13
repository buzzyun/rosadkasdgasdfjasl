import os
os.system('pip install --upgrade selenium')
import time
import datetime
import random
import socket
import urllib
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import subprocess
import taobao_func
import DBmodule_FR

ver = "01.19"
print(">> ver:{}".format(ver))

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
    option.add_argument("--disable-gpu")
    if str(kbn) == "Y":
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
    option.add_argument("--disable-gpu")
    if str(kbn) == "Y":
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
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

def connectDriver(tool):
    global set_browser
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    if tool == 'chrome':
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_argument("user-data-dir={}".format(userProfile))
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options) 

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')  
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random())\
            + " Safari/537.36, 'Referer': 'https://open-demo.otcommerce.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'brave':
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return browser

def replaceStr(in_word) :
    result = in_word.replace("'","`")
    result = result.replace("★","").replace("◆","").replace("/"," & ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","ー").replace("&times;"," x ").replace("、"," . ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")
    result = result.replace('\ue244','').replace('■','')

    return result

def getEndpage(db_con, listname):
    rtnPage = 30

    sql = " select endpage from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnPage = rs[0]

    print(">> getEndpage : "+str(rtnPage))

    return rtnPage

def getEndasin(db_con, listname):
    rtnAsin = 30000
    sql = " select endasin from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnAsin = rs[0]

    print(">> getEndasin : "+str(rtnAsin))

    return rtnAsin

def getAsinCnt(db_con, list):
    asinCnt = 0
    if list == "list":
        sql_cnt = " select count(*) from T_Category_BestAsin where catecode < 3000 "
    else:
        sql_cnt = " select count(*) from T_Category_BestAsin where catecode >= 3000 "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

def getSortType(db_con, listname):
    rtnType = ''
    sql = " select sort_type from python_version_manage where name = '{}'".format(listname)
    rs = db_con.selectone(sql)
    if rs:
        rtnType = rs[0]
    print(">> getSortType : "+str(rtnType))
    return rtnType

def has_duplicates(seq):
    len1 = len(seq)
    len2 = len(set(seq))
    dupCnt = len1 - len2
    return dupCnt


def set_language(browser):
    lang_name = ""
    print(">> set_language ")
    if browser.find_element(By.XPATH,'//*[@id="select-language"]/img'):
        time.sleep(0.5)
        lang_name = browser.find_element(By.XPATH,'//*[@id="select-language"]/img').accessible_name
        if str(lang_name).find('Korean') > -1:
            print(">> Korean OK ")
        else:
            browser.find_element(By.XPATH,'//*[@id="select-language"]').click()
            time.sleep(0.5)
            browser.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/div[3]/div/div/div/ul/li[2]').click()
            time.sleep(4)

            if browser.find_element(By.XPATH,'//*[@id="select-language"]/img'):
                lang_name = browser.find_element(By.XPATH,'//*[@id="select-language"]/img').accessible_name

    return str(lang_name)

def procLogSet(in_DB, in_proc_no, in_proc_memo, ip):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def newlist(db_con, endpage, ip):

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
        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY as a left outer join update_list b on(a.CateCode=b.catecode) where a.catecode > 10000 and IsHidden='F' and lastcate='1' and b.catecode is null order by up_date asc "

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

def procLastpage(in_cateidx, in_flg, db_con):

    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
        print('>> 마지막 page')

        if in_flg == "no_cateidx": # category_used_chk : 1 -> 카테고리 Skip 할수있게 표기
            sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2,used_flg = 'N', category_used_chk='1' where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)
        else:
            sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2,used_flg = 'N' where catecode='" + str(in_cateidx) + "'"
            db_con.execute(sql)

    elif in_flg == "no_connect":
        sql = "update T_CATEGORY set up_date = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_data":
        sql = "update T_CATEGORY set up_date = GETDATE()-1,used_flg = 'N' where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    print('>> sql : ' + str(sql))
    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
        sql = "delete from update_list where catecode ='" + str(in_cateidx) + "'"
        db_con.execute(sql)
        print('>> sql : ' + str(sql))

    return "0"


def procDbSet(in_asin, in_cateidx, in_price, in_istmall, in_sold_cnt, in_title, db_con):

    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        sql = "insert into T_Category_BestAsin (asin, catecode, price, isTmall, sold_cnt, title) values ('" + str(in_asin) + "','" + str(in_cateidx) + "'," + str(in_price) + ",'" + str(in_istmall) + "', " + str(in_sold_cnt) + ",'" + str(in_title) + "' )"
        #print('>> sql :'+str(sql))
        db_con.execute(sql)
    else:
        print('>> T_Category_BestAsin (Update)')
        sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + ", catecode = '" + str(in_cateidx) + "', title = '" + str(in_title) + "', isTmall = '" + str(in_istmall) + "', sold_cnt = " + str(in_sold_cnt) + " where asin='" + str(in_asin) + "'"
        #print('>> sql :'+str(sql))
        db_con.execute(sql)

    return "0"


def checkDelAsin(db_con, asin):
    # print(">> asin Check ")
    rtnCode = ""
    sql = " select asin, code from T_Category_BestAsin_del where code in ( 'S01','S02','D49', 'D03', 'D47', 'D09', 'D12' ) and asin = '{}'".format(asin)
    rs = db_con.selectone(sql)
    if rs:
        code = rs[1]
        print(">> Skip Aasin : {} : code : {}".format(asin, code))
        rtnCode = str(code)
    return rtnCode

def fun_chart(db_con, browser, CateCode, endpage, currIp, file_name, ver, errCnt, sort_type):

    # rtn_lang = set_language(browser)
    # if rtn_lang.find('Korean') > -1:
    #     print(">> Lang Set Ok : {}".format(rtn_lang))

    itemList = []
    print('>> fun_chart() ')
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, browser, file_name, ver, "list_api") # version 체크

    sp_tmp = str(CateCode).split('@')
    cateidx = sp_tmp[0]
    page = sp_tmp[1]
    if str(page) == "":
        page = "1"
    pglow = int(page)
    sql = "select amz_cateurl, name, kor_name, ExternalId, InternalId, isnull(sale_ck_new,'') from t_category where catecode = '{0}'".format(cateidx)
    rs = db_con.selectone(sql)
    print('>> ## ' + str(pglow) + ' ####(fun_chart) select one## sql :' + str(sql))
    if not rs:
        print(">> 해당 카테고리코드 없음 : " + str(cateidx))
        procLastpage(cateidx, "no_cateidx", db_con)
        return "1"

    amzurl = rs[0]
    cate_name = rs[1]
    cate_korname = rs[2]
    ExternalId = rs[3]
    InternalId = rs[4]
    sale_ck_new = rs[5]

    if sale_ck_new == "":
        endpage = int(endpage) / 2 
        print(">> sale_ck_new : {} -> endpage :{} 변경 (1/2)".format(sale_ck_new, endpage))
    else:
        print(">> sale_ck_new : {} | endpage :{} ".format(sale_ck_new, endpage))
    print('>> [{}] {} | {} | ({} | {}) page: {} | {}'.format(cateidx, cate_name, cate_korname, ExternalId, InternalId, page, amzurl))

    try:
        browser.get(amzurl)
    except Exception as e:
        print(">> Check Please Exception Url : {}".format(amzurl))
        print(">> data 없음 (end) : " + str(cateidx))
        procLastpage(cateidx, "end", db_con)
        return "1"

    time.sleep(random.uniform(5,7))
    result = str(browser.page_source)
    if str(result).find('<div class="listing-wrap"') == -1:
        print(">> Check Please page_source ")

        if str(result).find('<h1> 404 Not Found </h1>') == -1:
            print(">> 404 Not Found ")
            print(">> data 없음 (end) : " + str(cateidx))
            procLastpage(cateidx, "no_cateidx", db_con)
            return "1"

    idx_from = 0
    goodsCnt = 0
    while pglow <= endpage:
        time.sleep(1)
        print('>> time.sleep(1)')
        print('>> pglow :' + str(pglow))

        # amzurl = amzurl + "&sort_by="+str(sort_type)+"&cost%5Bfrom%5D=&cost%5Bto%5D=800&features%5BIsStock%5D=true"
        amzurl = amzurl + "&cost%5Bfrom%5D=&cost%5Bto%5D=800"
        if str(page) == "1":
            now_url = amzurl
        else:
            now_url = amzurl + "&from=" + str(idx_from)
        print('>> [' + str(cateidx) + '] page: ' + str(page) )
        print('>> now_url : {}'.format(now_url) )

        browser.get(now_url)
        time.sleep(random.uniform(6,8))

        result = str(browser.page_source)
        if str(result).find('<div class="listing-wrap">') == -1:
            time.sleep(4)

        if str(browser.page_source).find('<div class="listing-wrap">') == -1:
            print(">> Check Please page_source ")
            print(">> data 없음 (end) : " + str(cateidx))
            procLastpage(cateidx, "end", db_con)
            break

        result_source = getparse(str(browser.page_source),'<div class="listing-wrap"','</nav>')
        result_nav = getparse(str(result_source),'<nav>','')
        result_nav_tmp = getparse(str(result_nav),'class="page-item active">','</a>')
        curr_page = getparse(str(result_nav_tmp),'search-click page-link">','').strip()
        curr_from = getparse(str(result_nav_tmp),'from=','"').strip()
        print(">> curr_page : {} | curr_from : {}".format(curr_page, curr_from))
        if curr_from == "":
            idx_from = 40
        else:
            idx_from = int(curr_from) + 40

        result_list = getparse(str(result_source),'','<nav>')
        result_list_sp = result_list.split('class="product-item ')
        if len(result_list_sp) == 0:
            print(">> Item 0 ")
            print('>> no_data page'+str(endpage))
            procLastpage(cateidx, "no_data", db_con)
            break

        pageInCnt = 0
        pageUpdCnt = 0
        for ea_item in result_list_sp:
            asin = getparse(str(ea_item),'data-product-id="','"')

            if asin != "":
                goodsCnt = goodsCnt + 1
                itemList.append(asin)
                title = getparse(str(ea_item),'class="item-product__title">','</a>')
                price = getparse(str(ea_item),'itemprop="price"','>')
                price = getparse(str(price),'content="','"')
                sold_cnt = getparse(str(ea_item),'class="sold-block">','</span>')
                sold_cnt = getparse(str(sold_cnt),'sold:','').strip()
                if sold_cnt == "":
                    sold_cnt = 0
                else:
                    sold_cnt = int(sold_cnt.replace(',',''))
                istmall = "F"
                title = replaceStr(title)
                if str(ea_item).find('class="item-product__rubric-tmall"') > -1:
                    istmall = "T"
                rtnCode = checkDelAsin(db_con, asin)

                if asin.find('abb-') > -1:
                    print(">> abb-포함 asin (skip) : {}".format(asin))
                    rtnCode = "P07"
                if taobao_func.findChinese(title):
                    print('>> findChinese title (Skip) : {}'.format(title))
                    rtnCode = "D02"

                if rtnCode == "":
                    asinSql = " select ali_no from t_goods where ali_no = '{}'".format(asin)
                    asinrow = db_con.selectone(asinSql)
                    if asinrow:
                        print(">> [DB 존재 Skip] ({}) [ {} ] ( {} )  ".format(goodsCnt, asin, price))
                        pageUpdCnt = pageUpdCnt + 1
                    else:
                        procDbSet(asin, cateidx, price, istmall, sold_cnt, title, db_con) # DB 입력
                        print(">>({}) [ {} ] ( {} ) | {} | {} | {} | {} ".format(goodsCnt, asin, price, cateidx, istmall, sold_cnt, title[:20]))
                        pageInCnt = pageInCnt + 1
                else:
                    print(">>Skip : ({}) [ {} ] ( {} ) | {} | {} | {} | {} ".format(goodsCnt, asin, price, istmall, sold_cnt, title[:20], rtnCode))

        dupCount = has_duplicates(itemList)
        print(">> 중복 아이템수 : {}".format(dupCount))
        print(">> page(DB존재) : {} | pageInCnt(DB Ins) : {}".format(pageUpdCnt, pageInCnt))

        #print('>> page : '+str(page))
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

            sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(page, cateidx)
            db_con.execute(sql)
            print('>> sql : ' + str(sql))

        time.sleep(2)
        pglow = pglow + 1

    print(">> goodsCnt : {}".format(goodsCnt))
    return "0"

def billChk(browser, db_con):
    billChk = "https://open-demo.otcommerce.com/admin/?cmd=Reports&do=billing"
    browser.get(billChk)
    print(">> url : {}".format(billChk))
    time.sleep(4)
    if str(browser.page_source).find('Balance:') > -1:
        Billing = getparse(str(browser.page_source),'Balance:','</div>')
        Billing = getparse(Billing,'class="badge weight-normal font-13">','$').strip()
        print(">> Balance: {}".format(Billing))
        time.sleep(2)
        if str(Billing).replace('.','').isdigit():
            uSql = "update python_version_manage set api_balance = {}, api_balance_date = getdate() where name = 'goods_api'".format(Billing)
            print(">> uSql : {}".format(uSql))
            db_con.execute(uSql)
    return "0"

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
    proc = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)
    return proc, browser

if __name__ == '__main__':

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    currIp = socket.gethostbyname(socket.gethostname())
    file_name = "new_taobao_asin_new.exe"
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

    db_con = DBmodule_FR.Database('taobao')
    list_name = "list_api"
    print('>> fun_chart() ')
    if str(currIp).strip() != "222.104.189.18":
        version_check2(db_con, file_name, ver, list_name) # version 체크

    endasin = 0
    endasin = getEndasin(db_con,list_name)
    if endasin > 0:
        print('>> getEndasin OK : ' + str(endasin))
    else:
        print('>> getEndasin Check')

    endpage = 0
    endpage = getEndpage(db_con,list_name)
    if endpage > 9 and endpage < 300:
        print('>> getEndpage OK')
    else:
        print('>> getEndpage Check')

    time.sleep(1)
    now_url = "https://open-demo.otcommerce.com/ik.php"
    try:
        print(">> connectDriverNew set ")
        browser = connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverNew Exception : {}".format(e))
        try:
            print(">> connectDriverOld set ")
            browser = connectDriverOld(now_url, "")
        except Exception as e:
            print(">> connectDriverOld Exception : {}".format(e))
        else:
            print(">> connectDriverOld Ok")

    # now_url = "https://open-demo.otcommerce.com/ik.php"
    # try:
    #     proc_id, browser = connectSubProcess()
    #     #proc_id, browser = connectSubProcessNew()
    #     print("proc_id(pid) = {}".format(proc_id.pid))
    # except Exception as e:
    #     print('예외가 발생 (종료) : ', e)
    # else:
    #     print('connectDriver 연결 OK')
    time.sleep(2)
    #browser.set_window_size(1600, 1000)

    browser.get(now_url)
    time.sleep(4)
    if str(browser.page_source).find('Instance Key') > -1:
        print(">> Login Need ")
        taobao_func.demo_login_new(browser)
        time.sleep(2)

    if str(browser.current_url).find('https://open-demo.otcommerce.com/admin/') > -1:
        print(">> Login Ok ")
        billChk(browser, db_con) # api 잔액체크
        time.sleep(1)
        browser.get('https://open-demo.otcommerce.com/')
        time.sleep(3)
        i = 0
        # while i < 3:
        #     rtn_lang = set_language(browser)
        #     if rtn_lang.find('Korean') > -1:
        #         print(">> Lang Set Ok : {}".format(rtn_lang))
        #         break
    else:
        print(">> Login Fail Input Key : ")

    mainLow = 1
    errCnt = 0
    mainStop = "0"
    while mainLow < 10000:
        asinCnt = getAsinCnt(db_con, list_name)
        if asinCnt > endasin:
            print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
            procLogSet(db_con, "asin_new_list", " asinCnt : " + str(asinCnt)+' 건)', currIp)
            db_con.close()
            browser.quit()
            time.sleep(1)
            os._exit(0)

        sort_type = getSortType(db_con, 'list_api')
        print(">> sort_type : {}".format(sort_type))

        print('>> ------------- mainLow : ' + str(mainLow) + ' -------------')
        rCate = newlist(db_con, endpage, currIp)
        if rCate == "1":
            print(">> rCate : " + str(rCate))
        else:
            fun_chart(db_con, browser, rCate, endpage, currIp, file_name, ver, errCnt, sort_type)

        mainLow = mainLow + 1

    print('>> [--- main end ---] ' + str(datetime.datetime.now()))
    time.sleep(5)
    db_con.close()
    browser.quit()
    # try:
    #     subprocess.Popen.kill(proc_id)
    # except Exception as e:
    #     print(">> subprocess.Popen.kill(proc_id) exception")
    print(">> end ")
    os._exit(0)
