import requests
import re
import json
import time

#파싱 함수
def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result.strip()

# http://cross.transer.com (일본어 - 한국어 번역)
def getTranCross(word, from_country, to_country, tranId):
    result_str = ""

    url = "http://cross.transer.com/text/exec_tran" 

    tranLang = "CR-JK"
    if to_country == "en" or to_country == "us":
        tranLang = "CR-JE"
    param = {'e': tranLang, 't' : word, 'r' : '0'}

    time.sleep(1)
    try:
        req = requests.post(url, data=param, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
        if req.text:
            result = json.loads(req.text)
            result_str = getparse(str(result), "'text': '", "'")

    except Exception as ex:
        print(' cross.transer error : ', ex)
        return str(result_str)
    else:
        print(">> [tran] getTranCross")

    return str(result_str)

#www.webtran.eu
def getTranslationWebtran(word, from_country, to_country, tranId):

    result_str = ''
    if from_country == '' or from_country is None:
        from_country = 'zh-CN'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'ko'

    param = {'gfrom': from_country, 'text': word, 'gto': to_country,'key':'ABC'}
    url = "https://www.webtran.eu/gtranslate/"

    try:
        source_code = requests.post(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        if source_code.text:
            transoup = source_code.text
            state_code = len(transoup)
            if state_code > 0:
                result_str = transoup
                result_str = re.sub('<[^>]*>', '', result_str)

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)
        return ''
    else:
        print(">> [tran] getTranslationWebtran")

    return result_str

#yandex
def getTranslationYan(word, from_country, to_country, tranId):
    result_str = ''
    global db
    param = {'text': word, 'options': 4}
    if from_country == '' or from_country is None:
        from_country = 'zh'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'ko'

    tranId = str(tranId).strip()
    url = "https://translate.yandex.net/api/v1/tr.json/translate?id={0}&srv=tr-text&lang={1}-{2}&reason=paste&format=text".format(tranId, from_country,to_country)
    #url = "https://translate.yandex.net/api/v1/tr.json/translate?id={0}&srv=tr-text&lang={1}-{2}&reason=paste&format=text&yu=9488171461628832887&yum=1628832890518438905&sprvk=dD0xNjMwMzEzNTEyO2k9MjIyLjEwNC4xODkuMTg7RD1DRTIwRDhBNTYxOUVFODQyRTg5MkQ5ODdDRjRDMDhFRkY4NjAwMEZDMDExNDAxNjAxQTBENkFEMzVFQUFEMEFEO3U9MTYzMDMxMzUxMjc2NjAzMjM0MztoPTAwOTYwOGZhYzhjYWI4OTY4MDI4NGU1NGRjNDk2MmY5".format(tranId, from_country,to_country)

    time.sleep(1)
    try:
        source_code = requests.post(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        if source_code.text:
            transoup = source_code.text
            state_code = getparse(str(transoup), '"code":', ',')
            if str(state_code) == "200":
                result_str = getparse(str(transoup), '"text":["', '"')
                result_str = re.sub('<[^>]*>', '', result_str)

    except Exception as ex:
        print('에러가 발생했습니다.',ex)
        return ''
    else:
        print(">> [tran] getTranslationYan")

    return result_str


# def getTranslationFree(word, from_country, to_country, tranId):
#     result_str = ''
#     if from_country == '' or from_country is None:
#         from_country = 'auto'
#     if from_country == 'us':
#         from_country = 'en'
#     if from_country == 'jp':
#         from_country = 'ja'
#     if to_country == '' or to_country is None:
#         to_country = 'ko'
#     if to_country == 'us':
#         to_country = 'en'

#     url = "https://t1.freetranslations.org/freetranslationsorg.php?p1={0}&p2={1}&p3={2}".format(from_country,to_country,word)
#     try:
#         source_code = requests.post(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
#     except Exception as ex :
#         print('에러가 발생했습니다.',ex)
#         return ''
#     else:
#         if source_code.text:
#             transoup = source_code.text
#             state_code = len(transoup)
#             if state_code > 0:
#                 result_str = transoup
#                 result_str = re.sub('<[^>]*>', '', result_str)
#                 print(">> [tran] getTranslationFree")

#     return result_str

#카카오i
def getTranslationKakaoI(word, from_country, to_country, tranId):

    result_str = ''
    if from_country == '' or from_country is None:
        from_country = 'auto'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'kr'

    param = {'queryLanguage': from_country, 'q': word, 'resultLanguage': to_country}
    url = "https://translate.kakao.com/translator/translate.json"

    try:
        source_code = requests.post(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Referer':'https://translate.kakao.com/'})
        if source_code.text:
            state_code = len(source_code.text)
            if state_code > 0:
                transoup = json.loads(source_code.text)
                if str(transoup).find("'output': [['") > -1:
                    result_str = getparse(str(transoup), "'output': [['", "']],")
                    result_str = re.sub('<[^>]*>', '', result_str)

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)
        return ''
    else:
        print(">> [tran] getTranslationKakaoI")

    return result_str

#translate.com
def getTranslationTranslateCom(word, from_country, to_country, tranId):

    result_str = ''
    if from_country == '' or from_country is None:
        from_country = 'auto'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'ko'

    param = {'source_lang': from_country, 'text_to_translate': word, 'translated_lang': to_country,'use_cache_only':'false'}
    url = "https://www.translate.com/translator/ajax_translate"

    try:
        source_code = requests.post(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','referer':'https://www.translate.com/translator/'})
        if source_code.text:
            state_code = len(source_code.text)
            if state_code > 0:
                transoup = json.loads(source_code.text)
                if str(transoup).find("'translated_text': '") > -1:
                    result_str = getparse(str(transoup), "'translated_text': '", "',")
                    result_str = re.sub('<[^>]*>', '', result_str)

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)
        return ''
    else:
        print(">> [tran] getTranslationTranslateCom")

    return result_str

#translatedict.com
# def getTranslationTranslateDict(word, from_country, to_country, tranId):

#     result_str = ''
#     if from_country == '' or from_country is None:
#         from_country = 'auto'
#     if from_country == 'us':
#         from_country = 'en'
#     if from_country == 'jp':
#         from_country = 'ja'
#     if to_country == '' or to_country is None:
#         to_country = 'ko'
#     if to_country == 'us':
#         to_country = 'en'

#     param = {'p1': from_country, 'p3': word, 'p2': to_country}
#     url = "https://t1.translatedict.com/1.php?p1=auto&p2={1}&p3={0}".format(word,to_country)

#     try:
#         source_code = requests.get(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','referer':'https://www.translatedict.com/'})
#     except Exception as ex:  # 에러 종류
#         print('에러가 발생 했습니다', ex)
#         return ''
#     else:
#         if source_code.text:
#             transoup = source_code.text
#             if len(transoup) > 0:
#                 result_str = re.sub('<[^>]*>', '', transoup)
#                 print(">> [tran] getTranslationTranslateDict")

#     return result_str

#mymemory
def getTranslationMymemory(word, from_country, to_country, tranId):

    result_str = ''
    if from_country == '' or from_country is None:
        from_country = 'zh-CN'
    if from_country == 'us':
        from_country = 'en'
    if from_country == 'jp':
        from_country = 'ja'
    if to_country == '' or to_country is None:
        to_country = 'ko'

    param = {'langpair': from_country+'|'+to_country, 'q': word, 'mtonly': '1'}
    url = "https://mymemory.translated.net/api/ajaxfetch?q={0}&langpair={1}|{2}&mtonly=1".format(word,from_country,to_country)

    try:
        source_code = requests.get(url, data=param, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','referer':'https://mymemory.translated.net'})
        if source_code.text:
            transoup = json.loads(source_code.text)
            if str(transoup).find("'translatedText': '") > -1:
                result_str = getparse(str(transoup), "'translatedText': '", "',")
                result_str = re.sub('<[^>]*>', '', result_str)

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)
        return ''
    else:
        print(">> [tran] getTranslationMymemory")

    return result_str

def translator(word, from_country, to_country, tranId):
    #function_list = ['getTranslationYan','getTranslationWebtran','getTranslationFree', 'getTranslationKakaoI', 'getTranslationTranslateCom','getTranslationTranslateDict', 'getTranslationMymemory']
    function_list = ['getTranslationWebtran','getTranslationKakaoI', 'getTranslationTranslateCom','getTranslationMymemory','getTranslationYan']
    for translator in function_list:
        result = globals()[translator](word, from_country, to_country, tranId)
        if result != '' and result != None :
            return result

    return ""

def translator_JP(word, from_country, to_country, tranId):
    function_list = ['getTranCross','getTranslationWebtran','getTranslationYan','getTranslationKakaoI','getTranslationTranslateCom','getTranslationMymemory']
    for translator in function_list:
        result = globals()[translator](word, from_country, to_country, tranId)
        if result != '' and result != None :
            return result
    
    return ""


# aa = "大阪市中央区谷町"
# bb = translator(aa,'ja','ko','61ffbd2d.613165bd.8dce7b10.74722d74657874-2-0')
# print(bb)


# aa = "大阪市中央区谷町"
# bb = translator(aa,'ja','ko','61ffbd2d.613165bd.8dce7b10.74722d74657874-2-0')
# print(bb)