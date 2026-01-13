import datetime
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import chromedriver_autoinstaller
import DBmodule_FR
import func

global gProc_no
global upd_cnt

db_FS = DBmodule_FR.Database('freeship')

def replace_word(in_word):
    in_word = str(in_word)
    in_word = in_word.replace('<','').replace('>','').replace("&quot;","")
    in_word = in_word.replace("\xa0"," ").replace("\n","<br>")
    in_word = in_word.replace("'","").replace('"','').strip()
    return in_word


def get_email(mainDriver, proc_url, mail_kbn):
    global upd_cnt
    print(">> proc_url : {}".format(proc_url))
    mainDriver.get(proc_url)
    time.sleep(5)
    result = mainDriver.page_source
    result_soup = BeautifulSoup(str(result), 'html.parser')

    result = str(result)
    result_list = func.getparse(str(result),'class="main_table_body_Y0"','</table>')
    sp_item = result.split('class="main_table_body_')

    row_cnt = 0
    mail_no = ""
    for ea_item in sp_item:
        print("\\----------------------------------------------------------------")
        if row_cnt > 0:
            #print(">> item : {}".format(ea_item))
            sp_td = str(ea_item).split('<td ')
            row_cnt_td = 0
            mail_no = func.getparse(str(ea_item),'name="cmf[]" value="','"')
            print(">> mail_no : {}".format(mail_no))
            goodscode = ""
            for ea_td in sp_td:
                if row_cnt_td == 5:
                    item = func.getparse(str(ea_td),'title="','<font')
                    #name = func.getparse(str(item),'','<').replace("&quot;","")
                    name = func.getparse(str(item),'','<font color="#000000">')
                    if name.find('&quot;') > -1:
                        name = func.getparse(str(item),'','<').replace("&quot;","")
                        email = func.getparse(str(item),'<','>')
                    else:
                        name = func.getparse(str(item),'',',')
                        email = name

                    name = replace_word(name)
                    email = replace_word(email)
                    print(">> name : {}".format(name))
                    print(">> email : {}".format(email))
                if row_cnt_td == 6:
                    item = func.getparse(str(ea_td),'>','')
                    if mail_kbn == "sent":
                        title = func.getparse(str(item),'<a href="/mail_read.php?mb_id=sent','</a>')
                    else:
                        title = func.getparse(str(item),'<a href="/mail_read.php?mb_id=inbox','</a>')
                    title = func.getparse(str(title),'<font color="#000000">','</font>')
                    title = replace_word(title)
                    print(">> title : {}  ".format(title))
                    if title.find('상품코드') > -1:
                        goodscode = func.getparse(str(title),'프리쉽상품코드','')
                        goodscode = func.getparse(str(goodscode),':','').strip()
                        print(">> goodscode : {}  ".format(goodscode))
                        if len(goodscode) > 13:
                            print(">> goodscode Error : {}  ".format(goodscode))
                            goodscode = ""

                    content = func.getparse(item,'','<a href="/mail_read.php')
                    if str(content).find('님이 작성:') > -1:
                        content = func.getparse(str(content),'님이 작성:','')
                    if str(content).find('style="HEIGHT:15px; OVERFLOW:hidden;"') > -1:
                        content = func.getparse(str(content),'','style="HEIGHT:15px; OVERFLOW:hidden;"')
                    content_soup = BeautifulSoup(str(content), 'html.parser')
                    #print(">> content_soup (org) : {}  ".format(content_soup))
                    content_soup = str(content_soup).replace("\xa0"," ").replace('&lt;div title=','').replace("&lt;","<").replace("&gt;",">").replace("\n","<br>").replace('"','').replace("'","")
                    #print(">> content_soup : {}  ".format(content_soup))

                if row_cnt_td == 7:
                    item = func.getparse(str(ea_td),'>','')
                    regdate = func.getparse(str(item),'color=#000000-->','</td>')
                    print(">> regdate : {}  ".format(regdate))
                row_cnt_td = row_cnt_td + 1

            if str(mail_no).strip() == "":
                print(">> mail_no 없음 : {}".format(mail_no))
            else:
                sql_s = "select * from T_CONTACT_MAIL where mail_no = '{}'".format(mail_no)
                row = db_FS.selectone(sql_s)
                if row:
                    sql = " update T_CONTACT_MAIL set name = '{}', email = '{}', title = '{}', context = '{}', goodscode = '{}', mail_kbn = '{}',regdate = '{}' where mail_no = '{}'".format(name,email,title,content_soup,goodscode,mail_kbn,regdate,mail_no)
                    print(">> Update : {}".format(sql))
                else:
                    sql = " insert into T_CONTACT_MAIL (mail_no, name, email, title, context, goodscode, mail_kbn, regdate) values ( '{}','{}','{}','{}','{}','{}','{}','{}')".format(mail_no,name,email,title,content_soup,goodscode,mail_kbn,regdate,goodscode)
                    print(">> Insert : {}".format(sql))
                db_FS.execute(sql)
                upd_cnt = upd_cnt + 1

        print("\\----------------------------------------------------------------")
        row_cnt = row_cnt + 1

    return "0"

def procLogSet(db_con, in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "

    print(" setLogProc : " + str(sql))
    db_con.execute(sql)

def procUpdateCate(sitecate, guid, db_con):
    print("procUpdateCate")
    sql = "select cate_idx from t_goods where uid = '{}'".format(guid)
    row = db_con.selectone(sql)
    if row:
        cate_idx = row[0]
    

if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> Get Mail (T_CONTACT_MAIL) 작업 시작 :' + str(now))
    gProc_no = "MAIL_GET_CONTACT"
    procLogSet(db_FS, gProc_no, "S", "0", " Get Mail (Start) ")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    #path = "C:\\util\\chromedriver.exe"
    mainDriver = webdriver.Chrome(driver_path)
    site_url = 'http://mail.freeship.co.kr/login.php'
    print('>> site_url : {}'.format(site_url))
    mainDriver.get(site_url)
    mainDriver.set_window_size(1100, 800)
    mainDriver.implicitly_wait(3)
    time.sleep(3)

    # 로그인 ID/PASS 입력
    mainDriver.find_element_by_xpath(
        '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input').send_keys('contact')
    time.sleep(1)
    mainDriver.find_element_by_xpath(
        '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input').send_keys('allin1071@')
    time.sleep(1)
    # 로그인 버튼 클릭
    mainDriver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/a/img').click()
    print('>> 로그인 Ok')
    time.sleep(4)

    upd_cnt = 0
    # 받은 편지함 기져오기
    print('>> 받은 편지함 기져오기')
    get_email(mainDriver,'http://mail.freeship.co.kr/mail_list.php?mb_id=inbox','inbox')
    time.sleep(4)
    rcv_cnt = 0
    rcv_cnt = upd_cnt

    upd_cnt = 0
    # 보낸 편지함 기져오기
    print('>> 보낸 편지함 기져오기')
    get_email(mainDriver,'http://mail.freeship.co.kr/mail_list.php?mb_id=sent','sent')
    send_cnt = 0
    send_cnt = upd_cnt

    procLogSet(db_FS, gProc_no, "F", "0", " Get Mail (End) | rcv_cnt : {} | send_cnt : {} ".format(rcv_cnt, send_cnt))
    time.sleep(3)

    # ## T_CONTACT 테이블 sitecate, catecode Insert 
    # sql = "select goodscode from T_CONTACT where sitecate is null order by goodscode "
    # rows = db_FS.select(sql)
    # proc_sitecate = ""
    # rowcnt = 0
    # if rows:
    #     for row in rows:
    #         rowcnt = rowcnt + 1
    #         sitecate = ""
    #         db_goodscode = row[0]
    #         sitecate = func.getSiteName(db_goodscode)
    #         guid = func.getGuid(db_goodscode)

    #         print(">> goodscode : {} | sitecate : {} | guid : {} ".format(db_goodscode, sitecate, guid))
    #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    #         if rowcnt == 1:
    #             db_con = DBmodule_FR.Database(sitecate)
    #         else:
    #             if proc_sitecate != sitecate:
    #                 print(">> Site DB Open : {} ".format(sitecate))
    #                 db_con = DBmodule_FR.Database(sitecate)

    #         cate_idx = ""
    #         sql = "select cate_idx from t_goods where uid = '{}'".format(guid)
    #         crow = db_con.selectone(sql)
    #         if crow:
    #             cate_idx = crow[0]
    #         time.sleep(2)

    #         proc_sitecate = sitecate
    #         if rowcnt != 1 and proc_sitecate != sitecate:
    #             print(">> Site DB Close : {}".format(sitecate))
    #             db_con.close()

    #         if db_goodscode != "" and cate_idx != "":
    #             sql_u = " update T_CONTACT set sitecate = '{}', catecode = '{}' where goodscode = '{}'".format(sitecate, cate_idx, db_goodscode)
    #             print(">> sql_u : {}".format(sql_u))
    #             db_FS.execute(sql_u)

    mainDriver.quit()
    db_FS.close()
    print('>> 작업 완료 :' + str(now))
    os._exit(0)
