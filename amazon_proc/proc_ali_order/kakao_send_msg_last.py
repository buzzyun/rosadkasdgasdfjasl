import sys
import requests
import json
import datetime

now = datetime.datetime.now()
strnow = str(now)[:19].replace(' ','_').replace(':','').replace('-','') 

def get_new_token_v1():
    auth_server_url = "https://bizmsg-web.kakaoenterprise.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)

    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

token = get_new_token_v1()

test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/message/send"
api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

# contact / cancel1 / sold1 / norder1 / rserv7
template_code = "contacinfonew"
# message = """[FREESHIP] 기유진 고객님
# 문의 주신 내용은 대량구매관련 문의가 아니라 따로 답변이 어렵습니다.
# 상품 관련 문의나 기타 문의는 1:1친절상담이나
# 고객센터(1800-5086)로 문의바랍니다.
# 감사합니다.
# """

message = """[매스플렛폼] 김유진 고객님 
문의 주신 제품의 견적서를 전송 드리오니
검토하시어 안전하고 편리한 구매 되시길 바랍니다.

[견적내용]
▶상품명 : 상품제목테스트 상품제목테스트 상품제목테스트 상품제목테스트상품제목테스트 상품제목테스트상품제목테스트 상품제목테스트edwkkej q3ikejdjedjdjsjsjkdjfcjdhshdhfhdhdhjdkdkkdkdkdkddkk
▶수량 : 2개
▶제품단가 : 10,000원
▶부가세 : 1,000원
▶견적가 : 100,000원

[안내사항]
매스플렛폼의 대량구매는 견적된 금액 외에 추가로 금액이 발생 되지 않습니다.
배송기간 : 평균 영업일 기준 약 7~25일 소요
(담당자) 070-4763-7770
(이메일) contact@freeship.co.kr
"""

sender_no = "18005086"
phone_number = "01090467616"
sms_message = message
cid_key = str(sender_no) + '_' + str(strnow)
sms_title = "test"

url_mobile = "https://baby.freeship.co.kr/goods/content.asp?guid=7524548&cate=0"
url_pc = "https://baby.freeship.co.kr/goods/content.asp?guid=7524548&cate=0"

#buttonArray = [{ "name": "상품확인", "type": "웹링크", "scheme_android": "", "scheme_ios": "", "url_mobile": url_mobile, "url_pc": url_pc, "chat_extra": "", "chat_event": "", "plugin_id": "", "relay_id": "", "oneclick_id": "", "product_id": "", "target": "" }]
buttonArray = [{ "name": "상품확인", "type": "WL", "scheme_android": "", "scheme_ios": "", "url_mobile": url_mobile, "url_pc": url_pc, "chat_extra": "", "chat_event": "", "plugin_id": "", "relay_id": "", "oneclick_id": "", "product_id": "", "target": "" }]

param_date = {'client_id': 'C000000440','sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17','message_type': 'AT','message': message
,'cid': cid_key,'phone_number': phone_number,'template_code': template_code,'sender_no': sender_no,'sms_message':sms_message
,'sms_type':'LM' ,'title': sms_title, 'button': buttonArray }
print(">> param_date : {} ".format(param_date))

jsonString = json.dumps(param_date, indent=4)
api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
if api_call_response.status_code !=200:
    print(">> error ")
else:
    result = json.loads(api_call_response.text)
    rtn_uid =  result['uid']
    rtn_cid =  result['cid']
    rtn_code = result['code']
    rtn_message = result['message']
    print(">> result : {} ".format(result))

input("Key:")

