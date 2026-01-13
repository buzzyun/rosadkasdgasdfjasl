import sys
import requests
import json

##    function to obtain a new OAuth 2.0 token from the authentication server
##
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

## 	obtain a token before calling the API for the first time
token = get_new_token()
print(">> token : {} ".format(token))

test_api_url = "https://bizmsg-web.kakaoenterprise.com/v2/send/kakao"
api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

param_date = {'client_id': 'C000000440'
,'sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17'
,'message_type': 'AT'
,'message': "[FREESHIP]김유진고객님의 주문(상품명:테스트111)이 정상적으로 취소되었습니다.감사합니다."
,'cid': 'cid_key'
,'phone_number': '01090467616'
,'template_code': 'cancel1'
,'sms_message': 'sms test'
,'sms_type': 'SM'
,'sender_no': '01092215086'
,'fall_back_yn':True
}

api_call_response = requests.get(test_api_url, headers=api_call_headers, data=param_date)
print(api_call_response)

input("Key:")

