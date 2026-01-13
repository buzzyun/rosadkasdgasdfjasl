import time
import os
import datetime
import chromedriver_autoinstaller
from selenium import webdriver
import socket
import webbrowser
import sys
import func_user
import DBmodule_FR

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

if __name__=='__main__':

    now = datetime.datetime.now()
    print('\n [--- main Proc Start (신용카드 누락건 재생성 처리) ---] ' + str(now))
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe %s"
    cur_Ip = socket.gethostbyname(socket.gethostname())
    procLogSet("miss_order_proc", "S", "0", "신용카드 누락건 처리 : (" +str(cur_Ip)+ ") ")

    proc_List = []

    # 신용카드 누락건 조회
    sql = "select orderno,ordname,ordmobile,regdate,soc_no, OrderMemo from t_order as o left outer join t_order_info as i on o.uid = i.OrderUid where o.State = '200' and i.uid is null and payway not in ('Coupang','NaverPay')"
    rows = db_FS.select(sql)

    if not rows:
        print(" 신용카드 누락건이 없습니다. ")
    else:

        for row in rows:
            orderno = row[0]
            ordname = row[1]
            ordmobile = row[2]
            orddate = row[3]
            soc_no = row[4]
            OrderMemo = row[5]

            sqlm = "select orderno from miss_order_log where orderno = '" + str(orderno) + "'"
            row_m = db_FS.selectone(sqlm)
            if not row_m:
                # miss_order_log 로그 추가 
                sqli = "insert into miss_order_log (orderno,ordername,orderphone,orderdate,soc_no,OrderMemo,order_kbn) values('{}','{}','{}','{}','{}','{}','1')".format(orderno, ordname, ordmobile, orddate,soc_no, OrderMemo)
                db_FS.execute(sqli)
                procLogSet("miss_order_proc", "P", "0", " 주문 (상세)누락건 기존 로그 추가 (" +str(orderno)+ ") ")

            proc_List.append(orderno)

        try:
            browser = func_user.connectDriverNew("https://freeship.co.kr", "")
        except Exception as e:
            try:
                browser = func_user.connectDriverOld("https://freeship.co.kr", "")
            except Exception as e:
                print('예외가 발생 (종료) : ', e)
                os._exit(1)
        else:
            print('connectDriver Ok ')
        time.sleep(2)
        
        for ord_no in proc_List:
            print(">> proc OrderNo : {}".format(ord_no))
            sqlL = "SELECT LGD_OID FROM T_PAY_TRY_MOBILE WHERE LGD_OID = '{}'".format(ord_no)
            rowL = db_FS.selectone(sqlL)
            if not rowL:
                procLogSet("miss_order_proc", "E", "0", " 주문(상세) 누락건 T_PAY_TRY_MOBILE 내역 없음 (" +str(ord_no)+ ") ")
            else:
                print(">> T_PAY_TRY_MOBILE : {} 존재 ".format(ord_no))

                procLogSet("miss_order_proc", "P", "0", " 주문(상세) 누락건 기존 주문내역 삭제 (" +str(ord_no)+ ") ")
                sqld = "DELETE FROM T_ORDER where OrderNo = '{}'".format(ord_no)
                print(">> 기존 주문내역 삭제 : {}".format(sqld))
                db_FS.execute(sqld)

                run_url = "http://freeship.co.kr/mobile/LGU/input_payres_cart.asp?LGD_OID="+ord_no
                print(">> 주문내역 재생성 : {}".format(run_url))
                browser.get(run_url)
                time.sleep(4)

                # chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
                # webbrowser.get(chrome_path).open_new(run_url)
                # time.sleep(5)

                procLogSet("miss_order_proc", "F", "0", " 주문(상세) 누락건 실행완료 (" +str(ord_no)+ ") ")
                time.sleep(1)
                db_soc_no = ""
                sqls = "select o.uid, i.uid, soc_no, isnull(AdminMemo,'') from t_order as o inner join t_order_info as i on o.uid = i.OrderUid where orderno = '{}'".format(ord_no)
                rowS = db_FS.selectone(sqls)
                if rowS:
                    oUid = rowS[0]
                    iUid = rowS[1]
                    db_soc_no = rowS[2]
                    db_adminmemo = rowS[3]
                    if not rowS:
                        print(">> 주문생성 실패 ")
                        procLogSet("miss_order_proc", "F", "0", " 주문(상세) 누락건 주문생성 실패 (" +str(ord_no)+ ") ")
                        sqlu = " update miss_order_log set chk_flg = '0', chk_date = getdate() where orderno = '{}'".format(ord_no)
                        db_FS.execute(sqlu)      
                        time.sleep(1)
                    else:
                        print(">> 주문생성 OK ")
                        sqlu = " update miss_order_log set chk_flg = '1', chk_date = getdate() where orderno = '{}'".format(ord_no)
                        db_FS.execute(sqlu)
                        procLogSet("miss_order_proc", "F", "0", " 주문(상세) 누락건 주문생성 OK (" +str(ord_no)+ ") ")

                        adminmemo = ""    
                        adminmemo = db_adminmemo + " " + str(now)[:19] + " 주문(상세) 누락건 주문 재생성 완료 ( " + str(ord_no) + " ) " 
                        sqlu2 = " update t_order set AdminMemo = '{}' where orderno = '{}'".format(adminmemo, ord_no)
                        db_FS.execute(sqlu2)
                        print(">> AdminMemo Update OK ")
                        time.sleep(1)

        browser.quit()
    time.sleep(2)

    sql = "select top 10 l.orderno, isnull(l.soc_no,''), isnull(t.soc_no,''), chk_flg, chk_date from miss_order_log as l inner join t_order as t on l.orderno = t.OrderNo order by procdate desc"
    rows_log = db_FS.select(sql)
    for row in rows_log:
        db_orderno = row[0]
        log_soc_no = row[1].replace('None','')
        order_soc_no = row[2].replace('None','')
        chk_flg = row[3]
        chk_date = row[4]
        set_adminmemo = ""

        if chk_flg == "2": # 누락건 수동생성의 경우 어드민 메모 수정
            sql_q = "select isnull(AdminMemo,'') from t_order where regdate > '2022-09-29 00:00:00' and orderno = '{}'".format(db_orderno)
            rowQ = db_FS.selectone(sql_q)
            if rowQ:
                db_adminmemo = rowQ[0]
                if str(db_adminmemo).find('누락건') == -1:
                    set_adminmemo = ""
                    if len(db_adminmemo) == "":
                        set_adminmemo = db_adminmemo + " " + str(chk_date)[:19] + " 주문누락건 주문 수동생성 ( " + str(db_orderno) + " ) " 
                    else:
                        set_adminmemo = db_adminmemo + " / " + str(chk_date)[:19] + " 주문누락건 주문 수동생성 ( " + str(db_orderno) + " ) " 
                    sql_q2 = " update t_order set AdminMemo = '{}' where orderno = '{}'".format(set_adminmemo, db_orderno)
                    db_FS.execute(sql_q2)
                    print(">> admin memo 수동생성 Update : {}".format(db_orderno))

        if str(log_soc_no) != "" and str(log_soc_no) != str(order_soc_no):
            sql_l = " update t_order set soc_no = '{}' where orderno = '{}'".format(log_soc_no, db_orderno)
            db_FS.execute(sql_l)
            procLogSet("miss_order_proc", "F", "0", " 신용카드 누락건 통관번호 Update OK (" +str(db_orderno)+ ") ")

    db_FS.close()
    view_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/miss_order_page.asp"
    
    print(">> 신용카드 누락건 리스트 : {}".format(view_url))
    ##webbrowser.get(firefox_path).open_new(view_url)
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s"
    #webbrowser.get(chrome_path).open_new(view_url)
    webbrowser.open_new_tab(view_url)

    print('\n [--- main Proc End ---] ' + str(now))
    time.sleep(30)
    os._exit(0)