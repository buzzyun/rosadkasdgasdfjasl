

import os
import time
import datetime
import requests
import sys
import DBmodule_FR

def soc_check(soc_no, rcvname, rcv_phone):
    api_key = "g210s234u056t149h070p010e0"
    rtnFlg = "1"
    setrurl = "https://unipass.customs.go.kr:38010/ext/rest/persEcmQry/retrievePersEcm?crkyCn=" +str(api_key)+ "&persEcm=" + str(soc_no).upper() + "&pltxNm=" + str(rcvname) + "&cralTelno=" + str(rcv_phone)
    #param = {'text': word, 'options': 4}
    source_code = requests.get(setrurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    if source_code.status_code == 200:
        print(">> source_code.text : {}".format(source_code.text))
        if str(source_code.text).find('<tCnt>1</tCnt>') > -1:
            rtnFlg = "0"
        else:
            rtnFlg = "1"
            print(">> source_code.text : {}".format(source_code.text))
    else: 
        return "E"
    return rtnFlg

# soc_no = "P160016064892"
# RcvName = "김수정"
# RcvMobile = "01094230618"

soc_no = "P170022320762"
RcvName = "김유진"
RcvMobile = "01090467615"

# soc_no = "P671143724487"
# RcvName = "이재혁"
# RcvMobile = "01032404497"

rtn = soc_check(soc_no, RcvName, RcvMobile) 