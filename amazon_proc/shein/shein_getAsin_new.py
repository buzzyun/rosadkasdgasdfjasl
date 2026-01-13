# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:31:45 2023

@author: allin
"""
import json
import DBmodule_NEW
import shein_func
import util_func
import get_asin_function
import socket
import time
import random
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# 카테고리 내 상품 url 리스트 들고오기
def getProdAsin(json_data,catecode,cate_code2):
    asinList = []

    # start_index = html.find("gbProductListSsrData = ")
    # end_index = html.find("</script>",start_index)
    for goods in json_data["results"]["goods"]:
        dic = dict()
        try:
            goods_url = shein_func.makeSheinProdUrl(goods["goods_url_name"],str(goods["goods_id"]),str(goods["cat_id"]))
        except:
            continue
        asin = goods["goods_id"]
        # title = goods["goods_name"]
        dic["asin"] = "'"+str(asin)+"'"
        # dic["title"] = "'"+title+"'"
        dic["url"] = "'"+goods_url+"'"
        dic["catecode"] = "'"+str(catecode)+"'"
        dic["cate_code2"] = "'"+str(cate_code2)+"'"
        asinList.append(dic)

    return asinList

def cateClick(driver, depth, big, middle, small, little, last,amz_cateurl, cate_code2):
    try:
        xpath_depth2 = '//*[@class="side-filter__item-content"]/div/section/label/span[{}]'
        xpath_depth3 = '//*[@class="side-filter__item-content"]/div/section/section/label/span[{}]'
        xpath_depth4 = '//*[@class="side-filter__item-content"]/div/section/section/section/label/span[{}]'
        xpath_depth5 = '//*[@class="side-filter__item-content"]/div/section/section/section/section/label/span[{}]'
        print("Depth-1 : {} click".format(big))
        driver.find_element(By.LINK_TEXT,big).click()
        if depth>=2:
            time.sleep(random.uniform(3,5))
            try:
                driver.find_element(By.CLASS_NAME,"side-filter__item-viewMore").click()
                time.sleep(random.uniform(3,5))
            except:
                print("더 보기 버튼 없음")
            try:
                driver.find_element(By.XPATH,xpath_depth2.format('text()="'+middle+'"')).click()
            except:
                print("카테고리 이름 수정 후 클릭")
                middle_split = middle.split()
                xpath_depth2 = '//span['
                for middle_item in middle_split:
                    if xpath_depth2 == '//span[':
                        xpath_depth2 = xpath_depth2 + 'contains(text(),"{}")'.format(middle_item)
                    else:
                        xpath_depth2 = xpath_depth2 + ' and contains(text(),"{}")'.format(middle_item)
                xpath_depth2 = xpath_depth2 + ']'
                driver.find_element(By.XPATH,xpath_depth2).click()
                time.sleep(random.uniform(1,3))
            print("Depth-2 : {} click".format(middle))
        if depth>=3:
            time.sleep(random.uniform(3,5))
            try:
                driver.find_element(By.XPATH,xpath_depth3.format('text()="'+small+'"')).click()
            except:
                print("카테고리 이름 수정 후 클릭")
                small_split = small.split()
                xpath_depth3 = '//span['
                for small_item in small_split:
                    if xpath_depth3 == '//span[':
                        xpath_depth3 = xpath_depth3 + 'contains(text(),"{}")'.format(small_item)
                    else:
                        xpath_depth3 = xpath_depth3 + ' and contains(text(),"{}")'.format(small_item)
                xpath_depth3 = xpath_depth3 + ']'
                driver.find_element(By.XPATH,xpath_depth3).click()
                time.sleep(random.uniform(1,3))
            print("Depth-3 : {} click".format(small))
        if depth>=4:
            time.sleep(random.uniform(3,5))
            try:
                driver.find_element(By.XPATH,xpath_depth4.format('text()="'+little+'"')).click()                
            except:
                print("카테고리 이름 수정 후 클릭")
                little_split = little.split()
                xpath_depth4 = '//span['
                for little_item in little_split:
                    if xpath_depth4 == '//span[':
                        xpath_depth4 = xpath_depth4 + 'contains(text(),"{}")'.format(little_item)
                    else:
                        xpath_depth4 = xpath_depth4 + ' and contains(text(),"{}")'.format(little_item)
                xpath_depth4 = xpath_depth4 + ']'
                print(xpath_depth4)
                driver.find_element(By.XPATH,xpath_depth4).click()
                time.sleep(random.uniform(1,3))
            print("Depth-4 : {} click".format(little))
        if depth>=5:
            time.sleep(3)
            try:            
                driver.find_element(By.XPATH,xpath_depth5.format('text()="'+last+'"')).click()
                time.sleep(random.uniform(1,3))
            except:
                print("카테고리 이름 수정 후 클릭")
                last_split = last.split()
                xpath_depth5 = '//span['
                for last_item in last_split:
                    if xpath_depth5 == '//span[':
                        xpath_depth5 = xpath_depth5 + 'contains(text(),"{}")'.format(last_item)
                    else:
                        xpath_depth5 = xpath_depth5 + ' and contains(text(),"{}")'.format(last_item)
                xpath_depth5 = xpath_depth5 + ']'
                driver.find_element(By.XPATH,xpath_depth5).click()
                time.sleep(random.uniform(1,3))
            print("Depth-5 : {} click".format(last))
        now_url = driver.current_url
        if now_url.find(str(cate_code2)) > -1:
            print("정상 url")
        else:
            print("비정상 url 강제 {} 이동".format(amz_cateurl))
            driver.get(amz_cateurl)
    except:
        print("예외 상황 강제 {} 이동".format(amz_cateurl))
        driver.get(amz_cateurl)
        time.sleep(random.uniform(3,5))

def get_asin_count():
    end_asin_cnt = 50000
    sql = "select endasin from python_version_manage where name='list' "
    end_chk = db_con.selectone(sql)
    if end_chk:
        end_asin_cnt = end_chk[0]
    return end_asin_cnt

if __name__ == '__main__':    

    ip = socket.gethostbyname(socket.gethostname())
    if str(ip).find('222.104.189.18') == -1:
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
    db_con = DBmodule_NEW.Database('trend')
    ip = socket.gethostbyname(socket.gethostname())

    driver = util_func.chrom_drive()
    amz_cateurl = "https://asia.shein.com/"
    driver.get(amz_cateurl)
    time.sleep(random.uniform(3,5))
    first_chk = 1
    end_asin_cnt = 50000

    while True:
        time_num = random.randint(2, 5)
        time.sleep(1)
        end_asin_cnt = get_asin_count()
        sql = "select count(*) as cnt from t_getasin"
        cnt_chk = db_con.selectone(sql)
        if cnt_chk:
            if int(cnt_chk[0]) > int(end_asin_cnt):
                print(">> t_getasin : {} | {} 이상 ".format(cnt_chk[0], end_asin_cnt))
                break

        result = get_asin_function.newlist(db_con,ip)
        catecode = result["catecode"]
        cate_code2 = result["cate_code2"]
        page_num = result["page"]
        amz_cateurl = result["url"]
        big = result["big"]
        middle = result["middle"]
        small = result["small"]
        little = result["little"]
        last = result["last"]
        depth = result["depth"]        

        if first_chk==1 or page_num==1:
            cateClick(driver, depth, big, middle, small, little, last, amz_cateurl, cate_code2)
            first_chk=0
        else:
            try:
                print("다음 페이지")
                driver.find_element(By.CSS_SELECTOR,"span.sui-pagination__next.sui-pagination__btn.sui-pagination__hover").click()
            except:
                sql = "delete from update_list where catecode = '{0}'".format(result['catecode'])
                print("마지막 페이지 NEXT")
                db_con.execute(sql)
                db_con.commit()                
                continue
        print("amz_cateurl :{} | now page : {} ".format(amz_cateurl, page_num))
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        try:
            product_list_all = soup.select_one("section.product-list-v2__section")
            product_list = product_list_all.select("div > section")
        except:
            print("새로고침")
            driver.refresh()
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')    
            try:                
                product_list_all = soup.select_one("section.product-list-v2__section")
                product_list = product_list_all.select("div > section")
            except:                
                input("캡챠 확인")
                html = driver.page_source
                soup = BeautifulSoup(html,'html.parser')                 
                product_list_all = soup.select_one("section.product-list-v2__section")
                product_list = product_list_all.select("div > section")

        if len(product_list)==0:
            time.sleep(1)
            driver.refresh()
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            product_list_all = soup.select_one("section.product-list-v2__section")
            product_list = product_list_all.select("div > section")

        if len(product_list)==0:
            sql = "delete from update_list where catecode = '{0}'".format(result['catecode'])
            print(">> update_list delete : {}".format(result['catecode']))
            db_con.execute(sql)
            db_con.commit()
            print("상품없음 NEXT")
        else:
            asinList = []
            for product_item in product_list:
                dic = dict()
                try:
                    temp = product_item["data-expose-id"].split("-")
                    goods_url = product_item.select_one("div.product-card__top-wrapper > a")["href"]
                    if len(goods_url)>1000:
                        continue
                except:
                    continue
                t_asin = temp[1]
                # title = goods["goods_name"]
                dic["asin"] = "'"+str(t_asin)+"'"
                # dic["title"] = "'"+title+"'"
                dic["url"] = "'"+goods_url+"'"
                dic["catecode"] = "'"+str(catecode)+"'"
                dic["cate_code2"] = "'"+str(cate_code2)+"'"
                
                if str(t_asin) == "" or str(goods_url) == "":
                    print(">> No goods_url (skip) :{}".format(t_asin))
                asinList.append(dic)
            try:
                row = 0
                for asin in asinList:
                    sql_chk = "select top 1 asin from t_getasin where asin={}".format(asin["asin"])
                    chk = db_con.selectone(sql_chk)
                    if chk:
                        continue

                    sql_chk3 = "select top 1 ali_no, isnull(asin_url,'') asin from t_goods where ali_no={}".format(asin["asin"])
                    chk3 = db_con.selectone(sql_chk3)
                    if chk3:
                        db_ali_no = chk3[0]
                        db_asin_url = chk3[1]
                        if db_asin_url == "":
                            sql_u = " update t_goods set asin_url={}, cate_idx = {}, cate_code2 = {} where ali_no={}".format(asin["url"],asin["catecode"],asin["cate_code2"],asin["asin"])
                            print(">> t_goods: url update : {}".format(asin["asin"]))
                            db_con.execute(sql_u)
                            db_con.commit()
                        continue

                    sql_chk2 = "select top 1 option_code asin from t_goods_option where option_code={}".format(asin["asin"])
                    chk2 = db_con.selectone(sql_chk2)
                    if chk2:
                        continue

                    row = row + 1
                    print(">> ({}) {} | {} | {} ".format(row,asin["asin"],asin["catecode"],asin["cate_code2"]))
                    print(">> t_getasin insert : {}".format(asin["asin"]))
                    db_con.insert("t_getasin", asin)
                    db_con.commit()
                    
                sql = "update update_list set now_page = now_page + 1, regdate = getdate() where catecode = '{0}' and proc_ip = '{1}'".format(result['catecode'],ip)
                print(">> update update_list ")
                db_con.execute(sql)
                db_con.commit()
            except Exception as ex:
                print(ex)
                print("===break point===")
                print("[{}] {} | {}".format(asin["asin"],page_num,amz_cateurl))

                sql = "delete from update_list where catecode = '{0}'".format(result['catecode'])
                print(">> update_list delete : {}".format(result['catecode']))
                db_con.execute(sql)
                db_con.commit()
                print("Exception NEXT")
                # db_con.close()
                break

    try:
        db_con.close()
    except Exception as ex:
        pass
    driver.quit()
    os._exit(0)