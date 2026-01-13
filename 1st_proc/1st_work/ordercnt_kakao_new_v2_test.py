import json
import requests
import time
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import sys, os, random
import DBmodule_FR

print(">> Site DB Open : {} ".format("freeship"))
db_FS = DBmodule_FR.Database("freeship")

now_date = datetime.today().strftime("%Y-%m-%d")
now_datetime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

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
    #auth_server_url = "https://web1.dktechinmsg.com/v2/oauth/token"
    auth_server_url = "https://web1.dktechinmsg.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(msg, phone):
    token = get_new_token_v1()
    # test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
    # test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
    test_api_url = "https://web1.dktechinmsg.com/v2/send/kakao"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    sender_no = "18005086"
    template_code = "rserv6"
    phone_number = phone
    sender_key = "cid_" + str(phone_number) + "_" + str(datetime.now())[:20]
    sender_key = sender_key.replace(" ","_").strip()

    message = "[FREESHIP]프리쉽 고객님 \n▶상품명 : 주문내역\n▶주문번호 : M00000000000\n▶주문진행 관련 안내 : " + str(msg) + "\n▶전화상담 : 1800-5086 (상담가능시간 주중 오전9시30분~오후4시30분)"
    param_date = {
        'client_id': 'C000000440'
        ,'cid': 'M00000000000'
        ,'message_type': 'AT'
        ,'sender_key': sender_key
        ,'phone_number': phone_number
        ,'template_code': template_code
        ,'message': message
        ,'sender_no': sender_no
        ,'title': '주문관련 안내'
        ,'fall_back_yn': True
        ,'fall_back_message_type': 'LM'
        ,'fall_back_title': '주문관련 안내'
        ,'fall_back_message': message
    }

    jsonString = json.dumps(param_date, indent=4)
    api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
    if api_call_response.status_code !=200:
        print(">> error ")
    else:
        result = json.loads(api_call_response.text)
        rtn_uid =  result['uid']
        rtn_cid=  result['cid']
        rtn_code = result['result']['detail_code']
        rtn_message = result['result']['detail_message']
        #rtn_status_code =  result['kko_status_code']
        # rtn_code = result['code']
        # rtn_message = result['message']
        print(">> rtn_code : {} | rtn_message : {}".format(rtn_code, rtn_message))
        if rtn_code == "API_200": 
            result_code = "200"
            result_message = "OK"
        else:
            result_code = rtn_code
            result_message = rtn_message

    print(">> ")
        # iSql = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent, orderno) values\
        #     ('{}','{}','{}','{}','{}',getdate(),'auto','{}','{}','{}')".format("프리쉽",phone_number,rtn_uid,result_code,result_message,template_code,message,"M00000000000")
        # print(">> iSql : {} ".format(iSql))
        # db_FS.execute(iSql)

if __name__ == '__main__':

    message1 = ""
    sms_send_kakao_proc_new("", "01090467616")
    print(">> End ")
db_FS.close()