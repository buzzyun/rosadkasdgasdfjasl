import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
import subprocess
import os, sys
import datetime
import socket
import func_user
import DBmodule_FR
import func

global ver
ver = "241030"
print(">> var : {}".format(ver))

# 네이버 쇼핑 삭제상품 (중복상품 제외 나머지 상품 삭제)
print(">> 네이버 쇼핑 삭제상품 (중복상품 제외 나머지 상품 삭제) ")

db_FS = DBmodule_FR.Database('freeship')

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)


def goods_del_proc(table, reason, flg):
    print(">> goods_del_proc : {} | {} ".format(table, reason))

    site_list = ["fashion","auto","baby","electron","furniture","industry","jewelry","office","sports","beauty","fashion2","auto2","baby2","electron2","furniture2","industry2","jewelry2","office2","sports2","beauty2","mini","usa","mall","global","best","uk","de","cn","handmade","ref","trend","shop","red"]
    for site in site_list:
        sql = "select idx, guid, goodscode from {} where sitecate='{}'".format(table, site)
        rows = db_FS.select(sql)
        if rows:
            print("\n==========================================")
            print(">> Site DB Open: {}".format(site))
            print("==========================================")
            db_con = DBmodule_FR.Database(site)
            print(">> Site : {} | Del Goods Count : {}".format(site, len(rows)))
            for row in rows:
                idx, guid, goodscode = row
                # TODO : 네이버 상품 삭제 로직
                sqlg = "select isnull(naver_in,0), isnull(coupang_in,0), isnull(Del_Naver,0) from t_goods where uid='{}'".format(guid)
                rowg = db_con.selectone(sqlg)
                if not rowg:
                    print('>> (Skip) [{}] (idx) {} (guid) {} (goodscode) {} '.format(reason, idx, guid, goodscode))
                else:
                    naver_in, coupang_in, Del_Naver = rowg
                    print('>> [{}] (idx) {} (guid) {} (goodscode) {} (naver_in) {} (coupang_in) {} (Del_Naver) {}'.format(reason, idx, guid, goodscode, naver_in, coupang_in, Del_Naver))
                    if str(naver_in) == "1":
                        print(">> Naver In 상품 : {}".format(goodscode))
                        sql_n = "select goodscode from naver_del where goodscode = '{}'".format(goodscode)
                        row_n = db_FS.selectone(sql_n)
                        if not row_n:
                            sql_in = "insert into naver_del (goodscode) values('{}')".format(goodscode)
                            print(">> naver_del Insert : {}".format(goodscode))
                            #print(">> sql_in : {}".format(sql_in))
                            db_FS.execute(sql_in)

                    if str(coupang_in) == "1":
                        print(">> Coupang In 상품 : {}".format(goodscode))
                        sql_c = "select goodscode from coupang_del_goods where goodscode = '{}'".format(goodscode)
                        row_c = db_FS.selectone(sql_c)
                        if not row_c:
                            sql_ic = "insert into coupang_del_goods (goodscode) values('{}')".format(goodscode)
                            print(">> coupang_del_goods Insert : {}".format(goodscode))
                            #print(">> sql_ic : {}".format(sql_ic))
                            db_FS.execute(sql_ic)

                    if flg == "Y":
                        sqlu = "update t_goods set isdisplay='F',IsSoldOut='T',Stock='0', del_naver='1', stop_update = '1' where uid = '{}' ".format(guid)
                        print(">> t_goods Update (품절 처리) ")
                        db_con.execute(sqlu)
                    else:
                        sqlu = "update t_goods set del_naver = '1' where uid = '{}' ".format(guid)
                        print(">> t_goods Update (del_naver:1 처리) ")
                        db_con.execute(sqlu)

                sqld = "delete from {} where idx = '{}'".format(table, idx)
                print(">> delete {} | idx : {} (guid:{}) ".format(table, idx, guid))
                #print(">> sqld : {}".format(sqld))
                db_FS.execute(sqld)

            db_con.close()
            print("==========================================")

    return "0"


def procKill(currIp):
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskkill : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        time.sleep(2)


if __name__ == '__main__':
    now = datetime.datetime.now()
    currIp = socket.gethostbyname(socket.gethostname())
    procKill(currIp)

    print('>> 작업 시작 (네이버 쇼핑 삭제상품)(선택) :' + str(now))
    print('>> (Menu 1:중복(제외)상품, 2:중복상품, 3:전체상품)')
    sel_menu = str(sys.argv[1]).lower().strip()
    if sel_menu == "": sel_menu = "3"
    print(">> sel_menu : {}".format(sel_menu))

    sel_msg = ""
    ## sel_menu = input(">> (Menu 1:중복(제외)상품, 2:중복상품, 3:전체상품) 선택번호 입력:")
    if sel_menu == "1":
        sel_msg = "(1:중복(제외)상품)"
        print('>> 1:중복(제외)상품')
    elif sel_menu == "2":
        sel_msg = "2:중복상품"
        print('>> 2:중복상품')
    else:
        sel_msg = "3:전체상품"
        sel_menu = "3"
        print('>> 3:전체상품')

    now_url = 'https://center.shopping.naver.com/login'
    # try:
    #     mainDriver = func_user.connectDriverNew(now_url, "")
    # except Exception as e:
    #     print(">> connectDriverOld set ")
    #     mainDriver = func_user.connectDriverOld(now_url, "")
    #     print(">> connectDriverOld set OK ")
    proc_id = ""
    try:
        proc_id, mainDriver = func_user.connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    mainDriver.get(now_url)
    mainDriver.set_window_size(1400, 1000)
    mainDriver.implicitly_wait(3)

    time.sleep(2)
    print('time.sleep(2)')

    # 네이버 로그인 처리
    if str(mainDriver.current_url).find('shopping.naver.com/main') > -1:
        print(">> 로그인 되어있음 ")
    else:
        try:
            func_user.naver_login_in(mainDriver)
        except Exception as e:
            print(">> Login Exception ")
            input(">> 로그인 처리후 아무숫자나 입력해 주세요: ")

    time.sleep(1)
    print('time.sleep(1)')

    # 상품관리 버튼 클릭
    aGoodsbtn = mainDriver.find_element(By.LINK_TEXT,'상품관리')
    aGoodsbtn.click()
    print('>> 상품관리 버튼 클릭 Ok')

    time.sleep(3)
    print('time.sleep(3)')

    # 상품현황 및 관리 버튼 클릭
    aGoods2btn = mainDriver.find_element(By.LINK_TEXT,'상품현황 및 관리')
    aGoods2btn.click()
    print('>> 상품현황 및 관리 버튼 클릭 Ok')

    time.sleep(4)
    print('time.sleep(4)')

    # 삭제 상품 버튼 클릭
    # aGoods3btn = mainDriver.find_element(By.LINK_TEXT,'삭제 상품')
    # aGoods3btn.click()
    # print('>> 삭제 상품 버튼 클릭 Ok')
    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/deleted/list.nhn')
    print('>> 삭제 상품 page Ok')

    time.sleep(4)
    print('time.sleep(4)')
    time.sleep(4)
    print('time.sleep(4)')

    pMainSoup = mainDriver.page_source
    procDic = dict()
    procList = []
    procCnt = 0
    titCnt = 0
    tmpReasonLog = ""
    if str(pMainSoup).find('delResnList') > -1:
        naver_del_cnt = ""
        naver_del_cnt = func.getparse(str(pMainSoup), 'prdt_status_lst', 'delResnList')
        naver_del_cnt = func.getparse(str(naver_del_cnt), '<span>', '</span>')
        naver_del_cnt = naver_del_cnt.replace(",","").strip()
        print(" Naver 삭제 상품수 : {} ".format(naver_del_cnt))
        procLogSet("naver_shopping_del", "S", "0", " 네이버 쇼핑 삭제상품 삭제 (new) "+str(sel_msg)+" : " + str(naver_del_cnt))

        mainSoup = func.getparse(str(pMainSoup), 'delResnList', 'previousCursorState')
        spMainSoup = mainSoup.split('class="tit_cate"')

        for ea_mainitem in spMainSoup:
            ea_reason = func.getparse(str(ea_mainitem), '<strong>', '</strong>').strip()
            ea_delcnt = func.getparse(str(ea_mainitem), '<span>', '</span>').strip()

            if ea_delcnt == "":
                print('>>[{}] (SKIP) : {} '.format(titCnt, ea_reason))
            else:
                if sel_menu == "1": # 중복제외
                    if ea_reason == "중복상품":
                        print('>> (SKIP) {} '.format(ea_reason))
                    else:
                        print('>>[{}] {} | (상제상품수) : {} '.format(titCnt, ea_reason, ea_delcnt))
                        procList.append([])
                        procList[procCnt].append(titCnt)
                        procList[procCnt].append(ea_reason)
                        procList[procCnt].append(ea_delcnt)
                        procCnt = procCnt + 1
                elif sel_menu == "2": # 중복상품
                    if ea_reason == "중복상품":
                        print('>>[{}] {} | (상제상품수) : {} '.format(titCnt, ea_reason, ea_delcnt))
                        procList.append([])
                        procList[procCnt].append(titCnt)
                        procList[procCnt].append(ea_reason)
                        procList[procCnt].append(ea_delcnt)
                        procCnt = procCnt + 1
                else: # 전체
                    print('>>[{}] {} | (상제상품수) : {} '.format(titCnt, ea_reason, ea_delcnt))
                    procList.append([])
                    procList[procCnt].append(titCnt)
                    procList[procCnt].append(ea_reason)
                    procList[procCnt].append(ea_delcnt)
                    procCnt = procCnt + 1

                tmpReasonLog = tmpReasonLog + " [ " + str(ea_reason) + ":" + str(ea_delcnt) +" ] "

            procDic[titCnt] = ea_reason
            titCnt = titCnt + 1

        print(">> procCnt : {}".format(procCnt))
        print(">> tmpReasonLog : {}".format(tmpReasonLog))

        for pItem in procList:
            print("pItem : {}".format(pItem))
            del_cnt = str(pItem[2]).replace(",","").strip()
            #abtn = mainDriver.find_elements(By.CSS_SELECTOR,'tit_cate')[pItem[0]]
            abtn = mainDriver.find_element(By.CSS_SELECTOR,'#delResnList > li:nth-child('+str(pItem[0])+') > div > h5')
            abtn.click()
            print('>>{} Click'.format(pItem[1]))

            time.sleep(random.uniform(1.5, 2.5))
            print('time.sleep(2)')

            if int(del_cnt) > 10:

                # 리스팅 개수 클릭
                mainDriver.find_elements(By.CLASS_NAME,'tab_toggle')[1].click()
                time.sleep(2)
                print('time.sleep(2)')

                # 리스팅 100개
                aGoods5btn = mainDriver.find_element(By.LINK_TEXT,'100개')
                aGoods5btn.click()
                print('>> 리스팅 개수 100개')

                time.sleep(2)
                print('time.sleep(2)')

            pSoup = mainDriver.page_source
            pageAll = func.getparse(str(pSoup), 'func_rgt func_paginate', '</div>')
            pageAll = func.getparse(str(pageAll), '<fmt:formatnumber>', '</fmt:formatnumber>')
            print("총 {} 페이지 ".format(pageAll))
            if pageAll == "":
                pageAll = input(">> No pageAll - input Page : ")

            prow = 0
            for prow in range(1, int(pageAll)+1): 
                print(" page {} / {}".format(prow,pageAll))

                try:
                    pSoup = mainDriver.page_source
                except:
                    input(">> 페이지 새로고침 바람 wait : ")
                    time.sleep(1)
                    pSoup = mainDriver.page_source

                if str(pSoup).find('id="productTable"') == -1:
                    print(" No Data. End ")
                    break
                else:
                    soup = func.getparse(str(mainDriver.page_source), 'id="productTable"', '</table>')
                    spTrSoup = str(soup).split('<tr')

                    rowCnt = 0
                    for trRow in spTrSoup:
                        del_reason = ""
                        spTdSoup = str(trRow).split('<td')
                        naver_no = func.getparse(trRow, 'id="', '"')
                        goodscodeN = func.getparse(trRow, "openProductDetailPopup('", "')")
                        if str(naver_no) != "":
                            del_reason = spTdSoup[7]
                            del_reason = func.getparse(str(del_reason), ">", "</td>")

                        if naver_no != "" and goodscodeN != "" and del_reason != "":
                            goodscode = goodscodeN
                            if goodscode[-1:] == "N":  # goodscode 마지막 문자가 N일 경우 N제거
                                goodscode = goodscode[:-1]
                            sitecate = func.getSiteName(goodscode)
                            guid = func.getGuid(goodscode)

                            sql = " select goodscode from del_goods_naver where goodscode = '{}'".format(goodscode)
                            row = db_FS.selectone(sql)
                            if not row:
                                isql = "insert into del_goods_naver (guid,sitecate,goodscode,naver_no,reason,goodscodeN) values('{}','{}','{}','{}','{}','{}')".format(guid, sitecate, goodscode, naver_no, del_reason, goodscodeN)
                                db_FS.execute(isql)

                                print(' {} page [{}] {} | {} ( {} ) | {} | {} | (Insert Ok)'.format(prow, rowCnt, naver_no, goodscode,  guid, sitecate, del_reason))
                            else:
                                print(' {} page [{}] {} | {} ( {} ) | {} | {} | (del_goods_naver 존재 Skip)'.format(prow, rowCnt, naver_no, goodscode,  guid, sitecate, del_reason))

                        rowCnt = rowCnt + 1

                    if int(prow) < int(pageAll):
                        time.sleep(1)
                        print('time.sleep(1)')
                        try:
                            nextBtn = mainDriver.find_element(By.CSS_SELECTOR,'[data-direction=NEXT]')
                            if nextBtn:
                                nextBtn.click()
                                print("다음 ›")
                        except Exception as e:
                            waitError = input(">> 해결 :")
                            print(waitError)
                            nextBtn = mainDriver.find_element(By.CSS_SELECTOR,'[data-direction=NEXT]')
                            nextBtn.click()

                    time.sleep(1)
                    print('time.sleep(1)')

    sql = " select count(*) as gCnt from del_goods_naver"
    rowC = db_FS.selectone(sql)
    if rowC:
        gCnt = 0
        gCnt = rowC[0]
        if int(gCnt) == int(naver_del_cnt):
            print(">> 네이버 삭제상품수 : {} | del_goods_naver Inert 상품수 : {} (확인 완료) ".format(naver_del_cnt, gCnt))
        else:
            print(">> 네이버 삭제상품수 : {} | del_goods_naver Inert 상품수 : {} (확인 필요) ".format(naver_del_cnt, gCnt))

    print(">> 사이트별 삭제 Count Log Insert : {}".format(sel_msg))
    log_tmp = ""
    sql_l = "select sitecate, count(*) from del_goods_naver group by sitecate "
    rowL = db_FS.select(sql_l)
    if rowL:
        for rowlog in rowL:
            log_sitecate = rowlog[0]
            log_delcnt = rowlog[1]
            if log_tmp == "":
                log_tmp = log_tmp + str(log_sitecate) + "(" + str(log_delcnt) + ")"
            else:
                log_tmp = log_tmp + "," + str(log_sitecate) + "(" + str(log_delcnt) + ")"
        print(">> log_tmp : {}".format(log_tmp))

        sql_del_i = "delete from del_goods_log where regdate < getdate() - 90" # 90일 이전 로그 삭제
        print(">> sql_del_i : {}".format(sql_del_i))
        db_FS.execute(sql_del_i)

        sql_ins_i = "insert into del_goods_log (del_count, menu_kbn, memo, reason_memo) values ('{}','{}','{}','{}')".format(log_tmp,sel_menu,sel_msg, tmpReasonLog)
        print(">> sql_ins_i : {}".format(sql_ins_i))
        db_FS.execute(sql_ins_i)

    time.sleep(2)
    # procUrl = "http://imp.allinmarket.co.kr/admin/goods/freeship/del_goods_overlap.asp?mode=del&cateno=1"
    # print("procUrl : {}".format(procUrl))
    # # chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    # # webbrowser.get(chrome_path).open_new(procUrl)
    # webbrowser.open_new_tab(procUrl)

    ############################################
    # 네이버 삭제상품 - > 프리쉽 품절처리
    goods_del_proc("del_goods_naver", "네이버 삭제 상품", "Y")
    ############################################

    time.sleep(3)
    now = datetime.datetime.now()
    print('>> 작업 완료 (네이버 쇼핑 삭제상품) :' + str(now))
    procLogSet("naver_shopping_del", "F", "0", " 네이버 쇼핑 삭제상품 삭제 (new) OK " + (sel_msg) + " ")

    try:
        db_FS.close()
        mainDriver.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)
