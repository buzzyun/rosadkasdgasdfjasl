import os
import aiohttp
import asyncio
import aiofiles
# pip install aiofiles==0.7.0
import urllib.request
#import Image
from PIL import Image
import time,random
import os, socket, sys
import requests
import json
import datetime
import DBmodule_FR
global errCnt 
global okCnt 
global default_folder
global db_con

# 68번 ep_proc_amazon 테이블 Insert
async def proc_ep_insert(goodscode, mode):
    if str(goodscode) == '' or goodscode is None:
        print(">> 68번 ep_proc_amazon 테이블 (In) goodscode 없음 (SKIP)")
        return "1"

    print(">> 68번 ep_proc_amazon 테이블 (In) : {} | mode ({}) ".format(goodscode, mode))
    db_ep = DBmodule_FR.Database('naver_ep2')
    sql = "select goodscode from ep_proc_amazon where goodscode = '{}'".format(goodscode)
    print(">> sql : {}".format(sql))
    pRow = db_ep.selectone(sql)
    if not pRow:
        iSql = "insert ep_proc_amazon (goodscode, mode, regdate) values ('{}','{}', getdate())".format(goodscode, mode)
        print(">> iSql : {}".format(iSql))
        db_ep.execute(iSql)
    db_ep.close()

    return "0"

async def fetch(db_con, guid):

    input_site = "red"
    print("\n>>[{}]------------------------------------------------".format(guid))
    sql = " select uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where uid = '{}'".format(guid)
    row = db_con.selectone(sql)
    if row:
        uid = row[0]
        goodscode = row[1]
        imgB = row[2]
        cate_idx = row[3]
        regdate = row[4]
        updatedate = row[5]
        imgb_update_flg = row[6]
        naver_in = row[7]
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
            print(">> goodscode is null : {}".format(uid))
        else:
            goodsImgUrl = "http://" +str(input_site)+ ".freeship.co.kr/Goodsimage/Big/" + str(cate_idx) + "/" + savefilename
            #print(">> goodsImgUrl : {}".format(goodsImgUrl))

            if input_site == "cn":
                if imgUrl.find("https:") == -1:
                    imgUrl = "https:" + imgUrl

            ## img down Start
            savelocation = default_folder + str(cate_idx) # 내컴퓨터의 저장 위치
            savefile = savelocation + "/" + savefilename
            print(">> [{}] {} (update:{} | flg:{}) (naver_in :{}) | {} | {}".format(goodscode, regdate, updatedate, imgb_update_flg, naver_in, cate_idx, imgUrl))

            try:
                os.mkdir(savelocation)
            except FileExistsError:
                pass

            try:
                # time check
                start = time.time()
                # 이미지 요청 및 다운로드
                if input_site == "cn":
                    os.system("curl " + imgUrl + " > "+ str(savefile))
                elif input_site == "shop":
                    urllib.request.urlretrieve(imgUrl, savefile)
                elif input_site == "red":
                    imgChkUrl = str(imgB)[-5:].lower()
                    if imgChkUrl.find('.jpg') > -1 or imgChkUrl.find('.jpeg') > -1 or imgChkUrl.find('.png') > -1:
                        print(">> imgChkUrl (뒷5자리) : {}".format(imgChkUrl))
                        os.system("curl " + imgUrl + " > "+ str(savefile))
                    else:
                        urllib.request.urlretrieve(imgUrl, savefile)
                else:
                    urllib.request.urlretrieve(imgUrl, savefile)
                time.sleep(random.uniform(0.5,1))
            except Exception as e:
                print('>>\n error msg : {}'.format(e))
                print('>> imgB : {}'.format(imgB))
                errCnt = errCnt + 1
                rtn_chk = '1'
            else:
                tf = os.path.join(savelocation + "/", savefilename)
                # print(tf)

                try:
                    # 저장 된 이미지 확인
                    img = Image.open(tf)
                    imgx, imgy = img.size
                    print(">> img Size : {} | {} ".format(imgx, imgy))

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
                    rtn_chk = '1'

                else:
                    if imgx < 500 or imgy < 500:
                        print(">> (Skip) imgx {} | imgy {} size : {}".format(imgx, imgy, goodscode))
                        rtn_chk = '1'
                        img_size_del = '1'
                    else:
                        rtn_chk = '0'
                        print('>> 완료 : {} -> {}  ({})'.format(tf_format_ori, extension, goodsImgUrl))
                    img.close 

                # if rtn_chk == "0": # img download Ok  ( img_url, img_url_date update )
                #     if imgb_update_flg == "1" and naver_in == "1":
                #         # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(U)
                #         print(">> ep 68 ")
                #         await proc_ep_insert(goodscode,'U')
                #         print('>> 기존 데이터 네이버 (변경) ep_proc_amazon 테이블 넣기(U) : {}'.format(goodscode))

                #     if input_site == "cn" or input_site == "red":
                #         print(">> confirm_goods : null 변경 / imgb_update_flg : null 변경 ")
                #         uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), confirm_goods = null, imgb_update_flg = null where uid = '{}'".format(goodsImgUrl, uid)
                #     else:
                #         if str(confirm_goods) == "5":
                #             print(">> confirm_goods : 5 -> null / imgb_update_flg : null 변경 ")
                #             uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), confirm_goods = null, imgb_update_flg = null where uid = '{}'".format(goodsImgUrl, uid)
                #         else:
                #             print(">> imgb_update_flg : null 변경 ")
                #             uSql = "update t_goods set img_url = '{}', img_url_date = getdate(), imgb_update_flg = null where uid = '{}'".format(goodsImgUrl, uid)
                #     # print(">> uSql : {}".format(uSql))
                #     db_con.execute(uSql)
                # elif rtn_chk == "1": # img download Err ( img_url_date 만 update )
                #     if imgb_update_flg == "1":
                #         if img_size_del == '1':
                #             if naver_in == "1":
                #                 # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                #                 print(">> ep 68 ")
                #                 await proc_ep_insert(goodscode,'D')
                #                 print('>> 기존 데이터 네이버 (삭제) ep_proc_amazon 테이블 넣기(D) : {}'.format(goodscode))

                #         print(">> imgb_update_flg : 1 -> 2 변경 ")
                #         uSql = "update t_goods set img_url_date = getdate(), imgb_update_flg = '2' where uid = '{}'".format(uid)
                #     else:
                #         if naver_in == "1":
                #             # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                #             print(">> ep 68 ")
                #             await proc_ep_insert(goodscode,'D')
                #             print('>> 기존 데이터 네이버 (삭제) ep_proc_amazon 테이블 넣기(D) : {}'.format(goodscode))

                #         print(">> confirm_goods : 2 변경 ")
                #         uSql = "update t_goods set img_url_date = getdate(), confirm_goods = 2 where uid = '{}'".format(uid)
                #     # print(">> uSql : {}".format(uSql))
                #     db_con.execute(uSql)
                #     time.sleep(1)


async def main(db_con):
    proc_list = []
    input_site = "red"
    sql = " select top 25 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where RegDate >= '2023-08-01 00:00:00' and RegDate < DATEADD(HH, -1, getdate()) and img_url is null and goodscode is not null and confirm_goods = 1 and imgb_update_flg is null "
    sql = sql + " union all "
    sql = sql + " select top 25 uid, isnull(goodscode,''), imgB, cate_idx, regdate, updatedate, isnull(imgb_update_flg,''), isnull(naver_in,0), isnull(confirm_goods,'') from t_goods where UpdateDate > '2023-08-01 00:00:00' and goodscode is not null and imgb_update_flg = '1' and confirm_goods is null "
    rowMain = db_con.select(sql)
    if not rowMain:
        print(">> 작업 대상이 없습니다 : {} ".format(datetime.datetime.now()))
        return "1"

    rows = db_con.select(sql)
    i = 0
    for row in rows:
        guid = row[0]
        proc_list.append(guid)

    await asyncio.gather(*[fetch(db_con, guid) for guid in proc_list])


if __name__ == "__main__":

    print(str(datetime.datetime.now()))
    print(" start proc ({}) : {}".format("red", datetime.datetime.now()))
    current_folder = os.getcwd()
    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() == "222.104.189.18":
        default_folder = "E:/amazon_proc/Goodsimage/Big/"
    currtime = str(datetime.datetime.now()).replace(' ','_').replace(':','_')[:19]
    print(" default_folder : {}".format(default_folder))
    print(" currtime : {}".format(currtime))
    db_con = DBmodule_FR.Database("red")

    asyncio.run(main(db_con))

    db_con.close()