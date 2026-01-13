# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:33:38 2023

@author: allin
"""

import requests
import json
from operator import itemgetter
import re


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
    detail_images = json["goods_imgs"]["detail_image"]
    dic["main_image"] = main_image
    dic["detail_images"] = []
    if detail_images:
        for detail_image in detail_images:
            dic["detail_images"].append(detail_image["origin_image"].replace("//",""))        
    
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
    if goods_url_name[0]=="H":
        goods_url_name = goods_url_name[1:]
    if len(goods_url_name) > 100:
        goods_url_name = "item"
    url = "https://asia.shein.com/" + goods_url_name.replace(" ", "-") + "-p-" + str(goods_id) + "-cat-" + str(cat_id) + ".html"
    
    return url


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

def MakeTGoodsSub(goods_uid, recomend_json):
    dic = dict()
    dic["Uid"] = goods_uid
    dic["Product"] = "'China'"
    dic["gall_list"] = []
    dic["gall_list1"] = []
    dic["gall_list2"] = []
    dic["gall_list3"] = []
    dic["gall_list4"] = []
    for idx,gall in enumerate(recomend_json["info"]["products"]):
        goods_id = gall["goods_id"]
        if idx < 4:
            dic["gall_list"].append(goods_id)
        elif idx < 8:
            dic["gall_list1"].append(goods_id)
        elif idx < 12:
            dic["gall_list2"].append(goods_id)
        elif idx < 16:
            dic["gall_list3"].append(goods_id)            
        elif idx < 20:
            dic["gall_list4"].append(goods_id)  
            
    dic["gall_list"] = "'"+ListToStr(dic["gall_list"])+"'"
    dic["gall_list1"] = "'"+ListToStr(dic["gall_list1"])+"'"
    dic["gall_list2"] = "'"+ListToStr(dic["gall_list2"])+"'"
    dic["gall_list3"] = "'"+ListToStr(dic["gall_list3"])+"'"
    dic["gall_list4"] = "'"+ListToStr(dic["gall_list4"])+"'"
    
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