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

def procUpdateOrder(in_site, db_FS, db_con):

    site_kbn = ""
    if in_site == "usa" or in_site == "mall" or in_site == "global" or in_site == "best" or in_site == "de" or in_site == "uk" or in_site == "cn" or in_site == "handmade":
        sql = " select CateCode, count(*), max(goodsuid)  from t_order as o inner join t_order_info as i on i.OrderUid = o.uid "
        sql = sql + " where i.sitecate = '" + str(in_site) + "' and RegDate >= '2020-10-01 00:00:00' group by CateCode order by count(*) desc "
    elif in_site == "mini" or in_site == "shop" or in_site == "trend" or in_site == "ref" or in_site == "red":
        sql = " select CateCode, count(*), max(goodsuid)  from t_order as o inner join t_order_info as i on i.OrderUid = o.uid "
        sql = sql + " where i.sitecate = '" + str(in_site) + "' and RegDate >= '2022-06-01 00:00:00' group by CateCode order by count(*) desc "
    else:
        sql = " select CateCode, count(*), max(goodsuid) from t_order as o inner join t_order_info as i on i.OrderUid = o.uid "
        sql = sql + " where i.sitecate = '" + str(in_site) + "' group by CateCode order by count(*) desc"
        site_kbn = "ali"
    print('>> sql:' + str(sql))
    rows = db_FS.select(sql)
    if not rows:
        print('>> [ {} ] New Order : 0 '.format(in_site))
    else:
        rcnt = 0
        print(">> {} : 주문 카테고리 : {} 건".format(in_site, len(rows)))
        for row in rows:
            O_cateCode = row[0]
            O_ordercnt = row[1]
            O_goodsuid = row[2]
            print('>>{} ({}) [ {} ] 주문수 : {} | max(goodsuid)'.format(rcnt+1, in_site, O_cateCode, O_ordercnt, O_goodsuid))

            g_IsHidden = ""
            sql_g = "select dbo.fnGetCateNavi2('rental',catecode,'>>') as cate_info, IsHidden from t_category where catecode = '{}'".format(O_cateCode)
            rowG = db_con.selectone(sql_g)
            if rowG:
                g_cate_info = rowG[0]
                g_IsHidden = rowG[1]
                print(">> {} ({})".format(g_cate_info, g_IsHidden))

            db_goodscate_catecode = ""
            sql_gg = "select isnull(CateCode,'') from t_goods_category where GoodsUid = '{}'".format(O_goodsuid)
            rowGg = db_con.selectone(sql_gg)
            if rowGg:
                db_goodscate_catecode = rowGg[0] # 알리의 경우 t_goods_category 카테고리코드가 T_category 코드와일치
                print(">> t_goods_category ({}) {}".format(O_goodsuid, db_goodscate_catecode))

            ############################# t_order_category Update ####################################
            # db_ordercate_ordercnt = 0
            # sql_toc = " select ordercnt, flg from T_ORDER_CATEGORY where catecode = '{}'".format(O_cateCode)
            # rowOC = db_con.selectone(sql_toc)
            # if rowOC:
            #     db_ordercnt = rowOC[0]
            #     db_ordercate_ordercnt = getOrderCateCount(db_FS, in_site, O_cateCode)
            #     print(">> T_ORDER_CATEGORY 현재 ordercnt : {}".format(db_ordercnt))
            #     print(">> T_ORDER_CATEGORY 존재 (update) : {} - ordercnt 증가 ".format(O_cateCode))
            #     sql_Cu = "update T_ORDER_CATEGORY set cate_idx = '{0}', IsHidden = '{1}', ordercnt = '{2}', updatedate = getdate() where catecode = '{3}'".format(db_goodscate_catecode,g_IsHidden,db_ordercate_ordercnt,O_cateCode)
            #     db_con.execute(sql_Cu)  # update
            # else:
            #     db_ordercate_ordercnt = getOrderCateCount(db_FS, in_site, O_cateCode)
            #     print(">> T_ORDER_CATEGORY (Insert) : {}".format(O_cateCode))
            #     sql_Ci = "insert into T_ORDER_CATEGORY (CateCode, cate_idx, IsHidden, ordercnt) values ('{0}','{1}','{2}',{3})".format(O_cateCode,db_goodscate_catecode,g_IsHidden,db_ordercate_ordercnt)
            #     db_con.execute(sql_Ci)  # insert

            ############################# t_category (194) 알리 카테고리 주문수 update ####################################
            if site_kbn == "ali": 
                db_ordercate_count = 0
                print("ali (194 t_category) cate_order_cnt Update")
                db_ordercate_count = getOrderCateAli(db_FS, in_site, O_cateCode)
                sql_cc = "update t_category set cate_order_cnt = {} where catecode = '{}'".format(db_ordercate_count, O_cateCode)
                db_FS.execute(sql_cc)  # update (194 t_category)

            rcnt =  rcnt + 1

    return "0"


if __name__=='__main__':

    # 전체 T_order내역 catecode 주문수 체크 설정 
    print('>> [--- order_ckeck_category start ---] ' + str(datetime.datetime.now()))
    time.sleep(1)
    print('>> Proc Start ')

    ########################################################################################################################
    # 전체 T_order내역 catecode 주문수 체크 설정 
    ########################################################################################################################

    db_freeship = DBmodule_FR.Database('freeship')
    sitelist = ['best','global','mall','usa','de','uk','cn','handmade','red','mini','shop','trend','ref',
                'fashion','electron','furniture','beauty','jewelry','auto','sports','baby','office','industry',
                'fashion2','electron2','furniture2','beauty2','jewelry2','auto2','sports2','baby2','office2','industry2']

    for site in sitelist:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">> Site DB Open : {} ".format(site))
        db_con = DBmodule_FR.Database(site)
        procUpdateOrder(site, db_freeship, db_con)
        time.sleep(2)
        print(">> Site DB Close : {}".format(site))
        db_con.close()
    ##############################

    db_freeship.close()
    time.sleep(1)

    print('>> Proc End ')
    print('>> [--- order_ckeck_category end ---] ' + str(datetime.datetime.now()))
    os._exit(0)

