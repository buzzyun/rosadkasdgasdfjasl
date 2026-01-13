
import requests
import datetime
import time
import json
import socket
import re
from bs4 import BeautifulSoup
import taobao_func
import sys,os
p = os.path.abspath('.')
sys.path.insert(1, p)
import DBmodule_py
import DBmodule_FR

currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

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

#mssql 쿼리 문 null처리
def getQueryValue(target):
    if target == None :
        result = "NULL"
    else :
        result = "'{0}'".format(target)
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

#db 특수단어 제거
def replaceQueryString(target) :
    result = target.replace("'","")
    result = result.replace("★","").replace("◆","").replace("/","|").replace(","," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("【","(").replace("】",")").replace('"', '').replace("「","(").replace("」",")")
    return str(result).strip()

#db 특수단어 제거
def replaceQueryStringOption(target) :
    result = target.replace("'","`").replace(","," ").replace("正品","").replace("정품"," ").replace("、",".")
    result = result.replace("★","").replace("◆","").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("--","-").replace('"', '`')
    result = result.replace("{","(").replace("}",")").replace("/","|").replace("【","(").replace("】",")").replace("[","(").replace("]",")").replace("「","(").replace("」",")")
    return str(result).strip()

def replaceQueryStringTitle(target) :
    result = target.replace("'","").replace("tmall.com","").replace("- ChinaglobalMall","").replace("- CHINAGLOBALMALL","")
    result = result.replace("★","").replace("◆","").replace("/","|").replace(","," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("amp;","").replace("&#39;","`").replace("&quot;","").replace("【","(").replace("】",")").replace('"', '').replace("「","(").replace("」",")")
    return str(result).strip()

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

    db_ali2 = DBmodule_py.Database('aliexpress', True)
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
def generateOptionString(gDic, option_price_dic, option_dic, d_minus_opt, base_price_tmp, coupon):
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
            #option_value = "(" + str(key) + ")" + replaceQueryString(option_dic[key])
            option_value = replaceQueryStringOption(option_dic[key])
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
                option_marzin_sale_price = option_marzin_sale_price / 2
            else:
                if option_marzin_sale_price < 0:
                    option_marzin_sale_price = 0

            option_marzin_price_sale_dic[key] = option_marzin_sale_price
            #option_value = "(" + str(key) + ")" + replaceQueryString(option_dic[key])
            option_value = replaceQueryStringOption(option_dic[key])
            option_item_str.append(option_value)
            option_item_str.append(str(option_marzin_sale_price))
            option_item.append("/".join(option_item_str))

        #print(">>[{}] {} : {} : [ {} - {} = 차액 {}] ( {} )".format(klow, option_value, value, value, base_price_tmp, diff_sale_price, option_marzin_sale_price))

    #print(">> option_marzin_price_sale_dic : {} ".format(option_marzin_price_sale_dic))    return ",".join(option_item) 
    return ",".join(option_item)


def getDescription(instanceKey, language, headers, itemId):
    description = ""
    url = "http://otapi.net/service-json/GetItemDescription?instanceKey="+str(instanceKey)+"&\
        language=" +str(language)+ "&signature=&timestamp=&sessionId=&itemParameters=&itemId=" +str(itemId)
    res = requests.get(url, headers=headers)
    time.sleep(3)
    if res.status_code != 200:
        print("Can't request Description")
    else:
        #soup = BeautifulSoup(res.text, "html.parser")
        dataResult = json.loads(res.text)
        description = dataResult['OtapiItemDescription']['ItemDescription']
    return str(description)

def getImgCut(img):
    if str(img).find('.png.jpg') > -1:
        img = getparse(str(img),'.png.jpg','.png') #.png.jpg가 두개 있는 경우가 있음 뒷부분 .jpg 제거
    elif str(img).find('.jpg') > -1:
        img = getparse(str(img),'','.jpg') + '.jpg' #.jpg가 두개 있는 경우가 있음 뒷부분 .jpg 제거
    return str(img)

def removeAsin(db_con):
    # D49 : # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리  1000 위안 (15만원) over # D03 : 금지어 
    # D09 : 8000 위안 (150만원) over  # D12 : 1 위안 미만 (skip)  # D47 : 옵션명 불가단어 포함  # S02 : 네이버 노클릭상품  # S01 : stop_update 
    sql = "update T_Category_BestAsin set del_flg = '1' from T_Category_BestAsin where asin in (select asin from T_Category_BestAsin_del where code in ('D49', 'D09', 'D12', 'D47', 'D03', 'S02', 'S01') )"
    db_con.execute(sql)
    print('>> ## update del_flg = 1 (asin) :' + str(sql))


def newlist(db_con, in_ip):
    cateidx = ""
    sql = "select * from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        sql = "select top 1 catecode from T_Category_BestAsin where del_flg is null and catecode not in (select catecode from update_list2) order by up_date"
        row = db_con.selectone(sql)
        if row:
            cateidx = row[0]
            sql = "insert into update_list2 (catecode,proc_ip) values ('{0}','{1}')".format(cateidx, in_ip)
            try:
                db_con.execute(sql)
            except Exception as e:
                print('>> Error newlist ')
                # proc end
                ###################procEnd(db_con, db_ali, in_drive,in_pg)
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

def updateDB_asin(db_con, asin, code, del_flg):
    uSql = " update T_Category_BestAsin set del_flg = '{}', del_flg_date = getdate(), code = '{}' where asin = '{}'".format(del_flg, code, asin)
    print(">> asin[{}] table update : {}".format(asin, uSql))
    db_con.execute(uSql)    

def get_asinset(in_catecode, db_con, db_ali):
    asinset = []
    sql = "select top 100 asin, a.isTmall, t.Uid, isnull(title_tran,''), a.catecode, isnull(a.price, ''), c.bcate \
        , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
        , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0)\
        from T_Category_BestAsin as a inner join T_CATEGORY as c on c.CateCode = a.catecode left join t_goods as t on t.ali_no = a.asin \
        where a.del_flg is null and a.price is not null and stop_update is null and Del_Naver is null and t.api_flg is null \
        and c.sale_ck_new = '1' and a.up_date < '2022-01-01 00:00:00' \
        order by a.up_date asc ".format(in_catecode)
        ## order by newid()".format(in_catecode)

    rs_row = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rs_row:
        print('>> category complete! change catecode :' +str(in_catecode))
        where_condition = " catecode = '{0}'".format(in_catecode)
        db_con.delete('update_list2', where_condition)
        return ""

    for ea_asin in rs_row:
        asinInfoDic = dict()
        Duid = ""
        asin = ea_asin[0]
        isTmall = ea_asin[1]
        Duid = ea_asin[2]
        title_tran = ea_asin[3]
        catecode = ea_asin[4]
        price = ea_asin[5]
        bcate = ea_asin[6]
        db_stop_update = ea_asin[7]
        db_weight = ea_asin[8]
        db_Del_Naver = ea_asin[9]
        db_goodscode = ea_asin[10]
        db_DE_title = ea_asin[11]
        db_title = ea_asin[12]
        db_minus_opt = ea_asin[13]
        db_coupon = ea_asin[14]
        db_cate_weight = ea_asin[15]

        if Duid is None:
            Duid = ""

        if Duid != "" and db_stop_update == '1':
            print(">> stop_update goods : {}".format(asin))
            updateDB_asin(db_con, asin, 'S01', "1")
            continue

        if Duid != "" and db_Del_Naver == '9':
            print(">> Del_Naver 9 (네이버 노클릭상품) : {}".format(asin))
            updateDB_asin(db_con, asin, 'S02', "1")
            continue

        if price == "" or price == 0.0:
            pass #print('>> price 알수 없음 ')
        else:
            # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
            if str(bcate) == '1044' or str(bcate) == '1038' or str(bcate) == '1033':
                if float(price) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
                    print('>> 1000 위안 (15만원) over (skip)')
                    updateDB_asin(db_con, asin, 'D49', "1")
                    continue

            ##### price check #####
            if float(price) < 1:
                print('>> 1 위안 미만 (skip)')
                updateDB_asin(db_con, asin, 'D12', "1")
                continue

            if float(price) > 8000:
                print('>> 8000 위안 (150만원) over (skip)')
                updateDB_asin(db_con, asin, 'D09', "1")
                continue

        if title_tran != "":
            # title 금지어 체크 ###########
            forbidden_flag = checkForbidden_new(title_tran, db_ali)
            if str(forbidden_flag) != "0":
                print('>> checkForbidden_new : '+str(forbidden_flag))
                updateDB_asin(db_con, asin, 'D03', "1")
                continue

        asinInfoDic['asin'] = asin
        asinInfoDic['isTmall'] = isTmall
        asinInfoDic['Duid'] = Duid
        asinInfoDic['title_tran'] = title_tran
        asinInfoDic['catecode'] = catecode
        asinInfoDic['price'] = price
        asinInfoDic['bcate'] = bcate
        asinInfoDic['db_stop_update'] = db_stop_update
        asinInfoDic['db_weight'] = db_weight
        asinInfoDic['db_Del_Naver'] = db_Del_Naver
        asinInfoDic['db_goodscode'] = db_goodscode
        asinInfoDic['db_DE_title'] = db_DE_title
        asinInfoDic['db_title'] = db_title
        asinInfoDic['db_minus_opt'] = db_minus_opt
        asinInfoDic['db_coupon'] = db_coupon
        asinInfoDic['db_cate_weight'] = db_cate_weight
        asinset.append(asinInfoDic)

    return asinset

def get_asinset_test(in_asin, db_con, db_ali):
    asinset = []
    sql = "select top 100 t.ali_no, istmall, t.Uid, title, t.cate_idx, isnull(origin_dollar,''), c.bcate \
        , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
        , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0)\
        from t_goods as t inner join T_CATEGORY as c on c.CateCode = t.cate_idx \
        where ali_no = '{}' ".format(in_asin)
        ## order by newid()".format(in_catecode)

    print('>> ##select all## sql :' + str(sql))
    rs_row = db_con.select(sql)

    for ea_asin in rs_row:
        asinInfoDic = dict()
        Duid = ""
        asin = ea_asin[0]
        isTmall = ea_asin[1]
        Duid = ea_asin[2]
        title_tran = ea_asin[3]
        catecode = ea_asin[4]
        price = ea_asin[5]
        bcate = ea_asin[6]
        db_stop_update = ea_asin[7]
        db_weight = ea_asin[8]
        db_Del_Naver = ea_asin[9]
        db_goodscode = ea_asin[10]
        db_DE_title = ea_asin[11]
        db_title = ea_asin[12]
        db_minus_opt = ea_asin[13]
        db_coupon = ea_asin[14]
        db_cate_weight = ea_asin[15]

        if Duid is None:
            Duid = ""

        if Duid != "" and db_stop_update == '1':
            print(">> stop_update goods : {}".format(asin))
            updateDB_asin(db_con, asin, 'S01', "1")
            continue

        if Duid != "" and db_Del_Naver == '9':
            print(">> Del_Naver 9 (네이버 노클릭상품) : {}".format(asin))
            updateDB_asin(db_con, asin, 'S02', "1")
            continue

        # if price == "" or price == 0.0:
        #     pass #print('>> price 알수 없음 ')
        # else:
        #     # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
        #     if str(bcate) == '1044' or str(bcate) == '1038' or str(bcate) == '1033':
        #         if float(price) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
        #             print('>> 1000 위안 (15만원) over (skip)')
        #             updateDB_asin(db_con, asin, 'D49', "1")
        #             continue

        #     ##### price check #####
        #     if float(price) < 1:
        #         print('>> 1 위안 미만 (skip)')
        #         updateDB_asin(db_con, asin, 'D12', "1")
        #         continue

        #     if float(price) > 8000:
        #         print('>> 8000 위안 (150만원) over (skip)')
        #         updateDB_asin(db_con, asin, 'D09', "1")
        #         continue

        if title_tran != "":
            # title 금지어 체크 ###########
            forbidden_flag = checkForbidden_new(title_tran, db_ali)
            if str(forbidden_flag) != "0":
                print('>> checkForbidden_new : '+str(forbidden_flag))
                updateDB_asin(db_con, asin, 'D03', "1")
                continue

        asinInfoDic['asin'] = asin
        asinInfoDic['isTmall'] = isTmall
        asinInfoDic['Duid'] = Duid
        asinInfoDic['title_tran'] = title_tran
        asinInfoDic['catecode'] = catecode
        asinInfoDic['price'] = price
        asinInfoDic['bcate'] = bcate
        asinInfoDic['db_stop_update'] = db_stop_update
        asinInfoDic['db_weight'] = db_weight
        asinInfoDic['db_Del_Naver'] = db_Del_Naver
        asinInfoDic['db_goodscode'] = db_goodscode
        asinInfoDic['db_DE_title'] = db_DE_title
        asinInfoDic['db_title'] = db_title
        asinInfoDic['db_minus_opt'] = db_minus_opt
        asinInfoDic['db_coupon'] = db_coupon
        asinInfoDic['db_cate_weight'] = db_cate_weight
        asinset.append(asinInfoDic)

    return asinset

def getGoodsApi(instanceKey, language, header, asinInfo, gDic, db_price):

    itemId = asinInfo['asin']
    isTmall = asinInfo['isTmall']
    print(">> isTmall : {}".format(isTmall))
    base_url = "http://otapi.net/service-json/BatchGetItemFullInfo?instanceKey="+str(instanceKey)+"&language=" +str(language)+ "&signature=&timestamp=&sessionId=&itemParameters=&itemId=" +str(itemId) + \
    "&blockList=Description&blockList=RootPath&blockList=DeliveryCosts&blockList=ProviderReviews&blockList=MostPopularVendorItems16"

    res = requests.get(base_url, headers=header)
    time.sleep(4)
    if res.status_code != 200:
        print("Can't request website")
        return "E99"
    else:
        #soup = BeautifulSoup(res.text, "html.parser")
        dataResult = json.loads(res.text)
        #print(dataResult)
        print("\n")
        if dataResult['ErrorCode'] != "Ok":
            print(">> {} : Item Not Found ".format(itemId))
            print('>> 품절 (Skip) : {}'.format(itemId))
            return "D01" # 품절

        base_min_price = 0
        base_top_price = 0
        option_val_count = 0
        option_max_count = 100

        result_dic = dict()
        result = dataResult['Result']

        RootPath = ""
        if result.get('RootPath'):
            idx = 0
            RootPath = result['RootPath']
            RootPathContents = result['RootPath']['Content']
            for vRootPath in RootPathContents:
                if vRootPath:
                    vRootPath_ExternalId = ""
                    vRootPath_ParentId = ""
                    idx = idx + 1
                    vRootPath_id = vRootPath['Id']
                    if vRootPath.get('ExternalId'): vRootPath_ExternalId = vRootPath['ExternalId']
                    vRootPath_IsParent = vRootPath['IsParent']
                    if vRootPath.get('ParentId'): vRootPath_ParentId = vRootPath['ParentId']
                    vRootPath_Name = vRootPath['Name']
                    print(">>({}) vRootPath : {} | [ {} ] | {} | {} | {}  ".format(idx, vRootPath_id, vRootPath_ExternalId, vRootPath_IsParent , vRootPath_ParentId, vRootPath_Name))

        ProviderReviews = ""
        if result.get('ProviderReviews'):
            idx = 0
            ProviderReviews = result['ProviderReviews']
            ProviderReviewsContents = result['ProviderReviews']['Content']
            for vReview in ProviderReviewsContents:
                if vReview:
                    idx = idx + 1
                    vReview_id = vReview['ItemId']
                    vReview_ConfigurationId = vReview['ConfigurationId']
                    vReview_Content = vReview['Content']
                    vReview_Rating = vReview['Rating']
                    vReview_CreatedDate = vReview['CreatedDate']
                    vReview_UserNick = vReview['UserNick']
                    print(">>({}) vReview : {} | [ {} ] | {} | {} | {} | {} ".format(idx, vReview_id, vReview_ConfigurationId, vReview_Content , vReview_Rating, vReview_CreatedDate, vReview_UserNick))

        VendorItems = ""
        if result.get('VendorItems'):  
            idx = 0
            VendorItems = result['VendorItems']
            VendorItemsContents = result['VendorItems']['Content']
            for vItem in VendorItemsContents:
                if vItem:
                    idx = idx + 1
                    vItem_id = vItem['Id']
                    vItem_Title = vItem['Title']
                    vItem_CategoryId = vItem['CategoryId']
                    vItem_ExternalCategoryId = vItem['ExternalCategoryId']
                    vItem_OriginalPrice = vItem['Price']['OriginalPrice']
                    print(">>({}) vItem : {} | [ {} ] | {} | {} | {} ".format(idx, vItem_id, vItem_OriginalPrice, vItem_Title , vItem_CategoryId, vItem_ExternalCategoryId))

        #print(">> VendorItems : {}".format(VendorItems))
        result_item = result['Item']
        Id = result_item['Id']
        Title = result_item['Title']
        OriginalTitle = result_item['OriginalTitle']
        CategoryId = result_item['CategoryId']
        ExternalCategoryId = result_item['ExternalCategoryId']

        print(">> Id : {}".format(Id))
        print(">> Title : {}".format(Title))
        print(">> OriginalTitle : {}".format(OriginalTitle))
        print(">> CategoryId : {}".format(CategoryId))
        print(">> ExternalCategoryId : {}".format(ExternalCategoryId))

        Description = ""
        BrandId = ""
        BrandName = ""
        FeaturedValues = ""
        FeaturesTmp = ""
        if result_item.get('BrandId'):  BrandId = result_item['BrandId']  
        if result_item.get('BrandName'):  BrandName = result_item['BrandName']
        if result_item.get('Description'):  Description = result_item['Description']
        if result_item.get('FeaturedValues'):  FeaturedValues = result_item['FeaturedValues']
        if result_item.get('Features'):  FeaturesTmp = result_item['Features']  

        print(">> BrandId : {}".format(BrandId))
        print(">> BrandName : {}".format(BrandName))
        print(">> FeaturedValues : {}".format(FeaturedValues))
        print(">> FeaturesTmp : {}".format(FeaturesTmp))
        print(">> Description : {}".format(Description))
        

        TaobaoItemUrl = result_item['TaobaoItemUrl']  
        MainPictureUrl = result_item['MainPictureUrl']  
        StuffStatus = result_item['StuffStatus']   #Item condition - New: New | Unused: Unused | Second: Second-hand | Another: Another
        print(">> TaobaoItemUrl : {}".format(TaobaoItemUrl))
        print(">> StuffStatus : {}".format(StuffStatus))

        if str(StuffStatus) == "New":
            print(">> New (새상품) : {}".format(StuffStatus))
        else:
            print(">> (Buy used) Unsellable product : {}".format(StuffStatus))
            return "D04"

        mainPrice = result_item['Price']['OriginalPrice']
        MarginPrice = result_item['Price']['MarginPrice']
        if float(mainPrice) != float(MarginPrice):
            print(">>(확인필요) mainPrice : {} / MarginPrice : {}".format(mainPrice, MarginPrice))
        DeliveryPrice = result_item['Price']['DeliveryPrice']['OriginalPrice']
        if float(DeliveryPrice) > 0:
            print(">> DeliveryPrice : {}".format(DeliveryPrice))
            result_dic['taobao_shipping'] = 'T'
        else:
            result_dic['taobao_shipping'] = 'F'
        Pictures = result_item['Pictures']  
        Attributes = result_item['Attributes']     
        ConfiguredItems = result_item['ConfiguredItems']

        Weight = "0"
        Actual_Weight = "0"
        if result_item.get('WeightInfos'):
            if result_item.get('WeightInfos') != []:
                Weight = result_item['WeightInfos'][0]['Weight']
        if result_item.get('ActualWeightInfo'):    
            Actual_Weight = result_item['ActualWeightInfo']['Weight']
        if float(Weight) > 0:
            print(">> Weight : {}".format(Weight))
        if float(Actual_Weight) > 0:
            print(">> Actual_Weight : {}".format(Actual_Weight))
        print(">> mainPrice : {}".format(mainPrice))
        print(">> MarginPrice : {}".format(MarginPrice))

        # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
        if str(asinInfo['bcate']) == '1044' or str(asinInfo['bcate']) == '1038' or str(asinInfo['bcate']) == '1033':
            if float(mainPrice) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
                print('>> 1000 위안 (15만원) over (skip)')
                return "D49" + "( 1000 위안 (15만원) over 카테고리 ( " + str(mainPrice) + " 위안))"

        ##### price check #####
        if float(mainPrice) < 1:
            print('>> 1 위안 미만 (skip)')
            return "D12" + " ( " + str(mainPrice) + " ) "  # 1 위안 미만

        if float(mainPrice) > 8000:
            print('>> 8000 위안 (150만원) over (skip)')
            return "D09" + " ( " + str(mainPrice) + " 위안) "  # 8000 위안 over

        mainImg = getImgCut(MainPictureUrl)
        print(">> Main Img : {}".format(mainImg))

        other_img_set = []
        if Pictures:
            for ea_other_img in Pictures:
                ea_img = ea_other_img['Large']['Url']
                ea_img = getImgCut(ea_img)
                other_img_set.append(ea_img)
            print(">> other_img_set : {}".format(other_img_set))

        result_dic['ali_no'] = Id
        result_dic['catecode'] = asinInfo['catecode']
        result_dic['istmall'] = asinInfo['isTmall']
        result_dic['price'] = mainPrice
        result_dic['price_tmp'] = float(mainPrice)
        result_dic['imgB'] = mainImg
        result_dic['other_img_set'] = other_img_set
        result_dic['BrandName'] = BrandName
        result_dic['CategoryId'] = CategoryId
        result_dic['ExternalCategoryId'] = ExternalCategoryId
        result_dic['description'] = Description

        base_min_price = mainPrice
        base_top_price = mainPrice
        
        shipping_weight = float(asinInfo['db_weight'])
        if shipping_weight < float(asinInfo['db_cate_weight']):
            shipping_weight = float(asinInfo['db_cate_weight'])
        if float(Actual_Weight) > shipping_weight:
            result_dic['shipping_weight'] = float(Actual_Weight)
        else:
            result_dic['shipping_weight'] = shipping_weight

        option_image_dic = dict()
        features = ""
        features_org = ""
        if Attributes:
            for ea_item in Attributes:
                ImageUrl = ""
                #print(">> ea_item[{}] : {}".format(opt_cnt, ea_item))
                f_pid = ea_item['Pid']
                f_vid = ea_item['Vid']
                PropertyName = ea_item['PropertyName']
                PropertyValue = ea_item['Value']

                if str(f_pid).isdigit() == True:
                    if ea_item.get('ImageUrl'):
                        ImageUrl = ea_item['ImageUrl']
                        image_name = ea_item['Value']
                        option_image_dic[image_name] = ImageUrl
                        print(">> ImageUrl : {} | {}".format(image_name, ImageUrl))
                    else:
                        pass
                        #print(">> ImageUrl 존재 안함 ")
                else:
                    if str(features).find(PropertyName) > -1:
                        features = features + '  ' + PropertyValue
                    else:
                        features = features + str('<li> ') + PropertyName + str(' : ') + PropertyValue + str('</li>')
                    if str(features_org).find(f_pid) > -1:
                        features_org = features_org + '  ' + f_vid
                    else:
                        features_org = features_org + str('<li> ') + f_pid + str(' : ') + f_vid + str('</li>')
                    #features_org = features_org + str('● ') + f_pid + str(' : ') + f_vid + "\n"
        
        print("\n>> option_image_dic : \n{}".format(option_image_dic))
        print("\n>> features : \n{}".format(features))
        print("\n>> features_org : \n{}".format(features_org))
        if features == "" and BrandName != "":
            features = str('● Brand : ') + BrandName 
        result_dic['feature'] = features

        option_check = ""
        option_list = []
        option_value_dic = dict()
        option_price_dic = dict()
        opt_cnt = 0
        if ConfiguredItems:
            print("\n>> Option item :\n")
            option_check = "1"
            option_min_price = 0
            option_max_price = 0
            result_dic['OptionKind'] = '300'
            result_dic['many_option'] = '1'
            for ea_value in ConfiguredItems:
                option_dic = dict()
                opt_cnt = opt_cnt + 1
                #print(">> ea_value[{}] : {}".format(opt_cnt, ea_value))
                val_id = ea_value['Id']
                Quantity = ea_value['Quantity'] # 현재 구성의 항목 수량
                SalesCount = ea_value['SalesCount'] # 품목 판매 건수
                Configurators = ea_value['Configurators']
                valPrice = ea_value['Price']['OriginalPrice'] # 공급자의 원래 가격

                if float(Quantity) == 0:
                    print("({}) [{}] Sold Out ".format(opt_cnt, val_id))
                else:
                    option_dic['option_id'] = val_id
                    option_dic['option_price'] = valPrice
                    option_dic['option_qty'] = Quantity
                    option_price_dic[val_id] = valPrice
                    option_dic['option_stock'] = Quantity
                    option_name = ""
                    option_code = ""

                    #옵션 가격 처리
                    if option_min_price == 0 :
                        option_min_price = valPrice
                    else:
                        if option_min_price > valPrice:
                            option_min_price = valPrice
                    if option_max_price == 0 :
                        option_max_price = valPrice
                    else:
                        if option_max_price < valPrice:
                            option_max_price = valPrice                    

                    for ea_val in Configurators:
                        c_Pid = ea_val['Pid']
                        c_Vid = ea_val['Vid']
                        option_code = c_Pid + ":" + c_Vid
                        if Attributes:
                            for ea_item in Attributes:
                                #print(">> ea_item[{}] : {}".format(opt_cnt, ea_item))
                                a_pid = ea_item['Pid']
                                a_Vid = ea_item['Vid']
                                if str(a_pid).isdigit() == True:
                                    if c_Pid == a_pid and c_Vid == a_Vid:
                                        IsConfigurator = ea_item['IsConfigurator']
                                        if option_name != "":
                                            option_name = option_name + " | " + ea_item['Value']
                                            PropertyName = PropertyName + " | " + ea_item['PropertyName']
                                            org_option_name = org_option_name + " | " + ea_item['OriginalValue']
                                            option_code = option_code + ":" + a_pid + ":" + a_Vid
                                        else:
                                            option_name = ea_item['Value']
                                            PropertyName = ea_item['PropertyName']
                                            org_option_name = ea_item['OriginalValue']
                                            option_code = a_pid + ":" + a_Vid
                                        break

                    if str(org_option_name).find('定金') > -1: # 보증금 체크
                        print('>> 定金 (보증금) {}'.format(itemId))
                        return "D47"
                    if str(org_option_name).find('尾款') > -1: # 결제
                        print('>> 尾款 (결제) {}'.format(itemId))
                        return "D47"
                    if org_option_name.find("화물") > -1 or org_option_name.find("계약") > -1 or org_option_name.find("보증") > -1 or org_option_name.find("예약") > -1 or org_option_name.find("경매") > -1:
                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                        return "D47"
                    if org_option_name.lower().find("guarantee") > -1 or org_option_name.find("reservation") > -1 or org_option_name.find("contract") > -1 or org_option_name.find("freight") > -1 or org_option_name.find("auction") > -1:
                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                        return "D47"                        

                    option_name = replaceQueryStringOption(option_name)
                    option_val_count = option_val_count + 1
                    option_dic['option_name'] = option_name.strip()
                    option_dic['option_originalname'] = org_option_name
                    option_dic['option_code'] = option_code
                    option_value_dic[val_id] = option_name
                    option_list.append(option_dic)
                    print("({}) [{}] {}  ( {} ) [ 수량:{} ]  [ {} ]  {}".format(opt_cnt, val_id, option_name , valPrice , Quantity , option_code, org_option_name))

            if option_val_count == 0:
                # No Option
                print(">> Ooption_val_count = 0 : {}".format(itemId))
                print('>> Ooption_val_count = 0 (Option sold out) ')
                return "D07"

            print(">> Option_val_count : {}".format(option_val_count))
            print(">> option_value_dic : {}".format(option_value_dic))
            print(">> option_price_dic : {}".format(option_price_dic))
            print(">> option_image_dic : {}".format(option_image_dic))

            min_price = min(option_price_dic.values())
            top_price = max(option_price_dic.values())
            print(">> min_price : {}".format(min_price))
            print(">> top_price : {}".format(top_price))
            if min_price == 0 or min_price == 0.0:
                pass
            else:
                base_min_price = min_price
            if top_price == 0 or top_price == 0.0:
                pass
            else:
                base_top_price = top_price

        else:
            print("\n>> No Option Goods \n")
            option_check = "0"
            result_dic['OptionKind'] = None
            result_dic['many_option'] = '0'

        if asinInfo['db_minus_opt'] == "1": # 마이너스 옵션으로 set
            base_price_tmp = float(base_top_price)
            result_dic['price'] = float(base_top_price)
            result_dic['price_tmp'] = float(base_top_price)        
            print('>> 마이너스 옵션 set :' +str(base_price_tmp))
        else:
            base_price_tmp = float(base_min_price)
            result_dic['price'] = float(base_min_price)
            result_dic['price_tmp'] = float(base_min_price)        
            print('>> 플러스 옵션 set :' +str(base_price_tmp))

        d_coupon = asinInfo['db_coupon']
        tmp_coupon = d_coupon
        if d_coupon is None or d_coupon == "" or d_coupon == 0:
            tmp_coupon = gDic['py_coupon']

        result_dic['minus_opt'] = str(asinInfo['db_minus_opt'])
        result_dic['coupon'] = str(tmp_coupon)
        print('>> (DB) goods minus_opt : '+str(result_dic['minus_opt']))

        ########### title Check ###########
        Title = Title.replace('정품','').replace("'","`")
        result_dic['DE_title'] = Title
        Title = replaceTitle(Title, db_ali)
        Title = str(Title).replace("  ", " ").strip()
        print('>> tran_title (final) : ' + str(Title[:80]))
        if str(Title).strip() == "":
            print('>> No Title ')
            return "D02"
        if len(Title) < 5:
            print('>> Title len < 5 ')
            return "D02"

        # title 금지어 체크 ###########
        forbidden_flag = checkForbidden_new(Title, db_ali)
        if str(forbidden_flag) != "0":
            print('>> checkForbidden_new : '+str(forbidden_flag))
            return "D03 :" + " ( " + forbidden_flag[2:] + " ) "

        # originalprice
        originalprice = 0
        if asinInfo['db_minus_opt'] == '1':
            originalprice = float(result_dic['price']) * float(gDic['py_exchange_Rate'])
            print(">> originalprice ( {} * {} ) : {}".format(result_dic['price'],gDic['py_exchange_Rate'],originalprice))
        else:
            originalprice = float(result_dic['price_tmp']) * float(gDic['py_exchange_Rate'])
            print(">> originalprice ( {} * {} ) : {}".format(result_dic['price_tmp'],gDic['py_exchange_Rate'],originalprice))

        # 배대지 배송비
        delievey_fee = 5900 #
        delievey_fee = float(getDeliveryFee(gDic, shipping_weight))
        delievey_fee = round(delievey_fee)
        print(">> delievey_fee : {} ".format(delievey_fee))

        # 타오바오 유료배송비
        taobao_shipping_fee = float(DeliveryPrice) * float(gDic['py_exchange_Rate']) * 2
        taobao_shipping_fee = round(taobao_shipping_fee)
        result_dic['taobao_shipping_fee'] = taobao_shipping_fee      
        print(">> taobao_shipping_fee : {} ".format(taobao_shipping_fee))

        ########### goodsmoney ###########
        goodsmoney = 0
        goodsmoney = getWonpirce(gDic, base_price_tmp)
        print(">> goodsmoney (마진플러스): {} + (배대지) {} + (유료배송) {} ".format(goodsmoney, delievey_fee, taobao_shipping_fee))
        goodsmoney = goodsmoney + delievey_fee + taobao_shipping_fee
        goodsmoney = int(round(goodsmoney, -2))
        print(">> goodsmoney (Sum) ({}) ".format(goodsmoney))

        if float(goodsmoney) < 23000:
            goodsmoney = 23000
            print('>> goodsmoney 23,000원 이하 -> 23,000 set: ' + str(goodsmoney)) 
        sale_goodsmoney = int(goodsmoney) * ((100-tmp_coupon) / 100)
        print('>> (sale price) : ' + str(sale_goodsmoney)) 
        marjin = sale_goodsmoney - (originalprice + (delievey_fee/2))
        print('>> (sale marjin) : {} ( {} %)'.format(marjin, round((marjin/sale_goodsmoney * 100),2)))

        if goodsmoney >= 2500000:
            print('>> goodsmoney Over : '+str(goodsmoney))
            return "D09 :" + " ( " + str(goodsmoney) + "원)"

        result_dic['forbidden'] = 'F'                    
        result_dic['title'] = Title
        result_dic['OriginalPrice'] = originalprice
        result_dic['delivery_fee'] = delievey_fee
        result_dic['goodsmoney'] = goodsmoney

        if option_check == "1":
            result_dic['option_price_dic'] = option_price_dic
            result_dic['option_value_dic'] = option_value_dic
            result_dic['option_img_dic'] = option_image_dic
            result_dic['option_max_min_diff'] = float(option_max_price) - float(option_min_price)

            # 옵션 조합 
            option_item = generateOptionString(gDic, option_price_dic, option_value_dic, asinInfo['db_minus_opt'], base_price_tmp, tmp_coupon)
            #print(">> Option_item : {}".format(option_item))
            if option_item.find("/0") == -1:
                print('>> option_value check (0원 옵션 없음) : {}'.format(itemId))
                return "D07"
            if option_item.find("화물") > -1 or option_item.find("계약") > -1 or option_item.find("보증") > -1 or option_item.find("예약") > -1 or option_item.find("경매") > -1:
                print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                return "D47"
            if option_item.lower().find("guarantee") > -1 or option_item.find("reservation") > -1 or option_item.find("contract") > -1 or option_item.find("freight") > -1 or option_item.find("auction") > -1:
                print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                return "D47"

            option_item = option_item.replace("`","")
            print("\n>> option_item : {}".format(option_item))
            result_dic['Items'] = getQueryValue(option_item)

        # description = getDescription(instanceKey, language, headers, itemId)
        # print("\n\n>> description : {}".format(description))

        result_dic['api_flg'] = '1'

        rtnFlg = taobao_func.setDB_proc(itemId, result_dic, db_con, gDic['py_pgName'], asinInfo['Duid'], db_price)
        if rtnFlg[:2] != "0@":
            if rtnFlg == "D01":
                print(">> ## t_goods Option /0 없음 에러 (품절처리 필요)  ##")
                return "D01"
            else:
                print('>> setDB error --> DB check Rollback ')
                sql = "select top 1 uid,IsDisplay,OptionKind from t_goods where ali_no = '{0}'".format(itemId)
                row = db_con.selectone(sql)
                if not row:
                    print(">> ## t_goods Insert No goods (OK) ##")
                else:
                    DUid = row[0]
                    DIsDisplay = row[1]
                    DOptionKind = row[2]
                    # 상품 삭제처리 
                    #taobao_func.setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
                    # print('\n >> t_goods Insert (delete)')
                return str(rtnFlg) # exit

    return "0"

def proc_Main(instanceKey, language, headers, goods_dic, db_con, db_ali, db_price):

    
    pgName = goods_dic['py_pgFilename']
    # catecode = ""
    # loofCnt = 0
    # while loofCnt < 10:
    #     catecode = newlist(db_con, currIp)
    #     if catecode != "":
    #         break
    #     loofCnt = loofCnt + 1
    # if catecode == "":
    #     print(">> catecode 없습니다. ")

    test_asin = input("Test Asin :")
    # asin get
    get_asin_list = []
    get_asin_list = get_asinset_test(test_asin, db_con, db_ali)
    print(len(get_asin_list))
    if len(get_asin_list) == 0:
        print('>> test_asin : ' + str(test_asin))
        return "1"

    cnt_main = 0
    for ea_item in get_asin_list:
        print("\n\n>> --------------------------------------------------------------------------------")
        cnt_main = cnt_main + 1
        asin = ea_item['asin']
        guid = ea_item['Duid']
        istmall = ea_item['isTmall']
        if asin == "":
            print(">> No itemId Check please : {}".format(ea_item))
            continue
        if guid:
            print(">> ({}) asin : {}  | DB 존재 상품 : {}".format(cnt_main, asin, guid))
        else:
            print(">> ({}) asin : {}  | New 상품 ".format(cnt_main, asin))

        rtnChk = getGoodsApi(instanceKey, language, headers, ea_item, goods_dic, db_price)
        print('>> [ rtnChk ] : ' + str(rtnChk))
        if rtnChk[:1] == "0" or rtnChk[:1] == "D" or rtnChk[:1] == "C" or rtnChk[:1] == "S" or rtnChk[:1] == "Q" or rtnChk[:1] == "T" or rtnChk[:1] == "E":
            print('>> proc_asin_parse_brower (OK) ')
        else:
            rtnChk = "E01"

        rtnChk_no = ""
        rtnChk_no = str(rtnChk[:3])
        if rtnChk_no == "E99":
            print('>> E99 (api) Exit : ' + str(rtnChk_no))
            # taobao_func.procLogSet(db_con, pgName, " ( E99 ) api exit - asin: " + str(asin))
            rtnChk = "E99"
            break

        if rtnChk_no[:1] == "D":
            c_Errcnt = 0
            print('>> # Unsellable product (asin delete) : ' + str(rtnChk))
        elif rtnChk_no == "S01":
            print('>> # stop upadte (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "S02":
            print('>> # naver noclick goods (SKIP) : ' + str(rtnChk))
        elif rtnChk_no == "Q01":  # setDB ( Insert )
            print('>> # SetDB  Insert  : ' + str(rtnChk))
        elif rtnChk_no == "Q02":  # setDB ( Update )
            print('>> # SetDB  Update  : ' + str(rtnChk))
        elif rtnChk_no == "E01":
            print('>> # error : ' + str(rtnChk))
        elif rtnChk_no == "E99":
            print('>> # Error : ' + str(rtnChk))
        elif rtnChk_no == "0":
            c_Errcnt = 0
        else:
            print('>> # rtnChk_no : ' + str(rtnChk))


    if rtnChk == "E99":
        return rtnChk
    return "0"

if __name__ == '__main__':
    
    print(str(datetime.datetime.now()))
    timecount = 0
    language = "en"
    language = "ko"
    instanceKey = "1a8389aa-f246-4e24-8e87-de6f89806c6e"
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    # 661896067061 diposit_price 
    #itemId = "37719981982" # 옵션 / 품절항목 포함 , "520795434992" # 무게 -- api 반영안된것 같음 , "530419407507" # 품절코드,
    #itemId = "641026237447"  # tmall 상품 (옵션4개), 573452270641 # tmall (옵션없음), 41127522499 # 옵션없음
    db_con = DBmodule_FR.Database('taobao')
    db_ali = DBmodule_FR.Database('aliexpress')
    db_FS = DBmodule_FR.Database('freeship')
    db_price = DBmodule_FR.Database('naver_price')

    # 불필요한 asin 제거
    removeAsin(db_con)

    input_pgKbn = "goods"
    goods_dic = dict()
    if input_pgKbn == "test":
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon from python_version_manage where name = 'goods'"
    else:
        sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon from python_version_manage where name = '{}'".format(input_pgKbn)
    rs = db_con.selectone(sql)
    if rs:
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        goods_dic['py_now_url'] = str(rs[2]).strip()
        goods_dic['py_now_url2'] = str(rs[3]).strip()
        goods_dic['py_sql1'] = str(rs[4]).replace("`","'")
        goods_dic['py_sql2'] = str(rs[5]).replace("`","'")
        goods_dic['py_sql3'] = str(rs[6]).replace("`","'")
        goods_dic['py_exchange_Rate'] = str(rs[7]).strip()
        goods_dic['py_dollar_exchange'] = str(rs[8]).strip()
        goods_dic['py_withbuy_cost'] = str(rs[9]).strip()
        goods_dic['py_coupon'] = str(rs[10]).strip()

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName

        roofCnt = 0
        while roofCnt < 500:
            roofCnt = roofCnt + 1
            print(">> main mainRtn : {}".format(roofCnt))
            mainRtn = proc_Main(instanceKey, language, headers, goods_dic, db_con, db_ali, db_price)
            if mainRtn == "1":
                print(">> catecode parsing complete ")
                flgProc = "1"
            elif mainRtn == "E99":
                print(">> E99 exit ")
                flgProc = "1"
            time.sleep(2)

    db_con.close()
    db_ali.close()
    db_FS.close()
    # itemList = ['657363309435','661896067061','37719981982','520795434992','530419407507','641026237447','41127522499','44563078644','44947785655','632453787322','45267939973']
    input(">> Key : ")