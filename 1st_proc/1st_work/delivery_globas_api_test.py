import os
import json,requests
import socket
import datetime
from datetime import date, timedelta
import DBmodule_FR
import func_user
import delivery_globas_source


if __name__ == '__main__':

    print('>> globas Delivery Get ')
    ip = socket.gethostbyname(socket.gethostname())
    gProc_no = "DEV_GLOBAS_GET"
    in_taobaoId = "de"
    db_con = DBmodule_FR.Database('freeship')
    upd_cnt = 0

    
    member_id = 'allinmarket'
    secret_key = 'zgdlFgjqYlkt3LWSkP4V'

    # 글로바스 주문서 등록 -> 500에러 
    # api_url = "http://www.globas.co.kr/openapi/orderupdate.php"
    # param_date = { "apikey": "zgdlFgjqYlkt3LWSkP4V", "mb_id": "allinmarket", "od_type": "s", "od_warehouse": "bk", "od_custom_type": "1"
    #               , "od_b_name": "김찬우", "od_b_eng_name": "KIM CHANU", "od_pnum": "P170019478678", "od_b_hp": "010-8452-7897", "od_b_nzip": "28401"
    #               , "od_b_addr1": "충청북도 청주시 흥덕구 가경로 100-20 (가경동, 삼일 원앙 아파트)", "od_b_addr2": "104동 1102호", "od_memo": "문 앞에 놓아주세요"
    #               , "partner_od_id": "302-1508633-6464348"
    #               , "it_name": ["THE GOODFELLAS Smile Duo Set Orange Empire Shaving Soap Aftershave 250ML"]
    #               , "it_name_local": ["THE GOODFELLAS Smile Duo Set Orange Empire Shaving Soap Aftershave 250ML"]
    #               , "ct_price_usd": ["20.73"], "ct_price_eur": ["19.02"], "ct_qty": ["1"], "ct_od_num": ["M2411122812NOH"]
    #               , "ct_url": ["http://www.amazon.de/dp/B08P8RX82J"], "ct_website": ["http://www.amazon.de"]
    #               , "ct_brand": ["."], "ct_color": [""], "ct_size": [""], "hs_code": ["711790"]
    #               }

    # param_date = { "apikey": "zgdlFgjqYlkt3LWSkP4V", "mb_id": "allinmarket", "od_type": "s", "od_warehouse": "bk", "od_custom_type": "1"
    #               , "od_b_name": "김찬우", "od_b_eng_name": "KIM CHANU", "od_pnum": "P170019478678", "od_b_hp": "010-8452-7897", "od_b_nzip": "28401"
    #               , "od_b_addr1": "충청북도 청주시 흥덕구 가경로 100-20 (가경동, 삼일 원앙 아파트)", "od_b_addr2": "104동 1102호", "od_memo": "문 앞에 놓아주세요"
    #               , "partner_od_id": "302-1508633-6464348"
    #               , "it_name": "THE GOODFELLAS Smile Duo Set Orange Empire Shaving Soap Aftershave 250ML"
    #               , "it_name_local": "THE GOODFELLAS Smile Duo Set Orange Empire Shaving Soap Aftershave 250ML"
    #               , "ct_price_usd": "20.73", "ct_price_eur": "19.02", "ct_qty": "1", "ct_od_num": "M2411122812NOH"
    #               , "ct_url": "http://www.amazon.de/dp/B08P8RX82J", "ct_website": "http://www.amazon.de"
    #               , "ct_brand": ".", "ct_color": "", "ct_size": "", "hs_code": "711790"
    #               }

    # jsonString = json.dumps(param_date, indent=4)
    # res = requests.post(api_url, data=jsonString)
    # if res.status_code == 200:
    #     #print(">> res: {}".format(res))
    #     result_json = json.loads(res.text)
    #     if str(result_json['result']) != "success":
    #         print(">> res fail: {}".format(result_json['result']))
    #     else:
    #         print(">> result_json : {}".format(result_json))


    # 글로바스 주문서 수정 -> text OK
    api_url = "http://www.globas.co.kr/openapi/ordermodify.php"
    member_id = 'allinmarket'
    secret_key = 'zgdlFgjqYlkt3LWSkP4V'
    
    od_id = "2411110053"
    name="육현옥"
    eng_name="YUK HYEONOK"
    soc_no = "P190014297919"
    phone = "010-4160-2162"
    post = "15642"
    addr1 = "경기도 안산시 단원구 영전로 8-7 (대부동동)"
    addr2 = "전원주택 "
    ordmemo = ""
    ali_orderno = "M2411092624A7C"

    param_date = { "apikey": "zgdlFgjqYlkt3LWSkP4V", "mb_id": "allinmarket", "od_id": od_id, "od_warehouse": "bk", "od_custom_type": "1"
                  , "od_b_name": name, "od_b_eng_name": eng_name, "od_pnum": soc_no, "od_b_hp": phone, "od_b_nzip": post
                  , "od_b_addr1": addr1, "od_b_addr2": addr2, "od_memo": ordmemo
                  , "partner_od_id": ali_orderno
                  }

    # jsonString = json.dumps(param_date, indent=4)
    # res = requests.post(api_url, data=jsonString)
    # if res.status_code == 200:
    #     #print(">> res: {}".format(res))
    #     result_json = json.loads(res.text)
    #     if str(result_json['result']) != "success":
    #         print(">> res fail: {}".format(result_json['result']))
    #     else:
    #         print(">> result_json : {}".format(result_json))




  # 글로바스 상품 수정 -> text OK
    api_url = "http://www.globas.co.kr/openapi/cartmodify.php"
    member_id = 'allinmarket'
    secret_key = 'zgdlFgjqYlkt3LWSkP4V'
    
    od_id = "2411110053"
    name="육현옥"
    eng_name="YUK HYEONOK"
    soc_no = "P190014297919"
    phone = "010-4160-2162"
    post = "15642"
    addr1 = "경기도 안산시 단원구 영전로 8-7 (대부동동)"
    addr2 = "전원주택 "
    ordmemo = ""
    ali_orderno = "M2411092624A7C"

    param_date = { "apikey": "zgdlFgjqYlkt3LWSkP4V", "mb_id": "allinmarket", "od_id": od_id, "od_warehouse": "bk", "od_custom_type": "1"
                  , "od_b_name": name, "od_b_eng_name": eng_name, "od_pnum": soc_no, "od_b_hp": phone, "od_b_nzip": post
                  , "od_b_addr1": addr1, "od_b_addr2": addr2, "od_memo": ordmemo
                  , "partner_od_id": ali_orderno
                  }

    # jsonString = json.dumps(param_date, indent=4)
    # res = requests.post(api_url, data=jsonString)
    # if res.status_code == 200:
    #     #print(">> res: {}".format(res))
    #     result_json = json.loads(res.text)
    #     if str(result_json['result']) != "success":
    #         print(">> res fail: {}".format(result_json['result']))
    #     else:
    #         print(">> result_json : {}".format(result_json))



    # http://imp.allinmarket.co.kr/admin/goods/freeship/order_delivery/globas_tracking_proc.asp


    db_con.close()
    print(">> ")