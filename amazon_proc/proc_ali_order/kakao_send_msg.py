import sys
import requests
import json
import datetime
import sys,os
import DBmodule_FR
db_FS = DBmodule_FR.Database("freeship")

now = datetime.datetime.now()
def get_new_token_v1():
    auth_server_url = "https://bizmsg-web.kakaoenterprise.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(inOrderNo, inIuid, msg, phone):

    token = get_new_token_v1()
    test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/message/send"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    template_code = "norder1"
    sender_no = "18005086"
    cid_key = "cid_key"

    if phone != "":
        print(">> ")
        ordername = "주문팀"
        orderno = "M0000"
        phone_number = str(phone).replace('-','').strip()
        message = msg
        sms_message = message
        message_type = "SM"
        sms_type = "SM"
    else:
        sql = "select dbo.GetCutStr(GoodsTitle,80,'...') as GTitle,OrdName,OrdMobile,OrderNo,o.OrdTel from t_order as o inner join T_ORDER_INFO as i on o.uid = i.OrderUid where i.uid = '{}'".format(inIuid)
        row_data = db_FS.selectone(sql)
        title = row_data[0]
        ordername = row_data[1]
        phone_number = row_data[2]
        orderno = row_data[3]
        OrdTel = row_data[4]
        if phone_number == "" or phone_number is None:
            phone_number = OrdTel.replace("-","")
        message = "[FREESHIP]"+str(ordername)+" 고객님 주문하신 상품 "+str(title)+" 해외현지 주문 완료 되었습니다.\n최대한 빠르고 안전하게 배송해드리겠습니다. 감사합니다."
        sms_message = message
        message_type = "AT"
        sms_type = "LM"

    #---------------------------------------
    ###phone_number = "01090467616"
    #---------------------------------------
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
            ('{}','{}','{}','{}','{}',getdate(),'adminauto','{}','{}','{}')".format(ordername,phone_number,rtn_uid,result_code,result_message,template_code,message,orderno)
        print(">> iSql : {} ".format(iSql))
        db_FS.execute(iSql)


OrderNo = "MF222085998843"
infouid = "812543"
sms_send_kakao_proc_new(OrderNo, infouid, "슬라이드 해제 테스트 tes", "01090467616")


input("Key:")

