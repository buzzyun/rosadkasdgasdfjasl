import time
import os
import datetime
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
    print('\n [--- main Proc Start ( 탈퇴 회원 승인 처리 ) ---] ' + str(now))

    cnt = 0
    db_FS = DBmodule_FR.Database('freeship')
    # 탈퇴 요청한 최근 00개 탈퇴 승인 처리 
    sql = "SELECT top 50 M.Uid, M.UserID, MD.Reason, MD.IsAgree, MD.AgreeDate, MD.RegDate FROM T_MEMBER_DELETE AS MD JOIN T_MEMBER AS M ON MD.Uid=M.Uid where MD.IsAgree = 'F' ORDER BY MD.RegDate desc"
    rows = db_FS.select(sql)
    if not rows:
        print(">> 탈퇴 승인 요청이 없습니다. ")
    else:
        for row in rows:
            cnt = cnt + 1
            uid = row[0]
            userID = row[1]
            reason = row[2]
            isAgree = row[3]
            agreeDate = row[4]
            regDate = row[5]
            print(" [{}] userID : {} | {} | {} ( {} )  탈퇴 처리 ".format(cnt, userID, reason, regDate, uid))
            sp_sql = "EXEC spSecessionUser 'rental', '" +str(uid)+ "'"
            print(">> sp_sql : {}".format(sp_sql))
            db_FS.execute(sp_sql)

    time.sleep(3)
    procLogSet("freeship_member_del", "F", cnt, " 탈퇴 회원 승인처리 완료 ")

    time.sleep(2)
    print('\n [--- main Proc End ---] ' + str(now))
    os._exit(0)
