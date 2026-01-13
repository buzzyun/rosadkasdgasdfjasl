import random
import os
import datetime
import time
import DBmodule_FR

global proc_cnt

db_FS = DBmodule_FR.Database('freeship')

#파싱 함수
def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result.strip()

def do_proc(in_site):
    global proc_cnt
    sql = " SELECT top 50 Ouid, InfoUid, GoodsUid, delivery_price, O.orderno,amazon_orderno,weight_volume,weight_pay,weight_unit, I.sitecate, I.goodscode, W.regdate, SettlePrice, amazon_price, amazon_price_date, I.ali_id \
        from withbuy_tracking_price as W inner join T_ORDER_info as I on I.Uid = W.InfoUid inner join T_ORDER as O on O.uid = I.OrderUid \
        where check_flg is null and CAST(isnull(delivery_price,0) AS float) > 24000 and item_ea = '1' and goods_ea = '1' \
        and W.regdate >= '2022-01-01 00:00:00' and W.regdate < getdate() - 1 and sitecate = '" + str(in_site) + "' order by W.regdate asc "
    print(">> sql : {}".format(sql))

    rows = db_FS.select(sql)
    if not rows:
        print(">> 대상이 없습니다 ")
        return "0"

    print(">> -------------------------------------------------------------------------------------------")
    db_con = DBmodule_FR.Database(in_site)
    print(">> DB Open : {}".format(in_site))
    for rowsel in rows:
        time.sleep(0.5)
        Ouid = rowsel[0]
        Iuid = rowsel[1]
        GoodsUid = rowsel[2]
        delivery_price = int(rowsel[3])
        orderno = rowsel[4]
        amazon_orderno = rowsel[5]
        weight_volume = rowsel[6]
        weight_pay = float(rowsel[7])
        weight_unit = rowsel[8]
        sitecate = rowsel[9]
        goodscode = rowsel[10]
        regdate = rowsel[11]
        SettlePrice = int(rowsel[12])
        amazon_price = rowsel[13]
        amazon_price_date = rowsel[14]
        ali_id = rowsel[15]

        kg_weight = weight_pay
        if weight_unit == "LBS":
            kg_weight = weight_pay / 2
        kg_weight = round(float(kg_weight), 1)

        org_cost = 0
        amazon_price = str(amazon_price).replace(",","").replace(" ","").strip()
        amazon_price = float(amazon_price)
        if ali_id == "글로벌" or ali_id == "일본아마존" or ali_id == "amazon_global" or ali_id == "amazon_best": 
            org_cost = amazon_price * 11
        elif ali_id == "de" or ali_id == "amazon_de" or ali_id == "amazon_de2":
            org_cost = amazon_price * 1350
        elif ali_id == "uk" or ali_id == "amazon_uk":
            org_cost = amazon_price * 1700
        else:
            org_cost = amazon_price * 1350
        org_cost = org_cost + int(delivery_price)
        marzin = SettlePrice - org_cost
        marzinRate = (marzin / SettlePrice) * 100

        if marzinRate > 14:
            print(">> 마진율 15% 이상 (SKIP) : {} | goodscode : {} | delivery_price : {} | kg_weight : {} | marzinRate : {} %".format(orderno, goodscode, delivery_price, kg_weight, round(marzinRate)))
        else:
            print(">> 마진율 15% 이하 : {} | goodscode : {} | delivery_price : {} | kg_weight : {} | marzinRate : {} %".format(orderno, goodscode, delivery_price, kg_weight, round(marzinRate)))
            sql = " SELECT goodscode, isnull(display_ali_no,''), ali_no, isnull(input_shipping_weight,0) from t_goods where uid = '" + str(GoodsUid) + "' "
            row_good = db_con.selectone(sql)
            if row_good:
                goodscode = row_good[0]
                display_ali_no = row_good[1]
                ali_no = row_good[2]
                input_shipping_weight = row_good[3]
                if display_ali_no == "":
                    display_ali_no = ali_no
                print(">> goodscode : {} ({}) | display_ali_no : {} | ali_no : {} | input_shipping_weight : {}".format(goodscode, GoodsUid, display_ali_no, ali_no, input_shipping_weight))

                if float(input_shipping_weight) < float(kg_weight):
                    print(">> (DB) input_shipping_weight : {} | kg_weight : {} ".format(input_shipping_weight, kg_weight))
                    sql_upd = " update t_goods set input_shipping_weight = '{}' where uid = '{}'".format(kg_weight, GoodsUid)
                    print(">> t_goods - input_shipping_weight (Update) : {}".format(goodscode))
                    db_con.execute(sql_upd)

                    sql_se = "select display_ali_no from amazon_goods_update where guid = '{}' and sitecate = '{}'".format(GoodsUid, sitecate)
                    row_upd = db_FS.selectone(sql_se)
                    if row_upd:
                        sql_pp = " update amazon_goods_update set display_ali_no = '{}', regdate = getdate(), upddate = null, flg_chk = '0', mode = 'W' where guid = '{}'".format(display_ali_no, GoodsUid)
                        print(">> amazon_goods_update (Update) : {}".format(goodscode))
                    else:
                        sql_pp = " insert into amazon_goods_update (guid, sitecate, display_ali_no, regdate, flg_chk, mode)  values('{}','{}','{}',getdate(),'0','W')".format(GoodsUid,sitecate,display_ali_no)
                        print(">> amazon_goods_update (Insert) : {}".format(goodscode))
                        proc_cnt = proc_cnt + 1
                    db_FS.execute(sql_pp)

        sql_end = " update withbuy_tracking_price set check_flg = '1' where InfoUid = '{}'".format(Iuid)
        db_FS.execute(sql_end)
        print(">> withbuy_tracking_price (check_flg = 1) 완료처리 : {}".format(goodscode))
        print(">> -------------------------------------------------------------------------------------------")

    db_con.close()

    return "0"

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

    return "0"

if __name__ == '__main__':

    print(">> Start withbuy_delivery_price_apply ")
    print(str(datetime.datetime.now()))
    proc_cnt = 0
    
    siteList = ['best','global','mall','usa','de','uk']
    rtn_flg = "0"
    for ea_site in siteList:
        print("\n>> Site : {} ".format(ea_site))
        try:
            rtn_flg = do_proc(ea_site)
        except Exception as e:
            print('>> 예외가 발생 (종료) : ', e)
            time.sleep(5)
            break
        else:
            time.sleep(1)

        if rtn_flg != "0":
            print(">> Error Exit ")
            break
        time.sleep(random.uniform(6,8))

    procLogSet("withbuy_delivery_price", "P", str(proc_cnt), " (아마존) withbuy price update ")
    db_FS.close()
    print(str(datetime.datetime.now()))
    print(">> End withbuy_delivery_price_apply ")
    os._exit(0)

