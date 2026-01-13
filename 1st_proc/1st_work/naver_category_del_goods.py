import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import time
import webbrowser
import DBmodule_FR
import func_user
import func
global ver
ver = "241017"
print(">> var : {}".format(ver))
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
    print('>> 작업 시작 (네이버 카테고리 분류불가 치리) :' + str(now))
    ## in_page = input("Input end page :")
    in_page = ""

    now_url = 'https://center.shopping.naver.com/login'
    # try:
    #     mainDriver = func_user.connectDriverNew(now_url, "")
    # except Exception as e:
    #     print(">> connectDriverOld set ")
    #     mainDriver = func_user.connectDriverOld(now_url, "")
    #     print(">> connectDriverOld set OK ")
    # mainDriver.get(now_url)
    # mainDriver.set_window_size(1100, 800)
    # mainDriver.implicitly_wait(3)

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
    time.sleep(4)
    print('time.sleep(4)')

    # 상품현황 및 관리 버튼 클릭
    #aGoods2btn = WebDriverWait(mainDriver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.last>a")))
    aGoods2btn = mainDriver.find_element(By.LINK_TEXT,'상품현황 및 관리')
    aGoods2btn.click()
    print('>> 상품현황 및 관리 버튼 클릭 Ok')
    time.sleep(4)
    print('time.sleep(4)')


    # 미서비스 상품 버튼 클릭
    # aGoods3btn = mainDriver.find_element(By.LINK_TEXT,'미서비스 상품')
    # aGoods3btn.click()
    # print('>> 미서비스 상품 버튼 클릭 Ok')
    # time.sleep(4)
    # print('time.sleep(4)')
    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/noservice/list.nhn')
    print('>> 미서비스 상품 page Ok')

    # 카테고리 분류불가
    aGoods4btn = mainDriver.find_elements(By.CLASS_NAME,'tit_cate')[3]
    aGoods4btn.click()
    print('>> 카테고리 분류불가')
    time.sleep(4)
    print('time.sleep(4)')

    # 리스팅 개수 클릭
    mainDriver.find_elements(By.CLASS_NAME,'tab_toggle')[3].click()
    time.sleep(4)
    print('time.sleep(4)')

    # 리스팅 100개
    aGoods5btn = mainDriver.find_element(By.LINK_TEXT,'100개')
    aGoods5btn.click()
    print('>> 리스팅 개수 100개')

    # 정렬순서 클릭
    mainDriver.find_elements(By.CLASS_NAME,'tab_toggle')[4].click()
    time.sleep(4)
    print('time.sleep(4)')
    # 정렬순서 이전등록순
    aGoods5btn = mainDriver.find_element(By.LINK_TEXT,'이전등록순')
    aGoods5btn.click()
    print('>> 정렬순서 이전등록순')
    time.sleep(4)

    source_first = mainDriver.page_source
    time.sleep(4)
    if str(source_first).find('class="func_rgt func_paginate"') > -1:
        page_all = func.getparse(str(source_first), 'class="func_rgt func_paginate"', '</div>')
        page_all = func.getparse(str(page_all), '<fmt:formatnumber>', '</fmt:formatnumber>')
        page_all = str(page_all).strip()

    if in_page == "" or float(in_page) > float(page_all):
        in_page = page_all

    naver_del_cnt = 0
    if str(source_first).find('delResnList') > -1:
        naver_del_cnt = ""
        naver_del_cnt = func.getparse(str(source_first), 'prdt_status_lst', 'id="searchForm"')
        naver_del_cnt = func.getparse(str(naver_del_cnt), '미서비스 상품수', '</a>')
        naver_del_cnt = func.getparse(str(naver_del_cnt), '<span>', '</span>')
        naver_del_cnt = naver_del_cnt.replace(",","").strip()
        print(" Naver 삭제 상품수 : {} ".format(naver_del_cnt))

    procLogSet("naver_category_del_goods", "S", "0", " 네이버 카테고리분류불가 Start ( " + str(page_all) + str(" page : " + str(naver_del_cnt) + " 개 ) "))
    procCnt = 0
    mall_List = []
    for prow in range(1, int(in_page)+1):
        print(" Page : {} / {} ".format(prow, in_page))

        pSoup = mainDriver.page_source
        if str(pSoup).find('id="productTable"') > -1:
            soup = func.getparse(str(pSoup), 'id="productTable"', '</table>')
            spSoup = soup.split('<tr')
            #print('spSoup : {}'.format(spSoup))
            rowCnt = 0
            for ea_item in spSoup:
                ea_item = str(ea_item)
                spTdSoup = str(ea_item).split('<td')
                naver_no = func.getparse(ea_item, 'id="', '"')
                goodscodeN = func.getparse(ea_item, "openProductDetailPopup('", "')")
                if str(naver_no) != "":
                    sitecate = ""
                    guid = ""
                    chk_inFlg = ""
                    goodscode = goodscodeN
                    if goodscode[-1:] == "N":  # goodscode 마지막 문자가 N일 경우 N제거
                        goodscode = goodscode[:-1]

                    sitecate = func.getSiteName(goodscode)
                    guid = func.getGuid(goodscode)

                    if goodscode != "" and sitecate != "" and guid != "":
                        sql = " select goodscode from del_goods where goodscode = '{}'".format(goodscode)
                        row = db_FS.selectone(sql)
                        if not row:
                            isql = "insert into del_goods (guid,sitecate,goodscode) values('{}','{}','{}')".format(guid, sitecate, goodscode)
                            db_FS.execute(isql)
                            chk_inFlg = " (Insert Ok) "
                            procCnt = procCnt + 1

                    print(' {} / {} page [{}] {} ( {} ) | {} | {} '.format(prow, page_all, rowCnt, goodscode, guid, sitecate, chk_inFlg))
                    rowCnt = rowCnt + 1

        print(">> prow: {} | in_page : {} | page_all : {}".format(prow, in_page, page_all))
        if int(prow) >= int(in_page):
            print(">> 마지막 이상 stop ")
            break

        if int(prow) >= int(page_all):
            print(">> 마지막 이상 (1) stop ")
            break

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
            try:
                nextBtn = mainDriver.find_element(By.CSS_SELECTOR,'[data-direction=NEXT]')
                nextBtn.click()
            except Exception as e:
                print(">> nextBtn Exception ")

        time.sleep(1)
        print('time.sleep(1)')

    now = datetime.datetime.now()

    # 쿠키 정보 Save
    cookies = mainDriver.get_cookies()
    print(len(cookies))
    # print(cookies)

    cookies_list = mainDriver.get_cookies()
    cookieString = ""
    for cookie in cookies_list[:-1]:
        cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
    cookieString = cookieString + cookies_list[-1]["name"] + "=" + cookies_list[-1]["value"]

    # print(cookieString)
    uSql = " update cookie_list set cookie = '{}' where proc_id = 'naver_cps'".format(
        cookieString)
    db_FS.execute(uSql)

    print(">> 사이트별 삭제 Count Log Insert : 네이버 카테고리 분류불가 ")
    log_tmp = ""
    sql_l = "select sitecate, count(*) from del_goods group by sitecate "
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

        sql_ins_i = "insert into del_goods_log (del_count, menu_kbn, memo, reason_memo) values ('{}','{}','{}','{}')".format(log_tmp,"0","전체상품", "카테고리 분류불가")
        print(">> sql_ins_i : {}".format(sql_ins_i))
        db_FS.execute(sql_ins_i)


    procUrl = "http://imp.allinmarket.co.kr/admin/goods/freeship/del_goods_overlap_naverdel.asp?mode=del&cateno=1"
    print(">> procCnt : {}".format(procCnt))
    procLogSet("naver_thumbnail_click_cps", "P", str(procCnt), str(procUrl))
    print("procUrl : {}".format(procUrl))
    # chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    # webbrowser.get(chrome_path).open_new(procUrl)
    webbrowser.open_new_tab(procUrl)

    time.sleep(3)
    now = datetime.datetime.now()
    print('>> 작업 완료 (네이버 썸네일 생성) :' + str(now))
    procLogSet("naver_category_del_goods", "F", "0", " 네이버 카테고리분류불가 완료 :" + str(procUrl))

    try:
        db_FS.close()
        mainDriver.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)