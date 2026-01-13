from selenium import webdriver
import chromedriver_autoinstaller
import random
import urllib
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os,socket
import time
import DBmodule_FR

# 파싱함수
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

# 파싱함수 (뒤에서 부터 찾아서 파싱)
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

def makeBestKeyword(naver_catecode,keyword,ranking):
    dic = dict()
    dic["naver_catecode"] = naver_catecode
    dic["keyword"] = "'"+keyword+"'"
    dic["ranking"] = ranking
    
    return dic

def chkKeyword(keyword):
    global rs_ban, rs_x
    chk = False
    for row_ban in rs_ban:
        ban_keyword = row_ban[0]
        ban_catecode = row_ban[1]
        if keyword.strip()==ban_keyword.strip():
            chk = True
            print("밴키워드 : "+ban_keyword+" 밴카테고리 : "+str(ban_catecode))
            break
    for row_x in rs_x:
        x_keyword = row_x[0]
        if keyword.strip().find(x_keyword) > -1:
            chk = True
            print("x키워드 : "+x_keyword)
            break
            
    return chk

def replaceKeyword(keyword):
    global rs_replace
    for row_replace in rs_replace:
        keyword = keyword.replace(row_replace[1],row_replace[2])
    return keyword

def existKeyword(keyword):
    global rs_exist
    uid = 0
    for row_exist in rs_exist:
        rs_uid = row_exist[0]
        rs_keyword = row_exist[1]
        if keyword.strip()==rs_keyword.strip():
            uid = rs_uid
    
    return uid

def connectDriverOld(pgSite, mode):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    print(">> connectDriverOld ")
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    print(">> chrome_ver :{} | driver_path : {}".format(chrome_ver, driver_path))
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
        option.add_argument("user-data-dir={}".format(userProfile))
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': '" + str(pgSite) + "'")
    try:
        browser = webdriver.Chrome(options=option)
    except Exception as e:
        print(e)

    return browser

def connectDriverNew(pgSite, mode):
    option = Options()
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    option.add_experimental_option("useAutomationExtension", False) 
    option.add_argument("--disable-blink-features=AutomationControlled") 
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('--log-level=3')
    option.add_argument("--disable-gpu")
    if str(mode) == "S":
        option.add_argument("--incognito") # 시크릿 모드
    else:
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
        try:
            service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())
            browser = webdriver.Chrome(options=option, driver_executable_path=driver_executable_path)
            driver_executable_path = service.path
        except Exception as e:
            print(e)

    return browser


def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_con.execute(sql)


if __name__ == '__main__':

    print('>> [--- main start ---] ')
    print('>> naver best keyword (start)')
    cur_Ip = socket.gethostbyname(socket.gethostname())

    db_FS = DBmodule_FR.Database("freeship")
    db_con = DBmodule_FR.Database("aliexpress")
    gProc_no = "NAVER_BEST_KEYWORD"
    procLogSet(db_FS, gProc_no, "S", "0", " naver best keyword (start): "+str(cur_Ip))

    main_url = ""
    try:
        driver = connectDriverOld(main_url,"")
        print(">> connectDriverOld OK ")
    except Exception as e:
        driver = connectDriverNew(main_url,"")
        print(">> connectDriverNew set OK ")
    time.sleep(1)

    #driver = webdriver.Chrome(service=Service(executable_path='C:\\Users\\allin\\Downloads\\chromedriver_win32\\chromedriver.exe'))
    driver.maximize_window()
    driver.implicitly_wait(5)

    sql_x = "select ban_key from naver_shopping_best_ｘ_keyword"
    rs_x = db_con.select(sql_x)

    # sql = "select name, naver_catecode,depth,url,bcate,mcate,scate,parent from naver_shopping_catecode where lastcate=1 and ishidden='F' order by naver_catecode desc offset 883 rows"
    sql = "select name, naver_catecode,depth,url,bcate,mcate,scate,parent from naver_shopping_catecode where lastcate=1 and ishidden='F' order by naver_catecode desc"

    rs = db_con.select(sql)
    sql_exist = "select uid, keyword from naver_shopping_best_keyword"
    rs_exist = db_con.select(sql_exist)
    all_catecnt = len(rs)
    print("카테고리 총 {}개".format(len(rs)))
    ins_catecnt = 0
    for row in rs:
        time.sleep(1)
        name = row[0]
        naver_catecode = row[1]
        depth = row[2]
        url = row[3]
        bcate = row[4]
        mcate = row[5]
        scate = row[6]
        parent = row[7]
        print("카테고리 : "+str(naver_catecode) + " 시작")

        sql_ban = "select ban_keyword, naver_catecode from naver_shopping_ban_keyword where naver_catecode={}".format(str(naver_catecode))
        rs_ban = db_con.select(sql_ban)
        sql_replace = "select naver_catecode, keyword, replace_key from naver_shopping_best_replace_keyword where naver_catecode={}".format(str(naver_catecode))
        rs_replace = db_con.select(sql_replace)
        ## url = url.replace("click?","keyword?").replace("period=P1D","period=P7D")
        driver.get(url)
        time.sleep(random.uniform(3,5))
        if driver.current_url.find(str(naver_catecode)) == -1:
            print(">> 없는 카테고리 ( skip ) : {} | {}".format(naver_catecode, driver.current_url))
        else:
            html =driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            #driver.find_element(By.CSS_SELECTOR,'span.rankingTitleResponsive_inner__9_PWO > strong.rankingTitleResponsive_title__z9c4V')
            time.sleep(random.uniform(0.5,1))
            classname1 = getparse(html, 'rankingTitleResponsive_inner__', '">')
            element1 = 'rankingTitleResponsive_inner__' + str(classname1)
            element = 'span.'+str(element1)
            print(">> element : {}".format(element))
            keyword_list = driver.find_elements(By.CSS_SELECTOR, element)

            for item in keyword_list:
                strKeyword = item.get_attribute('innerHTML')
                rank = getparse(strKeyword,'rankingTitleResponsive_ranking','위')
                rank = getparse(rank,'">','<').strip()
                keyword = getparse(strKeyword,'rankingTitleResponsive_title','</strong>')
                keyword = getparse(keyword,'">','').strip()
                print(">> {} 위 : {}".format(rank, keyword))
                if chkKeyword(keyword):
                    print("ban키워드 스킵")
                    continue
                uid = existKeyword(keyword)
                if uid > 0:
                    print("중복 uid : "+str(uid))
                    insert_dic = makeBestKeyword(naver_catecode,keyword,0)
                    insert_dic["exist"] = "'1'"
                    db_con.insert("naver_shopping_best_keyword", insert_dic)
                    print("insert 완료(exist=1)")
                else:
                    insert_dic = makeBestKeyword(naver_catecode,keyword,0)            
                    db_con.insert("naver_shopping_best_keyword", insert_dic)
                    ins_catecnt = ins_catecnt + 1
                    print("insert 완료")

    print(">> 작업완료 ")
    procLogSet(db_FS, gProc_no, "F", ins_catecnt, " naver best keyword (end) 총카테고리 (" +str(all_catecnt)+ ") 추가키워드 ("+str(ins_catecnt)+") "+str(cur_Ip))
    print('>> naver best keyword (end)')
    driver.quit()
    db_con.close()
    db_FS.close()