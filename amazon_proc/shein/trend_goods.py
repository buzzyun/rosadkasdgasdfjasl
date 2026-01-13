# 공통된 코드 : goods_relation_id
# 상품옵션 여러개 : https://asia.shein.com/DAZY-Mock-Neck-Split-Hem-Tee-Without-Bra-p-13527921-cat-1738.html
# 단순옵션 여러개(ex 사이즈) : https://asia.shein.com/DAZY-Colorblock-Half-Zip-Crop-Tee-p-11892250-cat-1738.html
# 옵션 없음 : https://asia.shein.com/144pcs-Long-Coffin-Fake-Nail-p-10877746-cat-1869.html
# 색상 옵션만 있음 : https://asia.shein.com/Studded-Decor-Clear-Acrylic-Frame-Fashion-Glasses-p-2184197-cat-1770.html
# 리뷰url:https://asia.shein.com/goods_detail_nsw/getCommentInfoByAbc?_ver=1.1.8&_lang=ko&spu=w22110115095&goods_id=&page=1&limit=3&offset=0&sort=&size=&is_picture=&rule_id=recsrch_sort:A&tag_id=&local_site_abt_flag=1&shop_id=&query_rank=1
# 상품 데이터 위치 - productIntroData 밑
# 상품 상세설명 - productIntroData > relation_color
# 모델 - productIntroData > model
# 상품 이미지 - productIntroData > goods_img
# 사이즈 정보 - productIntroData > sizeInfoDes
# 신체 사이즈 - productIntroData > sizeInfoDes > basicAttribute > base_code_info

import os
os.system('pip install --upgrade selenium')
from selenium import webdriver
import datetime
import threading
import multiprocessing
import chromedriver_autoinstaller
import requests
import json
import urllib
from operator import itemgetter
import re
import traceback
import get_asin_function
import socket
import random
import time
import sys,uuid
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import subprocess
import os
import DBmodule_NEW
import trend_func

global ver
ver = "1.57"
print(">> ver : {}".format(ver))
global sleep_num 
sleep_num = 2
global err_cnt

db_con = DBmodule_NEW.Database('trend',True)
db_ali = DBmodule_NEW.Database('aliexpress',False)
# ip = socket.gethostbyname(socket.gethostname())

sql_ali = "select * from ali_price_ck"
sql_ali2 = "select ban_title_gubun, ban_title_gubun_2, ban_title_inner, ban_check from Ban_Title"
sql_ali3 = "select * from Replace_Title"
sql_info = "select exchange, delivery_fee, coupon from goods_var"
info = db_con.selectone(sql_info)
delivery_fee = info[1]
exchange = info[0]
coupon = info[2]
ban_title_list = db_ali.select(sql_ali2)
ali_price_ck = db_ali.selectone(sql_ali)
replace_title_list = db_ali.select(sql_ali3)
db_ali.close()


def open_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    # chromedriver_version = "114.0.5735.16"
    chromedriver_version = "114.0.5735.90"
    options.add_argument('--disable-loging')
    options.add_argument(r'user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data\Profile1')
    options.add_argument("lang=ko_KR") # 한국어!
    options.add_argument("language=ko") # 한국어!     
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(executable_path='C:\\project\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver    

def open_driver2():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.add_argument(r'user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data\Profile1')
    options.add_argument("lang=ko_KR") # 한국어!     
    options.add_argument("language=ko") # 한국어!     
    prefs = {'profile.default_content_setting_values': {'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
    options.add_experimental_option('prefs', prefs)    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # service = Service(executable_path=chromedriver_autoinstaller.install(True))
    s = Service(ChromeDriverManager(version="114.0.5735.90").install())
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()

    return driver


def connectSubProcess(type):
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    proc_id = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc_id = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc_id = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    option.add_argument("--incognito") ## 시크릿 모드 추가
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    if type == "H":
        option.add_argument("--headless") # headless
    
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    print(f" >> driver_path: {driver_path}")
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)

    return browser, proc_id

# def connectSubProcess():
#     try:
#         shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
#     except FileNotFoundError:
#         pass

#     filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
#     filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'

#     proc = ""
#     try:
#         print(">> C:\Program Files (x86)\Google\Chrome ")
#         proc = subprocess.Popen(filePath_86)   # Open the debugger chrome
#     except FileNotFoundError:
#         print(">> C:\Program Files\Google\Chrome ")
#         proc = subprocess.Popen(filePath)

#     option = Options()
#     option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
#     driver_path = f'./{chrome_ver}/chromedriver.exe'
#     if os.path.exists(driver_path):
#         print(f"chrom driver is insatlled: {driver_path}")
#     else:
#         print(f"install the chrome driver(ver: {chrome_ver})")
#         chromedriver_autoinstaller.install(True)
#     browser = webdriver.Chrome(options=option)

#     return proc, browser 

def chrom_click(selector, driver):
    try:
        driver.find_element(By.CSS_SELECTOR,selector).click()
    except:
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,selector))
    time.sleep(1)

def changeLang(driver):
    print("한국어로 변경")
    time.sleep(1)
    try:
        chrom_click("i[class='iconfont icon-close she-close']", driver)
    except:
        print("팝업 없음")
    chrom_click("i[class='suiiconfont-critical sui_icon_nav_global_24px']", driver)
    chrom_click("a[data-lang='asiako']", driver) 

def korlen(str):    
    korP = re.compile('[\u3131-\u3163\uAC00-\uD7A3]+',re.U)    
    temp = re.findall(korP, str)    
    temp_len = 0    
    for item in temp:
        temp_len = temp_len + len(item)
    return len(str) + temp_len

def getUrlToJsonData(url):
    rs = requests.get(url)
    html = rs.text
    json_data = json.loads(html)

    return json_data

# 상품페이지 - json 데이터 들고오기
def getPrdData(html):
    start_index = html.find('"productIntroData":{')
    end_index = html.find(',"defaultMallCode"',start_index)
    if html.find(',"fixedRatio"',start_index) > -1:
        end_index = html.find(',"fixedRatio"',start_index)
    html = html[start_index+19:end_index].strip()
    json_data = json.loads(html)

    return json_data

# 상품페이지 - json 데이터에서 옵션url 가져오기
def getOtherOptionUrl(json,reverse=False):
    option_urls=[]
    dic = dict()
    option_url = makeSheinProdUrl(json["detail"]["goods_url_name"],json["detail"]["goods_id"],json["detail"]["cat_id"])
    price = json["getPrice"]["salePrice"]["amount"]
    dic["option_url"] = option_url
    dic["price"] = price
    option_urls.append(dic)
    for goods in json["relation_color"]:
        if goods["stock"]==0 or goods["stock"]=="0":
            continue
        dic = dict()
        option_url = makeSheinProdUrl(goods["goods_url_name"],goods["goods_id"],goods["cat_id"])
        price = goods["retailPrice"]["amount"]
        dic["option_url"] = option_url
        dic["price"] = price
        option_urls.append(dic)
    if reverse:
        option_urls = sorted(option_urls,key=itemgetter("price"),reverse=True)
    else:
        option_urls = sorted(option_urls,key=itemgetter("price"))
    return option_urls

# 상품페이지 - 상품 색 옵션 가져오기(t_goods_content용) //\xa0
def getColorOptionName(json):
    color_option = dict()
    color_option["name"] = json["detail"]["mainSaleAttribute"][0]["attr_name"]
    color_option["value"] = json["detail"]["mainSaleAttribute"][0]["attr_value"]

    return color_option

# 상품페이지 - 상품 이미지 들고오기(t_goods_option용)
def getProdImg(json):
    dic = dict()
    main_image = json["goods_imgs"]["main_image"]["origin_image"].replace("//","")
    main_image = main_image.replace("http:","")
    detail_images = json["goods_imgs"]["detail_image"]
    dic["main_image"] = main_image
    dic["detail_images"] = []
    if detail_images:
        for detail_image in detail_images:
            dic["detail_images"].append(detail_image["origin_image"].replace("//","").replace("http:",""))        

    return dic

# 상품페이지 - 모델 및 사이즈 정보 들고오기(t_goods_option용)
def getProdDetail(json):
    dic = dict()
    model = dict()
    size = dict()
    detail = []
    prod_size = dict()
    body_size = dict()

    model_data = json["model"]
    if len(model_data) > 0:
        model["model_image"] = model_data["image"]
        model["model_wear"] = model_data["size"]
        model["model_size"] = model_data["attrcm"]
    dic["model"] = model

    size_data = json["sizeInfoDes"]    
    if len(size_data) > 0:    
        if len(size_data["multiPartInfo"]) > 0:
            prod_size["multiPartInfo"] = size_data["multiPartInfo"]
        else:
            prod_size["size_info"] = size_data["sizeInfo"]
        prod_size["template"] = json["detail"]["sizeTemplate"]
        size["product"] = prod_size
        
        body_size["size_info"] = size_data["basicAttribute"]["base_code_info"]
        body_size["template"] = {"image_url":size_data["basicAttribute"]["image_url"],"description_multi":size_data["basicAttribute"]["attribute_info"]}    
        size["body"] = body_size

    dic["size"] = size

    for product_detail in json["detail"]["productDetails"]:
        temp = dict()
        temp["name"] = product_detail["attr_name"]
        temp["value"] = product_detail["attr_value"]
        detail.append(temp)

    dic["product_detail"] = detail

    return dic

# 상품페이지 - 상품 사이즈 옵션 가져오기(t_goods_option용)
def getSizeOption(json, price_Symbol):
    size_option = []
    goods_id = json["detail"]["goods_id"]
    # attrSizeList > sale_attr_list > 상품코드 > sku_list > 리스트 > sku_sale_attr > 리스트
    # attrSizeList > sale_attr_list > 상품코드 > sku_list > 리스트 > stock : 0 이면 해당 사이즈 품절
    option_list = json["attrSizeList"]["sale_attr_list"][str(goods_id)]["sku_list"]
    if len(option_list) > 1:
        for option in option_list:
            temp = dict()
            # if len(option["sku_sale_attr"]) > 1:
            #     size_option = "except"
            #     break
            stock = option["stock"]
            name = option["sku_sale_attr"][0]["attr_value_name"]
            price = option["price"]["retailPrice"]["amount"]
            if price_Symbol.find('$') == -1:
                print(">> price_Symbol : {}".format(price_Symbol))
                print(">> (before) price : {} | {}".format(price, price_Symbol))
                price = check_price(price, price_Symbol)
                print(">> (after) price : {} | {}".format(price, price_Symbol))

            if stock==0:
                continue
            temp["name"] = name
            temp["price"] = price
            size_option.append(temp)

    return size_option

# 상품페이지 - 상품 상세설명 들고오기
def getProdInfo(json):
    dic = dict()
    dic["goods_name"] = json["detail"]["goods_name"]
    dic["main_image"] = json["goods_imgs"]["main_image"]["origin_image"]
    return dic

# shein 상품페이지 url 생성
def makeSheinProdUrl(goods_url_name,goods_id,cat_id):
    url=""
    goods_url_name = goods_url_name.replace(" ", "-")
    if len(goods_url_name)==0:
        goods_url_name = "item"
    if goods_url_name[0]=="H":
        goods_url_name = goods_url_name[1:]
    if len(goods_url_name) > 100:
        goods_url_name = "item"
    # url = "https://asia.shein.com/" + goods_url_name.replace(" ", "-") + "-p-" + str(goods_id) + "-cat-" + str(cat_id) + ".html"
    url = "https://kr.shein.com/" + goods_url_name.replace(" ", "-") + "-p-" + str(goods_id) + "-cat-" + str(cat_id) + ".html"
    return url

# 이미지 포맷 변경
def changImgFormat(img_url,img_type):    
    if img_url.find(".jpg") > -1:
        ext = ".jpg"
        img_url.replace(ext,"")        
    elif img_url.find(".png") > -1:
        ext = ".png"
        img_url.replace(ext,"")        
    if img_type == "thumbnail":
        img_url = img_url + "thumbnail_220x293" + ext
    return img_url

def MakeTGoodsDic(title,en_title,price,option_kind,img,goods_id,catecode,cate_code2,asin_url):
    global exchange
    asin_url = asin_url[:1000]
    img = img[:290]
    dic = dict()
    dic["SiteID"] = "'rental'"
    dic["DealerID"] = "'rental'"
    dic["GoodsType"] = "'N'"
    # title ban, replace 작업
    title = title.lower()
    title = SetReplaceTitle(title)
    en_title = SetReplaceTitle(en_title)
    title = title.replace("'","''")
    dic["Title"] = "dbo.GetCutStr('{0}',120,'...')".format(title)
    dic["E_title"] = "dbo.GetCutStr('{0}',120,'...')".format(title)
    dic["DE_title"] = "dbo.GetCutStr('{0}',120,'...')".format(en_title)

    # price 마진 계산
    margin = PriceMargin(float(price))
    dic["Price"] = margin
    dic['price_tmp'] = "'"+str(price)+"'"
    dic["OriginalPrice"] = int(float(price)*exchange)
    dic["origin_dollar"] = float(price)
    dic["OptionKind"] = option_kind
    if option_kind == "300":
        dic["many_option"] = "'1'"
    else:
        dic["many_option"] = "'0'"
    dic["State"] = "'100'"
    dic["ali_no"] = "'"+goods_id+"'"
    dic["Shipping_Fee"] = 0
    dic["imgB"] = "'https://"+img+"'"
    dic["imgM"] = "'https://"+img+"'"
    dic["imgS"] = "'https://"+img+"'"
    dic["naver_img"] = "'https://"+img+"'"
    dic["DeliveryPolicy"] = "'990'"
    dic['cate_idx'] = catecode
    dic['cate_code2'] = "'"+cate_code2+"'"
    dic['asin_url'] = "'"+asin_url+"'"

    print(">> margin : {0}".format(margin))
    print(">> OriginalPrice : {0}".format(int(float(price)*exchange)))
    #print(">> img : {0}".format(img))

    return dic

def makeTGoodsOptionDic(goods_uid,title,items,ali_no,description,sort):
    dic = dict()
    items = items.replace("'","")

    dic["GoodsUid"] = goods_uid
    dic["Title"] = "'"+title+"'"
    dic["Items"] = "'"+items+"'"
    dic["option_code"] = "'"+ali_no+"'"
    dic["sort"] = sort
    dic["option_image"] = "'https://"+description["image"]["main_image"]+"'"
    description = str(description).replace("'", '"')
    dic["backup_items"] = "'"+description+"'"  
    print(">> [t_goods_option] GoodsUid : {0}".format(goods_uid))
    print(">> Option Items : {0}".format(items))
    print(">> Option code : {0}".format(ali_no))

    return dic

def MakeTGoodsOptionItemDic(option_uid,item):
    dic = dict()
    item = str(item)
    dic["OptionUid"] = option_uid
    dic["item"] = "'"+item+"'"
    dic["sort"] = 1
    print(">> [t_goods_option_item] OptionUid : ({0}) | {1}".format(option_uid, item))
    return dic

def MakeTGoodsContentDic(goods_uid, description):
    dic = dict()
    content = MakeContent(description)
    content = content.replace("'", '"')
    description = str(description).replace("'", '"')
    dic["Uid"] = goods_uid
    dic["content"] = "'"+content+"'"
    dic["content_backup"] = "'"+description+"'"
    return dic

def MakeTGoodsCategory(catecode,goods_uid):
    dic = dict()
    dic["CateCode"] = catecode
    dic["GoodsUid"] = goods_uid
    dic["sort"] = 1
    return dic

def MakeTGoodsSub(goods_uid):

    dic = dict()
    dic["Uid"] = goods_uid
    dic["Product"] = "'China'"
    return dic

def MakeContent(description):
    # detail = content["detail"]
    # image = content["image"]
    
    content = '<div id="product_content_box">'
    content += '<div id="text_content_box">'
    content += '<div id="product_info"">'
    for product_detail in description["detail"]["product_detail"]:
        content += '<div class="detail_name">{}</div><div class="detail_value">{}</div><br>'.format(product_detail["name"],product_detail["value"])
    content += '</div>'#product_info
    
    if len(description["detail"]["model"]) > 0:
        content += '<div id="model_info">'
        content += '<div id="model_image_box">'
        content += '<div id="model_image_cover">'
        content += '<div id="model_image_inner">'
        content += '<img src="{}" id="model_image">'.format(description["detail"]["model"]["model_image"])
        content += '</div>'#model_image_inner
        content += '</div>'#model_image_cover
        content += '</div>'#model_image_box
        content += '<div id="model_size_info_box">'
        content += '<div id="model_wear">모델이 착용 중 : <span>{}</span></div>'.format(description["detail"]["model"]["model_wear"])
        content += '<div id="model_size_info">'
        for key,value in description["detail"]["model"]["model_size"].items():
            if value=="":
                continue
            content += '<div class="model_item">{} : <span>{}</span></div>'.format(key, value)
        content += '</div>'#model_size_info_box        
        content += '</div>'#model_info    
    
    content += '<div id="size_info">'
    content += '<div id="product_size">'

    if "multiPartInfo" in description["detail"]["size"]["product"]:
        table = description["detail"]["size"]["product"]["multiPartInfo"]
        for caption in table:
            if len(caption["multiPartSizeInfo"]) == 0 :
                continue
            content += '<table>'
            content += '<caption>{}</caption>'.format(caption["multiPartName"])
            content += '<tr>'
            th = caption["multiPartSizeInfo"][0]
            if th["attr_name"]!="":
                content += '<th>{}</th>'.format(th["attr_name"])
            for key, value in th.items():
                if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                    continue
                content += '<th>{}</th>'.format(key)
            content += '</tr>'
            for tr in caption["multiPartSizeInfo"]:
                content += '<tr>'
                if tr["attr_name"]!="":
                    content += '<td>{}</td>'.format(tr["attr_value_name"])
                for key, value in tr.items():
                    if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                        continue
                    content += '<td>{}</td>'.format(value) 
                content += '</tr>'
            content += '</table>'
    else:
        if "attr_name" in description["detail"]["size"]["product"]["size_info"][0]:
            content += '<table>'
            content += '<tr>'        
            th = description["detail"]["size"]["product"]["size_info"][0]
            if th["attr_name"]!="":
                content += '<th>{}</th>'.format(th["attr_name"])
                
            for key, value in th.items():
                if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                    continue
                content += '<th>{}</th>'.format(key)
            content += '</tr>'
            for tr in description["detail"]["size"]["product"]["size_info"]:
                content += '<tr>'
                if tr["attr_name"]!="":
                    content += '<td>{}</td>'.format(tr["attr_value_name"])
                for key, value in tr.items():
                    if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                        continue
                    content += '<td>{}</td>'.format(value) 
                content += '</tr>'
            content += '</table>'
    if len(description["detail"]["size"]["product"]["template"]) > 0:
        content += '<div class="size_template">'    
        content += '<div class="template_image_box">'
        content += '<img src="{}" class="template_image">'.format(description["detail"]["size"]["product"]["template"]["image_url"])
        content += '</div>'#template_image_box
        content += '<div class="template_description">'
        for template in description["detail"]["size"]["product"]["template"]["description_multi"]:        
            content += '<div class="template_description_item"><h6 class="description_item_title"><em class="sort">{}</em>{}</h6><p class="description_obj">{}</p></div>'.format(template["sort"],template["name"],template["description"])
        content += '</div>'#template_description
        content += '</div>'#size_template
    content += '</div>'#product_size

    if len(description["detail"]["size"]["body"]["size_info"]) > 0:
        content += '<div id="body_size">'
        content += '<table>'
        content += '<tr>'
        th = description["detail"]["size"]["body"]["size_info"][0]

        for key, value in th.items():
            if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                continue
            content += '<th>{}</th>'.format(key)
        content += '</tr>'
        for tr in description["detail"]["size"]["body"]["size_info"]:
            content += '<tr>'
            for key, value in tr.items():
                if key=="attr_id" or key=="attr_name" or key=="attr_value_id" or key=="attr_value_name" or key=="attr_value_name_en":
                    continue
                content += '<td>{}</td>'.format(value) 
            content += '</tr>'
        content += '</table>' 
        content += '<div class="size_template">'
        content += '<div class="template_image_box">'
        content += '<img src="{}" class="template_image">'.format(description["detail"]["size"]["body"]["template"]["image_url"])
        content += '</div>'#template_image_box
        content += '<div class="template_description">'
        for template in description["detail"]["size"]["body"]["template"]["description_multi"]:        
            content += '<div class="template_description_item"><h6 class="description_item_title"><em class="sort">{}</em>{}</h6><p class="description_obj">{}</p></div>'.format(template["sort"],template["name"],template["desc"])
        content += '</div>'#template_description
        content += '</div>'#size_template
        content += '</div>'#body_size
    content += '</div>'#size_info
    content += '</div>'#text_content_box

    content += '<div id="image_content_box">'
    content += '<div id="main_image"><img src="https://{}" class="product_image"></div>'.format(description["image"]["main_image"])
    content += '<div id="image_content"">'
    for image in description["image"]["detail_images"]:
        content += '<div class="detail_image"><img src="https://{}" class="product_image"></div>'.format(image)
    content += '</div>'#image_content
    content += '</div>'#image_content_box
    
    content = content + '</div>'#product_content_box
    
    return content

def MakeTGetAsin(recomend_json,db_con):
    lst = []
    for product in recomend_json["info"]["products"]:
        dic = dict()
        sql = "select * from t_goods_option where option_code='{}'".format(str(product["cat_id"]))
        row = db_con.selectone(sql)
        if row:
            continue
        goods_url_name = product["goods_url_name"]
        dic["asin"] = "'"+str(product["goods_id"])+"'"
        dic["cate_code2"] = "'"+str(product["cat_id"])+"'"
        dic["url"] = "'"+makeSheinProdUrl(goods_url_name,product["goods_id"],product["cat_id"])+"'"
        sql = "select top 1 CateCode from t_category where lastcate=1 and IsHidden='F' and cate_code2='{}'".format(product["cat_id"])
        row = db_con.selectone(sql)
        if row:
            dic["catecode"] = row[0]
        else:
            continue
        lst.append(dic)

    return lst

def OptionClear(db_con,goods_uid):
    # db_con_clear = DBmodule_FR.Database(DBname)
    sql = "select UID from t_goods_option where GoodsUid={}".format(goods_uid)
    rs = db_con.select(sql)
    for row in rs:
        db_con.delete("t_goods_option_item","OptionUid={}".format(row[0]))
    db_con.delete("t_goods_option","GoodsUid={}".format(goods_uid))
    print(">> OptionClear: {} ".format(goods_uid))

def PriceMargin(price):
    global exchange, ali_price_ck, delivery_fee, coupon
    delivery_fee = delivery_fee * exchange
    delivery_fee = ReversSale(delivery_fee,coupon)
    price = float(price)

    won_price = price * exchange
    for i in range(1,31):
        i = str(i)
        st = ali_price_ck["st_"+i+"p"]
        ed = ali_price_ck["ed_"+i+"p"]
        uppr = float(ali_price_ck["p_"+i+"uppr"])
        plus = ali_price_ck["plus_"+i+"p"]
        # print("{} < {} < {}".format(st,price,ed))
        if i=="30":
            ed = 99999

        if st < price <= ed:
            won_price = (won_price * uppr) + plus
        won_price = won_price + delivery_fee
    return int(round(won_price,-2))

def SetBanTitle(title):
    global ban_title_list
    chk = False

    for ban_title in ban_title_list:
        if ban_title["ban_check"] == 1 or ban_title["ban_check"] == "1":
            keyword = ban_title["ban_title_gubun"]
            pattern = keyword+r'\b'
            regex = re.compile(pattern,re.I)
            se = regex.search(title)
            
            pattern2 = r'\b'+keyword
            regex2 = re.compile(pattern2,re.I)
            se2 = regex2.search(title)    
            
            if se and se2:
                chk = True
                print(ban_title)
                break
        else:
            # 밴타이틀 한개
            if not(ban_title["ban_title_inner"]) or ban_title["ban_title_inner"]=="":
                if title.find(ban_title["ban_title_gubun"]) > -1:
                    chk = True
                    print(ban_title)
                    break
            # 밴타이틀 두개
            elif not(not(ban_title["ban_title_inner"]) or ban_title["ban_title_inner"]=="") and (not(ban_title["ban_title_gubun_2"]) or ban_title["ban_title_gubun_2"]==""):
                if (title.find(ban_title["ban_title_gubun"]) > -1) and (title.find(ban_title["ban_title_inner"]) > -1):
                    chk = True
                    print(ban_title)
                    break
            # 밴타이틀 세개
            else:
                if (title.find(ban_title["ban_title_gubun"]) > -1) and (title.find(ban_title["ban_title_inner"]) > -1) and (title.find(ban_title["ban_title_gubun_2"]) > -1):
                    chk = True
                    print(ban_title)
                    break
    return chk

def SetReplaceTitle(title):
    global replace_title_list
    for replace_title in replace_title_list:        
        title = title.replace(replace_title["replace_ban_title"],replace_title["replace_title"])    
    
    return title

def goodsCodeUpdate(db_con,goods_uid,code):
    dic = dict()
    num = len(str(goods_uid))
    goods_code = str(goods_uid)
    for i in range(10-num):
        goods_code = "0"+goods_code
    dic["GoodsCode"] = "'T"+str(goods_code)+"'"
    db_con.update("t_goods",dic,"Uid='{}'".format(goods_uid))
    goodscode = 'T'+ str(goods_code)
    print(">> goodsCodeUpdate : {}".format(goodscode))
    return goodscode

def ListToStr(lst):
    string = str(lst).replace("[", "").replace("]", "").replace("'", "")
    
    return string

def ReversSale(num,coupon):
    sale_per = (100-coupon)/100
    sale = num/sale_per
    
    return round(sale)

# 1분 마다 timecount 증가 (2시간 이후 종료)
def fun_timer():
    global timecount
    print(">> Timer : {}".format(datetime.datetime.now()))
    proces_timer = threading.Timer(60, fun_timer)
    timecount = timecount + 1
    print('>> timecount : '+str(timecount))
    proces_timer.start()

    if (timecount >= 120):
        print('>> 타임아웃 종료 : {}'.format(datetime.datetime.now()))
        #print(os.system('tasklist')) #프로세스 목록 출력

        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)

            fname = os.path.abspath( __file__ )
            fname = trend_func.getparseR(fname,"\\","")
            fname = fname.replace(".py",".exe")
            print(">> fname : {}".format(fname)) 

            time.sleep(5)
            taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr2 : {}".format(taskstr2))  
            os.system(taskstr2)
        except Exception as e:
            print('>> taskkill Exception (2)')

        time.sleep(5)
        os._exit(1)

def procLogSet(proc_no, ip, proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(proc_no) + "', '" + str(ip) + "', '" + str(proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    db_con.execute(sql)

    return "0"

def version_check(pgKbn):
    print(">> (PG) ver : " + ver)
    file_path = r"c:/project/"

    sql = "select version,url, pgFilename from python_version_manage where name = '" +str(pgKbn)+"'"
    print(">> sql:" + sql)
    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        pgFilename = rows[2]
        new_filename = file_path + pgFilename
        old_filename = file_path + str(pgFilename).replace("new_","")

        print(">> (DB) version : {} | version_url : {}" .format(version,version_url))
        if str(ver) != str(version):
            db_con.close()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)
            time.sleep(60)
            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize < 100000:
                time.sleep(60)
                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 100000:
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
            try:
                fname = os.path.abspath( __file__ )
                fname = trend_func.getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 
                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

def MakeManage(pgKbn, pgSite):
    dic = dict()
    sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,'') from python_version_manage where name = '{}'".format(pgKbn)
    rs = db_con.selectone(sql)
    if not rs:
        print(">> pgKbn 값을 확인하세요 : {} ".format(input_pgKbn))        
    else:
        dic["pgKbn"] = pgKbn
        dic["pgSite"] = pgSite
        dic["pgFilename"] = str(rs[0]).strip()
        dic["pgName"] = str(rs[1]).strip()
        dic["now_url"] = str(rs[2]).strip()
        dic["now_url2"] = str(rs[3]).strip()
        dic["sql1"] = str(rs[4]).replace("`","'")
        dic["sql2"] = str(rs[5]).replace("`","'")
        dic["sql3"] = str(rs[6]).replace("`","'")

    if dic["pgFilename"] is None or dic["pgFilename"] == "":
        dic["pgFilename"] = "new_" + str(dic["pgName"]) + ".exe"
    if dic["pgName"] is None or dic["pgName"] == "":
        dic["pgName"] = pgKbn
    if dic["sql1"] == "":
        print('>> 대상 sql 없습니다 (확인 필요) : ' + str(datetime.datetime.now()))

    print('>> pgName : {} | pgSite : {} | pgFilename : {} | pgKbn : {} | now_url : {} '.format(dic['pgName'],pgSite,dic["pgFilename"],pgKbn,dic["now_url"] ))
    return dic

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_NEW.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def del_proc(code, asin, catecode):

    if code[:1] == "D":
        DIsDisplay = ""
        D_naver_in = ""
        D_goodscode = ""
        D_asin_url = ""
        sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, isnull(asin_url,'') from T_goods where ali_no = '{0}'".format(asin)                 
        rs = db_con.selectone(sql)
        if rs:
            Duid = rs[0]
            DIsDisplay = rs[1]
            DDel_Naver = rs[2]
            D_regdate = rs[3]
            D_UpdateDate = rs[4]
            D_naver_in = rs[5]
            D_goodscode = rs[6]
            D_asin_url = rs[7]
            print(">> DB:{} ({}) | D_naver_in:{} | D_regdate :{} | D_UpdateDate:{}".format(D_goodscode, DIsDisplay, D_naver_in, D_regdate, D_UpdateDate))
            # T_goods sold out
            if DIsDisplay == 'T':
                if code == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                    sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', stock_ck = '1', stock_ck_date=getdate() where uid = {0}".format(Duid)
                    db_con.execute(sql_u1)

                    sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
                    db_con.execute(sql_u2)
                else:
                    print('>> [' + str(asin) + '] setDisplay (품절 처리) :' + str(Duid))                              
                    sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '1', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(Duid)
                    print(">> sql : " + str(sql))
                    print(">> 품절 처리 OK : " + str(asin))
                    db_con.execute(sql)

                # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc_amazon 테이블에 Insert (mode : D)
                if str(D_naver_in) == "1":
                    proc_ep_insert(D_goodscode,'D')

    # dic_b = dict()
    # dic_b['asin'] = "'" + asin + "'"
    # dic_b['catecode'] = catecode
    # if len(D_asin_url) > 1000:
    #     dic_b['url'] = "''"
    # else:
    #     dic_b['url'] = "'" + D_asin_url + "'"
    # dic_b['memo'] = "'" + code + "'"
    # dic_b['code'] = "'" + code[:3] + "'"
    # dic_b['reg_date'] = " getdate() "

    sql_d1 = "delete from t_getasin_del where asin ='{0}'".format(asin)
    db_con.execute(sql_d1)
    print('>> ##delete## : t_getasin_del')

    sql_d2 = "insert into T_GETASIN_DEL (asin, title, en_title, url, catecode, cate_code2, code, memo) select asin, title, en_title, url, catecode, cate_code2, '{}', '{}' from T_GETASIN where asin = '{}'".format(code[:3], code, asin)
    db_con.execute(sql_d2)
    print('>> ##insert## : t_getasin_del')

    sql = "delete from t_getasin where asin ='{0}'".format(asin)
    db_con.execute(sql)


def procWork(in_ip):
    print('>> procWork : ' + str(datetime.datetime.now()))

    ip_catecode = ""
    sql = "select catecode from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)
    if rows:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] Catecode : " + str(ip_catecode))
        sql = "update update_list2 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list2 (getdate) ")
        db_con.execute(sql)

    return "0"

def procWork_stock(in_ip):
    print('>> procWork_stock : ' + str(datetime.datetime.now()))

    ip_catecode = ""
    sql = "select catecode from update_list3 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)
    if rows:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] Catecode : " + str(ip_catecode))
        sql = "update update_list3 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list3 (getdate) ")
        db_con.execute(sql)

    return "0"


# Stock ###################################################################################
def get_stock_asin(in_sql1, in_sql2, in_sql3):
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
            url = ea_asin[1]
            cateidx = ea_asin[2]
            uid = ea_asin[3]
            if (uid is None) or (uid == '') or uid == "None":
                uid = ''
            if (url is None) or (url == ''):
                url = 'null'
            asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(url) + '@' + str(uid))

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
                url = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (uid is None) or (uid == '') or uid == "None":
                    uid = ''
                if (url is None) or (url == ''):
                    url = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(url) + '@' + str(uid))

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
                url = ea_asin[1]
                cateidx = ea_asin[2]
                uid = ea_asin[3]
                if (uid is None) or (uid == '') or uid == "None":
                    uid = ''
                if (url is None) or (url == ''):
                    url = 'null'
                asinset.append(str(asin) + '@' + str(cateidx) + '@' + str(url) + '@' + str(uid))

    if chk_data == "0":
        return ""

    return asinset


def stock_proc(Duid, D_naver_in, D_goodscode, flg):

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


def check_price(price, price_Symbol):
    print(">> check_price ")
    if price_Symbol.find('$') == -1:
        print(">> price_Symbol : {}".format(price_Symbol))
        price_won = price
        price = int(price) / (exchange-50)
        print(">> {} 원 -> $ {} 변경 ".format(price_won, round(price, 2)))
    return round(price, 2)

def main_proc_stock(dicMangage, test_asin, currIp):
    global err_cnt
    pgKbn = dicMangage["pgKbn"]
    pgSite = dicMangage["pgSite"]
    sql1 = dicMangage["sql1"]
    sql2 = dicMangage["sql2"]
    sql3 = dicMangage["sql3"]

    # asin get
    get_asin_list = []
    get_asin_list = get_stock_asin(sql1, sql2, sql3)
    print(get_asin_list)

    if len(get_asin_list) == 0:
        return "1"

    for asin_item in get_asin_list:
        print(">>---------------------------------------------")

        if err_cnt > 10:
            print(">> err_cnt over (exit) : {}".format(asin))
            procLogSet(pgKbn, currIp, " [" + str(asin) + "] err_cnt 10 over ")
            return "E"

        sp_item = asin_item.split("@")
        asin = sp_item[0]
        catecode = sp_item[1]
        item_url = sp_item[2]
        uid = sp_item[3]

        # asin_url = "https://asia.shein.com"+item_url+"&share_from=asia"
        asin_url = "https://kr.shein.com"+item_url+"&share_from=asia"
        print(">> [{}] asin : {} | {}".format(catecode, asin, asin_url))
        guid = ""
        if uid == "" or uid == "null" or uid == "None":
            sql = "select UID, goodscode, isnull(stop_update,'0'), naver_in, regdate, updatedate from t_goods where ali_no='{}'".format(asin)
        else:
            sql = "select UID, goodscode, isnull(stop_update,'0'), naver_in, regdate, updatedate from t_goods where uid='{}'".format(uid)
        row2 = db_con.selectone(sql)
        if not row2:
            print(">> t_goods 상품 없음(skip) : {}".format(asin))
        else:
            print(">> (stock check) t_goods 상품 존재함 : {}".format(asin))

            stop_update = ""
            goodscode = ""
            if row2:
                guid = str(row2[0])
                goodscode = str(row2[1])
                stop_update = str(row2[2])
                naver_in = str(row2[3])
                regdate = str(row2[4])
                updatedate = str(row2[5])
                print(">>(guid: {}) goodscode : {} | {} | {}".format(guid, goodscode, regdate, updatedate))
            if stop_update == "1":
                print(">> stop_update 상품 (skip) : {} ".format(asin))
                del_proc("S01", asin)
                continue

            try:
                driver.get(asin_url)
                time.sleep(random.uniform(4,6))
            except Exception as ex:
                # input(">> after check : ")
                print(">> Exception (driver.get) : {}".format(ex))
                print(str(datetime.datetime.now()))
                print(">> asin : {}".format(asin))
                return "E"

            try:
                if driver.find_element(By.CSS_SELECTOR, 'div.sui-dialog__body > div.c-coupon-box > span'):
                    driver.find_element(By.CSS_SELECTOR, 'div.sui-dialog__body > div.c-coupon-box > span').click()
            except:
                #print(">> Popup Exception")
                pass

            if driver.current_url.find("/risk/") > -1:
                procLogSet(input_pgKbn, currIp, " [" + str(asin) + "] 캡챠 확인 ")
                stock_proc(guid, naver_in, goodscode, "stock_ck_0") # blocked 상품 stock_ck : 0 
                input(">> 캡챠 확인 :")
                continue

            html = driver.page_source
            if str(html).find('class="coupon-dialog__top-title"') > -1:
                print(">> coupon-dialog ")

            if html.find("Your request is not compliant and has been blocked by us.") > -1:
                print(">> Your request is not compliant and has been blocked by us : {} ".format(asin))
                stop = input(">> block : ")

            soup = BeautifulSoup(html,'html.parser')
            time.sleep(1)
            html = driver.page_source
            if html.find('항목이 제거되었습니다') > -1:
                print(">> 품절상품 (2) (skip) : {} ".format(asin))
                del_proc("D01", asin, catecode)
                time.sleep(sleep_num)
                continue

            try:            
                json_data = getPrdData(html)
            except:
                print(">> 잘못된 상품 (skip) : {} ".format(asin))
                del_proc("D02", asin, catecode)
                # input(">> json_data Check :")
                err_cnt = err_cnt + 1
                time.sleep(sleep_num)
                continue

            if json_data == "":
                print(">> 잘못된 상품 (1)(skip) : {} ".format(asin))
                del_proc("D02", asin, catecode)
                # input(">> json_data Check :")
                err_cnt = err_cnt + 1
                time.sleep(sleep_num)
                continue

            if json_data["mallStock"]==0:
                print(">> 품절상품 (skip) : {} ".format(asin))
                del_proc("D01", asin, catecode)
                time.sleep(sleep_num)
                continue

            if str(driver.page_source).find('id="ProductDetailAddBtn"') > -1:
                btnChk = trend_func.getparse(str(html),'id="ProductDetailAddBtn"','>')
                if btnChk.find('disabled') > -1:
                    print(">> 품절상품 (장바구니 비활성화) (skip) : {} ".format(asin))
                    del_proc("D01", asin, catecode)
                    time.sleep(sleep_num)
                    continue

            title = json_data["detail"]["goods_name"]
            en_title = json_data["detail"]["goods_url_name"]
            if SetBanTitle(title):
                print(">> 금지어 상품 (skip) : {} ".format(asin))
                del_proc("D03", asin, catecode)
                time.sleep(sleep_num)
                continue

            price = json_data["getPrice"]["retailPrice"]["amount"]
            if str(price).find('undefined') > -1 or str(price).find("retailPrice") > -1:
                print(">> Price undefined or retailPrice (Skip) : {} ".format(asin))
                del_proc("D31", asin, catecode)
                time.sleep(sleep_num)
                continue

            price_Symbol = json_data["getPrice"]["retailPrice"]["amountWithSymbol"]
            if str(price) == "" or str(price) == "0":
                print(">> Price Check : {}".format(price))
                procLogSet(input_pgKbn, currIp, " [" + str(asin) + "] Price 없음 ")
                err_cnt = err_cnt + 1
                del_proc("D31", asin, catecode)
                # input(">> Price Check :")
                time.sleep(sleep_num)
                continue

            if price_Symbol.find('$') == -1:
                print(">> price_Symbol : {}".format(price_Symbol))
                print(">> (before) price : {} | {}".format(price, price_Symbol))
                price = check_price(price, price_Symbol)
                print(">> (after) price : {} | {}".format(price, price_Symbol))

            print(">> 재고체크 완료 : {} | {} ".format(asin, goodscode))
            stock_proc(guid, naver_in, goodscode, "stock_ck_2") # 정상상품 stock_ck : 2
            err_cnt = 0 

def moveScroll(driver, proc_cnt):
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
        if sroll_cnt > proc_cnt:
            break
        last_height = new_height

def del_cateasin(catecode):
    print(">> 카테고리 : "+str(catecode) + " asin 없음 다음 카테고리로 넘어감")
    
    sql_update_list = "delete from update_list2 where proc_ip = '{0}'".format(currIp)
    print(">> update_list2 (del) : {}".format(currIp))
    db_con.execute(sql_update_list)
    
    sql_del = "delete from t_getasin where catecode='{}'".format(catecode)
    print(">> t_getasin (del) {} (asin 삭제) ".format(catecode))
    db_con.execute(sql_del)
    
    sql_upd = "update t_category set site_chk = 'F' where catecode = '{}'".format(catecode)
    print(">> t_category 카테고리 {} (site_chk : F 설정) ".format(catecode))
    db_con.execute(sql_upd)


def main_proc_goods(dicMangage, test_asin, currIp):

    pgKbn = dicMangage["pgKbn"]
    pgSite = dicMangage["pgSite"]
    asin = ""
    try:
        result = get_asin_function.newlist2(db_con, currIp)
        sql_asin = "select top 1 asin, url, isnull(catecode,''), isnull(cate_code2,'') from t_getasin where catecode='{}' order by regdate".format(result['catecode'])
        asin_item = db_con.selectone(sql_asin)

        if not asin_item:
            sql_update_list = "delete from update_list2 where proc_ip = '{0}'".format(currIp)
            db_con.execute(sql_update_list)
            print("카테고리 : "+str(result['catecode']) + " asin 없음 다음 카테고리로 넘어감")
            return "1"
        else:
            catecode = asin_item[2]
            cate_code2 = asin_item[3]

        if result["page"] > 100:
            sql_catecode = "select top 1 catecode from T_CATEGORY where IsHidden='F' and lastcate=1 and catecode not in (select CateCode from T_GOODS_CATEGORY group by CateCode) order by catecode"
            row_catecode = db_con.selectone(sql_catecode)
            if row_catecode:
                update_catecode = row_catecode[0]
                # sql_update_list = "update update_list2 set catecode='{}', now_page=1 where proc_ip = '{}'".format(update_catecode,currIp)
                # catecode = row_catecode[0]
                # db_con.execute(sql_update_list)

                # 카테고리 및 asin 삭제처리
                del_cateasin(update_catecode)
                print("100개 입력 완료 다음 카테고리로 넘어감")
                return "2"

        amz_cateurl = ""
        if catecode=="":
            sql = "select CateCode, isnull(amz_cateurl,'') from t_category where lastcate=1 and IsHidden='F' and cate_code2='{}'".format(cate_code2)
            rs = db_con.selectone(sql)
            if rs:                
                catecode = rs[0]
                amz_cateurl = rs[1]
            else:
                print("잘못된 카테코드 skip")
                return "1"

        sql = "select minus_opt, isnull(amz_cateurl,'') from t_category where catecode={}".format(catecode)
        row = db_con.selectone(sql)
        if row:
            if amz_cateurl == "":  amz_cateurl = row[1]
            if row[0]==1 or row[0]=="1":
                minus_opt = True
            else:
                minus_opt = False        

        print(">> 카테코드 [{}] 링크 체크 : {}".format(catecode, amz_cateurl))
        try:
            driver.get(amz_cateurl)
            time.sleep(random.uniform(4,6))
        except Exception as ex:
            print(">> Exception (driver.get) : {}".format(ex))
            print(str(datetime.datetime.now()))
            print(">> asin : {}".format(asin))
            return "E"
        else:
            now_url = driver.current_url
            if now_url.find("/risk/") > -1:
                procLogSet(input_pgKbn, currIp, " [" + str(asin) + "] 캡챠 확인 ")
                input(">> 캡챠 확인 :")

            if str(driver.page_source).find('class="productList-empty__text"') > -1 or str(driver.page_source).find('항목이 제거되었습니다') > -1 or str(driver.page_source).find('item has been removed') > -1:
                # 카테고리 및 asin 삭제처리
                del_cateasin(catecode)
                return "2"

        if test_asin != "":
            sql_asin = "select asin, isnull(url,''), isnull(catecode,''), isnull(cate_code2,'') from t_getasin where asin='{}'".format(test_asin)
            asin_items = db_con.select(sql_asin)
            if not asin_items:
                sql_asin = "select ali_no, isnull(asin_url,''), isnull(cate_idx,''), isnull(cate_code2,'') from t_goods where ali_no = '{}'".format(test_asin)
                asin_items = db_con.select(sql_asin)
        else:
            sql_asin = "select top 100 asin, isnull(url,''), isnull(catecode,''), isnull(cate_code2,'') from t_getasin where catecode='{}' order by regdate".format(catecode)
            asin_items = db_con.select(sql_asin)

        price_chk_cnt = 0
        sold_cnt = 0
        # asin 100개 처리
        for asin_item in asin_items:
            print(">>---------------------------------------------")
            asin = asin_item[0]
            item_url = asin_item[1]
            catecode = asin_item[2]
            cate_code2 = asin_item[3]

            if sold_cnt > 7:
                sql_update_list = "delete from update_list2 where proc_ip = '{0}'".format(currIp)
                db_con.execute(sql_update_list)
                print("카테고리 : "+str(result['catecode']) + " asin 없음 다음 카테고리로 넘어감(2)")
                return "1"

            if item_url == "":
                print(">> asin_url 존재 안함 : {}".format(asin))
                del_proc("U01", asin, catecode)
                continue

            # url = "https://asia.shein.com"+asin_item[1]+"&share_from=asia"
            url = "https://kr.shein.com"+asin_item[1]+"&share_from=asia"
            asin_url = url
            print(">> [{}] asin : {} | {}".format(catecode, asin, asin_url))

            guid = ""
            ouid = ""
            sql = "select UID, goodsuid from t_goods_option where option_code='{}'".format(asin)
            row = db_con.selectone(sql)
            sql = "select UID, goodscode, isnull(stop_update,'0') from t_goods where ali_no='{}'".format(asin)
            row2 = db_con.selectone(sql)

            if not row2 and not row:
                mode = "insert"
            else:
                mode = "update"
                print(">> (update) t_goods 상품 존재함 : {}".format(asin))

                stop_update = ""
                goodscode = ""
                if row:
                    ouid = str(row[0])
                    goodsuid = str(row[1])
                    print(">>(ouid: {}) goodsuid : {}".format(ouid, goodsuid))
                if row2:
                    guid = str(row2[0])
                    goodscode = str(row2[1])
                    stop_update = str(row2[2])
                    print(">>(guid: {}) goodscode : {}".format(guid, goodscode))
                if stop_update == "1":
                    print(">> stop_update 상품 (skip) : {} ".format(asin))
                    del_proc("S01", asin, catecode)
                    continue

                print(">> t_goods 상품 존재함 : {}".format(asin))
                del_proc("U01", asin, catecode)
                continue

            try:
                driver.get(url)
                time.sleep(random.uniform(4,6))
            except Exception as ex:
                # input(">> after check : ")
                print(">> Exception (driver.get) : {}".format(ex))
                print(str(datetime.datetime.now()))
                print(">> asin : {}".format(asin))
                return "E"

            try:
                if driver.find_element(By.CSS_SELECTOR, 'div.sui-dialog__body > div.c-coupon-box > span'):
                    driver.find_element(By.CSS_SELECTOR, 'div.sui-dialog__body > div.c-coupon-box > span').click()
            except:
                #print(">> Popup Exception")
                pass
            now_url = driver.current_url
            if now_url.find("/risk/") > -1:
                procLogSet(input_pgKbn, currIp, " [" + str(asin) + "] 캡챠 확인 ")
                input(">> 캡챠 확인 :")
                continue

            if str(driver.page_source).find('항목이 제거되었습니다') > -1 or str(driver.page_source).find('item has been removed') > -1:
                print(">> 품절상품 (항목이 제거되었습니다.)(2) (skip) : {} ".format(asin))
                del_proc("D01", asin, catecode)
                time.sleep(sleep_num)
                sold_cnt = sold_cnt + 1
                continue

            html = driver.page_source
            if str(driver.page_source).find('id="ProductDetailAddBtn"') > -1:
                btnChk = trend_func.getparse(str(html),'id="ProductDetailAddBtn"','>')
                if btnChk.find('disabled') > -1:
                    print(">> 품절상품 (장바구니 비활성화) (skip) : {} ".format(asin))
                    del_proc("D01", asin, catecode)
                    time.sleep(sleep_num)
                    sold_cnt = 0
                    continue

            # scroll 
            try:
                moveScroll(driver, random.uniform(2,5))
            except:
                pass

            html = driver.page_source
            if str(html).find('class="coupon-dialog__top-title"') > -1:
                print(">> coupon-dialog ")

            if html.find("Your request is not compliant and has been blocked by us.") > -1:
                print(">> Your request is not compliant and has been blocked by us ")
                stop = input(">> block : ")

            soup = BeautifulSoup(html,'html.parser')
            time.sleep(1)
            lang = ""
            # try:
            #     lang = soup.select_one("a.col-xs-4.global-active").get_text()
            # except:
            #     lang = soup.select_one("a.col-xs-4 global-active").get_text()
            if str(html).find('카테고리별 쇼핑') > -1:
                lang = "Korea"
            if lang == "English":
                changeLang(driver)
                html = driver.page_source

            try:            
                json_data = getPrdData(html)
            except:
                print(">> 잘못된 상품 (skip) : {} ".format(asin))
                del_proc("D02", asin, catecode)
                time.sleep(sleep_num)
                continue

            mall_stock = ""
            try:  
                mall_stock = str(json_data["detail"]["mall_stock"][0]['stock'])
                print(">> mall_stock: {} ".format(mall_stock))
            except:
                print(">> mall_stock except : {} ".format(asin))
            else:
                if str(json_data["detail"]["mall_stock"][0]['stock']) == "0":
                    print(">> 품절상품 (skip) : {} ".format(asin))
                    del_proc("D01", asin, catecode)
                    time.sleep(sleep_num)
                    sold_cnt = 0
                    continue

            sold_cnt = 0 
            title = json_data["detail"]["goods_name"]
            en_title = json_data["detail"]["goods_url_name"]
            if SetBanTitle(title):
                print(">> 금지어 상품 (skip) : {} ".format(asin))
                del_proc("D03", asin, catecode)
                time.sleep(sleep_num)
                continue

            # if str(html).find('품절되었습니다') > -1:
            #     print(">> 품절상품 (품절되었습니다) (skip) : {} ".format(asin))
            #     del_proc("D01", asin, catecode)
            #     time.sleep(sleep_num)
            #     continue

            time_num = random.randint(3, 6)
            time.sleep(time_num)
            print(">> 작업 시작 : {}".format(asin))
            start = time.time()
            price = json_data["getPrice"]["retailPrice"]["amount"]
            price_won = price
            if str(price).find('undefined') > -1 or str(price).find("retailPrice") > -1:
                print(">> Price undefined or retailPrice (Skip) : {} ".format(asin))
                del_proc("D31", asin, catecode)
                time.sleep(sleep_num)
                continue

            price_Symbol = json_data["getPrice"]["retailPrice"]["amountWithSymbol"]
            if price_Symbol.find('$') == -1:
                print(">> price_Symbol : {}".format(price_Symbol))
                print(">> (before) price : {} | {}".format(price, price_Symbol))
                price = check_price(price, price_Symbol)
                print(">> (after) price : {} | {}".format(price, price_Symbol))

            goods_id = json_data["detail"]["goods_id"]
            cat_id = json_data["detail"]["cat_id"]
            store_code = json_data["detail"]["store_code"]
            option_urls = getOtherOptionUrl(json_data,minus_opt)
            size_options = getSizeOption(json_data,price_Symbol)
            if json_data["detail"]["customization_flag"]==1:
                print(">> 옵션 예외상품 (skip) : {} ".format(asin))
                del_proc("D07", asin, catecode)
                time.sleep(sleep_num)
                continue

            if len(option_urls) > 100:
                print(">> 옵션수 Over 상품 (skip) : {} ".format(asin))
                del_proc("D09", asin, catecode)
                time.sleep(sleep_num)
                continue

            img = getProdImg(json_data)
            detail = getProdDetail(json_data)
            option_color_name = getColorOptionName(json_data)
            description = dict()
            description["detail"] = detail
            description["image"] = img

            sort = 1

            goods_uid = ""
            option_kind = "'300'"
            json_data_for=[]
            if len(option_urls) > 1:
                # 색 있음
                if len(size_options) > 0:
                    print(">> (case1) 색 있음 | 사이즈 있음")
                    # 사이즈 있음
                    option_title = option_color_name["name"] + "|" + "사이즈"
                    print(">> option_title : {}".format(option_title))
                    for option_url in option_urls:
                        time.sleep(sleep_num)            
                        driver.get(option_url["option_url"])
                        html = driver.page_source
                        soup = BeautifulSoup(html,'html.parser')
                        # try:
                        #     lang = soup.select_one("a.col-xs-4.global-active").get_text()
                        # except:
                        #     lang = soup.select_one("a.col-xs-4 global-active").get_text()
                        if str(html).find('카테고리별 쇼핑') > -1:
                            lang = "Korea"
                        if lang == "English":
                            changeLang(driver)
                            html = driver.page_source                    
                        json_data_for.append(getPrdData(html))

                    for json_data in json_data_for:
                        price = json_data["getPrice"]["retailPrice"]["amount"]
                        if price_Symbol.find('$') == -1:
                            print(">> price_Symbol : {}".format(price_Symbol))
                            print(">> (before) price : {} | {}".format(price, price_Symbol))
                            price = check_price(price, price_Symbol)
                            print(">> (after) price : {} | {}".format(price, price_Symbol))

                        goods_id = json_data["detail"]["goods_id"]                
                        size_options = getSizeOption(json_data,price_Symbol)
                        img = getProdImg(json_data)
                        detail = getProdDetail(json_data)
                        option_color_name = getColorOptionName(json_data)
                        description = dict()
                        description["detail"] = detail
                        description["image"] = img
                        print(">> goods_id: {} | price : {}".format(goods_id,price))

                        # t_goods 입력 옵션
                        if sort==1:
                            t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id,catecode,cate_code2,asin_url)
                            if mode == "insert":
                                print(">> (case1) MakeTGoodsDic insert")
                                goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                                if str(goods_uid) == "":
                                    print(">> (case1) insertReturnIdx except (Q01) : {}".format(asin))
                                    del_proc("Q01", asin, catecode)
                                    break
                                else:
                                    t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                                    db_con.insert("t_goods_content",t_goods_content_dic)

                            elif mode =="update":
                                print(">> (case1) MakeTGoodsDic update")
                                goods_uid = row[0]
                                if str(goods_uid) == "":
                                    print(">> (case1) insertReturnIdx except (Q01) : {}".format(asin))
                                    del_proc("Q01", asin, catecode)
                                    break
                                db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0]))
                                t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                                db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                                OptionClear(db_con,goods_uid)

                        if str(goods_uid) != "":
                            color_items = []
                            size_items = []
                            for size_option in size_options:
                                color_items.append(option_color_name["value"]+"/"+size_option["name"])
                                size_items.append(PriceMargin(size_option["price"]))
                            color_item = ListToStr(color_items)
                            size_item = ListToStr(size_items)
                            t_goods_option_dic = makeTGoodsOptionDic(goods_uid,option_title,color_item,goods_id,description,sort)
                            option_uid = db_con.insertReturnIdx("t_goods_option",t_goods_option_dic)
                            t_goods_option_item_dic = MakeTGoodsOptionItemDic(option_uid,size_item)
                            db_con.insert("t_goods_option_item",t_goods_option_item_dic)

                        sort += 1

                else:
                    # 사이즈 없음
                    print(">> (case2) 색 있음 | 사이즈 없음")
                    option_title = option_color_name["name"]
                    for option_url in option_urls:
                        time.sleep(sleep_num)                  
                        driver.get(option_url["option_url"])                    
                        html = driver.page_source
                        soup = BeautifulSoup(html,'html.parser')
                        # try:
                        #     lang = soup.select_one("a.col-xs-4.global-active").get_text()
                        # except:
                        #     lang = soup.select_one("a.col-xs-4 global-active").get_text()
                        if str(html).find('카테고리별 쇼핑') > -1:
                            lang = "Korea"
                        if lang == "English":
                            changeLang(driver)
                            html = driver.page_source                    
                        json_data_for.append(getPrdData(html))

                    for json_data in json_data_for:                    
                        price = json_data["getPrice"]["retailPrice"]["amount"]
                        if price_Symbol.find('$') == -1:
                            print(">> (before) price : {} | {}".format(price, price_Symbol))
                            price = check_price(price, price_Symbol)
                            print(">> (after) price : {} | {}".format(price, price_Symbol))

                        goods_id = json_data["detail"]["goods_id"]                
                        size_options = getSizeOption(json_data,price_Symbol)
                        img = getProdImg(json_data)
                        detail = getProdDetail(json_data)
                        option_color_name = getColorOptionName(json_data)
                        description = dict()
                        description["detail"] = detail
                        description["image"] = img

                        if sort==1:
                            t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id,catecode,cate_code2,asin_url)
                            if mode == "insert":
                                print(">> (case2) MakeTGoodsDic insert")
                                goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                                if str(goods_uid) == "":
                                    print(">> (case2) insertReturnIdx excepting (Q01) : {}".format(asin))
                                    del_proc("Q01", asin, catecode)
                                    break
                                else:
                                    t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                                    db_con.insert("t_goods_content",t_goods_content_dic)

                            elif mode =="update":
                                print(">> (case2) MakeTGoodsDic update")
                                goods_uid = row[0]
                                if str(goods_uid) == "":
                                    print(">> (case1) insertReturnIdx except (Q01) : {}".format(asin))
                                    del_proc("Q01", asin, catecode)
                                    break
                                db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0]))
                                t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                                db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                                OptionClear(db_con,goods_uid)  

                        if str(goods_uid) != "":
                            t_goods_option_dic = makeTGoodsOptionDic(goods_uid,option_title,option_color_name["value"],goods_id,description,sort)
                            sort += 1
                            option_uid = db_con.insertReturnIdx("t_goods_option",t_goods_option_dic)
                            t_goods_option_item_dic = MakeTGoodsOptionItemDic(option_uid,PriceMargin(price))
                            db_con.insert("t_goods_option_item",t_goods_option_item_dic)

            else:
                # 색 없음
                if len(size_options) > 0:
                    print(">> (case3) 색 없음 | 사이즈 있음")
                    # 사이즈 있음
                    option_title = "사이즈"
                    t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id,catecode,cate_code2,asin_url)
                    if mode == "insert":
                        print(">> (case3) MakeTGoodsDic insert")
                        goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                        if str(goods_uid) == "":
                            print(">> (case3) insertReturnIdx excepting (skip) : {}".format(asin))
                            del_proc("Q01", asin, catecode)
                        else:
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.insert("t_goods_content",t_goods_content_dic)

                    elif mode =="update":
                        print(">> (case3) MakeTGoodsDic update")
                        goods_uid = row[0]
                        if str(goods_uid) == "":
                            print(">> (case1) insertReturnIdx except (Q01) : {}".format(asin))
                            del_proc("Q01", asin, catecode)
                        else:
                            db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0]))
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                            OptionClear(db_con,goods_uid)    

                    if str(goods_uid) != "":
                        color_items = []
                        size_items = []
                        for size_option in size_options:
                            color_items.append(size_option["name"])
                            size_items.append(PriceMargin(size_option["price"]))

                        color_item = ListToStr(color_items)
                        size_item = ListToStr(size_items)
                        t_goods_option_dic = makeTGoodsOptionDic(goods_uid,option_title,color_item,goods_id,description,sort)
                        option_uid = db_con.insertReturnIdx("t_goods_option",t_goods_option_dic)
                        t_goods_option_item_dic = MakeTGoodsOptionItemDic(option_uid,size_item)
                        db_con.insert("t_goods_option_item",t_goods_option_item_dic)

                else:
                    # 사이즈 없음
                    print(">> (case4) 색 없음 | 사이즈 없음")
                    option_kind = "NULL"
                    t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id,catecode,cate_code2,asin_url)
                    if mode == "insert":
                        print(">> (case4) MakeTGoodsDic insert")
                        goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                        if str(goods_uid) == "":
                            print(">> (case4) insertReturnIdx excepting (skip) : {}".format(asin))
                            del_proc("Q01", asin, catecode)
                    elif mode =="update":
                        print(">> (case4) MakeTGoodsDic update")
                        goods_uid = row[0]
                        if str(goods_uid) == "":
                            print(">> (case1) insertReturnIdx except (Q01) : {}".format(asin))
                            del_proc("Q01", asin, catecode)
                        else:
                            db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0]))
                            OptionClear(db_con,goods_uid)

                    if str(goods_uid) != "":
                        t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                        sql_content = "select Uid from t_goods_content where Uid={}".format(goods_uid)
                        content_row = db_con.select(sql_content)
                        if len(content_row) > 0:
                            db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                        else:
                            if t_goods_content_dic:
                                db_con.insert("t_goods_content",t_goods_content_dic)

            if str(goods_uid) != "":
                t_goods_sub_dic = MakeTGoodsSub(goods_uid)
                t_goods_category_dic = MakeTGoodsCategory(catecode,goods_uid)
                if mode == "insert":
                    db_con.insert("t_goods_sub",t_goods_sub_dic)
                    db_con.insert("t_goods_category", t_goods_category_dic)

                elif mode =="update":
                    db_con.update("t_goods_sub",t_goods_sub_dic,"Uid={}".format(goods_uid))
                    db_con.update("t_goods_category",t_goods_category_dic,"GoodsUid={}".format(goods_uid))

                goodsCodeUpdate(db_con,goods_uid,"T")

            # t_getasin_list = MakeTGetAsin(recomend_json,db_con)
            # for t_getasin_dic in t_getasin_list:
            #     try:
            #         db_con.insert("t_getasin",t_getasin_dic)
            #         db_con.commit()
            #     except:
            #         continue

            db_con.delete("t_getasin","asin={}".format(asin))
            sql = "update update_list2 set now_page = now_page + 1, regdate = getdate() where catecode = '{0}' and proc_ip = '{1}'".format(result['catecode'],currIp)
            db_con.execute(sql)

            if mode == "insert":
                print(">> [{}] INSERT 완료 : {}".format(asin, title))
            elif mode =="update":
                print(">> [{}] UPDATE 완료 : {}".format(asin, title)) 
            print(">> 작업시간 :", time.time() - start)
            print("\n>> ----------------------------------- ")
            # driver.quit()
            ## break

    except Exception as ex:
        print(">> Exception : {}".format(ex))
        print(str(datetime.datetime.now()))
        print(">> asin : {}".format(asin))
        #db_con.rollback()
        #driver.quit()
        traceback.print_exc()
        print(ex)
        return "E02"

    return "0"

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

# urls = []
# urls.append("https://asia.shein.com/DAZY-Mock-Neck-Split-Hem-Tee-Without-Bra-p-13527921-cat-1738.html")
# urls.append("https://asia.shein.com/DAZY-Colorblock-Half-Zip-Crop-Tee-p-11892250-cat-1738.html")
# urls.append("https://asia.shein.com/Studded-Decor-Clear-Acrylic-Frame-Fashion-Glasses-p-2184197-cat-1770.html")
# urls.append("https://asia.shein.com/DAZY-High-Waisted-Wide-Leg-Jeans-p-2614177-cat-1934.html")

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    multiprocessing.freeze_support()
    timecount = 0
    err_cnt = 0
    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
        time.sleep(4)

    # 설정 시간후 종료 fun_timer
    print(">> fun_timer Start ")
    fun_timer()

    # if str(ip).find('222.104.189.18') > -1:
    #     ip="121.150.53.160"

    input_Site = str(sys.argv[1]).strip()
    input_pgKbn = str(sys.argv[2]).strip()
    input_tor = str(sys.argv[3]).strip()
    input_type = str(sys.argv[4]).strip()
    print(">> SITE : {} | PG NAME : {} | Tor: | Type : {}".format(input_type, input_pgKbn, input_tor, input_type))
    if input_Site == "" or input_pgKbn == "" or input_tor == "" or input_type == "":
        print(">> 입력 값을 확인하세요. {} | {} | {} | {}".format(input_Site, input_pgKbn, input_tor, input_type))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    if input_Site != 'trend':
        print(">> 사이트 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    # 설정테이블값 가져오기
    if input_pgKbn == "test":
        dicMangage = MakeManage("goods", input_Site)
    else:
        dicMangage = MakeManage(input_pgKbn, input_Site)
    print('>> [--- (' + str(dicMangage["pgName"]) + ') main start ---] ' + str(datetime.datetime.now()))

    # 버젼체크 (버젼 변경되었으면 새로운 버젼 다운로드 처리)
    if str(currIp).strip() != "222.104.189.18":
        version_check(input_pgKbn)
    time.sleep(1)

    # chrome 드라이브 실행
    now_url = "https://kr.shein.com"
    # try:
    #     print(">> connectDriverOld set ")
    #     driver = trend_func.connectDriverOld(now_url, "", "")
    #     print(">> connectDriverOld set OK ")
    # except Exception as e:
    #     print(">> connectDriverNew set")
    #     driver = trend_func.connectDriverNew(now_url, "", "")
    #     print(">> connectDriverNew set OK ")

    # time.sleep(1)
    # driver.set_window_size(1200, 900)
    # driver.set_window_position(140, 0, windowHandle='current')
    # driver.implicitly_wait(3)
    # time.sleep(2)

    proc_id = ""
    if input_type == "W":
        options = Options()
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    else: 
        try:
            driver, proc_id = connectSubProcess(input_type)
            print(">> connectSubProcess OK ")
        except Exception as e:
            print(">> Exception : {}".format(e))
            try:
                print(">> connectDriverOld set ")
                driver = trend_func.connectDriverOld(now_url, "", input_type)
                print(">> connectDriverOld set OK ")
            except Exception as e:
                print(">> connectDriverOld except")

    # driver.set_window_size(1400, 900)
    # driver.set_window_position(140, 0, windowHandle='current')
    driver.implicitly_wait(3)
    time.sleep(random.uniform(5,7))

    # 1개이상 크롬브라우져가 있을경우 현재브라우져 이외 닫기처리
    if str(currIp).find('222.104.189.18') == -1:
        trend_func.check_browser(driver)
        time.sleep(1)

    # sql_asin = "select top 1 asin, url, catecode, cate_code2 from t_getasin"
    # asin_list = db_con.select(sql_asin)
    # asin_list = [('2184197', 'https://asia.shein.com/Studded-Decor-Clear-Acrylic-Frame-Fashion-Glasses-p-2184197-cat-1770.html', '22007','1'),('13527921', 'https://asia.shein.com/DAZY-Mock-Neck-Split-Hem-Tee-Without-Bra-p-13527921-cat-1738.html', '22007','1'),('11892250', 'https://asia.shein.com/DAZY-Colorblock-Half-Zip-Crop-Tee-p-11892250-cat-1738.html', '22007','1'),('10877746', 'https://asia.shein.com/144pcs-Long-Coffin-Fake-Nail-p-10877746-cat-1869.html', '22007','1')]
    test_asin = ""
    allCnt = 0
    rtn_flg = ""
    cate_skip_cnt = 0
    while True:
        # Test Proc 
        if input_pgKbn == "test":
            # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
            test_asin = input(">>test asin:")
            print(">> test_asin : " + str(test_asin))
            rtn_flg = main_proc_goods(dicMangage, test_asin, currIp)

        elif input_pgKbn == "goods":
            if input_tor == "V": # vpn 사용
                mac_Ip = mac_addr()
                print(">> mac_address : {}".format(mac_Ip))
                try:
                    rtn_flg = main_proc_goods(dicMangage, test_asin, mac_Ip)
                    procWork(mac_Ip)
                except Exception as e:
                    print(">> main_proc_goods Exception e : {}".format(e))
                    rtn_flg = "E"
            else:
                try:
                    rtn_flg = main_proc_goods(dicMangage, test_asin, currIp)
                    procWork(currIp)
                except Exception as e:
                    print(">> main_proc_goods Exception e : {}".format(e))
                    rtn_flg = "E"
            if rtn_flg == "1":
                cate_skip_cnt =  cate_skip_cnt + 1
                if cate_skip_cnt > 2: 
                    print(">> time.sleep(120) ")
                    time.sleep(120)
            else:
                cate_skip_cnt = 0
            print(">> cate_skip_cnt : {}".format(cate_skip_cnt))
            if cate_skip_cnt > 5:
                print(">> 수행할 카테고리 없음 (종료)")
                rtn_flg == "E"

        elif str(input_pgKbn).find("stock_out") > -1:
            print(">> stock_out check ....")
            if input_tor == "V": # vpn 사용
                mac_Ip = mac_addr()
                print(">> mac_address : {}".format(mac_Ip))
                try:
                    rtn_flg = main_proc_stock(dicMangage, test_asin, mac_Ip)
                    procWork_stock(mac_Ip)
                except Exception as e:
                    print(">> main_proc_stock Exception e : {}".format(e))
                    rtn_flg = "E"
            else:
                try:
                    rtn_flg = main_proc_stock(dicMangage, test_asin, currIp)
                    procWork_stock(currIp)
                except Exception as e:
                    print(">> main_proc_stock Exception e : {}".format(e))
                    rtn_flg = "E"
            if rtn_flg == "1":
                print(">> 수행할 데이터 없음 (종료)")
                rtn_flg == "E"

        if rtn_flg == "E":
            break
        if rtn_flg == "1":
            print(">> Next Catgory ")

        driver.refresh()
        time.sleep(1)
        allCnt = allCnt + 1
        if allCnt % 5 == 0:
            # 버젼체크 (버젼 변경되었으면 새로운 버젼 다운로드 처리)
            if str(currIp).strip() != "222.104.189.18":
                version_check(input_pgKbn)
            time.sleep(1)

    db_con.close()
    # driver.quit()
    try:
        driver.quit()
        print(">> driver.quit")
        driver.delete_all_cookies()
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)








