import socket
import socks
import http.client
from stem import Signal
from stem.control import Controller
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import time
import socket
import os,re
import func_user
import parsing_source_1
import parsing_source_2
import DBmodule_FR

global errcnt 

db_con = DBmodule_FR.Database('red')

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
def newCateDep1(in_dep):
	print('\n [--- newCateDep1 start ---] ')

	low1 = 0
	sp_main_cate = parsing_source_1.main_cate.split('data-web-log-event=')
	for ea_cate in sp_main_cate:
		bcate_url = func_user.getparse(ea_cate,'href="','"')
		if bcate_url.find('https://') == -1: bcate_url = "https://www.coupang.com" + str(bcate_url)
		bcate_name = func_user.getparse(ea_cate,'alt="','"')
		if bcate_name != "":
			print("\n\n------------------------------------------------------------------------------------------------------------")
			print(">> ( 1 Depth ) ({}) [{}] | {} | {} ".format(low1, bcate_name, bcate_name, bcate_url))
			print("\n\n------------------------------------------------------------------------------------------------------------")

			dic = dict()
			dic['name'] = "'" + bcate_name + "'"
			dic['kor_name'] = "'" + bcate_name + "'"
			dic['depth'] = 1
			dic['sort'] = low1
			dic['big'] = "'" + bcate_name + "'"

			sql = "select * from t_category_coupang where amz_cateurl = '{0}'".format(bcate_url)
			rs = db_con.selectone(sql)
			print('##select one## sql :' +str(sql))
			if not rs: # rs is None
				print('New Category')
				dic['amz_cateurl'] = "'" + str(bcate_url) + "'"
				db_con.insert('t_category_coupang', dic)  # insert
				print('##insert## : t_category_coupang')
			else:
				print('Category 존재')
				sql_where = " amz_cateurl = '" + str(bcate_url) + "'"
				db_con.update('t_category_coupang', dic, sql_where)  # update
				print('##update## : t_category_coupang')

			low1 = low1 + 1

	print('>> [--- newCateDep 1 End ---] ')
	return "0"


def newCateDep2(in_dep):
    print('\n [--- newCateDep2 start ---] ')

    last_ck = 0
    path_file = os.getcwd()
    sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,final from t_category_coupang where depth = '" +str(in_dep-1)+ "' and ishidden='F' and lastcate is null "
    print('\n [depth : {}] sql: {}'.format(in_dep, sql))

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

        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(bcate_catecode) + ' | ' + str(bcate_catename) + ' | ' + str(bcate_catekor_name) )
        print('\n ' + str(bcate_cateurl))

        result_site = getparse(parsing_source_2.cate_source, bcate_cateurl,'<h2>')
        low_2 = 0
        mscate_cnt = 0

        mcate_source = getparse(result_site,'<li class="search-option-item','')
        sp_mcate = mcate_source.split('<li class="search-option-item ')
        print(">> sp_mcate : {}".format(len(sp_mcate)))
        for ea_mcate in sp_mcate:
            mcate_tmp = getparse(str(ea_mcate),'<input type="radio"','</li>')
            mcate_name = getparse(str(mcate_tmp),'href="','</a>')
            mcate_name = getparse(str(mcate_name),'">','').strip()
            mcate_url = getparse(str(mcate_tmp),'href="','"')
            mcate_value = getparse(str(mcate_tmp),'value="','"')
            if mcate_url.find('https://') == -1: mcate_url = "https://www.coupang.com" + str(mcate_url)
            if mcate_name != "":
                if mcate_tmp.find('class="btn-fold"') > -1:
                    mcate_lastcate = '0'
                else:
                    mcate_lastcate = '1'
                    print(">> 마지막 카테고리 ")
                tran_mcate_name = ""
                tran_mcate_name = mcate_name
                if str(tran_mcate_name).strip() == "": tran_mcate_name = mcate_name
                tran_mcate_name = replace_str(tran_mcate_name).replace("/","&")
                low_2 = low_2 + 1

                print(">> ===================================================================================================== ")
                print(">> ( {} Depth ) ({}) [{}] | {} | (lastcate:{}) [{}] {} ".format(in_dep, low_2, mcate_name, tran_mcate_name, mcate_lastcate, mcate_value, mcate_url))
                print(">> ===================================================================================================== ")

                dic2 = dict()
                dic2['name'] = "'" + mcate_name + "'"
                dic2['kor_name'] = "'" + tran_mcate_name + "'"
                dic2['depth'] = in_dep
                dic2['sort'] = low_2
                dic2['cate_code2'] = mcate_value
                dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                dic2['parent'] = bcate_catecode
                dic2['bcate'] = bcate_catecode
                dic2['big'] = "'" + bcate_big + "'"
                dic2['middle'] = "'" + mcate_name + "'"

                sql2 = "select * from t_category_coupang where amz_cateurl = '{0}'".format(mcate_url)
                rs2 = db_con.selectone(sql2)
                #print('##select one## sql2 :' + str(sql2))
                if not rs2: # rs2 is None
                    print('New 2 Category : {}'.format(mcate_url))
                    dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                    print('##insert## : t_category_coupang : {}'.format(dic2))
                    db_con.insert('t_category_coupang', dic2)  # insert
                else:
                    print('Category 2 존재 : {}'.format(mcate_url))
                mscate_cnt = mscate_cnt + 1

        low = low + 1
        if mscate_cnt > 0:
            sql_um = " update t_category_coupang set lastcate = '0' where catecode = '{}'".format(bcate_catecode)
            print('>> lastcate = 0 처리 : {}'.format(bcate_catecode))
            db_con.execute(sql_um)
        else:
            sql_um = " update t_category_coupang set lastcate = '1' where catecode = '{}'".format(bcate_catecode)
            print('>> lastcate = 0 처리 : {}'.format(bcate_catecode))
            db_con.execute(sql_um)
        print('>> TIME : ' + str(datetime.datetime.now()))

    print('>> [--- newCateDep2 end ---] ')
    return "0"


def newCateDep3(in_drive, in_dep):
    print('\n [--- newCateDep'+str(in_dep)+' start ---] ')
    last_ck = 0
    path_file = os.getcwd()
    sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,final from t_category_coupang where depth = '" +str(in_dep-1)+ "' and ishidden='F' and lastcate is null "
    print('\n [depth : {}] sql: {}'.format(in_dep, sql))

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
        bcate_final = rows[low][14]

        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(bcate_catecode) + ' | ' + str(bcate_catename) )
        print('\n ' + str(bcate_cateurl))

        in_drive.get(bcate_cateurl)
        time.sleep(random.uniform(5,6))   
        result_site = ""
        result_site = in_drive.page_source
        time.sleep(3)
        if low == 0:
            with open(path_file + "/log/coupang_" +str(bcate_catecode)+ "_catecode.html","w",encoding="utf8") as f: 
                f.write(str(result_site))
        skip_flg = "0"
        low_2 = 0
        mscate_cnt = 0
        if result_site.find('id="searchCategoryComponent"') > -1:
            mcate_source = getparse(result_site,'id="searchCategoryComponent"','')
            mcate_source = getparse(mcate_source,bcate_cateurl,'')
            mcate_source_org = mcate_source
            low_2 = 0
            mscate_cnt = 0
            if mcate_source.find('class="search-option-items-child"></ul>') > -1:
                mcate_source = mcate_source.replace('class="search-option-items-child"></ul>','')
            if mcate_source.find('class="search-option-items-child">') > -1:
                mcate_source = getparse(mcate_source,'class="search-option-items-child">','</ul>')
            else:
                print(">> Check Plaeas : ")
                skip_flg = "1"
                ## input(">> Input : ")

            if skip_flg == "0":
                mcate_source = getparse(mcate_source,'<li class="search-option-item','')
                sp_mcate = mcate_source.split('<li class="search-option-item ')
                print(">> sp_mcate : {}".format(len(sp_mcate)))

                for ea_mcate in sp_mcate:
                    mcate_tmp = getparse(str(ea_mcate),'<input type="radio"','</li>')
                    mcate_name = getparse(str(mcate_tmp),'href="','</a>')
                    mcate_name = getparse(str(mcate_name),'">','').strip()
                    mcate_url = getparse(str(mcate_tmp),'href="','"')
                    mcate_value = getparse(str(mcate_tmp),'value="','"')
                    if mcate_url.find('https://') == -1: mcate_url = "https://www.coupang.com" + str(mcate_url)
                    if mcate_name != "":
                        tran_mcate_name = ""
                        tran_mcate_name = mcate_name
                        if str(tran_mcate_name).strip() == "": tran_mcate_name = mcate_name
                        tran_mcate_name = replace_str(tran_mcate_name).replace("/","&")
                        low_2 = low_2 + 1

                        print(">> ===================================================================================================== ")
                        if mcate_tmp.find('class="btn-fold"') > -1:
                            mcate_lastcate = '0'
                            print(">> ( {} Depth ) ({}) [{}] | {} | (lastcate:{}) [{}] {} ".format(in_dep, low_2, mcate_name, tran_mcate_name, mcate_lastcate, mcate_value, mcate_url))
                        else:
                            mcate_lastcate = '1'
                            print(">> [마지막 카테고리] ( {} Depth ) ({}) [{}] | {} | (lastcate:{}) [{}] {} ".format(in_dep, low_2, mcate_name, tran_mcate_name, mcate_lastcate, mcate_value, mcate_url))
                        print(">> ===================================================================================================== ")

                        dic2 = dict()
                        dic2['name'] = "'" + mcate_name + "'"
                        dic2['kor_name'] = "'" + tran_mcate_name + "'"
                        dic2['depth'] = in_dep
                        dic2['sort'] = low_2
                        dic2['cate_code2'] = mcate_value
                        dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                        dic2['parent'] = bcate_catecode

                        if str(in_dep) == "3":
                            dic2['bcate'] = bcate_bcate
                            dic2['mcate'] = bcate_catecode
                            dic2['big'] = "'" + bcate_big + "'"
                            dic2['middle'] = "'" + bcate_middle + "'"
                            dic2['small'] = "'" + mcate_name + "'"

                        elif str(in_dep) == "4":
                            dic2['bcate'] = bcate_bcate
                            dic2['mcate'] = bcate_mcate
                            dic2['scate'] = bcate_catecode
                            dic2['big'] = "'" + bcate_big + "'"
                            dic2['middle'] = "'" + bcate_middle + "'"
                            dic2['small'] = "'" + bcate_small + "'"
                            dic2['little'] = "'" + mcate_name + "'"

                        elif str(in_dep) == "5":
                            dic2['bcate'] = bcate_bcate
                            dic2['mcate'] = bcate_mcate
                            dic2['scate'] = bcate_scate
                            dic2['dcate'] = bcate_catecode
                            dic2['big'] = "'" + bcate_big + "'"
                            dic2['middle'] = "'" + bcate_middle + "'"
                            dic2['small'] = "'" + bcate_small + "'"
                            dic2['little'] = "'" + bcate_little + "'"
                            dic2['last'] = "'" + mcate_name + "'"

                        elif str(in_dep) == "6":
                            dic2['bcate'] = bcate_bcate
                            dic2['mcate'] = bcate_mcate
                            dic2['scate'] = bcate_scate
                            dic2['dcate'] = bcate_dcate
                            dic2['ecate'] = bcate_catecode
                            dic2['big'] = "'" + bcate_big + "'"
                            dic2['middle'] = "'" + bcate_middle + "'"
                            dic2['small'] = "'" + bcate_small + "'"
                            dic2['little'] = "'" + bcate_little + "'"
                            dic2['last'] = "'" + bcate_last + "'"
                            dic2['final'] = "'" + mcate_name + "'"

                        sql2 = "select * from t_category_coupang where amz_cateurl = '{0}'".format(mcate_url)
                        rs2 = db_con.selectone(sql2)
                        #print('##select one## sql2 :' + str(sql2))
                        if not rs2: # rs2 is None
                            print('New 2 Category : {}'.format(mcate_url))
                            dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                            print('##insert## : t_category_coupang : {}'.format(dic2))
                            db_con.insert('t_category_coupang', dic2)  # insert
                        else:
                            print('Category 2 존재 : {}'.format(mcate_url))
                        mscate_cnt = mscate_cnt + 1

        low = low + 1
        if mscate_cnt > 0:
            sql_um = " update t_category_coupang set lastcate = '0' where catecode = '{}'".format(bcate_catecode)
            print('>> lastcate = 0 처리 : {}'.format(bcate_catecode))
            db_con.execute(sql_um)
        else:
            sql_um = " update t_category_coupang set lastcate = '1' where catecode = '{}'".format(bcate_catecode)
            print('>> lastcate = 0 처리 : {}'.format(bcate_catecode))
            db_con.execute(sql_um)
        print('>> TIME : ' + str(datetime.datetime.now()))

    print('>> [--- newCateDep3 end ---] ')
    return "0"

if __name__ == '__main__':
    print(">> start ")
    errcnt = 0

    cate_main_url = "https://www.coupang.com/np/campaigns/83"
    try:
        proc_id, browser = func_user.connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    browser.get(cate_main_url)
    browser.set_window_size(1400, 1000)
    browser.implicitly_wait(3)

    depth = 1
    while depth < 7:
        print(">> Main Proc depth : {}".format(depth))
        if depth == 1:
            print(">> depth1")
            # depth 1 
            newCateDep1(1)
        elif depth == 2:
            print(">> depth2")
            # depth 1 
            newCateDep2(2)
        else:
            # depth 3~
            newCateDep3(browser, depth)
        depth = depth + 1

    time.sleep(10)
    db_con.close()
    browser.quit()
    os._exit(0)

