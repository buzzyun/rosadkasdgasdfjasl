import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import os
import datetime
import webbrowser
import DBmodule_FR
import func
import func_user

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

if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> 작업 시작 (네이버 쇼핑 삭제상품) :' + str(now))

    now_url = 'https://center.shopping.naver.com/login'
    try:
        mainDriver = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        mainDriver = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
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

    pMainSoup = mainDriver.page_source
    procList = []
    procCnt = 0
    titCnt = 0

    if str(pMainSoup).find('delResnList') > -1:
        naver_del_cnt = ""
        naver_del_cnt = func.getparse(str(pMainSoup), 'prdt_status_lst', 'delResnList')
        naver_del_cnt = func.getparse(str(naver_del_cnt), '<span>', '</span>')
        naver_del_cnt = naver_del_cnt.replace(",","").strip()
        print(" Naver 삭제 상품수 : {} ".format(naver_del_cnt))

        procLogSet("naver_shopping_del", "S", "0", " 네이버 쇼핑 삭제상품 삭제시작 (전체) : " + str(naver_del_cnt))

        mainSoup = func.getparse(str(pMainSoup), 'delResnList', 'previousCursorState')
        spMainSoup = mainSoup.split('class="tit_cate"')

        for ea_mainitem in spMainSoup:
            ea_reason = func.getparse(str(ea_mainitem), '<strong>', '</strong>')
            ea_delcnt = func.getparse(str(ea_mainitem), '<span>', '</span>')
            ea_reason = str(ea_reason).strip()
            ea_delcnt = str(ea_delcnt).strip()

            if ea_delcnt == "":
                print('>> (SKIP) ea_reason : {} '.format(ea_reason))
            elif ea_reason != "중복상품":
                print('>> ea_reason : {} | ea_delcnt : {} '.format(ea_reason, ea_delcnt))
            else: # 중복상품만 처리
                print('>> ea_reason : {} | ea_delcnt : {} '.format(ea_reason, ea_delcnt))
                procList.append([])
                procList[procCnt].append(titCnt)
                procList[procCnt].append(ea_reason)
                procList[procCnt].append(ea_delcnt)
                procCnt = procCnt + 1
            titCnt = titCnt + 1

        print(">> 중복상품 procCnt : {}".format(procCnt))

        for pItem in procList:
            print("pItem : {}".format(pItem))
            del_cnt = str(pItem[2]).replace(",","").strip()

            abtn = mainDriver.find_elements(By.CLASS_NAME,'tit_cate')[pItem[0]]
            abtn.click()
            print('>>{} Click'.format(pItem[1]))

            time.sleep(2)
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

            prow = 0
            for prow in range(1, int(pageAll)+1): 
                print(" page {} / {}".format(prow,pageAll))

                pSoup = mainDriver.page_source
                if str(pSoup).find('id="productTable"') == -1:
                    print(" No Data. End ")
                    break
                else:
                    soup = func.getparse(str(pSoup), 'id="productTable"', '</table>')
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

                            sql = " select goodscode from del_goods where goodscode = '{}'".format(goodscode)
                            row = db_FS.selectone(sql)
                            if not row:
                                isql = "insert into del_goods (guid,sitecate,goodscode,naver_no,reason,goodscodeN) values('{}','{}','{}','{}','{}','{}')".format(guid, sitecate, goodscode, naver_no, del_reason, goodscodeN)
                                db_FS.execute(isql)

                                print(' {} page [{}] {} | {} ( {} ) | {} | {} | (Insert Ok)'.format(prow, rowCnt, naver_no, goodscode,  guid, sitecate, del_reason))
                            else:
                                print(' {} page [{}] {} | {} ( {} ) | {} | {} | (del_goods 존재 Skip)'.format(prow, rowCnt, naver_no, goodscode,  guid, sitecate, del_reason))

                        rowCnt = rowCnt + 1

                    if int(prow) < int(pageAll):
                        time.sleep(1)
                        print('time.sleep(1)')
                        try:
                            nextBtn = mainDriver.find_element(By.LINK_TEXT,'다음 ›')
                            if nextBtn:
                                nextBtn.click()
                                print("다음 ›")
                        except Exception as e:
                            print(e)
                            break

                    time.sleep(1)
                    print('time.sleep(1)')


    sql = " select count(*) as gCnt from del_goods"
    rowC = db_FS.selectone(sql)
    if rowC:
        gCnt = 0
        gCnt = rowC[0]
        if int(gCnt) == int(naver_del_cnt):
            print(">> 네이버 삭제상품수 : {} | del_goods Inert 상품수 : {} (확인 완료) ".format(naver_del_cnt, gCnt))
        else:
            print(">> 네이버 삭제상품수 : {} | del_goods Inert 상품수 : {} (확인 필요) ".format(naver_del_cnt, gCnt))

    time.sleep(2)
    procUrl = "http://imp.allinmarket.co.kr/admin/goods/freeship/del_goods_overlap.asp?mode=del&cateno=1"
    print("procUrl : {}".format(procUrl))
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open_new(procUrl)

    time.sleep(3)
    mainDriver.quit()

    now = datetime.datetime.now()
    print('>> 작업 완료 (네이버 쇼핑 삭제상품) :' + str(now))
    procLogSet("naver_shopping_del", "F", "0", " 네이버 쇼핑 삭제상품 삭제 OK: " + str(procUrl))
    os._exit(0)
