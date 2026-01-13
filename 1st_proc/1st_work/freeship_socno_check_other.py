import os
import time
import datetime
import requests
import random
import DBmodule_FR

# 파싱 함수
def getparse(target, findstr, laststr):
    result = ""
    if findstr:
        pos = target.find(findstr)
        if pos > -1:
            result = target[pos + len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        if lastpos > -1:
            result = result[:lastpos]
    else:
        result = result

    return result.strip()

def procLogSet(db_FS,in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

    return "0"

# def soc_check(soc_no, rcvname, rcv_phone):
#     rtnFlg = "1"
#     setrurl = "https://unipass.customs.go.kr:38010/ext/rest/persEcmQry/retrievePersEcm?crkyCn=i240e230d172r106b010b060y0&persEcm=" + soc_no.upper() + "&pltxNm=" + rcvname + "&cralTelno=" + rcv_phone
#     #param = {'text': word, 'options': 4}
#     source_code = requests.get(setrurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
#     if source_code.status_code == 200:
#         if str(source_code.text).find('<tCnt>1</tCnt>') > -1:
#             rtnFlg = "0"
#         else:
#             rtnFlg = "1"
#             print(">> source_code.text : {}".format(source_code.text))
#     else: 
#         return "E"
#     return rtnFlg

def procSocCheck_0(db_FS):
    errCnt = 0
    sql = " select o.uid, orderno, state, isnull(soc_no_chk,''), isnull(soc_no,''), RcvName, isnull(RcvMobile,''), isnull(RcvTel,''), o.regdate from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where RegDate > getdate() -10 and state = '200' and isnull(soc_no_chk,'') = '' order by o.regdate desc "
    #print('>> sql:' + str(sql))
    rows = db_FS.select(sql)
    if not rows:
        print('>> 대상이 없습니다. ')
    else:
        print(">> 대상 : {}".format(len(rows)))
        for row in rows:
            time.sleep(3)
            sql_u = ""
            Ouid = row[0]
            orderno = row[1]
            state = row[2]
            soc_no_chk = row[3]
            soc_no = row[4]
            RcvName = row[5]
            RcvMobile = row[6]
            RcvTel = row[7]
            regdate = row[8]
            soc_no_chk = str(soc_no_chk).replace(" ","").strip()
            if soc_no.find('&#160;') > -1:
                soc_no = str(soc_no).replace("p","P").replace('&#160;','').strip()
            soc_no = str(soc_no).replace("p","P").replace(" ","").strip()
            rep_soc_no = soc_no
            RcvName = str(RcvName).replace(" ","").strip()
            RcvMobile = str(RcvMobile).replace("-","").replace(" ","").strip()
            RcvTel = str(RcvTel).replace("-","").replace(" ","").strip()
            if RcvMobile == "":
                RcvMobile = RcvTel
            print(">>--------------------------------------------")
            if soc_no_chk != "1" and state == "200" and soc_no != "" and len(soc_no) == 13:
                print('>> orderno ({}) : {} | {} | {} | {} | regdate : {}'.format(Ouid, orderno, soc_no, RcvName, RcvMobile, regdate))

                ## 임시 통관번호 확인용 https://gsiexpress.com/pcc_chk.php
                rtn = soc_check_other(soc_no, RcvName, RcvMobile) 
                print(">> rtn : {} ".format(rtn))
                if rtn == "E":
                    errCnt = errCnt + 1
                    sql_u = " update t_order set soc_no_chk = 'E', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
                elif rtn == "1":
                    errCnt = 0
                    print(">> 통관번호 불일치 ")
                    sql_u = " update t_order set soc_no_chk = '0', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
                else:
                    errCnt = 0
                    print(">> 통관번호 일치 ")
                    sql_u = " update t_order set soc_no_chk = '1', soc_no_chk_date = getdate(), soc_no = '{}' where uid = '{}'".format(rep_soc_no, Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
            else:
                print(">> 통관번호 불일치 (2) ")
                print('>> orderno ({}) : {} | soc_no : {} | RcvName : {} | RcvMobile : {} | regdate : {}'.format(Ouid, orderno, soc_no, RcvName, RcvMobile, regdate))
                sql_u = " update t_order set soc_no_chk = '0', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                #print(">> sql_u : {} ".format(sql_u))
                db_FS.execute(sql_u)

            if errCnt > 3:
                print(">> 통관번호 체크 에러 (종료) ")
                return "E"

    return "0"

def procSocCheck_1(db_FS):
    errCnt = 0
    # sql = " select o.uid, orderno, state, isnull(soc_no_chk,''), isnull(soc_no,''), RcvName, isnull(RcvMobile,''), isnull(RcvTel,''), o.regdate from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where RegDate > getdate() -10 and state = '200' and isnull(soc_no_chk,'') = '' order by o.regdate desc "
    sql = " select o.uid, orderno, state, isnull(soc_no_chk,''), isnull(soc_no,''), RcvName, isnull(RcvMobile,''), isnull(RcvTel,''), o.regdate from t_order as o inner join t_order_info as i on i.OrderUid = o.uid where RegDate > getdate() -5 and state = '200' and isnull(soc_no_chk,'') = '0' order by o.regdate desc "
    #print('>> sql:' + str(sql))
    rows = db_FS.select(sql)
    if not rows:
        print('>> 대상이 없습니다. ')
    else:
        print(">> 대상 : {}".format(len(rows)))
        for row in rows:
            time.sleep(3)
            sql_u = ""
            Ouid = row[0]
            orderno = row[1]
            state = row[2]
            soc_no_chk = row[3]
            soc_no = row[4]
            RcvName = row[5]
            RcvMobile = row[6]
            RcvTel = row[7]
            regdate = row[8]
            soc_no_chk = str(soc_no_chk).replace(" ","").strip()
            if soc_no.find('&#160;') > -1:
                soc_no = str(soc_no).replace("p","P").replace('&#160;','').strip()
            soc_no = str(soc_no).replace("p","P").replace(" ","").strip()
            rep_soc_no = soc_no
            RcvName = str(RcvName).replace(" ","").strip()
            RcvMobile = str(RcvMobile).replace("-","").replace(" ","").strip()
            RcvTel = str(RcvTel).replace("-","").replace(" ","").strip()
            if RcvMobile == "":
                RcvMobile = RcvTel
            print(">>--------------------------------------------")
            if state == "200" and soc_no != "" and len(soc_no) == 13:
                print('>> orderno ({}) : {} | {} | {} | {} | regdate : {}'.format(Ouid, orderno, soc_no, RcvName, RcvMobile, regdate))

                ## 임시 통관번호 확인용 https://gsiexpress.com/pcc_chk.php
                rtn = soc_check_other(soc_no, RcvName, RcvMobile) 
                print(">> rtn : {} ".format(rtn))
                if rtn == "E":
                    errCnt = errCnt + 1
                    sql_u = " update t_order set soc_no_chk = 'E', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
                elif rtn == "1":
                    errCnt = 0
                    print(">> 통관번호 불일치 ")
                    sql_u = " update t_order set soc_no_chk = '0', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
                else:
                    errCnt = 0
                    print(">> 통관번호 일치 ")
                    sql_u = " update t_order set soc_no_chk = '1', soc_no_chk_date = getdate(), soc_no = '{}' where uid = '{}'".format(rep_soc_no, Ouid)
                    #print(">> sql_u : {} ".format(sql_u))
                    db_FS.execute(sql_u)
            else:
                print(">> 통관번호 불일치 (2) ")
                print('>> orderno ({}) : {} | soc_no : {} | RcvName : {} | RcvMobile : {} | regdate : {}'.format(Ouid, orderno, soc_no, RcvName, RcvMobile, regdate))
                sql_u = " update t_order set soc_no_chk = '0', soc_no_chk_date = getdate() where uid = '{}'".format(Ouid)
                #print(">> sql_u : {} ".format(sql_u))
                db_FS.execute(sql_u)

            if errCnt > 3:
                print(">> 통관번호 체크 에러 (종료) ")
                return "E"

    return "0"

def soc_check_other(soc_no, rcvname, rcv_phone):
    rtnFlg = "1"

    setrurl = "https://gsiexpress.com/pcc_chk.php"
    paramdata = str(rcvname) +'/'+ str(soc_no.upper()) +'/'+ str(rcv_phone)
    param = {'action_type': 'query','chk_data': paramdata}

    res = requests.post(setrurl, data=param)
    if res.status_code == 200:
        #print(">> source_code.text : {}".format(res.text))
        #print(">> source_code.status_code : {}".format(res.status_code))
        result_tmp = getparse(str(res.text), '검증결과','사용방법')
        result_tmp = result_tmp.replace('\\n','').replace('\\r','').replace('\\t\\t','')
        if result_tmp.find('>오류<') > -1:
            result_fail = getparse(str(result_tmp), '오류','</tr>')
            result_fail = getparse(str(result_fail), '<td ','</td>')
            result_fail = getparse(str(result_fail), '>','').strip()
            print(">> [{}] fail : {}".format(paramdata, result_fail))
            rtnFlg = "1"
        elif result_tmp.find('>정상<') > -1:
            print(">> [{}] 정상 ".format(paramdata))
            rtnFlg = "0"
        else:
            print(">> [{}] check please : {}".format(paramdata, result_tmp))
            rtnFlg = "1"
    else: 
        return "E"

    return rtnFlg

# 통관번호 임시 체크 (https://gsiexpress.com/pcc_chk.php) 
if __name__=='__main__':
    print('>> [--- ORDER_SOC_CHECK start ---] ' + str(datetime.datetime.now()))
    time.sleep(1)
    print('>> Proc Start ')
    db_FS = DBmodule_FR.Database('freeship')

    time.sleep(1)
    rtn_flg = procSocCheck_0(db_FS)
    if rtn_flg == "E":
        print('>> ORDER_SOC_CHECK API 에러 ')
        procLogSet(db_FS,"ORDER_SOC_CHECK", "E", "0", "ORDER_SOC_CHECK API 에러 ")

    print('>> Proc End ')
    db_FS.close()
    print('>> [--- order_check end ---] ' + str(datetime.datetime.now()))
    os._exit(0)

