from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox as msgbox
import os
import datetime
from openpyxl import load_workbook
import pandas as pd
import sys
# p = os.path.abspath('.')
# sys.path.insert(1, p)
# from dbCon import DBmodule_FR5
import DBmodule_FR
import warnings
warnings.simplefilter("ignore")

root = Tk()
root.title("신용카드.가상결제.계좌이체 결제내역 (Excel) 누락건 확인")
root.geometry("640x680") # 가로 * 세로

# 파일 프레임 (파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="파일을 선택하세요", \
        filetypes=(("xlsx 파일","*.xlsx"),("모든파일","*.*")), \
        initialdir="C:/") # 최초에 사용자가 지정한 경로를 보여줌

    for file in files:
        #print(file)
        list_file.insert(END, file)

    print(">> files : {}".format(files))

# 파일 삭제
def del_file():
    #print(list_file.curselection())
    
    for index in reversed(list_file.curselection()):
        #print(index)
        list_file.delete(index)

def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):

    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)

def table_proc(db_con, order_no, regdate, state, ordername, price, price_cancel, pay_kind):
    
    sql_k = "select orderno from miss_pay_tmp where orderno = '{}' and state = '{}'".format(order_no, state)
    row_k = db_con.selectone(sql_k)
    if row_k:
        print(">> Update Skip ")
    else:
        #print(">> Insert miss_pay_tmp")
        if price_cancel == "":
            sql = " Insert into miss_pay_tmp ( orderno, regdate, state, payname, price, pay_kind) values ('{}','{}','{}','{}','{}','{}') ".format(order_no, regdate, state, ordername, price, pay_kind)
        else:
            sql = " Insert into miss_pay_tmp ( orderno, regdate, state, payname, price, cancel_price, pay_kind) values ('{}','{}','{}','{}','{}','{}','{}') ".format(order_no, regdate, state, ordername, price, price_cancel, pay_kind)
        # print(">> sql : {}".format(sql))
        db_con.execute(sql)


def missOrderLog(db_con, order_no, regdate, pay_kind):
    # T_PAY_TRY_MOBILE 테이블에 검색
    sql_l = "select LGD_BUYER, isnull(Re_Hphone, isnull(Re_Phone,'')), regdate, soc_no, LGD_CUSTOM_FIRSTPAY from T_PAY_TRY_MOBILE  where lgd_oid = '{}'".format(order_no)
    row_l = db_con.selectone(sql_l)
    if row_l:
        ordername = row_l[0]
        orderphone = row_l[1]
        orderdate = row_l[2]
        soc_no = row_l[3]
    else:
        ordername = ""
        orderphone = ""
        orderdate = regdate
        soc_no = ""

    sql_k = "select ordername, isnull(orderphone,''), orderdate, isnull(soc_no,'') from miss_order_log where orderno = '{}' ".format(order_no)
    row_k = db_con.selectone(sql_k)
    if row_k:
        ordername = row_k[0]
        orderphone = row_k[1]
        orderdate = row_k[2]
        soc_no = row_k[3]
        if ordername == "":
            sql = "update miss_order_log set ordername = '" +str(ordername)+ "', orderphone = '" +str(orderphone)+ "', orderdate = '" +str(orderdate)+ "', soc_no = '" +str(soc_no)+ "', pay_kind = '" +str(pay_kind)+ "' where orderno = '" +str(order_no)+ "' "
    else:
        sql = " Insert into miss_order_log ( orderno,ordername,orderphone,orderdate,soc_no,pay_kind,order_kbn) values ('{}','{}','{}','{}','{}','{}','2') ".format(order_no, ordername, orderphone, orderdate, soc_no, pay_kind)
        print(">> sql : {}".format(sql))
        db_con.execute(sql)

def orderCheck(db_con, order_no):
    sql = "select OrderNo from t_order where OrderNo = '{}'".format(order_no)
    row = db_con.selectone(sql)
    if not row:
        return "1"

    return "0"

def mian_proc(list_file):
    print(">> mian_proc ")

    db_con = DBmodule_FR.Database('freeship')
    sql_d = "delete from miss_pay_tmp " # 임시 테이블 삭제
    print(">> 임시 테이블 삭제 : miss_pay_tmp ")
    db_con.execute(sql_d)
    procLogSet(db_con, "miss_order_excel", "S", 0, " miss_order_excel Start ")

    f_row = 0
    miss_cnt = 0
    while f_row < list_file.size():
        filename = list_file.get(f_row)
        print("\n---------------------------------------------------")
        print(">> filename ({}) : ".format(filename))
        list_log_wr(">> [{}] ReadFile : {}".format(f_row+1, filename))
        df_excel = pd.read_excel(filename, engine = "openpyxl", header=0)

        if df_excel.columns[2] == "주문번호":
            miss_cnt = 0
            for i in range(0, df_excel.shape[0]):
                shop_no = df_excel.iloc[i,0] # 상점아이디
                regdate = df_excel.iloc[i,1] # 결제.취소일시
                order_no = df_excel.iloc[i,2] # 주문번호
                state = df_excel.iloc[i,3] # 결제상태
                ordername = df_excel.iloc[i,6] # 입금자명
                price = df_excel.iloc[i,7] # 결제.취소액
                pay_kind = "계좌이체"
                table_proc(db_con, order_no, regdate, state, ordername, price, "", pay_kind)

                if orderCheck(db_con, order_no) == "1":
                    missOrderLog(db_con, order_no, regdate, pay_kind)
                    log_msg = ">> 계좌이체 누락건 확인 필요 : {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, regdate)
                    miss_cnt = miss_cnt + 1
                    print(log_msg)
                    list_log_wr(log_msg)

            print(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))
            list_log_wr(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))

        elif df_excel.columns[3] == "주문번호":
            check_list = []
            miss_cnt = 0
            for i in range(0, df_excel.shape[0]):
                shop_no = df_excel.iloc[i,0] # 상점아이디
                regdate = df_excel.iloc[i,1] # 결제.취소일시
                order_no = df_excel.iloc[i,3] # 주문번호
                state = df_excel.iloc[i,4] # 결제상태
                ordername = df_excel.iloc[i,5] # 구매자명
                price = df_excel.iloc[i,6] # 결제액
                price_cancel = df_excel.iloc[i,7] # 취소액
                ordername = ordername[:1] + '*' + ordername[2:]
                pay_kind = "신용카드"
                table_proc(db_con, order_no, regdate, state, ordername, price, price_cancel, pay_kind)

                if orderCheck(db_con, order_no) == "1":
                    print(">> 신용카드 누락건 확인 필요 : {} | {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, price_cancel, regdate))
                    check_list.append(order_no)

            print(">> check_list : {}".format(check_list))
            for check_no in check_list:
                sql = "select orderno, state from miss_pay_tmp where orderno = '{}' and pay_kind = '신용카드' group by orderno, state".format(check_no)
                rows = db_con.select(sql)
                if rows:
                    if len(rows) == 2:
                        print(">> 정상 카드취소건 (Skip) : {}".format(check_no))
                        state1 = rows[0][1]
                        state2 = rows[1][1]
                    else:
                        missOrderLog(db_con, check_no, "", pay_kind)
                        log_msg = ">> 카드 누락건 확인필요(1): {}".format(check_no)
                        print(log_msg)
                        miss_cnt = miss_cnt + 1
                        list_log_wr(log_msg)

                else:
                    missOrderLog(db_con, check_no, "", pay_kind)
                    log_msg = ">> 카드 누락건 확인필요(2): {}".format(check_no)
                    print(log_msg)
                    miss_cnt = miss_cnt + 1
                    list_log_wr(log_msg)

            print(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))
            list_log_wr(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))

        elif df_excel.columns[5] == "주문번호":
            miss_cnt = 0
            for i in range(0, df_excel.shape[0]):
                shop_no = df_excel.iloc[i,0] # 상점아이디
                regdate = df_excel.iloc[i,3] # 결제.취소일시
                order_no = df_excel.iloc[i,5] # 주문번호
                state = df_excel.iloc[i,6] # 결제상태
                ordername = df_excel.iloc[i,9] # 입금자명
                price = df_excel.iloc[i,10] # 결제.취소액
                pay_kind = "가상계좌"
                table_proc(db_con, order_no, regdate, state, ordername, price, "", pay_kind)

                if orderCheck(db_con, order_no) == "1":
                    missOrderLog(db_con, order_no, regdate, pay_kind)
                    log_msg = ">> 가상계좌 누락건 확인 필요 : {} | {} | {} | {} | {} ".format(order_no, ordername, state, price, regdate)
                    print(log_msg)
                    miss_cnt = miss_cnt + 1
                    list_log_wr(log_msg)

            print(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))
            list_log_wr(">> [{}] 누락건 : {} 건 ".format(f_row+1, miss_cnt))

        f_row = f_row + 1
        procLogSet(db_con, "miss_order_excel", "P", miss_cnt, " miss_order_excel (toss 내역) : " + filename)

    procLogSet(db_con, "miss_order_excel", "F", 0, " miss_order_excel End ")
    db_con.close()


def list_log_wr(logmsg):
    list_log.insert(END, logmsg)

# 시작 버튼 클릭 
def start_run():

    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "파일을 추가하세요")
        return

    list_log_wr(">> Log Start : {}".format(str(datetime.datetime.now())))
    try:
        mian_proc(list_file)
    except Exception as err:
        msgbox.showerror("에러", err)        
    list_log_wr(">> Log End : {}".format(str(datetime.datetime.now())))
    list_log_wr("http://imp.allinmarket.co.kr/admin/goods/freeship/miss_order_page.asp")


btn_add_file = Button(file_frame, text="파일추가", padx=5,pady=5, width=12, command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, text="파일삭제", padx=5,pady=5, width=12, command=del_file)
btn_del_file.pack(side="right")

# list 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended",height=10, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

# 닫기 버튼
btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

# 시작 버튼
btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start_run)
btn_start.pack(side="right", padx=5, pady=5)


# list Log 프레임
list_log_frame = Frame(root)
list_log_frame.pack(fill="both", padx=5, pady=5)

scrollbar2 = Scrollbar(list_log_frame)
scrollbar2.pack(side="right", fill="y")

list_log = Listbox(list_log_frame, selectmode="extended",height=20, yscrollcommand=scrollbar2.set)
list_log.pack(side="left", fill="both", expand=True)
scrollbar2.config(command=list_log.yview)

root.resizable(False, False) #창크기변경(x,y)
root.mainloop()

