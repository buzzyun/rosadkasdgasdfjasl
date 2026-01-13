import time
import os
import datetime
from openpyxl import load_workbook
import pandas as pd
import sys
import DBmodule_FR

def table_proc(db_con, order_no, regdate, state, ordername, price, price_cancel, pay_kind):

    sql_k = "select orderno from miss_pay_tmp where orderno = '{}' and state = '{}'".format(order_no, state)
    row_k = db_con.selectone(sql_k)
    if row_k:
        print(">> Update Skip ")
    else:
        #print(">> Insert miss_pay_tmp")
        if price_cancel == "":
            sql = " Insert into miss_pay_tmp ( orderno, regdate, state, payname, price, pay_kind) values ('{}','{}','{}','{}','{}','{}') ".format(order_no, regdate, state, ordername, price, pay_kind)
        else:
            sql = " Insert into miss_pay_tmp ( orderno, regdate, state, payname, price, cancel_price, pay_kind) values ('{}','{}','{}','{}','{}','{}','{}') ".format(order_no, regdate, state, ordername, price, price_cancel, pay_kind)
        # print(">> sql : {}".format(sql))
        db_con.execute(sql)


def missOrderLog(db_con, order_no, regdate, pay_kind):
    # T_PAY_TRY_MOBILE 테이블에 검색
    sql_l = "select LGD_BUYER, isnull(Re_Hphone, Re_Phone), regdate, soc_no, LGD_CUSTOM_FIRSTPAY from T_PAY_TRY_MOBILE  where lgd_oid = '{}'".format(order_no)
    row_l = db_con.selectone(sql_l)
    if row_l:
        ordername = row_l[0]
        orderphone = row_l[1]
        orderdate = row_l[2]
        soc_no = row_l[3]
    else:
        ordername = ""
        orderdate = regdate
        soc_no = ""

    sql_k = "select ordername, orderphone, orderdate, isnull(soc_no,'') from miss_order_log where orderno = '{}' ".format(order_no)
    row_k = db_con.selectone(sql_k)
    if row_k:
        ordername = row_k[0]
        orderphone = row_k[1]
        orderdate = row_k[2]
        soc_no = row_k[3]
        if ordername == "":
            sql = "update miss_order_log set ordername = '" +str(ordername)+ "', orderphone = '" +str(orderphone)+ "', orderdate = '" +str(orderdate)+ "', soc_no = '" +str(soc_no)+ "', pay_kind = '" +str(pay_kind)+ "' where orderno = '" +str(order_no)+ "' "
    else:
        sql = " Insert into miss_order_log ( orderno,ordername,orderphone,orderdate,soc_no,pay_kind,order_kbn) values ('{}','{}','{}','{}','{}','{}','2') ".format(order_no, ordername, orderphone, orderdate, soc_no, pay_kind)
        print(">> sql : {}".format(sql))
        db_con.execute(sql)

def orderCheck(db_con, order_no):
    sql = "select OrderNo from t_order where OrderNo = '{}'".format(order_no)
    row = db_con.selectone(sql)
    if not row:
        return "1"

    return "0"

if __name__ == '__main__':

    print(' [--- main start ---] ' + str(datetime.datetime.now()))

    filename = input(">> 실행할 파일명 : ")
    # filename = "E:\\tmp\\1112.xlsx"
    filepath = str(filename)
    if os.path.isfile(filepath):
        print(">> 파일명 : {}".format(filepath))
    else:
        print(">> {} 파일이 없습니다. (종료) ".format(filename))
        os._exit(1)

    df_excel = pd.read_excel(filepath, engine = "openpyxl", header=0)

    wCnt = 0
    db_con = DBmodule_FR.Database('freeship')

    sql_d = "delete from miss_pay_tmp " # 임시 테이블 삭제
    print(">> 임시 테이블 삭제 : miss_pay_tmp ")
    db_con.execute(sql_d)

    if df_excel.columns[2] == "주문번호":
        for i in range(0, df_excel.shape[0]):
            wCnt = wCnt + 1
            shop_no = df_excel.iloc[i,0] # 상점아이디
            regdate = df_excel.iloc[i,1] # 결제.취소일시
            order_no = df_excel.iloc[i,2] # 주문번호
            state = df_excel.iloc[i,3] # 결제상태
            ordername = df_excel.iloc[i,6] # 입금자명
            price = df_excel.iloc[i,7] # 결제.취소액
            pay_kind = "계좌이체"
            table_proc(db_con, order_no, regdate, state, ordername, price, "", pay_kind)

            if orderCheck(db_con, order_no) == "1":
                print(">> 계좌이체 누락건 확인 필요 : {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, regdate))
                missOrderLog(db_con, order_no, regdate, pay_kind)

    elif df_excel.columns[3] == "주문번호":
        check_list = []
        for i in range(0, df_excel.shape[0]):
            wCnt = wCnt + 1
            shop_no = df_excel.iloc[i,0] # 상점아이디
            regdate = df_excel.iloc[i,1] # 결제.취소일시
            order_no = df_excel.iloc[i,3] # 주문번호
            state = df_excel.iloc[i,4] # 결제상태
            ordername = df_excel.iloc[i,5] # 구매자명
            price = df_excel.iloc[i,6] # 결제액
            price_cancel = df_excel.iloc[i,7] # 취소액
            ordername = ordername[:1] + '*' + ordername[2:]
            pay_kind = "신용카드"
            table_proc(db_con, order_no, regdate, state, ordername, price, price_cancel, pay_kind)

            if orderCheck(db_con, order_no) == "1":
                print(">> 신용카드 누락건 확인 필요 : {} | {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, price_cancel, regdate))
                check_list.append(order_no)

        print(">> check_list : {}".format(check_list))
        for check_no in check_list:
            sql = "select orderno, state from miss_pay_tmp where orderno = '{}' and pay_kind = '신용카드' group by orderno, state".format(check_no)
            rows = db_con.select(sql)
            if rows:
                if len(rows) == 2:
                    print(">> 정상 카드취소건 (Skip) : {}".format(check_no))
                    state1 = rows[0][1]
                    state2 = rows[1][1]
                else:
                    print(">> 카드 누락건 확인필요(1): {}".format(check_no))
                    missOrderLog(db_con, check_no, "", pay_kind)
            else:
                print(">> 카드 누락건 확인필요(2): {}".format(check_no))
                missOrderLog(db_con, check_no, "", pay_kind)


    elif df_excel.columns[5] == "주문번호":
        for i in range(0, df_excel.shape[0]):
            wCnt = wCnt + 1
            shop_no = df_excel.iloc[i,0] # 상점아이디
            regdate = df_excel.iloc[i,3] # 결제.취소일시
            order_no = df_excel.iloc[i,5] # 주문번호
            state = df_excel.iloc[i,6] # 결제상태
            ordername = df_excel.iloc[i,9] # 입금자명
            price = df_excel.iloc[i,10] # 결제.취소액
            pay_kind = "가상계좌"
            table_proc(db_con, order_no, regdate, state, ordername, price, "", pay_kind)

            if orderCheck(db_con, order_no) == "1":
                print(">> 가상계좌 누락건 확인 필요 : {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, regdate))
                missOrderLog(db_con, order_no, regdate, pay_kind)

    db_con.close()

    print(' [--- main End ---] ' + str(datetime.datetime.now()))
    os._exit(0)
