import datetime
import os
import time
import random
import socket
from selenium import webdriver
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import sys
import func_user
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

db_FS = DBmodule_FR.Database('freeship')

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

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

#중국어 찾기
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

#reg 한글 체크
def regKrStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

#reg 일본어 체크
def regJpStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+",chkStr) #일본어(Katakana/Hiragana/Kanji)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()

    return result_str

# 상품 guid 가져오기 (goodscode --> guid)
def getGuid(gCode):
    rtn_guid = ""
    tmpGuid = str(gCode)[2:]
    tmpGuid = str(tmpGuid).lstrip("0")
    rtn_guid = str(tmpGuid).replace("N", "")

    return str(rtn_guid)

def do_proc(db_con, browser, site_list):

    #### sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where sitecate in ('global','best','usa','mall','de','uk','cn','ref') and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') "
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where sitecate in (" +str(site_list)+ ") and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') and tran_GoodsTitle is null "
    row = db_FS.selectone(sql)
    print('>> ##select ## sql ')

    if not row:
        print('>> 대상 없음 (exit) ')
        return "1"

    url_link = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order.asp" 
    print('>> url_link : ' + str(url_link))
    browser.get(url_link)
    time.sleep(5)
    result2 = browser.page_source
    time.sleep(1)

    if str(result2).find('<div class="skiptranslate') == -1:
        print('>> 대상 없음 ' )
        return "1" 

    lowCnt = 0
    check_cnt = 0

    tran_source = getparse(str(result2),'<div id="google_translate_element">','')
    if str(tran_source).find('<pre>') > -1:
        tran_source = getparse(str(tran_source),'<pre>','')
    if str(tran_source).find('</pre>') > -1:
        tran_source = getparse(str(tran_source),'','</pre>')
    sp_tran = tran_source.split('<input type="hidden"')

    for ea_item in sp_tran:
        time.sleep(0.2)
        tran_title = ""
        ea_tmp = getparse(ea_item,'value="','')
        ea_Iuid = getparse(ea_tmp,'','"')
        ea_Iuid = str(ea_Iuid).replace("\u200b","").replace(",","").replace(" ","").replace("'","").strip()
        if ea_tmp.find('<div>') > -1:
            ea_tmp = str(ea_tmp).replace("<div>","").replace("</div>","").replace("'","").strip()
        tran_title = getparse(ea_tmp,'>','')
        tran_title = replace_main_str(tran_title).replace('<hr>','')
        if str(tran_title).find('inherit;">') > -1:
            tran_title = getparse(str(tran_title),'inherit;">','')

        if str(ea_Iuid) == "":
            print(">> [{}] No ea_Iuid or check ea_Iuid : {}".format(lowCnt, ea_tmp))
        else:
            db_orderno = ""
            sql_s = " select orderno from t_order as o inner join t_order_info as i on i.orderuid = o.uid where i.uid = '{}'".format(ea_Iuid)
            row_search = db_con.selectone(sql_s)
            if row_search:
                db_orderno = row_search[0]
            
            print('>> [{}] {} ({}) | {}'.format(lowCnt, db_orderno, ea_Iuid, tran_title))
            tran_title = tran_title.replace("'","").replace('  ',' ').strip()

            if regJpStrChk(tran_title) == "1": # 일본어 미포함 
                check_cnt = check_cnt + 1
                print(">> [{}] (일본어 존재) : {} ({})".format(lowCnt, db_orderno, ea_Iuid))  
            elif regKrStrChk(tran_title) == "1": # 한글 미포함
                check_cnt = check_cnt + 1
                print(">> [{}] (한글 존재) : {} ({})".format(lowCnt, db_orderno, ea_Iuid))
            else:
                check_cnt = 0

            if check_cnt > 10:
                print(">> Check Tran ")
            else:
                sql_u = "update T_ORDER_INFO set tran_GoodsTitle = dbo.GetCutStr('{}',200,'...') where uid = '{}'".format(tran_title, ea_Iuid)
                db_con.execute(sql_u)
                print(" Update Ok : {} ({}) ".format(db_orderno, ea_Iuid))
        lowCnt = lowCnt + 1

    print(">> check_cnt : {}".format(check_cnt))

    return "0"


def proc_tran(db_con, browser, url_link, type):

    print('>> url_link : ' + str(url_link))
    browser.get(url_link)
    time.sleep(5)
    result2 = browser.page_source
    time.sleep(1)
    if str(result2).find('<input type="hidden"') == -1:
        print('>> 대상 없음 ' )
        return "1" 

    lowCnt = 0
    check_cnt = 0

    tran_source = getparse(str(result2),'<div id="google_translate_element">','')
    if str(tran_source).find('<pre>') > -1:
        tran_source = getparse(str(tran_source),'<pre>','')
    if str(tran_source).find('</pre>') > -1:
        tran_source = getparse(str(tran_source),'','</pre>')
    sp_tran = tran_source.split('<input type="hidden"')

    for ea_item in sp_tran:
        time.sleep(0.2)
        tran_title = ""
        ea_tmp = getparse(ea_item,'value="','')
        ea_Iuid = getparse(ea_tmp,'','"')
        ea_Iuid = str(ea_Iuid).replace("\u200b","").replace(",","").replace(" ","").replace("'","").strip()
        if ea_tmp.find('<div>') > -1:
            ea_tmp = str(ea_tmp).replace("<div>","").replace("</div>","").replace("'","").strip()
        tran_title = getparse(ea_tmp,'>','')
        tran_title = replace_main_str(tran_title).replace('<hr>','')
        if str(tran_title).find('inherit;">') > -1:
            tran_title = getparse(str(tran_title),'inherit;">','')

        if str(ea_Iuid) == "":
            print(">> [{}] No ea_Iuid or check ea_Iuid : {}".format(lowCnt, ea_tmp))
        else:
            db_orderno = ""
            sql_s = " select orderno from t_order as o inner join t_order_info as i on i.orderuid = o.uid where i.uid = '{}'".format(ea_Iuid)
            row_search = db_con.selectone(sql_s)
            if row_search:
                db_orderno = row_search[0]
            
            print('>> [{}] {} ({}) | {}'.format(lowCnt, db_orderno, ea_Iuid, tran_title))
            tran_title = tran_title.replace("'","").replace('  ',' ').strip()

            if type == "title":
                sql_u = "update T_ORDER_INFO set tran_GoodsTitle = dbo.GetCutStr('{}',200,'...') where uid = '{}'".format(tran_title, ea_Iuid)
            elif type == "option":
                sql_u = "update T_ORDER_option set tran_Item = dbo.GetCutStr(N'{}',200,'...') where OrderInfoUid = '{}'".format(tran_title, ea_Iuid)
            db_con.execute(sql_u)
            print(" Update Ok : {} ({}) ".format(db_orderno, ea_Iuid))

        lowCnt = lowCnt + 1

    print(">> check_cnt : {}".format(check_cnt))


def do_proc_red(db_con, browser, site):

    #sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where sitecate = '" +str(site)+ "' and state in ('200','201','421') and tran_GoodsTitle is null "
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where ali_id = '" +str(site)+ "' and state in ('200','201','421') and tran_GoodsTitle is null "
    row = db_FS.selectone(sql)
    print('>> ##select ## sql ')

    if not row:
        print('>> 대상 없음 (exit) ')
        return "1"
    if site == 'red2' :
      url_link = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red2.asp'
      proc_tran(db_con, browser, url_link, "title")
    else :  
      url_link = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red.asp" 
      proc_tran(db_con, browser, url_link, "title")

      url_link = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red_option.asp" 
      proc_tran(db_con, browser, url_link, "option")

    return "0"

def do_proc_red2(db_con, browser, site):

    #sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where sitecate = '" +str(site)+ "' and state in ('200','201','421') and tran_GoodsTitle is null "
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where ali_id = '" +str(site)+ "' and state in ('200','201','421') and tran_GoodsTitle is null "
    row = db_FS.selectone(sql)
    print('>> ##select ## sql ')

    if not row:
        print('>> 대상 없음 (exit) ')
        return "1"
    if site == 'red2' :
      url_link = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red2.asp'
      proc_tran(db_con, browser, url_link, "title")
    else :  
      url_link = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red2.asp" 
      proc_tran(db_con, browser, url_link, "title")

      url_link = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_order_ali_red2_option.asp" 
      proc_tran(db_con, browser, url_link, "option")

    return "0"

def check_proc_red():
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where i.ali_id in ('red') and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') and tran_GoodsTitle is null "
    rows = db_FS.select(sql)
    print('>> ##select ## sql ')
    if not rows:
        return "0"
    else:
        return "1"

def check_proc(site_list):
    flg1 = ""
    flg2 = ""
    flg3 = ""
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where i.ali_id in ('red') and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') and tran_GoodsTitle is null "
    rows = db_FS.select(sql)
    print('>> ##select ## sql ')
    if not rows:
        flg1 = "0"
        
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where i.ali_id in ('red2') and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') and tran_GoodsTitle is null "
    rows = db_FS.select(sql)
    print('>> ##select ## sql ')
    if not rows:
        flg3 = "0"
        
    sql = "select top 1 orderno from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where sitecate in (" +str(site_list)+ ") and RegDate > '2020-12-20 00:00:00' and state in ('200','201','421') and tran_GoodsTitle is null "
    rows = db_FS.select(sql)
    print('>> ##select ## sql ')
    if not rows:
        flg2 = "0"

    if flg1 == "0" and flg2 == "0" and flg3 == "0":
        print('>> 대상 없음 (exit) ')
        db_FS.close()
        print(str(datetime.datetime.now()))
        print(">> End order_title_tran ")
        os._exit(0)


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
    option.add_argument("--disable-gpu")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        browser = webdriver.Chrome(service=s, options=option)
    return browser

if __name__ == '__main__':

    print(">> Start order_title_tran ")
    print(str(datetime.datetime.now()))

    site_list = "'global','best','usa','mall','de','uk','cn','ref','shop','red'"

    # 실행대상 체크
    check_proc(site_list)

    now_url = 'https://dev.freeship.co.kr'
    try:
        browser = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    browser.implicitly_wait(3)
    browser.set_window_size(1400, 1000)
    browser.set_window_position(140, 0, windowHandle='current')


    rtn_flg = "0"
    while( rtn_flg == "0"):

        site_list1 = "'global','best','usa','mall','de','uk','cn','ref','shop'"
        try:
            rtn_flg2 = do_proc_red(db_FS, browser, 'red')
            rtn_flg3 = do_proc_red2(db_FS, browser, 'red2')
            rtn_flg1 = do_proc(db_FS, browser, site_list1)
        except Exception as e:
            print('>> 예외가 발생 (종료) : ', e)
            time.sleep(5)
            rtn_flg = "1"
            break
        else:
            time.sleep(1)
            if rtn_flg1 == "1" and rtn_flg2 == "1" and rtn_flg3 == "1":
                rtn_flg = "1"

        # # 번역 대상 체크
        # rtn_flg1 = check_proc(site_list)
        time.sleep(random.uniform(3,5))

    db_FS.close()
    time.sleep(10)
    browser.quit()
    print(str(datetime.datetime.now()))
    print(">> End order_title_tran ")
    os._exit(0)
