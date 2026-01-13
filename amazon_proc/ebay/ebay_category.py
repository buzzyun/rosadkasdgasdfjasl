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
import DBmodule_FR

global errcnt 

db_con = DBmodule_FR.Database('REF')

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
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        # 크롤링 방지 설정을 undefined로 변경 
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

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

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace(',','|').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp

# Depth 1~2
def newCateDep1(browser):
    print('\n [--- newCateDep1~2 start ---] ')

    site_url = "https://pages.ebay.com/sitemap.html"
    print('>> site_url : ' + str(site_url)) 
    browser.get(site_url)
    time.sleep(random.uniform(5,6))   
    result = ""
    result = browser.page_source
    time.sleep(3)
    # with open("result_ebay_stiemap.html","w",encoding="utf8") as f: 
    #     f.write(str(result))

    if result.find('id="buy" class="h2content"') > -1:
        buy_category = getparse(result,'id="buy" class="h2content"','id="sell" class="h2content">')
        buy_category = getparse(buy_category,'<h3>All categories</h3>','</div>')

        sp_bcate = str(buy_category).split('<h4>')
        print(">> sp_bcate : {}".format(len(sp_bcate)-1))
        low1 = 0
        for ea_bcate in sp_bcate:
            if ea_bcate != "":
                bcate_tmp = getparse(str(ea_bcate),'','</h4>')
                bcate_url = getparse(str(bcate_tmp),'href="','">').replace("'","").strip()
                bcate_name = getparse(str(bcate_tmp),'">','</a>')
                bcate_name = replace_str(bcate_name)
                bcate_code = getparseR(getparse(str(bcate_url),'','/bn'),'/','')
                print("\n\n-----------------------------------------------------------------------------")
                print(">> [{}] {}   |   {}    |    {} ".format(low1, bcate_code, bcate_name, bcate_url))

                sql = "select * from t_category where cate_code2 = '{0}'".format(bcate_code)
                rs = db_con.selectone(sql)
                print('##select one## sql :' +str(sql))

                trans_text = ""
                dic = dict()
                dic['name'] = "'" + bcate_name + "'"
                dic['kor_name'] = "'" + trans_text + "'"
                dic['depth'] = 1
                dic['sort'] = low1
                dic['big'] = "'" + bcate_name + "'"
                dic['cate_code2'] = "'" + bcate_code + "'"
                dic['amz_cateurl'] = "'" + str(bcate_url) + "'"

                if not rs: # rs is None
                    print('New Category')
                    db_con.insert('t_category', dic)  # insert
                    print('##insert## : t_category')
                else:
                    print('Category 존재 : {} '.format(bcate_code))

                # 1depth New CateCode 
                sql = "select catecode from t_category where cate_code2 = '{0}'".format(bcate_code)
                rs = db_con.selectone(sql)
                if rs:
                    now_catecode = rs[0]
                    print('>> [ 1depth ] New catecode:' + str(now_catecode))

                    ea_bcate = getparse(str(ea_bcate),'<ul class="itemcols">','</ul>')
                    sp_mcate = str(ea_bcate).split('<li>')
                    print(">> sp_mcate : {}".format(len(sp_mcate)-1))
                    low2 = 0
                    for ea_mcate in sp_mcate:
                        if ea_mcate != "":
                            mcate_tmp = getparse(str(ea_mcate),'href="','</a>')
                            mcate_url = getparse(str(mcate_tmp),'','">').replace("'","").strip()
                            mcat_name = getparse(str(mcate_tmp),'">','')
                            mcat_name = replace_str(mcat_name)
                            mcate_code = getparseR(getparse(str(mcate_url),'','/bn'),'/','')
                            print(">>    ({}) {}   |   {}    |    {} ".format(low2, mcate_code, mcat_name, mcate_url))
                            
                            sql2 = "select * from t_category where cate_code2 = '{0}'".format(mcate_code)
                            rs2 = db_con.selectone(sql2)
                            print('##select one## sql2 :' + str(sql2))                        

                            trans_text_2 = ""
                            dic2 = dict()
                            dic2['name'] = "'" + mcat_name + "'"
                            dic2['kor_name'] = "'" + trans_text_2 + "'"
                            dic2['depth'] = 2
                            dic2['sort'] = low2
                            dic2['parent'] = now_catecode
                            dic2['bcate'] = now_catecode
                            dic2['big'] = "'" + bcate_name + "'"
                            dic2['middle'] = "'" + mcat_name + "'"
                            dic2['cate_code2'] = "'" + mcate_code + "'"
                            dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"

                            if not rs2: # rs2 is None
                                print('New Category')
                                db_con.insert('t_category', dic2)  # insert
                                print('##insert## : t_category')
                            else:
                                print('Category 존재 : {} '.format(mcate_code))

                        low2 = low2 + 1
            low1 = low1 + 1

    print('>> [--- newCateDep 1~2 End ---] ')
    return "0"


# Depth 3~
def newCateDep3(browser, in_dep):
    global errcnt
    print('\n [--- newCateDep3~ start ---] ')

    sql = " select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1, cate_code2 from T_CATEGORY where ishidden = 'F' and depth = " + str(int(in_dep)-1)+ " and lastcate is null and proc_chk is null and skip_cnt < 2"

    sql = " select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1, cate_code2 from T_CATEGORY where ishidden = 'F' and depth = " + str(int(in_dep)-1)+ " and lastcate is null and proc_chk is null and skip_cnt < 2 and cate_code2 in ('80914','73353','41372','113526','261044','183460','10885')"

    rows = db_con.select(sql)
    print('>> len(rows) :' + str(len(rows)))
    print('##select ## sql :' +str(sql))

    if not rows:
        print('>> ' + str(in_dep) + ' Depth 처리 완료 :' + str(len(rows)))
        return "F"

    cnt = 0
    low2 = 0
    rtnCode = ""
    while low2 < len(rows):
        cnt = cnt + 1
        now_catecode = rows[low2][0]
        now_catename = rows[low2][1]
        now_catekor_name = rows[low2][2]
        now_cateurl = rows[low2][3]

        now_parent = rows[low2][4]
        now_bcate = rows[low2][5]
        now_mcate = rows[low2][6]
        now_scate = rows[low2][7]
        now_dcate = rows[low2][8]
        now_big = rows[low2][9]
        now_middle = rows[low2][10]
        now_small = rows[low2][11]
        now_little = rows[low2][12]
        now_last = rows[low2][13]
        now_ecate = rows[low2][14]
        now_final = rows[low2][15]
        now_fcate = rows[low2][16]
        now_final1 = rows[low2][17]
        now_cate_code2 = rows[low2][18]

        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(now_catecode) + ' | ' + str(now_catename) + ' | ' + str(now_catekor_name) + ' | ' + str(now_cate_code2))
        print('\n ' + str(now_cateurl))

        time.sleep(1)
        print('time.sleep(1)')

        site_url = "https://www.ebay.com/b/{}".format(now_cate_code2)
        print('>> site_url : ' + str(site_url))
        browser.get(site_url)
        time.sleep(random.uniform(5,6))   
        result = ""
        result = browser.page_source
        time.sleep(3)
        # with open("result_ebay_leftmenu.html","w",encoding="utf8") as f: 
        #     f.write(str(result))

        if str(result).find('Shop by Category</h2>') == -1:
            print('>> No Shop by Category : ' + str(datetime.datetime.now()))
            if str(result).find('Please verify yourself to continue') > -1:
                print('>> Please verify yourself to continue : ' + str(datetime.datetime.now()))

            sql_u = "update t_category set skip_cnt = skip_cnt + 1 where cate_code2 = '{}'".format(now_cate_code2)
            print('>> sql_u : {}'.format(sql_u))
            db_con.execute(sql_u)

            procIpChange(5)
            errcnt = errcnt + 1
            #return "E"

            if errcnt > 7:
                print('>> ** Error over 7 ** ')
                rtnCode = "E"
                break
        else:
            if result.find('Shop by Category</h2>') > -1:
                buy_category = getparse(result,'Shop by Category</h2>','</ul>')
                if str(buy_category).find('<strong class="bold">') > -1:
                    buy_category = getparse(buy_category,'<strong class="bold">','')

                sp_bcate = str(buy_category).split('<li>')
                print(">> sp_bcate : {}".format(len(sp_bcate)-1))

                errcnt = 0
                low = 1
                for ea_bcate in sp_bcate:
                    cate_tmp = getparse(str(ea_bcate),'b-textlink--sibling"','</li>')
                    if cate_tmp != "":
                        cate_url = getparse(str(cate_tmp),'href="','">').replace("'","").strip()
                        cate_name = getparse(str(cate_tmp),'">','</a>')
                        cate_name = replace_str(cate_name)
                        cate_code2 = getparseR(getparse(str(cate_url),'','/bn'),'/','')
                        print("\n\n-----------------------------------------------------------------------------")
                        print(">> ({}) {}   |   {}    |    {} ".format(low, cate_code2, cate_name, cate_url))

                        sql2 = "select * from t_category where cate_code2 = '{0}'".format(cate_code2)
                        rs2 = db_con.selectone(sql2)
                        print('##select one## sql2 :' + str(sql2))

                        trans_text = ""
                        dic2 = dict()
                        dic2['name'] = "'" + cate_name + "'"
                        dic2['kor_name'] = "'" + trans_text + "'"
                        dic2['depth'] = in_dep
                        dic2['sort'] = low
                        dic2['parent'] = now_catecode
                        dic2['cate_code2'] = cate_code2

                        if str(in_dep) == "3":
                            #print('>> depth == 3')

                            dic2['bcate'] = now_bcate
                            dic2['mcate'] = now_catecode
                            dic2['big'] = "'" + now_big + "'"
                            dic2['middle'] = "'" + now_middle + "'"
                            dic2['small'] = "'" + cate_name + "'"

                        elif str(in_dep) == "4":
                            #print('>> depth == 4')

                            dic2['bcate'] = now_bcate
                            dic2['mcate'] = now_mcate
                            dic2['scate'] = now_catecode
                            dic2['big'] = "'" + now_big + "'"
                            dic2['middle'] = "'" + now_middle + "'"
                            dic2['small'] = "'" + now_small + "'"
                            dic2['little'] = "'" + cate_name + "'"

                        elif str(in_dep) == "5":
                            #print('>> depth == 5')

                            dic2['bcate'] = now_bcate
                            dic2['mcate'] = now_mcate
                            dic2['scate'] = now_scate
                            dic2['dcate'] = now_catecode
                            dic2['big'] = "'" + now_big + "'"
                            dic2['middle'] = "'" + now_middle + "'"
                            dic2['small'] = "'" + now_small + "'"
                            dic2['little'] = "'" + now_little + "'"
                            dic2['last'] = "'" + cate_name + "'"

                        elif str(in_dep) == "6":
                            #print('>> depth == 6')

                            dic2['bcate'] = now_bcate
                            dic2['mcate'] = now_mcate
                            dic2['scate'] = now_scate
                            dic2['dcate'] = now_dcate
                            dic2['ecate'] = now_catecode
                            dic2['big'] = "'" + now_big + "'"
                            dic2['middle'] = "'" + now_middle + "'"
                            dic2['small'] = "'" + now_small + "'"
                            dic2['little'] = "'" + now_little + "'"
                            dic2['last'] = "'" + now_last + "'"
                            dic2['final'] = "'" + cate_name + "'"

                        elif str(in_dep) == "7":
                            #print('>> depth == 7')

                            dic2['bcate'] = now_bcate
                            dic2['mcate'] = now_mcate
                            dic2['scate'] = now_scate
                            dic2['dcate'] = now_dcate
                            dic2['ecate'] = now_ecate
                            dic2['fcate'] = now_catecode
                            dic2['big'] = "'" + now_big + "'"
                            dic2['middle'] = "'" + now_middle + "'"
                            dic2['small'] = "'" + now_small + "'"
                            dic2['little'] = "'" + now_little + "'"
                            dic2['last'] = "'" + now_last + "'"
                            dic2['final'] = "'" + now_final + "'"
                            dic2['final1'] = "'" + cate_name + "'"


                        if not rs2:  # rs is None
                            dic2['amz_cateurl'] = "'" + cate_url + "'"
                            db_con.insert('t_category', dic2)  # insert
                            print('##insert## ({}) : t_category : {} 하위 '.format(in_dep, now_catecode))

                        else:
                            print('# : 중복 데이터 skip : {}'.format(cate_code2))
                            # last_ck = 1
                            # print('lastcate update :'+str(last_ck))
                            # sql3_where = " catecode = '" + str(now_catecode) + "'"
                            # dic3 = dict()
                            # dic3['lastcate'] = last_ck
                            # db_con.update('t_category', dic3, sql3_where)  # update
                            # print('##update## : t_category : {} '.format(now_catecode))

                    low = low + 1

                # last_ck = 0
                # print('lastcate update :'+str(last_ck))
                # sql3_where = " catecode = '" + str(now_catecode) + "'"
                # dic3 = dict()
                # dic3['lastcate'] = last_ck
                # db_con.update('t_category', dic3, sql3_where)  # update
                sql3_where = " catecode = '" + str(now_catecode) + "'"
                dic3 = dict()
                dic3['proc_chk'] = "'1'"
                db_con.update('t_category', dic3, sql3_where)  # update            
                print('##update## : t_category : {} '.format(now_catecode))

                time.sleep(1)
                sql5 = "select catecode from t_category where Parent = ( select catecode from t_category where catecode = '{}' and proc_chk = '1' )".format(now_catecode)
                rs5 = db_con.selectone(sql5)
                print('##select one## sql5 :' + str(sql5))
                if rs5:
                    last_ck = 0
                    print('No lastcate update :'+str(last_ck))
                else:
                    last_ck = 1
                    print('lastcate update :'+str(last_ck))
                sql5_where = " catecode = '" + str(now_catecode) + "'"
                dic5 = dict()
                dic5['lastcate'] = last_ck
                db_con.update('t_category', dic5, sql5_where)  # update

        low2 = low2 + 1
        print('>>n Next (low2) : ' + str(datetime.datetime.now()))

    print('>> [--- newCateDep 3~ End ---] ')
    if rtnCode == "E":
        print('>> rtnCode : {}'.format(rtnCode))
        return rtnCode

    return "0"


if __name__ == '__main__':
    print(">> start ")
    errcnt = 0
    browser = connectDriver("chrome")
    main_url = "https://www.ebay.com"
    print('>> main_url : ' + str(main_url)) 
    browser.get(main_url)
    time.sleep(3)     
    main_result = ""
    main_result = browser.page_source

    # depth 1~2
    #newCateDep1(browser)

    depth = "3"
    procFlg = "0"

    while procFlg == "0":
        rtnFlg = newCateDep3(browser, str(depth))
        print('>> errcnt : {} ' +str(errcnt))
        if rtnFlg == "F":
            sql = " select catecode from T_CATEGORY where ishidden = 'F' and depth = " + str(int(depth)-1)+ " and lastcate is null and proc_chk is null and skip_cnt = 0 "
            row = db_con.selectone(sql)
            print('>> depth : {} Check '.format(sql))
            if row:
                print('>> 처리할 카테고리 존재 ')
            else:
                print('>> depth : {} 완료 '.format(depth))
                errcnt = 0
                depth = int(depth) + 1
            if int(depth) > 7:
                procFlg = "1"
            time.sleep(5)

        if rtnFlg == "E":
            procFlg = "1"
        time.sleep(2)

    db_con.close()
    os._exit(0)
    #input(">> Key : ")

######
