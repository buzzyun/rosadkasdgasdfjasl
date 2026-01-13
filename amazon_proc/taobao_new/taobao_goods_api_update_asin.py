
import requests
import datetime
import time
import json
import socket
import urllib
import os
import sys
p = os.path.abspath('.')
sys.path.insert(1, p)
from dbCon import DBmodule_FR
import taobao_func

in_ver = "9.41"
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))

def version_check(db_con, db_ali, in_ver, in_pgFilename, in_pgKbn):

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
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)
            time.sleep(60)
            print(">> time.sleep(60)")
            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))
            if fileSize > 5000000:
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
                fname = taobao_func.getparseR(fname,"\\","")
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

    return "0"

def getImgCut(img):
    if str(img).find('.png.jpg') > -1:
        img = taobao_func.getparse(str(img),'.png.jpg','.png') #.png.jpg가 두개 있는 경우가 있음 뒷부분 .jpg 제거
    elif str(img).find('.jpg') > -1:
        img = taobao_func.getparse(str(img),'','.jpg') + '.jpg' #.jpg가 두개 있는 경우가 있음 뒷부분 .jpg 제거
    return str(img)

def removeAsin(db_con):
    # D49 : # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리  1000 위안 (15만원) over # D03 : 금지어 
    # D09 : 8000 위안 (150만원) over  # D12 : 1 위안 미만 (skip)  # D47 : 옵션명 불가단어 포함  # S02 : 네이버 노클릭상품  # S01 : stop_update 
    # sql = "update T_Category_BestAsin set del_flg = '1' from T_Category_BestAsin where asin in (select asin from T_Category_BestAsin_del where code in ('D49', 'D09', 'D12', 'D47', 'D03', 'S02', 'S01') )"
    sql = "delete from T_Category_BestAsin where asin in (select asin from T_Category_BestAsin_del where code in ('D49', 'D09', 'D12', 'D47', 'D03', 'S02', 'S01') )"
    db_con.execute(sql)
    print('>> ## delete del_flg = 1 (asin) :' + str(sql))

def procWork(db_con, in_ip):
    print('>> procWork : ' + str(datetime.datetime.now()))
    ip_catecode = ""
    sql = "select catecode from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] Catecode No. ")
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] Catecode : " + str(ip_catecode))

        sql = "update update_list2 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list2 (getdate) ")
        db_con.execute(sql)
    return "0"

# def updateDB_asin(db_con, asin, code, del_flg):
#     uSql = " update T_Category_BestAsin set del_flg = '{}', del_flg_date = getdate(), code = '{}' where asin = '{}'".format(del_flg, code, asin)
#     print(">> asin[{}] table update : {}".format(asin, uSql))
#     db_con.execute(uSql)

def newlist_new(db_con, in_ip):
    cateidx = ""
    sql = "select * from update_list2 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.select(sql)
    print('>> ##select all## sql :' + str(sql))

    if not rows:
        page = 1
        # new catecode 
        #sql = "select top 1 catecode from T_Category_BestAsin where del_flg is null and catecode not in (select catecode from update_list2) order by up_date"
        #sql = "select top 1 catecode from T_Category_BestAsin as a left join t_goods as g on g.ali_no = a.asin where catecode > 3000 and a.del_flg is null and g.uid is null and catecode not in (select catecode from update_list2) order by up_date"
        sql = "select top 1 catecode from T_Category_BestAsin as a left join t_goods as g on g.ali_no = a.asin where catecode not in (select catecode from update_list2) order by up_date"
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

def get_asinset(in_catecode, db_con, db_ali):
    asinset = []
    # sql = "select top 100 asin, a.isTmall, t.Uid, isnull(a.title,''), a.catecode, isnull(a.price, 0), c.bcate \
    #     , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
    #     , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0), a.del_flg, isnull(t.OriginalPrice,0) \
    #     from T_Category_BestAsin as a inner join T_CATEGORY as c on c.CateCode = a.catecode left join t_goods as t on t.ali_no = a.asin \
    #     where a.catecode = '{}' and a.del_flg is null and t.uid is null \
    #     order by newid() ".format(in_catecode)

    sql = "select top 100 asin, a.isTmall, t.Uid, isnull(a.title,''), a.catecode, isnull(a.price, 0), c.bcate \
        , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
        , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0), a.del_flg, isnull(t.OriginalPrice,0) \
        , isnull(t.price_tmp,0), t.regdate, t.UpdateDate \
        from T_Category_BestAsin as a inner join T_CATEGORY as c on c.CateCode = a.catecode left join t_goods as t on t.ali_no = a.asin \
        where a.catecode = '{}' order by newid() ".format(in_catecode)

    rs_row = db_con.select(sql)
    #print('>> ##select all## sql :' + str(sql))

    if not rs_row:
        print('>> category complete! change catecode :' +str(in_catecode))
        where_condition = " catecode = '{0}'".format(in_catecode)
        db_con.delete('update_list2', where_condition)
        return ""

    asinCnt = 0
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
        db_del_flg = ea_asin[16]
        db_OriginalPrice = ea_asin[17]
        db_price_tmp = ea_asin[18]
        db_regdate = ea_asin[19]
        db_UpdateDate = ea_asin[20]

        if Duid is None:
            Duid = ""

        if Duid != "":
            if str(price) == "" or  str(price) == "0":
                price = float(db_price_tmp)
            title_tran = db_title

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
        asinInfoDic['db_OriginalPrice'] = db_OriginalPrice
        asinInfoDic['db_regdate'] = db_regdate
        asinInfoDic['db_UpdateDate'] = db_UpdateDate

        asinset.append(asinInfoDic)
        asinCnt = asinCnt + 1 

    return asinset

def get_asinset_test(in_asin, db_con, db_ali):
    asinset = []
    sql = "select top 100 asin, a.isTmall, t.Uid, isnull(a.title,''), a.catecode, isnull(a.price, 0), c.bcate \
        , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
        , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0), a.del_flg, isnull(t.OriginalPrice,0) \
        from T_Category_BestAsin as a inner join T_CATEGORY as c on c.CateCode = a.catecode left join t_goods as t on t.ali_no = a.asin \
        where a.asin = '{}'".format(in_asin)

    print('>> ##select all## sql :' + str(sql))
    rs_row = db_con.select(sql)
    
    if not rs_row:
        sql = "select top 100 ali_no, isTmall, Uid, isnull(title,''), cate_idx, isnull(price, 0), c.bcate \
            , isnull(stop_update,'0'), isnull(input_shipping_weight,'0'), isnull(Del_Naver,'0'), goodscode, DE_title, t.title \
            , isnull(minus_opt,''), dbo.fnCheckCoupon_result('rental','', '', GETDATE(),''), isnull(c.weight,0), 0, isnull(t.OriginalPrice,0) \
            , isnull(t.price_tmp,0), t.regdate, t.UpdateDate \
            from t_goods as t inner join t_category as c on c.catecode = t.cate_idx \
            where ali_no = '{}'".format(in_asin)

        print('>> ##select all## sql :' + str(sql))
        rs_row = db_con.select(sql)

    asinCnt = 0
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
        db_OriginalPrice = ea_asin[16]
        db_del_flg = ea_asin[16]
        db_OriginalPrice = ea_asin[17]
        db_price_tmp = ea_asin[18]
        db_regdate = ea_asin[19]
        db_UpdateDate = ea_asin[20]
    
        if Duid is None:
            Duid = ""

        if Duid != "":
            if str(price) == "" or  str(price) == "0":
                price = float(db_price_tmp)
            title_tran = db_title

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
        asinInfoDic['db_OriginalPrice'] = db_OriginalPrice
        asinInfoDic['db_regdate'] = db_regdate
        asinInfoDic['db_UpdateDate'] = db_UpdateDate

        asinset.append(asinInfoDic)
        asinCnt = asinCnt + 1 

    return asinset

def get_Review(ProviderReviewsContents, in_asin):
    idx = 0
    reviews_arr = []
    if ProviderReviewsContents:
        vReview_UserNick = ""
        print(">> Reviews : {}".format(in_asin))
        for vReview in ProviderReviewsContents:
            if vReview:
                review_dic = {}
                idx = idx + 1
                vReview_id = vReview['ItemId']
                vReview_ConfigurationId = vReview['ConfigurationId']
                vReview_Content = vReview['Content']
                vReview_Content = str(vReview_Content).replace("/", "").replace("'", "").replace('&AMP;','')
                vReview_Rating = vReview['Rating']
                vReview_CreatedDate = vReview['CreatedDate']
                if vReview_UserNick == vReview['UserNick']:
                    vReview_UserNick = vReview['UserNick']
                    #print(">>({}) (skip) vReview : {} | [ {} ] | {} | {} | {} | {} ".format(idx, vReview_id, vReview_ConfigurationId, vReview_Content , vReview_Rating, vReview_CreatedDate, vReview_UserNick))
                else:
                    vReview_UserNick = vReview['UserNick']
                    review_dic['title'] = ''
                    review_dic['rating'] = vReview_Rating
                    review_dic['author'] = vReview_UserNick
                    review_dic['date'] = vReview_CreatedDate
                    review_dic['review_text'] = vReview_Content
                    review_dic['review_image'] = ''
                    review_dic['helpful_votes'] = ''
                    review_dic['rating_star'] = ''
                    if str(vReview_Content).find('사용자는 평가를 채우지') > -1:
                        #print(">>({}) (skip) vReview : {} | [ {} ] | {} | {} | {} | {} (Skip) ".format(idx, vReview_id, vReview_ConfigurationId, vReview_Content , vReview_Rating, vReview_CreatedDate, vReview_UserNick))
                        pass
                    else:
                        #print(">>({}) vReview : {} | [ {} ] | {} | {} | {} ".format(idx, vReview_id, vReview_ConfigurationId, vReview_Rating, vReview_CreatedDate, vReview_UserNick))
                        reviews_arr.append(review_dic)

    else:
        print(">> No Reviews : {}".format(in_asin))

    return reviews_arr

def repleaseDesc(tmp_desc, findStr, endStr):
    sp_desc = str(tmp_desc).split(findStr)
    for line_desc in sp_desc:
        line_desc = taobao_func.getparse(line_desc,'',endStr)
        if line_desc[:10].find('<img ') > -1:
            rel_line_desc = findStr + line_desc + endStr
            tmp_desc = tmp_desc.replace(rel_line_desc,'')
    return tmp_desc

# 68번 ep_proc 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep')
    sql = "select goodscode from ep_proc where goodscode = '{}'".format(goodscode)
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def checkAsin(asinInfoDic, asin):

    Duid = asinInfoDic['Duid']
    title_tran = asinInfoDic['title_tran']
    catecode = asinInfoDic['catecode']
    price = asinInfoDic['price']
    bcate = asinInfoDic['bcate']
    db_Del_Naver = asinInfoDic['db_Del_Naver'] 

    if Duid != "" and asinInfoDic['db_stop_update'] == '1':
        print(">> stop_update goods : {}".format(asin))
        return 'S01'

    if Duid != "" and db_Del_Naver == '9':
        print(">> Del_Naver 9 (네이버 노클릭상품) : {}".format(asin))
        return 'S02'

    ##### price check #####
    # if str(price) != "" and str(price) != "0":
    #     # 1044 : 쥬얼리 & 안경 & 시계, 1038 : 신발 & 가방 & 액세사리, 1033 : 의류 & 란제리
    #     if str(bcate) == '1044' or str(bcate) == '1038' or str(bcate) == '1033':
    #         if float(price) > 1000: # 해당 카테고리의 경우 15만원 이상 상품 SKIP
    #             print('>> 1000 위안 (15만원) over (skip)')
    #             return 'D49'

        # if float(price) < 1:
        #     print('>> 1 위안 미만 (skip)')
        #     return 'D12'
        # if float(price) > 8000:
        #     print('>> 8000 위안 (150만원) over (skip)')
        #     return 'D09'

    # title 금지어 체크 ###########
    forbidden_flag = taobao_func.checkForbidden_new(title_tran, db_ali)
    if str(forbidden_flag) != "0":
        print('>> checkForbidden_new : '+str(forbidden_flag))
        return 'D03'

    return ""

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
            print(">> {} : Item Not Found : {} ".format(itemId, dataResult['ErrorCode']))
            print('>> 품절 (Skip) : {}'.format(itemId))
            return "D01" # 품절

        base_min_price = 0
        base_top_price = 0
        option_val_count = 0

        result_dic = dict()
        result = dataResult['Result']
        result_item = result['Item']

        result_dic['api_UpdatedTime'] = None
        result_dic['api_CreatedTime'] = None
        if result_item.get('UpdatedTime'):
            print('>> api item UpdatedTime : {}'.format(result_item['UpdatedTime']))
            result_dic['api_UpdatedTime'] = result_item['UpdatedTime']
        if result_item.get('CreatedTime'):
            print('>> api item CreatedTime : {}'.format(result_item['CreatedTime']))
            result_dic['api_CreatedTime'] = result_item['CreatedTime']

        result_dic['api_sell_reason'] = ''
        if result_item['IsSellAllowed'] == False:
            print('>> 판매자 사유 sell not allowed : {}'.format(itemId))
            if result_item.get('SellDisallowReason'):
                print('>> 판매자 사유 : {}'.format(result_item['SellDisallowReason']))
                TaobaoItemUrl = result_item['TaobaoItemUrl']  
                print(">> TaobaoItemUrl : {}".format(TaobaoItemUrl))
                if result_item['SellDisallowReason'] == 'IsNotDeliverable':
                    print('>> 판매자 사유 IsNotDeliverable (OK) : {}'.format(result_item['SellDisallowReason']))
                    result_dic['api_sell_reason'] = '1'
                elif result_item['SellDisallowReason'] == 'IsInStock':
                    print('>> 판매자 사유 IsInStock (Skip) : {}'.format(result_item['SellDisallowReason']))
                    return "D71" # 품절
                else:
                    print('>> 판매자 사유 else (Skip) : {}'.format(result_item['SellDisallowReason']))
                    return "D71" # 품절

        #print(">> VendorItems : {}".format(VendorItems))

        Id = result_item['Id']
        Title = result_item['Title']
        OriginalTitle = result_item['OriginalTitle']
        CategoryId = result_item['CategoryId']
        ExternalCategoryId = result_item['ExternalCategoryId']

        print(">> Id : {}".format(Id))
        print(">> Title : {}".format(Title))
        #print(">> OriginalTitle : {}".format(OriginalTitle))
        print(">> CategoryId : {}".format(CategoryId))
        print(">> ExternalCategoryId : {}".format(ExternalCategoryId))

        ########### title Check ###########
        Title = Title.replace('정품','').replace("'","`")
        result_dic['DE_title'] = OriginalTitle.replace("'","`")
        Title = taobao_func.replaceQueryStringTitle(Title)
        Title = taobao_func.replaceTitle(Title, db_ali)
        Title = str(Title).replace("  ", " ").strip()
        print('>> tran_title (final) : ' + str(Title[:80]))
        if str(Title).strip() == "":
            print('>> No Title ')
            return "D02"
        if len(Title) < 5:
            print('>> Title len < 5 ')
            return "D02"

        # title 금지어 체크 ###########
        forbidden_flag = taobao_func.checkForbidden_new(Title, db_ali)
        if str(forbidden_flag) != "0":
            print('>> checkForbidden_new : '+str(forbidden_flag))
            return "D03 :" + " ( " + forbidden_flag[2:] + " ) "
        result_dic['forbidden'] = 'F'                    
        result_dic['title'] = Title

        MainPictureUrl = result_item['MainPictureUrl']  
        StuffStatus = result_item['StuffStatus']   #Item condition - New: New | Unused: Unused | Second: Second-hand | Another: Another
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
            if float(DeliveryPrice) > 25:
                print(">> shipping price over: {} | {} ".format(itemId, DeliveryPrice))
                return "D11" + " ( " + str(DeliveryPrice) + " )"  # shipping_price 25 위안 (SKIP)
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
            if float(Actual_Weight) > 1:
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

        videocloud = ""
        if result_item.get('Videos'):
            videoUrl = result_item['Videos'][0]['Url']
            videocloud = taobao_func.getparse(videoUrl,'video.taobao.com/play/u/','/')
            print(">> videocloud : {}".format(videocloud))

        other_img_set = []
        imgCnt = 0
        if Pictures:
            for ea_other_img in Pictures:
                ea_img = ea_other_img['Large']['Url']
                ea_img = getImgCut(ea_img)
                imgCnt = imgCnt + 1
                other_img_set.append(ea_img)
                if videocloud != "" and str(mainImg).find('/'+videocloud+'/') > -1 and imgCnt == 2:
                    # video 가 존재할경우 mainimg에 존재하는지 체크후 other_img 두번째를 mainImg 에 넣기
                    print(">> mainImg (other_img 두번째 이미지) 교체 : {}".format(ea_img))
                    mainImg = getImgCut(ea_img)
            #print(">> other_img_set : {}".format(other_img_set))

        if mainImg == "":
            print('>> no Img ')
            return "D19" # No img   
        if videocloud != "" and imgCnt < 2:
            print('>> no Img ')
            return "D19" # No img   

        Description = ""
        BrandId = ""
        BrandName = ""
        #FeaturedValues = ""
        #FeaturesTmp = ""
        if result_item.get('BrandId'):  BrandId = result_item['BrandId']  
        if result_item.get('BrandName'):  BrandName = result_item['BrandName']
        if result_item.get('Description'):  Description = result_item['Description']
        #if result_item.get('FeaturedValues'):  FeaturedValues = result_item['FeaturedValues']
        #if result_item.get('Features'):  FeaturesTmp = result_item['Features']  

        #print(">> BrandId : {}".format(BrandId))
        print(">> BrandName : {}".format(BrandName))
        #print(">> FeaturedValues : {}".format(FeaturedValues))
        #print(">> FeaturesTmp : {}".format(FeaturesTmp))
        TaobaoItemUrl = result_item['TaobaoItemUrl']  
        print(">> TaobaoItemUrl : {}".format(TaobaoItemUrl))

        if str(Description).find('<p style="margin: 0;overflow: hidden;"') > -1:
            Description = repleaseDesc(Description, '<p style="margin: 0;overflow: hidden;"','</p>')
        elif str(Description).find('<p style="margin: 0 0 5.0px 0;overflow: hidden;">') > -1:
            Description = repleaseDesc(Description, '<p style="margin: 0 0 5.0px 0;overflow: hidden;">','</p>')
        elif str(Description).find('<p style="margin:0 0 5.0px 0;width:0;height:0;overflow:hidden;">') > -1:
            Description = repleaseDesc(Description, '<p style="margin:0 0 5.0px 0;width:0;height:0;overflow:hidden;">','</p>')
        else:
            print(">> Description Ok ")

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
        result_dic['description'] = taobao_func.replaceDescription(str(Description))
        result_dic['db_OriginalPrice'] = asinInfo['db_OriginalPrice']

        #print(">> Description : {}".format(Description))
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
        f_pid = ""
        f_vid = ""
        PropertyValue = ""
        if Attributes:
            for ea_item in Attributes:
                ImageUrl = ""
                f_pid = ea_item['Pid']
                if not ea_item.get('Vid'):
                    print(">> ea_item No Vid : {}".format(ea_item))
                    f_vid = ""
                else:
                    f_vid = ea_item['Vid']
                f_IsConfigurator = ea_item['IsConfigurator']
                PropertyName = ea_item['PropertyName']
                
                if not ea_item.get('Value'):
                    print(">> ea_item No Value : {}".format(ea_item))
                    PropertyValue = ""
                else:
                    if ea_item.get('ValueAlias'):
                        PropertyValue = ea_item['ValueAlias']
                    else:
                        PropertyValue = ea_item['Value']

                if f_IsConfigurator == True:
                    if ea_item.get('ImageUrl'):
                        ImageUrl = ea_item['ImageUrl']
                        if ea_item.get('ValueAlias'):
                            image_name = ea_item['ValueAlias']
                        else:
                            image_name = ea_item['Value']
                        if PropertyName == '크기' or PropertyName == '신발 사이즈':
                            pass
                            #print(">> (skip) ImageUrl : {} | {}".format(image_name, ImageUrl))
                        else:
                            option_image_dic[image_name] = ImageUrl
                            #print(">> ImageUrl : {} | {}".format(image_name, ImageUrl))
                    else:
                        pass
                else:
                    if str(PropertyName) == "가격표":
                        pass
                    else:
                        if str(features).find(PropertyName) > -1:
                            features = features + '  ' + PropertyValue
                        else:
                            features = features + str('<li> ') + PropertyName + str(' : ') + PropertyValue + str('</li>')
                        if str(features_org).find(f_pid) > -1:
                            features_org = features_org + '  ' + f_vid
                        else:
                            features_org = features_org + str('<li> ') + f_pid + str(' : ') + f_vid + str('</li>')

        #print("\n>> option_image_dic : \n{}".format(option_image_dic))
        #print("\n>> features_org : \n{}".format(features_org))
        if features == "" and BrandName != "":
            features = str('● Brand : ') + BrandName 
        #print("\n>> features : \n{}".format(features))
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
                    org_option_name = ""
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
                                a_IsConfigurator = ea_item['IsConfigurator']
                                #if str(a_pid).isdigit() == True:
                                if a_IsConfigurator == True:
                                    a_Vid = ea_item['Vid']
                                    if c_Pid == a_pid and c_Vid == a_Vid:
                                        if option_name != "":
                                            if ea_item.get('ValueAlias'):
                                                option_name = option_name + " | " + ea_item['ValueAlias']
                                            else:
                                                option_name = option_name + " | " + ea_item['Value']
                                            PropertyName = PropertyName + " | " + ea_item['PropertyName']
                                            org_option_name = org_option_name + " | " + ea_item['OriginalValue']
                                            option_code = option_code + ":" + a_pid + ":" + a_Vid
                                        else:
                                            if ea_item.get('ValueAlias'):
                                                option_name = ea_item['ValueAlias']
                                            else:
                                                option_name = ea_item['Value']
                                            PropertyName = ea_item['PropertyName']
                                            org_option_name = ea_item['OriginalValue']
                                            option_code = a_pid + ":" + a_Vid
                                        break

                                    if org_option_name != "":
                                        if str(org_option_name).find('定金') > -1: # 보증금 체크
                                            print('>> 定金 (보증금) {}'.format(itemId))
                                            return "D47"
                                        if str(org_option_name).find('尾款') > -1: # 결제
                                            print('>> 尾款 (결제) {}'.format(itemId))
                                            return "D47"
                                    if option_name.find("화물") > -1 or option_name.find("계약") > -1 or option_name.find("인증서") > -1 or option_name.find("보증") > -1 or option_name.find("예약") > -1 or option_name.find("경매") > -1 or option_name.find("사전 판매") > -1:
                                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(option_name))
                                        return "D47"
                                    if option_name.lower().find("guarantee") > -1 or option_name.find("reservation") > -1 or option_name.find("contract") > -1 or option_name.find("freight") > -1 or option_name.find("auction") > -1:
                                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(option_name))
                                        return "D47"

                    if option_name != "":
                        option_name = taobao_func.replaceQueryStringOption(option_name)
                        option_val_count = option_val_count + 1
                        option_dic['option_name'] = option_name.strip()
                        option_dic['option_originalname'] = org_option_name
                        option_dic['option_code'] = option_code
                        option_value_dic[val_id] = option_name
                        option_list.append(option_dic)
                        print("({}) [{}] {}  ( {} ) [ 수량:{} ]".format(opt_cnt, val_id, option_name , valPrice , Quantity))
                        if option_val_count > 150:
                            print('>> 옵션 갯수 150개 이상 (Skip) : {}'.format(option_val_count))
                            break
                    else:
                        print(">> No option_name ")

            if option_val_count == 0:
                # No Option
                print(">> Ooption_val_count = 0 : {}".format(itemId))
                print('>> Ooption_val_count = 0 (Option sold out) ')
                return "D07"

            print(">> Option_val_count : {}".format(option_val_count))
            #print(">> option_value_dic : {}".format(option_value_dic))
            #print(">> option_price_dic : {}".format(option_price_dic))
            #print(">> option_image_dic : {}".format(option_image_dic))

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
        # tmp_coupon = d_coupon
        # if d_coupon is None or d_coupon == "" or d_coupon == 0:
        tmp_coupon = int(gDic['py_coupon'])

        result_dic['minus_opt'] = str(asinInfo['db_minus_opt'])
        result_dic['coupon'] = str(tmp_coupon)
        print('>> (DB) goods minus_opt : '+str(result_dic['minus_opt']))

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
        delievey_fee = float(taobao_func.getDeliveryFee(gDic, shipping_weight))
        delievey_fee = round(delievey_fee)
        print(">> delievey_fee : {} ".format(delievey_fee))

        # 타오바오 유료배송비
        taobao_shipping_fee = float(DeliveryPrice) * float(gDic['py_exchange_Rate']) * 2
        taobao_shipping_fee = round(taobao_shipping_fee)
        result_dic['taobao_shipping_fee'] = taobao_shipping_fee      
        print(">> taobao_shipping_fee : {} ".format(taobao_shipping_fee))

        ########### goodsmoney ###########
        goodsmoney = 0
        goodsmoney = taobao_func.getWonpirce(gDic, base_price_tmp)
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

        low_price = float(result_dic['price']) * float(gDic['py_exchange_Rate']) + (int(taobao_shipping_fee) * (100-tmp_coupon) / 100) + (int(delievey_fee) * (100-tmp_coupon) / 100)
        print('>> low_price : {} (환율 {}) '.format(float(result_dic['price']) * float(gDic['py_exchange_Rate']), float(gDic['py_exchange_Rate'])))
        print('>> taobao_shipping_fee : {} | 배대지 : {} '.format((int(taobao_shipping_fee) * (100-tmp_coupon) / 100),(int(delievey_fee) * (100-tmp_coupon) / 100)))
        low_price = int(low_price)
        print('>> low_price (최저원가) : ' + str(low_price))
        result_dic['low_price'] = low_price

        result_dic['OriginalPrice'] = originalprice
        result_dic['delivery_fee'] = delievey_fee
        result_dic['goodsmoney'] = goodsmoney

        if option_check == "1":
            result_dic['option_price_dic'] = option_price_dic
            result_dic['option_value_dic'] = option_value_dic
            result_dic['option_img_dic'] = option_image_dic
            result_dic['option_max_min_diff'] = float(option_max_price) - float(option_min_price)

            try:
                # 옵션 조합 
                option_item = taobao_func.generateOptionString(gDic, option_price_dic, option_value_dic, asinInfo['db_minus_opt'], base_price_tmp, tmp_coupon)
            except Exception as e:
                print('>> Exception (generateOptionString)')
                taobao_func.procLogSet(db_con, 'goods_api', " ( generateOptionString ) Exception - asin: " + str(itemId))
                return "E01 :" + " ( " + str(itemId) + ")"

            #print(">> Option_item : {}".format(option_item))
            if option_item.find("/0") == -1:
                print('>> option_value check (0원 옵션 없음) : {}'.format(itemId))
                return "D07"
            if option_item.find("화물") > -1 or option_item.find("계약") > -1 or option_item.find("인증서") > -1 or option_item.find("보증") > -1 or option_item.find("예약") > -1 or option_item.find("경매") > -1 or option_item.find("사전 판매") > -1:
                print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                return "D47"
            if option_item.lower().find("guarantee") > -1 or option_item.find("reservation") > -1 or option_item.find("contract") > -1 or option_item.find("freight") > -1 or option_item.find("auction") > -1:
                print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(itemId))
                return "D47"

            option_item = option_item.replace("`","")
            #print("\n>> option_item : {}".format(option_item))
            print("\n>> option_item OK ")
            result_dic['Items'] = taobao_func.getQueryValue(option_item)

        result_dic['api_flg'] = '1'
        InternalId = ""
        ExternalId = ""
        categoryInfo = ""
        tmp_cateInfo = ""
        if result.get('RootPath'):
            idx = 0
            RootPathContents = result['RootPath']['Content']
            if RootPathContents: 
                InternalId = RootPathContents[0]['Id']
                if RootPathContents[0].get('ExternalId'): 
                    ExternalId = RootPathContents[0]['ExternalId']
                categoryInfo = RootPathContents
                for vRootPath in RootPathContents:
                    if vRootPath:
                        idx = idx + 1
                        vRootPath_Name = vRootPath['Name']
                        if tmp_cateInfo == "":
                            tmp_cateInfo = vRootPath_Name
                        else:
                            tmp_cateInfo = tmp_cateInfo + " << " + vRootPath_Name

        result_dic['db_goodscode'] = asinInfo['db_goodscode']
        result_dic['api_InternalId'] = InternalId
        result_dic['api_ExternalId'] = ExternalId
        result_dic['api_categoryInfo'] = str(categoryInfo).replace("'","")
        print('>> cateInfo : ' + str(tmp_cateInfo))

        rtn_reviews_arr = []
        if result.get('ProviderReviews'):
            idx = 0
            ProviderReviewsContents = result['ProviderReviews']['Content']
            if ProviderReviewsContents:
                rtn_reviews_arr = get_Review(ProviderReviewsContents, itemId)
        #print(">> rtn_reviews_arr : {}".format(rtn_reviews_arr))
        result_dic['review'] = rtn_reviews_arr

        gallery_tmp = ""
        if result.get('VendorItems'):  
            idx = 0
            VendorItemsContents = result['VendorItems']['Content']
            for vItem in VendorItemsContents:
                if vItem:
                    idx = idx + 1
                    vItem_id = vItem['Id']
                    vItem_Title = vItem['Title']
                    vItem_CategoryId = vItem['CategoryId']
                    vItem_ExternalCategoryId = vItem['ExternalCategoryId']
                    vItem_OriginalPrice = vItem['Price']['OriginalPrice']
                    #print(">>({}) vItem : {} | [ {} ] | {} | {} | {} ".format(idx, vItem_id, vItem_OriginalPrice, vItem_Title , vItem_CategoryId, vItem_ExternalCategoryId))
                    if gallery_tmp == "":
                        gallery_tmp = vItem_id
                    else:
                        gallery_tmp = gallery_tmp + "," + vItem_id

        result_dic['gallery'] = str(gallery_tmp)
        print(">> gallery : {}".format(gallery_tmp))
        # in_asin, dic, db_con, in_pg, in_guid, db_price
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
                    taobao_func.setGoodsdelProc(db_con, DUid, DIsDisplay, DOptionKind)
                    # print('\n >> t_goods Insert (delete)')
                return str(rtnFlg) # exit

    return "0"

def proc_Main(instanceKey, language, headers, goods_dic, db_con, db_ali, input_pgKbn, db_price):
    catecode = ""
    get_asin_list = []
    pgName = goods_dic['py_pgFilename']
    if input_pgKbn == "test_api":
        test_asin = input(">> 업데이트할 타오바오 상품번호 : ")
        get_asin_list = get_asinset_test(test_asin, db_con, db_ali)
        print(len(get_asin_list))
        if len(get_asin_list) == 0:
            print('>> test_asin len no : ' + str(test_asin))
            return "1"
    else:
        loofCnt = 0
        while loofCnt < 2:
            #catecode = newlist(db_con, currIp)
            catecode = newlist_new(db_con, currIp)
            if catecode != "":
                break
            loofCnt = loofCnt + 1
        if catecode == "":
            print(">> catecode 없습니다. ")
            return "1"
        else:
            get_asin_list = get_asinset(catecode, db_con, db_ali)
            print(len(get_asin_list))
            if len(get_asin_list) == 0:
                print('>> category complete! change catecode :' +str(catecode))
                sql_d = "delete from update_list2 where catecode = '{0}'".format(catecode)
                db_con.execute(sql_d)              
                print('>> catecode parsing complete : ' + str(catecode))
                return "1"

    cnt_main = 0
    c_Errcnt = 0
    for ea_item in get_asin_list:
        print("\n\n>> --------------------------------------------------------------------------------")
        cnt_main = cnt_main + 1
        asin = ea_item['asin']
        guid = ea_item['Duid']
        catecode = ea_item['catecode']
        istmall = ea_item['isTmall']
        db_regdate = ea_item['db_regdate']
        db_UpdateDate = ea_item['db_UpdateDate']
        print("\n\n\n### {} : ### [ {} ] (catecode : {}) reg: {} | upd: {} #################################################".format(cnt_main, asin, catecode, db_regdate, db_UpdateDate))
        if cnt_main == 1 or cnt_main == 50:
            procWork(db_con, currIp)
        print('>> version : '+str(in_ver))

        if asin == "":
            print(">> No itemId Check please : {}".format(ea_item))
            continue
        if guid:
            print(">> ({}) asin : {}  | DB 존재 상품 : {}".format(cnt_main, asin, guid))
        else:
            print(">> ({}) asin : {}  | New 상품 ".format(cnt_main, asin))

        rtnCheckCode = checkAsin(ea_item, asin)
        if rtnCheckCode != "":
            rtnChk = rtnCheckCode
        else:
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
            taobao_func.procLogSet(db_con, pgName, " ( E99 ) api exit - asin: " + str(asin))
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

        dic_b = dict()
        dic_b['asin'] = "'" + asin + "'"
        dic_b['cate_idx'] = catecode
        dic_b['memo'] = "'" + taobao_func.getMemo(rtnChk) + "'"
        dic_b['code'] = "'" + rtnChk[:3] + "'"
        dic_b['reg_date'] = " getdate() "
        dic_b['isTmall'] = "'" + istmall + "'"

        if rtnChk != "0":  
            if rtnChk_no[:1] == "D":
                if str(guid) == '' or guid is None or guid == "None":
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, api_flg, api_date from T_goods where ali_no = '{0}'".format(asin)
                else:
                    sql = "select uid, IsDisplay, isnull(Del_Naver,0),regdate, UpdateDate, isnull(naver_in,0), goodscode, api_flg, api_date from T_goods where uid = '{0}'".format(guid)                    
                rs = db_con.selectone(sql)
                D_naver_in = ""
                D_goodscode = ""
                if rs:
                    Duid = rs[0]
                    DIsDisplay = rs[1]
                    D_naver_in = rs[5]
                    D_goodscode = rs[6]
                    # T_goods sold out
                    if DIsDisplay == 'T':
                        if rtnChk_no == "D03":  # Forbidden 금지어일 경우 판매불가 상품처리
                            sql_u1 = "UPDATE t_goods SET isdisplay='F',IsSoldOut='T', Stock='0', Del_Naver='1',NAVER_stockout='2', stop_update='1', api_flg = '1', api_date = getdate() where uid = {0}".format(Duid)
                            db_con.execute(sql_u1)

                            sql_u2 = "update t_goods_sub set IsDelContentFile = 'T' where uid = {0}".format(Duid)
                            db_con.execute(sql_u2)
                        else:
                            print('>> [' + str(asin) + '] setDisplay (품절 처리) :' + str(Duid))
                            #setDisplay(Duid, 'F', '', db_con)                                
                            sql = "update T_goods set IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = null, UpdateDate=getdate(), api_flg = '1', api_date = getdate() where uid='{0}'".format(Duid)
                            print(">> sql : " + str(sql))
                            print(">> 품절 처리 OK : " + str(asin))
                            db_con.execute(sql)
                        # 네이버 노출 상품이 품절되었을 경우, 68번 ep_proc 테이블에 Insert (mode : D)
                        if str(D_naver_in) == "1":
                            proc_ep_insert(D_goodscode,'D')

            sql = "delete from T_Category_BestAsin_del where asin ='{0}'".format(asin)
            db_con.execute(sql)
            db_con.insert('T_Category_BestAsin_del', dic_b)  # insert
            print('>> ##insert## : T_Category_BestAsin_del')

        sql = "delete from T_Category_BestAsin where asin ='{0}'".format(asin)
        db_con.execute(sql)
        print('>> ##delete## : T_Category_BestAsin')

        # if rtnChk_no == "D47" or rtnChk_no == "D12" or rtnChk_no == "D11" or rtnChk_no == "D09" or rtnChk_no == "D49" or rtnChk_no == "D03":
        #     updateDB_asin(db_con, asin, rtnChk_no, "1")
        #     print(">> T_Category_BestAsin (Update) : {}".format(rtnChk_no))
        # else:
        #     sql = "delete from T_Category_BestAsin where asin ='{0}'".format(asin)
        #     db_con.execute(sql)
        print(">> Errcnt : {0}".format(c_Errcnt))

        if rtnChk == "E99":
            return rtnChk
        time.sleep(3)

    return "0"

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    timecount = 0
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

    #########################################
    input_Site = 'taobao'
    input_pgKbn = 'test_api'
    # input_Site = sys.argv[1]
    # input_pgKbn = sys.argv[2]
    #########################################
    if input_Site == "" or input_pgKbn == "":
        print(">> 입력 값을 확인하세요 : {} | {}".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    goods_dic = dict()
    sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, withbuy_cost, coupon, api_balance, api_balance_date from python_version_manage where name = 'goods_api'"
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
        goods_dic['py_api_balance'] = str(rs[11]).strip()
        goods_dic['py_api_balance_date'] = str(rs[12]).strip()

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName
        if float(goods_dic['py_api_balance']) < 130 :
            print(">> api 잔액 체크 필요 : {}".format(goods_dic['py_api_balance']),goods_dic['py_api_balance_date'])
            print(">> Main End : " + str(datetime.datetime.now()))
            os._exit(1)

        roofCnt = 0
        while roofCnt < 500:
            if str(currIp).strip() == "222.104.189.18":
                print('>> version_check (Skip) local : ' + str(currIp))
            else:
                # version check
                version_check(db_con, db_ali, in_ver, pgFilename, input_pgKbn)
            roofCnt = roofCnt + 1
            print(">> main roofCnt : {}".format(roofCnt))
            mainRtn = proc_Main(instanceKey, language, headers, goods_dic, db_con, db_ali, input_pgKbn, db_price)
            if mainRtn == "1":
                print(">> catecode parsing complete ")
                flgProc = "1"
                break
            elif mainRtn == "E99":
                print(">> E99 exit ")
                flgProc = "1"
                break

            time.sleep(2)

    db_con.close()
    db_ali.close()
    db_FS.close()
    os._exit(0)