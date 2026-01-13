import random
import time
import os
import re
import DBmodule_FR
import category

# Depth 1
def newCateDep1():
    print('\n [--- newCateDep1 start ---] ')

    main_category = category.category_tmp
    sp_bcate = str(main_category).split('<div class="categories-list__wrap">')
    print(">> sp_bcate : {}".format(len(sp_bcate)-1))
    low1 = 0
    for ea_bcate in sp_bcate:
        bcate_name = category.category(ea_bcate, '<h3>','</h3>')
        bcate_name = bcate_name.replace('/',' . ').replace('  ',' ').strip()
        tran_bcate_name = bcate_name
        if bcate_name != "":
            print("\n\n------------------------------------------------------------------------------------------------------------")
            print(">> ( 1 Depth ) ({}) [{}] | {} ".format(low1, bcate_name, tran_bcate_name))
            print("\n\n------------------------------------------------------------------------------------------------------------")

            sql = "select * from t_category_new2 where name = '{0}'".format(bcate_name)
            rs = db_con.selectone(sql)
            print('##select one## sql :' +str(sql))
            if not rs: # rs is None
                dic = dict()
                dic['name'] = "'" + bcate_name + "'"
                dic['kor_name'] = "'" + tran_bcate_name + "'"
                dic['depth'] = 1
                dic['sort'] = low1
                dic['big'] = "'" + tran_bcate_name + "'"
                print('##insert## : t_category_new2')
                db_con.insert('t_category_new2', dic)  # insert
            else:
                print('>> Category 존재 : {}'.format(bcate_name))

        low1 = low1 + 1

    print('>> [--- newCateDep 1 End ---] ')
    return "0"

def newCateDep2(browser, in_dep):
    print('\n [--- newCateDep2 start ---] ')

    sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1 from t_category_new2 where CateCode > 10000 and depth = '1' and ishidden='F' and lastcate is null and cate_kbn is null "
    print('\n sql:' + str(sql))

    rows = db_con.select(sql)
    print('\n len(rows) :' + str(len(rows)))
    if not rows:
        print('\n ' + str(in_dep) + ' Depth 처리 완료 :' + str(len(rows)))
        return "F"

    cnt = 0
    low = 0
    oldCnt = 0
    newCnt = 0
    while low < len(rows):

        cnt = cnt + 1
        bcate_catecode = rows[low][0]
        bcate_catename = rows[low][1]
        bcate_catekor_name = rows[low][2]
        bcate_cateurl = rows[low][3]
        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(bcate_catecode) + ' | ' + str(bcate_catename) + ' | ' + str(bcate_catekor_name) )
        print('\n ' + str(bcate_cateurl))

        try:
            browser.get(bcate_cateurl)
        except Exception as e:
            print('>> err : {}'.format(e))

        time.sleep(random.uniform(5,7))
        result = browser.page_source
        if result.find('id="filter-price"') == "":
            time.sleep(random.uniform(5,7))
            result = browser.page_source

        low_2 = 0
        if result.find('suitable_category') == -1:
            print(">> 마지막 카테고리 ")
            sql_u = " update t_category_new2 set lastcate = '1', cate_kbn = '1' where catecode = '{}'".format(bcate_catecode)
            print('bcate ({}) proc end (sql_u) : {}'.format(bcate_catecode, sql_u))
            db_con.execute(sql_u)
        else:
            category_tmp = category.getparse(str(result),'id="search-content_categories-interested_categories"','')
            category_tmp = category.getparse(str(category_tmp),'<ul>','</ul>')
            sp_cate = category_tmp.split('</li>')

            print('category_tmp : {}'.format(type))
            print(">> len(sp_cate) : {}".format(len(sp_cate)))

            print(">> sp_mcate ")
            print(">> ===================================================================================================== ")
            for ea_mcate in sp_cate:
                mcate_tmp = ea_mcate
                mcate_tmp = category.getparse(str(mcate_tmp),'<a ','</a>')
                mcate_url = category.getparse(str(mcate_tmp),'href="','"').replace('amp;','').strip()
                mcate_name = category.getparse(str(mcate_tmp),'">','<')
                mcate_name = mcate_name.replace(', ',' & ').replace('  ',' ').strip()
                mcate_url = mcate_url.replace('&amp;','&').strip()
                mcate_url = "https://open-demo.otcommerce.com" + mcate_url
                cate_code2 = category.getparse(str(mcate_url),'cid=','&').strip()

                sqlg = "select catecode, name, amz_cateurl from t_category where amz_cateurl like '%" +str(cate_code2)+ "%' "
                print('\n sqlg:' + str(sqlg))
                row = db_con.selectone(sqlg)
                if row:
                    old_catecode = row[0]
                    old_catename = row[1]
                    old_cateurl = row[2]
                    print(">> {} | {} | {} ".format(old_catecode, old_catename, old_cateurl))
                    print(">> 기존 category 테이블 존재 : {} --> {}".format(mcate_name, old_catename))
                    oldCnt = oldCnt + 1
                else:
                    if mcate_name != "" and mcate_url != "":
                        low_2 = low_2 + 1
                        newCnt = newCnt + 1
                        print(">> ( 2 Depth ) [{}] {} | {} | {}".format(low_2, mcate_name, cate_code2, mcate_url))
                        print(">>>>>>>>>>>>>> {} >> {} ".format(bcate_catename, mcate_name))
                        dic2 = dict()
                        dic2['name'] = "'" + mcate_name + "'"
                        dic2['kor_name'] = "'" + mcate_name + "'"
                        dic2['depth'] = 2
                        dic2['sort'] = low_2
                        dic2['parent'] = bcate_catecode
                        dic2['bcate'] = bcate_catecode
                        dic2['big'] = "'" + bcate_catekor_name + "'"
                        dic2['middle'] = "'" + mcate_name + "'"
                        dic2['cate_code2'] = "'" + str(cate_code2) + "'"
                        dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                        dic2['lastcate'] = "'0'"
                        
                        sql2 = "select catecode from t_category_new2 where amz_cateurl = '" + str(mcate_url) + "'"
                        row2 = db_con.selectone(sql2)
                        if row2:
                            print(">> 기존 존재 (Skip) : {} | {} >> {}".format(bcate_catecode, bcate_catekor_name, mcate_name))
                        else:
                            print('New 2 Category : {}'.format(mcate_name))
                            db_con.insert('t_category_new2', dic2)  # insert
                            print('##insert## : t_category_new2')
                    else:
                        print(">> Check Please ( 2 Depth ) [{}] {} | {} | {}".format(low_2, mcate_name, cate_code2, mcate_url))
                        print(">>>>>>>>>>>>>> {} >> {} ".format(bcate_catename, mcate_name))

        low = low + 1

        sql_u = " update t_category_new2 set cate_kbn = '1' where catecode = '{}'".format(bcate_catecode)
        print('bcate ({}) proc end (sql_u) : {}'.format(bcate_catecode, sql_u))
        db_con.execute(sql_u)

    print('>> [--- newCateDep2 end ---] ')
    return "0"

if __name__ == '__main__':
    print(">> start ")
    errcnt = 0
    set_browser = "chrome"
    now_url = "https://open-demo.otcommerce.com/?q=allcats"
    db_con = DBmodule_FR.Database('cn')

    main_url = "https://open-demo.otcommerce.com/?q=allcats"
    try:
        browser = category.connectDriverNew(main_url,"", "N")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = category.connectDriverOld(main_url,"", "N")
        print(">> connectDriverOld set OK ")

    browser.get(now_url)
    browser.set_window_size(1200, 800)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(2)
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logo-link')))
    time.sleep(random.uniform(2,4))
    input(">> login :")

    # depth 1
    ## newCateDep1()

    # depth 2
    newCateDep2(browser, "1")

    db_con.close()
    os._exit(0)