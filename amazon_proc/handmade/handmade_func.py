# -*- coding: utf-8 -*-
import datetime, os, random
import socket
import socks
import http.client
import uuid
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from stem import Signal
from stem.control import Controller
import chromedriver_autoinstaller
import subprocess
import time
import re
import DBmodule_FR

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

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket
    print(">> Connected to Tor")

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into etsy_proc_log (proc_no, proc_log, proc_memo) "
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

#rfind 파싱함수
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

def getWonpirce(db_ali2, price, exchange_rate):
    final_price = 0
    price = float(price)
    dollar_price = price 
    dollar_price = abs(dollar_price)
    won_price = price * float(exchange_rate)

    sql = "select * from ali_price_ck where cate_code = 'MAIN'"
    rs = db_ali2.selectone(sql)
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

    return round(final_price, 2)


#옵션처리
def generateOptionString(db_ali2, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, exchange_rate, coupon):
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

        if str(value) == '0' or str(value) == '0.0':
            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            option_value = "(" + str(key) + ")" + replaceQueryString(option_value_dic[key])
            option_item_str.append(option_value)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))
        else:
            diff_sale_price = float(value)-float(base_price_tmp)
            base_price_marzin = getWonpirce(db_ali2, float(base_price_tmp), exchange_rate)
            value_price_marzin = getWonpirce(db_ali2, float(value), exchange_rate)
            option_marzin_price = value_price_marzin - base_price_marzin  
            option_marzin_price = round(option_marzin_price, -2)
            #option_marzin_sale_price = option_marzin_price * ((100-coupon) / 100)
            option_marzin_sale_price = option_marzin_price
            option_marzin_sale_price = int(round(option_marzin_sale_price, -2))
            
            if d_minus_opt == "1":
                if option_marzin_sale_price > 0:
                    option_marzin_sale_price = 0
                option_marzin_sale_price = option_marzin_sale_price / 2
            else:
                if option_marzin_sale_price < 0:
                    option_marzin_sale_price = 0

            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            option_value = "(" + str(key) + ")" + replaceQueryString(option_value_dic[key])
            option_item_str.append(option_value)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))

        print(">>[{}] {} : {} : [차액 {}] ( {} | {} )".format(klow, option_value, value, diff_sale_price, option_marzin_price, option_marzin_sale_price))

    #print(">> option_marzin_price_sale_dic : {} ".format(option_marzin_price_sale_dic))
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
        result = target[target_len:]
        if isNumber(result) == True :
            number_ck = True
            temp_string = result
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

def set_new_tor_ip(torKbn):
    # """Change IP using TOR"""
    if torKbn == "Y":
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
        except Exception as e:
            print(">> set_new_tor_ip except")
        print(">> set_new_tor_ip ")
    time.sleep(1)

def checkCurrIP():
    time.sleep(1)
    # proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    # res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    # print('>> Tor Current IP:', res.text)


def checkCurrIP_new(torKbn):
    time.sleep(1)
    if torKbn == "Y":
        try:
            proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
            res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
        except Exception as e:
            print(">> checkCurrIP_new except")
        else:
            print('>> Tor Current IP:', res.text)
    time.sleep(1)

# mssql null
def getQueryValue(in_value):
    if in_value == None:
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

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
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    if in_kbn == "KR":
        regStr = re.search('[가-힣]+',chkStr)
    else:
        regStr = re.search('[^. %–|<>&`()+A-Za-z0-9가-힣]+',chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result


# (사이트DB 체크) 사이트내 금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_site(target, pdb):
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

# (사이트DB 체크) 사이트내 금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_site(target, cate_idx, db_con):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'
    sql = "select ban_title_gubun, ban_title_inner, ban_title_gubun_2, ban_check, isnull(ban_cate_idx,'') from Ban_Title where ban_title = 'title' "
    print('>> (db_con) sql :' + str(sql))
    prs = db_con.select(sql)
    for rs in prs:
        ban_title_gubun = rs[0]
        ban_title_inner = rs[1]
        ban_title_gubun_2 = rs[2]
        ban_check = rs[3]
        ban_cate_idx = (rs[4]).strip()
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
        if ban_cate_idx != "":
            if str(ban_cate_idx) == str(cate_idx):
                result = result + '@' + ban_str
            else:
                result = "0"
                print(">> 금지어 제외안함 카테고리 다름 : (db){} (cateidx){}".format(ban_cate_idx, cate_idx))
        else:
            result = result + '@' + ban_str

    return result

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
    result = ""
    regStr = re.compile('[^-. %–|<>&`()+A-Za-z0-9가-힣]+')
    result = regStr.sub('', in_str)
    #print(result)

    return result

# 특수단어 제거
def replaceQueryString(in_word) :
    result = in_word.replace("'","")
    result = result.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ").replace("–","-")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","").replace("  "," ")

    return result

#goodscode
def getGoodsCode(uid,goodshead):
    result = goodshead+str(uid).zfill(10)
    return result

# contents
def generateContent(dic):
    feature_item = []
    description_item = []
    content_item = []
    description = []
    feature = []

    feature_item.append('<br><br><font color="orange"><b>Highlights</b></font><br><br>')
    description_item.append('<br><br><font color="red"><b>Description</b></font><br><br>')

    feature_item.append("".join(dic['feature']))
    feature = "".join(feature_item)
    description_item.append(dic['description'].replace("'","").replace("Description",""))
    description = "".join(description_item)

    option_img_set = []
    for key,values in dic['option_image'].items():
        if str(values) == '<br>' or str(values) == '':
            print(">> option_image values 없음 : "+str(values))
        else:
            option_img_set.append('<br><br><img src="{}"><br><br>'.format(values))
    opt_img_item = "".join(option_img_set)
    content_item.append(feature.replace("'","").replace("・","·"))
    content_item.append(opt_img_item.replace("'",""))
    content_item.append(description.replace("'","").replace("・","·"))

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
        print('>> Exception [t_goods]', e)
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
        print('>> Exception [t_goods]', e)
        return "Q02"

    return "0"

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

#DB set
def setDB_proc(in_asin, dic, db_con, db_ali2, db_price, in_pg, in_guid, exchange_rate):

    err_flg = "0"
    rtn_goodscode = ""
    print('>> setDB in_guid :' + str(in_guid))
    print('>> setDB start : ' +str(in_pg))
    print('>> [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_asin))

    goods_title = dic['goods_title']
    
    if dic['minus_opt'] == '1':
        originalprice = float(dic['price']) * float(exchange_rate)
    else:
        originalprice = float(dic['price_tmp']) * float(exchange_rate)
    print('>> price : ' + str(dic['price']))
    print('>> originalprice (rate:' +str(exchange_rate)+ ') : ' + str(originalprice))

    ##### price check #####
    if float(dic['price']) < 1:
        print('>> 1 달러 미만 (skip)')
        return "D12" + " ( " + str(dic['price']) + " ) "  # 1 달러 미만 

    # DB query
    goodsinfo_dic = dict()
    goodsinfo_dic['SiteID'] = "'rental'"
    goodsinfo_dic['DealerID'] = "'rental'"
    goodsinfo_dic['GoodsType'] = "'N'"
    goodsinfo_dic['Title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['IT_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['IT_title'])
    goodsinfo_dic['ImgB'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgM'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgS'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['naver_img'] = getQueryValue(dic['naver_img'])
    goodsinfo_dic['OptionKind'] = getQueryValue(dic['optionkind'])
    goodsinfo_dic['DeliveryPolicy'] = "'990'"
    goodsinfo_dic['State'] = "'100'"
    #########################goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
    goodsinfo_dic['price_tmp'] = getQueryValue(dic['price_tmp'])
    goodsinfo_dic['OriginalPrice'] = originalprice
    goodsinfo_dic['ali_no'] = getQueryValue(dic['ali_no'])
    goodsinfo_dic['cate_idx'] = dic['catecode']
    goodsinfo_dic['E_title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['shipping_fee'] = getQueryValue(dic['shipping_fee'])
    goodsinfo_dic['shipping_fee_tmp'] = getQueryValue(dic['shipping_fee_tmp'])
    goodsinfo_dic['shipping_weight'] = getQueryValue(dic['shipping_weight'])
    goodsinfo_dic['stock_tmp'] = getQueryValue(dic['stock_tmp'])
    goodsinfo_dic['option_input_title'] = getQueryValue(dic['option_input_title'])
    goodsinfo_dic['option_input_msg'] = getQueryValue(dic['option_input_msg'])
    goodsinfo_dic['option_input_msg_tran'] = getQueryValue(dic['option_input_msg_tran'])
    goodsinfo_dic['option_input_size'] = getQueryValue(dic['option_input_size'])
    goodsinfo_dic['option_optional_flg'] = getQueryValue(dic['option_optional_flg'])
    #goodsinfo_dic['source'] = getQueryValue(dic['source'])
    goodsinfo_dic['seller_name'] = getQueryValue(dic['seller_name'])
    goodsinfo_dic['seller_url'] = getQueryValue(dic['seller_url'])
    goodsinfo_dic['ships_from'] = getQueryValue(dic['ships_from'])
    
    many_option_ck = dic['many_option']
    if many_option_ck == '1' :
        goodsinfo_dic['many_option'] = "'1'"

    #other img
    option_img_dic = dict()
    otherimg_low = 1
    for otherimg in dic['image']:
        if otherimg_low <= 5:
            goodsinfo_dic['other_img_chk_'+str(otherimg_low)] = "'1'"
            goodsinfo_dic['other_img'+str(otherimg_low)] = getQueryValue(otherimg)
        otherimg_low += 1
        option_img_dic[otherimg_low] = otherimg

    dic['option_image'] = option_img_dic

    ##############################################
    #option (goodsinfo_option_dic)
    ##############################################
    goodsinfo_option_dic = dict()
    if dic['optionkind'] == '300' or dic['optionkind'] == 300:
        goodsinfo_option_dic['Title'] = getQueryValue(replaceQueryString(dic['option_type']))
        goodsinfo_option_dic['Items'] = dic['Items']

        if str(goodsinfo_option_dic['Items']).find('/0') > -1:
            print('>> Opt 기본옵션 /0 포함 ')
        else:
            print('>> Opt 기본옵션 /0 없음 (SKIP) ')
            print(dic['Items'])
            return "D01"

        print('>> option (type) : '+str(dic['option_type']))
        print('>> option (final) : ')
        print(goodsinfo_option_dic['Items'])

        goodsinfo_option_dic['Sort'] = 1
        goodsinfo_option_dic['ali_no'] = getQueryValue(dic['ali_no'])

    ##############################################
    #t_goods_content
    ##############################################
    goodsinfo_content_dic = dict()
    goodsinfo_content_dic['Content'] = "N" + getQueryValue(generateContent(dic))

    goodsreview = dic['review']
    goodsreview = str(goodsreview).replace("'",'"')
    goodsreview = get_replace_viewbox(goodsreview)
    goodsinfo_content_dic['ReviewContent'] = getQueryValue(goodsreview)
    goodsinfo_content_dic['ReviewRegDate'] = 'getdate()'


    ##############################################
    #t_goods_sub
    ##############################################
    goodsinfo_sub_dic = dict()
    goodsinfo_sub_dic['Product'] = getQueryValue(dic['ships_from'])
    goodsinfo_sub_dic['gall_list'] = getQueryValue(dic['gallery'])

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
    D_naver_in = ""
    procFlg = ""
    if str(in_guid) == '' or in_guid is None or in_guid == 'None':
        procFlg = "N"
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where ali_no = '{0}'".format(dic['ali_no'])
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
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), ali_no, goodscode, isnull(naver_in,0) from t_goods where uid = {0} ".format(in_guid)
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (2) (parentali_noasin) ')  

        if rows:
            procFlg = "U" 
            old_guid = rows[0]
            ck_isdisplay = rows[1]
            ck_delnaver = rows[2]
            D_ali_no = rows[3]
            D_goodscode = rows[4]
            D_naver_in = rows[5]
            rtn_goodscode = D_goodscode
        else:
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))
            return "E01"

    if procFlg == "N":
        goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])        
        goodsinfo_dic['confirm_goods'] = 1
        goodsinfo_dic['naver_price_ck'] = "'0'"
        #####################################################################
        print(">> ## setDB New Insert : " + str(in_asin))
        #####################################################################
        #insert t_goods
        try:
            db_con.insert('t_goods',goodsinfo_dic)
            print('>> ## t_goods  insert ')
        except Exception as e:
            print('>> Exception [t_goods]', e)
            err_flg = "1"
            return "Q01"

        time.sleep(1)
        #goodscode #######################
        sql = "select top 1 uid from t_goods where ali_no = '{0}'".format(dic['ali_no'])
        coderow = db_con.selectone(sql)
        now_guid = coderow[0]         

        new_goodscode = getGoodsCode(now_guid, 'H')
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

        if dic['optionkind'] == '300' or dic['optionkind'] == 300 :
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

        #T_GOODS_IMG_DOWN #######################
        if dic['img_down_flg'] == "1":
            imgTemp = ""
            if dic['naver_img'] == "" or dic['naver_img'] is None:
                imgTemp = getQueryValue(dic['mainimage'])
            else:
                imgTemp = getQueryValue(dic['naver_img'])

            print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Start ")
            imgSql = "select GoodsCode from T_GOODS_IMG_DOWN where GoodsCode = '" + str(new_goodscode) + "'"
            imgRows = db_con.selectone(imgSql)

            if not imgRows:
                sqlImg = " insert into T_GOODS_IMG_DOWN (GoodsCode, GoodsUid, ImgPath, cate_idx) values ('" + str(new_goodscode) + "'," +str(now_guid)+ "," + str(imgTemp) + "," +str(dic['catecode'])+") "
                db_con.execute(sqlImg)
            else:
                sqlImg = " update T_GOODS_IMG_DOWN set ImgPath = " + str(imgTemp) + ", GoodsUid = " +str(now_guid)+ ", cate_idx = " +str(dic['catecode'])+ ", regDate=getdate() where  GoodsCode = '" + str(new_goodscode) + "'"
                db_con.execute(sqlImg)
            print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Ok ")


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
        goodsinfo_dic['naver_price_ck'] = "'0'"
        if dic['db_goodscode'] != "" or D_goodscode != "":
            if D_goodscode == "":
                D_goodscode = dic['db_goodscode']
            ## [naver_price 테이블 ] change_price 최저가 확인후 처리  
            sql_price = "select price, DATEDIFF(dd,isnull(update_date, regdate), getdate()) as diff_day from change_price where flag = '4' and goodscode = '{}'".format(D_goodscode)
            row = db_price.selectone(sql_price)
            if row:
                naver_rowprice = row[0]
                diff_day = row[1]
                print(">> [{}] | low_price : {} | naver_rowprice : {} | diff_day : {}".format(D_goodscode, dic['low_price'], naver_rowprice, diff_day))
                # change_price 최저가 비교
                if int(dic['low_price']) > int(naver_rowprice):
                    if diff_day > 90:
                        print(">> change_price 업데이트가 90일 이상지난 상품으로 실제 가격 Update : {}".format(diff_day))
                    elif int(dic['low_price']) * 0.85 > int(naver_rowprice):
                        print(">> change_price 최저가 15프로 이상 차액으로 실제 가격 Update : {} ".format(int(dic['low_price']) * 0.85))
                    else:
                        ## change_price --->  minus_check = 1  update  처리 
                        slq_price_up = "update change_price set minus_check = '1' where goodscode = '{}'".format(D_goodscode)
                        print(">> [naver_price 테이블 ] change_price --->  minus_check = 1 update  처리 : {}".format(D_goodscode))
                        print(">> [t_goods 테이블 ] pirce 변경 (SKIP) : {}".format(D_goodscode))
                        db_price.execute(slq_price_up)
                        goodsinfo_dic['naver_price_ck'] = "'1'"

        if goodsinfo_dic['naver_price_ck'] == "'0'":
            # change_price 최저가 없음
            goodsinfo_dic['Price'] = getQueryValue(dic['goodsmoney'])
            goodsinfo_dic['naver_price_ck'] = "'0'"

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

        if dic['optionkind'] == 300 or dic['optionkind'] == '300':
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


        # #T_GOODS_IMG_DOWN #######################
        if dic['img_down_flg'] == "1":
            imgTemp = ""
            if dic['naver_img'] == "" or dic['naver_img'] is None:
                imgTemp = getQueryValue(dic['mainimage'])
            else:
                imgTemp = getQueryValue(dic['naver_img'])

            print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Start ")
            imgSql = "select GoodsCode from T_GOODS_IMG_DOWN where GoodsCode = '" + str(D_goodscode) + "'"
            imgRows = db_con.selectone(imgSql)

            if not imgRows:
                sqlImg = " insert into T_GOODS_IMG_DOWN (GoodsCode, GoodsUid, ImgPath, cate_idx) values ('" + str(D_goodscode) + "'," +str(old_guid)+ "," + str(imgTemp) + "," +str(dic['catecode'])+") "
                print(">> sqlImg : " +str(sqlImg))
                db_con.execute(sqlImg)
            else:
                sqlImg = " update T_GOODS_IMG_DOWN set GoodsUid = " +str(old_guid)+ ", ImgPath = " + str(imgTemp) + ", cate_idx = " +str(dic['catecode'])+ ", regDate=getdate() where GoodsCode = '" + str(D_goodscode) + "'"
                print(">> sqlImg : " +str(sqlImg))
                db_con.execute(sqlImg)
            print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Ok ")


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
            # if str(ck_delnaver) == "0":
            print('>> IsDisplay Update (품절 -> 노출)')
            sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = null, stock_ck_cnt = '0', UpdateDate=getdate() where uid = {0}".format(old_guid)
            #print('>> setDisplay : ' + str(sql))
            try:
                db_con.execute(sql)
                print('>> ## update_execute ')
            except Exception as e:
                print('>> Exception [t_goods]', e)
                return "Q02"

        # 네이버 노출 상품이고, change_price 최저가 없고, OriginalPrice 가 변경되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : U)
        if str(D_naver_in) == "1" and goodsinfo_dic['naver_price_ck'] == "'0'" and ( float(dic['db_OriginalPrice']) != float(goodsinfo_dic['OriginalPrice']) ):
            proc_ep_insert(D_goodscode,'U')
        # # 네이버 노출 상품이고 품절 -> 노출의 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : U)
        # elif str(D_naver_in) == "1" and ck_isdisplay == "F" and str(ck_delnaver) == "0":
        #     proc_ep_insert(D_goodscode,'U')

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
    result = ""
    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)
    if (regStr):
        result = "1"
    else:
        result = "0"
    return result

def repDesc(in_description):
    desc = str(in_description).replace("https://www.etsy.com/shop/","").replace("http://www.etsy.com/shop/","").replace("https://etsy.me/","").replace("https://www.etsy.com/listing/","")
    desc = desc.replace("www.etsy.com/shop/","").replace("www.etsy.com/listing/","").replace("etsy.me","").replace("#reviews","").replace("www.etsy.com","").replace(".com","")
    desc = desc.replace('Express Shipping','').replace('https:\\/\\/','').replace('https:','').replace('www','').replace('gmail','')
    desc = desc.replace('PayPal','').replace('Instagram','').replace('instagram','').replace('Facebook','').replace('facebook','').replace('Follow us','').replace('Credit cards','').replace('gift cards','')
    desc = desc.replace('\\n','<br>').replace('"','').replace('offer 100% Money Back','').replace('Money Back','')
    desc = desc.replace('\\u2605','★').replace('\\u2665','♥').replace('\\u2022','`').replace('\\u201d','`').replace('\\u2013','–').replace('\\u00b7','·').replace('\\','')
    desc = desc.replace('\\u201c','').replace('/shop/','').replace('?ref=seller-platform','').replace('ion_id=','').replace('Paypal','').replace('Ebay','')
    desc = desc.replace('refund','').replace('Refund','').replace('youtube.com','').replace('youtube','').replace('youtu.be','')
    return desc.strip()


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


def procIpChange(maxCnt, torKbn):
    wCnt = 0 
    while wCnt < maxCnt:
        # set_new_ip()
        # print(checkIP())
        set_new_tor_ip(torKbn)
        checkCurrIP_new(torKbn)
        time.sleep(2)
        wCnt = wCnt + 1

def getSource(in_drive, db_con, db_ali, in_pg, now_url):

    print('>> now_url : ' + str(now_url)) 
    try:
        in_drive.get(now_url)
    except Exception as e:
        print(">> Exception : {}".format(e))
    time.sleep(random.uniform(3.5,4.5))     

    result = ""
    result = in_drive.page_source
    time.sleep(0.5)
    
    if str(result).find('HTTP ERROR 429') > -1:
        print('>> Connect Error ')
        return "E99"       

    # if str(result).find('data-id="gnav-search-submit-button"') > -1 and str(result).find('data-buy-box-listing-title="true">') > -1:
    if str(result).find('data-id="gnav-search-submit-button"') > -1 and str(result).find('data-buy-box-listing-title="true"') > -1:
        print('>> Connect Ok ')

        if str(result).find('Deliver to South Korea') > -1:
            print('>> Deliver to South Korea ')
        elif str(result).find('shipping to South Korea') > -1:
            print('>> shipping to South Korea ')
        elif str(result).find('Change shipping country') > -1:
            print('>> Change shipping country (Korea 배송 불가) ')
            return "D11" 
        else:
            time.sleep(1)
            kr_flg = "0"
            try:
                # in_drive.find_element_by_css_selector('#shipping-and-returns-div > div > div.wt-grid.wt-mb-xs-3 > div.wt-grid__item-xs-12.wt-text-gray > button').click()
                in_drive.find_element(By.CSS_SELECTOR, '#shipping-and-returns-div > div > div.wt-grid.wt-mb-xs-3 > div.wt-grid__item-xs-12.wt-text-gray > button').click()
                time.sleep(1)
                list_country = getparse(str(in_drive.page_source),'<optgroup label="Choose country">','</optgroup>')
                if list_country.find('South Korea') > -1:
                    kr_flg = "1"
                sp_list_country = str(list_country).split('<option ')
                cnt = 0
                for ea_coutry in sp_list_country:
                    countryValue = getparse(str(ea_coutry),'value="','"')
                    countryName = getparse(str(ea_coutry),'">','</option>')
                    if countryName == "South Korea":
                        print(">> cnt : {} | countryName : {} | countryValue : {}".format(cnt, countryName, countryValue))
                        break
                    cnt = cnt + 1

                # in_drive.find_element_by_xpath('//*[@id="estimated-shipping-country"]/optgroup/option['+str(cnt)+']').click()
                in_drive.find_element(By.XPATH, '//*[@id="estimated-shipping-country"]/optgroup/option['+str(cnt)+']').click()
                time.sleep(1)
                #delievey_to = in_drive.find_element_by_xpath('//*[@id="estimated-shipping-country"]/optgroup/option[216]').text
                # in_drive.find_element_by_xpath('//*[@id="estimated-shipping-submit-button"]').click()
                in_drive.find_element(By.XPATH, '//*[@id="estimated-shipping-submit-button"]').click()
                time.sleep(2)
            except TimeoutException as ex:
                print('>> TimeoutException select country  ')
                result = "E99"                      
            except Exception as e:
                print('>> Exception select country  ')
                if kr_flg == "1":
                    input(">> Please Select country : ")
                result = ""
            else:
                time.sleep(1)
                result = in_drive.page_source
                if str(result).find('Deliver to South Korea') > -1:
                    print('>> Deliver to South Korea ')
                else:
                    print('>> 배송비 확인불가 ')
                    return "D11"  
            if result == "":
                print('>> Connect Error ')
                return "D11"

    elif str(result).find('Items sold by Etsy sellers') > -1:
        print('>> sold out (Items sold by Etsy sellers) ')
        return "D01"
    elif str(result).find('Sorry, this item is unavailable') > -1:
        print('>> sold out (this item is unavailable) ')
        return "D17"       
    elif str(result).find('Sorry, this item and shop are currently unavailable') > -1:
        print('>> sold out (this item and shop are currently unavailable)')
        return "D01"
    elif str(result).find('Sorry, this item is sold out') > -1:
        print('>> sold out (this item is sold out)')
        return "D01"
    elif str(result).find('This shop is taking a short break') > -1:
        print('>> sold out (This shop is taking a short break) ')
        return "D01"
    elif str(result).find('A stitch has gone awry.') > -1:
        print('>> sold out (A stitch has gone awry.) ')
        return "D01"
    else:
        with open(os.getcwd() + "/log/handmade_C02.html","w",encoding="utf8") as f: 
            f.write(str(result))
        chkCode = "C02"
        return "C02"

    if str(in_drive.page_source).find('Deliver to South Korea') > -1:
        print('>> Deliver to South Korea ')
    else:
        print('>> 배송비 확인불가 ')
        return "D11"

    print(">> Browser Count : {}".format(len(in_drive.window_handles)))
    if str(socket.gethostbyname(socket.gethostname())).strip() != "222.104.189.18":
        if len(in_drive.window_handles) != 1:
            print(">> Browser Close : {}".format(len(in_drive.window_handles)))
            procLogSet(db_con, in_pg, ">> ( Browser Count) : " + str(len(in_drive.window_handles)))  
            procEnd(db_con, db_ali, in_drive, in_pg)

    result = ""
    result = in_drive.page_source
    time.sleep(1)
    #########################################################################
    if str(result).find('HTTP ERROR ') > -1:
        print('>> HTTP ERROR ')
        print('>> C05 blocked ')
        return "C05"  # blocked

    if str(result).find('data-buy-box-listing-title="true"') == -1:
        print('>> detail_soup No')
        print('>> C02 blocked ')
        return "C02"  # Connect error

    if str(result).find('HTTP ERROR 429') > -1:
        print('>> Connect Error ')
        return "E99"  

    return str(result)


def get_goods_price(in_source):
    goods_price = ""
    price_tmp = getparse(str(in_source),'data-buy-box-region="price"','</div>')
    if str(price_tmp).find('>Price:</span>') > -1:
        goods_price = getparse(str(in_source),'>Price:</span>','</p>')
    elif str(price_tmp).find('<p class="wt-text-title-03 wt-mr-xs-2">') > -1:
        goods_price = getparse(str(in_source),'<p class="wt-text-title-03 wt-mr-xs-2">','</p>')
    elif str(price_tmp).find('<p class="wt-text-title-03 wt-mr-xs-1">') > -1:
        goods_price = getparse(str(in_source),'<p class="wt-text-title-03 wt-mr-xs-1">','</p>')

    if str(goods_price).find('<span class="currency-value">') > -1:
        goods_price = getparse(str(goods_price),'<span class="currency-value">','</span>')
    if str(goods_price).find("<span class='currency-value'>") > -1:
        goods_price = getparse(str(goods_price),"<span class='currency-value'>","</span>")
    if str(goods_price).find("-") > -1:
        goods_price = getparse(str(goods_price),"","-")       
    if str(goods_price).find("$") > -1:
        goods_price = getparse(str(goods_price),"$","")
        if str(goods_price).find("$") > -1:
            goods_price = getparse(str(goods_price),'','$').replace('-','')
    if str(goods_price).find("USD") > -1:
        goods_price = getparse(str(goods_price),"USD","")

    goods_price = str(goods_price).replace('<span class="">','').replace('</span>','').replace('\n','').strip()
    return goods_price

def proc_asin_parse_brower(in_asin_str,db_con, db_ali, db_ali2, db_price, in_drive, in_pg, in_pgsite):   
    countryKbn = ""
    asin = ""
    cateidx = ""
    gallery_tmp = ""
    db_Del_Naver = ""
    sp_asin = in_asin_str.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    display_price = sp_asin[2]
    guid = ""
    guid = sp_asin[3]
    db_org_title = ''
    db_title = ''
    db_order_ck = ''
    db_goodscode = ''
    db_OriginalPrice = 0
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    db_Weight = "0"
    DB_stop_update = "0"
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        db_org_title = ''
        db_title = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, order_ck, isnull(OriginalPrice,0) from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, order_ck, isnull(OriginalPrice,0) from t_goods where uid = {0}".format(guid)

    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_title = rowUP[6]
        db_order_ck = rowUP[7]
        db_OriginalPrice = rowUP[8]

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

    result = ""
    now_url = "https://www.etsy.com/listing/" + str(asin) + "/"

    try:
        result = getSource(in_drive, db_con, db_ali, in_pg, now_url)
    except Exception as e:
        print('>> Error : '+str(e))
        result = "E99"
    else:    
        print('>> getSource Ok : {}'.format(now_url))

    if result == "C02" or result == "C05" or result == "D01" or result == "D17" or result == "D11" or result == "E99":
        return result 
    
    if result == "":
        return "E99"

    ######################## goods parsing ########################
    print('>> goods parsing ######################## ')

    if str(result).find('data-buy-box-region="price"') == -1:
        print('>> Sold Out')
        return "D01"

    if str(result).find('Sorry, this item is unavailable') > -1:
        print('>> sold out (this item is unavailable) ')
        return "D17"       
    elif str(result).find('Sorry, this item and shop are currently unavailable') > -1:
        print('>> sold out (this item and shop are currently unavailable)')
        return "D01"
    elif str(result).find('Sorry, this item is sold out') > -1:
        print('>> sold out (this item is sold out)')
        return "D01"
    elif str(result).find('This shop is taking a short break') > -1:
        print('>> sold out (This shop is taking a short break) ')
        return "D01"
    elif str(result).find('This shop is taking a short break') > -1:
        print('>> sold out (This shop is taking a short break)')
        return "D01"
    elif str(result).find('A stitch has gone awry.') > -1:
        print('>> sold out (A stitch has gone awry.) ')
        return "D01"

    goods_price = "0"
    original_price = "0"

    goods_price = get_goods_price(result)
    goods_price = regRemoveText(goods_price)
    goods_price = str(goods_price).replace(" ","").replace("+","").replace("USD","").replace("$","").replace(",","").replace("\n","").strip()
    print("goods_price : {}".format(goods_price))

    # Original price  
    price_tmp = getparse(str(result),'data-buy-box-region="price"','</div>')  
    price = getparse(price_tmp,'Price:','</p>').replace("</span>","\n").strip()
    if str(price_tmp).find('>Price:</span>') > -1:
        original_price = getparse(str(price_tmp),'>Original Price:</span>','</p>')
        if original_price.find('-'):
            original_price = getparse(str(original_price),'','-')
        if str(original_price).find("$") > -1:
            original_price = getparse(str(original_price),"$","")
            if str(original_price).find("$") > -1:
                original_price = getparse(str(original_price),"","$").replace("-","")
    else:
        original_price = "0"

    print(">> {} : {} ".format(price, original_price))
    original_price = regRemoveText(original_price)
    original_price = str(original_price).replace(" ","").replace("+","").replace("USD","").replace("$","").replace(",","").replace("\n","").strip()

    if goods_price == "": goods_price = "0"
    if original_price.replace(".",'').isdigit() == True:
        if float(original_price) > float(goods_price):
            goods_price = original_price

    if str(goods_price) == "0" or str(goods_price) == "":
        print('>> Sold Out')
        return "D22"

    ##### price check #####
    if str(result).find('id="inventory-variation-select-0"') == -1:
        if float(goods_price) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 달러 미만

        if float(goods_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 달러 over

    # Korea 배송 
    if str(result).find('Deliver to South Korea') > -1:
        print('>> Deliver to South Korea ')
    elif str(result).find('shipping to South Korea') > -1:
        print('>> shipping to South Korea ')
    elif str(result).find('Change shipping country') > -1:
        print('>> Change shipping country (Korea 배송 불가) ')
        return "D11" 
    else:
        print('>> Korea 배송 확인불가 ')
        return "D11" 

    ########### shipping_fee ###########
    # Cost to ship (배송비)
    ship_tmp = "0"
    if str(result).find('Cost to ship') > -1:
        ship_tmp = getparse(str(result),'Cost to ship','</div>')
        if str(ship_tmp).find('Free') > -1:
            ship_tmp = "0"
        else:
            if ship_tmp.find("USD") > -1:
                print(">> 배송비 USD Ok ")
            elif ship_tmp.find("$") > -1:
                print(">> 배송비 $ Ok ")
            else:
                print('>> 배송비 (USD 없음) Currency 확인필요 (SKIP)')
                return "D11" 
            if ship_tmp.find("<span class='currency-value'>") > -1:
                ship_tmp = getparse(str(ship_tmp),"<span class='currency-value'>","</span>")
            else:
                ship_tmp = getparse(str(ship_tmp),'<span class="currency-value">','</span>')
        print(">> ship_tmp : {}".format(ship_tmp))
    elif str(result).find('<span data-estimated-shipping') > -1:
        ship_tmp = getparse(str(result),'<span data-estimated-shipping','</div>')
        ship_tmp = getparse(str(ship_tmp),'>','')
        print('>> 배송비 체크')
        if str(ship_tmp).find('Free') > -1:
            ship_tmp = "0"
        else:
            if ship_tmp.find("<span class='currency-value'>") > -1:
                ship_tmp = getparse(str(ship_tmp),"<span class='currency-value'>","</span>")
            else:
                ship_tmp = getparse(str(ship_tmp),'<span class="currency-value">','</span>')
    else:
        if str(result).find('Shipping and return policies') > -1:
            ship_tmp = getparse(str(result),'Shipping and return policies','Deliver to ')
        if str(ship_tmp).find('Free shipping') > -1:
            ship_tmp = "0"
        else:
            print('>> 배송비 Cost to ship 없음 (SKIP)')
            return "D11" 

    if str(ship_tmp) != "0":
        print('>>유료 배송비 상품 : {}'.format(ship_tmp))
        ship_tmp = str(ship_tmp).replace(",","").strip()
        if ship_tmp.replace('.','').isdigit() == False:
            print(">> 유료배송비 숫자인지 확인필요 SKIP : {}".format(ship_tmp))
            return "D11" + " ( " + str(ship_tmp) + " ) " 

        if float(ship_tmp) > 20:
            print(">> 유료배송비 20달러 이상 SKIP : {}".format(ship_tmp))
            return "D11" + " ( " + str(ship_tmp) + " ) " 
        else:
            print(">> 유료배송비 : {}".format(ship_tmp))

        if db_order_ck == '1':
            print(">> 유료배송비 (주문이력있음) 진행 : {}".format(ship_tmp))
        else:
            ori_title = getparse(str(result), 'data-buy-box-listing-title="true"','</h1>')
            ori_title = getparse(str(ori_title), '>','')
            if str(ori_title).lower().find("westwood ") > -1:
                print(">> title WESTWOOD 포함 상품 ")
                return "D21"

            if str(ori_title).find("Vintage ") > -1:
                print(">> title 빈티지 포함 상품 (유료 배송비도 파싱하기) ")

    # Seller Contact (판매자)
    seller_tmp = ""
    seller_name = ""
    seller_url = ""
    if str(result).find('Meet your seller') > -1:
        seller_tmp = getparse(str(result),'Meet your seller','class="other-info"')
        seller_name = getparse(str(seller_tmp),'data-to_user_display_name="','"').strip()
        seller_url = getparse(str(seller_tmp),'rel="nofollow"','</p>')
        seller_url = getparse(str(seller_url),'href="','"').replace("'","`").strip()
    print("seller_name : {} | seller_url : {}".format(seller_name, seller_url))

    if str(seller_tmp) != "":
        print('>> No seller info )')

    ##### gallery #########################
    gallery_tmp = get_galleryGoods(str(result), asin)
    if gallery_tmp == "1":
        print('>> gallery no')
    else:
        print('>> gallery goodscode : ' + str(gallery_tmp))

    ##### review #########################
    rtn_reviews_arr = []
    if str(result).find('No customer reviews') > -1:
        pass
        #print('>> No customer reviews')
    else:
        reviews = getparse(str(result),'data-review-region="','<div class="other-info">')
        reviews_view = get_Review(reviews, asin)
        # with open("aa_etsy_reviews_view.html","w", encoding="utf8") as f:
        #     f.write(str(reviews_view))
        #reviews_photo = getparse(str(result),'<div data-appears-component-name="customer_photos">','<div class="other-info">')
        rtn_reviews_arr = reviews_view
        # print('>> reviews OK : ' + str(rtn_reviews_arr))
        print('>> reviews OK ')

    #print('>> Sale Goods')
    goods = dict()
    ########### price / gallery / review ###########
    goods['catecode'] = str(cateidx)
    goods['price'] = float(goods_price)
    goods['price_tmp'] = float(goods_price)
    goods['gallery'] = str(gallery_tmp)
    goods['review'] = rtn_reviews_arr
    goods['guid'] = str(guid)
    goods['db_Weight'] = str(db_Weight)
    goods['db_title'] = str(db_title)
    goods['db_org_title'] = str(db_org_title)
    #goods['source'] = str(result).replace("'","")
    goods['seller_name'] = str(seller_name)
    goods['seller_url'] = str(seller_url)
    goods['shipping_fee_tmp'] = str(ship_tmp)
    goods['db_goodscode'] = str(db_goodscode)
    goods['db_OriginalPrice'] = float(db_OriginalPrice)

    in_old_title = goods['db_title']
    in_org_title = goods['db_org_title']
    goods['ali_no'] = asin
    in_price = float(goods['price'])
    goods['price_tmp'] = float(in_price)
    base_min_price = in_price
    base_top_price = in_price

    # title
    ori_title = ""
    chk_title = ""
    ori_title = getparse(str(result), 'data-buy-box-listing-title="true"','</h1>')
    ori_title = getparse(str(ori_title), '>','')
    print('>> title(ORI) : ' + str(ori_title[:80]))

    chk_title = get_replace_title(ori_title)
    if len(chk_title) < 5:
        print('>> title len < 5 ')
        return "D02"
    
    time.sleep(1)
    ##############################
    dic_tran = dict()
    py_coupom = ""
    exchange_rate = "1300"
    img_down_flg = ""

    sql = " select tran_name1, tran_url1, tran_name2, tran_url2, tran_flg, yan_tran_id, exchange_rate, coupon, img_down_flg from python_version_manage where name = 'goods' "
    row = db_con.selectone(sql)
    if not row:
        print(">> python_version_manage 오류 ")
        return "E02"
    else:
        dic_tran['tran_name1'] = row[0]
        dic_tran['tran_url1']  = row[1]
        dic_tran['tran_name2']  = row[2]
        dic_tran['tran_url2']  = row[3]
        dic_tran['tran_flg']  = row[4]
        dic_tran['yan_tran_id']  = row[5]
        exchange_rate = row[6]
        py_coupom = row[7]
        img_down_flg = row[8]

    goods['exchange_rate'] = exchange_rate    
    goods['img_down_flg'] = img_down_flg        

    ########### title ###########
    goods_title = chk_title.replace(r'\x26', ' & ').replace("'", "`").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('–','-').replace('・','.')
    goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '').replace('  ',' ')
    goods_title = replaceQueryString(goods_title)
    goods_title = replaceTitle(goods_title, db_ali)
    if goods_title[-1:] == ".":
        goods_title = goods_title[:-1]
    if goods_title[-1:] == "|":
        goods_title = goods_title[:-1]
    goods_title = str(goods_title).replace("  ", " ").strip()

    print('>> goods_title (final) : ' + str(goods_title[:80]))
    if str(goods_title).strip() == "" or len(goods_title) < 5:
        print('>> no title ')
        return "D02"

    ########### title (checkForbidden_new) ###########
    forbidden_flag = checkForbidden_new(chk_title, db_ali)
    if str(forbidden_flag) == "0":
        pass
        #print('>> No checkForbidden_new: ' + str(forbidden_flag))
    else:
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # (사이트 DB) title 금지어 체크 ###########
    forbidden_flag_site = checkForbidden_site(chk_title, cateidx, db_con)
    if str(forbidden_flag_site) != "0":
        print('>> checkForbidden_site : '+str(forbidden_flag_site))
        return "D03 :" + " ( site: " + forbidden_flag_site[2:] + " ) "

    goods['forbidden'] = 'F'
    goods['goods_title'] = goods_title

    in_org_title = str(in_org_title).replace(",","").upper()
    if in_org_title == goods_title: # 기존 org title 과 파싱 title 비교
        print(">> 타이틀 변화없음 ")
        goods['goods_title'] = in_old_title # 기존 DB title 그대로 반영 

    goods['IT_title'] = goods_title

    ########### image ###########
    mainimage = ""
    img_items_str = getparse(str(result), ',"image":[',']')
    image_data = str(img_items_str).split("},{")
    print("image_data len : {}".format(len(image_data)))
    image_list = []
    ilow = 0
    for img_ea in image_data:
        imgUrl = getparse(str(img_ea),'contentURL":"','"').replace('\\','')
        if imgUrl not in image_list:
            if str(imgUrl).strip() != "":
                ilow = ilow + 1
                image_list.append(imgUrl)
                if mainimage == "":
                    mainimage = imgUrl

    if str(mainimage).strip() == "":
        print('>> no Img ')
        return "D19"  # No img 

    goods['naver_img'] = mainimage
    goods['mainimage'] = mainimage

    goods['image'] = image_list
    print("mainimage : {}".format(mainimage))
    #print("image_list : {}".format(image_list))
    print(">> Url : {}".format(now_url))

    ########### feature ###########
    highlights = get_highlights(result)
    print("highlights : {}".format(highlights[:50]))
    # with open("aa_etsy_highlights.html","w", encoding="utf8") as f:
    #     f.write(str(highlights))    
    
    goods['feature'] = highlights
    print('>> feature OK ')
    #print('>> feature : '+str(featureset))


    ########### Ships from ###########
    ships_from = ""
    ships_from = getparse(str(result),'Cost to ship','<div class="other-info">')
    ships_from = getparse(str(ships_from),'Ships from ','</div>').strip()
    if str(ships_from).strip() == "":
        ships_from = ''
    elif str(ships_from).find("Korea") > -1:
        print(">> ships_from : South Korea (Skip) D20 ")
        return "D20"
    elif str(ships_from).find(",") > -1:
        ships_from = 'United States'
    goods['ships_from'] = ships_from

    ########### description ###########
    description = ""
    description = getparse(str(result),'"description":"',',"image"')
    description = repDesc(description)
    goods['description'] = description
    print("description : {}".format(description[:100]))
    # with open(os.getcwd() + "/log/description1_"+str(asin)+".html","w", encoding="utf8") as f:
    #     f.write(str(description))    

    ########### stock ###########
    stock = "0"
    stock_tmp = getparse(str(result),'data-buy-box-price-spinner="">','Add to cart')
    stock_tmp = getparse(str(stock_tmp),'class="wt-display-flex-xs','</p>')
    stock = getparse(str(stock_tmp),'<b>','</b>')
    print("stock : {}".format(stock))
    goods['stock_tmp'] = stock

    ########### option ###########
    #   https://www.etsy.com/listing/886301407/?variation0=2310285822&variation1=1895154966 
    
    goods['minus_opt'] = ""
    goods['coupon'] = "" 
    goods['many_option'] = '0'
    goods['Items'] = ""
    goods['option_type'] = ""
    min_price = 0
    top_price = 0

    d_minus_opt = ""
    opmaxlen = 0
    option_count = 0
    option_kubun = "0"
    option_type_str = ""
    opmaxlen = 0
    option_optional = "" 
    option_input_title = ""
    option_input_msg = ""
    option_input_msg_tran = ""
    option_input_size = ""
    option_optional_flg = "0"  # 0: optional 없음 , 1: optional 필수 : 2: optional 선택

    ######### catecode의 minus_opt 플래그 확인 #############################
    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),'') from t_category where CateCode = '{0}'".format(cateidx)
    rsCate = db_con.selectone(sql2)
    if rsCate:
        d_minus_opt = rsCate[0]
        d_minus_opt = str(d_minus_opt).strip()
        d_coupon = rsCate[1]
    #print('>> (DB) d_minus_opt : '+str(d_minus_opt))
    print('>> (DB) coupon : '+str(d_coupon))

    option_value_dic = dict()
    option_price_dic = dict()

    option_input_title = getparse(str(result),'id="personalization-field-label">','<')
    option_optional = getparse(str(result),'<span id="personalization-optional-label">','</span>')
    print("option_optional : {}".format(option_optional))
    option_input_msg = getparse(str(result),'<p id="personalization-instructions"','</p>')
    option_input_msg = getparse(str(option_input_msg),'">','')

    if str(option_input_title) != "" and str(option_input_title).find("(optional)") > -1:
        option_optional_flg = "2" # 선택 입력 옵션
        #option_input_title = option_input_title + " (optional)"
    elif str(option_input_title) != "" and str(option_optional) == "":
        option_optional_flg = "1" # 필수 입력 옵션
        print(" Option Check (필수 입력 옵션 skip): D77")
        return "D77"
    # option : option_input_size
    option_input_size = getparse(str(result),'listing-page-personalization-character-remaining"','</div>')
    option_input_size = getparse(str(option_input_size),'class="wt-text-caption wt-text-right-xs">','')
    if option_input_size.isdigit == False:
        option_input_size = ""
    option_input_msg = str(option_input_msg).replace("'","").replace("<br>"," ").replace("  "," ").strip()
    option_input_msg = option_input_msg[:200]

    goods['option_input_title'] = option_input_title
    goods['option_input_msg'] = option_input_msg
    goods['option_input_msg_tran'] = option_input_msg_tran
    goods['option_input_size'] = option_input_size
    goods['option_optional_flg'] = option_optional_flg

    print(">> option_input_title : {}".format(option_input_title))
    print(">> option_input_msg : {}".format(option_input_msg))
    print(">> option_input_size : {}".format(option_input_size))
    print(">> option_optional_flg : {}".format(option_optional_flg))

    # 옵션수 체크
    option_source = ""
    option_source = getparse(str(result),'"listing-page-variations"','class="add-to-cart-form"')
    if result.find('listing-page-quantity') > -1:
        option_source = getparse(str(option_source),'','listing-page-quantity')
    sp_opt = option_source.split('id="variation-selector')
    print(">> sp_opt : {}".format(len(sp_opt)-1))
    option_count = 0
    if len(sp_opt)-1 == 0: 
        # No Option
        option_kubun = "0" # 옵션 없음
        print(">> No Option Goods : {}".format(asin))
        goods['many_option'] = '0'
        option_ck = None    
    else:
        option_ck = "300"
        goods['many_option'] = '1'
        option_valDic = dict()
        if len(sp_opt)-1 == 2: # 옵션 2개일 경우 
            option_count = 2
            option_kubun = "2" # 옵션 2개일 경우
            url_option2_tmp = ""
            url_option2_tmp = getparse(str(option_source),'id="variation-selector-1"','').replace('\n','')
            if url_option2_tmp.find('</select>') > -1:
                url_option2_tmp = getparse(url_option2_tmp,'','</select>')
            if str(url_option2_tmp).find('- USD') > -1 or str(url_option2_tmp).find('- $') > -1:
                print(" 2 Option price check : D20")
                return "D20"

            sp_url_opt2_val = str(url_option2_tmp).split('</option>')
            for ea_url_opt2_val in sp_url_opt2_val:
                url_opt2_val = ""
                url_opt2_name = ""
                url_opt2_val = getparse(str(ea_url_opt2_val),'value="','"')
                if url_opt2_val == "":
                    continue
                url_opt2_name = getparse(str(ea_url_opt2_val),'>','')
                if str(url_opt2_name).find('Sold out') > -1:
                    print(">> (SKIP) Sold out [Option Sel] url_opt2_val (Sold out) : {} | {}".format(url_opt2_val, url_opt2_name))
                    continue
                else:
                    print(">> [Option Sel] url_opt2_val : {} | {}".format(url_opt2_val, url_opt2_name))
                    break

            url_option1_tmp = ""
            url_option1_tmp = getparse(str(option_source),'id="variation-selector-0"','id="variation-selector-1"').replace('\n','')
            if url_option1_tmp.find('class="add-to-cart-form"') > -1:
                url_option1_tmp = getparse(str(url_option1_tmp),'','class="add-to-cart-form"')
            if url_option1_tmp.find('</select>') > -1:
                url_option1_tmp = getparse(url_option1_tmp,'','</select>')
            if str(url_option1_tmp).find('- USD') > -1 or str(url_option1_tmp).find('- $') > -1:
                print(" 2 Option price check : D20")
                return "D20"

            sp_url_opt1_val = str(url_option1_tmp).split('</option>')
            for ea_url_opt1_val in sp_url_opt1_val:
                url_opt1_val = ""
                url_opt1_name = ""
                url_opt1_val = getparse(str(ea_url_opt1_val),'value="','"')
                if url_opt1_val == "":
                    continue
                url_opt1_name = getparse(str(ea_url_opt1_val),'>','')
                if str(url_opt1_name).find('Sold out') > -1:
                    print(">> (SKIP) Sold out [Option Sel] url_opt1_val (Sold out) : {} | {}".format(url_opt1_val, url_opt1_name))
                    continue
                else:
                    print(">> [Option Sel] url_opt1_val : {} | {}".format(url_opt1_val, url_opt1_name))
                    break

            if str(url_option1_tmp).find('- USD') > -1 or str(url_option2_tmp).find('- USD') > -1 or str(url_option1_tmp).find('- $') > -1 or str(url_option2_tmp).find('- $') > -1:
                print(">> Option Parsing 불가 (USD - USD) : {} | {} ".format(url_opt1_val, url_opt1_name))
                return "D20"

        elif len(sp_opt)-1 == 1: 
            option_kubun = "1" # 옵션 1개일 경우
            option_count = 1
        else:
            print(" Option Check : D07")
            return "D07"

        ###  option :   class="wt-display-block wt-label wt-text-caption"  
        if str(option_source).find('"listing-page-quantity"') > -1:
            option_source = getparse(str(option_source),'','"listing-page-quantity"')
        if str(option_source).find('<div id="variation-error-1"') > -1:
            option_source = getparse(str(option_source),'','<div id="variation-error-1"')
        if str(option_source).find('<div id="error-variation-selector-1"') > -1:
            option_source = getparse(str(option_source),'','<div id="error-variation-selector-1"')
        # with open("aa_etsy_option.html","w", encoding="utf8") as f:
        #     f.write(str(option_source))
        
        if str(option_source).find('id="variation-selector-0"') > -1:
            option_type_str = getparse(str(result), 'for="variation-selector-0"', '</label>')
            if option_type_str.find('<span data-label>') > -1:
                option_type_str = getparse(str(option_type_str), '<span data-label>', '</span>')
            if option_type_str.find('<span data-label="">') > -1:
                option_type_str = getparse(str(option_type_str), '<span data-label="">', '</span>')
            if option_type_str.find('>') > -1:
                option_type_str = getparse(str(option_type_str), '>', '')
            if option_type_str.find('<') > -1:
                option_type_str = getparse(str(option_type_str), '', '<')
            if str(option_source).find('id="variation-selector-1"') > -1:
                option_type_str_2 = getparse(str(result), 'for="variation-selector-1"', '</label>')
                if option_type_str_2.find('<span data-label>') > -1:
                    option_type_str_2 = getparse(str(option_type_str_2), '<span data-label>', '</span>')
                if option_type_str_2.find('<span data-label="">') > -1:
                    option_type_str_2 = getparse(str(option_type_str_2), '<span data-label="">', '</span>')  
                if option_type_str_2.find('>') > -1:
                    option_type_str_2 = getparse(str(option_type_str_2), '>', '')
                if option_type_str_2.find('<') > -1:
                    option_type_str_2 = getparse(str(option_type_str_2), '', '<')
                option_type_str = option_type_str + str("|") + option_type_str_2
                if str(option_type_str).find('>') > -1:
                    option_type_str = ""
            option_type_str = option_type_str.replace("\n","").strip()
            print(">> option_type_str : {} ".format(option_type_str))

            option1_tmp = getparse(str(option_source),'id="variation-selector-0"','</select>').replace('\n','')
            if option_count == 2:
                option2_tmp = getparse(str(option_source),'id="variation-selector-1"','class="add-to-cart-form"').replace('\n','')
                option2_valDic = dict()
                sp_opt2_val = str(option2_tmp).split('</option>')
                low_cnt2 = 0
                for ea_opt2_val in sp_opt2_val:   
                    opt2_val = ""
                    opt2_name = ""
                    opt2_price = ""
                    opt2_val = getparse(str(ea_opt2_val),'value="','"')
                    if opt2_val == "":
                        low_cnt2 = low_cnt2 + 1
                        continue
                    opt2_name = getparse(str(ea_opt2_val),'value="','')
                    opt2_name = getparse(opt2_name,'>','').strip()
                    opt2_price = '0'
                    if str(opt2_name).find('Sold out') > -1:
                        print(">> (SKIP) Sold out [Option Sel] url_opt1_val (Sold out) : {} | {}".format(opt2_val, opt2_name))
                        low_cnt2 = low_cnt2 + 1
                        continue
                    else:
                        if str(ea_opt2_val).find('(USD') > -1:
                            opt2_name = getparse(str(ea_opt2_val),'value="','')
                            opt2_name = getparse(opt2_name,'>','(USD').strip()
                            opt2_price = getparse(str(ea_opt2_val),'(USD',')')
                            if opt2_price.find('data-option-original') > -1:
                                opt2_price = getparse(str(opt2_price),'','data-option-original').replace('"','').strip()
                            if str(opt2_price).find('- USD') > -1:
                                opt2_price = '0'
                        elif str(ea_opt2_val).find('($') > -1:
                            opt2_name = getparse(str(ea_opt2_val),'value="','')
                            opt2_name = getparse(opt2_name,'>','($')
                            opt2_price = getparse(str(ea_opt2_val),'($',')')
                            if str(opt2_price).find('- $') > -1:
                                opt2_price = '0'  

                        opt2_price = str(opt2_price).replace('$','').replace(',','').replace(' ','').strip()
                        option2_valDic[opt2_val] = opt2_name + "@@" + opt2_price                    
                        # print(">> [Option2] {} | {} | {}".format(opt2_val, opt2_name, opt2_price))
                    low_cnt2 = low_cnt2 + 1

            sp_opt1_val = str(option1_tmp).split('</option>')
            low_cnt = 0

            opt1_search_val = ""
            for ea_opt1_val in sp_opt1_val:
                opt1_val = ""
                opt1_name = ""
                opt1_price = ""
                opt1_val = getparse(str(ea_opt1_val),'value="','"')
                if opt1_val == "":
                    low_cnt = low_cnt + 1
                    continue
                opt1_name = getparse(str(ea_opt1_val),'value="','')
                opt1_name = getparse(str(opt1_name),'>','').strip()
                opt1_price = '0'
                if str(opt1_name).find('Sold out') > -1:
                    print(">> (SKIP) Sold out Options : [{}] -  {} | {} ".format(low_cnt, opt1_val, opt1_name))
                    low_cnt = low_cnt + 1
                    continue
                if low_cnt > 50:
                    print("Option 50 Over ")
                    break

                if str(ea_opt1_val).find('(USD') > -1:
                    opt1_name = getparse(str(ea_opt1_val),'value="','')
                    opt1_name = getparse(str(opt1_name),'>','(USD').strip()
                    opt1_price = getparse(str(ea_opt1_val),'(USD',')')
                    if opt1_price.find('data-option-original') > -1:
                        opt1_price = getparse(str(opt1_price),'','data-option-original').replace('"','').strip()
                    if str(opt1_price).find('- USD') > -1:
                        opt1_price = getparse(str(ea_opt1_val),'(USD',')')
                    if str(opt1_price).find('- USD') > -1:
                        opt1_price = '0'
                elif str(ea_opt1_val).find('($') > -1:
                    opt1_name = getparse(str(ea_opt1_val),'value="','')
                    opt1_name = getparse(str(opt1_name),'>','($')
                    opt1_price = getparse(str(ea_opt1_val),'($',')')
                    if str(opt1_price).find('- $') > -1:
                        opt1_price = '0'
                opt1_name = replaceQueryString(opt1_name)
                opt1_price = str(opt1_price).replace('$','').replace(',','').replace(' ','').strip()
                # print(">> [Option1] {} | {} | {}".format(opt1_val, opt1_name, opt1_price))
                # print("\n\n")

                if option_kubun == "2":
                    for key, val in option2_valDic.items():
                        opt2_val = key
                        opt2_name = replaceQueryString(getparse(str(val),'','@@'))
                        opt2_price = getparse(str(val),'@@','')
                        if float(opt1_price) > 0:
                            sum_price = float(opt1_price)
                        else:
                            sum_price = float(opt2_price)
                        option_valDic[opt1_val+str(":")+opt2_val] = sum_price
                        print(">> (옵션2개일떄) : [{}] -  {}:{} | {}:{} | {} ".format(low_cnt, opt1_val, opt2_val, opt1_name, opt2_name, sum_price))
                        opmaxlen = opmaxlen + 1
                        option_value_dic[str(opt1_val)+":"+str(opt2_val)] = str(opt1_name)+":"+str(opt2_name)
                        option_price_dic[str(opt1_val)+":"+str(opt2_val)] = sum_price
                else:
                    option_valDic[opt1_val] = float(opt1_price)
                    print(">> (옵션1개일때) : [{}] -  {} | {} | {} ".format(low_cnt, opt1_val, opt1_name, opt1_price))
                    opmaxlen = opmaxlen + 1
                    option_value_dic[opt1_val] = opt1_name
                    option_price_dic[opt1_val] = opt1_price
                    opt1_search_val = opt1_val

                low_cnt = low_cnt + 1

            print(">> option_value_dic : {}".format(option_value_dic))
            print(">> option_price_dic : {}".format(option_price_dic))

            if option_count > 0 and opmaxlen == 0:
                # No Option
                print(">> Option Goods - opmaxlen :0 : {}".format(asin))
                print('>> option_value check .')
                return "D07"

            if option_kubun != "0":
                rcnt = 0
                for k, v in option_valDic.items():
                    if rcnt == 0:
                        min_price = float(v)
                        top_price = float(v)
                    else:
                        if float(v) > float(top_price):
                            top_price = float(v)
                        if float(v) < float(min_price):
                            min_price = float(v)
                    rcnt = rcnt + 1 
                print(">> min_price : {} top_price: {}".format(min_price, top_price))

            if min_price == 0 or min_price == 0.0:
                print(">> Option Min Price : 0 ")
            else:
                base_min_price = min_price
            if top_price == 0 or top_price == 0.0:
                print(">> Option Max Price : 0 ")
            else:
                base_top_price = top_price

            if option_count == 1 and min_price == 0 and top_price == 0:
                print(">> option len 1 and price 0 case ")
                if str(get_goods_price(result)).find("+") > -1:
                    print(">> opt1_search_val : {}".format(opt1_search_val))
                    print('>> option_value check .')
                    return "D07"

            print(">> Option Max Price : {} | Option Min Price : {} ".format(base_top_price, base_min_price))
            if option_count > 0 and opmaxlen == 0:
                # No Option
                print(">> Option Goods - opmaxlen :0 : {}".format(asin))
                print('>> option_value check .')
                return "D07"

    if d_minus_opt == "1": # 마이너스 옵션으로 set
        base_price_tmp = float(base_top_price)
        goods['price'] = float(base_top_price)
        goods['price_tmp'] = float(base_top_price)        
        print('>> price 마이너스 set :' +str(base_price_tmp))
    else:
        base_price_tmp = float(base_min_price)
        goods['price'] = float(base_min_price)
        goods['price_tmp'] = float(base_min_price)        
        print('>> price 플러스 set :' +str(base_price_tmp))

    tmp_coupon = float(py_coupom)
    goods['minus_opt'] = str(d_minus_opt)
    goods['coupon'] = str(tmp_coupon)
    print('>> (set) coupon : '+str(tmp_coupon))
    print('>> (DB) goods minus_opt : '+str(goods['minus_opt']))

    ########### option Item / option type ###########
    if option_count == 0:
        print('>> Items 0 :  ' + str(goods['Items']))
        print('>> option_type 0 :  ' + str(option_type_str))
    else:
        goods['Items'] = getQueryValue(generateOptionString(db_ali2, option_price_dic, option_value_dic, d_minus_opt, base_price_tmp, exchange_rate, tmp_coupon))
        goods['option_type'] = option_type_str
        #print('>> Items :  ' + str(goods['Items']))
        print('>>  option Items : OK ')
        print('>> option_type :  ' + str(option_type_str))

        ##### price check #####
        if float(base_min_price) < 1 or str(base_min_price) == "":
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(base_min_price) + " ) "  # 1 달러 미만
        if float(base_top_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(base_top_price) + " ) "  # 1100 달러 over

    ########### optionkind ###########
    goods['optionkind'] = str(option_ck)
    print('>> optionkind :  ' + str(option_ck))

    ########### shipping_weight ###########
    goods['shipping_weight'] = "0"

    # handmade 유료배송비
    etsy_shipping_fee = float(goods['shipping_fee_tmp']) * float(exchange_rate) * 2
    print(">> etsy_shipping_fee : {} ".format(etsy_shipping_fee))
    goods['shipping_fee'] = int(round(etsy_shipping_fee, -2))

    ########### goodsmoney ###########
    goodsmoney = 0
    goodsmoney = getWonpirce(db_ali2, base_price_tmp, exchange_rate)
    print(">> goodsmoney : {}".format(goodsmoney))
    goodsmoney = goodsmoney + etsy_shipping_fee
    goodsmoney = int(round(goodsmoney, -2))
    print(">> goodsmoney + shipping_fee (Sum) : {} ".format(goodsmoney))

    if int(goodsmoney) > 5000000:
        print('>> 5백만원 over (skip)')
        return "D09" + " ( " + str(goodsmoney) + " ) "  # 500백만원 over

    goods['goodsmoney'] = goodsmoney
    print('>> goodsmoney : ' + str(goodsmoney))
    print('>> (sale price) : ' + str(int(goodsmoney) * (100-tmp_coupon) / 100))    

    low_price = float(goods['price']) * float(exchange_rate) + (int(etsy_shipping_fee) * (100-tmp_coupon) / 100)
    print('>> low_price : {} (환율 {}) + {} = {}'.format(float(goods['price']) * float(exchange_rate), exchange_rate, (int(etsy_shipping_fee) * (100-tmp_coupon) / 100),int(low_price)))
    low_price = int(low_price)
    print('>> low_price (최저원가) : ' + str(low_price))
    goods['low_price'] = low_price
    
    if int(goodsmoney) < 19000:
        goods['goodsmoney'] = 19000
        print('>> goodsmoney (19000 보다 작을경우 19000으로 설정) : ' + str(goodsmoney))

    #DB set
    rtnDBflg = setDB_proc(asin, goods, db_con, db_ali2, db_price, in_pg, guid, exchange_rate)
    sel_goodscode = ""
    if rtnDBflg[:2] != "0@":
        if rtnDBflg == "D01":
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
            return str(rtnDBflg) # exit
    else:
        sel_goodscode = getparse(rtnDBflg,"0@","")
        sql_i = "insert into goods_title_tran (goodscode, asin_no, Title) values ('{}', '{}',dbo.GetCutStr('{}',240,'...'))".format(sel_goodscode, asin, goods_title)
        in_org_title = str(in_org_title).replace(",","").upper()
        if in_org_title == goods_title: # 기존 org title 과 파싱 title 비교
            print(">> 타이틀 변화없음 ")
            if regKrStrChk(in_old_title) == "0": # 기존 DB title 한글번역 없을경우 번역 대상
                print(">> 한글 없음 번역 Insert : {} ".format(asin))
                db_con.execute(sql_i)
        else:
            print(">> 타이틀 번역 Insert : {} ".format(asin))
            db_con.execute(sql_i)

    return "0"

def get_asinset(in_catecode,db_con):
    asinset = []

    #sql = "select top 100 asin,price from T_Category_BestAsin where cate_idx = '{0}' order by newid()".format(in_catecode)
    #sql = "select top 100 asin,price from T_Category_BestAsin where cate_idx = '{0}' order by reg_date ".format(in_catecode)
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
                print('>> Error : '+str(e))
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
    elif in_code_no == "D77":
        rtnMemo = str(in_code) + ' : (Option Check) Required Options '
    elif in_code_no == "D20":
        rtnMemo = str(in_code) + ' : (option check) 2 option price check'
    elif in_code_no == "D08":
        rtnMemo = str(in_code) + ' : (option price check) Unsellable product'
    elif in_code_no == "D09":
        rtnMemo = str(in_code) + ' : (max price over) Unsellable product'
    elif in_code_no == "D10":
        rtnMemo = str(in_code) + ' : (Pre-order) Unsellable product'
    elif in_code_no == "D11":
        rtnMemo = str(in_code) + ' : (shipping price over) Unsellable product'
    elif in_code_no == "D12":
        rtnMemo = str(in_code) + ' : (min price) Unsellable product'
    elif in_code_no == "D13":
        rtnMemo = str(in_code) + ' : (Pantry Goods) Unsellable product'
    elif in_code_no == "D17":
        rtnMemo = str(in_code) + ' : (No goodscode) Unsellable product'
    elif in_code_no == "D18":
        rtnMemo = str(in_code) + ' : (black-curtain-redirect) Unsellable product'
    elif in_code_no == "D19":
        rtnMemo = str(in_code) + ' : (No img) Unsellable product'
    elif in_code_no == "D20":
        rtnMemo = str(in_code) + ' : Deliver to check (Ship from Korea)'
    elif in_code_no == "D21":
        rtnMemo = str(in_code) + ' : (title) Unsellable product'
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
        rtnMemo = str(in_code) + ' : connect error '
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

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'

    proc = ""
    try:
        proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
        print(">> C:\Program Files (x86)\Google\Chrome ")
    except FileNotFoundError:
        print(">> C:\Program Files\Google\Chrome ")
        proc = subprocess.Popen(filePath)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(options=option)

    return proc, browser

def connectDriverOld(pgSite, kbn, type):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer':'" + str (pgSite) + "'")
    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, kbn, type):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
        print(">> ChromeDriverManager install ")
    except Exception as e:
        print(e)
        # print(">> ChromeDriverManager 114.0.5735.90 install ")
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)

        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path

    return browser


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

def version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn):
    
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
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 1000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")

                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 1000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")

            time.sleep(3)
            
            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception ')
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
    chk_data = ""

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

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    return result

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

# Goods ###################################################################################
def set_multi(in_drive, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, db_con, db_ali, db_ali2, db_price, input_tor):
###########################################################################################
    print('>> set_multi ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    cateidx = ""

    # procIpChange(2)
    # time.sleep(1)

    # category get
    if input_tor != "Y":
        cateidx = newlist(db_con, db_ali, in_drive, in_pg, mac_addr())
    else:
        cateidx = newlist(db_con, db_ali, in_drive, in_pg, currIp)
    print('>> newlist() catecode :' + str(cateidx))
    if cateidx == "":
        print('>> catecode parsing complete : ' + str(cateidx))
        return "0"
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
        #version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn)
    else:
        # version check
        version_check(db_con, db_ali, in_drive, in_ver, in_pgFilename, in_pgKbn)

    # asin get
    get_asin_list = []
    get_asin_list = get_asinset(cateidx, db_con)
    print(get_asin_list)
    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(cateidx))
        return "1"

    c_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))
    rtnChk_no = ""

    for asin_low in get_asin_list:
        tmp_msg = ""
        allCnt = allCnt + 1
        if allCnt == 1 or allCnt == 50:
            if input_tor != "Y":
                procWork(db_con, db_ali, in_drive, in_pg, mac_addr())
            else:
                procWork(db_con, db_ali, in_drive, in_pg, currIp)
        #if allCnt % 10 == 0:
        set_new_tor_ip(input_tor)
        checkCurrIP()

        time.sleep(0.5)
        print('\n\n')
        print('>> version : '+str(in_ver))
        # print(checkIP2())
        print('>> ------- < set_multi [' + str(allCnt) + '] >  catecode : ' + str(cateidx) + ' | goodscode : ' + str(asin_low) + ' -------')

        rtnChk = proc_asin_parse_brower(asin_low, db_con, db_ali, db_ali2, db_price, in_drive, in_pg, in_pgsite)  
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

        if rtnChk_no == "E99":
            print('>> E99 Exit : ' + str(rtnChk_no))
            break

        if rtnChk_no[:1] == "D":
            if rtnChk_no[:3] == "D11":
                c_Errcnt = c_Errcnt + 1
            else:
                c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03" or rtnChk_no == "C04" or rtnChk_no == "C05":  # Connection Error
            c_Errcnt = c_Errcnt + 1
            print('>> # Url Connect Error : ' + str(rtnChk))
            procIpChange(3, input_tor)
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
            c_Errcnt = c_Errcnt + 1
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
                DIsDisplay = ""
                D_naver_in = ""
                D_goodscode = ""
                if str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where ali_no = '{0}'".format(rtn_asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode from T_goods where uid = '{0}'".format(rtn_uid)                    
                rs = db_con.selectone(sql)
                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    DDel_Naver = rs[2]
                    D_regdate = rs[3]
                    D_UpdateDate = rs[4]
                    D_naver_in = rs[5]
                    D_goodscode = rs[6]

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

                        # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                        if str(D_naver_in) == "1":
                            proc_ep_insert(D_goodscode,'D')

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
            # set_new_tor_ip()
            checkCurrIP()
            time.sleep(1)
            if c_Errcnt > 5:
                print('>> ( c_Errcnt 5 over ) exit - catecode :' + str(cateidx))
                procLogSet(db_con, in_pg, " ( c_Errcnt 5 over ) exit - catecode: " + str(cateidx))
                procEnd(db_con, db_ali, in_drive, in_pg)

    if rtnChk_no == "E99":
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
def set_stock_out(db_con, db_ali, db_price, in_drive, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2, in_sql3, input_tor):
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
            if input_tor != "Y":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)
            time.sleep(1)
        # if allCnt % 10 == 0:
        set_new_tor_ip(input_tor)
        checkCurrIP()

        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> ----------------- < (set_stock_out) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_out_brower(asin_low,db_con,db_ali,db_price,in_drive,in_pg,in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_stock_out Exception Error : ' + str(ex))
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

        d_GoodsCode = ""
        d_naver_in = ""
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
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
            d_naver_in = rs_row[8]

            print(">> d_stock_ck_cnt : " + str(d_stock_ck_cnt))
            print(">> d_IsDisplay : " + str(d_IsDisplay))
            print(">> d_Del_Naver : " + str(d_Del_Naver))
            print(">> d_GoodsCode : " + str(d_GoodsCode))
            print(">> d_stock_ck : " + str(d_stock_ck))
            print(">> d_naver_in : " + str(d_naver_in))

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
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

            elif rtnChk_no[:1] == "S": 
                if d_IsDisplay == 'T':
                    sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                    print(">> sql : " + str(sql))
                    print(">> 품절처리 Ok stock_ck update : " + str(d_GoodsCode))
                    db_con.execute(sql)
                    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                    if str(d_naver_in) == "1":
                        proc_ep_insert(d_GoodsCode,'D')

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
            # print(checkIP())
            # set_new_tor_ip()
            checkCurrIP()            
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
def proc_asin_out_brower(in_asin_str,db_con, db_ali, db_price, in_drive, in_pg, in_pgsite):   

    asin = ""
    cateidx = ""
    db_Del_Naver = ""
    sp_asin = in_asin_str.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    guid = ""
    guid = sp_asin[3]
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    db_Weight = "0"
    DB_stop_update = "0"
    db_order_ck = ''
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title, order_ck from t_goods where ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title, order_ck from t_goods where uid = {0}".format(guid)
    
    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_title = rowUP[5]
        db_order_ck = rowUP[6]

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

    result = ""
    now_url = "https://www.etsy.com/listing/" + str(asin) + "/"

    try:
        result = getSource(in_drive, db_con, db_ali, in_pg, now_url)
    except Exception as e:
        print('>> Error : '+str(e))
        result = "E99"
    else:    
        print('>> getSource Ok : {}'.format(now_url))

    if result == "C02" or result == "C05" or result == "D01" or result == "D17" or result == "D11" or result == "E99":
        return result 
    if result == "":
        return "E99"
    ######################## goods parsing ########################
    print('>> goods parsing ######################## ')

    if str(result).find('data-buy-box-region="price"') == -1:
        print('>> Sold Out')
        return "D01"

    if str(result).find('Sorry, this item is unavailable') > -1:
        print('>> sold out (this item is unavailable) ')
        return "D17"       
    elif str(result).find('Sorry, this item and shop are currently unavailable') > -1:
        print('>> sold out (this item and shop are currently unavailable)')
        return "D01"
    elif str(result).find('Sorry, this item is sold out') > -1:
        print('>> sold out (this item is sold out)')
        return "D01"
    elif str(result).find('This shop is taking a short break') > -1:
        print('>> sold out (This shop is taking a short break) ')
        return "D01"
    elif str(result).find('Items sold by Etsy sellers') > -1:
        print('>> sold out (Items sold by Etsy sellers) ')
        return "D01"
    elif str(result).find('A stitch has gone awry.') > -1:
        print('>> sold out (A stitch has gone awry.) ')
        return "D01"

    goods_price = "0"
    original_price = "0"

    goods_price = get_goods_price(result)
    goods_price = regRemoveText(goods_price)
    goods_price = str(goods_price).replace(" ","").replace("+","").replace("USD","").replace("$","").replace(",","").replace("\n","").strip()
    print("goods_price : {}".format(goods_price))

    # Original price  
    price_tmp = getparse(str(result),'data-buy-box-region="price"','</div>')  
    price = getparse(price_tmp,'Price:','</p>').replace("</span>","\n").strip()
    if str(price_tmp).find('>Price:</span>') > -1:
        original_price = getparse(str(price_tmp),'>Original Price:</span>','</p>')
        if original_price.find('-'):
            original_price = getparse(str(original_price),'','-')
        if str(original_price).find("$") > -1:
            original_price = getparse(str(original_price),"$","")
            if str(original_price).find("$") > -1:
                original_price = getparse(str(original_price),"","$").replace("-","")
    else:
        original_price = "0"

    print(">> {} : {} ".format(price, original_price))
    original_price = regRemoveText(original_price)
    original_price = str(original_price).replace(" ","").replace("+","").replace("USD","").replace("$","").replace(",","").replace("\n","").strip()

    if goods_price == "": goods_price = "0"
    if original_price.replace(".",'').isdigit() == True:
        if float(original_price) > float(goods_price):
            goods_price = original_price

    if str(goods_price) == "0" or str(goods_price) == "":
        print('>> Sold Out')
        return "D22"

    ##### price check #####
    if str(result).find('id="inventory-variation-select-0"') == -1:
        if float(goods_price) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 달러 미만

        if float(goods_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 달러 over

    # Korea 배송 
    if str(result).find('Deliver to South Korea') > -1:
        print('>> Deliver to South Korea ')
    elif str(result).find('shipping to South Korea') > -1:
        print('>> shipping to South Korea ')
    elif str(result).find('Change shipping country') > -1:
        print('>> Change shipping country (Korea 배송 불가) ')
        return "D11" 
    else:
        print('>> Korea 배송 확인불가 ')
        return "D11" 

    ########### shipping_fee ###########
    # Cost to ship (배송비)
    ship_tmp = "0"
    if str(result).find('Cost to ship') > -1:
        ship_tmp = getparse(str(result),'Cost to ship','</div>')
        if str(ship_tmp).find('Free') > -1:
            ship_tmp = "0"
        else:
            if ship_tmp.find("USD") > -1:
                print(">> 배송비 USD Ok ")
            elif ship_tmp.find("$") > -1:
                print(">> 배송비 $ Ok ")
            else:
                print('>> 배송비 (USD 없음) Currency 확인필요 (SKIP)')
                return "D11" 
            if ship_tmp.find("<span class='currency-value'>") > -1:
                ship_tmp = getparse(str(ship_tmp),"<span class='currency-value'>","</span>")
            else:
                ship_tmp = getparse(str(ship_tmp),'<span class="currency-value">','</span>')
        print(">> ship_tmp : {}".format(ship_tmp))
    elif str(result).find('<span data-estimated-shipping') > -1:
        ship_tmp = getparse(str(result),'<span data-estimated-shipping','</div>')
        ship_tmp = getparse(str(ship_tmp),'>','')
        print('>> 배송비 체크')
        if str(ship_tmp).find('Free') > -1:
            ship_tmp = "0"
        else:
            if ship_tmp.find("<span class='currency-value'>") > -1:
                ship_tmp = getparse(str(ship_tmp),"<span class='currency-value'>","</span>")
            else:
                ship_tmp = getparse(str(ship_tmp),'<span class="currency-value">','</span>')
    else:
        if str(result).find('Shipping and return policies') > -1:
            ship_tmp = getparse(str(result),'Shipping and return policies','Deliver to ')
        if str(ship_tmp).find('Free shipping') > -1:
            ship_tmp = "0"
        else:
            print('>> 배송비 Cost to ship 없음 (SKIP)')
            return "D11" 

    if str(ship_tmp) != "0":
        print('>>유료 배송비 상품 : {}'.format(ship_tmp))
        ship_tmp = str(ship_tmp).replace(",","").strip()
        if ship_tmp.replace('.','').isdigit() == False:
            print(">> 유료배송비 숫자인지 확인필요 SKIP : {}".format(ship_tmp))
            return "D11" + " ( " + str(ship_tmp) + " ) " 

        if float(ship_tmp) > 20:
            print(">> 유료배송비 20달러 이상 SKIP : {}".format(ship_tmp))
            return "D11" + " ( " + str(ship_tmp) + " ) " 
        else:
            print(">> 유료배송비 : {}".format(ship_tmp))

        if db_order_ck == '1':
            print(">> 유료배송비 (주문이력있음) 진행 : {}".format(ship_tmp))
        else:
            ori_title = getparse(str(result), 'data-buy-box-listing-title="true"','</h1>')
            ori_title = getparse(str(ori_title), '>','')
            if str(ori_title).lower().find("westwood ") > -1:
                print(">> title WESTWOOD 포함 상품 ")
                return "D21"

            if str(ori_title).find("Vintage ") > -1:
                print(">> title 빈티지 포함 상품 (유료 배송비도 파싱하기) ")

    return "0"


# Stock ###################################################################################
def set_updatelist(db_FS, db_con, db_ali, db_ali2, db_price, in_drive, in_pg, in_pgsite, in_ver, input_tor):
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
            if input_tor != "Y":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)          
            time.sleep(1)

        print('\n\n ----------------- < (stock check) set_updatelist [' + str(cnt_asinlist2) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_ali,db_ali2,db_price,in_drive,in_pg, in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_updatelist Exception Error : ' + str(ex))
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

        d_naver_in = ""
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
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
            d_naver_in = rs_row[8]

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

                # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                if str(d_naver_in) == "1":
                    proc_ep_insert(d_GoodsCode,'D')

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
def set_stock_multi(db_con, db_ali, db_ali2, db_price, in_drive, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2, in_sql3, input_tor):
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
        if allCnt == 1 or allCnt == 50:
            if input_tor != "Y":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)
        #if allCnt % 10 == 0:
        set_new_tor_ip(input_tor)
        checkCurrIP()

        print('\n\n')
        print('>> version : '+str(in_ver))
        print('>> ----------------- < (set_stock_multi) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_ali,db_ali2,db_price,in_drive,in_pg,in_pgsite)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_multi Exception Error : ' + str(ex))
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


        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
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
            d_naver_in = rs_row[8]

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

                # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                if str(d_naver_in) == "1":
                    proc_ep_insert(d_GoodsCode,'D')

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
            # print(checkIP())
            # set_new_tor_ip()
            checkCurrIP()
            time.sleep(2)
            #print('>> time.sleep(2) ')

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
