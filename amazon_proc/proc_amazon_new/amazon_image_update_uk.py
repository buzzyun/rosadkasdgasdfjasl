import datetime
import os
from urllib.request import Request, urlopen
import time
import DBmodule_AM

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

def procChgContentImg(str_target):
    resultContent = str(str_target)

    repImgStr = ""
    if resultContent == "None" or resultContent == "" or resultContent is None:
        pass
    else:
        tmp_target = getparse(str(str_target),'<br><br><Font color=blue><b>','')
        sp_img = str(tmp_target).split('<br><br><Font color=blue><b>')
        print(">> len(sp_img) : {}".format(len(sp_img)))
        if len(sp_img) < 1:
            pass
        else:
            for ea_img in sp_img:
                if ea_img.find('/images/W/MEDIAX_') > -1:
                    pass
                elif ea_img.find('/images/W/') > -1:
                    repImgStr = getparse(ea_img,'/images/W/','/images/I/')
                    resultContent = resultContent.replace('/images/W/'+ str(repImgStr),'')

    return resultContent

def procChgImg(img_target):
    resultImg = img_target

    repImgStr = ""
    if resultImg == "None" or resultImg == "" or resultImg is None:
        pass
    else:
        if resultImg.find('/images/W/MEDIAX_') > -1:
            pass
        elif resultImg.find('/images/W/') > -1:
            repImgStr = getparse(img_target,'/images/W/','/images/I/')
            resultImg = img_target.replace('/images/W/'+ str(repImgStr),'')
            print(">>(after) mainImg : {}".format(resultImg))
        else:
            print(">> mainImg : {}".format(resultImg))

    return resultImg

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    print(">> Start amazon_image_update")
    sel_sql = input("sel sql:")
    if sel_sql == "":
        print(">> No sel_sql ")
    else:
        print(">> sel_sql : {}".format(sel_sql))
        db_am = DBmodule_AM.Database("uk")
        rcnt = 0
        sql = ""
        if sel_sql == "1":
            sql = " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-02-01 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2023-03-15 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/WEBP_%' and naver_in is null "
            sql = sql + " union all "
            sql = sql + " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-02-01 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2023-03-15 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/IMAGERENDERING_%' and naver_in is null "
        elif sel_sql == "2":
            sql = " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-03-15 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2023-03-25 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/WEBP_%' and naver_in is null "
            sql = sql + " union all "
            sql = sql + " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-03-15 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2023-03-25 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/IMAGERENDERING_%' and naver_in is null "
        elif sel_sql == "3":
            sql = " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-03-25 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2024-01-09 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/WEBP_%' and naver_in is null "
            sql = sql + " union all "
            sql = sql + " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-03-25 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2024-01-09 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/IMAGERENDERING_%' and naver_in is null "
        elif sel_sql == "4":
            sql = " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-02-01 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2024-01-09 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/WEBP_%' and naver_in = '1' "
            sql = sql + " union all "
            sql = sql + " select goodscode, naver_img, imgb, naver_in, other_img1, other_img2, other_img3, other_img4, other_img5, c.Content, g.uid from t_goods as g inner join T_GOODS_CONTENT as c on c.uid = g.uid  where stop_update is null and IsDisplay = 'T' and isnull(g.UpdateDate,g.regdate) >= '2023-02-01 00:00:00' and isnull(g.UpdateDate,g.regdate) < '2024-01-09 00:00:00' and imgb like 'https://m.media-amazon.com/images/W/IMAGERENDERING_%' and naver_in = '1' "

        rows = db_am.select(sql)
        print(">> rows : {}".format(len(rows)))
        time.sleep(1)
        for row in rows:
            rcnt = rcnt + 1
            D_goodscode = row[0]
            D_naver_img = row[1]
            D_imgb = row[2]
            D_naver_in = row[3]
            D_other_img1 = row[4]
            D_other_img2 = row[5]
            D_other_img3 = row[6]
            D_other_img4 = row[7]
            D_other_img5 = row[8]
            D_Content = row[9]
            D_uid = row[10]
            print(">>({}) (before)[{}] mainImg : {}".format(rcnt, D_goodscode, D_imgb))
            
            if D_Content.find('m.media-amazon.com/images/W/') > -1:
                print(">> Content Check ")
                content = procChgContentImg(D_Content)

            if D_imgb == "None" or D_imgb == "" or D_imgb is None:
                continue

            imgB = procChgImg(D_imgb)
            if imgB.find('.jpg') > -1 or imgB.find('.JPG') > -1:
                if imgB.find('._') > -1:
                    imgB = getparse(imgB, '', '._') + '.jpg'
                imgB = imgB.replace('.jpg.jpg','.jpg')
            other_img1 = procChgImg(D_other_img1)
            other_img2 = procChgImg(D_other_img2)
            other_img3 = procChgImg(D_other_img3)
            other_img4 = procChgImg(D_other_img4)
            other_img5 = procChgImg(D_other_img5)

            if D_naver_img is None or D_naver_img == "" or D_naver_img == "None":
                print(">> D_naver_img : {}".format(D_naver_img))

            uSql = ""
            if imgB != "":
                uSql = " update t_goods set imgB = '{}', imgM = '{}', imgS = '{}' ".format(imgB, imgB, imgB)
                if D_naver_img:
                    uSql = uSql + ", naver_img = '{}'".format(imgB)
                if other_img1:
                    uSql = uSql + ", other_img1 = '{}'".format(other_img1)
                if other_img2:
                    uSql = uSql + ", other_img2 = '{}'".format(other_img2)
                if other_img3:
                    uSql = uSql + ", other_img3 = '{}'".format(other_img3)
                if other_img4:
                    uSql = uSql + ", other_img4 = '{}'".format(other_img4)
                if other_img5:
                    uSql = uSql + ", other_img5 = '{}'".format(other_img5)
                uSql = uSql + " where goodscode = '{}' ".format(D_goodscode)
                print(">> uSql : {}".format(uSql))
                db_am.execute(uSql)

                if D_Content.find('m.media-amazon.com/images/W/') > -1:
                    uSql2 = " update T_GOODS_CONTENT set content = '{}' where uid = '{}' ".format(content, D_uid)
                    print(">> content Update : {}".format(D_goodscode))
                    db_am.execute(uSql2)

                if str(D_naver_in) == "1": # 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D)
                    proc_ep_insert(D_goodscode,'U')
                    print('>> 기존 데이터 네이버 ep_proc_amazon 테이블 넣기(D) : {}'.format(D_goodscode))

        db_am.close()
    print(str(datetime.datetime.now()))
    print(">> End amazon_image_update")

