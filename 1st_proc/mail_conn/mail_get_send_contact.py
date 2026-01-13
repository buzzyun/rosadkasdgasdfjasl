import datetime
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
import DBmodule_FR
import func

global gProc_no
global upd_cnt

def replace_word(in_word):
    in_word = str(in_word)
    in_word = in_word.replace('<','').replace('>','').replace("&quot;","")
    in_word = in_word.replace("\xa0"," ").replace("\n","<br>")
    in_word = in_word.replace("'","").replace('"','').strip()
    return in_word

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

def chrome_driver():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)

    chormedriver = webdriver.Chrome(driver_path)
    return chormedriver

def login_proc():
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
                    print(">> Update : T_CONTACT_MAIL ")
                else:
                    sql = " insert into T_CONTACT_MAIL (mail_no, name, email, title, context, goodscode, mail_kbn, regdate) values ( '{}','{}','{}','{}','{}','{}','{}','{}')".format(mail_no,name,email,title,content_soup,goodscode,mail_kbn,regdate,goodscode)
                    print(">> Insert : T_CONTACT_MAIL ")
                db_FS.execute(sql)
                upd_cnt = upd_cnt + 1

        print("\\----------------------------------------------------------------")
        row_cnt = row_cnt + 1

    return "0"

def send_email(mainDriver, url, write_msg, sendto, uid, name, goodscode, db_FS):

    mainDriver.get(url)
    time.sleep(1)

    mailto = mainDriver.find_element_by_xpath('//*[@id="mf_to"]')
    mailto.click()
    mailto.send_keys(sendto)
    subject = mainDriver.find_element_by_name('mf_subject')
    subject.click()
    subject.send_keys("[프리쉽]{} 님 대량구매 견적드립니다. 프리쉽상품코드 : {}".format(name, goodscode))
    time.sleep(1)

    # iframe 으로 전환 
    mainDriver.switch_to.frame('mf_body_html_ifr')
    time.sleep(1)
    # content 작성
    test = mainDriver.find_element(By.XPATH, '//*[@id="tinymce"]/p[1]')
    time.sleep(1)

    print(">> 메일 쓰기 ")
    mainDriver.find_element_by_class_name('mceContentBody') #mainDriver.find_element_by_id('mf_body_html_ifr')
    content = mainDriver.find_element(By.CSS_SELECTOR, '#tinymce > p:nth-child(1)')
    content.send_keys(write_msg)
    time.sleep(1)

    # iframe -> parent 전환 
    mainDriver.switch_to.parent_frame()
    time.sleep(1)

    if mainDriver.find_element(By.CSS_SELECTOR, '[alt="보내기"]'):
        mainDriver.find_element(By.CSS_SELECTOR, '[alt="보내기"]').click()
        time.sleep(random.uniform(1,2))
        print(">> 메일 보내기 Click : {}".format(sendto))
        result = mainDriver.page_source
        checkSend = func.getparse(str(result),'class="main_table_body_Y0"','</tr>')
        if checkSend.find(sendto) > -1:
            print(">> Mail Send Ok")
            uSql = " update t_contact_price set mail_send = '1', mail_send_date = getdate() where uid = '{}'".format(uid)
            print(">> uSql : {}".format(uSql))
            db_FS.execute(uSql)

    print(">> ---------------------------------------  ")


def makeMsg(name, title, ea, ea_price, vat_price, sale_price, goodsUrl):

    #linktitle = '<a href="' + goodsUrl + '" target="_blank">' + title + '</a>'
    linktitle = title
    tmpMsg = """


[매스플렛폼] """+ name +""" 고객님 
문의 주신 제품의 견적서를 전송 드리오니
검토하시어 안전하고 편리한 구매 되시길 바랍니다.

[견적내용]
▶상품명 : """ + str(linktitle) + """
  ( """ + str(goodsUrl) + """ )
▶수량 : """+ str(ea) +"""
▶제품단가 : """+ str(ea_price) +"""원
▶부가세 : """+ str(vat_price) +"""원
▶견적가 : """+ str(sale_price) +"""원

[안내사항]
매스플렛폼의 대량구매는 견적된 금액 외에 추가로 금액이 발생 되지 않습니다.
배송기간 : 평균 영업일 기준 약 7~25일 소요



Mass Platform
-
이 성 훈
대량구매 팀 |팀장|

대구광역시 동구 이노밸리로 38, 2F
email : contact@freeship.co.kr
M : 010 3548 2104 | T : 070 4763 7770
F  : 053 762 3210  | E : contact@freeship.co.kr

""" 
    return tmpMsg

def senProc(db_FS, mainDriver):
    send_cnt = 0
    print(">> ")
    sql = " select C.uid, name, email, dbo.GetCutStr(title,120,'...') as title, vat, p.sale_price, p.vat_price, p.ea, p.ea_price, goodscode \
    from T_CONTACT as C inner join t_contact_price as P on P.uid = C.uid where C.del_flg is null and P.mail_send_set = '1' and P.mail_send is null "

    rows = db_FS.select(sql)
    if rows:
        for row in rows:
            uid = row[0]
            name = row[1]
            email = str(row[2]).strip()
            title = row[3]
            vat = row[4]
            sale_price = format(int(row[5]),',')
            vat_price = format(int(row[6]),',')
            ea = format(row[7],',')
            ea_price = format(row[8],',')
            goodscode = row[9]
            sitename = func.getSiteName(goodscode)
            goodsuid = func.getGuid(goodscode)
            goodsUrl = "https://" + str(sitename) + ".freeship.co.kr/goods/content.asp?guid=" + str(goodsuid)
            TemplateMsg = makeMsg(name, title, ea, ea_price, vat_price, sale_price, goodsUrl)

            print('>> 이메일 작성하기 ')
            send_email(mainDriver,'http://mail.freeship.co.kr/mail_write.php', TemplateMsg, email, uid, name, goodscode, db_FS)
            time.sleep(4)

            send_cnt = send_cnt + 1

    procLogSet(db_FS, gProc_no, "F", "0", " Write Mail (End) | send_cnt : {} ".format(send_cnt))
    time.sleep(3)


if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> Get Mail (T_CONTACT_MAIL) 작업 시작 :' + str(now))
    gProc_no = "MAIL_GET_CONTACT"

    db_FS = DBmodule_FR.Database('freeship')
    procLogSet(db_FS, gProc_no, "S", "0", " Get Mail (Start) ")

    mainDriver = chrome_driver()
    site_url = 'http://mail.freeship.co.kr/login.php'
    print('>> site_url : {}'.format(site_url))
    mainDriver.get(site_url)
    mainDriver.set_window_size(1100, 800)
    mainDriver.implicitly_wait(3)
    time.sleep(3)

    # 로그인 처리
    login_proc()

    time.sleep(2)
    # 이메일 견적서 발송 처리 
    senProc(db_FS, mainDriver)

    time.sleep(2)
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

    print('>> 작업 완료 :' + str(now))
    mainDriver.quit()
    db_FS.close()
    os._exit(0)
