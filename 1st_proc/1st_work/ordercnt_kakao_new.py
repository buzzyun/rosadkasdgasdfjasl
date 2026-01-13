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


# def my_send_kakao_proc(msg, phone):
#     #print('>> [--- my 카카오톡 전송 start ---] ' + str(datetime.datetime.now()))
#     MSG = msg
#     FAILED_MSG = msg[:13]
#     #print(MSG)
#     #print(FAILED_MSG)

#     ordname = "프리쉽"
#     PHONE = "01090467616"
#     #PHONE = str(phone).replace('-','').strip()
#     CALLBACK = "18005086"
#     TEMPLATE_CODE = "rserv6"
#     FAILED_TYPE = "SMS"
#     FAILED_SUBJECT = "sendmsg"

#     site = "freeship"
#     name = "프리쉽"
#     orderno = "M0000000000"
#     content = msg
#     MSG = "[{}]{} 고객님 \n▶주문번호 : {}\n▶주문진행 관련 안내 : {}\n▶전화상담 : 1800-5086 (상담가능시간 주중 오전10시~오후5시)".format(site,name,orderno,content)

#     url = "http://api.apistore.co.kr/kko/1/msg/1stplatform"
#     params = {'PHONE': PHONE, 'CALLBACK': CALLBACK, 'MSG': MSG, 'TEMPLATE_CODE': TEMPLATE_CODE,'FAILED_TYPE': FAILED_TYPE, 'FAILED_MSG': FAILED_MSG, 'FAILED_SUBJECT': FAILED_SUBJECT}
#     headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','x-waple-authorization': 'ODE3NC0xNTI0NDU5NzIwNDU3LTNmZTU0YWM0LTA0ZTItNGQ3My1hNTRhLWM0MDRlMjJkNzMyNw=='}

#     resultStr = ""
#     webpage = requests.post(url, data=params, headers=headers)
#     soupNm = BeautifulSoup(webpage.content, "html.parser")
#     resultStr = soupNm.text
#     #print('>> resultStr : ' + str(resultStr))

#     result_code = getparse(resultStr, '"result_code":"', '"')
#     result_message = getparse(resultStr, '"result_message":"', '"')
#     cmid = getparse(resultStr, '"cmid":"', '"')
#     ori_MSG = MSG.replace("'", "")

#     sql_ins = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent) values ('" + ordname + "','" + PHONE + "','" + cmid + "','" + result_code + "','" + result_message + "',getdate(),'" + "freeship" + "','auto','" + ori_MSG + "')"
#     #print('>> sql_ins : ' + str(sql_ins))
#     db_FS.execute(sql_ins)
#     print(">> 카톡전송 (T_KAKAOALIM_LOG) : {}".format(PHONE))

#     #print('>> [--- my 카카오톡 전송 end ---] ' + str(datetime.datetime.now()))
#     return "0"

def get_new_token_v1():
    #auth_server_url = "https://web1.dktechinmsg.com/v1/oauth/token"
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
    #test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
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

## https://www.koreaexim.go.kr/ir/HPHKIR055M01  (네이버로그인-본부장님 (연락처:유진)) # 현재환율 API : vxBZ81mNOIP8twd3Ny4jBMLb05JyfhEO  (재발급일 : 2024.07.03)
# def get_exrate(rate_unit):
#     # * authkey : 인증키  / searchdate : 검색요청날짜 ex) 2015-01-01, 20150101, (DEFAULT)현재일 /  data : 검색요청API타입 AP01 : 환율, AP02 : 대출금리, AP03 : 국제금리
#     # * RESULT : 
#     #    - 조회 결과 1 : 성공, 2 : DATA코드 오류, 3 : 인증코드 오류, 4 : 일일제한횟수 마감
#     #    - CUR_UNIT : 통화코드 / CUR_NM : 국가 통화명 / TTB : 전신환(송금) 받으실때 / TTS : 전신환(송금) 보내실때 / DEAL_BAS_R : 매매 기준율
#     # https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=vxBZ81mNOIP8twd3Ny4jBMLb05JyfhEO&searchdate=20220927&data=AP01

#     openApiKey = "vxBZ81mNOIP8twd3Ny4jBMLb05JyfhEO"
#     weekday = datetime.today().weekday()
#     if weekday == 0:
#         yesterday = date.today() - timedelta(3)
#         print(">> 월요일의 경우 (금요일 환율): {}".format(yesterday))
#     elif  weekday == 6:
#         yesterday = date.today() - timedelta(2)
#         print(">> 일요일의 경우 (금요일 환율): {}".format(yesterday))
#     elif  weekday == 5:
#         yesterday = date.today() - timedelta(1)
#         print(">> 토요일의 경우 (금요일 환율): {}".format(yesterday))
#     else:
#         yesterday = date.today() - timedelta(1)
#         print(">> 기준일 (하루전) : {}".format(yesterday))

#     procDate = yesterday.strftime('%Y-%m-%d')
#     procDate = str(procDate)[:10].replace("-","").strip()
#     url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=" +str(openApiKey)+ "&searchdate=" +str(procDate)+ "&data=AP01"

#     result_rate = "0"
#     try:
#         result = requests.get(url)
#         time.sleep(2)
#     except Exception as e:
#         print(">> requests (www.koreaexim.go.kr) : {}".format(e))
#         return "E"
#     else:
#         time.sleep(2)
#         if result.status_code == 200:
#             json_object = json.loads(result.text)
#             json_string = json.dumps(json_object)
#             # print(json_string)
#             result_tmp = getparse(str(json_string), '"cur_unit": "'+str(rate_unit)+'"', '"bkpr"')
#             result_tmp = getparse(str(result_tmp), '"deal_bas_r":', '').replace(",","").replace("'","").replace('"','').strip()
#             # result_tmp = getparse(str(json_object), "cur_unit': '" +str(rate_unit)+ "'", "'bkpr'")
#             # result_tmp = getparse(str(result_tmp), "'deal_bas_r':", "").replace(",","").replace("'","").strip()
#             if result_tmp == "":
#                 return "0"
#             result_rate = round(float(result_tmp))
#             return result_rate
#         else:
#             return "E"


def get_exrate_new():
    time.sleep(random.uniform(1,2))
    # * authkey : 인증키  / searchdate : 검색요청날짜 ex) 2015-01-01, 20150101, (DEFAULT)현재일 /  data : 검색요청API타입 AP01 : 환율, AP02 : 대출금리, AP03 : 국제금리
    # * RESULT : 
    #    - 조회 결과 1 : 성공, 2 : DATA코드 오류, 3 : 인증코드 오류, 4 : 일일제한횟수 마감
    #    - CUR_UNIT : 통화코드 / CUR_NM : 국가 통화명 / TTB : 전신환(송금) 받으실때 / TTS : 전신환(송금) 보내실때 / DEAL_BAS_R : 매매 기준율
    # https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=vxBZ81mNOIP8twd3Ny4jBMLb05JyfhEO&searchdate=20220927&data=AP01

    json_string = ""
    openApiKey = "vxBZ81mNOIP8twd3Ny4jBMLb05JyfhEO"
    weekday = datetime.today().weekday()
    if weekday == 0:
        yesterday = date.today() - timedelta(3)
        print(">> 월요일의 경우 (금요일 환율): {}".format(yesterday))
    elif  weekday == 6:
        yesterday = date.today() - timedelta(2)
        print(">> 일요일의 경우 (금요일 환율): {}".format(yesterday))
    elif  weekday == 5:
        yesterday = date.today() - timedelta(1)
        print(">> 토요일의 경우 (금요일 환율): {}".format(yesterday))
    else:
        yesterday = date.today() - timedelta(1)
        print(">> 기준일 (하루전) : {}".format(yesterday))

    procDate = yesterday.strftime('%Y-%m-%d')
    procDate = str(procDate)[:10].replace("-","").strip()
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=" +str(openApiKey)+ "&searchdate=" +str(procDate)+ "&data=AP01"
    try:
        result = requests.get(url)
    except Exception as e:
        print(">> requests (www.koreaexim.go.kr) : {}".format(e))
        #input(">> msg : ")
        return "E"
    else:
        time.sleep(random.uniform(5,7))
        if result.status_code == 200:
            json_object = json.loads(result.text)
            json_string = json.dumps(json_object)
            # print(json_string)
            return json_string
        else:
            return "E"

def get_cur_rate(json_string, rate_unit):
    result_tmp = ""
    result_tmp = getparse(str(json_string), '"cur_unit": "'+str(rate_unit)+'"', '"bkpr"')
    result_tmp = getparse(str(result_tmp), '"deal_bas_r":', '')
    result_tmp = result_tmp.replace(",","").replace("'","").replace('"','').strip()
    return result_tmp


def get_msg_rate():
    msg_rate = ""
    rateDate = date.today().strftime('%Y-%m-%d') # 오늘날짜

    # 환율 정보 api값 가져오기
    result_rate = get_exrate_new()

    if result_rate == "" or result_rate == "E":
        msg_rate = msg_rate + str("\n[ {} 기준환율 정보 없음 ] ".format(rateDate))
        return msg_rate

    # USD : 미국 달러 / EUR : 유로 / CNH : 위안화 / GBP : 영국 파운드 / JPY(100) : 일본 옌 / EUR : 프랑스 유로
    countryUnit = ['USD','CNH','GBP','JPY(100)','EUR']
    for ea_item in countryUnit:
        result_tmp = getparse(str(result_rate), '"cur_unit": "'+str(ea_item)+'"', '"bkpr"')
        rtn_rate = getparse(str(result_tmp), '"deal_bas_r":', '').replace(",","").replace("'","").replace('"','').strip()
        if rtn_rate.find('.') > -1: rtn_rate = getparse(str(rtn_rate), '', '.')
        if result_rate == "" or result_rate == "E":
            msg_rate = ""
        else:
            msg_rate = msg_rate + str("\n[ {} ] rate : {}").format(ea_item, rtn_rate)
            print(">> [ {} ] rate : {}".format(ea_item, rtn_rate))

            sql = " select top 1 * from price_set where exrate_date = '" +str(rateDate)+ "' " 
            rowO = db_FS.selectone(sql)
            if not rowO: # insert 
                sql_i = "insert into price_set select top 1 '" + str(rateDate) + "', exrate_us, exrate_jp, exrate_uk, exrate_de, exrate_cn, day_exrate_us, day_exrate_jp, day_exrate_uk, day_exrate_de, day_exrate_cn, day_updatedate, exrate_fr, day_exrate_fr from price_set order by exrate_date desc "
                print(">> sql_i : {}".format(sql_i))
                db_FS.execute(sql_i)

                sql_u = ""
                sql_u = " update price_set set day_updatedate = getdate()," 
                if ea_item == "USD":
                    sql_u = sql_u + " day_exrate_us = '" + str(rtn_rate) + "' "
                if ea_item == "CNH":
                    sql_u = sql_u + " day_exrate_cn = '" + str(rtn_rate) + "' "
                if ea_item == "GBP":
                    sql_u = sql_u + " day_exrate_uk = '" + str(rtn_rate) + "' "
                if ea_item == "JPY(100)":
                    sql_u = sql_u + " day_exrate_jp = '" + str(rtn_rate) + "' "
                if ea_item == "EUR":
                    sql_u = sql_u + " day_exrate_fr = '" + str(rtn_rate) + "' "
                sql_u = sql_u + " where exrate_date = '" + str(rateDate) + "' "

                print(">> sql_u : {}".format(sql_u))
                db_FS.execute(sql_u)

    return msg_rate


if __name__ == '__main__':

    message1 = ""
    message2 = ""
    msg_rate = get_msg_rate()

    total = 0
    amazonCnt = 0
    aliCnt = 0
    etsyCnt = 0
    refCnt = 0
    trendCnt = 0
    shopCnt = 0
    cnCnt = 0
    miniCnt = 0
    redCnt = 0

    sql = " select sitecate, count(*) from t_order as o inner join t_order_info as i on i.orderuid = o.uid where regdate >= '{} 00:00:00' and regdate < getdate()  group by sitecate ".format(now_date)
    print(">> sql : {}".format(sql))
    rows = db_FS.select(sql)
    if rows:
        for row in rows:
            ord_count = 0
            sitecate = row[0]
            ord_count = row[1]
            print(">> {} : {} ".format(sitecate, ord_count))
            total = total + ord_count

            if sitecate == 'usa' or sitecate == 'mall' or sitecate == 'global' or sitecate == 'best' or sitecate == 'uk' or sitecate == 'de':
                amazonCnt = amazonCnt + ord_count
            elif sitecate == 'mini':
                miniCnt = miniCnt + ord_count
            elif sitecate == 'cn':
                cnCnt = cnCnt + ord_count
            elif sitecate == 'handmade':
                etsyCnt = etsyCnt + ord_count
            elif sitecate == 'ref':
                refCnt = refCnt + ord_count
            elif sitecate == 'trend':
                trendCnt = trendCnt + ord_count
            elif sitecate == 'shop':
                shopCnt = shopCnt + ord_count
            elif sitecate == 'red':
                redCnt = redCnt + ord_count
            else:
                aliCnt = aliCnt + ord_count

        message1 = "\n" + str(now_datetime) + "\n----------------------------\n** 주문 총합계 : {} 건 **\n\n알리 : {} 건 \n아마존 : {} 건\n타오바오 : {} 건 \n핸드메이드 : {} 건 \n이베이 : {} 건 \n트렌드 : {} 건 \n라쿠텐 : {} 건 \n미니 : {} 건 \ntemu : {} 건 ".format(total, aliCnt, amazonCnt, cnCnt, etsyCnt, refCnt, trendCnt, shopCnt, miniCnt, redCnt)
        message1 = message1 + "\n----------------------------\n** 환율정보(전일기준) ** \n" + msg_rate
        print(message1)

        sql2 = " select GoodsCode, count(*) as orderCnt from t_order as o inner join t_order_info as i on i.orderuid = o.uid and state = '200' group by GoodsCode having count(*) > 10 "
        print(">> sql2 : {}".format(sql2))
        rows2 = db_FS.select(sql2)
        message2 = "\n---------------------------\n** 10개 이상 주문건 ** \n"
        if rows2:
            for row2 in rows2:
                ord_count = 0
                GoodsCode = row2[0]
                orderCnt = row2[1]
                message2 = message2 + "\n" + str(GoodsCode) + " : " + str(orderCnt) + " 개 "
                message2 = message2 + "\nhttp://imp.allinmarket.co.kr/admin/goods/freeship/view_goods.asp?count=1&method=goodscode&del_item1=" + str(GoodsCode)
        else:
            message2 = message2 + "\n없습니다. "
        message2 = message2 + "\n---------------------------\n"
        message2 = message2 + "** 현황 ** \n\nhttp://imp.allinmarket.co.kr/admin/goods/freeship/view_order_200_list_ordercnt.asp?selState=200"
        message2 = message2 + "\n---------------------------\n"

        message = message1 + message2
        #my_send_kakao_proc(message, "01090467616")
        
        sql = " select isnull(memo,'') from ali_order_auto_set where proc_name = 'order_kakao_phonelist' "
        print(">> sql : {}".format(sql))
        rowp = db_FS.selectone(sql)
        if rowp:
            phoneList = rowp[0]
            spPhoneList = phoneList.split('/')
            print(">> spPhoneList : {}".format(spPhoneList))
        phone_list = ['01090467616','01027809438','01051287243','01083160955','01077583791','01045296842']
        # phone_list = ['01090467616']
        for eaPhone in spPhoneList:
            if eaPhone.strip() != "":
                phone_list.append(eaPhone.strip())
                print(">> sms_send_kakao_proc_new : {}".format(eaPhone))
                sms_send_kakao_proc_new(message, eaPhone)
                time.sleep(2)

    print(">> End ")
db_FS.close()