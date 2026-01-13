import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
import time
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
    print('>> 작업 시작 (네이버 썸네일 생성) :' + str(now))

    in_page = input("Input end page :")
    now_url = 'https://center.shopping.naver.com/login'
    try:
        mainDriver = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        mainDriver = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    mainDriver.get(now_url)
    mainDriver.set_window_size(1100, 800)
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

    time.sleep(2)
    print('time.sleep(2)')

    # 상품현황 및 관리 버튼 클릭
    #aGoods2btn = WebDriverWait(mainDriver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.last>a")))
    aGoods2btn = mainDriver.find_element(By.LINK_TEXT,'상품현황 및 관리')
    aGoods2btn.click()
    print('>> 상품현황 및 관리 버튼 클릭 Ok')

    time.sleep(2)
    print('time.sleep(2)')

    # 미서비스 상품 버튼 클릭
    # aGoods3btn = mainDriver.find_element(By.LINK_TEXT,'미서비스 상품')
    # aGoods3btn.click()
    # print('>> 미서비스 상품 버튼 클릭 Ok')
    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/noservice/list.nhn')
    print('>> 미서비스 상품 page Ok')

    time.sleep(2)
    print('time.sleep(2)')

    # 썸네일 생성실패
    aGoods4btn = mainDriver.find_elements(By.CLASS_NAME,'tit_cate')[2]
    aGoods4btn.click()
    print('>> 썸네일 생성실패')

    time.sleep(2)
    print('time.sleep(2)')

    # 리스팅 개수 클릭
    mainDriver.find_elements(By.CLASS_NAME,'tab_toggle')[3].click()
    time.sleep(2)
    print('time.sleep(2)')

    # 리스팅 100개
    aGoods5btn = mainDriver.find_element(By.LINK_TEXT,'100개')
    aGoods5btn.click()
    print('>> 리스팅 개수 100개')

    # 정렬순서 클릭
    mainDriver.find_elements(By.CLASS_NAME,'tab_toggle')[4].click()
    time.sleep(2)
    print('time.sleep(2)')
    # 정렬순서 이전등록순
    aGoods5btn = mainDriver.find_element(By.LINK_TEXT,'이전등록순')
    aGoods5btn.click()
    print('>> 정렬순서 이전등록순')

    time.sleep(2)
    procLogSet("naver_thumbnail_click_cps", "S", "0", " 네이버 썸네일 시작 ")

    source_first = mainDriver.page_source
    time.sleep(2)
    if str(source_first).find('class="func_rgt func_paginate"') > -1:
        page_all = func.getparse(str(source_first), 'class="func_rgt func_paginate"', '</div>')
        page_all = func.getparse(str(page_all), '<fmt:formatnumber>', '</fmt:formatnumber>')
        page_all = str(page_all).strip()

    if in_page == "" or float(in_page) > float(page_all):
        in_page = page_all

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

                n_regdate = ""
                n_reason = ""
                spTdSoup = str(ea_item).split('<td')
                naver_no = func.getparse(ea_item, 'id="', '"')
                goodscodeN = func.getparse(ea_item, "openProductDetailPopup('", "')")
                if str(naver_no) != "":
                    n_regdate = spTdSoup[7] # 등록일자
                    n_regdate = func.getparse(str(n_regdate), ">", "</td>")
                    n_reason = spTdSoup[10] # 이미지 생성실패 사유
                    n_reason = func.getparse(str(n_reason), ">", "</td>")
                    print(" 등록일자 : {} | 이미지 생성실패 사유 : {} ".format(n_regdate, n_reason))

                reason = ""
                if naver_no != "":
                    if n_reason.find('파일이 없음') > -1:
                        reason = "파일이 없음"
                    elif n_reason.find('이미지 사이즈 오류') > -1:
                        reason = "이미지 사이즈 오류"
                    elif n_reason.find('이미지 포맷 오류') > -1:
                        reason = "이미지 포맷 오류"
                    elif n_reason.find('블랙리스트') > -1:
                        reason = "블랙리스트"
                    elif n_reason.find('접속권한 없음') > -1:
                        reason = "접속권한 없음"
                    elif n_reason.find('다운로드 오류') > -1:
                        reason = "다운로드 오류"
                    elif n_reason.find('서버 오류') > -1:
                        reason = "서버 오류"
                    elif n_reason.find('Time-out') > -1:
                        reason = "Time-out"
                    else:
                        reason = "기타"

                    sitecate = ""
                    guid = ""
                    chk_inFlg = ""

                    goodscode = goodscodeN
                    if goodscode[-1:] == "N":  # goodscode 마지막 문자가 N일 경우 N제거
                        goodscode = goodscode[:-1]

                    sitecate = func.getSiteName(goodscode)
                    guid = func.getGuid(goodscode)

                    if goodscode != "" and sitecate != "" and guid != "" and reason != "기타":

                        if sitecate == "best" or sitecate == "global" or sitecate == "mall" or sitecate == "usa" or sitecate == "de" or sitecate == "uk" or sitecate == "handmade" or sitecate == "cn":
                            if reason == "파일이 없음":
                                reason = "아마존 파일이 없음"

                        sql = " select goodscode from img_del_goods where goodscode = '{}'".format(
                            goodscode)
                        row = db_FS.selectone(sql)
                        if not row:
                            isql = "insert into img_del_goods (goodscode, goodscodeN, nvMid, guid, sitecate,reason, naver_regdate) values('{}','{}','{}','{}','{}','{}','{}')".format(
                                goodscode, goodscodeN, naver_no, guid, sitecate, reason, n_regdate)
                            db_FS.execute(isql)
                            chk_inFlg = " (Insert Ok) "
                            procCnt = procCnt + 1

                    print(' {} page [{}] {} | {} ( {} ) | {} | {} | {} | {}'.format(
                        prow, rowCnt, naver_no, goodscode,  guid, sitecate, reason, n_regdate, chk_inFlg))

                    rowCnt = rowCnt + 1

        time.sleep(1)
        print('time.sleep(1)')
        
        try:
            nextBtn = mainDriver.find_element(By.LINK_TEXT,'다음 ›')
            nextBtn.click()
        except Exception as e:
            print(e)
            break
        else:
            print("다음 ›")

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

    procUrl = "http://imp.allinmarket.co.kr/admin/goods/freeship/naver_cps_img_update_v3.asp?cateno=1"
    procLogSet("naver_thumbnail_click_cps", "P", str(procCnt), str(procUrl))
    print("procUrl : {}".format(procUrl))
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open_new(procUrl)
    
    time.sleep(3)
    mainDriver.quit()
    procLogSet("naver_thumbnail_click_cps", "F", "0", " 네이버 썸네일 완료 : {}".format(procUrl))
    
    db_FS.close()
    print(">> procCnt : {}".format(procCnt))
    print('>> 작업 완료 (네이버 썸네일 생성) :' + str(now))

    os._exit(0)

    #input("KEY : ")