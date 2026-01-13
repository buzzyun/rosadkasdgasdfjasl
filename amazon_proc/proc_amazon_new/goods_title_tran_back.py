# -*- coding: utf-8 -*-
import os
os.system('pip install --upgrade selenium')
import datetime
import os
import time
import sys
import random
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
import json
import urllib
import re
import sys
import DBmodule_FR


global ver
ver = "01.07"
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


def get_replace_title(str_title):

    tmp_title = str(str_title).strip()
    tmp_title = tmp_title.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ').replace("&lt;","<").replace("&gt;",">")
    tmp_title = tmp_title.replace("&ndash;","-").replace("&times;"," x ").replace("&rdquo;","").replace('–','-').replace('「',' ').replace('」',' ')
    tmp_title = tmp_title.replace("&quot;","").replace("\\", "").replace("★","").replace("◆","").replace('"', '').replace('  ', ' ')

    return tmp_title

# (사이트DB 체크) 사이트내 금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_site(target, cate_idx, db_con):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
    print('>> (db_con) sql :' + str(sql))
    prs = db_con.select(sql)
    for rs in prs:
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        ban_cate_idx = (rs[4]).strip()
        if ban_title_inner == None or ban_title_inner == '' : #case 1
            if ban_check == '1' :
                if target.lower().find(ban_title_gubun.lower()) == 0 :
                    result = "1"
                    print('>> [Forbidden (1) 1 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 1  : " + str(ban_title_gubun)
                    break
                elif target.lower().find(ban_title_gubun.lower()) > 0 :
                    forward_index = target.lower().find(ban_title_gubun.lower())
                    backward_index = target.lower().rfind(ban_title_gubun.lower())
                    if forward_index == backward_index :                        
                        check_str = target[forward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-1 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-1  : " + str(ban_title_gubun)                            
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-2 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-2  : " + str(ban_title_gubun)  
                                break                       
                    else:
                        check_str = target[forward_index-1]
                        backward_str = target[backward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-3 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-3  : " + str(ban_title_gubun)  
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-5 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-5  : " + str(ban_title_gubun)  
                                break
                        if backward_str == '' or backward_str ==' ' or backward_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-4 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-4  : " + str(ban_title_gubun) 
                            break
                        else:
                            backward_check_symbol = len(re.sub(parttern,'',backward_str))
                            if backward_check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-6 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-6  : " + str(ban_title_gubun)  
                                break  
            else :
                if target.lower().find(ban_title_gubun.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (1) 0 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 0 : " + str(ban_title_gubun)                    
                    break
        else:
            if ban_title_gubun_2 == None or ban_title_gubun_2 == '' : #case 2
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                    ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                    break
            else: #case 3
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 and target.lower().find(ban_title_gubun_2.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (3)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2))
                    ban_str = "Forbidden (3) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2)
                    break

    if result == "1":
        if ban_cate_idx != "":
            if str(ban_cate_idx) == str(cate_idx):
                result = result + '@' + ban_str
            else:
                result = "0"
                print(">> 금지어 제외안함 카테고리 다름 : (db){} (cateidx){}".format(ban_cate_idx, cate_idx))
        else:
            result = result + '@' + ban_str

    return result


#금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_new(target, pdb):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check from Ban_Title where ban_title = 'title' and (ban_cate_idx is null or ban_cate_idx = '')"
    prs = pdb.select(sql)
    for rs in prs :
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        
        if ban_title_inner == None or ban_title_inner == '' : #case 1
            if ban_check == '1' :
                if target.lower().find(ban_title_gubun.lower()) == 0 :
                    result = "1"
                    print('>> [Forbidden (1) 1 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 1  : " + str(ban_title_gubun)
                    break
                elif target.lower().find(ban_title_gubun.lower()) > 0 :
                    forward_index = target.lower().find(ban_title_gubun.lower())
                    backward_index = target.lower().rfind(ban_title_gubun.lower())
                    
                    if forward_index == backward_index :                        
                        check_str = target[forward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-1 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-1  : " + str(ban_title_gubun)                            
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-2 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-2  : " + str(ban_title_gubun)  
                                break                            
                    else:
                        check_str = target[forward_index-1]
                        backward_str = target[backward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-3 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-3  : " + str(ban_title_gubun)  
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-5 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-5  : " + str(ban_title_gubun)  
                                break    
                        
                        if backward_str == '' or backward_str ==' ' or backward_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-4 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-4  : " + str(ban_title_gubun) 
                            break
                        else:
                            backward_check_symbol = len(re.sub(parttern,'',backward_str))
                            if backward_check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-6 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-6  : " + str(ban_title_gubun)  
                                break  
            else :
                if target.lower().find(ban_title_gubun.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (1) 0 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 0 : " + str(ban_title_gubun)                    
                    break
        else:
            if ban_title_gubun_2 == None or ban_title_gubun_2 == '' : #case 2
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                    ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                    break
            else: #case 3
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 and target.lower().find(ban_title_gubun_2.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (3)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2))
                    ban_str = "Forbidden (3) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2)
                    break

    if result == "1":
        result = result + '@' + ban_str

    return result

# Forbidden
def checkForbidden(in_word, db_ali):

    ban_chk = "0"
    ban_str = ""
    sql = "select ban_title_gubun, ban_title_inner from Ban_Title where ban_title = 'title' and (ban_cate_idx is null or ban_cate_idx = '')"

    prs = db_ali.select(sql)
    #print('##select ## sql :' + str(sql))

    for rs in prs:
        ban_str = ""
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        if ban_title_inner == None or ban_title_inner == '':
            if in_word.lower().find(ban_title_gubun.lower()) > -1:
                ban_chk = "1"
                print('>> [Forbidden (1)] :' + str(ban_title_gubun))
                ban_str = "Forbidden (1) : " + str(ban_title_gubun)
                break
        else:
            if in_word.lower().find(ban_title_gubun.lower()) > -1 and in_word.lower().find(ban_title_inner.lower()) > -1:
                ban_chk = "1"
                print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                break

    if ban_chk == "1":
        ban_chk = ban_chk + '@' + ban_str

    return ban_chk

# replace
def replaceTitle(in_word,db_ali):
    target = str(in_word).upper()

    sql = "select replace_ban_title,replace_title from Replace_Title"
    prs = db_ali.select(sql)
    #print('##select ## sql :' + str(sql))

    for rs in prs:
        replace_ban_title = rs[0]
        replace_title = rs[1]
        if replace_ban_title != '' and replace_ban_title != None:

            if target.find(replace_ban_title.upper()) >= 0:
                target = target.replace(replace_ban_title.upper()," " + replace_title + " ")
                print('>> [replace (1)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.lower()) >= 0:
                target = target.replace(replace_ban_title.lower(), " " + replace_title + " ")
                print('>> [replace (2)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.capitalize()) >= 0 :
                target = target.replace(replace_ban_title.capitalize(), " " + replace_title + " ")
                print('>> [replace (3)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

    #print('[replace)] :' + str(target))
    return target


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

#reg 일본어 체크
def replace_regJpStrChk(in_str):
    result = ""
    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+",chkStr) #일본어(Katakana/Hiragana/Kanji)
    result = in_str.replace(regStr[0],' ')
    if len(result) == "":
        result = in_str

    return str(result).replace('  ',' ').strip()

#중국어 찾기
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

# 상품 guid 가져오기 (goodscode --> guid)
def getGuid(gCode):
    rtn_guid = ""
    tmpGuid = str(gCode)[2:]
    tmpGuid = str(tmpGuid).lstrip("0")
    rtn_guid = str(tmpGuid).replace("N", "")

    return str(rtn_guid)

###############################################

def replace_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").replace("<hr>","").strip()
    
    return result_str

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()

    return result_str


def do_proc(db_con, browser, proc_name, in_site):

    if in_site == "red":
        sql = "select top 100 goodscode, title, ali_no from t_goods where confirm_goods = '5' "
        rows= db_con.select(sql)
        print('##select ## sql :' + str(sql))
    else:
        sql = "select top 100 goodscode, Title, asin_no from goods_title_tran order by idx asc"
        rows= db_con.select(sql)
        print('##select ## sql :' + str(sql))

    if not rows:
        print('>> 대상 없음 (0) : {}'.format(in_site))
        return "1"

    print(">> 대상 : {}".format(len(rows)))
    # if len(rows) < 30:
    #     print('>> 대상 30건 이하 : ' + str(len(rows)))
    #     return "1"

    try:
        url_link = "https://dev.freeship.co.kr/_GoodsUpdate/" + str(proc_name)
        print('>> url_link : ' + str(url_link))
        browser.get(url_link)
    except Exception as e:
        print('>> 예외가 발생 (종료) : ', e)
        return "E"
    else:
        time.sleep(3)
        result2 = browser.page_source
        time.sleep(0.5)

    if str(result2).find('<div class="skiptranslate') == -1:
        print('>> 대상 없음 ' )
        return "1" 

    lowCnt = 0
    skip_cnt = 0

    tran_source = getparse(str(result2),'<div id="google_translate_element">','')
    if str(tran_source).find('<pre>') > -1:
        tran_source = getparse(str(tran_source),'<pre>','')
    if str(tran_source).find('</pre>') > -1:
        tran_source = getparse(str(tran_source),'','</pre>')
    sp_tran = tran_source.split('<input type="hidden"')
    for ea_item in sp_tran:
        # time.sleep(0.1)
        tran_title = ""
        edit_title = ""
        forbidden_flag = "1"
        #print(">> ea_item : {}".format(ea_item))
        ea_tmp = getparse(ea_item,'value="','')
        ea_goodscode = getparse(ea_tmp,'','"')
        ea_goodscode = str(ea_goodscode).replace("\u200b","").replace(",","").replace(" ","").replace("'","").strip()
        if ea_tmp.find('<div>') > -1:
            ea_tmp = str(ea_tmp).replace("<div>","").replace("</div>","").replace("'","").strip()
        tran_title = getparse(ea_tmp,'>','')
        tran_title = replace_main_str(tran_title).replace('<hr>','')
        tran_title = tran_title.replace("?"," ").replace("  "," ").strip() # ? 제거하기
        if str(ea_goodscode) == "":
            print(">> [{}] No ea_goodscode or check ea_goodscode : {}".format(lowCnt, ea_tmp))
        elif len(str(ea_goodscode)) > 14 or len(str(ea_goodscode)) < 9:
            print(">> [{}] check ea_goodscode : {}".format(lowCnt, ea_tmp))
        else:
            ea_guid = ""
            ea_guid = getGuid(ea_goodscode)
            print('>> [{}] {} ({}) | {}'.format(lowCnt, ea_goodscode, ea_guid, tran_title))
            tran_title = tran_title.replace("'","").strip()

            if str(tran_title).find('inherit;">') > -1:
                tran_title = getparse(str(tran_title),'inherit;">','')
            #print("[{}] {} | {}".format(lowCnt,ea_goodscode,ea_title))

            if regKrStrChk(tran_title) == "1": # 한글 포함 
                edit_title = replaceTitle(tran_title, db_ali)
                forbidden_flag = checkForbidden_new(edit_title, db_ali)  # title (checkForbidden_new)
                forbidden_flag_site = "0"
                if forbidden_flag == "0":
                    cate_idx = ""
                    sql_g = "select cate_idx from t_goods where uid = '{}'".format(ea_guid)
                    row_g= db_con.selectone(sql_g)
                    if row_g:
                        cate_idx = row_g[0]
                    forbidden_flag_site = checkForbidden_site(edit_title, cate_idx, db_con)

                edit_title = edit_title.replace('  ',' ').strip()
                #print("[{}] {} ({}) | {}".format(lowCnt, ea_goodscode, ea_goodscode, edit_title))

                if str(forbidden_flag) == "0" and str(forbidden_flag_site) == "0":
                    if len(edit_title) > 4:
                        if in_site == "shop" or in_site == "ref": # shop / ref 사이트의 경우 confirm_goods = '5'로 변환 ( 추후 이미지 변경후 confirm_goods = null 처리 예정 )
                            sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods = '5' where uid = '{}'".format(edit_title, edit_title, ea_guid)
                        else:
                            sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods = null where uid = '{}'".format(edit_title, edit_title, ea_guid)
                        print(">> [{}] t_goods (update) : {} ({})".format(lowCnt, ea_goodscode, ea_guid))
                        db_con.execute(sql_u)
                    else:
                        sql_u = "update t_goods set confirm_goods = null, Del_Naver='1' where uid = '{}'".format(ea_guid)
                        print(">> [{}] t_goods (update) : {} ({})".format(lowCnt, ea_goodscode, ea_guid))
                        db_con.execute(sql_u)
                        skip_cnt = skip_cnt + 1
                else:
                    print(">> 금지어 포함 : {} | {}".format(forbidden_flag, forbidden_flag_site))
                    sql_u1 = "update t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', confirm_goods = null where uid = {0}".format(ea_guid)
                    db_con.execute(sql_u1)
                    sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(ea_guid)
                    db_con.execute(sql_u2)
                    print(">> [{}] t_goods 금지어 처리 : {} ({})".format(lowCnt, ea_goodscode, ea_guid))
            else:
                if tran_title == "":
                    sql_u = "update t_goods set confirm_goods = '2' where uid = '{}'".format(ea_guid)
                    db_con.execute(sql_u)
                elif regJpStrChk(tran_title) == "1":
                    skip_cnt = skip_cnt + 1
                    sql_u = "update t_goods set confirm_goods = '2' where uid = '{}'".format(ea_guid)
                    db_con.execute(sql_u)
                    print(">> [{}] (일본어존재) confirm_goods = 2 : {}".format(lowCnt, ea_goodscode))
                elif findChinese(tran_title) == True:
                    skip_cnt = skip_cnt + 1
                    sql_u = "update t_goods set confirm_goods = '2', title_chk = '2' where uid = '{}'".format(ea_guid)
                    db_con.execute(sql_u)
                    print(">> [{}] (중국어존재) confirm_goods = 2, title_chk = 2 : {}".format(lowCnt, ea_goodscode))
                else:
                    if in_site == "shop" or in_site == "ref": # shop / ref 사이트의 경우 confirm_goods = '5'로 변환 ( 추후 이미지 변경후 confirm_goods = null 처리 예정 )
                        sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods =  '5' where uid = '{}'".format(tran_title, tran_title, ea_guid)
                    else:
                        sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods = null where uid = '{}'".format(tran_title, tran_title, ea_guid)
                    # sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods = null where uid = '{}'".format(tran_title, tran_title, ea_guid)
                    print(">> [{}] t_goods (update) : {} ({})".format(lowCnt, ea_goodscode, ea_guid))
                    db_con.execute(sql_u)

        if in_site != "red":
            sql_d = "delete from goods_title_tran where goodscode = '{}'".format(ea_goodscode)
            #print(">> [{}] goods_title_tran (del) : {} ( {} )".format(lowCnt, ea_goodscode, len(ea_goodscode)))
            db_con.execute(sql_d)
        lowCnt = lowCnt + 1

    print(">> skip_cnt : {}".format(skip_cnt))
    return "0"


def do_proc2(db_con, browser, proc_name, in_site):

    sql = "select top 50 goodscode, Title, uid from t_goods where confirm_goods = '2' order by uid asc"
    rows= db_con.select(sql)
    print('##select ## sql :' + str(sql))
    if not rows:
        print('>> 대상 없음 (skip) ')
        return "1"

    cnt = 0
    skip_cnt = 0
    for row in rows:
        db_goodscode = row[0]
        db_title = row[1]
        db_uid = row[2]
        url_link = f"https://translate.google.co.kr/?hl=ko&sl=auto&tl=en&text={db_title}&op=translate"
        print('>> [{}] url_link : {}'.format(db_goodscode, url_link))
        try:
            browser.get(url_link)
            time.sleep(3)
            result2 = browser.page_source
        except Exception as e:
            print('>> 예외가 발생 (종료) : ', e)
            return "E"
        else:
            tran_txt = getparse(str(result2),'<div class="lRu31">','<div ').split('jsname="')[-1]
            tran_txt = getparse(str(tran_txt),'">','').replace('</span>','').replace("?"," ").replace("'","`").replace("  "," ").strip()
            print(">> tran_txt : {}".format(tran_txt))
            cnt = cnt + 1

            edit_title = replaceTitle(tran_txt, db_ali).replace('  ',' ').strip()
            forbidden_flag = checkForbidden_new(edit_title, db_ali)  # title (checkForbidden_new)

            if str(forbidden_flag) == "0":
                if regJpStrChk(edit_title) == "1":
                    edit_title = replace_regJpStrChk(edit_title)
                if regJpStrChk(edit_title) == "1":
                    skip_cnt = skip_cnt + 1
                    sql_u = "update t_goods set confirm_goods = null, Del_Naver='1' where uid = '{}'".format(db_uid)
                    db_con.execute(sql_u)
                    print(">> [{}] (일본어존재) confirm_goods = 2 : {}".format(cnt, db_goodscode))
                else:
                    edit_title = edit_title.replace('  ',' ').strip()
                    if len(edit_title) > 4:
                        sql_u = "update t_goods set Title = dbo.GetCutStr('{}',240,'...'), E_title = dbo.GetCutStr('{}',240,'...'), confirm_goods = null where uid = '{}'".format(edit_title, edit_title, db_uid)
                        print(">> [{}] t_goods (update) : {} ({})".format(cnt, db_goodscode, db_uid))
                        db_con.execute(sql_u)
                    else:
                        sql_u = "update t_goods set confirm_goods = null, Del_Naver='1' where uid = '{}'".format(db_uid)
                        print(">> [{}] t_goods (update) : {} ({})".format(cnt, db_goodscode, db_uid))
                        db_con.execute(sql_u)
                        skip_cnt = skip_cnt + 1
            else:
                print(">> 금지어 포함 : {} ".format(forbidden_flag))
                sql_u1 = "update t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', confirm_goods = null where uid = {0}".format(db_uid)
                db_con.execute(sql_u1)
                sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(db_uid)
                db_con.execute(sql_u2)
                print(">> [{}] t_goods 금지어 처리 : {} ({})".format(cnt, db_goodscode, db_uid))

    return "0"


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
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)

    return browser

def connectDriverOld(pgSite, kbn, type):
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
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer':'" + str (pgSite) + "'")
    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, kbn, type):
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
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
        print(">> ChromeDriverManager install ")
    except Exception as e:
        print(e)
        # print(">> ChromeDriverManager 114.0.5735.90 install ")
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)

        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path

    return browser


def version_check(db_con, in_ver, in_pgFilename, in_pgKbn):

    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")

    sql = "select version,url from python_version_manage where name = '" +str(in_pgKbn)+ "'"
    print(">> sql:" + sql)

    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        print(">> (DB) version :" +str(version))

        if str(in_ver) != str(version):
            db_con.close()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 1000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")

                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 1000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")

            time.sleep(3)
            
            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception ')
            else:
                pass

            try:
                fname = os.path.abspath( __file__ )
                fname = getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 

                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')
            else:
                pass

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

def get_new_token_v1():
    auth_server_url = "https://bizmsg-web.kakaoenterprise.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(msg, phone):
    db_FS = DBmodule_FR.Database("freeship")
    token = get_new_token_v1()
    test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/message/send"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    template_code = "norder1"
    sender_no = "18005086"
    cid_key = "cid_key"

    if phone != "":
        print(">> ")
        ordername = "주문팀"
        orderno = "M0000"
        phone_number = str(phone).replace('-','').strip()
        message = msg
        sms_message = message
        message_type = "SM"
        sms_type = "SM"

        #---------------------------------------
        ###phone_number = "01090467616"
        #---------------------------------------
        param_date = {'client_id': 'C000000440','sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17','message_type': message_type,'message': message
        ,'cid': cid_key,'phone_number': phone_number,'template_code': template_code,'sender_no': sender_no,'sms_message':sms_message, 'sms_type':sms_type,'title': '주문관련 안내'}

        jsonString = json.dumps(param_date, indent=4)
        api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
        if api_call_response.status_code !=200:
            print(">> error ")
        else:
            result = json.loads(api_call_response.text)
            rtn_uid =  result['uid']
            rtn_status_code =  result['kko_status_code']
            rtn_code = result['code']
            rtn_message = result['message']
            print(">> rtn_status_code : {} | rtn_message : {}".format(rtn_status_code, rtn_message))
            if rtn_code == "API_200" or rtn_status_code == "0000": 
                result_code = "200"
                result_message = "OK"
            else:
                result_code = rtn_code
                result_message = rtn_message

            iSql = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent, orderno) values\
                ('{}','{}','{}','{}','{}',getdate(),'adminauto','{}','{}','{}')".format(ordername,phone_number,rtn_uid,result_code,result_message,template_code,message,orderno)
            print(">> iSql : {} ".format(iSql))
            db_FS.execute(iSql)

    db_FS.close()

if __name__ == '__main__':

    print(">> Start title_tran ")
    print(str(datetime.datetime.now()))
    input_type = str(sys.argv[1]).strip()
    input_phone = str(sys.argv[2]).strip()
    print(">> Headless TYPE: {} | error alarm phone : {}".format(input_type, input_phone))

    #browser = connectDriver('dev.freeship.co.kr')
    pgSite = 'https://dev.freeship.co.kr'
    try:
        browser = connectDriverNew(pgSite, "N", input_type)
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(pgSite, "N", input_type)
        print(">> connectDriverOld set OK ")
    browser.set_window_size(1100, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    proc_flg = "0"
    arrCnt = 0
    while proc_flg == "0":
        site_list = ['usa','mall','global','best','uk','de','handmade','ref','shop','global']
        site_file_name = ['title_tran_usa.asp','title_tran_mall.asp','title_tran_global.asp','title_tran_best.asp','title_tran_uk.asp','title_tran_de.asp','handmade_title_tran.asp','title_tran_ref.asp','title_tran_shop.asp','title_tran']
        # site_list = ['red']
        # site_file_name = ['title_tran_red.asp']

        for site, filename in zip(site_list, site_file_name):

            input_Site = site.strip()
            input_pgKbn = filename.strip()
            print(">> ------------------------------------------------------------")
            print(">> SITE : {} | File Name : {} | TYPE: {} ".format(input_Site, input_pgKbn, input_type))

            if input_Site == "" and input_pgKbn == "" and input_type == "":
                print(">> 입력 값을 확인하세요. {} | {} | {}".format(input_Site, input_pgKbn, input_type))
                print(">> Main End : " + str(datetime.datetime.now()))
                os._exit(1)

            db_ali = DBmodule_FR.Database('aliexpress')
            db_con = DBmodule_FR.Database(input_Site)
            print(">> input_pgKbn : {}".format(input_pgKbn))

            if str(currIp).strip() != "222.104.189.18":
                version_check(db_con, ver, "new_goods_title_tran.exe", "goods_title_tran")
            time.sleep(1)

            try:
                if str(input_pgKbn).find('.asp') > -1:
                    rtn_flg = do_proc(db_con, browser, input_pgKbn, input_Site)
                else:
                    rtn_flg = do_proc2(db_con, browser, input_pgKbn, input_Site)
                if rtn_flg == "E":
                    arrCnt = arrCnt + 1
                    print('>> 예외가 발생 arrCnt : {}'.format(arrCnt))
                else:
                    arrCnt = 0
            except Exception as e:
                print('>> 예외가 발생 (종료) : ', e)
                sms_send_kakao_proc_new("title_tran error check", input_phone)
                proc_flg = "1"
                time.sleep(5)
                break
            else:
                time.sleep(1)

            if arrCnt > 3:
                sms_send_kakao_proc_new("title_tran error check", input_phone)
                proc_flg = "1"

            db_con.close()
            db_ali.close()
            time.sleep(random.uniform(2,5))

        time.sleep(random.uniform(10,20))

    browser.quit()
    print(str(datetime.datetime.now()))
    print(">> End title_tran ")
    if proc_flg == "1":
        os._exit(1)
    os._exit(0)
