
from urllib.error import URLError, HTTPError
import urllib.request
import time
from PIL import Image
import time,random
import os, socket, sys
import requests
import json
import datetime
import DBmodule_AM
global errCnt 
global okCnt 

# 68번 ep_proc_amazon 테이블 Insert
def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_AM.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    print(">> sql : {}".format(sql))
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

def get_new_token_v1():
    auth_server_url = "https://bizmsg-web.kakaoenterprise.com/v1/oauth/token"
    headers = {'Authorization': 'Basic C000000440 C000000440_BxgTAnthSdSiwK13yJ7eYg','Content-Type': 'application/x-www-form-urlencoded'}
    token_req = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url, data=token_req, headers=headers)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server")
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

def sms_send_kakao_proc_new(msg, phone):
    db_FS = DBmodule_AM.Database("freeship")
    token = get_new_token_v1()
    test_api_url = "https://bizmsg-web.kakaoenterprise.com/v1/message/send"
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
        print(">> phone_number : {}".format(phone_number))

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

    db_FS.close()


def downFileProc2(down_url, save_file):
    downFlg = "1"
    max_retries = 2 # 재시도 횟수 설정
    attempt = 0
    while attempt < max_retries:
        try:
            # URL에서 데이터를 읽어옵니다. timeout=00 는 000초의 제한시간을 설정합니다.
            with urllib.request.urlopen(down_url, timeout=60) as response:
                with open(save_file, 'wb') as file:
                    file.write(response.read())
            print(">> 이미지가 성공적으로 저장 : {}".format(save_file))
            downFlg = "0"
            break  # 성공 시 반복 종료

        # HTTP 오류 처리 (상태 코드 포함)
        except HTTPError as e:
            print(f">> HTTP 오류가 발생했습니다: {e.code}, {e.reason}")
            break  # HTTP 오류는 재시도할 필요가 없을 수 있으므로 종료

        # URL 오류 처리 (네트워크 오류, 잘못된 URL 등)
        except URLError as e:
            print(f">> URL 오류가 발생했습니다: {e.reason}")
            attempt += 1

            if isinstance(e.reason, TimeoutError):
                print(">> 요청 시간이 초과되었습니다.")
                time.sleep(random.uniform(3,5))
                if attempt < max_retries:
                    print(">> 재시도 중...")
                    time.sleep(2)  # 2초 대기 후 재시도                
                else:
                    print(">> 재시도 횟수를 초과했습니다.")
                    break
            else:
                print(f">> URL 오류가 발생했습니다: {e.reason}")
                break

        # 그 외의 일반적인 예외 처리
        except Exception as e:
            print(f">> 알 수 없는 오류가 발생했습니다: {e}")
            break

    return downFlg


def downFileProc(down_url, save_file):
    downFlg = "1"
    max_retries = 2 # 재시도 횟수 설정
    attempt = 0
    while attempt < max_retries:
        try:
            # 이미지 다운로드 시도
            urllib.request.urlretrieve(down_url, save_file)
            print(">> 이미지가 성공적으로 저장 : {}".format(save_file))
            downFlg = "0"
            break  # 성공 시 반복 종료

        # HTTP 오류 처리 (상태 코드 포함)
        except HTTPError as e:
            print(f">> HTTP 오류가 발생했습니다: {e.code}, {e.reason}")
            break  # HTTP 오류는 재시도할 필요가 없을 수 있으므로 종료

        # URL 오류 처리 (네트워크 오류, 잘못된 URL 등)
        except URLError as e:
            print(f">> URL 오류가 발생했습니다: {e.reason}")
            attempt += 1
            if attempt < max_retries:
                print(">> 재시도 중...")
                time.sleep(2)  # 2초 대기 후 재시도
            else:
                print(">> 재시도 횟수를 초과했습니다.")
                break

        # 그 외의 일반적인 예외 처리
        except Exception as e:
            print(f">> 알 수 없는 오류가 발생했습니다: {e}")
            break

    return downFlg

if __name__ == '__main__':

    print(">> Start Image Conver ")
    print(str(datetime.datetime.now()))
    inpit_site = str(sys.argv[1]).lower().strip()
    input_phone = str(sys.argv[2]).strip()
    print(">> Site : {} | error alarm phone : {}".format(inpit_site, input_phone))

    sel_sql = ""
    if inpit_site.find('@') > -1:
        sel_site = inpit_site.split('@')[0]
        sel_sql = inpit_site.split('@')[1]
    else:
        sel_site = inpit_site

    proc_flg = ""
    if sel_site == "cn" or sel_site == "shop" or sel_site == "ref" or sel_site == "red":
        proc_flg = "0"
        pass
    else:
        proc_flg = "1"
        print(">> Site Check Please : {}".format(sel_site))

    print(str(datetime.datetime.now()))
    print(" start proc ({}) : {}".format(sel_site, datetime.datetime.now()))
    current_folder = os.getcwd()
    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() == "222.104.189.18":
        default_folder = "E:/amazon_proc/Goodsimage/Big/"
    else:
        if sel_site == "shop":
            default_folder = "E:/Goodsimage/Big/"
        elif sel_site == "ref":
            default_folder = "G:/Goodsimage/Big/"
        elif sel_site == "cn":
            default_folder = "F:/Goodsimage/Big/"
        elif sel_site == "red":
            default_folder = "F:/Goodsimage/Big/"
    currtime = str(datetime.datetime.now()).replace(' ','_').replace(':','_')[:19]
    print(" default_folder : {}".format(default_folder))
    print(" currtime : {}".format(currtime))

    # TEST #######################################################
    ## default_folder = "D:/Goodsimage/Big/"
    # TEST #######################################################

    while proc_flg == "0":
        errCnt = 0
        okCnt = 0

        db_con = DBmodule_AM.Database(sel_site)
        input_kbn = ""
        sql = ""
        if sel_site == "cn":
            sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate >= '2023-08-01 00:00:00' and RegDate < DATEADD(HH, -1, getdate()) and img_url is null and goodscode is not null and confirm_goods = 1 and imgb_update_flg is null "
            sql = sql + " union all "
            sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate < '2023-08-01 00:00:00' and UpdateDate > '2023-08-01 00:00:00' and UpdateDate < '2024-01-09 00:00:00' and img_url is null and goodscode is not null and naver_in = '1' and confirm_goods is null "
            sql = sql + " union all "
            sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where UpdateDate > '2023-08-01 00:00:00' and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
        elif sel_site == "red" :
            if sel_sql == "":
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate >= '2023-08-01 00:00:00' and RegDate < DATEADD(HH, -12, getdate()) and img_url is null and goodscode is not null and confirm_goods = 1 and imgb_update_flg is null "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where UpdateDate >= '2023-08-01 00:00:00' and UpdateDate < DATEADD(HH, -12, getdate()) and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
            elif sel_sql == "1":
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate >= getdate()-3 and RegDate < DATEADD(HH, -12, getdate()) and img_url is null and goodscode is not null and confirm_goods = 1 and imgb_update_flg is null "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where UpdateDate >= getdate()-3 and UpdateDate < DATEADD(HH, -12, getdate()) and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
            elif sel_sql == "2":
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate < getdate()-3 and img_url is null and goodscode is not null and confirm_goods = 1 and imgb_update_flg is null "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where UpdateDate < getdate()-3 and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
        elif sel_site == "ref" :
            if sel_sql == "1":
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate < DATEADD(HH, -1, getdate()) and img_url is null and goodscode is not null and del_naver = '7' and stop_update is null and IsDisplay = 'T' and imgb_update_flg is null and confirm_goods <> 2 "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where goodscode is not null and confirm_goods = 5 and RegDate < getdate()-3 "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where del_naver is null and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
            elif sel_sql == "2":
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where goodscode is not null and confirm_goods = 5 and RegDate >= getdate()-3 "
            else:
                sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate < DATEADD(HH, -1, getdate()) and img_url is null and goodscode is not null and del_naver = '7' and stop_update is null and IsDisplay = 'T' and imgb_update_flg is null and confirm_goods <> 2 "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where goodscode is not null and confirm_goods = 5 "
                sql = sql + " union all "
                sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where del_naver is null and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
        else:
            sql = " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate < DATEADD(HH, -1, getdate()) and img_url is null and goodscode is not null and del_naver = '7' and stop_update is null and IsDisplay = 'T' and imgb_update_flg is null and confirm_goods <> 2 "
            sql = sql + " union all "
            sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where goodscode is not null and confirm_goods = 5 "
            sql = sql + " union all "
            sql = sql + " select top 50 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where del_naver is null and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "

        print("\n>> sql : {}".format(sql))
        print("\n-------------------------------------------------")
        proc_cnt = 0
        while proc_cnt < 10:
            rowMain = db_con.selectone(sql)
            if not rowMain:
                print(">> 작업 대상이 없습니다 : {} ".format(datetime.datetime.now()))
                break

            rows = db_con.select(sql)
            i = 0
            for row in rows:
                rtn_chk = ""
                img_size_del = ""
                uid = row[0]
                goodscode = row[1]
                imgB = row[2]
                cate_idx = row[3]
                regdate = row[4]
                updatedate = row[5]
                imgb_update_flg = row[6]
                naver_in = str(row[7])
                confirm_goods = row[8]
                imgUrl = str(imgB)

                exeName = ".jpg"
                if str(imgB).lower().find('.jpg') > -1:
                    exeName = '.jpg'
                elif str(imgB).lower().find('.jpeg') > -1:
                    exeName = '.jpeg'
                elif str(imgB).lower().find('.png') > -1:
                    exeName = '.png'
                savefilename = goodscode + exeName

                if goodscode == "":
                    continue

                print("\n")
                print("\n{}".format(datetime.datetime.now()))
                print("\n\n[ {} ] ( {} ) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>".format(sel_site, i+1))

                ## oodsImgUrl = "https://" +str(sel_site)+ ".freeship.co.kr/Goodsimage/Big/" + str(cate_idx) + "/" + savefilename
                goodsImgUrl = "http://" +str(sel_site)+ ".freeship.co.kr/Goodsimage/Big/" + str(cate_idx) + "/" + savefilename
                #print(">> goodsImgUrl : {}".format(goodsImgUrl))

                if sel_site == "cn":
                    if imgUrl.find("https:") == -1:
                        imgUrl = "https:" + imgUrl

                ## img down Start
                savelocation = default_folder + str(cate_idx) # 내컴퓨터의 저장 위치
                savefile = savelocation + "/" + savefilename
                print(">> [{}] {} (update:{} | flg:{}) (naver_in :{}) | {} | {}".format(goodscode, regdate, updatedate, imgb_update_flg, naver_in, cate_idx, imgUrl))
                print(">> savelocation:{}".format(savelocation))
                try:
                    if not os.path.exists(savelocation):
                        os.mkdir(savelocation)
                        print(f">> mkdir : {savelocation}")
                    else:
                        print(">> floder Ok ")
                except OSError as e:
                    print(">> OSError : {}".format(e))
                    input(">> Input(1) : ")
                except Exception as e:
                    print(">> Exception : {}".format(e))
                    input(">> Input(1-1) : ")
                else:
                    time.sleep(random.uniform(1.5,2))
                    try:
                        # time check
                        start = time.time()
                        # 이미지 요청 및 다운로드
                        if sel_site == "cn":
                            print(">> (curl) ")
                            os.system("curl " + imgUrl + " > "+ str(savefile))
                        elif sel_site == "shop":
                            ## urllib.request.urlretrieve(imgUrl, savefile)
                            request_fp = urllib.urlopen(imgUrl, timeout=600)
                            with open(savefile, 'wb') as f:
                                try:
                                    f.write(request_fp.read())
                                except:
                                    print(">> (urllib) tre error ")
                        elif sel_site == "red":
                            imgChkUrl = str(imgB)[-5:].lower()
                            if imgChkUrl.find('.jpg') > -1 or imgChkUrl.find('.jpeg') > -1 or imgChkUrl.find('.png') > -1:
                                print(">> (curl) imgChkUrl (뒷5자리) : {}".format(imgChkUrl))
                                os.system("curl " + imgUrl + " > "+ str(savefile))
                            else:
                                print(">> (urlretrieve) ")
                                urllib.request.urlretrieve(imgUrl, savefile)
                        elif sel_site == "ref":
                            time.sleep(random.uniform(1.5,3))
                            rtn_chk = downFileProc2(imgUrl, savefile)
                            print(">> rtn_chk : {}".format(rtn_chk))
                            # if imgUrl.find('i.ebayimg.com') > -1:
                            #     print(">> (urlretrieve) ")
                            #     urllib.request.urlretrieve(imgUrl, savefile)                               
                            # else:
                            #     print(">> (curl) ")
                            #     os.system("curl " + imgUrl + " > "+ str(savefile))
                        else:
                            print(">> (urlretrieve) ")
                            urllib.request.urlretrieve(imgUrl, savefile)
                        print(">> img down end ... : {}".format(time.time() - start))

                    except Exception as e:
                        print('>>\n error msg : {}'.format(e))
                        if str(e).find('호스트로부터 응답이 없어') > -1 and sel_site == "ref":
                            print(">> Retry ")
                            time.sleep(random.uniform(2,4))
                            try:
                                print(">> (curl) ")
                                os.system("curl " + imgUrl + " > "+ str(savefile))
                            except Exception as e:
                                print('>>\n error msg : {}'.format(e))
                                print('>> imgB : {}'.format(imgB))
                                errCnt = errCnt + 1
                                rtn_chk = '1'
                        else:
                            print('>> imgB : {}'.format(imgB))
                            errCnt = errCnt + 1
                            rtn_chk = '1'
                        #input(">>Input 1 :")

                    if rtn_chk != "1":
                        tf = os.path.join(savelocation + "/", savefilename)
                        # print(tf)

                        try:
                            # 저장 된 이미지 확인
                            img = Image.open(tf)
                            imgx, imgy = img.size
                            print(">> img Size : {} | {} ".format(imgx, imgy))

                            ## img.resize((512, 512))    # 이미지 크기 변경하기
                            # if imgx < 500 and imgy < 500:
                            #     img = img.resize((512, 512)) 
                            #     print(">> imgx {} | imgy {} -> 512 | 512 size convert : {}".format(imgx, imgy, goodscode))
                            # elif imgx < 500:
                            #     img = img.resize((512, imgy)) 
                            #     print(">> imgx {} -> 512 size convert : {}".format(imgx, goodscode))
                            # elif imgy < 500:
                            #     img = img.resize((imgx, 512)) 
                            #     print(">> imgy {} -> 512 size convert : {}".format(imgy, goodscode))
                            root,extension = os.path.splitext(tf)
                            tf_format_ori = img.format
                            extension = extension[1:]
                            #if tf_format_ori == 'WEBP':
                            img = img.convert('RGB')
                            if extension == 'jpg' or extension == 'jpeg' :
                                img.save(tf,'jpeg')
                            else :
                                img.save(tf,extension)
                        except Exception as e:
                            print("error file : {} | {}".format(tf, imgB))
                            print("error msg : {}".format(e))
                            errCnt = errCnt + 1
                            rtn_chk = '1'
                            #input(">>Input 2:")
                        else:
                            if imgx < 500 or imgy < 500:
                                print(">> (Skip) imgx {} | imgy {} size : {}".format(imgx, imgy, goodscode))
                                rtn_chk = '1'
                                img_size_del = '1'
                            else:
                                rtn_chk = '0'
                                print('>> 완료 : {} -> {}  ({})'.format(tf_format_ori, extension, goodsImgUrl))
                            okCnt = okCnt + 1
                            errCnt = 0
                            img.close 

                if rtn_chk == "0": # img download Ok  ( img_url, img_url_date update )
                    if imgb_update_flg == "1" and naver_in == "1":
                        # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(U)
                        print(">> ep 68 ")
                        proc_ep_insert(goodscode,'U')
                        print('>> 기존 데이터 네이버 (변경) ep_proc_amazon 테이블 넣기(U) : {}'.format(goodscode))

                    if sel_site == "cn" or sel_site == "red":
                        print(">> confirm_goods : null 변경 / imgb_update_flg : null 변경 ")
                        uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), confirm_goods = null, imgb_update_flg = null, naver_img = '{}' where uid = '{}'".format(goodsImgUrl, goodsImgUrl, uid)
                    else:
                        if str(confirm_goods) == "5":
                            print(">> confirm_goods : 5 -> null / imgb_update_flg : null 변경 ")
                            uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), confirm_goods = null, imgb_update_flg = null, naver_img = '{}' where uid = '{}'".format(goodsImgUrl, goodsImgUrl, uid)
                        else:
                            print(">> imgb_update_flg : null 변경 ")
                            uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), imgb_update_flg = null, naver_img = '{}' where uid = '{}'".format(goodsImgUrl, goodsImgUrl, uid)
                    # print(">> uSql : {}".format(uSql))
                    db_con.execute(uSql)
                    print(">> Imgurl update OK ")
                elif rtn_chk == "1": # img download Err ( img_url_date 만 update )
                    if imgb_update_flg == "1":
                        if img_size_del == '1':
                            if naver_in == "1":
                                # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                                print(">> ep 68 ")
                                proc_ep_insert(goodscode,'D')
                                print('>> 기존 데이터 네이버 (삭제) ep_proc_amazon 테이블 넣기(D) : {}'.format(goodscode))

                        print(">> imgb_update_flg : 1 -> 2 변경 ")
                        uSql = "update t_goods set img_url_date = getdate(), imgb_update_flg = '2' where uid = '{}'".format(uid)
                    else:
                        if naver_in == "1":
                            # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                            print(">> ep 68 ")
                            proc_ep_insert(goodscode,'D')
                            print('>> 기존 데이터 네이버 (삭제) ep_proc_amazon 테이블 넣기(D) : {}'.format(goodscode))

                        print(">> confirm_goods : 2 변경 ")
                        uSql = "update t_goods set img_url_date = getdate(), confirm_goods = 2 where uid = '{}'".format(uid)
                    # print(">> uSql : {}".format(uSql))
                    db_con.execute(uSql)
                    print(">> Err confirm_goods = 2 ")
                    #input(">> Input : ")
                    time.sleep(1)

                i = i + 1

            proc_cnt = proc_cnt + 1

        if errCnt > 50:
            sms_send_kakao_proc_new("img cover error check", input_phone)
            proc_flg = "1"

        print(">> errCnt : {}".format(errCnt))
        print(">> okCnt : {}".format(okCnt))
        db_con.close()

        print('--------------------------------------------------------')
        print(str(datetime.datetime.now()))
        time.sleep(random.uniform(120, 300))

    print(str(datetime.datetime.now()))
    print(" end proc ")
    os._exit(0)