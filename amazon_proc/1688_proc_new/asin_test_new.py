import random
import time
import socket
import os
import func_1688 as func
import DBmodule_FR

global errcnt 
db_con = DBmodule_FR.Database('red')

ip = socket.gethostbyname(socket.gethostname())
amzurl = ""
chkTime = time.time()
print(">> chkTime : "+str(chkTime))

if __name__ == '__main__':
    print(">> start ")
    errcnt = 0

    # newCateDep1()
    print("-------------------------------")

    time.sleep(1)
    now_url = "https://open-demo.otcommerce.com/ik.php"
    try:
        print(">> connectDriverOld set ")
        browser = func.connectDriverOld(now_url, "N", "N")
    except Exception as e:
        print(">> connectDriverNew set ")
        browser = func.connectDriverNew(now_url, "N", "N")
    time.sleep(3)
    browser.set_window_size(1600, 1000)

    browser.get(now_url)
    time.sleep(4)
    if str(browser.page_source).find('Instance Key') > -1:
        print(">> Login Need ")
        func.demo_login_new(browser)
        time.sleep(2)

    if str(browser.current_url).find('https://open-demo.otcommerce.com/admin/') > -1:
        print(">> Login Ok ")
        func.billChk(browser, db_con) # api 잔액체크
        time.sleep(1)
        browser.get('https://open-demo.otcommerce.com/')
        time.sleep(3)
    else:
        print(">> Login Fail Input Key : ")

    time.sleep(1)
    

    db_con.close()
    os._exit(0)