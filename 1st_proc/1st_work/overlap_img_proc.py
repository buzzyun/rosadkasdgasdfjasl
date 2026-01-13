import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
import subprocess
import os
import datetime
import webbrowser
import DBmodule_FR
import func
import func_user


def procLogSet(db_FS, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

if __name__ == '__main__':
    now = datetime.datetime.now()

    print('>> 작업 완료 (중복이미지 삭제시작) :' + str(now))
    db_FS = DBmodule_FR.Database('freeship')
    procLogSet(db_FS, "over_lap_img", "S", "0", " 중복이미지 삭제완료 삭제 시작 ")

    time.sleep(2)
    print('time.sleep(2)')
    del_cnt = 0
    ###################################
    sitedir = "mini"
    site = "1"
    fdate = "2024-12-20"
    ###################################
    db_con = DBmodule_FR.Database(sitedir)

    work_chk = ""
    sql = "select top 1 group_no from a_TEMP_IMG where sitecate = '{}'".format(sitedir)
    row_main = db_con.selectone(sql)
    if not row_main:
        print(">> No data ")
        work_chk = "0"
    else:
        work_chk = "1"
        group_no = row_main[0]

        sql2 = "select ali_no from a_TEMP_IMG where sitecate = '{}' and group_no = '{}'".format(sitedir, group_no)
        rows = db_con.select(sql2)
        if rows:
            all_tmp_ali_no = ""
            for row in rows:
                ali_no = row[0]
                if all_tmp_ali_no == "":
                    all_tmp_ali_no = "'" + str(ali_no) + "'"
                else:
                    all_tmp_ali_no = all_tmp_ali_no + "," + "'" + str(ali_no) + "'"

            sql3 = "select uid,isnull(naver_in,0),goodscode,ali_no,price, isnull(order_ck,'') from t_goods where IsDisplay = 'T' and ali_no in ("+str(all_tmp_ali_no)+") order by price asc"
            rows_goods = db_con.select(sql3)
            row_cnt = 0
            if rows_goods:
                for row_goods in rows_goods:
                    guid = row_goods[0]
                    naver_in = row_goods[1]
                    goodscode = row_goods[2]
                    ea_ali_no = row_goods[3]
                    price = row_goods[4]
                    order_ck = row_goods[5]

                    if row_cnt == 0:
                        print(">> [low price] ({}) [{}] goodscode: {} naver_in : {} | price : {} | order_ck : {}".format(row_cnt, ea_ali_no, goodscode, naver_in, price, order_ck))
                    else:
                        print(">> [loverlap] ({}) [{}] goodscode: {} naver_in : {} | price : {} | order_ck : {}".format(row_cnt, ea_ali_no, goodscode, naver_in, price, order_ck))
                        if str(naver_in) == "1":
                            sql4 = "select goodscode from naver_del where goodscode = '{}'".format(goodscode)
                            row_chk = db_con.selectone(sql4)
                            if not row_chk:
                                sql_ins = "insert into naver_del (goodscode) values('{}')".format(goodscode)
                                print(">> sql_ins : {}".format(sql_ins))
                                db_con.execute(sql_ins)

                        sql_ups = "update t_goods set Del_Naver=1 where uid = '{}'".format(guid)
                        print(">> sql_ups : {}".format(sql_ups))
                        db_con.execute(sql_ups)
                        del_cnt = del_cnt + 1

                    row_cnt = row_cnt + 1

        sql_del = "delete from a_TEMP_IMG where sitecate = '{}' and group_no = '{}'".format(sitedir, group_no)
        print(">> sql_del : {}".format(sql_del))
        db_con.execute(sql_del)   

    if work_chk != "":
        sql5 = "select count(*) as cnt from a_TEMP_IMG sitecate = '{}'".format(sitedir)
        print(">> sql5 : {}".format(sql5))
        temp_row = db_con.selectone(sql5)   
        if temp_row[0] == 0:
            ############ DB confirm_goods = null처리
            sel_sql = " select count(*) as db_cnt from t_goods where RegDate < '" +str(fdate)+ "' and confirm_goods='1' "
            row_db_cnt = db_con.selectone(sel_sql)
            confirm_cnt = row_db_cnt[0]
            if confirm_cnt > 0:
                db_up_sql = " update t_goods set confirm_goods=null where RegDate < '" +str(fdate)+ "' and confirm_goods='1' "
                print(">> db_up_sql : {}".format(db_up_sql))
                db_con.execute(db_up_sql)


    time.sleep(3)
    now = datetime.datetime.now()
    print('>> 작업 완료 (중복이미지 삭제완료) :' + str(now))
    procLogSet(db_FS, "over_lap_img", "F", "0", " 중복이미지 삭제완료 삭제 종료 ")

    db_FS.close()
    os._exit(0)
