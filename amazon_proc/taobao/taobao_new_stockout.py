import time
import os
import datetime
import random
import socket
import urllib
import sys
from selenium import webdriver
import chromedriver_autoinstaller
import taobao_func
import sys
p = os.path.abspath('.')
sys.path.insert(1, p)
from dbCon import DBmodule_FR

ver = "01.07"
currIp = socket.gethostbyname(socket.gethostname())

def connectDriver(tool):
    global set_browser
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    if tool == 'chrome':
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_argument("user-data-dir={}".format(userProfile))
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options) 

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')  
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random())\
            + " Safari/537.36, 'Referer': 'https://open-demo.otcommerce.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'brave':
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return browser

def procLogSet(in_DB, in_proc_no, in_proc_memo, ip):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(ip) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

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

def goodsDicInfo(goods_dic, input_pgKbn, db_con):
    sql = " select pgFilename, pgName, now_url, now_url2, target_sql1, isnull(target_sql2,''), isnull(target_sql3,''), exchange_Rate, dollar_exchange, \
        withbuy_cost, coupon from python_version_manage where name = 'stock_out_api'"
    rs = db_con.selectone(sql)
    if rs:
        pgFilename = str(rs[0]).strip()
        pgName = str(rs[1]).strip()
        goods_dic['py_now_url'] = str(rs[2]).strip()
        goods_dic['py_now_url2'] = str(rs[3]).strip()
        goods_dic['py_sql1'] = str(rs[4]).replace("`","'")
        goods_dic['py_sql2'] = str(rs[5]).replace("`","'")
        goods_dic['py_sql3'] = str(rs[6]).replace("`","'")
        goods_dic['py_exchange_Rate'] = str(rs[7]).strip()
        goods_dic['py_dollar_exchange'] = str(rs[8]).strip()
        goods_dic['py_withbuy_cost'] = str(rs[9]).strip()
        goods_dic['py_coupon'] = str(rs[10]).strip()

        if pgFilename is None or pgFilename == "":
            pgFilename = "new_" + str(pgName) + ".exe"
        if pgName is None or pgName == "":
            pgName = input_pgKbn
        goods_dic['py_pgFilename'] = pgFilename
        goods_dic['py_pgName']  = pgName

    return goods_dic

def processKill():
    try:
        taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
        print(">> taskstr : {}".format(taskstr))  
        os.system(taskstr)
    except Exception as e:
        print('>> taskkill Exception (1)')
    else:
        pass
    time.sleep(4)

def procLogSet(in_DB, in_proc_no, in_proc_memo):
    sql = " insert into goods_proc_log (proc_no, proc_log, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "', '" + str(currIp) + "', '" + str(in_proc_memo) + "') "

    print(">> setLogProc : " + str(sql))
    in_DB.execute(sql)

    return "0"

## browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic
def doTestProc(browser, db_con, db_ali, in_pgKbn, in_ver, goods_dic, asin_low):
    spm_asin = asin_low.split('@')
    goods_dic['asin'] = spm_asin[0]
    goods_dic['catecode'] = spm_asin[1]
    goods_dic['istmall'] = spm_asin[2]
    goods_dic['guid'] = spm_asin[3]

    rtnChk = taobao_func.proc_asin_out_brower_new(goods_dic, db_con, db_ali, browser)
    print('>> [ rtnChk ] : ' + str(rtnChk))

    rtn_uid = spm_asin[3]
    rtnChk_no = str(rtnChk[:3])
    print(taobao_func.getMemo(rtnChk))

    if rtnChk_no[:1] == "D": c_Errcnt = 0
    elif rtnChk_no == "C01" or rtnChk_no == "C02" or rtnChk_no == "C03": c_Errcnt = c_Errcnt + 1
    elif rtnChk_no == "C04" or rtnChk_no == "C05" or rtnChk_no == "C06": c_Errcnt = c_Errcnt + 1
    elif rtnChk_no == "0": 
        c_Errcnt = 0
        print('>> # SetDB OK (완료) : ' + str(rtnChk))

    sql = "select cate_idx, isnull(stock_ck_cnt,'0'), GoodsCode, IsDisplay, isnull(Del_Naver,''), isnull(stock_ck,''), regdate, UpdateDate, isnull(naver_in,0) from t_goods where uid = '" + str(rtn_uid) + "'"
    rs_row = db_con.selectone(sql)
    print('>> ##selectone## sql :' + str(sql))
    d_naver_in = ""
    if not rs_row:
        print('>> No date Check please : ' + str(asin_low))
    else:
        d_GoodsCode = rs_row[2]
        d_IsDisplay = rs_row[3]
        d_naver_in = rs_row[8]

        if rtnChk_no[:1] == "D":  # sold out
            if d_IsDisplay == 'T':
                print('>> IsDisplay Update (F) 품절처리 ')
                sql = "update T_goods SET IsDisplay='F', IsSoldOut='T', Stock='0', stock_ck = '4', stock_ck_date=getdate(), UpdateDate=getdate() where uid='{0}'".format(rtn_uid)
                print(">> sql : " + str(sql))
                print(">> Ok stock_ck update : " + str(d_GoodsCode))

        elif rtnChk_no == "0":
            sql = "update T_goods set stock_ck = '2' where uid='{0}'".format(rtn_uid)
            print(">> sql : " + str(sql))
            print(">> Ok stock_ck update : " + str(d_GoodsCode))

        else:  # blocked
            sql = "update T_goods set stock_ck = '0' where uid='{0}'".format(rtn_uid)
            print(">> sql : " + str(sql))
            print(">> UpdateDate  : " + str(d_GoodsCode))

        print(">> Errcnt : {0} ".format(c_Errcnt))

    return "0"


if __name__ == '__main__':

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    currIp = socket.gethostbyname(socket.gethostname())
    if str(currIp).strip() != "222.104.189.18":
        processKill()

    input_Site = sys.argv[1]
    input_pgKbn = sys.argv[2]
    input_Site = str(input_Site).strip()
    input_pgKbn = str(input_pgKbn).strip()
    print(">> SITE : {}".format(input_Site))
    print(">> PG NAME : {}".format(input_pgKbn))
    if input_Site == "" and input_pgKbn == "":
        print(">> 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    db_FS = DBmodule_FR.Database('freeship')
    db_con = DBmodule_FR.Database('taobao')
    db_ali = DBmodule_FR.Database('aliexpress')
    goods_dic = dict()
    goods_dic = goodsDicInfo(goods_dic, input_pgKbn, db_con)

    time.sleep(1)
    browser = connectDriver("chrome_secret")
    time.sleep(3)
    browser.set_window_size(1100, 800)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    now_url = "https://open-demo.otcommerce.com/ik.php"
    browser.get(now_url)
    time.sleep(4)
    if str(browser.page_source).find('Instance Key') > -1:
        print(">> Login Need ")
        taobao_func.demo_login_new(browser)
        time.sleep(2)
    if str(browser.current_url).find('https://open-demo.otcommerce.com/admin/') > -1:
        print(">> Login Ok ")
        browser.get('https://open-demo.otcommerce.com/')
        time.sleep(3)
    else:
        print(">> Login Fail Input Key : ")

    # Test Proc 
    if input_pgKbn == "stock_out_api_test":
        # asin_list = in_asin + "@" + str(in_cate_idx) + "@0" + "@" + str(in_guid)  -----  ex) B0117TLSZS@6245@0@ 
        asin_list = input(" asin@cate_idx@0@guid : ")
        print(" input asin_list : " + str(asin_list))
        doTestProc(browser, db_con, db_ali, input_pgKbn, ver, goods_dic, asin_list)
        db_FS.close()
        db_con.close()
        browser.quit()

    rtnFlg = ""
    mainLow = 1
    while mainLow < 100:
        taobao_func.check_browser(browser)
        if str(input_pgKbn).find('stock_out_api') > -1:
            rtnFlg = taobao_func.set_stock_out_new(browser, db_con, db_ali, input_pgKbn, ver, goods_dic)
        if rtnFlg == "E99":
            time.sleep(10)
            print(">> Error Exit ")
            break
        if rtnFlg == "1" or rtnFlg == "F":
            time.sleep(2)
            print(">> complete ")
            break
        mainLow = mainLow + 1

    print('>> [--- main end ---] ' + str(datetime.datetime.now()))
    db_ali.close()
    db_FS.close()
    db_con.close()
    browser.quit()


