import os
import json,requests
import socket,subprocess
import datetime, time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import DBmodule_FR
import func_user

def proc_run(db_con, browser, site):
    api_url = "http://www.globas.co.kr/openapi/orderview.php"
    member_id = 'allinmarket'
    secret_key = 'zgdlFgjqYlkt3LWSkP4V'

    print('>> globas Delivery get ')
    get_page(browser, 1, site)

    page_source = str(browser.page_source)
    pageTmp = func_user.getparse(page_source, '<nav class="pg_wrap">','</nav>')
    endPage = func_user.getparseR(pageTmp, '&amp;page=','class="pg_page pg_end"').replace('"','').strip()
    if endPage == "": endPage = "1"
    if int(endPage) > 35:
        endPage = 35
    endPage = int(endPage)
    idx = 0
    upd_cnt = 0
    page = 0
    while page < endPage:
        page = page + 1
        print('>> globas Delivery get (page:{})'.format(page))
        get_page(browser, page, site)
        page_source = str(browser.page_source)

        pageTmp = func_user.getparse(page_source, '<nav class="pg_wrap">','</nav>')
        itemResult = func_user.getparse(page_source, 'name="frmorderlist"','</form>')
        itemResult = func_user.getparse(itemResult, '</table>','<table>')
        sp_source = itemResult.split('onclick="od_del_click')
        for ea_itme in sp_source:
            idx = idx + 1
            ea_tmp = func_user.getparse(ea_itme,'<tr>','')
            od_id = func_user.getparse(ea_tmp,'orderinquiryview.php?od_id=','"').strip()

            if od_id == "":
                print(">> ({}) No od_id Check please ".format(idx))
                idx = idx + 1
                continue
            ali_order_no = func_user.getparse(ea_tmp,'귀사 주문번호 : ','"').strip()
            delieveyNo = func_user.getparse(ea_tmp,'expressweb.co.kr/enha"','</a>')
            delieveyNo = func_user.getparse(delieveyNo,'<u>','</u>').strip()
            if len(ali_order_no) < 19:
                sql = "select ali_orderno, orderno from t_order as o inner join t_order_info as i on i.orderUid = o.uid where o.OrderNo = '{}'".format(ali_order_no)
                row = db_con.selectone(sql)
                if row:
                    ali_order_no = row[0]

            param_date = {'apikey': secret_key, 'mb_id': member_id, 'od_id': od_id }
            jsonString = json.dumps(param_date, indent=4)
            res = requests.post(api_url, data=jsonString)
            if res.status_code == 200:
                #print(">> res: {}".format(res))
                result_json = json.loads(res.text)
                if str(result_json['result']) != "success":
                    print(">> ({}) [{}] 신청서번호 : {} | res fail: {}".format(idx, ali_order_no, od_id, result_json['result']))
                else:
                    delivery_weight = result_json['od_weight']
                    delivery_price = result_json['od_receipt_emoney']
                    od_status = result_json['od_status']

                    if od_status == '국제배송중' or od_status == '완료':
                        #ali_order_no = result_json['partner_od_id']
                        delieveyNo = result_json['od_tracking_num']
                        print(">> ({}) [{}] 신청서번호 : {} | 운송장번호 : {} | 결제금액 : {}원 |  무게: {} | {}".format(idx, ali_order_no, od_id, delieveyNo, delivery_price, delivery_weight, od_status))
                        # 송장번호 매칭 택배사명 가져오기 DeliveryUid, DeliveryName, delivery_company
                        DeliveryUid, DeliveryName, delivery_company = func_user.get_track_name(delieveyNo)
                        print(">>>> 송장번호 : " + str(delieveyNo) + " (" + str(DeliveryName) + ") [" + str(DeliveryUid) + " : " +str(delivery_company)+ "] | " + str(ali_order_no))

                        sql = "select amazon_orderno from globas_tracking where amazon_orderno = '" + str(ali_order_no) + "' "
                        row = db_con.selectone(sql)
                        if not row:
                            sql = "insert into globas_tracking (delivery_id,delicode, amazon_orderno, itemNo, pkgNo, delivery_price, item_weight) values ('" + str( DeliveryUid) + "','" + str(delieveyNo) + "','" + str(ali_order_no) + "','" + str(od_id) + "','','" + str(delivery_price) + "','" + str(delivery_weight) + "')"
                            print(">>>> Insert table : globas_tracking ")
                            upd_cnt = upd_cnt + 1
                            db_con.execute(sql)
                    else:
                        print(">> ({}) [{}] 신청서번호 : {} : {} (SKIP) ".format(idx, ali_order_no, od_id, od_status))

        time.sleep(random.uniform(2,3))

    func_user.procLogSet(db_con,gProc_no, "P", upd_cnt, ' 글로바스 (globas) 발송 내역 ('+str(site)+') : ' +str(ip))
    return upd_cnt

def login_proc(loginid, loginpass):
    print('>> globas Login ')
    proc_url = "http://www.globas.co.kr/bbs/login.php?url=%2F"
    print(">> proc_url : {}".format(proc_url))

    browser.get(proc_url)
    time.sleep(random.uniform(3,4))
    if str(browser.page_source).find('로그아웃') > -1:
        print(">> 로그인 되어있음")
        time.sleep(random.uniform(1,2))
    else:
        browser.find_element(By.ID,'login_id').send_keys(loginid)
        time.sleep(random.uniform(1,2))
        browser.find_element(By.ID,'login_pw').send_keys(loginpass)
        time.sleep(random.uniform(1,2))
        browser.find_element(By.XPATH,'/html/body/table[5]/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[3]/input').click()
        time.sleep(random.uniform(2,3))

def get_page(browser, page, site):
    if site == "de":
        base_url = "http://www.globas.co.kr/shop/order_list_bk.php"
    elif site == "uk":
        base_url = "http://www.globas.co.kr/shop/order_list_ld.php"
    elif site == "fr":
        base_url = "http://www.globas.co.kr/shop/order_list_fr.php"

    if page == 1:
        proc_url = base_url
    else:
        proc_url = base_url + "?sel_field=od_id&search=&save_search=&sort1=od_time&sort2=desc&page=" +str(page)
    print("\n\n-----------------------------------------------")
    print(">> [{}] (page:{}) {}".format(site, page, proc_url))
    browser.get(proc_url)
    time.sleep(random.uniform(4,6))

if __name__ == '__main__':

    print('>> globas Delivery Get ')
    print('\n [--- main start ---] ')
    ip = socket.gethostbyname(socket.gethostname())
    gProc_no = "DEV_GLOBAS_GET"
    in_taobaoId = "de"
    db_con = DBmodule_FR.Database('freeship')
    upd_cnt = 0

    loginid = ""
    loginpass = ""
    sql = "select login_id, login_pw from ali_order_auto_set where proc_name = 'globas'"
    row = db_con.selectone(sql)
    if row:
        loginid = str(row[0])
        loginpass = str(row[1])
        print(">> loginid : {}".format(loginid))

    time.sleep(1)
    func_user.procLogSet(db_con,gProc_no, "S", 0, ' 글로바스 (globas) -> 송장 시작 : ' +str(ip))
    proc_id = ""
    try:
        proc_id, browser = func_user.connectSubProcess()
    except Exception as e:
        try:
            browser = func_user.connectDriverOld("http://www.globas.co.kr", "S")
        except Exception as e:
            print('예외가 발생 (종료) : ', e)
            func_user.procLogSet(db_con,gProc_no, "E", "0", 'connectDriver 접속 에러 (종료)')
            time.sleep(5)
            print('>> time.sleep(5) ')
            os._exit(1)
    else:
        print('connectDriver Ok ')

    time.sleep(3)
    browser.set_window_size(1600, 1000)
    browser.implicitly_wait(3)
    time.sleep(random.uniform(1,2))

    sql = "delete from globas_tracking "
    print("Delete : " + str(sql))
    db_con.execute(sql)

    login_proc(loginid, loginpass)
    if str(browser.page_source).find('로그아웃') == -1:
        input(">> 로그인 처리후 아무숫자나 입력해 주세요 : ")
        time.sleep(2)

    site_list = ['de','uk','fr']
    for site in site_list:
        rtn_cnt = proc_run(db_con, browser, site)

    func_user.procLogSet(db_con,gProc_no, "F", 0, ' 글로바스 (globas) -> 송장 완료 : ' +str(ip))

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/globas_tracking_proc.asp"
    print(" >> Next Proc 실행 (프리쉽 송장처리 : globas_tracking_proc.asp) : " + str(run_url))
    browser.get(run_url)
    time.sleep(5)
    ##############################################
    func_user.procLogSet(db_con, gProc_no, "F", 0, ' 글로바스 (globas) -> 송장완료 : ' +str(run_url))

    db_con.close()
    print(">> time.sleep(60) ")
    time.sleep(60)
    print('\n [--- main End ---] ' + str(datetime.datetime.now()))
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)
