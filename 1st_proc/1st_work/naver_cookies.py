import datetime
import os, random
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
    print("\n>>===========================================")
    print('>> 네이버 쿠키값 가져오기 Start :' + str(now))
    in_page = ""

    now_url = 'https://center.shopping.naver.com/login'
    proc_id = ""
    try:
        proc_id, mainDriver = func_user.connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    mainDriver.get(now_url)
    mainDriver.set_window_size(1400, 1000)
    mainDriver.implicitly_wait(3)    
    time.sleep(5)

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

    # 상품관리 버튼 클릭
    aGoodsbtn = mainDriver.find_element(By.LINK_TEXT,'상품관리')
    aGoodsbtn.click()
    #print('>> 상품관리 버튼 클릭 Ok')
    time.sleep(3)

    # 상품현황 및 관리 버튼 클릭
    aGoods2btn = mainDriver.find_element(By.LINK_TEXT,'상품현황 및 관리')
    aGoods2btn.click()
    #print('>> 상품현황 및 관리 버튼 클릭 Ok')
    time.sleep(4)

    # 삭제 상품 버튼 클릭
    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/deleted/list.nhn')
    #print('>> 삭제 상품 page Ok')
    time.sleep(4)

    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/deleted/list.nhn')
    print('>> 삭제 상품 page Ok')

    pMainSoup = mainDriver.page_source
    procDic = dict()
    procList = []
    procCnt = 0
    titCnt = 0
    if str(pMainSoup).find('delResnList') > -1:
        mainSoup = func.getparse(str(pMainSoup), 'delResnList', 'previousCursorState')
        spMainSoup = mainSoup.split('class="tit_cate"')
        for ea_mainitem in spMainSoup:
            ea_reason = func.getparse(str(ea_mainitem), '<strong>', '</strong>').strip()
            ea_delcnt = func.getparse(str(ea_mainitem), '<span>', '</span>').strip()
            if ea_delcnt == "":
                pass
                #print('>>[{}] (SKIP) : {} '.format(titCnt, ea_reason))
            else:
                if ea_reason == "중복상품":
                    print('>>[{}] {} | (상제상품수) : {} '.format(titCnt, ea_reason, ea_delcnt))
                    procList.append([])
                    procList[procCnt].append(titCnt)
                    procList[procCnt].append(ea_reason)
                    procList[procCnt].append(ea_delcnt)
                    procCnt = procCnt + 1

            procDic[titCnt] = ea_reason
            titCnt = titCnt + 1
        # print(">> procCnt : {}".format(procCnt))
        time.sleep(2)
        for pItem in procList:
            print("pItem : {}".format(pItem))
            del_cnt = str(pItem[2]).replace(",","").strip()
            #abtn = mainDriver.find_elements(By.CSS_SELECTOR,'tit_cate')[pItem[0]]
            abtn = mainDriver.find_element(By.CSS_SELECTOR,'#delResnList > li:nth-child('+str(pItem[0])+') > div > h5')
            abtn.click()
            print('>>{} Click'.format(pItem[1]))

            time.sleep(random.uniform(1.5, 2.5))
            #print('time.sleep(2)')

            if int(del_cnt) > 1:
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
                        if goodscodeN != "":
                            url = "https://adcenter.shopping.naver.com/product/manage/product_detail.nhn?mallPid=" + str(goodscodeN)
                            mainDriver.get(url)
                            time.sleep(5)
                            result = mainDriver.page_source
                            if result != "":
                                print(">> Ok Break ")
                                break

        # 쿠키 가져오기
        cookies=mainDriver.get_cookies()
        naver_cookie=""
        for cookie in cookies[:-1]:
            naver_cookie=naver_cookie+cookie["name"]
            naver_cookie=naver_cookie+"="
            naver_cookie=naver_cookie+cookie["value"]
            naver_cookie=naver_cookie+";"
        naver_cookie=naver_cookie+cookies[-1]["name"]+"="+cookies[-1]["value"]
        print(">> naver_cookie get ")

        # naver_cookie DB Update    
        if naver_cookie != "":
            sqlu = "update cookie_list set cookie = '{}', updatedate=getdate() where proc_id = 'naver'".format(naver_cookie)
            #print(">> sqlu : {}".format(sqlu))
            db_FS.execute(sqlu)
            print(">> naver cookie DB Update ")

    time.sleep(1)
    print('>> 네이버 쿠키값 가져오기 End : ' + str(now))

    try:
        db_FS.close()
        mainDriver.quit()
        #print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        #print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    print(">>===========================================\n")
    os._exit(0)