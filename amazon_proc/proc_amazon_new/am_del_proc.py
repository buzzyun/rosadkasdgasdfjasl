import datetime
import os
import time
import sys
import DBmodule_AM
import am_JP_del

global ver
ver = "13.01"
print('>> ver : '+str(ver))

def checkSql(db_con, sql1, sql2):
    rtn_flg = "0"
    rs_row = db_con.select(sql1)
    print('>> ##select all## in_sql1 :' + str(sql1))
    if not rs_row:
        print('>> 삭제 대상 sql1 데이터 없음 : ' + str(datetime.datetime.now()))
        rtn_flg = "1"

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

    input_Site = sys.argv[1]
    input_pgKbn = sys.argv[2]
    input_Site = str(input_Site).strip()
    input_pgKbn = str(input_pgKbn).strip()
    print(" SITE : {}".format(input_Site))
    print(" PG NAME : {}".format(input_pgKbn))

    if input_Site == "" and input_pgKbn == "":
        print(" 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(" Main End : " + str(datetime.datetime.now()))
        os._exit(1)
    if input_Site == 'best' or input_Site == 'global' or input_Site == 'mall' or input_Site == 'usa' or input_Site == 'de' or input_Site == 'uk' or input_Site == 'handmade' or input_Site == 'cn' or input_Site == 'taobao' or input_Site == 'ref' :
        pass
    else:
        print(" 사이트 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(" Main End : " + str(datetime.datetime.now()))
        os._exit(1)        

    db_FS = DBmodule_AM.Database('freeship')
    db_am = DBmodule_AM.Database(input_Site.upper())

    #########################################################################
    sql = " select pgFilename, pgName, now_url, now_url2, sitePost, siteCUR, target_sql1, isnull(target_sql2,''), isnull(target_sql3,'') from python_version_manage where name = '{}'".format(input_pgKbn)
    rs = db_am.selectone(sql)
    if not rs:
        print(" pgKbn 값을 확인하세요 : {} ".format(input_pgKbn))
        print(" Main End : " + str(datetime.datetime.now()))
        os._exit(1)            
    else:
        pgKbn = input_pgKbn
        pgSite = input_Site
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        now_url = str(rs[2]).strip()
        now_url2 = str(rs[3]).strip()
        sitePost = str(rs[4]).replace('&#8204;','').strip()
        siteCUR = str(rs[5]).strip()
        sql1 = str(rs[6]).replace("`","'")
        sql2 = str(rs[7]).replace("`","'")
        sql3 = str(rs[8]).replace("`","'")

    if pgFilename is None or pgFilename == "":
        pgFilename = "new_" + str(pgName) + ".exe"

    if pgName is None or pgName == "":
        pgName = pgKbn

    if sql1 == "":
        print(' 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        os._exit(1)

    if checkSql(db_am, sql1, sql2) == "1":
        print('>>< 삭제 대상이 없습니다 (exit) : ' + str(datetime.datetime.now()))
        time.sleep(5)
        os._exit(0)

    print(' [--- ' + str(pgName) + ' main start ---] ' + str(datetime.datetime.now()))
    print('pgName : {} | pgSite : {} | pgFilename : {} | pgKbn : {}'.format(pgName,pgSite,pgFilename,pgKbn))

    #########################################################################
    flg_m = "0"
    low_l = 0

    while flg_m == "0":
        print(">> (Main) start  : " + str(low_l) + " : " + str(datetime.datetime.now()))
        time.sleep(1)
        print('time.sleep(1)')
        if checkEpMode(db_FS) == "1":
            print('>> 삭제 불가상태 (EP 실행중) ')
            break
        flg_multi = am_JP_del.set_old_delete(db_am, pgName, pgFilename, pgKbn, pgSite, ver, sql1, sql2)
        if flg_multi == "1":
            print(' delete complete ')
            break
        elif flg_multi == "E":
            print(" 주문 내역 확인 ERROR (Exit) ")
            break           

        time.sleep(1)
        # print("time.sleep(1)")

        low_l = low_l + 1

    print(" Main End : " + str(datetime.datetime.now()))
    db_am.close()
    os._exit(0)






