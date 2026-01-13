import datetime
import time
import DBmodule_FR

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(db_ep, goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)

    return "0"

if __name__ == '__main__':
    print(str(datetime.datetime.now()))
    db = DBmodule_FR.Database('taobao')
    db_ep = DBmodule_FR.Database('naver_ep2')

    proc_flg = "0"
    cnt = 0
    selno = input(">>sel sql no :")
    while proc_flg == "0":
        cnt = cnt + 1
        if selno == "1":
            sql = " select top 100 uid, GoodsCode, RegDate, UpdateDate from t_goods where stop_update is null and UpdateDate is null and RegDate >= '2024-02-05 00:00:00' and RegDate < '2024-02-23 14:25:00'  and IsDisplay = 'T' and naver_in = '1' and move_flg = '1' "
        elif selno == "2":
            sql = "select top 100 uid, GoodsCode, RegDate, UpdateDate from t_goods where stop_update is null and UpdateDate is not null and UpdateDate >= '2024-02-05 00:00:00' and UpdateDate < '2024-02-23 14:25:00' and IsDisplay = 'T' and naver_in = '1' and move_flg = '1' "

        rows = db.select(sql)
        if not rows:
            print(">> 대상 없음 end ")
            proc_flg = "1"
            break

        tmpUid = ""
        for row in rows:
            guid = row[0]
            goodscode = row[1]
            RegDate = row[2]
            UpdateDate = row[3]
            print("[{}] {} ({}) | {} | {}".format(cnt, goodscode, guid, RegDate, UpdateDate))
            proc_ep_insert(db_ep, goodscode, "D")

            if guid != "":
                if tmpUid == "":
                    tmpUid = tmpUid + "'" + str(guid) + "'"
                else:
                    tmpUid = tmpUid + ",'" + str(guid) + "'"

        if tmpUid != "":
            tmpUid = " (" + tmpUid + ")"
            sqlu = "update t_goods set move_flg = 2 where uid in {}".format(tmpUid)
            print(">> sqlu : {}".format(sqlu))
            db.execute (sqlu)

        time.sleep(3)

    print(">> Proc End ")

    db_ep.close()
    db.close()
    time.sleep(5)
    print(str(datetime.datetime.now()))
