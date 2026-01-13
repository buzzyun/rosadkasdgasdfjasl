import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
import subprocess
import os, sys
import datetime
import webbrowser
import func_user
import DBmodule_FR
import func
import parsing_source


db_FS = DBmodule_FR.Database('freeship')

if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> 작업 시작 (네이버 쇼핑 삭제상품)(선택) :' + str(now))

    cate_main_url = "https://www.coupang.com/np/campaigns/83"
    try:
        proc_id, mainDriver = func_user.connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    mainDriver.get(cate_main_url)
    mainDriver.set_window_size(1400, 1000)
    mainDriver.implicitly_wait(3)

    time.sleep(2)
    print('time.sleep(2)')


    mainDriver.get('https://adcenter.shopping.naver.com/iframe/product/manage/deleted/list.nhn')
    print('>> 삭제 상품 page Ok')

    time.sleep(4)
    print('time.sleep(4)')

    pMainSoup = mainDriver.page_source
    procDic = dict()
    procList = []
    procCnt = 0
    titCnt = 0
    tmpReasonLog = ""
    if str(pMainSoup).find('delResnList') > -1:
        naver_del_cnt = ""
        naver_del_cnt = func.getparse(str(pMainSoup), 'prdt_status_lst', 'delResnList')
        naver_del_cnt = func.getparse(str(naver_del_cnt), '<span>', '</span>')
        naver_del_cnt = naver_del_cnt.replace(",","").strip()
        print(" Naver 삭제 상품수 : {} ".format(naver_del_cnt))

    try:
        db_FS.close()
        mainDriver.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    os._exit(0)
