
import time
import os
import datetime
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR
import func_user

db_con = DBmodule_FR.Database('freeship')

########################################################################################
# http://kpsanews.kr/  리콜 상품 및 위해 상품 판매불가 처리 
########################################################################################
global gProc_no
global upd_cnt
global sold_cnt
gProc_no = "KPSANEWS_PROC"

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)

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


# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode) values ('{}','{}')".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def notSale_proc(db_FS, db_con, Duid, D_naver_in, D_goodscode, flg):

    sql_u1 = "update t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1' where uid = {0}".format(Duid)
    db_con.execute(sql_u1)
    sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
    db_con.execute(sql_u2)
    print(">> 판매불가 처리 : {}".format(D_goodscode))

    # 네이버 노출 상품이 품절되었을 경우,naver_del 테이블에 Insert 
    if str(D_naver_in) == "1":
        # proc_ep_insert(D_goodscode,'D')
        sql = "select goodscode from naver_del where goodscode = '{}'".format(D_goodscode)
        rowFS = db_FS.selectone(sql)
        if not rowFS:
            i_sql = "insert into naver_del (goodscode) values('" +str(D_goodscode)+ "')"
            print(">> naver_del Insert (i_sql) : {}".format(i_sql))
            db_FS.execute(i_sql)

def moveScroll(driver, height, max_sroll_cnt):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = height
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > max_sroll_cnt:
            break
        last_height = new_height


def proc_write(browser, row_cnt):
    write_flg = ""
    time.sleep(1)
    try:
        elems2 = browser.find_elements(By.CSS_SELECTOR,'div.d-flex.btn-area > button')
        if elems2[row_cnt]:
            elems2[row_cnt].click() # 문의사항 클릭
            time.sleep(1)
            browser.find_element(By.CSS_SELECTOR,'#user1').click()
            time.sleep(0.5)
            browser.find_element(By.XPATH,'//*[@id="inquiryModal"]/ul/li[2]/div/input').send_keys("프리쉽")
            time.sleep(0.5)
            browser.find_element(By.XPATH,'//*[@id="inquiryModal"]/ul/li[3]/div/input').send_keys("1800-5086")
            time.sleep(0.5)
            browser.find_element(By.XPATH,'//*[@id="inquiryModal"]/ul/li[4]/div/input').send_keys("help@freeship.co.kr")
            time.sleep(0.5)
            browser.find_element(By.XPATH,'//*[@id="inquiryModal"]/ul/li[5]/div/textarea').send_keys("(프리쉽) 상품삭제 완료 하였습니다.")
            time.sleep(1)

            browser.find_element(By.CSS_SELECTOR,'#inquireModal > div > div > form > input').click() # 제출 버튼
            time.sleep(1)

            try:
                # alert 확인 클릭
                da = Alert(browser)
                time.sleep(0.5)
                if str(da.text).find('문의가') > -1:
                    write_flg = "0"
                    print(da.text)
                da.accept()
                time.sleep(1)
            except:
                print(" No Alert ")
            else:
                write_flg = "0"
            time.sleep(1)

    except Exception as ex:
        print('>>문의사항 쓰기 Exception : ' + str(ex))

    return write_flg


def proc_work_1(db_FS, browser, row_cnt, recall_uid):
    global upd_cnt
    global sold_cnt

    time.sleep(1)
    elem = '#gall_ul > div:nth-child(' + str(row_cnt) + ') > div > div.product > div.info > button'
    if browser.find_element(By.CSS_SELECTOR,elem):
        browser.find_element(By.CSS_SELECTOR,elem).click() # 판매몰 확인 클릭
        time.sleep(1)
        pop_result = str(browser.page_source)

        tmp_guid = ""
        tmp_sitecate = ""
        tmp_goodscode = ""

        pop_result = func_user.getparse(pop_result,'id="shopModal"','')
        pop_list = func_user.getparse(pop_result,'id="shopModalCont"','</ul>')
        sp_pop = pop_list.split('<li>')

        for ea_name in sp_pop:
            store_name = func_user.getparse(ea_name,'<p>','</p>')
            store_url = func_user.getparse(ea_name,'href="','"')
            if store_name.find("프리쉽") > -1:
                # 프리쉽 체크 
                uSql = " update recall_kpsanews set freeship_ck = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
                db_FS.execute(uSql)
                # print(">> uSql: {} ".format(uSql))

                print(">> 프리쉽 처리 (freeship_ck=1) : {} | {}".format(store_name, store_url))
                guid = func_user.getparse(store_url,'guid=','&')
                sitecate = func_user.getparse(store_url,'sitecate=','&')
                print(">> sitecate : {} | guid : {}".format(sitecate, guid))

                if tmp_guid == "":
                    tmp_guid = guid
                    tmp_sitecate = sitecate
                else:
                    tmp_guid = tmp_guid + " / " + guid
                    tmp_sitecate = tmp_sitecate + " / " + sitecate

                db_con = DBmodule_FR.Database(sitecate)
                sql2 = "select IsDelContentFile from t_goods_sub where uid = {0}".format(guid)
                row2 = db_con.selectone(sql2)
                if row2:
                    IsDelContentFile = row2[0]
                    if IsDelContentFile == "T":
                        print(">> 판매불가 되어있음 {} (Skip): {}".format(guid))
                    else:
                        print(">> 판매불가 처리 실행 : {}".format(guid))
                        sql = "select goodscode, IsDisplay, isnull(Del_Naver,''), isnull(stop_update,''), isnull(naver_in,0) from t_goods where uid = '{}'".format(guid)
                        row = db_con.selectone(sql)
                        if row:
                            goodscode = row[0]
                            isdisplay = row[1]
                            del_naver = row[2]
                            stop_update = row[3]
                            naver_in = row[4]

                            # 판매불가 처리
                            notSale_proc(db_FS, db_con, guid, naver_in, goodscode, "")
                            if tmp_goodscode == "":
                                tmp_goodscode = goodscode
                            else:
                                tmp_goodscode = tmp_goodscode + " / " + goodscode
                            sold_cnt = sold_cnt + 1
                db_con.close()

    browser.find_element(By.CSS_SELECTOR,'#shopModal > div > div > button').click() # 닫기 버튼 클릭
    time.sleep(1)

    if tmp_guid != "":
        uSql = " update recall_kpsanews set freeship_ck = '1', updatedate = getdate(), tmp_guid = '{}', tmp_sitecate = '{}', tmp_goodscode = '{}' where recall_uid = '{}'".format(tmp_guid, tmp_sitecate, tmp_goodscode, recall_uid)
        db_FS.execute(uSql)
        print(">> recall_kpsanews : {} ( 리콜 프리쉽 체크 처리 ) ".format(recall_uid))
        # print(">> uSql: {} ".format(uSql))

        # 문의사항 입력
        write_flg = proc_write(browser, row_cnt)
        if write_flg == "0":
            uSql = " update recall_kpsanews set proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
            db_FS.execute(uSql)
            print(">> recall_kpsanews 문의사항 쓰기 OK: {} ( 리콜 프리쉽 완료처리 ) ".format(recall_uid))
            # print(">> uSql: {} ".format(uSql))
            upd_cnt = upd_cnt + 1

    else:
        # 프리쉽 없음 완료처리 
        uSql = " update recall_kpsanews set freeship_ck = '0', proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
        db_FS.execute(uSql)
        print(">> 판매자명 프리쉽 없음: {} (완료처리) ".format(recall_uid))
        print(">> uSql: {} ".format(uSql))

    return "0"

def proc_main_1(browser, procflg):
    global sold_cnt
    sold_cnt = 0

    now_url = "http://kpsanews.kr/bbs/board.php?bo_table=monitor"
    browser.get(now_url)
    time.sleep(3)
    result = str(browser.page_source)
    maxCnt = func_user.getparse(str(result),'class="view-num ml-auto"','</select>')
    now_url = now_url + "&newP=" + func_user.getparseR(str(maxCnt),'value="','"')
    print(">> now_url : {}".format(now_url))
    browser.get(now_url)

    time.sleep(3)
    moveScroll(browser, 380, 1)
    time.sleep(1)

    result = str(browser.page_source)
    tmpList = func_user.getparse(result,'name="fboardlist"','</form>')
    tmpList = func_user.getparse(tmpList,'gall_ul','')
    sp_tmpList = tmpList.split('class="gall_li')
    print(">> sp_tmpList : {}".format(len(sp_tmpList)))

    db_FS = DBmodule_FR.Database("freeship")
    row_cnt = 0
    for item in sp_tmpList:
        if row_cnt == 0:
            row_cnt = row_cnt + 1
            print(">> row_cnt Skip ")
            continue

        recall_img = func_user.getparse(item,'class="img">','</div>')
        if recall_img.find('-->') > -1:
            recall_img = func_user.getparse(recall_img,'-->','')
        recall_img = func_user.getparse(recall_img,'<img src="','"').replace("'","").strip()
        info = func_user.getparse(item,'<div class="info">','</div>')
        recall_cate = func_user.getparse(info,'<p>','</p>')
        recall_model = func_user.getparse(info,'모델명 :','</li>')
        recall_model = func_user.getparse(recall_model,'>','<')
        recall_biz_name = func_user.getparse(info,'사업자명 : ','</li>')
        recall_biz_name = func_user.getparse(recall_biz_name,'>','<')
        recall_type = func_user.getparse(info,'리콜종류 :','</li>')
        recall_regdate = func_user.getparse(info,'공표일 :','</li>')
        popup_no = func_user.getparse(info,'mall_board_popup(',')').replace("'","")
        recall_url = func_user.getparse(item,'class="d-flex btn-area"','</div>')
        recall_url = func_user.getparse(recall_url,'a href="','"').replace("'","").strip()
        recall_url = recall_url.replace("&amp;","&").strip()
        recall_certNum = ""

        recall_uid = ""
        print("\n\n-----------------------------------------------")
        print(">>({}) [{}] {} | {} | {} | {} (popup:{})".format(row_cnt, recall_cate, recall_model, recall_biz_name, recall_type, recall_regdate, popup_no))

        if str(recall_url).find("selectBbsNttView.do") > -1: # 소비자위해감시시스템
            recall_uid = func_user.getparse(recall_url,'key=','&') + "_" + func_user.getparse(recall_url,'bbsNo=','&') + "_" + func_user.getparse(recall_url,'nttNo=','&').strip()
            recall_kbn = '2'
        elif  str(recall_url).find("ajax/recallBoard") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'recallUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("ajax/fRecallBoard") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'recallUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("certUid=") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'certUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("certNum=") > -1: # 제품안전정보협회
            recall_uid = func_user.getparse(recall_url,'certNum=','').strip()
            recall_kbn = '3'
        elif str(recall_url) == "-":
            print(">> No recall_url : {}".format(recall_url))
        else:
            print(">> No recall_url !! Check Please : {}".format(recall_url))
            func_user.procLogSet(db_FS, gProc_no, "E", "0", " recall_url Check : "+str(recall_url))

        print(">> Recall [{}] {} | {}".format(recall_uid, recall_certNum, recall_url))
        if recall_uid == "":
            row_cnt = row_cnt + 1
            print(">> No recall_uid !! Check Please : {}".format(recall_url))
            continue
        time.sleep(1)

        sql = " select isnull(freeship_ck,''), isnull(proc_flg,'') from recall_kpsanews where recall_uid = '{}'".format(recall_uid)
        rowF = db_FS.selectone(sql)
        if not rowF:
            print(">> DB Insert : {}".format(recall_uid))
            iSql = " insert into recall_kpsanews \
                (recall_uid,recall_kbn,recall_cate,recall_model,recall_biz_name,recall_type,recall_regdate,recall_url,recall_img) \
                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')\
                ".format(recall_uid,recall_kbn,recall_cate[:200],recall_model[:500],recall_biz_name[:500],recall_type[:200],recall_regdate,recall_url[:200],recall_img[:200])
            db_FS.execute(iSql)
            freeship_ck = ""
            proc_flg = ""
        else:
            freeship_ck = rowF[0]
            proc_flg = rowF[1]
            print(">> recall_kpsanews (DB 존재) : {} | freeship_ck : {} | proc_flg : {} ".format(recall_uid, freeship_ck, proc_flg))

        if proc_flg == "1":
            print(">> 이미 완료된 건 ( Skip ) : {}".format(recall_uid))
        else:
            if popup_no == "":
                uSql = " update recall_kpsanews set freeship_ck = '0', proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
                db_FS.execute(uSql)
                print(">> recall_kpsanews : {} ( 리콜 판매자정보 없음 완료 처리 ) ".format(recall_uid))
                # print(">> uSql: {} ".format(uSql))
            else:
                proc_work_1(db_FS, browser, row_cnt, recall_uid)

        row_cnt = row_cnt + 1

    db_FS.close()
    print(">> proc_cnt (전체리스트) : {} | upd_cnt (문의사항 완료) : {} | sold_cnt (판매불가 완료) : {} ".format(len(sp_tmpList), upd_cnt, sold_cnt))
    func_user.procLogSet(db_con, gProc_no, "P", upd_cnt, " 리콜상품 (전체:"+str(len(sp_tmpList))+"|문의완료:"+str(upd_cnt)+"|판매불가:"+str(sold_cnt)+")")

    return "0"


def proc_work_2(db_FS, browser, row_cnt, recall_uid, store_name, store_url):
    global upd_cnt
    global sold_cnt

    time.sleep(1)
    tmp_guid = ""
    tmp_sitecate = ""
    tmp_goodscode = ""

    print(">> 프리쉽 처리 (freeship_ck=1) : {} | {}".format(store_name, store_url))
    uSql = " update recall_kpsanews set freeship_ck = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
    db_FS.execute(uSql)
    # print(">> uSql: {} ".format(uSql))

    guid = func_user.getparse(store_url,'guid=','&')
    sitecate = func_user.getparse(store_url,'sitecate=','&')
    print(">> sitecate : {} | guid : {}".format(sitecate, guid))
    tmp_guid = guid
    tmp_sitecate = sitecate

    db_con = DBmodule_FR.Database(sitecate)
    sql2 = "select IsDelContentFile from t_goods_sub where uid = '{}'".format(guid)
    row2 = db_con.selectone(sql2)
    if row2:
        IsDelContentFile = row2[0]
        if IsDelContentFile == "T":
            print(">> 판매불가 되어있음 {} (Skip): {}".format(guid))
        else:
            print(">> 판매불가 처리 실행 : {}".format(guid))
            sql = "select goodscode, IsDisplay, isnull(Del_Naver,''), isnull(stop_update,''), isnull(naver_in,0) from t_goods where uid = '{}'".format(guid)
            row = db_con.selectone(sql)
            if row:
                goodscode = row[0]
                isdisplay = row[1]
                del_naver = row[2]
                stop_update = row[3]
                naver_in = row[4]

                # 판매불가 처리
                notSale_proc(db_FS, db_con, guid, naver_in, goodscode, "")
                tmp_goodscode = goodscode
                sold_cnt = sold_cnt + 1

    db_con.close()

    if tmp_guid != "":
        uSql = " update recall_kpsanews set freeship_ck = '1', updatedate = getdate(), tmp_guid = '{}', tmp_sitecate = '{}', tmp_goodscode = '{}' where recall_uid = '{}'".format(tmp_guid, tmp_sitecate, tmp_goodscode, recall_uid)
        db_FS.execute(uSql)
        print(">> recall_kpsanews : {} ( 리콜 프리쉽 체크 처리 ) ".format(recall_uid))
        print(">> uSql: {} ".format(uSql))

        # 문의사항 입력
        write_flg = proc_write(browser, row_cnt)
        if write_flg == "0":
            uSql = " update recall_kpsanews set proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
            db_FS.execute(uSql)
            print(">> recall_kpsanews 문의사항 쓰기 OK: {} ( 리콜 프리쉽 완료처리 ) ".format(recall_uid))
            # print(">> uSql: {} ".format(uSql))
            upd_cnt = upd_cnt + 1

    else:
        # 프리쉽 없음 완료처리 
        uSql = " update recall_kpsanews set freeship_ck = '0', proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
        db_FS.execute(uSql)
        print(">> 판매자명 프리쉽 없음: {} (완료처리) ".format(recall_uid))
        print(">> uSql: {} ".format(uSql))

    return "0"

def proc_main_2(browser, procflg):
    global sold_cnt
    sold_cnt = 0
    now_url = "http://kpsanews.kr/sub/monitor.php"
    print(">> now_url : {}".format(now_url))
    browser.get(now_url)
    time.sleep(3)

    maxCnt = 10
    result = str(browser.page_source)
    tmpPage = func_user.getparse(str(result),'class="view-num ml-auto"','</select>')
    spMaxCnt = tmpPage.split('</option>')
    maxCnt = len(spMaxCnt) - 1
    print(">> maxCnt : {}".format(maxCnt))
    time.sleep(3)
    moveScroll(browser, 380, 1)
    time.sleep(1)

    browser.find_element(By.CSS_SELECTOR,'#limit').click()
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR,'#limit > option:nth-child(' +str(maxCnt)+ ')').click()
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR,'#keyword').click()
    time.sleep(1)

    result = str(browser.page_source)
    tmpList = func_user.getparse(result,'id="monitor_list"','</section>')
    sp_tmpList = tmpList.split('class="product"')
    print(">> sp_tmpList : {}".format(len(sp_tmpList)))

    db_FS = DBmodule_FR.Database("freeship")
    row_cnt = 0
    for item in sp_tmpList:
        if row_cnt == 0:
            row_cnt = row_cnt + 1
            print(">> row_cnt Skip ")
            continue

        recall_img = ""
        info = func_user.getparse(item,'<div class="info">','')
        recall_cate = func_user.getparse(info,'<p>','</p>')
        recall_model = func_user.getparse(info,'품목명 :','</li>').replace('"','').strip()
        recall_biz_name = func_user.getparse(info,'판매몰 : ','</li>').replace('"','').strip()
        recall_type = func_user.getparse(info,'위해구분 :','</li>').replace('"','').strip()
        recall_regdate = ""
        popup_link = func_user.getparseR(info,'','class="shop-link"')
        popup_link = func_user.getparse(popup_link,'<a href="','"')
        recall_url = func_user.getparse(item,'class="d-flex btn-area"','</div>')
        recall_url = func_user.getparse(recall_url,"javascript:window.open(",')').replace("'","").strip()
        recall_url = recall_url.replace("&amp;","&").strip()
        recall_certNum = ""

        recall_uid = ""
        print("\n\n-----------------------------------------------")
        print(">>({}) [{}] {} | {} | {} | {} (popup:{})".format(row_cnt, recall_cate, recall_model, recall_biz_name, recall_type, recall_regdate, popup_link))

        if str(recall_url).find("selectBbsNttView.do") > -1: # 소비자위해감시시스템
            recall_uid = func_user.getparse(recall_url,'key=','&') + "_" + func_user.getparse(recall_url,'bbsNo=','&') + "_" + func_user.getparse(recall_url,'nttNo=','&').strip()
            recall_kbn = '2'
        elif  str(recall_url).find("ajax/recallBoard") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'recallUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("ajax/fRecallBoard") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'recallUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("certUid=") > -1: # 제품안전정보센터
            recall_uid = func_user.getparse(recall_url,'certUid=','').strip()
            recall_kbn = '1'
        elif  str(recall_url).find("certNum=") > -1: # 제품안전정보협회
            recall_uid = func_user.getparse(recall_url,'certNum=','').strip()
            recall_kbn = '3'
        elif str(recall_url) == "-":
            print(">> No recall_url : {}".format(recall_url))
        else:
            print(">> No recall_url !! Check Please : {}".format(recall_url))
            func_user.procLogSet(db_FS, gProc_no, "E", "0", " recall_url Check : "+str(recall_url))

        print(">> Recall [{}] {} | {}".format(recall_uid, recall_certNum, recall_url))
        if recall_uid == "":
            row_cnt = row_cnt + 1
            print(">> No recall_uid !! Check Please : {}".format(recall_url))
            continue
        time.sleep(1)

        sql = " select isnull(freeship_ck,''), isnull(proc_flg,'') from recall_kpsanews where recall_uid = '{}'".format(recall_uid)
        rowF = db_FS.selectone(sql)
        if not rowF:
            print(">> DB Insert : {}".format(recall_uid))
            iSql = " insert into recall_kpsanews \
                (recall_uid,recall_kbn,recall_cate,recall_model,recall_biz_name,recall_type,recall_regdate,recall_url,recall_img) \
                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')\
                ".format(recall_uid,recall_kbn,recall_cate[:200],recall_model[:500],recall_biz_name[:500],recall_type[:200],recall_regdate,recall_url[:200],recall_img[:200])
            db_FS.execute(iSql)
            freeship_ck = ""
            proc_flg = ""
        else:
            freeship_ck = rowF[0]
            proc_flg = rowF[1]
            print(">> recall_kpsanews (DB 존재) : {} | freeship_ck : {} | proc_flg : {} ".format(recall_uid, freeship_ck, proc_flg))

        if proc_flg == "1":
            print(">> 이미 완료된 건 ( Skip ) : {}".format(recall_uid))
        else:
            if popup_link.find('freeship.co.kr') == -1:
                uSql = " update recall_kpsanews set freeship_ck = '0', proc_flg = '1', updatedate = getdate() where recall_uid = '{}'".format(recall_uid)
                db_FS.execute(uSql)
                print(">> recall_kpsanews : {} ( 위해제품 판매자정보 없음 완료 처리 ) ".format(recall_uid))
                # print(">> uSql: {} ".format(uSql))
            else:
                proc_work_2(db_FS, browser, row_cnt, recall_uid, recall_biz_name, popup_link)

        row_cnt = row_cnt + 1

    db_FS.close()
    print(">> proc_cnt (전체리스트) : {} | upd_cnt (문의사항 완료) : {} | sold_cnt (판매불가 완료) : {} ".format(len(sp_tmpList), upd_cnt, sold_cnt))
    func_user.procLogSet(db_con, gProc_no, "P", upd_cnt, " 위해상품 (전체:"+str(len(sp_tmpList))+"|문의완료:"+str(upd_cnt)+"|판매불가:"+str(sold_cnt)+")")
    return "0"

if __name__ == '__main__':

    upd_cnt = 0
    sold_cnt = 0
    print('>> http://kpsanews.kr recall goods proc (recall 해당상품 --> 프리쉽 상품 판매불가 처리) ')
    print('>> [--- main start ---] ' + str(datetime.datetime.now()))

    func_user.procLogSet(db_con, gProc_no, "S", "0", " Start kpsanews recall ")

    now_url = "http://kpsanews.kr/"
    # browser = connectDriver('kpsanews.kr')
    try:
        browser = func_user.connectDriverNew(now_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    browser.set_window_size(1700, 1040)
    browser.set_window_position(50, 0, windowHandle='current')
    browser.implicitly_wait(3)

    # 리콜제품 온라인 유통현황
    proc_main_1(browser, "1")

    time.sleep(2)

    # 위해제품 온라인 유통현황
    proc_main_2(browser, "2")

    func_user.procLogSet(db_con, gProc_no, "F", "0", " End kpsanews recall ")
    print('>> [--- main End ---] ' + str(datetime.datetime.now()))
    time.sleep(5)
    browser.quit()

