# -*- coding: utf-8 -*-
import socket
from datetime import datetime
import time
import DBmodule_FR
global ver
ver = "24.11.19.v01"
print(">> ver : {}".format(ver))
def procLogSet(db_FS, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_cnt, proc_memo) values('{}','{}','{}','{}')".format(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo)
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

if __name__ == '__main__':

    print('>> ali cancel proc start ')
    print('\n [--- main start ---] ' + str(datetime.now()))
    cur_Ip = socket.gethostbyname(socket.gethostname())    
    gProc_no = "ALI_CANCEL_LIST"
    cnt = 0
    db_FS = DBmodule_FR.Database('freeship')
    procLogSet(db_FS, gProc_no, "S", "0", "(알리 취소) 실행 : " +str(cur_Ip))

    del_sql = "delete from ali_orderCancel where regdate < getdate() - 300"
    print(">> del_sql : {}".format(del_sql))
    db_FS.execute(del_sql)

    sql2 = "select getdate(), o.regdate, o.orderno, i.ali_orderno, i.ali_id, O.PAYWAY, o.naver_pay_product_code, o.coupang_orderid,  o.state, o.uid, i.uid, c.status "
    sql2 = sql2 + "from ali_orderCancel as c "
    sql2 = sql2 + "inner join t_order_info as i on i.ali_orderno = c.ali_orderNo "
    sql2 = sql2 + "inner join t_order as o on o.uid = i.OrderUid "
    sql2 = sql2 + "inner join T_ORDER_DELIVERY as d on d.uid = i.uid "
    sql2 = sql2 + "where o.state in ('201','301','421') and c.status in ('취소', '폐쇄', '종료됨')"

    rows = db_FS.select(sql2)
    for row in rows:
        cnt = cnt + 1
        regdate = row[1]
        orderNo = row[2]
        ali_orderNo = row[3]
        ali_id = row[4]
        PAYWAY = row[5]
        naver_pay_product_code = row[6]
        coupang_orderid = row[7]
        c_status = row[11]
        if c_status == "취소":
            Reason = "cancel"
        elif c_status == "폐쇄" or c_status == "종료됨":
            Reason = "closed"
        state = row[8]
        Ouid = row[9]
        luid = row[10]
        if PAYWAY == "NaverPay":
            Pay_orderno = naver_pay_product_code
        elif PAYWAY == "Coupang":
            Pay_orderno = coupang_orderid
        else:
            Pay_orderno = None

        # freeship_tracking_check 중복 체크
        # sqlC = "select OrderNo, proc_state from freeship_tracking_check where OrderNo = '{}' and ali_orderno = '{}' and Reason <> 'delivername_error'".format(orderNo, ali_orderNo)
        sqlC = "select OrderNo, proc_state from freeship_tracking_check where OrderNo = '{}' and ali_orderno = '{}'".format(orderNo, ali_orderNo)
        row0 = db_FS.selectone(sqlC)
        if row0:
            if row0[1]=="1":
                print(">> ali_orderNo : ",ali_orderNo,"ali_id : ",ali_id, "proc_state : ",row0[1], "proc_state 1 스킵")
            else:
                update_sql = "update freeship_tracking_check set RegDate = '{}', OrderNo = '{}', ali_id = '{}', PAYWAY = '{}', Pay_orderno = '{}', Reason = '{}', Ouid = '{}', InfoUid = '{}' where ali_orderno = '{}'".format(regdate, orderNo, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, luid, ali_orderNo)
                db_FS.execute(update_sql)
                print("[{}] ali_orderNo : {} | ali_id : {} | Reason : {} 업데이트 완료".format(cnt, ali_orderNo, ali_id, Reason))
        else:
            insert_sql = "insert into freeship_tracking_check(ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, InfoUid) values(getdate(), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(regdate, orderNo, ali_orderNo, ali_id, PAYWAY, Pay_orderno, Reason, Ouid, luid)
            db_FS.execute(insert_sql)
            print("[{}] ali_orderNo : {} | ali_id : {} | Reason : {} 입력 완료".format(cnt, ali_orderNo, ali_id, Reason))

    time.sleep(10)
    procLogSet(db_FS, gProc_no, "F", "0", "(알리 취소) 실행 완료 : " +str(cur_Ip))
    db_FS.close()
    print('>> ali cancel proc end ')


