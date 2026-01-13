import os
os.system('pip install --upgrade selenium')
import datetime
import os
import time
import re
import random
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import subprocess
import taobao_func
import sys
import DBmodule_FR

global currIp
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp  : '+str(currIp))

ver = "01.81"
db_con = DBmodule_FR.Database("taobao")

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

def connectSubProcess():
    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    proc_id = ""
    try:
        proc_id = subprocess.Popen(filePath_86)   # Open the debugger chrome
        print(">> C:\Program Files (x86)\Google\Chrome ")
    except FileNotFoundError:
        print(">> C:\Program Files\Google\Chrome ")
        proc_id = subprocess.Popen(filePath)

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(options=option)

    return proc_id, browser

#중국어 찾기 ( 중국어 : True )
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    timecount = 0

    currIp = socket.gethostbyname(socket.gethostname())
    db_con = DBmodule_FR.Database('taobao')

    proc_id = ""
    try:
        proc_id, browser = connectSubProcess()
    except Exception as e:
        print(">> connectSubProcess Exception ")

    time.sleep(2)
    main_url = "https://sharkda.kr"
    browser.get(main_url)
    browser.set_window_size(1600, 1000)
    #browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(random.uniform(4,5))

    sql = "select top 100 ali_no, goodscode, IsDisplay, regdate from t_goods order by updatedate desc"
    rows = db_con.select(sql)
    cnt = 0

    option_code_dic = dict()
    option_value_dic = dict()
    option_value_org_dic = dict()
    option_price_dic = dict()
    option_img_dic = dict()

    for row in rows:
        cnt = cnt + 1
        asin = input(">> asin :")
        # asin = row[0]
        # goodscode = row[1]
        # isdisplay = row[2]
        # regdate = row[3]
        print("---------------------------------------------------------")
        ## print(">> ({}) [{}] {} ({}) {}".format(cnt, asin, goodscode, isdisplay, regdate))
        print(">> [{}] [{}] ".format(cnt, asin))
        if asin == "":
            continue
        ## https://sharkda.kr/ali/view/code/taobao/itemId/782462164175/categoryNo/1276/pageNo/1
        cateno = random.randint(100,3000)
        proc_url = "https://sharkda.kr/ali/view/code/taobao/itemId/{}/categoryNo/{}/pageNo/1".format(asin, cateno)
        print(">> proc_url proc : {}".format(proc_url))
        try:
            browser.get(proc_url)
        except Exception as e:
            print(">> proc_url Exception ")
        else:
            time.sleep(random.uniform(5,8))
            result = browser.page_source
            with open(os.getcwd() + "/log/sharkda_"+str(asin)+".html","w",encoding="utf8") as f: 
                f.write(str(result))

            title = getparse(str(result),'<div class="title-area">','</div>')
            title = getparse(str(title),'<h3 class="need-trans">','</h3>')
            if findChinese(title):
                print(">> 중국어 발견 sleep ")
                time.sleep(random.uniform(5,8))
                result = browser.page_source

            result_soup = BeautifulSoup(result, 'html.parser')
            if result.find('타오바오내 재고가 없는 상품') > -1:
                print(">> [{}] 재고없음 ".format(asin))
            else:      
                title = getparse(str(result),'<div class="title-area">','</div>')
                title = getparse(str(title),'<h3 class="need-trans">','</h3>')
                org_url = getparse(str(title),'<a href="','"')
                base_price = getparse(str(result),'<strong class="price">','</strong>')
                print(">> title : {}".format(title))
                print(">> base_price : {}".format(base_price))
                base_img = getparse(str(result),'id="main-thumb"','</div>')
                base_img = getparse(base_img,'src="','"')
                sub_img = getparse(str(result),'id="sub-thumb"','class="info-wrap"')
                sp_subimg = sub_img.split('<img ')
                for sub_img in sp_subimg:
                    sub_img_url = getparse(sub_img,'src="','"')
                    print(">> sub_img_url : {}".format(sub_img_url))
                print(">> base_img : {}".format(base_img))

                option_area = getparse(str(result),'id="option-area"','id="option-result-area"')
                result_json = getparse(str(result),'var jsonData =','property="og:title"')
                result_options = getparse(str(result_json),'"skus":{','"props":')
                sp_options = result_options.split('},')

                option_cnt = 0
                for ea_option in sp_options:
                    opt_val_tmp = ""
                    if ea_option != "":
                        option_cnt = option_cnt + 1
                        option_sku_id = getparse(str(ea_option),'"sku_id":',',')
                        option_id = getparse(str(ea_option),'"','":')
                        sp_skdid = option_id.split(';')
                        for ea_sku in sp_skdid:
                            findSku = 'data-prop="{}"'.format(ea_sku)
                            option_str = getparseR(str(option_area), '','data-prop="' +str(ea_sku)+ '"')
                            option_val = getparseR(option_str, 'value="','"')
                            if opt_val_tmp == "":
                                opt_val_tmp = opt_val_tmp + option_val
                            else:
                                opt_val_tmp = opt_val_tmp + " | " + option_val
                        print("\n>> ({}) {} ".format(option_sku_id, opt_val_tmp))
                        option_price = getparse(str(ea_option),'"price":',',')
                        option_price_won = getparse(str(ea_option),'"getPrice":',',')
                        option_stock = getparse(str(ea_option),'"quantity":',',')
                        option_img = getparse(str(ea_option),'"pic_url":"','"')
                        print(">> ({}) {} : {} => {} ( {}원) stock: {} ".format(option_cnt, option_id, option_sku_id, option_price, option_price_won, option_stock))
                        print(">> img : {}".format(option_img))

                        option_code_dic[option_sku_id] = sp_skdid
                        option_value_dic[option_sku_id] = opt_val_tmp
                        option_price_dic[option_sku_id] = option_price

                sp_opt_img = option_area.split('class="need-trans-option option-select"')
                for ea_img in sp_opt_img:
                    opt_img_txt = getparse(str(ea_img),'value="','"')
                    if str(ea_img).find('<img') > -1:
                        opt_img_url = getparse(str(ea_img),'src="','"')
                        if opt_img_url != "":
                            print(">> {} : {}".format(opt_img_txt, opt_img_url))
                            option_img_dic[opt_img_url] = opt_img_txt
                        #print(">> \n\n ")

                print(">> option_code_dic : {}".format(option_code_dic))
                print(">> option_value_dic : {}".format(option_value_dic))
                print(">> option_price_dic : {}".format(option_price_dic))
                print(">> option_img_dic : {}".format(option_img_dic))

        detail = getparse(str(result),'<h3>상품정보</h3>','')
        detail = getparse(result,'shadow.innerHTML = "','[...shadow').replace("\\","").replace(";","").replace('"','').replace("'","").replace("<div style=>","")
        print(">> -------------------------------- ")

    db_con.close()
    print(">> proc end ... ")
    ## https://sharkda.kr/ali/view/code/taobao/itemId/782462164175/categoryNo/1276/pageNo/1