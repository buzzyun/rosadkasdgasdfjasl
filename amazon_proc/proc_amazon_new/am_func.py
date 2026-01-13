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
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import time
import requests
from PIL import Image
import re
import uuid
import sys
import DBmodule_AM

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

global cnt_title_tran
global EX_PRICE
global gTWOCAPTCHA_API_KEY
gTWOCAPTCHA_API_KEY = "decc2c5553302ce2df33ddb9cf1f4846"

ip = socket.gethostbyname(socket.gethostname())
#print('>> IP : '+str(ip))

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket
    print(">> Connected to Tor")

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_AM.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    print(">> sql : {}".format(sql))
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into amazon_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(currIp) + "', '" + str(in_proc_memo) + "') "
    print(">> setLogProc : " + str(sql))
    try:
        in_DB.execute(sql)
    except Exception as e:
        print(">> procLogSet except")
    return "0"

def procEnd(db_con, in_drive, in_pg):
    time.sleep(1)
    #print(' time.sleep(1)')

    #in_drive.get_screenshot_as_file('C:\\project\\log\\procEnd.png')
    print(">> procEnd : " + str(datetime.datetime.now()))
    try:
        db_con.close()
        in_drive.quit()
    except Exception as e:
        print(">> procEnd except")
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
    try:
        conn = http.client.HTTPConnection("icanhazip.com")
        conn.request("GET", "/")
        time.sleep(1)
        response = conn.getresponse()
        print('>> current ip :', response.read())
    except Exception as e:
        print(">> checkIP except")

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

def set_new_tor_ip():
    # """Change IP using TOR"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    except Exception as e:
        print(">> set_new_tor_ip except")
    print(">> set_new_tor_ip()")
    time.sleep(1)

def checkCurrIP():
    time.sleep(1)
    # proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    # res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    # print('>> Tor Current IP:', res.text)
    #time.sleep(1)

def checkCurrIP_new():
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

def getCountryInfo(in_CountryKbn, in_kbn):
    contry_kbn = ""
    contry_cur = ""
    contry_site = ""    
    contry_post = ""
    #print("in_kbn : "+str(in_kbn))
    if str(in_CountryKbn).find('_') > -1:
        in_CountryKbn = getparse(in_CountryKbn,'','_')

    if str(in_CountryKbn).find('best') > -1 or str(in_CountryKbn).find('global') > -1 or str(in_CountryKbn).find('JP') > -1:
        contry_kbn = "JP"
        contry_cur = "¥"
        contry_site = "www.amazon.co.jp"    
    elif str(in_CountryKbn).find('usa') > -1 or str(in_CountryKbn).find('mall') > -1 or str(in_CountryKbn).find('US') > -1:
        contry_kbn = "US"
        contry_cur = "$"
        contry_site = "www.amazon.com"  
    elif str(in_CountryKbn).find('de') > -1 or str(in_CountryKbn).find('DE') > -1:
        contry_kbn = "DE"
        #contry_cur = "€"        
        contry_cur = "USD"
        contry_site = "www.amazon.de"
    elif str(in_CountryKbn).find('uk') > -1 or str(in_CountryKbn).find('UK') > -1:
        contry_kbn = "UK"      
        contry_cur = "£"
        contry_site = "www.amazon.co.uk"  
    elif str(in_CountryKbn).find('fr') > -1 or str(in_CountryKbn).find('FR') > -1:
        contry_kbn = "FR"      
        contry_cur = "€"
        contry_site = "www.amazon.fr"  


    if in_kbn == "1":
        return contry_kbn
    elif in_kbn == "2":
        return contry_cur
    elif in_kbn == "3":
        return contry_site
    elif in_kbn == "4":
        return contry_post
    else:
        return contry_kbn 


# review
def get_Review(in_soup, in_asin):

    reviews_arr = []

    if str(in_soup).find(in_asin) == -1:
        print(">> get_Review : asin unmatch : " + str(in_asin))
    else:
        sp_review = str(in_soup).split('"a-section review aok-relative"')
        if len(sp_review) == 0:
            print(">> Review No(2) ")
        else:
            r_cnt = 1
            print('>> len(sp_review) : ' + str(len(sp_review) - 1))
            while r_cnt < len(sp_review):
                review_dic = {}
                tmp_title = getparse(str(sp_review[r_cnt]),'review-title-content a-text-bold"','</span>')
                if tmp_title.find('<span class="cr-original-review-content">') > -1:
                    tmp_title = getparse(str(tmp_title), '<span class="cr-original-review-content">','')
                else:
                    tmp_title = getparse(str(tmp_title), '<span>', '')

                tmp_title = tmp_title.replace("/", "").replace("'", "").replace('&AMP;','')
                review_dic['title'] = tmp_title

                review_dic['rating'] = getparse(str(sp_review[r_cnt]), '<span class="a-icon-alt">', '</span>')
                review_dic['author'] = getparse(str(sp_review[r_cnt]), '<span class="a-profile-name">', '</span>')

                review_dic['date'] = getparse(str(sp_review[r_cnt]), 'review-date">', '</span>')
                purchase = getparse(str(sp_review[r_cnt]), '"avp-badge-linkless"', '</span>')
                review_dic['purchase'] = getparse(purchase, 'a-text-bold">', '')
                review_text = getparse(str(sp_review[r_cnt]), 'a-expander-partial-collapse-content">', '</>')
                if review_text.find('<span class="cr-original-review-content">') > -1:
                    review_text = getparse(str(review_text), '<span class="cr-original-review-content">','')
                else:
                    review_text = getparse(str(review_text), '<span>', '')

                review_text = review_text.replace("/", "").replace("'", "").replace('&AMP;', '')
                review_dic['review_text'] = review_text

                review_dic['review_image'] = ''
                review_dic['helpful_votes'] = getparse(str(sp_review[r_cnt]), 'cr-vote-text">', '</span>')
                rating_star = getparse(str(sp_review[r_cnt]), '<i data-hook="review-star-rating"', '">')
                review_dic['rating_star'] = getparse(rating_star, 'class="', '"')

                reviews_arr.append(review_dic)
                r_cnt = r_cnt + 1

    return reviews_arr

# review
def get_Review_new(in_soup, in_asin):

    # rate 평점
    rate_arr = []
    rate_dic = {}
    if in_soup.find('<h2>Customer reviews</h2>') > -1:
        review_rate = getparse(str(in_soup),'<h2>Customer reviews</h2>','"aui-da-a-expander-toggle"')
        total_cnt = getparse(str(in_soup),'"total-review-count"','global ratings')
        total_cnt = getparse(str(total_cnt),'">','')
        average_star_rating = getparse(str(review_rate),'<span class="a-icon-alt">','</span>') 
        rate_dic['average_star'] = average_star_rating.replace("'","")
        rate_dic['total_cnt'] = total_cnt

        rate_list = getparse(str(review_rate),'<ul id="histogramTable"','</ul>')
        sp_rate = str(rate_list).split('</li>')
        r_cnt = 1
        cnt_star = len(sp_rate) - 1
        print('>> len(sp_rate) : {}'.format(len(sp_rate) - 1))
        for ea_rate in sp_rate:
            rate_star = getparse(str(ea_rate),'<a aria-label="','"')
            if rate_star != "":
                rate_dic[str(cnt_star)] = rate_star.replace("'","")
                cnt_star = cnt_star - 1 
        print('>> rate_dic : {}'.format(rate_dic))
        rate_arr.append(rate_dic)

    # reviews
    reviews_arr = []
    if str(in_soup).find(in_asin) == -1:
        print(">> get_Review : asin unmatch : " + str(in_asin))
    else:
        # sp_review = str(in_soup).split('"a-section review aok-relative"')
        review_temp = getparse(str(in_soup),'id="customer-reviews-content"','')
        if review_temp != "":
            sp_review = str(review_temp).split('data-hook="review"')
        else:
            sp_review = str(in_soup).split('data-hook="review"')

        if len(sp_review) == 0:
            print(">> Review No(2) ")
        else:
            r_cnt = 1
            print('>> len(sp_review) : ' + str(len(sp_review) - 1))
            while r_cnt < len(sp_review):
                review_dic = {}
                tmp_title = getparse(str(sp_review[r_cnt]),'data-hook="review-title"','data-hook="review-date"')
                if tmp_title.find('<span class="cr-original-review-content">') > -1:
                    tmp_title = getparse(str(tmp_title), '<span class="cr-original-review-content">','</span>')
                else:
                    tmp_title = getparse(str(tmp_title), '<span>', '</span>')

                tmp_title = tmp_title.replace("/", "").replace("'", "").replace('&AMP;','')
                review_dic['title'] = tmp_title

                review_dic['rating'] = getparse(str(sp_review[r_cnt]), '<span class="a-icon-alt">', '</span>')
                review_dic['author'] = getparse(str(sp_review[r_cnt]), '<span class="a-profile-name">', '</span>')

                review_dic['date'] = getparse(str(sp_review[r_cnt]), 'review-date">', '</span>')
                purchase = getparse(str(sp_review[r_cnt]), '"avp-badge-linkless"', '</span>')
                review_dic['purchase'] = getparse(purchase, 'a-text-bold">', '')

                review_text = getparse(str(sp_review[r_cnt]), 'data-hook="review-date"', '')
                review_text = getparse(str(review_text), 'review-text-content a-expander-partial-collapse-content">', '')
                
                if review_text.find('<span class="cr-original-review-content">') > -1:
                    review_text = getparse(str(review_text), '<span class="cr-original-review-content">','</span>')
                else:
                    review_text = getparse(str(review_text), '<span>', '</span>')
                review_text = review_text.replace("/", "").replace("'", "").replace('&AMP;', '')
                review_dic['review_text'] = review_text

                review_dic['review_image'] = ''
                review_dic['helpful_votes'] = getparse(str(sp_review[r_cnt]), 'cr-vote-text">', '</span>')
                rating_star = getparse(str(sp_review[r_cnt]), '<i data-hook="review-star-rating"', '">')
                review_dic['rating_star'] = getparse(rating_star, 'class="', '"')

                reviews_arr.append(review_dic)
                r_cnt = r_cnt + 1

    return reviews_arr, rate_arr


def soldout_check_2(in_source, inCountry):

    rtn_price = "0"
    check = ""
    plusShip = 0

    contryCur = getCountryInfo(inCountry,"2")

    time.sleep(1)
    #print("time.sleep(1)")

    if str(in_source).find('a-section a-spacing-none aok-align-center aok-relative">') > -1:
        check = getparse(str(in_source), 'a-section a-spacing-none aok-align-center aok-relative>', '</span>')
        print('>> check (8-1) aok-align-center aok-relative ')
        if check.find('<span class="aok-offscreen">') > -1:
            check = check.replace('<span class="aok-offscreen">','')
        if inCountry == "FR" and check.find('€') > -1 and check.find(','):
            frontStr = getparse(check, '', ',').replace(' ','').strip()
            backStr = getparse(check, ',', '€').strip()
            check = frontStr + "." + backStr
            print(">> check : {}".format)
    if str(in_source).find('a-color-price priceBlockBuyingPriceString">') > -1:
        check = getparse(str(in_source), 'a-color-price priceBlockBuyingPriceString">', '</span>')
        print('>> check (8) priceBlockBuyingPriceString ')

    if str(check).strip() == "" and str(in_source).find('priceBlockSalePriceString">') > -1:
        check = getparse(str(in_source), 'priceBlockSalePriceString">', '</span>')
        print('>> check (3) SalePrice')

    if str(check).strip() == "" and str(in_source).find('priceBlockDealPriceString">') > -1:
        check = getparse(str(in_source), 'priceBlockDealPriceString">', '</span>')
        print('>> check (4) DealPrice')

    if str(check).strip() == "" and str(in_source).find('priceBlockStrikePriceString a-text-strike">') > -1:
        check = getparse(str(in_source), 'priceBlockStrikePriceString a-text-strike">', '</span>')
        print('>> check (1) strike ')

    if str(check).strip() == "" and str(in_source).find('priceBlockBuyingPriceString">') > -1:
        check = getparse(str(in_source), 'priceBlockBuyingPriceString">','</span>')
        print('>> check (2) BuyingPrice ')

    if str(check).strip() == "" and str(in_source).find('nowrap">Price:') > -1:
        check = getparse(str(in_source), 'nowrap">Price:', '</span>')
        print('>> check (10) nowrap Price ')

    if str(check).strip() == "" and str(in_source).find('nowrap">With Deal:') > -1:
        check = getparse(str(in_source), 'nowrap">With Deal:', '</span>')
        print('>> check (11) nowrap With Deal ')

    if str(check).strip() == "" and str(in_source).find('<span class="a-price a-text-price a-size-medium"') > -1:
        check = getparse(str(in_source), '<span class="a-price a-text-price a-size-medium"', '</span>')
        print('>> check (12) a-price a-text-price a-size-medium')

    if str(check).strip() == "" and str(in_source).find('basisPrice">') > -1:
        check = getparse(str(in_source), 'basisPrice">', '</span>')
        print('>> check (13-1) basisPrice ')
        check = getparse(str(check), 'class="a-offscreen">', '')
        print('>> a-offscree : {}'.format(check))

    if str(check).strip() == "" and str(in_source).find('basisPrice">Was:') > -1:
        check = getparse(str(in_source), 'basisPrice">Was:', '</span>')
        print('>> check (13-2) basisPrice Was ')

    if str(check).strip() == "" and str(in_source).find('basisPrice">List Price:') > -1:
        check = getparse(str(in_source), 'basisPrice">List Price:', '</span>')
        print('>> check (13-3) basisPrice List Price ')

    if str(check).strip() == "" and str(in_source).find('nowrap">List Price:') > -1:
        check = getparse(str(in_source), 'nowrap">List Price:', '</span>')
        print('>> check (13) nowrap List Price ')

    if str(check).strip() == "" and str(in_source).find('nowrap">Bundle Price:') > -1:
        check = getparse(str(in_source), 'nowrap">Bundle Price:', '</span>')
        print('>> check (14) nowrap Bundle Price ')

    if str(check).strip() == "" and str(in_source).find('nowrap">Deal Price:') > -1:
        check = getparse(str(in_source), 'nowrap">Deal Price:', '</span>')
        print('>> check (15) nowrap Deal Price:	 ')

    if str(check).strip() == "" and str(in_source).find('nowrap">Top Deal:') > -1:
        check = getparse(str(in_source), 'nowrap">Top Deal:', '</span>')
        print('>> check (16) nowrap Top Deal:	 ')

    if str(check).strip() == "" and str(in_source).find('aok-align-center aok-relative">') > -1:
        check = getparse(str(in_source), 'aok-align-center aok-relative">', '</span>')
        if check.find('<span class="aok-offscreen">') > -1:
            check = getparse(str(check), '<span class="aok-offscreen">', '')
        print('>> check (16-2) aok-align-center aok-relative : {}'.format(check))

    if str(check).strip() == "" and str(in_source).find('priceToPay"') > -1:
        check = getparse(str(in_source), 'priceToPay"', '</span>')
        print('>> check (17) priceToPay : {}'.format(check))

    if str(check).strip() == "" and str(in_source).find('apexPriceToPay"') > -1:
        check = getparse(str(in_source), 'apexPriceToPay"', '</span>')
        print('>> check (18) apexPriceToPay : {}'.format(check))

    if str(check).find('class="a-offscreen"') > -1:
        check = getparse(str(check), 'class="a-offscreen">', '')
        print('>> check (19) a-offscree : {}'.format(check))

    if str(check).find(">USD") > -1:
        check = getparse(str(check), '>USD', '')
        print('>> price >USD :	 ')

    if str(check).find("</span>") > -1:
        check = getparse(str(check), '', '</span>')
        print('>> price span :	 ')

    if inCountry != "FR":
        if str(check).strip() == "" and str(in_source).find('</span><span class="a-size-base a-color-price">') > -1 and str(in_source).find('<span>New (') > -1:
            tmp_source = getparse(str(in_source), '</span><span class="a-size-base a-color-price">', '</div>')
            if str(tmp_source).find('FREE Shipping') > -1 or str(tmp_source).find('FREE Delivery') > -1 :
                check = getparse(str(in_source), '</span><span class="a-size-base a-color-price">', '</span>')
                print('>> check (16) <span>New: (FREE)')
            elif str(tmp_source).find('a-color-secondary a-size-base">+') > -1:
                if str(tmp_source).find(' shipping</span>') > -1 or str(tmp_source).find(' delivery</span>') > -1 :
                    test_check = getparse(str(in_source), '</span><span class="a-size-base a-color-price">', '</span>')
                    print('>> check (16) <span>New:	 ')

                    plusShip = "0"
                    if str(test_check).strip() != "":
                        if str(tmp_source).find(' delivery</span>') > -1:
                            plusShip = getparse(tmp_source,'a-color-secondary a-size-base">+','delivery</span>')
                        else:
                            plusShip = getparse(tmp_source,'a-color-secondary a-size-base">+','shipping</span>')
                        plusShip = getparse(plusShip, contryCur, '') 

                        if str(plusShip).strip() != "":
                            #check = (float)check + (float)plusShip
                            print('>> check (7) plusShip : ' + str(plusShip))
                            if str(plusShip) != "0":
                                test_check = str(test_check).replace(',', '')
                                test_check = replace_currency(test_check)
                                plusShip = str(plusShip).replace(',','')
                                plusShip = replace_currency(plusShip)
                                plusShip = regRemoveText(plusShip)
                                
                                check = float(test_check) + float(plusShip)
                                print('>> check (7) price + plusShip : ' + str(check))
            else:
                check = getparse(str(in_source), '</span><span class="a-size-base a-color-price">', '</span>')
                print('>> check (16-2) <span>New:	 ')

    if str(check).strip() == "" and str(in_source).find('id="priceblock_ourprice"') > -1:
        check = getparse(str(in_source), 'id="priceblock_ourprice"', '</span>')
        print(">> check (5) :" + str(check))

    if str(check).strip() == "":
        print('>> soldout_check No price !! ')
        check = ""
    else:
        if str(check).find(contryCur) > -1 and inCountry != "FR":
            check = str(check).strip()
            if str(check).find('</span>') > -1:
                check = getparse(check, contryCur, '</span>')
            else:
                check = getparse(check, contryCur, '')
            print(">> check (Edit) :" + str(check))       

    if str(check).strip() == "" and inCountry != "FR":
        if str(in_source).find('data-asin-price="') > -1:
            print('>> check (6)')
            check = getparse(str(in_source), 'data-asin-price="', '"')
            if str(check).find('.') > -1:
                check = getparse(check, '', '.')
            print('>> check (6) data-asin-price : ' + str(check))

    if str(check).strip() == "" and inCountry != "FR":
        if str(in_source).find('id="olp_feature_div"') > -1 and str(in_source).find('class="a-size-base a-color-price">') > -1:
            print('>> check (7)')
            chk_str = getparse(str(in_source), 'id="olp_feature_div"', 'class="a-size-base a-color-price">')
            print('>> check (7) olp-upd-new (pos) :'+str(str(chk_str).find('id="olp-upd-new"')))
            print('>> check (7) New (pos) :' + str(str(chk_str).find('<span>New ')))
            #if str(chk_str).find('id="olp-upd-new"') > -1 and str(chk_str).find('<span>New ') > -1:
            if str(chk_str).find('condition=NEW') > -1 and str(chk_str).find('<span>New ') > -1:
                print('>> check (7) - 1')
                check_test = getparse(str(in_source), 'id="olp-upd-new"', '</div>')
                #print('(Test) check_test : ' + str(check_test))
                check = getparse(str(check_test), 'class="a-size-base a-color-price">', '</span>')
                if str(check).find(contryCur) > -1:
                    check = getparse(str(check), contryCur, '') 
                    print(">> check (7-1) :" + str(check))

                print('>> check (7): ' + str(check))
                if str(check).find('.') > -1:
                    check = getparse(check, '', '.')

                plusShip = 0
                if str(check).strip() != "":
                    plusShip = getparse(check_test,'<span class="a-size-base">','</span>')
                    plusShip = getparse(plusShip, contryCur, '') 

                    if str(plusShip).strip() != "":
                        #check = (float)check + (float)plusShip
                        print('>> check (7) plusShip : ' + str(plusShip))
                        if str(plusShip) != "0":
                            check = str(check).replace(',', '')
                            check = replace_currency(check)
                            plusShip = str(plusShip).replace(',','')
                            plusShip = replace_currency(plusShip)
                            check = float(check) + float(plusShip)
                            print('>> check (7) price + plusShip : ' + str(check))

            print('>> check (7) a-color-price : ' + str(check))
        else:
            if str(check).strip() == "":
                if str(in_source).find('class="a-size-base a-color-price">') > -1:
                    check = getparse(str(in_source), 'class="a-size-base a-color-price">', '</span>')
                    print(">> check (last3) :" + str(check))
                    if str(check).find(contryCur) > -1:
                        check = getparse(str(check), contryCur, '') 
                        print(">> check (last3-1) :" + str(check))

    if str(check).strip() != "":
        if inCountry != "FR":
            if str(check).find('</') > -1:
                check = getparse(str(check), '', '</') 
            rtn_price = str(check).strip().replace(',', '').replace('&nbsp;', '')
            if rtn_price.find('-') > -1:
                rtn_price = getparse(rtn_price, '-', None)

        rtn_price = rtn_price.replace('</span>', '').replace('>', '').strip()
        rtn_price = replace_currency(rtn_price)
        rtn_price = regRemoveText(rtn_price)

        if (rtn_price.replace(".","").isdigit()):
            rtn_price = float(rtn_price)
        else:
            print('>> soldout_check [Float Error] : ' + str(rtn_price))
            rtn_price = "0"

        print('>> soldout_check [price] : ' + str(rtn_price))
    return str(rtn_price)


#reg
def regStrChk(in_str, in_kbn):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    if in_kbn == "KR":
        regStr = re.search('[가-힣]+',chkStr)
    else:
        regStr = re.search('[^. %-|<>&`()+A-Za-z0-9가-힣]+',chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

#reg
def regJpStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search(u"[\u30a0-\u30ff\u3040-\u309f\u4E00-\u9FFF]+",chkStr) #일본어(Katakana/Hiragana/Kanji)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result


# (사이트DB 체크) 사이트내 금지단어 체크 "0":정상단어, "1":금지단어
def checkForbidden_site(target, cate_idx, replace_site_title_list):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'

    for rs in replace_site_title_list:
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
def checkForbidden_new(target, ban_title_list):
    ban_str = ""
    result = "0"
    parttern = '[가-핳a-zA-Z0-9]'

    for rs in ban_title_list:
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

# replace
def replaceTitle(in_word, replace_title_list):
    target = str(in_word).upper()

    for rs in replace_title_list:
        replace_ban_title = rs[0]
        replace_title = rs[1]
        if str(replace_ban_title) != '' and replace_ban_title != None:

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

#withbuy
# def getWithbuyFee(in_weight, withbuy_base, in_coupon, in_country):
#     base_fee = withbuy_base + (withbuy_base * (in_coupon / 100))
#     if float(in_weight) > 1:
#          #plus_fee = 2000 * in_coupon / 100  #500그램당 2천원플러스 + 쿠폰할인가격 플러스
#         if in_country == "UK" or in_country == "US":
#             plus_fee = 3000 + (3000 * (in_coupon / 100))  #500그램당 3천원플러스 + 쿠폰할인가격 플러스
#         else:
#             plus_fee = 2300 + (2300 * (in_coupon / 100))  #500그램당 2천원플러스 + 쿠폰할인가격 플러스
#         add_shipping_fee = ((float(in_weight) / 0.5) - 2 ) * plus_fee 
#         withbuy_shipping_fee = base_fee + add_shipping_fee

#         if float(in_weight) > 10:
#             withbuy_shipping_fee = withbuy_shipping_fee + 20000 + plus_fee
#     else:
#         withbuy_shipping_fee = base_fee
#     return int(round(withbuy_shipping_fee, -2))


# #withbuy 
def getWithbuyFee(in_weight, withbuy_base, manage_dic):
    withbuy_base_plus = manage_dic['py_withbuy_cost_plus']
    in_coupon = manage_dic['py_coupon']
    withbuy_shipping_fee = 0
    # 추가요금 : 일본 2,000원 / 독일 2,400원 / 영국 2,700원 / 미국 2,500원 
    # 기본요금 (1키로): 일본 10,000원 / 독일 14,900원 / 영국 14,000원 / 미국 9,000원 
    base_fee = withbuy_base / ((100-in_coupon)/100)
    #print('>>Withbuy (base_fee) : {}'.format(base_fee)) 
    if float(in_weight) > 1:
        plus_fee = float(withbuy_base_plus) / ((100-in_coupon)/100)
        add_shipping_fee = ((float(in_weight) / 0.5) - 2 ) * plus_fee 
        withbuy_shipping_fee = base_fee + add_shipping_fee
        if float(in_weight) > 10:
            withbuy_shipping_fee = withbuy_shipping_fee + 20000 + plus_fee
    else:
        withbuy_shipping_fee = base_fee

    return int(round(withbuy_shipping_fee, -2))

# reg replace
def regReplaceStr(in_str):
    result = ""
    regStr = re.compile('[^-. %–|<>&`()+A-Za-z0-9가-힣]+')
    result = regStr.sub('', in_str)
    #print(result)

    return result

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    return result

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveTextWeight(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    if result.count('.') > 1:
        result = ""
    return result

def replaceQueryString(in_word) :
    result = in_word.replace("'","`")
    result = result.replace("★","").replace("◆","").replace("/"," & ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","ー").replace("&times;"," x ").replace("、"," . ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【"," ").replace("】"," ").replace("()","").replace("[]","").replace(";","")

    return result


#goodscode
# def getGoodsCode(uid,goodshead):
#     result = goodshead+str(uid).zfill(10)
#     return result
def getGoodsCode(uid,goodshead, fillcnt):
    result = goodshead+str(uid).zfill(int(fillcnt))
    return result


#옵션처리
def generateOptionString(dic, manage_dic):
    print(">> DB Option (generateOptionString)")
    #print(dic['subasin'])
    #print(str(len(dic['subasin'])))

    #print(dic['option_price'])
    #print(str(len(dic['option_price'])))

    minus_optflg = ""
    minus_optflg = dic['minus_opt']
    print(">> minus_optflg :"+str(minus_optflg))

    option_item = []
    for low in dic['subasin']:
        option_item_str = []
        
        if dic['option_price'].get(low):
            # 옵션 가격 set
            option_price_diff = getAddpirce(dic['option_price'][low], manage_dic) - getAddpirce(dic['price'], manage_dic)
            option_price_diff = int(round(option_price_diff, -2))
            #print(str(low) + " : " + str(option_price_diff) + " = " + str(getAddpirce(dic['option_price'][low])) + str(' - ') + str(getAddpirce(dic['price'])))

            if minus_optflg == "1":
                if option_price_diff > 0:
                    option_price_diff = 0
            else:
                if option_price_diff < 0:
                    option_price_diff = 0    

            #print(">>< option_price_diff : {}".format(option_price_diff))
            option_value = replaceQueryString(dic['option_value'][low]).replace("`", "")
            option_value = option_value.replace("("," - ").replace(")"," ").replace("  ", " ").strip()
            option_item_str.append(option_value)
            option_item_str.append(str(option_price_diff))
            option_item.append("/".join(option_item_str))

    return ",".join(option_item)


# contents
def generateContent(dic):
    feature_item = []
    description_item = []
    content_item = []
    description = []
    feature = []
    optionkind = 0
    optionkind = dic['optionkind']

    if optionkind == 300:
        feature_item.append('<br><br><font color="orange"><b>Feature</b></font>(may vary by option.)<br><br>')
    else:
        feature_item.append('<br><br><font color="orange"><b>Feature</b></font><br><br>')
    description_item.append('<br><br><font color="red"><b>Description</b></font><br><br>')
    for low in dic['feature']:

        if str(low).rfind('by entering your model number.') == -1:
            feature_str = []
            feature_str.append("<b>●")
            feature_str.append(low.replace("'",""))
            feature_str.append("</b><br>")
            feature_item.append("".join(feature_str))

    feature = "".join(feature_item)
    description_item.append(dic['description'].replace("'",""))
    description = "".join(description_item)
    if optionkind == 300:
        option_img_set = []
        for key,values in dic['option_image'].items():
            if str(values) == '<br>' or str(values) == '':
                print(">> option_image values 없음 : "+str(values))
                #option_img_set.append('<br><Font color=blue><b>{0}</b></FONT><br><img src="{1}"><br><br>'.format(key,values))
            else:
                values = replaceQueryString(values).replace("`", "")
                #option_img_set.append('<br><Font color=blue><b>[{0}]</b></FONT><br><img src="{1}"><br><br>'.format(key,values))
                option_img_set.append('<br><Font color=blue><b><pre>[{0}]</pre></b></FONT><br><img src="{1}"><br><br>'.format(values.replace('"','').replace("'",""),key))
        opt_img_item = "".join(option_img_set)
        content_item.append(feature.replace("'","").replace("・","·"))
        content_item.append(opt_img_item.replace("'",""))
        content_item.append(description.replace("'","").replace("・","·"))
    else :
        content_item.append(feature.replace("'","").replace("・","·"))
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

# 23.03.15 마진 플러스 금액 4구간으로 수정 ( min, middle, middle2 ,max )
def getAddpirce_plus(in_price, in_base_price, manage_dic):
    g_exchange_rate = manage_dic['py_exchange_rate']
    g_rate_margin = manage_dic['py_rate_margin']
    f_price = 0
    f_base_price = 0
    f_price = float(in_price)
    f_base_price = float(in_base_price)

    if g_exchange_rate == "" or g_exchange_rate == "0":
        print(">> getAddpirce 오류 ")
        return "E02"
    else:
        add_plus = manage_dic['py_price_plus']
        if f_base_price <= manage_dic['py_price_min']:
            add_plus = manage_dic['py_price_min_plus']
        elif f_base_price > manage_dic['py_price_middle_from'] and f_base_price <= manage_dic['py_price_middle_to']:
            add_plus = manage_dic['py_price_middle_plus']
        elif f_base_price > manage_dic['py_price_middle_from2'] and f_base_price <= manage_dic['py_price_middle_to2']:
            add_plus = manage_dic['py_price_middle_plus2']
        elif f_base_price > manage_dic['py_price_max']:
            add_plus = manage_dic['py_price_max_plus']

        wonprice = f_price * float(g_rate_margin) * float(g_exchange_rate) + add_plus
        print(">> " + str(wonprice) + " : " + str(f_price) + " * " + str(g_rate_margin) + " * " + str(g_exchange_rate) + " + (add_plus) : "+str(add_plus))

    return int(round(wonprice, -2))

# option 가격 = 달러 * 마진 * 환율
def getAddpirce(in_price, manage_dic):
    g_exchange_rate = manage_dic['py_exchange_rate']
    g_rate_margin = manage_dic['py_rate_margin']
    f_price = 0
    f_price = float(in_price)
    if g_exchange_rate == "" or g_exchange_rate == "0":
        print(">> getAddpirce 오류 ")
        return "E02"
    else:
        wonprice = f_price * float(g_rate_margin) * float(g_exchange_rate)

    return int(round(wonprice, -2))


def proc_DB_other(db_con, goodsinfo_content_dic, goodsinfo_option_dic, goodsinfo_sub_dic, goodsinfo_cate_dic, dic, guid):
    print(">> proc_DB_other ")
    #t_goods_content #######################
    sql = "select * from t_goods_content where uid = {0}".format(guid)
    contentrow = db_con.selectone(sql)
    print('>> t_goods_content Update')
    if not contentrow:
        goodsinfo_content_dic['Uid'] = guid
        try:
            db_con.insert('t_goods_content', goodsinfo_content_dic)
        except Exception as e:
            print('>> Exception [t_goods_content]', e)
            return "Q02"
    else:
        content_where_condition = "uid = '{0}'".format(guid)
        try:
            db_con.update('t_goods_content',goodsinfo_content_dic,content_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_content]', e)
            return "Q02"

    #option #######################
    option_where_condition = "GOODSUID = '{0}'".format(guid)
    try:
        db_con.delete('t_goods_option', option_where_condition)
    except Exception as e:
        print('>> Exception [t_goods_option]', e)
        return "Q02"

    if dic['optionkind'] == 300 :
        goodsinfo_option_dic['GOODSUID'] = guid
        print('>> t_goods_option Insert')
        #print(goodsinfo_option_dic)
        try:
            db_con.insert('t_goods_option',goodsinfo_option_dic)
        except Exception as e:
            print('>> Exception [t_goods_option]', e)
            return "Q01"

    #t_goods_category #######################
    sql = "select * from t_goods_category where GoodsUid = '{0}'".format(guid)
    categoryrow = db_con.selectone(sql)
    print('>> t_goods_category Update')

    if not categoryrow :
        goodsinfo_cate_dic['GoodsUid'] = guid
        try:
            db_con.insert('t_goods_category', goodsinfo_cate_dic)
        except Exception as e:
            print('>> Exception [t_goods_category]', e)
            return "Q02"
    else:
        goodsinfo_cate_where = "GoodsUid = '{0}'".format(guid)
        try:
            db_con.update('t_goods_category', goodsinfo_cate_dic, goodsinfo_cate_where)
        except Exception as e:
            print('>> Exception [t_goods_category]', e)
            return "Q02"

    #t_goods_sub #######################
    sql = "select * from t_goods_sub where uid={0}".format(guid)
    goodssubrow = db_con.selectone(sql)
    print('>> t_goods_sub Update')
    #print(goodsinfo_sub_dic)
    if not goodssubrow:
        goodsinfo_sub_dic['Uid'] = guid
        try:
            db_con.insert('t_goods_sub', goodsinfo_sub_dic)
        except Exception as e:
            print('>> Exception [t_goods_sub]', e)
            return "Q02"
    else:
        try:
            goodsinfo_sub_where_condition = "uid='{0}'".format(guid)
            db_con.update('t_goods_sub', goodsinfo_sub_dic, goodsinfo_sub_where_condition)
        except Exception as e:
            print('>> Exception [t_goods_sub]', e)
            err_flg = "1"
            return "Q02"

    #T_GOODS_IMG_DOWN #######################
    # if g_img_down_flg == "1":
    #     imgTemp = ""
    #     if dic['naver_img'] == "" or dic['naver_img'] is None:
    #         imgTemp = getQueryValue(dic['mainimage'])
    #     else:
    #         imgTemp = getQueryValue(dic['naver_img'])

    #     print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Start ")
    #     imgSql = "select GoodsCode from T_GOODS_IMG_DOWN where GoodsCode = '" + str(D_goodscode) + "'"
    #     imgRows = db_con.selectone(imgSql)

    #     if not imgRows:
    #         sqlImg = " insert into T_GOODS_IMG_DOWN (GoodsCode, GoodsUid, ImgPath, cate_idx) values ('" + str(D_goodscode) + "'," +str(guid)+ "," + str(imgTemp) + "," +str(dic['catecode'])+") "
    #         print(">> sqlImg : " +str(sqlImg))
    #         db_con.execute(sqlImg)
    #     else:
    #         sqlImg = " update T_GOODS_IMG_DOWN set GoodsUid = " +str(guid)+ ", ImgPath = " + str(imgTemp) + ", cate_idx = " +str(dic['catecode'])+ ", regDate=getdate() where GoodsCode = '" + str(D_goodscode) + "'"
    #         print(">> sqlImg : " +str(sqlImg))
    #         db_con.execute(sqlImg)
    #     print(">> T_GOODS_IMG_DOWN 이미지 테이블 저장 Ok ")

    return "0"

def get_newgoodscode(db_con, now_guid, pgsite):
    new_goodscode = ""

    if pgsite == 'best' or pgsite == 'BEST':
        new_goodscode = getGoodsCode(now_guid, 'X', 10)
    elif pgsite == 'global' or pgsite == 'GLOBAL':
        new_goodscode = getGoodsCode(now_guid, 'V', 10)
    if pgsite == 'mall' or pgsite == 'MALL':
        new_goodscode = getGoodsCode(now_guid, 'N', 10)
    elif pgsite == 'usa' or pgsite == 'USA':
        new_goodscode = getGoodsCode(now_guid, 'Q', 10)
    elif pgsite == "de" or pgsite == "DE":
        new_goodscode = getGoodsCode(now_guid, 'D', 10)
    elif pgsite == "uk" or pgsite == "UK":
        new_goodscode = getGoodsCode(now_guid, 'K', 10)
    elif pgsite == "fr" or pgsite == "FR":
        new_goodscode = getGoodsCode(now_guid, 'K', 10)

    print('>> new_goodscode : '+str(new_goodscode))

    if str(new_goodscode) == "":
        print('>> goodscode 생성 오류 (Q01) : '+str(new_goodscode))
        return "Q01"

    if str(new_goodscode).find(str(now_guid)) == -1:
        print('>> goodscode가 unmatch (Q01) : '+str(new_goodscode))
        return "Q01"

    sql = "update t_goods set goodscode = '{0}' where uid = {1}".format(new_goodscode,now_guid)
    db_con.execute(sql)
    print('>> t_goods table goodscode update')

    return str(new_goodscode).strip()


def get_proc_Info(db_con, dic, in_pg, in_asin, in_guid, proc_dic, in_pgSite):
    if str(in_guid) == '' or in_guid is None or in_guid == 'None':
        procFlg = "N"
        if in_pgSite == "uk" or in_pgSite == "fr":
            sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), display_ali_no, goodscode, isnull(naver_in,0), \
                regdate, DATEDIFF(mm,regdate,getdate()) as reg_diff, UpdateDate, isnull(DATEDIFF(mm,UpdateDate,getdate()),-1) as upd_diff, \
                isnull(order_ck,'0'), isnull(stop_update,'0') from t_goods where ali_no = '" + str(dic['parentasin']) + "' and site_kbn = '" +str(in_pgSite)+ "'"
        else:
            sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), display_ali_no, goodscode, isnull(naver_in,0), \
                regdate, DATEDIFF(mm,regdate,getdate()) as reg_diff, UpdateDate, isnull(DATEDIFF(mm,UpdateDate,getdate()),-1) as upd_diff, \
                isnull(order_ck,'0'), isnull(stop_update,'0') from t_goods where ali_no = '" +str(dic['parentasin'])+ "'"
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (1) (parentasin) : {}'.format(dic['parentasin']))

        if not rows:
            if in_pgSite == "uk" or in_pgSite == "fr":
                sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), display_ali_no, goodscode, isnull(naver_in,0), \
                    regdate, DATEDIFF(mm,regdate,getdate()) as reg_diff, UpdateDate, isnull(DATEDIFF(mm,UpdateDate,getdate()),-1) as upd_diff, \
                    isnull(order_ck,'0'), isnull(stop_update,'0') from t_goods where display_ali_no = '"+str(dic['display_ali_no'])+"' and site_kbn = '" +str(in_pgSite)+ "'"
            else:
                sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), display_ali_no, goodscode, isnull(naver_in,0), \
                    regdate, DATEDIFF(mm,regdate,getdate()) as reg_diff, UpdateDate, isnull(DATEDIFF(mm,UpdateDate,getdate()),-1) as upd_diff, \
                    isnull(order_ck,'0'), isnull(stop_update,'0') from t_goods where display_ali_no = '"+str(dic['display_ali_no'])+"'"
            rows = db_con.selectone(sql)
            print('>> ## t_goods table 검색 (2) (display_ali_no) : {}'.format(dic['display_ali_no']))
            if not rows:
                procFlg = "N"
            else:
                procFlg = "U"
                old_guid = rows[0]
                ck_isdisplay = rows[1]
                ck_delnaver = rows[2]
                D_display_ali_no = rows[3]
                D_goodscode = rows[4]
                D_naver_in = rows[5]
                D_regdate = rows[6]
                D_reg_diff = rows[7]
                D_UpdateDate = rows[8]
                D_upd_diff = rows[9]
                D_order_ck = rows[10]
                D_stop_update = rows[11]
                rtn_goodscode = D_goodscode              
        else:
            procFlg = "U"
            old_guid = rows[0]
            ck_isdisplay = rows[1]
            ck_delnaver = rows[2]
            D_display_ali_no = rows[3]
            D_goodscode = rows[4]
            D_naver_in = rows[5]
            D_regdate = rows[6]
            D_reg_diff = rows[7]
            D_UpdateDate = rows[8]
            D_upd_diff = rows[9]
            D_order_ck = rows[10]
            D_stop_update = rows[11]
            rtn_goodscode = D_goodscode
    else:
        sql = "select top 1 uid, IsDisplay, isnull(Del_Naver,0), isnull(display_ali_no,ali_no), goodscode, isnull(naver_in,0), \
            regdate, DATEDIFF(mm,regdate,getdate()) as reg_diff, UpdateDate, isnull(DATEDIFF(mm,UpdateDate,getdate()),-1) as upd_diff, \
            isnull(order_ck,'0'), isnull(stop_update,'0') from t_goods where uid = '{0}' ".format(in_guid)
        rows = db_con.selectone(sql)
        print('>> ## t_goods table 검색 (3) (uid) ')  
        if rows:
            procFlg = "U" 
            old_guid = rows[0]
            ck_isdisplay = rows[1]
            ck_delnaver = rows[2]
            D_display_ali_no = rows[3]
            D_goodscode = rows[4]
            D_naver_in = rows[5]
            D_regdate = rows[6]
            D_reg_diff = rows[7]
            D_UpdateDate = rows[8]
            D_upd_diff = rows[9]
            D_order_ck = rows[10]
            D_stop_update = rows[11]
            rtn_goodscode = D_goodscode    
        else:
            procFlg = "E01"
            print(">> ### 확인 필요. Guid 존재 table에 없음 (E01): " + str(in_guid))
            procLogSet(db_con, in_pg, " [" + str(in_asin) + "] Guid 존재 table에 없음 : " + str(datetime.datetime.now()))

    print(' procFlg : '+str(procFlg))
    proc_dic['procFlg'] = procFlg
    if procFlg == "U":
        proc_dic['old_guid'] = old_guid
        proc_dic['ck_isdisplay'] = ck_isdisplay
        proc_dic['ck_delnaver'] = ck_delnaver
        proc_dic['D_display_ali_no'] = D_display_ali_no
        proc_dic['D_goodscode'] = D_goodscode
        proc_dic['D_naver_in'] = D_naver_in
        proc_dic['D_regdate'] = D_regdate
        proc_dic['D_reg_diff'] = D_reg_diff
        proc_dic['D_UpdateDate'] = D_UpdateDate
        proc_dic['D_upd_diff'] = D_upd_diff
        proc_dic['D_order_ck'] = D_order_ck
        proc_dic['D_stop_update'] = D_stop_update
        proc_dic['rtn_goodscode'] = rtn_goodscode

    return proc_dic

def dup_check(db_con, in_asin, in_parentasin, old_guid):
    ##### 중복 데이터가 있을 경우 삭제 #######
    dSql = "select top 1 uid, IsDisplay, OptionKind, display_ali_no, naver_in, goodscode, isnull(order_ck,''), isnull(proc_flg,''), isnull(Del_naver,''), isnull(stop_update,'0') from t_goods where display_ali_no = '" + str(in_asin) + "' and uid <> '" + str(old_guid) + "'"
    print('>> 중복 데이터 체크 [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_parentasin))
    rowDS = db_con.selectone(dSql)
    if rowDS:      
        DUid = rowDS[0]
        DIsDisplay = rowDS[1]
        DOptionKind = rowDS[2]
        D_naver_in = rowDS[4]
        D_goodscode = rowDS[5]
        order_ck = rowDS[6]
        proc_flg = rowDS[7]
        Del_naver = rowDS[8]
        stop_update = rowDS[9]

        if proc_flg == "UN" or order_ck == "1" or Del_naver == "4" or stop_update == "1":
            print('>> skip [{}] proc_flg : {} | order_ck : {} | Del_naver : {} | stop_update : {}'.format(D_goodscode, proc_flg, order_ck, Del_naver, stop_update))
            pass
        else:
            # 중복데이터 삭제처리
            if str(D_naver_in) == "1": # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                proc_ep_insert(D_goodscode,'D')
                print('>> 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D) : {}'.format(D_goodscode))
            setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
            procLogSet(db_con, "", " 중복 상품 삭제 : " + str(in_asin) + " | " + str(D_goodscode) + " | " + str(DUid))

            # print('>> 중복 데이터 삭제X --> 판매불가처리 [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_parentasin) + " | [UID] " + str(DUid))
            # ### setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)

            # sql = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1' where uid='{0}'".format(DUid)
            # print('>> 중뵥 데이터 판매불가 처리 (update) : {}'.format(D_goodscode))
            # db_con.execute(sql)
            # procLogSet(db_con, "", " 중복 상품 판매불가 : " + str(in_asin) + " | " + str(D_goodscode))

            # if str(D_naver_in) == "1": # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
            #     proc_ep_insert(D_goodscode,'D')
            #     print('>> 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D) : {}'.format(D_goodscode))


# 네이버 최저가 체크
def naver_price_check(db_price, low_price, D_goodscode):
    print(">> naver_price_check ")
    naver_price_ck = '0'
    ## [naver_price 테이블 ] change_price 최저가 확인후 처리  
    sql_price = "select price, DATEDIFF(dd,isnull(update_date, regdate), getdate()) as diff_day from change_price where flag = '4' and goodscode = '{}'".format(D_goodscode)
    row = db_price.selectone(sql_price)
    if row:
        naver_rowprice = row[0]
        diff_day = row[1]

        print(">> [{}] | low_price : {} | naver_rowprice : {} | diff_day : {}".format(D_goodscode, low_price, naver_rowprice, diff_day))
        # change_price 최저가 비교
        ## if int(low_price) > naver_rowprice:

        if int(low_price) > int(naver_rowprice):
            if diff_day > 90:
                print(">> change_price 업데이트가 90일 이상지난 상품으로 실제 가격 Update : {}".format(diff_day))
                naver_price_ck = '0'
            elif int(low_price) * 0.85 > int(naver_rowprice):
                print(">> change_price 최저가 15프로 이상 차액으로 실제 가격 Update : {} ".format(int(low_price) * 0.85))
                naver_price_ck = '0'
            else:
                ## change_price ---> minus_check = 1 (update) 처리 
                slq_price_up = "update change_price set minus_check = '1' where goodscode = '{}'".format(D_goodscode)
                print(">> [naver_price 테이블 ] change_price --->  minus_check = 1 update  처리 : {}".format(D_goodscode))
                print(">> [t_goods 테이블 ] pirce 변경 (SKIP) : {}".format(D_goodscode))
                db_price.execute(slq_price_up)
                naver_price_ck = '1'
    else:
        # change_price 최저가 없음
        naver_price_ck = '0'

    return naver_price_ck

#DB set
def setDB_proc(in_asin, in_parentasin, dic, db_con, db_price, in_pg, in_countryKbn, in_guid, in_pgsite, manage_dic):

    print('>> setDB start : ' +str(in_pg))
    print('>> [asin] '+ str(in_asin)+' | [parent asin] ' + str(in_parentasin))
    g_coupon = manage_dic['py_coupon']
    g_withbuy_cost = manage_dic['py_withbuy_cost']
    g_exchange_rate = manage_dic['py_exchange_rate']
    g_rate_margin = manage_dic['py_rate_margin']
    g_img_down_flg = manage_dic['py_impy_down_flg']

    goods_title = dic['goods_title']
    originalprice = float(dic['price']) * float(g_exchange_rate)
    originalprice = int(originalprice)
    print('>> price : ' + str(dic['price']))
    print('>> originalprice (rate:' +str(g_exchange_rate)+ ') : ' + str(originalprice))

    ##### check #####
    if in_countryKbn == "JP":
        if float(dic['price']) < 99:
            print('>> 99 (skip)')
            return "D12" + " ( " + str(dic['price']) + " ) "  # 99
    else:
        if float(dic['price']) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(dic['price']) + " ) "  # 1 달러 미만

    # shipping_fee
    shipping_fee = dic['shipping_price']
    # print('>> shipping_fee (before): ' + str(shipping_fee))
    if str(shipping_fee).strip() == "0" or str(shipping_fee).strip() == "0.0":
        shipping_fee = "0"
    else:
        shipping_fee = getAddpirce(dic['shipping_price'], manage_dic)
    print('>> shipping_fee : ' + str(shipping_fee))

    # withbuy
    shipping_withbuy = getWithbuyFee(dic['shipping_weight'], g_withbuy_cost, manage_dic)
    print('>> shipping_withbuy  : ' + str(shipping_withbuy))
    sale_shipping_withbuy = int(shipping_withbuy) * (100-g_coupon) / 100
    print('>> sale_shipping_withbuy (sale price) : ' + str(sale_shipping_withbuy))

    if str(shipping_withbuy) == "" or str(shipping_withbuy) == "0" or str(shipping_withbuy) == "0.0":
        shipping_withbuy = g_withbuy_cost / ((100-g_coupon)/100)
        print('>> g_withbuy_cost 플러스 : ' + str(shipping_withbuy))
        if str(shipping_withbuy) == "":
            shipping_withbuy = 18500
            print('>> shipping_withbuy 없음 18,500원 플러스 : ' + str(shipping_withbuy))

    goodsmoney = getAddpirce_plus(dic['price'], dic['base_price'], manage_dic) + int(shipping_fee) + int(shipping_withbuy)
    #goodsmoney = int(round(goodsmoney, -2))
    print('>> goodsmoney : ' + str(goodsmoney))

    if int(goodsmoney) > 5000000:
        print('>> 최대금액 초과 (skip)')
        return "D09" + " ( " + str(goodsmoney) + " ) "  # 500만원 초과

    low_price = float(dic['price']) * float(g_exchange_rate) + (int(shipping_fee) * (100-g_coupon) / 100)  + (int(shipping_withbuy) * (100-g_coupon) / 100)
    print('>> low_price : {} (환율 {}) + {} + {} = {}'.format(float(dic['price']) * float(g_exchange_rate), g_exchange_rate, (int(shipping_fee) * (100-g_coupon) / 100), (int(shipping_withbuy) * (100-g_coupon) / 100),int(low_price)))
    low_price = int(low_price)
    print('>> low_price (최저원가) : ' + str(low_price))

    if dic['minus_opt'] == "1":
        diff_plus = 0
        diff_plus = float(dic['base_tmp_price']) - float(dic['base_price'])
        print('>> diff_plus : ' + str(diff_plus) + " = " + str(dic['base_tmp_price']) + " - " + str(dic['base_price']))
        diff_plus = (diff_plus * float(g_rate_margin) * float(g_exchange_rate)) * (g_coupon / 100) * (100 / (100-g_coupon))
        print('>> diff_plus (2) : ' + str(diff_plus))
        goodsmoney = goodsmoney + float(diff_plus)
        goodsmoney = int(round(goodsmoney, -2))
        sale_price = int(goodsmoney) * (100-g_coupon) / 100
        print('>> goodsmoney (sale price) : ' + str(sale_price))
        #print('>> (sale price) : ' + str(int(goodsmoney) * (100-tmp_coupon) / 100))
    else:
        sale_price = int(goodsmoney) * (100-g_coupon) / 100
        print('>> goodsmoney (sale price) : ' + str(sale_price))

    # DB query
    goodsinfo_dic = dict()
    goodsinfo_dic['SiteID'] = "'rental'"
    goodsinfo_dic['DealerID'] = "'rental'"
    goodsinfo_dic['GoodsType'] = "'N'"
    goodsinfo_dic['Title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    if in_countryKbn == "JP":
        goodsinfo_dic['JP_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['JP_title'])
    else:
        goodsinfo_dic['IT_title'] = "dbo.GetCutStr('{0}',240,'...')".format(dic['IT_title'])
    goodsinfo_dic['ImgB'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgM'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['ImgS'] = getQueryValue(dic['mainimage'])
    goodsinfo_dic['naver_img'] = getQueryValue(dic['naver_img'])
    goodsinfo_dic['OptionKind'] = getQueryValue(dic['optionkind'])
    goodsinfo_dic['DeliveryPolicy'] = "'990'"
    goodsinfo_dic['State'] = "'100'"
    ######################goodsinfo_dic['Price'] = goodsmoney
    goodsinfo_dic['price_tmp'] = getQueryValue(dic['price_tmp'])
    goodsinfo_dic['withbuy_price_tmp'] = getQueryValue(shipping_withbuy)
    goodsinfo_dic['OriginalPrice'] = originalprice
    goodsinfo_dic['ali_no'] = getQueryValue(dic['parentasin'])
    goodsinfo_dic['display_ali_no'] = getQueryValue(dic['display_ali_no'])
    goodsinfo_dic['cate_idx'] = dic['catecode']
    goodsinfo_dic['E_title'] = "dbo.GetCutStr('{0}',240,'...')".format(goods_title)
    goodsinfo_dic['shipping_fee'] = getQueryValue(shipping_fee)
    goodsinfo_dic['shipping_weight'] = getQueryValue(dic['shipping_weight'])
    goodsinfo_dic['stock_tmp'] = dic['stock_tmp']
    goodsinfo_dic['site_kbn'] = getQueryValue(manage_dic['py_pgSite'])
    goodsinfo_dic['set_coupon'] = int(manage_dic['py_coupon'])
    goodsinfo_dic['set_exchange_rate'] = int(manage_dic['py_exchange_rate'])

    in_pgSite = manage_dic['py_pgSite']

    many_option_ck = dic['many_option']
    if many_option_ck == '1' :
        goodsinfo_dic['many_option'] = "'1'"

    #other img
    otherimg_low = 1
    for otherimg in dic['image']:
        if otherimg_low <= 5:
            goodsinfo_dic['other_img_chk_'+str(otherimg_low)] = "'1'"
            goodsinfo_dic['other_img'+str(otherimg_low)] = getQueryValue(otherimg)
        otherimg_low += 1

    ##############################################
    #option (goodsinfo_option_dic)
    ##############################################
    goodsinfo_option_dic = dict()
    if dic['optionkind'] == 300 :
        goodsinfo_option_dic['Title'] = getQueryValue(replaceQueryString(dic['option_type']))
        goodsinfo_option_dic['Items'] = getQueryValue(generateOptionString(dic, manage_dic))

        goodsinfo_option_dic['Items_org'] = "'N'+'" + str(dic['option_value_dic_org']).replace("'",'') + "'"
        goodsinfo_option_dic['Items_tran'] = "'N'+'" + str(dic['option_value']).replace("'",'') + "'"
        goodsinfo_option_dic['Items_img_org'] = "'N'+'" + str(dic['option_img_dic_org']).replace("'",'') + "'"

        if str(goodsinfo_option_dic['Items']).find('Internal Server Error ') > -1:
            print('>> Option : Internal Server Error ')
            return "D77"
        if str(goodsinfo_option_dic['Items']).find('/0') > -1:
            print('>> Opt 기본옵션 /0 포함 ')
        else:
            print('>> Opt 기본옵션 /0 없음 (SKIP) ')
            return "D01"
        print('>> option (type) : '+str(dic['option_type']))
        #print('>> option (final) ')
        print(goodsinfo_option_dic['Items'])
        goodsinfo_option_dic['Sort'] = 1
        goodsinfo_option_dic['ali_no'] = getQueryValue(dic['parentasin'])

    ##############################################
    #t_goods_content
    ##############################################
    goodsinfo_content_dic = dict()
    goodsinfo_content_dic['Content'] = "N" + getQueryValue(generateContent(dic))
    goodsreview = dic['review']
    goodsreview = str(goodsreview).replace("'",'"')
    goodsinfo_content_dic['ReviewContent'] = getQueryValue(goodsreview)
    goodsinfo_content_dic['ReviewRegDate'] = 'getdate()'
    goodsinfo_content_dic['ReviewRate'] = getQueryValue(str(dic['rate']).replace("'",'"'))

    ##############################################
    #t_goods_sub
    ##############################################
    goodsinfo_sub_dic = dict()
    if in_countryKbn == "JP":
        goodsinfo_sub_dic['Product'] = "'JAPAN'"
    elif in_countryKbn == "US":
        goodsinfo_sub_dic['Product'] = "'USA'"
    elif in_countryKbn == "DE":
        goodsinfo_sub_dic['Product'] = "'DE'"
    elif in_countryKbn == "UK":
        goodsinfo_sub_dic['Product'] = "'UK'"
    elif in_countryKbn == "FR":
        goodsinfo_sub_dic['Product'] = "'FR'"
    goodsinfo_sub_dic['gall_list'] = getQueryValue(dic['gallery'])

    ##############################################
    # t_goods_category
    ##############################################
    goodsinfo_cate_dic = dict()
    goodsinfo_cate_dic['CateCode'] = dic['catecode']
    goodsinfo_cate_dic['Sort'] = 1

    #input("Key input setDB : ")
    ck_isdisplay = ""
    ck_delnaver = ""
    D_naver_in = ""
    procFlg = ""

    proc_dic = dict()
    proc_dic = get_proc_Info(db_con, dic, in_pg, in_asin, in_guid, proc_dic, in_pgSite)
    if proc_dic['procFlg'] == "E01":
        return "E01"
    procFlg = proc_dic['procFlg']

    if procFlg == "N":

        goodsinfo_dic['Price'] = goodsmoney
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
            return "Q01"

        time.sleep(1)
        #goodscode #######################
        if in_pgsite == "uk" or in_pgsite == "fr":
            sql = "select top 1 uid from t_goods where ali_no = '{0}' and site_kbn = '{1}'".format(dic['parentasin'], in_pgsite)
        else:
            sql = "select top 1 uid from t_goods where ali_no = '{0}'".format(dic['parentasin'])
        coderow = db_con.selectone(sql)
        now_guid = coderow[0]         

        # New Goodscode 생성후 t_goods  Update  처리
        new_goodscode = get_newgoodscode(db_con, now_guid, in_pgsite)
        if new_goodscode == "Q01":
            return "Q01"

        # Other DB Insert #######################
        rtn_set_flg = proc_DB_other(db_con, goodsinfo_content_dic, goodsinfo_option_dic, goodsinfo_sub_dic, goodsinfo_cate_dic, dic, now_guid)
        if rtn_set_flg != "0":
            return rtn_set_flg

        rtn_goodscode = new_goodscode
        print(">> 신규 상품 insert goods Ok : {}".format(rtn_goodscode))
    else:
        #####################################################################
        print(">> ## setDB Update ")
        #####################################################################
        D_goodscode = proc_dic['D_goodscode']
        old_guid = proc_dic['old_guid']
        D_naver_in = proc_dic['D_naver_in']
        ck_delnaver = proc_dic['ck_delnaver']
        ck_isdisplay = proc_dic['ck_isdisplay']
        print(">> [{}] old_guid : {} | ck_isdisplay : {} | ck_delnaver : {} ".format(D_goodscode,old_guid,ck_isdisplay,ck_delnaver))
        print(">> regdate : {} | diff : {} | update : {} ".format(proc_dic['D_regdate'],proc_dic['D_reg_diff'],proc_dic['D_UpdateDate']))

        if D_goodscode == "":
            D_goodscode = dic['db_goodscode']

        # 네이버 최저가 체크 ( 24.01 네이버 최저가 비교 처리 제외 )
        # naver_price_ck = naver_price_check(db_price, low_price, D_goodscode)
        # if naver_price_ck == "0":
        #     goodsinfo_dic['Price'] = goodsmoney
        #     goodsinfo_dic['naver_price_ck'] = "'0'"
        # else:
        #     goodsinfo_dic['naver_price_ck'] = "'1'"
        goodsinfo_dic['Price'] = goodsmoney
        goodsinfo_dic['naver_price_ck'] = "'0'"

        ##### 중복 데이터가 있을 경우 삭제 #######
        dup_check(db_con, in_asin, in_parentasin, old_guid)

        if str(dic['del_naver']) == "5" :
            # 네이버에서 오래된 날짜 상품 (제외상품 다시 추가) -> del_naver -> null 로 변경
            goodsinfo_dic['del_naver'] = getQueryValue(None)
            goodsinfo_dic['before_del_naver'] = getQueryValue("5")
            print(">> del_naver 5 -> null 처리 : {}".format(dic['db_goodscode']))

        goodsinfo_dic['UpdateDate'] = 'getdate()'
        arr_where_condition = "uid = {0}".format(old_guid)
        try:
            db_con.update('t_goods', goodsinfo_dic, arr_where_condition)
            print('>> t_goods Update ')
        except Exception as e:
            print('>> Exception [t_goods]', e)
            return "Q03"

        # Other DB Update #######################
        rtn_set_flg = proc_DB_other(db_con, goodsinfo_content_dic, goodsinfo_option_dic, goodsinfo_sub_dic, goodsinfo_cate_dic, dic, old_guid)
        if rtn_set_flg != "0":
            return "Q03"

        # 품절/진열 변경 #######################
        if ck_isdisplay == "F": # 품절상태의 경우
            #if ck_delnaver == 0:
            print('>> IsDisplay Update (품절 -> 노출)')
            sql = "UPDATE t_goods SET IsDisplay='T', IsSoldOut='F', Stock='00', stock_ck = null, stock_ck_cnt = '0', UpdateDate=getdate() where uid = {0}".format(old_guid)
            db_con.execute(sql)

        # 네이버 노출 상품이고, change_price 최저가 없고, OriginalPrice 가 변경되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : U)
        if str(D_naver_in) == "1" and goodsinfo_dic['naver_price_ck'] == "'0'" and ( int(dic['db_OriginalPrice']) != int(goodsinfo_dic['OriginalPrice']) ):
            proc_ep_insert(D_goodscode,'U')

        rtn_goodscode = D_goodscode
        print(">> 기존 상품 update goods Ok : {}".format(rtn_goodscode))

        ### if in_pg == "goods" and procFlg == "U":
        if procFlg == "U":
            # regdate 6개월 pass, 주문 이력 없음, del_naver = null, stop_update = null
            if int(str(proc_dic['D_reg_diff'])) > 6 and str(proc_dic['D_order_ck']) == "0" and str(proc_dic['ck_delnaver']) == "0" and str(proc_dic['D_stop_update']) == "0":
                print(">> 6개월 pass data 재등록 대상 (setDB New Insert) : {}".format(in_asin))

                goodsinfo_dic['confirm_goods'] = getQueryValue(None)
                goodsinfo_dic['UpdateDate'] = getQueryValue(None)
                goodsinfo_dic['proc_flg'] = getQueryValue("UN")
                goodsinfo_dic['proc_flg_date'] = getQueryValue(str(proc_dic['D_regdate'])[:19])
                #insert t_goods
                try:
                    db_con.insert('t_goods',goodsinfo_dic)
                    print('>> ## t_goods  insert ')
                except Exception as e:
                    print('>> Exception [t_goods]', e)
                    return "Q04"

                time.sleep(1)
                #goodscode #######################
                sql_n = "select top 1 uid from t_goods where ali_no = '{0}' and uid <> '{1}'".format(dic['parentasin'], old_guid)
                coderow = db_con.selectone(sql_n)
                now_guid = coderow[0]         

                # New Goodscode 생성후 t_goods  Update  처리
                new_goodscode = get_newgoodscode(db_con, now_guid, in_pgsite)
                if new_goodscode == "Q01":
                    return "Q01"

                # Other DB Insert #######################
                rtn_set_flg = proc_DB_other(db_con, goodsinfo_content_dic, goodsinfo_option_dic, goodsinfo_sub_dic, goodsinfo_cate_dic, dic, now_guid)
                if rtn_set_flg != "0":
                    return rtn_set_flg

                rtn_goodscode = new_goodscode               
                print(">> 신규 재등록 상품 insert goods Ok : {}".format(rtn_goodscode))           

                if str(D_naver_in) == "1": # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                    proc_ep_insert(D_goodscode,'D')
                    print('>> 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D) : {}'.format(D_goodscode))

                # 기존 데이터 Del_Naver = 4 
                sql = "UPDATE t_goods SET Del_Naver = '4', proc_flg = 'UN', proc_flg_date = getdate() where uid = {0}".format(old_guid) 
                print('>> 기존 데이터 Del_Naver = 4 (update) : {}'.format(D_goodscode))
                db_con.execute(sql)

        # elif in_pg != "goods" and procFlg == "U" and ( in_pgsite == "usa" or in_pgsite == "global" ):
        #     pass
            # regdate 24개월 pass, 주문 이력 없음, sale_ck_new = 1
            # if int(str(proc_dic['D_reg_diff'])) > 24 and str(proc_dic['D_order_ck']) == "0" and str(dic['d_sale_ck_new']) == "1":
            #     print(">> 24개월 pass data 네이버에서 미노출 전환 (Del_Naver = 5) : {}".format(in_asin))

            #     if str(D_naver_in) == "1": # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
            #         proc_ep_insert(D_goodscode,'D')
            #         print('>> 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D) : {}'.format(D_goodscode))

            #     # 기존 데이터 Del_Naver = 4 
            #     sql = "UPDATE t_goods SET Del_Naver = '5', proc_flg = 'UD', proc_flg_date = getdate() where uid = {0}".format(old_guid) 
            #     print('>> 기존 데이터 Del_Naver = 5, proc_flg = UD (update) : {}'.format(D_goodscode))
            #     db_con.execute(sql)

    dic.clear()
    goodsinfo_dic.clear()
    goodsinfo_content_dic.clear()
    goodsinfo_option_dic.clear()
    goodsinfo_sub_dic.clear()
    goodsinfo_cate_dic.clear()
    print(">> SetDB OK ASIN : " + str(in_asin))
    return "0@" + str(rtn_goodscode)


def getWeightNum(shipping_str, unit_kbn):
    shipping_weight = 1
    shipping_tmp = str(shipping_str)
    shipping_tmp = shipping_tmp.replace("\n","").replace('\u200e', '').replace('&lrm;', '').strip()
    shipping_tmp = regRemoveTextWeight(shipping_tmp).strip()

    if shipping_tmp != "":
        if shipping_tmp.replace('.','').isdigit() == True:
            if unit_kbn == "ounces":
                shipping_weight = float(shipping_tmp) * 0.0625 * 0.453592
            elif unit_kbn == "pounds":
                shipping_weight = float(shipping_tmp) * 0.453592
            elif unit_kbn == "gram":
                shipping_weight = float(shipping_tmp) * 0.001
            elif unit_kbn == "g":
                shipping_weight = float(shipping_tmp) * 0.001
            else:
                shipping_weight = float(shipping_tmp)

    return round(shipping_weight, 2)

def cutStrShipping(shipping_str):
    shipping_tmp = str(shipping_str)
    if shipping_tmp.find('<td') > -1: shipping_tmp = getparse(shipping_tmp, '<td', '</')
    if shipping_tmp.find('</') > -1: shipping_tmp = getparse(shipping_tmp, '', '</')
    if shipping_tmp.find('>') > -1: shipping_tmp = getparseR(shipping_tmp, '>', '')
    shipping_tmp = shipping_tmp.replace("\n","").replace('\u200e', '').replace('&lrm;', '').strip()

    return shipping_tmp

def getShipping_weight_new(in_soup, in_countrykbn):

    ########### shipping_weight ###########
    shipping_weight = 0
    shipping_weight_str = ""
    #print(" getShipping_weight_new check  ")

    if str(in_soup).find('id="productDetails_feature_div"') > -1:
        in_soup = getparse(str(in_soup), 'id="productDetails_feature_div"', '')
    elif str(in_soup).find('id="productDetails"') > -1:
        in_soup = getparse(str(in_soup), 'id="productDetails"', '')

    if str(in_soup).find('Shipping Weight') > -1:
        print(">> (1) Shipping Weight ")
        shipping_weight_str = getparse(str(in_soup), 'Shipping Weight', '<tr>')
        shipping_weight_str = cutStrShipping(shipping_weight_str)
    # if shipping_weight_str == "" and str(in_soup).find('Package Weight') > -1:
    #     print(">> (2) Package Weight ")
    #     shipping_weight_str = getparse(str(in_soup), 'Package Weight', '<tr>')
    #     if str(shipping_weight_str).find('prodDetAttrValue">') > -1:
    #         shipping_weight_str = getparse(shipping_weight_str, 'prodDetAttrValue">', '</')
    #     shipping_weight_str = cutStrShipping(shipping_weight_str)
    # if shipping_weight_str == "" and str(in_soup).find('Item Weight') > -1:
    #     print(">> (3) Item Weight ")
    #     shipping_weight_str = getparse(str(in_soup), 'Item Weight', '<tr>')
    #     if str(shipping_weight_str).find('<span class="a-size-base">') > -1:
    #         shipping_weight_str = getparse(shipping_weight_str, '<span class="a-size-base">', '')
    #     elif str(shipping_weight_str).find('prodDetAttrValue">') > -1:
    #         shipping_weight_str = getparse(shipping_weight_str, 'prodDetAttrValue">', '</')
    if shipping_weight_str == "" and str(in_soup).find('Shipping Weight:') > -1:
        print(">> (4) Shipping Weight: ")
        shipping_weight_str = getparse(str(in_soup), 'Shipping Weight:', '<span')
        shipping_weight_str = cutStrShipping(shipping_weight_str)
    if shipping_weight_str == "" and str(in_soup).find('Item display weight') > -1:
        print(">> (4-1) Item display weight ")
        shipping_weight_str = getparse(str(in_soup), 'Item display weight', '<tr>')
        shipping_weight_str = cutStrShipping(shipping_weight_str)

    if in_countrykbn == "JP" or in_countrykbn == "DE" or in_countrykbn == "UK" or in_countrykbn == "FR":
        if shipping_weight_str == "" and str(in_soup).find('"size-weight"') > -1:
            print(" (5) size-weight ")
            shipping_weight_str = getparse(str(in_soup), '"size-weight"', '</td></tr>')
            shipping_weight_str = getparse(shipping_weight_str, '<td class="value">', '')
            shipping_weight_str = cutStrShipping(shipping_weight_str)
        if shipping_weight_str == "" and str(in_soup).find('"shipping-weight"') > -1:
            print(" (6) shipping-weight ")
            shipping_weight_str = getparse(str(in_soup), '"shipping-weight"', '</td></tr>')
            shipping_weight_str = getparse(shipping_weight_str, '<td class="value">', '')
            shipping_weight_str = cutStrShipping(shipping_weight_str)

    if str(shipping_weight_str).strip() == "":
        print(">> (0) Shipping Weight 없음 ")
        shipping_weight = 0
    else:
        if str(shipping_weight_str).lower().find('pounds') > -1:
            shipping_weight = getWeightNum(shipping_weight_str, 'pounds')
            print(">> pounds (ok) : "+str(shipping_weight))
        elif str(shipping_weight_str).lower().find('ounces') > -1:
            shipping_weight = getWeightNum(shipping_weight_str, 'ounces')
            print(">> ounces (ok) : "+str(shipping_weight))
        elif str(shipping_weight_str).lower().find('kilogram') > -1 or str(shipping_weight_str).lower().find('kg') > -1:
            shipping_weight = getWeightNum(shipping_weight_str, 'kg')
            print(">> kg (ok) : "+str(shipping_weight))
        elif str(shipping_weight_str).lower().find('gram') > -1 or str(shipping_weight_str).find('g') > -1:
            shipping_weight = getWeightNum(shipping_weight_str, 'gram')
            print(">> gram (ok) : "+str(shipping_weight))
        else:
            shipping_weight = 1

    print(">> shipping_weight : "+str(shipping_weight))
    return shipping_weight


def getShipping_weight(in_soup, in_countrykbn):

    ########### shipping_weight ###########
    org_soup = in_soup
    shipping_weight = 0
    shipping_weight_str = ""
    #print(" getShipping_weight check  ")

    if str(in_soup).find('id="productDetails_feature_div"') > -1:
        in_soup = getparse(str(in_soup), 'id="productDetails_feature_div"', '')
    elif str(in_soup).find('id="productDetails"') > -1:
        in_soup = getparse(str(in_soup), 'id="productDetails"', '')

    if in_countrykbn == "US":
        # shipping_weight

        if str(in_soup).find('Shipping Weight') > -1:
            print(">> (2) Shipping Weight ")
            shipping_weight_str = getparse(str(in_soup), 'Shipping Weight', '<tr>')

        elif str(in_soup).find('Item Weight') > -1:
            print(">> (3) Item Weight ")
            shipping_weight_str = getparse(str(in_soup), 'Item Weight', '<tr>')

        elif str(in_soup).find('Package Weight') > -1:
            print(">> (4) Package Weight ")
            shipping_weight_str = getparse(str(in_soup), 'Package Weight', '<tr>')

        elif str(org_soup).find('Shipping Weight:') > -1:
            print(">> (1) Shipping Weight: ")
            shipping_weight_str = getparse(str(org_soup), 'Shipping Weight:', '<span')

        if str(shipping_weight_str).strip() == "":
            print(">> (5) Shipping Weight 없음 ")
            shipping_weight = 0
        else:

            if str(shipping_weight_str).find('pounds') > -1 or str(shipping_weight_str).find('Pounds')> -1:
                if str(shipping_weight_str).find('pounds') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'pounds')
                elif str(shipping_weight_str).find('Pounds') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'Pounds')

                print(">> pounds ")
                if str(shipping_weight_str).find('>') > -1:
                    shipping_weight_str = getparseR(shipping_weight_str, '>', None)
                shipping_weight = str(shipping_weight_str).strip()
                shipping_weight = shipping_weight.replace("\n","").replace('\u200e', '').replace('&lrm;', '')
                shipping_weight = regRemoveTextWeight(shipping_weight)
                print(">> pounds : "+str(shipping_weight))

                tmpWeight = ""
                tmpWeight = str(shipping_weight).strip()
                tmpWeight = tmpWeight.replace(".","")
                if tmpWeight.isdigit() == True:
                    shipping_weight = stringGetNumber(shipping_weight)
                    shipping_weight = float(shipping_weight)
                else:
                    shipping_weight = 1
                    
                print(">> pounds (ok) : "+str(shipping_weight))

            elif str(shipping_weight_str).find('ounces') > -1 or str(shipping_weight_str).find('Ounces') > -1:
                if str(shipping_weight_str).find('ounces') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'ounces')
                elif str(shipping_weight_str).find('Ounces') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'Ounces')

                #print(">> ounces ")
                if str(shipping_weight_str).find('>') > -1:
                    shipping_weight_str = getparseR(shipping_weight_str, '>', None)
                #print(">> ounces : "+str(shipping_weight))    
                shipping_weight = shipping_weight_str.strip()
                shipping_weight = shipping_weight.replace("\n","").replace('\u200e', '').replace('&lrm;', '')
                shipping_weight = regRemoveTextWeight(shipping_weight)

                tmpWeight = ""
                tmpWeight = str(shipping_weight).strip()
                tmpWeight = tmpWeight.replace(".","")
                if tmpWeight.isdigit() == True:
                    shipping_weight = stringGetNumber(shipping_weight)
                    shipping_weight = float(shipping_weight) * 0.0625
                else:
                    shipping_weight = 1

                print(">> ounces (ok) : "+str(shipping_weight))
            elif str(shipping_weight_str).find('Kilogram') > -1 or str(shipping_weight_str).find('Kg') > -1:
                if str(shipping_weight_str).find('Kilogram') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'Kilogram')
                elif str(shipping_weight_str).find('Kg') > -1:
                    shipping_weight_str = getparse(shipping_weight_str, '', 'Kg')

                #print(">> ounces ")
                if str(shipping_weight_str).find('>') > -1:
                    shipping_weight_str = getparseR(shipping_weight_str, '>', None)
                #print(">> ounces : "+str(shipping_weight))    
                shipping_weight = shipping_weight_str.strip()
                shipping_weight = shipping_weight.replace("\n","").replace('\u200e', '').replace('&lrm;', '')
                shipping_weight = regRemoveTextWeight(shipping_weight)

                tmpWeight = ""
                tmpWeight = str(shipping_weight).strip()
                tmpWeight = tmpWeight.replace(".","")
                if tmpWeight.isdigit() == True:
                    shipping_weight = stringGetNumber(shipping_weight)
                    shipping_weight = float(shipping_weight)
                else:
                    shipping_weight = 1

                print(">> Kilogram (ok) : "+str(shipping_weight))
            else:
                #print(">> else ")
                shipping_weight = 1

    elif in_countrykbn == "JP" or in_countrykbn == "DE" or in_countrykbn == "UK" or in_countrykbn == "FR":
    
        ########### shipping_weight ###########
        shipping_weight = 0
        shipping_weight_str = ""
        shipping_weight_str2 = ""

        if str(in_soup).find('"size-weight"') > -1:
            print(" (2) size-weight ")
            shipping_weight_str = getparse(str(in_soup), '"size-weight"', '</td></tr>')
            shipping_weight_str2 = getparse(shipping_weight_str, '<td class="value">', None)

        elif str(in_soup).find('Item Weight') > -1:
            print(" (3) Item-weight ")
            shipping_weight_str = getparse(str(in_soup), 'Item Weight', '</tr>')
            if str(shipping_weight_str).find('<span class="a-size-base">') > -1:
                shipping_weight_str2 = getparse(shipping_weight_str, '<span class="a-size-base">', '')
            elif str(shipping_weight_str).find('class="a-size-base prodDetAttrValue">') > -1:
                shipping_weight_str2 = getparse(shipping_weight_str, 'class="a-size-base prodDetAttrValue">', '</')

        elif str(in_soup).find('Package Weight') > -1:
            print(" (4) Package Weight ")
            shipping_weight_str = getparse(str(in_soup), 'Package Weight', '</tr>')
            shipping_weight_str2 = getparse(shipping_weight_str, 'class="a-size-base prodDetAttrValue">', '</')

        elif str(org_soup).find('"shipping-weight"') > -1:
            print(" (1) shipping-weight ")
            shipping_weight_str = getparse(str(org_soup), '"shipping-weight"', '</td></tr>')
            shipping_weight_str2 = getparse(shipping_weight_str, '<td class="value">', None)

        #print(">> weight : "+str(shipping_weight_str2))

        if str(shipping_weight_str2).find('>') > -1:
            shipping_weight_str2 = getparseR(shipping_weight_str2, '>', '')

        if shipping_weight_str2.find('Kg') > -1 or shipping_weight_str2.find('kg') > -1 or shipping_weight_str2.find('Kilograms') > -1:
            shipping_weight = shipping_weight_str2.replace('Kg', '').replace('kg', '').replace('Kilograms', '').replace('\u200e', '').replace('&lrm;', '').strip()
            shipping_weight = regRemoveTextWeight(shipping_weight)
            if shipping_weight.replace(".","").isdigit() == True:
                shipping_weight = stringGetNumber(shipping_weight)
                shipping_weight = float(shipping_weight)
            else:
                shipping_weight = 0
            #shipping_weight = float(shipping_weight)

        shipping_weight_str2 = shipping_weight_str2.strip()
        if (shipping_weight_str2 is None) or (shipping_weight_str2 == ''):
            shipping_weight = 0

    #print(">> shipping_weight : "+str(shipping_weight))
    return shipping_weight


def getDescriptionCut(in_desc):

    description_str = ""

    if str(in_desc).find('<div class="a-row a-spacing-top-base">') > -1:
        description_str = getparse(str(in_desc), '', '<div class="a-row a-spacing-top-base">')
        print("description cut(0) ")
    if str(in_desc).find('<div id="sponsoredProducts2_feature_div') > -1:
        description_str = getparse(str(in_desc), '', '<div id="sponsoredProducts2_feature_div')
        print("description cut(1) ")
    if str(in_desc).find('What other items do') > -1:
        description_str = getparse(str(in_desc), '', 'What other items do')
        print("description cut(1-1) ")
    if str(in_desc).find('<div id="sims-consolidated-4_feature_div">') > -1:
        description_str = getparse(str(in_desc), '', '<div id="sims-consolidated-4_feature_div">')
        print("description cut(2) ")
    if str(in_desc).find('<div id="like-delayed-render_feature_div">') > -1:
        description_str = getparse(str(in_desc), '', '<div id="like-delayed-render_feature_div">')
        print("description cut(3) ")
    if str(in_desc).find('<span class="a-carousel-page-count">') > -1:
        description_str = getparse(str(in_desc), '', '<span class="a-carousel-page-count">')
        print("description cut(4) ")
    if str(in_desc).find('Customers who viewed this item also viewed') > -1:
        description_str = getparse(str(in_desc), '', 'Customers who viewed this item also viewed')
        print("description cut(5-1) ")
    if str(in_desc).find('Customers who bought this item also bought') > -1:
        description_str = getparse(str(in_desc), '', 'Customers who bought this item also bought')
        print("description cut(5-2) ")
    if str(in_desc).find('Products related to this item') > -1:
        description_str = getparse(str(in_desc), '', 'Products related to this item')
        print("description cut(5-3) ")
    if str(in_desc).find('Customer questions') > -1:
        description_str = getparse(str(in_desc), '', 'Customer questions')
        print("description cut(6) ")
    if str(in_desc).find('Customer reviews') > -1:
        description_str = getparse(str(in_desc), '', 'Customer reviews')
        print("description cut(7) ")
    if str(in_desc).find('Special offers and product promotions') > -1:
        description_str = getparse(str(in_desc), '', 'Special offers and product promotions')
        print("description cut(8) ")
    if str(in_desc).find('Have a question?') > -1:
        description_str = getparse(str(in_desc), '', 'Have a question?')
        print("description cut(9) ")
    if str(in_desc).find('Compare with similar items') > -1:
        description_str = getparse(str(in_desc), '', 'Compare with similar items')
        print("description cut(9-1) ")

    if str(in_desc).find('Technical Details') > -1:
        description_str = getparse(str(in_desc), '', 'Technical Details')
        print("description cut(10) ")
    if str(in_desc).find('<div id="dpx-detail-bullets_feature_div">') > -1:
        description_str = getparse(str(in_desc), '', '<div id="dpx-detail-bullets_feature_div">')
        print("description cut(11) ")
    if str(in_desc).find('<div id="detailBullets"') > -1:
        description_str = getparse(str(in_desc), '', '<div id="detailBullets"')
        print("description cut(12) ")


    return str(description_str).strip()



def getDescriptionNew(in_soup, inCountryKbn):

    ########### description ###########
    description_str = ""
    description_tmp = ""
    pos_desc1 = -1
    pos_desc2 = -1
    description_tmp1 = ""
    description_tmp2 = ""
    description_tmp = ""

    if str(in_soup).find('<h2>Product Description</h2>') > -1:
        print("Pos1 : " + str(in_soup).find('<h2>Product Description</h2>'))
        pos_desc1 = str(in_soup).find('<h2>Product Description</h2>')

    if str(in_soup).find('<h2>From the Manufacturer</h2>') > -1:
        print("Pos2 : " + str(in_soup).find('<h2>Product Description</h2>'))
        pos_desc2 = str(in_soup).find('<h2>From the Manufacturer</h2>')

    if pos_desc1 > -1 and pos_desc2 == -1: # Product Description 만 존재
        print(" Product Description 만 존재 ")
        #description_tmp1 = getparse(str(in_soup), '<h2>Product Description</h2>', '')
        description_tmp1 = str(in_soup)[pos_desc1:]
        description_tmp1 = getDescriptionCut(description_tmp1)

    elif pos_desc1 == -1 and pos_desc2 > -1: # From the Manufacturer 만 존재
        print(" From the Manufacturer 만 존재 ")
        #description_tmp2 = getparse(str(in_soup), '<h2>From the Manufacturer</h2>', '')
        description_tmp2 = str(in_soup)[pos_desc2:]
        description_tmp2 = getDescriptionCut(description_tmp2)

    elif pos_desc1 > -1 and pos_desc2 > -1: # 둘다 존재
        print(" desc1 and desc2 둘다 존재 ")
        if pos_desc1 > pos_desc2:
            print(" From the Manufacturer 앞(1)")
            #description_tmp2 = getparse(str(in_soup), '<h2>From the Manufacturer</h2>', '')
            description_tmp2 = str(in_soup)[pos_desc2:]
            description_tmp2 = getDescriptionCut(description_tmp2)
            if str(description_tmp2).find('<h2>Product Description</h2>') > -1:
                description_tmp2 = getparse(str(description_tmp2), '', '<h2>Product Description</h2>')
                print("description cut ")
        else:
            print(" Product Description 앞(1)")
            #description_tmp1 = getparse(str(in_soup), '<h2>Product Description</h2>', '')
            description_tmp1 = str(in_soup)[pos_desc1:]
            description_tmp1 = getDescriptionCut(description_tmp1)

            if str(description_tmp1).find('<h2>From the Manufacturer</h2>') > -1:
                description_tmp1 = getparse(str(description_tmp1), '', '<h2>From the Manufacturer</h2>')
                print("description cut ")

    elif pos_desc1 == -1 and pos_desc2 == -1:
        description_tmp = ""
        print(" desc1 no and desc2 no")
        if str(in_soup).find('<div id="productDescription" class="a-section a-spacing-small">') > -1:
            print("description (00)")
            description_tmp = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">','')
            description_tmp = getDescriptionCut(description_tmp)

    if str(description_tmp1) != "":
        print("Product Description OK")
        description_tmp = description_tmp + '<h2>Product Description</h2>' + '<br><br>' + description_tmp1

    if str(description_tmp2) != "":
        print("From the Manufacturer OK")
        description_tmp = description_tmp + '<h2>From the Manufacturer</h2>' + '<br><br>' + description_tmp2

    if str(description_tmp).strip() == "":
        print("description (last check)")
        if str(in_soup).find('<div id="productDescription" class="a-section a-spacing-small">') > -1:
            print("description (productDescription)")
            description_tmp = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">', '')
            description_tmp = getDescriptionCut(description_tmp)

    if str(description_tmp).strip() != "":
        description_tmp = getDescriptionCut(description_tmp)
        description_tmp = str(description_tmp).replace('Amazon.co.jp', '').replace('Amazon.com', '')
        description_tmp = str(description_tmp).replace('<noscript>', '').replace('</noscript>', '')
        description_tmp = str(description_tmp).replace('asin', '').replace('ASIN', '')
        description_tmp = str(description_tmp).replace('Update Button', '')

    else:
        print("description_tmp No : "+str(description_tmp))

    return str(description_tmp).strip()



def getDescription(in_soup, inCountryKbn):

    ########### description ###########
    description_str = ""
    description_tmp = ""

    if str(in_soup).find('<div id="productDescription" class="a-section a-spacing-small">') > -1:
        #print("description (1)")
        description_str = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">','</div>')

        if str(description_str).find('<div class="disclaim">') > -1:
            print('>> description (class="disclaim" 있음) ')
            description_str = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">','<style type="text/css">')
            description_pos2 = str(description_str).rfind('</div>')
            description_str = description_str[:description_pos2]

    if str(description_str).strip() == "" and str(in_soup).find('<div id="productDescription" class="a-section a-spacing-small">') > -1:
        print(">> description (1) -1 ")
        description_str = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">','</div></div>')

    if description_str == "":
        in_soup_desc = str(in_soup)
    else:
        in_soup_desc = description_str
        description_tmp = description_str

    if str(in_soup_desc).find('Description du produit  </h2>') > -1:
        description_tmp = getparse(str(in_soup_desc), 'Description du produit  </h2>', '')
    elif str(in_soup_desc).find('<h2>Description du produit</h2>') > -1:
        description_tmp = getparse(str(in_soup_desc), '<h2>Description du produit</h2>', '')
    elif str(in_soup_desc).find('<h2>Détails sur le produit</h2>') > -1:
        description_tmp = getparse(str(in_soup_desc), '<h2>Détails sur le produit</h2>', '')
    elif str(in_soup_desc).find('<h2>Product Description</h2>') > -1:
        description_tmp = getparse(str(in_soup_desc), '<h2>Product Description</h2>', '')
    
    if str(description_tmp).find('class="a-carousel-heading a-inline-block"') > -1:
        description_str = getparse(str(description_tmp), '', 'class="a-carousel-heading a-inline-block"')
    elif str(description_tmp).find('id="ask-btf_feature_div"') > -1:
        description_str = getparse(str(description_tmp), '', 'id="ask-btf_feature_div"')
    elif str(description_tmp).find('class="a-carousel-pagination a-size-base"') > -1:
        description_str = getparse(str(description_tmp), '', 'class="a-carousel-pagination a-size-base"')
    elif str(description_tmp).find('Products related to this item') > -1:
        description_str = getparse(str(description_tmp), '', 'Products related to this item')
    elif str(description_tmp).find('Produits liés à cet article') > -1:
        description_str = getparse(str(description_tmp), '', 'Produits liés à cet article')
    elif str(description_tmp).find('class="a-divider-normal bucketDivider"') > -1:
        description_str = getparse(str(description_tmp), '', 'class="a-divider-normal bucketDivider"')
    elif str(description_tmp).find('Customer questions & answers') > -1:
        description_str = getparse(str(description_tmp), '', 'Customer questions & answers')
    elif str(description_tmp).find('Customer reviews') > -1:
        description_str = getparse(str(description_tmp), '', 'Customer reviews')
    elif str(description_tmp).find('<div id="detailBullets"') > -1:
        description_str = getparse(str(description_tmp), '', '<div id="detailBullets"')
    elif str(description_tmp).find('id="customerReviews"') > -1:
        description_str = getparse(str(description_tmp), '', 'id="customerReviews"')

    print(">> description (2) Product Description ")
    #description_str = getparse(str(in_soup), '<h2>Product Description</h2>', '<div id="detailBullets"')
    description_str = str(description_str).replace('<noscript>', '').replace('</noscript>', '')

    if str(in_soup).find('<h2>From the Manufacturer</h2>') > -1:
        if str(description_str).find('From the Manufacturer') == -1:
            description_tmp = ""
            print(">> description (1) From the Manufacturer 있음")
            description_tmp = getparse(str(in_soup), '<h2>From the Manufacturer</h2>', 'Customer questions')
            description_str = description_str + '<br><br><h2>From the Manufacturer</h2><br><br>' + description_tmp
            print(">> description (1) bucketDivider plus ")
    else:
        print(">> description (1) bucketDivider 없음")

    if str(description_str).strip() == "" and str(in_soup).find('id="aplus_feature_div"') > -1:
        print(">> description (3) productDescription")
        description_str = getparse(str(in_soup), 'id="aplus_feature_div"', '')
    if str(description_str).strip() == "" and str(in_soup).find('id="productDescription">') > -1:
        print(">> description (3) productDescription")
        description_str = getparse(str(in_soup), 'id="productDescription">', '</div>')
    if str(description_str).strip() == "" and str(in_soup).find('<div id="dpx-aplus-3p-product-description_feature_div">') > -1:
        print(">> description (4) dpx-aplus-3p-product-description_feature_div")
        description_str = getparse(str(in_soup), '<div id="dpx-aplus-3p-product-description_feature_div">', '</div></div>')
    if str(description_str).strip() == "" and str(in_soup).find('<div id="productDescription" class="a-section a-spacing-small">') > -1:
        print(">> description (5) productDescription a-section a-spacing-small")
        description_str = getparse(str(in_soup), '<div id="productDescription" class="a-section a-spacing-small">', '</div>')
    if str(description_str).strip() == "" and str(in_soup).find('<div class="pfDescContent">') > -1:
        print(">> description (6) pfDescContent ")
        description_str = getparse(str(in_soup), '<div class="pfDescContent">','')
        if str(description_str).find('<div id="productFactsToggleButton"') > -1:
            description_str = getparse(str(description_str), '','<div id="productFactsToggleButton"')
        else:
            description_str = getparse(str(description_str), '','</div> </div>')

    if str(description_str).strip() == "":
        print(">> description (6) 없음")
    else:
        if str(description_str).find('<div class="a-row a-spacing-top-base">') > -1:
            description_str = getparse(str(description_str),'','<div class="a-row a-spacing-top-base">')
            print(">> description cut(0) ")
        if str(description_str).find('<div id="sponsoredProducts2_feature_div') > -1:
            description_str = getparse(str(description_str),'','<div id="sponsoredProducts2_feature_div')
            print(">> description cut(1) ")
        if str(description_str).find('What other items do') > -1:
            description_str = getparse(str(description_str),'','What other items do')
            print(">> description cut(1-1) ")
        if str(description_str).find('<div id="sims-consolidated-4_feature_div">') > -1:
            description_str = getparse(str(description_str),'','<div id="sims-consolidated-4_feature_div">')
            print(">> description cut(2) ")
        if str(description_str).find('<div id="like-delayed-render_feature_div">') > -1:
            description_str = getparse(str(description_str),'','<div id="like-delayed-render_feature_div">')
            print(">> description cut(3) ")
        if str(description_str).find('<span class="a-carousel-page-count">') > -1:
            description_str = getparse(str(description_str),'','<span class="a-carousel-page-count">')
            print(">> description cut(4) ")
        if str(description_str).find('Customers who viewed this item also viewed') > -1:
            description_str = getparse(str(description_str), '', 'Customers who viewed this item also viewed')
            print(">> description cut(5-1) ")
        if str(description_str).find('Customers who bought this item also bought') > -1:
            description_str = getparse(str(description_str),'','Customers who bought this item also bought')
            print(">> description cut(5-2) ")
        if str(description_str).find('Products related to this item') > -1 or str(description_str).find('4 étoiles et plus') > -1:
            description_str = getparse(str(description_str), '', 'Products related to this item')
            print(">> description cut(5-3) ")
        if str(description_str).find('class="sp_desktop_sponsored_label"') > -1:
            description_str = getparse(str(description_str), '', 'class="sp_desktop_sponsored_label"')
            print(">> description cut(5-3-1) ")
        if str(description_str).find('Customer questions') > -1:
            description_str = getparse(str(description_str), '', 'Customer questions')
            print(">> description cut(6) ")
        if str(description_str).find('Customer reviews') > -1:
            description_str = getparse(str(description_str), '', 'Customer reviews')
            print(">> description cut(7) ")
        if str(description_str).find('Special offers and product promotions') > -1:
            description_str = getparse(str(description_str),'','Special offers and product promotions')
            print(">> description cut(8) ")
        if str(description_str).find('Have a question?') > -1:
            description_str = getparse(str(description_str),'','Have a question?')
            print(">> description cut(9) ")
        if str(description_str).find('Compare with similar items') > -1:
            description_str = getparse(str(description_str), '', 'Compare with similar items')
            print(">> description cut(9-1) ")
        if str(description_str).find('Technical Details') > -1:
            description_str = getparse(str(description_str), '', 'Technical Details')
            print(">> description cut(10) ")
        if str(description_str).find('<div id="dpx-detail-bullets_feature_div">') > -1:
            description_str = getparse(str(description_str), '', '<div id="dpx-detail-bullets_feature_div">')
            print(">> description cut(11) ")
        if str(description_str).find('<div class="a-cardui-body">') > -1:
            description_str = getparse(str(description_str), '', '<div class="a-cardui-body">')
            print(">> description cut(11-2) ")
        if str(description_str).find('<div id="detailBullets"') > -1:
            description_str = getparse(str(description_str), '', '<div id="detailBullets"')
            print(">> description cut(12) ")

    if str(description_str).strip() != "":
        description_str = str(description_str).replace('<noscript>', '').replace('</noscript>', '')
        description_str = str(description_str).replace('asin ', '').replace('ASIN ', '').replace('ASIN\n', '')
        description_str = str(description_str).replace('Update Button ', '')

#############################################
    # path_file = os.getcwd()
    # with open(path_file + "/log/amzon_description2.html","w",encoding="utf8") as f: 
    #     f.write(str(description_str))
#############################################
    return description_str


def setGoodsdelProc(db_con, in_DUid, in_DIsDisplay, in_DOptionKind):

    db_con.delete('t_goods_sub', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_category', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_option', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_content', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods', "uid = '{0}'".format(in_DUid))

    print('>> (setGoodsdelProc) t_goods (delete ok) : {}'.format(in_DUid))

    return "0"


def checkOrder(in_code):

    rtnCnt = ""
    rtnGoodsuid = ""
    rtnGoodscode = "E"
    rtnSitecate = ""

    time.sleep(1)
    searchurl = "http://59.23.231.204:8090/service/search.json?cn=freeship&fl=GOODSUID,goodscode,sitecate&se={goodscode:ALL(" +str(in_code)+ "):100:15}&sn=1&ln=10"
    print(">> searchurl : "+str(searchurl))

    try:
        print('>> searchurl Connect ')
        req: Request = Request(searchurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                random.random()) + ' Safari/537.36', 'Referer': 'https://www.freeship.co.kr'})
        connection = urlopen(req)

    except Exception as ex:
        print('>> checkOrder error (E): ', ex)
        #os._exit(1)
        return "E"
    else:
        rtnGoodscode = ""
        resultSoup = BeautifulSoup(connection, "html.parser")
        rtnCnt = getparse(str(resultSoup), '"total_count":', ',')
        rtnGoodsuid = getparse(str(resultSoup), '"GOODSUID":"', '"')
        rtnGoodscode = getparse(str(resultSoup), '"GOODSCODE":"', '"')
        rtnSitecate = getparse(str(resultSoup), '"SITECATE":"', '"')

        #print(str(rtnGoodsuid) + " | " + str(rtnGoodscode) + " | " + str(rtnSitecate))
        if rtnGoodscode != "":
            print(">> 주문 내역 있음 : " + str(rtnGoodscode) + " | " + str(rtnSitecate) + " | " + str(rtnGoodsuid))
        else:
            print(">> 주문 내역 없음 : " + str(rtnGoodscode))

    return str(rtnGoodsuid)

def get_replace_title(str_title):

    tmp_title = str(str_title).strip()
    tmp_title = tmp_title.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ').replace("&lt;","<").replace("&gt;",">")
    tmp_title = tmp_title.replace("&ndash;","-").replace("&times;"," x ").replace("&rdquo;","").replace('–','-').replace('「',' ').replace('」',' ')
    tmp_title = tmp_title.replace("&quot;","").replace("\\", "").replace("★","").replace("◆","").replace('"', '').strip()

    return tmp_title

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

def procTranConect(browser, in_asin, in_site, option_max_count, proc_flg):
    result_tran = ""
    if proc_flg == "option":
        tran_url = 'https://{}.freeship.co.kr/_GoodsUpdate/title_tran_{}_option_image.asp?asin={}'.format(in_site, in_site, in_asin)
    else:
        tran_url = 'https://{}.freeship.co.kr/_GoodsUpdate/title_tran_{}.asp?asin={}'.format(in_site, in_site, in_asin)
    if in_site == "fr":
        tran_url = tran_url.replace("fr.freeship.co.kr","uk.freeship.co.kr")
    print(">> tran_url : {}".format(tran_url))
    try:
        browser.get(tran_url)
    except Exception as e:
        print('>> exception procTranConect ')
    else:
        time.sleep(random.uniform(4,6))
        if option_max_count > 25:
            moveScroll(browser)
        time.sleep(1)
        #result_tran = browser.find_element(By.ID,'google_translate_element').get_attribute("outerHTML")
        result_tran = str(browser.page_source)
        #print(">> result_tran : {}".format(result_tran))
    return result_tran

def replace_main_str(in_str):
    result_str = str(in_str).strip()
    result_str = result_str.replace('</font>','').replace('</FONT>','').replace('<font style="vertical-align: inherit;">','').replace('</font></font>','')
    result_str = result_str.replace('&amp;','').replace("<p>","").replace("</p>","").replace("<P>","").replace("</P>","").replace("<pre>","").replace("</pre>","").replace("<PRE>","").replace("</PRE>","")
    result_str = result_str.replace("<xmp>","").replace("</xmp>","").replace("<XMP>","").replace("</XMP>","")
    result_str = result_str.replace("...","").replace("  "," ").replace("&nbsp;"," ").replace("<br>","").strip()
    return result_str

def getTranTitle(result_tmp, in_asin):
    tran_title = ""
    if str(result_tmp).find(in_asin) > -1:
        tran_title = getparse(result_tmp,'<div id="google_translate_element">','<hr>')
        tran_title = getparse(tran_title,'<input type="hidden"','')
        tran_title = getparse(tran_title,'">','')
        tran_title = replace_main_str(tran_title)
        tran_title = tran_title.replace("- ChinaglobalMall","").strip()
    return str(tran_title)

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

def desc_replace(descript):
    target_desc = str(descript)

    sp_desc = target_desc.split('<a ')
    for ea_desc in sp_desc:
        if ea_desc.find('href="') > -1:
            tmp_href = getparse(ea_desc, 'href="', '"')
            #print(">> tmp_href : {}".format(tmp_href))
            target_desc = target_desc.replace('href="' + str(tmp_href) +'"','href="#"')

#############################################
    # path_file = os.getcwd()
    # with open(path_file + "/log/amzon_description3.html","w",encoding="utf8") as f: 
    #     f.write(str(target_desc))
#############################################

    return target_desc


## parsing_detail #######################################
def parsing_detail(in_soup, in_asin, goods, db_con, db_price, in_drive, in_pg, in_countryKbn, in_pgsite, manage_dic):
    global cnt_title_tran
    currSymbol = ""
    stock_flg = "0"

    ########### price / gallery / review ###########
    in_cateidx = goods['catecode']
    catecode = in_cateidx
    in_price = float(goods['price'])
    in_DB_weight = goods['db_Weight']
    in_guid = goods['guid']
    #in_title = goods['db_title']
    in_old_title = goods['db_title']
    in_org_title = goods['db_org_title']

    # title
    ori_title = ""
    chk_title = ""
    ori_title = getparse(str(in_soup), 'id="productTitle"', '')
    if ori_title.rfind('">') > -1:
        ori_title = getparse(ori_title, '">', '</span>')
    print('>> title(ORI) : ' + str(ori_title[:80]))
    chk_title = get_replace_title(ori_title)

    ########### title (checkForbidden_new) ###########
    ban_title_list = manage_dic['ban_title_list']
    forbidden_flag = checkForbidden_new(chk_title, ban_title_list)
    if str(forbidden_flag) == "0":
        pass
    else:
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

    # (사이트 DB) title 금지어 체크 ###########
    replace_site_title_list = manage_dic['replace_site_title_list']
    forbidden_flag_site = checkForbidden_site(chk_title, catecode, replace_site_title_list)
    if str(forbidden_flag_site) != "0":
        print('>> checkForbidden_site : '+str(forbidden_flag_site))
        return "D03 :" + " ( site: " + forbidden_flag_site[2:] + " ) "

    if len(chk_title) < 5:
        print('>> title len < 5 ')
        return "D02"

    chk_title = chk_title.replace("'", "")
    if in_countryKbn == "JP":
        currSymbol = "¥"
    elif in_countryKbn == "US":
        currSymbol = "$"
    elif in_countryKbn == "DE":
        currSymbol = "$"
    elif in_countryKbn == "UK":
        currSymbol = "£"
    elif in_countryKbn == "FR":
        currSymbol = "€"
    time.sleep(1)

    ########### title ###########
    goods_title = chk_title.replace(r'\x26', ' & ').replace("'", "`").replace(","," ").replace("&rdquo;"," ").replace('”',' ').replace('“',' ').replace('„',' ').replace('・','.')
    goods_title = goods_title.replace('&AMP;',' ').replace('&NBSP;',' ').replace("~"," ").replace("[","(").replace("]",")").replace('"', '')
    goods_title = replaceQueryString(goods_title)

    replace_title_list = manage_dic['replace_title_list']
    goods_title = replaceTitle(goods_title, replace_title_list)

    if goods_title[-1:] == ".":
        goods_title = goods_title[:-1]
    if goods_title[-1:] == "|":
        goods_title = goods_title[:-1]
    goods_title = str(goods_title).replace("  ", " ").strip()

    print('>> goods_title (final) : ' + str(goods_title[:80]))
    if str(goods_title).strip() == "" or len(goods_title) < 5:
        print('>> no title ')
        return "D02"

    #####################################################################################
    goods['forbidden'] = 'F'
    if in_countryKbn == "JP":
        goods['JP_title'] = goods_title
    else:
        goods['IT_title'] = goods_title
    goods['goods_title'] = goods_title
    if in_guid != "" and in_org_title == goods_title: # 기존 org title 과 파싱 title 비교
        print(">> 타이틀 변화없음 ")
        goods['goods_title'] = in_old_title # 기존 DB title 그대로 반영 

    ########### image ########### 
    # 변경대상 (https://m.media-amazon.com/images/W/WEBP_xxxxx/images/I/xxxx.jpg) -> https://m.media-amazon.com/images/I/xxxx.jpg
    # 변경대상 (https://m.media-amazon.com/images/W/IMAGERENDERING_xxxxx/images/I/xxxx.jpg) -> https://m.media-amazon.com/images/I/xxxx.jpg
    # Img 소스 변경 
    mainImg = ""
    naverImg = ""
    imglist = getparse(str(in_soup),"'colorImages':", "</script>")
    if imglist.find('"large":"') == -1:
        print('>> no Img ')
        return "D19"  # No img

    spImgList = imglist.split('},{')
    imgList = []
    imgCnt = 0
    flg_noimg = "0"
    for ea_img in spImgList:
        if str(ea_img).find('"hiRes":"') > -1:
            imgUrl = getparse(ea_img,'"hiRes":"','"')
            if imgUrl.find('/images/W/MEDIAX_') > -1:
                pass
            elif imgUrl.find('/images/W/') > -1:
                repImgStr = getparse(imgUrl,'/images/W/','/images/I/')
                imgUrl = imgUrl.replace('/images/W/'+ str(repImgStr),'')
                print(">>(after) (/images/W/) -> imgUrl : {}".format(imgUrl))
            if naverImg == "" and imgUrl != "": 
                if str(imgUrl).find('.jpg') > -1 or str(imgUrl).find('.JPG') > -1:
                    imgUrl = getparse(imgUrl, '', '._') + '.jpg'
                naverImg = imgUrl
        else:
            imgUrl = getparse(ea_img,'"large":"','"')
            if imgUrl.find('/images/W/') > -1:
                repImgStr = getparse(imgUrl,'/images/W/','/images/I/')
                imgUrl = imgUrl.replace('/images/W/'+ str(repImgStr),'')
                print(">>(after) (/images/W/) -> imgUrl : {}".format(imgUrl))

        if str(imgUrl).find('21EvqGR5jyL.') > -1:
            print('>> Noimg : '+str(imgUrl))
            flg_noimg = "1"
            break
        if str(imgUrl).find('01MKUOLsA5L.') > -1:
            print('>> Noimg : '+str(imgUrl))
            flg_noimg = "1"
            break
        if str(imgUrl).find('21i3Jn-5C5L.') > -1:
            print('>> Noimg : '+str(imgUrl))
            flg_noimg = "1"
            break

        if imgUrl.lower().find('.jpg') > -1 or imgUrl.lower().find('.jpeg') > -1 or imgUrl.lower().find('.png') > -1:
            if mainImg == "":
                mainImg = imgUrl
            else:
                imgCnt = imgCnt + 1
                imgList.append(imgUrl)
                if imgCnt >= 5:
                    break
    print(">> imgList : {}".format(imgList))
    print(">> mainImg : {}".format(mainImg))

    if str(mainImg).strip() == "":
        print('>> no Img ')
        return "D19"  # No img     
    if flg_noimg == "1":
        print('>> no Img ')
        return "D19" # No img

    if str(naverImg) != "":
        goods['naver_img'] = naverImg
    else:
        goods['naver_img'] = None
    goods['mainimage'] = mainImg
    goods['image'] = imgList

    ########### feature ###########
    featureList = []
    featureList = get_feature(in_soup)
    goods['feature'] = featureList
    print('>> feature OK ')
    #print('>> featureList : '+str(featureList))
    if str(featureList).find('We are required to verify the age of the purchaser ') > -1:
        print('>> feature : 주류 판매 전에 구매자의 연령을 확인 ')

    ########### shipping_weight ###########
    shipping_weight = "0"
    print('>> in_DB_weight : ' + str(in_DB_weight))

    try:
        shipping_weight = getShipping_weight_new(str(in_soup), in_countryKbn)
    except Exception as ex:  # 에러 종류
        print('>> getShipping_weight_new error (SKIP) : '+str(ex))
        shipping_weight = "1"

    if float(in_DB_weight) > float(shipping_weight):
        shipping_weight = in_DB_weight

    if float(shipping_weight) < 1:
        shipping_weight = "0"

    if float(shipping_weight) > 30:
        print('>> shipping_weight 30kg over : ' + str(shipping_weight))
        if in_countryKbn == "US":
            print(">> Weight Check Please ... ")
        else:
            return "D11" + " ( " + str(shipping_weight) + " )"  # shipping_weight 30kg (SKIP)

    goods['shipping_weight'] = shipping_weight
    print('>> shipping_weight : ' + str(shipping_weight))

    ######### shipping_category_weight / catecode의 minus_opt 플래그 확인 #############################
    d_minus_opt = ""
    d_coupon = ""
    c_weight = 0
    d_sale_ck_new = '0'
    sql2 = "select top 1 isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(weight,0), isnull(sale_ck_new,'0') from t_category where CateCode = '{0}'".format(in_cateidx)
    print(">> sql2 : {}".format(sql2))
    rsCate = db_con.selectone(sql2)
    if rsCate:
        d_minus_opt = rsCate[0].strip()
        d_coupon = rsCate[1]
        c_weight = rsCate[2]
        d_sale_ck_new = rsCate[3]

    goods['d_sale_ck_new'] = d_sale_ck_new
    if float(shipping_weight) < float(c_weight):
        goods['shipping_weight'] = c_weight

    ########### shipping_price ###########
    shipping_price = 0
    shipping_price_str = ""
    if str(in_soup).find('data-asin-shipping="') > -1:
        shipping_price_str = getparse(str(in_soup), 'data-asin-shipping="', '"').strip()
        #print('shipping_price_str : ' + str(shipping_price_str))
        if str(shipping_price_str).strip() != '':
            shipping_price = float(shipping_price_str)
        else:
            shipping_price = 0
    else:
        shipping_price = 0

    shipping_price_str = str(in_soup)
    if str(in_soup).find('id="quantity"') > -1:
        shipping_price_str = getparse(str(in_soup), '', 'id="quantity"').strip()
    elif str(in_soup).find('id="olpLinkWidget_feature_div"') > -1:
        shipping_price_str = getparse(str(in_soup), '', 'id="olpLinkWidget_feature_div"').strip()
    elif str(in_soup).find('id="moreBuyingChoices_feature_div"') > -1:
        shipping_price_str = getparse(str(in_soup), '', 'id="moreBuyingChoices_feature_div"').strip()

    if str(in_soup).find('data-csa-c-delivery-price="') > -1:
        shipping_price_str = getparse(str(shipping_price_str), 'data-csa-c-delivery-price="', '"').strip()
        print('>> 추가배송비 (2) data-csa-c-delivery-price : ' + str(shipping_price_str))
        if in_pgsite == "fr":
            shipping_price_str = str(shipping_price_str).replace(',','').replace('\u202f', '').replace('u202f', '').strip()
        else:
            shipping_price_str = str(shipping_price_str).replace(',','').strip()
        shipping_price_str = replace_currency(shipping_price_str)
        shipping_price_str = regRemoveText(shipping_price_str)
        if str(shipping_price_str).strip() != '':
            if str(shipping_price_str).replace(".","").isdigit() == True:
                shipping_price = float(shipping_price_str)
        else:
            shipping_price = 0
    elif str(in_soup).find('<span id="price-shipping-message"') > -1:
        shipping_price_str = getparse(str(shipping_price_str), '<span class="a-color-secondary a-size-base">+', 'shipping</span>').strip()
        print('>> 추가배송비 (1) price-shipping-message : ' + str(shipping_price_str))
        if in_pgsite == "fr":
            shipping_price_str = str(shipping_price_str).replace(',','').replace('\u202f', '').replace('u202f', '').strip()
        else:
            shipping_price_str = str(shipping_price_str).replace(',','').strip()
        shipping_price_str = replace_currency(shipping_price_str)
        shipping_price_str = regRemoveText(shipping_price_str)
        if str(shipping_price_str).strip() != '':
            if str(shipping_price_str).replace(".","").isdigit() == True:
                shipping_price = float(shipping_price_str)
        else:
            shipping_price = 0

    goods['shipping_price'] = shipping_price
    print('>> shipping_price : '+str(shipping_price))

    if in_countryKbn == "US" or in_countryKbn == "DE":
        if float(shipping_price) > 20.0:
            print('>> shipping_price 20달러 over : ' + str(shipping_price))
            return "D11" + " ( " + str(shipping_price) + " )"  # shipping_price 20달러 (SKIP)
    elif in_countryKbn == "UK" or in_countryKbn == "FR":
        if float(shipping_price) > 11.0:
            print('>> shipping_price 11파운드 over : ' + str(shipping_price))
            return "D11" + " ( " + str(shipping_price) + " )"  # shipping_price 11파운드 (SKIP)
    elif in_countryKbn == "JP":
        if float(shipping_price) > 2000:
            print('>> shipping_price 2000 over : ' + str(shipping_price))
            return "D11" + " ( " + str(shipping_price) + " )"  # shipping_price 2000 (SKIP)

    ########### description ###########
    description_str = ""
    description_str = getDescription(str(in_soup), in_countryKbn)
    description_str = description_str.replace(in_asin,'').replace('warranty ','**').replace('garantie ','**')
    if str(description_str).find("Medical Device Certification Number") > -1 or str(description_str).find("Numéro de certification du dispositif médical") > -1:
        print("(skip) Medical Device Certification Number ")
        return "D22"

    if str(description_str).find("Managed medical device") > -1:
        print("(skip) Managed medical device ")
        return "D22"

    if str(description_str).find("医療機器届休番号") > -1:
        print("(skip) 医療機器届休番号")
        return "D22"

    description_str = desc_replace(description_str)
    goods['description'] = description_str
    print('>> description OK')
    description_test = getparse(str(in_soup), 'Product Details', 'Description')

    ########### stock ###########
    stock_tmp = '0'
    stock_flg = "0"
    if str(in_soup).find('id="availability"') > -1:
        stock_chk = getparse(str(in_soup), 'id="availability"', '</span>')
        stock_chk = str(stock_chk).strip()
        #print("stock_chk :" + str(stock_chk))

        if stock_chk.find('Only ') > -1:
            stock_chk = getparse(str(stock_chk), 'Only', 'left')
            stock_chk = stock_chk.strip()
            #print("stock_chk :" + str(stock_chk))
            if stock_chk != "" and stock_chk.isdigit() == True:
                stock_tmp = str(stock_chk)
        elif stock_chk.find('In stock on') > -1:
            stock_tmp = '0'
        elif stock_chk.find('In Stock.') > -1 or stock_chk.find('En stock') > -1:
            stock_tmp = '99999'

        if stock_chk.find('Temporarily out of stock') > -1:
            stock_flg = "1"
            print('>> Temporarily out of stock ')
            #return "D06"  # Temporarily out of stock

        if stock_chk.find('stock temporaire') > -1:
            stock_flg = "1"
            print('>> Temporarily out of stock (En rupture de stock temporaire)')
            #return "D06"  # Temporarily out of stock
            print(">> Temporarily out of stock : {}".format(in_asin))
            if in_pgsite == "fr":
                in_drive.get_screenshot_as_file("C:\\project\\log\\result_amzon_stock_"+str(in_asin)+".html")

    print('>> stock_tmp : ' + str(stock_tmp))
    goods['stock_tmp'] = stock_tmp

    ########### option ###########
    base_price = float(in_price)
    base_tmp_price = float(in_price)
    print('>> base_price (before) :  ' + str(base_price))
    print('>> base_tmp_price (before) :  ' + str(base_tmp_price))
    goods['base_price'] = float(in_price)
    goods['base_tmp_price'] = float(in_price)
    goods['minus_opt'] = ""
    goods['coupon'] = "" 

    opmaxlen = 0
    option_flg = ""
    option_pos = str(in_soup).find('"parentAsin" : "')
    if option_pos == -1:
        print('>> no option goods : '+str(in_asin))
        option_ck = None
        option_flg = "0"
        goods['parentasin'] = in_asin
        goods['display_ali_no'] = in_asin
        goods['many_option'] = '0'
        goods['optionkind'] = option_ck
        print('>> optionkind :  ' + str(option_ck))
        parentasin = in_asin
        # Temporarily out of stock (No Option)
        if stock_flg == "1":
            print('>> Temporarily out of stock ')
            return "D06"  # Temporarily out of stock

    else:
        print('>> option goods : '+str(in_asin))
        option_ck = 300
        option_flg = "1"
        option_kind_count = 0
        parentasin = getparse(str(in_soup), '"parentAsin" : "', '"')
        subasin_str = getparse(str(in_soup), '"dimensionToAsinMap" : {', '}')
        option_value_str = getparse(str(in_soup), '"dimensionValuesDisplayData" : {', '},')
        option_type_str = getparse(str(in_soup), '"variationDisplayLabels" : {', '}')
        option_kind_count = len(str(option_type_str).split(','))
        option_type_items = option_type_str.split('":"')
        print('>> parent : ' + str(parentasin))
        print('>> option_kind_count : ' + str(option_kind_count))

        otlow = 1
        option_type = ''
        while otlow < len(option_type_items):
            ea_option_type = getparse(option_type_items[otlow], None, '"')
            en_ea_option_type_str = ea_option_type
            option_type = option_type + '|' + en_ea_option_type_str
            #print('>> option type : ' + str(option_type))
            otlow += 1

        goods['parentasin'] = parentasin
        goods['display_ali_no'] = in_asin
        goods['option_type'] = option_type[1:]
        goods['optionkind'] = option_ck
        print('>> optionkind :  ' + str(option_ck))
        print('>> option type : ' + str(option_type[1:]))
        subasin_items = subasin_str.split('":"')
        subasin_set = []
        temp_option_asin_set = []
        oplow = 1
        resetlow = 1

        option_value_tran_arr = []
        option_image_tran_arr = []
        option_value_org_dic = dict()
        option_value_dic = dict()
        option_price_dic = dict()
        option_img_dic = dict()
        option_cnt = len(subasin_items) - 1
        #print('>> option_value_str : ' + str(option_value_str))

        if option_cnt > 25:
            print('>> option 25 over : ' + str(len(subasin_items) - 1))
            opmaxlen = 25
            goods['many_option'] = '1'
        else:
            print('>> option 25 miman : ' + str(len(subasin_items) - 1))
            opmaxlen = option_cnt
            goods['many_option'] = '0'
        #print('>> option Time (S) :  ' + str(datetime.datetime.now()))
        #print('>> option_cnt : ' + str(option_cnt) + ' | opmaxlen :  ' + str(opmaxlen))

        temp_option_asin_set = []
        #print('>> (DB) minus_opt : '+str(d_minus_opt))
        print('>> (DB) goods table coupon : '+str(d_coupon))

        goods['minus_opt'] = str(d_minus_opt)
        goods['coupon'] = str(d_coupon)
        print('>> (DB) goods minus_opt : '+str(goods['minus_opt']))

        ######### catecode의 minus_opt 플래그 확인 #############################

        flg_opt_chk = "0"
        optFirstChkFlg = "0"
        oplow = 1
        ea_price_last_asin = ""
        itemaisnTmp = ""
        print('======================================')
        while oplow < opmaxlen+1:
            option_value_tran_dic = {}
            ea_asin = getparse(subasin_items[oplow], None, '"')

            ########### option code ###########
            subasin_set.append(ea_asin)
            temp_option_asin_set.append(parentasin + '@' + ea_asin + '@' + str(''))
            if itemaisnTmp == "":
                itemaisnTmp = itemaisnTmp + ea_asin
            else:
                itemaisnTmp = itemaisnTmp + "," + ea_asin
            ########### option name ###########
            ea_option_value_str = getparse(option_value_str, '"{0}":["'.format(ea_asin), '"]')
            ea_option_value_str = str(ea_option_value_str).replace('"', '').replace('\\', ' ')
            en_option_value = replace_option_value(ea_option_value_str)
            en_option_value = replace_currency_opt(en_option_value)

            if str(en_option_value).strip() == "":
                print('>> en_option_value check .')
                #return "D07"

            option_value_dic[ea_asin] = en_option_value
            option_value_org_dic[ea_asin] = en_option_value
            option_value_tran_dic[en_option_value] = en_option_value
            if in_countryKbn == "JP" or  in_countryKbn == "FR":
                option_value_tran_dic['code'] = str(ea_asin).strip()
                option_value_tran_dic['name'] = en_option_value.replace(" ","&nbsp;")
                option_value_tran_arr.append(option_value_tran_dic)

            # option 1 : ase_price
            if option_cnt == 1:
                print('>> option 1 base_price :')
                ea_opt_price = base_price
                option_price_dic[ea_asin] = float(ea_opt_price)
            # option 1 over
            else:
                ea_opt_price = 0
                ea_price_asin = ""
                ea_opt_price_str = ""
                ea_opt_price_tmp = ""
                in_soup_twister = ""
                now_source = str(in_drive.page_source)
                if str(now_source).find('id="twister_feature_div"') > -1 or str(now_source).find('id="softlinesTwister_feature_div"') > -1 or str(now_source).find('id="twister-plus-inline-twister-card"') > -1:
                    if str(in_drive.page_source).find('id="twister_feature_div"') > -1:
                        in_soup_twister = getparse(str(now_source), 'id="twister_feature_div"', '')
                    elif str(in_drive.page_source).find('id="softlinesTwister_feature_div"') > -1:
                        in_soup_twister = getparse(str(now_source), 'id="softlinesTwister_feature_div"', '')
                    else:
                        in_soup_twister = getparse(str(now_source), 'id="twister-plus-inline-twister-card"', '')

                    if str(in_soup_twister).find('<li data-asin="') > -1:
                        ea_price_asin = '<li data-asin="'+str(ea_asin)+'"'
                    elif str(in_soup_twister).find('data-defaultasin=') > -1:
                        if str(in_soup_twister).find('<form id="twister"') > -1:
                            in_soup_twister = getparse(str(in_soup_twister), '<form id="twister"', '</form>')
                        ea_price_asin = 'data-defaultasin="'+str(ea_asin)+'"'
                    else:
                        ea_price_asin = str(ea_asin)

                    ea_opt_price_tmp = getparse(str(in_soup_twister), ea_price_asin,'</span></li>')
                    if str(ea_opt_price_tmp).find('twisterSwatchPrice') > -1:
                        ea_opt_price_str = getparse(str(ea_opt_price_tmp),'twisterSwatchPrice','</span>')
                    elif str(ea_opt_price_tmp).find('class="olpWrapper') > -1:
                        ea_opt_price_str = getparse(str(ea_opt_price_tmp),'class="olpWrapper','</span>')
                        if str(ea_opt_price_str).find("from") > -1: 
                            ea_opt_price_str = getparse(str(ea_opt_price_str),'from ','')
                    elif str(ea_opt_price_tmp).find('option from ') > -1:
                        ea_opt_price_str = getparse(str(ea_opt_price_tmp),'option from ','</span>')
                    if str(ea_opt_price_str).find('">') > -1:
                        ea_opt_price_str = getparse(str(ea_opt_price_str),'">','')

                    ea_opt_price_str = str(ea_opt_price_str).replace('</p>', '')
                    if currSymbol == '€' or in_pgsite == "fr" and ea_opt_price_str != "":
                        #print(">> 영국 아마존 : 옵션가격 ({})".format(ea_opt_price_str))
                        if ea_opt_price_str.find(",") > -1:
                            print('>> option_value check (over option price) : {}'.format(ea_opt_price_str))
                            ea_opt_price_str = ea_opt_price_str.replace(',','')
                        ea_opt_price_str = ea_opt_price_str.replace(' ','').replace('&nbsp;', '').replace('\u202f', '').replace('u202f', '')
                        #print(">> 영국 아마존 : 옵션가격 edit ({})".format(ea_opt_price_str))
                    ea_opt_price_str = str(ea_opt_price_str).replace('USD', '').replace('¥', '').replace(currSymbol, '').replace('&nbsp;', '').strip()
                    # print(">> ea_price_asin : " + str(ea_price_asin))  
                    # print(">> ea_opt_price_str : " + str(ea_opt_price_str))  

                    if in_pgsite != "fr":
                        if str(ea_opt_price_str) == "":
                            ea_opt_price_str = getparse(str(ea_opt_price_tmp), 'olpWrapper">', '</span>')
                            ea_opt_price_str = getparse(str(ea_opt_price_str), 'from', '')
                            #print("ea_opt_price_str (olpWrapper) : " + str(ea_opt_price_str))

                        if str(ea_opt_price_str) == "":
                            ea_opt_price_str = getparse(str(ea_opt_price_tmp), 'class="a-size-mini olpMessageWrapper">', '</span>')
                            ea_opt_price_str = getparse(str(ea_opt_price_str), currSymbol, '')
                            if str(ea_opt_price_str).find('USD') > -1:
                                ea_opt_price_str = getparse(str(ea_opt_price_str), "USD", '')
                            #print("ea_opt_price_str (olpMessageWrapper) : " + str(ea_opt_price_str))

                    ea_opt_price_str = str(ea_opt_price_str).replace('</p>', '').replace('Â\xa0', '')
                    if ea_opt_price_str.find('<') > -1:
                        ea_opt_price_str = getparse(str(ea_opt_price_str), '', '<')

                    if ea_opt_price_str.find('(') > -1:
                        print(">> ea_opt_price_str (before) : {}".format(ea_opt_price_str))
                        ea_opt_price_str = getparse(str(ea_opt_price_str), '', '(')
                        print(">> ea_opt_price_str (after) : {}".format(ea_opt_price_str))

                    ea_opt_price_str = str(ea_opt_price_str).replace(' ', '').strip()
                    ea_opt_price_str = str(ea_opt_price_str).replace('\\', '').replace('/', '').strip()
                    ea_opt_price = ea_opt_price_str.replace("'", "").replace(',', '').replace(currSymbol, '').strip()
                    ea_opt_price = replace_currency(ea_opt_price)
                    #print(">> (ea_opt_price) : "+str(ea_opt_price))

                    if str(ea_opt_price).strip() != "":
                        tmp_ea_opt_price = str(ea_opt_price).replace('.','').strip()
                        tmp_ea_opt_price = regRemoveText(tmp_ea_opt_price)
                        #print(">> (tmp_ea_opt_price) : " + str(tmp_ea_opt_price))
                        if tmp_ea_opt_price.isdigit() == True:
                            if ea_opt_price.find('(') > -1:
                                ea_opt_price = getparse(str(ea_opt_price), '', '(')
                            option_price_dic[ea_asin] = ea_opt_price
                            ea_price_last_asin = ea_asin
                            #print(">> (ea_opt_price) : " + str(ea_opt_price))

                            if optFirstChkFlg == "0": #첫번째 옵션값이 있을경우 그 옵션값을 base_price로 설정
                                optFirstChkFlg = "1"
                                base_price = float(ea_opt_price)
                                base_tmp_price = float(ea_opt_price)

                            if in_countryKbn == "JP":# 플러스 옵션
                                if float(ea_opt_price) > 1 and float(ea_opt_price) < float(base_price):
                                    base_price = float(ea_opt_price)
                            else:
                                if float(ea_opt_price) > 0.1 and float(ea_opt_price) < float(base_price):
                                    base_price = float(ea_opt_price)

                            if d_minus_opt == "1": # 마이너스 옵션
                                if in_countryKbn == "JP":
                                    if float(ea_opt_price) > 1 and float(ea_opt_price) > float(base_tmp_price):
                                        base_tmp_price = float(ea_opt_price)
                                else:
                                    if float(ea_opt_price) > 0.1 and float(ea_opt_price) > float(base_tmp_price):
                                        base_tmp_price = float(ea_opt_price)

                            if opmaxlen == 1 and float(ea_opt_price) > float(base_price):
                                base_price = float(ea_opt_price)  
                                base_tmp_price = float(ea_opt_price)

                        else:
                            #procLogSet(db_con, in_pg, "[" + str(ea_asin) + "] (1)ea_opt_price.isdigit : " + str(ea_opt_price))
                            print('>> option_value check .')
                            #return "D07"

                else:
                    flg_opt_chk = "1"

            # option info  option_value
            print('>> [옵션] (' + str(oplow) + ') ' + str(ea_asin) + ' | ' + str(en_option_value)  + ' | ' + str(ea_opt_price))
            oplow += 1

        if in_countryKbn == "JP" or in_countryKbn == "FR":
            option_value_tran_arr = str(option_value_tran_arr).replace('\\u3000',' ').replace("'",'"')
            #print('>> option_value_tran_arr :  ' + str(option_value_tran_arr))      

        opt_val_cnt = 0
        opt_price_cnt = 0
        if opmaxlen > 0:
            opt_val_cnt = len(option_value_dic)
            opt_price_cnt = len(option_price_dic)
            print('>> opt_val_cnt : {} | opt_price_cnt : {}'.format(opt_val_cnt,opt_price_cnt))
            if opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt == opt_price_cnt:
                flg_opt_chk = "0"
            elif opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt > opt_price_cnt and option_kind_count == 1:
                flg_opt_chk = "0"
            else:
                flg_opt_chk = "1"
        print(">> Option get type (flg_opt_chk) : "+str(flg_opt_chk))
        print('>> base_price (after) :  ' + str(base_price))

        # 옵션 가격 가져오기 (1)
        if flg_opt_chk == "1":
            print(">> 옵션 가격 가져오기 (1) Start")
            chkOptPrice = 0
            optFirstChkFlg = "0"
            #----------------------------------------------------------------------------------------
            # print(">> subasin_set : {}".format(subasin_set))
            ### https://www.amazon.co.jp/gp/twister/dimension?isDimensionSlotsAjax=1&asinList=B09T2P7DTK,B09T2FTRVJ,B09XTTRYB7,B09T2HWJLR,B09XTPMW7Y,B09XTNYDFT=1&productTypeDefinition=DISHWARE_BOWL&productGroupId=home_display_on_website&parentAsin=B0BPBF5BNG&isPrime=0&isOneClickEnabled=0&deviceType=web&showFancyPrice=false&twisterFlavor=twisterPlusDesktopConfigurator
            cookies = {'lc-acbjp': 'en_US'}
            if in_countryKbn == "US":
                cookies = {'lc-main': 'en_US'}
            elif in_countryKbn == "JP":
                cookies = {'lc-acbjp': 'en_US'}
            elif in_countryKbn == "DE":
                cookies = {'lc-acbde': 'en_GB', 'i18n-prefs': 'USD'}
            elif in_countryKbn == "UK":
                #cookies = {'lc-acbuk': 'en_GB', 'i18n-prefs': 'USD'}
                cookies = {'lc-acbuk': 'en_GB'}
            elif in_countryKbn == "FR":
                cookies = {'lc-acbfr': 'en_GB'}
            siteName = getCountryInfo(in_countryKbn,"3")
            contry_cur = getCountryInfo(in_countryKbn,"2")
            itemaisnTmp = str(itemaisnTmp).replace(" ","").strip()
            flg_opt_chk = "2"
            #----------------------------------------------------------------------------------------

            # 옵션 가격 가져오기 (2)
            if flg_opt_chk == "2":
                print(">> 옵션 가격 가져오기 (2) Start")
                cntj = 0
                optFirstChkFlg = "0"
                cntOptPrice = 0

                test_source = str(in_drive.page_source)
                ## https://www.amazon.com/gp/twister/ajaxv2?acAsin=B09DPLBDY3&sid=136-3253781-4692159&ptd=DECORATIVE_SIGNAGE&sCac=1&twisterView=glance&pgid=office_product_display_on_website&rid=STY37YWP6S15ZPKG4J10&auiAjax=1&json=1&dpxAjaxFlag=1&isUDPFlag=1&ee=2&parentAsin=B083SHH21W&enPre=1&dcm=1&storeID=office-products&ppw=&ppl=&isFlushing=2&dpEnvironment=hardlines&asinList=B09DPLBDY3&id=B09DPLBDY3&mType=full&psc=1
                ajaxUrl = getparse(str(in_drive.page_source),'"immutableURLPrefix":"',',')
                dpEnvironment = getparse(str(now_source),'"dpEnvironment" : "','"')
                ajaxUrl = getparse(ajaxUrl,'','"')

                optSkipCnt = 0
                for item_optcode in subasin_set:
                    priceToSet = ""
                    cntj = cntj + 1

                    ajaxUrl = ""
                    ajaxUrl = getparse(str(in_drive.page_source),'"immutableURLPrefix":"',',')
                    dpEnvironment = getparse(str(now_source),'"dpEnvironment" : "','"')
                    ajaxUrl = getparse(ajaxUrl,'','"')

                    onurl = 'https://' + str(siteName)  + ajaxUrl
                    onurl = onurl.replace("?sid=","?acAsin=" +str(item_optcode)+ "&sid=") + "&ppw=&ppl=&isFlushing=2&dpEnvironment="+str(dpEnvironment)+"&asinList="+str(item_optcode)+"&id="+str(item_optcode)+"&mType=full&psc=1"
                    # print(">> onurl : {}".format(onurl))
                    opt_html_str = ""

                    try:
                        opt_source_code = requests.get(onurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + ' Safari/537.36', 'Referer': 'https://' + str(siteName)}, cookies=cookies)
                    except Exception as e:
                        print(">> requests Exception item_optcode : {}".format(item_optcode))
                        time.sleep(random.uniform(1,1.5))
                        optSkipCnt = optSkipCnt + 1
                        continue
                    else:
                        time.sleep(random.uniform(0.7,1.2))
                        if opt_source_code.status_code == 200:
                            opt_html_str = opt_source_code.text

                            if str(opt_html_str).find(item_optcode) == -1:
                                print(">> Not Found : {} ".format(item_optcode))
                                time.sleep(0.5)
                                optSkipCnt = optSkipCnt + 1
                                continue

                            if str(opt_html_str).find(item_optcode) > -1:
                                priceToSet = getparse(opt_html_str,'"priceToSet":"','"')
                                # print(">> (" + str(cntj) + ") priceToSet (" +str(item_optcode)+ ") : " + str(priceToSet) +"  [ " + str(option_value_dic[item_optcode]) + " ] ")
                                if priceToSet.find('Currently unavailable') > -1:
                                    print(">> [{}] Currently unavailable ".format(item_optcode))

                            if priceToSet == "" and str(opt_html_str).find('twister-plus-price-data-price') > -1:
                                priceToSet = getparse(opt_html_str,'twister-plus-price-data-price','>')
                                priceToSet = getparse(priceToSet,'value=','')
                                print(">> [{}] priceToSet(org) : {} ".format(item_optcode, priceToSet))

                            priceToSet = priceToSet.replace('\\', '').replace('/', '').replace('"', '').strip()
                            priceToSet = priceToSet.replace('\xa0','').replace('xa0','').replace('\\u20ac','').replace('u20ac','').strip()
                            if in_pgsite == "fr":
                                priceToSet = priceToSet.replace("'", "").replace(',', '.').replace(currSymbol, '').strip()
                            else:
                                priceToSet = priceToSet.replace("'", "").replace(',', '').replace(currSymbol, '').strip()
                            ea_opt_price = replace_currency(priceToSet)
                            print(">> [{}] priceToSet (edit) : {} | {}".format(item_optcode, priceToSet, ea_opt_price))
                            if str(priceToSet).strip() == "" and str(opt_html_str).find('sp_detail2') > -1:
                                # print(">> [{}] sp_detail2 : ".format(item_optcode))
                                priceToSet = getparse(opt_html_str,'','sp_detail2')
                                # priceToSet = getparse(priceToSet,'a-offscreen','<')
                                # priceToSet = getparse(priceToSet,'>','').replace('\\', '').replace('"', '').strip()

                            if str(priceToSet).strip() == "" and str(opt_html_str).find('olpLinkWidget_feature_div') > -1:
                                #print(">> [{}] sp_detail2 : ".format(item_optcode))
                                priceToSet = getparse(opt_html_str,'olpLinkWidget_feature_div','script>')

                            if str(ea_opt_price).strip() != "":
                                ea_opt_price = str(ea_opt_price).replace('</p>', '')
                                ea_opt_price = replace_currency(ea_opt_price)
                                ea_opt_price = ea_opt_price.replace(',', '').replace(' ', '')
                                ea_opt_price = str(ea_opt_price).strip()
                                ea_opt_price = regRemoveText(ea_opt_price)
                                # print(">>[{}] ea_opt_price : {} ".format(item_optcode,ea_opt_price))

                                tmp_ea_opt_price = str(ea_opt_price).replace('.', '').strip()
                                if tmp_ea_opt_price.isdigit() == True:
                                    
                                    if in_countryKbn == "JP": # 플러스 옵션
                                        if float(ea_opt_price) > 50000:
                                            print(">> ea_opt_price [JP] 50000 Over : {}".format(ea_opt_price))
                                            return "D09" + " ( " + str(ea_opt_price) + " ) "  
                                    elif in_countryKbn == "US" or in_countryKbn == "DE":
                                        if float(ea_opt_price) > 700:
                                            print(">> ea_opt_price [US] 700 Over : {}".format(ea_opt_price))
                                            return "D09" + " ( " + str(ea_opt_price) + " ) "  
                                    elif in_countryKbn == "UK" or in_countryKbn == "FR":
                                        if float(ea_opt_price) > 400:
                                            print(">> ea_opt_price [UK] 400 Over : {}".format(ea_opt_price))
                                            return "D09" + " ( " + str(ea_opt_price) + " ) "  

                                    option_price_dic[item_optcode] = float(ea_opt_price)
                                    cntOptPrice = cntOptPrice + 1
                                    ea_price_last_asin = item_optcode
                                    #print("ea_opt_price : " + str(ea_opt_price))

                                    if optFirstChkFlg == "0": #첫번째 옵션값이 있을경우 그 옵션값을 base_price로 설정
                                        optFirstChkFlg = "1"
                                        base_price = float(ea_opt_price)
                                        base_tmp_price = float(ea_opt_price)

                                    if in_countryKbn == "JP": # 플러스 옵션
                                        if float(ea_opt_price) > 1 and float(ea_opt_price) < float(base_price):
                                            base_price = float(ea_opt_price)
                                    else:
                                        if float(ea_opt_price) > 0.1 and float(ea_opt_price) < float(base_price):
                                            base_price = float(ea_opt_price)   

                                    if d_minus_opt == "1": # 마이너스 옵션으로 set
                                        if in_countryKbn == "JP":
                                            if float(ea_opt_price) > 1 and float(ea_opt_price) > float(base_tmp_price):
                                                base_tmp_price = float(ea_opt_price)
                                        else:
                                            if float(ea_opt_price) > 0.1 and float(ea_opt_price) > float(base_tmp_price):
                                                base_tmp_price = float(ea_opt_price)

                                    if opmaxlen == 1 and float(ea_opt_price) > float(base_price):
                                        base_price = float(ea_opt_price)
                                        base_tmp_price = float(ea_opt_price)

                                else:
                                    print(">>[{}] option_value check : {} ".format(item_optcode,ea_opt_price))
                                    ## procLogSet(db_con, in_pg, "[" + str(ea_asin) + "] (1-2)ea_opt_price.isdigit : " + str(ea_opt_price))
                                    #return "D07"
                                print(">> (" + str(cntj) + ") 옵션가격 (" +str(item_optcode)+ ") : " + str(ea_opt_price) +"  [ " + str(option_value_dic[item_optcode]) + " ] ")

                            else:
                                optSkipCnt = optSkipCnt + 1
                                if str(opt_html_str).find('Currently unavailable.') > -1:
                                    print(">> (" + str(cntj) + ") 옵션가격 (" +str(item_optcode)+ ") : (없음) Currently unavailable [ " + str(option_value_dic[item_optcode]) + " ] ")
                                else:
                                    print(">> (" + str(cntj) + ") 옵션가격 (" +str(item_optcode)+ ") : (없음) [ " + str(option_value_dic[item_optcode]) + " ] ")
                                    time.sleep(0.5)
                        else:
                            chkOptPrice = chkOptPrice + 1

                        if cntj > 8:
                            if cntOptPrice == 0:
                                print(">> 옵션 금액 없음 half check (D07) ")
                                return "D07"

                if len(subasin_set) == chkOptPrice:
                    print('>> Option Price check please (3) ')
                    #if in_pgsite != "uk" :
                        #set_new_tor_ip()
                        #checkCurrIP_new()
                    time.sleep(1)
                    return "C03"

                #if cntOptPrice == 0:
                    #path_file = os.getcwd()
                    # with open(path_file + "/result_price_option3.html","w",encoding="utf8") as f: 
                    #     f.write(str(opt_html_str))
                    # if in_pgsite != "uk" and  in_pgsite != "de":
                    #     set_new_tor_ip()
                    #     checkCurrIP_new()
                    #time.sleep(1)

        opt_val_cnt = 0
        opt_price_cnt = 0
        if opmaxlen > 0:
            opt_val_cnt = len(option_value_dic)
            opt_price_cnt = len(option_price_dic)
            print('>> opt_val_cnt : {} | opt_price_cnt : {}'.format(opt_val_cnt,opt_price_cnt))
            if opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt == opt_price_cnt:
                print('>> option OK')
            elif opt_val_cnt > 0 and opt_price_cnt > 0 and opt_val_cnt > opt_price_cnt:
                print('>> option_cnt  option_cnt  unmatch (Progress)')
            else:
                #procLogSet(db_con, in_pg, " {} : option (D07) : opt_val : {}  | opt_price : {} ").format(in_asin,opt_val_cnt,opt_price_cnt)
                print('>> option_value check (2) - opt_val_cnt : {} | opt_price_cnt : {}'.format(opt_val_cnt,opt_price_cnt))
                return "D07"

        print('>> base_price :' +str(base_price))
        print('>> base_tmp_price :' +str(base_tmp_price))

        # min / max 가격 체크 
        rtnPriceFlg = priceCheck(in_countryKbn, base_price)
        if rtnPriceFlg != "":
            print('>> price check. (99) :' +str(rtnPriceFlg))
            return rtnPriceFlg

        if d_minus_opt == "1": # 마이너스 옵션으로 set
            #base_price = (base_tmp_price + ((base_tmp_price - base_price) * (d_coupon/100))) * (100/(100-d_coupon))
            #base_price = base_tmp_price + ((base_tmp_price - base_price) * (d_coupon/100)) * (100/(100-d_coupon))
            print('>> 마이너스 옵션 set :' +str(base_tmp_price))
            goods['price'] = float(base_tmp_price)
            goods['price_tmp'] = float(base_tmp_price)
        else:
            goods['price'] = float(base_price)
            goods['price_tmp'] = float(base_price)

        if in_countryKbn == "JP":
            if float(base_price) < 99 or str(base_price) == "" or str(base_price) == "0" or str(base_price) == "0.0":
                print('>> price check. (99) :' +str(base_price))
                return "D12" + " ( " + str(base_price) + " ) "

        elif in_countryKbn == "US" or in_countryKbn == "DE" or in_countryKbn == "UK" or in_countryKbn == "FR":
            if float(base_price) < 1 or str(base_price) == "" or str(base_price) == "0" or str(base_price) == "0.0":
                print('>> price check. (1달러 미만) :' +str(base_price))
                return "D12" + " ( " + str(base_price) + " ) "

        goods['base_price'] = float(base_price)
        goods['base_tmp_price'] = float(base_tmp_price)
        goods['subasin'] = subasin_set
        goods['option_value'] = option_value_dic
        goods['option_price'] = option_price_dic
        goods['option_value_dic_org'] = option_value_org_dic

        ############################################################################################################
        ## 여러옵션중 1개만 재고있을경우 (해당 이미지로 변경)
        ############################################################################################################
        if option_flg == "1" and opt_val_cnt > 1 and opt_price_cnt == 1:
            print('>> 여러옵션중 1개만 재고있을경우 (해당 이미지로 변경) : ' + str(opt_price_cnt))
            #procLogSet(db_con, in_pg, "[" + str(ea_price_last_asin) + "] 여러옵션중 1개만 재고있을경우 (해당 이미지로 변경) : " + str(opt_price_cnt))
            amazon_siteUrl = str(getCountryInfo(in_countryKbn,"3"))
            if ea_price_last_asin != "":
                # asin 코드로 새로 상품 당겨와 이미지 업데이트 처리
                now2_url = ""
                if in_countryKbn == "DE":
                    now2_url = "https://" +amazon_siteUrl+ "/-/en/dp/" + str(ea_price_last_asin) + "?currency=EUR&language=en_GB"
                elif in_countryKbn == "UK":
                    now2_url = "https://" +amazon_siteUrl+ "/-/en/dp/" + str(ea_price_last_asin) + "?language=en_GB"
                elif in_countryKbn == "FR":
                    now2_url = "https://" +amazon_siteUrl+ "/-/en/dp/" + str(ea_price_last_asin) + "?language=en_GB"
                elif in_countryKbn == "JP":
                    now2_url = "https://" +amazon_siteUrl+ "/-/en/dp/" + str(ea_price_last_asin) + "?language=en_US"
                else:
                    now2_url = "https://" +amazon_siteUrl+ "/-/en/dp/" + str(ea_price_last_asin)
                #now2_url = "https://" + getCountryInfo(in_countryKbn,"3") + "/-/en/dp/" + str(ea_price_last_asin) + "?currency=EUR&language=en_GB"
                print('>> 여러옵션중 1개만 재고있을경우 url : ' + str(now2_url))

                try:
                    in_drive.get(now2_url)
                except Exception as e:
                    print('>> 여러옵션중 1개만 재고있을경우 접속 Exception Error ')
                    return "C01"
                else:
                    #print('>> time.sleep(5) ')
                    time.sleep(3)

                result_2 = in_drive.page_source
                #print('>> time.sleep(1) ')
                time.sleep(1)

                if str(result_2).find('id="productTitle"') == -1:
                    print('>> 여러옵션중 1개만 재고있을경우 (접속 불가 SKIP) ')
                    print('>> option_value Connect Error .')
                    # nput("Ket Option Check (2) : ")
                    #procLogSet(db_con, in_pg, " 여러옵션중 1개만 재고있을경우 (접속 불가 SKIP) ")
                    return "C02"
                else:
                    print('>> 여러옵션중 1개만 재고있을경우 (접속 OK) ')
                    ########### image (해당 옵션 이미지 변경) ###########
                    flg_noimg = "0"
                    
                    mainImg = ""
                    naverImg = ""
                    imglist = getparse(str(in_soup),"'colorImages':", "</script>")
                    if imglist.find('"large":"') == -1:
                        print('>> no Img ')
                        return "D19"  # No img

                    spImgList = imglist.split('},{')
                    imgList = []
                    imgCnt = 0
                    flg_noimg = "0"
                    for ea_img in spImgList:
                        if str(ea_img).find('"hiRes":"') > -1:
                            imgUrl = getparse(ea_img,'"hiRes":"','"')
                            if imgUrl.find('/images/W/MEDIAX_') > -1:
                                pass
                            elif imgUrl.find('/images/W/') > -1:
                                repImgStr = getparse(imgUrl,'/images/W/','/images/I/')
                                imgUrl = imgUrl.replace('/images/W/'+ str(repImgStr),'')
                                print(">>(after) (/images/W/) -> imgUrl : {}".format(imgUrl))
                            if naverImg == "" and imgUrl != "": 
                                if str(imgUrl).find('.jpg') > -1 or str(imgUrl).find('.JPG') > -1:
                                    imgUrl = getparse(imgUrl, '', '._') + '.jpg'
                                naverImg = imgUrl
                        else:
                            imgUrl = getparse(ea_img,'"large":"','"')
                            if imgUrl.find('/images/W/') > -1:
                                repImgStr = getparse(imgUrl,'/images/W/','/images/I/')
                                imgUrl = imgUrl.replace('/images/W/'+ str(repImgStr),'')
                                print(">>(after) (/images/W/) -> imgUrl : {}".format(imgUrl))

                        if str(imgUrl).find('21EvqGR5jyL.') > -1:
                            print('>> Noimg : '+str(imgUrl))
                            flg_noimg = "1"
                            break
                        if str(imgUrl).find('01MKUOLsA5L.') > -1:
                            print('>> Noimg : '+str(imgUrl))
                            flg_noimg = "1"
                            break
                        if str(imgUrl).find('21i3Jn-5C5L.') > -1:
                            print('>> Noimg : '+str(imgUrl))
                            flg_noimg = "1"
                            break

                        if imgUrl.lower().find('.jpg') > -1 or imgUrl.lower().find('.jpeg') > -1 or imgUrl.lower().find('.png') > -1:
                            if mainImg == "":
                                mainImg = imgUrl
                            else:
                                imgCnt = imgCnt + 1
                                imgList.append(imgUrl)
                                if imgCnt >= 5:
                                    break
                    print(">> imgList : {}".format(imgList))
                    print(">> mainImg : {}".format(mainImg))
                    if str(mainImg).strip() == "":
                        print('>> no Img ')
                        return "D19"  # No img     
                    if flg_noimg == "1":
                        print('>> no Img ')
                        return "D19" # No img

                    if str(naverImg) != "":
                        goods['naver_img'] = naverImg
                    else:
                        goods['naver_img'] = None
                    goods['mainimage'] = mainImg
                    goods['image'] = imgList


        ########## option image ###########
        otimgCnt2 = 0
        in_soup_img2 = getparse(str(in_soup), '"colorImages":{', '}}]},')
        sp_option_img2 = in_soup_img2.split(']}}],')
        otimgCnt2 = len(sp_option_img2)
        print('>> 옵션 이미지 (len) : ' + str(otimgCnt2))

        otimglow2 = 1
        img_otp_cnt = 1000
        if otimgCnt2 == 0:
            print('>> 옵션 이미지 없음 otimgCnt2 (len) : ' + str(otimgCnt2))
        else:
            for item_option_img2 in sp_option_img2:
                option_image_tran_dic = {}
                en_ea_option_img_str = ""
                ea_option_img_name = ""
                ea_option_img_url = ""
                if otimglow2 > 40:
                    break

                ea_option_img_name = getparse(str(item_option_img2), '"', '":[{')
                ea_option_img_name = str(ea_option_img_name).replace('<br>',' ').replace('\\',' ').replace('  ',' ')
                ea_option_img_url = getparse(str(item_option_img2), '[{"large":"', '",')
                if ea_option_img_url.find('/images/W/MEDIAX_') > -1:
                    pass
                elif ea_option_img_url.find('/images/W/') > -1:
                    repImgStr = getparse(ea_option_img_url,'/images/W/','/images/I/')
                    ea_option_img_url = ea_option_img_url.replace('/images/W/'+ str(repImgStr),'')
                    print(">>(after) (/images/W/) -> ea_option_img_url : {}".format(ea_option_img_url))

                ea_option_img_ori = ea_option_img_name
                if str(ea_option_img_name).strip() == "" or str(ea_option_img_name).strip() == " " or str(ea_option_img_url).strip() == "":
                    print('>> ea_option_img_url (No Data) : ' + str(ea_option_img_url))
                else:
                    if in_countryKbn == "JP" or in_countryKbn == "FR":
                        if regJpStrChk(ea_option_img_name) == "1":
                            en_ea_option_img_str = ea_option_img_name
                        else:
                            en_ea_option_img_str = ea_option_img_name
                    else:
                        en_ea_option_img_str = ea_option_img_name

                    en_ea_option_img_str = replace_option_value(en_ea_option_img_str)
                    en_ea_option_img_str = replace_currency_opt(en_ea_option_img_str)
                    en_ea_option_img_str =  "'" + str(en_ea_option_img_str) +"'"
                    
                    #print('>> [옵션] img : ' + str(ea_option_img_name))
                    if str(ea_option_img_url).find('.gif') > -1:
                        print('>> ea_option_img_url (.gif) : ' + str(ea_option_img_url))
                    else:
                        option_img_dic[ea_option_img_url] = en_ea_option_img_str
                        if in_countryKbn == "JP" or in_countryKbn == "FR":
                            option_image_tran_dic['code'] = ea_option_img_url
                            option_image_tran_dic['name'] = en_ea_option_img_str.replace(" ","&nbsp;")
                            option_image_tran_arr.append(option_image_tran_dic)

                otimglow2 += 1

        goods['option_image'] = option_img_dic
        goods['option_img_dic_org'] = option_img_dic
        #print('\n >> option_image :  ' + str(option_img_dic))

        if in_countryKbn == "JP" or in_countryKbn == "FR":
            option_image_tran_arr = str(option_image_tran_arr).replace('\\u3000',' ').replace("'",'"')
            #print('>> option_image_tran_arr :  ' + str(option_image_tran_arr))    

    if in_countryKbn == "JP" or in_countryKbn == "FR":
        tran_title = ""
        opt_tran_cnt = 0
        goods_title = str(goods_title).replace("'","")
        if option_flg == "0":
            option_item_string = "''"
            option_image_string = "''"
        else:
            option_item_string = 'N'+getQueryValue(option_value_tran_arr)
            option_image_string = 'N'+getQueryValue(option_image_tran_arr)
            option_image_string = option_image_string.replace('""','"')
            if option_flg == "1":
                if regJpStrChk(option_item_string) == "1" or in_countryKbn == "FR": 
                    sql_d = "delete from T_Category_BestAsin_tran where asin = '{}'".format(in_asin)
                    #print(">> insert sql_i : {}".format(sql_d))
                    print(">> (tran) del asin : {}".format(in_asin))
                    db_con.execute(sql_d)

                    sql_i = "insert into T_Category_BestAsin_tran (asin, up_date, title, option_item, option_image) values ('{}',getdate(),{},{},{})".format(in_asin,'N'+getQueryValue(get_replace_title(goods_title)), option_item_string, option_image_string)
                    #print(">> insert sql_i : {}".format(sql_i))
                    print(">> (tran) insert asin : {}".format(in_asin))
                    db_con.execute(sql_i)

                    time.sleep(2)
                    # 일본어 포함 되었을 경우 번역처리 / 프랑스어 번역처리
                    opt_tran_cnt = 0
                    # tran 옵션  
                    
                    result_tran_option = procTranConect(in_drive, in_asin, in_pgsite, opmaxlen, "option")
                    if result_tran_option == "":
                        print('>> procTranConect except ')
                        return "C08"
                    time.sleep(2)
                    tran_option = getTranOption(result_tran_option, in_asin)
                    if str(tran_option) != "":
                        sp_tran_option = str(tran_option).split('<input type="hidden"')
                        for ea_tran_item in sp_tran_option:
                            ea_tran_code = ""
                            ea_tran_name = ""
                            ea_tran_code = getparse(ea_tran_item,'value="','">')
                            ea_tran_name = getparse(ea_tran_item,'">','').replace("/", "|").replace("&nbsp;", " ").replace("`", "").replace('\n', '').replace('<hr>', '').replace('"', '').strip()
                            if str(ea_tran_code).strip() != "" and str(ea_tran_name).strip() != "":
                                #print(">> {} : {}".format(ea_tran_code, option_value_dic[ea_tran_code]))
                                if regJpStrChk(ea_tran_name) == "0" or in_countryKbn == "FR":
                                    ea_tran_name = str(ea_tran_name)
                                    option_value_dic[ea_tran_code] = ea_tran_name
                                    opt_tran_cnt = opt_tran_cnt + 1
                                    #print(">> {} : {} ".format(ea_tran_code,option_value_dic[ea_tran_code]))

                    if opt_tran_cnt == 0:
                        # No Option
                        print(">> opt_tran_cnt  0 : {}".format(in_asin))
                        print('>> Option_value tran delay ')
                        return "C08"

                    if regJpStrChk(option_image_string) == "1" or in_countryKbn == "FR": 
                        time.sleep(2)
                        tran_option_img = getTranOption_image(result_tran_option, in_asin)
                        if str(tran_option_img) != "":
                            sp_tran_option_img = str(tran_option_img).split('<input type="hidden"')
                            for ea_tran_img in sp_tran_option_img:
                                ea_img_tran_code = ""
                                ea_img_tran_name = ""
                                ea_img_tran_code = getparse(ea_tran_img,'value="','">')
                                ea_img_tran_name = getparse(ea_tran_img,'">','').replace("/", "|").replace("&nbsp;", " ").replace("`", "").replace('\n', '').replace('<hr>', '').replace('"', '').strip()
                                if str(ea_img_tran_code).strip() != "" and str(ea_img_tran_name).strip() != "":
                                    #print(">> {} : {}".format(ea_img_tran_code, option_img_dic[ea_img_tran_code]))
                                    if regJpStrChk(ea_img_tran_name) == "0" or in_countryKbn == "FR":
                                        ea_img_tran_name = str(ea_img_tran_name)
                                        option_img_dic[ea_img_tran_code] = ea_img_tran_name
                                        #print(">> {} : {} ".format(ea_img_tran_code,option_img_dic[ea_img_tran_code]))

            else:
                print(">> (final) (No tran) option_value_dic : {} ".format(option_value_dic))

            goods['option_value'] = option_value_dic
            goods['option_image'] = option_img_dic

    #DB set
    rtnDBflg = setDB_proc(in_asin, parentasin, goods, db_con, db_price, in_pg, in_countryKbn, in_guid, in_pgsite, manage_dic)
    sel_goodscode = ""
    if rtnDBflg[:2] != "0@":
        if rtnDBflg == "D01":
            print(">> ## t_goods Option /0 없음 에러 (품절처리 필요)  ##")
            return "D01"
        elif rtnDBflg == "D77":
            print(">>  Option : Internal Server Error (옵션 확인 필요)  ##")
            return "D77"
        else:
            print('>> setDB error --> DB check Rollback ')
            sql = "select top 1 uid,IsDisplay,OptionKind from t_goods where ali_no = '{0}'".format(parentasin)
            print(">> sql : {}".format(sql))
            row = db_con.selectone(sql)
            if not row:
                print(">> ## t_goods Insert No goods (OK) ##")
                # insert
            else:
                DUid = row[0]
                DIsDisplay = row[1]
                DOptionKind = row[2]
                if rtnDBflg == "Q01" or rtnDBflg == "Q02":
                    # 상품 삭제처리 
                    setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
                    print('>> >> DB Insert Error : t_goods (상품 삭제 처리) : {}'.format(DUid))

                elif rtnDBflg == "Q03" or rtnDBflg == "Q04":
                    print('>> DB Update Error (상품 품절 처리) : {}'.format(DUid))
                    sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate() where uid='{0}'".format(DUid)
                    db_con.execute(sql)

            return str(rtnDBflg) # exit
    else:
        sel_goodscode = getparse(rtnDBflg,"0@","")
        sql_i = "insert into goods_title_tran (goodscode, asin_no, Title) values ('{}', '{}',dbo.GetCutStr('{}',240,'...'))".format(sel_goodscode, in_asin, goods_title)
        in_org_title = str(in_org_title).replace(",","").upper()
        #print(">> 타이틀 (DB It-title)) : {}".format(in_org_title))
        if in_org_title == goods_title: # 기존 org title 과 파싱 title 비교
            print(">> 타이틀 변화없음 : {}".format(in_asin))
            if regStrChk(in_old_title,"KR") == "0": # 기존 DB title 한글번역 없을경우 번역 대상
                print(">> 한글 없음 번역 Insert : {} ".format(in_asin))
                db_con.execute(sql_i)
                time.sleep(1)
                sql_u = "update t_goods set confirm_goods = '1' where goodscode = '{}'".format(sel_goodscode)
                print(">> 일본어 포함 confirm_goods = 1 : {} ".format(sel_goodscode))
                db_con.execute(sql_u)
            else:
                print(">> 한글있음 (skip) : {} ".format(in_old_title))
        else:
            print(">> 타이틀 번역 Insert : {} ".format(in_asin))
            db_con.execute(sql_i)

    return "0"

def replace_option_value(ori_value):

    rep_value = ori_value.replace('「', ' ').replace('」', ' ')
    rep_value = rep_value.replace(',', ' | ')
    rep_value = rep_value.replace('&gt;', ' - ').replace('&lt;', ' ')
    rep_value = rep_value.replace('<br>', ' ').replace('\n', '')
    rep_value = rep_value.replace('/', ' & ')
    rep_value = rep_value.replace('{', ' ').replace('}', ' ').replace("、"," . ")

    return str(rep_value).strip()


# get_galleryGoods
def get_galleryGoods(in_soup, in_asin):
    gallery_tmp = ""
    cnt_save = 0
    detail_gallery_item = str(in_soup).split('data-asin=')
    print('>> gallery cnt : ' + str(len(detail_gallery_item)))

    if len(detail_gallery_item) == 0:
        print('>> gallery goods 0')
        return "1"

    glow = 1
    while glow < len(detail_gallery_item):
        detail_gallery_ea = getparse(detail_gallery_item[glow], '"', '"')
        # print('>> gallery_ea ('+str(glow)+') : ' + str(detail_gallery_ea))

        if str(detail_gallery_ea) != str(in_asin) and gallery_tmp.find(detail_gallery_ea) == -1 and len(detail_gallery_ea) == 10:
            cnt_save = cnt_save + 1
            if gallery_tmp == "":
                gallery_tmp = detail_gallery_ea
            else:
                gallery_tmp = gallery_tmp + "," + detail_gallery_ea

        glow = glow + 1

    print('>> gallery goods (only) : ' + str(cnt_save))
    return "".join(gallery_tmp)

def replace_currency_opt(in_string):
    result_str = str(in_string)
    result_str = result_str.replace('￥', '').replace('¥', '').replace('¥', '').replace('$', '').replace('€', '').replace('£', '').replace('USD', '')
    result_str = result_str.replace('Â\xa0', '').replace('Â', '').replace('\u202f','').replace('u202f','').strip()

    return result_str

def replace_currency(in_string):
    result_str = str(in_string)
    result_str = result_str.replace('￥', '').replace('¥', '').replace('¥', '').replace('$', '').replace('€', '').replace('£', '').replace('USD', '')
    result_str = result_str.replace('Â\xa0', '').replace('&nbsp;', '').replace('\u202f','').replace('u202f','').replace('\\','').replace('/','').replace('"','').replace("'","")
    result_str = result_str.replace('Â', '').strip()

    return result_str

# get_option_price_new2 (옵션 가격)
def get_option_price_new2(temp_asin_str, nFlg):

    temp_asin = ""
    temp_asin_item = temp_asin_str.split('@')
    temp_parent_asin = temp_asin_item[0]
    temp_asin = temp_asin_item[1]
    opt_goods_price = "0"
    temp_result_str = ""

    cookies = {'lc-acbjp': 'en_US'}
    if nFlg == "US":
        cookies = {'lc-main': 'en_US'}
    elif nFlg == "JP":
        cookies = {'lc-acbjp': 'en_US'}
    elif nFlg == "DE":
        cookies = {'lc-acbde': 'en_GB', 'i18n-prefs': 'USD'}
    elif nFlg == "UK" or nFlg == "FR":
        #cookies = {'lc-acbuk': 'en_GB', 'i18n-prefs': 'USD'}
        cookies = {'lc-acbuk': 'en_GB'}

    siteName = getCountryInfo(nFlg,"3")
    time.sleep(random.uniform(1,2))
    if str(temp_asin).strip() == "":
        print('temp_asin No')
    else:

        ### https://www.amazon.co.jp/gp/twister/dimension?isDimensionSlotsAjax=1&asinList=B09T2P7DTK,B09T2FTRVJ,B09XTTRYB7,B09T2HWJLR,B09XTPMW7Y,B09XTNYDFT=1&productTypeDefinition=DISHWARE_BOWL&productGroupId=home_display_on_website&parentAsin=B0BPBF5BNG&isPrime=0&isOneClickEnabled=0&deviceType=web&showFancyPrice=false&twisterFlavor=twisterPlusDesktopConfigurator
        
        onurl = 'https://' + str(siteName) + '/gp/p13n-shared/faceout-partial?asinMetadataKeys=adId%3AParentReasonId%3AParentReasonId.substitutions.purchase_date%3ArId&widgetTemplateClass=PI%3A%3ASimilarities%3A%3AViewTemplates%3A%3ACarousel%3A%3ADesktop&productDetailsTemplateClass=PI%3A%3AP13N%3A%3AViewTemplates%3A%3AProductDetails%3A%3ADesktop%3A%3ADeliverySpeed&forceFreshWin=0&painterId=PersonalizationDesktopSimilaritiesCarousel&featureId=SimilaritiesCarousel&reftagPrefix=pd_sim_263&faceoutTemplateClass=PI%3A%3AP13N%3A%3AViewTemplates%3A%3AProduct%3A%3ADesktop%3A%3ACarouselFaceout&auiDeviceType=desktop&schemaVersion=2&relatedRequestID=ZK6NV7SJJ8BQC2RFERAF&productDataFlavor=FaceoutAddToCartShippingPromises&maxLineCount=6&count=6&offset=12&asins=' + str(temp_asin) + '%3A%3A%3A%3A&_=1601727641226'
        #print(">> onurl : {}".format(onurl))
        try:
            opt_source_code = requests.get(onurl, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                    random.random()) + ' Safari/537.36', 'Referer': 'https://' + str(siteName)}, cookies=cookies)

        except Exception as ex:
            print('>> Exception  ')
            time.sleep(2)
            print('>> No check')
            #return "C03"
        else:
            time.sleep(random.uniform(2,3))
            opt_html_str = opt_source_code.text
            
            if str(opt_html_str).find(temp_asin) == -1:
                set_new_tor_ip()
                #checkCurrIP()
                return "D08"
            if str(opt_html_str).find(temp_asin) > -1:
                opt_goods_price = getparse(str(opt_html_str),"class='p13n-sc-price' >","</span>")
                opt_goods_price = str(opt_goods_price).replace('</p>', '').strip()
                opt_goods_price = replace_currency(opt_goods_price)

            if (str(opt_goods_price) == "0"):
                print('>> No check : {}'.format(temp_asin))
                #print('>> opt_html_str : '+str(opt_html_str))
                #return "D08"
                set_new_tor_ip()
                #checkCurrIP()
                time.sleep(1)
            else:
                temp_result_str = temp_asin + '@' + str(opt_goods_price)
                #print(temp_result_str)
                #print('>> option price (new) : ' + str(opt_goods_price))

    return temp_result_str

# 2captcha
def send_capcha():
    numbers = []

    imgfilename = "C:\project\log\captche_img\captche_img_full.png"
    print('\n screen filename : ' + str(imgfilename))
    #fileWt('\n screen filenam : ' + str(imgfilename))

    im = Image.open(str(imgfilename))  # uses PIL library to open image in memory

    left = 400
    top = 345
    right = left + 420
    bottom = top + 90

    im = im.crop((left, top, right, bottom))  # defines crop points
    savefilename = "C:\project\log\captche_img\captche_img_crop.png"
    print('\n captche_img file : ' + str(savefilename))
    #fileWt('\n captche_img fil : ' + str(savefilename))
    im.save(str(savefilename))

    captchafile = {'file': open(savefilename, 'rb')}
    data = {'key': gTWOCAPTCHA_API_KEY, 'method': 'post'}
    r = requests.post('http://2captcha.com/in.php', files=captchafile, data=data)
    soupNm = BeautifulSoup(r.content, "html.parser")
    resultStr = soupNm.text
    #print('\n resultStr : ' + str(resultStr))


    if r.ok and r.text.find('OK') > -1:
        reqid = r.text[r.text.find('|') + 1:]
        print("[+] Capcha id: " + reqid)
        for timeout in range(40):
            r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(gTWOCAPTCHA_API_KEY, reqid))
            if r.text.find('CAPCHA_NOT_READY') > -1:
                print(r.text)
                time.sleep(3)
            if r.text.find('ERROR') > -1:
                print('\n CAPCHA ERROR')
                #fileWt('\n CAPCHA ERROR')
                return []
            if r.text.find('OK') > -1:
                print('\n CAPCHA OK  ')
                #fileWt('\n CAPCHA OK  ')

                return list(r.text[r.text.find('|') + 1:])
    return []


# getCaptcha
def getCaptcha(in_driver):
    strCaptcha = ""

    ########################################################################
    in_driver.implicitly_wait(3)
    sc_img_name = "C:\project\log\captche_img\captche_img_full.png"
    in_driver.get_screenshot_as_file(str(sc_img_name))
    ########################################################################

    time.sleep(1)
    #print('time.sleep(1)')

    print('>> send_capcha ')
    # 2captcha
    captRtn = send_capcha()
    print('\n captRtn : ' + str(captRtn))
    #fileWt('\n captRtn  : ' + str(captRtn))

    low = 0
    while low < len(captRtn):
        # print(captRtn[low])
        strCaptcha = strCaptcha + captRtn[low]
        low = low + 1

    print('\n Captcha : ' + strCaptcha)
    #fileWt('\n Captcha: ' + strCaptcha)

    time.sleep(1)
    print('time.sleep(1)')

    return str(strCaptcha).strip()



def checkOrderHistory(in_code):
    
    rtnCnt = ""
    rtnGoodsuid = ""
    rtnGoodscode = ""
    rtnSitecate = ""

    time.sleep(1)
    searchurl = "http://59.23.231.204:8090/service/search.json?cn=freeship&fl=GOODSUID,goodscode,sitecate&se={goodscode:ALL(" +str(in_code)+ "):100:15}&sn=1&ln=10"
    #print("searchurl : "+str(searchurl))

    try:
        print('>> searchurl Connect ')
        req: Request = Request(searchurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                random.random()) + ' Safari/537.36', 'Referer': 'https://www.freeship.co.kr'})
        connection = urlopen(req)

    except Exception as ex:
        print('>> checkOrder error (Exit): ', ex)
        #os._exit(1)
        return "E"
    else:
        resultSoup = BeautifulSoup(connection, "html.parser")
        rtnCnt = getparse(str(resultSoup), '"total_count":', ',')
        rtnGoodsuid = getparse(str(resultSoup), '"GOODSUID":"', '"')
        rtnGoodscode = getparse(str(resultSoup), '"GOODSCODE":"', '"')
        rtnSitecate = getparse(str(resultSoup), '"SITECATE":"', '"')

        #print(str(rtnGoodsuid) + " | " + str(rtnGoodscode) + " | " + str(rtnSitecate))
        if rtnGoodscode != "":
            print(">> 주문 내역 있음 : " + str(rtnGoodscode) + " | " + str(rtnSitecate) + " | " + str(rtnGoodsuid))
        else:
            print(">> 주문 내역 없음 : " + str(in_code))

    return str(rtnGoodsuid).strip()


def procIpChange(maxCnt):
    wCnt = 0 
    while wCnt < maxCnt:
        set_new_tor_ip()
        checkCurrIP()
        time.sleep(5)
        wCnt = wCnt + 1


def priceCheck(countryKbn, goods_price):
    ##### price check #####
    if countryKbn == "JP":
        if float(goods_price) < 99:
            print('>> 99 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 99

        if float(goods_price) > 120000:
            print('>> 120,000 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 120000 over

    elif countryKbn == "US":
        if float(goods_price) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 달러 미만

        if float(goods_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 달러 over

    elif countryKbn == "DE":
        if float(goods_price) < 1:
            print('>> 1 달러 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 유로 미만

        if float(goods_price) > 1100:
            print('>> 1100 달러 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 유로 over

    elif countryKbn == "UK" or countryKbn == "FR":
        if float(goods_price) < 1:
            print('>> 1 파운드 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 유로 미만

        if float(goods_price) > 700:
            print('>> 700 파운드 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 유로 over

    else:
        if float(goods_price) < 1:
            print('>> 1 미만 (skip)')
            return "D12" + " ( " + str(goods_price) + " ) "  # 1 미만

    return ""

def check_browser(browser, now_url):
    print(">> Browser Count : {}".format(len(browser.window_handles)))
    if len(browser.window_handles) != 1:
        print(">> Browser Close : {}".format(len(browser.window_handles)))
        time.sleep(1)
        main = browser.window_handles
        last_tab = browser.window_handles[len(main) - 1]
        print('>> last_tab: ' + str(last_tab))
        if str(len(main)) != "1":
            for handle in main:
                if handle != last_tab:
                    browser.switch_to.window(window_name=handle)
                    browser.close()
                browser.switch_to.window(window_name=last_tab)
            time.sleep(2)
        print(">> Browser Close (after) : {}".format(len(browser.window_handles)))
        time.sleep(1)
        browser.get(now_url)
        time.sleep(4)

def proc_asin_parse_brower(in_asin_str, db_con, db_price, in_drive, in_pg, in_pgsite, manage_dic):   
    countryKbn = getCountryInfo(in_pgsite,"1")
    in_tor =  manage_dic['py_tor'] 
    in_pgSite = manage_dic['py_pgSite']
    chkCode = ""
    asin = ""
    cateidx = ""
    detail_soup = ""
    gallery_tmp = ""
    db_Del_Naver = ""
    db_goodscode = ""
    sp_asin = in_asin_str.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]

    guid = ""
    guid = sp_asin[3]
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    db_org_title = ''
    db_Del_Naver = ""
    db_title = ''
    db_Weight = "0"
    DB_stop_update = "0"
    db_OriginalPrice = 0
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        if countryKbn == "JP":
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, JP_title, title, isnull(OriginalPrice,0) from t_goods where display_ali_no = '{0}'".format(asin)
        else:
            if in_pgSite == "uk" or in_pgSite == "fr":
                sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, isnull(OriginalPrice,0) from t_goods where display_ali_no = '{}' and site_kbn = '{}'".format(asin, in_pgSite)
            else:
                sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, isnull(OriginalPrice,0) from t_goods where display_ali_no = '{0}'".format(asin)
    else:
        if countryKbn == "JP":
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, JP_title, title, isnull(OriginalPrice,0) from t_goods where uid = {0}".format(guid)
        else:
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, IT_title, title, isnull(OriginalPrice,0) from t_goods where uid = {0}".format(guid)
    try:
        rowUP = db_con.selectone(sql)
    except Exception as e:
        print(">> exception sql : {}".format(sql))
        print('>> exception 1-1 asin : {}'.format(asin))
        print(">> mac_address : {}".format(mac_addr()))
        checkIP()
        time.sleep(10)
        #procEnd(db_con, in_drive, "")
        return "E99"

    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_org_title = rowUP[5]
        db_title = rowUP[6]
        db_OriginalPrice = rowUP[7]
        if db_goodscode == None or db_goodscode == "":
            print(">> 기존 상품 goodscode 없는 상품 goodscode 재생성 후 update 처리 ")
            newgoodscode = ""
            newgoodscode = get_newgoodscode(db_con, db_uid, in_pgsite)
            if newgoodscode == "Q01":
                return "Q01"
            db_goodscode = newgoodscode

        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid

        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"

        if str(db_Del_Naver) == "4":
            print('>> Del_Naver 4 (6개월 지난 데이터 재등록 처리후 삭제대상) : ' + str(asin))
            return "S03"

        if str(db_Del_Naver) == "1":
            print('>> Del_Naver 1 (네이버 미노출상품) : ' + str(asin))
            #return "S02"

        if str(DB_stop_update) == "1":
            print('>> stop_update goods : ' + str(asin))
            return "S01"
    print('>> stop_update No goods : ' + str(asin))

    if str(guid) == '':
        print('>>>>>>>>>>>>>>>>>>>>> no guid (신규) ')
        sqlre = ""
        if in_pgSite == "uk":
            sqlre = "select goodscode from t_goods where display_ali_no = '{}' and site_kbn = 'fr'".format(asin)
        elif in_pgSite == "fr":
            sqlre = "select goodscode from t_goods where display_ali_no = '{}' and site_kbn = 'uk'".format(asin)
        if sqlre != "":
            try:
                rowRe = db_con.selectone(sqlre)
            except Exception as e:
                print(">> exception sql : {}".format(sql))
            else:
                if rowRe:
                    find_goodscode = rowRe[0]
                    print(">> {} already exists asin (SKIP) : {} | {}".format(in_pgSite, find_goodscode, asin))
                    return "S04"
    else:
        print('>>>>>>>>>>>>>>>>>>>>> guid (존재) : ' + str(guid))

    r_cnt = 1
    while r_cnt < 3:

        if r_cnt > 1:
            time.sleep(3)

            in_drive.refresh()
            if in_tor == "Y":
                set_new_tor_ip()
                checkCurrIP()

        time.sleep(random.uniform(0.5,1))
        #############################################################################
        now_url = ""
        amazon_siteUrl = str(getCountryInfo(in_pgsite,"3"))
        if countryKbn == "DE":
            now_url = "https://" + amazon_siteUrl + "/-/en/dp/" + str(asin) + "?currency=USD&language=en_GB"
        elif countryKbn == "UK":
                now_url = "https://" + amazon_siteUrl + "/-/en/dp/" + str(asin) + "?language=en_GB"
        elif countryKbn == "FR":
            now_url = "https://" + amazon_siteUrl + "/-/en/dp/" + str(asin) + "?language=en_GB"
        elif countryKbn == "JP":
            now_url = "https://" + amazon_siteUrl + "/-/en/dp/" + str(asin) + "?language=en_US"
        else:
            now_url = "https://" + amazon_siteUrl + "/-/en/dp/" + str(asin)

        print('>> now_url : ' + str(now_url))
        try:
            in_drive.get(now_url)
        except Exception as e:
            print('>> now_url Connect Exception Error ')
            #return "C01"
            chkCode = "C01"
            return chkCode
        else:
            time.sleep(random.uniform(3,4))

        result = ""
        result = str(in_drive.page_source)
        time.sleep(1)

        if str(in_drive.current_url).find(asin) > -1:
            print(">> current_url : {}".format(in_drive.current_url))
        else:
            time.sleep(random.uniform(4,5.5))
            result = in_drive.page_source

        if str(in_drive.current_url).find(asin) == -1:
            print(">> current_url : {}".format(in_drive.current_url))
            chkCode = "C02"
            return "C02"

        # with open(os.getcwd() + "/amazon_file/result_amzon_" +str(asin)+ ".html","w",encoding="utf8") as f: 
        #     f.write(str(result))
        if str(result).find('validateCaptcha') > -1 or str(result).find('Enter the characters') > -1 or str(result).find('Type the characters') > -1:
            print('>> validateCaptcha (auto) ')
            if in_tor == "Y":
                # ip 3회 변경
                procIpChange(3) 
            chkCode = "C02"
            return chkCode

        if str(result).find('continue-shopping.gif') > -1:
            print('>> continue-shopping.gif (auto) ')
            try:
                in_drive.find_element(By.XPATH,'/html/body/center/center/p/table/tbody/tr/td/p[5]/a').click()
            except Exception as ex:
                print('>> Exception (SKIP)', ex)
            else:
                #print('>> time.sleep(2) ')
                time.sleep(1)
            if in_tor == "Y":
                # ip 3회 변경
                procIpChange(3) 

        if str(result).find('[YES]') > -1:
            print('>> [YES] button ')
            try:
                # in_drive.find_element_by_link_text('[YES]').click()
                in_drive.find_element(By.LINK_TEXT,'[YES]').click()
            except Exception as ex:
                print('>> Exception (SKIP)', ex)
            else:
                print('>> [YES] button Click Ok ')
                time.sleep(1)

        if str(result).find('black-curtain-redirect.html') > -1:
            print('>> black-curtain-redirect.html ')

            if str(result).find('[YES]') > -1:
                print('>> [YES] button ')
                try:
                    in_drive.find_element(By.LINK_TEXT,'[YES]').click()
                except Exception as ex:
                    print('>> Exception (SKIP)', ex)
                else:
                    print('>> [YES] button Click Ok ')
                    time.sleep(1)
            else:
                chkCode = "D18"
                break

        if str(result).find('kailey-kitty._TTD_.gif') > -1:
            print('>> Click here to go back to the Amazon home page ')
            chkCode = "D17"
            break

        if str(result).find('title._TTD_.png') > -1:
            print('>> (title._TTD_.png) No goods ')
            chkCode = "D17"
            break

        if str(result).find('not a functioning page on our site') > -1:
            print('>> not a functioning page on our site ')
            chkCode = "D17"
            break

        if str(result).find('id="ListenNowButton"') > -1:
            print('>> (ListenNowButton) Music goods ')
            chkCode = "D17"
            break

        if str(result).find('500_503.png') > -1:
            print('>> 500_503.png ')
            chkCode = "D17"
            break

        if str(result).find('Please go back and try again') > -1:
            print('>> Please go back and try again or go to Amazon ')
            chkCode = "D17"
            break

        if str(result).find('continue-shopping.gif') == -1 and str(result).find('validateCaptcha') == -1 and str(
                result).find('kailey-kitty._TTD_.gif') == -1:
            print('>> Connect Ok ')
            break

        if str(result).find('continue-shopping.gif') > -1:
            print('>> (continue-shopping.gif) error ')
            chkCode = "C02"
            break
            #return "C02"

        r_cnt = r_cnt + 1

    if chkCode == "D17":
        print('>>  No goodscode ')
        return chkCode

    if chkCode == "C02" or chkCode == "C01":  # continue-shopping.gif
        print('>> continue-shopping.gif ')
        return chkCode

    if chkCode == "D18":  # black-curtain-redirect
        print('>> black-curtain-redirect ')
        return chkCode

    if str(result).find('continue-shopping.gif') > -1 or str(result).find('validateCaptcha') > -1:
        print('>> Connect Error ')

        if str(result).find('continue-shopping.gif') > -1:
            print('>> (continue-shopping.gif) error ')
            return "C05"

    result = str(in_drive.page_source)
    chkString = getparse(str(result),'<title>','</title>')
    if str(chkString).find('Tut uns Leid!') > -1:
        print('>> Url Connect error ')
        return "C02"

    print(">> Browser Count : {}".format(len(in_drive.window_handles)))
    if len(in_drive.window_handles) != 1:
        check_browser(in_drive, now_url)

    ############ Deliver to check #############################
    deliverTo = procDeliverChk(in_drive)  # Deliver to check
    print('>> deliverTo : ' + str(deliverTo))
    cPost = str(manage_dic['py_sitePost'])
    print('>> cPost : ' + str(cPost))

    tmp_cPost = cPost
    if countryKbn == "UK" or countryKbn == "DE":
        tmp_cPost = cPost[:5]

    if str(deliverTo).find(tmp_cPost) == -1:
        print('>> Deliver to set : ' + str(deliverTo))

        if countryKbn == "UK" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "DE" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "FR" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "US" and str(deliverTo).find("97223") > -1:
            print("(US) 97223 OK ")
        else:
            procDelivertoSet(in_drive,countryKbn, cPost)  # Deliver to Set
            time.sleep(2)

    deliverTo = procDeliverChk(in_drive)  # Deliver to check
    print('>> deliverTo (after): ' + str(deliverTo))
    if countryKbn == "US" and str(deliverTo).find("97223") > -1:
        print("(US) 97223 OK ")
    elif str(deliverTo).find(tmp_cPost) == -1:
        print('>> deliverTo noset (SKIP) ' + str(deliverTo))
        if in_tor == "Y":
            return "C06"
        else:
            pass

    #########################################################################
    time.sleep(1)
    detail_soup = ""
    chk_soup = ""
    priceSource = ""
    result = ""
    result = in_drive.page_source
    # print("result : "+str(result))
    #########################################################################
    time.sleep(1)
    if str(result).find('id="productTitle"') == -1:
        print('>> detail_soup No')

        if str(result).find('https://images-na.ssl-images-amazon.com/captcha') > -1:
            print('>> Error block - captcha - ')
            print('>> C04 blocked (captcha) ')
            return "C04"  # blocked

        if countryKbn == "UK" or countryKbn == "DE" or countryKbn == "FR":
            print('>> C5 blocked ')
            return "C05"  # blocked
        else:
            print('>> D02 No Title ')
            return "D02"  # blocked

    deliver_post = ""
    try:
        #deliver_post = in_drive.find_element_by_id('glow-ingress-line2').text
        deliver_post = in_drive.find_element(By.ID, 'glow-ingress-line2').text
    except Exception as ex:
        print('>> error : ', ex)
        return "C01"
    else:
        deliver_post = str(deliver_post).replace('\u200c','')
        print(">> deliver_post : " + str(deliver_post))

    ######################## goods parsing ########################
    print('>> goods parsing ######################## ')
    result = in_drive.page_source
    if str(result).find('id="dp-container"') > -1:
        if str(result).find('id="rhf-container"') > -1:
            detail_soup = getparse(str(result), 'id="dp-container"', 'id="rhf-container"')
        else:
            detail_soup = getparse(str(result), 'id="dp-container"', '')
    else:
        if str(result).find('id="rhf-container"') > -1:
            detail_soup = getparse(str(result), '', 'id="rhf-container"')
        else:
            detail_soup = str(result)
    #time.sleep(1)
    #print('time.sleep(1)')

    ##### Buy used check #####
    chk_soup = getparse(str(detail_soup), 'div id="usedBuySection"', '<div class="a-button-stack">')
    if str(chk_soup).find('Buy used:') > -1:
        print('>> Buy used (1)')
        return "D04"
    elif str(chk_soup).find('Used - Good') > -1:
        print('>> Used - Good (1)')
        return "D04"
    elif str(chk_soup).find('Buy pre-owned:') > -1:
        print('>> Buy pre-owned (1)')
        return "D04"
    elif str(chk_soup).find('Pre-owned:') > -1:
        print('>> Pre-owned (1)')
        return "D04"
    elif str(chk_soup).find("Achetez d'occasion") > -1:
        print('>> Buy used (fr)')
        return "D04"
    else:
        print('>> Buy used check ok')

    ##### Customisable check #####
    if str(result).find(' <div id="gestalt-buybox"') > -1:
        print('>> (Customisable) Unsellable product ')
        return "D120"

    ##### Pre-order #####
    # strPreorder = getparse(str(detail_soup), 'id="buy-now-button"', '<div class="a-button-stack">')
    # if str(strPreorder).find('Pre-order') > -1:
    #     print('>> Pre-order (1)')
    #     return "D10"  # Pre-order
    # else:
    #     print('>> Pre-order check Ok')

    ##### add-on Item  #####
    strAddon = getparse(str(detail_soup), '<div class="a-box-group">', "</div>")
    if str(strAddon).find('Add-on Item') > -1:
        print('>> add-on Item (1)')
        # return "D05" # Add-on Item
    #else:
        #print('>> Add-on Item (check ok)')

    priceSource = getparse(str(result), 'id="productTitle"', 'id="featurebullets_feature_div"')
    ##### Sold Out #####
    if priceSource.find('Currently unavailable.') > -1:
        if priceSource.find('when or if this item will be back in stock.') > -1:
            print('>> Currently unavailable. : ' + str(asin))
            print('>> Sold Out')
            return "D01"

    ##### Sold Out #####
    if priceSource.find('Actuellement indisponible.') > -1:
        if priceSource.find('Nous ne savons pas quand cet article sera de nouveau approvisionné') > -1:
            print('>> Currently unavailable. (Actuellement indisponible.) : ' + str(asin))
            print('>> Sold Out')
            return "D01"

    ##### pantry #####
    if priceSource.find('class="pantry-store-info-inner"') > -1:
        print('>> pantry-store unavailable. : ' + str(asin))
        print('>> pantry goods')
        return "D13"  # pantry goods

    if str(result).find('id="olp_feature_div"') > -1 and str(result).find('div id="hover-zoom-end"') > -1:
        priceSource = getparse(str(result), 'id="productTitle"', 'div id="hover-zoom-end"')
    goods_price = "0"

    priceValue = getparse(str(result), 'type="hidden" name="priceValue" value="', '"')
    if priceValue != "":
        priceValue = replace_currency(priceValue)
        print(">> priceValue : {}".format(priceValue))
        goods_price = priceValue
    else:
        print(">> No priceValue ")
        displayPrice = getparse(str(result), '{"desktop_buybox_group_1":[{"displayPrice":"', '"')
        if displayPrice != "":
            displayPrice = replace_currency(displayPrice)
            print(">> displayPrice : {}".format(displayPrice))

            if in_pgSite == "fr" and displayPrice.find(',') > -1:
                displayPrice = displayPrice.replace(',','').replace('\u202f', '').replace('u202f', '').replace(' ','.').strip()
                print(">> displayPrice (프랑스 edt) : {}".format(displayPrice))
            else:
                displayPrice = displayPrice.replace(',','').strip()
                print(">> displayPrice (edt) : {}".format(displayPrice))
            goods_price = displayPrice
        else:
            print(">> No displayPrice ")

    if str(goods_price) == "0" or str(goods_price) == "":
        goods_price = soldout_check_2(str(priceSource),countryKbn)
        if in_pgSite == "fr" and goods_price.find(',') > -1:
            # goods_price = goods_price.replace(',','.').replace('\u202f', '').replace('u202f', '').replace(' ','.')
            # print(">> goods_price (영국 edt) : {}".format(goods_price))
            print('>> 700 파운드 over (skip)')
            return "D09" + " ( " + str(goods_price) + " ) "  # 1100 유로 over

    if str(goods_price) == "0" or str(goods_price) == "":
        if str(result).find('See All Buying Options') > -1 and guid != "":
            print('>> See All Buying Options (B01)')
            return "B01"
        if str(result).find('id="unqualifiedBuyBox"') > -1 and guid != "":
            print('>> See All Buying Options (B01)')
            return "B01"
        if str(priceSource).find('"parentAsin" : "') == -1:
            if str(result).find('"parentAsin" : "') == -1:
                print('>>No parentAsin .. Sold Out')
                return "D31"
    else:
        ##### price check #####
        rtnPriceCheck = priceCheck(countryKbn, goods_price)
        if rtnPriceCheck != "":
            return rtnPriceCheck

    gallery_tmp = get_galleryGoods(str(detail_soup), asin)
    # if gallery_tmp == "1":
    #     print('>> gallery no')
    # else:
    #     # print('>> gallery goodscode : ' + str(gallery_tmp))
    #     print('>> gallery OK ')

    rtn_reviews_arr = []
    rtn_rate_arr = []
    if str(detail_soup).find('No customer reviews') > -1:
        pass
        #print('>> No customer reviews')
    else:
        # rtn_reviews_arr = get_Review(str(detail_soup), asin)
        rtn_reviews_arr, rtn_rate_arr = get_Review_new(str(detail_soup), asin)
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
    goods['rate'] = rtn_rate_arr
    goods['guid'] = str(guid)
    goods['db_Weight'] = str(db_Weight)
    goods['db_title'] = str(db_title)
    goods['db_org_title'] = str(db_org_title)
    goods['db_goodscode'] = str(db_goodscode)
    goods['db_OriginalPrice'] = float(db_OriginalPrice)
    goods['del_naver'] = db_Del_Naver

    rtnDetail = ""
    rtnDetail = parsing_detail(str(detail_soup), asin, goods, db_con, db_price, in_drive, in_pg, countryKbn, in_pgsite, manage_dic)
    if rtnDetail != "0":
        print('>> error :' + str(rtnDetail))
        return rtnDetail

    return "0"


# 재고 체크
def proc_asin_out_brower(in_asin_str,db_con, db_price, in_drive, in_pg, in_pgsite, manage_dic):   
    countryKbn = getCountryInfo(in_pgsite,"1")
    in_tor = manage_dic['py_tor'] 
    chkCode = ""
    asin = ""
    cateidx = ""
    detail_soup = ""
    db_Del_Naver = ""
    priceSource = ""
    sp_asin = in_asin_str.split('@')
    asin = sp_asin[0]
    cateidx = sp_asin[1]
    guid = ""
    guid = sp_asin[3]
    print('>> guid : ' + str(guid))
    print('>> catecode : ' + str(cateidx) + ' | asin : ' + str(asin) + ' | ' + str(datetime.datetime.now()))

    db_Weight = "0"
    DB_stop_update = "0"
    # stop_update check
    if str(guid) == '' or guid is None or guid == "None":
        guid = ''
        if in_pgsite == "uk" or in_pgsite == "fr":
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where display_ali_no = '{}' and site_kbn = '{}'".format(asin, in_pgsite)
        else:
            sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where display_ali_no = '{0}'".format(asin)
    else:
        sql = "select isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), uid, isnull(Del_Naver,0), goodscode, title from t_goods where uid = {0}".format(guid)
    checkIP()
    print(">> mac_address : {}".format(mac_addr()))
    print(">> sql : {}".format(sql))
    rowUP = db_con.selectone(sql)
    if rowUP:
        DB_stop_update = rowUP[0]
        db_Weight = rowUP[1]
        db_uid = rowUP[2]
        db_Del_Naver = rowUP[3]
        db_goodscode = rowUP[4]
        db_title = rowUP[5]
        if db_goodscode == None or db_goodscode == "":
            print(">> 기존 상품 goodscode 없는 상품 goodscode 재생성 후 update 처리 ")
            newgoodscode = get_newgoodscode(db_con, db_uid, in_pgsite)
            if newgoodscode == "Q01":
                return "Q01"
            db_goodscode = newgoodscode

        print('>> [DB] {0} ( {1} ) : stop_update ({2}) | db_Weight ({3}) | db_Del_Naver ({4})'.format(db_goodscode,db_uid,DB_stop_update,db_Weight,db_Del_Naver))
        guid = db_uid

        if str(db_Del_Naver) == "9":
            print('>> Del_Naver 9 (네이버 노클릭상품) : ' + str(asin))
            return "S02"

        if str(db_Del_Naver) == "4":
            print('>> Del_Naver 4 (6개월 지난 데이터 재등록 처리후 삭제대상) : ' + str(asin))
            return "S03"

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

    r_cnt = 1
    while r_cnt < 3:

        if r_cnt > 1:
            time.sleep(2)
            in_drive.refresh()
            if in_tor == "Y":
                set_new_tor_ip()
                checkCurrIP()
        time.sleep(2)

        #############################################################################
        now_url = ""
        if countryKbn == "DE":
            now_url = "https://" +str(getCountryInfo(in_pgsite,"3"))+ "/-/en/dp/" + str(asin) + "?currency=EUR&language=en_GB"
        elif countryKbn == "UK" or countryKbn == "FR":
            now_url = "https://" +str(getCountryInfo(in_pgsite,"3"))+ "/-/en/dp/" + str(asin) + "?language=en_GB"
        elif countryKbn == "JP":
            now_url = "https://" +str(getCountryInfo(in_pgsite,"3"))+ "/-/en/dp/" + str(asin) + "?language=en_US"
        else:
            now_url = "https://" +str(getCountryInfo(in_pgsite,"3"))+ "/-/en/dp/" + str(asin)

        print('>> now_url : ' + str(now_url))
        try:
            in_drive.get(now_url)
        except Exception as e:
            print('>> now_url Connect Exception Error ')
            return "C01"
        else:
            time.sleep(4)     

        result = in_drive.page_source
        time.sleep(1)
        if str(in_drive.current_url).find(asin) > -1:
            print(">> current_url : {}".format(in_drive.current_url))
        else:
            time.sleep(4) 
            result = in_drive.page_source

        if str(in_drive.current_url).find(asin) == -1:
            print(">> current_url : {}".format(in_drive.current_url))
            chkCode = "C02"
            return "C02"

        if str(result).find('continue-shopping.gif') > -1:
            print('>> continue-shopping.gif (auto) ')
            try:
                in_drive.find_element(By.XPATH,'/html/body/center/center/p/table/tbody/tr/td/p[5]/a').click()
            except Exception as ex:
                print('>> Exception (SKIP)', ex)
            else:
                time.sleep(1)

        if str(result).find('validateCaptcha') > -1 or str(result).find('Enter the characters') > -1 or str(result).find('Type the characters') > -1:
            print('>> validateCaptcha (auto) ')
            if in_tor == "Y":
                # ip 3회 변경
                procIpChange(3) 
            chkCode = "C02"
            break

        if str(result).find('black-curtain-redirect.html') > -1:
            print('>> black-curtain-redirect.html ')
            chkCode = "D18"
            break

        if str(result).find('kailey-kitty._TTD_.gif') > -1:
            print('>> Click here to go back to the Amazon home page ')
            chkCode = "D17"
            break

        if str(result).find('title._TTD_.png') > -1:
            print('>> (title._TTD_.png) No goods ')
            chkCode = "D17"
            break

        if str(result).find('not a functioning page on our site') > -1:
            print('>> not a functioning page on our site ')
            chkCode = "D17"
            break

        if str(result).find('id="ListenNowButton"') > -1:
            print('>> (ListenNowButton) Music goods ')
            chkCode = "D17"
            break

        if str(result).find('500_503.png') > -1:
            print('>> 500_503.png ')
            chkCode = "D17"
            break

        if str(result).find('Please go back and try again') > -1:
            print('>> Please go back and try again or go to Amazon ')
            chkCode = "D17"
            break

        if str(result).find('continue-shopping.gif') == -1 and str(result).find('validateCaptcha') == -1 and str(result).find('kailey-kitty._TTD_.gif') == -1:
            print('>> Connect Ok ')
            break

        if str(result).find('continue-shopping.gif') > -1:
            print('>> (continue-shopping.gif) error ')
            return "C02"

        r_cnt = r_cnt + 1

    if chkCode == "D17":
        print('>>  No goodscode ')
        return chkCode

    if chkCode == "D18":  # black-curtain-redirect
        print('>> black-curtain-redirect ')
        return chkCode

    if str(result).find('continue-shopping.gif') > -1 or str(result).find('validateCaptcha') > -1:
        print('>> Connect Error ')
        if str(result).find('continue-shopping.gif') > -1:
            print('>> (continue-shopping.gif) error ')
            return "C05"

    chkString = getparse(str(result),'<title>','</title>')
    if str(chkString).find('Tut uns Leid!') > -1:
        print('>> Url Connect error ')
        return "C02"

    print(">> Browser Count : {}".format(len(in_drive.window_handles)))
    if len(in_drive.window_handles) != 1:
        check_browser(in_drive, now_url)

    ############ Deliver to check #############################
    deliverTo = procDeliverChk(in_drive)  # Deliver to check
    cPost = getCountryInfo(countryKbn,"4")
    print('>> cPost : ' + str(cPost))

    tmp_cPost = cPost
    if countryKbn == "UK":
        tmp_cPost = cPost[:5]

    if str(deliverTo).find(tmp_cPost) == -1:
        print('>> Deliver to set : ' + str(deliverTo))
        if countryKbn == "UK" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "DE" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "FR" and str(deliverTo).find("Select your address") > -1:
            print("Select your address (SKIP) ")
        elif countryKbn == "US" and str(deliverTo).find("97223") > -1:
            print("(US) 97223 OK ")
        else:
            procDelivertoSet(in_drive,countryKbn, cPost)  # Deliver to Set
            time.sleep(2)

    deliverTo = procDeliverChk(in_drive)  # Deliver to check
    print('>> deliverTo (after): ' + str(deliverTo))
    if countryKbn == "US" and str(deliverTo).find("97223") > -1:
        print("(US) 97223 OK ")
    elif str(deliverTo).find(tmp_cPost) == -1:
        print('>> deliverTo noset (SKIP) ' + str(deliverTo))
        if in_tor == "Y":
            return "C06"
    
    #########################################################################
    time.sleep(1)
    result = in_drive.page_source
    time.sleep(1)
    #########################################################################

    if str(result).find('id="productTitle"') == -1:
        print('>> detail_soup No')
        if str(result).find('https://images-na.ssl-images-amazon.com/captcha') > -1:
            print('>> Error block - captcha - ')
            print('>> C04 blocked (captcha) ')
            return "C04"  # blocked
        if countryKbn == "UK" or countryKbn == "DE" or countryKbn == "FR":
            print('>> C5 blocked ')
            return "C05"  # blocked
        else:
            print('>> D02 No Title ')
            return "D02"  # blocked

    deliver_post = ""
    try:
        # deliver_post = in_drive.find_element_by_id('glow-ingress-line2').text
        deliver_post = in_drive.find_element(By.ID,'glow-ingress-line2').text
    except Exception as ex:
        print('>> error : ', ex)
        return "C01"
    else:
        deliver_post = str(deliver_post).replace('\u200c','')

    ######################## goods check ########################
    print('>> goods check ######################## ')
    if str(result).find('id="dp-container"') > -1:
        if str(result).find('id="rhf-container"') > -1:
            detail_soup = getparse(str(result), 'id="dp-container"', 'id="rhf-container"')
        else:
            detail_soup = getparse(str(result), 'id="dp-container"', '')
    else:
        if str(result).find('id="rhf-container"') > -1:
            detail_soup = getparse(str(result), '', 'id="rhf-container"')
        else:
            detail_soup = str(result)
    time.sleep(0.5)

    ##### Buy used check #####
    chk_soup = getparse(str(detail_soup), 'div id="usedBuySection"', '<div class="a-button-stack">')
    if str(chk_soup).find('Buy used:') > -1:
        print('>> Buy used (1)')
        return "D04"
    elif str(chk_soup).find('Used - Good') > -1:
        print('>> Used - Good (1)')
        return "D04"
    elif str(chk_soup).find('Buy pre-owned:') > -1:
        print('>> Buy pre-owned (1)')
        return "D04"
    elif str(chk_soup).find('Pre-owned:') > -1:
        print('>> Pre-owned (1)')
        return "D04"
    else:
        print('>> Buy used check ok')

    ##### Customisable check #####
    if str(result).find(' <div id="gestalt-buybox"') > -1:
        print('>> (Customisable) Unsellable product ')
        return "D120"

    ##### Pre-order #####
    # strPreorder = getparse(str(detail_soup), 'id="buy-now-button"', '<div class="a-button-stack">')
    # if str(strPreorder).find('Pre-order') > -1:
    #     print('>> Pre-order (1)')
    #     return "D10"  # Pre-order

    # ##### add-on Item  #####
    # strAddon = getparse(str(detail_soup), '<div class="a-box-group">', "</div>")
    # if str(strAddon).find('Add-on Item') > -1:
    #     print('>> add-on Item (1)')

    priceSource = getparse(str(detail_soup), 'id="productTitle"', 'id="featurebullets_feature_div"')
    if priceSource.find('Currently unavailable.') > -1:
        if priceSource.find('when or if this item will be back in stock.') > -1:
            print('>> Currently unavailable. : ' + str(asin))
            print('>> Sold Out')
            return "D01"

    ##### pantry #####
    if priceSource.find('class="pantry-store-info-inner"') > -1:
        print('>> pantry-store unavailable. : ' + str(asin))
        print('>> pantry goods')
        return "D13"  # pantry goods

    # goods_price = soldout_check_2(str(detail_soup),countryKbn)
    # if countryKbn == "DE" and str(goods_price) == "-1":
    # ##########################################################################
    #     print('>> USD설정 안되었음. Exit ')
    #     procLogSet(db_con, in_pg, "[" + str(asin) + "] USD설정 안되었음 exit : " + str(goods_price))
    #     procEnd(db_con, in_drive, in_pg)
    # ##########################################################################

    return "0"


def procDeliverChk(in_drive):

    ############ Deliver to Check #############################
    deliver_post = ""
    try:
        # deliver_post = in_drive.find_element_by_id('glow-ingress-line2').text
        deliver_post = in_drive.find_element(By.ID, 'glow-ingress-line2').text
    except Exception as ex:
        print('error : ', ex)
        return "1"
    else:
        deliver_post = str(deliver_post).strip()
        #print("deliver_post : " + str(deliver_post))

    if deliver_post == "":
        print('deliver_post : not check ')
        return "1"

    return deliver_post


def procDelivertoSet(in_drive, nFlg, cPost):
    time.sleep(1)
    nFlg = str(nFlg).upper()
    try:
        # in_drive.find_element_by_id('glow-ingress-line2').click()
        in_drive.find_element(By.ID, 'glow-ingress-line2').click()
    except Exception as ex:
        print('>> Error : ', ex)
        return "1"
    else:
        if nFlg == "USA" or nFlg == "MALL" or nFlg == "US" or nFlg == "DE" or nFlg == "UK" or nFlg == "FR":
            time.sleep(1)
            devSour = in_drive.page_source
            devSourCut = getparse(str(devSour),'id="glow-ingress-line1">','</span>')
            time.sleep(1)
            if devSourCut.find("Deliver to") > -1:
                # tmpChange = getparse(str(devSour),'id="GLOWFeature_AddressList">','class="a-popover-footer">')
                # if tmpChange.find('id="GLUXChangePostalCodeLink"') > -1:
                #     in_drive.find_element(By.XPATH,'//*[@id="GLUXChangePostalCodeLink"]').click()
                #     print(">> change click ")
                # time.sleep(3)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys(Keys.CONTROL + "a")
                time.sleep(1)
                in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys(Keys.DELETE)
                time.sleep(2)

            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys(cPost)
            time.sleep(1)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input').click()
            time.sleep(2)
            #in_drive.find_element(By.XPATH,'//*[@id="a-autoid-1-announce"]').click()
            #time.sleep(3)

        elif nFlg == "JP" or nFlg == "BEST" or nFlg == "GLOBAL":
            time.sleep(3)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput_0"]').send_keys('542')
            time.sleep(1)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput_1"]').send_keys('0012')
            time.sleep(1)
            in_drive.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input').click()
            time.sleep(3)

        time.sleep(2)
        devSourF = in_drive.page_source
        time.sleep(1)
        if devSourF.find("Continue") > -1:
            time.sleep(1)
            try:
                if devSourF.find('name="glowDoneButton"') > -1:
                    in_drive.find_element(By.XPATH,'//*[@id="a-autoid-7-announce"]').click()
                else:
                    # in_drive.find_element(By.XPATH,'//*[@id="GLUXConfirmClose"]').click()
                    in_drive.find_element(By.XPATH,'//*[@id="a-popover-1"]/div/div[2]/span').click()
            except Exception as ex:
                print('error : ', ex)
            else:
                time.sleep(3)
            print('>> procDelivertoSet OK ')
        elif devSourF.find("Done") > -1:
            time.sleep(1)
            try:
                if devSourF.find('name="glowDoneButton"') > -1:
                    in_drive.find_element(By.NAME, 'glowDoneButton').click()
                else:
                    # in_drive.find_element(By.XPATH,'//*[@id="GLUXConfirmClose"]').click()
                    in_drive.find_element(By.XPATH,'//*[@id="a-popover-2"]/div/div[2]/span').click()
            except Exception as ex:
                print('error : ', ex)
            else:
                time.sleep(3)
            print('>> procDelivertoSet OK ')
    return "0"


def get_asinset(in_catecode,db_con, in_pgsite):
    asinset = []

    #sql = "select top 100 asin,price from T_Category_BestAsin where cate_idx = '{0}' order by newid()".format(in_catecode)
    #sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsin_fr as a left join t_goods as t on t.display_ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
    if in_pgsite == "fr":
        #sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsin_fr as a left join t_goods as t on t.display_ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
        sql = "select top 100 a.asin, a.price, t.Uid from T_Category_BestAsin_fr as a left join ( select uid, cate_idx, display_ali_no from t_goods where cate_idx = '" +str(in_catecode)+ "' ) as t on t.display_ali_no = a.asin where a.cate_idx = '" +str(in_catecode)+ "' "
    else:
        #sql = "select top 100 asin, a.price, t.Uid from T_Category_BestAsin as a left join t_goods as t on t.display_ali_no = a.asin where a.cate_idx = '{0}' order by newid()".format(in_catecode)
        sql = "select top 100 a.asin, a.price, t.Uid from T_Category_BestAsin as a left join ( select uid, cate_idx, display_ali_no from t_goods where cate_idx = '" +str(in_catecode)+ "' ) as t on t.display_ali_no = a.asin where a.cate_idx = '" +str(in_catecode)+ "' "        
    rs_row = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rs_row:
        print('>> category complete! change catecode :' +str(in_catecode))

        where_condition = " catecode = '{0}'".format(in_catecode)
        db_con.delete('update_list2', where_condition)
        return 0

    for ea_asin in rs_row:
        asin = ea_asin[0]
        price = ea_asin[1]
        Duid = ea_asin[2]
        if (Duid is None) or (Duid == '') or Duid == "None":
            Duid = ''
        if (price is None) or (price == ''):
            price = 'null'
        #asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(price))
        asinset.append(str(asin) + '@' + str(in_catecode) + '@' + str(price) + '@' + str(Duid))
    return asinset


def getMemo(in_code):
    in_code_no = ""
    in_code_no = str(in_code[:3])
    rtnMemo = ""
    if in_code_no == "D01":
        rtnMemo = str(in_code) + ' : (Sold Out) Unsellable product'
    elif in_code_no == "D31":
        rtnMemo = str(in_code) + ' : (Sold Out) no price product'
    elif in_code_no == "D02":
        rtnMemo = str(in_code) + ' : (No Title) nsellable product'
    elif in_code_no == "D22":
        rtnMemo = str(in_code) + ' : (Fobidden) Medical product'
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
        rtnMemo = str(in_code) + ' : (option) Internal Server Error'
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
        rtnMemo = str(in_code) + ' : (Customisable) Unsellable product'
    elif in_code_no == "C01":
        rtnMemo = str(in_code) + ' : (Connection aborted(goods)) Url Connect Error'
    elif in_code_no == "C02":
        rtnMemo = str(in_code) + ' : (Connection aborted(option)) Url Connect Error'
    elif in_code_no == "C03":
        rtnMemo = str(in_code) + ' : (Connection aborted(option)2) Connect Error'
    elif in_code_no == "C04":
        rtnMemo = str(in_code) + ' : blocked (captcha) Url blocked '
    elif in_code_no == "C05":
        rtnMemo = str(in_code) + ' : blocked  Url blocked '
    elif in_code_no == "C06":
        rtnMemo = str(in_code) + ' : Deliver to check '
    elif in_code_no == "C07":
        rtnMemo = str(in_code) + ' : (Title cannot be translated) Japanese included'
    elif in_code_no == "C08":
        rtnMemo = str(in_code) + ' : (translated) translation delay '         
    elif in_code_no == "B01":
        rtnMemo = str(in_code) + ' : See All Buying Options '      
    elif in_code_no == "E01":
        rtnMemo = str(in_code) + ' : error check '
    elif in_code_no == "E02":
        rtnMemo = str(in_code) + ' : margin set error '
    elif in_code_no == "S01":
        rtnMemo = str(in_code) + ' : update stop goods (SKIP)'
    elif in_code_no == "S02":
        rtnMemo = str(in_code) + ' : naver noclick goods (SKIP)'
    elif in_code_no == "S03":
        rtnMemo = str(in_code) + ' : Delete after regeneration goods (SKIP)'
    elif in_code_no == "S04":
        rtnMemo = str(in_code) + ' : uk or fr already exists asin (SKIP)'
    elif in_code_no == "Q01":
        rtnMemo = str(in_code) + ' : setDB (Insert error)'
    elif in_code_no == "Q02":
        rtnMemo = str(in_code) + ' : setDB (Update error)'
    elif in_code_no == "B01":
        rtnMemo = str(in_code) + ' : See All Buying Options '

    return rtnMemo

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

# def connectDriver2(tool):
#     global set_browser

#     if tool == 'chrome':
#         chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#         driver_path = f'./{chrome_ver}/chromedriver.exe'
#         if os.path.exists(driver_path):
#             print(f"chrom driver is insatlled: {driver_path}")
#         else:
#             print(f"install the chrome driver(ver: {chrome_ver})")
#             chromedriver_autoinstaller.install(True)
#         time.sleep(1)
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)        
#         options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         options.add_argument("--disable-gpu")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
#                 random.random()) + " Safari/537.36, 'Referer':'https://www.amazon.co.uk'")
#         browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

#     return browser

# def connectDriver(tool, pgSite):
#     global set_browser

#     if tool == 'chrome':
#         chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#         driver_path = f'./{chrome_ver}/chromedriver.exe'
#         if os.path.exists(driver_path):
#             print(f"chrom driver is insatlled: {driver_path}")
#         else:
#             print(f"install the chrome driver(ver: {chrome_ver})")
#             chromedriver_autoinstaller.install(True)
#         time.sleep(1)
#         #path = "C:\\project\\chromedriver.exe"
#         username = os.getenv("USERNAME")
#         #c:\Users\allin\AppData\Local\Google\Chrome\User Data\Default
#         userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         options.add_argument("--disable-gpu")
#         #options.add_argument("--proxy-server=socks5://127.0.0.1:9150") # tor browser
#         options.add_argument("--proxy-server=socks5://127.0.0.1:9050") # tor service
#         options.add_argument("user-data-dir={}".format(userProfile))
#         #options.add_argument("--user-data-dir=chrome-data")

#         contrySite = getCountryInfo(pgSite,"3")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
#                 random.random()) + " Safari/537.36, 'Referer': 'https://" + str(contrySite) + "'")
#         browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

#     elif tool == 'brave':
#         path = "C:\\Project\\chromedriver.exe"
#         username = os.getenv("USERNAME")
#         userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
#         options = webdriver.ChromeOptions()
#         brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#         #options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-features=VizDisplayCompositor")
#         #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
#         options.add_argument("user-data-dir={}".format(userProfile))
#         options.binary_location = brave_path
#         browser = webdriver.Chrome(executable_path=path, chrome_options=options)

#     elif tool == 'Firefox':

#         path = "C:\Project\cgeckodriver.exe"
#         profile = webdriver.FirefoxProfile()
#         profile.set_preference('network.proxy.type', 1)
#         profile.set_preference('network.proxy.socks', '127.0.0.1')
#         profile.set_preference('network.proxy.socks_port', 9150)
#         profile.update_preferences()
#         browser = webdriver.Firefox(profile, executable_path=path)

#     return browser

def version_check(db_con, in_drive, in_ver, in_pgFilename, in_pgKbn, in_pgsite):

    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")
    if in_pgsite == "fr":
        sql = "select version,url from python_version_manage_fr where name = '" +str(in_pgKbn)+ "'"
    else:
        sql = "select version,url from python_version_manage where name = '" +str(in_pgKbn)+ "'"
    print(">> sql:" + sql)

    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        print(">> (DB) version :" +str(version))

        if str(in_ver) != str(version):
            db_con.close()           
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


def version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn, pgSite):

    print(">> version : " + in_ver)
    file_path = r"c:/project/"
    new_filename = file_path + in_pgFilename
    old_filename = file_path + in_pgFilename.replace("new_","")

    if pgSite == "fr":
        sql = "select version,url from python_version_manage_fr where name = '" +str(in_pgKbn)+ "'"
    else:
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

def procWork(db_con, in_drive, in_pg, in_ip):

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


def newlist(db_con, in_drive, in_pg, in_ip, in_pgsite):

    cateidx = ""
    sql = "select * from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    #print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        # sql = "select top 1 cate_idx from T_Category_BestAsin as a inner join t_category as c on c.CateCode = a.cate_idx where c.sale_ck_new = '1' and cate_idx not in (select catecode from update_list2) order by a.up_date"
        if in_pgsite == "fr":
            sql = "select cate_idx from (select top 1 cate_idx from T_Category_BestAsin_fr where cate_idx not in (select catecode from update_list2) order by up_date) as cc group by cate_idx"
        else:
            sql = "select cate_idx from (select top 1 cate_idx from T_Category_BestAsin where cate_idx not in (select catecode from update_list2) order by up_date) as cc group by cate_idx"
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> Error : '+str(e))
                # proc end
                procEnd(db_con, in_drive,in_pg)

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


def get_update_goods(in_site, db_FS, db_con):
    chk_data = "0"
    asinset = []
    tmp_guid = ""

    sql = " select top 100  guid, sitecate,  display_ali_no, regdate, upddate, flg_chk "
    sql = sql + " from amazon_goods_update "
    sql = sql + " where flg_chk ='0' and sitecate = '" + str(in_site) + "'"
    sql = sql + " order by RegDate asc "

    rs_row = db_FS.select(sql)
    #print('>> ##select all## sql :' + str(sql))

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
        sql = "select top 25 display_ali_no, price, cate_idx, uid from t_goods where uid in " + str(tmp_guid) 
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
                if (uid is None) or (uid == '') or uid == "None":
                    uid = ''                
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cate_idx) + '@' + str(price) + '@' + str(uid))

        if chk_data == "0":
            return ""

    return asinset


def endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt):
    if rtnChk_no[:1] == "C":
        if in_pgsite != "uk" :
            set_new_tor_ip()
            checkCurrIP()
        time.sleep(2)
        if c_Errcnt > 4:
            print('>> ( c_Errcnt 5 over ) exit :' + str(asin_low))
            procLogSet(db_con, in_pg, " ( c_Errcnt 7 over ) exit : " + str(asin_low))
            #procEnd(db_con, in_drive, in_pg)
            return "E99"

    if rtnChk_no == "D17":
        if d17_Errcnt % 2 == 0:
            if in_pgsite != "uk" :
                set_new_tor_ip()
                checkCurrIP()
        time.sleep(2)
        if d17_Errcnt > 7:
            print('>> ( d17_Errcnt 7 over ) exit :' + str(asin_low))
            procLogSet(db_con, in_pg, " ( d17_Errcnt 7 over ) exit : " + str(asin_low))
            #procEnd(db_con, in_drive, in_pg)
            return "E99"

    if rtnChk_no == "D07":
        if in_pgsite != "uk" :
            set_new_tor_ip()
            checkCurrIP_new()
            time.sleep(2)
            # set_new_tor_ip()
            # checkCurrIP_new()
            # time.sleep(2)  
            # set_new_tor_ip()
            # checkCurrIP_new()
            # time.sleep(2)
        time.sleep(1)
        if d07_Errcnt > 7:
            print('>> ( D07_Errcnt 7 over ) exit :' + str(asin_low))
            procLogSet(db_con, in_pg, " ( D07_Errcnt 7 over ) exit : " + str(asin_low))
            #procEnd(db_con, in_drive, in_pg)
            return "E99"

def D03_proc(db_con, Duid, D_naver_in, D_goodscode, flg):

    
    if flg == "goods":
        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1' where uid = {0}".format(Duid)
        db_con.execute(sql_u1)

    elif flg == "updatelist" or flg == "stock_multi":
        sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1', NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(
            Duid)
        db_con.execute(sql_u1)

    sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
    db_con.execute(sql_u2)    
    print(">> 금지어 처리 : {}".format(D_goodscode))

    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
    if str(D_naver_in) == "1":
        proc_ep_insert(D_goodscode,'D')

def sold_proc(db_con, Duid, D_naver_in, D_goodscode, flg):
    sql = ""
    if flg == "goods":
        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate() where uid='{0}'".format(Duid)
        print(">> sql : " + str(sql))
        db_con.execute(sql)

    elif flg == "stock_out":
        sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
        print(">> sql : " + str(sql))
        db_con.execute(sql)

    elif flg == "updatelist" or flg == "stock_multi":     
        sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
        print(">> sql : " + str(sql))
        db_con.execute(sql)

    print(">> sql : " + str(sql))
    print(">> [ {} ] 품절 처리 : {}".format(flg, D_goodscode))

    # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
    if str(D_naver_in) == "1":
        proc_ep_insert(D_goodscode,'D')
        print(">> (네이버 노출) ep_proc_amazon 테이블에 (mode : D) : {}".format(flg, D_goodscode))

def stock_proc(db_con, Duid, D_naver_in, D_goodscode, flg):

    if flg == "stock_ck_2": # 아마존 노출중
        sql = "update T_goods set stock_ck = '2' where uid='{0}'".format(Duid)
        print(">> (OK) stock_ck = 2  : " + str(D_goodscode))
        db_con.execute(sql)

    elif flg == "stock_ck_4": # (B01) See All Buying Options
        sql = "update T_goods set stock_ck = '4' where uid='{0}'".format(Duid)
        print(">> stock_ck = 4  : " + str(D_goodscode))
        db_con.execute(sql)

    elif flg == "stock_ck_0": # set_stock_out ---> 정상및 품절이외 기타 
        sql = "update T_goods set stock_ck = '0' where uid='{0}'".format(Duid)
        print(">> stock_ck = 0  : " + str(D_goodscode))
        db_con.execute(sql)

    elif flg == "stock_ck_1": # connet error 나중에 새로 업데이트할 대상
        sql = "update T_goods set stock_ck = '1', UpdateDate = UpdateDate - 3 where uid='{0}'".format(Duid)
        print(">> stock_ck = 1  : " + str(D_goodscode))
        db_con.execute(sql)

    elif flg == "stock_ck_null": # 정상 Update data
        sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate(), stock_ck_cnt = '0' where uid='{0}'".format(Duid)
        print(">> stock_ck = null  : " + str(D_goodscode))
        db_con.execute(sql)

    elif flg == "updatelist" or flg == "stock_multi":
        sql = "update T_goods set UpdateDate = getdate(), stock_ck = '1', stock_ck_date=getdate(), stock_ck_cnt = stock_ck_cnt + 1 where uid='{0}'".format(Duid)
        print(">> (updatelist) sql : " + str(sql))
        print(">> stock_ck = 1 stock_ck_cnt + 1 : " + str(D_goodscode))
        db_con.execute(sql)

    print(">> [ {} ] stock_ck 처리 : {}".format(flg, D_goodscode))


# Goods ###################################################################################
def set_multi(in_drive, in_ver, db_con, db_price, manage_dic):
###########################################################################################
    print('>> set_multi ')
    global cnt_title_tran
    cnt_title_tran = 0
    rtn_end = ""
    allCnt = 0
    c_Errcnt = 0
    cateidx = ""
    in_pg = manage_dic['py_pgName']
    in_pgFilename = manage_dic['py_pgFilename']
    in_pgKbn = manage_dic['py_pgKbn']
    in_pgsite = manage_dic['py_pgSite']
    in_tor = manage_dic['py_tor']

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, in_drive, in_ver, in_pgFilename, in_pgKbn, in_pgsite)

    # category get
    if in_tor == "Y": # 토루 사용
        cateidx = newlist(db_con, in_drive, in_pg, ip, in_pgsite)
    elif in_tor == "V": # vpn 사용
        cateidx = newlist(db_con, in_drive, in_pg, mac_addr(), in_pgsite)
    else:
        cateidx = newlist(db_con, in_drive, in_pg, ip, in_pgsite)
    print('>> newlist() catecode :' + str(cateidx))

    if cateidx == "":
        print('>> catecode parsing complete : ' + str(cateidx))
        return "0"

    # asin get
    get_asin_list = []
    get_asin_list = get_asinset(cateidx, db_con, in_pgsite)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(cateidx))
        return "1"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    print('>> (get_asin_list) len :' + str(cnt_asinlist))
    mac_address = mac_addr()
    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt % 5 == 0:
            if in_tor == "Y": # 토루 사용
                procWork(db_con, in_drive, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP()
                time.sleep(2)
            elif in_tor == "V": # vpn 사용
                procWork(db_con, in_drive, in_pg, mac_address)
                time.sleep(4)
            else:
                procWork(db_con, in_drive, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP()
                time.sleep(2)

        if allCnt % 20 == 0:
            in_drive.get_screenshot_as_file('C:\\project\\log\\set_multi_' +str(allCnt)+ '.png')

        print('\n\n')
        print('>> version : '+str(in_ver))
        # checkIP()
        # print(">> mac_address : {}".format(mac_address))
        print('>> ----------------- < set_multi [' + str(allCnt) + ' ] >  catecode : ' + str(cateidx) + ' | ' + str(asin_low) + ' -------------------------------------')
        time.sleep(random.uniform(0.5,1))
        rtnChk = proc_asin_parse_brower(asin_low, db_con, db_price, in_drive, in_pg, in_pgsite, manage_dic)  
        print('>> [ rtnChk ] : ' + str(rtnChk))

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = spm_asin[3]
        rtnChk_no = str(rtnChk[:3])
        print(getMemo(rtnChk))

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            if rtnChk_no != "D17": d17_Errcnt = 0
            elif rtnChk_no == "D17": d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1 # Connection Error 
        elif rtnChk_no == "C04" or rtnChk_no == "C05": c_Errcnt = c_Errcnt + 1 # blocked          
        elif rtnChk_no == "0":
            print('>> # SetDB OK (완료) : ' + str(rtnChk))
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0

        dic_b = dict()
        dic_b['asin'] = "'" + rtn_asin + "'"
        dic_b['cate_idx'] = cateidx
        dic_b['memo'] = "'" + getMemo(rtnChk) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "

        # checkIP()
        # print(">> mac_address : {}".format(mac_address))
        if rtnChk != "0":  
            if rtnChk_no[:1] == "D":
                D_naver_in = ""
                D_goodscode = ""
                if ( str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None" ) and (in_pgsite == "fr" or in_pgsite == "uk"):
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, isnull(stock_ck_cnt,0), isnull(order_ck, 0) from T_goods where display_ali_no = '{}' and site_kbn = '{}'".format(rtn_asin, in_pgsite)
                elif str(rtn_uid) == '' or rtn_uid is None or rtn_uid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, isnull(stock_ck_cnt,0), isnull(order_ck, 0) from T_goods where display_ali_no = '{0}'".format(rtn_asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, isnull(stock_ck_cnt,0), isnull(order_ck, 0) from T_goods where uid = '{0}'".format(rtn_uid)                    
                # print(">> sql : {}".format(sql))
                try:
                    rs = db_con.selectone(sql)
                except Exception as e:
                    print('>> exception 1-1 (sql) : {}'.format(sql))
                    checkIP()
                    print(">> mac_address : {}".format(mac_address))
                    time.sleep(10)
                    # procLogSet(db_con, in_pg, " ( exception 1-1  ) exit - rtn_asin: " + str(rtn_asin) + " | checkIP : " + str(checkIP()))
                    # procEnd(db_con, in_drive,"")
                    rtn_end = "E99"

                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    D_naver_in = rs[5]
                    D_goodscode = rs[6]
                    D_stock_ck_cnt = rs[7]
                    D_order_ck = rs[8]
                    print(">> [{}] isDisplay : {} | naver_in : {} ".format(D_goodscode, DIsDisplay, D_naver_in))
                    # sold out
                    if DIsDisplay == 'T':
                        if rtnChk_no == "D03":  # 금지어 처리 : Forbidden 금지어일 경우 판매불가 상품처리
                            D03_proc(db_con,Duid, D_naver_in, D_goodscode, "goods")
                        elif rtnChk_no == "D07":
                            print(">> D07 - 품절처리안함 (Skip) ")
                            stock_proc(db_con, rtn_uid, D_naver_in, D_goodscode, "stock_ck_4")
                        elif (in_pgsite == "usa" or in_pgsite == "mall") and rtnChk_no == "D17" and int(D_order_ck) == 1:
                            print(">> D17 - 품절처리안함 (order_ck = 1) (Skip) ")
                            stock_proc(db_con, rtn_uid, D_naver_in, D_goodscode, "stock_multi")
                        elif (in_pgsite == "usa" or in_pgsite == "mall") and rtnChk_no == "D17" and int(D_stock_ck_cnt) < 2:
                            print(">> D17 - 품절처리안함 (Skip) stock_ck_cnt : {}".format(D_stock_ck_cnt))
                            stock_proc(db_con, rtn_uid, D_naver_in, D_goodscode, "stock_multi")
                        else:
                            sold_proc(db_con, Duid, D_naver_in, D_goodscode, "goods") # 품절처리 ( 68번 ep_proc_amazon 테이블에 Insert 처리)

            if in_pgsite == "fr":
                sql = "delete from T_Category_BestAsin_fr_del where asin ='{0}'".format(rtn_asin)
                db_con.execute(sql)
                db_con.insert('T_Category_BestAsin_fr_del', dic_b)  # insert
            else:
                sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(rtn_asin)
                db_con.execute(sql)
                db_con.insert('T_Category_BestAsin_del', dic_b)  # insert
            print('>> ##insert## : T_Category_BestAsin_del')

        if in_pgsite == "fr":
            sql = "delete from T_Category_BestAsin_fr where asin ='{0}'".format(rtn_asin)
        else:
            sql = "delete from T_Category_BestAsin where asin ='{0}'".format(rtn_asin)
        db_con.execute(sql)
        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D07) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        rtn_end = endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt)
        if rtn_end == "E99":
            return rtn_end

    return "0"


# stock_out ###################################################################################
def set_stock_out(db_con, db_price, in_drive, in_ver, manage_dic):
###########################################################################################
    print('>> set_stock_out ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    in_pg = manage_dic['py_pgName']
    in_pgFilename = manage_dic['py_pgFilename']
    in_pgKbn = manage_dic['py_pgKbn']
    in_pgsite = manage_dic['py_pgSite']
    in_sql1 = manage_dic['py_sql1']
    in_sql2 = manage_dic['py_sql2']
    in_sql3 = manage_dic['py_sql3']
    in_tor = manage_dic['py_tor']

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, in_drive, in_ver, in_pgFilename, in_pgKbn, in_pgsite)

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
    mac_address = mac_addr()
    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt % 10 == 0:
            if in_tor == "Y":
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP()  
            elif in_tor == "V":
                procStockWork(db_con, in_pg, mac_address)
            else:
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP() 
        time.sleep(1)

        print('\n\n')
        print('>> version : '+str(in_ver))
        checkIP()
        print(">> mac_address : {}".format(mac_address))
        print('>> ----------------- < (set_stock_out) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_out_brower(asin_low,db_con, db_price,in_drive,in_pg,in_pgsite, manage_dic)
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
        rtn_uid = spm_asin[3]
        rtnChk_no = str(rtnChk[:3])
        print(getMemo(rtnChk))

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            if rtnChk_no != "D17":
                d17_Errcnt = 0
            elif rtnChk_no == "D17": d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK (완료) : ' + str(rtnChk))

        checkIP()
        print(">> mac_address : {}".format(mac_address))
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0), isnull(stock_ck_cnt,0), isnull(order_ck, 0) from t_goods where uid = '" + str(rtn_uid) + "'"
        print(">> sql : {}".format(sql))
        rs_row = db_con.selectone(sql)
        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_naver_in = rs_row[8]
            d_stock_ck_cnt = rs_row[9]
            d_order_ck = rs_row[10]
            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1
            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    sold_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_out") # 품절처리 ( 68번 ep_proc_amazon 테이블에 Insert 처리)
            elif rtnChk_no == "0": # 정상상품 stock_ck : 2
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_2")
            elif rtnChk_no[:1] == "B":
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_4")
            else:  # blocked 상품 stock_ck : 0 
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_0")

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        rtn_end = endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt)
        if rtn_end == "E99":
            return rtn_end

    return "0"


# Stock ###################################################################################
def set_updatelist(db_FS, db_con, db_price, in_drive, in_ver, manage_dic):
###########################################################################################
    print('>> set_updatelist ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    in_pg = manage_dic['py_pgName']
    in_pgsite = manage_dic['py_pgSite']
    in_tor = manage_dic['py_tor']

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
    mac_address = mac_addr()
    for asin_low in get_asin_list2:
        tmp_msg = ""
        allCnt = allCnt + 1
        if allCnt == 1 or allCnt == 50:
            if in_tor == "Y":
                procStockWork(db_con, in_pg, ip)
            elif in_tor == "V":
                procStockWork(db_con, in_pg, mac_address)
            else:
                procStockWork(db_con, in_pg, ip)
            time.sleep(1)
        print('\n\n ----------------- < (stock check) set_updatelist [' + str(cnt_asinlist2) + ' / ' + str(allCnt) + '] >  | ' + str(asin_low) + ' -------------------------------------')
        checkIP()
        print(">> mac_address : {}".format(mac_address))
        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_price,in_drive,in_pg, in_pgsite, manage_dic)
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
        print(getMemo(rtnChk))

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            if rtnChk_no != "D17": d17_Errcnt = 0
            elif rtnChk_no == "D17": d017_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK : ' + str(rtnChk))

        checkIP()
        print(">> mac_address : {}".format(mac_address))
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        print(">> sql : {}".format(sql))
        rs_row = db_con.selectone(sql)
        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_stock_ck = rs_row[5]
            d_naver_in = rs_row[8]	
            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1
            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        D03_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "updatelist")
                    else:
                        sold_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "updatelist") # 품절처리 ( 68번 ep_proc_amazon 테이블에 Insert 처리)
                if str(d_stock_ck) != '9':
                    stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "updatelist")

            elif rtnChk_no == "0":
                # ep 반영될수 있도록 update_price = '1' 추가
                sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date = getdate(), stock_ck_cnt = '0', update_price = '1' where uid='{0}'".format(rtn_uid)
                print(">> ep 반영될수 있도록 update_price = '1' 추가 sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))
                db_con.execute(sql)
                if str(d_naver_in) == "1":
                    sql_ch = " select * from naver_del where goodscode = '{}'".format(d_GoodsCode)
                    row_ch = db_FS.selectone(sql_ch)
                    if not row_ch:
                        sql_i = "insert into naver_del (goodscode,deldate,ep_mode) values ('{}',getdate(),'U')".format(d_GoodsCode)
                        print(">> ep 반영될수 있도록 naver_del 추가 : ".format(sql_i))
                        db_FS.execute(sql_i)

            # blocked 경우 amazon_goods_update 테이블 regdate + 1 다음에 다시 시도
            if rtnChk_no[:1] == "C" or rtnChk_no[:1] == "Q" or rtnChk_no[:1] == "E":
                sql = "update amazon_goods_update set flg_chk = '0', regdate = regdate + 1 where guid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)
            elif rtnChk_no == "0" or rtnChk_no[:1] == "D" or rtnChk_no[:1] == "S":
                sql = "update amazon_goods_update set flg_chk = '1', upddate = getdate() where guid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> amazon_goods_update  : " + str(rtn_uid))
                db_FS.execute(sql)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        rtn_end = endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt)
        if rtn_end == "E99":
            return rtn_end
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
            if (uid is None) or (uid == '') or uid == "None":
                uid = ''
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
                if (uid is None) or (uid == '') or uid == "None":
                    uid = ''
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
                if (uid is None) or (uid == '') or uid == "None":
                    uid = ''
                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if chk_data == "0":
        return ""

    return asinset

# Stock ###################################################################################
def set_stock_multi(db_con, db_price, in_drive, in_ver, manage_dic):
###########################################################################################
    print('>> set_stock_multi ')
    global cnt_title_tran
    cnt_title_tran = 0
    allCnt = 0
    c_Errcnt = 0
    in_pg = manage_dic['py_pgName']
    in_pgFilename = manage_dic['py_pgFilename']
    in_pgKbn = manage_dic['py_pgKbn']
    in_pgsite = manage_dic['py_pgSite']
    in_sql1 = manage_dic['py_sql1']
    in_sql2 = manage_dic['py_sql2']
    in_sql3 = manage_dic['py_sql3']
    in_tor = manage_dic['py_tor']

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, in_drive, in_ver, in_pgFilename, in_pgKbn, in_pgsite)

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
    mac_address = mac_addr()
    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt % 5 == 0:
            if in_tor == "Y":
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP()  
            elif in_tor == "Y":
                procStockWork(db_con, in_pg, mac_address)
            else:
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP()  
        time.sleep(1)

        print('\n\n')
        print('>> version : '+str(in_ver))
        checkIP()
        print(">> mac_address : {}".format(mac_address))
        print('>> ----------------- < (set_stock_multi) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_price,in_drive,in_pg,in_pgsite, manage_dic)
            print('>> [ rtnChk ] : ' + str(rtnChk))
        except Exception as ex:
            print('>> set_multi Exception Error : ' + str(ex))
            print('>> asin_low : ' + str(asin_low))
            if rtnChk == "": rtnChk = "E01"
        else:
            print('>> -- proc_asin_parse_brower (OK) -- ')

        spm_asin = asin_low.split('@')
        rtn_asin = spm_asin[0]
        rtn_uid = spm_asin[3]
        rtnChk_no = str(rtnChk[:3])
        print(getMemo(rtnChk))

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            if rtnChk_no != "D17": d17_Errcnt = 0
            elif rtnChk_no == "D17": d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK : ' + str(rtnChk))

        checkIP()
        print(">> mac_address : {}".format(mac_address))
        sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
        print(">> sql : {}".format(sql))
        rs_row = db_con.selectone(sql)
        d_naver_in = ""
        if not rs_row:
            print('>> No date Check please : ' + str(asin_low))
        else:
            d_stock_ck_cnt = rs_row[1]
            d_GoodsCode = rs_row[2]
            d_IsDisplay = rs_row[3]
            d_stock_ck = rs_row[5]
            d_naver_in = rs_row[8]	
            stock_cnt = 0
            if d_stock_ck_cnt != '':
                stock_cnt = int(d_stock_ck_cnt) + 1
            if rtnChk_no[:1] == "D":  # sold out
                if d_IsDisplay == 'T':
                    if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                        D03_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_multi")
                    elif rtnChk_no == "D07": 
                        stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_4")
                    else:
                        sold_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_multi")
                if str(d_stock_ck) != '9':
                    stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_multi")
            elif rtnChk_no == "0":
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_null")
            elif rtnChk_no[:1] == "B":
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_4")
            else:  # blocked
                stock_proc(db_con, rtn_uid, d_naver_in, d_GoodsCode, "stock_ck_1")

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        rtn_end = endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt)
        if rtn_end == "E99":
            return rtn_end
    return "0"


#### Old Goods #####################################################################################################################
def get_old_asin(db_con, in_sql1, in_sql2):
####################################################################################################################################
    asinset = []
    chk_data = "0"

    #RegDate 2019-01-01 이전 상품 삭제 
    #sql = "select top 25 display_ali_no, price, cate_idx, uid from t_goods where stop_update is null and UpdateDate is null and regdate <= CONVERT(varchar(10), getdate()-22, 120) "
    #sql = "select top 50 isnull(display_ali_no,ali_no), price, cate_idx, uid, isnull(Del_naver,'') from t_goods where regdate >= '" +str(gStartDate)+ "' and regdate < '" +str(gEndDate)+ "' and updatedate is null and del_naver is null and stop_update is null "
    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_asin in rs_row:
            d_Del_naver = ""
            asin = ea_asin[0]
            price = ea_asin[1]
            cateidx = ea_asin[2]
            uid = ea_asin[3]
            d_Del_naver = ea_asin[4]

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
                d_Del_naver = ""
                asin = ea_asin[0]
                price = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                d_Del_naver = ea_asin[4]

                if (price is None) or (price == ''):
                    price = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(price) + '@' + str(uid))

    if chk_data == "0":
        return ""

    return asinset

#### Old Goods #####################################################################################################################
def set_old_multi(db_con, db_price, in_drive, in_ver, manage_dic):
####################################################################################################################################
    print('>> PG set_old_multi ')
    in_pg = manage_dic['pgName']
    in_pgFilename = manage_dic['pgFilename']
    in_pgKbn = manage_dic['pgKbn']
    in_pgsite = manage_dic['pgSite']
    in_sql1 = manage_dic['sql']
    in_sql2 = manage_dic['sq2']
    in_tor = manage_dic['py_tor']

    print('>> PG Info : in_pg - {0} | in_pgFilename : {1} | in_pgKbn : {2} | in_pgsite : {3} '.format(in_pg,in_pgFilename,in_pgKbn,in_pgsite))
    allCnt = 0
    c_Errcnt = 0
    rtn_end = ""

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check(db_con, in_drive, in_ver, in_pgFilename, in_pgKbn, in_pgsite)
        #print(' version_check (Skip) ')

    # asin get
    get_asin_list = []
    get_asin_list = get_old_asin(db_con, in_sql1, in_sql2)
    print(get_asin_list)

    if str(get_asin_list).rfind('@') == -1:
        print('>> catecode parsing complete : ' + str(ip))
        return "1"

    c_Errcnt = 0
    d17_Errcnt = 0
    d07_Errcnt = 0
    cnt_asinlist = 0
    cnt_asinlist = len(get_asin_list)
    rtnChk = ""
    print('>> (get_asin_list) len :' + str(cnt_asinlist))

    for asin_low in get_asin_list:
        allCnt = allCnt + 1
        if allCnt % 5 == 0:
            if in_tor == "Y":
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP_new()
            elif in_tor == "V":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)
                set_new_tor_ip()
                checkCurrIP_new()
        time.sleep(1)

        print('\n\n')
        print('>> (Tor) version : '+str(in_ver))
        #print(checkIP())
        print('>> ----------------- < (set_old_multi) [' + str(cnt_asinlist) + ' / ' + str(allCnt) + '] >  | goodscode : ' + str(asin_low) + ' -------------------------------------')

        try:
            rtnChk = proc_asin_parse_brower(asin_low,db_con,db_price,in_drive,in_pg,in_pgsite)
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

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
            if rtnChk_no != "D17": d17_Errcnt = 0
            elif rtnChk_no == "D17": d17_Errcnt = d17_Errcnt + 1
            if rtnChk_no == "D07": d07_Errcnt = d07_Errcnt + 1
        elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06": c_Errcnt = c_Errcnt + 1
        elif rtnChk_no == "0":
            c_Errcnt = 0
            d17_Errcnt = 0
            d07_Errcnt = 0
            print('>> # SetDB OK : ' + str(rtnChk))

        if rtnChk_no == "0":
            sql = "update T_goods set UpdateDate = getdate(), stock_ck = null, stock_ck_date=getdate() where uid='{0}'".format(rtn_uid)
            print(">> sql : " + str(sql))
            print(">> Ok stock_ck update : " + str(spm_asin))
            db_con.execute(sql)
        else:  # delete 대상 
            sql = "select cate_idx, isnull(stock_ck_cnt,''), GoodsCode, IsDisplay, isnull(Del_Naver,''), regdate, UpdateDate, isnull(order_ck,'') from t_goods where uid = '" + str(rtn_uid) + "'"
            print('>> ##selectone## sql :' + str(sql))
            rs_row = db_con.selectone(sql)

            d_GoodsCode = ""
            if not rs_row:
                print('>> No date Check please : ' + str(asin_low))
                procLogSet(db_con, in_pg, "[" + str(rtn_asin) + "] No date Check  : " + str(rtn_uid))
            else:
                d_GoodsCode = rs_row[2]
                d_order_ck = rs_row[7]
                print('>> d_GoodsCode : '+str(d_GoodsCode))
                goodsUid = checkOrder(d_GoodsCode)
                print('>> goodsUid : '+str(goodsUid))

                if goodsUid == "E":
                    print('>> 주문내역 확인불가 (END) ')
                    procLogSet(db_con, in_pg, " 주문내역 확인불가 exit : " + str(asin_low))
                    #procEnd(db_con, in_drive, in_pg)
                    rtn_end = "E99"

                if goodsUid == "" or d_order_ck == "":
                    print(">> 상품 삭제 처리 : " +str(spm_asin))
                    ###################   상품 삭제   ###################    
                    setGoodsdelProc(db_con, rtn_uid, '', '')
                    ###################   상품 삭제   ###################  
                else:
                    ##### Log Insert ##############
                    print('>> Log Insert ')
                    procLogSet(db_con, in_pg, "[" + str(d_GoodsCode) + "] 주문이력 있음 (품절처리) : " + str(goodsUid))

                    print('>> 품절 상품처리 ')
                    sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate(), order_ck = '1' where uid = {0}".format(rtn_uid)
                    db_con.execute(sql_u1)

        print(">> Errcnt : {0} | Errcnt (D17) : {1} | Errcnt (D17) : {2} ".format(c_Errcnt, d17_Errcnt, d07_Errcnt))
        rtn_end = endProc(db_con, in_drive, rtnChk_no, in_pg, in_pgsite, asin_low, c_Errcnt, d17_Errcnt, d07_Errcnt)
        if rtn_end == "E99":
            return rtn_end
    return "0"

####################################################################################################################################


#### Old Goods #####################################################################################################################
def get_old_goodscode(db_con, in_sql1, in_sql2):
####################################################################################################################################
    goodscode_set = []
    chk_data = "0"

    # Del_naver = 1 or 9 상품 삭제 
    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_goodscode in rs_row:
            goodscode = ea_goodscode[0]
            uid = ea_goodscode[1]
            d_Del_naver = ea_goodscode[2]
            RegDate = ea_goodscode[3]
            UpdateDate = ea_goodscode[4]

            goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if in_sql2 != "":
        rs_row2 = db_con.select(in_sql2)
        print('>> ##select all## in_sql2 :' + str(in_sql2))

        if not rs_row2:
            print('>> (UpdateDate) Stock Check complete! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_goodscode in rs_row2:
                goodscode = ea_goodscode[0]
                uid = ea_goodscode[1]
                d_Del_naver = ea_goodscode[2]
                RegDate = ea_goodscode[3]
                UpdateDate = ea_goodscode[4]

                goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if chk_data == "0":
        return ""

    return goodscode_set

#### Old Goods delete ##############################################################################################################
def set_old_delete(db_con, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2, manage_dic):
####################################################################################################################################
    print('>> PG Info : in_pg - {0} | in_pgFilename : {1} | in_pgKbn : {2} | in_pgsite : {3} '.format(in_pg,in_pgFilename,in_pgKbn,in_pgsite))
    allCnt = 0
    c_Errcnt = 0
    in_tor = manage_dic['py_tor']

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn, in_pgsite)
        #print(' version_check (Skip) ')

    # asin get
    get_goods_list = []
    get_goods_list = get_old_goodscode(db_con, in_sql1, in_sql2)
    print(get_goods_list)

    if str(get_goods_list).rfind('@') == -1:
        print('>> parsing complete : ' + str(ip))
        return "1"

    rtnChk = ""
    print('>> (get_goods_list) len :' + str(len(get_goods_list)))
    print(str(datetime.datetime.now()))

    for goods_low in get_goods_list:
        tmp_msg = ""
        allCnt = allCnt + 1

        if allCnt == 1 or allCnt == 50:
            if in_tor == "Y":
                procStockWork(db_con, in_pg, ip)
            elif in_tor == "V":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)
            time.sleep(1)

        sp_goods = goods_low.split('@')
        d_goodscode = sp_goods[0]
        d_uid = sp_goods[1]
        d_Del_naver = sp_goods[2]
        d_RegDate = sp_goods[3]
        d_UpdateDate = sp_goods[4]

        print('>> (set_old_delete) goodscdoe : {} | uid : {} | Del_naver : {} | d_RegDate : {} | d_UpdateDate : {}'.format(d_goodscode,d_uid,d_Del_naver,d_RegDate,d_UpdateDate))

        time.sleep(1)
        rtnFlg = checkOrderHistory(d_goodscode)
        if rtnFlg == "":
            #setGoodsdelProc
            delFlg = setGoodsdelProc(db_con, d_uid, '', '')
            if delFlg == "0":
                print(">> 주문 내역 없음 삭제처리 OK : {}".format(d_goodscode))
        elif rtnFlg == "E":
            print(">> 주문 내역 확인 ERROR : {}".format(d_goodscode))
            return "E"
        else:
            print(">> 주문 내역 있음 : {}".format(d_goodscode))
            print('>> t_goods 테이블 : order_ck = 1 처리 : {}'.format(d_goodscode))
            uSql3 = " update t_goods set order_ck = '1' where uid = '{}'".format(d_uid)
            db_con.execute(uSql3)

            if d_Del_naver == '9':
                db_NC = DBmodule_AM.Database('navernoclick')

                sql = " select goodscode, del_flag from naver_noclick_goods_20210315 where goodscode = '{}'".format(d_goodscode)
                rs = db_NC.selectone(sql)
                if rs:
                    print('>> naver_noclick_goods_20210315 테이블 존재 : del_flag = null 처리 : {}'.format(d_goodscode))
                    uSql = " update naver_noclick_goods_20210315 set del_flag = null where goodscode = '{}'".format(d_goodscode)
                    db_NC.execute(uSql)
                else:
                    sql2 = " select goodscode, del_flag from naver_noclick_goods where goodscode = '{}'".format(d_goodscode)
                    rs2 = db_NC.selectone(sql2)
                    if rs2:
                        print('>> naver_noclick_goods 테이블 존재 : del_flag = null 처리 : {}'.format(d_goodscode))
                        uSql2 = " update naver_noclick_goods set del_flag = null where goodscode = '{}'".format(d_goodscode) 
                        db_NC.execute(uSql2)

                print('>> t_goods 테이블 : Del_naver = null / order_ck = 1 처리 : {}'.format(d_goodscode))
                uSql3 = " update t_goods set Del_naver = null, order_ck = '1' where uid = '{}'".format(d_uid)
                db_con.execute(uSql3) 

                db_NC.close()

    return "0"

def write_file(file_name, write_str):
    path_file = os.getcwd()
    #with open(path_file + "/" + str(file_name),"w",encoding="utf8") as f: 
    #    f.write(str(write_str))

def get_feature(in_soup):

    featureset = []
    feature_before_str = ""
    feature_before_tmp = ""
    if str(in_soup).find('Product Details </h3>') > -1: ## Product Details
        feature_before_str = getparse(str(in_soup), 'Product Details </h3>', '')
    elif str(in_soup).find('Product details</h3>') > -1:
        feature_before_str = getparse(str(in_soup), 'Product details</h3>', '')
    elif str(in_soup).find('Détails sur le produit</h2>') > -1:
        feature_before_str = getparse(str(in_soup), 'Détails sur le produit</h2>', '')
    elif str(in_soup).find('Product Details</h2>') > -1:
        feature_before_str = getparse(str(in_soup), 'Product Details</h2>', '')
    elif str(in_soup).find('About this Item </h3>') > -1:
        feature_before_str = getparse(str(in_soup), 'About this Item </h3>', '')
    elif str(in_soup).find('About this item </h3>') > -1:
        feature_before_str = getparse(str(in_soup), 'About this item </h3>', '')
    elif str(in_soup).find('À propos de cet article </h3>') > -1:
        feature_before_str = getparse(str(in_soup), ' À propos de cet article </h3>', '')
    elif str(in_soup).find('<span>About this item</span>') > -1:
        feature_before_str = getparse(str(in_soup), '<span>About this item</span>', '')
    elif str(in_soup).find('id="feature-bullets"') > -1:
        feature_before_str = getparse(str(in_soup), 'id="feature-bullets"', '')
    feature_before_tmp = feature_before_str

    if str(feature_before_str).find('<div id="feature-bullets"') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', '<div id="feature-bullets"')
    elif str(feature_before_str).find('class="product-facts-title"') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', 'class="product-facts-title"')
    elif str(feature_before_str).find('id="productFactsToggleButton"') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', 'id="productFactsToggleButton"')
    elif str(feature_before_str).find('id="edpIngress_feature_div"') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', 'id="edpIngress_feature_div"')
    elif str(feature_before_str).find('<hr aria-hidden') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', '<hr aria-hidden')
    elif str(feature_before_str).find('</ul>') > -1:
        feature_before_str =  getparse(str(feature_before_str), '', '</ul>')
    else:
        feature_before_str =  getparse(str(feature_before_str), '', '</div> </div>')

    if str(in_soup).find('"parentAsin" : "') == -1:
        print('>> no option goods : Product details (Add)')
        if str(feature_before_str).find('<span class="a-color-base a-text-bold">') > -1:
            feature_sp = feature_before_str.split('<span class="a-color-base a-text-bold">')
            flow_cnt = 1
            while flow_cnt < len(feature_sp):
                ea_item = getparse(feature_sp[flow_cnt], '', '</span>')
                ea_item_2 = getparse(feature_sp[flow_cnt], '<span class="a-color-secondary">', '</span>')
                featureset.append(ea_item + str(" : ") + ea_item_2)
                flow_cnt += 1 
        elif str(feature_before_str).find('<span class="a-size-small a-text-bold">') > -1:
            feature_sp = feature_before_str.split('<span class="a-size-small a-text-bold">')
            flow_cnt = 1
            while flow_cnt < len(feature_sp):
                ea_item = getparse(feature_sp[flow_cnt], '', '</span>')
                ea_item_2 = getparse(feature_sp[flow_cnt], '<span class="a-size-base a-color-tertiary">', '</span>')
                featureset.append(ea_item + str(" : ") + ea_item_2)
                flow_cnt += 1 
        ## write_file("ebay/tmp/feature_before.html", featureset)

    feature_str_tmp = ""
    if str(in_soup).find('id="feature-bullets"') > -1:
        feature_str = getparse(str(in_soup), 'id="feature-bullets"', '')
        if str(feature_str).find('Loading EDP related metadata') > -1:
            feature_str = getparse(str(feature_str), '','Loading EDP related metadata')
        elif str(feature_str).find('id="productFactsToggleButton"') > -1:
            feature_str = getparse(str(feature_str), '','id="productFactsToggleButton"')
        else:
            feature_str = getparse(str(feature_str), '','</ul>')
        feature_str_tmp = getparse(str(feature_str), '">', '')
    elif str(feature_before_tmp).find('class="product-facts-title">') > -1: ## About this Item
        if str(feature_before_tmp).find('class="product-facts-title"> Description') > -1: ## About this Item
            feature_str = getparse(str(feature_before_tmp), '', 'class="product-facts-title"> Description')
        else:
            feature_str = getparse(str(feature_before_tmp), '', 'class="product-facts-title">')

        if str(feature_str).find('Loading EDP related metadata') > -1:
            feature_str = getparse(str(feature_str), '','Loading EDP related metadata')
        elif str(feature_str).find('id="productFactsToggleButton"') > -1:
            feature_str = getparse(str(feature_str), '','id="productFactsToggleButton"')
        # else:
        #     feature_str = getparse(str(feature_str), '','</ul>')
        feature_str_tmp = getparse(str(feature_str), '">', '')
    else:
        feature_str = str(feature_before_str)
        feature_str_tmp = feature_str

    if str(feature_str_tmp).strip() != "":
        feature_str = getparse(str(feature_str), '<ul', '')
        if str(feature_str).find('<li') > -1:
            feature_items = feature_str.split('<li')
            flow = 1
            while flow < len(feature_items):
                ea_feature = getparse(feature_items[flow], '<span', '</span>')
                ea_feature = getparse(ea_feature, '>', '')
                if ea_feature != "":
                    if str(ea_feature).find(' class=') == -1:
                        featureset.append(ea_feature)
                flow += 1

    ## write_file("ebay/tmp/feature.html", featureset)

    return featureset