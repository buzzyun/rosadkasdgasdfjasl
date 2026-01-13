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

import chromedriver_autoinstaller
import DBmodule_NEW
import requests
import json
from operator import itemgetter
import re
import traceback
import get_asin_function
import socket
import random
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import subprocess
import os
import util_func
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

# 상품페이지 - 상품 색 옵션 가져오기(t_goods_content용)
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
def getSizeOption(json):
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
    url = "https://asia.shein.com/" + goods_url_name.replace(" ", "-") + "-p-" + str(goods_id) + "-cat-" + str(cat_id) + ".html"
    
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

def MakeTGoodsDic(title,en_title,price,option_kind,img,goods_id):
    global exchange
    dic = dict()
    dic["DealerID"] = "'rental'"
    dic["GoodsType"] = "'N'"
    # title ban, replace 작업
    title = title.lower()
    title = SetReplaceTitle(title)
    en_title = SetReplaceTitle(en_title)
    title = title.replace("'","''")
    dic["title"] = "'"+title+"'"
    dic["E_title"] = "'"+title+"'"
    dic["DE_title"] = "'"+en_title+"'"
    # price 마진 계산
    dic["Price"] = PriceMargin(float(price))
    dic["OriginalPrice"] = int(float(price)*exchange)
    dic["origin_dollar"] = float(price)
    dic["OptionKind"] = option_kind
    dic["State"] = "'100'"
    dic["ali_no"] = "'"+goods_id+"'"
    dic["Shipping_Fee"] = 0
    dic["imgB"] = "'https://"+img+"'"
    dic["imgM"] = "'https://"+img+"'"
    dic["imgS"] = "'https://"+img+"'"
    dic["naver_img"] = "'https://"+img+"'"
    dic["DeliveryPolicy"] = "'990'"
    
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
    
    return dic

def MakeTGoodsOptionItemDic(option_uid,item):
    dic = dict()
    item = str(item)
    dic["OptionUid"] = option_uid
    dic["item"] = "'"+item+"'"
    dic["sort"] = 1

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
    dic["GoodsCode"] = "'T"+goods_code+"'"
    db_con.update("t_goods",dic,"Uid='{}'".format(goods_uid))
    
    print(dic["GoodsCode"])

def ListToStr(lst):
    string = str(lst).replace("[", "").replace("]", "").replace("'", "")
    
    return string

def ReversSale(num,coupon):
    sale_per = (100-coupon)/100
    sale = num/sale_per
    
    return round(sale)
    
global guarantee_price

# try:
#     taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
#     print(">> taskstr : {}".format(taskstr))  
#     os.system(taskstr)
# except Exception as e:
#     print('>> taskkill Exception (1)')
# else:
#     pass

db_con = DBmodule_NEW.Database('trend')
db_ali = DBmodule_NEW.Database('aliexpress',False)
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
sleep_num = 2


# urls = []
# urls.append("https://asia.shein.com/DAZY-Mock-Neck-Split-Hem-Tee-Without-Bra-p-13527921-cat-1738.html")
# urls.append("https://asia.shein.com/DAZY-Colorblock-Half-Zip-Crop-Tee-p-11892250-cat-1738.html")
# urls.append("https://asia.shein.com/Studded-Decor-Clear-Acrylic-Frame-Fashion-Glasses-p-2184197-cat-1770.html")
# urls.append("https://asia.shein.com/DAZY-High-Waisted-Wide-Leg-Jeans-p-2614177-cat-1934.html")

sql_asin = "select top 1 asin, url, catecode, cate_code2 from t_getasin"
asin_list = db_con.select(sql_asin)
# asin_list = [('2184197', 'https://asia.shein.com/Studded-Decor-Clear-Acrylic-Frame-Fashion-Glasses-p-2184197-cat-1770.html', '22007','1'),('13527921', 'https://asia.shein.com/DAZY-Mock-Neck-Split-Hem-Tee-Without-Bra-p-13527921-cat-1738.html', '22007','1'),('11892250', 'https://asia.shein.com/DAZY-Colorblock-Half-Zip-Crop-Tee-p-11892250-cat-1738.html', '22007','1'),('10877746', 'https://asia.shein.com/144pcs-Long-Coffin-Fake-Nail-p-10877746-cat-1869.html', '22007','1')]

ip = socket.gethostbyname(socket.gethostname())
proc, driver = connectSubProcess()
ip="121.150.53.160"
try:
    while True:
        result = get_asin_function.newlist2(db_con, ip)
        sql_asin = "select top 1 asin, url, catecode, cate_code2 from t_getasin where catecode='{}' order by regdate".format(result['catecode'])
        asin_item = db_con.selectone(sql_asin)

        if not asin_item:
            sql_update_list = "delete from update_list2 where proc_ip = '{0}'".format(ip)
            db_con.execute(sql_update_list)
            print("카테고리 : "+str(result['catecode']) + " asin 없음 다음 카테고리로 넘어감")
            continue
        
        if result["page"] > 100:
            sql_catecode = "select top 1 catecode from T_CATEGORY where IsHidden='F' and lastcate=1 and catecode not in (select CateCode from T_GOODS_CATEGORY group by CateCode) order by catecode"
            row_catecode = db_con.selectone(sql_catecode)
            if row_catecode:
                update_catecode = row_catecode[0]
                sql_update_list = "update update_list2 set catecode='{}', now_page=1 where proc_ip = '{}'".format(update_catecode,ip)
                catecode = row_catecode[0]
                db_con.execute(sql_update_list)
                print("100개 입력 완료 다음 카테고리로 넘어감")
                continue

        asin = asin_item[0]
        catecode = asin_item[2]
        url = "https://asia.shein.com"+asin_item[1]+"&share_from=asia"
        cate_code2 = asin_item[3]
        

        if catecode=="":
            sql = "select CateCode from t_category where lastcate=1 and IsHidden='F' and cate_code2='{}'".format(cate_code2)
            rs = db_con.selectone(sql)
            if rs:                
                catecode = rs[0]
            else:
                print("잘못된 카테코드 skip")
                continue
        sql = "select top 1 UID from t_goods_option where option_code='{}'".format(asin)
        row = db_con.select(sql)
        sql = "select top 1 UID from t_goods where ali_no='{}'".format(asin)
        row2 = db_con.select(sql)
        
        if len(row) == 0 and len(row2) == 0:
            mode = "insert"
        else:            
            mode = "update"
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit() 
            print(asin+" t_goods 상품 존재함 skip")
            continue  
        mode = "insert"  
        # driver = chrom_drive()
        try:
            driver.get(url)
            time.sleep(random.uniform(4,6))
        except:
            print(">> driver.get(url) except ")
            input(">> after check : ")
            driver.get(url)
            time.sleep(random.uniform(4,6))

        time.sleep(1)
        now_url = driver.current_url
        if now_url.find("/risk/") > -1:
            input("캡챠 확인")

        sql = "select minus_opt from t_category where catecode={}".format(catecode)
        row = db_con.selectone(sql)
        if row[0]==1 or row[0]=="1":
            minus_opt = True
        else:
            minus_opt = False        

        html = driver.page_source
        if html.find("Your request is not compliant and has been blocked by us.") > -1:
            stop = input("block")
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
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit()
            # driver.quit()
            print("잘못된 상품 skip")
            time.sleep(sleep_num)
            continue
        
        if json_data["mallStock"]==0:
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit()
            # driver.quit()
            print(asin+"품절상품 skip")
            time.sleep(sleep_num)
            continue
        
        title = json_data["detail"]["goods_name"]
        en_title = json_data["detail"]["goods_url_name"]
        if korlen(title) > 200 or korlen(en_title) > 200:
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit()
            # driver.quit()
            print(asin+"타이틀 글자 수 초과 skip")
            time.sleep(sleep_num)
            continue        
        if SetBanTitle(title):
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit()
            # driver.quit()
            print(asin+"금지어 상품 skip")
            time.sleep(sleep_num)
            time.sleep(sleep_num)
            continue
        
        time_num = random.randint(3, 6)
        time.sleep(time_num)        
        print(asin+" 작업 시작")
        start = time.time()
        
        price = json_data["getPrice"]["retailPrice"]["amount"]
        goods_id = json_data["detail"]["goods_id"]
        cat_id = json_data["detail"]["cat_id"]
        store_code = json_data["detail"]["store_code"]
        option_urls = getOtherOptionUrl(json_data,minus_opt)
        size_options = getSizeOption(json_data)
        if json_data["detail"]["customization_flag"]==1:
            db_con.delete("t_getasin","asin={}".format(asin))
            db_con.commit()            
            print("옵션 예외상품 skip")
            continue
        img = getProdImg(json_data)
        detail = getProdDetail(json_data)
        option_color_name = getColorOptionName(json_data)
        description = dict()
        description["detail"] = detail
        description["image"] = img
        
        sort = 1

        
        option_kind = "'300'"
        json_data_for=[]
        if len(option_urls) > 1:
            # 색 있음
            if len(size_options) > 0:
                # 사이즈 있음
                option_title = option_color_name["name"] + "|" + "사이즈"
                for option_url in option_urls:
                    time.sleep(sleep_num)            
                    driver.get(option_url["option_url"])
                    html = driver.page_source
                    soup = BeautifulSoup(html,'html.parser')
                    try:
                        lang = soup.select_one("a.col-xs-4.global-active").get_text()
                    except:
                        lang = soup.select_one("a.col-xs-4 global-active").get_text()
                    if lang == "English":
                        changeLang(driver)
                        html = driver.page_source                    
                    json_data_for.append(getPrdData(html))
                    
                for json_data in json_data_for:
                    price = json_data["getPrice"]["retailPrice"]["amount"]
                    goods_id = json_data["detail"]["goods_id"]                
                    size_options = getSizeOption(json_data)
                    img = getProdImg(json_data)
                    detail = getProdDetail(json_data)
                    option_color_name = getColorOptionName(json_data)
                    description = dict()
                    description["detail"] = detail
                    description["image"] = img

                    # t_goods 입력 옵션
                    if sort==1:
                        t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id)
                        if mode == "insert":
                            goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.insert("t_goods_content",t_goods_content_dic)
                            
                        elif mode =="update":
                            db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0][0]))
                            goods_uid = row[0][0]
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                            OptionClear(db_con,goods_uid)
                            
                    
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
                option_title = option_color_name["name"]
                for option_url in option_urls:
                    time.sleep(sleep_num)                  
                    driver.get(option_url["option_url"])                    
                    html = driver.page_source
                    soup = BeautifulSoup(html,'html.parser')
                    try:
                        lang = soup.select_one("a.col-xs-4.global-active").get_text()
                    except:
                        lang = soup.select_one("a.col-xs-4 global-active").get_text()
                    if lang == "English":
                        changeLang(driver)
                        html = driver.page_source                    
                    json_data_for.append(getPrdData(html))
                    
                for json_data in json_data_for:                    
                    price = json_data["getPrice"]["retailPrice"]["amount"]
                    goods_id = json_data["detail"]["goods_id"]                
                    size_options = getSizeOption(json_data)
                    img = getProdImg(json_data)
                    detail = getProdDetail(json_data)
                    option_color_name = getColorOptionName(json_data)
                    description = dict()
                    description["detail"] = detail
                    description["image"] = img
                    
                    if sort==1:
                        t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id)
                        if mode == "insert":
                            goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.insert("t_goods_content",t_goods_content_dic)
                            
                        elif mode =="update":
                            db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0][0]))
                            goods_uid = row[0][0]
                            t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                            db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                            OptionClear(db_con,goods_uid)  
                            
    
                    t_goods_option_dic = makeTGoodsOptionDic(goods_uid,option_title,option_color_name["value"],goods_id,description,sort)
                    sort += 1
                    option_uid = db_con.insertReturnIdx("t_goods_option",t_goods_option_dic)
                    t_goods_option_item_dic = MakeTGoodsOptionItemDic(option_uid,PriceMargin(price))
                    db_con.insert("t_goods_option_item",t_goods_option_item_dic)
                    
        else:
            # 색 없음
            if len(size_options) > 0:
                # 사이즈 있음
                option_title = "사이즈"
                t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id)
                if mode == "insert":
                    goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                    t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                    db_con.insert("t_goods_content",t_goods_content_dic)
                    
                elif mode =="update":
                    db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0][0]))
                    goods_uid = row[0][0]
                    t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                    db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                    OptionClear(db_con,goods_uid)    
                    
                
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
                option_kind = "NULL"
                t_goods_dic = MakeTGoodsDic(title,en_title,price,option_kind,img["main_image"],goods_id)
                if mode == "insert":
                    goods_uid = db_con.insertReturnIdx("t_goods",t_goods_dic)
                    
                elif mode =="update":
                    db_con.update("t_goods",t_goods_dic,"Uid={}".format(row[0][0]))
                    goods_uid = row[0][0]
                    OptionClear(db_con,goods_uid)
                    
                    
                t_goods_content_dic = MakeTGoodsContentDic(goods_uid,description)
                sql_content = "select Uid from t_goods_content where Uid={}".format(goods_uid)
                content_row = db_con.select(sql_content)
                if len(content_row) > 0:
                    db_con.update("t_goods_content",t_goods_content_dic,"Uid={}".format(goods_uid))
                    
                else:
                    db_con.insert("t_goods_content",t_goods_content_dic)
                    
        
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
        sql = "update update_list2 set now_page = now_page + 1, regdate = getdate() where catecode = '{0}' and proc_ip = '{1}'".format(result['catecode'],ip)
        db_con.execute(sql)
        db_con.commit()
        #db_con.rollback()

        if mode == "insert":
            print("title : "+title+" 입력 완료")
        elif mode =="update":
            print("title : "+title+" 업데이트 완료")
        print("작업시간 :", time.time() - start)
        # driver.quit()
        break
except Exception as ex:
    print(asin)
    db_con.rollback()
    driver.quit()
    traceback.print_exc()
    print(ex)
    db_con.close()
    # try:
    #     taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
    #     print(">> taskstr : {}".format(taskstr))  
    #     os.system(taskstr)
    # except Exception as e:
    #     print('>> taskkill Exception (1)')
    # else:
    #     pass    
    

db_con.close()
driver.quit()








