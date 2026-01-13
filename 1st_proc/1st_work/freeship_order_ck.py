from dataclasses import replace
import os
import time
import datetime
import sys
import DBmodule_FR

# 파싱 함수
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

# mssql null
def getQueryValue(in_value):
    if in_value == None:
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

# mssql null
def getQueryValueNew(in_value):
    if in_value == None:
        result = "NULL"
    elif in_value == "":
        result = "NULL"
    elif in_value == "None":
        result = "NULL"
    else:
        result = "'{0}'".format(in_value)
    return result

def getOrderCount(db_FS, goodscode):
    orderCnt = 0
    sql_g = " select count(*) from t_order_info where GoodsCode = '{}'".format(goodscode)
    rowG = db_FS.selectone(sql_g)    
    if rowG:
        orderCnt = rowG[0]
    return orderCnt

def getOrderCateCount(db_FS, site, catecode):
    orderCnt = 0
    sql_g = " select count(*) from t_order_info where sitecate = '{}' and catecode = '{}'".format(site, catecode)
    rowG = db_FS.selectone(sql_g)    
    if rowG:
        orderCnt = rowG[0]
    return orderCnt

def getOrderCateAli(db_FS, site, catecode):
    orderCnt = 0
    if site[-1:] == '2':
        site1 = site[:-1]
        site2 = site
    else:
        site1 = site
        site2 = site+'2'
    print(">> {} | {} ".format(site1,site2))
    sql_g = " select count(*) from t_order_info where sitecate in ('{}','{}') and catecode = '{}'".format(site1, site2, catecode)
    rowG = db_FS.selectone(sql_g)    
    if rowG:
        orderCnt = rowG[0]
    return orderCnt

def procUpdateOrder(db_FS):

    rowCnt = 0
    site_kbn = ""
    sql = " select top 100 i.uid, goodscode, goodsuid, i.CateCode, o.regdate, i.goodstitle, o.uid, o.orderno, i.sitecate from t_order as o inner join t_order_info as i on i.OrderUid = o.uid "
    sql = sql + " where RegDate >= '2020-10-01 00:00:00' and i.order_ck is null "
    rows = db_FS.select(sql)
    if not rows:
        print('>>  New Order : 0 ')
    else:
        for row in rows:
            ordCnt = 0
            infouid = row[0]
            goodscode = row[1]
            goodsuid = row[2]
            CateCode = row[3]
            regdate = row[4]
            goodstitle = row[5]
            Ouid = row[6]
            orderno = row[7]
            order_sitecate = row[8]
            in_site = order_sitecate

            if in_site == "usa" or in_site == "mall" or in_site == "global" or in_site == "best" or in_site == "de" or in_site == "uk" or in_site == "cn" or in_site == "handmade":
                site_kbn = ""
            elif in_site == "mini" or in_site == "shop" or in_site == "trend" or in_site == "ref" or in_site == "red":
                site_kbn = ""
            else:
                site_kbn = "ali"
            print(">>\n-----------------------------------------------")
            print('>> {} [ {} ] {} ({}) | CateCode : {} | infouid : {} | regdate : {} '.format(order_sitecate, orderno, goodscode, goodsuid, CateCode, infouid, regdate))

            # 해당 사이트 DB 연결 
            db_con = DBmodule_FR.Database(order_sitecate)
            print(">> Site Open : {}".format(order_sitecate))

            if str(goodsuid).strip() != "":
                ordCnt = getOrderCount(db_FS, goodscode)
                rowCnt = rowCnt + 1

                if in_site == "usa" or in_site == "mall" or in_site == "global" or in_site == "best" or in_site == "de" or in_site == "uk":
                    sql_g = "select GoodsCode, ali_no, isnull(display_ali_no,''), isnull(Del_naver,0), isnull(fr_title,''),Title,ImgB,isnull(Keyword,''),OriginalPrice,Price,OptionKind,isnull(DeliveryFee,''),isnull(UpdateDate,''),RegDate,isnull(ali_no_temp,''),isnull(datefolder,''),origin_dollar,cate_idx,isnull(JP_title,''),isnull(IT_title,''),isnull(img_url,''),delivery_fee,google_in,isnull(order_ck,''),isnull(ep_in,''),naver_in, isnull(withbuy_price_tmp,''), site_kbn, uid from t_goods where uid = '{}'".format(goodsuid)
                else:
                    sql_g = "select GoodsCode, ali_no, '' as display_ali_no, isnull(Del_naver,0), isnull(fr_title,''),Title,ImgB,isnull(Keyword,''),OriginalPrice,Price,OptionKind,isnull(DeliveryFee,''),isnull(UpdateDate,''),RegDate,isnull(ali_no_temp,''),isnull(datefolder,''),origin_dollar,cate_idx,isnull(JP_title,''),isnull(IT_title,''),isnull(img_url,''),delivery_fee,google_in,isnull(order_ck,''),isnull(ep_in,''),naver_in, '' as withbuy_price_tmp, '' as site_kbn, uid from t_goods where uid = '{}'".format(goodsuid)
                rowG = db_con.selectone(sql_g)
                db_ali_no = ""
                if not rowG:
                    print(">> T_goods 없는 상품 : {} ({}) | 주문번호: {}".format(goodscode, goodsuid, orderno))
                    uSql_i2 = " update t_order_info set order_ck = '1' where uid = '{}'".format(infouid)
                    print(' [{}] t_order_info order_ck Update Ok : {}'.format(goodscode, orderno))
                    db_FS.execute(uSql_i2)  # update
                else:
                    db_goodscode = rowG[0]
                    db_ali_no = rowG[1]
                    db_display_ali_no = rowG[2]
                    db_Del_naver = rowG[3]
                    db_fr_title = rowG[4]
                    db_Title = rowG[5]
                    db_ImgB = rowG[6]
                    db_Keyword = rowG[7]
                    db_OriginalPrice = rowG[8]
                    db_Price = rowG[9]
                    db_OptionKind = rowG[10]
                    db_DeliveryFee = rowG[11]
                    db_UpdateDate = rowG[12]
                    db_RegDate = rowG[13]
                    db_ali_no_temp = rowG[14]
                    db_datefolder = rowG[15]
                    db_origin_dollar = rowG[16]
                    db_cate_idx = rowG[17]
                    db_JP_title = rowG[18]
                    db_IT_title = rowG[19]
                    db_img_url = rowG[20]
                    db_delivery_fee = rowG[21]
                    db_google_in = rowG[22]
                    db_order_ck = rowG[23]
                    db_ep_in = rowG[24]
                    db_naver_in = rowG[25]
                    db_withbuy_price_tmp = rowG[26]
                    db_site_kbn = rowG[27]
                    db_guid = rowG[28]
                    if db_site_kbn is None or db_site_kbn == "":
                        db_site_kbn = in_site

                    if db_google_in is None or db_google_in == "None" or db_google_in == "":
                        db_google_in = "null"
                    db_content = ""
                    sql_gc = "select isnull(content,'') from t_goods_content where uid = '{}'".format(db_guid)
                    rowGC = db_con.selectone(sql_gc)
                    if rowGC:
                        db_content = rowGC[0]

                    db_option_Title = ""
                    db_option_Items = ""
                    if db_OptionKind == '300':
                        sql_go = "select isnull(Title,''), isnull(items,'') from t_goods_option where goodsuid = '{}'".format(db_guid)
                        rowGO = db_con.selectone(sql_go)
                        if rowGO:
                            db_option_Title = rowGO[0]
                            db_option_Items = rowGO[1]

                    db_ali_no = str(db_ali_no).replace("_del","").strip()
                    if db_fr_title != "":
                        print(">> keyword : {}".format(db_fr_title))

                    print(">> db_ali_no : {} | db_goodscode : {} | OrderCount : {} | db_Del_naver : {}".format(db_ali_no, db_goodscode, ordCnt, db_Del_naver))

                    ############################# t_order_info Update ####################################
                    if str(goodstitle).find('(대량주문전용)') > -1:
                        uSql_i2 = " update t_order_info set order_ck = '1', order_ali_no = '{}', orderCnt = {}, bulk_order = '1', site_kbn = '{}' where uid = '{}'".format(db_ali_no, ordCnt, db_site_kbn, infouid)
                        print(' [{}] t_order_info order_ck, order_ali_no, orderCnt, bulk_order Update Ok : {}'.format(db_goodscode, db_ali_no))
                        db_FS.execute(uSql_i2)  # update
                    else:
                        uSql_i2 = " update t_order_info set order_ck = '1', order_ali_no = '{}', orderCnt = {}, keyword = '{}', site_kbn = '{}' where uid = '{}'".format(db_ali_no, ordCnt, db_fr_title, db_site_kbn, infouid)
                        print(' [{}] t_order_info order_ck, order_ali_no, orderCnt Update Ok : {}'.format(db_goodscode, db_ali_no))
                        db_FS.execute(uSql_i2)  # update

                    ############################# t_goods Update ####################################
                    if str(db_Del_naver) == "5": # 네이버 에서 (상품수 줄이기위한 : 5) 미노출 상품의 경우 --> null 변경
                        print(">> db_Del_naver = 5 --> null update : {} ".format(db_goodscode))
                        uSql_i3 = " update t_goods set Del_naver = null where uid = '{}'".format(goodsuid)
                        print(' [{}] db_Del_naver = 5 --> null update Ok : {}'.format(db_goodscode, db_ali_no))
                        db_con.execute(uSql_i3)

                    uSql = " update t_goods set order_ck = '1' where uid = '" + str(goodsuid) + "' and order_ck is null "
                    print(' <{}> order_ck Update Ok : {}'.format(in_site, db_guid))
                    db_con.execute(uSql)  # update

                    uSql_c = " update t_category set sale_ck_new = '1' where catecode = '" + str(CateCode) + "' and sale_ck_new is null "
                    print(' <{}> t_category sale_ck_new Update Ok : {}'.format(in_site, db_cate_idx))
                    db_con.execute(uSql_c)  # update

                    ############################# t_order_goodsinfo Insert ####################################
                    sql_og = " select Uid from t_order_goodsinfo where Uid = '{}'".format(infouid)
                    rowOg = db_FS.selectone(sql_og)
                    if not rowOg:
                        print(">> (Insert) t_order_goodsinfo ")
                        sql_ii = "insert into T_ORDER_GOODSINFO (Uid, OrderUid, GoodsCode, ali_no, display_ali_no, Del_naver, fr_title, Title, ImgB, Keyword, OriginalPrice, Price, OptionKind, DeliveryFee, g_UpdateDate, g_RegDate, ali_no_temp, datefolder, origin_dollar, cate_idx, JP_title, IT_title, img_url, delivery_fee, google_in, order_ck, ep_in, naver_in, withbuy_price_tmp, site_kbn, content, option_Title, option_Items, guid, sitecate, orderno, o_RegDate) values "
                        sql_ii = sql_ii + "({0},{1},'{2}','{3}','{4}',{5},'{6}','{7}','{8}','{9}',{10},{11},'{12}',{13},'{14}','{15}','{16}','{17}','{18}',{19},'{20}','{21}','{22}','{23}',{24},'{25}','{26}',{27},'{28}','{29}','{30}','{31}','{32}',{33},'{34}','{35}','{36}')".format(infouid,Ouid,db_goodscode,db_ali_no,db_display_ali_no,db_Del_naver,db_fr_title,db_Title,db_ImgB,db_Keyword,db_OriginalPrice,db_Price,db_OptionKind,db_DeliveryFee,db_UpdateDate,db_RegDate,db_ali_no_temp,db_datefolder,db_origin_dollar,db_cate_idx,db_JP_title,db_IT_title,db_img_url,db_delivery_fee,db_google_in,db_order_ck,db_ep_in,db_naver_in,db_withbuy_price_tmp,db_site_kbn,db_content,db_option_Title,db_option_Items,db_guid,in_site,orderno, regdate)
                        #print(">> sql_ii : {}".format(sql_ii))
                        try:
                            db_FS.executeRep(sql_ii)  # insert
                        except Exception as e:
                            print(">> T_ORDER_GOODSINFO Insert Error ")
                        else:
                            print(">> T_ORDER_GOODSINFO Insert ")

            ############################# t_goods_category 테이블 catecode 조회 
            db_goodscate_catecode = ""
            sql_gg = "select isnull(CateCode,'') from t_goods_category where GoodsUid = '{}'".format(goodsuid)
            rowGg = db_con.selectone(sql_gg)
            if rowGg:
                db_goodscate_catecode = rowGg[0] # 알리의 경우 t_goods_category 카테고리코드가 T_category 코드와일치
            else:
                db_goodscate_catecode = CateCode
            ############################# t_category 테이블 IsHidden 조회  
            db_category_IsHidden = ""
            sql_cc = "select IsHidden from t_category where catecode = '{}'".format(CateCode)
            rowC = db_con.selectone(sql_cc)
            if rowC:
                db_category_IsHidden = rowC[0] # T_category테이블 IsHidden

            ############################# t_order_category Update ####################################
            db_ordercate_ordercnt = 0
            sql_toc = " select ordercnt, flg from T_ORDER_CATEGORY where catecode = '{}'".format(CateCode)
            rowOC = db_con.selectone(sql_toc)
            if rowOC:
                db_ordercate_curr = rowOC[0]
                db_ordercate_ordercnt = getOrderCateCount(db_FS, in_site, CateCode)
                #print(">> T_ORDER_CATEGORY 현재 ordercnt : {}".format(db_ordercate_curr))
                print(">> T_ORDER_CATEGORY 존재 (update) : {} (ordercnt 증가) ".format(CateCode))
                sql_Cu = "update T_ORDER_CATEGORY set cate_idx = '{0}', IsHidden = '{1}', ordercnt = {2}, updatedate = getdate() where catecode = '{3}'".format(db_goodscate_catecode,db_category_IsHidden,db_ordercate_ordercnt,CateCode)
                db_con.execute(sql_Cu)  # update
            else:
                db_ordercate_ordercnt = getOrderCateCount(db_FS, in_site, CateCode)
                print(">> T_ORDER_CATEGORY (Insert) : {}".format(CateCode))
                sql_Ci = "insert into T_ORDER_CATEGORY (CateCode, cate_idx, IsHidden, ordercnt) values ({0},{1},'{2}',{3})".format(CateCode,db_goodscate_catecode,db_category_IsHidden,db_ordercate_ordercnt)
                db_con.execute(sql_Ci)  # insert

            ############################# t_category (194) 알리 카테고리 주문수 update ####################################
            if site_kbn == "ali":
                db_ordercate_count = 0
                print("ali (194 t_category) cate_order_cnt(주문수) Update ")
                db_ordercate_count = getOrderCateAli(db_FS, in_site, CateCode)
                sql_cc = "update t_category set cate_order_cnt = {} where catecode = '{}'".format(db_ordercate_count, CateCode)
                db_FS.execute(sql_cc)  # update (194 t_category)
            ###################################################################################################################

            print(">> Site DB Close : {}".format(order_sitecate))
            db_con.close()

    return "0"


if __name__=='__main__':

    print('>> [--- order_ckeck start ---] ' + str(datetime.datetime.now()))
    time.sleep(1)
    print('>> Proc Start ')

    ########################################################################################################################
    # T_order_info 주문건 -> T_goods 테이블 : order_ck = '1' 설정 / t_category 테이블 : sale_ck_new = '1' 설정
    ########################################################################################################################

    db_freeship = DBmodule_FR.Database('freeship')
    procUpdateOrder(db_freeship)
    db_freeship.close()
    time.sleep(1)

    print('>> Proc End ')
    print('>> [--- order_check end ---] ' + str(datetime.datetime.now()))
    os._exit(0)

