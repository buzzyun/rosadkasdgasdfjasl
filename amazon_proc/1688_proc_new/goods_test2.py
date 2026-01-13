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
    now_url = "https://www.dcbuy.co.kr"
    try:
        browser = connectDriverNew(now_url, "N", "N")
    except Exception as e:
        print(">> connectDriverOld set ")
        browser = connectDriverOld(now_url, "N", "N")
        print(">> connectDriverOld set OK ")

    time.sleep(1)
    browser.set_window_size(1200, 700)
    browser.set_window_position(140, 0, windowHandle='current')

    proc_flg = "0"
    while proc_flg == "0":
        in_asin = input(">>asin :").strip()
        if in_asin == "":
            in_asin = input(">>Please Input asin :").strip()
        asin = in_asin
        link_url = "https://www.dcbuy.co.kr/mall/detail/" +str(asin)+ "?origin="
        req_link = "https://www.dcbuy.co.kr/api/product/productDetail"

        data = {'spuId' : str(asin) }
        headers = {
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json;charset=UTF-8', 
            'X-Language': 'ko',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.random()) + 'Safari/537.36',
            'Referer': str(link_url)
            }
        #print(data)
        #print(headers)
        print("\n\n ------------------------------------------------------------ ")

        try:
            res_post = requests.post(req_link, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(e)
        else:
            time.sleep(random.uniform(4,8))
            # print(res_post.status_code)
            if res_post.status_code == 200:
                org_result = str(res_post.text)
                result_goods = org_result.replace('\\r\\n',' ').replace('\\','').replace('  ',' ').strip()
                with open(os.getcwd() + "/log/1688_result"+str(asin)+".html","w",encoding="utf8") as f: 
                    f.write(str(result_goods))

                rtnMsg = getparse(result_goods,'errMsg":"','"')
                offerId = getparse(result_goods,'offerId":',',')
                categoryId = getparse(result_goods,'categoryId":',',')
                subject = getparse(result_goods,'subject":"','"')
                print(">> subject : {}".format(subject))
                description = getparse(result_goods,'description":"','"productImage"').replace('\\','')
                if description.find('","mainVideo":') > -1:
                    description = getparse(description,'','","mainVideo":')
                with open(os.getcwd() + "/log/1688_description"+str(asin)+".html","w",encoding="utf8") as f: 
                    f.write(str(description))

                images = getparse(result_goods,'"images":[',']}')
                print(">> images : {}".format(images))
                
                productSkuInfos = getparse(result_goods,'productSkuInfos":[','"productSaleInfo"')
                spSku = productSkuInfos.split('}]}')

                option_value_dic = dict()
                option_price_dic = dict()
                option_skuid_dic = dict()
                option_image_dic = dict()
                for ea_sku in spSku:
                    sku_id = getparse(ea_sku,'skuId":"','"')
                    if sku_id != "":
                        sku_stock = getparse(ea_sku,'amountOnSale":"','"')
                        price = getparse(ea_sku,'price":"','"')
                        jxhyPrice = getparse(ea_sku,'jxhyPrice":',',')
                        if price == "":
                            sku_price = jxhyPrice
                        else:
                            sku_price = price
                        sku_img = getparse(ea_sku,'skuImageUrl":"','"')
                        sttrSku = ea_sku.split('},{')
                        tmp_attrId = ""
                        tmp_attrVlue = ""
                        for ea_attr in sttrSku:
                            attrValue = getparse(ea_attr,'value":"','"')
                            if tmp_attrVlue != "":
                                tmp_attrVlue = tmp_attrVlue + ":" + attrValue
                            else:
                                tmp_attrVlue = attrValue
                        if sku_stock == "0":
                            print(">> [{}] (품절) {} | {} ({}) {}".format(sku_id, tmp_attrVlue, sku_price, sku_stock, sku_img))
                        else:
                            print(">> [{}] {} | {} ({}) {}".format(sku_id, tmp_attrVlue, sku_price, sku_stock, sku_img))

                        option_value_dic[sku_id] = tmp_attrVlue
                        option_price_dic[sku_id] = sku_price
                        option_image_dic[sku_id] = sku_img

                #print(">> option_value_dic : {}".format(option_value_dic))
                #print(">> option_price_dic : {}".format(option_price_dic))
                #print(">> option_image_dic : {}".format(option_image_dic))

                priceRangeList = getparse(result_goods,'priceRangeList":[',']')
                startQuantity = getparse(priceRangeList,'startQuantity":"','"')
                print(">> startQuantity : {}".format(startQuantity))

                price = getparse(priceRangeList,'price":"','"')
                print(">> price : {}".format(price))
                sellerOpenId = getparse(result_goods,'sellerOpenId":"','"')
                minOrderQuantity = getparse(result_goods,'minOrderQuantity":"','"')
                print(">> minOrderQuantity : {}".format(minOrderQuantity))
                if int(minOrderQuantity) > 2:
                    print(">> minOrderQuantity 2 Over : {}".format(minOrderQuantity))

                status = getparse(result_goods,'status":"','"')
                if status == "published":
                    print(">> status : {}".format(status))
                else:
                    print(">> status : {}".format(status))
                asinLink = getparse(result_goods,'link":"','"')
                print(">> asinLink : {}".format(asinLink))

            print(">>")


### https://www.dcbuy.co.kr/api/product/productDetail 
### "skuAttributes":[  --> 옵션 
### {"amountOnSale":"0" --> 재고 없는 옵션 
### {"startQuantity":"2","price":"13.9"}  / "minOrderQuantity":"2"  --> 최소수량 2개이상 
'''

'{"code":200,"errorCode":"2000","errMsg":"success",

"data":{"offerId":676651652931,

"subject":"RosyPosy 전용 시리즈 눈물 종이 5 색 내부 페이지 계획 노트북 두꺼운 하단 스케치 패드",


"description":"<div id=\\"offer-template-0\\"></div><p style=\\"text-align: center;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01YcyLcm21zhLSBfEr7_!!3330047056-0-cib.jpg\\" alt=\\"lADPDg7mR5-WgofNASHNAu4_750_28\\"/></p>\\r\\n<p style=\\"text-align: center;\\"><span style=\\"font-size: 26.0pt;\\">箱规\xa0<span style=\\"color: #ff0000;\\">40本/件</span></span></p>\\r\\n<p style=\\"text-align: center;\\"><span style=\\"font-size: 26.0pt;\\">最低零售限价：<span style=\\"color: #ff0000;\\">22.9元</span></span></p>\\r\\n<p style=\\"text-align: center;\\"><span style=\\"font-size: 26.0pt;color: #ff0000;\\">低于限价销售，停止供货，投诉不撤</span></p>\\r\\n<p style=\\"text-align: center;\\"><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01jlMF0621zhP0NzfYx_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01WIaaKh21zhP2nB7a6_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN019epUuE21zhP78fCi6_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01XyxwRD21zhOxJb1Nx_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01HQIFsW21zhR6qMIqU_!!3330047056-0-cib.jpg?__r__=1669343376214\\" alt=\\"undefined\\"/><br class=\\"img-brk\\"/><br class=\\"img-brk\\"/><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01eoB1Yw21zhP98OvZy_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01PnCOUP21zhOqqWAw2_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01dliJcK21zhP7v9goc_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN015U43ex21zhP53p0th_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01zU0JMt21zhOxJZoXt_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01wbtg3W21zhP1DQ1Rr_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01spCs5S21zhOvklzmA_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01roe0YA21zhP5tbJjS_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01YcqTjw21zhP53rxvk_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01OxYqyT21zhP0O4ZF8_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01MBXQUo21zhP0O4ZFS_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN015HRJXy21zhOqqZCDu_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><span style=\\"font-size: 26.0pt;\\"><img src=\\"https://cbu01.alicdn.com/img/ibank/O1CN01aNls3M21zhOy2siks_!!3330047056-0-cib.jpg\\" alt=\\"undefined\\"/></span><br/><br/><br/><br/></p>","mainVideo":"https://cloud.video.taobao.com/play/u/3330047056/p/1/e/6/t/1/365777946116.mp4","detailVideo":null,"productImage":{"images":["https://cbu01.alicdn.com/img/ibank/O1CN01AGwXXl21zhP0URFzQ_!!3330047056-0-cib.jpg","https://cbu01.alicdn.com/img/ibank/O1CN01dqfeNG21zhP97Rujs_!!3330047056-0-cib.jpg","https://cbu01.alicdn.com/img/ibank/O1CN01ynQzyB21zhP97OtgS_!!3330047056-0-cib.jpg","https://cbu01.alicdn.com/img/ibank/O1CN015RrDgd21zhP0MvXcE_!!3330047056-0-cib.jpg","https://cbu01.alicdn.com/img/ibank/O1CN015befmQ21zhP0MwDDj_!!3330047056-0-cib.jpg"]},


"productSkuInfos":[
{"amountOnSale":"1030","price":"14.9","jxhyPrice":null,"skuId":"4878065068300","specId":"b222c2964434b1ab3e92753338fa6af2","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"B5 수평선","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01qYqdHh21zhP9zXovN_!!3330047056-0-cib.jpg"}]},

{"amountOnSale":"591","price":"14.9","jxhyPrice":null,"skuId":"4878065068295","specId":"c770735a4c7fa31037d62bd14e34bbf3","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"B5 광장","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01TO6Rq621zhP47DIIe_!!3330047056-0-cib.jpg"}]},

{"amountOnSale":"825","price":"14.9","jxhyPrice":null,"skuId":"4878065068298","specId":"4d951fbb8fed08673ddd6bb1d2b37473","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"B5 공백","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01fCsJVe21zhP47Eu5Z_!!3330047056-0-cib.jpg"}]},

{"amountOnSale":"145","price":"13.9","jxhyPrice":null,"skuId":"4878065068296","specId":"132d73687bfeb645b8af2316e20427fe","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"A5 수평선","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01VW5ap421zhPcsB3p6_!!3330047056-0-cib.jpg"}]},

{"amountOnSale":"0","price":"13.9","jxhyPrice":null,"skuId":"4878065068299","specId":"6490904c6269fa48d8ba74ca9e99b7df","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"A5 광장","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN013RTwUO21zhPcsAFwr_!!3330047056-0-cib.jpg"}]},

{"amountOnSale":"0","price":"13.9","jxhyPrice":null,"skuId":"4878065068297","specId":"76bdf816bd8d9a50125975972141478a","skuAttributes":[{"attributeId":100019517,"attributeName":"커버 색상","value":"A5 공백","skuImageUrl":"https://cbu01.alicdn.com/img/ibank/O1CN01U16RAi21zhPlwHtOB_!!3330047056-0-cib.jpg"}]}
]

,"productSaleInfo":{"priceRanges":null,"amountOnSale":"2591",
"priceRangeList":[{"startQuantity":"2","price":"13.9"}],
"quoteType":"1","consignPrice":null,"jxhyPrice":null},"isJxhy":false,
"sellerOpenId":"BBBspz8Z4AmsyZ5SmwYL4Xi_A","minOrderQuantity":"2","batchNumber":null,"status":"published",
"link":"https://detail.1688.com/offer/676651652931.html","sellerMixSetting":{"generalHunpi":true,"mixAmount":"100","mixNumber":"2"}},
"success":true,"xtraceId":"1828354a-d948-4b4a-a33a-491a0ee1db32"}'

'''