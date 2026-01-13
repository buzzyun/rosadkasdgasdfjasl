import urllib.request
import os
# import psutil
from stem import Signal
from stem.control import Controller

# def version_check(cursor,ver):

#     print("version:" + ver)
#     file_path = r"c:/project/"
#     file_name = "new_shein.exe"
#     sql = "select version,url from python_version_manage where name = 'list'"
#     rows = cursor.selectone(sql)
#     version = rows[0]
#     version_url = rows[1]
#     if ver != version:
#         urllib.request.urlretrieve(version_url, file_path + file_name)
#         # os.system("taskkill /f /im geckodriver.exe")
#         return False
#     else:
#         return True

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

def reConnection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

# def getService(name):
#     service = None
#     try:
#         service = psutil.win_service_get(name)
#         service = service.as_dict()
#     except Exception as ex:
#         print(str(ex))
    
#     return service

def newlist(cursor,ip):

    sql = "select top 1 * from update_list where proc_ip = '{0}'".format(ip)
    rows = cursor.selectone(sql)
    if not rows:
        page = 1
        sql = "SELECT top 1 a.amz_cateurl,a.catecode,a.cate_code2, a.big, a.middle, a.small, a.little, a.last, a.depth FROM T_CATEGORY a left outer join update_list b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and a.site_chk is null and b.catecode is null order by up_date asc"
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        cate_code2 = row[2]
        big = row[3]
        middle = row[4]
        small = row[5]
        little = row[6]
        last = row[7]
        depth = row[8]
        sql = "update T_CATEGORY set up_date = GETDATE() where catecode='{0}'".format(cateidx)       
        cursor.execute(sql)

        sql = "insert into update_list (catecode,now_page,proc_ip,amz_cateurl,cate_code2,regdate, big, middle, small, little, last, depth) values ('{0}','{1}','{2}','{3}','{4}',getdate(),'{5}','{6}','{7}','{8}','{9}',{10})".format(cateidx, page, ip,amzurl,cate_code2,big,middle,small,little,last,depth)
        try:
            cursor.execute(sql)
        except Exception as e:
            os._exit(1)
    else:
        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        rows = cursor.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            cursor.execute(sql)

        sql = "select c.amz_cateurl,u.catecode,u.now_page,u.cate_code2, u.big, u.middle, u.small, u.little, u.last, u.depth from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(ip)
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        cate_code2 = row[3]
        big = row[4]
        middle = row[5]
        small = row[6]
        little = row[7]
        last = row[8]
        depth = row[9]

    result = {"catecode": cateidx, "page": int(page),"url":amzurl,"cate_code2":cate_code2,"big":big,"middle":middle,"small":small,"little":little,"last":last,"depth":depth}
    return result

def newlist2(cursor,ip):

    sql = "select top 1 * from update_list2 where proc_ip = '{0}'".format(ip)
    rows = cursor.selectone(sql)
    if not rows:
        sql = "select catecode from update_list2"
        cateList = []
        where = ""
        row = cursor.select(sql)
        for rs in row:
            cateList.append(rs[0])
        if len(cateList) > 0:            
            cateList = str(cateList).replace("[", "").replace("]", "").replace("'", "")
            # where = " where catecode not in ({})".format(cateList)
            where = " and catecode not in ({})".format(cateList)
        page = 1        

        # sql = "select top 1 catecode from t_getasin{} group by catecode order by count(catecode)".format(where)
        sql = "select * from T_CATEGORY where CateCode not in (select CateCode from t_goods as g join T_GOODS_CATEGORY as c on g.uid=c.GoodsUid group by CateCode) and CateCode in (select catecode from t_getasin group by catecode){} and IsHidden='F' and lastcate=1".format(where)
        print(sql)
        row = cursor.selectone(sql)
        cateidx = row[0]

        sql = "insert into update_list2 (catecode,now_page,proc_ip,regdate) values ('{0}','{1}','{2}',getdate())".format(cateidx, page, ip)
        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            os._exit(1)
    else:
        sql = "select count(*) from update_list2 where proc_ip = '{0}'".format(ip)
        rows = cursor.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list2 where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list2 where proc_ip='{0}' order by regdate desc)".format(ip)
            cursor.execute(sql)
            cursor.commit()

        sql = "select u.catecode,u.now_page from update_list2 as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(ip)
        row = cursor.selectone(sql)
        cateidx = row[0]
        page = row[1]

    result = {"catecode": cateidx, "page": int(page)}
    return result

def newlist3(cursor,ip):

    sql = "select top 1 * from update_list3 where proc_ip = '{0}'".format(ip)
    rows = cursor.selectone(sql)
    if not rows:
        sql = "select guid from update_list3"
        cateList = []
        where = ""
        row = cursor.select(sql)
        for rs in row:
            cateList.append(rs[0])
        if len(cateList) > 0:            
            cateList = str(cateList).replace("[", "").replace("]", "").replace("'", "")
            where = " where g.uid not in ({})".format(cateList)     
        sql = "select top 1 g.Uid, g.ali_no, c.CateCode, isnull(g.DE_title,''), tc.cate_code2 from T_GOODS as g join T_GOODS_CATEGORY as c on g.Uid=c.GoodsUid join T_CATEGORY as tc on tc.CateCode=c.CateCode{} order by g.UpdateDate".format(where)
        print(sql)
        row = cursor.selectone(sql)
        guid = row[0]
        asin = row[1]        
        cateidx = row[2]
        de_title = row[3]
        catecode2 = row[4]
        
        sql = "insert into update_list3 (guid,asin,catecode,proc_ip,catecode2) values ({0},'{1}',{2},'{3}','{}')".format(guid, asin, cateidx,ip,catecode2)
        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            os._exit(1)
    else:
        sql = "select guid from update_list3 where proc_ip <> '{}'".format(ip)
        cateList = []
        where = ""
        row = cursor.select(sql)
        for rs in row:
            cateList.append(rs[0])
        if len(cateList) > 0:            
            cateList = str(cateList).replace("[", "").replace("]", "").replace("'", "")
            where = " where g.uid not in ({})".format(cateList)       
        sql = "select top 1 g.Uid, g.ali_no, c.CateCode, isnull(g.DE_title,''), tc.cate_code2 from T_GOODS as g join T_GOODS_CATEGORY as c on g.Uid=c.GoodsUid join T_CATEGORY as tc on tc.CateCode=c.CateCode{} order by g.UpdateDate".format(where)
        row = cursor.selectone(sql)
        guid = row[0]
        asin = row[1]        
        cateidx = row[2]
        de_title = row[3]
        catecode2 = row[4]
        
        sql = "update update_list3 set guid={}, asin='{}', catecode='{}', catecode2='{}' where proc_ip='{}'".format(guid, asin, cateidx,catecode2,ip)
        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            os._exit(1)
    
    result = {"guid":guid,"asin":asin,"catecode": cateidx,"de_title": de_title, "catecode2":catecode2}
    return result

def newlist_zaful(cursor,ip):

    sql = "select top 1 * from update_list_zaful where proc_ip = '{0}'".format(ip)
    rows = cursor.selectone(sql)
    if not rows:
        page = 1
        sql = "SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list_zaful b on(a.CateCode=b.catecode) where IsHidden='F' and lastcate=1 and b.catecode is null and site_chk=1 order by up_date asc"
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        sql = "update T_CATEGORY set up_date = GETDATE() where catecode='{0}'".format(cateidx)       
        cursor.execute(sql)
        cursor.commit()
        
        sql = "insert into update_list_zaful (catecode,now_page,proc_ip,amz_cateurl,regdate) values ('{0}','{1}','{2}','{3}',getdate())".format(cateidx, page, ip,amzurl)

        cursor.execute(sql)
        cursor.commit()

    else:
        sql = "select count(*) from update_list_zaful where proc_ip = '{0}'".format(ip)
        rows = cursor.selectone(sql)
        ip_count = rows[0]

        if ip_count > 1:
            sql = "delete from update_list_zaful where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list_zaful where proc_ip='{0}' order by regdate desc)".format(ip)
            cursor.execute(sql)

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list_zaful as u inner join T_CATEGORY as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(ip)
        row = cursor.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
    
    result = {"catecode": cateidx, "page": int(page),"url":amzurl}
    return result