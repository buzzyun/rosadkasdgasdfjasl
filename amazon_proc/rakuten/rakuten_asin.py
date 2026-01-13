# -*- coding: utf-8 -*-
import datetime
import os
import random
import socket
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import re
import subprocess
import shutil
import DBmodule_FR

global timecount
global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

ver = "05.0"

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

def option_parse(in_sour):
    sp_opt_val = str(in_sour).split('<option value="')
    for ea_opt_val in sp_opt_val:
        opt_val = ""
        opt_name = ""
        if str(ea_opt_val).find('selected="">') > -1:
            print(">> option Skip ")
        else:
            #print("ea_opt_val : {}".format(ea_opt_val))
            opt_val = getparse(str(ea_opt_val),'','"')
            opt_name = getparse(str(ea_opt_val),'">','</option>')
            print(">> option : {} | {}".format(opt_val, opt_name))
    return ""


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
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
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
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
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

def replace_jpTitle(title):
    # print(">> Org Title : {}".format(itme_title))
    rtnTitle = title

    i = 0
    while i < 3:
        if title.find('【') > -1:
            repStr = "【" + getparse(title, '【', '】') + "】"
            rtnTitle = rtnTitle.replace(repStr,'').strip()
        if title.find('『') > -1:
            repStr = "『" + getparse(title, '『', '』') + "』"
            rtnTitle = rtnTitle.replace(repStr,'').strip()
        if title.find('≪') > -1:
            repStr = "≪" + getparse(title, '≪', '≫') + "≫"
            rtnTitle = rtnTitle.replace(repStr,'').strip()

        title = rtnTitle
        i = i + 1

    if len(rtnTitle) < 5:
        rtnTitle = title

    rtnTitle = rtnTitle.replace('SALE','').replace('セール','').replace('送料無料','').replace('無料','').replace('クーポン','').replace('オリジナル','').replace('半額','').replace('円','').strip()
    rtnTitle = rtnTitle.replace('【】','').replace('『』','').replace('≪≫','').replace('送料','').replace('％OFF','').replace('楽天','').replace('1位','').replace('宅配便','').replace('宅配','')
    rtnTitle = rtnTitle.replace("即納",'').replace("大人気",'').replace("即納",'').replace("価格",'')
    rtnTitle = rtnTitle.replace("'",'').replace('  ',' ')
    return str(rtnTitle)

def procDbSet(in_asin, in_cateidx, in_price, db_con):
    
    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        sql = "insert into T_Category_BestAsin (asin, cate_idx, price, reg_date) values ('" + str(in_asin) + "','" + str(in_cateidx) + "','" + str(in_price) + "',getdate()) "
        # print('sql :'+str(sql))
        db_con.execute(sql)

    else:
        print('>> T_Category_BestAsin (Update)')
        sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + " where asin='" + str(in_asin) + "'"
        # print('sql :'+str(sql))
        db_con.execute(sql)

    return "0"

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    return result

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

def procDelStopUpdateGoods(db_con):
    dSql = "delete from T_Category_BestAsin where asin in (select g.ali_no from T_Category_BestAsin as a inner join t_goods as g on g.ali_no = a.asin and g.stop_update = '1')"
    print('>> procDelStopUpdateGoods (dSql) :' + str(dSql))
    db_con.execute(dSql)

    return "0"

def del_naver4_remove(db_con):

    print('>> del_naver4_remove --> Insert')
    sql = "select count(*) as cnt from T_Category_BestAsin as a inner join t_goods as g on g.ali_no = a.asin where g.Del_naver = '4' "
    rows = db_con.select(sql)
    print('>> del_naver4_remove (sql) :' + str(sql))
    if not rows:
        print('>> del_naver4_remove 대상 없음 ')
    else:
        sql_del = "delete from T_Category_BestAsin where asin in (select ali_no from T_Category_BestAsin as a inner join t_goods as g on g.ali_no = a.asin where g.Del_naver = '4')"
        print('# sql_del :' + str(sql_del))
        db_con.execute(sql_del)
    return "0"

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

def getAsinCnt(db_con):
    asinCnt = 0
    sql_cnt = " select count(*) from T_Category_BestAsin "
    rowCnt = db_con.selectone(sql_cnt)
    if rowCnt:
        asinCnt = rowCnt[0]
    return asinCnt

def procLastpage(in_cateidx, in_flg, db_con):

    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
        #print('>> 마지막 page')
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


def fun_chart(db_con, in_drive, in_catetmp, endpage, ip, file_name, ver, errCnt, site_url, list_name):

    sp_tmp = str(in_catetmp).split('@')
    cateidx = sp_tmp[0]
    page = sp_tmp[1]
    if str(page) == "":
        page = 1

    today = datetime.date.today()
    yyyy = today.year
    sql = "select cate_code2 from t_category where catecode = '{0}'".format(cateidx)
    rs = db_con.selectone(sql)
    print('>> ## ' + str(page) + ' ####(fun_chart) select one## sql :' + str(sql))

    if not rs:
        print(">> 해당 카테고리코드 없음 : " + str(cateidx))
        procLastpage(cateidx, "no_cateidx", db_con)
        return "0"
    else:
        cate_code2 = rs[0]

    print('>> [' + str(cateidx) + '] page: ' + str(page) + ' ################################################################ ')

    now_url = "https://ranking.rakuten.co.jp/daily/"+str(cate_code2)+"/p="+str(page)+"/"
    time.sleep(2)
    browser.get(now_url)
    time.sleep(random.uniform(3,5))
    result = browser.page_source
    time.sleep(1.5)

    if result.find('アクセスが集中し') > -1 and result.find('id="errorTxt"') > -1:
        print(">> アクセスが集中し、ページを閲覧しにくい状態になっております ")
        now_url = "https://www.rakuten.co.jp/"
        print('\n\n>> main url : ' + str(now_url)) 
        time.sleep(1)
        try:
            browser.get(now_url)
        except Exception as e:
            print(">> browser.get Except ")
            browser.refresh()
            time.sleep(5)

        procLastpage(cateidx, "end", db_con)

        return "C"

    # page 파싱
    pageTmp = getparse(str(result),'<div class="pager">','</div>')
    pageTmp = getparseR(str(pageTmp),'<a href="','"')
    p_endPage = getparseR(str(pageTmp),'/p=','/')
    if p_endPage == "":
        p_endPage = 0
        endpage = 1
    if int(p_endPage) < int(endpage):
        endpage = int(p_endPage)

    rowcnt = 0
    while int(page) <= int(endpage):
        if int(page) != 1:
            now_url = "https://ranking.rakuten.co.jp/daily/"+str(cate_code2)+"/p="+str(page)+"/"
            time.sleep(1)
            browser.get(now_url)
            time.sleep(4)
            result = browser.page_source

        # asin 파싱
        resultTmp = getparse(str(result),'<div id="rnkRankingMain">','<div class="rnkContentsSpaceS">')
        spList = resultTmp.split('class="rnkRanking_rank">')
        print(">> spList Count : {} ".format(len(spList)))

        print("\n\n>> page : {} ============================================".format(page))
        insCnt = 0
        for item in spList:
            itemTmp = getparse(item, '<div class="rnkRanking_imageBox">', '</div>')
            itme_url = getparse(itemTmp, '<a href="', '"')
            itme_id = getparse(itme_url, 'item.rakuten.co.jp/', '"')
            if itme_id[-1:] == "/":
                itme_id = itme_id[:-1]
            itme_id = itme_id.replace('/','_')

            if itme_id == "":
                print("\n ({}) [catecode:{}] [ {} ]  -- itme_id 없음 (Skip)".format(rowcnt, cateidx, itme_id))
            elif itme_url.find('item.rakuten') == -1:
                print("\n ({}) [catecode:{}] [ {} ]  -- itme.rakuten 없음 (Skip) : {}".format(rowcnt, cateidx, itme_id, itme_url))
            elif len(itme_id) > 50:
                print("\n ({}) [catecode:{}] [ {} ]  -- itme_id 50 over (Skip) : {}".format(rowcnt, cateidx, itme_id, itme_url))
            else:
                #repTitle = replace_jpTitle(itme_title)
                price = getparse(item, 'class="rnkRanking_price">', '</div>')
                price = getparse(price, '', '円').replace(",","")
                price = regRemoveText(price)
                if price == "":
                    print("\n ({}) [catecode:{}] [ {} ]  {} -- price 없음 (Skip) ".format(rowcnt, cateidx, itme_id, price))
                elif price.isdigit() == False:
                    print("\n ({}) [catecode:{}] [ {} ]  {} -- price check (Skip) ".format(rowcnt, cateidx, itme_id, price))
                elif int(price) < 100:
                    print("\n ({}) [catecode:{}] [ {} ]  {} -- price Low (Skip) ".format(rowcnt, cateidx, itme_id, price))
                elif int(price) > 100000:
                    print("\n ({}) [catecode:{}] [ {} ]  {} -- price Over (Skip) ".format(rowcnt, cateidx, itme_id, price))
                else:
                    print("\n ({}) [catecode:{}] [ {} ]  {} -- (Insert DB)".format(rowcnt, cateidx, itme_id, price))
                    # DB 입력
                    procDbSet(itme_id, cateidx, price, db_con)

            insCnt = insCnt + 1
            if insCnt > 80:
                print(">> asin 80 Over Break : {}".format(insCnt))
                break
            rowcnt = rowcnt + 1
        page = int(page) + 1

        rep_asin = str(itme_id).replace('_','/').strip()
        now_url = "https://item.rakuten.co.jp/" + str(rep_asin)
        print('\n\n>> now_url : ' + str(now_url)) 
        time.sleep(1)
        try:
            browser.get(now_url)
        except Exception as e:
            print(">> browser.get Except ")
            browser.refresh()
            time.sleep(2)

    if int(page) >= int(endpage):
        print('>> 마지막 page'+str(endpage))
        procLastpage(cateidx, "end", db_con)

    return "0"

def procLogSet(in_DB, in_proc_no, in_proc_memo, ip):
    sql = " insert into amazon_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def newlist(db_con, endpage, ip, listname, site_kbn):
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

        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null order by up_date asc "
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

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    errCnt = 0
    errFlg = ""
    proc_id = ""
    file_name = "new_asin_shop.exe"
    site_url = "https://www.rakuten.co.jp"
    db_con = DBmodule_FR.Database('shop')
    list_name = "list"
    site_kbn = "shop"

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
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
    # procBlockGoods(db_con)
    # time.sleep(2)
    # print('>> time.sleep(2) ')

    # delete stopUpdateGoods 
    procDelStopUpdateGoods(db_con)
    time.sleep(1)

    # del_naver (4) 재등록 후 삭제할 데이터 ---> asin list 에서 제거
    del_naver4_remove(db_con)
    time.sleep(2)
    print('>> time.sleep(2) ')

    endpage = 0
    endpage = getEndpage(db_con,'list')
    endasin = 0
    endasin = getEndasin(db_con,'list')
    if endasin > 0:
        print('>> getEndasin OK' + str(endasin))
    else:
        print('>> getEndasin Check')

    asinCnt = getAsinCnt(db_con)
    if asinCnt > endasin:
        print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
        #am_asin.procLogSet(db_con, "asin_list", " asinCnt : " + str(asinCnt)+' 건)', ip)
        db_con.close()
        time.sleep(1)
        os._exit(0)

    main_url = "https://www.rakuten.co.jp"
    try:
        shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
    except FileNotFoundError:
        pass

    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    # Open the debugger chrome
    try:
        proc_id = subprocess.Popen(filePath_86)
    except FileNotFoundError:
        proc_id = subprocess.Popen(filePath)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(options=option)
    #browser.set_window_size(1200, 900)
    #browser.set_window_position(140, 0, windowHandle='current')
    #browser.implicitly_wait(3)
    time.sleep(2)

    mainLow = 1
    mainStop = "0"
    while mainLow < 100:
        asinCnt = getAsinCnt(db_con)
        if asinCnt > endasin:
            #print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
            procLogSet(db_con, "asin_list", " asinCnt : " + str(asinCnt)+' 건)', currIp)
            db_con.close()
            browser.quit()
            time.sleep(1)
            print("proc1 = ", proc_id.pid)
            subprocess.Popen.kill(proc_id)
            os._exit(0)

        print('>> ------------- mainLow : ' + str(mainLow) + ' -------------')

        rCate = newlist(db_con, endpage, currIp, list_name, site_kbn)
        if rCate == "1":
            print(">> rCate : " + str(rCate))
        else:
            sp_tmp = str(rCate).split('@')
            cateidx = sp_tmp[0]
            test_asin = ""
            sql = "select top 1 ali_no from t_goods where IsDisplay = 'T' order by RegDate desc "
            rs_Asin = db_con.selectone(sql)
            if rs_Asin:
                test_asin = rs_Asin[0]
                print('>> [' +str(rCate)+ '] test_asin :' + str(test_asin))
                if test_asin != "":
                    rep_asin = str(test_asin).replace('_','/').strip()
                    test_url = "https://item.rakuten.co.jp/" + str(rep_asin)
                    try:
                        browser.get(test_url)
                    except Exception as ex:
                        print('>> test_asin Get Error Skip : ', ex)
                    time.sleep(2)

            fun_chart(db_con, browser, rCate, endpage, currIp, file_name, ver, errCnt, site_url, list_name)

        mainLow = mainLow + 1

    print('>> [--- main end ---] ' + str(datetime.datetime.now()))
    db_con.close()
    time.sleep(2)
    print("proc1 = ", proc_id.pid)
    subprocess.Popen.kill(proc_id)
    browser.quit()
    time.sleep(2)
    os._exit(0)



