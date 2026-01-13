import socket
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
import func_ali
import sys
p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR
import DBmodule_FR

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
    ####db_FS.execute(sql)

    return "0"

def proc_LogSet(m_OrderNo, goodscode, code, msg):
    print(">> code : {} | msg : {}".format(code, msg))

    if msg == "":
        msg = func_ali.get_codeMsg(code)

    sql = "select orderNo from auto_order_ali_new where orderno = '{}'".format(m_OrderNo)
    row = db_FS.selectone(sql)
    if row:
        sql_u = " update auto_order_ali_new set code = '{}', msg = '{}', goodscode = '{}' where orderno = '{}'".format(code, msg, goodscode, m_OrderNo)
    else:
        sql_u = " insert into auto_order_ali_new ( orderno, code, msg, goodscode ) values ( '{}', '{}', '{}', '{}') ".format(m_OrderNo, code, msg, goodscode)

    #print(">> sql_u : {} ".format(sql_u))
    #####db_FS.execute(sql_u)

    # 어드민 메모 작성 ##
    ##################################################
    ####adminMemoSet(m_OrderNo, msg)

    return "0"


def proc_LogDetailSet(m_OrderNo, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no):
    print(">> code : {} | msg : {}".format(code, msg))

    sql = "select orderNo from auto_order_ali_new where orderno = '{}'".format(m_OrderNo)
    row = db_FS.selectone(sql)
    if row:
        sql_u = " update auto_order_ali_new set goodscode = '{}', code = '{}', msg = '{}', sell_price = '{}', ali_price = '{}', org_price = '{}', marzin = '{}', dev_detail = '{}', ali_order_no = '{}' where orderno = '{}'".format(goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no, m_OrderNo)
    else:
        sql_u = " insert into auto_order_ali_new ( orderno, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no ) values ( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' , '{}', '{}') ".format(m_OrderNo, goodscode, code, msg, sell_price, ali_price, org_price, marzin, dev_detail, ali_order_no)

    #print(">> sql_u : {} ".format(sql_u))
    ####db_FS.execute(sql_u)

    # 어드민 메모 작성 ##
    ###adminMemoSet(m_OrderNo, msg)

    return "0"

def getMakeSql_test(in_sel_flg, searchUid, searchInfoUid, in_ip, in_orderno):
    ex_now = datetime.datetime.now()
    ex_eDate = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M" + ":00")
    print('>> eDate: ' + str(ex_eDate)) #30분전 시간

    sql = ""
    if in_sel_flg == "main_all":
        sql = " select count(*) "
    elif in_sel_flg == "main":
        sql = " select top 1 t.Uid, i.Uid, OrderNo, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, i.ea, isnull(i.optionKind,''), isnull(o.Item,''), RcvPost, isnull(soc_no,''), rcvName, isnull(OrderMemo,''), isnull(cancel_cate,''), isnull(cancel_reason,''), RcvMobile, t.regdate, i.CateCode, isnull(AdminMemo,'') "
    elif in_sel_flg == "addr":
        sql = " select t.Uid, i.Uid, OrderNo, SettlePrice, RcvPost, rcvName, replace(soc_no,'p','P'), RcvMobile, RcvAddr, isnull(RcvAddrDetail,''), isnull(cancel_cate,''), isnull(cancel_reason,''), t.coupang_auto, isnull(t.naver_pay_order_id,''), t.naver_pay_unitprice, i.sitecate "
    else:
        sql = " select top 5 t.Uid, OrderNo, SettlePrice, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, RcvPost, isnull(soc_no,''), rcvName, i.sitecate, isnull(OrderMemo,''), "
        sql = sql + " i.ea, isnull(cancel_cate,''), isnull(cancel_reason,''), isnull(i.amazon_price,''), isnull(i.ali_orderno,''), isnull(i.optionKind,''), isnull(AdminMemo,''), isnull(auto_flg,''), RcvMobile  "
    sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.Uid left join t_order_option as o on o.OrderInfoUid = i.Uid "
    sql = sql + " where t.orderno = '" + str(in_orderno) + "' " ##  주문테스트
    if searchUid != "":
        sql = sql + " and t.Uid = '" +str(searchUid)+ "'"
    if searchInfoUid != "":
        sql = sql + " and i.Uid = '" +str(searchInfoUid)+ "'"


    return str(sql)

def getMakeSql(in_sel_flg, searchUid, searchInfoUid, in_ip):

    ex_eDate = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M" + ":00")
    print('>> eDate: ' + str(ex_eDate)) #30분전 시간

    sql = ""
    if in_sel_flg == "main_all":
        sql = " select count(*) "
    elif in_sel_flg == "main":
        sql = " select top 10 t.Uid, i.Uid, OrderNo, i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, i.ea, isnull(i.optionKind,''), isnull(o.Item,''), RcvPost, isnull(soc_no,''), rcvName, isnull(OrderMemo,''), isnull(cancel_cate,''), isnull(cancel_reason,''), RcvMobile, t.regdate, i.CateCode, isnull(AdminMemo,'') "
    elif in_sel_flg == "addr":
        sql = " select t.Uid, i.Uid, OrderNo, SettlePrice , RcvPost, rcvName, replace(soc_no,'p','P'), RcvMobile, RcvAddr, isnull(RcvAddrDetail,'') "
    else:
        sql = " select top 5 t.Uid, OrderNo, SettlePrice , i.GoodsCode, isnull(i.ali_seller,''), i.sitecate, RcvPost, isnull(soc_no,''), rcvName, i.sitecate, isnull(OrderMemo,''), "
        sql = sql + " i.ea, isnull(cancel_cate,''), isnull(cancel_reason,''), isnull(i.amazon_price,''), isnull(i.ali_orderno,''), isnull(i.optionKind,''), isnull(AdminMemo,''), isnull(auto_flg,''), RcvMobile  "
    sql = sql + " from t_order as t inner join t_order_info as i on i.OrderUid = t.Uid left join t_order_option as o on o.OrderInfoUid = i.Uid "
    sql = sql + " where t.state = '200' " ## 배송준비중
    if in_sel_flg != "addr":
        sql = sql + " and UserID <> 'kbw4798' "    # 본부장님 주문건 제외
        sql = sql + " and soc_no is not null "     # 통관번호 있는 주문건
        sql = sql + " and naver_pay_cancel_wait is null " # 네이버 페이 취소대기건 제외
        #sql = sql + " and cancel_cate is null and isnull(cancel_reason,'') = '' " # 취소 관련 메모 주문건 제외
        #sql = sql + " and i.ea < 4 "                # 수량이 4개 이하
        sql = sql + " and auto_check_code is null " # code 없는것
        sql = sql + " and i.sitecate = 'mini' "
#######################################################
        # sql = sql + " and t.regdate <= '" + str(ex_eDate) + "'"
        # sql = sql + " and t.orderno in ('M22160571712C6') " ##  주문테스트
        sql = sql + " and t.coupang_auto = '1' "
#######################################################
    if searchUid != "":
        sql = sql + " and t.Uid = '" +str(searchUid)+ "'"
    if searchInfoUid != "":
        sql = sql + " and i.Uid = '" +str(searchInfoUid)+ "'"
    if in_sel_flg  == "main_all" or in_sel_flg == "main":
        #sql = sql + " order by t.uid asc"
        sql = sql + " order by t.regdate asc "

    return str(sql)

def orderCntProc(inAliID, inUid):
    curDate = ""
    nowTime = str(datetime.datetime.now())
    curDate = nowTime[:10]
    #print(curDate)

    # curAliId = func_ali.getOrderIDCount(inAliID)
    # print('>> curAliId : ' + str(curAliId))

    # sql = " select idx from T_COUNT_ORDER where date = '" + curDate + "'"
    # #print('>> sql: ' + str(sql))
    # row_cp = db_FS.selectone(sql)
    # if not row_cp:
    #     sql_ins = "insert into T_COUNT_ORDER (date," + curAliId + ") values('" + curDate + "',1)"
    #     #print('>> sql_ins: ' + str(sql_ins))
    #     db_FS.execute(sql_ins)
    # else:
    #     ridx = row_cp[0]
    #     sql_upd = "update T_COUNT_ORDER set " + curAliId + " = " + curAliId + " + 1 where idx = '" + str(ridx) + "'"
    #     #print('>> sql_upd: ' + str(sql_upd))
    #     db_FS.execute(sql_upd)

    # #print('>> 주문 통계 UPDATE 완료')

    # # 해외 배송중 상태로 변경
    # sql_upd = "UPDATE T_ORDER SET State=201, BuyID ='" + gAdmin_Id + "', ChkDate=GETDATE() WHERE Uid='" + str(inUid) + "'"
    # #print('>> sql_upd: ' + str(sql_upd))
    # db_FS.execute(sql_upd)
    # #print('>> 해외 배송중 상태로 변경 완료')

    return "0"

# inOrderUid : (t_order : uid)
def aliOrdernoSet(inOrderNo, inOuid, inIuid, inAliOrderNo, inAliPrice, inAliID, ingoodscode):
    print(">> aliOrdernoSet")
    # sql = " select OrderNo,IsConfirm from t_order where Uid = '" + str(inOuid) + "'"
    # #print('>> sql: ' + str(sql))
    # row_t = db_FS.selectone(sql)
    # rOrderNo = row_t[0]
    # rIsConfirm = row_t[1]

    # if rIsConfirm == "F":
    #     print('>> 해외주문번호 입력 불가 (주문 상태를 확인 필요) {} | {} '.format(rIsConfirm, inOrderNo))
    #     proc_LogSet(inOrderNo, ingoodscode, "E08", "해외주문번호 입력 불가 (주문 상태를 확인 필요)")
    #     return "E08"

    # if inOuid != "" and inAliOrderNo != "" and inAliID != "":
    #     sql = " select Uid, isnull(ali_orderno,'') from T_ORDER_INFO where Uid = '" + str(inIuid) + "'"
    #     #print('>> sql: ' + str(sql))
    #     row_info = db_FS.selectone(sql)
    #     if row_info:
    #         rUid = row_info[0]
    #         rAli_orderno = row_info[1]
    #         rAli_orderno = str(rAli_orderno).strip()
    #         #print('>> DB rUid: ' + str(rUid))
    #         #print('>> DB rAli_orderno: ' + str(rAli_orderno))

    #         ####### 주문 입력 / 통계 카운트 / 주문상태변경 / 카톡발송 #######
    #         if rAli_orderno == "":
    #             ####### 해외주문번호 입력 #######
    #             sql_upd = "update t_order_info set ali_id = '" + str(inAliID) + "', ali_orderno = '" + str(inAliOrderNo) + "', amazon_price = '" + str(inAliPrice) + "',amazon_price_id = '" + str(gAdmin_Id) + "',amazon_price_date=getdate(), ali_ord_date = convert(varchar(50),getdate(),120) where Uid='" + str(inIuid) + "'"
    #             #print('>> sql_upd : ' + str(sql_upd))
    #             #print('>> 해외 주문번호 UPDATE 처리 : {}'.format(inAliOrderNo))
    #             db_FS.execute(sql_upd)
    #             print('>> 해외 주문번호 UPDATE 완료 : {}'.format(inAliOrderNo))
    
    #             ####### 통계 카운트 처리 및 해외배송중 상태로 변경 #######
    #             #print('>> 통계 카운트 처리 및 해외배송중 상태로 변경')
    #             orderCntProc(inAliID, inOuid)
    #             print('>> 통계 카운트 및 해외배송중 상태 변경완료')

    #             # 카카오톡 전송 (실패할 경우 sms 전송)
    #             #print('>> 카카오톡 전송')
    #             sms_send_kakao_proc(inOrderNo, inIuid)
    #             print('>> 카카오톡 전송 완료')

    #             sql_u2 = " update t_order set coupang_auto = null where uid = '{}'".format(inOuid)
    #             #print(">> sql_u2 : {} ".format(sql_u2))
    #             db_FS.execute(sql_u2)

    #             return "0"
    #     else:
    #         print('>> 해외 주문번호 UPDATE 불가 (현지주문번호가 이미 존재) ' + str(rAli_orderno))
    #         proc_LogSet(inOrderNo, ingoodscode, "E09", "해외 주문번호 UPDATE 불가 (현지주문번호가 이미 존재) ")
    #         return "E09"
    # else:
    #     print('>> 해외주문번호 입력 불가 ' + str(rIsConfirm))
    #     proc_LogSet(inOrderNo, ingoodscode, "E07", "해외주문번호 입력 불가 ")
    #     return "E07"
    return "0"

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

    # browser.get('https://ko.aliexpress.com/')
    # time.sleep(4)

    # # 알리 상품코드 입력
    # time.sleep(1)
    # print('>> time.sleep(1)')
    # wait = WebDriverWait(browser, 20)
    # browser.find_element(By.XPATH,'//*[@id="search-key"]').send_keys(aliCode)

    # # 상품코드 검색창 버튼 클릭
    # time.sleep(2)
    # print('>> time.sleep(2)')
    # wait = WebDriverWait(browser, 20)
    # #aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-in-aliexpress")))
    # aSearchBtn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-button")))
    # if aSearchBtn:
    #     aSearchBtn.click()
    # else:
    #     print(">> 상품코드 검색창 버튼 없음 확인필요. ")
    #     proc_LogSet(orderno, goodscode, "E12", "상품코드 검색창 버튼 없음")
    #     return "E12"

    ali_url = "https://ko.aliexpress.com/item/" +str(aliCode)+ ".html"
    print("ali_url : {}".format(ali_url))
    browser.get(ali_url)

    time.sleep(4)
    print('>> time.sleep(4)')

    #if debug_mode == "1":
    #    input(">> Key Press (상품코드 검색) : ")

    result = browser.page_source
    result_org = str(result)
    result_soup = BeautifulSoup(result, 'html.parser')
    
    path_file = os.getcwd()
    #with open(path_file + "/log/new_ali.html","w",encoding="utf8") as f: 
    #    f.write(str(result))
    #with open(path_file + "/log/new_ali_soup.html","w",encoding="utf8") as f: 
    #    f.write(str(result_soup))

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

        #input(">> type : 2 (check) ")

    #input(">> Input key : ")
    ######################### product-main-wrap
    ######################### pdp-wrap pdp-body
    #if str(result_org).find('class="titleBanner') > -1: 
    if str(result_org).find('class="product-title"') > -1:
        title = func_ali.getparse(str(result_org),'class="product-title"','</h1>').replace('<h1 class="product-title-text">','').replace('>','')
        #print(">> title Ok : {}".format(title))
    elif str(result_org).find('class="titleBanner--title') > -1:
        title = func_ali.getparse(str(result_org),'class="titleBanner--title','</h3>')
        if str(title).find('title="') > -1:
            title = func_ali.getparse(str(title),'title="','').replace("'","").replace('"','')
        proc_LogSet(orderno, goodscode, "X04", msg)
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
    #print(">> product_delivery : {} ".format(product_delivery))
    if str(product_delivery).find('Korea') > -1:
        pass
        #print(">> product_delivery : {}".format(product_delivery)) 
    else:
        print(">> No product_delivery ") 
        print(">> product_delivery : {} ".format(product_delivery))
    if str(result_org).find('배송지로 배송이 불가능') > -1:
        print(">> 배송 불가능 : {}".format(aliCode))
        proc_LogSet(orderno, goodscode, "S024", "배송 불가능")
        return "S024"

    if str(result_org).find('class="uniform-banner"') > -1:
        product_price = func_ali.getparse(result_org,'class="uniform-banner-box-price"','</span>')
    else:
        product_price = func_ali.getparse(result_org,'class="product-price-value"','</span>')

    if product_price == "" and ali_screen_type == 2:
        product_price = func_ali.getparse(result_org,'price-current">','</span>')
        print(">> product_price : {} ".format(product_price))

    if product_price == "" and ali_screen_type == 3:
        product_price = func_ali.getparse(result_org,'data-pl="product-price"','data-pl="product-title"')
        # print(">> product_price : {} ".format(product_price))

    if str(product_price).find('US') > -1:
        pass #print(">> price Ok : {}".format(product_price)) 
    else:
        print(">> No price ") 
        print(">> product_price : {} ".format(product_price))
    if ali_screen_type == 2:
        buy_now = func_ali.getparse(result_org,'class="action--container','')
        buy_now = func_ali.getparse(buy_now,'<button type','</button>')
    elif ali_screen_type == 3:
        buy_now = func_ali.getparse(result_org,'class="quantity--','')
        if buy_now.find('class="pdp-wrap"') > -1:
            buy_now = func_ali.getparse(buy_now,'','class="pdp-wrap"')
    else:
        buy_now = func_ali.getparse(result_org,'class="product-action"','</span>')

    if str(buy_now).find('즉시 구매') > -1 or str(buy_now).find('Buy Now') > -1 or str(buy_now).find('바로 구매') > -1:
        pass
        #print(">> 즉시 구매 버튼 있음")
    elif str(result_org).find('<button title="즉시 구매"') > -1:
        pass
    elif str(result_org).find('comet-btn-important"><span>바로 구매</span>') > -1:
        print(">> 바로 구매 (type 2) ")
        pass
    else:
        print(">> No 즉시 구매 버튼 확인불가 ")
        proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매 버튼 확인불가")
        return "D003"


    # 알리 상품 이미지 체크
    ### ali_url = func_ali.getparse(str(result_org),'"imagePath":"','"')
    ali_url = func_ali.getImgUrl(result_org, ali_screen_type)
    #print("ali_url : " + str(ali_url))
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
        proc_LogSet(orderno, goodscode, edit_option, msg)
        return edit_option
    else:
        print(">> (주문) edit_option : {}".format(edit_option))

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
                flg_search = "S01"  # SKIP
                print(">> 옵션코드 옵션명 갯수 불일치 SKIP 대상: {}".format(edit_option))
                proc_LogSet(orderno, goodscode, "S01", msg)
                return flg_search

        dicOpt['code'] = option_code
        dicOpt['name'] = option_name.replace("  "," ").strip()
        print(" dicOpt : {}".format(dicOpt))
        if dicOpt == "S01" or dicOpt == "S04":
            print(" (확인필요) after : {}".format(dicOpt))
            proc_LogSet(orderno, goodscode, dicOpt, msg)
            return dicOpt
        else:
            dicOpt['title'] = option_title
            #print(">> dicOpt : {}".format(dicOpt))

    #input(">> next 버튼 클릭전 : ")
    next_url = func_ali.getOtionUrl(browser, dicOpt, aliCode, d_ea, ali_screen_type)
    #print(" next_url  : {}".format(next_url))
    time.sleep(1)

    if next_url[:1] == "X" or next_url[:1] == "S":
        print(">> 주문 불가 옵션 확인필요  : {}".format(next_url))
        proc_LogSet(orderno, goodscode, next_url, msg)
        return next_url

    ######################################################################
    # 옵션 선택
    ######################################################################
    source_tmp = browser.page_source
    str_soup_val = func_ali.getparse(str(source_tmp), 'productSKUPropertyList":', '"skuPriceList":')
    if str(ali_screen_type) == "2" or str(ali_screen_type) == "3":
        str_soup_val = func_ali.getparse(str(source_tmp), '"skuPropertyValues":', '')
        sp_sour_val = str_soup_val.split('"skuPropertyValues":')
    else:
        str_soup_val = func_ali.getparse(str(source_tmp), '"skuPropertyName":', '')
        sp_sour_val = str_soup_val.split('"skuPropertyName":')
    #print(">> str_soup_val : {}".format(str_soup_val))

    opt_cnt = 0
    opt_cnt_sel = 0
    option_name_list = dicOpt['name']
    sp_list = option_name_list.split(':')
    sp_title = option_title.split('|')
    ship_flg = "0"
    rtnFlg = ""
    if len(sp_sour_val) > 0:
        if len(sp_sour_val) == 1:
            if str(sp_sour_val).find('"배송지"') > -1 or str(sp_sour_val).lower().find('ships from') > -1:
                if str(sp_sour_val).lower().find(':"china"') > -1 or str(sp_sour_val).lower().find(':"cn"') > -1 or str(sp_sour_val).find(':"중국"') > -1 :
                    ship_flg = "1"
                    print(">> 소스 옵션 1 배송지 china 포함 ") 
                else:
                    proc_LogSet(orderno, goodscode, "S05", "옵션 불일치 확인필요")
                    return "S05"                    
        # 옵션처리
        for ea_opname in sp_list:
            print(">> option name : {}".format(ea_opname))
            time.sleep(1)
            if ea_opname == "":
                print(">> 옵션 없음 ")
            else:
                ship_flg = "0"
                sour_val_tmp = sp_sour_val[opt_cnt]
                #print(">> 소스 옵션 [{}] : {}".format(opt_cnt, sour_val_tmp))
                if str(sour_val_tmp).find('"배송지"') > -1 or str(sour_val_tmp).lower().find('ships from') > -1:
                    if (str(sour_val_tmp).lower().find('china') > -1 or str(sour_val_tmp).lower().find('cn') > -1):
                        ship_flg = "1"
                    else:
                        proc_LogSet(orderno, goodscode, "S05", "옵션 불일치 확인필요")
                        return "S05"

                    if ea_opname.lower().find('china') > -1 or ea_opname.lower().find('cn') > -1:
                        ship_flg = "1"
                    else:
                        proc_LogSet(orderno, goodscode, "S05", "옵션 불일치 확인필요")
                        return "S05"
                else:
                    print(">> 소스 배송지 china 미포함 ")

                if option_title != "":
                    if str(sp_title[opt_cnt]).find('"배송지"') > -1 or str(sp_title[opt_cnt]).lower().find('ships from') > -1:
                        if ea_opname.lower().find('china') > -1 or ea_opname.lower().find('cn') > -1:
                            #print(">> 주문옵션 china 포함")
                            ship_flg = "1"
                        else:
                            print(">> 주문옵션 china 미포함")
                            proc_LogSet(orderno, goodscode, "S05", "옵션 불일치 확인필요")
                            return "S05"

                if ship_flg == "1":
                    print(">> ship_flg : {}".format(ea_opname))
                else:
                    print(">> opt_cnt_sel : {} | ea_opname : {} ".format(opt_cnt_sel, ea_opname))
                    if ali_screen_type == 2:
                        rtnFlg = func_ali.selOptionClick_type2(browser, ea_opname, opt_cnt_sel)
                    elif ali_screen_type == 3:
                        rtnFlg = func_ali.selOptionClick_type2(browser, ea_opname, opt_cnt_sel)
                    else:
                        rtnFlg = func_ali.selOptionClick_type1(browser, ea_opname, opt_cnt_sel)
                    if rtnFlg == "1":
                        pass
                        # print('>> 옵션 선택 완료 ')
                    else:
                        print('>> S025 : 옵션 선택 불가 ')
                        proc_LogSet(orderno, goodscode, "S025", "옵션 선택 불가")
                        return "S025"
                    opt_cnt_sel = opt_cnt_sel + 1

            opt_cnt = opt_cnt + 1

        print('>> 옵션 선택후 검색창 일시클릭 ')
        if ali_screen_type == 3:
            if rtnFlg == "1" and browser.find_element(By.CSS_SELECTOR,'#search-words'):
                #browser.find_element(By.CSS_SELECTOR,'#search-words').click()
                #browser.find_element(By.CSS_SELECTOR,'#search-words').click()
                browser.find_element(By.CSS_SELECTOR, '#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-left > div.pdp-info > div.pdp-info-right > div > h1').click()
        else:
            if rtnFlg == "1" and browser.find_element(By.CSS_SELECTOR,'div.search-key-box'):
                browser.find_element(By.CSS_SELECTOR,'div.search-key-box').click()


    ############################################
    # input(">> 옵션 선택 완료 ")
    
    #return "0"
    
    ###########################################


    time.sleep(1)
    ######################################################################
    # 수량 선택
    ######################################################################
    if int(d_ea) > 1:
        func_ali.procInputEa(browser, d_ea, ali_screen_type)
        time.sleep(1)

    ######################################################################
    # 배송기간 선택
    ######################################################################
    
    # 배송 클릭
    rtnFlg = func_ali.selShipOption(browser, ali_screen_type)
    if rtnFlg == "1":
        print('>> 추적가능 배송 선택 완료 ')
    else:
        print('>> S024 : 추적가능 배송사 없음 확인필요 ')
        proc_LogSet(orderno, goodscode, "S024", "추적가능 배송사 없음")
        return "S024"

    time.sleep(1)
    result_buy = str(browser.page_source)
    # buy_now = func_ali.getparse(result_buy,'class="product-action"','</span>')
    if ali_screen_type == 2:
        buy_now = func_ali.getparse(result_buy,'class="action--container','')
        buy_now = func_ali.getparse(buy_now,'<button type','</button>')
    elif ali_screen_type == 3:
        buy_now = func_ali.getparse(result_buy,'class="quantity--','')
        if buy_now.find('class="pdp-wrap"') > -1:
            buy_now = func_ali.getparse(buy_now,'','class="pdp-wrap"')
    else:
        buy_now = func_ali.getparse(result_buy,'class="product-action"','</span>')

    if str(buy_now).find('즉시 구매') > -1 or str(buy_now).find('Buy Now') > -1 or str(buy_now).find('바로 구매') > -1:
        pass
        #print(">> 즉시 구매 버튼 존재 OK")
    elif str(result_buy).find('comet-btn-important"><span>바로 구매</span>') > -1:
        print(">> 바로 구매 버튼 존재 OK (type 2) ")
        pass
    else:
        print(">> No 즉시 구매 버튼 확인불가")
        browser.get_screenshot_as_file('C:/project/log/D003_check_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매")
        return "D003"

    browser.set_window_size(1300, 1000)
    browser.set_window_position(0, 0, windowHandle='current')
    time.sleep(1)

    # 즉시구매 버튼 (Element 클릭)
    # if browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow'):
    #     browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow').click()
    #     print('>> 즉시구매 Click OK')
    # elif browser.find_element(By.CLASS_NAME,'button.comet-btn.comet-btn-primary.comet-btn-large.buy-now--buynow--pfifHOs.comet-btn-important'):
    #     browser.find_element(By.CLASS_NAME,'button.comet-btn.comet-btn-primary.comet-btn-large.buy-now--buynow--pfifHOs.comet-btn-important').click()
    #     print('>> 즉시구매 (type 2) Click OK')

    # 즉시구매 버튼 (Element 클릭)
    
    if str(ali_screen_type) == "2" or str(ali_screen_type) == "3":
        # findClassname3 = func_ali.getparse(str(browser.page_source),'class="comet-btn comet-btn-primary comet-btn-large buy-now--buynow--',' comet-btn-important')
        # findSelectname3 = 'button.comet-btn.comet-btn-primary.comet-btn-large.buy-now--buynow--' +str(findClassname3)+ '.comet-btn-important'
        findClassname3 = func_ali.getparse(str(browser.page_source),'comet-v2-btn comet-v2-btn-primary comet-v2-btn-large buy-now--buynow--',' comet-v2-btn-important')
        findSelectname3 = 'button.comet-v2-btn.comet-v2-btn-primary.comet-v2-btn-large.buy-now--buynow--' +str(findClassname3)+ '.comet-v2-btn-important'
        print('>> 즉시구매 - findSelectname3 : {}'.format(findSelectname3))
        if browser.find_element(By.CSS_SELECTOR,findSelectname3):
            browser.find_element(By.CSS_SELECTOR,findSelectname3).click()
        else:
            print('>> 즉시구매 버튼 확인 불가 (type 2) ')
            browser.get_screenshot_as_file('C:/project/log/check_'+str(orderno)+'.png')
            time.sleep(1)
            proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매")
            return "D003"
    else:
        if browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow'):
            browser.find_element(By.CLASS_NAME,'next-btn.next-large.next-btn-primary.buynow').click()
            print('>> 즉시구매 Click OK')
        else:
            print('>> 즉시구매 버튼 확인 불가')
            browser.get_screenshot_as_file('C:/project/log/check_'+str(orderno)+'.png')
            time.sleep(1)
            proc_LogSet(orderno, goodscode, "D003", "No 즉시 구매")
            return "D003"

    time.sleep(3)
    print(">> current_url : {}".format(browser.current_url))


    ##################################################################################
    # 결제 방법 선택
    ##################################################################################
    curr_source = str(browser.page_source)
    
    sour_pay_tmp = func_ali.getparse(str(browser.page_source),'class="payment-safe-info-content"','id="payment-botton-section"')
    sp_pay = sour_pay_tmp.split('data-pl="payment-method-title"')
    print(">> Len(sp_pay) : {}".format(len(sp_pay)))

    # payCnt = 0
    # pay_index = 0
    # for ea_pay in sp_pay:
    #     if payCnt == 0:
    #         payCnt = payCnt + 1
    #         continue
    #     pay_name = func_ali.getparse(str(ea_pay),'>','</span>')
    #     if pay_name.find('******') > -1:
    #         pay_index = payCnt
    #         print(">> Pay_index : {}".format(pay_index))
    #         break

    # curr_source = str(browser.page_source)
    # if curr_source.find('결제 방법 선택') > -1:
    #     findClassnameT = ""
    #     findClassnameC = ""
    #     findClassname = ""
    #     sour_tmp = func_ali.getparse(str(browser.page_source),'data-pl="payment-method-title"','')
    #     if str(sour_tmp).find('chosen-channel--chosen-channel-container--') > -1:
    #         findClassnameT = func_ali.getparse(str(sour_tmp),'chosen-channel--chosen-channel-container--','"').replace(' ','.')
    #         # print(">> findClassnameT : {}".format(findClassnameT))
    #     if str(sour_tmp).find('chosen-channel--chosen-channel-content--') > -1:
    #         findClassnameC = func_ali.getparse(str(sour_tmp),'chosen-channel--chosen-channel-content--','"').replace(' ','.')
    #         # print(">> findClassnameC : {}".format(findClassnameC))

    #     print(">> 결제 방법 선택 Click")
    #     if findClassnameT != "" and findClassnameC != "":
    #         findClassname = 'div.chosen-channel--chosen-channel-container--' +str(findClassnameT)+ ' > div.chosen-channel--chosen-channel-content--' +str(findClassnameC)+ ' > span > span > span'
    #         print(">> findClassname : {}".format(findClassname))
    #         if browser.find_element(By.CSS_SELECTOR, findClassname):
    #             ## div.chosen-channel--chosen-channel-container--2TwO5WE.chosen-channel--pc--2DZIgIG > div.chosen-channel--chosen-channel-content--3OYmsMr > span > span > span
    #             browser.find_element(By.CSS_SELECTOR, findClassname).click() # 결제방법선택
    #             time.sleep(1)

    #             if str(browser.page_source).find('comet-modal-body pop-modal--payment-container-body--') > -1:
    #                 findClassnameP = func_ali.getparse(str(browser.page_source),'comet-modal-body pop-modal--payment-container-body--','"')
    #                 findClassnameP = 'div.comet-modal-body.pop-modal--payment-container-body--' +str(findClassnameP)
    #                 ## findClassnameP = findClassnameP.replace(' ','.') + ' > div:nth-child(1) > div:nth-child(2) > div > div'
                    
    #                 if str(ali_screen_type) == "3":
    #                     findClassnameP = findClassnameP.replace(' ','.') + '.payment-container-body > div:nth-child(1) > div:nth-child(' + pay_index + ') > div > div'
    #                 else:
    #                     findClassnameP = findClassnameP.replace(' ','.') + ' > div:nth-child(1) > div:nth-child(' + pay_index + ') > div > div'
    #                 print(">> (카드선택) findClassnameP : {}".format(findClassnameP))
    #                 # browser.find_element(By.CSS_SELECTOR, 'div.comet-modal-body.pop-modal--payment-container-body--3TzH3_f.payment-container-body > div:nth-child(1) > div:nth-child(2) > div > div')
    #                 browser.find_element(By.CSS_SELECTOR, findClassnameP).click() # 카드선택
    #                 time.sleep(1)
    #                 print(">> (카드선택 확인) Click ")
    #                 browser.find_element(By.CSS_SELECTOR, '#payment-botton-section > button').click() # 카드선택(확인)
    #                 time.sleep(1)

    # sour_tmp = func_ali.getparse(str(browser.page_source),'data-pl="payment-title"','type="button"')
    # if sour_tmp.find('class="chosen-channel--chosen-channel-icon--') > -1:
    #     print(">> Card Icon OK " )
    # else:
    #     print(">> No Card Icon -- Check Please " )
    #     input(">> 결제 방법 선택이 되지 않았습니다. 선택후 아무키나 입력해 주세요:")



    ###########################################################################
    #  전체 입력값 및 상품 체크 하기 
    #  상품 / 가격 / 수량 / 주소 / 총 배송비 / 총합계 
    ###########################################################################
    orderCheckStyle = "0"
    # if str(browser.current_url).find('/order/confirm_order.htm') > -1:
    #     time.sleep(0.5)
    #     orderCheckStyle = "1"
    # elif str(browser.current_url).find('/p/trade/confirm.htm') > -1:
    #     time.sleep(0.5)
    #     orderCheckStyle = "2"
    # else:
    #     print(">> Next page current_url 확인필요 ")
    #     time.sleep(2)
    #     browser.get_screenshot_as_file('C:/project/log/E03_check_'+str(orderno)+'.png')
    #     time.sleep(1)
    #     proc_LogSet(orderno, goodscode, "E03", "Next page Url 확인필요")
    #     return "E03"

    # if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
    #     print(">> 배송 정보 및 주문검토 체크 불가 wait(2) ")
    #     time.sleep(2)
    # if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
    #     print(">> 배송 정보 및 주문검토 체크 불가2 wait(2) ")
    #     time.sleep(2)

    # if str(browser.current_url).find('objectId='+str(aliCode)) == -1:
    #     print(">> 배송 정보 및 주문검토 체크 불가 확인필요 ")
    #     browser.get_screenshot_as_file('C:/project/log/E04_check_'+str(orderno)+'.png')
    #     time.sleep(1)
    #     proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
    #     return "E04"

    # save_current_url = str(browser.current_url)
    # curr_source = str(browser.page_source)
    # if curr_source.find('주문 검토') > -1 or curr_source.find('결제 방법') > -1:
    #     print(">> 주문 검토 / 결제 방법 Ok ")
    # else:
    #     browser.get_screenshot_as_file('C:/project/log/E04_check2_'+str(orderno)+'.png')
    #     time.sleep(1)
    #     proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
    #     return "E04"

    # if browser.find_element(By.XPATH,'//*[@id="root"]'):
    #     txtOrd = str(browser.find_element(By.XPATH,'//*[@id="root"]').text)
    #     if txtOrd.find('주문하기') > -1 :
    #         print(">> 주문하기 버튼 존재 OK ")
    #     elif txtOrd.find('결제하기') > -1:
    #         print(">> 결제하기 버튼 존재 OK ")
    #     else:
    #         print(">> 주문하기 버튼 확인불가 ")
    #         browser.get_screenshot_as_file('C:/project/log/E04_check3_'+str(orderno)+'.png')  
    #         proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
    #         return "E04"
    # else:
    #     browser.get_screenshot_as_file('C:/project/log/E04_check4_'+str(orderno)+'.png')
    #     proc_LogSet(orderno, goodscode, "E04", "배송 정보 및 주문검토 체크 불가 확인필요")
    #     return "E04"

    ######################## 
    # 선택 옵션 체크
    ######################## 
    # check_objectId = func_ali.getparse(str(next_url),'objectId=','&').strip()
    # check_skuAttr = func_ali.getparse(str(next_url),'skuAttr=','&').strip()
    # check_skuId = func_ali.getparse(str(next_url),'skuId=','&').strip()
    # check_quantity = func_ali.getparse(str(next_url),'quantity=','').strip()

    # option_ck_flg = "0"
    # opt_url_check = str(browser.current_url)
    # if opt_url_check.find("countryCode=KR") == -1:
    #     print(">> countryCode=KR 확인필요")
    #     option_ck_flg = "1"
    # if opt_url_check.find(check_objectId) == -1:
    #     print(">> check_objectId 확인필요")
    #     option_ck_flg = "1"
    # if opt_url_check.find(check_skuAttr) == -1:
    #     print(">> check_skuAttr 확인필요")
    #     option_ck_flg = "1"
    # if opt_url_check.find(check_skuId) == -1:
    #     print(">> check_skuId 확인필요")
    #     option_ck_flg = "1"
    
    # if option_ck_flg == "1":
    #     # 주문 옵션 없고, 소스 옵션 갯수 1 이고 ships from 옵션의 경우
    #     if len(sp_sour_val) == 1 and ship_flg == "1" and edit_option == "":
    #         print(" next_url check skip ")
    #     else:
    #         proc_LogSet(orderno, goodscode, "S027", "옵션 선택 불일치 확인필요")
    #         print(">> 옵션 선택 불일치 확인필요")
    #         return "S027"
    # if opt_url_check.find('quantity='+str(check_quantity)) == -1:
    #     print(">> 수량 선택 불일치 확인필요")
    #     proc_LogSet(orderno, goodscode, "S028", "수량 선택 불일치 확인필요")
    #     return "S028"



##############################################
    #sql = getMakeSql("addr", Ouid, Iuid, "")
    sql = getMakeSql_test("addr","","","",orderno)
    #print(">> sql : {}".format(sql))
    row_rcv = db_FS.selectone(sql)
    if not row_rcv:
        print(">> 배송준비중 상태가 아닙니다. ")
        proc_LogSet(orderno, goodscode, "S016", "배송준비중 상태가 아님")
        #return "S016"

    # sql = " select t.uid, i.OrderUid, OrderNo, SettlePrice , RcvPost, rcvName, replace(soc_no,'p','P'), RcvMobile, RcvAddr, RcvAddrDetail "
    m_SettlePrice = row_rcv[3]
    m_RcvPost = str(row_rcv[4]).replace('-','').strip()
    m_rcvName = str(row_rcv[5]).strip()
    m_soc_no = str(row_rcv[6]).strip()
    m_RcvMobile = str(row_rcv[7]).replace('-','').strip()
    m_RcvAddr = str(row_rcv[8]).strip()
    m_RcvAddrDetail = str(row_rcv[9]).strip()
    m_RcvAddrDetail = m_RcvAddrDetail + " (주문:" +str(orderno)+ ")"
    #print(">> 상세 주소 : {}".format(m_RcvAddrDetail))
    print(">> m_SettlePrice : {} | m_RcvPost : {} | m_rcvName : {} | m_soc_no : {} | m_RcvAddr : {} | m_RcvAddrDetail : {} ".format(m_SettlePrice, m_RcvPost, m_rcvName, m_soc_no, m_RcvAddr, m_RcvAddrDetail))

    curr_source1 = browser.page_source
    # time.sleep(0.5)
    # ali_won_cost = ""
    # sell_marzin = ""
    # sell_marzin_rate = 0
    # ali_delivery_cost = "0"
    # dev_detail = ""
    # if orderCheckStyle == "1":
    #     if str(curr_source1).find('class="shopping-cart-product"') > -1:
    #         if str(curr_source1).find('class="logistics-company"') > -1:
    #             ali_logistics_company = func_ali.getparse(str(curr_source1),'class="logistics-company">','</span>')
    #             ali_delivery_day = func_ali.getparse(str(curr_source1),'class="logistics-delivery">','</span>').replace('<font color="#000000">','').replace('</font>','')
    #             ali_delivery_price = func_ali.getparse(str(curr_source1),'class="logistics-cost ">','</span>')
    #             if str(ali_delivery_price).find('$') > -1:
    #                 ali_delivery_price = func_ali.getparse(str(ali_delivery_price),'$','')
    #             if str(ali_delivery_price).find('₩') > -1:
    #                 ali_delivery_price = func_ali.getparse(str(ali_delivery_price),'₩','')
    #             ali_delivery_price = str(ali_delivery_price).replace('US','').replace('$','')
    #             print(">> (0) {} | {} | {}".format(ali_logistics_company, ali_delivery_day, ali_delivery_price))
    #             dev_detail = ali_logistics_company + " | " + ali_delivery_day + " | " + ali_delivery_price

    #         ali_goods_cost = func_ali.getparse(str(curr_source1),'class="charge-cost">','</div>')
    #         ali_delivery_cost = func_ali.getparse(str(curr_source1),'<div class="charge-title">배송','</div>')
    #         if str(ali_delivery_cost).strip() == "":
    #             ali_delivery_cost = "0"
    #         ali_total_cost = func_ali.getparse(str(curr_source1),'class="total-cost"','</div>')
    #         print(">> (1) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
    #     else:
    #         ali_goods_cost = func_ali.getparse(str(curr_source1),'소계','배송')
    #         ali_goods_cost = func_ali.getparse(str(ali_goods_cost),'US','</div>')
    #         ali_delivery_cost = func_ali.getparse(str(curr_source1),'배송','총액')
    #         if ali_delivery_cost.find('무료') > -1:
    #             ali_delivery_cost = "0"
    #         else:
    #             ali_delivery_cost = func_ali.getparse(str(ali_delivery_cost),'US','</div>')
    #         if str(curr_source1).find("주문하기") > -1:
    #             ali_total_cost = func_ali.getparse(str(curr_source1),'총액','주문하기')
    #         elif str(curr_source1).find("지금 결제하기") > -1:
    #             ali_total_cost = func_ali.getparse(str(curr_source1),'총액','지금 결제하기')
    #         else:
    #             ali_total_cost = func_ali.getparse(str(curr_source1),'총액','결제하기')
    #         ali_total_cost = func_ali.getparse(str(ali_total_cost),'US','</div>').replace('</span>','')
    #         dev_detail = "총 배송비 : " + ali_delivery_cost 
    #         print(">> (2) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
    # elif orderCheckStyle == "2":
    #     ali_goods_cost = func_ali.getparse(str(curr_source1),'총 상품 금액','총 배송비')
    #     ali_goods_cost = func_ali.getparse(str(ali_goods_cost),'US','</div>')
    #     ali_delivery_cost = func_ali.getparse(str(curr_source1),'총 배송비','총 합계')
    #     if ali_delivery_cost.find('무료') > -1:
    #         ali_delivery_cost = "0"
    #     else:
    #         ali_delivery_cost = func_ali.getparse(str(ali_delivery_cost),'US','</div>')
    #     if str(curr_source1).find("주문하기") > -1:
    #         ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','주문하기')
    #     elif str(curr_source1).find("지금 결제하기") > -1:
    #         ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','지금 결제하기')
    #     else:
    #         ali_total_cost = func_ali.getparse(str(curr_source1),'총 합계','결제하기')
    #     ali_total_cost = func_ali.getparse(str(ali_total_cost),'US','</div>').replace('</span>','')
    #     dev_detail = "총 배송비 : " + ali_delivery_cost 
    #     print(">> (3) {} | {} | {}".format(ali_goods_cost, ali_delivery_cost, ali_total_cost))
    # else:
    #     print(">> 상품 금액 확인 불가 (exit)")
    #     browser.get_screenshot_as_file('C:/project/log/S020_check_'+str(orderno)+'.png')
    #     # proc_LogSet(orderno, goodscode, "S020", "상품 금액 확인 불가 ")
    #     # return "S020"

    # tmp_ali_total_cost = str(ali_total_cost)
    # while (tmp_ali_total_cost.find('<span') > -1):
    #     if tmp_ali_total_cost.find('<span') > -1:
    #         strSpan = '<span ' + func_ali.getparse(str(tmp_ali_total_cost),'<span','>') + '>'
    #         tmp_ali_total_cost = tmp_ali_total_cost.replace(strSpan,'')
    # tmp_ali_total_cost = tmp_ali_total_cost.replace('<span','').replace('>','').replace('<','').replace('$','').strip()
    # if str(tmp_ali_total_cost).replace('.','').isdigit() == True:
    #     print(">> tmp_ali_total_cost : {}".format(ali_total_cost))
    # else:
    #     print(">> 상품 금액 확인 불가 (exit)")
    #     browser.get_screenshot_as_file('C:/project/log/S020_check_'+str(orderno)+'.png')
    #     # proc_LogSet(orderno, goodscode, "S020", "상품 금액 확인 불가 ")
    #     # return "S020"

    # login_mode : 1 -> input 키값 확인후 진행
    # debug_mode : 1 -> input 키값 확인후 진행
    # gOrder_mode : 1 -> 실제 주문 모드
    # connect_mode : chrome_mode 
    gExchangerate = 1350
    gMarzin_rate = 10
    gDelivery_cost = 4.0
    order_screen_img = ""
    sql = "select login_id, debug_mode, order_mode, exchangerate, marzin_rate, delivery_cost, order_screen_img, isnull(marzin,0), isnull(marzin_set,0) from ali_order_auto_set where login_ip = '{}'".format(currIp)
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
    print(">> ID : {} | debug_mode : {} | gOrder_mode : {} | (설정마진)gMarzin : {} | (gMarzin_set) {} ".format(loginId, debug_mode, gOrder_mode, gMarzin, gMarzin_set))

    # if float(ali_delivery_cost) > gDelivery_cost:
    #     print(">> 배송비 {}달러 초과 ".format(gDelivery_cost))
    #     proc_LogSet(orderno, goodscode, "S021", "배송비 " +str(gDelivery_cost)+ "달러 초과")
    #     return "S021"
    # else:
    #     print(">> 배송비 OK : {} ".format(ali_delivery_cost))
    # ali_won_cost = float(ali_total_cost) * gExchangerate
    # print(">> 원가 | ali: {} * {} = {}".format(ali_total_cost, gExchangerate, ali_won_cost))
    # sell_marzin = float(m_SettlePrice) - float(ali_won_cost)
    # print(">> 마진 | {} - {} = {}".format(m_SettlePrice, ali_won_cost, sell_marzin))
    # if float(sell_marzin) < 0:
    #     print(">> sell_marzin 가격 초과 확인필요 : {}".format(sell_marzin))
    #     proc_LogSet(orderno, goodscode, "S022", "가격 초과 확인필요")
    #     return "S022"

    # if float(sell_marzin) < int(gMarzin):
    #     print(">> sell_marzin 가격 초과 확인필요 : {}".format(sell_marzin))
    #     if str(gMarzin_set) == "0" or str(gMarzin_set) == "1":
    #         proc_LogSet(orderno, goodscode, "S022", "가격 초과 확인필요")
    #         return "S022"

    # sell_marzin_rate = int((sell_marzin / m_SettlePrice) * 100)
    # if sell_marzin_rate < gMarzin_rate:
    #     print(">> 마진율 {}% 이하 가격 확인필요 : {}".format(gMarzin_rate, sell_marzin_rate))
    #     if str(gMarzin_set) == "0" or str(gMarzin_set) == "2":
    #         proc_LogSet(orderno, goodscode, "S023", "마진율 " +str(gMarzin_rate)+ "% 이하 가격 확인필요")
    #         return "S023"
    # else:
    #     print(">> 마진율 : {}".format(sell_marzin_rate))


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
        time.sleep(1)
        proc_LogSet(orderno, goodscode, "E01", "주소 변경 버튼 없음 확인필요")
        return "E01"

    time.sleep(2)
    curr_source2 = browser.page_source
    time.sleep(0.5)

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
        time.sleep(2)
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

    if str(curr_source3).find("여권번호/외국인등록증번호") > -1:
        # func_ali.elem_clear(browser, "[placeholder='여권번호/외국인등록증번호']")
        func_ali.elem_clear(browser, "[placeholder='여권번호/외국인등록증번호*']")
    else:
        func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")
    time.sleep(1)

    func_ali.elem_clear(browser, "[placeholder='받는 사람*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='받는 사람*']")[0].send_keys(m_rcvName)
    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='휴대폰 번호*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='휴대폰 번호*']")[0].send_keys(m_RcvMobile)
    time.sleep(0.2)

    # # 우편번호 검색
    # elem = browser.find_element(By.XPATH,'//*[@id="halo-wrapper-root"]/div/div/form/div[3]/div[2]/div[1]/div/div/div/span/span[1]/input')
    # elem.send_keys(m_RcvPost)
    # time.sleep(1)
    # elem.send_keys(Keys.ENTER)
    # time.sleep(2)

# -------------------------------------------------------------------------------------------------------------
    # browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field")[1]
    # func_ali.getparse(str(browser.page_source),'<input placeholder="상세주소 입력','')
    # func_ali.getparse(str(browser.page_source),'<div class="next-overlay-wrapper opened"','')
    # browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child(4)')

    ## 주소 입력 변경 23.11.23
    ## m_RcvAddr = " 강원특별자치도 원주시 양지로 160 (반곡동, 원주혁신도시 8단지 사랑으로 부영아파트)"
    rtn_addr1, rtn_addr2, rtn_addr3 = func_ali.cut_address(db_FS, m_RcvAddr)
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
        for ea_addr in sp_addr:
            opt_title = func_ali.getparse(ea_addr,'role="option" title="','"')
            liCnt = liCnt + 1
            if opt_title == rtn_addr1:
                print(">>Find (1) OK - ({}) : {}".format(liCnt, opt_title))
                city1_chk = 1
                break
        browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child('+str(liCnt)+')').click()
        time.sleep(2)
        print(">> addr1 Select ")
        # city_elem_after = browser.find_elements(By.CSS_SELECTOR,"span.next-input.next-medium.next-select-inner > span.next-select-values.next-input-text-field > em")
        # if str(city_elem_after[1].text).strip() == rtn_addr1.strip():
        #     print(">> addr1 Select Ok : {}".format(city_elem[1].text))
        # else:
        #     print(">> addr1 Unmatch Check Please : {}".format(city_elem[1].text))
        #     proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(1)")
        #     return "S030"

        time.sleep(1)
        # 주소 구/시 입력
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
                        print(">>Find (2) OK - ({}) : {}".format(liCnt2, opt_title))
                        break
                time.sleep(0.5)
                browser.find_element(By.CSS_SELECTOR,'body > div.next-overlay-wrapper.opened > div > ul > li:nth-child('+str(liCnt2)+')').click()
                time.sleep(1)

        time.sleep(0.5)
        addr_source2 = func_ali.getparse(str(browser.page_source),'<input placeholder="상세주소 입력','placeholder="우편번호*"')
        sp_addr2 = addr_source2.split('</em>')
        chkCnt = 0
        for ea_chk in sp_addr2:
            chkCnt = chkCnt + 1
            opt_title = func_ali.getparse(ea_chk,'<em title="','"')
            if chkCnt == 2:
                if str(opt_title).strip() == rtn_addr2.strip():
                    print(">> addr2 Select Ok : {}".format(opt_title))
                else:
                    print(">> addr2 Unmatch Check Please : {}".format(opt_title))
                    input(">> Key check : ")
                    proc_LogSet(orderno, goodscode, "S050", "자동주소 변환불가(2)")
                    #return "S030"


    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='우편번호*']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='우편번호*']")[0].send_keys(m_RcvPost)
    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='번지, 건물/아파트/단위*']")
    # browser.find_elements(By.CSS_SELECTOR,"[placeholder='번지, 건물/아파트/단위*']")[0].send_keys(m_RcvAddr)
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='번지, 건물/아파트/단위*']")[0].send_keys(rtn_addr3) # 주소3 입력
    time.sleep(0.2)
    func_ali.elem_clear(browser, "[placeholder='상세주소 입력']")
    browser.find_elements(By.CSS_SELECTOR,"[placeholder='상세주소 입력']")[0].send_keys(m_RcvAddrDetail)
    time.sleep(1)

    if len(m_rcvName) < 4:
        if str(curr_source3).find("여권번호/외국인등록증번호*") > -1:
            # 대한민국 국적입니다. YES 클릭
            if browser.find_elements(By.CSS_SELECTOR,'input.next-radio-input')[0]:
                browser.find_elements(By.CSS_SELECTOR,'input.next-radio-input')[0].click()
                time.sleep(1)
        func_ali.elem_clear(browser, "[placeholder='개인통관고유부호*']")
        browser.find_elements(By.CSS_SELECTOR,"[placeholder='개인통관고유부호*']")[0].send_keys(m_soc_no)
        time.sleep(1)
    else:
        print(">> 수령인명 확인 필요 : {} ".format(m_rcvName))
        proc_LogSet(orderno, goodscode, "S017", "수령인명 확인 필요")
        return "S017"
    # if str(curr_source3).find("여권번호/외국인등록증번호") > -1:
    #     browser.find_elements(By.CSS_SELECTOR,"[placeholder='여권번호/외국인등록증번호']")[0].send_keys(m_soc_no)
    # else:
    #     browser.find_elements(By.CSS_SELECTOR,"[placeholder='개인통관고유부호']")[0].send_keys(m_soc_no)
    # print(">> 배송 주소 입력 완료 ")
    time.sleep(1)
    # 배송 주소 편집  Confirm 클릭
    #if browser.find_elements(By.CSS_SELECTOR,'span.next-btn-helper')[0]:
    #    browser.find_elements(By.CSS_SELECTOR,'span.next-btn-helper')[0].click()
    # if browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button'):
    #     browser.find_element(By.CSS_SELECTOR,'button.comet-btn.comet-btn-primary.comet-btn-large.form-item-button').click()
    #     print(">> 배송 주소 입력후 Confirm 클릭")

    # time.sleep(3)
    # curr_source4 = browser.page_source
    # # 배송주소 (기본) 버튼 클릭 #####################################################################
    # if str(curr_source4).find('기본') > -1 or str(curr_source4).find('Default') > -1:
    #     try: # browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-opt-btn > span')[0]
    #         # if browser.find_element(By.CSS_SELECTOR,'span.cm-address-item-content-default-tag'):
    #         #     browser.find_element(By.CSS_SELECTOR,'span.cm-address-item-content-default-tag').click()
    #         print(">> 배송주소 첫번째 선택 ")
    #         if browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-content'):
    #             browser.find_elements(By.CSS_SELECTOR,'div.cm-address-item-content')[0].click()
    #             time.sleep(1)
    #     except Exception as e:
    #         print(">> 배송주소 기본 버튼 클릭 Exception ")
    #         input(">> 알리 Key (기본) 설정을 눌러 주세요 그리고 command 창에 아무키나 입력해주세요: ")
    #     else:
    #         print(">> 배송주소 첫번째 선택 클릭 Ok ")
    # # input(">> check address : ")


    ############################################
    
        # 배송주소 입력하기 완료 #####################################################################
    time.sleep(2)
    curr_source5 = browser.page_source
    time.sleep(1)

    if str(curr_source5).find("배송 정보") > -1 or str(curr_source5).find("배송 주소") > -1  or str(curr_source5).find("shipping address") > -1:
        pass
        #print(">> 배송 정보 Ok")
    else:
        print(">> 배송 정보 입력 오류 (exit)")
        browser.get_screenshot_as_file('C:/project/log/S019_check_'+str(orderno)+'.png')
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류")
        #return "S019"

    delievey_check_str = str(curr_source5)
    if str(curr_source5).find('class="card-container') > -1:
        delievey_check_str = func_ali.getparse(str(curr_source5),'','class="card-container')
    if str(delievey_check_str).find(m_rcvName) > -1:
        if str(delievey_check_str).find(m_RcvMobile) == -1:
            proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (수령인)")
            #return "S019"            
    else:
        if browser.find_element(By.CLASS_NAME,'address-item'):
            delievey_check_str = browser.find_element(By.CLASS_NAME,'address-item').text
            if str(delievey_check_str).find(m_rcvName) == -1:
                proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (수령인)")
                #return "S019"   

    if str(delievey_check_str).find(m_RcvMobile) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (휴대폰)")
        #return "S019" 
    if str(delievey_check_str).find(m_RcvPost) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (우편번호)")
        #return "S019" 
    # if str(delievey_check_str).find(m_RcvAddr) == -1:
    if str(delievey_check_str).find(rtn_addr3) == -1: ## 주소입력 변경
        print(">> delievey_check_str : {}".format(delievey_check_str))
        print(">> rtn_addr3 : {}".format(rtn_addr3))
        input(">> 배송 정보 입력 오류 (주소) : ")
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주소)")
        #return "S019" 
    if str(delievey_check_str).find(orderno) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주문번호)")
        #return "S019"
    
    
    return "0"
    
    ###########################################
    



    # 배송주소 입력하기 완료 #####################################################################
    time.sleep(3)
    curr_source5 = browser.page_source
    time.sleep(1)

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
    if str(delievey_check_str).find(m_RcvAddr) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주소)")
        return "S019" 
    if str(delievey_check_str).find(orderno) == -1:
        proc_LogSet(orderno, goodscode, "S019", "배송 정보 입력 오류 (주문번호)")
        return "S019"

########  test end  ################################################################



########  test end  ################################################################


    return "0"



####################################################################################


    curr_source = str(browser.page_source)
    if curr_source.find('주문 검토') > -1 or curr_source.find('결제 방법') > -1:
        print(">> 주문 검토 / 결제 방법 Ok ")
    else:
        print(">> 주문 검토 / 결제 방법 확인불가")

    if browser.find_element(By.XPATH,'//*[@id="root"]'):
        txtOrd = str(browser.find_element(By.XPATH,'//*[@id="root"]').text)
        if txtOrd.find('주문하기') > -1:
            print(">> 주문하기 버튼 존재 OK ")
        elif txtOrd.find('결제하기') > -1:
            print(">> 결제하기 버튼 존재 OK ")
        else:
            print(">> 주문하기 버튼 확인불가 ")

    return "0"



####################################################################################

#     if gOrder_mode == "1":
#         key_sel = "1"
#     else:
#         key_sel = input(">> 최종 버튼 선택 element 1 | 수동입력 2 : ")

#     if str(key_sel).strip() == "1":
#         button_style = "0"
#         try:
#             buttonB = browser.find_element(By.XPATH,'//*[@id="checkout-button"]')
#             if buttonB:
#                 button_style = "1"
#         except Exception as e:
#             button_style = "0"

#         time.sleep(0.5)
#         if button_style == "0":
#             try:
#                 buttonB = browser.find_element(By.CSS_SELECTOR,'div.pl-order-toal-container__btn-box > button')
#                 if buttonB:
#                     button_style = "2"
#             except Exception as e:
#                 button_style = "0"

#         time.sleep(0.5)
#         if button_style == "0":
#             print(">> E06 : 주문 버튼 클릭 불가 (button Element 확인불가) ")
#             browser.get_screenshot_as_file('C:/project/log/E06_check_'+str(orderno)+'.png')
#             time.sleep(1)
#             proc_LogSet(orderno, goodscode, "E06", "주문 버튼 클릭 불가")
#             return "E06"

#         if buttonB:
#             buttonB.click()
#             print(">> 주문 버튼 클릭 (최종클릭) 완료 ")
#         else:
#             print(">> (최종클릭) 주문 버튼 클릭 불가 ")
#             browser.get_screenshot_as_file('C:/project/log/E06_check2_'+str(orderno)+'.png')
#             time.sleep(1)
#             proc_LogSet(orderno, goodscode, "E06", "주문 버튼 클릭 불가")
#             return "E06"

#     else:
#         input(">> 최종 버튼 선택 수동 입력후 아무키나 눌러주세요 : ")

#     time.sleep(2)
#     result_check = str(browser.page_source)
#     slide_flg = "0"
#     try:
#         if browser.find_element(By.CSS_SELECTOR,'body > div.baxia-dialog.auto > div.baxia-dialog-content'):
#             print(">> [ Slide] we have detected ... ")
#             slide_flg = "1"
#     except Exception as e:
#         print(">> No Slide Exception ")
#     else:
#         print(">> No Slide ")

#     if slide_flg == "1":
#         print(">> [ Slide ] 해제해 주세요 ")
#         my_send_kakao_proc("[Slide] 해제요청 : "+str(datetime.datetime.now()), notice_phone) # 담당자에게 알림톡 전송
#         print(">> 담장자에게 알림톡 발송 : {}".format(notice_phone))
#         input(">> 슬라이드 해제후 아무키나 입력해 주세요 : ")
#         time.sleep(1)

#     time.sleep(3)
#     if str(browser.current_url).find('pay-result.htm') > -1 or str(browser.current_url).find('payResult.htm') > -1:
#         pay_result = browser.page_source
#         if debug_mode == "1":
#             with open("C:/project/log/pay_result_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
#                 f.write(str(pay_result))
#             time.sleep(0.5)

#         if str(pay_result).find('결제 완료') == -1:
#             time.sleep(3)

#         pay_result = browser.page_source
#         if str(pay_result).find('결제 완료') > -1:
#             print(">> 결제 완료 확인 ")
#             if str(pay_result).find(orderno) > -1:
#                 print(">> 결제 완료 OK : {}".format(orderno))
#                 adminMemoSet(orderno, "결제 완료")

#             else:
#                 print(">> 결제완료 확인불가 : {}".format(orderno))
#                 browser.get_screenshot_as_file('C:/project/log/E16_check_'+str(orderno)+'.png')
#                 time.sleep(1)
#                 if debug_mode == "1":
#                     input(">> Key Press (결제 확인불가 0) : ")
#                 else:
#                     proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가")
#                     return "E16"
#         else:
#             print(">> 결제완료 확인불가 ")
#             browser.get_screenshot_as_file('C:/project/log/E16_check2_'+str(orderno)+'.png')
#             time.sleep(1)
#             if debug_mode == "1":
#                 input(">> Key Press (결제 확인불가 1) : ")
#             else:
#                 proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가")
#                 return "E16"
#     else:
#         print(">> 결제 확인불가 ")
#         browser.get_screenshot_as_file('C:/project/log/E16_check3_'+str(orderno)+'.png')
#         time.sleep(1)
#         if debug_mode == "1":
#             input(">> Key Press (결제 확인불가 2) : ")
#         else:
#             proc_LogSet(orderno, goodscode, "E16", "결제완료 확인불가")
#             return "E16"

#     time.sleep(1)
#     try:
#         buttonTest = browser.find_element(By.CSS_SELECTOR,'div.pl-order-toal-container__btn-box > button')
#         if buttonTest:
#             print(">> buttonTest (1) OK ")
#             print(">> buttonTest (1) : {}".format(buttonTest.text))
#             buttonTest.click()
#             print(">> buttonTest (1) click ")
#             time.sleep(3)
#     except Exception as e:
#         print(">> buttonTest (1) Exception ")

#     ###########################################################################
#     #  주문내역 확인하기  
#     #  해외주문번호 / 가격 / 상품정보 체크
#     ###########################################################################
#     time.sleep(1)
#     if str(browser.current_url).find('/order/index.htm') == -1:
#         orderLiskUrl = 'https://www.aliexpress.com/p/order/index.html'
#         browser.get(orderLiskUrl)
#         print(">> {} ".format(orderLiskUrl))
#         time.sleep(3)

#     curr_source_orderlist = browser.page_source
#     time.sleep(0.5)
#     #result_ordlist = browser.page_source
#     # with open("C:/project/log/result_orderlist_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
#     #     f.write(str(result_ordlist))
#     # if debug_mode == "1":
#     #     input(">> Key Press (주문내역 화면) : ")

#     if str(browser.current_url).find('/order/index.htm') == -1:
#         print(">> current_url : {}".format(browser.current_url))
#         print(">> time.sleep(3) wait ")
#         time.sleep(3)

#     if str(browser.current_url).find('/order/index.htm') == -1:
#         print(">> current_url : {}".format(browser.current_url))
#         browser.get_screenshot_as_file('C:/project/log/E15_check_'+str(orderno)+'.png')
#         time.sleep(1)
#         proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가")
#         return "E15"

#     if str(curr_source_orderlist).find('class="order-item"') > -1:
#         print(">> Order List 확인 OK ")
#         new_order_no = ""
#         sp_ord_list = str(browser.page_source).split('order-item-header-right-info')
#         if len(sp_ord_list) > 0:
#             ord_item = sp_ord_list[1]
#             new_order_no = func_ali.getparse(str(ord_item),'detail.html?orderId=','"').strip() # 생성된 새로운 주문번호 
#             new_alino = func_ali.getparse(str(ord_item),'aliexpress.com/item/','.html"').strip()
#             print(">> 주문번호: {} | NEW해외주문번호 : {} | 상품코드 : {}".format(orderno, new_order_no, new_alino))
            
#             sql_o = "select goodscode from t_order_info where sitecate = 'mini' and ali_orderno = '{}'".format(new_order_no)
#             row = db_FS.selectone(sql_o)
#             if row:
#                 print(">> 해외주문번호가 이미 존재 확인필요 : {}".format(new_order_no))
#                 proc_LogSet(orderno, goodscode, "E17", "해외주문번호가 이미 존재 확인필요")
#                 return "E17"

#             if str(new_alino).strip() == aliCode:
#                 pass
#                 #print(">> new_alino : {} | aliCode : {}".format(new_alino, aliCode))
#             else:
#                 order_link = "https://www.aliexpress.com/p/order/detail.html?orderId="+str(new_order_no)
#                 browser.get(order_link)
#                 time.sleep(3)
#                 result_detail_ordlist = browser.page_source
#                 if debug_mode == "1":
#                     with open("C:/project/log/result_detail_ordlist_" +str(orderno)+ ".html","w",encoding="utf8") as f: 
#                         f.write(str(result_detail_ordlist))
#                     time.sleep(0.5)

#                 if str(result_detail_ordlist).find(new_alino) > -1:
#                     print(">> 주문내역 일치하는 상품코드 확인 OK")
#                 if str(result_detail_ordlist).find(m_RcvMobile) > -1:
#                     print(">> 주문내역 일치하는 전화번호 확인 OK") 
#                 else:
#                     print(">> 주문내역 일치하는 연락처 확인불가 (주문내역 확인필요) ")
#                     browser.get_screenshot_as_file('C:/project/log/E02_check_'+str(orderno)+'.png')
#                     proc_LogSet(orderno, goodscode, "E02", "주문내역 일치하는 연락처 확인불가 (주문내역 확인필요)")
#                     return "E02"

#             if new_order_no == "":
#                 print(">> 해외주문번호 확인불가 (주문내역 확인필요)")
#                 browser.get_screenshot_as_file('C:/project/log/E10_check_'+str(orderno)+'.png')
#                 proc_LogSet(orderno, goodscode, "E10", "해외주문번호 확인불가 (주문내역 확인필요)")
#                 return "E10"

#             if debug_mode == "1":
#                 input(">> Key Press (해외주문번호 입력전) :")

#             ## 주문통계갱신 | 해외주문번호 입력 | 카톡 발송 
#             rtnFlg = aliOrdernoSet(orderno, Ouid, Iuid, new_order_no, ali_total_cost, ali_id, goodscode)
#             if rtnFlg == "0":
#                 proc_LogDetailSet(orderno, goodscode, '0', '주문완료 : ' + str(new_order_no), m_SettlePrice, ali_total_cost, ali_won_cost, sell_marzin, dev_detail, new_order_no)
#                 print(">> 주문 [정상] 완료 : {}".format(orderno))
#             else:
#                 return rtnFlg

# ################################################################################################################
#     else:
#         print(">> Order List View Error ")
#         browser.get_screenshot_as_file('C:/project/log/E15_check2_'+str(orderno)+'.png')
#         proc_LogSet(orderno, goodscode, "E15", "주문내역 페이지 확인불가")
#         return "E15"

    return "0"

def adminMemoSet(inOrderno, inMemo):
    print(">> adminMemoSet : {}".format(inMemo))
    memoTime = str(datetime.datetime.now())
    wDate = memoTime[6:-16]
    wDate = wDate.replace("-", "/")
    print(wDate)

    # if inOrderno != "" and inMemo != "":
    #     strAdminMemo = " " + wDate + " [자동주문] " + inMemo + " [adminauto] "
    #     sql = " select isnull(AdminMemo,''), AdminMemoUpdateID, AdminMemoUpdateDate from T_ORDER where OrderNo = '" + inOrderno + "'"
    #     row_a = db_FS.selectone(sql)
    #     if row_a:
    #         rAdminMemo = row_a[0]
    #         #print('>> DB rAdminMemo: ' + str(rAdminMemo))
    #     if rAdminMemo != "":
    #         strAdminMemo = str(rAdminMemo).strip() + " " + strAdminMemo

    #     strAdminMemo = strAdminMemo.replace("'", "")
    #     #print('>> strAdminMemo: ' + str(strAdminMemo))
    #     sql_upd = "UPDATE T_ORDER SET AdminMemo = '" + strAdminMemo + "', AdminMemoUpdateID = '" + gAdmin_Id + "', AdminMemoUpdateDate = getdate() where OrderNo = '" + inOrderno + "'"
    #     #print('>> sql_upd : ' + str(sql_upd))
    #     #print('>> AdminMemo UPDATE : ' + str(strAdminMemo))
    #     if gOrder_mode == "1":
    #         db_FS.execute(sql_upd)
    #         print('>> AdminMemo UPDATE 완료')
    #     return "0"
    # else:
    #     print('>> 입력값을 확인해 주세요. inMemo: ' + str(inMemo))
    #     return "1"

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

    # MSG = msg
    # FAILED_MSG = msg[:13]
    # #print(MSG)
    # #print(FAILED_MSG)

    # ordname = "주문팀"
    # #PHONE = "01090467616"
    # PHONE = str(phone).replace('-','').strip()
    # CALLBACK = "18005086"
    # TEMPLATE_CODE = "norder1"
    # FAILED_TYPE = "SMS"
    # FAILED_SUBJECT = "sendmsg"

    # url = "http://api.apistore.co.kr/kko/1/msg/1stplatform"
    # params = {'PHONE': PHONE, 'CALLBACK': CALLBACK, 'MSG': MSG, 'TEMPLATE_CODE': TEMPLATE_CODE,'FAILED_TYPE': FAILED_TYPE, 'FAILED_MSG': FAILED_MSG, 'FAILED_SUBJECT': FAILED_SUBJECT}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','x-waple-authorization': 'ODE3NC0xNTI0NDU5NzIwNDU3LTNmZTU0YWM0LTA0ZTItNGQ3My1hNTRhLWM0MDRlMjJkNzMyNw=='}

    # resultStr = ""
    # webpage = requests.post(url, data=params, headers=headers)
    # soupNm = BeautifulSoup(webpage.content, "html.parser")
    # resultStr = soupNm.text
    # #print('>> resultStr : ' + str(resultStr))

    # result_code = func_ali.getparse(resultStr, '"result_code":"', '"')
    # result_message = func_ali.getparse(resultStr, '"result_message":"', '"')
    # cmid = func_ali.getparse(resultStr, '"cmid":"', '"')
    # ori_MSG = MSG.replace("'", "")

    # sql_ins = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent) values ('" + ordname + "','" + PHONE + "','" + cmid + "','" + result_code + "','" + result_message + "',getdate(),'" + gAdmin_Id + "','auto','" + ori_MSG + "')"
    # #print('>> sql_ins : ' + str(sql_ins))
    # db_FS.execute(sql_ins)
    # print(">> 카톡전송 (T_KAKAOALIM_LOG) : {}".format(PHONE))

    #print('>> [--- my 카카오톡 전송 end ---] ' + str(datetime.datetime.now()))
    return "0"

def sms_send_kakao_proc(inOrderno, inOrderinfouid):
    #print('>> [--- 카카오톡 전송 start ---] ' + str(datetime.datetime.now()))

#     sql_sel = "select dbo.GetCutStr(GoodsTitle,80,'...') as GTitle,OrdName,OrdMobile from t_order as o inner join T_ORDER_INFO as i on o.uid = i.OrderUid where i.uid = '" + str(inOrderinfouid) + "'"
#     #print('>> sql_sel:' + str(sql_sel))
#     row = db_FS.selectone(sql_sel)

#     if not row:
#         print('>> 해당 데이터가 없습니다. inOrderno: ' + str(inOrderno))
#         return "1"
#     else:
#         goodstitle = row[0]
#         ordname = row[1]
#         ordmobile = row[2]

#         MSG = setMSG("1", ordname, goodstitle)
#         FAILED_MSG = setMSG("2", "", "")
#         #print(MSG)
#         #print(FAILED_MSG)

#         PHONE = ordmobile.replace("-", "")
# ######## test ############################################
#         ## PHONE = "01090467616"
# ##########################################################
#         CALLBACK = "18005086"
#         TEMPLATE_CODE = "norder1"
#         FAILED_TYPE = "SMS"
#         FAILED_SUBJECT = "sendmsg"

#         url = "http://api.apistore.co.kr/kko/1/msg/1stplatform"
#         params = {'PHONE': PHONE, 'CALLBACK': CALLBACK, 'MSG': MSG, 'TEMPLATE_CODE': TEMPLATE_CODE,'FAILED_TYPE': FAILED_TYPE, 'FAILED_MSG': FAILED_MSG, 'FAILED_SUBJECT': FAILED_SUBJECT}
#         headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','x-waple-authorization': 'ODE3NC0xNTI0NDU5NzIwNDU3LTNmZTU0YWM0LTA0ZTItNGQ3My1hNTRhLWM0MDRlMjJkNzMyNw=='}

#         resultStr = ""
#         webpage = requests.post(url, data=params, headers=headers)
#         soupNm = BeautifulSoup(webpage.content, "html.parser")
#         resultStr = soupNm.text
#         #print('>> resultStr : ' + str(resultStr))

#         result_code = func_ali.getparse(resultStr, '"result_code":"', '"')
#         result_message = func_ali.getparse(resultStr, '"result_message":"', '"')
#         cmid = func_ali.getparse(resultStr, '"cmid":"', '"')
#         ori_MSG = MSG.replace("'", "")

#         sql_ins = "insert into T_KAKAOALIM_LOG (ordername,ordermobile,cmid,result_code,result_message,senddate,sendID,sendMethod,sendContent) values ('" + ordname + "','" + PHONE + "','" + cmid + "','" + result_code + "','" + result_message + "',getdate(),'" + gAdmin_Id + "','auto','" + ori_MSG + "')"
#         #print('>> sql_ins : ' + str(sql_ins))
#         db_FS.execute(sql_ins)
#         print(">> 카톡전송 OK (T_KAKAOALIM_LOG) : {}".format(inOrderno))

#         if result_code == "600":
#             # 충전요금부족시 문자발송
#             sql_e = "Insert into sms_msg (phone, callback, status, reqdate, msg ) values('01083160955', '1800-5086', '0', getdate(), '카카오알림톡 충전금 부족' )"
#             #print('>> sql_e : ' + str(sql_e))
#             print(">> 충전요금부족시 문자발송 01083160955 : {}".format(inOrderno))
#             db2 = DBmodule_FR.Database("Main_allinmarket")
#             db2.execute(sql_e)
#             db2.close()

        #print('>> [--- 카카오톡 전송 end ---] ' + str(datetime.datetime.now()))
        return "0"

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

    if m_AdminMemo != "":
        memoTime = str(datetime.datetime.now())
        if m_AdminMemo[:1] == ".":
            print(">> 어드민메모 [자동주문] 있음 ")
        elif m_AdminMemo[:14].find("[자동주문]") > -1 and m_AdminMemo.find("결제 완료") > -1:
            rtn_msg = "주문내역 페이지 확인불가"
            proc_LogSet(m_OrderNo, m_GoodsCode, "E15", rtn_msg)
            #return "E15"
        elif m_AdminMemo[:14].find("[자동주문]") > -1:
            print(">> 어드민메모 [자동주문] 있음 ")
        else:
            rtn_msg = "어드민메모 있음"
            proc_LogSet(m_OrderNo, m_GoodsCode, "S029", rtn_msg)
            #return "S029"

    ## t_order_info 주문건수 1개 이상인지 체크 ##
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
    if int(m_ea) > 3:
        rtn_msg = "수량 3개 이상"
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
    if func_ali.soc_check(m_soc_no, m_rcvName, m_RcvMobile) == "1":
        rtn_msg = "통관번호 불일치"
        proc_LogSet(m_OrderNo, m_GoodsCode, "S008", rtn_msg)
        return "S008"

    return ""

def procStateUpdate(db_con, code, m_Iuid, m_Ouid, m_OrderNo):
    print(">> procStateUpdate 처리 : {} ".format(m_OrderNo))
    # if code == "" or code == "0":
    #     pass
    # else:
    #     print(">> t_order_info 테이블 auto_check_code (update) : {} ".format(code))
    #     sql_u = " update t_order_info set auto_check_code = '{}' where uid = '{}'".format(code, m_Iuid)
    #     #print(">> sql_u : {} ".format(sql_u))
    #     db_con.execute(sql_u)


if __name__ == '__main__':

    now = datetime.datetime.now()
    print('>> [--- main Proc start ---] ' + str(now))
    proc_LogState(">>ali_proc Start")

    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            #print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
    time.sleep(1)

    err_cnt = 0
    proc_flg = "0"
    debug_mode = ""
    login_mode = ""
    ali_id = ""
    order_mode = ""
    connect_mode = "chrome"
    # # 로그인 ID/PASS 입력
    if currIp == "222.104.189.18":
        loginId = 'koiforever0526@gmail.com'
        loginPass = 'uiop7890'

    # login_mode : 1 -> input 키값 확인후 진행
    # debug_mode : 1 -> input 키값 확인후 진행
    # gOrder_mode : 1 -> 실제 주문 모드
    # connect_mode : chrome_mode 
    sql = "select login_id, login_pw, debug_mode, login_mode, ali_id, order_mode, connect_mode, notice_phone from ali_order_auto_set where login_ip = '{}'".format(currIp)
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
        if str(loginId) == "":
            proc_LogState("로그인 아이디 확인불가")
            db_FS.close()
            os._exit(1)

    print(">> ID : {} | debug_mode : {} | login mode : {} | gOrder_mode : {} | connect_mode : {}".format(loginId, debug_mode, login_mode, gOrder_mode, connect_mode))

    time.sleep(1)
    #mainDriver = func_ali.connectDriver(connect_mode)
    main_url = 'http://imp.allinmarket.co.kr'
    # mainDriver = func_ali.connectDriverNew(main_url,"")
    try:
        mainDriver = func_ali.connectDriverNew(main_url,"")
    except Exception as e:
        print(">> connectDriverOld set ")
        mainDriver = func_ali.connectDriverOld(main_url,"")
        print(">> connectDriverOld set OK ")
    time.sleep(1)

    mainDriver.get('https://ko.aliexpress.com/')
    time.sleep(2)
    # if login_mode == "1":
    #     input(">> 로그인 처리후 아무키나 눌러주세요 :")
    # else:
    #     rtnLogin = func_ali.loginProcNew(mainDriver, loginId, loginPass)
    #     if rtnLogin == "1":
    #         input(">> 로그인 처리후 아무키나 눌러주세요 :")

    # time.sleep(1)

    # if str(mainDriver.current_url).find('order/index.htm') > -1:
    #     mainDriver.get('https://ko.aliexpress.com/')
    #     time.sleep(2)
    # mainDriver.set_window_size(1300, 1000)
    # mainDriver.set_window_position(0, 0, windowHandle='current')
    # time.sleep(1)
    # mainDriver.refresh()
    # time.sleep(2)

    # try:
    #     if mainDriver.find_element(By.CSS_SELECTOR,'img._24EHh'):
    #         mainDriver.find_element(By.CSS_SELECTOR,'img._24EHh').click()
    # except Exception as e:
    #     print(">> pop up (img._24EHh) close Exception ")
    # else:
    #     print(">> pop up close Ok ")
    # time.sleep(0.5)

    # try:
    #     if mainDriver.find_element(By.CSS_SELECTOR,'img.btn-close'):
    #         mainDriver.find_element(By.CSS_SELECTOR,'img.btn-close').click()
    # except Exception as e:
    #     print(">> pop up (img.btn-close) close Exception ")
    # else:
    #     print(">> pop up close Ok ")
    # time.sleep(0.5)

    # if str(mainDriver.current_url).find("login.aliexpress") > -1:
    #     print(">> 로그인 불가 종료")
    #     proc_LogState(">> 로그인 불가")
    #     db_FS.close()
    #     mainDriver.quit()
    #     os._exit(1)


    # time.sleep(1)
    # result = mainDriver.page_source
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
    # result = mainDriver.page_source
    # if str(result).find('class="currency">USD') == -1:
    #     print(">> USD 설정 불가 ")

    # if str(result).find('class="language_txt">한국어') == -1:
    #     print(">> 한국어 설정 불가 ")

    input(">> Login After Input : ")

    result = mainDriver.page_source
    # if str(result).find('class="currency">USD') == -1:
    #     print(">> USD 설정 불가 ")
    #     proc_LogState(">> USD 설정 불가") 
    #     proc_flg = "1"

    # if str(result).find('class="language_txt">한국어') == -1:
    #     print(">> 한국어 설정 불가 ")
    #     proc_LogState(">> 한국어 설정 불가")
    #     proc_flg = "1"

    if str(mainDriver.current_url).find('gatewayAdapt=glo2kor') > -1 or str(mainDriver.current_url).find('ko.aliexpress.com') > -1:
        print(">> 한국 배송 ko.aliexpress ")

    if str(result).find('class="ship-to--menuItem') == -1:
        input(">> 한국어 설정 및 USD 통화 설정 하고 숫자키를 입력해 주세요:")
        time.sleep(1)
    else:
        if func_ali.getparse(str(result),'<span class="ship-to--small','</div>').find('/KO/</span><b>USD') > -1:
            print(">> 한국 설정 / USD 설정 OK ")
        else:
            input(">> 한국어 설정 및 USD 통화 설정 하고 숫자키를 입력해 주세요:")
            time.sleep(1)   

    db_ali = DBmodule_FR.Database("aliexpress")
    if proc_flg == "0":
        stop_flg = "0"
        while stop_flg == "0":
            #sql = getMakeSql("main","","","")
            in_orderno = input("주문번호를 입력해주세요: ")
            sql = getMakeSql_test("main","","","",in_orderno)
            if debug_mode == "1":
                print(">> sql : {}".format(sql))
            mainRows = db_FS.select(sql)
            icnt = 0
            if not mainRows:
                print(">> 대상이 없습니다. (종료) ")
                proc_LogState(">>대상이 없습니다")
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

                    m_rcvName = str(m_rcvName).replace(' ','').strip()
                    m_RcvPost = str(m_RcvPost).replace('-','').strip()
                    m_soc_no = str(m_soc_no).replace(' ','').strip()
                    m_RcvMobile = str(m_RcvMobile).replace('-','').strip()

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

                    time.sleep(1)
                    print("\n\n")
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print(">> 주문번호 : {} | alicode : {} | goodscode : {} | site : {} | ea : {} , option : {}, m_regdate : {}".format(m_OrderNo,m_ali_code,m_GoodsCode,m_site,m_ea,m_Item,m_regdate))
                    order_rtn = proc_order_check(dic_order, db_ali)
                    # if order_rtn != "":
                    #     print(">> 주문 불가 (SKIP) : {} ".format(m_OrderNo))
                    #     procStateUpdate(db_FS, order_rtn, m_Iuid, m_Ouid, m_OrderNo)
                    # else:
                    ali_ea = str(m_ali_code) + "@@" + str(m_ea) + "@@" + str(m_Item) + "@@" + str(m_option_title)
                    #print(">> Item : {}".format(ali_ea))
                    if m_ali_code == "":
                        print(">> ali_code 없음 (Skip) : {}".format(m_OrderNo))
                    else:
                        rtn_main = proc_order(mainDriver, dic_order)
                        print(">> 결과 CODE : {}".format(rtn_main))
                        if rtn_main == "0":
                            err_cnt = 0
                        elif rtn_main[:1] == "S" or rtn_main[:1] == "D" or rtn_main[:1] == "X":
                            err_cnt = err_cnt + 1
                            procStateUpdate(db_FS, rtn_main, m_Iuid, m_Ouid, m_OrderNo)
                        else:
                            err_cnt = err_cnt + 1
                        print(">> err_cnt : {} ".format(err_cnt))
                        if rtn_main.find('E') > -1:
                            proc_LogState(">> E 코드 발생 {} | {} ".format(rtn_main, m_OrderNo))
                            stop_flg = "1"
                            break
                        if err_cnt > 10:
                            proc_LogState(">> err_cnt (skip) 10개 이상 : {}".format(rtn_main))
                            stop_flg = "1"
                            break

            # ali_temp = ['4000031771209@@(1052:100014065)Rose Red:XL@@2','32732081471@@/:(193)24V 65ML WEBASTO: (+2,450원),수량:1(옵션가:2450)@@1','1005003617224244@@:(361180:201336100)NL15874XL:CHINA:@@3','33003969449@@:(200971939:200004183)FIREBRICK:0.5MM:@@4']
            # for ali_ea in ali_temp:
            #     print(">> Item : {}".format(ali_ea))
            #     proc_order(mainDriver, ali_ea)

    proc_LogState(">> ali_proc End")

    if debug_mode == "1":
        input(">> Key Press (End): ")

    db_FS.close()
    db_ali.close()
    now = datetime.datetime.now()
    print('>> [--- main Proc End ---] ' + str(now))
    mainDriver.quit()
    os._exit(0)