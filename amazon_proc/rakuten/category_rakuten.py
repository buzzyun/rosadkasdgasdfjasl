# -*- coding: utf-8 -*-
import datetime
import os
import random
import socket
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

global timecount
global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

ver = "61.25"

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

def connectDriverNew(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1300x1080")  # 화면크기
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")

    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver
    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)

    return browser


# Depth 1
def newCateDep1(db_con, browser):
    print('\n [--- newCateDep1 start ---] ')

    now_url = "https://ranking.rakuten.co.jp/"
    browser.get(now_url)
    time.sleep(4)

    result = browser.page_source
    resultTmp = str(result)
    print(">> ------------------------- ")
    menuList = getparse(str(resultTmp),'<div class="pulldownMenu">','<div class="sideContents03">')
    menuList = getparse(menuList,'<ul class=','</ul>')
    spList = resultTmp.split('id="rankingGenreBox')
    print(">> spList Count : {} ".format(len(spList)))
    low1 = 0
    print(">>\n============================================")
    for item in spList:
        menu_title = getparse(item, 'class="rigGnrCategory"', '</span>')
        if menu_title == "":
            low1 = low1 + 1
            continue
        bcate_url = getparse(menu_title, 'href="', '"')
        bcate_name = getparse(menu_title, '>', '</a>')
        if bcate_name.find("<font ") > -1:
            repStr = "<font " + getparse(bcate_name, '<font ', '>') + ">"
            bcate_name = bcate_name.replace(repStr,'').replace('</font>','')
        bcate_name = bcate_name.replace("'","").replace(","," &").replace("/"," & ").strip()
        bcate_code = getparse(bcate_url, '/daily/', '/')
        sitemap_url = getparse(item, 'class="sitemap"', '</a>')
        sitemap_url = getparse(sitemap_url, 'href="', '"')
        bcate_url = "https://ranking.rakuten.co.jp" + str(bcate_url)
        sitemap_url = "https://ranking.rakuten.co.jp" + str(sitemap_url)

        tran_bcate_name = bcate_name
        print(">>\n( 1 Depth ) [{}] itme_id : {} | {} ".format(low1, bcate_code, bcate_name))
        print(">> {}".format(bcate_url))
        if sitemap_url == "":
            print(">> sitemap_url 없음 확인필요 : {}".format(menu_title))
        print(">> {}".format(sitemap_url))

        sql = "select * from t_category where amz_cateurl = '{0}'".format(bcate_url)
        rs = db_con.selectone(sql)
        print('##select one## sql :' +str(sql))
        if not rs: # rs is None
            dic = dict()
            dic['name'] = "'" + bcate_name + "'"
            dic['kor_name'] = "'" + tran_bcate_name + "'"
            dic['depth'] = 1
            dic['sort'] = low1
            dic['big'] = "'" + tran_bcate_name + "'"
            dic['cate_code2'] = "'" + bcate_code + "'"
            dic['sitemap'] = "'" + sitemap_url + "'"
            print('New Category')
            dic['amz_cateurl'] = "'" + str(bcate_url) + "'"
            db_con.insert('t_category', dic)  # insert
            print('##insert## : t_category')
        else:
            print('Category 존재')

        low1 = low1 + 1

    print('>> [--- newCateDep 1 End ---] ')
    return "0"

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace(',','|').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp


# Depth 2~ 
def newCateDep2(db_con, browser, in_dep):
    global errcnt
    print('\n [--- newCateDep2 start ---] ')

    # sql = " select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1, cate_code2 from T_CATEGORY where catecode = '{}'".format(p_catecode)
    sql = " select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1, cate_code2, sitemap from T_CATEGORY where ishidden = 'F' and depth = " + str(int(in_dep)-1) + " and lastcate is null and proc_chk is null"
    rows = db_con.select(sql)
    print('>> len(rows) :' + str(len(rows)))
    print('##select ## sql :' +str(sql))

    if not rows:
        print('>> 2depth 처리 완료 :' + str(len(rows)))
        return "F"

    cnt = 0
    low1 = 0
    rtnCode = ""
    while low1 < len(rows):
        cnt = cnt + 1
        now_catecode = rows[low1][0]
        now_catename = rows[low1][1]
        now_catekor_name = rows[low1][2]
        now_cateurl = rows[low1][3]
        now_parent = rows[low1][4]
        now_cate_code2 = rows[low1][18]
        sitemap = rows[low1][19]

        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(now_catecode) + ' | ' + str(now_catename) + ' | ' + str(now_catekor_name) + ' | ' + str(now_cate_code2))
        print('\n ' + str(sitemap))

        time.sleep(1)
        print('time.sleep(1)')

        print('>> sitemap : ' + str(sitemap))
        browser.get(sitemap)
        time.sleep(random.uniform(5,6))
        result = ""
        result = browser.page_source
        time.sleep(3)
        cateTmp = getparse(str(result),'<div class="rnkContentsSpaceL">','<div id="rankingLinkBaseBox">')

        spDep2 = cateTmp.split('<div class="rnkSitemapHead">')
        print(">> Len(spDep2) : {}".format(len(spDep2)))

        low = 0
        while low < len(spDep2):
            print()
            last_ck = ""
            eaItem = str(spDep2[low])
            d2_cate_name = getparse(eaItem,'<a','</a>')
            d2_cate_url = "https://ranking.rakuten.co.jp" + getparse(d2_cate_name,'href="','"')
            d2_cate_code2 = getparse(d2_cate_name,'/daily/','/')
            d2_cate_name = getparse(d2_cate_name,'>','')
            if d2_cate_name == "":
                low = low + 1
                continue

            if d2_cate_name.find("<font ") > -1:
                repStr = "<font " + getparse(d2_cate_name, '<font ', '>') + ">"
                d2_cate_name = d2_cate_name.replace(repStr,'').replace('</font>','')
            d2_cate_name = d2_cate_name.replace("'","").replace(","," &").replace("/"," & ").replace("├","").replace("└","").strip()

            dic2 = dict()
            dic2['name'] = "'" + d2_cate_name + "'"
            dic2['kor_name'] = "'" + d2_cate_name + "'"
            dic2['depth'] = "'" + str(in_dep) + "'"
            dic2['sort'] = low
            dic2['parent'] = now_catecode
            dic2['bcate'] = now_catecode
            dic2['big'] = "'" + now_catename + "'"
            dic2['middle'] = "'" + d2_cate_name + "'"
            dic2['cate_code2'] = d2_cate_code2
            dic2['amz_cateurl'] = "'" + d2_cate_url + "'"

            if eaItem.find('<div style="padding-left') == -1:
                print(">> 마지막 카테고리 ")
                last_ck = 1
                dic2['lastcate'] = "'1'"
            else:
                print(">> 하위 카테고리 존재 ")
                sourceTmp = str(eaItem).replace("'","").replace("\n","").replace("\t","").replace('<font style="vertical-align: inherit;">','').replace("├","").replace("└","")
                dic2['sitemap_source'] = "'" + sourceTmp + "'"
                last_ck = 0

            sql2 = "select * from t_category where cate_code2 = '{0}'".format(d2_cate_code2)
            rs2 = db_con.selectone(sql2)
            print('##select one## sql2 :' + str(sql2))
            if not rs2:  # rs is None
                db_con.insert('t_category', dic2)  # insert
                print('##insert## (2Depth) : t_category : {} | 하위 {} cate_code2 : {} '.format(now_catecode, d2_cate_name, d2_cate_code2))
            else:
                print('# : 중복 데이터 skip : {}'.format(d2_cate_code2))
                sql2_where = " cate_code2 = '" + str(d2_cate_code2) + "'"
                db_con.update('t_category', dic2, sql2_where)  # update            
                print('##(update)## (2Depth) : t_category : {} | 하위 {} cate_code2 : {} '.format(now_catecode, d2_cate_name, d2_cate_code2))
            low = low + 1

        low1 = low1 + 1
        usql = " update t_category set proc_chk = '1' where catecode = '" +str(now_catecode)+ "'"
        print(">> (상위 완료처리) usql : {}".format(usql))
        db_con.execute(usql)

    return "0"

def newCateDep3(db_con, in_dep):
    
    # depth 3~ check 
    sql = " select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1,cate_code2, sitemap_source  from T_CATEGORY where ishidden = 'F' and depth = " + str(int(in_dep)-1)+ " and lastcate is null and proc_chk is null "
    rows_d2= db_con.select(sql)
    print('>> len(rows) :' + str(len(rows_d2)))
    print('##select ## sql :' +str(sql))

    if not rows_d2:
        print('>> depth {} 완료 :' + str(in_dep))
    else:
        for row in rows_d2:
            now_catecode = row[0]
            now_catename = row[1]
            now_catekor_name = row[2]
            now_cateurl = row[3]
            now_parent = row[4]
            now_bcate = row[5]
            now_mcate = row[6]
            now_scate = row[7]
            now_dcate = row[8]
            now_big = row[9]
            now_middle = row[10]
            now_small = row[11]
            now_little = row[12]
            now_last = row[13]
            now_cate_code2 = row[18]  
            sitemap_source = str(row[19]).replace('</font>','')  
            print(">> (상위) [{}] {} | {} ".format(now_catecode, now_catename, now_cate_code2))

            if str(in_dep) == "3":
                sitemap_source = getparse(sitemap_source,'<div style="padding-left:10px">','')
                spDep3 = sitemap_source.split('<div style="padding-left:10px">')
                print("\n\n>> depth 3 split : {}".format(len(spDep3)))
            elif str(in_dep) == "4":
                sitemap_source = getparse(sitemap_source,'<div style="padding-left:20px">','')
                spDep3 = sitemap_source.split('<div style="padding-left:20px">')
                print("\n\n>> depth 4 split : {}".format(len(spDep3)))
            elif str(in_dep) == "5":
                sitemap_source = getparse(sitemap_source,'<div style="padding-left:30px">','')
                spDep3 = sitemap_source.split('<div style="padding-left:30px">')
                print("\n\n>> depth 5 split : {}".format(len(spDep3)))
            elif str(in_dep) == "6":
                sitemap_source = getparse(sitemap_source,'<div style="padding-left:40px">','')
                spDep3 = sitemap_source.split('<div style="padding-left:40px">')
                print("\n\n>> depth 6 split : {}".format(len(spDep3)))
            else:
                print("\n\n>>spDep3 :  depth 7 check ")

            low = 0
            while low < len(spDep3):
                eaItem = str(spDep3[low])
                # d3_cate_name = getparse(eaItem,'<a','</a>')
                d3_cate_name = getparse(eaItem,'','</a>')
                d3_cate_url = "https://ranking.rakuten.co.jp" + getparse(d3_cate_name,'href="','"')
                d3_cate_code2 = getparse(d3_cate_name,'/daily/','/')
                
                if d3_cate_name.find("<a href=") > -1:
                    repStr = "<a href=" + getparse(d3_cate_name, '<a href=', '>') + ">"
                    d3_cate_name = d3_cate_name.replace(repStr,'').replace('</font>','')
                d3_cate_name = d3_cate_name.replace("'","").replace(","," &").replace("/"," & ").replace("├","").replace("└","").replace("_","").strip()

                dic3 = dict()
                dic3['name'] = "'" + d3_cate_name + "'"
                dic3['kor_name'] = "'" + d3_cate_name + "'"
                dic3['depth'] = "'" + str(in_dep) + "'"
                dic3['sort'] = low
                dic3['parent'] = now_catecode
                dic3['cate_code2'] = d3_cate_code2
                dic3['amz_cateurl'] = "'" + d3_cate_url + "'"

                if str(in_dep) == "3":
                    #print('>> depth == 3')

                    dic3['bcate'] = now_bcate
                    dic3['mcate'] = now_catecode
                    dic3['big'] = "'" + now_big + "'"
                    dic3['middle'] = "'" + now_middle + "'"
                    dic3['small'] = "'" + d3_cate_name + "'"
                    print(">> 3depth : {} >> {} >> {}".format(now_big, now_middle, d3_cate_name))
                elif str(in_dep) == "4":
                    #print('>> depth == 4')

                    dic3['bcate'] = now_bcate
                    dic3['mcate'] = now_mcate
                    dic3['scate'] = now_catecode
                    dic3['big'] = "'" + now_big + "'"
                    dic3['middle'] = "'" + now_middle + "'"
                    dic3['small'] = "'" + now_small + "'"
                    dic3['little'] = "'" + d3_cate_name + "'"
                    print(">> 4depth : {} >> {} >> {} >> {}".format(now_big, now_middle, now_small, d3_cate_name))

                elif str(in_dep) == "5":
                    #print('>> depth == 5')

                    dic3['bcate'] = now_bcate
                    dic3['mcate'] = now_mcate
                    dic3['scate'] = now_scate
                    dic3['dcate'] = now_catecode
                    dic3['big'] = "'" + now_big + "'"
                    dic3['middle'] = "'" + now_middle + "'"
                    dic3['small'] = "'" + now_small + "'"
                    dic3['little'] = "'" + now_little + "'"
                    dic3['last'] = "'" + d3_cate_name + "'"
                    print(">> 5depth : {} >> {} >> {} >> {} >> {}".format(now_big, now_middle, now_small, now_little, d3_cate_name))

                elif str(in_dep) == "6":
                    #print('>> depth == 6')

                    dic3['bcate'] = now_bcate
                    dic3['mcate'] = now_mcate
                    dic3['scate'] = now_scate
                    dic3['dcate'] = now_dcate
                    dic3['ecate'] = now_catecode
                    dic3['big'] = "'" + now_big + "'"
                    dic3['middle'] = "'" + now_middle + "'"
                    dic3['small'] = "'" + now_small + "'"
                    dic3['little'] = "'" + now_little + "'"
                    dic3['last'] = "'" + now_last + "'"
                    dic3['final'] = "'" + d3_cate_name + "'"
                    print(">> 6depth : {} >> {} >> {} >> {} >> {} >> {}".format(now_big, now_middle, now_small, now_little, now_last, d3_cate_name))
                else:
                    print(">> depth 7 check ")

                nextItem = spDep3[low]
                if nextItem.find('<div style="padding-left:') == -1:
                    print(">> 마지막 카테고리 ")
                    last_ck = 1
                    dic3['lastcate'] = "'1'"
                else:
                    print(">> 하위 카테고리 존재 ")
                    dic3['sitemap_source'] = "'" + eaItem + "'"
                    last_ck = 0

                sql3 = "select * from t_category where cate_code2 = '{0}'".format(d3_cate_code2)
                rs3 = db_con.selectone(sql3)
                # print('##select one## sql3 :' + str(sql3))

                if not rs3:  # rs is None
                    db_con.insert('t_category', dic3)  # insert
                    print('##insert## ("{}"Depth) : (상위) {} | 하위 {}  : {} '.format(in_dep, now_catecode, d3_cate_name, d3_cate_code2))
                else:
                    print('# : 중복 데이터 skip : {}'.format(d3_cate_code2))
                    sql3_where = " cate_code2 = '" + str(d3_cate_code2) + "'"
                    db_con.update('t_category', dic3, sql3_where)  # update            
                    print('##(update)## ("{}"Depth) : (상위) {} | 하위 {}  : {} '.format(in_dep, now_catecode, d3_cate_name, d3_cate_code2))

                low = low + 1

            usql = " update t_category set proc_chk = '1' where catecode = '" +str(now_catecode)+ "'"
            print(">> (상위 완료처리) usql : {}".format(usql))
            db_con.execute(usql)

    return "0"

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    timecount = 0

    now_url = "https://ranking.rakuten.co.jp/"
    # browser = connectDriverNew(now_url, "")
    # time.sleep(2)
    # browser.get(now_url)
    # time.sleep(4)

    db_con = DBmodule_FR.Database('shop') #rakuten

    # 1depth
    # newCateDep1(db_con, browser)

    # 2depth
    # newCateDep2(db_con, browser, 2)

    # browser.quit()

    # 3depth ( browser 끄고, 2depth의 저장된 소스로 파싱하기 )
    # newCateDep3(db_con, 3)

    # 4depth 
    newCateDep3(db_con, 4)

    # 5depth 
    newCateDep3(db_con, 5)

    # 6depth 
    newCateDep3(db_con,6)

    input(">> ")






