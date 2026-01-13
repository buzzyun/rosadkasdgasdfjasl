import time
import os
import datetime
import webbrowser
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
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
    print('\n [--- main Proc Start (결제 시도 세션저장 테이블 (T_ORDER_PAY_INFO) 2일전 데이터 삭제 처리) ---] ' + str(now))

    run_url = "http://imp.allinmarket.co.kr/admin/goods/freeship/delproc_ORDER_PAY_INFO.asp"
    print("procUrl : {}".format(run_url))
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open_new(run_url)
    procLogSet("delProc_OrderPayInfo", "F", "0", " 결제시도 테이블 데이터삭제 실행완료 " + str(run_url))

    time.sleep(3)

    print('\n [--- main Proc End ---] ' + str(now))
    time.sleep(2)
    os._exit(0)