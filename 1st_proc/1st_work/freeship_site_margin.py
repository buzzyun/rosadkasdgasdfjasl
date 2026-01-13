
import os
import socket
import json
import datetime, time
import requests
from datetime import date, timedelta
from logging.config import dictConfig
import logging
import DBmodule_FR

nowTime = str(datetime.datetime.now())
log_file_name = 'debug_'+nowTime.replace(' ','_').replace(':','')+'.log'
print("log_file_name : {}".format(log_file_name))

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': log_file_name,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

def write_log(msg):
    logging.debug(msg)

def procLogSet(db_FS, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

# 파싱함수
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

def get_new_token_v1():
    auth_server_url = "https://web1.dktechinmsg.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

# 카카오톡 전송
def sms_send_kakao_proc_new(db_FS, msg, phone):
    token = get_new_token_v1()
    test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    sender_no = "18005086"
    cid_key = "cid_key"
    template_code = "rserv6"
    phone_number = phone

    message = "[FREESHIP]프리쉽 고객님 \n▶상품명 : 주문내역\n▶주문번호 : M00000000000\n▶주문진행 관련 안내 : " + str(msg) + "\n▶전화상담 : 1800-5086 (상담가능시간 주중 오전9시30분~오후4시30분)"
    message_type = "AT"
    sms_type = "LM"
    sms_message = message

    param_date = {'client_id': 'C000000440','sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17','message_type': message_type,'message': message
    ,'cid': cid_key,'phone_number': phone_number,'template_code': template_code,'sender_no': sender_no,'sms_message':sms_message, 'sms_type':sms_type,'title': '주문관련 안내'}

    jsonString = json.dumps(param_date, indent=4)
    api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
    if api_call_response.status_code !=200:
        print(">> error ")
    else:
        result = json.loads(api_call_response.text)
        rtn_uid =  result['uid']
        rtn_status_code =  result['kko_status_code']
        rtn_code = result['code']
        rtn_message = result['message']
        print(">> rtn_status_code : {} | rtn_message : {}".format(rtn_status_code, rtn_message))
        if rtn_code == "API_200" or rtn_status_code == "0000": 
            result_code = "200"
            result_message = "OK"
        else:
            result_code = rtn_code
            result_message = rtn_message

        iSql = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent, orderno) values\
            ('{}','{}','{}','{}','{}',getdate(),'auto','{}','{}','{}')".format("프리쉽",phone_number,rtn_uid,result_code,result_message,template_code,message,"M00000000000")
        print(">> iSql : {} ".format(iSql))
        db_FS.execute(iSql)

    return result_code

if __name__=='__main__':

    print('[ Freeship Site Margin Check Start ] ' + str(datetime.datetime.now()))
    today = date.today()
    yesterday = date.today() - timedelta(1)
    print("(처리기준) 날짜 : ",yesterday)

    proc_name = "freeship_site_margin"
    currIp = socket.gethostbyname(socket.gethostname())
    db_FS = DBmodule_FR.Database("freeship")
    procLogSet(db_FS,proc_name, "S", "0", "프리쉽 사이트별 마진 : " + str(currIp))
    change_msg = ""
    write_log("프리쉽 사이트별 마진 Log Start")

    update_chk = 0

    # 68번 ep2 DB freeship_site_margin_log 테이블에 기준날짜 and flag = '1' 데이터 가져오기 
    db_ep2 = DBmodule_FR.Database("naver_ep2")
    sql_ep = "select sitecate, margin, idx from freeship_site_margin_log where regdate = convert(varchar(10), getdate() - 1, 120) and flag = '1' "
    print("sql_ep : {}".format(sql_ep))
    rows_ep = db_ep2.select(sql_ep)
    if not rows_ep:
        log_msg = "{}일 마진 변경 내역이 없습니다. ".format(yesterday)
        print(log_msg)
        write_log(log_msg)
    else:
        log_msg = "{}일 마진 변경 리스트 : {} 개".format(yesterday, len(rows_ep))
        print(log_msg)
        write_log(log_msg)
        print("------------------------------------------------------")
        for row_ep in rows_ep:
            site = row_ep[0]
            margin = int(row_ep[1])
            ep_idx = row_ep[2]
            print("[{}] margin : {} | (ep_idx : {}) ".format(site, margin, ep_idx))
            write_log("[{}] margin : {} | (ep_idx : {}) ".format(site, margin, ep_idx))
            # 194 사이트 마진변경이 있을경우, 194 사이트 T_COUPON 변경처리 
            sql_194 = "select Discount, Uid from T_COUPON where isUse = 'T' and kind = '1' and sitecate = '{}'".format(site)
            row_194 = db_FS.selectone(sql_194)
            if row_194:
                curr_194_Discount = int(row_194[0])
                uid_194 = row_194[1]
                log_msg = ">> (194) [{}] | curr_194_Discount : {} | uid_194 : {}".format(site, curr_194_Discount, uid_194)
                print(log_msg)
                if int(margin) == int(curr_194_Discount):
                    print(">> [{}] 마진 변경 없음 : {} | {}".format(site, margin, curr_194_Discount))
                    write_log(">> [{}] 마진 변경 없음 : {} | {}".format(site, margin, curr_194_Discount))

                    sqlu_ep = "update freeship_site_margin_log set flag = null where idx = '{}'".format(ep_idx)
                    print(">> sqlu_ep (flag = null 처리) : {}".format(sqlu_ep))
                    write_log(">> [{}] sqlu_ep : {}".format(site, sqlu_ep))
                    db_ep2.execute(sqlu_ep)

                else: # 마진 변경 적용
                    print(">> (194) Update ")
                    sqlu_194 = "update T_COUPON set Discount = '{}' where uid = '{}'".format(margin, uid_194)
                    print(">> sqlu_194 : {}".format(sqlu_194))
                    procLogSet(db_FS,proc_name, "P", "0", "(194 T_COUPON) Update - site: {} margin: {} -> {} ".format(site, curr_194_Discount, margin))
                    write_log(">> [{}] sqlu_194 : {}".format(site, sqlu_194))
                    db_FS.execute(sqlu_194)

                    # 변경되었는지 검증 
                    sqlu_194_chk = "select Discount, Uid from T_COUPON where isUse = 'T' and kind = '1' and sitecate = '{}'".format(site)
                    row_194_chk = db_FS.selectone(sqlu_194_chk)
                    if row_194_chk:
                        after_194_Discount = row_194_chk[0]
                        print(">> 194 Discount 변경 확인 : [{}] {} ".format(site, after_194_Discount))
                        if int(margin) == int(after_194_Discount):
                            print(">> 194 Discount 변경 OK ")
                            update_chk = 1
                            change_msg = change_msg + "\n (194) [{}] {} -> {}".format(site, curr_194_Discount, margin)
                            write_log(">> [{}] 194 Discount 변경 OK : {}".format(site, after_194_Discount))

                    # 해당 사이트 마진변경이 있을경우, 해당 사이트 T_COUPON 변경처리 
                    db_gdb = DBmodule_FR.Database(site)
                    print(">> ({}) Site Open ".format(site))
                    sql_site = "select Discount from T_COUPON where isUse = 'T' and kind = '1' and cuid = '{}'".format(uid_194)
                    row_site = db_gdb.selectone(sql_site)
                    if row_site:
                        curr_site_Discount = int(row_site[0])
                        print(">> (사이트) [{}] | curr_site_Discount : {} ".format(site, curr_site_Discount))
                        if int(margin) != int(curr_site_Discount):
                            print(">> (사이트) Update ")
                            sqlu_site = "update T_COUPON set Discount = '{}' where isUse = 'T' and kind = '1' and cuid = '{}'".format(margin, uid_194)
                            print(">> sqlu_site : {}".format(sqlu_site))
                            procLogSet(db_FS, proc_name, "P", "0", "(사이트별 T_COUPON) Update - site: {} margin: {} -> {} ".format(site, curr_site_Discount, margin))
                            write_log(">> [{}] sqlu_site : {}".format(site, sqlu_site))
                            db_gdb.execute(sqlu_site)

                            sql_site_chk = "select Discount from T_COUPON where isUse = 'T' and kind = '1' and cuid = '{}'".format(uid_194)
                            row_site_chk = db_gdb.selectone(sql_site_chk)
                            if row_site_chk:
                                after_site_Discount = row_site_chk[0]
                                print(">> 사이트 변경 확인 : [{}] {} ".format(site, after_site_Discount))
                                if int(margin) == int(after_site_Discount):
                                    print(">> 사이트 Discount 변경 OK ")
                                    update_chk = 1
                                    change_msg = change_msg + "\n (사이트) [{}] {} -> {}".format(site, curr_site_Discount, margin)
                                    write_log(">> 사이트 Discount 변경 OK : {}".format(after_site_Discount))

                    db_gdb.close()

                    if update_chk == 1:
                        sqlu_ep = "update freeship_site_margin_log set flag = null where idx = '{}'".format(ep_idx)
                        print(">> sqlu_ep (flag = null 처리) : {}".format(sqlu_ep))
                        write_log(">> [{}] sqlu_ep : {}".format(site, sqlu_ep))
                        db_ep2.execute(sqlu_ep)
        print("------------------------------------------------------")
    db_ep2.close()

    # 변경사항이 있을경우 카카오톡 전송처리
    if update_chk == 1:
        phone_list = ['01090467616','01083160955']
        #phone_list = ['01090467616']
        message = "\n * 프리쉽 사이트 마진 관련 Update 수행 " + change_msg
        for eaPhone in phone_list:
            if eaPhone.strip() != "":
                print(">> sms_send_kakao_proc_new : {}".format(eaPhone))
                rtn_code = sms_send_kakao_proc_new(db_FS, message, eaPhone)
                time.sleep(2)
                if str(rtn_code) != "200":
                    procLogSet(db_FS,proc_name, "E", "0", "카카오톡 발송 에러 : " + str(eaPhone))
                else:
                    write_log(">> kakao send Ok : {} ".format(eaPhone))

    procLogSet(db_FS,proc_name, "F", "0", "프리쉽 사이트별 마진 : " + str(currIp))
    db_FS.close()
    print('[ Freeship Site Margin Check End ] ' + str(datetime.datetime.now()))
    write_log("프리쉽 사이트별 마진 Log End")
    time.sleep(300)
    os._exit(0)
