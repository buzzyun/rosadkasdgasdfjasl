# -*- coding: utf-8 -*-
import datetime
import os
import random
import socket
import socks
import http.client
import urllib
from urllib.request import Request, urlopen
from stem import Signal
from stem.control import Controller
from selenium.common.exceptions import TimeoutException
from stem import Signal
from stem.control import Controller
import pyautogui
import time
import re
from dbCon import DB_shop_py


global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

global cnt_title_tran
global EX_PRICE
global gTWOCAPTCHA_API_KEY
gTWOCAPTCHA_API_KEY = "decc2c5553302ce2df33ddb9cf1f4846"

EX_PRICE = 12
EX_PRICE_US = 1300

ip = socket.gethostbyname(socket.gethostname())
#print('>> IP : '+str(ip))
#translator = googletrans.Translator()

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(currIp) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def procEnd(db_con, db_ali, in_drive, in_pg):
    time.sleep(1)
    #print(' time.sleep(1)')
    print(">> procEnd : " + str(datetime.datetime.now()))

    db_con.close()
    db_ali.close()
    in_drive.quit()
    time.sleep(2)
    os._exit(0)

def getparse(target, findstr, laststr):
    result_goods = ""
    if findstr:
        pos = target.find(findstr)
        if pos > -1:
            result_goods = target[pos + len(findstr):]
    else:
        result_goods = target
    if laststr:
        lastpos = result_goods.find(laststr)
        if lastpos > -1:
            result_goods = result_goods[:lastpos]
    else:
        result_goods = result_goods

    return result_goods.strip()

#rfind 파싱함수
def getparseR(target, findstr, laststr):
    if findstr:
        pos = target.rfind(findstr)
        result_goods = target[pos+len(findstr):]
    else:
        result_goods = target
    if laststr:
        lastpos = result_goods.find(laststr)
        result_goods = result_goods[:lastpos]
    else:
        result_goods = result_goods
    return result_goods

#중국어 찾기
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

def replaceQueryStringTitle(target) :
    result = target.replace("'","").replace("★","").replace("◆","").replace("/","|").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("【","(").replace("】",")").replace('"', '').replace("「","(").replace("」",")")
    return str(result).strip()

def getDeliveryFee(gDic, in_weight):
    deliveryFee = gDic['py_withbuy_cost']
    deliveryFee = float(deliveryFee)

    weight = in_weight
    if weight == None or weight == 0 or weight == 0.0 or weight == '' :
        pass
    else:
        if weight <= 15 :
            deliveryFee = deliveryFee + (weight*500)
        else:
            deliveryFee = (deliveryFee + 14000) + ((weight-15)*3000)

    result = deliveryFee * 2
    print(">> getDeliveryFee : {}".format(result))
    return int(round(result, -2))

def getWonpirce(gDic, price):
    dollar_exchange = float(gDic['py_dollar_exchange']) # 0.16
    won_exchange = float(gDic['py_exchange_Rate']) # 180 -> 210
    final_price = 0
    price = float(price)
    dollar_price = price * dollar_exchange
    dollar_price = abs(dollar_price)
    won_price = price * won_exchange

    db_ali2 = DB_shop_py.Database('aliexpress', True)
    sql = "select * from ali_price_ck where cate_code = 'MAIN'"
    rs = db_ali2.selectone(sql)
    db_ali2.close()
    start_arr = []
    end_arr = []
    uppr_arr = []
    add_arr = []

    for i in range(0,30):
        pre_fix = str(i+1)
        start_arr.append(rs[str('st_'+pre_fix+'p')])
        end_arr.append(rs[str('ed_'+pre_fix+'p')])
        uppr_arr.append( rs[str('p_'+pre_fix+'uppr')])
        add_arr.append(rs[str('plus_'+pre_fix+'p')])

        if final_price == 0:
            if i == 0 :
                if dollar_price > 0 and dollar_price <= end_arr[i] :
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])
            elif i == 29 :
                if dollar_price > start_arr[i] :
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])
            else :
                if dollar_price > start_arr[i] and dollar_price <= end_arr[i]:
                    final_price = float((won_price * float(uppr_arr[i])) + add_arr[i])

        if final_price != 0:
            #print(" [{}] : {} * {} + {} = {}".format(price, round(won_price), uppr_arr[i], add_arr[i], round(final_price)))
            return round(final_price, 2)

    #print(">> final_price : [{}] {} | sale : {}".format(price, final_price, (final_price*0.5)))
    return round(final_price, 2)

#옵션처리
def generateOptionString(gDic, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, coupon):
    #################################################################
    klow = 0
    option_item = []
    option_marzin_price_sale_dic = dict()
    for key, value in option_price_dic.items():
        option_item_str = []
        klow = klow + 1
        diff_sale_price = 0
        option_marzin_price = 0
        option_marzin_sale_price = 0
        base_price_marzin = 0
        value_price_marzin = 0
        if str(value) == '0.0':
            value = '0'

        if str(value) == '0' or str(value) == '0.0':
            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            #option_value = "(" + str(key) + ")" + replaceQueryString(option_value_dic[key])
            option_value = replaceQueryStringOption(option_value_dic[key])
            option_item_str.append(option_value)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))
        else:
            diff_sale_price = float(value)-float(base_price_tmp)
            base_price_marzin = getWonpirce(gDic,float(base_price_tmp))
            value_price_marzin = getWonpirce(gDic, float(value))
            option_marzin_price = value_price_marzin - base_price_marzin  
            option_marzin_price = option_marzin_price
            #option_marzin_sale_price = option_marzin_price * ((100-coupon) / 100)
            option_marzin_sale_price = option_marzin_price
            option_marzin_sale_price = int(round(option_marzin_sale_price, -2))

            if d_minus_opt == "1":
                if option_marzin_sale_price >= 0:
                    option_marzin_sale_price = 0
                option_marzin_sale_price = int(round((option_marzin_sale_price / 2), -2))
            else:
                if option_marzin_sale_price < 0:
                    option_marzin_sale_price = 0
            if str(option_marzin_sale_price) == "0.0":
                option_marzin_sale_price = 0

            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            #option_value = "(" + str(key) + ")" + replaceQueryString(option_value_dic[key])
            option_value = replaceQueryStringOption(option_value_dic[key])
            option_item_str.append(option_value)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))

        #print(">>[{}] {} : {} : [ {} - {} = 차액 {}] ( {} )".format(klow, option_value, value, value, base_price_tmp, diff_sale_price, option_marzin_sale_price))

    #print(">> option_marzin_price_sale_dic : {} ".format(option_marzin_price_sale_dic))    return ",".join(option_item) 
    return ",".join(option_item)

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def stringGetNumber(target):
    number_ck = False
    temp_string = ''
    target_len = 0
    while number_ck == False :
        result_goods = target[target_len:]
        if isNumber(result_goods) == True :
            number_ck = True
            temp_string = result_goods
        else:
            target_len += 1
    print(">> stringGetNumber : " +str(temp_string))
    return temp_string

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip :', response.read())

def checkIP2():
    print(" checkIP2 : ",socket.gethostbyname(socket.gethostname()))
    #print("IP Address(External) : ",socket.gethostbyname(socket.getfqdn()))

def set_new_ip():
    #print("set_new_ip()")
    # disable socks server and enabling again
    socks.setdefaultproxy()
    # """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)


# mssql null
def getQueryValue(in_value):
    if in_value == None:
        result_goods = "NULL"
    else:
        result_goods = "'{0}'".format(in_value)
    return result_goods


# review
def get_Review(in_soup, in_asin):

    reviews_arr = []
    sp_review = str(in_soup).split('data-review-region="')
    if len(sp_review) == 0:
        print(">> Review No(2) ")
    else:
        r_cnt = 0
        print('>> len(sp_review) : ' + str(len(sp_review)))
        while r_cnt < len(sp_review):
            review_dic = {}
            tmp_review = getparse(str(sp_review[r_cnt]),'data-transaction-id=','</div>')
            tmp_date = getparse(tmp_review, '</a>', '</p>')
            review_dic['date'] = tmp_date.replace("/", "").replace("\n\n", "<br>").replace("\n", "").replace("'", "").replace('&AMP;', '')
            tmp_review = getparse(str(tmp_review), '">', '</a>')
            tmp_review = tmp_review.replace("/", "").replace("\n\n", "<br>").replace("\n", "").replace("'", "").replace('&AMP;', '')
            review_dic['author'] = tmp_review
            tmp_rating = getparse(str(sp_review[r_cnt]),'<input type="hidden" name="rating"','</div>')
            tmp_rating = getparse(str(tmp_rating), '<span class="wt-screen-reader-only">', '</span>')
            tmp_rating = tmp_rating.replace("/", "").replace("\n\n", "<br>").replace("\n", "").replace("'", "").replace('&AMP;', '').replace('viewBox="3 3 18 18"','viewBox=""')
            tmp_rating = get_replace_viewbox(tmp_rating)
            review_dic['rating'] = tmp_rating

            review_text = ""
            review_tmp = ""
            review_tmp = getparse(str(sp_review[r_cnt]), '', '<div class="other-info">')

            # if str(review_tmp).find('<ul class="wt-list-unstyled wt-overflow-hidden">') > -1:
            #     review_text = review_text + getparse(str(review_tmp), '<ul class="wt-list-unstyled wt-overflow-hidden">', '</ul>')
            # if str(review_tmp).find('<div class="wt-content-toggle--truncated-inline-multi">') > -1:
            #     review_text = review_text + getparse(str(review_tmp), '<div class="wt-content-toggle--truncated-inline-multi">', '</div>')

            # if str(review_tmp).find('data-js-action="openReviewPhotoInline">') > -1:
            #     review_text = review_text + getparse(str(review_tmp), 'data-js-action="openReviewPhotoInline">', '</button>')

            review_text = getparse(str(review_tmp), 'id="review-preview-toggle-', '</p>')
            review_text = getparse(str(review_text), '">', '')
            review_text = review_text.replace("/", "").replace("\n\n", "<br>").replace("\n", "").replace("'", "").replace('&AMP;', '')
            review_dic['review_text'] = review_text.replace('viewBox="3 3 18 18"','viewBox=""')

            review_img = ""
            if str(review_tmp).find('class="wt-height-full wt-width-full wt-display-block"') > -1:
                review_img = getparse(str(review_tmp), 'class="wt-height-full wt-width-full wt-display-block"', 'Purchased item:')
                review_img = getparse(str(review_img), 'src="', '"')
            review_dic['image'] = review_img

            review_item = ""
            review_item_img = ""
            if str(review_tmp).find('Purchased item:') > -1:
                review_item = getparse(str(review_tmp), 'Purchased item:', '')
                review_item_img = getparse(str(review_item), 'src="', '"')
                review_item = getparse(str(review_item), 'data-transaction-id=', '</a>')
                review_item = getparse(str(review_item), '">', '')
            review_dic['review_item'] = review_item
            review_dic['review_item_img'] = review_item_img

            reviews_arr.append(review_dic)
            r_cnt = r_cnt + 1

    return reviews_arr

#reg
def regStrChk(in_str, in_kbn):
    result_goods = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    if in_kbn == "KR":
        regStr = re.search('[가-힣]+',chkStr)
    else:
        regStr = re.search('[^. %–|<>&`()+A-Za-z0-9가-힣]+',chkStr)

    if (regStr):
        result_goods = "1"
    else:
        result_goods = "0"

    return result_goods


#금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_new(target, pdb):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check from Ban_Title where ban_title = 'title' and (ban_cate_idx is null or ban_cate_idx = '')"
    prs = pdb.select(sql)
    for rs in prs :
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        
        if ban_title_inner == None or ban_title_inner == '' : #case 1
            if ban_check == '1' :
                if target.lower().find(ban_title_gubun.lower()) == 0 :
                    result = "1"
                    print('>> [Forbidden (1) 1 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 1  : " + str(ban_title_gubun)
                    break
                elif target.lower().find(ban_title_gubun.lower()) > 0 :
                    forward_index = target.lower().find(ban_title_gubun.lower())
                    backward_index = target.lower().rfind(ban_title_gubun.lower())
                    
                    if forward_index == backward_index :                        
                        check_str = target[forward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-1 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-1  : " + str(ban_title_gubun)                            
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-2 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-2  : " + str(ban_title_gubun)  
                                break                            
                    else:
                        check_str = target[forward_index-1]
                        backward_str = target[backward_index-1]
                        if check_str == '' or check_str ==' ' or check_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-3 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-3  : " + str(ban_title_gubun)  
                            break
                        else:
                            check_symbol = len(re.sub(parttern,'',check_str))
                            if check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-5 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-5  : " + str(ban_title_gubun)  
                                break    
                        
                        if backward_str == '' or backward_str ==' ' or backward_str == None:
                            result = "1"
                            print('>> [Forbidden (1) 1-4 ] :' + str(ban_title_gubun))
                            ban_str = "Forbidden (1) 1-4  : " + str(ban_title_gubun) 
                            break
                        else:
                            backward_check_symbol = len(re.sub(parttern,'',backward_str))
                            if backward_check_symbol > 0 :
                                result = "1"
                                print('>> [Forbidden (1) 1-6 ] :' + str(ban_title_gubun))
                                ban_str = "Forbidden (1) 1-6  : " + str(ban_title_gubun)  
                                break  
            else :
                if target.lower().find(ban_title_gubun.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (1) 0 ] :' + str(ban_title_gubun))
                    ban_str = "Forbidden (1) 0 : " + str(ban_title_gubun)                    
                    break
        else:
            if ban_title_gubun_2 == None or ban_title_gubun_2 == '' : #case 2
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                    ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                    break
            else: #case 3
                if target.lower().find(ban_title_gubun.lower()) > -1 and target.lower().find(ban_title_inner.lower()) > -1 and target.lower().find(ban_title_gubun_2.lower()) > -1 :
                    result = "1"
                    print('>> [Forbidden (3)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2))
                    ban_str = "Forbidden (3) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner) + ' | ' + str(ban_title_gubun_2)
                    break

    if result == "1":
        result = result + '@' + ban_str

    return result

# Forbidden
def checkForbidden(in_word, db_ali):

    ban_chk = "0"
    ban_str = ""
    sql = "select ban_title_gubun, ban_title_inner from Ban_Title where ban_title = 'title' and (ban_cate_idx is null or ban_cate_idx = '')"

    prs = db_ali.select(sql)
    #print('##select ## sql :' + str(sql))

    for rs in prs:
        ban_str = ""
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        if ban_title_inner == None or ban_title_inner == '':
            if in_word.lower().find(ban_title_gubun.lower()) > -1:
                ban_chk = "1"
                print('>> [Forbidden (1)] :' + str(ban_title_gubun))
                ban_str = "Forbidden (1) : " + str(ban_title_gubun)
                break
        else:
            if in_word.lower().find(ban_title_gubun.lower()) > -1 and in_word.lower().find(ban_title_inner.lower()) > -1:
                ban_chk = "1"
                print('>> [Forbidden (2)] :' + str(ban_title_gubun) + ' | ' + str(ban_title_inner))
                ban_str = "Forbidden (2) : " + str(ban_title_gubun) + ' | ' + str(ban_title_inner)
                break

    if ban_chk == "1":
        ban_chk = ban_chk + '@' + ban_str

    return ban_chk

# replace
def replaceTitle(in_word,db_ali):
    target = str(in_word).upper()

    sql = "select replace_ban_title,replace_title from Replace_Title"
    prs = db_ali.select(sql)
    #print('##select ## sql :' + str(sql))

    for rs in prs:
        replace_ban_title = rs[0]
        replace_title = rs[1]
        if replace_ban_title != '' and replace_ban_title != None:

            if target.find(replace_ban_title.upper()) >= 0:
                target = target.replace(replace_ban_title.upper()," " + replace_title + " ")
                print('>> [replace (1)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.lower()) >= 0:
                target = target.replace(replace_ban_title.lower(), " " + replace_title + " ")
                print('>> [replace (2)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

            if target.find(replace_ban_title.capitalize()) >= 0 :
                target = target.replace(replace_ban_title.capitalize(), " " + replace_title + " ")
                print('>> [replace (3)] :' + str(replace_ban_title) + ' -> ' + str(replace_title))

    #print('[replace)] :' + str(target))
    return target


# reg replace
def regReplaceStr(in_str):
    result_goods = ""
    regStr = re.compile('[^-. %–|<>&`()+A-Za-z0-9가-힣]+')
    result_goods = regStr.sub('', in_str)
    #print(result_goods)

    return result_goods

# 특수단어 제거
def replaceQueryString(in_word) :
    result_goods = in_word.replace("'","")
    result_goods = result_goods.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result_goods = result_goods.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result_goods = result_goods.replace("&ndash;","-").replace("&times;"," x ").replace("–","-")
    result_goods = result_goods.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result_goods = result_goods.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","").replace("  "," ")

    return result_goods

#goodscode
def getGoodsCode(uid,goodshead):
    result_goods = goodshead+str(uid).zfill(10)
    return result_goods

# contents
def generateContent(dic):
    feature_item = []
    description_item = []
    content_item = []
    description = []
    feature = []

    feature_item.append('<br><br><font color="orange"><b>Highlights</b></font><br><br><br><br>')
    description_item.append('<br><br><br><font color="red"><b>Description</b></font><br><br><br>')

    feature_item.append("".join(dic['feature']))
    feature = "".join(feature_item)
    description_item.append(dic['description'].replace("'","").replace("Description",""))
    description = "".join(description_item)

    if dic['OptionKind'] == '300' or dic['OptionKind'] == 300:
        option_img_set = []
        for key,values in dic['option_img_dic'].items():
            if str(values) == '<br>' or str(values) == '':
                print(">> option_image values 없음 : "+str(values))
            else:
                values = replaceQueryString(values).replace("`", "")
                #option_img_set.append('<Font color=blue><pre><b>[ {0} ]</b></pre></FONT><br><img src="{1}"><br><br>'.format(key,values))
                option_img_set.append('<br><Font color=blue><b><pre>[{0}]</pre></b></FONT><br><img src="{1}"><br><br>'.format(values.replace('"','').replace("'",""),key))
        opt_img_item = "".join(option_img_set)
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(opt_img_item.replace("'",""))
        content_item.append(description.replace("'","").replace("・","·"))
    else:
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(description.replace("'",""))        

    return "".join(content_item)


def setDisplay(guid,isdisplay,stock_flg,db_con):
    sql = ""

    if isdisplay == 'T':
        if stock_flg != "":
            sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = '{0}', UpdateDate=getdate() where uid = {1}".format(stock_flg, guid)
        else:
            sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = null, UpdateDate=getdate() where uid = {0}".format(guid)
    else:
        if stock_flg != "":
            sql = "UPDATE t_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '{0}', UpdateDate=getdate() where uid = {1}".format(stock_flg, guid)
        else:
            sql = "UPDATE t_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate() where uid = {0}".format(guid)

    print('>> setDisplay : '+str(sql))

    try:
        db_con.execute(sql)
        print('>> ## update_execute ')
    except Exception as e:
        print('>> setDisplay Exception [t_goods]')
        return "Q02"

    return "0"


def setStock_ck(guid, flg, db_con, regdate, UpdateDate):

    if UpdateDate == "" or UpdateDate is None:
        sql = " UPDATE t_goods SET stock_ck = '{0}', stock_ck_cnt = stock_ck_cnt + 1, stock_ck_date=getdate(), UpdateDate = regdate  where uid = {1}".format(flg, guid)
    else:
        sql = " UPDATE t_goods SET stock_ck = '{0}', stock_ck_cnt = stock_ck_cnt + 1, stock_ck_date=getdate(), UpdateDate= UpdateDate - 3 where uid = {1}".format(flg, guid)
    print('>> setStock_ck : '+str(sql))

    try:
        db_con.execute(sql)
        print('>> ## update_execute ')
    except Exception as e:
        print('>> setStock_ck Exception [t_goods]')
        return "Q02"

    return "0"

#DB set
def setDB_proc(in_asin, dic, db_con, in_pg, in_guid):

    rtn_goodscode = ""
    #print('>> setDB in_guid :' + str(in_guid))
    print('>> setDB start : ' +str(in_pg))
    #print('>> [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_asin))

    goods_title = dic['title']
    
    ##### price check #####
    if float(dic['price']) < 1:
        print('>> 1 위안 미만 (skip)')
        return "D12" + " ( " + str(dic['price']) + " ) "  # 1 위안 미만 

    # DB query
    goodsinfo_dic = dict()
    goodsinfo_dic['SiteID'] = "'rental'"
    goodsinfo_dic['DealerID'] = "'rental'"
    goodsinfo_dic['GoodsType'] = "'N'"
    goodsinfo_dic['Title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)

    goodsinfo_dic['ImgB'] = getQueryValue(dic['ImgB'])
    goodsinfo_dic['ImgM'] = getQueryValue(dic['ImgB'])
    goodsinfo_dic['ImgS'] = getQueryValue(dic['ImgB'])
    #goodsinfo_dic['naver_img'] = getQueryValue(dic['naver_img'])
    goodsinfo_dic['OptionKind'] = getQueryValue(dic['OptionKind'])
    goodsinfo_dic['DeliveryPolicy'] = "'990'"
    goodsinfo_dic['State'] = "'100'"
    goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
    goodsinfo_dic['price_tmp'] = getQueryValue(dic['price_tmp'])
    goodsinfo_dic['OriginalPrice'] = dic['OriginalPrice']
    goodsinfo_dic['ali_no'] = getQueryValue(dic['ali_no'])
    goodsinfo_dic['cate_idx'] = dic['catecode']
    goodsinfo_dic['E_title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['DE_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['DE_title'])
    goodsinfo_dic['shipping_fee'] = getQueryValue(dic['shipping_fee'])
    goodsinfo_dic['shipping_weight'] = getQueryValue(dic['shipping_weight'])
    goodsinfo_dic['origin_dollar'] = getQueryValue(dic['price'])
    goodsinfo_dic['withbuy_price_tmp'] = getQueryValue(dic['delivery_fee'])
    goodsinfo_dic['price_ea'] = getQueryValue(dic['price_ea'])
    goodsinfo_dic['price_begin'] = getQueryValue(dic['price_begin'])
    goodsinfo_dic['price2_ea'] = getQueryValue(dic['price2_ea'])
    goodsinfo_dic['price2_begin'] = getQueryValue(dic['price2_begin'])
    goodsinfo_dic['price3_ea'] = getQueryValue(dic['price3_ea'])
    goodsinfo_dic['price3_begin'] = getQueryValue(dic['price3_begin'])
    many_option_ck = dic['many_option']
    if many_option_ck == '1' :
        goodsinfo_dic['many_option'] = "'1'"

    #other img
    otherimg_low = 1
    for otherimg in dic['other_img_set']:
        if otherimg_low <= 5:
            goodsinfo_dic['other_img_chk_'+str(otherimg_low)] = "'1'"
            goodsinfo_dic['other_img'+str(otherimg_low)] = getQueryValue(otherimg)
        otherimg_low += 1

    ##############################################
    #option (goodsinfo_option_dic)
    ##############################################
    goodsinfo_option_dic = dict()
    if dic['OptionKind'] == '300' or dic['OptionKind'] == 300:
        goodsinfo_option_dic['Title'] = "'옵션선택'"
        goodsinfo_option_dic['Items'] = dic['Items']

        if str(goodsinfo_option_dic['Items']).find('/0') > -1:
            print('>> Opt 기본옵션 /0 포함 ')
        else:
            print('>> Opt 기본옵션 /0 없음 (SKIP) ')
            print(dic['Items'])
            return "D01"

        print('>> option (final) ')
        #print(goodsinfo_option_dic['Items'])

        goodsinfo_option_dic['Sort'] = 1
        goodsinfo_option_dic['ali_no'] = getQueryValue(dic['ali_no'])

    ##############################################
    #t_goods_content
    ##############################################
    goodsinfo_content_dic = dict()
    goodsinfo_content_dic['Content'] = "N" + getQueryValue(generateContent(dic))

    ##############################################
    #t_goods_sub
    ##############################################
    goodsinfo_sub_dic = dict()
    goodsinfo_sub_dic['Product'] = "'CHINA'"

    ##############################################
    # t_goods_category
    ##############################################
    goodsinfo_cate_dic = dict()
    goodsinfo_cate_dic['CateCode'] = dic['catecode']
    goodsinfo_cate_dic['Sort'] = 1
    
    ck_isdisplay = ""
    ck_delnaver = ""
    searchFlg = "0"
    D_ali_no = ""
    procFlg = ""
    if str(in_guid) == '' or in_guid is None or in_guid == 'None':
        procFlg = "N"
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (ali_no) : {}'.format(dic['ali_no']))

        if not rows:
            procFlg = "N"
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"

        print(' procFlg : '+str(procFlg))  
    else:
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode from t_goods where uid = {0} ".format(in_guid)
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (2) (parentali_noasin) ')  

        if rows:
            procFlg = "U" 
            old_guid = rows[0]
            ck_isdisplay = rows[1]
            ck_delnaver = rows[2]
            D_ali_no = rows[3]
            D_goodscode = rows[4]    
            rtn_goodscode = D_goodscode
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"

    if procFlg == "N":
##############################################################
        goodsinfo_dic['confirm_goods'] = 1
##############################################################
        #####################################################################
        print(">> ## setDB New Insert : " + str(in_asin))
        #####################################################################
        #insert t_goods
        try:
            db_con.insert('t_goods',goodsinfo_dic)
            print('>> ## t_goods  insert ')
        except Exception as e:
            print('>> insert t_goods Exception [t_goods]')
            err_flg = "1"
            return "Q01"

        time.sleep(1)
        #goodscode #######################
        sql = "select top 1 uid from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        coderow = db_con.selectone(sql)
        now_guid = coderow[0]         

        new_goodscode = getGoodsCode(now_guid, 'P')
        print('>> new_goodscode : '+str(new_goodscode))
        rtn_goodscode = new_goodscode
        err_flg = "0"

        if str(new_goodscode) == "":
            print('>> goodscode 생성 오류 (Q01) : '+str(new_goodscode))
            err_flg = "1"
            return "Q01"

        if str(new_goodscode).find(str(now_guid)) == -1:
            print('>> goodscode가 unmatch (Q01) : '+str(new_goodscode))
            err_flg = "1"
            return "Q01"

        try:
            sql = "update t_goods set goodscode = '{0}' where uid = {1}".format(new_goodscode,now_guid)
            db_con.execute(sql)
            print('>> t_goods table goodscode update')
        except Exception as e:
            print('>> Exception [#goodscode]', e)
            err_flg = "1"
            return "Q01"

        #option #######################
        option_where_condition = "GOODSUID = '{0}'".format(now_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]', e)
            return "Q02"

        if dic['OptionKind'] == '300' or dic['OptionKind'] == 300 :
            goodsinfo_option_dic['GOODSUID'] = now_guid
            print('>> t_goods_option Insert')
            #print(goodsinfo_option_dic)
            try:
                db_con.insert('t_goods_option',goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_content #######################
        sql = "select * from t_goods_content where uid = {0}".format(now_guid)
        contentrow = db_con.selectone(sql)

        print('>> t_goods_content Insert')
        if not contentrow:
            goodsinfo_content_dic['Uid'] = now_guid
            try:
                db_con.insert('t_goods_content', goodsinfo_content_dic)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q01"
        else:
            content_where_condition = "uid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_sub #######################
        sql = "select * from t_goods_sub where uid={0}".format(now_guid)
        goodssubrow = db_con.selectone(sql)
        print('>> t_goods_sub Insert')
        if not goodssubrow:
            goodsinfo_sub_dic['Uid'] = now_guid
            try:
                db_con.insert('t_goods_sub', goodsinfo_sub_dic)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q01"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(now_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q01"

        #t_goods_category #######################
        sql = "select * from t_goods_category where GoodsUid = '{0}'".format(now_guid)
        categoryrow = db_con.selectone(sql)
        print('>> t_goods_category Insert')
        if not categoryrow :
            goodsinfo_cate_dic['GoodsUid'] = now_guid
            try:
                db_con.insert('t_goods_category', goodsinfo_cate_dic)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q01"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(now_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q01"
        
        print(">> 신규 상품 insert goods Ok : {}".format(rtn_goodscode))
    else:
        #####################################################################
        print(">> ## setDB Update ")
        #####################################################################

        goodsinfo_dic['UpdateDate'] = 'getdate()'
        arr_where_condition = "uid = {0}".format(old_guid)
        print(">> old_guid : " +str(old_guid) + " | ck_isdisplay : "+str(ck_isdisplay) + " | ck_delnaver : " + str(ck_delnaver))
        ### Test ############################
        #print(goodsinfo_dic)
        try:
            db_con.update('t_goods', goodsinfo_dic, arr_where_condition)
            print('>> t_goods Update ')
        except Exception as e:
            print('>> Exception [t_goods]', e)
            err_flg = "1"
            return "Q02"

        # option #######################
        option_where_condition = "GOODSUID = '{0}'".format(old_guid)
        try:
            db_con.delete('t_goods_option', option_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_option]', e)
            return "Q02"

        if dic['OptionKind'] == 300 or dic['OptionKind'] == '300':
            goodsinfo_option_dic['GOODSUID'] = old_guid
            print('>> t_goods_option UPdate:')
            #print(goodsinfo_option_dic)

            try:
                db_con.insert('t_goods_option', goodsinfo_option_dic)
            except Exception as e:
                print('>> Exception [t_goods_option]', e)
                return "Q02"

        #t_goods_content #######################
        sql = "select * from t_goods_content where uid = {0}".format(old_guid)
        contentrow = db_con.selectone(sql)

        print('>> t_goods_content Update')
        if not contentrow:
            goodsinfo_content_dic['Uid'] = old_guid
            try:
                db_con.insert('t_goods_content', goodsinfo_content_dic)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q02"
        else:
            content_where_condition = "uid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_content]', e)
                err_flg = "1"
                return "Q02"

        #t_goods_category #######################
        sql = "select * from t_goods_category where GoodsUid = '{0}'".format(old_guid)
        categoryrow = db_con.selectone(sql)
        print('>> t_goods_category Update')

        if not categoryrow :
            goodsinfo_cate_dic['GoodsUid'] = old_guid
            try:
                db_con.insert('t_goods_category', goodsinfo_cate_dic)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q02"
        else:
            goodsinfo_cate_where = "GoodsUid = '{0}'".format(old_guid)
            try:
                db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
            except Exception as e:
                print('>> Exception [t_goods_category]', e)
                err_flg = "1"
                return "Q02"

        #t_goods_sub #######################
        sql = "select * from t_goods_sub where uid={0}".format(old_guid)
        goodssubrow = db_con.selectone(sql)
        print('>> t_goods_sub Update')
        #print(goodsinfo_sub_dic)
        if not goodssubrow:
            goodsinfo_sub_dic['Uid'] = old_guid
            try:
                db_con.insert('t_goods_sub', goodsinfo_sub_dic)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q02"
        else:
            try:
                goodsinfo_sub_where_condition = "uid='{0}'".format(old_guid)
                db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
            except Exception as e:
                print('>> Exception [t_goods_sub]', e)
                err_flg = "1"
                return "Q02"


        # 품절/진열 변경 #######################
        if ck_isdisplay == "F": # 품절상태의 경우
            if ck_delnaver == 0:
                print('>> IsDisplay Update (품절 -> 노출)')
                sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = null, stock_ck_cnt = '0', UpdateDate=getdate() where uid = {0}".format(old_guid)
                #print('>> setDisplay : ' + str(sql))
                try:
                    db_con.execute(sql)
                    print('>> ## update_execute ')
                except Exception as e:
                    print('>> Exception [t_goods]', e)
                    return "Q02"

        print(">> 기존 상품 update goods Ok ")

    dic.clear()
    goodsinfo_dic.clear()
    goodsinfo_content_dic.clear()
    goodsinfo_option_dic.clear()
    goodsinfo_sub_dic.clear()
    goodsinfo_cate_dic.clear()

    print(">> SetDB OK ASIN : " + str(in_asin))
    return "0@" + str(rtn_goodscode)

def setGoodsdelProc(db_con, in_DUid, in_DIsDisplay, in_DOptionKind):

    db_con.delete('t_goods_sub', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_category', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_option', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_content', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods', "uid = '{0}'".format(in_DUid))

    print('>> (setGoodsdelProc) t_goods (delete ok) : {}'.format(in_DUid))

    return "0"



def get_replace_title(str_title):

    tmp_title = str(str_title).strip()
    tmp_title = tmp_title.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ').replace("&lt;","<").replace("&gt;",">")
    tmp_title = tmp_title.replace("&ndash;","-").replace("&times;"," x ").replace("&rdquo;","").replace('–','-').replace('「',' ').replace('」',' ')
    tmp_title = tmp_title.replace("&quot;","").replace("\\", "").replace("★","").replace("◆","").replace('"', '')

    return tmp_title


def get_replace_viewbox(str_tmp):
    
    str_tmp = str(str_tmp).strip()
    str_tmp = str_tmp.replace('viewBox="0 0 32 32"','viewBox=""').replace('viewBox="0 0 24 24"','viewBox=""').replace('viewBox="0 0 16 16"','viewBox=""')
    str_tmp = str_tmp.replace('viewBox="0 0 18 18"','viewBox=""').replace('viewBox="3 3 18 18','viewBox=""').replace('viewBox="0 0 12 12"','viewBox=""')

    return str_tmp    

#reg 한글 체크
def regKrStrChk(in_str):
    result_goods = ""
    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)
    if (regStr):
        result_goods = "1"
    else:
        result_goods = "0"
    return result_goods

# get_galleryGoods
def get_galleryGoods(in_soup, in_asin):
    gallery_tmp = ""
    cnt_save = 0

    related_asin = ""
    related_asin = getparse(str(in_soup),'<div class="other-info">','<div data-appears-component-name="tags">')
    detail_gallery_item = str(related_asin).split('data-palette-listing-image')
    print("detail_gallery_item cnt: {}".format(len(detail_gallery_item)))
    
    if len(detail_gallery_item) == 0:
        print('>> gallery goods 0')
        return "1"

    glow = 1
    while glow < len(detail_gallery_item):
        info_url = getparse(str(detail_gallery_item[glow]),'href="','"')
        info_asin = getparse(str(info_url),'/listing/','/').strip()
        if str(info_asin) != str(in_asin) and gallery_tmp.find(info_asin) == -1 and len(info_asin) == 10:
            cnt_save = cnt_save + 1
            if gallery_tmp == "":
                gallery_tmp = info_asin
            else:
                gallery_tmp = gallery_tmp + "," + info_asin

        glow = glow + 1

    print('>> gallery goods (only) : ' + str(cnt_save))
    return "".join(gallery_tmp)


# highlights
def get_highlights(in_soup):
    highlights_tmp = ""
    cnt_save = 0

    highlights = ""
    highlights = getparse(str(in_soup),'data-content-toggle-uid="product-details-content-toggle"','"listing_page_policy_shipping_variant"')
    highlights = getparse(str(highlights),'aria-expanded="true">','<div data-appears-component-name=')
    if str(highlights).find('Exceptions may apply') > -1:
        highlights = getparse(str(highlights),'','Exceptions may apply')
    if str(highlights).find('aria-controls="product-description-content-toggle"') > -1:
        highlights = getparse(str(highlights),'','aria-controls="product-description-content-toggle"')
    highlights = highlights.replace('Highlights','').replace('Read the full description','')
    highlights = get_replace_viewbox(highlights)

    detail_highlights = str(highlights).split('<li class="wt-list-unstyled wt-display-flex-xs wt-align-items-flex-start">')
    print("detail_highlights cnt: {}".format(len(detail_highlights)))
    
    if len(detail_highlights) == 0:
        print('>> No highlights ')
        return "1"

    glow = 1
    while glow < len(detail_highlights):
        ea_temp = ""
        if str(detail_highlights[glow]).find('</svg></span></div>') > -1:
            ea_temp = getparse(str(detail_highlights[glow]),'</svg></span></div>','</li>')
        elif str(detail_highlights[glow]).find('<div class="wt-ml-xs-2">') > -1:
            ea_temp = getparse(str(detail_highlights[glow]),'<div class="wt-ml-xs-2">','</div>')            
        else:
            ea_temp = getparse(str(detail_highlights[glow]),'','</li>')
        highlights_tmp = highlights_tmp + "<br>" + ea_temp
        glow = glow + 1

    print('>> highlights : ' + str(cnt_save))
    return "".join(highlights_tmp)


def procIpChange(maxCnt):
    wCnt = 0 
    while wCnt < maxCnt:
        set_new_ip()
        print(checkIP())
        time.sleep(2)
        wCnt = wCnt + 1
        
def getSource(in_drive, db_con, db_ali, in_pg, now_url):

    print('>> now_url : ' + str(now_url)) 
    in_drive.get(now_url)
    time.sleep(3)     

    result_goods = ""
    result_goods = in_drive.page_source
    time.sleep(1)
    
    if str(result_goods).find('HTTP ERROR 429') > -1:
        print('>> Connect Error ')
        return "E99"       

    if str(result_goods).find('data-id="gnav-search-submit-button"') > -1 and str(result_goods).find('data-buy-box-listing-title="true">') > -1:
        print('>> Connect Ok ')

        if str(result_goods).find('Deliver to South Korea') > -1:
            print('>> Deliver to South Korea ')
        else:
            time.sleep(1)
            try:
                in_drive.find_element_by_xpath('//*[@id="shipping-variant-div"]/div/div[2]/div[6]/button/span[1]').click()
                time.sleep(1)
                in_drive.find_element_by_xpath('//*[@id="estimated-shipping-country"]/optgroup/option[216]').click()
                time.sleep(1)
                delievey_to = in_drive.find_element_by_xpath('//*[@id="estimated-shipping-country"]/optgroup/option[216]').text
            except TimeoutException as ex:
                print('>> getSource TimeoutException Error ')
                result_goods = "E99"                      
            except Exception as e:
                print('>> getSource Exception Error ')
                result_goods = ""
            else:
                time.sleep(1)
                result_goods = in_drive.page_source
                if str(result_goods).find('Deliver to South Korea') > -1:
                    print('>> Deliver to South Korea ')
                else:
                    print('>> 배송비 확인불가 ')
                    return "D11"  
            if result_goods == "":
                print('>> Connect Error ')
                return "D11"

    elif str(result_goods).find('Sorry, this item is unavailable') > -1:
        print('>> sold out (this item is unavailable) ')
        return "D17"       
    elif str(result_goods).find('Sorry, this item and shop are currently unavailable') > -1:
        print('>> sold out (this item and shop are currently unavailable)')
        return "D01"
    elif str(result_goods).find('Sorry, this item is sold out') > -1:
        print('>> sold out (this item is sold out)')
        return "D01"
    elif str(result_goods).find('This shop is taking a short break') > -1:
        print('>> sold out (This shop is taking a short break) ')
        return "D01"
    else:
        chkCode = "C02"
        return "C02"

    print(">> Browser Count : {}".format(len(in_drive.window_handles)))
    if len(in_drive.window_handles) != 1:
        print(">> Browser Close : {}".format(len(in_drive.window_handles)))
        procLogSet(db_con, in_pg, ">> ( Browser Count) : " + str(len(in_drive.window_handles)))  
        procEnd(db_con, db_ali, in_drive, in_pg)

    result_goods = ""
    result_goods = in_drive.page_source
    time.sleep(1)
    #########################################################################
    if str(result_goods).find('HTTP ERROR ') > -1:
        print('>> HTTP ERROR ')
        print('>> C05 blocked ')
        return "C05"  # blocked

    if str(result_goods).find('data-buy-box-listing-title="true">') == -1:
        print('>> detail_soup No')
        print('>> C02 blocked ')
        return "C02"  # Connect error

    if str(result_goods).find('HTTP ERROR 429') > -1:
        print('>> Connect Error ')
        return "E99"  

    return str(result_goods)


def get_goods_price(in_source):
    goods_price = ""
    price_tmp = getparse(str(in_source),'data-buy-box-region="price"','</div>')
    if str(price_tmp).find('>Price:</span>') > -1:
        goods_price = getparse(str(in_source),'>Price:</span>','</p>')
    elif str(price_tmp).find('<p class="wt-text-title-03 wt-mr-xs-2">') > -1:
        goods_price = getparse(str(in_source),'<p class="wt-text-title-03 wt-mr-xs-2">','</p>')

    if str(goods_price).find('<span class="currency-value">') > -1:
        goods_price = getparse(str(goods_price),'<span class="currency-value">','</span>')       
    if str(goods_price).find("<span class='currency-value'>") > -1:
        goods_price = getparse(str(goods_price),"<span class='currency-value'>","</span>")

    #goods_price = str(goods_price).replace("+","").replace("USD","").replace("$","").replace(",","").strip()
    return goods_price

def moveSlide(driver):
    print('slide proc')
    #//*[@id="nc_1_n1z"]
    #pyautogui.moveTo(random.randint(800,900), random.randint(580,650), duration=random.uniform(1.5,3.5), tween=pyautogui.easeInBounce)
    print(pyautogui.position())
    sliderA = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    time.sleep(0.5)
    if sliderA:
        xpos = sliderA.location['x'] + random.randint(29,31) #30
        ypos = sliderA.location['y'] + random.randint(97,99) #98
        pyautogui.moveTo(xpos, ypos, duration=random.uniform(1.0,3.5), tween=pyautogui.easeInBounce)
        pyautogui.mouseDown()
        time.sleep(1)
        distance = 260
        current_x = 0
        while True:
            dx = random.randint(50,100)
            dy = random.randint(-3,3)
            dt = random.randint(50,100) / 100
            print(" dx: {}  dy: {}  dt: {} ".format(dx,dy,dt))
            pyautogui.moveRel(dx, dy, dt, tween=pyautogui.easeInOutSine)
            current_x += dx
            if current_x >= distance:
                dx = distance - current_x
                dy = random.randint(-8, 8)
                pyautogui.moveRel(dx, dy, 0.25, tween=pyautogui.easeInOutSine)
                break

        pyautogui.mouseUp()
        print(pyautogui.position())


        # sliderA.click()
        # time.sleep(0.5)
        # sliderC = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        # if sliderC:
        #     #sliderC.click()
        #     time.sleep(random.uniform(0.2,1))
        #     pyautogui.moveTo(sliderC.location['x'] + 30 -2, sliderC.location['y'] + 98, duration=4, tween=pyautogui.easeInElastic)
        #     pyautogui.click(duration=random.uniform(0.2,0.5))
        #     pyautogui.mouseDown()
        #     pyautogui.moveTo(sliderC.location['x'] + 30 + 282 , sliderC.location['y'] + 99, duration=random.uniform(1.5,2.5))
        #     time.sleep(0.1)
        #     pyautogui.mouseUp()
        #     time.sleep(1)
        #     #input(">> position (1)")
        #     print(pyautogui.position())

    #slider = None
    #if slider:
        # move = ActionChains(driver)
        # move.click_and_hold(slider).perform()
        # driver.implicitly_wait(5)
        # xval = 0
        # try:
        #     move.move_by_offset(10, 1).perform()
        #     time.sleep(0.1)
        #     move.move_by_offset(20, 1).perform()
        #     move.move_by_offset(60, 1).perform()
        #     move.move_by_offset(80, 1).perform()
        #     move.move_by_offset(120, 1).perform()
        #     move.move_by_offset(180, 1).perform()
        #     move.move_by_offset(250, 1).perform()
        #     time.sleep(4)
        #     main_result_goods = driver.page_source
        #     if str(main_result_goods).find('Please refresh and try again') > -1:
        #         driver.find_element_by_xpath('//*[@id="`nc_1_refresh1`"]').click()
        #         time.sleep(1)
        # except UnexpectedAlertPresentException:
        #     print("UnexpectedAlertPresentException")
        # else:
        #     move.reset_actions()
        #     time.sleep(0.1)
        # time.sleep(random.uniform(3,5))

def checkSlide(driver):
    driver.delete_all_cookies()
    flg = "1"
    count = 0
    main_result_goods = driver.page_source
    if str(main_result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network (SKIP) ")
        time.sleep(1)
        flg = "0"
        while flg == "0":
            count = count + 1
            #driver.refresh()
            print('slide click : {}'.format(count))
            try:
                moveSlide(driver)
            except Exception as e:
                print('>> checkSlide Exception Error ')

            time.sleep(random.uniform(2,4))
            main_result_goods = driver.page_source
            if str(main_result_goods).find('we have detected unusual traffic from your network.') == -1:
                print(">> Slide check OK ")
                flg == "1"
                break
            else:
                driver.refresh()

            if count > 3:
                flg == "E"
                break
    return flg

#db 특수단어 제거
def replaceQueryStringOption(target) :
    result = target.replace("'","`").replace(","," ").replace("正品","").replace("정품"," ").replace("、",".")
    result = result.replace("★","").replace("◆","").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("--","-").replace('"', '`')
    result = result.replace("{","(").replace("}",")").replace("/"," . ").replace("【","(").replace("】",")").replace("[","(").replace("]",")").replace("「","(").replace("」",")").replace("  "," ")
    return result

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()
    return result_str

def moveScroll(driver):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 700
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > 5:
            break
        last_height = new_height

def moveScrollMain(driver):
    SCROLL_PAUSE_SEC = 0.5
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = "1000"
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 800
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > 10:
            break
        last_height = new_height

def procTranConect(browser, in_asin, option_max_count, proc_flg):
    result_tran = ""
    if proc_flg == "option":
        tran_url = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_shop_option.asp?asin={0}'.format(in_asin)
    else:
        tran_url = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_shop.asp?asin={0}'.format(in_asin)
    print(">> tran_url : {}".format(tran_url))
    browser.get(tran_url)
    time.sleep(random.uniform(6,7))
    if option_max_count > 25:
        moveScroll(browser)
    time.sleep(1)
    result_tran = str(browser.page_source)
    #print(">> result_tran : {}".format(result_tran))
    return result_tran

def getTranTitle(result_tmp, in_asin):
    tran_title = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_title = getparse(result_tmp,'<div id="google_translate_element">','<hr>')
        tran_title = getparse(tran_title,'<input type="hidden"','')
        tran_title = getparse(tran_title,'">','')
        tran_title = replace_main_str(tran_title)
        tran_title = tran_title.replace("- ChinaglobalMall","").strip()
    return str(tran_title)

# def getTranOption(result_tmp, in_asin):
#     tran_option = ""
#     if str(result_tmp).find(in_asin) > -1:
#         tran_option = getparse(result_tmp,'<div id="google_translate_element">','<div class="skiptranslate ')
#         tran_option = getparse(tran_option,'<hr>','')
#         tran_option = replace_main_str(tran_option)
#     return str(tran_option)

def getTranOption(result_tmp, in_asin):
    tran_option = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_option = getparse(result_tmp,'<div id="google_translate_element">','<div class="skiptranslate ')
        tran_option = getparse(tran_option,'<hr>','')
        if tran_option.find('<div class="option_image">') > -1:
            tran_option = getparse(tran_option,'','<div class="option_image">')
        tran_option = replace_main_str(tran_option)
    return str(tran_option)

def getTranOption_image(result_tmp, in_asin):
    tran_img_option = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_img_option = getparse(result_tmp,'<div id="google_translate_element">','<div class="skiptranslate ')
        tran_img_option = getparse(tran_img_option,'<hr>','')
        tran_img_option = getparse(tran_img_option,'<div class="option_image">','</div>')
        tran_img_option = replace_main_str(tran_img_option)
    return str(tran_img_option)

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9]', '', in_str)
    return result

def proc_asin_parse_brower(gDic, db_con, db_ali, browser, in_pg, in_pgsite):

    guid = ""
    asin = gDic['asin']
    catecode = gDic['catecode']
    guid = gDic['guid']
    option_item = ""
    title = ""
    descript = ""
    tran_title = ""
    tran_option = ""
    base_min_price = 0
    base_top_price = 0
    option_val_count = 0
    option_max_count = 100

    time.sleep(1)
    #goods_url = "https://detail.1688.com/offer/{}.html".format(asin)
    goods_url = "https://detail.1688.com/offer/{}.html?sk=consign".format(asin)
    print(">> {} | {}".format(catecode, goods_url))

    browser.get(goods_url)
    browser.set_window_position(0, 0, windowHandle='current')
    time.sleep(random.uniform(4,6))

    result_goods = ""
    result_goods = str(browser.page_source)
    # with open("soup_result_goods" +str(ea_asin)+ ".html","w",encoding="utf8") as f: 
    #     f.write(str(soup_result_goods))
    if str(result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network [1]")
        print(">> time.sleep(5) ")
        time.sleep(5)

    if str(result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network [2]")
        print(">> checkSlide Start ")
        try:
            rtnFlg = checkSlide(browser)
        except Exception as e:
            print(">> checkSlide Exception ")

        print(">> time.sleep(10) ")
        time.sleep(10)
        #return "E99"

    result_goods = str(browser.page_source)
    if str(result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network (exit) ")
        time.sleep(5)
        return "E99"

    ##### ea #####
    price_head = getparse(str(result_goods),'class="price-header">','class="service-content"')
    ea_tmp = getparse(str(price_head),'class="unit-text">','</span>')
    ea_disit = regRemoveText(ea_tmp).strip()
    if str(ea_disit) != "1":
        print('>> 최소 수량 1개 초과')
        return "D13" + " ( " + str(ea_tmp) + " ) " 

    # try:
    #     moveScrollMain(browser)
    # except Exception as e:
    #     print(">> moveScrollMain Exception ")
    #     time.sleep(5)

    time.sleep(1)
    result_goods = ""
    result_goods = str(browser.page_source)
    time.sleep(1)

    if str(result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network (exit) ")
        time.sleep(5)
        return "E99"
    # else:
    #     rtnFlg = checkSlide(browser)
    #     if rtnFlg == "1":
    #         result_goods = browser.page_source
    #         print(">> RE page_source Ok")
    #     else:
    #         print(">> Slide Error (SKIP) ")
    #         time.sleep(3)
    #         print(">> error_cnt 5 Over (Exit) ")
    #         print(">> Connect page Error (E99) : {}".format(curr_page))
    #         return "E99"

    curr_page = browser.current_url
    if str(curr_page).find('/member/login') > -1:
        print(">> Connect page Error (E99) : {}".format(curr_page))
        return "E99"

    db_Weight = "0"
    DB_stop_update = "0"
    shipping_weight = 0
    # stop_update check
    if str(guid) == '' or guid == 'None' or guid is None:
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, DE_title, title from t_goods where uid = {0}".format(guid)

    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_title = rowUP[6]
        shipping_weight = float(db_Weight)

        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid
        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"
        if str(db_Del_Naver) == "1":
            print('>> Del_Naver 1 (네이버 미노출상품) : ' + str(asin))
        if str(DB_stop_update) == "1":
            print('>> stop_update goods : ' + str(asin))
            return "S01"

    print('>> stop_update No goods : ' + str(asin))
    if str(guid) == '':
        print('>>>>>>>>>>>>>>>>>>>>> no guid (신규) ')
    else:
        print('>>>>>>>>>>>>>>>>>>>>> guid (존재) : ' + str(guid))

    # page 체크 #######################################
    if str(browser.current_url).find('wrongpage.html') > -1:
        print('>> No Page 404 wrongpage.html : {}'.format(asin))
        return "D17"
    if str(browser.current_url).find('home.html?') > -1:
        print('>> No Page 404 home.html : {}'.format(asin))
        return "D17"
    if str(browser.current_url).find('1688.com/offer/') > -1:
        print('>> (Page Ok) Url Ok : {}'.format(asin))

    # 품절 체크 #######################################
    if str(result_goods).find('暂不支持在线交易') > -1:
        print('>> (품절) 暂不支持在线交易  (온라인거래 지원무): {}'.format(asin))
        return "D01"

    if str(result_goods).find('立即订购') > -1:
        #print('>> (구매가능) 立即订购  (지금 주문하세요): {}'.format(asin))
        pass

    try:
        moveScrollMain(browser)
    except Exception as e:
        print(">> moveScrollMain Exception ")
        time.sleep(3)

    time.sleep(1)
    result_goods = ""
    result_goods = str(browser.page_source)
    time.sleep(1)
    if str(result_goods).find('we have detected unusual traffic from your network.') > -1:
        print(">> detected unusual traffic from your network (exit) ")
        time.sleep(5)
        return "E99"

    ##################################################
    result_dic = dict()
    result_goods = str(result_goods)
    ######################## goods parsing ########################
    #print('>> goods parsing ######################## ')

    ##### title #####
    title = getparse(str(result_goods),'class="title-text">','</div>')
    #print(">> Title : {}".format(title))
    if findChinese(title):
        title = replaceQueryStringTitle(title)
        print(">> title (2) : {}".format(title))

    ##### price #####
    price_head = getparse(str(result_goods),'class="price-header">','class="service-content"')
    if str(price_head).find('class="step-price-item"') > -1:
        #print(">> price Select (step-price-item) [1] ")
        pass
    elif str(price_head).find('class="price-column"') > -1:
        #print(">> price Select (price-column) [2] ")
        pass

    price_tap = getparse(str(result_goods),'class="od-pc-offer-price-contain"','class="od-pc-offer-discount-contain"')
    sp_price_tap = str(price_tap).split('<div class="price-box">')
    print(">> price_cnt : {}".format(len(sp_price_tap)-1))
    price_cnt = len(sp_price_tap)-1
    # if str(result_goods).find('<div class="step-price-wrapper"') > -1:
    #     print(">> price (3) 3개 setp price ")
    # elif str(result_goods).find('<span class="price-space">~') > -1 and price_cnt == 2:
    #     print(">> price (2) 2개 from~to ")
    # elif str(result_goods).find('<div class="price-content">') > -1 and price_cnt == 1:
    #     print(">> price (1) 1개 price ")
    # else:
    #     print(">> price (4) Check price sytle")

    price_ea = "2"
    price_begin = None
    price2_ea = None
    price2_begin = None
    price3_ea = None
    price3_begin = None
    if price_cnt > 2:
        disPriceRanges = getparse(str(result_goods),'disPriceRanges','skuMapOriginal')
        disPriceRanges = getparse(str(disPriceRanges),'[',']')
        spDisPrice = disPriceRanges.split('},{')
        pRow = 0
        for sItem in spDisPrice:
            pRow = pRow + 1
            beginAmount = getparse(str(sItem),'beginAmount\\":','').replace('}','')
            endAmount = getparse(str(sItem),'endAmount\\":',',').replace('}','')
            sprice = getparse(str(sItem),'price\\":\\"','\\",').replace('}','')
            if endAmount == "0" and int(beginAmount) > int(endAmount):
                endAmount = int(beginAmount) * 10
            if pRow == 1 and beginAmount != "":
                price_ea = str(beginAmount).strip()
                price_begin = str(sprice).strip()
            if price_cnt > 2:
                if pRow == 2 and beginAmount != "":
                    price2_ea = str(beginAmount).strip()
                    price2_begin = str(sprice).strip()
                if pRow == 3 and beginAmount != "":
                    price3_ea = str(beginAmount).strip()
                    price3_begin = str(sprice).strip()
            #print(">> ({}) {} | {} | {} ".format(pRow, sprice, beginAmount, endAmount))

    price = getparse(str(result_goods),'class="price-text">','</span>')
    price = str(price).replace("+","").replace("USD","").replace("$","").replace(",","").strip()
    print("price : {}".format(price))

    if str(price) == "0" or str(price) == "":
        print('>> Sold Out')
        return "D01"
    if float(price) < 1:
        print('>> 1 위안 미만 (skip)')
        return "D12" + " ( " + str(price) + " ) "  # 1 위안 미만
    if float(price) > 7000:
        print('>> 7000 위안 over (skip)')
        return "D09" + " ( " + str(price) + " ) "  # 7000 위안 over

    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(weight,0), bcate from t_category where CateCode = '{0}'".format(catecode)
    rsCate = db_con.selectone(sql2)
    if rsCate:
        d_minus_opt = rsCate[0]
        d_coupon = rsCate[1]
        cate_weight = rsCate[2]
        d_bcate = rsCate[3]
        d_minus_opt = str(d_minus_opt).strip()

    if float(shipping_weight) < float(cate_weight):
        shipping_weight = cate_weight

    ########### shipping_fee ###########
    shop_shipping_fee = 0
    if str(result_goods).find('class="logistics-express-price">') > -1:
        shipping_fee_tmp = getparse(str(result_goods),'class="logistics-express-price">','</font>')
        if str(shipping_fee_tmp).find('</span>') > -1:
            shipping_fee_tmp = getparse(str(shipping_fee_tmp),'','</span>')
        shipping_fee_tmp = str(shipping_fee_tmp).replace('<font style="vertical-align: inherit;">','').strip()
        shipping_fee_tmp = shipping_fee_tmp[:10]
        #print(">> shipping_fee_tmp : {}".format(shipping_fee_tmp))

        if shipping_fee_tmp.find('.') > -1:
            #print(">> shipping_fee_tmp find : {}".format(shipping_fee_tmp))
            pass

        if shipping_fee_tmp.replace('.','').isdigit():
            shop_shipping_fee = float(shipping_fee_tmp)
            if shop_shipping_fee > 25:
                print(">> shipping price over: {} | {} ".format(asin, shop_shipping_fee))
                return "D11" + " ( " + str(shop_shipping_fee) + " )"  # shipping_price 25 위안 (SKIP)
    print(">> shop_shipping_fee : {}".format(shop_shipping_fee))

    ########### image ###########
    mainimage = ""
    other_img_set = []
    img_cnt = 0
    if str(result_goods).find('class="detail-gallery-turn-wrapper') > -1:
        img_sorce = getparse(str(result_goods),'class="detail-gallery-turn-wrapper','class="layout-right"')
        sp_img = str(img_sorce).split('class="detail-gallery-turn-wrapper')
        for ea_img_item in sp_img:
            if str(ea_img_item).find('class="video-icon"') > -1:
                print(">> Skip ")
            else:
                ea_img = str(getparse(str(ea_img_item),'src="','"')).strip() 
                if ea_img != "":
                    other_img_set.append(ea_img)
                    img_cnt = img_cnt + 1
                    #print(">> ea_img : {}".format(ea_img))
                    if img_cnt == 1:
                        mainimage = ea_img

    if str(mainimage).strip() == "":
        print(">> No imag : {}".format(asin))
        return "D19"  # No img 
    print("mainimage : {}".format(mainimage))
    print("len(imgset) : {}".format(len(other_img_set)))

    ########### feature ###########
    feature = ""
    #print(">> feature : {}".format(str(feature)))

    ########### description ###########
    description = ""
    description = getparse(str(result_goods),'id="detailContentContainer">','<div class="price-info-module">')
    description = description.replace('src="//cbu','src="https://cbu')
    description_prt = getparse(str(description),'<img src="','"')
    #print(">> description_prt : {}".format(description_prt[:50])) 
    #with open("soup_description_1688_" +str(asin)+ ".html","w",encoding="utf8") as f: 
    #    f.write(str(description))

    if description.find('src="https://cbu01.alicdn.com/cms/upload/other/lazyload.png" data-lazyload-') > -1:
        description = description.replace('src="https://cbu01.alicdn.com/cms/upload/other/lazyload.png" data-lazyload-','')
    description = description.replace("data-lazyload-", "")
    if description.find('src="null"') > -1:
        description = description.replace('src="null"', '')
        # with open("soup_description_1688_" +str(asin)+ ".html","w",encoding="utf8") as f: 
        #     f.write(str(description))

    result_dic['ali_no'] = asin
    result_dic['catecode'] = catecode
    result_dic['title'] = title
    result_dic['price'] = price
    result_dic['price_tmp'] = float(price)
    result_dic['ImgB'] = mainimage
    result_dic['other_img_set'] = other_img_set
    result_dic['feature'] = feature
    result_dic['description'] = description
    result_dic['shipping_weight'] = shipping_weight
    result_dic['price_ea'] = price_ea
    result_dic['price_begin'] = price_begin
    result_dic['price2_ea'] = price2_ea
    result_dic['price2_begin'] = price2_begin
    result_dic['price3_ea'] = price3_ea
    result_dic['price3_begin'] = price3_begin
    base_min_price = price
    base_top_price = price
            
    ########### option ###########
    skuModel = getparse(str(result_goods),"skuModel","skuInfoMap")
    skuInfoMap = getparse(str(result_goods),"skuInfoMap","skuInfoMapOriginal")
    # with open("soup_skuInfoMap_1688.html","w",encoding="utf8") as f: 
    #     f.write(str(skuInfoMap))

    sp_skuInfoMap = skuInfoMap.split('"specId"')
    opt_val_cnt = len(sp_skuInfoMap)
    if opt_val_cnt > 1:
        result_dic['OptionKind'] = '300'
        result_dic['many_option'] = '1'
        print('>> option item')
        option_check = "1"
    else:
        result_dic['OptionKind'] = None
        result_dic['many_option'] = '0'
        print('>> No option item')
        option_check = "0"

    if option_check == "1":
        option_code_dic = dict()
        option_value_dic = dict()
        option_price_dic = dict()
        option_img_dic = dict()
        option_value_tran_arr = []
        option_image_tran_arr = []
        option_min_price = 0
        option_max_price = 0
        option_val_count = 0
        opt_tran_cnt = 0
        option_max_count = 100

        sp_option_cnt = len(sp_skuInfoMap)
        if sp_option_cnt > 300:
            option_max_count = 100
            print(">> Option Cnt 300 over ")

        if option_max_count > sp_option_cnt:
            option_max_count = sp_option_cnt  ################ option max 값 한정하기 

        ### option image
        sp_opt_img = skuModel.split('"imageUrl":"')
        for ea_opt_img in sp_opt_img:
            option_image_tran_dic = {}
            option_image_name = ""
            option_image = ""
            if str(ea_opt_img).find('https:') > -1:
                option_image = str('https:') + getparse(str(ea_opt_img),'https:','"').strip()
                option_image_name = getparse(str(ea_opt_img),'"name":"','"').replace('/',' . ').replace('&gt;',' | ')
                option_image_name = option_image_name.replace(r'\x26', '&').replace('&#39;', '`').replace('&amp;', '&').replace('&quot;', '').replace("'", "`").replace('"', '').strip()
                option_image_name = replaceQueryStringOption(option_image_name)
                if option_image != "":
                    option_img_dic[option_image] = option_image_name
                    option_image_tran_dic['code'] = option_image
                    option_image_tran_dic['name'] = option_image_name.replace(" ","&nbsp;")
                    option_image_tran_arr.append(option_image_tran_dic)
                    #print(">> option_image : {}".format(option_image))

        ### option value | option price
        for ea_sku in sp_skuInfoMap:
            option_value_tran_dic = dict()
            item_value = getparse(str(ea_sku), '"specAttrs":"', '"')
            if item_value == "":
                continue
            item_value = item_value.replace('/',' . ').replace('&gt;',' | ')
            item_value = item_value.replace(r'\x26', '&').replace('&#39;', '`').replace('&amp;', '&').replace('&quot;', '').replace("'", "`").replace('"', '').strip()
            item_saleCount = getparse(str(ea_sku), '"saleCount":', ',')
            item_canBookCount = getparse(str(ea_sku), '"canBookCount":', ',')
            item_discountPrice = getparse(str(ea_sku), '"discountPrice":', ',')
            if item_discountPrice == "":
                item_discountPrice = price
            item_skuId = getparse(str(ea_sku), '"skuId":', ',')
            if item_canBookCount == "0":
                pass
                #print(">> ({}) {}  (price: {} 위안) (stock: {} ) [품절] ".format(item_skuId, item_value, item_discountPrice, item_canBookCount, item_saleCount))
            elif float(item_canBookCount) < 20:
                pass
                #print(">> ({}) {}  (price: {} 위안) (stock: {} ) [재고20개미만] ".format(item_skuId, item_value, item_discountPrice, item_canBookCount, item_saleCount))
            else:
                print(">> ({}) {}  (price: {} 위안) (stock: {} ) ".format(item_skuId, item_value, item_discountPrice, item_canBookCount, item_saleCount))
                option_value = replaceQueryStringOption(item_value)
                if option_value.strip() != "":
                    option_val_count = option_val_count + 1
                    option_price = str(item_discountPrice).replace('"','')
                    option_price_dic[item_skuId] = float(option_price)
                    option_value_dic[item_skuId] = option_value
                    option_value_tran_dic['code'] = str(item_skuId).strip()
                    option_value_tran_dic['name'] = option_value.replace(" ","&nbsp;")
                    option_value_tran_arr.append(option_value_tran_dic)

                #옵션 가격 처리
                if option_min_price == 0 :
                    option_min_price = option_price
                else:
                    if option_min_price > option_price :
                        option_min_price = option_price

                if option_max_price == 0 :
                    option_max_price = option_price
                else:
                    if option_max_price < option_price :
                        option_max_price = option_price

                if option_val_count > option_max_count:
                    break

        # skuInfoMapOriginal = getparse(str(result_goods),"skuInfoMapOriginal","offerBaseInfo")
        # print(">> skuInfoMapOriginal : {}".format(skuInfoMapOriginal))
        option_value_tran_arr = str(option_value_tran_arr).replace("'",'"')
        option_image_tran_arr = str(option_image_tran_arr).replace('\\u3000',' ').replace("'",'"')
        # print(">> ------------- option ---------------------------------------- ")
        # print(">> option_value_dic : {}".format(option_value_dic))
        # print(">> option_price_dic : {}".format(option_price_dic))
        # print(">> option_img_dic : {}".format(option_img_dic))
        # print(">> option_value_tran_arr : {}".format(option_value_tran_arr))
        # print(">> option_image_tran_arr : {}".format(option_image_tran_arr))
        # print(">> ------------- option ---------------------------------------- ")

        if option_val_count == 0:
            ####### No Option
            print(">> Option Goods - opmaxlen 0 : {}".format(asin))
            print('>> Option_value check .')
            return "D07"

        min_price = min(option_price_dic.values())
        top_price = max(option_price_dic.values())
        if min_price != top_price:
            print(">> Option 차액 있음 ")
        if min_price == 0 or min_price == 0.0:
            print(">> Option Min Price : 0 ")
        else:
            base_min_price = min_price
        if top_price == 0 or top_price == 0.0:
            print(">> Option Max Price : 0 ")
        else:
            base_top_price = top_price
        #print(">> Option Max Price : {} ({}) | Option Min Price : {} ( {} ) ".format(base_top_price, getWonpirce(db_ali2,base_top_price,exchange_rate), base_min_price, getWonpirce(db_ali2,base_min_price,exchange_rate)))
        print(">> Option Max Price : {} | Option Min Price : {} ".format(base_top_price, base_min_price))
        print(">> Option_val_count : {}".format(option_val_count))


    if d_minus_opt == "1": # 마이너스 옵션으로 set
        base_price_tmp = float(base_top_price)
        result_dic['price'] = float(base_top_price)
        result_dic['price_tmp'] = float(base_top_price)        
        print('>> 마이너스 옵션 set :' +str(base_price_tmp))
    else:
        base_price_tmp = float(base_min_price)
        result_dic['price'] = float(base_min_price)
        result_dic['price_tmp'] = float(base_min_price)        
        print('>> 플러스 옵션 set :' +str(base_price_tmp))

    tmp_coupon = d_coupon
    if d_coupon is None or d_coupon == "" or d_coupon == 0:
        tmp_coupon = gDic['py_coupon']

    result_dic['minus_opt'] = str(d_minus_opt)
    result_dic['coupon'] = str(tmp_coupon)
    print('>> (DB) goods minus_opt : '+str(result_dic['minus_opt']))

    if option_check == "":
        print(">> Goods Check : {}".format(asin))
        return "D01"       
    if str(price) == "":
        print('>> Sold Out')
        return "D01"

    title = str(title).replace("'","")
    descript = str(descript).replace("'","")
    if option_check == "0":
        option_item_str = "''"
        option_image_str = "''"
    else:
        option_item_str = 'N'+getQueryValue(option_value_tran_arr)
        option_image_str = 'N'+getQueryValue(option_image_tran_arr)
        option_image_str = option_image_str.replace('""','"')

    sql_d = "delete from T_Category_BestAsin_tran where asin = '{}'".format(asin)
    #print(">> insert sql_i : {}".format(sql_d))
    print(">> del asin : {}".format(asin))
    db_con.execute(sql_d)

    sql_i = "insert into T_Category_BestAsin_tran (asin, up_date, price, title, descript, option_item, option_image) values ('{}',getdate(),'{}',{},'{}',{},{})".format(asin,price,'N'+getQueryValue(replaceQueryStringTitle(title)), descript, option_item_str, option_image_str)
    #print(">> insert sql_i : {}".format(sql_i))
    print(">> insert asin : {}".format(asin))
    db_con.execute(sql_i)

    time.sleep(0.5)
    # tran 타이틀 / 옵션 
    if option_check == "0":
        result_tran = procTranConect(browser, asin, option_val_count, "")
    else:
        result_tran = procTranConect(browser, asin, option_val_count, "option")
    time.sleep(0.5)
    tran_title = getTranTitle(result_tran,asin)
    print(">> tran_title : {}".format(tran_title))
    if option_check == "1":
        opt_tran_cnt = 0
        tran_option = getTranOption(result_tran,asin)
        if str(tran_option) != "":
            sp_tran_option = str(tran_option).split('<input type="hidden"')
            for ea_tran_item in sp_tran_option:
                ea_tran_code = ""
                ea_tran_name = ""
                ea_tran_code =  getparse(ea_tran_item,'value="','">')
                ea_tran_name =  getparse(ea_tran_item,'">','').replace("/", "|").replace("&nbsp;", " ").replace("`", "").replace('\n', '').replace('<hr>', '').replace('"', '').strip()
                if str(ea_tran_code).strip() != "" and str(ea_tran_name).strip() != "":
                    #print(">> {} : {}".format(ea_tran_code, option_value_dic[ea_tran_code]))
                    if not findChinese(ea_tran_name):
                        ea_tran_name = str(ea_tran_name)
                        option_value_dic[ea_tran_code] = ea_tran_name
                        opt_tran_cnt = opt_tran_cnt + 1
                        #print(">> {} : {} ".format(ea_tran_code,option_value_dic[ea_tran_code]))

        if option_check == "1" and opt_tran_cnt == 0:
            # No Option
            print(">> opt_tran_cnt  0 : {}".format(asin))
            print('>> Option_value check .')
            return "C02"

        if len(option_image_tran_arr) > 0:
            time.sleep(2)
            tran_option_img = getTranOption_image(result_tran, asin)
            if str(tran_option_img) != "":
                sp_tran_option_img = str(tran_option_img).split('<input type="hidden"')
                for ea_tran_img in sp_tran_option_img:
                    ea_img_tran_code = ""
                    ea_img_tran_name = ""
                    ea_img_tran_code = getparse(ea_tran_img,'value="','">')
                    ea_img_tran_name = getparse(ea_tran_img,'">','').replace("/", "|").replace("&nbsp;", " ").replace("`", "").replace('\n', '').replace('<hr>', '').replace('"', '').strip()
                    if str(ea_img_tran_code).strip() != "" and str(ea_img_tran_name).strip() != "":
                        #print(">> {} : {}".format(ea_img_tran_code, option_img_dic[ea_img_tran_code]))
                        if not findChinese(ea_img_tran_name):
                            ea_img_tran_name = str(ea_img_tran_name)
                            option_img_dic[ea_img_tran_code] = ea_img_tran_name
                            print(">> {} : {} ".format(ea_img_tran_code,option_img_dic[ea_img_tran_code]))

    ########### title Check ###########
    result_dic['DE_title'] = title
    if str(tran_title).strip() == "":
        tran_title = title
    tran_title = tran_title.replace('정품','')
    tran_title = replaceTitle(tran_title, db_ali)
    tran_title = str(tran_title).replace("  ", " ").strip()
    print('>> tran_title (final) : ' + str(tran_title[:80]))
    if str(tran_title).strip() == "":
        print('>> no title ')
        return "D02"
    if len(tran_title) < 5:
        print('>> title len < 5 ')
        return "D02"

    # title 금지어 체크 ###########
    forbidden_flag = checkForbidden_new(tran_title, db_ali)
    if str(forbidden_flag) != "0":
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # originalprice
    if d_minus_opt == '1':
        originalprice = float(result_dic['price']) * float(gDic['py_exchange_Rate'])
        print(">> originalprice ( {} * {} ) : {}".format(result_dic['price'],gDic['py_exchange_Rate'],originalprice))
    else:
        originalprice = float(result_dic['price_tmp']) * float(gDic['py_exchange_Rate'])
        print(">> originalprice ( {} * {} ) : {}".format(result_dic['price_tmp'],gDic['py_exchange_Rate'],originalprice))

    # 배대지 배송비
    delievey_fee = 5900 #
    delievey_fee = float(getDeliveryFee(gDic, shipping_weight))
    print(">> delievey_fee : {} ".format(delievey_fee))

    # shop 유료배송비
    shop_shipping_fee = shop_shipping_fee * float(gDic['py_exchange_Rate']) * 2
    result_dic['shipping_fee'] = shop_shipping_fee
    print(">> shop_shipping_fee : {} ".format(shop_shipping_fee))

    ########### goodsmoney ###########
    goodsmoney = 0
    goodsmoney = getWonpirce(gDic, base_price_tmp)
    print(">> goodsmoney (마진플러스): {} + (배대지) {} + (유료배송) {} ".format(goodsmoney, delievey_fee, shop_shipping_fee))
    goodsmoney = goodsmoney + delievey_fee + shop_shipping_fee
    goodsmoney = int(round(goodsmoney, -2))
    print(">> goodsmoney (Sum) ({}) ".format(goodsmoney))

    if float(goodsmoney) < 28000:
        goodsmoney = 28000
        print('>> goodsmoney 28,000원 이하 -> 28,000 set: ' + str(goodsmoney)) 
    sale_goodsmoney = int(goodsmoney) * ((100-tmp_coupon) / 100)
    print('>> (sale price) : ' + str(sale_goodsmoney)) 
    marzin = sale_goodsmoney - (originalprice + (delievey_fee/2))
    print('>> (sale marzin) : {} ( {} %)'.format(marzin, (marzin/sale_goodsmoney * 100)))    

    if goodsmoney >= 2500000:
        print('>> goodsmoney Over : '+str(goodsmoney))
        return "D09 :" + " ( " + str(goodsmoney) + "원)"

    tran_title = tran_title.replace('<FONT CLASS="" STYLE="VERTICAL-ALIGN: INHERIT;">','')
    tran_title = tran_title.replace('<FONT CLASS="GOOG-TEXT-HIGHLIGHT" STYLE="VERTICAL-ALIGN: INHERIT;">','')        
    result_dic['forbidden'] = 'F'                    
    result_dic['title'] = tran_title
    result_dic['OriginalPrice'] = originalprice
    result_dic['delivery_fee'] = delievey_fee
    result_dic['goodsmoney'] = goodsmoney

    if option_check == "1":
        result_dic['option_code_dic'] = option_code_dic
        result_dic['option_price_dic'] = option_price_dic
        result_dic['option_value_dic'] = option_value_dic
        result_dic['option_img_dic'] = option_img_dic
        result_dic['option_max_min_diff'] = float(option_max_price) - float(option_min_price)

        # 옵션 조합 
        option_item = generateOptionString(gDic, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, tmp_coupon)
        #print(">> Option_item : {}".format(option_item))
        if option_item.find("/0") == -1:
            print('>> option_value check (0원 옵션 없음) : {}'.format(asin))
            return "D07"
        if option_item.find("화물") > -1 or option_item.find("계약") > -1 or option_item.find("보증") > -1 or option_item.find("예약") > -1 or option_item.find("경매") > -1:
            print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(asin))
            return "D47"

        option_item = option_item.replace("`","")
        result_dic['Items'] = getQueryValue(option_item)

    rtnFlg = setDB_proc(asin, result_dic, db_con, in_pg, guid)
    if rtnFlg[:2] != "0@":
        if rtnFlg == "D01":
            print(">> ## t_goods Option /0 없음 에러 (품절처리 필요)  ##")
            return "D01"
        else:
            print('>> setDB error --> DB check Rollback ')
            sql = "select top 1 uid,IsDisplay,OptionKind from t_goods where ali_no = '{0}'".format(asin)
            row = db_con.selectone(sql)
            if not row:
                print(">> ## t_goods Insert No goods (OK) ##")
            else:
                DUid = row[0]
                DIsDisplay = row[1]
                DOptionKind = row[2]
                # 상품 삭제처리 
                setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
                # print('\n >> t_goods Insert (delete)')
            return str(rtnFlg) # exit

    # if str(result_goods).find("we have detected unusual traffic from your network") > -1:
    #     print(">> we have detected unusual traffic from your network : {}".format(asin))
    #     return "E99"

    return "0"

def get_asinset(in_catecode,db_con):
    asinset = []

    sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
    rs_row = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rs_row:
        print('>> category complete! change catecode :' +str(in_catecode))

        where_condition = " catecode = '{0}'".format(in_catecode)
        db_con.delete('update_list2', where_condition)
        return 0

    for ea_asin in rs_row:
        Duid = ""
        asin = ea_asin[0]
        price = ea_asin[1]
        Duid = ea_asin[2]
        if (Duid is None) or (Duid == '') or (Duid == 'None'):
            Duid = ''
        if (price is None) or (price == ''):
            price = 'null'
        #asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(price))
        asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(price) + '@' + str(Duid))

    return asinset

def newlist(db_con, db_ali, in_drive, in_pg, in_ip):

    cateidx = ""
    sql = "select * from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        sql = "select top 1 cate_idx from T_Category_BestAsin where cate_idx not in (select catecode from update_list2) order by up_date"
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> newlist except Error ')
                # proc end
                procEnd(db_con, db_ali, in_drive,in_pg)

    else:
        sql = "select count(*) from update_list2 where proc_ip = '{0}'".format(in_ip)
        rows = db_con.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list2 where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list2 where proc_ip='{0}' order by regdate desc)".format(in_ip)
            db_con.execute(sql)

        sql = "select catecode, now_page from update_list2  where proc_ip = '{0}'".format(in_ip)
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            now_page = row[1]
            if now_page > 2:
                now_page = 2

            sql = "update update_list2 set now_page = {0} ,regdate=getdate() where proc_ip='{1}'".format(now_page, in_ip)
            db_con.execute(sql)

    return cateidx

def getMemo(in_code):
    in_code_no = ""
    in_code_no = str(in_code[:3])
    rtnMemo = ""
    if in_code_no == "D01":
        rtnMemo = str(in_code) + ' : (Sold Out) Unsellable product'
    elif in_code_no == "D02":
        rtnMemo = str(in_code) + ' : (No Title) nsellable product'
    elif in_code_no == "D03":
        rtnMemo = str(in_code) + ' : (Fobidden) Unsellable product'
    elif in_code_no == "D04":
        rtnMemo = str(in_code) + ' : (Buy used) Unsellable product'
    elif in_code_no == "D05":
        rtnMemo = str(in_code) + ' : (Add-on Item) Unsellable product'
    elif in_code_no == "D06":
        rtnMemo = str(in_code) + ' : (Temporarily out of stock) Unsellable product'
    elif in_code_no == "D07":
        rtnMemo = str(in_code) + ' : (option check) Unsellable product'
    elif in_code_no == "D47":
        rtnMemo = str(in_code) + ' : (option check) Unsellable option word'
    elif in_code_no == "D20":
        rtnMemo = str(in_code) + ' : (option check) 2 option price check'
    elif in_code_no == "D08":
        rtnMemo = str(in_code) + ' : (option price check) Unsellable product'
    elif in_code_no == "D09":
        rtnMemo = str(in_code) + ' : (max price over) Unsellable product'
    elif in_code_no == "D49":
        rtnMemo = str(in_code) + ' : (deposit_price) Unsellable product'
    elif in_code_no == "D49": 
        rtnMemo = str(in_code) + ' : (max price over) Unsellable product'
    elif in_code_no == "D10":
        rtnMemo = str(in_code) + ' : (Pre-order) Unsellable product'
    elif in_code_no == "D11":
        rtnMemo = str(in_code) + ' : (shipping price over) Unsellable product'
    elif in_code_no == "D12":
        rtnMemo = str(in_code) + ' : (min price) Unsellable product'
    elif in_code_no == "D13":
        rtnMemo = str(in_code) + ' : (min ea) Unsellable product'
    elif in_code_no == "D17":
        rtnMemo = str(in_code) + ' : (No goodscode) Unsellable product'
    elif in_code_no == "T01":
        rtnMemo = str(in_code) + ' : tmall product'
    elif in_code_no == "D18":
        rtnMemo = str(in_code) + ' : (black-curtain-redirect) Unsellable product'
    elif in_code_no == "D19":
        rtnMemo = str(in_code) + ' : (No img) Unsellable product'
    elif in_code_no == "C01":
        rtnMemo = str(in_code) + ' : (Connection aborted(goods)) Url Connect Error'
    elif in_code_no == "C02":
        rtnMemo = str(in_code) + ' : (Connection aborted(option)) Url Connect Error'
    elif in_code_no == "C04":
        rtnMemo = str(in_code) + ' : blocked (captcha) Url blocked '
    elif in_code_no == "C05":
        rtnMemo = str(in_code) + ' : blocked  Url blocked '
    elif in_code_no == "C06":
        rtnMemo = str(in_code) + ' : Deliver to check '
    elif in_code_no == "C07":
        rtnMemo = str(in_code) + ' : (Title cannot be translated) Japanese included'        
    elif in_code_no == "E99":
        rtnMemo = str(in_code) + ' : error exit '
    elif in_code_no == "E01":
        rtnMemo = str(in_code) + ' : error check '
    elif in_code_no == "E02":
        rtnMemo = str(in_code) + ' : margin set error '
    elif in_code_no == "S01":
        rtnMemo = str(in_code) + ' : update stop goods (SKIP)'
    elif in_code_no == "S02":
        rtnMemo = str(in_code) + ' : naver noclick goods (SKIP)'
    elif in_code_no == "Q01":
        rtnMemo = str(in_code) + ' : setDB (Insert error)'
    elif in_code_no == "Q02":
        rtnMemo = str(in_code) + ' : setDB (Update error)'
    return rtnMemo

def version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn):
    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")

    sql = "select version,url from python_version_manage where name = '" +str(in_pgKbn)+ "'"
    print(">> sql:" + sql)

    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        print(">> (DB) version :" +str(version))

        if str(in_ver) != str(version):
            db_con.close()
            db_ali.close()            
            in_drive.quit()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 10000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")
                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 10000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")

            time.sleep(2)

            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception (1)')
            else:
                pass

            try:
                fname = os.path.abspath( __file__ )
                fname = getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 

                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')
            else:
                pass

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

def procWork(db_con, db_ali, in_drive, in_pg, in_ip):

    print('>> procWork : ' + str(datetime.datetime.now()))
    ip_catecode = ""
    sql = "select catecode from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(ip) + " ] Catecode No. ")
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(ip) + " ] Catecode : " + str(ip_catecode))

        sql = "update update_list2 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list2 (getdate) ")
        db_con.execute(sql)

    return "0"


def procStockWork(db_con, in_pg, in_ip):

    print('>> procStockWork : ' + str(datetime.datetime.now()))
    ip_catecode = ""
    sql = "select proc_ip from update_list3 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] proc_ip No : " + str(ip))
        sql = "insert into update_list3 (regdate, proc_ip) values (getdate(),'{0}')".format(in_ip)
        print(">> insert update_list3 (getdate) ")
        db_con.execute(sql)
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] proc_ip : " + str(ip_catecode))
        sql = "update update_list3 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update update_list3 (getdate) ")
        db_con.execute(sql)

    return "0"

def get_update_goods(in_site, db_FS, db_con):
    asinset = []
    tmp_guid = ""

    sql = " select top 100  guid, sitecate,  display_ali_no, regdate, upddate, flg_chk "
    sql = sql + " from amazon_goods_update "
    sql = sql + " where flg_chk ='0' and sitecate = '" + str(in_site) + "'"
    sql = sql + " order by RegDate asc "

    rs_row = db_FS.select(sql)
    print('>> ##select all## sql :' + str(sql))

    rowCnt = 0
    if rs_row:
        print('>> (amazon_goods_update) top 100 guid ')
        for ea_item in rs_row:
            rowCnt = rowCnt + 1
            d_guid = ea_item[0]
            if rowCnt == 1:
                tmp_guid = " ( " + "'" + str(d_guid) + "'"
            tmp_guid = tmp_guid + ",'" + str(d_guid) + "'"
        if tmp_guid != "":
            tmp_guid = tmp_guid + " ) "
        print('>> tmp_guid :' + str(tmp_guid))

        # 우선 업데이트 대상 상품 업데이트 
        sql = "select top 25 ali_no, price, cate_idx, uid from t_goods where uid in " + str(tmp_guid) 
        rs_row2 = db_con.select(sql)
        print('>> ##select all## sql :' + str(sql))

        if not rs_row2:
            print('>> (UpdateDate) Date No ! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_asin in rs_row2:
                asin = ea_asin[0]
                price = ea_asin[1]
                cate_idx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cate_idx) + '@' + str(price) + '@' + str(uid))
        if chk_data == "0":
            return ""

    return asinset


def set_multi(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic):

    pgName = goods_dic['py_pgFilename']
    cateidx = newlist(db_con, db_ali, browser, pgName, currIp)
    print('>> newlist() catecode :' + str(cateidx))
    if cateidx == "":
        print('>> catecode parsing complete : ' + str(cateidx))
        return "1"
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, db_ali, browser, in_ver, pgName, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_asinset(cateidx, db_con)
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(cateidx))
        return "1"

    allCnt = 0
    c_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        time.sleep(1)
        sp_asin = asin_low.split('@')
        asin = sp_asin[0]
        catecode = sp_asin[1]
        in_price = sp_asin[2]
        guid = sp_asin[3]
        print("\n\n\n### {} : ### [ {} ] (catecode : {}) #################################################".format(allCnt, asin, catecode))
        if allCnt == 1 or allCnt == 50:
            procWork(db_con, db_ali, browser, "", currIp)
        print('>> version : '+str(in_ver))

        goods_dic['asin'] = str(asin)
        goods_dic['catecode'] = str(catecode)
        goods_dic['guid'] = str(guid)

        rtnChk = proc_asin_parse_brower(goods_dic, db_con, db_ali, browser, pgName, "shop")  
        print('>> [ rtnChk ] : ' + str(rtnChk))
        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "E":
            print('>> proc_asin_parse_brower (OK) ')
        else:
            rtnChk = "E01"

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        if rtnChk_no == "E99" or rtnChk_no == "E01":
            print('>> Error Exit : ' + str(rtnChk_no))
            break

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03" or rtnChk_no == "C04" or rtnChk_no == "C05":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
            #procIpChange(3)
            time.sleep(1)
        elif rtnChk_no == "S01":
            print('>> # stop upadte (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "S02":
            print('>> # naver noclick goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB ( Insert )
            print('>> # SetDB  Insert  : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB ( Update )
            print('>> # SetDB  Update  : ' + str(rtnChk))
        elif rtnChk_no == "E01":
            c_Errcnt = c_Errcnt + 1
            print('>> # error : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            c_Errcnt = "E99"
        elif rtnChk_no == "0":
            c_Errcnt = 0
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        dic_b = dict()
        dic_b['asin'] = "'" + rtn_asin + "'"
        dic_b['cate_idx'] = cateidx
        dic_b['memo'] = "'" + getMemo(rtnChk) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "
        #input(" Key Test : ")

        if rtnChk != "0":  
            if rtnChk_no[:1] == "D":
                if str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate from T_goods where ali_no = '{0}'".format(rtn_asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate from T_goods where uid = '{0}'".format(rtn_uid)                    
                rs = db_con.selectone(sql)
                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    DDel_Naver = rs[2]
                    D_regdate = rs[3]
                    D_UpdateDate = rs[4]

                    # T_goods sold out
                    if DIsDisplay == 'T':
                        if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                            sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(Duid)
                            db_con.execute(sql_u1)

                            sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
                            db_con.execute(sql_u2)
                        else:
                            print('>> [' + str(rtn_asin) + '] setDisplay (품절 처리) :' + str(Duid))
                            #setDisplay(Duid, 'F', '', db_con)                                
                            sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
                            print(">> sql : " + str(sql))
                            print(">> 품절 처리 OK : " + str(asin_low))
                            db_con.execute(sql)

                # set_new_ip()
                # print(checkIP())
                # time.sleep(1)

            sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(rtn_asin)
            db_con.execute(sql)
            db_con.insert('T_Category_BestAsin_del', dic_b)  # insert
            print('>> ##insert## : T_Category_BestAsin_del')

        sql = "delete from T_Category_BestAsin where asin ='{0}'".format(rtn_asin)
        db_con.execute(sql)

        print(">> Errcnt : {0} ".format(c_Errcnt))

        if rtnChk_no[:1] == "C":
            # set_new_ip()
            # print(checkIP())
            time.sleep(1)
            if c_Errcnt > 5:
                print('>> ( c_Errcnt 5 over ) exit - catecode :' + str(cateidx))
                procLogSet(db_con, pgName, " ( c_Errcnt 5 over ) exit - catecode: " + str(cateidx))
                procEnd(db_con, db_ali, browser, pgName)

    if rtnChk_no == "E99" or rtnChk_no == "E01":
        print('>> E99 Exit : ' + str(rtnChk_no))
        return "E99"

    return "0"


# Stock ###################################################################################
def get_stock_asin(db_con, in_sql1, in_sql2, in_sql3):
###########################################################################################
    asinset = []
    chk_data = "0"

    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_asin in rs_row:
            asin = ea_asin[0]
            price = ea_asin[1]
            cateidx = ea_asin[2]
            uid = ea_asin[3]
            if (price is None) or (price == ''):
                price = 'null'
            asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if in_sql2 != "":
        rs_row2 = db_con.select(in_sql2)
        print('>> ##select all## in_sql2 :' + str(in_sql2))

        if not rs_row2:
            print('>> (UpdateDate) Stock Check complete! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_asin in rs_row2:
                asin = ea_asin[0]
                price = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if in_sql3 != "":
        rs_row3 = db_con.select(in_sql3)
        print('>> ##select all## in_sql3 :' + str(in_sql3))

        if not rs_row3:
            print('>> ( stock_ck = 9) Check complete! ')
        else:
            print('>> (stock_ck = 9) len :' + str(len(rs_row3)))
            chk_data = "1"
            for ea_asin in rs_row3:
                asin = ea_asin[0]
                price = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if chk_data == "0":
        return ""

    return asinset

# stock_out ###############################################################################
def set_stock_out(db_con, db_ali, in_drive, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2, in_sql3):
###########################################################################################
    print('>> set_stock_out ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, in_sql1, in_sql2, in_sql3)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> get_asin_list parsing complete : ' + str(ip))
        return "11"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        tmp_msg = ""
        allCnt = allCnt + 1

        if allCnt == 1 or allCnt == 50:
            procStockWork(db_con, in_pg, ip)
            time.sleep(1)

        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> ----------------- < (set_stock_out) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_out_brower(asin_low,db_con,db_ali,in_drive,in_pg,in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_stock_out set_stock_out Exception Error' )
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "":
                print('>> error : ' + str(rtnChk))
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_out_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]

        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            break

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> Unsellable product (asin delete) : ' + str(rtnChk))
            if rtnChk_no != "D17":
                d17_Errcnt = 0
            elif rtnChk_no == "D17":
                d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07":
                d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06":  # blocked
            c_Errcnt = c_Errcnt + 1
            print('>> # blocked 에러 : ' + str(rtnChk))
        elif rtnChk_no == "S01":
            print('>> # update stop goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "S02":
            print('>> # naver noclick goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB
            print('>> # SetDB Insert error : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB
            print('>> # SetDB Update error : ' + str(rtnChk))
        elif rtnChk_no == "E01":
            c_Errcnt = c_Errcnt + 1
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK (완료) : ' + str(rtnChk))
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))

        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    print('>> IsDisplay Update (F) 품절처리 ')
                    #setDisplay(rtn_uid, 'F','1', db_con)
                    sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> Ok stock_ck update : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no[:1] == "S": 
                sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> 품절처리 Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            elif rtnChk_no == "0":
                sql = "update T_goods set stock_ck = '2' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            else:  # blocked
                sql = "update T_goods set stock_ck = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))

        if rtnChk_no[:1] == "C":
            # set_new_ip()
            # print('>> set_new_ip() ')
            print(checkIP())
            time.sleep(3)
            if c_Errcnt > 5:
                print('>> ( c_Errcnt 5 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                print(">> End : " + str(datetime.datetime.now()))
                procLogSet(db_con, in_pg, " c_Errcnt 5 over exit : " + str(asin_low))
                procEnd(db_con, db_ali, in_drive, in_pg)

    if rtnChk_no == "E99":
        return "E99"

    return "0"

# 재고 체크
def proc_asin_out_brower(in_asin_str,db_con, db_ali, in_drive, in_pg, in_pgsite):   

    chkCode = ""
    asin = ""
    cateidx = ""
    display_price = ""
    source_code = ""
    html_str = ""
    detail_soup = ""
    gallery_tmp = ""
    db_Del_Naver = ""
    priceSource = ""
    sp_asin = in_asin_str.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    display_price = sp_asin[2]
    guid = ""
    guid = sp_asin[3]
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    db_Weight = "0"
    DB_stop_update = "0"
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where uid = {0}".format(guid)
    
    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_title = rowUP[5]

        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid

        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"

        if str(db_Del_Naver) == "1":
            print('>> Del_Naver 1 (네이버 미노출상품) : ' + str(asin))
            #return "S02"

        if str(DB_stop_update) == "1":
            print('>> stop_update goods : ' + str(asin))
            return "S01"

    print('>> stop_update No goods : ' + str(asin))
    if str(guid) == '':
        print('>>>>>>>>>>>>>>>>>>>>> no guid (신규) ')
    else:
        print('>>>>>>>>>>>>>>>>>>>>> guid (존재) : ' + str(guid))

    result_goods = ""
    now_url = "https://detail.1688.com/offer/{}.html".format(asin)
    try:
        result_goods = getSource(in_drive, db_con, db_ali, in_pg, now_url)
    except Exception as e:
        print('>> proc_asin_out_brower Exception Error ')
        if str(e).find('Timed out receiving message') > -1:
            result_goods = "C02"
        if result_goods == "":
            result_goods = "D11"
        return result_goods

    if result_goods == "C02" or result_goods == "C05" or result_goods == "D01" or result_goods == "D17" or result_goods == "D11":
        return result_goods 

    ######################## goods parsing ########################
    print('>> goods parsing ######################## ')

    goods_price = "0"
    original_price = "0"

    if str(result_goods).find('data-buy-box-region="price"') == -1:
        print('>> Sold Out')
        return "D01"
    
    price_tmp = getparse(str(result_goods),'data-buy-box-region="price"','</div>')
    if str(price_tmp).find('>Price:</span>') > -1:
        goods_price = getparse(str(result_goods),'>Price:</span>','</p>')
    elif str(price_tmp).find('<p class="wt-text-title-03 wt-mr-xs-2">') > -1:
        goods_price = getparse(str(result_goods),'<p class="wt-text-title-03 wt-mr-xs-2">','</p>')

    if str(goods_price).find('<span class="currency-value">') > -1:
        goods_price = getparse(str(goods_price),'<span class="currency-value">','</span>')       
    if str(goods_price).find("<span class='currency-value'>") > -1:
        goods_price = getparse(str(goods_price),"<span class='currency-value'>","</span>")

    goods_price = str(goods_price).replace("+","").replace("USD","").replace("$","").replace(",","").strip()
    print("goods_price : {}".format(goods_price))

    # Original price    
    if str(price_tmp).find('>Price:</span>') > -1:
        original_price = getparse(str(price_tmp),'>Original Price:</span>','</p>')
    else:
        original_price = ""
    original_price = str(original_price).replace("+","").replace("USD","").replace("$","").strip()
    print("original_price : {}".format(original_price))

    if str(goods_price) == "0" or str(goods_price) == "":
        print('>> Sold Out')
        return "D01"

    ##### price check #####
    if str(result_goods).find('id="inventory-variation-select-0"') == -1:
        if float(goods_price) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 달러 미만

        if float(goods_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 달러 over

    if str(result_goods).find('Deliver to South Korea') > -1:
        print('>> Deliver to South Korea ')
    else:
        print('>> 배송비 확인불가 ')
        return "D11" 

    ship_tmp = ""
    if str(result_goods).find('Cost to ship') > -1:
        ship_tmp = getparse(str(result_goods),'Cost to ship','</div>')
        if str(ship_tmp).find('Free') > -1:
            ship_tmp = ""
    else:
        print('>> 배송비 Free 없음 (skip)')
        return "D11" 
        
    if str(ship_tmp) != "":
        print('>> 배송비 Free 없음 (skip)')
        return "D11" 

    return "0"



# Stock ###################################################################################
def set_updatelist(db_FS, db_con, db_ali, in_drive, in_pg, in_pgsite, in_ver):
###########################################################################################
    print('>> set_updatelist ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0

    # asin get
    get_asin_list2 = []
    get_asin_list2 = get_update_goods(in_pgsite, db_FS, db_con)
    print(get_asin_list2)

    if str(get_asin_list2).rfind('@') == -1:
        print('>> 우선 없데이트 처리 대상 없음. (완료)')
        return "1"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist2 = 0
    cnt_asinlist2 = len(get_asin_list2)
    rtnChk = ""
    print('>> (get_asin_list2) len :' + str(cnt_asinlist2))

    for asin_low in get_asin_list2:
        tmp_msg = ""
        allCnt = allCnt + 1

        if allCnt == 1 or allCnt == 50:
            procStockWork(db_con, in_pg, ip)            
            time.sleep(1)

        print('\n\n ----------------- < (stock check) set_updatelist [' + str(cnt_asinlist2) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_ali,in_drive,in_pg, in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_updatelist Exception Error ')
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "":
                print('>> error : ' + str(rtnChk))
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_parse_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]

        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            return "E99"

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
            if rtnChk_no != "D17":
                d17_Errcnt = 0
            elif rtnChk_no == "D17":
                d017_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07":
                d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06":  # blocked
            c_Errcnt = c_Errcnt + 1
            print('>> # blocked 에러 : ' + str(rtnChk))
        elif rtnChk_no == "S01":
            print('>> # update stop goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB
            print('>> # SetDB Insert error : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB
            print('>> # SetDB Update error : ' + str(rtnChk))
        elif rtnChk_no == "E01":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK : ' + str(rtnChk))
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))

        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))

        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        print('>> Forbidden 금지어일 경우 판매불가 상품처리 ')
                        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1', NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(
                            rtn_uid)
                        db_con.execute(sql_u1)

                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(rtn_uid)
                        db_con.execute(sql_u2)
                    else:
                        print('>> [' + str(rtn_asin) + '] setDisplay (품절 처리) :' + str(rtn_uid))
                        #setDisplay(rtn_uid, 'F', '', db_con)      
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                        print(">> sql : " + str(sql))
                        print(">> 품절 처리 OK : " + str(d_GoodsCode))
                        db_con.execute(sql)

                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no == "0":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            # blocked 경우 amazon_goods_update 테이블 regdate + 1 다음에 다시 시도
            if rtnChk_no[:1] == "C" or rtnChk_no[:1] == "Q" or rtnChk_no[:1] == "E":
                sql = "update amazon_goods_update set flg_chk = '0', regdate = regdate + 1 where guid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)
            elif rtnChk_no == "0" or rtnChk_no[:1] == "D":
                sql = "update amazon_goods_update set flg_chk = '1', upddate = getdate() where guid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))

        if rtnChk_no[:1] == "C":
            print('>> ( 접속불가 ) exit -  :' + str(asin_low))
            time.sleep(1)
            #print('\n time.sleep(1)')
            print(">> End : " + str(datetime.datetime.now()))

            procLogSet(db_con, in_pg, " 접속불가 또는 에러발생 : " + str(asin_low))
            # proc end
            procEnd(db_con, db_ali, in_drive, in_pg)


    return "0"


# Stock ###################################################################################
def set_stock_multi(db_con, db_ali, db_ali2, in_drive, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2, in_sql3):
###########################################################################################
    print('>> set_stock_multi ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(db_con, in_sql1, in_sql2, in_sql3)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(ip))
        return "11"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        tmp_msg = ""
        allCnt = allCnt + 1

        procStockWork(db_con, in_pg, ip)
        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> ----------------- < (set_stock_multi) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_ali,db_ali2,in_drive,in_pg,in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_multi proc_asin_parse_brower Exception Error ')
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "":
                print('>> error : ' + str(rtnChk))
                rtnChk = "E01"
        else:
            print('>> -- proc_asin_parse_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = ""
        rtn_uid = spm_asin[3]
        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            break

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> Unsellable product (asin delete) : ' + str(rtnChk))
            if rtnChk_no != "D17":
                d17_Errcnt = 0
            elif rtnChk_no == "D17":
                d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07":
                d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06":  # blocked
            c_Errcnt = c_Errcnt + 1
            print('>> # blocked 에러 : ' + str(rtnChk))
        elif rtnChk_no == "S01":
            print('>> # update stop goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB
            print('>> # SetDB Insert error : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB
            print('>> # SetDB Update error : ' + str(rtnChk))
        elif rtnChk_no == "E01":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK : ' + str(rtnChk))
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))


        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate from t_goods where uid = '" + str(rtn_uid) + "'"
        rs_row = db_con.selectone(sql)
        print('>> ##selectone## sql :' + str(sql))

        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_cate_idx = rs_row[0]
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_Del_Naver = rs_row[4]
            d_stock_ck = rs_row[5]
            d_regdate = rs_row[6]
            d_UpdateDate = rs_row[7]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))

            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1

            if rtnChk_no[:1] == "D":  # sold out
                # if rtnChk_no == "D05" or rtnChk_no == "D06" or rtnChk_no == "D07" or rtnChk_no == "D10":
                #     print("sold out SKIP : " + str(rtnChk_no))
                # else:
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        print('>> Forbidden 금지어일 경우 판매불가 상품처리 ')
                        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(
                            rtn_uid)
                        db_con.execute(sql_u1)

                        sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(rtn_uid)
                        db_con.execute(sql_u2)
                    else:
                        print('>> IsDisplay Update (F) 품절처리 ')
                        #setDisplay(rtn_uid, 'F','', db_con)
                        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                        print(">> sql : " + str(sql))
                        print(">> sold out OK : " + str(d_GoodsCode))
                        db_con.execute(sql)
                        
                if str(d_stock_ck) != '9':
                    sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> sold out OK : " + str(d_GoodsCode))
                    db_con.execute(sql)

            elif rtnChk_no == "0":
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)

            else:  # blocked
                sql = "update T_goods set stock_ck = '1', UpdateDate = UpdateDate - 3 where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> UpdateDate  : " + str(d_GoodsCode))
                db_con.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))

        if rtnChk_no[:1] == "C":
            # set_new_ip()
            # print('>> set_new_ip() ')
            print(checkIP())
            time.sleep(3)
            #print('>> time.sleep(3) ')

            if c_Errcnt > 5:
                print('>> ( c_Errcnt 5 over ) exit -  :' + str(asin_low))
                time.sleep(1)
                #print('\n time.sleep(1)')
                print(">> End : " + str(datetime.datetime.now()))
                #input("Key Press : ")

                procLogSet(db_con, in_pg, " c_Errcnt 5 over exit : " + str(asin_low))
                procEnd(db_con, db_ali, in_drive, in_pg)

    if rtnChk_no == "E99":
        print('>> E99 Exit : ' + str(rtnChk_no))
        return rtnChk_no

    return "0"
