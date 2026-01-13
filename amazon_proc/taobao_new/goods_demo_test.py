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


def connectDriverOld(pgSite, kbn, type):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False) 
    option.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer':'" + str (pgSite) + "'")
    browser = webdriver.Chrome(options=option)
    return browser

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
    option.add_argument("--disable-gpu")
    if type == "H":
        option.add_argument("--headless") # headless
    if str(kbn) == "Y":
        option.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    browser = ""
    try:
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s, options=option)
        print(">> ChromeDriverManager install ")
    except Exception as e:
        print(e)
        latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
        service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
        browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
        driver_executable_path = service.path
    return browser

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

    set_browser = "chrome"
    now_url = "https://open-demo.otcommerce.com"
    try:
        browser = connectDriverNew(now_url, "N", "N")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(now_url, "N", "N")
        print(">> connectDriverOld set OK ")

    time.sleep(1)
    browser.set_window_size(1200, 700)
    browser.set_window_position(140, 0, windowHandle='current')

    input(">> after Key :")

    proc_flg = "0"
    while proc_flg == "0":
        in_asin = input(">>asin :").strip()
        if in_asin == "":
            in_asin = input(">>Please asin :").strip()

        link_url = "https://open-demo.otcommerce.com/?p=item&id=" + str(in_asin)
        browser.get(link_url)
        time.sleep(random.uniform(2,5))
        result = browser.page_source
        soup = BeautifulSoup(result, 'html.parser')
        # print(soup)
        with open(os.getcwd()+"/log/result_taobao_demo_"+str(in_asin)+".html","w",encoding="utf8") as f:
            f.write(str(soup))

        opt_url = "https://open-demo.otcommerce.com/?q=product/get-configuration-info&id=" + str(in_asin)
        browser.get(opt_url)
        time.sleep(random.uniform(2,5))
        result_opt = browser.page_source
        soup_opt = BeautifulSoup(result_opt, 'html.parser')
        # print(soup)
        with open(os.getcwd()+"/log/result_taobao_demo_opt_"+str(in_asin)+".html","w",encoding="utf8") as f:
            f.write(str(soup_opt))


        time.sleep(random.uniform(2,5))
        data = {'current[property][1627207]:' : '28338', 'current[quantity]':'1' }
        headers = {
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + 'Safari/537.36',
            'Referer': str(link_url)
            }
        print(data)
        print(headers)

        # #data = 'spuId=' + str(asin)
        # print("--------------- ")
        # res_get = requests.get(req_link, headers=headers, data=data)
        # time.sleep(random.uniform(4,8))
        # print(res_get.status_code)
        
        #time.sleep(5)
        print("--------------- ")
        
        res_post = requests.post(opt_url, headers=headers, data=json.dumps(data))
        time.sleep(random.uniform(4,8))
        print(res_post.status_code)
        print(res_post.text)
        with open(os.getcwd()+"/log/result_taobao_demo_opt2_"+str(in_asin)+".html","w",encoding="utf8") as f:
            f.write(res_post.text)


        print(">>")
        #input(">>")

    print(">>")
    input(">> ")
