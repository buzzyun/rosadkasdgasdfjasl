import random
import time
import os
import func_1688 as func
import DBmodule_FR
import cate_tmp_api

global errcnt 
db_con = DBmodule_FR.Database('red')

def newCateDep1():
    print('\n [--- newCateDep1 start ---] ')

    result = str(cate_tmp_api.cate_result)    
    row1 = 0
    spList = result.split('</li>')
    for item in spList:
        row1 = row1 + 1
        cate_tmp = func.getparse(item,'<a ','</a>')
        cate_url = func.getparse(cate_tmp,'href="','"')
        cate_name = func.getparse(cate_tmp,'>','')
        cate_name = func.replace_str(cate_name)
        cate_url = "https://open-demo.otcommerce.com" + cate_url.replace('amp;','')
        if cate_name != "":
            print(">> ({}) {} | {}".format(row1, cate_name, cate_url))

            sql = " select * from t_category where amz_cateurl = '{}'".format(cate_url)
            row = db_con.selectone(sql)
            # print('##select one## sql :' +str(sql))
            if not row:
                dic = dict()
                dic['name'] = "'" + cate_name + "'"
                dic['kor_name'] = "'" + cate_name + "'"
                dic['depth'] = 1
                dic['sort'] = row1
                dic['big'] = "'" + cate_name + "'"
                print('New Category')
                dic['amz_cateurl'] = "'" + str(cate_url) + "'"
                db_con.insert('t_category', dic)  # insert
                print('##insert## : t_category : {}'.format(cate_name))
            else:
                print('Category 존재 : {} | {}'.format(cate_name,cate_url))

    return "0"

def getCate(cate_tmp, bcate_code, bcate_name):
    sp_tmp = cate_tmp.split('</li>')
    row2 = 0
    for item in sp_tmp:
        row2 = row2 + 1
        item = func.getparse(item,'<li>','')
        cate_tmp = func.getparse(item,'<a ','</a>')
        cate_url = func.getparse(cate_tmp,'href="','"').replace('amp;','')
        cate_name = func.getparse(cate_tmp,'>','')
        if cate_name.find('<span') > -1:
            cate_name = func.getparse(cate_name,'','<span')
        cate_name = func.replace_str(cate_name)
        if cate_url.find('cid=abb-') > -1:
            cate_id = func.getparse(cate_url,'cid=abb-','&')
        else:
            cate_id = func.getparse(cate_url,'cid=','&')
        cate_url = "https://open-demo.otcommerce.com" + cate_url
        if cate_name != "":
            print(">>(depth2) ({}) {} | {}".format(row2, cate_name, cate_url))

            sql = " select * from t_category where amz_cateurl = '{}'".format(cate_url)
            row = db_con.selectone(sql)
            # print('##select one## sql :' +str(sql))
            if not row:
                print('New Category')
                dic2 = dict()
                dic2['name'] = "'" + cate_name + "'"
                dic2['kor_name'] = "'" + cate_name + "'"
                dic2['depth'] = 2
                dic2['sort'] = row2
                dic2['parent'] = bcate_code
                dic2['bcate'] = bcate_code
                dic2['big'] = "'" + bcate_name + "'"
                dic2['middle'] = "'" + cate_name + "'"
                dic2['cate_code2'] = "'" + cate_id + "'"
                dic2['amz_cateurl'] = "'" + str(cate_url) + "'"
                print('##insert## : t_category : {}'.format(cate_name))
                db_con.insert('t_category', dic2)  # insert
            else:
                print('Category 존재 : {} | {}'.format(cate_name,cate_url))

    return "0"

def getCate_new(cate_tmp, bcate_code, bcate_name, mcate_code, mcate_name, depth):
    sp_tmp = cate_tmp.split('</li>')
    rowCnt = 0
    for item in sp_tmp:
        rowCnt = rowCnt + 1
        item = func.getparse(item,'<li>','')
        if item == "":
            continue
        cate_tmp = func.getparse(item,'<a ','</a>')
        cate_url = func.getparse(cate_tmp,'href="','"').replace('amp;','')
        cate_name = func.getparse(cate_tmp,'>','')
        if cate_name.find('<span') > -1:
            cate_name = func.getparse(cate_name,'','<span')
        cate_name = func.replace_str(cate_name)
        if cate_url.find('cid=abb-') > -1:
            cate_id = func.getparse(cate_url,'cid=abb-','&')
        else:
            cate_id = func.getparse(cate_url,'cid=','&')
        cate_url = "https://open-demo.otcommerce.com" + cate_url
        if cate_name != "":
            print(">>(depth2) ({}) {} | {}".format(rowCnt, cate_name, cate_url))

            sql = " select * from t_category where amz_cateurl = '{}'".format(cate_url)
            row = db_con.selectone(sql)
            # print('##select one## sql :' +str(sql))
            if not row:
                print('New Category')
                if depth == 2:
                    dic2 = dict()
                    dic2['name'] = "'" + cate_name + "'"
                    dic2['kor_name'] = "'" + cate_name + "'"
                    dic2['depth'] = 2
                    dic2['sort'] = rowCnt
                    dic2['parent'] = bcate_code
                    dic2['bcate'] = bcate_code
                    dic2['big'] = "'" + bcate_name + "'"
                    dic2['middle'] = "'" + cate_name + "'"
                    dic2['cate_code2'] = "'" + cate_id + "'"
                    dic2['amz_cateurl'] = "'" + str(cate_url) + "'"
                    print('##insert## (dic2) : t_category : {}'.format(cate_name))
                    db_con.insert('t_category', dic2)  # insert

                elif depth == 3:
                    dic3 = dict()
                    dic3['name'] = "'" + cate_name + "'"
                    dic3['kor_name'] = "'" + cate_name + "'"
                    dic3['depth'] = 3
                    dic3['sort'] = rowCnt
                    dic3['parent'] = mcate_code
                    dic3['bcate'] = bcate_code
                    dic3['mcate'] = mcate_code
                    dic3['big'] = "'" + bcate_name + "'"
                    dic3['middle'] = "'" + mcate_name + "'"
                    dic3['small'] = "'" + cate_name + "'"
                    dic3['cate_code2'] = "'" + cate_id + "'"
                    dic3['amz_cateurl'] = "'" + str(cate_url) + "'"
                    print('##insert## (dic3) : t_category : {}'.format(cate_name))
                    db_con.insert('t_category', dic3)  # insert
            else:
                print('Category 존재 : {} | {}'.format(cate_name,cate_url))

    return "0"

def newCateDep2(browser):

    sql = "select catecode,name,amz_cateurl,parent,bcate,big from t_category where catecode > 3000 and depth = '1' and ishidden='F' and lastcate is null "
    print('\n sql:' + str(sql))
    rows = db_con.select(sql)
    print('\n len(rows) :' + str(len(rows)))
    if not rows:
        print('\n 1 Depth 처리 완료 :' + str(len(rows)))
        return "F"

    for row in rows:
        d1_catecode = row[0]
        d1_catename = row[1]
        d1_amz_cateurl = row[2]

        try:
            browser.get(d1_amz_cateurl)
        except Exception as e:
            print("Exception:{}".format(e))
        else:
            time.sleep(random.uniform(2, 5))
            cate_result = browser.page_source
            print(">> (1depth 파싱) {} | {} ".format(d1_catename, d1_amz_cateurl))
            cate_tmp1 = func.getparse(str(cate_result),'id="search-content_categories-interested_categories"','</ul>')
            if cate_tmp1 != "":
                #getCate(cate_tmp1, d1_catecode, d1_catename)
                getCate_new(cate_tmp1, d1_catecode, d1_catename, '', '', 2)
            cate_tmp2 = func.getparse(str(cate_result),'id="search-content_categories-sub_categories"','</ul>')
            if cate_tmp2 != "":
                #getCate(cate_tmp2, d1_catecode, d1_catename)
                getCate_new(cate_tmp2, d1_catecode, d1_catename, '', '', 2)

    return ""

def newCateDep3(browser):

    sql = "select catecode,name,amz_cateurl,parent,bcate,big from t_category where catecode > 3000 and depth = '2' and ishidden='F' and lastcate is null "
    print('\n sql:' + str(sql))
    rows = db_con.select(sql)
    print('\n len(rows) :' + str(len(rows)))
    if not rows:
        print('\n 2 Depth 처리 완료 :' + str(len(rows)))
        return "F"

    for row in rows:
        d2_catecode = row[0]
        d2_catename = row[1]
        d2_amz_cateurl = row[2]
        d2_parent = row[3]
        d1_bcate = row[4]
        d1_big = row[5]
        print(">> -----------------------------  ")
        try:
            browser.get(d2_amz_cateurl)
        except Exception as e:
            print("Exception:{}".format(e))
        else:
            time.sleep(random.uniform(2, 5))
            cate_result = browser.page_source
            print(">> (2depth 파싱) {} | {} ".format(d2_catename, d2_amz_cateurl))
            cate_tmp = func.getparse(str(cate_result),'<div class="accordion accordion-menu">','class="accordion accordion-menu accordion-filters"')
            if str(cate_tmp).find('class="card-header ') > -1:
                print(">> 하위 카테고리 존재 ")
                cate_tmp1 = func.getparse(str(cate_result),'id="search-content_categories-interested_categories"','</ul>')
                if cate_tmp1 != "":
                    getCate_new(cate_tmp1, d1_bcate, d1_big, d2_catecode, d2_catename, 3)
                cate_tmp2 = func.getparse(str(cate_result),'id="search-content_categories-sub_categories"','</ul>')
                if cate_tmp2 != "":
                    getCate_new(cate_tmp2, d1_bcate, d1_big, d2_catecode, d2_catename, 3)
            else:
                print(">> 마지막 카테고리")
                slq_u = "update t_category set lastcate = '1' where amz_cateurl = '{}'".format(d2_amz_cateurl)
                print(">> slq_u : {}".format(slq_u))
                db_con.execute(slq_u)

    return ""

if __name__ == '__main__':
    print(">> start ")
    errcnt = 0

    # newCateDep1()
    print("-------------------------------")

    time.sleep(1)
    now_url = "https://open-demo.otcommerce.com/ik.php"
    try:
        print(">> connectDriverOld set ")
        browser = func.connectDriverOld(now_url, "N", "N")
    except Exception as e:
        print(">> connectDriverNew set ")
        browser = func.connectDriverNew(now_url, "N", "N")
    time.sleep(3)
    browser.set_window_size(1600, 1000)

    browser.get(now_url)
    time.sleep(4)
    if str(browser.page_source).find('Instance Key') > -1:
        print(">> Login Need ")
        func.demo_login_new(browser)
        time.sleep(2)

    if str(browser.current_url).find('https://open-demo.otcommerce.com/admin/') > -1:
        print(">> Login Ok ")
        func.billChk(browser, db_con) # api 잔액체크
        time.sleep(1)
        browser.get('https://open-demo.otcommerce.com/')
        time.sleep(3)
    else:
        print(">> Login Fail Input Key : ")

    time.sleep(1)
    newCateDep2(browser)

    time.sleep(1)
    newCateDep3(browser)

    db_con.close()
    os._exit(0)
