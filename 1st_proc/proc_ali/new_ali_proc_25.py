import os
## os.system('pip install --upgrade selenium')
import socket
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import datetime
import json
import func_ali
import random
import DBmodule_FR
global ver
ver = "24.05.16 17:00"
print(">> ver : {}".format(ver))

global gAdmin_Id
global gOrder_mode
global curr_ip
gAdmin_Id = "adminauto" #주문자ID
currIp = socket.gethostbyname(socket.gethostname())
currIp = str(currIp).strip()
print(">> currIp : {}".format(currIp))
db_FS = DBmodule_FR.Database("freeship")

def proc_LogState(in_proc_memo):
    sql = " insert into ali_order_proc_log (proc_ip, proc_memo) values('{}','{}')".format(currIp, in_proc_memo) 
    print(">> setLogProc : " + str(sql))
    db_FS.execute(sql)

    return "0"

def proc_LogSet(m_OrderNo, goodscode, code, msg):
    print(">> code : {} | msg : {}".format(code, msg))

    if msg == "":
        msg = func_ali.get_codeMsg(code)

    sql = "select orderNo from auto_order_ali_new where orderno = '{}'".format(m_OrderNo)
    row = db_FS.selectone(sql)
    if row:
        sql_u = " update auto_order_ali_new set code = '{}', msg = '{}', goodscode = '{}', upddate = getdate(), currIp = '{}' where orderno = '{}'".format(code, msg, goodscode, m_OrderNo, currIp)
    else:
        sql_u = " insert into auto_order_ali_new ( orderno, code, msg, goodscode, currIp ) values ( '{}', '{}', '{}', '{}', '{}') ".format(m_OrderNo, code, msg, goodscode, currIp)

    #print(">> sql_u : {} ".format(sql_u))
    db_FS.execute(sql_u)

    # 어드민 메모 작성 ##
    ##################################################
    adminMemoSet(m_OrderNo, msg)

    return "0"


def proc_LogDetailSet(m_OrderNo, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, dic_order):
    print(">> code : {} | msg : {}".format(code, msg))

    sql = "select orderNo from auto_order_ali_new where orderno = '{}'".format(m_OrderNo)
    row = db_FS.selectone(sql)
    if row:
        sql_u = " update auto_order_ali_new set goodscode = '{}', code = '{}', msg = '{}', sell_price = '{}', ali_price = '{}', org_price = '{}', marzin = '{}', dev_detail = '{}', ali_order_no = '{}', upddate = getdate(), currIp = '{}' where orderno = '{}'".format(goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, currIp, m_OrderNo)
    else:
        if str(dic_order['m_choice']) == "1":
            sql_u = " insert into auto_order_ali_new ( orderno, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, currIp, choice_goods ) values ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' , '{}', '{}', '{}', 'choice') ".format(m_OrderNo, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, currIp)
        else:
            sql_u = " insert into auto_order_ali_new ( orderno, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, currIp, choice_goods ) values ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' , '{}', '{}', '{}','') ".format(m_OrderNo, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, currIp)
    #print(">> sql_u : {} ".format(sql_u))
    db_FS.execute(sql_u)

    # 어드민 메모 작성 ##
    adminMemoSet(m_OrderNo, msg)

    return "0"

def getMakeSql(in_sel_flg, searchUid, searchInfoUid, in_ip, in_orderno, site_list):

    ex_eDate = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M" + ":00")
    print('>> eDate: ' + str(ex_eDate)) #30분전 시간

    site_list_arr = ""
    if site_list != "":
        site_sp = site_list.split(',')
        for site in site_sp:
            site = site.strip()
            if site_list_arr == "":
                site_list_arr = "'" +str(site) + "'"
            else:
                site_list_arr = site_list_arr + ",'" +str(site) + "'"
        site_list_arr = "(" + site_list_arr + ")"
        print(">> site_list_arr : {}".format(site_list_arr))

    sql = ""
    if in_sel_flg == "main_all":
        sql = " select count(*) "
    elif in_sel_flg == "main":
        sql = " select top 5 t.Uid, i.Uid, OrderNo, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, i.ea, isnull(i.optionKind,''), isnull(o.Item,''), RcvPost, isnull(soc_no,''), rcvName, isnull(OrderMemo,''), isnull(cancel_cate,''), isnull(cancel_reason,''), RcvMobile, t.regdate, i.CateCode, isnull(AdminMemo,''), RcvTel, RcvAddr, RcvAddrDetail, i.GoodsTitle "
    elif in_sel_flg == "addr":
        sql = " select t.Uid, i.Uid, OrderNo, SettlePrice, RcvPost, rcvName, replace(soc_no,'p','P'), RcvMobile, RcvAddr, isnull(RcvAddrDetail,''), isnull(cancel_cate,''), isnull(cancel_reason,''), t.coupang_auto, isnull(t.naver_pay_order_id,''), t.naver_pay_unitprice, i.sitecate "
    else:
        sql = " select top 5 t.Uid, OrderNo, SettlePrice, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, RcvPost, isnull(soc_no,''), rcvName, i.sitecate, isnull(OrderMemo,''), "
        sql = sql + " i.ea, isnull(cancel_cate,''), isnull(cancel_reason,''), isnull(i.amazon_price,''), isnull(i.ali_orderno,''), isnull(i.optionKind,''), isnull(AdminMemo,''), isnull(auto_flg,''), RcvMobile  "
    sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.Uid left join t_order_option as o on o.OrderInfoUid = i.Uid "
    sql = sql + " where t.state = '200' " ## 배송준비중
    if in_sel_flg != "addr":
        sql = sql + " and UserID <> 'kbw4798' "    # 본부장님 주문건 제외
        sql = sql + " and naver_pay_cancel_wait is null " # 네이버 페이 취소대기건 제외
        #sql = sql + " and cancel_cate is null and isnull(cancel_reason,'') = '' " # 취소 관련 메모 주문건 제외
        sql = sql + " and auto_check_code is null " # code 없는것
        ### sql = sql + " and i.sitecate = 'mini' "
#######################################################
        # sql = sql + " and t.regdate <= '" + str(ex_eDate) + "'"
        # sql = sql + " and t.orderno in ('M22160571712C6') " ##  주문테스트
        sql = sql + " and t.coupang_auto = '1' "
#######################################################
    if searchUid != "":
        sql = sql + " and t.Uid = '" +str(searchUid)+ "'"
    if searchInfoUid != "":
        sql = sql + " and i.Uid = '" +str(searchInfoUid)+ "'"
    if in_orderno != "":
        sql = sql + " and t.orderno = '" + str(in_orderno) + "' " ##  주문테스트

    if site_list != "": # 해당 사이트만 처리
        sql = sql + " and i.sitecate in " +str(site_list_arr)

    if in_sel_flg  == "main_all" or in_sel_flg == "main":
        #sql = sql + " order by t.uid asc"
        sql = sql + " order by t.regdate asc "
    

    #주문 실행했던 결과 에러 또는 주문 내용 체크대상은 조건에서 제외
    #sql = sql + " and t.OrderNo not in (select OrderNo from ali_order_auto where state in ('E','K','C'))"
    #sql = sql + " and naver_pay_cancel_wait is null " #네이버 페이 취소대기건 제외
    #sql = sql + " and soc_no is not null "  # 수량1개 통관번호 있는 주문건
    #sql = sql + " and i.ea = 1 "  # 수량1개 통관번호 있는 주문건
    #sql = sql + " and cancel_cate is null and cancel_reason is null " # 취소 관련 메모 없는 주문건
    #sql = sql + " and i.amazon_price is null and i.ali_orderno is null "
    #sql = sql + " and (i.optionKind is null or i.optionKind = '100' or i.optionKind = 'null')"
    #sql = sql + " and OrderMemo is null " #요청메모
    #sql = sql + " and AdminMemo is null "
    #ql = sql + " and t.SettlePrice < '" + str(ex_gMaxOrdPrice) + "' " # 2만원 이하 상품
    #sql = sql + " and ConfirmDate >= '" + str(ex_sDate) + "' "

    return str(sql)

def orderCntProc(inAliID, inUid):
    curDate = ""
    nowTime = str(datetime.datetime.now())
    curDate = nowTime[:10]
    #print(curDate)

    curAliId = func_ali.getOrderIDCount(inAliID)
    print('>> curAliId : ' + str(curAliId))

    sql = " select idx from T_COUNT_ORDER where date = '" + curDate + "'"
    #print('>> sql: ' + str(sql))
    row_cp = db_FS.selectone(sql)
    if not row_cp:
        sql_ins = "insert into T_COUNT_ORDER (date," + curAliId + ") values('" + curDate + "',1)"
        #print('>> sql_ins: ' + str(sql_ins))
        db_FS.execute(sql_ins)
    else:
        ridx = row_cp[0]
        sql_upd = "update T_COUNT_ORDER set " + curAliId + " = " + curAliId + " + 1 where idx = '" + str(ridx) + "'"
        #print('>> sql_upd: ' + str(sql_upd))
        db_FS.execute(sql_upd)

    #print('>> 주문 통계 UPDATE 완료')

    # 해외 배송중 상태로 변경
    sql_upd = "UPDATE T_ORDER SET State=201, BuyID ='" + gAdmin_Id + "', ChkDate=GETDATE() WHERE Uid='" + str(inUid) + "'"
    #print('>> sql_upd: ' + str(sql_upd))
    db_FS.execute(sql_upd)
    #print('>> 해외 배송중 상태로 변경 완료')

    return "0"

# inOrderUid : (t_order : uid)
def aliOrdernoSet(inOrderNo, inOuid, inIuid, inAliOrderNo, inAliPrice, inAliID, ingoodscode):

    sql = " select OrderNo,IsConfirm from t_order where Uid = '" + str(inOuid) + "'"
    #print('>> sql: ' + str(sql))
    row_t = db_FS.selectone(sql)
    rOrderNo = row_t[0]
    rIsConfirm = row_t[1]

    if rIsConfirm == "F":
        print('>> 해외주문번호 입력 불가 (주문 상태를 확인 필요) {} | {} '.format(rIsConfirm, inOrderNo))
        proc_LogSet(inOrderNo, ingoodscode, "E08", "해외주문번호 입력 불가 (주문 상태를 확인 필요)")
        return "E08"

    if inOuid != "" and inAliOrderNo != "" and inAliID != "":
        sql = " select Uid, isnull(ali_orderno,'') from T_ORDER_INFO where Uid = '" + str(inIuid) + "'"
        #print('>> sql: ' + str(sql))
        row_info = db_FS.selectone(sql)
        if row_info:
            rUid = row_info[0]
            rAli_orderno = row_info[1]
            rAli_orderno = str(rAli_orderno).strip()
            #print('>> DB rUid: ' + str(rUid))
            #print('>> DB rAli_orderno: ' + str(rAli_orderno))

            ####### 주문 입력 / 통계 카운트 / 주문상태변경 / 카톡발송 #######
            if rAli_orderno == "":
                ####### 해외주문번호 입력 #######
                sql_upd = "update t_order_info set ali_id = '" + str(inAliID) + "', ali_orderno = '" + str(inAliOrderNo) + "', amazon_price = '" + str(inAliPrice) + "',amazon_price_id = '" + str(gAdmin_Id) + "',amazon_price_date=getdate(), ali_ord_date = convert(varchar(50),getdate(),120) where Uid='" + str(inIuid) + "'"
                #print('>> sql_upd : ' + str(sql_upd))
                #print('>> 해외 주문번호 UPDATE 처리 : {}'.format(inAliOrderNo))
                db_FS.execute(sql_upd)
                print('>> 해외 주문번호 UPDATE 완료 : {}'.format(inAliOrderNo))
    
                ####### 통계 카운트 처리 및 해외배송중 상태로 변경 #######
                #print('>> 통계 카운트 처리 및 해외배송중 상태로 변경')
                orderCntProc(inAliID, inOuid)
                print('>> 통계 카운트 및 해외배송중 상태 변경완료')

                # 카카오톡 전송 (실패할 경우 sms 전송)
                #print('>> 카카오톡 전송')
                #sms_send_kakao_proc(inOrderNo, inIuid)
                sms_send_kakao_proc_new(inOrderNo, inIuid, "", "")
                print('>> 카카오톡 전송 완료')

                sql_u2 = " update t_order set coupang_auto = null where uid = '{}'".format(inOuid)
                #print(">> sql_u2 : {} ".format(sql_u2))
                db_FS.execute(sql_u2)

                return "0"
        else:
            print('>> 해외 주문번호 UPDATE 불가 (현지주문번호가 이미 존재) ' + str(rAli_orderno))
            proc_LogSet(inOrderNo, ingoodscode, "E09", "해외 주문번호 UPDATE 불가 (현지주문번호가 이미 존재) ")
            return "E09"
    else:
        print('>> 해외주문번호 입력 불가 ' + str(rIsConfirm))
        proc_LogSet(inOrderNo, ingoodscode, "E07", "해외주문번호 입력 불가 ")
        return "E07"

#reg 숫자및 소수점만 추출 (그외 문자 제거)
def regRemoveText(in_str):
    result = ""
    result = re.sub(r'[^0-9.]', '', in_str)
    return result

def replaceQueryString(in_word) :
    result = in_word.replace("'","")
    result = result.replace("★","").replace("◆","").replace("&lt;"," ").replace("&gt;"," ")
    result = result.replace(r'\x26', ' ').replace('&amp;',' ').replace('&AMP;',' ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;"," - ").replace("&times;"," x ").replace("、"," . ")
    result = result.replace("&#39;","").replace("&quot;","").replace("\\", "").replace("®","")
    result = result.replace("【","(").replace("】",")").replace("<","(").replace(">",")").replace("()","").replace("[]","").replace(";","")

    return result

def proc_order(browser, dic_order):
    msg = ""
    Ouid = dic_order['m_Ouid']
    Iuid = dic_order['m_Iuid']
    aliCode = dic_order['m_ali_code']
    d_ea = dic_order['m_ea']
    ord_optionstr = dic_order['m_Item']
    fs_url = dic_order['fs_url']
    goodscode = dic_order['m_GoodsCode']
    orderno = dic_order['m_OrderNo']
    debug_mode = dic_order['debug_mode']
    notice_phone = dic_order['notice_phone']
    ali_id = dic_order['ali_id']
    option_title = dic_order['m_option_title']
    m_option_items = dic_order['m_option_items']
    procIP = dic_order['m_ip']
    dic_order['m_choice'] = ""

    ali_url = "https://ko.aliexpress.com/item/" +str(aliCode)+ ".html"
    print("ali_url : {}".format(ali_url))
    browser.get(ali_url)

    time.sleep(random.uniform(4, 4.5))
    #if debug_mode == "1":
    #    input(">> Key Press (상품코드 검색) : ")

    result = browser.page_source
    result_org = str(result)
    result_soup = BeautifulSoup(result, 'html.parser')
    ali_screen_type = 0
    if str(result_org).find('product-main-wrap') > -1:
        print(">> product-main-wrap (type : 1)")
        ali_screen_type = 1
    elif str(result_org).find('pdp-wrap pdp-body') > -1:
        print(">> pdp-wrap pdp-body (type : 2)")
        ali_screen_type = 2
    elif str(result_org).find('pdp-body-top') > -1:
        print(">> pdp-body-top (type : 3)")
        ali_screen_type = 3

    if str(browser.page_source).find('businessModel') > -1:
        choice_tmp = func_ali.getparse(str(browser.page_source),'businessModel',',').replace('\\n','').replace("'","")
        if str(choice_tmp).find('UN_CHOICE') > -1:
            print(">> UN_CHOICE : {}".format(choice_tmp))
        elif str(choice_tmp).find('CHOICE') > -1:
            print(">> CHOICE : {}".format(choice_tmp))
            dic_order['m_choice'] = "1"
            print(">> choice goods: {}".format(aliCode))

    #if str(result_org).find('class="titleBanner') > -1: 
    if str(result_org).find('class="product-title"') > -1:
        title = func_ali.getparse(str(result_org),'class="product-title"','</h1>').replace('<h1 class="product-title-text">','').replace('>','')
        #print(">> title Ok : {}".format(title))
    elif str(result_org).find('class="titleBanner--title') > -1:
        title = func_ali.getparse(str(result_org),'class="titleBanner--title','</h3>')
        if str(title).find('title="') > -1:
            title = func_ali.getparse(str(title),'title="','').replace("'","").replace('"','')
        proc_LogSet(orderno, goodscode, "X04", "알리 신 버젼 상품 자동불가")
        return "X04"
    elif str(result_org).find('"product-title">') > -1:
        title = func_ali.getparse(str(result_org),'"product-title">','</h1>').replace('>','')
        #print(">> title Ok : {}".format(title))
    else:
        if str(result_org).find('class="zero-list"') > -1:
            msg = "[D001] 품절 (aliCode 일치하는 상품 없음) "
        else:
            msg = "[D001] 품절 (aliCode No product-title) "
        if str(result_org).find('class="product-container"') > -1:
            msg = "[D001] 품절 (유사상품 view)"
        print(msg) 
        proc_LogSet(orderno, goodscode, "D001", msg)
        return "D001"

    if str(result_org).find('next-btn-primary buynow disable"') > -1:
        proc_LogSet(orderno, goodscode, "D001", "품절")
        return "D001"

    if ali_screen_type == 2:
        product_delivery = func_ali.getparse(result_org,'class="delivery--to--','</span>')
        product_delivery = func_ali.getparse(product_delivery,'>','')
    elif ali_screen_type == 3:
        product_delivery = func_ali.getparse(result_org,'data-pl="product-delivery"','class="quantity--')
    else:
        product_delivery = func_ali.getparse(result_org,'class="product-delivery-to">','</span>')

    if str(product_delivery).find('Korea') > -1:
        pass
        #print(">> product_delivery : {}".format(product_delivery)) 
    else:
        print(">> No product_delivery ") 
        print(">> product_delivery : {} ".format(product_delivery))

    # if str(result_org).find('배송지로 배송이 불가능') > -1:
    #     print(">> 배송 불가능 : {}".format(aliCode))
    #     proc_LogSet(orderno, goodscode, "S024", "배송 불가능")
    #     return "S024"

    if str(result_org).find('class="uniform-banner"') > -1:
        product_price = func_ali.getparse(result_org,'class="uniform-banner-box-price"','</span>')
    else:
        product_price = func_ali.getparse(result_org,'class="product-price-value"','</span>')
    #print(">> product_price : {} ".format(product_price))
    if product_price == "" and ali_screen_type == 2:
        product_price = func_ali.getparse(result_org,'price-current">','</span>')
        print(">> product_price : {} ".format(product_price))

    if product_price == "" and ali_screen_type == 3:
        product_price = func_ali.getparse(result_org,'data-pl="product-price"','data-pl="product-title"')
        # print(">> product_price : {} ".format(product_price))

    if str(product_price).find('US') > -1:
        pass # print(">> price Ok : {}".format(product_price)) 
    else:
        print(">> No price ") 
        print(">> product_price : {} ".format(product_price))

    # buy_now = func_ali.getparse(result_org,'class="product-action"','</span>')
    if ali_screen_type == 2:
        buy_now = func_ali.getparse(result_org,'class="action--container','')
        buy_now = func_ali.getparse(buy_now,'<button type','</button>')
    elif ali_screen_type == 3:
        buy_now = func_ali.getparse(result_org,'class="quantity--','')
        if buy_now.find('class="pdp-wrap"') > -1:
            buy_now = func_ali.getparse(buy_now,'','class="pdp-wrap"')
    else:
        buy_now = func_ali.getparse(result_org,'class="product-action"','</span>')

    if str(buy_now).find('즉시 구매') > -1 or str(buy_now).find('Buy Now') > -1 or str(buy_now).find('Buy now') > -1 or str(buy_now).find('바로 구매') > -1:
        pass
    elif str(result_org).find('<button title="즉시 구매"') > -1:
        pass
    elif str(result_org).find('comet-btn-important"><span>바로 구매</span>') > -1:
        print(">> 바로 구매 버튼 있음 (type 2) ")
    elif str(result_org).find('<span>주문하기</span>') > -1:
        print(">> 주문하기 버튼 존재 OK ")
    else:
        print(">> 즉시 구매 버튼 확인불가 ")
        proc_LogSet(orderno, goodscode, "D003", "즉시 구매 버튼 확인불가")
        return "D003"

    # 알리 상품 이미지 체크
    ## ali_url = func_ali.getparse(str(result_org),'"imagePath":"','"')
    ali_url = func_ali.getImgUrl(result_org, ali_screen_type)
    # print("ali_url : " + str(ali_url))

    try:
        rtn_img = func_ali.imgComp(fs_url, ali_url)
    except Exception as e:
        print(">> 이미지 비교 Exception : " + str(ali_url))
        proc_LogSet(orderno, goodscode, "S011", "알리 상품이미지 다름")
        return "S011"
    else:
        #print(" rtn_img : "+ str(rtn_img))
        if rtn_img == "1":
            print(">> 알리 상품이미지 다름 : {} | {}".format(fs_url, ali_url))
            proc_LogSet(orderno, goodscode, "S011", "알리 상품이미지 다름")
            return "S011"

###################################################################################################################

    edit_option = func_ali.option_dist(ord_optionstr)
    if edit_option == "S01" or edit_option == "S04":
        print(" (확인필요) after : {}".format(edit_option))
        proc_LogSet(orderno, goodscode, edit_option, "옵션형식 구버젼")
        return edit_option
    else:
        print(">> (주문) Edit Option : {}".format(edit_option))

    ali_opt_cnt = 0
#-- test ----------------------------------------------------------
    req_source = ""
    if str(browser.page_source).find('<div class="sku--wrap--') == -1:
        print(">> 옵션 없는 소스 ")
    else:
        print(">> 옵션 있는 소스 ")
        if str(browser.page_source).find("productSKUPropertyList") == -1:
            print(">> 소스 확인 불가상태 (1)")
        else:
            print(">> 소스 확인 (productSKUPropertyList) OK ")
#------------------------------------------------------------
    ali_opt_cnt = 0
    opt_source = str(browser.page_source)
    sp_opt_title = opt_source.split('class="sku-item--property')
    ali_opt_cnt = len(sp_opt_title) -1
    print(">> (len) ali 화면 source 옵션갯수 : {}".format(ali_opt_cnt))

    dicOpt = dict()
    option_code = ""
    option_name = ""
    if edit_option == "":
        print(">> 옵션 없는 상품 ")
        dicOpt['code'] = ""
        dicOpt['name'] = ""
    else:
        if edit_option.find("(") > -1:
            opt_tmp = func_ali.getparse(edit_option,"(","").strip()
            if opt_tmp.find("(") > -1:
                #flg_search = "S01"  # SKIP
                print(">>  예전 옵션 (괄호 중복 1개이상 ) : {}".format(opt_tmp))
                #return flg_search

            option_code = func_ali.getparse(edit_option,"(",")").strip()
            option_name = func_ali.getparse(edit_option,")","").strip()
            if option_name[-1:] == ":":
                option_name = option_name[:-1]
            if option_name.find("(") > -1:
                #flg_search = "S01"  # SKIP
                print(">>  예전 옵션 (괄호 중복 1개이상 ) : {}".format(edit_option))
                #return flg_search

            sp_opt_code = option_code.split(":")
            sp_opt_name = option_name.split(":")
            if len(sp_opt_code) != len(sp_opt_name):

                # 새로 적용된 (이미지 있는 옵션의 경우 (옵션2개인 경우))
                if len(sp_opt_code) == 1 and len(sp_opt_name) == 2 and ali_opt_cnt == 2:
                    flg_search = "S01"  # SKIP
                    print(">> 옵션코드 옵션명 갯수 불일치 SKIP 대상: {}".format(edit_option))
                    proc_LogSet(orderno, goodscode, "S01", "옵션코드 옵션명 갯수 불일치 SKIP")
                    return flg_search

        dicOpt['code'] = option_code
        dicOpt['name'] = option_name.replace("  "," ").strip()
        print(" dicOpt : {}".format(dicOpt))
        if dicOpt == "S01" or dicOpt == "S04":
            print(" (확인필요) after : {}".format(dicOpt))
            proc_LogSet(orderno, goodscode, dicOpt, "옵션형식 구버젼")
            return dicOpt
        else:
            dicOpt['title'] = option_title
            #print(">> dicOpt : {}".format(dicOpt))


    # 옵션 [더 보기] 버튼 있는지 체크 후 있으면, [더 보기] 클릭
    findClassnameO = func_ali.getparse(str(browser.page_source),'class="sku--wrap--','">')
    #print(">> findClassnameO : {}".format(findClassnameO))

    moreCheck = func_ali.getparse(str(browser.page_source),'class="sku--wrap--','class="product-main"').strip()
    if str(moreCheck).find('ViewMore--') > -1:
        print(">> 옵션 [더 보기] 있음")

        findClassnameB = func_ali.getparse(str(browser.page_source),'class="sku-item--box--','">')
        #print(">> findClassnameB : {}".format(findClassnameB))
        moreBtn = 'div.sku--wrap--' +str(findClassnameO)+ ' > div > div > div.sku-item--box--' +str(findClassnameB)+ ' > div > button'
        #print(">> moreBtn : {}".format(moreBtn))
        time.sleep(0.5)
        try:
            print(">> [더 보기] 클릭전 ")
            if browser.find_element(By.CSS_SELECTOR,moreBtn):
                browser.find_element(By.CSS_SELECTOR,moreBtn).click()
                print(">> [더 보기] 클릭 ")
                time.sleep(random.uniform(2, 2.5))
        except Exception as e:
            print(">> [더 보기] 클릭 Exception ")
        else:
            print(">> [더 보기] 클릭 Ok ")
            moreCheck = func_ali.getparse(str(browser.page_source),'class="sku--wrap--','class="product-main"')
            if str(moreCheck).find('ViewMore--') == -1:
                print(">> 옵션 더보기 없음 OK ")
            else:
                print(">> 옵션 더보기 아직 존재 ")

    # 옵션 체크 추가 
    ###############################################################
    if ali_opt_cnt > 0:
        opt_source = str(browser.page_source)
        elem_sku_wrap = browser.find_element(By.CSS_SELECTOR, 'div.sku--wrap--' +str(findClassnameO)) # 옵션전체 elem
        sp_opt_title = opt_source.split('class="sku-item--property')
        ali_opt_cnt = len(sp_opt_title) -1

        i = 0
        cnt_opt_match = 0
        while i < ali_opt_cnt:
            source_opt_tmp = str(sp_opt_title[i+1])
            findClassnameB = func_ali.getparse(source_opt_tmp,'class="sku-item--box--','">')
            elem_classname = 'div > div:nth-child(' + str(i+1) + ') > div.sku-item--box--' +str(findClassnameB) # 옵션별 박스
            #print(">> [옵션:{}] elem_classname : {}".format(i+1, elem_classname))
            elem_list = elem_sku_wrap.find_element(By.CSS_SELECTOR, elem_classname)
            elem_list_opt = elem_list.find_elements(By.CSS_SELECTOR, 'div') # (옵션별 리스트) sku-item--skus-- 
            print(">> [옵션:{}] elem_list_opt (옵션리스트) : {}".format(i+1, len(elem_list_opt)-1))

            title_name = func_ali.getparse(source_opt_tmp,'class="sku-item--title--','<div>')
            title_name = func_ali.getparse(title_name,'<span>','<span>').replace(":","")
            option_coltmp = func_ali.getparse(source_opt_tmp,'class="sku-item--skus--','')
            if option_coltmp.find('split-line--wrap') > -1:
                option_coltmp = func_ali.getparse(option_coltmp,'','split-line--wrap')
            print("\n>>[옵션:{}] title_name : {}".format(i+1, title_name))
            sp_opt_col = option_coltmp.split('<div data-')
            opt_name_list = []
            eaCnt = 0
            for ea_col in sp_opt_col:
                ea_opt_name = ""
                if ea_col.find('sku-col') == -1:
                    eaCnt = eaCnt + 1
                    continue

                ea_opt_code_tmp = func_ali.getparse(ea_col,'sku-col="','"')
                ea_opt_code = ea_opt_code_tmp.split('-')[1]
                ea_opt_class = func_ali.getparse(ea_col,'class="','"')
                if ea_col.find('title="') > -1:
                    ea_opt_name = func_ali.getparse(ea_col,'title="','"')
                elif ea_col.find('alt="') > -1:
                    ea_opt_name = func_ali.getparse(ea_col,'alt="','"')
                else:
                    print(">> Option Name check ")
                opt_name_list.append(ea_opt_name)

                print(">>[옵션:{}] ({}) {} ".format(i+1, ea_opt_code, ea_opt_name))
                if sp_opt_code[i] == ea_opt_code:
                    print(">> Opttion Code Match : {} | {}".format(sp_opt_code[i], ea_opt_code))
                    if sp_opt_name[i].strip().upper() == ea_opt_name.strip().upper():
                        print(">> Opttion Name Match : {} | {}".format(sp_opt_name[i], ea_opt_name))
                        if ea_opt_class.find('soldOut') > -1:
                            print(">>[옵션:{}] (soldOut) ({}) {} ".format(i+1, ea_opt_code, ea_opt_name))
                            print('>> [X02] 옵션 품절 (soldOut) : {}'.format(ea_opt_name))
                            proc_LogSet(orderno, goodscode, "S05", "옵션 품절 (soldOut)")
                            return "X02"
                        else:
                            cnt_opt_match = cnt_opt_match + 1 # 매칭 옵션이 있을경우
                            if ea_opt_class.find('selected') > -1:
                                print(">> 옵션 선택되어있음 (Option Selected )")
                            else:
                                print(">> 옵션 클릭 (Option Click) ")
                                elem_list_opt[eaCnt].click()

                eaCnt = eaCnt + 1
            i = i + 1
            # if func_ali.has_duplicates(opt_name_list) == True:
            #     print('>> [S06] 중복 옵션명 있음 (확인필요) ')
            #     proc_LogSet(orderno, goodscode, "S06", "중복 옵션명 있음")
            #     return "S06"
            # else:
            #     print(">> 중복옵션명 없음 ")

        if cnt_opt_match == ali_opt_cnt:
            print(">> Option Matching Ok : {} | {} | {}".format(option_code, option_name, dicOpt['name']))
        else:
            print(">> Option Not Matching : 매칭cnt : {} | 옵션수 : {}".format(cnt_opt_match, ali_opt_cnt))
            print(">> 옵션코드 옵션명 갯수 불일치 SKIP 대상: {}".format(edit_option))
            proc_LogSet(orderno, goodscode, "S01", "옵션코드 옵션명 갯수 불일치")
            return "S01"

        print(">> 옵션 선택 완료 ")

    time.sleep(random.uniform(1, 1.5))
    ######################################################################
    # 배송 가능 여부 체크 
    ######################################################################
    if str(browser.page_source).find('배송지로 배송이 불가') > -1:
        print(">> 배송 불가능 : {}".format(aliCode))
        proc_LogSet(orderno, goodscode, "S024", "배송 불가")
        return "S024"

    ######################################################################
    # 수량 선택
    ######################################################################
    if int(d_ea) > 1:
        if str(browser.page_source).find('class="quantity--limit--') > -1:
            limit_tmp = func_ali.getparse(str(browser.page_source),'class="quantity--limit--','</div>')
            limit_ea = func_ali.getparse(limit_tmp,'>','개').strip()
            print(">> 주문가능 수량 : {}".format(limit_ea))
            if int(d_ea) > int(limit_ea):
                print(">> 주문 불가 수량 : 알리 - {} | 주문 - {} ".format(limit_ea, d_ea))
                proc_LogSet(orderno, goodscode, "S028", "주문 불가 수량 확인필요")
                return "S028"

        mainDriver.set_window_size(1600, 1400)
        mainDriver.maximize_window()
        time.sleep(0.5)
        func_ali.procInputEa(browser, d_ea, ali_screen_type)
        time.sleep(random.uniform(1, 1.5))

    ######################################################################
    # 배송기간 선택
    ######################################################################
    if str(browser.page_source).find('배송지로 배송이 불가능') > -1:
        print(">> 배송 불가능 : {}".format(aliCode))
        proc_LogSet(orderno, goodscode, "S024", "배송 불가능")
        return "S024"

    if str(browser.page_source).find('Select another product or address') > -1:
        print(">> 배송 불가능(Select another product or address) : {}".format(aliCode))
        proc_LogSet(orderno, goodscode, "S024", "배송 불가능")
        return "S024"

    # 배송 클릭
    rtnFlg = func_ali.selShipOption(browser, ali_screen_type)
    if rtnFlg == "1":
        print('>> 추적가능 배송 선택 완료 ')
    else:
        print('>> S024 : 추적가능 배송사 없음 확인필요 ')
        proc_LogSet(orderno, goodscode, "S024", "추적가능 배송사 없음")
        return "S024"

    time.sleep(random.uniform(1, 1.5))
    result_buy = str(browser.page_source)
    # buy_now = func_ali.getparse(result_buy,'class="product-action"','</span>')
    if ali_screen_type == 2:
        buy_now = func_ali.getparse(result_org,'class="action--container','')
        buy_now = func_ali.getparse(buy_now,'<button type','</button>')
    elif ali_screen_type == 3:
        buy_now = func_ali.getparse(result_buy,'class="quantity--','')
        if buy_now.find('class="pdp-wrap"') > -1:
            buy_now = func_ali.getparse(buy_now,'','class="pdp-wrap"')
    else:
        buy_now = func_ali.getparse(result_org,'class="product-action"','</span>')

    if str(buy_now).find('즉시 구매') > -1 or str(buy_now).find('Buy Now') > -1 or str(buy_now).find('Buy now') > -1 or str(buy_now).find('바로 구매') > -1:
        pass
        #print(">> 즉시 구매 버튼 존재 OK")
    elif str(result_buy).find('comet-btn-important"><span>바로 구매</span>') > -1:
        print(">> 바로 구매 버튼 존재 OK (type 2) ")
        pass
    else:
        print(">> 즉시 구매 버튼 확인불가")
        browser.get_screenshot_as_file('C:/project/log/D003_check_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "D003", "즉시 구매 버튼 확인불가")
        return "D003"

    # 즉시구매 버튼 (Element 클릭)
    # if browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow'):
    #     browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow').click()
    #     print('>> 즉시구매 Click OK')

    mainDriver.set_window_size(1500, 1200)
    time.sleep(random.uniform(1, 1.5))

    # 즉시구매 버튼 (Element 클릭)
    if str(ali_screen_type) == "2" or str(ali_screen_type) == "3":
        # findClassname3 = func_ali.getparse(str(browser.page_source),'class="comet-btn comet-btn-primary comet-btn-large buy-now--buynow--',' comet-btn-important')
        # findSelectname3 = 'button.comet-btn.comet-btn-primary.comet-btn-large.buy-now--buynow--' +str(findClassname3)+ '.comet-btn-important'
        findClassname3 = func_ali.getparse(str(browser.page_source),'comet-v2-btn comet-v2-btn-primary comet-v2-btn-large buy-now--buynow--',' comet-v2-btn-important')
        findSelectname3 = 'button.comet-v2-btn.comet-v2-btn-primary.comet-v2-btn-large.buy-now--buynow--' +str(findClassname3)+ '.comet-v2-btn-important'
        if browser.find_element(By.CSS_SELECTOR,findSelectname3):
            browser.find_element(By.CSS_SELECTOR,findSelectname3).click()
            print('>> 즉시구매 (type 2) Click OK')
        else:
            print('>> 즉시구매 버튼 확인 불가 (type 2) ')
            browser.get_screenshot_as_file('C:/project/log/check_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))
            proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매")
            return "D003"
    else:
        if browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow'):
            browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow').click()
            print('>> 즉시구매 Click OK')
        else:
            print('>> 즉시구매 버튼 확인 불가')
            browser.get_screenshot_as_file('C:/project/log/D003_check_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))
            proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매")
            return "D003"

    time.sleep(random.uniform(3,4))
    #print(">> current_url : {}".format(browser.current_url))

    ###########################################################################
    #  전체 입력값 및 상품 체크 하기 
    #  상품 / 가격 / 수량 / 주소 / 총 배송비 / 총합계 
    ###########################################################################
    orderCheckStyle = "0"
    if str(browser.current_url).find('/order/confirm_order.htm') > -1:
        time.sleep(0.5)
        orderCheckStyle = "1"
    elif str(browser.current_url).find('/p/trade/confirm.htm') > -1:
        time.sleep(0.5)
        orderCheckStyle = "2"
    else:
        print(">> Next page current_url 확인필요 ")
        time.sleep(2)
        browser.get_screenshot_as_file('C:/project/log/E03_check_'+str(orderno)+'.png')
        time.sleep(1)
        proc_LogSet(orderno, goodscode, "E03", "Next page Url 확인필요")
        return "E03"

    if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
        print(">> 배송 정보 및 주문검토 체크 불가 wait(3) ")
        time.sleep(random.uniform(13, 3.5))
    if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
        print(">> 배송 정보 및 주문검토 체크 불가2 wait(3) ")
        time.sleep(3)

    if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
        print(">> 배송 정보 및 주문검토 체크 불가 확인필요 ")
        browser.get_screenshot_as_file('C:/project/log/E04_check_'+str(orderno)+'.png')
        time.sleep(1)
        proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
        return "E04"

    if str(browser.page_source).find('결제 방법') == -1:
        time.sleep(2)

    #save_current_url = str(browser.current_url)
    curr_source = str(browser.page_source)
    if curr_source.find('주문 검토') > -1 or curr_source.find('결제 방법') > -1:
        print(">> 주문 검토 / 결제 방법 Ok ")
    else:
        browser.get_screenshot_as_file('C:/project/log/E04_check2_'+str(orderno)+'.png')
        time.sleep(1)
        proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
        return "E04"

    if browser.find_element(By.XPATH,'//*[@id="root"]'):
        txtOrd = str(browser.find_element(By.XPATH,'//*[@id="root"]').text)
        if txtOrd.find('주문하기') > -1 :
            print(">> 주문하기 버튼 존재 OK ")
        elif txtOrd.find('결제하기') > -1:
            print(">> 결제하기 버튼 존재 OK ")
        else:
            print(">> 주문하기 버튼 확인불가 ")
            browser.get_screenshot_as_file('C:/project/log/E04_check3_'+str(orderno)+'.png')  
            proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
            return "E04"
    else:
        browser.get_screenshot_as_file('C:/project/log/E04_check4_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
        return "E04"

    ######################## 
    # 선택 옵션 체크 
    ######################## 
    opt_url_check = str(browser.current_url)
    check_objectId = func_ali.getparse(str(opt_url_check),'objectId=','&').strip()
    check_skuAttr = func_ali.getparse(str(opt_url_check),'skuAttr=','&').strip()
    check_skuId = func_ali.getparse(str(opt_url_check),'skuId=','&').strip()
    check_quantity = func_ali.getparse(str(opt_url_check),'quantity=','').strip()

    option_ck_flg = "0"
    if opt_url_check.find("countryCode=KR") == -1:
        print(">> countryCode=KR 확인필요")
        option_ck_flg = "1"
    if opt_url_check.find(aliCode) == -1:
        print(">> objectId 확인필요")
        option_ck_flg = "1"
    if str(browser.page_source).find(check_skuId) == -1:
        print(">> skuId 확인필요")
        option_ck_flg = "1"

    if ali_opt_cnt > 0:
        skuAttr = str(check_skuAttr).replace("%3A",":")
        skuAttr = str(skuAttr).replace("%3B",";")
        skuAttr = str(skuAttr).replace("%23","#")
        skuAttr = str(skuAttr).replace("%20"," ")
        print(">> skuAttr : {}".format(skuAttr))
        for ea_code in sp_opt_code:
            if skuAttr.find(ea_code) > -1:
                print(">> Option Code Match Ok")
            else:
                print(">> check_skuAttr 확인필요")
                option_ck_flg = "1"

    if option_ck_flg == "1":
        proc_LogSet(orderno, goodscode, "S027", "옵션 선택 불일치 확인필요")
        print(">> 옵션 선택 불일치 확인필요")
        return "S027"

    if opt_url_check.find('quantity='+str(check_quantity)) == -1:
        print(">> 수량 선택 불일치 확인필요")
        proc_LogSet(orderno, goodscode, "S028", "수량 선택 불일치 확인필요")
        return "S028"


    ##############################################
    sql = getMakeSql("addr", Ouid, Iuid, "", "", "")
    #print(">> sql : {}".format(sql))
    row_rcv = db_FS.selectone(sql)
    if not row_rcv:
        print(">> 배송준비중 상태가 아닙니다. ")
        proc_LogSet(orderno, goodscode, "S016", "배송준비중 상태가 아님")
        return "S016"

    # sql = " select t.uid, i.OrderUid, OrderNo, SettlePrice, RcvPost, rcvName, replace(soc_no,'p','P'), RcvMobile, RcvAddr, RcvAddrDetail "
    m_SettlePrice = row_rcv[3]
    m_RcvPost = str(row_rcv[4]).replace('-','').strip()
    m_rcvName = str(row_rcv[5]).strip()
    m_soc_no = str(row_rcv[6]).strip()
    m_RcvMobile = str(row_rcv[7]).replace('-','').strip()
    m_RcvAddr = str(row_rcv[8]).strip()
    m_RcvAddrDetail = str(row_rcv[9]).strip()
    m_cancel_cate = str(row_rcv[10]).strip()
    m_cancel_reason = str(row_rcv[11]).strip()
    m_coupang_auto = str(row_rcv[12]).strip()
    m_naver_pay_order_id = str(row_rcv[13]).strip()
    m_naver_pay_unitprice = str(row_rcv[14]).strip()
    m_sitecate = str(row_rcv[15]).strip()
    m_RcvAddrDetail = replaceQueryString(m_RcvAddrDetail)
    # if m_naver_pay_order_id != "":
    #     if m_sitecate == "mini":
    #         m_SettlePrice = int(m_naver_pay_unitprice) + 3000
    #     else:
    #         m_SettlePrice = int(m_naver_pay_unitprice)
    m_RcvAddrDetail = m_RcvAddrDetail + " (주문:" +str(orderno)+ ")"
    #print(">> 상세 주소 : {}".format(m_RcvAddrDetail))
    print(">> m_SettlePrice : {} | m_RcvPost : {} | m_rcvName : {} | m_soc_no : {} | m_RcvAddr : {} | m_RcvAddrDetail : {} | m_cancel_cate : {}".format(m_SettlePrice, m_RcvPost, m_rcvName, m_soc_no, m_RcvAddr, m_RcvAddrDetail, m_cancel_cate))

    if m_coupang_auto != "1":
        rtn_msg = "자동주문 대상에서 제외 "
        proc_LogSet(m_OrderNo, m_GoodsCode, "S031", rtn_msg)
        return "S031"

    if m_cancel_cate != "" or m_cancel_reason != "":
        rtn_msg = "취소사유 있음"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S006", rtn_msg)
        return "S006"

    curr_source1 = browser.page_source
    time.sleep(0.5)
    ali_won_cost = ""
    sell_marzin = ""
    sell_marzin_rate = 0
    ali_delivery_cost = "0"
    dev_detail = ""
    if orderCheckStyle == "1":
        if str(curr_source1).find('class="shopping-cart-product"') > -1:
            if str(curr_source1).find('class="logistics-company"') > -1:
                ali_logistics_company = func_ali.getparse(str(curr_source1),'class="logistics-company">','</span>')
                ali_delivery_day = func_ali.getparse(str(curr_source1),'class="logistics-delivery">','</span>').replace('<font color="#000000">','').replace('</font>','')
                ali_delivery_price = func_ali.getparse(str(curr_source1),'class="logistics-cost ">','</span>')
                if str(ali_delivery_price).find('$') > -1:
                    ali_delivery_price = func_ali.getparse(str(ali_delivery_price),'$','')
                if str(ali_delivery_price).find('₩') > -1:
                    ali_delivery_price = func_ali.getparse(str(ali_delivery_price),'₩','')
                ali_delivery_price = str(ali_delivery_price).replace('US','').replace('$','')
                print(">> (0) {} | {} | {}".format(ali_logistics_company, ali_delivery_day, ali_delivery_price))
                dev_detail = ali_logistics_company + " | " + ali_delivery_day + " | " + ali_delivery_price

            ali_goods_cost = func_ali.getparse(str(curr_source1),'class="charge-cost">','</div>')
            ali_delivery_cost = func_ali.getparse(str(curr_source1),'<div class="charge-title">배송','</div>')
            if str(ali_delivery_cost).strip() == "":
                ali_delivery_cost = "0"
            ali_total_cost = func_ali.getparse(str(curr_source1),'class="total-cost"','</div>')
            print(">> (1) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
        else:
            ali_goods_cost = func_ali.getparse(str(curr_source1),'소계','배송')
            ali_goods_cost = func_ali.getparse(str(ali_goods_cost),'US','</div>')
            ali_delivery_cost = func_ali.getparse(str(curr_source1),'배송','총액')
            if ali_delivery_cost.find('무료') > -1:
                ali_delivery_cost = "0"
            else:
                ali_delivery_cost = func_ali.getparse(str(ali_delivery_cost),'US','</div>')
            if str(curr_source1).find("주문하기") > -1:
                ali_total_cost = func_ali.getparse(str(curr_source1),'총액','주문하기')
            elif str(curr_source1).find("지금 결제하기") > -1:
                ali_total_cost = func_ali.getparse(str(curr_source1),'총액','지금 결제하기')
            else:
                ali_total_cost = func_ali.getparse(str(curr_source1),'총액','결제하기')
            ali_total_cost = func_ali.getparse(str(ali_total_cost),'US','</div>').replace('</span>','')
            dev_detail = "총 배송비 : " + ali_delivery_cost 
            print(">> (2) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
    elif orderCheckStyle == "2":
        ali_goods_cost = func_ali.getparse(str(curr_source1),'총 상품 금액','총 배송비')
        ali_goods_cost = func_ali.getparse(str(ali_goods_cost),'US','</div>')
        ali_delivery_cost = func_ali.getparse(str(curr_source1),'총 배송비','총 합계')
        if ali_delivery_cost.find('무료') > -1:
            ali_delivery_cost = "0"
        else:
            ali_delivery_cost = func_ali.getparse(str(ali_delivery_cost),'US','</div>')
        if str(curr_source1).find("주문하기") > -1:
            ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','주문하기')
        elif str(curr_source1).find("지금 결제하기") > -1:
            ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','지금 결제하기')
        else:
            ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','결제하기')
        ali_total_cost = func_ali.getparse(str(ali_total_cost),'US','</div>').replace('</span>','')
        dev_detail = "총 배송비 : " + ali_delivery_cost 
        print(">> (3) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
    else:
        print(">> 상품 금액 확인 불가 (exit)")
        browser.get_screenshot_as_file('C:/project/log/S020_check_'+str(orderno)+'.png')
        ###################
        input(">> tmp_ali_total_cost Check (1): ")
        #print(">> page_source : {}".format(str(browser.page_source)))
        input(">> tmp_ali_total_cost Check (end): ")
        ###################
        proc_LogSet(orderno, goodscode, "S020", "상품 금액 확인 불가 ")
        return "S020"

    tmp_ali_total_cost = str(ali_total_cost)
    while (tmp_ali_total_cost.find('<span') > -1):
        if tmp_ali_total_cost.find('<span') > -1:
            strSpan = '<span ' + func_ali.getparse(str(tmp_ali_total_cost),'<span','>') + '>'
            tmp_ali_total_cost = tmp_ali_total_cost.replace(strSpan,'')

    tmp_ali_total_cost = str(tmp_ali_total_cost).replace('<p>','').replace('</p>','').replace('<span','').replace('>','').replace('<','').replace('$','').strip()
    tmp_ali_total_cost = regRemoveText(tmp_ali_total_cost)

    if str(tmp_ali_total_cost).replace('.','').isdigit() == True:
        print(">> tmp_ali_total_cost : {}".format(tmp_ali_total_cost))
    else:
        print(">> 상품 금액 확인 불가 (exit)")
        print(">> tmp_ali_total_cost : {}".format(tmp_ali_total_cost))
        browser.get_screenshot_as_file('C:/project/log/S020_check_'+str(orderno)+'.png')
        ###################
        input(">> tmp_ali_total_cost Check (2): ")
        #print(">> page_source : {}".format(str(browser.page_source)))
        input(">> tmp_ali_total_cost Check (end): ")
        ###################
        proc_LogSet(orderno, goodscode, "S020", "상품 금액 확인 불가 ")
        return "S020"

    ali_total_cost = str(tmp_ali_total_cost)
    ali_goods_cost = func_ali.curr_replace(ali_goods_cost)
    ali_delivery_cost = func_ali.curr_replace(ali_delivery_cost)
    ali_total_cost = func_ali.curr_replace(ali_total_cost)
    print(">> {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))

    # login_mode : 1 -> input 키값 확인후 진행
    # debug_mode : 1 -> input 키값 확인후 진행
    # gOrder_mode : 1 -> 실제 주문 모드
    # connect_mode : chrome_mode 
    gExchangerate = 1350
    gMarzin_rate = 10
    gDelivery_cost = 4.0
    order_screen_img = ""
    card_lastnum = ""
    sql = "select login_id, debug_mode, order_mode, exchangerate, marzin_rate, delivery_cost, order_screen_img, isnull(marzin,0), isnull(marzin_set,0), isnull(mini_delivery_fee,0), isnull(card_lastnum,'') from ali_order_auto_set where login_ip = '{}'".format(currIp)
    row = db_FS.selectone(sql)
    if row:
        loginId = row[0]
        debug_mode = row[1]
        gOrder_mode = row[2]
        gExchangerate = row[3]
        gMarzin_rate = row[4]
        gDelivery_cost = row[5]
        order_screen_img = row[6]
        gMarzin = row[7]
        gMarzin_set = row[8]
        mini_delivery_fee = row[9]
        card_lastnum = row[10]
    print(">> ID : {} | debug_mode : {} | gOrder_mode : {} | (설정마진)gMarzin : {} | (gMarzin_set) {} | card_num : {}".format(loginId, debug_mode, gOrder_mode, gMarzin, gMarzin_set, card_lastnum))

    if m_naver_pay_order_id != "":
        if m_sitecate == "mini":
            m_SettlePrice = int(m_naver_pay_unitprice) + int(mini_delivery_fee)
            print(">> m_SettlePrice (naver_pay_unitprice) : {} ".format(m_SettlePrice))
        else:
            m_SettlePrice = int(m_naver_pay_unitprice)
            print(">> m_SettlePrice (naver_pay_unitprice) : {} ".format(m_SettlePrice))

    if float(ali_delivery_cost) > gDelivery_cost:
        print(">> 배송비 {}달러 초과 ".format(gDelivery_cost))
        proc_LogSet(orderno, goodscode, "S021", "배송비 " +str(gDelivery_cost)+ "달러 초과")
        return "S021"
    else:
        print(">> 배송비 OK : {} ".format(ali_delivery_cost))
    ali_won_cost = float(ali_total_cost) * gExchangerate
    print(">> 원가 | ali: {} * {} = {}".format(ali_total_cost, gExchangerate, ali_won_cost))
    sell_marzin = float(m_SettlePrice) - float(ali_won_cost)
    print(">> 마진 | {} - {} = {}".format(m_SettlePrice, ali_won_cost, sell_marzin))
    # if float(sell_marzin) < 0:
    #     print(">> sell_marzin 가격 초과 확인필요 : {}".format(sell_marzin))
    #     proc_LogSet(orderno, goodscode, "S022", "가격 초과 확인필요")
    #     return "S022"

    if float(sell_marzin) < int(gMarzin):
        print(">> sell_marzin 가격 초과 확인필요 : {}".format(sell_marzin))
        if str(gMarzin_set) == "0" or str(gMarzin_set) == "1":
            proc_LogSet(orderno, goodscode, "S022", "가격 초과 확인필요")
            return "S022"

    sell_marzin_rate = int((sell_marzin / m_SettlePrice) * 100)
    if sell_marzin_rate < gMarzin_rate:
        print(">> 마진율 {}% 이하 가격 확인필요 : {}".format(gMarzin_rate, sell_marzin_rate))
        if str(gMarzin_set) == "0" or str(gMarzin_set) == "2":
            proc_LogSet(orderno, goodscode, "S023", "마진율 " +str(gMarzin_rate)+ "% 이하 가격 확인필요")
            return "S023"
    else:
        print(">> 마진율 : {}".format(sell_marzin_rate))

    # 통관정보 클릭하기 #####################################################################
    if str(curr_source1).find('통관 정보') > -1 or str(curr_source1).find('pl-clearance-change') > -1:
        time.sleep(random.uniform(0.5, 1))
        if browser.find_element(By.CSS_SELECTOR,'div.pl-main-container.large > div:nth-child(2) > div > span'): #변경 버튼클릭
            browser.find_element(By.CSS_SELECTOR,'div.pl-main-container.large > div:nth-child(2) > div > span').click()
            print(">> 통관정보 변경 버튼 Clicked ")

            time.sleep(random.uniform(2, 2.5))
            # 통관 정보 팝업창 확인 #####################################################################
            if str(browser.page_source).find('class="deliver-address-wrap"') > -1:
                func_ali.elem_clear(browser, "[placeholder='받는 사람*']")
                func_ali.elem_clear(browser, "[placeholder='휴대폰 번호*']")
                func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")

                func_ali.elem_clear(browser, "[placeholder='받는 사람*']")
                browser.find_elements(By.CSS_SELECTOR,"[placeholder='받는 사람*']")[0].send_keys(m_rcvName)
                time.sleep(0.2)
                func_ali.elem_clear(browser, "[placeholder='휴대폰 번호*']")
                browser.find_elements(By.CSS_SELECTOR,"[placeholder='휴대폰 번호*']")[0].send_keys(m_RcvMobile)
                time.sleep(0.2)
                func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")
                browser.find_elements(By.CSS_SELECTOR,"[placeholder='개인통관고유부호*']")[0].send_keys(m_soc_no)
                time.sleep(random.uniform(1, 1.5))

                # 개인통관고유부호 수집 및 이용 동의（필수） 체크 
                if browser.find_elements(By.CSS_SELECTOR,'span.next-checkbox')[0]:
                    browser.find_elements(By.CSS_SELECTOR,'span.next-checkbox')[0].click()
                time.sleep(random.uniform(1, 1.5))
                tmp_agree = func_ali.getparse(str(browser.page_source),'class="deliver-address-wrap"','class="next-checkbox-label"')
                tmp_agree = func_ali.getparse(tmp_agree,'type="checkbox"','</span>')
                if tmp_agree.find('aria-checked="true"') > -1: # 체크 되었는지 확인
                    print(">> 개인통관 수집 동의 체크 확인 OK")
                else:
                    browser.find_elements(By.CSS_SELECTOR,'span.next-checkbox')[0].click()
                time.sleep(0.5)
                if browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button'):
                    browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button').click()
                    print(">> 확인버튼 클릭")
                time.sleep(random.uniform(1, 1.5))

    time.sleep(1)

    # 주소 수정 버튼 클릭하기 #####################################################################
    if str(curr_source1).find('다른 주소를 선택') > -1 or str(curr_source1).find('Select other addresses') > -1:
        if browser.find_element(By.CSS_SELECTOR,'div.address-list-opt > button:nth-child(2)'): #수정하기 버튼
            browser.find_element(By.CSS_SELECTOR,'div.address-list-opt > button:nth-child(2)').click()
            print(">> 주소 수정 버튼")

    elif str(curr_source1).find('Change') > -1:
        if browser.find_element(By.XPATH,'//*[@id="placeorder_wrap__inner"]/div/div[1]/div[1]/div/div[2]/span/a'): #Change 버튼
            browser.find_element(By.XPATH,'//*[@id="placeorder_wrap__inner"]/div/div[1]/div[1]/div/div[2]/span/a').click()
            print(">> 주소 Change 버튼")
    else:
        print(">> 주소 변경 버튼 없음 확인필요 ")
        browser.get_screenshot_as_file('C:/project/log/E01_check_'+str(orderno)+'.png')
        time.sleep(random.uniform(1, 1.5))
        proc_LogSet(orderno, goodscode, "E01", "주소 변경 버튼 없음 확인필요")
        return "E01"

    time.sleep(random.uniform(2, 2.5))
    curr_source2 = browser.page_source
    time.sleep(random.uniform(0.5, 1))

    # 배송주소 (기본) 수정하기 버튼 클릭 #####################################################################
    if str(curr_source2).find('수정하기') > -1:
        if browser.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/span/a'):
            browser.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/span/a').click()
            print(">> 배송주소 (기본) 수정하기 ")
    elif str(curr_source2).find('수정') > -1 or str(curr_source2).find('Edit') > -1:
        if browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/ul/li[1]/div[2]/button[2]'):
            browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/ul/li[1]/div[2]/button[2]').click()
            print(">> 배송주소 (기본) 수정") 
    else:
        if browser.find_elements(By.CSS_SELECTOR,"[ae_page_area='Deliver_to_an_address']")[0]:
            browser.find_elements(By.CSS_SELECTOR,"[ae_page_area='Deliver_to_an_address']")[0].click()
            print(">> 배송주소 (기본) change")

    # 배송주소 입력하기 시작 #####################################################################
    time.sleep(0.5)
    try:
        wait = WebDriverWait(browser, 20)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.section-title")))
    except Exception as e:
        print(">> 배송주소 수정 Exception ")

    curr_source3 = browser.page_source
    time.sleep(0.5)

    if str(curr_source3).find('개인정보') == -1:
        time.sleep(random.uniform(2, 2.5))
        curr_source3 = browser.page_source

    soc_check_tmp = func_ali.getparse(str(curr_source3),'대한민국 국적입니다','YES')
    if str(soc_check_tmp).find('aria-checked="false"') > -1:
        print(">> 현재 대한민국 국적 : No Checked ")

    func_ali.elem_clear(browser, "[placeholder='받는 사람*']")
    func_ali.elem_clear(browser, "[placeholder='휴대폰 번호*']")
    func_ali.elem_clear(browser, "[placeholder='번지, 건물/아파트/단위*']")
    # func_ali.elem_clear(browser, "[placeholder='아파트, 사무실, 부서 등']")
    func_ali.elem_clear(browser, "[placeholder='상세주소 입력']")
    func_ali.elem_clear(browser, "[placeholder='우편번호*']")

    # if str(curr_source3).find("여권번호/외국인등록증번호") > -1:
    #     # func_ali.elem_clear(browser, "[placeholder='여권번호/외국인등록증번호']")
    #     func_ali.elem_clear(browser, "[placeholder='여권번호/외국인등록증번호*']")
    # else:
    #     func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")
    time.sleep(random.uniform(1, 1.5))

    func_ali.elem_clear(browser, "[placeholder='받는 사람*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='받는 사람*']")[0].send_keys(m_rcvName)
    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='휴대폰 번호*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='휴대폰 번호*']")[0].send_keys(m_RcvMobile)
    time.sleep(0.2)

    # if str(browser.find_elements(By.CSS_SELECTOR,"[placeholder='도시*']")[0].text) == "Other":
    #     print(">> 이미 Other 설정되어있음 ")
    # else:
    #     # Other 설정
    #     func_ali.setAddrOther(browser)
    #     time.sleep(0.3)
    #     func_ali.elem_clear(browser, "[placeholder='도시*']")
    #     browser.find_elements(By.CSS_SELECTOR,"[placeholder='도시*']")[0].send_keys('Other')

    # browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field")[1]
    # func_ali.getparse(str(browser.page_source),'<input placeholder="상세주소 입력','')
    # func_ali.getparse(str(browser.page_source),'<div class="next-overlay-wrapper opened"','')
    # browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child(4)')

    ## 주소 입력 변경 23.11.23
    ## m_RcvAddr = " 강원특별자치도 원주시 양지로 160 (반곡동, 원주혁신도시 8단지 사랑으로 부영아파트)"
    rtn_addr1, rtn_addr2, rtn_addr3 = func_ali.cut_address(db_FS, m_RcvAddr)
    if rtn_addr1 == "" or rtn_addr2 == "" or rtn_addr3 == "":
        proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(2)")
        return "S030"

    city_elem = browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field")
    # 시 입력
    if city_elem[1]:
        city_elem[1].click()
        time.sleep(0.5)

        addr_source = func_ali.getparse(str(browser.page_source),'<div class="next-overlay-wrapper opened"','')
        addr_source = func_ali.getparse(addr_source,'<ul role="listbox"','</ul>')
        sp_addr = addr_source.split('</li>')
        liCnt = 0
        city1_chk = 0
        city2_chk = 0
        for ea_addr in sp_addr:
            opt_title = func_ali.getparse(ea_addr,'role="option" title="','"')
            liCnt = liCnt + 1
            if opt_title == rtn_addr1:
                print(">>Find (1) OK - ({}) : {}".format(liCnt, opt_title))
                city1_chk = 1
                break
        browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child('+str(liCnt)+')').click()
        time.sleep(2)

        city_elem_after = browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field > em")
        if str(city_elem_after[1].text).strip() == rtn_addr1.strip():
            print(">> addr1 Select Ok : {}".format(city_elem[1].text))
        else:
            print(">> addr1 Unmatch Check Please : {}".format(city_elem[1].text))
            proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(1)")
            return "S030"

        time.sleep(1)
        # 주소 구/시 입력
        if rtn_addr2 == "Other":
            print(">> addr2 : Other ")
            city2_chk = 1
        else:
            city_elem = browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field")
            print(city_elem)
            if city1_chk == 1:
                if city_elem[2]:
                    print(">> 2 click before ")
                    city_elem[2].click()
                    time.sleep(0.5)
                    addr_source = func_ali.getparse(str(browser.page_source),'<div class="next-overlay-wrapper opened"','')
                    addr_source = func_ali.getparse(addr_source,'<ul role="listbox"','</ul>')
                    sp_addr = addr_source.split('</li>')
                    liCnt2 = 0

                    for ea_addr in sp_addr:
                        opt_title = func_ali.getparse(ea_addr,'role="option" title="','"')
                        liCnt2 = liCnt2 + 1
                        if opt_title == rtn_addr2:
                            city2_chk = 1
                            print(">>Find (2) OK - ({}) : {}".format(liCnt2, opt_title))
                            break
                    time.sleep(0.5)
                    browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child('+str(liCnt2)+')').click()
                    time.sleep(1)

        if city1_chk == 1 and city2_chk == 1:
            pass
        else:
            proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(2)")
            return "S030"

        time.sleep(0.5)
        addr_source2 = func_ali.getparse(str(browser.page_source),'<input placeholder="상세주소 입력','placeholder="우편번호*"')
        sp_addr2 = addr_source2.split('</em>')
        chkCnt = 0
        for ea_chk in sp_addr2:
            chkCnt = chkCnt + 1
            opt_title = func_ali.getparse(ea_chk,'<em title="','"')
            if chkCnt == 2:
                if str(opt_title).strip() == rtn_addr2.strip():
                    print(">> addr2 Select Ok : {} | {}".format(opt_title, opt_title))
                else:
                    print(">> addr2 Unmatch Check Please : {} | {}".format(opt_title, opt_title))

    else:
        proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(0)")
        return "S030"

    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='우편번호*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='우편번호*']")[0].send_keys(m_RcvPost)
    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='번지, 건물/아파트/단위*']")

    ## browser.find_elements(By.CSS_SELECTOR,"[placeholder='번지, 건물/아파트/단위*']")[0].send_keys(m_RcvAddr)
    # 주소3 입력 변경 23.11.23
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='번지, 건물/아파트/단위*']")[0].send_keys(rtn_addr3)

    time.sleep(0.2)
    # func_ali.elem_clear(browser, "[placeholder='아파트, 사무실, 부서 등']")
    # browser.find_elements(By.CSS_SELECTOR,"[placeholder='아파트, 사무실, 부서 등']")[0].send_keys(m_RcvAddrDetail)
    func_ali.elem_clear(browser, "[placeholder='상세주소 입력']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='상세주소 입력']")[0].send_keys(m_RcvAddrDetail)
    time.sleep(random.uniform(1, 1.5))

    if len(m_rcvName) < 4:
        # if str(curr_source3).find("여권번호/외국인등록증번호*") > -1:
        #     # 대한민국 국적입니다. YES 클릭
        #     if browser.find_elements(By.CSS_SELECTOR,'input.next-radio-input')[0]:
        #         browser.find_elements(By.CSS_SELECTOR,'input.next-radio-input')[0].click()
        #         time.sleep(1)
        # func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")
        # browser.find_elements(By.CSS_SELECTOR,"[placeholder='개인통관고유부호*']")[0].send_keys(m_soc_no)
        time.sleep(0.2)
    else:
        print(">> 수령인명 확인 필요 : {} ".format(m_rcvName))
        proc_LogSet(orderno, goodscode, "S017", "수령인명 확인 필요")
        return "S017"
###################################################################
    # input(">> address checak after : ")
###################################################################
    # if str(curr_source3).find("여권번호/외국인등록증번호") > -1:
    #     browser.find_elements(By.CSS_SELECTOR,"[placeholder='여권번호/외국인등록증번호']")[0].send_keys(m_soc_no)
    # else:
    #     browser.find_elements(By.CSS_SELECTOR,"[placeholder='개인통관고유부호']")[0].send_keys(m_soc_no)
    # print(">> 배송 주소 입력 완료 ")

    # # 개인통관고유부호 수집 및 이용 동의（필수） 체크 
    # if browser.find_elements(By.CSS_SELECTOR,'span.next-checkbox')[0]:
    #     browser.find_elements(By.CSS_SELECTOR,'span.next-checkbox')[0].click()

    time.sleep(random.uniform(1, 1.5))
    # 배송 주소 편집  Confirm 클릭
    #if browser.find_elements(By.CSS_SELECTOR,'span.next-btn-helper')[0]:
    #    browser.find_elements(By.CSS_SELECTOR,'span.next-btn-helper')[0].click()
    if browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button'):
        browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button').click()
        print(">> 배송 주소 입력후 Confirm 클릭")

    time.sleep(random.uniform(3, 3.5))
    curr_source4 = browser.page_source
    # 배송주소 (기본) 버튼 클릭 #####################################################################
    if str(curr_source4).find('기본') > -1 or str(curr_source4).find('Default') > -1:
        try: # browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-opt-btn > span')[0]
            # if browser.find_element(By.CSS_SELECTOR,'span.cm-address-item-content-default-tag'):
            #     browser.find_element(By.CSS_SELECTOR,'span.cm-address-item-content-default-tag').click()
            print(">> 배송주소 첫번째 선택 ")
            if browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-content'):
                browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-content')[0].click()
                time.sleep(random.uniform(1, 1.5))
        except Exception as e:
            print(">> 배송주소 기본 버튼 클릭 Exception ")
            input(">> 알리 Key (기본) 설정을 눌러 주세요 그리고 command 창에 아무키나 입력해주세요: ")
        else:
            print(">> 배송주소 첫번째 선택 클릭 Ok ")
    # input(">> check address : ")

    # 배송주소 입력하기 완료 #####################################################################
    time.sleep(2)
    curr_source5 = browser.page_source
    time.sleep(random.uniform(1, 1.5))

    if str(curr_source5).find("배송 정보") > -1 or str(curr_source5).find("배송 주소") > -1  or str(curr_source5).find("shipping address") > -1:
        pass
        #print(">> 배송 정보 Ok")
    else:
        print(">> 배송 정보 입력 오류 (exit)")
        browser.get_screenshot_as_file('C:/project/log/S019_check_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류")
        return "S019"

    delievey_check_str = str(curr_source5)
    if str(curr_source5).find('class="card-container') > -1:
        delievey_check_str = func_ali.getparse(str(curr_source5),'','class="card-container')
    if str(delievey_check_str).find(m_rcvName) > -1:
        if str(delievey_check_str).find(m_RcvMobile) == -1:
            proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (수령인)")
            return "S019"            
    else:
        if browser.find_element(By.CLASS_NAME,'address-item'):
            delievey_check_str = browser.find_element(By.CLASS_NAME,'address-item').text
            if str(delievey_check_str).find(m_rcvName) == -1:
                proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (수령인)")
                return "S019"   

    if str(delievey_check_str).find(m_RcvMobile) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (휴대폰)")
        return "S019" 
    if str(delievey_check_str).find(m_RcvPost) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (우편번호)")
        return "S019" 
    # if str(delievey_check_str).find(m_RcvAddr) == -1:
    if str(delievey_check_str).find(rtn_addr3) == -1: ## 주소입력 변경
        #print(">> delievey_check_str : {}".format(delievey_check_str))
        print(">> rtn_addr3 : {}".format(rtn_addr3))
        #input(">> 배송 정보 입력 오류 (주소) : ")
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주소)")
        return "S019" 
    if str(delievey_check_str).find(orderno) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주문번호)")
        return "S019"

    time.sleep(0.5)
    # 통관 정보 입력후 입력값 체크
    tmp_clearance = func_ali.getparse(str(browser.page_source),'class="pl-clearance-item__head__','</span>')
    print(">> 통관정보 수령인  : {}".format(m_rcvName))
    if str(tmp_clearance).find(m_rcvName) > -1:
        print(">> 통관정보 수령인 확인 OK : {}".format(m_rcvName))
    else:
        proc_LogSet(orderno, goodscode, "S060", "통관정보 입력불가 확인필요")
        return "S060"

    ##################################################################################
    # 결제 방법 선택
    ##################################################################################
    curr_source = str(browser.page_source)
    sour_pay_tmp = func_ali.getparse(str(browser.page_source),'class="payment-safe-info-content"','id="payment-botton-section"')
    sp_pay = sour_pay_tmp.split('data-pl="payment-method-title"')
    print(">> Len(sp_pay) : {}".format(len(sp_pay)))

    payCnt = 0
    pay_index = 0
    for ea_pay in sp_pay:
        if payCnt == 0:
            payCnt = payCnt + 1
            continue
        pay_name = func_ali.getparse(str(ea_pay),'>','</span>')
        #print(">> [{}] pay_name : {}".format(payCnt, pay_name))
        if pay_name.find(card_lastnum) > -1:
            pay_index = payCnt
            print(">> Pay_index : {} | card num : {} | pay_name : {} ".format(pay_index, card_lastnum, pay_name))
            break
        payCnt = payCnt + 1

    if pay_index == 0:
        print(">> Card 결제방법 확인필요 " )
        input(">> 결제 방법 카드가 확인 되지 않았습니다. 선택후 아무키나 입력해 주세요:")

    if curr_source.find('변화') > -1  or curr_source.find('결제 방법 선택') > -1 or curr_source.find('더보기') > -1:
        if curr_source.find('결제 방법 선택') > -1:
            print(">> (결제 방법) 결제 방법 선택 ")

            findClassname = ""
            sour_tmp = func_ali.getparse(str(browser.page_source),'data-pl="payment-method-title"','')
            findClassnameT = ""
            findClassnameC = ""
            if str(sour_tmp).find('chosen-channel--chosen-channel-container--') > -1:
                findClassnameT = func_ali.getparse(str(sour_tmp),'chosen-channel--chosen-channel-container--','"').replace(' ','.')
                print(">> findClassnameT : {}".format(findClassnameT))
            if str(sour_tmp).find('chosen-channel--chosen-channel-content--') > -1:
                findClassnameC = func_ali.getparse(str(sour_tmp),'chosen-channel--chosen-channel-content--','"').replace(' ','.')
                print(">> findClassnameC : {}".format(findClassnameC))
            if findClassnameT != "" and findClassnameC != "":
                findClassname = 'div.placeorder-page-payment-container > div.chosen-channel--chosen-channel-container--' +str(findClassnameT)+ ' > div.chosen-channel--chosen-channel-content--' +str(findClassnameC)+ ' > span > span > span'

        elif curr_source.find('변화') > -1:
            print(">> (결제 방법) 변화 ")
            findClassname = ""
            findClassname = func_ali.getparse(str(curr_source),'결제 방법','class="pl-store-container')
            if findClassname.find('결제 방법') > -1:
                findClassname = func_ali.getparse(findClassname,'결제 방법','')
            if findClassname.find('변화') > -1:
                findClassname = func_ali.getparse(findClassname,'','변화')
            # print("\n-----------------------------------")
            print(">> findClassname(2-1): {}".format(findClassname))
            # print("\n-----------------------------------")
            findClassname = func_ali.getparse(findClassname,'type="button" class="','"').strip()
            findClassname = 'button.' + findClassname.replace(' ','.')
            print(">> (결제 방법) 변화 : {}".format(findClassname))

        elif curr_source.find('더보기') > -1:
            print(">> (결제 방법) 더보기 ")
            findClassname = ""
            findClassname = func_ali.getparse(str(curr_source),'결제 방법','class="pl-store-container')
            if findClassname.find('결제 방법') > -1:
                findClassname = func_ali.getparse(findClassname,'결제 방법','')
            if findClassname.find('더보기') > -1:
                findClassname = func_ali.getparse(findClassname,'','더보기')
            # print("\n-----------------------------------")
            print(">> findClassname(2-2): {}".format(findClassname))
            # print("\n-----------------------------------")
            findClassname = func_ali.getparse(findClassname,'<span class="','"').strip()
            findClassname = 'span.' + findClassname.replace(' ','.')
            print(">> (결제 방법) 더보기 : {}".format(findClassname))

        if findClassname != "":
            print(">> findClassname : {}".format(findClassname))
            if browser.find_element(By.CSS_SELECTOR, findClassname):
                ## div.chosen-channel--chosen-channel-container--2TwO5WE.chosen-channel--pc--2DZIgIG > div.chosen-channel--chosen-channel-content--3OYmsMr > span > span > span
                browser.find_element(By.CSS_SELECTOR, findClassname).click() # 결제방법선택 (더보기)
                time.sleep(random.uniform(1, 1.5))
                print(">> 결제 방법 선택 Ok ")
                if str(browser.page_source).find('comet-modal-body pop-modal--payment-container-body--') > -1:
                    findClassP = func_ali.getparse(str(browser.page_source),'comet-modal-body pop-modal--payment-container-body--','"')
                    findClassP = 'div.comet-modal-body.pop-modal--payment-container-body--' +str(findClassP)
                    print(">> findClassP : {}".format(findClassP))
                    if str(ali_screen_type) == "3":
                        findClassnameP = findClassP.replace(' ','.') + '.payment-container-body > div:nth-child(1) > div:nth-child(' + str(pay_index) + ') > div > div'
                    else:
                        findClassnameP = findClassP.replace(' ','.') + ' > div:nth-child(1) > div:nth-child(' + str(pay_index) + ') > div > div'
                    print(">> (카드선택) findClassnameP : {}".format(findClassnameP))
                    # browser.find_element(By.CSS_SELECTOR, 'div.comet-modal-body.pop-modal--payment-container-body--3TzH3_f.payment-container-body > div:nth-child(1) > div:nth-child(2) > div > div')
                    browser.find_element(By.CSS_SELECTOR, findClassnameP).click() # 카드선택
                    time.sleep(random.uniform(1, 1.5))
                    print(">> (카드선택 확인) Click Before ")
                    browser.find_element(By.CSS_SELECTOR, '#payment-botton-section > button').click() # 카드선택(확인)
                    time.sleep(random.uniform(1, 1.5))
                    print(">> (카드선택 확인) Click Ok ")

    sour_tmp = func_ali.getparse(str(browser.page_source),'data-pl="payment-title"','type="button"')
    if sour_tmp.find('class="chosen-channel--chosen-channel-icon--') > -1:
        print(">> Card Icon OK " )
    else:
        print(">> No Card Icon -- Check Please " )
        input(">> 결제 방법 선택이 되지 않았습니다. 선택후 아무키나 입력해 주세요:")

    sour_pay_tmp = func_ali.getparse(str(browser.page_source),'class="payment-safe-info-content"','id="payment-botton-section"')
    if sour_pay_tmp.find(card_lastnum) == -1:
        print(">> 결제카드번호가 없습니다. 확인해 주세요. ")
        input(">> 결제 방법 선택 되지 않았습니다.(2) 선택후 아무키나 입력해 주세요:")
    else:
        print(">> {} 결제카드 선택 확인 완료 ".format(card_lastnum))

    # 정보 권한 부여 (동의 체크)
    if browser.find_element(By.CSS_SELECTOR,'div.pl-block-agreement-pc > label > span.comet-checkbox-icon'):
        browser.find_element(By.CSS_SELECTOR,'div.pl-block-agreement-pc > label > span.comet-checkbox-icon').click()
        time.sleep(random.uniform(1.5, 2))

    # input(">> 결제전 Test : ")

    # if str(browser.page_source).find('결제 방법 선택') > -1:
    #     # print(">> 결제 방법 선택 되지 않았습니다. 확인해 주세요. ")
    #     input(">> 결제 방법 선택 되지 않았습니다. 선택후 아무키나 입력해 주세요:")
    #     time.sleep(0.5)
    ##################################################################################
    mainDriver.set_window_size(1500, 1200)
    time.sleep(0.5)
    if order_screen_img == "1":
        browser.get_screenshot_as_file('C:/project/log_order/결제전_'+str(orderno)+'.png')
        time.sleep(0.5)

    if gOrder_mode == "1":
        key_sel = "1"
    else:
        key_sel = input(">> 최종 버튼 선택 element 1 | 수동입력 2 : ")

######################
    #input(">> test input : ")

    if str(key_sel).strip() == "1":
        button_style = "0"
        try:
            buttonB = browser.find_element(By.XPATH,'//*[@id="checkout-button"]')
            if buttonB:
                button_style = "1"
        except Exception as e:
            button_style = "0"

        time.sleep(0.5)
        if button_style == "0":
            try:
                buttonB = browser.find_element(By.CSS_SELECTOR,'div.pl-order-toal-container__btn-box > button')
                if buttonB:
                    button_style = "2"
            except Exception as e:
                button_style = "0"

        time.sleep(0.5)
        if button_style == "0":
            print(">> E06 : 주문 버튼 클릭 불가 (button Element 확인불가) ")
            browser.get_screenshot_as_file('C:/project/log/E06_check_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))
            proc_LogSet(orderno, goodscode, "E06", "주문 버튼 클릭 불가")
            return "E06"

        try:
            if buttonB:
                buttonB.click()
                print(">> 주문 버튼 클릭 (최종클릭) 완료 ")
            else:
                print(">> (최종클릭) 주문 버튼 클릭 불가 ")
                browser.get_screenshot_as_file('C:/project/log/E06_check2_'+str(orderno)+'.png')
                time.sleep(random.uniform(1, 1.5))
                proc_LogSet(orderno, goodscode, "E06", "주문 버튼 클릭 불가")
                return "E06"
        except Exception as e:
            print(">> (최종클릭) 주문 버튼 클릭 불가 ")

            if str(browser.page_source).find('unsuccessful') > -1 or str(browser.page_source).find('주문 실패') > -1:
                print(">> Order Unsuccessful ")
                browser.get_screenshot_as_file('C:/project/log/E16_S088_check_'+str(orderno)+'.png')
                time.sleep(random.uniform(1, 1.5))
                proc_LogSet(orderno, goodscode, "S088", "결제 실패 (결제불가)")
                return "S088"

            browser.get_screenshot_as_file('C:/project/log/E06_check7_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))
            proc_LogSet(orderno, goodscode, "E06", "주문 버튼 클릭 불가")
            return "E06"

    else:
        input(">> 최종 버튼 선택 수동 입력후 아무키나 눌러주세요 : ")

    slide_flg = "0"
    try:
        if browser.find_element(By.CSS_SELECTOR,'body > div.baxia-dialog.auto > div.baxia-dialog-content'):
            print(">> [ Slide] we have detected ... ")
            slide_flg = "1"
    except Exception as e:
        print(">> No Slide Exception ")
    else:
        print(">> No Slide ")

    if slide_flg == "1":
        print(">> [ Slide ] 해제해 주세요 ")
        #my_send_kakao_proc("[Slide] 해제요청 : "+str(datetime.datetime.now()), notice_phone) # 담당자에게 알림톡 전송
        sms_send_kakao_proc_new("", "", "[Slide] 해제요청 (서버"+str(procIP)+"): " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
        print(">> 담장자에게 알림톡 발송 : {}".format(notice_phone))
        proc_LogState(">> [Slide] 해제요청 (서버"+str(procIP)+"): " + str(datetime.datetime.now())[:19])
        input(">> 슬라이드 해제후 아무키나 입력해 주세요 : ")
        time.sleep(random.uniform(1, 1.5))
        proc_LogState(">> [Slide] 해제완료 (서버"+str(procIP)+")(Input OK) : " + str(datetime.datetime.now())[:19])

    time.sleep(3)
    if str(browser.current_url).find('pay-result.htm') > -1 or str(browser.current_url).find('payResult.htm') > -1:
        pass
    else:
        print(">> current_url (1) : {} ".format(str(browser.current_url)[:50]))
        print(">> url check ...")
        time.sleep(random.uniform(4, 4.5))
        tmp_modal = func_ali.getparse(str(browser.page_source),'comet-zoom-appear-done comet-zoom-enter-done','<div class="comet-modal-body">')
        #print(">> tmp_modal : {} ".format(tmp_modal))
        if str(browser.page_source).find('unsuccessful') > -1 or str(browser.page_source).find('주문 실패') > -1:
            print(">> Order Unsuccessful (2)")
            browser.get_screenshot_as_file('C:/project/log/E16_S088_check2_'+str(orderno)+'.png')
            time.sleep(1)
            proc_LogSet(orderno, goodscode, "S088", "결제 실패 (결제불가)")
            return "S088"

    if str(browser.current_url).find('pay-result.htm') > -1 or str(browser.current_url).find('payResult.htm') > -1:
        pay_result = browser.page_source
        if debug_mode == "1":
            with open("C:/project/log/pay_result_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
                f.write(str(pay_result))
            time.sleep(0.5)

        if str(pay_result).find('결제 완료') > -1 or str(pay_result).find('내 주문 확인') > -1:
            pass
        else:
            time.sleep(random.uniform(3, 4))
        pay_result = browser.page_source
        if str(pay_result).find('결제 완료') > -1 or str(pay_result).find('내 주문 확인') > -1:
            pass
        else:
            time.sleep(random.uniform(5, 6))
        pay_result = browser.page_source
        if str(pay_result).find('결제 완료') > -1 or str(pay_result).find('내 주문 확인') > -1:
            pass
        else:
            time.sleep(20)
        pay_result = browser.page_source
        if str(pay_result).find('결제 완료') > -1 or str(pay_result).find('내 주문 확인') > -1:
            print(">> 결제 완료 확인 ")
            if str(pay_result).find('결제 완료') > -1 and str(pay_result).find(orderno) > -1:
                print(">> 결제 완료 OK : {}".format(orderno))
                adminMemoSet(orderno, "결제 완료")
            elif str(pay_result).find('내 주문 확인') > -1:
                print(">> 내 주문 확인 OK ")
                adminMemoSet(orderno, "결제 완료(2)")
            else:
                print(">> 결제완료 확인불가 (1) : {}".format(orderno))
                browser.get_screenshot_as_file('C:/project/log/E16_check1_'+str(orderno)+'.png')
                time.sleep(1)
                if debug_mode == "1":
                    input(">> Key Press (결제 확인불가 0) : ")
                else:
                    # proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가(1)")
                    # sms_send_kakao_proc_new("", "", "[확인요청] 결제완료 확인요청(1)(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                    # input(">> (1) 결제 확인 후 아무숫자키나 입력해 주세요 : ")
                    time.sleep(random.uniform(1, 1.5))
                    if str(browser.page_source).find(orderno) > -1:
                        print(">> (1) 결제 완료 (주문번호확인) OK : {}".format(orderno))
                        adminMemoSet(orderno, "결제 완료")
                    elif str(pay_result).find('내 주문 확인') > -1:
                        print(">> 내 주문 확인 OK ")
                        adminMemoSet(orderno, "결제 완료(2)")                        
                    else:
                        proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가(1-1)")
                        return "E16"

        elif str(pay_result).find('결제 실패') > -1:
            print(">> 결제 실패 확인 ")
            if dic_order['m_choice'] == "1":
                browser.get_screenshot_as_file('C:/project/log/S088_check_'+str(orderno)+'.png')
                time.sleep(1)
                proc_LogSet(orderno, goodscode, "S088", "초이스상품 결제 실패 (결제불가)")
                return "S088"
            else:
                browser.get_screenshot_as_file('C:/project/log/E16_S099_check3_'+str(orderno)+'.png')
                time.sleep(1)
                proc_LogSet(orderno, goodscode, "S099", "결제 실패 (결제불가)")
                return "S099"
        else:
            print(">> 결제완료 확인불가 (2) ")
            browser.get_screenshot_as_file('C:/project/log/E16_check2_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))

            if debug_mode == "1":
                input(">> Key Press (결제 확인불가 1) : ")
            else:
                proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가(2)")
                sms_send_kakao_proc_new("", "", "[확인요청] 결제완료 확인요청(2)(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                input(">> (2) 결제 확인 후 아무숫자키나 입력해 주세요 : ")

                time.sleep(random.uniform(1, 1.5))
                if str(browser.page_source).find('결제 완료') > -1 and str(browser.page_source).find(orderno) > -1:
                    print(">> (2) 결제 완료 (주문번호확인) OK : {}".format(orderno))
                    adminMemoSet(orderno, "결제 완료")
                elif str(browser.page_source).find('내 주문 확인') > -1:
                    print(">> (2) 결제 완료 (내 주문 확인) ")
                    adminMemoSet(orderno, "결제 완료(2)")
                else:
                    proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가(2-2)")
                    return "E16"

    else:
        print(">> 결제 확인불가 ")
        if str(browser.page_source).find('unsuccessful') > -1 or str(browser.page_source).find('주문 실패') > -1:
            print(">> Order Unsuccessful (3) ")
            browser.get_screenshot_as_file('C:/project/log/E16_S088_check4_'+str(orderno)+'.png')
            time.sleep(random.uniform(1, 1.5))
            proc_LogSet(orderno, goodscode, "S088", "결제 실패 (결제불가)")
            return "S088"

        browser.get_screenshot_as_file('C:/project/log/E16_check3_'+str(orderno)+'.png')
        time.sleep(random.uniform(1, 1.5))
        if debug_mode == "1":
            input(">> Key Press (결제 확인불가 2) : ")
        else:
            proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가")
            return "E16"

    time.sleep(random.uniform(1, 1.5))
    try:
        buttonTest = browser.find_element(By.CSS_SELECTOR,'div.pl-order-toal-container__btn-box > button') # button.comet-btn.comet-btn-primary.comet-btn-large.comet-btn-block
        if buttonTest:
            print(">> buttonTest (1) OK ")
            print(">> buttonTest (1) : {}".format(buttonTest.text))
            buttonTest.click()
            print(">> buttonTest (1) click ")
            time.sleep(3)
            browser.get_screenshot_as_file('C:/project/log/buttonTest_'+str(orderno)+'.png')
    except Exception as e:
        print(">> buttonTest (1) Exception ")
        # browser.get_screenshot_as_file('C:/project/log/buttonTest_'+str(orderno)+'.png')
        # proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가")
        # return "E16"

    ###########################################################################
    #  주문내역 확인하기  
    #  해외주문번호 / 가격 / 상품정보 체크
    ###########################################################################
    time.sleep(random.uniform(2, 2.5))
    if str(browser.current_url).find('/order/index.htm') == -1:
        orderLiskUrl = 'https://www.aliexpress.com/p/order/index.html'
        print(">> {} ".format(orderLiskUrl))

        try:
            browser.get(orderLiskUrl)
            time.sleep(random.uniform(3, 3.5))
        except Exception as e:
            proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가(1)")
            browser.get_screenshot_as_file('C:/project/log/E15_check5_'+str(orderno)+'.png')

            time.sleep(random.uniform(1, 1.5))
            browser.get(orderLiskUrl)
            print(">> (주문내역 다시 접속) {} ".format(orderLiskUrl))
            time.sleep(4)
            if str(browser.current_url).find('/order/index.htm') == -1:
                sms_send_kakao_proc_new("", "", "[확인요청] E15 주문내역 페이지 확인필요(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                input(">> 주문내역을 확인한후 아무숫자키나 입력해 주세요. : ")
                time.sleep(random.uniform(2, 2.5))

    curr_source_orderlist = browser.page_source
    time.sleep(0.5)
    #result_ordlist = browser.page_source
    # with open("C:/project/log/result_orderlist_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
    #     f.write(str(result_ordlist))
    # if debug_mode == "1":
    #     input(">> Key Press (주문내역 화면) : ")

    if str(browser.current_url).find('/order/index.htm') == -1:
        print(">> current_url : {}".format(browser.current_url))
        print(">> time.sleep(3) wait ")
        time.sleep(3)

    if str(browser.current_url).find('/order/index.htm') == -1:
        print(">> current_url : {}".format(browser.current_url))
        print(">> time.sleep(3) wait ")
        time.sleep(7)

    if str(browser.current_url).find('/order/index.htm') == -1:
        print(">> current_url : {}".format(browser.current_url))
        browser.get_screenshot_as_file('C:/project/log/E15_check6_'+str(orderno)+'.png')
        time.sleep(1)
        proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가(2)")
        return "E15"
    if order_screen_img == "1":
        browser.get_screenshot_as_file('C:/project/log_order/주문완료_'+str(orderno)+'.png')
        time.sleep(0.5)

    if str(browser.page_source).find('class="order-item"') == -1:
        print(">> Order List View Check ")
        browser.get_screenshot_as_file('C:/project/log/E15_check2_a1_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가 (a1)")
        sms_send_kakao_proc_new("", "", "[확인요청] E15 주문내역 페이지 확인필요(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
        input(">> 주문내역을 확인한후 아무숫자키나 입력해 주세요. : ")
        time.sleep(2)

    if str(browser.page_source).find('class="order-item"') > -1:
        print(">> Order List 확인 OK ")
        new_order_no = ""
        sp_ord_list = str(browser.page_source).split('order-item-header-right-info')
        if len(sp_ord_list) > 0:
            ord_item = sp_ord_list[1]
            new_order_no = func_ali.getparse(str(ord_item),'detail.html?orderId=','"').strip() # 생성된 새로운 주문번호 
            new_alino = func_ali.getparse(str(ord_item),'aliexpress.com/item/','.html"').strip()
            print(">> 주문번호: {} | NEW해외주문번호 : {} | 상품코드 : {}".format(orderno, new_order_no, new_alino))

            #sql_o = "select goodscode from t_order_info where sitecate = 'mini' and ali_orderno = '{}'".format(new_order_no)
            sql_o = "select goodscode from t_order_info where ali_orderno = '{}'".format(new_order_no)
            row = db_FS.selectone(sql_o)
            if row:
                print(">> 해외주문번호가 이미 존재 확인필요 : {}".format(new_order_no))
                proc_LogSet(orderno, goodscode, "E17", "해외주문번호가 이미 존재 확인필요")
                return "E17"

            if str(new_alino).strip() == aliCode:
                pass
                #print(">> new_alino : {} | aliCode : {}".format(new_alino, aliCode))
            else:
                order_link = "https://www.aliexpress.com/p/order/detail.html?orderId="+str(new_order_no)
                browser.get(order_link)
                time.sleep(random.uniform(3, 4))
                result_detail_ordlist = browser.page_source
                if debug_mode == "1":
                    with open("C:/project/log/result_detail_ordlist_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
                        f.write(str(result_detail_ordlist))
                    time.sleep(0.5)

                if str(result_detail_ordlist).find(new_alino) > -1:
                    print(">> 주문내역 일치하는 상품코드 확인 OK")
                if str(result_detail_ordlist).find(m_RcvMobile) > -1:
                    print(">> 주문내역 일치하는 전화번호 확인 OK") 
                else:
                    print(">> 주문내역 일치하는 연락처 확인불가 (주문내역 확인필요) ")
                    browser.get_screenshot_as_file('C:/project/log/E02_check_'+str(orderno)+'.png')
                    proc_LogSet(orderno, goodscode, "E02", "주문내역 일치하는 연락처 확인불가 (주문내역 확인필요)")
                    return "E02"

            if new_order_no == "":
                print(">> 해외주문번호 확인불가 (주문내역 확인필요)")
                browser.get_screenshot_as_file('C:/project/log/E10_check_'+str(orderno)+'.png')
                proc_LogSet(orderno, goodscode, "E10", "해외주문번호 확인불가 (주문내역 확인필요)")
                return "E10"

            if debug_mode == "1":
                input(">> Key Press (해외주문번호 입력전) :")

            ## 주문통계갱신 | 해외주문번호 입력 | 카톡 발송 
            rtnFlg = aliOrdernoSet(orderno, Ouid, Iuid, new_order_no, ali_total_cost, ali_id, goodscode)
            if rtnFlg == "0":
                proc_LogDetailSet(orderno, goodscode, '0', '주문완료 : ' + str(new_order_no), m_SettlePrice, ali_total_cost, ali_won_cost, sell_marzin, dev_detail, new_order_no, dic_order)
                print(">> 주문 [정상] 완료 : {}".format(orderno))
            else:
                return rtnFlg

################################################################################################################
    else:
        print(">> Order List View Error ")
        browser.get_screenshot_as_file('C:/project/log/E15_check2_a_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가 (a)")
        return "E15"

    return "0"

def adminMemoSet(inOrderno, inMemo):
    print(">> adminMemoSet : {}".format(inMemo))
    memoTime = str(datetime.datetime.now())
    wDate = memoTime[5:-16]
    wDate = wDate.replace("-", "/")
    print(wDate)

    if inOrderno != "" and inMemo != "":
        strAdminMemo = " " + wDate + " [자동주문] " + inMemo + " [adminauto] "
        sql = " select isnull(AdminMemo,''), AdminMemoUpdateID, AdminMemoUpdateDate from T_ORDER where OrderNo = '" + inOrderno + "'"
        row_a = db_FS.selectone(sql)
        if row_a:
            rAdminMemo = row_a[0]
            #print('>> DB rAdminMemo: ' + str(rAdminMemo))
        if rAdminMemo != "":
            strAdminMemo = str(rAdminMemo).strip() + " " + strAdminMemo

        strAdminMemo = strAdminMemo.replace("'", "")
        #print('>> strAdminMemo: ' + str(strAdminMemo))
        sql_upd = "UPDATE T_ORDER SET AdminMemo = '" + strAdminMemo + "', AdminMemoUpdateID = '" + gAdmin_Id + "', AdminMemoUpdateDate = getdate() where OrderNo = '" + inOrderno + "'"
        #print('>> sql_upd : ' + str(sql_upd))
        #print('>> AdminMemo UPDATE : ' + str(strAdminMemo))
        if gOrder_mode == "1":
            db_FS.execute(sql_upd)
            print('>> AdminMemo UPDATE 완료')
        return "0"
    else:
        print('>> 입력값을 확인해 주세요. inMemo: ' + str(inMemo))
        return "1"

def setMSG(num, name, str):
    strMSG = ""

    if num == "1":
        sql = " select content1, content2, content3 from T_KAKAOALIM_CONTENT where uid ='13' "
        row2 = db_FS.selectone(sql)
        content1 = row2[0]
        content2 = row2[1]
        content3 = row2[2]
        strMSG = content1 + name + content2 + str + content3

    if num == "2":
        sql = " select content1, content2, content3 from T_KAKAOALIM_CONTENT where uid ='15' "
        row2 = db_FS.selectone(sql)
        content1 = row2[0]
        strMSG = content1

    return strMSG

def my_send_kakao_proc(msg, phone):
    #print('>> [--- my 카카오톡 전송 start ---] ' + str(datetime.datetime.now()))

    MSG = msg
    FAILED_MSG = msg[:13]
    #print(MSG)
    #print(FAILED_MSG)

    ordname = "주문팀"
    #PHONE = "01090467616"
    PHONE = str(phone).replace('-','').strip()
    CALLBACK = "18005086"
    TEMPLATE_CODE = "norder1"
    FAILED_TYPE = "SMS"
    FAILED_SUBJECT = "sendmsg"

    url = "http://api.apistore.co.kr/kko/1/msg/1stplatform"
    params = {'PHONE': PHONE, 'CALLBACK': CALLBACK, 'MSG': MSG, 'TEMPLATE_CODE': TEMPLATE_CODE,'FAILED_TYPE': FAILED_TYPE, 'FAILED_MSG': FAILED_MSG, 'FAILED_SUBJECT': FAILED_SUBJECT}
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','x-waple-authorization': 'ODE3NC0xNTI0NDU5NzIwNDU3LTNmZTU0YWM0LTA0ZTItNGQ3My1hNTRhLWM0MDRlMjJkNzMyNw=='}

    resultStr = ""
    webpage = requests.post(url, data=params, headers=headers)
    soupNm = BeautifulSoup(webpage.content, "html.parser")
    resultStr = soupNm.text
    #print('>> resultStr : ' + str(resultStr))

    result_code = func_ali.getparse(resultStr, '"result_code":"', '"')
    result_message = func_ali.getparse(resultStr, '"result_message":"', '"')
    cmid = func_ali.getparse(resultStr, '"cmid":"', '"')
    ori_MSG = MSG.replace("'", "")

    sql_ins = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent) values ('" + ordname + "','" + PHONE + "','" + cmid + "','" + result_code + "','" + result_message + "',getdate(),'" + gAdmin_Id + "','auto','" + ori_MSG + "')"
    #print('>> sql_ins : ' + str(sql_ins))
    db_FS.execute(sql_ins)
    print(">> 카톡전송 (T_KAKAOALIM_LOG) : {}".format(PHONE))

    #print('>> [--- my 카카오톡 전송 end ---] ' + str(datetime.datetime.now()))
    return "0"

def sms_send_kakao_proc(inOrderno, inOrderinfouid):
    #print('>> [--- 카카오톡 전송 start ---] ' + str(datetime.datetime.now()))

    sql_sel = "select dbo.GetCutStr(GoodsTitle,80,'...') as GTitle,OrdName,OrdMobile from t_order as o inner join T_ORDER_INFO as i on o.uid = i.OrderUid where i.uid = '" + str(inOrderinfouid) + "'"
    #print('>> sql_sel:' + str(sql_sel))
    row = db_FS.selectone(sql_sel)

    if not row:
        print('>> 해당 데이터가 없습니다. inOrderno: ' + str(inOrderno))
        return "1"
    else:
        goodstitle = row[0]
        ordname = row[1]
        ordmobile = row[2]

        MSG = setMSG("1", ordname, goodstitle)
        FAILED_MSG = setMSG("2", "", "")
        #print(MSG)
        #print(FAILED_MSG)

        PHONE = ordmobile.replace("-", "")
######## test ############################################
        ## PHONE = "01090467616"
##########################################################
        CALLBACK = "18005086"
        TEMPLATE_CODE = "norder1"
        FAILED_TYPE = "SMS"
        FAILED_SUBJECT = "sendmsg"

        url = "http://api.apistore.co.kr/kko/1/msg/1stplatform"
        params = {'PHONE': PHONE, 'CALLBACK': CALLBACK, 'MSG': MSG, 'TEMPLATE_CODE': TEMPLATE_CODE,'FAILED_TYPE': FAILED_TYPE, 'FAILED_MSG': FAILED_MSG, 'FAILED_SUBJECT': FAILED_SUBJECT}
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','x-waple-authorization': 'ODE3NC0xNTI0NDU5NzIwNDU3LTNmZTU0YWM0LTA0ZTItNGQ3My1hNTRhLWM0MDRlMjJkNzMyNw=='}

        resultStr = ""
        webpage = requests.post(url, data=params, headers=headers)
        soupNm = BeautifulSoup(webpage.content, "html.parser")
        resultStr = soupNm.text
        #print('>> resultStr : ' + str(resultStr))

        result_code = func_ali.getparse(resultStr, '"result_code":"', '"')
        result_message = func_ali.getparse(resultStr, '"result_message":"', '"')
        cmid = func_ali.getparse(resultStr, '"cmid":"', '"')
        ori_MSG = MSG.replace("'", "")

        sql_ins = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent) values ('" + ordname + "','" + PHONE + "','" + cmid + "','" + result_code + "','" + result_message + "',getdate(),'" + gAdmin_Id + "','auto','" + ori_MSG + "')"
        #print('>> sql_ins : ' + str(sql_ins))
        db_FS.execute(sql_ins)
        print(">> 카톡전송 OK (T_KAKAOALIM_LOG) : {}".format(inOrderno))

        if result_code == "600":
            # 충전요금부족시 문자발송
            sql_e = "Insert into sms_msg (phone, callback, status, reqdate, msg ) values('01083160955', '1800-5086', '0', getdate(), '카카오알림톡 충전금 부족' )"
            #print('>> sql_e : ' + str(sql_e))
            print(">> 충전요금부족시 문자발송 01083160955 : {}".format(inOrderno))
            db2 = DBmodule_FR.Database("Main_allinmarket")
            db2.execute(sql_e)
            db2.close()

        #print('>> [--- 카카오톡 전송 end ---] ' + str(datetime.datetime.now()))
        return "0"

def get_new_token_v1():
    auth_server_url = "https://web1.dktechinmsg.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(inOrderNo, inIuid, msg, phone):
    token = get_new_token_v1()
    test_api_url = "https://web1.dktechinmsg.com/v1/message/send"
    api_call_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    template_code = "norder1"
    sender_no = "18005086"
    cid_key = "cid_key"

    if phone != "":
        print(">> ")
        ordername = "주문팀"
        orderno = "M0000"
        phone_number = str(phone).replace('-','').strip()
        message = msg
        sms_message = message
        message_type = "SM"
        sms_type = "SM"
    else:
        sql = "select dbo.GetCutStr(GoodsTitle,80,'...') as GTitle,OrdName,OrdMobile,OrderNo,o.OrdTel from t_order as o inner join T_ORDER_INFO as i on o.uid = i.OrderUid where i.uid = '{}'".format(inIuid)
        row_data = db_FS.selectone(sql)
        title = row_data[0]
        ordername = row_data[1]
        phone_number = row_data[2]
        phone_number = str(phone_number).replace('-','').strip()
        orderno = row_data[3]
        OrdTel = row_data[4]
        if phone_number == "" or phone_number is None:
            phone_number = OrdTel.replace("-","").strip()
        message = "[FREESHIP]"+str(ordername)+" 고객님 주문하신 상품 "+str(title)+" 해외현지 주문 완료 되었습니다.\n최대한 빠르고 안전하게 배송해드리겠습니다. 감사합니다."
        sms_message = message
        message_type = "AT"
        sms_type = "LM"
    #---------------------------------------
    ###phone_number = "01090467616"
    #---------------------------------------
    param_date = {'client_id': 'C000000440','sender_key': '3f6d483342e2ab3cb58e061960c6488fa3e0ad17','message_type': message_type,'message': message
    ,'cid': cid_key,'phone_number': phone_number,'template_code': template_code,'sender_no': sender_no,'sms_message':sms_message, 'sms_type':sms_type,'title': '주문관련 안내'}

    jsonString = json.dumps(param_date, indent=4)
    api_call_response = requests.post(test_api_url, headers=api_call_headers, data=jsonString)
    if api_call_response.status_code !=200:
        print(">> error ")
    else:
        result = json.loads(api_call_response.text)
        rtn_uid =  result['uid']
        rtn_status_code =  result['kko_status_code']
        rtn_code = result['code']
        rtn_message = result['message']
        print(">> rtn_status_code : {} | rtn_message : {}".format(rtn_status_code, rtn_message))
        if rtn_code == "API_200" or rtn_status_code == "0000": 
            result_code = "200"
            result_message = "OK"
        else:
            result_code = rtn_code
            result_message = rtn_message

        iSql = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent, orderno) values\
            ('{}','{}','{}','{}','{}',getdate(),'adminauto','{}','{}','{}')".format(ordername,phone_number,rtn_uid,result_code,result_message,template_code,message,orderno)
        print(">> iSql : {} ".format(iSql))
        db_FS.execute(iSql)


def checkBlacklist(rcvMobile, RcvTel, rcvAddr, rcvAddrDetail):
    rtnCode = ""
    findTel = ""
    if rcvMobile is None or rcvMobile == "":
        if RcvTel is None or RcvTel == "":
            findTel = ""
        else:
            findTel = str(RcvTel)
    else:
        findTel = str(rcvMobile)
    findAddr = str(rcvAddr ) + " " + str(rcvAddrDetail)

    if findAddr.find("시흥대로 350") > -1 or findAddr.find("독산동 1054") > -1: # 한국제품안전관리원
        rtnCode = "[ 확인사항 : 한국제품안전관리원  주소 확인필요 ]"
    elif findAddr.find("빛가람로 767") > -1 or findAddr.find("빛가람동 273") > -1 or findAddr.find("장덕동길 107-27") > -1 or findAddr.find("장덕리 102") > -1: # 전파연구소
        rtnCode = "[ 확인사항 : 전파연구소 주소 확인필요 ]" 
    elif findAddr.find("한국제품안전관리") > -1 or findAddr.find("제품안전관리") > -1 or findAddr.find("제품 안전관리") > -1 or findAddr.find("제품 안전 관리") > -1: # 전파연구소
        rtnCode = "[ 확인사항 : 한국제품안전관리 주소 확인필요 ]"
    elif findAddr.find("전파연구") > -1 or findAddr.find("전파 연구") > -1 or findAddr.find("전파센터") > -1 or findAddr.find("전파 센터") > -1: # 전파연구소
        rtnCode = "[ 확인사항 : 전파연구소 주소 있음 확인필요 ]"
    elif findTel.find("01090713279") > -1 or findTel.find("01030325126") > -1 or findTel.find("01043367200") > -1 or findTel.find("01077074649") > -1 or findTel.find("01074868642") > -1 or findTel.find("01039153048") > -1 or findTel.find("01076707436") > -1 or findTel.find("01055615129") > -1: # 한국제품안전관리원
        rtnCode = "[ 확인사항 : 한국제품안전관리원 연락처 있음 확인필요 ]"
    elif findTel.find("01055955115") > -1 or findTel.find("01088046053") > -1: # 전파연구소
        rtnCode = "[ 확인사항 : 전파연구소 연락처 있음 확인필요 ]"

    return rtnCode

def checkBlacklist2(rcvMobile, RcvTel):
    memo = ""
    tmpTel = rcvMobile
    if not rcvMobile:
        tmpTel = RcvTel
    tmpTel = str(tmpTel).replace("-","").strip()

    sql = "select mobile_phone, order_name, memo from freeship_blacklist where mobile_phone = '{}'".format(tmpTel)
    row = db_FS.selectone(sql)
    if row:
        memo = row[2]
        print(">> BlackList Phone: {}".format(tmpTel))
        return "[ 확인사항 (BlackList) : " + str(memo) + " ] "

    return memo

def proc_order_check(dic_ORD, db_ali):
    rtn_msg = ""
    m_Ouid = dic_ORD['m_Ouid']
    m_rcvName = dic_ORD['m_rcvName']
    m_ea = dic_ORD['m_ea']
    m_OrderNo = dic_ORD['m_OrderNo']
    m_GoodsCode = dic_ORD['m_GoodsCode']
    m_RcvPost = dic_ORD['m_RcvPost']
    m_cancel_cate = dic_ORD['m_cancel_cate']
    m_cancel_reason = dic_ORD['m_cancel_reason']
    m_soc_no = dic_ORD['m_soc_no']
    m_AdminMemo = dic_ORD['m_AdminMemo']
    m_RcvMobile = dic_ORD['m_RcvMobile']
    m_RcvTel = dic_ORD['m_RcvTel']
    m_RcvAddr = dic_ORD['m_RcvAddr']
    m_RcvAddrDetail = dic_ORD['m_RcvAddrDetail']
    m_GoodsTitle = dic_ORD['m_GoodsTitle']
    auto_ea_max = dic_ORD['auto_ea_max']

    # 주소 연락처 확인 (제품안전관리/전파연구소 확인)
    rtn_msg = checkBlacklist(m_RcvMobile, m_RcvTel, m_RcvAddr, m_RcvAddrDetail)
    if rtn_msg != "":
        proc_LogSet(m_OrderNo, m_GoodsCode, "E15", rtn_msg)
        return "E25"

    # 블랙리스트 대상 확인
    rtn_msg = checkBlacklist2(m_RcvMobile, m_RcvTel)
    if rtn_msg != "":
        proc_LogSet(m_OrderNo, m_GoodsCode, "E15", rtn_msg)
        return "E25"

    if m_AdminMemo != "":
        memoTime = str(datetime.datetime.now())
        if m_AdminMemo[:1] == ".":
            print(">> 어드민메모 [자동주문] 있음 ")
        elif m_AdminMemo[:14].find("[자동주문]") > -1 and m_AdminMemo.find("결제 완료") > -1:
            rtn_msg = "주문내역 페이지 확인불가"
            proc_LogSet(m_OrderNo, m_GoodsCode, "E15", rtn_msg)
            return "E15"
        elif m_AdminMemo[:14].find("[자동주문]") > -1:
            print(">> 어드민메모 [자동주문] 있음 ")
        else:
            rtn_msg = "어드민메모 있음"
            proc_LogSet(m_OrderNo, m_GoodsCode, "S029", rtn_msg)
            return "S029"

    ## t_order_info 주문건수 1개 (묶음주문 체크) 이상인지 체크 ##
    sql_r = " select goodscode as orderInfoCnt from t_order_info where OrderUid ='" + str(m_Ouid) + "'"
    #print('>> sql_r:' + str(sql_r))
    ord_info_rows = db_FS.select(sql_r)
    if len(ord_info_rows) > 1:
        rtn_msg = "묶음 주문건"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S001", rtn_msg)
        return "S001"
    if len(m_rcvName) > 3:
        rtn_msg = "수령인 3자리이상"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S002", rtn_msg)
        return "S002"
    if func_ali.isEnglishOrKorean(m_rcvName) > 0:
        rtn_msg = "수령인 한글아님"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S003", rtn_msg)
        return "S003"
    if int(m_ea) > int(auto_ea_max):
        rtn_msg = "수량 " +str(auto_ea_max)+ "개 이상"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S004", rtn_msg)
        return "S004"
    if len(m_RcvPost) > 5:
        rtn_msg = "우편번호 5자리이상"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S005", rtn_msg)
        return "S005"
    if m_cancel_cate != "" or m_cancel_reason != "":
        rtn_msg = "취소사유 있음"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S006", rtn_msg)
        return "S006"
    if len(m_soc_no) != 13 or str(m_soc_no)[:1].upper() != "P":
        rtn_msg = "통관번호 불일치"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S007", rtn_msg)
        return "S007"
    # if func_ali.soc_check(m_soc_no, m_rcvName, m_RcvMobile) == "1":
    #     rtn_msg = "통관번호 불일치"
    #     proc_LogSet(m_OrderNo, m_GoodsCode, "S008", rtn_msg)
    #     return "S008"

    # 타이틀 체크
    forTitle_flag = func_ali.checkTitle_new(m_GoodsTitle, db_FS)
    if forTitle_flag == "0":
        print(">> 타이틀 체크 완료 : {}".format(m_GoodsTitle))
    else:
        rtn_msg = "타이틀 확인필요 : " + " ( " + forTitle_flag[2:] + " ) "
        proc_LogSet(m_OrderNo, m_GoodsCode, "S030", rtn_msg)
        return "S030"

    # 타이틀 체크
    forbidden_flag = func_ali.checkForbidden_new(m_GoodsTitle, db_ali)
    if forbidden_flag == "0":
        print(">> 타이틀 금지어 체크 완료 : {}".format(m_GoodsTitle))
    else:
        rtn_msg = "타이틀 금지어 확인필요 : " + " ( " + forbidden_flag[2:] + " ) "
        proc_LogSet(m_OrderNo, m_GoodsCode, "S030", rtn_msg)
        return "S030"

    return ""

def procStateUpdate(db_con, code, m_Iuid, m_Ouid, m_OrderNo):
    print(">> procStateUpdate 처리 : {} ".format(m_OrderNo))
    if code == "" or code == "0":
        pass
    else:
        print(">> t_order_info 테이블 auto_check_code (update) : {} ".format(code))
        sql_u = " update t_order_info set auto_check_code = '{}' where uid = '{}'".format(code, m_Iuid)
        #print(">> sql_u : {} ".format(sql_u))
        db_con.execute(sql_u)

        sql_u2 = " update t_order set coupang_auto = null where uid = '{}'".format(m_Ouid)
        #print(">> sql_u2 : {} ".format(sql_u2))
        db_FS.execute(sql_u2)


if __name__ == '__main__':

    now = datetime.datetime.now()
    print('>> [--- main Proc start ---] ' + str(now))
    time.sleep(1)

    err_cnt = 0
    err_cnt_s099 = 0
    err_cnt_E = 0
    proc_flg = "0"
    debug_mode = ""
    login_mode = ""
    ali_id = ""
    order_mode = ""
    auto_max_list = 0
    connect_mode = "chrome"
    # # 로그인 ID/PASS 입력
    if currIp == "222.104.189.18" or currIp == "222.104.189.242":
        input(">> ip 확인하세요 : {}".format(currIp))

    # login_mode : 1 -> input 키값 확인후 진행
    # debug_mode : 1 -> input 키값 확인후 진행
    # gOrder_mode : 1 -> 실제 주문 모드
    # connect_mode : chrome_mode 
    if currIp == "222.104.189.18":
        currIp = "222.104.189.208"

    procIP = currIp.split('.')[-1]
    proc_LogState(">>ali_proc Start (서버"+str(procIP)+")")

    sql = "select login_id, login_pw, debug_mode, login_mode, ali_id, order_mode, connect_mode, notice_phone \
        , delivery_cost, auto_price_from, auto_price_to, auto_ea_max, auto_max_list, set_err_cnt, site_list \
        from ali_order_auto_set where login_ip = '{}'".format(currIp)
    row = db_FS.selectone(sql)
    if row:
        loginId = row[0]
        loginPass = row[1]
        debug_mode = row[2]
        login_mode = row[3]
        ali_id = row[4]
        gOrder_mode = row[5]
        connect_mode = row[6]
        notice_phone = row[7]
        delivery_cost = row[8]
        auto_price_from = row[9]
        auto_price_to = row[10]
        auto_ea_max = row[11]
        auto_max_list = row[12]
        set_err_cnt = row[13]
        site_list = row[14]
        if str(loginId) == "":
            proc_LogState("로그인 아이디 확인불가 (서버"+str(procIP)+")")
            db_FS.close()
            os._exit(1)

    print(">> ID : {} | debug_mode : {} | login mode : {} | gOrder_mode : {} | connect_mode : {}".format(loginId, debug_mode, login_mode, gOrder_mode, connect_mode))
    print(">> site_list : {}".format(site_list))

    time.sleep(1)
    main_url = 'http://imp.allinmarket.co.kr'
    try:
        mainDriver = func_ali.connectDriverOld('https://best.aliexpress.com/',"")
        print(">> connectDriverOld OK ")
    except Exception as e:
        mainDriver = func_ali.connectDriverNew('https://best.aliexpress.com/',"")
        print(">> connectDriverNew set OK ")
    time.sleep(1)

    ## mainDriver.get('https://ko.aliexpress.com/')
    mainDriver.get('http://imp.allinmarket.co.kr/')
    mainDriver.set_window_size(1500, 1200)
    mainDriver.set_window_position(0, 0, windowHandle='current')
    time.sleep(2)

    print(">> currIp : {}".format(currIp))
    input(">> (언어 / USD 확인필수) 로그인 처리후 아무키나 눌러주세요 :")
    time.sleep(1)

    # if str(result).find('class="currency">USD') > -1:
    #     print(">> USD OK ")
    # else:
    #     time.sleep(1)
    #     try:
    #         func_ali.setShipTO(mainDriver,"USD")
    #     except Exception as e:
    #         print(">> USD 설정 Exception")
    #     time.sleep(0.5)

    # if str(result).find('class="language_txt">한국어') > -1:
    #     print(">> 한국어 OK ")
    # else:
    #     time.sleep(1)
    #     try:
    #         func_ali.setShipTO(mainDriver,"한국어")
    #     except Exception as e:
    #         print(">> USD 설정 Exception")
    #     time.sleep(0.5)

    result = mainDriver.page_source
    time.sleep(1)

    if str(mainDriver.current_url).find('gatewayAdapt=glo2kor') > -1 or str(mainDriver.current_url).find('ko.aliexpress.com') > -1:
        print(">> 한국 배송 ko.aliexpress ")

    if str(result).find('class="ship-to--menuItem') == -1:
        # input(">> 한국어 설정 및 USD 통화 설정 하고 숫자키를 입력해 주세요:")
        time.sleep(1)
    else:
        if func_ali.getparse(str(result),'<span class="ship-to--small','</div>').find('/KO/</span><b>USD') > -1:
            print(">> 한국 설정 / USD 설정 OK ")
        else:
            #input(">> 한국어 설정 및 USD 통화 설정 하고 숫자키를 입력해 주세요:")
            time.sleep(1)

    db_ali = DBmodule_FR.Database("aliexpress")
    proc_all_cnt = 0
    err_cnt = 0
    err_cnt_s099 = 0
    err_cnt_E = 0
    mainDriver.set_window_size(1500, 1200)
    if proc_flg == "0":
        stop_flg = "0"
        while stop_flg == "0":

            # 실행대상 가져오기 Sql 
            sql = getMakeSql("main","","","","",site_list)
            if debug_mode == "1":
                print(">> sql : {}".format(sql))
            mainRows = db_FS.select(sql)
            icnt = 0
            if not mainRows:
                print(">> 대상이 없습니다. (종료) ")
                proc_LogState(">>대상이 없습니다 (서버"+str(procIP)+")")
                stop_flg = "1"
                break
            else:
                for rs in mainRows:
                    # select top 10 t.Uid, i.Uid, OrderNo, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, i.ea, isnull(i.optionKind,''), isnull(o.Item,''), RcvPost, isnull(soc_no,''), rcvName, isnull(OrderMemo,''), isnull(cancel_cate,''), isnull(cancel_reason,''), RcvMobile, t.regdate, i.CateCode, isnull(AdminMemo,'')
                    m_Ouid = rs[0]
                    m_Iuid = rs[1]
                    m_OrderNo = rs[2]
                    m_GoodsCode = rs[3]
                    m_ali_code = rs[4]
                    m_site = rs[5]
                    m_ea = rs[6]
                    m_optionKind = rs[7]
                    if m_optionKind == "300":
                        m_Item = rs[8]
                    else:
                        m_Item = ""
                    m_RcvPost = rs[9]
                    m_soc_no = rs[10]
                    m_rcvName = rs[11]
                    m_OrderMemo = rs[12]
                    m_cancel_cate = rs[13]
                    m_cancel_reason = rs[14]
                    m_RcvMobile = rs[15]
                    m_regdate = rs[16]
                    m_CateCode = rs[17]
                    m_AdminMemo = rs[18]
                    m_RcvTel = rs[19]
                    m_RcvAddr = rs[20]
                    m_RcvAddrDetail = rs[21]
                    m_GoodsTitle = rs[22]

                    m_rcvName = str(m_rcvName).replace(' ','').strip()
                    m_RcvPost = str(m_RcvPost).replace('-','').strip()
                    m_soc_no = str(m_soc_no).replace(' ','').strip()
                    m_RcvMobile = str(m_RcvMobile).replace('-','').strip()
                    m_RcvTel = str(m_RcvTel).replace('-','').strip()

                    # T_goods 에 해당 주문 ali_code, img 등 가져오기
                    db_con = DBmodule_FR.Database(m_site)
                    sql_code = " select g.ali_no, imgB, cate_idx, datefolder, isnull(o.Title,''), o.Items from t_goods as g left join t_goods_option as o on o.GoodsUid = g.uid where GoodsCode = '" + m_GoodsCode + "' "
                    #print('>> sql :' + str(sql_code))
                    fs_url = ""
                    row_code = db_con.selectone(sql_code)
                    if row_code:
                        m_ali_code = row_code[0]
                        m_imgB = row_code[1]       
                        m_cate_idx = row_code[2]   
                        m_datefolder = row_code[3]
                        m_option_title = row_code[4].strip()
                        m_option_items = row_code[5]
                        m_ali_code = str(m_ali_code).replace("_del","").strip()
                        m_datefolder = m_datefolder.replace("\\","/")
                        fs_url =  "https://" +str(m_site)+ ".freeship.co.kr/goodsimg/" + str(m_cate_idx) + str(m_datefolder) + "/big/" + str(m_imgB)
                        #print("fs_url : " + str(fs_url))

                    if m_ali_code == "":
                        rtn_msg = ">> ali 상품코드 확인불가 (SKIP) : {}".format(m_ali_code)
                        proc_LogSet(m_OrderNo, m_GoodsCode, "S009", rtn_msg)
                        continue
                    if fs_url == "":
                        rtn_msg = ">> ali 상품이미지 확인불가 (SKIP) : {}".format(fs_url)
                        proc_LogSet(m_OrderNo, m_GoodsCode, "S010", rtn_msg)
                        continue

                    proc_all_cnt = proc_all_cnt + 1
                    dic_order = dict()
                    ########### price / gallery / review ###########
                    dic_order['m_Ouid'] = str(m_Ouid)
                    dic_order['m_Iuid'] = str(m_Iuid)
                    dic_order['m_OrderNo'] = str(m_OrderNo)
                    dic_order['m_GoodsCode'] = str(m_GoodsCode)
                    dic_order['m_ali_code'] = str(m_ali_code)
                    dic_order['m_site'] = str(m_site)
                    dic_order['m_ea'] = str(m_ea)
                    dic_order['m_optionKind'] = str(m_optionKind)
                    dic_order['m_Item'] = str(m_Item)
                    dic_order['m_RcvPost'] = str(m_RcvPost)
                    dic_order['m_soc_no'] = str(m_soc_no)
                    dic_order['m_rcvName'] = str(m_rcvName)
                    dic_order['m_OrderMemo'] = str(m_OrderMemo)
                    dic_order['m_cancel_cate'] = str(m_cancel_cate)
                    dic_order['m_cancel_reason'] = str(m_cancel_reason)
                    dic_order['m_RcvMobile'] = str(m_RcvMobile)
                    dic_order['m_regdate'] = str(m_regdate)
                    dic_order['m_imgB'] = str(m_imgB)
                    dic_order['m_datefolder'] = str(m_datefolder) 
                    dic_order['m_CateCode'] = str(m_CateCode)
                    dic_order['fs_url'] = str(fs_url) 
                    dic_order['debug_mode'] = debug_mode
                    dic_order['notice_phone'] = notice_phone
                    dic_order['ali_id'] = ali_id
                    dic_order['m_option_title'] = m_option_title
                    dic_order['m_AdminMemo'] = str(m_AdminMemo)
                    dic_order['m_RcvTel'] = str(m_RcvTel)
                    dic_order['m_RcvAddr'] = str(m_RcvAddr)
                    dic_order['m_RcvAddrDetail'] = str(m_RcvAddrDetail)
                    dic_order['m_GoodsTitle'] = m_GoodsTitle
                    dic_order['auto_ea_max'] = str(auto_ea_max)
                    dic_order['m_option_items'] = str(m_option_items)
                    dic_order['m_ip'] = str(procIP)

                    time.sleep(1)
                    print("\n\n")
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print(">> 주문번호 : {} | alicode : {} | goodscode : {} | site : {} | ea : {} , option : {}, m_regdate : {}".format(m_OrderNo,m_ali_code,m_GoodsCode,m_site,m_ea,m_Item,m_regdate))
                    print(">> Site : {}".format(m_site))
                    # 주문가능한지 체크 (주문메모, 통관번호, 금지어, 블랙리스트 대상인지 확인)
                    order_rtn = proc_order_check(dic_order, db_ali)
                    if order_rtn != "":
                        print(">> 주문 불가 (SKIP) : {} ".format(m_OrderNo))
                        procStateUpdate(db_FS, order_rtn, m_Iuid, m_Ouid, m_OrderNo)
                    else:

                        if m_ali_code == "":
                            print(">> ali_code 없음 (Skip) : {}".format(m_OrderNo))
                        else:
                            # 주문 main 실행
                            rtn_main = proc_order(mainDriver, dic_order)
                            print(">> 결과 CODE : {}".format(rtn_main))

                            if rtn_main == "0": # 주문정상
                                err_cnt = 0
                                err_cnt_s099 = 0
                                err_cnt_E = 0
                            elif rtn_main[:1] == "S" or rtn_main[:1] == "D" or rtn_main[:1] == "X": # 주문 품절 및 스킵주문
                                if rtn_main == "S077":
                                    print(">> 소스 옵션 확인 불가상태 (S077) SKIP ")
                                else:
                                    err_cnt = err_cnt + 1
                                procStateUpdate(db_FS, rtn_main, m_Iuid, m_Ouid, m_OrderNo)
                                if rtn_main[:4] == "S099":
                                    err_cnt_s099 = err_cnt_s099 + 1
                                    print(">> err_cnt_s099 : {}".format(err_cnt_s099))
                            else: # 주문 에러
                                err_cnt = err_cnt + 1
                                err_cnt_E = err_cnt_E + 1
                            print(">> err_cnt : {} ".format(err_cnt))
                            if rtn_main[:1] == "E":
                                # 주문 담당자에게 알림톡발송 (에러)
                                sms_send_kakao_proc_new("", "", "[" +str(rtn_main)+ "](서버"+str(procIP)+") 에러코드발생 확인필요(종료) : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                                proc_LogState(">> E 코드 발생 (서버"+str(procIP)+") {} | {} ".format(rtn_main, m_OrderNo))
                                stop_flg = "1"
                                err_cnt_E = err_cnt_E + 1
                                break
                            #if err_cnt > 13:
                                # 주문 담당자에게 알림톡발송
                                # sms_send_kakao_proc_new("", "", " (skip) 13개 이상(진행중)(서버"+str(procIP)+"): " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                                # 개발 담당자에게 알림톡발송
                                #sms_send_kakao_proc_new("", "", " (skip) 13개 이상(진행중)(서버"+str(procIP)+"): " + str(datetime.datetime.now())[:19], "01090467616") # 알림톡 전송

                            if err_cnt > int(set_err_cnt):
                                # 주문 담당자에게 알림톡발송
                                sms_send_kakao_proc_new("", "", " (skip) "+str(set_err_cnt)+"개 이상 확인필요(종료)(서버"+str(procIP)+"): " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                                proc_LogState(">> err_cnt (skip) {}개 이상 (서버"+str(procIP)+"): {}".format(set_err_cnt, rtn_main)) # 에러 및 스킵대상이 연속 10개이상일 경우 STOP
                                stop_flg = "1"
                                break
                            if err_cnt_s099 > 2: # err_cnt_s099 2개 이상 결제실패의 경우 STOP
                                # 주문 담당자에게 알림톡발송
                                sms_send_kakao_proc_new("", "", " 2개 이상 결제실패 확인필요(종료)(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                                proc_LogState(">> err_cnt_s099 2개 이상 결제실패 확인필요 (서버"+str(procIP)+"): {}".format(rtn_main))
                                stop_flg = "1"
                                break
                            if err_cnt_E > 2: # err_cnt_E 2개 이상 경우 STOP
                                # 주문 담당자에게 알림톡발송
                                sms_send_kakao_proc_new("", "", " 2개 이상 결제실패 확인필요(종료)(서버"+str(procIP)+") : " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                                proc_LogState(">> err_cnt_E 2개 이상 결제실패 확인필요 (서버"+str(procIP)+"): {}".format(rtn_main))
                                stop_flg = "1"
                                break

                    if proc_all_cnt > auto_max_list: # 주문설정 에서 설정한 max값 이상일경우 STOP
                        # 주문 담당자에게 알림톡발송
                        sms_send_kakao_proc_new("", "", "[1회 최대: " +str(proc_all_cnt)+ "건](서버"+str(procIP)+") 수행 완료 (종료): " + str(datetime.datetime.now())[:19], notice_phone) # 담당자에게 알림톡 전송
                        print(">> auto_max_list 수행 완료 (종료) : {}".format(proc_all_cnt))
                        stop_flg = "1"
                        break

    proc_LogState(">> ali_proc End (서버"+str(procIP)+")")

    if debug_mode == "1":
        input(">> Key Press (End): ")

    db_FS.close()
    db_ali.close()
    now = datetime.datetime.now()
    print('>> [--- main Proc End ---] ' + str(now))
    mainDriver.quit()
    os._exit(0)