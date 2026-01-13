import sys
import datetime
import random
import socket
import requests
import json
import time
import socket
import os
import urllib
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import subprocess
import shutil
import DBmodule_FR

in_ver = "9.65"
currIp = socket.gethostbyname(socket.gethostname())
print('>> currIp : '+str(currIp))
global procCnt

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
    # Selenium 4.0 - load webdriver

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

def repleaseDesc(tmp_desc, findStr, endStr):
    sp_desc = str(tmp_desc).split(findStr)
    for line_desc in sp_desc:
        line_desc = getparse(line_desc,'',endStr)
        if line_desc[:10].find('<img ') > -1:
            rel_line_desc = findStr + line_desc + endStr
            tmp_desc = tmp_desc.replace(rel_line_desc,'')
    return tmp_desc

def goodsProc(browser, db_con):

    test_asin = input(">> Test Asin:")
    sp_asin = test_asin.split('@')

    asin = sp_asin[0]
    catecode = sp_asin[1]
    isTmall = sp_asin[2]
    guid = sp_asin[3]
    goods_url = "https://open-demo.otcommerce.com/?p=item&id=" + str(asin)
    print(">> goods_url : {}".format(goods_url))

    time.sleep(2)
    language = "ko"
    instanceKey = "1a8389aa-f246-4e24-8e87-de6f89806c6e"
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    print(">> isTmall : {}".format(isTmall))
    base_url = "http://otapi.net/service-json/BatchGetItemFullInfo?instanceKey="+str(instanceKey)+"&language=" +str(language)+ "&signature=&timestamp=&sessionId=&itemParameters=&itemId=" +str(asin) + \
    "&blockList=Description&blockList=RootPath&blockList=DeliveryCosts&blockList=ProviderReviews&blockList=MostPopularVendorItems16"

    res = requests.get(base_url, headers=headers)
    time.sleep(4)
    if res.status_code != 200:
        print("Can't request website")
        return "E99"
    else:
        #soup = BeautifulSoup(res.text, "html.parser")
        dataResult = json.loads(res.text)
        #print(dataResult)
        print("\n")
        if dataResult['ErrorCode'] != "Ok":
            print(">> {} : Item Not Found : {} ".format(asin, dataResult['ErrorCode']))
            print('>> 품절 (Skip) : {}'.format(asin))
            return "D01" # 품절

        itemId = asin
        base_min_price = 0
        base_top_price = 0
        option_val_count = 0

        result_dic = dict()
        result = dataResult['Result']
        result_item = result['Item']

        result_dic['api_UpdatedTime'] = None
        result_dic['api_CreatedTime'] = None
        if result_item.get('UpdatedTime'):
            print('>> api item UpdatedTime : {}'.format(result_item['UpdatedTime']))
            result_dic['api_UpdatedTime'] = result_item['UpdatedTime']
        if result_item.get('CreatedTime'):
            print('>> api item CreatedTime : {}'.format(result_item['CreatedTime']))
            result_dic['api_CreatedTime'] = result_item['CreatedTime']

        result_dic['api_sell_reason'] = ''
        if result_item['IsSellAllowed'] == False:
            print('>> 판매자 사유 sell not allowed : {}'.format(itemId))
            if result_item.get('SellDisallowReason'):
                print('>> 판매자 사유 : {}'.format(result_item['SellDisallowReason']))
                TaobaoItemUrl = result_item['TaobaoItemUrl']  
                print(">> TaobaoItemUrl : {}".format(TaobaoItemUrl))
                if result_item['SellDisallowReason'] == 'IsNotDeliverable':
                    print('>> 판매자 사유 IsNotDeliverable (OK) : {}'.format(result_item['SellDisallowReason']))
                    result_dic['api_sell_reason'] = '1'
                elif result_item['SellDisallowReason'] == 'IsInStock':
                    print('>> 판매자 사유 IsInStock (Skip) : {}'.format(result_item['SellDisallowReason']))
                    return "D71" # 품절
                else:
                    print('>> 판매자 사유 else (Skip) : {}'.format(result_item['SellDisallowReason']))
                    return "D71" # 품절

        #print(">> VendorItems : {}".format(VendorItems))

        Id = result_item['Id']
        Title = result_item['Title']
        OriginalTitle = result_item['OriginalTitle']
        CategoryId = result_item['CategoryId']
        ExternalCategoryId = result_item['ExternalCategoryId']

        print(">> Id : {}".format(Id))
        print(">> Title : {}".format(Title))
        #print(">> OriginalTitle : {}".format(OriginalTitle))
        print(">> CategoryId : {}".format(CategoryId))
        print(">> ExternalCategoryId : {}".format(ExternalCategoryId))

        ########### title Check ###########
        Title = Title.replace('정품','').replace("'","`")
        result_dic['DE_title'] = OriginalTitle.replace("'","`")
        Title = str(Title).replace("  ", " ").strip()
        print('>> tran_title (final) : ' + str(Title[:80]))
        if str(Title).strip() == "":
            print('>> No Title ')
            return "D02"
        if len(Title) < 5:
            print('>> Title len < 5 ')
            return "D02"

        MainPictureUrl = result_item['MainPictureUrl']  
        StuffStatus = result_item['StuffStatus']   #Item condition - New: New | Unused: Unused | Second: Second-hand | Another: Another
        print(">> StuffStatus : {}".format(StuffStatus))
        if str(StuffStatus) == "New":
            print(">> New (새상품) : {}".format(StuffStatus))
        else:
            print(">> (Buy used) Unsellable product : {}".format(StuffStatus))
            return "D04"

        mainPrice = result_item['Price']['OriginalPrice']
        MarginPrice = result_item['Price']['MarginPrice']
        if float(mainPrice) != float(MarginPrice):
            print(">>(확인필요) mainPrice : {} / MarginPrice : {}".format(mainPrice, MarginPrice))
        DeliveryPrice = result_item['Price']['DeliveryPrice']['OriginalPrice']
        if float(DeliveryPrice) > 0:
            print(">> DeliveryPrice : {}".format(DeliveryPrice))
            result_dic['taobao_shipping'] = 'T'
            if float(DeliveryPrice) > 25:
                print(">> shipping price over: {} | {} ".format(itemId, DeliveryPrice))
                #### return "D11" + " ( " + str(DeliveryPrice) + " )"  # shipping_price 25 위안 (SKIP)
        else:
            result_dic['taobao_shipping'] = 'F'

        Pictures = result_item['Pictures']  
        Attributes = result_item['Attributes']     
        ConfiguredItems = result_item['ConfiguredItems']

        Weight = "0"
        Actual_Weight = "0"
        if result_item.get('WeightInfos'):
            if result_item.get('WeightInfos') != []:
                Weight = result_item['WeightInfos'][0]['Weight']
        if result_item.get('ActualWeightInfo'):    
            Actual_Weight = result_item['ActualWeightInfo']['Weight']
        if float(Weight) > 0:
            print(">> Weight : {}".format(Weight))
        if float(Actual_Weight) > 0:
            print(">> Actual_Weight : {}".format(Actual_Weight))
            if float(Actual_Weight) > 1:
                print(">> Actual_Weight : {}".format(Actual_Weight))
        print(">> mainPrice : {}".format(mainPrice))
        print(">> MarginPrice : {}".format(MarginPrice))

        ##### price check #####
        if float(mainPrice) < 1:
            print('>> 1 위안 미만 (skip)')
            return "D12" + " ( " + str(mainPrice) + " ) "  # 1 위안 미만

        if float(mainPrice) > 8000:
            print('>> 8000 위안 (150만원) over (skip)')
            return "D09" + " ( " + str(mainPrice) + " 위안) "  # 8000 위안 over

        print(">> Main Img MainPictureUrl : {}".format(MainPictureUrl))

        other_img_set = []
        imgCnt = 0
        if Pictures:
            for ea_other_img in Pictures:
                ea_img = ea_other_img['Large']['Url']
                print(">> ea_img : {}".format(ea_img))
                imgCnt = imgCnt + 1

        Description = ""
        BrandId = ""
        BrandName = ""
        #FeaturedValues = ""
        #FeaturesTmp = ""
        if result_item.get('BrandId'):  BrandId = result_item['BrandId']  
        if result_item.get('BrandName'):  BrandName = result_item['BrandName']
        if result_item.get('Description'):  Description = result_item['Description']
        #if result_item.get('FeaturedValues'):  FeaturedValues = result_item['FeaturedValues']
        #if result_item.get('Features'):  FeaturesTmp = result_item['Features']  

        #print(">> BrandId : {}".format(BrandId))
        print(">> BrandName : {}".format(BrandName))
        #print(">> FeaturedValues : {}".format(FeaturedValues))
        #print(">> FeaturesTmp : {}".format(FeaturesTmp))
        TaobaoItemUrl = result_item['TaobaoItemUrl']  
        print(">> TaobaoItemUrl : {}".format(TaobaoItemUrl))

        if str(Description).find('<p style="margin: 0;overflow: hidden;"') > -1:
            Description = repleaseDesc(Description, '<p style="margin: 0;overflow: hidden;"','</p>')
        elif str(Description).find('<p style="margin: 0 0 5.0px 0;overflow: hidden;">') > -1:
            Description = repleaseDesc(Description, '<p style="margin: 0 0 5.0px 0;overflow: hidden;">','</p>')
        elif str(Description).find('<p style="margin:0 0 5.0px 0;width:0;height:0;overflow:hidden;">') > -1:
            Description = repleaseDesc(Description, '<p style="margin:0 0 5.0px 0;width:0;height:0;overflow:hidden;">','</p>')
        else:
            print(">> Description Ok ")


        #print(">> Description : {}".format(Description))
        base_min_price = mainPrice
        base_top_price = mainPrice
        
        option_value_tran_arr = []
        tran_title = ""
        tran_option = ""
        option_image_dic = dict()
        features = ""
        features_org = ""
        f_pid = ""
        f_vid = ""
        PropertyValue = ""
        if Attributes:
            for ea_item in Attributes:
                ImageUrl = ""
                f_pid = ea_item['Pid']
                if not ea_item.get('Vid'):
                    print(">> ea_item No Vid : {}".format(ea_item))
                    f_vid = ""
                else:
                    f_vid = ea_item['Vid']
                f_IsConfigurator = ea_item['IsConfigurator']
                PropertyName = ea_item['PropertyName']
                
                if not ea_item.get('Value'):
                    print(">> ea_item No Value : {}".format(ea_item))
                    PropertyValue = ""
                else:
                    if ea_item.get('ValueAlias'):
                        PropertyValue = ea_item['ValueAlias']
                    else:
                        PropertyValue = ea_item['Value']

                if f_IsConfigurator == True:
                    if ea_item.get('ImageUrl'):
                        ImageUrl = ea_item['ImageUrl']
                        if ea_item.get('ValueAlias'):
                            image_name = ea_item['ValueAlias']
                        else:
                            image_name = ea_item['Value']
                        if PropertyName == '크기' or PropertyName == '신발 사이즈':
                            pass
                            #print(">> (skip) ImageUrl : {} | {}".format(image_name, ImageUrl))
                        else:
                            option_image_dic[image_name] = ImageUrl
                            #print(">> ImageUrl : {} | {}".format(image_name, ImageUrl))
                    else:
                        pass
                else:
                    if str(PropertyName) == "가격표":
                        pass
                    else:
                        if str(features).find(PropertyName) > -1:
                            features = features + '  ' + PropertyValue
                        else:
                            features = features + str('<li> ') + PropertyName + str(' : ') + PropertyValue + str('</li>')
                        if str(features_org).find(f_pid) > -1:
                            features_org = features_org + '  ' + f_vid
                        else:
                            features_org = features_org + str('<li> ') + f_pid + str(' : ') + f_vid + str('</li>')

        #print("\n>> option_image_dic : \n{}".format(option_image_dic))
        #print("\n>> features_org : \n{}".format(features_org))
        if features == "" and BrandName != "":
            features = str('● Brand : ') + BrandName 
        #print("\n>> features : \n{}".format(features))
        result_dic['feature'] = features

        option_check = ""
        option_list = []
        option_value_dic = dict()
        option_price_dic = dict()
        opt_cnt = 0
        if ConfiguredItems:
            print("\n>> Option item :\n")
            option_check = "1"
            option_min_price = 0
            option_max_price = 0
            result_dic['OptionKind'] = '300'
            result_dic['many_option'] = '1'
            for ea_value in ConfiguredItems:
                option_dic = dict()
                option_value_tran_dic = dict()
                opt_cnt = opt_cnt + 1
                #print(">> ea_value[{}] : {}".format(opt_cnt, ea_value))
                val_id = ea_value['Id']
                Quantity = ea_value['Quantity'] # 현재 구성의 항목 수량
                SalesCount = ea_value['SalesCount'] # 품목 판매 건수
                Configurators = ea_value['Configurators']
                valPrice = ea_value['Price']['OriginalPrice'] # 공급자의 원래 가격

                if float(Quantity) == 0:
                    print("({}) [{}] Sold Out ".format(opt_cnt, val_id))
                else:
                    option_dic['option_id'] = val_id
                    option_dic['option_price'] = valPrice
                    option_dic['option_qty'] = Quantity
                    option_price_dic[val_id] = valPrice
                    option_dic['option_stock'] = Quantity
                    option_name = ""
                    org_option_name = ""
                    option_code = ""

                    #옵션 가격 처리
                    if option_min_price == 0 :
                        option_min_price = valPrice
                    else:
                        if option_min_price > valPrice:
                            option_min_price = valPrice
                    if option_max_price == 0 :
                        option_max_price = valPrice
                    else:
                        if option_max_price < valPrice:
                            option_max_price = valPrice                    

                    for ea_val in Configurators:
                        c_Pid = ea_val['Pid']
                        c_Vid = ea_val['Vid']
                        option_code = c_Pid + ":" + c_Vid
                        if Attributes:
                            for ea_item in Attributes:
                                #print(">> ea_item[{}] : {}".format(opt_cnt, ea_item))
                                a_pid = ea_item['Pid']
                                a_IsConfigurator = ea_item['IsConfigurator']
                                #if str(a_pid).isdigit() == True:
                                if a_IsConfigurator == True:
                                    a_Vid = ea_item['Vid']
                                    if c_Pid == a_pid and c_Vid == a_Vid:
                                        if option_name != "":
                                            if ea_item.get('ValueAlias'):
                                                option_name = option_name + " | " + ea_item['ValueAlias']
                                            else:
                                                option_name = option_name + " | " + ea_item['Value']
                                            PropertyName = PropertyName + " | " + ea_item['PropertyName']
                                            org_option_name = org_option_name + " | " + ea_item['OriginalValue']
                                            option_code = option_code + ":" + a_pid + ":" + a_Vid
                                        else:
                                            if ea_item.get('ValueAlias'):
                                                option_name = ea_item['ValueAlias']
                                            else:
                                                option_name = ea_item['Value']
                                            PropertyName = ea_item['PropertyName']
                                            org_option_name = ea_item['OriginalValue']
                                            option_code = a_pid + ":" + a_Vid
                                        break

                                    if org_option_name != "":
                                        if str(org_option_name).find('定金') > -1: # 보증금 체크
                                            print('>> 定金 (보증금) {}'.format(itemId))
                                            return "D47"
                                        if str(org_option_name).find('尾款') > -1: # 결제
                                            print('>> 尾款 (결제) {}'.format(itemId))
                                            return "D47"
                                    if option_name.find("화물") > -1 or option_name.find("계약") > -1 or option_name.find("보증") > -1 or option_name.find("예약") > -1 or option_name.find("경매") > -1 or \
                                        option_name.find("무료배송") > -1 or option_name.find("무료 배송") > -1 or option_name.find("환불 불가") > -1 or option_name.find("환불불가") > -1 or \
                                        option_name.find("반품 불가") > -1 or option_name.find("반품불가") > -1 or option_name.find("선주문") > -1 or option_name.find("도착 예정") > -1 or \
                                        option_name.find("위안") > -1 or option_name.find("보증") > -1 or option_name.find("사전 판매") > -1 or option_name.find("인증서") > -1 \
                                        or option_name.find("본인 부담") > -1 or option_name.find("배송 불가") > -1:
                                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(option_name))
                                        return "D47"
                                    if option_name.lower().find("guarantee") > -1 or option_name.find("reservation") > -1 or option_name.find("contract") > -1 or option_name.find("freight") > -1 or option_name.find("auction") > -1:
                                        print('>> Unsellable option word ( 옵션명 불가단어 포함 ) : {}'.format(option_name))
                                        return "D47"

                    if option_name != "":
                        option_val_count = option_val_count + 1
                        option_dic['option_name'] = option_name.strip()
                        option_dic['option_originalname'] = org_option_name
                        option_dic['option_code'] = option_code
                        option_value_dic[val_id] = option_name
                        option_list.append(option_dic)

                        print("({}) [{}] {}  ( {} ) [ 수량:{} ]".format(opt_cnt, val_id, option_name , valPrice , Quantity))
                        if option_val_count > 150:
                            print('>> 옵션 갯수 150개 이상 (Skip) : {}'.format(option_val_count))
                            break
                    else:
                        print(">> No option_name ")

            if option_val_count == 0:
                # No Option
                print(">> Ooption_val_count = 0 : {}".format(itemId))
                print('>> Ooption_val_count = 0 (Option sold out) ')
                return "D07"

            print(">> Option_val_count : {}".format(option_val_count))
            print(">> option_value_dic : {}".format(option_value_dic))
            print(">> option_price_dic : {}".format(option_price_dic))
            print(">> option_image_dic : {}".format(option_image_dic))

            min_price = min(option_price_dic.values())
            top_price = max(option_price_dic.values())
            print(">> min_price : {}".format(min_price))
            print(">> top_price : {}".format(top_price))
            if min_price == 0 or min_price == 0.0:
                pass
            else:
                base_min_price = min_price
            if top_price == 0 or top_price == 0.0:
                pass
            else:
                base_top_price = top_price

        else:
            print("\n>> No Option Goods \n")
            option_check = "0"
            result_dic['OptionKind'] = None
            result_dic['many_option'] = '0'


    # try:
    #     browser.get(goods_url)
    #     print(">> page_source ")
    # except Exception as e:
    #     print(">> Connect Error (SKIP): {}".format(goods_url))
    #     return "1"  
    # else:
    #     time.sleep(random.uniform(4,6))
    #     print(">> time.sleep(random.uniform(4,6)) ")
    #     result = str(browser.page_source)

    print(">> ")
    return "0"

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    timecount = 0

    # now_url = "https://open-demo.otcommerce.com"
    # try:
    #     shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
    # except FileNotFoundError:
    #     pass

    # filePath_86 = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    # filePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"'
    # # Open the debugger chrome
    # try:
    #     proc_id = subprocess.Popen(filePath_86)
    # except FileNotFoundError:
    #     proc_id = subprocess.Popen(filePath)

    # option = Options()
    # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # driver_path = f'./{chrome_ver}/chromedriver.exe'
    # if os.path.exists(driver_path):
    #     print(f"chrom driver is insatlled: {driver_path}")
    # else:
    #     print(f"install the chrome driver(ver: {chrome_ver})")
    #     chromedriver_autoinstaller.install(True)
    # browser = webdriver.Chrome(options=option)
    # # browser.set_window_size(1200, 900)
    # # browser.set_window_position(140, 0, windowHandle='current')
    # browser.implicitly_wait(3)
    # time.sleep(2)   
    # browser.get("https://open-demo.otcommerce.com/")

    # input(">> After Login : ")

    browser = ""
    db_con = DBmodule_FR.Database('taobao')
    procFlg = "0"
    while procFlg == "0":
        rtnFlg = goodsProc(browser, db_con)
        if rtnFlg == "1":
            procFlg = "1"

    time.sleep(1)
    db_con.close()
    print(">> End ")