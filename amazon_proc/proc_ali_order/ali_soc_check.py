import requests

def soc_check(soc_no, rcvname, rcv_phone):
    # soc_no = "P170022320762"
    # rcvname2 = "김유진"
    rcv_phone = str(rcv_phone).replace("-","").strip()
    rtnFlg = "1"
    setrurl = "https://unipass.customs.go.kr:38010/ext/rest/persEcmQry/retrievePersEcm?crkyCn=i240e230d172r106b010b060y0&persEcm=" + soc_no + "&pltxNm=" + rcvname + "&cralTelno=" + rcv_phone
    #param = {'text': word, 'options': 4}
    source_code = requests.get(setrurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    if source_code.status_code == 200:
        if str(source_code.text).find('<tCnt>1</tCnt>') > -1:
            rtnFlg = "0"
        else:
            rtnFlg = "1"
            print(">> source_code.text : {}".format(source_code.text))

    return rtnFlg

rtn = soc_check("P712145073431","최지영","010-4517-0545")
print(rtn)