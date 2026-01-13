import os
import socket
import datetime
from openpyxl import load_workbook, Workbook
import pandas as pd
import DBmodule_FR

ver = "네이버페이_전제주문배송현황 1.0"
print(" Ver : {}".format(ver))
log_now = datetime.datetime.now()
log_date = str(str(log_now)[:10] + "_" + str(log_now)[11:-7].replace(":", ""))

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

def procLogSet(db_FS, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)

if __name__ == '__main__':
    upd_cnt = 0
    currIp = socket.gethostbyname(socket.gethostname())
    print(' [--- main start ---] ' + str(datetime.datetime.now()))

    in_file = input('>> Input File : ')
    print('File name :    ', os.path.basename(in_file))
    print('Directory Name:     ', os.path.dirname(in_file))
    
    filepath = os.path.dirname(in_file) + str('\\') + os.path.basename(in_file)
    print('filepath : {}'.format(filepath))
    
    if os.path.isfile(filepath):
        print(">> 파일명 : {}".format(filepath))
    else:
        os._exit(1)

    workbook = load_workbook(filepath)
    df_excel = pd.read_excel(filepath, engine = "openpyxl", header=0)

    rowCnt = 0
    procCnt = 0
    InsCnt = 0
    db_FS = DBmodule_FR.Database("freeship")

    for i in range(0, df_excel.shape[0]):
        naver_pay_no = df_excel.iloc[i,0] # 상품주문번호
        naver_no = df_excel.iloc[i,1] # 주문번호(네이버)
        naver_track_date = df_excel.iloc[i,2] # 발송처리일
        naver_track_name = df_excel.iloc[i,5] # 택배사
        naver_track_no = df_excel.iloc[i,6] # 송장번호
        naver_state = df_excel.iloc[i,7] # 구매확정연장 상태
        naver_goods = df_excel.iloc[i,9] # 상품번호
        naver_price = df_excel.iloc[i,14] # 상품가격
        naver_pay_date = df_excel.iloc[i,19] # 상품결제일
        naver_purchase_date = df_excel.iloc[i,24] # 구매확정 요청일
        naver_purchase_requester = df_excel.iloc[i,25] # 구매확정 요청자
        naver_purchase_confirmdate = df_excel.iloc[i,29] # 구매확정 예정일
        naver_purchase_setdate = df_excel.iloc[i,30] # 구매확정연장 설정일
        naver_purchase_reason = df_excel.iloc[i,31] # 구매확정연장 사유
        naver_state = str(naver_state).replace('nan','').replace('NaT','')
        naver_purchase_date = str(naver_purchase_date).replace('nan','').replace('NaT','')
        naver_purchase_requester = str(naver_purchase_requester).replace('nan','').replace('NaT','')
        naver_purchase_confirmdate = str(naver_purchase_confirmdate).replace('nan','').replace('NaT','')
        naver_purchase_setdate = str(naver_purchase_setdate).replace('nan','').replace('NaT','')
        naver_purchase_reason = str(naver_purchase_reason).replace('nan','').replace('NaT','')
        # print(">> naver_pay_no : {}".format(naver_pay_no))

        if str(naver_pay_no) == "":
            continue

        sql = " select DeliveryNo, orderno, ali_orderno, i.CateCode, i.sitecate, regdate, o.state, i.ali_id, o.PAYWAY, o.naver_pay_product_code, o.uid, i.uid, isnull(d.after_trackno,'') from t_order as o inner join t_order_info as i on i.OrderUid = o.uid inner join t_order_delivery as d on d.uid = i.uid  where o.naver_pay_product_code = '{}'".format(naver_pay_no)
        row = db_FS.selectone(sql)
        if row:
            DeliveryNo = row[0]
            orderno = row[1]
            ali_orderno = row[2] 
            CateCode = row[3] 
            sitecate = row[4] 
            regdate = row[5]
            state = row[6]
            ali_id = row[7]
            payway = row[8]
            Pay_orderno = row[9]
            oUid = row[10]
            iUid = row[11]
            after_trackno = row[12]

            if str(DeliveryNo).strip().upper() != str(naver_track_no).strip().upper():
                print("\n\n---------------------------------------------------")
                if str(naver_state) == "nan" or str(naver_state) == "":
                    pass
                elif str(naver_state) == "무기한연장 중":
                    print(">> [{}] 무기한연장 중 : {}".format(naver_pay_no, naver_state))
                    sql = "select naver_pay_orderno from naver_delivering_list where naver_pay_orderno = {}".format(Pay_orderno)
                    row = db_FS.selectone(sql)
                    if not row:
                        sql_i = "insert into naver_delivering_list (naver_pay_no, naver_pay_orderno, Ouid, Iuid, sitecate, deliveryNo_freeship, deliveryNo_naver) \
                            values ('{}','{}',{},{},'{}','{}','{}')".format(naver_no,naver_pay_no,oUid,iUid,sitecate,DeliveryNo,naver_track_no)
                        print(">> (Insert) naver_delivering_list ")
                        db_FS.execute(sql_i)
                else:
                    print(">> 구매확정연장 상태 : {}".format(naver_state))
                procCnt = procCnt + 1
                print(">> Unmatch Track No : {} | {} | freeship state : {}".format(DeliveryNo, naver_track_no, state))
                print(">>({}) {} [{}] {} | {} | {} | {} ".format(procCnt, naver_pay_no, DeliveryNo, orderno, ali_orderno, sitecate, regdate))
                print(">> {} | {} | {} | {} | {} | {} | {} | {} | {} ".format(naver_track_date, naver_track_name, naver_track_no, naver_state, naver_purchase_date, naver_purchase_requester, naver_purchase_confirmdate, naver_purchase_setdate, naver_purchase_reason))

                sqlW = "select Pay_orderno, ProcDate, OrderNo, Reason, proc_state, memo, memodate, pre_trackno, now_trackno from freeship_tracking_check where Pay_orderno = '{}' and Reason = 'naver_unmatch' ".format(naver_pay_no)
                rowW = db_FS.selectone(sqlW)
                if not rowW:
                    if after_trackno == "":
                        print(">> (변경대상아님) [{}] after_trackno : {}".format(Pay_orderno, after_trackno))
                    else:
                        sql_Ins = "insert into freeship_tracking_check ( ProcDate, RegDate, OrderNo, ali_orderno, ali_id, PAYWAY, Pay_orderno, Reason, OUid, InfoUid, proc_state, memo, tmp_delivery_no, new_delivery_no, naver_state,naver_purchase_date,naver_purchase_requester,naver_purchase_confirmdate,naver_purchase_setdate,naver_purchase_reason) values \
                            ( getdate(), '{}','{}','{}','{}','{}','{}','naver_unmatch','{}','{}','3','네이버송장비교', '{}','{}','{}','{}','{}','{}','{}','{}')".format(regdate,orderno,ali_orderno,ali_id,payway,Pay_orderno,oUid,iUid,naver_track_no,DeliveryNo,naver_state,naver_purchase_date,naver_purchase_requester,naver_purchase_confirmdate,naver_purchase_setdate,naver_purchase_reason)
                        print(">> sql_Ins : {}".format(sql_Ins))
                        db_FS.execute(sql_Ins)
                        InsCnt = InsCnt + 1
                else:
                    Pay_orderno = rowW[0]
                    ProcDate = rowW[1]
                    OrderNo = rowW[2] 
                    Reason = rowW[3] 
                    proc_state = rowW[4]
                    memo = rowW[5]
                    memodate = rowW[6]
                    pre_trackno = rowW[7] 
                    now_trackno = rowW[8]
                    print(">> DB 존재(state:3) : {} | {} | {} | {} | {} | {} | {} | {} ".format(Pay_orderno, ProcDate, OrderNo, Reason, proc_state, memo, memodate, pre_trackno, now_trackno))
        else:
            print(">> ")

    procLogSet(db_FS,"naver_unmatch", "P", InsCnt, "프리쉽 송장 네이버 페이 송장비교 : " + str(currIp))
    db_FS.close()
    print(' [--- main End ---] ' + str(datetime.datetime.now()))
    os._exit(0)
