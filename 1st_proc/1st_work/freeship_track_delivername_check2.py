

from dataclasses import replace
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os, random
import time, socket
import datetime
import requests
import func_user 
import DBmodule_FR
global upd_cnt
global err_cnt

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

def get_delivery(last_track_no):
    CJ_LIST = ['56','57','58','59','43']
    HJ_LIST = ['80','51']
    deliveryName = ""
    if len(last_track_no) == 12:
        if last_track_no[:2] in CJ_LIST: 
            deliveryName = "CJ대한통운"
        elif last_track_no[:2] in HJ_LIST: 
            deliveryName = "한진택배"
        elif last_track_no[:2] == "31":
            deliveryName = "롯데택배"
        elif last_track_no[:2] == "80" or last_track_no[:2] == "51":
            deliveryName = "한진택배"
    elif len(last_track_no) == 13:
        if last_track_no[:4] == "8003": 
            deliveryName = "한진택배"
        elif last_track_no[:2] == "60":
            deliveryName = "우체국택배"
        elif last_track_no[:2] == "LP": 
            deliveryName = "EMS"

    return deliveryName

def proc_upd(db_fs, orderNo, ouid, InfoUid, last_track_no):
    print(">> proc_upd : {} : {}".format(orderNo, last_track_no))

    deliveryName = get_delivery(last_track_no)
    if last_track_no != "" and deliveryName != "":
        upd_sql = "update freeship_tracking_check set after_trackno = '{0}', after_DeliveryName = '{1}', reason = 'mismatchtracking' where InfoUid = '{2}'".format(last_track_no, deliveryName, InfoUid)
        print(">> upd_sql : {}".format(upd_sql))
        db_fs.execute(upd_sql)

        upd_sql2 = "update T_ORDER_DELIVERY set after_trackno = '{0}', after_DeliveryName = '{1}' where uid = '{2}'".format(last_track_no, deliveryName, InfoUid)
        print(">> upd_sql2 : {}".format(upd_sql2))
        db_fs.execute(upd_sql2)
    else:
        print(">> (skip) update : {} ".format(last_track_no))

def proc_do_global(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs):
    global upd_cnt

    onurl = "https://global.cainiao.com/global/detail.json?mailNos={}&lang=en-US&language=en-US".format(deliveryNo)
    try:
        res = requests.get(onurl, headers={'User-Agent': user_agent, 'Referer': 'https://global.cainiao.com/'})
    except Exception as ex:
        print('>> Exception  ')
    else:
        time.sleep(random.uniform(3, 4.5))
        if res.status_code == 200:
            chk_clearance = "0"
            slide_chk = "0"
            finish_chk = "0"
            if res.text.find('"captcha"') > -1:
                print(">> Slide Check (1) : {}".format(deliveryNo))
                slide_chk = "1"
                try:
                    now_url = "https://global.cainiao.com/newDetail.htm?mailNoList={}&otherMailNoList=".format(deliveryNo)
                    mainDriver.get(now_url)
                    time.sleep(random.uniform(2, 3))
                except Exception as ex:
                    print('>> Exception  ')
                    slide_chk = "1"
                else:
                    time.sleep(random.uniform(1.5, 3))
                    check_flg = "0"
                    while check_flg == "0":
                        if str(mainDriver.page_source).find('captcha') > -1:
                            print(">> Slide Check (1) : {}".format(deliveryNo))
                            procLogSet(db_fs,"naver_unmatch", "E", 0, "프리쉽 송장 delivername_error (Slide Check) : " + str(currIp))
                            input(">> Slide 해제후 아무숫자나 입력 : ")

                            time.sleep(random.uniform(1.5, 3))
                            if str(mainDriver.page_source).find('captcha') == -1:
                                slide_chk = "0"
                                break
                        else:
                            slide_chk = "0"
                            break

                    time.sleep(random.uniform(1.5, 3))
                    res_result = mainDriver.page_source
                    if res_result.find('captcha') > -1:
                        print(">> Slide Check (exit) : {}".format(deliveryNo))
                        procLogSet(db_fs,"naver_unmatch", "E", 0, "프리쉽 송장 delivername_error (Slide Check (exit)) : " + str(currIp))
                        return "1"
                    else:
                        if res_result.find('class="Tracking--desc') > -1:
                            res_desc = getparse(str(res_result),'class="Tracking--desc','class="footer-wrapper')
                            track_no = deliveryNo
                            status = getparse(res_desc,'class="Tracking--orderCode','</p>')
                            status = getparse(status,'<span class="">','</span>')
                            if status.find('<span ') > -1:
                                status = getparse(status,'','<span ')
                            last_track_no = getparse(res_desc,'(Latest Tracking Number:','</span>').replace('\\', '').replace('\t', '').strip()
                            if last_track_no.find('<img ') > -1:
                                last_track_no = getparse(last_track_no,'','<img ').strip()
                            if last_track_no != "":
                                if status == 'DELIVERED' or status == 'DELIVERING' or status == 'CLEAR_CUSTOMS':
                                    chk_clearance == "1"
                                    if status == 'DELIVERED': 
                                        finish_chk = "1"
                                elif res_desc.find("customs clearance") > -1:
                                    chk_clearance = "2"
                                if chk_clearance == "0":
                                    print(">> ({}) {} : {} : ( {} ) status (skip2) ({}) | {}".format(cnt, orderNo, track_no, status, last_track_no, deliveryNo))
                                else:
                                    upd_cnt = upd_cnt + 1
                                    print(">> ({}) {} : {} ( {} ) [ {} ] {}".format(cnt, orderNo, track_no, status, last_track_no, deliveryNo))
                            else:
                                if finish_chk == "1":
                                    upd_sql = "update freeship_tracking_check set delivername_error_flg = '1' where InfoUid = '{}'".format(InfoUid)
                                    print(">> (delivername_error_flg:1) upd_sql : {}".format(upd_sql))
                                    db_fs.execute(upd_sql)
                                print(">> ({}) {} : {} : ( {} ) No lastno (skip3) | {}".format(cnt, orderNo, track_no, status, deliveryNo))
                        else:
                            print(">> ({}) {} | Slide Check (skip1) | {} ".format(cnt, orderNo, deliveryNo))

            else:
                res_json = res.json()
                try:
                    track_no = res_json['module'][0]['mailNo']
                    status = res_json['module'][0]['status']
                    detailList = res_json['module'][0]['detailList']
                except Exception as ex:
                    print('>> Exception : {}'.format(ex))
                    print(">> ({}) {} (skip:e) ".format(cnt, orderNo))
                else:
                    if len(detailList) == 0:
                        print(">> ({}) {} : {} : ( {} ) status (skip0) ".format(cnt, orderNo, track_no, status))
                    else:
                        if status == 'DELIVERED' or status == 'DELIVERING' or status == 'CLEAR_CUSTOMS':
                            chk_clearance = "1"
                            if status == 'DELIVERED': 
                                finish_chk = "1"
                        else:
                            for ea_contant in detailList: # 세부내역확인
                                if ea_contant['standerdDesc'].find("customs clearance") > -1:
                                    chk_clearance = "1"
                                    break

                        if chk_clearance == "1":
                            try:
                                last_track_no = str(res_json['module'][0]['realMailNo']).strip()
                            except Exception as ex:
                                last_track_no = ''
                            if last_track_no != "":  
                                if last_track_no.find('Latest Tracking Number:') > -1:
                                    last_track_no = last_track_no.replace('Latest Tracking Number:', '').replace('\\', '').replace('\t', '').strip()
                                processInfo = res_json['module'][0]['processInfo']
                                print(">> ({}) {} : {} ( {} ) [ {} ] ".format(cnt, orderNo, track_no, status, last_track_no))
                                upd_cnt = upd_cnt + 1
                                proc_upd(db_fs, orderNo, ouid, InfoUid, last_track_no)
                            else:
                                if finish_chk == "1":
                                    upd_sql = "update freeship_tracking_check set delivername_error_flg = '1' where InfoUid = '{}'".format(InfoUid)
                                    print(">> (delivername_error_flg:1) upd_sql : {}".format(upd_sql))
                                    db_fs.execute(upd_sql)
                                print(">> ({}) {} : {} : ( {} ) No lastno (skip3) ".format(cnt, orderNo, track_no, status))
                        else:
                            try:
                                last_track_no = str(res_json['module'][0]['realMailNo']).strip()
                            except Exception as ex:
                                last_track_no = ''
                            if last_track_no != "":  
                                last_track_no = last_track_no.replace('Latest Tracking Number:', '').replace('\\', '').replace('\t', '').strip()

                                try:
                                    progressStatus = str(res_json['module'][0]['processInfo']['progressStatus']).strip()
                                    timeStr = str(res_json['module'][0]['globalCombinedLogisticsTraceDTO']['timeStr']).strip()
                                    desc = str(res_json['module'][0]['globalCombinedLogisticsTraceDTO']['desc']).strip()
                                    desc_tmp = "[{}] [{}] [{}] ( {} )".format(timeStr, progressStatus, desc, status)
                                    print(">> desc_tmp : {}".format(desc_tmp))
                                except Exception as ex:
                                    print(">> except ")
                                    return "E"

                            print(">> ({}) {} : {} : ( {} ) status (skip2) ({}) ".format(cnt, orderNo, track_no, status, last_track_no))

        else:
            print(">> ({}) {} (res.status_code: {} ) (skip1)  ".format(cnt, orderNo, res.status_code))
        return "0"

def proc_do_parcel(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs):
    global upd_cnt
    global err_cnt
    track_no = ""
    status = ""
    print("\n------------------------------------------")
    print(">> ({}) {} : {} ".format(cnt, orderNo, deliveryNo))
    try:
        now_url = "https://parcelsapp.com/ko/tracking/{}".format(deliveryNo)
        mainDriver.get(now_url)
        print(">> now_url : {} ".format(now_url))
        time.sleep(2)
    except Exception as ex:
        print('>> Exception  ')
        slide_chk = "1"
    else:
        time.sleep(random.uniform(3.5, 5))
        className = '#tracking-info > div:nth-child(1) > div.row.parcel'
        try:
            chk_elem = WebDriverWait(mainDriver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, className)))
            print(">> chk_elem Ok ")
        except:
            #print(">> chk_elem : " + className + " 없음")
            chk_elem = ""

        chk_flg = "0"
        while chk_flg == "0":
            if str(mainDriver.page_source).find('class="row parcel"') > -1:
                res_desc = getparse(str(mainDriver.page_source),'class="row parcel"','class="sharing-wrap"')
                if res_desc.find(deliveryNo) > -1:
                    print(">> Find dedeliveryNo : {}".format(deliveryNo))
                    chk_flg = "1"
                    break
                else:
                    time.sleep(random.uniform(1.5, 2.5))

        if str(mainDriver.page_source).find('class="row parcel"') > -1:
            print(">> Source Ok ")
            res_result = mainDriver.page_source
        else:
            input(">> refresh :")
            time.sleep(1)
            res_result = mainDriver.page_source

        if str(mainDriver.page_source).find('아직 정보를 찾지 못했습니다') > -1:
            print(">> 아직 정보를 찾지 못했습니다")
            print(">> After Check (exit) : {}".format(deliveryNo))
            procLogSet(db_fs,"naver_unmatch", "E", 0, "프리쉽 송장 delivername_error (After Check (exit)) : " + str(currIp))
            return "E"

        finish_chk = "0"
        if res_result.find('class="row parcel"') > -1:
            res_desc = getparse(str(res_result),'class="row parcel"','class="sharing-wrap"')
            if res_desc.find(deliveryNo) > -1:
                print(">> Find dedeliveryNo : {}".format(deliveryNo))
                track_no = deliveryNo

                if res_desc.find("택배 배송 완료") > -1:
                    status = "택배 배송 완료"
                    finish_chk = "1"
                elif res_desc.find("소포가 완료") > -1:
                    status = "소포가 완료"
                    # finish_chk = "1"
                elif res_desc.find("지역 배송 센터에 도착") > -1:
                    status = "지역 배송 센터에 도착"
                elif res_desc.find("수입 통관") > -1:
                    status = "수입 통관"
                elif res_desc.find("라인홀 사무실에 도착") > -1:
                    status = "라인홀 사무실에 도착"    
                elif res_desc.find("출발 운송 허브에 도착") > -1:
                    status = "출발 운송 허브에 도착"
                elif res_desc.find("패키지에 대한 정보가 없습니다") > -1:
                    status = "패키지에 대한 정보가 없습니다"
                    time.sleep(random.uniform(1.5, 3))
                else:
                    status_desc = getparse(str(res_desc),'class="event-content">','</div>')
                    status_desc = getparse(str(status_desc),'<strong>','</strong>')
                    print(">> status Check : {}".format(status_desc))

                last_track_no = getparse(res_desc,'다음 추적 번호','</tr>')
                last_track_no = getparse(last_track_no,'class="value">','</td>')
                last_track_no = getparse(last_track_no,'<span>','</span>').replace('\\', '').replace('\t', '').strip()
                if last_track_no != "":
                    print(">> ({}) {} : {} ( {} ) [ {} ] {}".format(cnt, orderNo, track_no, status, last_track_no, deliveryNo))
                    proc_upd(db_fs, orderNo, ouid, InfoUid, last_track_no)
                else:
                    print(">> ({}) {} : {} : ( {} ) No lastno (skip3) | {}".format(cnt, orderNo, track_no, status, deliveryNo))
                    if finish_chk == "1":
                        upd_sql = "update freeship_tracking_check set delivername_error_flg = '1' where InfoUid = '{}'".format(InfoUid)
                        print(">> (delivername_error_flg:1) upd_sql : {}".format(upd_sql))
                        db_fs.execute(upd_sql)
            else:
                print(">> ({}) {} | not found dedeliveryNo (skip1-1) | {} ".format(cnt, orderNo, deliveryNo))
        else:
            print(">> Error Check : {}".format(deliveryNo))
        time.sleep(random.uniform(1, 1.5))
    return "0" 


def proc_do_pkge(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs):
    global upd_cnt
    global err_cnt
    track_no = ""
    status = ""
    print("\n------------------------------------------")
    print(">> ({}) {} : {} ".format(cnt, orderNo, deliveryNo))
    try:
        now_url = "https://pkge.net/ko/parcel/{}".format(deliveryNo)
        mainDriver.get(now_url)
        print(">> now_url : {} ".format(now_url))
        time.sleep(2)
    except Exception as ex:
        print('>> Exception  ')
        slide_chk = "1"
    else:
        time.sleep(random.uniform(3.5, 5))
        className = '#tracking-info > div:nth-child(1) > div.row.parcel'
        try:
            chk_elem = WebDriverWait(mainDriver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, className)))
            print(">> chk_elem Ok ")
        except:
            #print(">> chk_elem : " + className + " 없음")
            chk_elem = ""

        chk_flg = "0"
        while chk_flg == "0":
            if str(mainDriver.page_source).find('class="row parcel"') > -1:
                res_desc = getparse(str(mainDriver.page_source),'class="row parcel"','class="sharing-wrap"')
                if res_desc.find(deliveryNo) > -1:
                    print(">> Find dedeliveryNo : {}".format(deliveryNo))
                    chk_flg = "1"
                    break
                else:
                    time.sleep(random.uniform(1.5, 2.5))

        if str(mainDriver.page_source).find('class="row parcel"') > -1:
            print(">> Source Ok ")
            res_result = mainDriver.page_source
        else:
            input(">> refresh :")
            time.sleep(1)
            res_result = mainDriver.page_source

        if str(mainDriver.page_source).find('아직 정보를 찾지 못했습니다') > -1:
            print(">> 아직 정보를 찾지 못했습니다")
            print(">> After Check (exit) : {}".format(deliveryNo))
            procLogSet(db_fs,"naver_unmatch", "E", 0, "프리쉽 송장 delivername_error (After Check (exit)) : " + str(currIp))
            return "E"

        finish_chk = "0"
        if res_result.find('class="row parcel"') > -1:
            res_desc = getparse(str(res_result),'class="row parcel"','class="sharing-wrap"')
            if res_desc.find(deliveryNo) > -1:
                print(">> Find dedeliveryNo : {}".format(deliveryNo))
                track_no = deliveryNo

                if res_desc.find("택배 배송 완료") > -1:
                    status = "택배 배송 완료"
                    finish_chk = "1"
                elif res_desc.find("소포가 완료") > -1:
                    status = "소포가 완료"
                    # finish_chk = "1"
                elif res_desc.find("지역 배송 센터에 도착") > -1:
                    status = "지역 배송 센터에 도착"
                elif res_desc.find("수입 통관") > -1:
                    status = "수입 통관"
                elif res_desc.find("라인홀 사무실에 도착") > -1:
                    status = "라인홀 사무실에 도착"    
                elif res_desc.find("출발 운송 허브에 도착") > -1:
                    status = "출발 운송 허브에 도착"
                elif res_desc.find("패키지에 대한 정보가 없습니다") > -1:
                    status = "패키지에 대한 정보가 없습니다"
                    time.sleep(random.uniform(1.5, 3))
                else:
                    status_desc = getparse(str(res_desc),'class="event-content">','</div>')
                    status_desc = getparse(str(status_desc),'<strong>','</strong>')
                    print(">> status Check : {}".format(status_desc))

                last_track_no = getparse(res_desc,'다음 추적 번호','</tr>')
                last_track_no = getparse(last_track_no,'class="value">','</td>')
                last_track_no = getparse(last_track_no,'<span>','</span>').replace('\\', '').replace('\t', '').strip()
                if last_track_no != "":
                    print(">> ({}) {} : {} ( {} ) [ {} ] {}".format(cnt, orderNo, track_no, status, last_track_no, deliveryNo))
                    proc_upd(db_fs, orderNo, ouid, InfoUid, last_track_no)
                else:
                    print(">> ({}) {} : {} : ( {} ) No lastno (skip3) | {}".format(cnt, orderNo, track_no, status, deliveryNo))
                    if finish_chk == "1":
                        upd_sql = "update freeship_tracking_check set delivername_error_flg = '1' where InfoUid = '{}'".format(InfoUid)
                        print(">> (delivername_error_flg:1) upd_sql : {}".format(upd_sql))
                        db_fs.execute(upd_sql)
            else:
                print(">> ({}) {} | not found dedeliveryNo (skip1-1) | {} ".format(cnt, orderNo, deliveryNo))
        else:
            print(">> Error Check : {}".format(deliveryNo))
        time.sleep(random.uniform(1, 1.5))
    return "0" 


if __name__=='__main__':

    print('>> [--- deliver check start ---] ' + str(datetime.datetime.now()))
    currIp = socket.gethostbyname(socket.gethostname())
    time.sleep(1)
    print('>> Proc Start : delivername_error ')
    upd_cnt = 0
    err_cnt = 0
    db_fs = DBmodule_FR.Database('freeship')
    procLogSet(db_fs,"naver_unmatch", "S", upd_cnt, "프리쉽 송장 delivername_error 변경송장확인 : " + str(currIp))

    now_url = 'https://https://global.cainiao.com/'
    try:
        print(">> connectDriverOld set ")
        mainDriver = func_user.connectDriverOld(now_url, "")
        print(">> connectDriverOld set OK ")
    except Exception as e:
        print(">> connectDriverNew set ")
        mainDriver = func_user.connectDriverNew(now_url, "")
    mainDriver.set_window_size(1400, 1000)

    print('connectDriver 연결 OK')
    mainDriver.implicitly_wait(3)

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + ' Safari/537.36'
    headers = {'User-Agent': user_agent, 'Referer': 'https://global.cainiao.com/'}

    sql = "select t.OrderNo, t.RegDate, i.ali_orderno, t.state, d.DeliveryName, d.DeliveryNo, c.pay_orderno, t.naver_pay_order_id, \
    i.ali_id, c.procdate, c.ouid, c.InfoUid \
    from freeship_tracking_check as c inner join t_order as t on t.uid = c.ouid \
    inner join t_order_info as i on i.OrderUid = t.uid inner join T_ORDER_DELIVERY as d on d.uid = i.uid \
    where Reason = 'delivername_error' and proc_state is null and c.payway = 'NaverPay' \
    and state in ('201','301','421') and i.ali_id not in ('taobao','taobao1') and d.after_trackno is null \
    and delivername_error_flg is null and c.procdate < getdate() - 2 order by c.procdate asc "

    rows = db_fs.select(sql)
    if rows:
        cnt = 0
        select_flg = "2"
        for row in rows:
            orderNo = row[0]
            regDate = row[1]
            ali_orderno = row[2]
            state = row[3]
            deliveryName = row[4]
            deliveryNo = row[5]
            pay_orderno = row[6]
            naver_pay_order_id = row[7]
            ali_id = row[8]
            procdate = row[9]
            ouid = row[10]
            InfoUid = row[11]
            tmp_chk = ""
            if deliveryNo[:3] == "CNG" or deliveryNo[:2] == "LP":
                pass
            else:
                rtn_deliveryName = get_delivery(deliveryNo)
                if rtn_deliveryName != "":
                    upd_cnt = upd_cnt + 1
                    print(">> ({}) {} : {} (송장변경이동 deliveryNo)".format(cnt, orderNo, deliveryNo))
                    proc_upd(db_fs, orderNo, ouid, InfoUid, deliveryNo)

                else:
                    cnt = cnt + 1
                    print(">> ({}) {} : {} (미체크대상)".format(cnt, orderNo, deliveryNo))
                    continue

            if cnt % 10 == 0:
                print(">> mainDriver.refresh ")
                try:
                    mainDriver.refresh()
                except Exception as e:
                    print(">> connectDriverNew set ")
                time.sleep(2)

            # https://parcelsapp.com/ko/tracking/***** (접속)
            # if select_flg == "1":
            #     #rtn_flg = proc_do_parcel(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs)
            #     rtn_flg = proc_do_pkge(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs)
            #     if rtn_flg == "E":
            #         err_cnt = err_cnt + 1
            #         print(">> ({}) {} : {} | parcel 트래킹 정보 확인 불가 (다음) ".format(cnt, orderNo, deliveryNo))
            #         select_flg = "2"
            #         mainDriver.refresh()
            #         time.sleep(random.uniform(1, 2))
            #     else:
            #         err_cnt = 0
            
            #     if err_cnt > 3:
            #         select_flg = "2"

            if select_flg == "2":
                print("\n------------------------------------------")
                print(">> ({}) {} : {} | {} ".format(cnt, orderNo, deliveryNo, procdate))
    
                # https://global.cainiao.com/newDetail.htm?mailNoList=********&otherMailNoList=  (접속)
                rtn_flg = proc_do_global(user_agent, currIp, mainDriver, deliveryNo, cnt, orderNo, ouid, InfoUid, db_fs)
                if rtn_flg == "E":
                    print(">> ({}) {} : {} | global 트래킹 정보 확인 불가 (종료) ".format(cnt, orderNo, deliveryNo))
                    break

            cnt = cnt + 1
            time.sleep(random.uniform(1, 2))

    procLogSet(db_fs,"naver_unmatch", "F", upd_cnt, "프리쉽 송장 delivername_error 변경송장확인 : " + str(currIp))
    db_fs.close()
    time.sleep(1)
    mainDriver.quit()

    print('>> Proc End upd_cnt : {}'.format(upd_cnt))
    print('>> [--- deliver check end ---] ' + str(datetime.datetime.now()))
    os._exit(0)



