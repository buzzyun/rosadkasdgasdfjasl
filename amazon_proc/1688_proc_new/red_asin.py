import os
os.system('pip install --upgrade selenium')
import time
import os
import datetime
import random
import socket
import urllib
import asin_func
import DBmodule_FR

ver = "01.11"

def procLogSet(in_DB, in_proc_no, in_proc_memo, ip):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

def newlist(db_con, endpage, ip):

    rtnStr = ""
    cateidx = ""
    amzurl = ""
    page = 1

    print('>> -- newlist() -- work ip : '+str(ip))

    sql = "select * from update_list where proc_ip = '{0}'".format(ip)
    rows = db_con.select(sql)

    if not rows:
        print('>> update_list 테이블에 proc_ip 없음 : ' +str(ip))
        page = 1
        sql = " SELECT top 1 a.amz_cateurl,a.catecode FROM T_CATEGORY a left outer join update_list b on (a.CateCode=b.catecode) where IsHidden='F' and lastcate='1' and a.catecode > 3000 and b.catecode is null order by up_date asc "

        if page > endpage:
            page = endpage

        row = db_con.selectone(sql)
        if not row:
            print('>> work ip 데이터 등록 ')
        else:
            amzurl = row[0]
            cateidx = row[1]
            print('>> [new] cateidx : '+str(cateidx))

            dic_up = dict()
            dic_up['up_date'] = "getdate()"
            dic_up['list_in'] = "1"
            sql_where = " catecode='" + str(cateidx) + "'"
            db_con.update('T_CATEGORY', dic_up, sql_where)  # update
            print('>> ##update## : T_CATEGORY (up_date 변경 및 list_in = 1 처리)')

            dic_in = dict()
            dic_in['catecode'] = cateidx
            dic_in['now_page'] = page
            dic_in['amz_cateurl'] = "'" + str(amzurl) + "'"
            dic_in['proc_ip'] = "'" + str(ip) + "'"

            db_con.insert('update_list', dic_in)  # insert
            print('>> ##insert## : update_list ( catecode | now_page | proc_ip )')

    else:
        print('>> update_list 테이블에 proc_ip 있음 : ' +str(ip))

        sql = "select count(*) from update_list where proc_ip = '{0}'".format(ip)
        row = db_con.selectone(sql)
        ip_count = row[0]
        print('ip_count :'+str(ip_count))

        if ip_count > 1:
            sql_where = "where proc_ip = '{0}' and catecode not in (select top 1 catecode from update_list where proc_ip='{0}' order by regdate desc)".format(ip)
            db_con.delete('update_list',sql_where)
            print('>> ##delete## : update_list')

        sql = "select c.amz_cateurl,u.catecode,u.now_page from update_list as u inner join t_category as c on u.catecode = c.catecode where u.proc_ip = '{0}'".format(
            ip)
        row = db_con.selectone(sql)
        amzurl = row[0]
        cateidx = row[1]
        page = row[2]
        if page > endpage:
            page = endpage

    print('>> cateidx : '+str(cateidx)+ ' | page : ' + str(page)+' | amzurl : '+str(amzurl))
    rtnStr = str(cateidx) + "@" + str(page)

    return rtnStr

def version_check2(db_con, file_name, ver, list_name):

    print("version:" + ver)
    file_path = r"c:/project/"

    sql = "select version,url from python_version_manage where name = '{}'".format(list_name)
    print(">> sql:" + sql)
    row = db_con.selectone(sql)
    if row:
        version = row[0]
        version_url = row[1]
        if ver != version:
            urllib.request.urlretrieve(version_url, file_path + file_name)
            print(">> New version Download :" + str(version_url) + " | "+ str(file_path + file_name))
            time.sleep(30)
            print(">> time.sleep(30)")
            print(">> New version update exit")

            db_con.close()
            time.sleep(2)
            os._exit(1)

def version_check(db_con, in_drive, file_name, ver, list_name):

    print("version:" + ver)
    file_path = r"c:/project/"

    sql = "select version,url from python_version_manage where name = '{}'".format(list_name)
    print(">> sql:" + sql)
    rows = db_con.selectone(sql)
    version = rows[0]
    version_url = rows[1]
    if ver != version:
        urllib.request.urlretrieve(version_url, file_path + file_name)
        print(">> New version Download :" + str(version_url) + " | "+ str(file_path + file_name))

        time.sleep(30)
        print(">> time.sleep(30)")
        print(">> New version update exit")

        db_con.close()
        in_drive.quit()
        time.sleep(2)
        os._exit(1)

def procLastpage(in_cateidx, in_flg, db_con):

    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_page":
        print('>> 마지막 page')
        sql = "update T_CATEGORY set up_date = GETDATE(),list_in=2 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_connect":
        sql = "update T_CATEGORY set up_date = '2020-11-01 00:00:00' where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    elif in_flg == "no_data":
        sql = "update T_CATEGORY set up_date = GETDATE()-1 where catecode='" + str(in_cateidx) + "'"
        db_con.execute(sql)

    print('>> sql : ' + str(sql))
    if in_flg == "end" or in_flg == "no_cateidx" or in_flg == "no_data" or in_flg == "no_page":
        sql = "delete from update_list where catecode ='" + str(in_cateidx) + "'"
        db_con.execute(sql)
        print('>> sql : ' + str(sql))

    return "0"


def procDbSet(in_asin, in_cateidx, in_price, in_istmall, in_sold_cnt, in_title, in_range, db_con):

    sql = "select * from T_Category_BestAsin where asin = '{0}'".format(in_asin)
    rs = db_con.selectone(sql)
    # print('##select one## sql :' + str(sql))

    if not rs:  # rs is None
        print('>> T_Category_BestAsin (New)')
        sql = "insert into T_Category_BestAsin (asin, cate_idx, price, isTmall, sold_cnt, title, range) values ('" + str(in_asin) + "','" + str(in_cateidx) + "'," + str(in_price) + ",'" + str(in_istmall) + "', " + str(in_sold_cnt) + ",'" + str(in_title) + "' ," + str(in_range) + " )"
        #print('>> sql :'+str(sql))
        db_con.execute(sql)
    else:
        print('>> T_Category_BestAsin (Update)')
        sql = "update T_Category_BestAsin set up_date = GETDATE(), price = " + str(in_price) + ", cate_idx = '" + str(in_cateidx) + "', title = '" + str(in_title) + "', isTmall = '" + str(in_istmall) + "', sold_cnt = " + str(in_sold_cnt) + ", range = " +str(in_range)+ " where asin='" + str(in_asin) + "'"
        #print('>> sql :'+str(sql))
        db_con.execute(sql)

    return "0"


def checkDelAsin(db_con, asin):
    print(">> asin Check ")
    rtnCode = ""
    sql = " select asin, code from T_Category_BestAsin_del where code in ( 'S01','S02','D49', 'D03', 'D47', 'D09', 'D12' ) and asin = '{}'".format(asin)
    rs = db_con.selectone(sql)
    if rs:
        code = rs[1]
        print(">> Skip Aasin : {} : code : {}".format(asin, code))
        rtnCode = str(code)
    return rtnCode

def fun_chart(db_con, browser, CateCode, endpage, currIp, file_name, ver, errCnt, sort_type, min_qty_order):

    itemList = []
    print('>> fun_chart() ')
    if str(currIp).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(currIp))
    else:
        version_check(db_con, browser, file_name, ver, "list_api") # version 체크

    sp_tmp = str(CateCode).split('@')
    cateidx = sp_tmp[0]
    page = sp_tmp[1]
    if str(page) == "":
        page = "1"
    pglow = int(page)
    sql = "select amz_cateurl from t_category where catecode = '{0}'".format(cateidx)
    rs = db_con.selectone(sql)
    print('>> ## ' + str(pglow) + ' ####(fun_chart) select one## sql :' + str(sql))
    if not rs:
        print(">> 해당 카테고리코드 없음 : " + str(cateidx))
        procLastpage(cateidx, "no_cateidx", db_con)
        return "1"

    amzurl = rs[0]
    print('>> [' + str(cateidx) + '] page: ' + str(page) + ' | ' + str(amzurl) )

    idx_from = 0
    goodsCnt = 0
    while pglow <= endpage:

        time.sleep(1)
        print('>> time.sleep(1)')
        print('>> pglow :' + str(pglow))

        amzurl = amzurl + "&cost%5Bfrom%5D=&cost%5Bto%5D=800&rating%5Bfrom%5D=&rating%5Bto%5D=&features%5BIsStock%5D=true&layout=list"
        if str(page) == "1":
            now_url = amzurl
        else:
            now_url = amzurl + "&from=" + str(idx_from)
        print('>> [' + str(cateidx) + '] page: ' + str(page) )
        print('>> now_url : {}'.format(now_url) )

        try:
            browser.get(now_url)
        except Exception as e:
            print('>> browser.get Exception (1)')
        else:
            time.sleep(random.uniform(6,8))

        if str(browser.page_source).find('products_not_found') > -1:
            print(">> products_not_found (end) : " + str(cateidx))
            procLastpage(cateidx, "end", db_con)
            break

        result = str(browser.page_source)
        if str(result).find('<div class="listing-wrap') == -1:
            time.sleep(4)
            result = str(browser.page_source)

        if str(result).find('<div class="listing-wrap') == -1:
            print(">> Check Please page_source ")
            print(">> data 없음 (end) : " + str(cateidx))
            procLastpage(cateidx, "end", db_con)
            break

        result_source = asin_func.getparse(result,'<div class="listing-wrap','</nav>')
        result_nav = asin_func.getparse(str(result_source),'<nav>','')
        result_nav_tmp = asin_func.getparse(str(result_nav),'class="page-item active">','</a>')
        curr_page = asin_func.getparse(str(result_nav_tmp),'search-click page-link">','').strip()
        curr_from = asin_func.getparse(str(result_nav_tmp),'from=','"').strip()
        print(">> curr_page : {} | curr_from : {}".format(curr_page, curr_from))
        if curr_from == "":
            idx_from = 40
        else:
            idx_from = int(curr_from) + 40

        result_list = asin_func.getparse(str(result_source),'','<nav>')
        result_list_sp = result_list.split('class="product-item ')
        if len(result_list_sp) == 0:
            print(">> Item 0 ")
            print('>> no_data page'+str(endpage))
            procLastpage(cateidx, "no_data", db_con)
            break

        pageInCnt = 0
        for ea_item in result_list_sp:
            rtnCode = ""
            asin = asin_func.getparse(str(ea_item),'data-product-id="','"').replace('abb-','').strip()
            if asin != "":
                goodsCnt = goodsCnt + 1
                itemList.append(asin)
                title = asin_func.getparse(str(ea_item),'class="item-product__title','</a>')
                title = asin_func.getparse(title,'">','')

                rangeTmp = ""
                range = 0
                if ea_item.find('class="list_quantity-ranges"') > -1:
                    rangeTmp = asin_func.getparse(str(ea_item),'class="list_quantity-ranges"','</div>')
                    rangeTmp = asin_func.getparse(rangeTmp,'<td class="range">','</td>')
                    if rangeTmp.find('-') > -1:
                        rangeTmp = asin_func.getparse(rangeTmp,'','-')
                    if rangeTmp.find('&nbsp;') > -1:
                        rangeTmp = asin_func.getparse(rangeTmp,'','&nbsp;')

                if rangeTmp != "":
                    print(">> rangeTmp : {}".format(rangeTmp))
                    if rangeTmp.isdigit() == True:
                        range = int(rangeTmp)
                        if range > int(min_qty_order):
                            print(">> 최소수량 {}개이상 skip : {}".format(min_qty_order, range))
                            rtnCode = "D01"

                price = asin_func.getparse(str(ea_item),'itemprop="price"','>')
                price = asin_func.getparse(str(price),'content="','"')

                sold_cnt = asin_func.getparse(str(ea_item),'class="sold-block">','</span>')
                sold_cnt = asin_func.getparse(str(sold_cnt),'sold:','').strip()
                if sold_cnt == "":
                    sold_cnt = 0
                else:
                    sold_cnt = int(sold_cnt.replace(',',''))
                istmall = "F"
                title = asin_func.replaceStr(title)
                title = title[:100]
                if str(ea_item).find('class="item-product__rubric-tmall"') > -1:
                    istmall = "T"
                elif str(ea_item).find('tmall') > -1:
                    istmall = "T"

                if asin_func.findChinese(title):
                    print('>> findChinese title (Skip) : {}'.format(title))
                    rtnCode = "D02"

                if rtnCode == "":
                    asinSql = " select ali_no from t_goods where ali_no = '{}'".format(asin)
                    asinrow = db_con.selectone(asinSql)
                    if asinrow:
                        print(">> [DB 존재 Skip] ({}) [ {} ] ( {} )  ".format(goodsCnt, asin, price))
                    else:
                        procDbSet(asin, cateidx, price, istmall, sold_cnt, title, range, db_con) # DB 입력
                        print(">>({}) [ {} ] ( {} ) | {} | {} | {} ".format(goodsCnt, asin, price, istmall, sold_cnt, title[:20]))
                        pageInCnt = pageInCnt + 1
                else:
                    print(">>Skip : ({}) [ {} ] ( {} ) | {} | {} | {} | {} ".format(goodsCnt, asin, price, istmall, sold_cnt, title[:20], rtnCode))

        dupCount = asin_func.has_duplicates(itemList)
        print(">> 중복 아이템수 : {}".format(dupCount))
        print(">> pageInCnt : {}".format(pageInCnt))

        #print('>> page : '+str(page))
        page = int(page)
        if int(page) >= int(endpage):
            print('>> 마지막 page'+str(endpage))
            procLastpage(cateidx, "end", db_con)
            break
        else:
            page += 1
            if page > int(endpage):
                page = int(endpage)
            print('>> Next page : '+str(page))

            sql = "update update_list set now_page = '{0}' where catecode = '{1}'".format(page, cateidx)
            db_con.execute(sql)
            print('>> sql : ' + str(sql))

        time.sleep(2)
        pglow = pglow + 1

    print(">> goodsCnt : {}".format(goodsCnt))
    return "0"

def billChk(browser, db_con):
    billChk = "https://open-demo.otcommerce.com/admin/?cmd=Reports&do=billing"
    browser.get(billChk)
    print(">> url : {}".format(billChk))
    time.sleep(4)
    if str(browser.page_source).find('Balance:') > -1:
        Billing = asin_func.getparse(str(browser.page_source),'Balance:','</div>')
        Billing = asin_func.getparse(Billing,'class="badge weight-normal font-13">','$').strip()
        print(">> Balance: {}".format(Billing))
        time.sleep(2)
        if str(Billing).replace('.','').isdigit():
            uSql = "update python_version_manage set api_balance = {}, api_balance_date = getdate() where name = 'goods_api'".format(Billing)
            print(">> uSql : {}".format(uSql))
            db_con.execute(uSql)
    return "0"

if __name__ == '__main__':

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    currIp = socket.gethostbyname(socket.gethostname())
    file_name = "new_red_asin.exe"
    if str(currIp).strip() != "222.104.189.18":
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
        time.sleep(4)

    db_con = DBmodule_FR.Database('red')
    list_name = "list_api"
    print('>> fun_chart() ')
    if str(currIp).strip() != "222.104.189.18":
        version_check2(db_con, file_name, ver, list_name) # version 체크

    endpage, endasin, sort_type, min_qty_order = asin_func.getSet(db_con, list_name)
    endasin = asin_func.getEndasin(db_con,list_name)
    if endasin > 0:
        print('>> asin_func.getEndasin OK : ' + str(endasin))
    else:
        print('>> asin_func.getEndasin Check')

    endpage = asin_func.getEndpage(db_con,list_name)
    if endpage > 9 and endpage < 300:
        print('>> asin_func.getEndpage OK : {}'.format(endpage))
    else:
        print('>> asin_func.getEndpage Check')

    time.sleep(1)
    now_url = "https://open-demo.otcommerce.com/ik.php"
    try:
        print(">> asin_func.connectDriverOld set ")
        browser = asin_func.connectDriverOld(now_url, "")
    except Exception as e:
        print(">> asin_func.connectDriverNew set ")
        browser = asin_func.connectDriverNew(now_url, "")
    time.sleep(3)
    browser.set_window_size(1600, 1000)

    browser.get(now_url)
    time.sleep(4)
    if str(browser.page_source).find('Instance Key') > -1:
        print(">> Login Need ")
        asin_func.demo_login_new(browser)
        time.sleep(2)

        if str(browser.page_source).find('https://open-demo.otcommerce.com/admin/') > -1:
            print(">> Login Ok ")
            billChk(browser, db_con) # api 잔액체크
            time.sleep(1)
            browser.get('https://open-demo.otcommerce.com/')
            time.sleep(3)
        else:
            print(">> Login Fail Input Key : ")

    mainLow = 1
    errCnt = 0
    mainStop = "0"
    while mainLow < 10000:
        asinCnt = asin_func.getAsinCnt(db_con, list_name)
        if asinCnt > endasin:
            print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
            procLogSet(db_con, "asin_new_list", " asinCnt : " + str(asinCnt)+' 건)', currIp)
            db_con.close()
            browser.quit()
            time.sleep(1)
            os._exit(0)

        print('>> ------------- mainLow : ' + str(mainLow) + ' -------------')
        rCate = newlist(db_con, endpage, currIp)
        if rCate == "1":
            print(">> rCate : " + str(rCate))
        else:
            fun_chart(db_con, browser, rCate, endpage, currIp, file_name, ver, errCnt, sort_type, min_qty_order)

        mainLow = mainLow + 1

    print('>> [--- main end ---] ' + str(datetime.datetime.now()))
    time.sleep(5)
    db_con.close()
    browser.quit()

