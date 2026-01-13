
# import time, random, requests

# siteName = "dev.freeship.co.kr"
# in_asin = "B000I5MNNO"
# onurl = "https://dev.freeship.co.kr/_GoodsUpdate/title_tran_best_option_image.asp?asin={}".format(in_asin)
# try:
#   opt_source_code = requests.get(onurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + ' Safari/537.36', 'Referer': 'https://' + str(siteName)})
# except Exception as e:
#   print("Exception")
#   time.sleep(random.uniform(1,1.5))

# else:
#   if opt_source_code.status_code == 200:
#     opt_html_str = opt_source_code.text
#   else:
#     print(">> else ")
#   print(">>opt_html_str: {}".format(opt_html_str))


import os
os.system('pip install --upgrade selenium')
import datetime, time, random
import multiprocessing
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def procTranConect(browser, in_asin, in_site, option_max_count, proc_flg):
    result_tran = ""
    if proc_flg == "option":
        tran_url = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_{}_option_image.asp?asin={}'.format(in_site, in_asin)
    else:
        tran_url = 'https://dev.freeship.co.kr/_GoodsUpdate/title_tran_{}.asp?asin={}'.format(in_site, in_asin)
    print(">> tran_url : {}".format(tran_url))
    
    try:
        browser.get(tran_url)
    except Exception as e:
        print('>> exception procTranConect ')
    else:
        time.sleep(random.uniform(7,8))
        # if option_max_count > 25:
        #     #moveScroll(browser)
        # time.sleep(1)
        result_tran = browser.find_element(By.ID,'google_translate_element').get_attribute("outerHTML")
        #result_tran = str(browser.page_source)
        #print(">> result_tran : {}".format(result_tran))
    return result_tran

if __name__ == '__main__':
  now_url = "https://dev.freeship.co.kr"
  browser = connectDriverOld(now_url, "", "")
  in_asin = "B000G2IGQC"
  procTranConect(browser, in_asin, "best", 0, "option")
  print("")