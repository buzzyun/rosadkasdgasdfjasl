from ast import Pass
import requests
import socket
import socks
import http.client
from stem import Signal
from stem.control import Controller
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import time
import socket
import os
import chromedriver_autoinstaller
import re
import tran_func
import DBmodule_FR

global errcnt 

db_con = DBmodule_FR.Database('shop__')

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

def connectDriver(tool):
    if tool == 'chrome':
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        driver_path = f'./{chrome_ver}/chromedriver.exe'
        if os.path.exists(driver_path):
            print(f"chrom driver is insatlled: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver})")
            chromedriver_autoinstaller.install(True)
        time.sleep(1)
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        # user_ag = UserAgent().random 
        # options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        # 크롤링 방지 설정을 undefined로 변경 
        #browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 
    elif tool == 'brave':
        path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("window-size=1400x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
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

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip :', response.read())

def set_new_ip():
    #print("set_new_ip()")
    # disable socks server and enabling again
    socks.setdefaultproxy()
    # """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)

def procIpChange(maxCnt):
    wCnt = 0 
    while wCnt < maxCnt:
        set_new_ip()
        print(checkIP())
        time.sleep(2)
        wCnt = wCnt + 1

#db 특수단어 제거
def replaceQueryString(in_word) :
    result = in_word.replace("'","`").replace("&rdquo;"," ").replace('”',' ')
    result = result.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")

    return result

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace(',','|').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp

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

# Depth 1
def newCateDep1(browser):
    print('\n [--- newCateDep1~2 start ---] ')

    path_file = os.getcwd()
    main_url = "https://www.1688.com/"
    print('>> site_url : ' + str(main_url)) 
    browser.get(main_url)
    time.sleep(random.uniform(5,6))   
    result = ""
    result = browser.page_source
    time.sleep(3)
    with open(path_file + "/1688_proc/result_1688.html","w",encoding="utf8") as f: 
        f.write(str(result))

    if result.find('"home-category"') > -1:
        main_category = getparse(result,'"home-category"','<div class="right-box">')
        sp_bcate = str(main_category).split('<a href=')
        print(">> sp_bcate : {}".format(len(sp_bcate)-1))
        low1 = 0
        for ea_bcate in sp_bcate:
            if str(ea_bcate).find('class="f-14 c-name"') > -1:
                bcate_url = getparse(str(ea_bcate),'"','"')
                bcate_name = getparse(str(ea_bcate),'class="f-14 c-name"','</a>')
                bcate_name = getparse(str(bcate_name),'">','')
                bcate_name = replace_str(bcate_name).strip()

                tran_bcate_name = ""
                if regKrStrChk(bcate_name) != "1": # 한글 미포함
                    tran_bcate_name = tran_func.translator(bcate_name, '', 'ko', "")
                if str(tran_bcate_name).strip() == "":
                    tran_bcate_name = bcate_name                
                print("\n\n------------------------------------------------------------------------------------------------------------")
                print(">> ( 1 Depth ) ({}) [{}] | {} | {} ".format(low1, bcate_name, tran_bcate_name, bcate_url))
                print("\n\n------------------------------------------------------------------------------------------------------------")

                dic = dict()
                dic['name'] = "'" + bcate_name + "'"
                dic['kor_name'] = "'" + tran_bcate_name + "'"
                dic['depth'] = 1
                dic['sort'] = low1
                dic['big'] = "'" + tran_bcate_name + "'"

                sql = "select * from t_category where amz_cateurl = '{0}'".format(bcate_url)
                rs = db_con.selectone(sql)
                print('##select one## sql :' +str(sql))
                if not rs: # rs is None
                    print('New Category')
                    dic['amz_cateurl'] = "'" + str(bcate_url) + "'"
                    db_con.insert('t_category', dic)  # insert
                    print('##insert## : t_category')
                else:
                    print('Category 존재')
                    sql_where = " amz_cateurl = '" + str(bcate_url) + "'"
                    db_con.update('t_category', dic, sql_where)  # update
                    print('##update## : t_category')

            low1 = low1 + 1

    print('>> [--- newCateDep 1 End ---] ')
    return "0"


def newCateDep2(in_drive, in_dep):
    print('\n [--- newCateDep2 start ---] ')
    last_ck = 0
    path_file = os.getcwd()

    #sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1 from t_category where depth = '" + str(int(in_dep)-1) + "' and ishidden='F' and lastcate is null "
    sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1 from t_category where depth = '1' and ishidden='F' and lastcate is null "
    print('\n sql:' + str(sql))

    rows = db_con.select(sql)
    print('\n len(rows) :' + str(len(rows)))
    if not rows:
        print('\n ' + str(in_dep) + ' Depth 처리 완료 :' + str(len(rows)))
        return "F"

    cnt = 0
    low = 0
    while low < len(rows):
        cnt = cnt + 1
        bcate_catecode = rows[low][0]
        bcate_catename = rows[low][1]
        bcate_catekor_name = rows[low][2]
        bcate_cateurl = rows[low][3]
        bcate_parent = rows[low][4]
        bcate_bcate = rows[low][5]
        bcate_mcate = rows[low][6]
        bcate_scate = rows[low][7]
        bcate_dcate = rows[low][8]
        bcate_big = rows[low][9]
        bcate_middle = rows[low][10]
        bcate_small = rows[low][11]
        bcate_little = rows[low][12]
        bcate_last = rows[low][13]
        bcate_ecate = rows[low][14]
        bcate_final = rows[low][15]
        bcate_fcate = rows[low][16]
        bcate_final1 = rows[low][17]

        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(bcate_catecode) + ' | ' + str(bcate_catename) + ' | ' + str(bcate_catekor_name) )
        print('\n ' + str(bcate_cateurl))

        in_drive.get(bcate_cateurl)
        time.sleep(random.uniform(5,6))   
        result_site = ""
        result_site = in_drive.page_source
        time.sleep(3)
        with open(path_file + "/1688_proc/result_" +str(bcate_catecode)+ "_stie.html","w",encoding="utf8") as f: 
            f.write(str(result_site))

        low_2 = 0
        if result_site.find('class="ch-menu"') > -1:
            print('class="ch-menu"')
            mcate_source = getparse(str(result_site),'class="ch-menu"','class="right"')
            if mcate_source.find('class="ch-menu-item"') > -1:
                mscate_cnt = 0
                sp_mcate = mcate_source.split('class="ch-menu-item"')
                print(">> sp_mcate ")
                for ea_mcate in sp_mcate:
                    mcate_name = getparse(str(ea_mcate),'class="item-title-text"','</div>')
                    mcate_name = getparse(str(mcate_name),'>','</span>')
                    if mcate_name != "":
                        tran_mcate_name = ""
                        tran_mcate_name = tran_func.translator(mcate_name, '', 'ko', "")
                        if str(tran_mcate_name).strip() == "":
                            tran_mcate_name = mcate_name
                        tran_mcate_name = replace_str(tran_mcate_name).replace("/","&")
                        low_2 = low_2 + 1
                        mcate_url = str(bcate_catecode) + "bcate_" + str(low_2) + "mcate_menu"
                        print(">> ===================================================================================================== ")
                        print(">> ( 2 Depth ) ({}) [{}] | {} | {} ".format(low_2, mcate_name, tran_mcate_name, mcate_url))
                        print(">> ===================================================================================================== ")

                        dic2 = dict()
                        dic2['name'] = "'" + mcate_name + "'"
                        dic2['kor_name'] = "'" + tran_mcate_name + "'"
                        dic2['depth'] = 2
                        dic2['sort'] = low_2
                        dic2['parent'] = bcate_catecode
                        dic2['bcate'] = bcate_catecode
                        dic2['big'] = "'" + bcate_catekor_name + "'"
                        dic2['middle'] = "'" + tran_mcate_name + "'"

                        sql2 = "select * from t_category where amz_cateurl = '{0}'".format(mcate_url)
                        rs2 = db_con.selectone(sql2)
                        #print('##select one## sql2 :' + str(sql2))
                        if not rs2: # rs2 is None
                            print('New 2 Category : {}'.format(mcate_url))
                            dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                            db_con.insert('t_category', dic2)  # insert
                            print('##insert## : t_category')
                            mscate_cnt = mscate_cnt + 1
                        else:
                            print('Category 2 존재 : {}'.format(mcate_url))
                            mscate_cnt = mscate_cnt + 1

                        scate_cnt = 0
                        sql3 = "select catecode from t_category where amz_cateurl = '{0}'".format(mcate_url)
                        rs3 = db_con.selectone(sql3)
                        #print('##select one## sql3 :' + str(sql3))
                        if not rs3:
                            print('>> 해당 mcate_url 없음 :' + str(mcate_url))
                        else:
                            now_mcatecode = rs3[0]
                            print('>> now_mcatecode : {} | {} '.format(now_mcatecode, mcate_url))

                            low3 = 0
                            mcate_item_source = getparse(str(ea_mcate),'<ul class="fd-clr"','')
                            mcate_item_source = getparse(str(mcate_item_source),'class="item">','')
                            sp_mcate_item = mcate_item_source.split('</li>')
                            scate_url = ""
                            for ea_item in sp_mcate_item:
                                scate_name  = getparse(str(ea_item),'alt="','"')
                                scate_url  = getparse(str(ea_item),'href="','"').replace('amp;','').replace('?&','?')
                                sceneSetId  = getparse(str(ea_item),'SetId=','&')
                                sceneId  = getparse(str(ea_item),'sceneId=','&')
                                bizId  = getparse(str(ea_item),'bizId=','&')
                                adsSearchWord = getparse(str(ea_item),'adsSearchWord=','"')
                                #print(">> {} | {} | {} | {} ".format(sceneSetId, sceneId, bizId, adsSearchWord))

                                low3 = low3 + 1
                                if scate_name != "":
                                    tran_scate_name = ""
                                    tran_scate_name = tran_func.translator(scate_name, '', 'ko', "")
                                    if str(tran_scate_name).strip() == "":
                                        tran_scate_name = scate_name
                                    tran_scate_name = replace_str(tran_scate_name).replace("/","&")
                                    print(">> ( 3 Depth ) ({}) [{}] | {} | {} ".format(low3, scate_name, tran_scate_name, scate_url))

                                    dic3 = dict()
                                    dic3['name'] = "'" + scate_name + "'"
                                    dic3['kor_name'] = "'" + tran_scate_name + "'"
                                    dic3['depth'] = 3
                                    dic3['sort'] = low3
                                    dic3['parent'] = now_mcatecode
                                    dic3['bcate'] = bcate_catecode
                                    dic3['mcate'] = now_mcatecode
                                    dic3['big'] = "'" + bcate_catekor_name + "'"
                                    dic3['middle'] = "'" + tran_mcate_name + "'"
                                    dic3['small'] = "'" + tran_scate_name + "'"

                                    sql4 = "select catecode from t_category where amz_cateurl = '{0}'".format(scate_url)
                                    rs4 = db_con.selectone(sql4)
                                    #print('##select one## sql4 :' + str(sql4))
                                    if not rs4:  # rs is None
                                        dic3['amz_cateurl'] = "'" + scate_url + "'"
                                        db_con.insert('t_category', dic3)  # insert
                                        print('##insert## ({}) : t_category : {}'.format("3", tran_scate_name))
                                        scate_cnt = scate_cnt + 1
                                    else:
                                        print('# : 중복 데이터 skip : {}'.format(tran_scate_name))
                                        scate_cnt = scate_cnt + 1



                        if len(sp_mcate_item) > 0 and scate_cnt > 0:
                            sql_u = " update t_category set lastcate = '0' where catecode = '{}'".format(now_mcatecode)
                            print('>> lastcate = 0 처리 : {}'.format(now_mcatecode))
                            db_con.execute(sql_u)
                        else:
                            print('# : 하위카테고리 없음 확인필요 : {}'.format(scate_url))

        low = low + 1
        if mscate_cnt > 0:
            sql_um = " update t_category set lastcate = '0' where catecode = '{}'".format(bcate_catecode)
            print('>> lastcate = 0 처리 : {}'.format(bcate_catecode))
            db_con.execute(sql_um)
            
        print('>> TIME : ' + str(datetime.datetime.now()))

    print('>> [--- newCateDep2 end ---] ')
    return "0"

if __name__ == '__main__':
    print(">> start ")
    errcnt = 0
    browser = connectDriver("chrome")

    # depth 1 
    #newCateDep1(browser)

    # depth 2~3
    newCateDep2(browser, "2")

    db_con.close()
    os._exit(0)
    #input(">> Key : ")

######
