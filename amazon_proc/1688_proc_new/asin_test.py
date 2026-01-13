import os
os.system('pip install --upgrade selenium')
import datetime
import time
import datetime
import os
import random
import requests
import urllib
import json
from stem import Signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen
from stem.control import Controller
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import http.client
import socks
import socket
import time
import uuid

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

def connectDriverOld(pgSite, kbn):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
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
    option.add_argument("--disable-gpu")
    if str(kbn) == "":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")

    browser = webdriver.Chrome(options=option)

    return browser

def connectDriverNew(pgSite, kbn):
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
    option.add_argument("--disable-gpu")
    if str(kbn) == "":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    # Selenium 4.0 - load webdriver

    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
    except Exception as e:
        print(e)
        # s = Service(ChromeDriverManager(version="114.0.5735.90").install())
        # browser = webdriver.Chrome(service=s, options=option)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

def checkIP():
    conn = http.client.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    time.sleep(1)
    response = conn.getresponse()
    print('>> current ip address :', response.read())


def set_new_ip():
    print('>> set_new_ip')
    # disable socks server and enabling again
    socks.setdefaultproxy()
    # """Change IP using TOR"""
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
        socket.socket = socks.socksocket
        controller.signal(Signal.NEWNYM)

def set_new_tor_ip():
    # """Change IP using TOR"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    print(">> set_new_tor_ip()")

def checkCurrIP():
    time.sleep(2)
    # proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    # res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    # print('>> Tor Current IP:', res.text)

def checkCurrIP_new():
    time.sleep(1)
    proxy = { 'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050', }
    res = requests.get('https://icanhazip.com', proxies=proxy)  # using TOR network
    print('>> Tor Current IP:', res.text)
    time.sleep(1)

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


if __name__ == '__main__':

    print(str(datetime.datetime.now()))

    wCnt = 0
    while wCnt < 3 :
        set_new_tor_ip()
        checkCurrIP_new()
        time.sleep(5)
        wCnt = wCnt + 1

    # 크롬 드라이버 연결
    site_url = "https://www.1688.com"
    try:
        browser = connectDriverNew(site_url, "")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(site_url, "")
        print(">> connectDriverOld set OK ")
    browser.set_window_size(1200, 900)
    browser.set_window_position(140, 0, windowHandle='current')
    browser.implicitly_wait(3)
    time.sleep(1)
    set_new_tor_ip()
    checkCurrIP_new()
    time.sleep(2)

    cnt = 0
    proc_flg = "0"
    while proc_flg == "0":
        link_url = input(">> link_url :").strip()
        if link_url == "":
            link_url = input(">>Please Input Url :").strip() # https://www.dcbuy.co.kr/mall/search/%EB%AA%A9%EC%95%88%EB%A7%88%EA%B8%B0%EA%B5%AC

        # req_link = "https://www.dcbuy.co.kr/api/product/productListSearchByKeyword"
        # headers = {
        #     'Accept-Encoding': 'gzip, deflate, br, zstd',
        #     'Content-Type': 'application/json;charset=UTF-8', 
        #     'X-Language': 'ko',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + 'Safari/537.36',
        #     'Referer': str(link_url)
        #     }

        # #res = requests.get(link_url)
        # #print(">> 1: {} ".format(res.status_code))
    
        # try:
        #     res2 = requests.get(link_url, headers=headers)
        # except Exception as e:
        #         print(">> Except : {}".format(e)) 
        # else:
        #     time.sleep(2)
        #     print(">> 2: {} ".format(res2.status_code))

        print(">>")
        # time.sleep(1)
        # browser.get(link_url)
        # time.sleep(4)
        # print(f">> Link_url : {link_url}")
        # result = str(browser.page_source)
        # time.sleep(1)
        # print(">> result : {}".format(result))

        keyword = link_url.strip()
        print(">> Keyword : {}".format(keyword))
        req_link = "https://www.dcbuy.co.kr/api/product/productListSearchByKeyword"
        data = {'current' : 1, 'keyword' : str(keyword), 'size': 50, 'sort': '', 'sortType': '', 'type':0 }
        headers = {
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json;charset=UTF-8', 
            'X-Language': 'ko',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + 'Safari/537.36',
            'Referer': str(req_link)
            }
        print(data)
        print(headers)
        print("--------------- ")
        try:
            res_post = requests.post(req_link, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(">> Except : {}".format(e)) 
        else:
            time.sleep(random.uniform(4,8))
            print(res_post.status_code)
            print(res_post.text)
            result = ""
            if res_post.status_code == 200:
                result = res_post.text
                resultJson = res_post.json()
                if resultJson['code'] == 200:
                    asinUrl = getparse(result,'imageUrl":"','"')
                    asinSubject = getparse(result,'subject":"','"')
                    asin = getparse(result,'offerId":',',')
                    asinPrice = getparse(result,'"price":"','"')
                    print("[{}] {} | {} | {}".format(cnt+1, asin, asinPrice, asinSubject))
                else:
                    print("[{}] {} : fail({}) : {} ".format(cnt+1,res_post.status_code,resultJson['code'],keyword))
            else:
                print("[{}] {} : fail {} : {}".format(cnt+1, res_post.status_code,keyword))
        cnt = cnt + 1
        print(">>")
        # wCnt = 0
        # while wCnt < 2 :
        #     set_new_tor_ip()
        #     checkCurrIP_new()
        #     time.sleep(3)
        #     wCnt = wCnt + 1

    print(">>")
    input(">> ")

'''
{"code":200,"errorCode":"2000","errMsg":"success","data":{"current":"1","pages":"41","size":"50","total":"2000"
,"data":[
{"imageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01TWxf1i287qGa3FVbJ_!!3369597886-0-cib.jpg",
"subject":"새로운 8DB 2.4G /5.8G 듀얼 밴드 내장 높은 이득 PCB 안테나 무선 라우터 WIFI 네트워크 카드"
,"subjectTrans":"New 8DB 2.4g/5.8G dual band built-in high gain PCB antenna wireless router for WIFI network card"
,"offerId":556733445249
,"isJxhy":false
,"priceInfo":{"price":"1.20","jxhyPrice":null,"pfJxhyPrice":null}
,"repurchaseRate":"25%"
,"monthSold":"172"
,"link":"https://detail.1688.com/offer/556733445249.html"}

,{"imageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01OUODAz26xTYA8HBDP_!!998727728-0-cib.jpg"
,"subject":"12.0V RS-232 버섯 헤드 케이스 GPS 모듈 안테나 4800 방수 해양 수신기 BP-275S"
,"subjectTrans":"12.0V RS-232 mushroom head shell GPS module antenna 4800 waterproof marine receiver BP-275S"
,"offerId":674333109224,"isJxhy":false,"priceInfo":{"price":"85.00","jxhyPrice":null,"pfJxhyPrice":null}
,"repurchaseRate":"100%","monthSold":"40","link":"https://detail.1688.com/offer/674333109224.html"}

,{"imageUrl":"https://cbu01.alicdn.com/img/ibank/10699959731_1583742058.jpg"
,"subject":"FM 라디오 FM 통신 Yagi 안테나 스테레오 라디오 야외 홈 파워 앰프 수신 발코니"
,"subjectTrans":"FM broadcasting FM communication Yagi antenna stereo broadcasting radio outdoor home power amplifier receiving balcony"
,"offerId":590571473658,"isJxhy":false,"priceInfo":{"price":"120.00","jxhyPrice":null,"pfJxhyPrice":null}
,"repurchaseRate":"0%","monthSold":"0","link":"https://detail.1688.com/offer/590571473658.html"}



'''