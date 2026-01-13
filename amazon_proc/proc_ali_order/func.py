import datetime
import time
import os
import random
import requests
import re


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


# 파싱함수 (뒤에서 부터 찾아서 파싱)
def getparseR(target, findstr, laststr):
    if findstr:
        pos = target.rfind(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result

# mssql null


def getQueryValue(in_value):
    if in_value == None:
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

# 번역 bing
def getTranslationBing_new(word, from_country, to_country):
    result_str = ""
    if from_country == '' or from_country is None:
        from_country = 'auto-detect'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'ko'

    time.sleep(1)
    param = {'fromLang': from_country, 'text': word, 'to': to_country}
    url = "https://www.bing.com/ttranslatev3?isVertical=1&&IG=AB0612CFE6864BF898B784C2B76B60AE&IID=translator.5028.3"
    try:
        source_code = requests.post(url, data=param, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})

    except Exception as ex:
        print(' error : ', ex)
        return "1"
    else:
        transoup = source_code.text
        result_str = getparse(str(transoup), 'text":"', '"')

    return result_str

# 정규식 체크 : 특수문자/숫자/영문/한글
def regStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ', '')
    chkStr = chkStr.strip()
    regStr = re.search('[^. %–|<>&`()+A-Za-z0-9가-힣]+', chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result


# 정규식 체크 : 일본어 체크 (Katakana/Hiragana/Kanji)
def regJpStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ', '')
    chkStr = chkStr.strip()

    # 일본어(Katakana/Hiragana/Kanji)
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+", chkStr)

    if (regStr):
        result = "1"  # 일본어 포함
    else:
        result = "0"  # 일본어 없음

    return result

# 특수문자 replace
def replaceQueryString(in_word):
    result = in_word.replace("'", "`")
    result = result.replace("★", "").replace("◆", "").replace(
        "/", " | ").replace(",", " ").replace("&lt;", "<").replace("&gt;", ">")
    result = result.replace(r'\x26', ' ').replace('&amp;', ' & ').replace(
        '&AMP;', ' & ').replace('&nbsp;', ' ').replace('&NBSP;', ' ')
    result = result.replace(
        "&ndash;", "-").replace("&times;", " x ").replace("–", "-")
    result = result.replace("&#39;", "`").replace(
        "&quot;", "").replace("\\", "").replace("®", "")
    result = result.replace("【", "(").replace("】", ")").replace(
        "()", "").replace("[]", "").replace(";", "")

    return result


# 상품코드 생성 goodscode
def getGoodsCode(uid, goodshead):
    result = goodshead+str(uid).zfill(10)
    return result


# 상품 guid 가져오기 (goodscode --> guid)
def getGuid(gCode):
    rtn_guid = ""
    tmpGuid = str(gCode)[2:]
    tmpGuid = str(tmpGuid).lstrip("0")
    rtn_guid = str(tmpGuid).replace("N", "")

    return str(rtn_guid)

# 상품코드의 사이트명 가져오기
def getSiteName(gCode):
    sitename = ""
    gHead = str(gCode)[:1]
    if gHead == "G":
        sitename = "fashion"
    elif gHead == "A":
        sitename = "auto"
    elif gHead == "B":
        sitename = "beauty"
    elif gHead == "Y":
        sitename = "baby"
    elif gHead == "E":
        sitename = "electron"
    elif gHead == "F":
        sitename = "furniture"
    elif gHead == "I":
        sitename = "industry"
    elif gHead == "J":
        sitename = "jewelry"
    elif gHead == "O":
        sitename = "office"
    elif gHead == "S":
        sitename = "sports"
    elif gHead == "Q":
        sitename = "usa"
    elif gHead == "X":
        sitename = "best"
    elif gHead == "V":
        sitename = "global"
    elif gHead == "D":
        sitename = "de"
    elif gHead == "N":
        sitename = "mall"
    elif gHead == "L":
        sitename = "cn"
    elif gHead == "K":
        sitename = "uk"
    elif gHead == "H":
        sitename = "handmade"
    elif gHead == "Z":
        sitename = "red"
    elif gHead == "C":
        gHead_2 = str(gCode)[:2]
        if gHead_2 == "CG":
            sitename = "fashion2"
        elif gHead_2 == "CA":
            sitename = "auto2"
        elif gHead_2 == "CY":
            sitename = "baby2"
        elif gHead_2 == "CE":
            sitename = "electron2"
        elif gHead_2 == "CF":
            sitename = "furniture2"
        elif gHead_2 == "CI":
            sitename = "industry2"
        elif gHead_2 == "CJ":
            sitename = "jewelry2"
        elif gHead_2 == "CO":
            sitename = "office2"
        elif gHead_2 == "CS":
            sitename = "sports2"
        elif gHead_2 == "CB":
            sitename = "beauty2"

    return sitename
