import os
os.system('pip install --upgrade selenium')
import DBmodule_NEW
import shein_func
import trend_func_asin
import socket
import time
import random
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller

global ver
ver = "1.25"

def procWork(in_ip):
    ip_catecode = ""
    sql = "select catecode from update_list where proc_ip = '{0}'".format(in_ip)
    rows = db_con.selectone(sql)
    if rows:
        ip_catecode = rows[0]
        print(">> [ " + str(in_ip) + " ] Catecode : " + str(ip_catecode))
        sql = "update update_list set regdate=getdate() where proc_ip='{0}'".format(in_ip)
        print(">> update_list (getdate) ")
        db_con.execute(sql)
    return "0"

# 카테고리 내 상품 url 리스트 들고오기
def getProdAsin(json_data,catecode,cate_code2):
    asinList = []

    # start_index = html.find("gbProductListSsrData = ")
    # end_index = html.find("</script>",start_index)
    for goods in json_data["results"]["goods"]:
        dic = dict()
        try:
            goods_url = shein_func.makeSheinProdUrl(goods["goods_url_name"],str(goods["goods_id"]),str(goods["cat_id"]))
        except:
            continue
        asin = goods["goods_id"]
        # title = goods["goods_name"]
        dic["asin"] = "'"+str(asin)+"'"
        # dic["title"] = "'"+title+"'"
        dic["url"] = "'"+goods_url+"'"
        dic["catecode"] = "'"+str(catecode)+"'"
        dic["cate_code2"] = "'"+str(cate_code2)+"'"
        asinList.append(dic)

    return asinList

def cateClick(driver, depth, big, middle, small, little, last,amz_cateurl, cate_code2, result):
    try:
        xpath_depth2 = '//*[@class="side-filter__item-content"]/div/section/label/span[{}]'
        xpath_depth3 = '//*[@class="side-filter__item-content"]/div/section/section/label/span[{}]'
        xpath_depth4 = '//*[@class="side-filter__item-content"]/div/section/section/section/label/span[{}]'
        xpath_depth5 = '//*[@class="side-filter__item-content"]/div/section/section/section/section/label/span[{}]'
        print("Depth-1 : {} click".format(big))
        driver.find_element(By.LINK_TEXT,big).click()
        if depth>=2:
            time.sleep(random.uniform(3,5))
            try:
                driver.find_element(By.CLASS_NAME,"side-filter__item-viewMore").click()
                time.sleep(random.uniform(3,5))
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
                time.sleep(random.uniform(1,3))
            print("Depth-2 : {} click".format(middle))
        if depth>=3:
            time.sleep(random.uniform(3,5))
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
                time.sleep(random.uniform(1,3))
            print("Depth-3 : {} click".format(small))
        if depth>=4:
            time.sleep(random.uniform(3,5))
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
                time.sleep(random.uniform(1,3))
            print("Depth-4 : {} click".format(little))
        if depth>=5:
            time.sleep(3)
            try:            
                driver.find_element(By.XPATH,xpath_depth5.format('text()="'+last+'"')).click()
                time.sleep(random.uniform(1,3))
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
                time.sleep(random.uniform(1,3))
            print("Depth-5 : {} click".format(last))
        now_url = driver.current_url
        if now_url.find(str(cate_code2)) > -1:
            print("정상 url")
        else:
            print("비정상 url 강제 {} 이동".format(amz_cateurl))
            driver.get(amz_cateurl)
            time.sleep(random.uniform(2,5))
    except:
        print("예외 상황 강제 {} 이동".format(amz_cateurl))
        time.sleep(random.uniform(8,15))
        #input(">> Input : ")
        driver.get(amz_cateurl)
        time.sleep(random.uniform(3,5))

        # 카테고리 작업완료처리
        proc_cate_end(db_con, result)
        time.sleep(random.uniform(2,3))

def get_asin_count():
    
    end_asin_cnt = 50000
    sql = "select endasin from python_version_manage where name='list' "
    end_chk = db_con.selectone(sql)
    if end_chk:
        end_asin_cnt = end_chk[0]
    return end_asin_cnt

def version_check():
    print(">> (PG) ver : " + ver)
    file_path = r"c:/project/"

    sql = "select version, url, pgFilename from python_version_manage where name = 'list'"
    print(">> sql:" + sql)
    rows = db_con.selectone(sql)
    if rows:
        version = rows[0]
        version_url = rows[1]
        pgFilename = rows[2]
        new_filename = file_path + pgFilename
        old_filename = file_path + str(pgFilename).replace("new_","")

        print(">> (DB) version : {} | version_url : {}" .format(version,version_url))
        if str(ver) != str(version):
            db_con.close()
            print(">> New version Download :" + str(version_url) + " | "+ str(new_filename))
            urllib.request.urlretrieve(version_url, new_filename)
            time.sleep(60)
            fileSize = os.path.getsize(new_filename)
            print(">> fileSize : {}".format(fileSize))

            if fileSize < 100000:
                time.sleep(60)
                fileSize = os.path.getsize(new_filename)
                print(">> fileSize : {}".format(fileSize))  

            if fileSize > 100000:
                time.sleep(5)
                if os.path.isfile(new_filename):
                    print(">> New File : {}".format(new_filename))
                    os.chmod(old_filename, 0o777)
                    print(">> OldFile chmod change Ok ")
            time.sleep(3)
            try:
                taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr : {}".format(taskstr))  
                os.system(taskstr)
            except Exception as e:
                print('>> taskkill Exception ')
            try:
                fname = os.path.abspath( __file__ )
                fname = trend_func_asin.getparseR(fname,"\\","")
                fname = fname.replace(".py",".exe")
                print(">> fname : {}".format(fname)) 
                time.sleep(5)
                taskstr2 = "taskkill /f /im " + fname + " /t" #프로세스명을 사용한 프로세스 종료
                print(">> taskstr2 : {}".format(taskstr2))  
                os.system(taskstr2)
            except Exception as e:
                print('>> taskkill Exception (2)')

            print(">> New version update exit")
            time.sleep(2)
            os._exit(1)

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

def moveScroll(driver, proc_cnt):
    SCROLL_PAUSE_SEC = 1
    sroll_cnt = 0
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_SEC)
    setHeight = 700
    while True:
        sroll_cnt = sroll_cnt + 1
        time.sleep(0.5)
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, {});".format(setHeight*sroll_cnt))
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(SCROLL_PAUSE_SEC)
        # if new_height == last_height:
        #     break
        if sroll_cnt > proc_cnt:
            break
        last_height = new_height

def proc_cate_end(db_con, result, flg='0'):
    sql = "delete from update_list where catecode = '{0}'".format(result['catecode'])
    db_con.execute(sql)
    print(">> delete (update_list) : {}".format(sql))   
    db_con.commit()

    if flg == "1":
        sql = "update T_CATEGORY set up_date = GETDATE(), ishidden = 'T' where catecode='{0}'".format(result['catecode'])    
    else:
        sql = "update T_CATEGORY set up_date = GETDATE() where catecode='{0}'".format(result['catecode'])
    print(">> update (T_CATEGORY) : {}".format(sql))   
    db_con.execute(sql)
    db_con.commit()


if __name__ == '__main__':    

    ip = socket.gethostbyname(socket.gethostname())
    if str(ip).find('222.104.189.18') == -1:
        try:
            taskstr = "taskkill /f /im chrome.exe /t" #프로세스명을 사용한 프로세스 종료
            print(">> taskstr : {}".format(taskstr))  
            os.system(taskstr)
        except Exception as e:
            print('>> taskkill Exception (1)')
        else:
            pass
    db_con = DBmodule_NEW.Database('trend',True)
    ip = socket.gethostbyname(socket.gethostname())

    # 버젼체크 (버젼 변경되었으면 새로운 버젼 다운로드 처리)
    if str(ip).strip() != "222.104.189.18":
        version_check()
    time.sleep(1)

    # driver = connectSubProcess()
    # time.sleep(3)
    # amz_cateurl = "https://asia.shein.com/"
    # driver.get(amz_cateurl)
    # time.sleep(random.uniform(3,5))
    # chrome 드라이브 실행
    now_url = "https://kr.shein.com"
    # try:
    #     print(">> connectDriverOld set ")
    #     driver = connectDriverOld(now_url, "", "")
    #     print(">> connectDriverOld set OK ")
    # except Exception as e:
    #     print(">> connectDriverNew set")
    #     driver = connectDriverNew(now_url, "", "")
    #     print(">> connectDriverNew set OK ")

    options = Options()
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    time.sleep(1)
    driver.get(now_url)
    # driver.set_window_size(1200, 900)
    # driver.set_window_position(140, 0, windowHandle='current')
    driver.implicitly_wait(3)
    time.sleep(2)

    first_chk = 1
    end_asin_cnt = 50000
    allCnt = 0
    while True:
        time_num = random.randint(2, 5)
        time.sleep(1)

        end_asin_cnt = get_asin_count()
        sql = "select count(*) as cnt from t_getasin"
        cnt_chk = db_con.selectone(sql)
        if cnt_chk:
            if int(cnt_chk[0]) > int(end_asin_cnt):
                print(">> t_getasin : {} | {} 이상 ".format(cnt_chk[0], end_asin_cnt))
                break

        allCnt = allCnt + 1
        procWork(ip)
        if allCnt % 20 == 0:
            # 버젼체크 (버젼 변경되었으면 새로운 버젼 다운로드 처리)
            if str(ip).strip() != "222.104.189.18":
                version_check()
            time.sleep(1)

        result = trend_func_asin.newlist(db_con,ip)
        catecode = result["catecode"]
        cate_code2 = result["cate_code2"]
        page_num = result["page"]
        amz_cateurl = result["url"]
        big = result["big"]
        middle = result["middle"]
        small = result["small"]
        little = result["little"]
        last = result["last"]
        depth = result["depth"]    
        amz_cateurl = amz_cateurl.replace('asia.shein.com','kr.shein.com')

        if first_chk==1 or page_num==1:
            cateClick(driver, depth, big, middle, small, little, last, amz_cateurl, cate_code2, result)
            first_chk=0
        else:
            try:
                driver.find_element(By.CSS_SELECTOR,"span.sui-pagination__next.sui-pagination__btn.sui-pagination__hover").click()
                print("다음 페이지")
            except:
                # 카테고리 작업완료처리
                proc_cate_end(db_con, result)
                continue
        print("amz_cateurl : "+ amz_cateurl + ", now page : " + str(page_num))
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        product_list_all = ""
        product_list = ""
        try:
            product_list_all = soup.select_one("section.product-list-v2__section")
            product_list = product_list_all.select("div > section")
        except:
            print("새로고침")
            driver.refresh()
            time.sleep(random.uniform(5,10))
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')    
            try:                
                product_list_all = soup.select_one("section.product-list-v2__section")
                product_list = product_list_all.select("div > section")
            except:                
                input("캡챠 확인 :")
                html = driver.page_source
                soup = BeautifulSoup(html,'html.parser')                 
                product_list_all = soup.select_one("section.product-list-v2__section")
                product_list = product_list_all.select("div > section")

        if len(product_list)==0:
            time.sleep(1)
            driver.refresh()
            time.sleep(random.uniform(2,5))
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            try:                
                product_list_all = soup.select_one("section.product-list-v2__section")
                product_list = product_list_all.select("div > section")
            except: 
                print(">> product_list_all except (SKIP)")

        if len(product_list)==0:
            # sql = "delete from update_list where catecode = '{0}'".format(result['catecode'])
            # db_con.execute(sql)
            print("상품없음 NEXT")
            # 카테고리 작업완료처리
            proc_cate_end(db_con, result, "1")
        else:
            # scroll 
            try:
                moveScroll(driver, random.uniform(2,5))
            except:
                pass
            
            asinList = []
            for product_item in product_list:
                dic = dict()
                try:
                    temp = product_item["data-expose-id"].split("-")
                    goods_url = product_item.select_one("div.product-card__top-wrapper > a")["href"]
                    if len(goods_url)>1000:
                        continue
                except:
                    continue
                asin = temp[1]
                # title = goods["goods_name"]
                dic["asin"] = "'"+str(asin)+"'"
                # dic["title"] = "'"+title+"'"
                dic["url"] = "'"+goods_url+"'"
                dic["catecode"] = "'"+str(catecode)+"'"
                dic["cate_code2"] = "'"+str(cate_code2)+"'"
                asinList.append(dic)
            try:
                row = 0
                for asin in asinList:
                    sql_chk = "select top 1 asin from t_getasin where asin={}".format(asin["asin"])
                    chk = db_con.selectone(sql_chk)
                    if chk:
                        continue

                    # sql_chk3 = "select top 1 ali_no asin from t_goods where ali_no={}".format(asin["asin"])
                    # chk3 = db_con.selectone(sql_chk3)
                    # if chk3:
                    #     continue
                    sql_chk3 = "select top 1 ali_no, isnull(asin_url,'') asin from t_goods where ali_no={}".format(asin["asin"])
                    chk3 = db_con.selectone(sql_chk3)
                    if chk3:
                        db_ali_no = chk3[0]
                        db_asin_url = chk3[1]
                        if db_asin_url == "":
                            sql_u = " update t_goods set asin_url={}, cate_idx = {}, cate_code2 = {} where ali_no={}".format(asin["url"],asin["catecode"],asin["cate_code2"],asin["asin"])
                            print(">> t_goods: url update : {}".format(asin["asin"]))
                            db_con.execute(sql_u)
                            db_con.commit()
                        continue

                    sql_chk2 = "select top 1 option_code asin from t_goods_option where option_code={}".format(asin["asin"])
                    chk2 = db_con.selectone(sql_chk2)
                    if chk2:
                        continue

                    row = row + 1
                    print(">> ({}) 입력 {} | {} | {} ".format(row,asin["asin"],asin["catecode"],asin["cate_code2"]))
                    print(">> t_getasin insert : {}".format(asin["asin"]))
                    db_con.insert("t_getasin", asin)

                sql = "update update_list set now_page = now_page + 1, regdate = getdate() where catecode = '{0}' and proc_ip = '{1}'".format(result['catecode'],ip)
                db_con.execute(sql)
                if asin != "":
                    try:
                        driver.get(asin)
                    except:
                        pass
                    else:
                        time.sleep(random.uniform(2,5))

            except Exception as ex:
                print(ex)
                print("===break point===")
                print("[{}] {} | {}".format(asin["asin"],page_num,amz_cateurl))
                # 카테고리 작업완료처리
                proc_cate_end(db_con, result, "1")
                print("Exception NEXT")
                # db_con.close()
                break

    db_con.close()
    driver.quit()
    os._exit(0)