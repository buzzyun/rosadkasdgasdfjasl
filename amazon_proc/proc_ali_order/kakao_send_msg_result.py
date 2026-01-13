import sys
import requests
import json
import datetime
import time
import os
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon 
import DBmodule_FR

# def getSendResultAll(token):
#     test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/info/message/results"
#     api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

#     api_call_response = requests.get(test_api_url, headers=api_call_headers)
#     #print(api_call_response)

#     sendResult = json.loads(api_call_response.text)
#     print(">> sendResult : {}".format(sendResult))

def get_new_token():

    auth_server_url = "https://bizmsg-web.kakaoenterprise.com/v1/oauth/token"
    client_id = 'C000000440'
    client_secret = 'C000000440_BxgTAnthSdSiwK13yJ7eYg'
    token_req = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url, data=token_req, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        #sys.exit(1)

    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def getSendResult(token, cmid, uid, db_FS):

    test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/info/message/search/detail/"+cmid+"?client_id=C000000440"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

    api_call_response = requests.get(test_api_url, headers=api_call_headers)
    sendResult = json.loads(api_call_response.text)
    #print(">> sendResult : {}".format(sendResult))

    if sendResult['code'] == "API_200":
        print(">> code = 200 ")
        result_message_after = ""
        result_code_after = ""
    else:
        result_message_after = ""
        result_code_after = ""
        if sendResult['result']['status_code']:
            kko_status_code = sendResult['result']['kko_status_code']
            req_sms_yn = sendResult['result']['req_sms_yn']
            status_code = sendResult['result']['status_code']
            sms_status_code = ""
            req_sms_date = ""
            if req_sms_yn == "Y" and kko_status_code != "3018":
                sms_status_code = sendResult['result']['sms_status_code'] 
                req_sms_date = sendResult['result']['req_sms_date']
            print(">> [{}] [{}] [{}] [{}] ".format(req_sms_yn, status_code, sms_status_code, req_sms_date))
            
            if status_code == "API_200" and req_sms_yn == "Y" and sms_status_code == "-100":
                result_message_after = " : LMS 전송 OK (" + sms_status_code + " : " + req_sms_date + ")"
                result_code_after = "200"
            elif status_code == "API_202" and req_sms_yn == "Y":
                result_message_after = " : LMS 전송중 (" + sms_status_code + " : " + req_sms_date + ")"
                result_code_after = "API_202"
            else:
                result_message_after = " : LMS 전송 실패 (" + sms_status_code + ")"
                result_code_after = status_code       
        else:
            result_message_after = " : 확인불가 합니다. 직접 확인해 주세요."
            result_code_after = status_code

    if result_code_after != "":
        sql = "update T_KAKAOALIM_LOG set result_code_after = '" + str(result_code_after) + "', result_message_after = '" + result_message_after +  "' where uid = '" + str(uid) + "'"
        db_FS.execute(sql)      
        print(">> DB Update : {}".format(result_message_after))


if __name__ == '__main__':
    
    now = datetime.datetime.now()
    print('>> [--- main Proc start ---] ' + str(now))
    token = get_new_token()
    print(">> token : {} ".format(token))

    db_FS = DBmodule_FR.Database("freeship")
    sql = "select top 100 uid, ordername, ordermobile, cmid, ordername from T_KAKAOALIM_LOG where result_code <> '200' and result_code_after is null and cmid <> '' and senddate > '2022-11-14 00:00:00' order by senddate desc "
    rows = db_FS.select(sql)

    if not rows:
        print(">> 대상 데이터가 없습니다. ")

    for row in rows:
        uid = row[0]
        ordermobile = row[2]
        cmid = row[3]
        ordername = row[4]
        cmid_rep = cmid.replace(' ','+')
        print(">>---------------------------") 
        print("\n>> ({}) {} | {}".format(uid, ordermobile, cmid_rep))
        time.sleep(1)
        if ordername == "주문팀" or cmid_rep == "":
            continue
        getSendResult(token, cmid_rep, uid, db_FS)

    db_FS.close()
    os._exit(0)
