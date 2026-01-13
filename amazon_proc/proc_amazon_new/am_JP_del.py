import datetime
import os
import random
import uuid
import urllib
import socket
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import DBmodule_AM

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))
ip = socket.gethostbyname(socket.gethostname())

def version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn):
    
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
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)

            time.sleep(60)
            print(">> time.sleep(60)")

            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize > 1000000:
                pass
            else:
                time.sleep(60)
                print(">> time.sleep(60)")

                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 1000000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")

            time.sleep(3)
            
            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception ')
            else:
                pass

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

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

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

def procStockWork(db_con, in_pg, in_ip):
    
    print('>> procStockWork : ' + str(datetime.datetime.now()))

    ip_catecode = ""
    sql = "select proc_ip from update_list3 where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)

    if not rows:
        print(">> [ " + str(in_ip) + " ] proc_ip No : " + str(ip))
        sql = "insert into update_list3 (regdate, proc_ip) values (getdate(),'{0}')".format(in_ip)
        print(">> insert update_list3 (getdate) ")
        db_con.execute(sql)
    else:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] proc_ip : " + str(ip_catecode))
        sql = "update update_list3 set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update update_list3 (getdate) ")
        db_con.execute(sql)

def setGoodsdelProc(db_con, in_DUid, in_DIsDisplay, in_DOptionKind):
    db_con.delete('t_goods_sub', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_category', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_option', "GoodsUid = '{0}'".format(in_DUid))
    db_con.delete('t_goods_content', "uid = '{0}'".format(in_DUid))
    db_con.delete('t_goods', "uid = '{0}'".format(in_DUid))

    print('>> (setGoodsdelProc) t_goods (delete ok) : {}'.format(in_DUid))

    return "0"

def checkOrderHistory(in_code):
    
    rtnCnt = ""
    rtnGoodsuid = ""
    rtnGoodscode = ""
    rtnSitecate = ""

    time.sleep(0.2)
    searchurl = "http://59.23.231.204:8090/service/search.json?cn=freeship&fl=GOODSUID,goodscode,sitecate&se={goodscode:ALL(" +str(in_code)+ "):100:15}&sn=1&ln=10"
    #print("searchurl : "+str(searchurl))

    try:
        print('>> searchurl Connect ')
        req: Request = Request(searchurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(
                random.random()) + ' Safari/537.36', 'Referer': 'https://www.freeship.co.kr'})
        connection = urlopen(req)

    except Exception as ex:
        print('>> checkOrder error (Exit): ', ex)
        #os._exit(1)
        return "E"
    else:
        resultSoup = BeautifulSoup(connection, "html.parser")
        rtnCnt = getparse(str(resultSoup), '"total_count":', ',')
        rtnGoodsuid = getparse(str(resultSoup), '"GOODSUID":"', '"')
        rtnGoodscode = getparse(str(resultSoup), '"GOODSCODE":"', '"')
        rtnSitecate = getparse(str(resultSoup), '"SITECATE":"', '"')

        #print(str(rtnGoodsuid) + " | " + str(rtnGoodscode) + " | " + str(rtnSitecate))
        if rtnGoodscode != "":
            print(">> 주문 내역 있음 : " + str(rtnGoodscode) + " | " + str(rtnSitecate) + " | " + str(rtnGoodsuid))
        else:
            print(">> 주문 내역 없음 : " + str(in_code))

    return str(rtnGoodsuid).strip()

#### Old Goods #####################################################################################################################
def get_old_goodscode(db_con, in_sql1, in_sql2):
####################################################################################################################################
    goodscode_set = []
    chk_data = "0"

    # Del_naver = 1 or 9 상품 삭제 
    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_goodscode in rs_row:
            goodscode = ea_goodscode[0]
            uid = ea_goodscode[1]
            d_Del_naver = ea_goodscode[2]
            RegDate = ea_goodscode[3]
            UpdateDate = ea_goodscode[4]
            goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if in_sql2 != "":
        rs_row2 = db_con.select(in_sql2)
        print('>> ##select all## in_sql2 :' + str(in_sql2))

        if not rs_row2:
            print('>> (UpdateDate) Stock Check complete! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_goodscode in rs_row2:
                goodscode = ea_goodscode[0]
                uid = ea_goodscode[1]
                d_Del_naver = ea_goodscode[2]
                RegDate = ea_goodscode[3]
                UpdateDate = ea_goodscode[4]

                goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if chk_data == "0":
        return ""

    return goodscode_set

#### Old Goods delete ##############################################################################################################
def set_old_delete(db_con, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2):
####################################################################################################################################
    print('>> PG Info : in_pg - {0} | in_pgFilename : {1} | in_pgKbn : {2} | in_pgsite : {3} '.format(in_pg,in_pgFilename,in_pgKbn,in_pgsite))
    allCnt = 0

    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn)

    # asin get
    get_goods_list = []
    get_goods_list = get_old_goodscode(db_con, in_sql1, in_sql2)
    print(get_goods_list)

    if str(get_goods_list).rfind('@') == -1:
        print('>> parsing complete : ' + str(ip))
        return "1"

    print('>> (get_goods_list) len :' + str(len(get_goods_list)))
    print(str(datetime.datetime.now()))
    print('\n\n----------------------------------------------------------')
    for goods_low in get_goods_list:
        allCnt = allCnt + 1

        sp_goods = goods_low.split('@')
        d_goodscode = sp_goods[0]
        d_uid = sp_goods[1]
        d_Del_naver = sp_goods[2]
        d_RegDate = sp_goods[3]
        d_UpdateDate = sp_goods[4]
        print('>>[{}] (set_old_delete) goodscdoe : {} | uid : {} | Del_naver : {} | d_RegDate : {} | d_UpdateDate : {}'.format(allCnt, d_goodscode,d_uid,d_Del_naver,d_RegDate,d_UpdateDate))

        time.sleep(0.5)
        rtnFlg = checkOrderHistory(d_goodscode)
        if rtnFlg == "":
            #setGoodsdelProc
            delFlg = setGoodsdelProc(db_con, d_uid, '', '')
            if delFlg == "0":
                print(">> 주문 내역 없음 삭제처리 OK : {}".format(d_goodscode))
                time.sleep(0.5)
        elif rtnFlg == "E":
            print(">> 주문 내역 확인 ERROR : {}".format(d_goodscode))
            return "E"
        else:
            print(">> 주문 내역 있음 : {}".format(d_goodscode))
            print('>> t_goods 테이블 : order_ck = 1 처리 : {}'.format(d_goodscode))
            uSql3 = " update t_goods set order_ck = '1' where uid = '{}'".format(d_uid)
            db_con.execute(uSql3)

            # if d_Del_naver == '9':
            #     db_NC = DBmodule_AM.Database('navernoclick')
            #     sql = " select goodscode, del_flag from naver_noclick_goods_20210315 where goodscode = '{}'".format(d_goodscode)
            #     rs = db_NC.selectone(sql)
            #     if rs:
            #         print('>> naver_noclick_goods_20210315 테이블 존재 : del_flag = null 처리 : {}'.format(d_goodscode))
            #         uSql = " update naver_noclick_goods_20210315 set del_flag = null where goodscode = '{}'".format(d_goodscode)
            #         db_NC.execute(uSql)
            #     else:
            #         sql2 = " select goodscode, del_flag from naver_noclick_goods where goodscode = '{}'".format(d_goodscode)
            #         rs2 = db_NC.selectone(sql2)
            #         if rs2:
            #             print('>> naver_noclick_goods 테이블 존재 : del_flag = null 처리 : {}'.format(d_goodscode))
            #             uSql2 = " update naver_noclick_goods set del_flag = null where goodscode = '{}'".format(d_goodscode) 
            #             db_NC.execute(uSql2)

            #     print('>> t_goods 테이블 : Del_naver = null / order_ck = 1 처리 : {}'.format(d_goodscode))
            #     uSql3 = " update t_goods set Del_naver = null, order_ck = '1' where uid = '{}'".format(d_uid)
            #     db_con.execute(uSql3) 
            #     db_NC.close()

    return "0"


#### Old Goods #####################################################################################################################
def get_del_naver_goodscode(db_con, in_sql1, in_sql2):
####################################################################################################################################
    goodscode_set = []
    chk_data = "0"

    # Del_naver = 4 상품 삭제 
    rs_row = db_con.select(in_sql1)
    print('>> ##select all## in_sql1 :' + str(in_sql1))

    if not rs_row:
        print('>> (RegDate) Stock Check complete! ')
    else:
        print('>> (RegDate) len :' + str(len(rs_row)))
        chk_data = "1"
        for ea_goodscode in rs_row:
            goodscode = ea_goodscode[0]
            uid = ea_goodscode[1]
            d_Del_naver = ea_goodscode[2]
            RegDate = ea_goodscode[3]
            UpdateDate = ea_goodscode[4]

            goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if in_sql2 != "":
        rs_row2 = db_con.select(in_sql2)
        print('>> ##select all## in_sql2 :' + str(in_sql2))

        if not rs_row2:
            print('>> (UpdateDate) Stock Check complete! ')
        else:
            print('>> (UpdateDate) len :' + str(len(rs_row2)))
            chk_data = "1"
            for ea_goodscode in rs_row2:
                goodscode = ea_goodscode[0]
                uid = ea_goodscode[1]
                d_Del_naver = ea_goodscode[2]
                RegDate = ea_goodscode[3]
                UpdateDate = ea_goodscode[4]

                goodscode_set.append(str(goodscode) + '@' + str(uid) + '@' + str(d_Del_naver) + '@' + str(RegDate) + '@' + str(UpdateDate))

    if chk_data == "0":
        return ""

    return goodscode_set

#### del_naver = 4 delete ##############################################################################################################
def set_del_naver4_delete(db_con, in_pg, in_pgFilename, in_pgKbn, in_pgsite, in_ver, in_sql1, in_sql2):
####################################################################################################################################
    allCnt = 0
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        # version check
        version_check_2(db_con, in_ver, in_pgFilename, in_pgKbn)

    # asin get
    get_goods_list = []
    get_goods_list = get_del_naver_goodscode(db_con, in_sql1, in_sql2)
    # print(get_goods_list)
    if str(get_goods_list).rfind('@') == -1:
        print('>> parsing complete : ' + str(ip))
        return "1"
    print('>> (get_goods_list) len :' + str(len(get_goods_list)))
    print(str(datetime.datetime.now()))

    for goods_low in get_goods_list:
        allCnt = allCnt + 1
        if allCnt == 1 or allCnt == 50:
            if in_pgsite == "uk" or in_pgsite == "UK":
                procStockWork(db_con, in_pg, mac_addr())
            else:
                procStockWork(db_con, in_pg, ip)
            time.sleep(0.2)

        sp_goods = goods_low.split('@')
        d_goodscode = sp_goods[0]
        d_uid = sp_goods[1]
        d_Del_naver = sp_goods[2]
        d_RegDate = sp_goods[3]
        d_UpdateDate = sp_goods[4]
        print('>> [{}] (old_delete) {} ({}) (del:{}) | R: {} | U: {}'.format(in_pgsite,d_goodscode,d_uid,d_Del_naver,d_RegDate,d_UpdateDate))

        time.sleep(0.1)
        try:
            setGoodsdelProc(db_con, d_uid, '', '')
        except Exception as e:
            print('>> 삭제처리 Exception : {}'.format(e))
            return "E"

    return "0"
