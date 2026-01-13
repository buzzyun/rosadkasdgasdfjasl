import os
os.system('pip install --upgrade selenium')
import datetime
import random
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import socket
import uuid
import time
import sys
import subprocess
import urllib
import DBmodule_AM
import am_asin

global ip
global ver
global chkTime
global endpage
global errCnt
ver = "61.0"

ip = socket.gethostbyname(socket.gethostname())
amzurl = ""
chkTime = time.time()
print(">> chkTime : "+str(chkTime))

def mac_addr():
    print('\n\n')
    a = uuid.getnode()
    mac = ':'.join(("%012X" % a)[i:i+2] for i in range(0, 12, 2))
    print('>> MAC : '+str(mac))

    return str(mac)

# def connectChromeDriverNew(pgSite):
#     option = Options()
#     option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
#     option.add_experimental_option('excludeSwitches', ['enable-logging'])
#     option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
#     option.add_experimental_option("useAutomationExtension", False) 
#     option.add_argument("--disable-blink-features=AutomationControlled") 
#     option.add_argument("--disable-features=VizDisplayCompositor")
#     option.add_argument("--disable-gpu")
#     option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': " + str(pgSite) + "'")
#     # Selenium 4.0 - load webdriver
#     browser = ""
#     try:
#         s = Service(ChromeDriverManager().install())
#         browser = webdriver.Chrome(service=s, options=option)
#         browser.set_window_size(1200, 900)
#         browser.set_window_position(140, 0, windowHandle='current')
#         browser.implicitly_wait(3)
#     except Exception as e:
#         print(e)

#     return browser

def connectSubProcess():

    filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    proc_id = ""
    try:
        print(">> C:\Program Files (x86)\Google\Chrome ")
        proc_id = subprocess.Popen(filePath_86)   # Open the debugger chrome
    except Exception as e:
        print(">> C:\Program Files\Google\Chrome ")
        try:
            proc_id = subprocess.Popen(filePath)
        except Exception as e:
            print(">> subprocess.Popen(filePath) failed")
            print(e)

    option = Options()
    # option.add_argument("--incognito") ## 시크릿 모드 추가
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        try:
            chromedriver_autoinstaller.install(True)
        except Exception as e:
            print(">> chromedriver_autoinstaller.install failed")
            print(e)

    browser = webdriver.Chrome(options=option)
    return browser, proc_id

def connectDriverNew(pgSite, kbn, type):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    #option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
        print(">> ChromeDriverManager install ")
    except Exception as e:
        print(e)
        # print(">> ChromeDriverManager 114.0.5735.90 install ")
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)

        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path

    return browser

def connectChromeDriver(site_url):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
            random.random()) + " Safari/537.36, 'Referer':'{}'".format(site_url))
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    
    browser.set_window_size(1200, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)

    return browser

def deliveryToSet(browser, site):
    ############ Deliver to Set #############################
    deliverTo = am_asin.procDeliverChk(browser) #Deliver to check
    print('deliverTo (before): ' + str(deliverTo))
    if site == "uk":
        cPost = deliverTo[:5]

    if site == "usa":
        if str(deliverTo).find('97005') == -1:
            try:
                am_asin.procDelivertoSet(browser, "US") #Deliver to Set
            except Exception as ex:
                print('>> procDelivertoSet Error : ', ex)
        time.sleep(1)
        deliverTo = am_asin.procDeliverChk(browser) #Deliver to check
        print('deliverTo (after): ' + str(deliverTo))
        if str(deliverTo).find('97005') == -1:
            print('deliverTo no set (SKIP) ' + str(deliverTo))

    elif site == "uk":
        if str(deliverTo).find(cPost) == -1:
            print('>> Deliver to set : ' + str(deliverTo))
            if str(deliverTo).find("Select your address") > -1:
                print(">> Select your address (SKIP) ")
            else:
                print(">> 확인 필요 ")

    elif site == "global":
        if str(deliverTo).find('542-0012‌') == -1:
            try:
                am_asin.procDelivertoSet(browser, "JP") #Deliver to Set
            except Exception as ex:
                print('>> procDelivertoSet Error : ', ex)
        time.sleep(1)
        deliverTo = am_asin.procDeliverChk(browser) #Deliver to check
        print('deliverTo (after): ' + str(deliverTo))
        if str(deliverTo).find('542-0012‌') == -1:
            print('deliverTo no set (SKIP) ' + str(deliverTo))

    elif site == "de":
        if str(deliverTo).find('60386') == -1:
            try:
                am_asin.procDelivertoSet(browser, "DE") #Deliver to Set
            except Exception as ex:
                print('>> procDelivertoSet Error : ', ex)
        time.sleep(1)
        deliverTo = am_asin.procDeliverChk(browser) #Deliver to check
        print('deliverTo (after): ' + str(deliverTo))
        if str(deliverTo).find('60386') == -1:
            print('deliverTo no set (SKIP) ' + str(deliverTo))


def procKill(currIp):
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

if __name__ == '__main__':

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    errCnt = 0
    errFlg = ""
    input_Site = sys.argv[1]
    input_pgKbn = sys.argv[2]
    input_torKbn = sys.argv[3]
    site = str(input_Site).strip()
    list_name = str(input_pgKbn).strip()
    print(">> SITE : {}".format(site))
    print(">> list NAME : {}".format(list_name))
    print(">> Tor Kbn : {}".format(input_torKbn))
    if input_Site == "" and input_pgKbn == "":
        print(">> 입력 값을 확인하세요. {} | {} ".format(input_Site, input_pgKbn))
        print(">> Main End : " + str(datetime.datetime.now()))
        os._exit(1)

    file_name = "new_am_asin_all.exe"
    if site == "usa": 
        site_url = "https://www.amazon.com"
        db_con = DBmodule_AM.Database('USA')
    elif site == "global":
        site_url = "https://www.amazon.co.jp"
        db_con = DBmodule_AM.Database('global')
    elif site == "uk":
        site_url = "https://www.amazon.co.uk"
        db_con = DBmodule_AM.Database('UK')
    elif site == "de":
        site_url = "https://www.amazon.de"
        db_con = DBmodule_AM.Database('DE')

    currIp = socket.gethostbyname(socket.gethostname())
    procKill(currIp)

    if str(ip).strip() == "222.104.189.18":
        print('>> version_check (Skip) local : ' + str(ip))
    else:
        # version 체크
        am_asin.version_check2(db_con, file_name, ver, list_name)

    # del_naver (4) 재등록 후 삭제할 데이터 ---> asin list 에서 제거
    am_asin.del_naver4_remove(db_con)
    time.sleep(2)
    print('>> time.sleep(2) ')

    # delete stopUpdateGoods 
    am_asin.procDelStopUpdateGoods(db_con)
    time.sleep(1)

    # Block Goods --> T_Category_BestAsin 이동
    am_asin.procBlockGoods(db_con)
    time.sleep(2)
    print('>> time.sleep(2) ')

    endasin = 0
    endasin = am_asin.getEndasin(db_con, list_name)
    if endasin > 0:
        print('>> getEndasin : ' + str(endasin))
    else:
        print('>> getEndasin Check')

    asinCnt = am_asin.getAsinPriorityCnt(db_con, list_name)
    print(">> Curr asinCnt : {}".format(asinCnt))
    if asinCnt > endasin:
        print('>> (SKIP) asinCnt가 ' +str(endasin)+ '건 이상 입니다. (T_Category_BestAsin : '+str(asinCnt)+' 건)')
        db_con.close()
        time.sleep(1)
        os._exit(0)

    proc_id = ""
    # 크롬 드라이버 연결
    if site == "global" or site == "de": 
        # browser = am_asin.connectDriverNew(site_url, "")
        try:
            browser = am_asin.connectDriverNew(site_url, "")
        except Exception as e:
            print(">> connectDriverOld set ")
            browser = am_asin.connectDriverOld(site_url, "")
            print(">> connectDriverOld set OK ")
        browser.set_window_size(1200, 900)
        browser.set_window_position(140, 0, windowHandle='current')
        browser.implicitly_wait(3)
        time.sleep(1)
        am_asin.set_new_tor_ip()
        am_asin.checkCurrIP_new()
        time.sleep(2)
    elif (site == "usa" or site == "uk") and input_torKbn == "N":
        # try:
        #     print(">> connectDriverOld set ")
        #     browser = am_asin.connectDriverOld(site_url, "1")
        # except Exception as e:
        #     browser = am_asin.connectDriverNew(site_url, "1")
        #     print(">> connectDriverNew set OK ")
        # browser.set_window_size(1200, 900)
        # browser.set_window_position(140, 0, windowHandle='current')
        # browser.implicitly_wait(3)
        # time.sleep(1)
        
        try:
            browser, proc_id = connectSubProcess()
        except Exception as e:
            print(">> Exception : {}".format(e))
        browser.set_window_size(1200, 900)
        browser.set_window_position(140, 0, windowHandle='current')
        browser.implicitly_wait(3)
        time.sleep(1)
    else:
        try:
            browser = am_asin.connectDriverNew(site_url, "")
        except Exception as e:
            print(">> connectDriverOld set ")
            browser = am_asin.connectDriverOld(site_url, "")
            print(">> connectDriverOld set OK ")
        am_asin.set_new_tor_ip()
        am_asin.checkCurrIP_new()
        time.sleep(2)

    time.sleep(1)
    browser.get(site_url)
    time.sleep(4)
    result = str(browser.page_source)
    time.sleep(1)

    if str(result).find('validateCaptcha') > -1:
        print('>> validateCaptcha (auto) ')
        time.sleep(2)
        if site == "global" or site == "de":
            am_asin.set_new_tor_ip()
            am_asin.checkCurrIP()
            time.sleep(2)
        elif (site == "usa" or site == "uk") and input_torKbn == "Y":
            am_asin.set_new_tor_ip()
            am_asin.checkCurrIP()
            time.sleep(2)

        try:
            browser.get(site_url)
        except Exception as ex:
            print('>> now_url Get Error Skip ')
        else:                    
            time.sleep(3)
            print('>> time.sleep(3) ')

    ############ Deliver to Set ###########
    deliveryToSet(browser, site)

    endpage = 0
    endpage = am_asin.getEndpage(db_con, list_name)
    if endpage > 2 and endpage < 300:
        print('>> getEndpage OK')
    else:
        print('>> getEndpage Check')

    mainLow = 1
    mainStop = "0"
    while mainLow < 100:
        ## asinCnt = am_asin.getAsinCnt(db_con)
        asinCnt = am_asin.getAsinPriorityCnt(db_con, list_name)
        if asinCnt > endasin:
            am_asin.procLogSet(db_con, "asin_list", " asinCnt : " + str(asinCnt)+' 건)', ip)
            db_con.close()
            browser.quit()
            time.sleep(1)
            os._exit(0)

        print('>> ------------- mainLow : ' + str(mainLow) + ' -------------')

        #rCate = am_asin.newlist(db_con, endpage, ip, list_name)
        #판매수량이 많은 카테고리 (list_priority) / 그외 카테고리 (list) 구분하여 실행 (t_category 테이블 priority_flg)
        try:
            if site == "global" or site == "de":
                rCate = am_asin.newlist_priority(db_con, endpage, ip, list_name)
            elif (site == "usa" or site == "uk") and input_torKbn == "N":
                rCate = am_asin.newlist_priority(db_con, endpage, ip, list_name)
            else:
                rCate = am_asin.newlist_priority(db_con, endpage, mac_addr(), list_name)
        except Exception as ex:
            print('>> newlist_priority Exception Exit ')
            break
        else:
            try:
                am_asin.fun_chart(db_con, browser, rCate, endpage, ip, file_name, ver, errCnt, site_url, list_name)
            except Exception as ex:
                print('>> fun_chart Exception Exit : {}'.format(ex))
                input(">> input (2):")
                break

        mainLow = mainLow + 1

    print('>> [--- main end ---] ' + str(datetime.datetime.now()))
    print(">> (실행 시간) time :", time.time() - chkTime)  # 현재시각 - 시작시간 = 실행 시간

    db_con.close()
    time.sleep(2)
    try:
        browser.quit()
        print(">> driver.quit")
        subprocess.Popen.kill(proc_id)
        print(">> subprocess.Popen.kill")
    except:
        print(">> subprocess.Popen.kill except")
    time.sleep(2)
    os._exit(0)

