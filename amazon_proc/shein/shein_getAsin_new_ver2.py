# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 08:26:27 2024

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



def cateClick(driver, depth, big, middle, small, little, last,amz_cateurl, cate_code2):
    try:
        xpath_depth2 = '//*[@class="side-filter__item-content"]/div/section/label/span[{}]'
        xpath_depth3 = '//*[@class="side-filter__item-content"]/div/section/section/label/span[{}]'
        xpath_depth4 = '//*[@class="side-filter__item-content"]/div/section/section/section/label/span[{}]'
        xpath_depth5 = '//*[@class="side-filter__item-content"]/div/section/section/section/section/label/span[{}]'
        print("Depth-1 : {} click".format(big))
        driver.find_element(By.LINK_TEXT,big).click()
        if depth>=2:
            time.sleep(3)
            try:
                driver.find_element(By.CLASS_NAME,"side-filter__item-viewMore").click()
                time.sleep(3)
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
            print("Depth-2 : {} click".format(middle))
        if depth>=3:
            time.sleep(3)
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
            print("Depth-3 : {} click".format(small))
        if depth>=4:
            time.sleep(3)
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
            print("Depth-4 : {} click".format(little))
        if depth>=5:
            time.sleep(3)
            try:            
                driver.find_element(By.XPATH,xpath_depth5.format('text()="'+last+'"')).click()
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

def cateClick2(driver, depth, catecode, big, mcate, scate, dcate):
    
    print("Depth-1 : {} click".format(big))
    driver.find_element(By.LINK_TEXT,big).click()
    if depth>=2:
        time.sleep(3)
        try:
            driver.find_element(By.CLASS_NAME,"side-filter__item-viewMore").click()
            time.sleep(3)
        except:
            print("더 보기 버튼 없음")
        if mcate==None:
            mcate = catecode
        driver.find_element(By.CSS_SELECTOR,"label[data-cat-id='{}']".format(str(mcate))).click()
        print("Depth-2 : {} click".format(middle))
    if depth>=3:
        time.sleep(3)
        if scate==None:
            scate = catecode
        driver.find_element(By.CSS_SELECTOR,"label[data-cat-id='{}']".format(str(scate))).click()
        print("Depth-3 : {} click".format(small))
    if depth>=4:
        time.sleep(3)
        if dcate==None:
            dcate = catecode
        driver.find_element(By.CSS_SELECTOR,"label[data-cat-id='{}']".format(str(dcate))).click()
        print("Depth-4 : {} click".format(little))
    if depth>=5:
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR,"label[data-cat-id='{}']".format(str(catecode))).click()
        print("Depth-5 : {} click".format(last))
driver = util_func.chrom_drive()
driver.get("https://asia.shein.com/")
db_con = DBmodule_NEW.Database('trend')

sql = "select big, middle, small, little, last, depth,amz_cateurl, cate_code2 from t_category where catecode='5682'"
rs = db_con.selectone(sql)
big = rs[0]
middle = rs[1]
small = rs[2]
little = rs[3]
last = rs[4]
depth = rs[5]
amz_cateurl = rs[6]
cate_code2 = rs[7]
cateClick(driver, depth, big, middle, small, little, last,amz_cateurl, cate_code2)
db_con.close()