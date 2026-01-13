import datetime
import os
import time
import sys
import DBmodule_FR
import am_JP_del

global ver
ver = "3.00"
print('>> ver : '+str(ver))

### del_naver = '4' (regdate 6개월 이상인 데이터 재등록한 기존데이터 삭제처리 ) 인 데이터 주문체크후 주문이력 없을경우 삭제처리 (del_naver = '4' 10일 지난건 삭제 )

def checkSql(db_con, sql1, sql2):
    rtn_flg = "0"
    rs_row = db_con.select(sql1)
    print('>> ##select all## in_sql1 :' + str(sql1))
    if not rs_row:
        print('>> 삭제 대상 sql1 데이터 없음 : ' + str(datetime.datetime.now()))
        rtn_flg = "1"
        if sql2 != "":
            rs_row2 = db_con.select(sql2)
            print('>> ##select all## in_v :' + str(sql2))
            if not rs_row2:
                print('>> 삭제 대상 sql2 데이터 없음 : ' + str(datetime.datetime.now()))
                rtn_flg = "1"
            else:
                rtn_flg = "0"

    return rtn_flg

# ep 실행여부 체크 : reset = 'T' --> 삭제 불가 / reset = 'F' 삭제 가능
def checkEpMode(db_fs):
    rtn_flg = "0"
    sql = "select reset from naver_del_reset where flag = 'ep'"
    rs_row = db_fs.selectone(sql)
    print('>> sql :' + str(sql))
    if rs_row:
        resetFlg = rs_row[0]
        print('>> resetFlg : {}'.format(resetFlg))
        if resetFlg == "T":
            rtn_flg = "1" # 삭제 불가

    return rtn_flg

if __name__ == '__main__':
    print(str(datetime.datetime.now()))

    db_FS = DBmodule_FR.Database('freeship')
    if checkEpMode(db_FS) == "1":
        print('>> 삭제 불가상태 (EP 실행중) 종료 ')
        db_FS.close()
        os._exit(1)      

    site_list = ['usa','mall','global','best','de','uk']
    for site in site_list:
        print("\n\n>>>>>>>>> [{}] ----------------------- ".format(site))
        db_am = DBmodule_FR.Database(site.upper())

        if checkEpMode(db_FS) == "1":
            print('>> 삭제 불가상태 (EP 실행중) 종료 ')
            db_am.close()
            break

        pgKbn = "del_naver4"
        #########################################################################
        sql = " select pgFilename, pgName, target_sql1, isnull(target_sql2,''), isnull(target_sql3,'') from python_version_manage where name = '{}'".format(pgKbn)
        rs = db_am.selectone(sql)
        if not rs:
            print(" pgKbn 값을 확인하세요 : {} ".format(pgKbn))
            print(" Main End : " + str(datetime.datetime.now()))

        else:
            pgSite = site
            pgFilename = str(rs[0]).strip()
            pgName = str(rs[1]).strip()
            sql1 = str(rs[2]).replace("`","'")
            sql2 = str(rs[3]).replace("`","'")

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"

        if pgName is None or pgName == "":
            pgName = pgKbn

        if sql1 == "":
            print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
            time.sleep(30)
            continue

        if checkSql(db_am, sql1, sql2) == "1":
            print('>> 삭제 대상이 없습니다 (exit) : ' + str(datetime.datetime.now()))
            time.sleep(30)
            continue

        flg_multi = am_JP_del.set_del_naver4_delete(db_am, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2)
        if flg_multi == "E":
            print(" 주문 내역 확인 Exception ERROR (Exit) ")
            break           

        db_am.close()

    print(" Main End : " + str(datetime.datetime.now()))
    db_FS.close()
    os._exit(0)






