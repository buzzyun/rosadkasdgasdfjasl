# -*- coding: utf-8 -*-

from selenium.webdriver import ChromeOptions
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 첫 번째 단계는 Taobao에 로그인
class Chrome_drive():
    def __init__(self):
        ua = UserAgent()
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        NoImage = {"profile.managed_default_content_settings.images": 2}  # 사진 없음 제어
        option.add_experimental_option("prefs", NoImage)
        # option.add_argument(f'user-agent={ua.chrome}')  # 브라우저 헤더 추가
        # chrome_options.add_argument(f"--proxy-server=http://{self.ip}")  # IP 주소 추가
        # option.add_argument('--headless')  # 헤드리스 모드 브라우저 팝업 없음

        self.browser = webdriver.Chrome(options=option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
        })  # 셀레늄 드라이버 설정 제거

        self.browser.set_window_size(1200,768)
        self.wait = WebDriverWait(self.browser, 12)

    def get_login(self):
        url='https://www.1688.com/'
        self.browser.get(url)
        #self.browser.maximize_window()  # 在这里登陆的中国大陆的邮编
        #这里进行人工登陆。
        time.sleep(2)
        self.browser.refresh()  # 刷新方法 refres

        # login_id = "Kimbyeongwan21"
        # login_pass = "order1071tao*"    
        # url = 'https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253D%25252F%25252Fwww.1688.com%25252F&style=tao_custom&from=1688web'

        # self.browser.get(url)
        # time.sleep(1)
        # print('>> loginProc_new ')

        # wait = WebDriverWait(self.browser, 30)
        # id_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id"))) 
        # id_input.send_keys(login_id) 
        # print('>> ID OK ')
        # time.sleep(2)
        # wait = WebDriverWait(self.browser, 30)
        # pw_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-password"))) 
        # pw_input.send_keys(login_pass) 
        # print('>> pass OK ')
        # time.sleep(2)
        # wait = WebDriverWait(self.browser, 30)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fm-button"))).click()
        # print('>> click OK ')
        # time.sleep(4)    
        
        self.browser.refresh()  # 새로 고침

        return


    #판단 페이지 텍스트의 내용 가져오기
    def index_page(self,page,wd):
        """
        抓取索引页
        :param page: 页码
        """
        print('正在爬取第', page, '页')

        #url = f'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%A1%D0%CD%C3%AB%BD%ED%BC%D3%C8%C8%B9%F1&n=y&netType=16&beginPage=1#sm-filtbar'
        url = f'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%A1%D0%CD%C3%AB%BD%ED%BC%D3%C8%C8%B9%F1&n=y&netType=16&beginPage={page}#sm-filtbar'
        #url = f'https://s.1688.com/selloffer/industry_offer_search.htm?industryFlag=xiebaopeishi&holidayTagId=10010552&uniqfield=pic_tag_id&keywords=%D5%DA%D1%F4%C3%B1&beginPage={page}&from=industrySearch&filt=y&n=y&filt=y#_fb_top'
        
        js1 = f" window.open('{url}')"  # 실행하여 새 탭 열기
        print(url)
        self.browser.execute_script(js1)  # 새 웹 탭 열기
            # 실행하여 새 탭을 엽니다.
        self.browser.switch_to.window(self.browser.window_handles[-1])  # 현재 페이지 창을 찾는 데 사용
        self.buffer()  # 페이지 스와이프 전환 성공
            # 요소가 로드될 때까지 기다립니다.
        time.sleep(7)
        #self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#render-engine-page-container > div > div.common-pagination > div > div > div > span:nth-child(2) > input')))
            # 웹 페이지의 소스 코드 가져오기
        html =  self.browser.page_source

        get_products(wd,html)

        self.close_window()


    def buffer(self): # 스와이프 웹
        for i in range(20):
            time.sleep(0.5)
            self.browser.execute_script('window.scrollBy(0,380)', '')  # 300픽셀 아래로 슬라이드

    def close_window(self):
        length=self.browser.window_handles
        print('length',length) # 현재 웹 페이지 창 수 확인
        if  len(length) > 3:
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.close()
            time.sleep(1)
            self.browser.switch_to.window(self.browser.window_handles[-1])


import csv
def save_csv(lise_line):
    file = csv.writer(open("./1688_com.csv",'a',newline="",encoding="utf-8"))
    file.writerow(lise_line)

# 웹 페이지 구문 분석
from scrapy.selector import Selector
def get_products(wd,html_text):
    """
    데이터 추출
    """
    select=Selector(text=html_text)
    # 大概有47个
    items = select.xpath('//*[@id="sm-offer-list"]/div/*').extract()
    print('产品数 ',len(items))
    for i in range(1, len(items)+1):
        #详情页链接
        desc_href = select.xpath(f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="img-container"]//a/@href').extract_first()
        # 图片链接
        img_url  = select.xpath(f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="img"]/@style').extract_first()
        # 复购率
        shop_repurchase_rate = select.xpath(
            f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="desc-container"]//span[@class="shop-repurchase-rate"]/text()').extract_first()
        # title  # 标题
        title = select.xpath(
            f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="desc-container"]//div[@class="title"]//text()').extract()
        title_name=''.join(title)
        #price  #价格
        price = select.xpath(f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="desc-container"]//div[@class="price-container"]/div[@class="price"]/text()').extract_first()
        # sales_num  # 成交量
        sales_num = select.xpath(
            f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="desc-container"]//div[@class="price-container"]/div[@class="sale"]/text()').extract_first()
        #company_name  # 公司名称
        company_name = select.xpath(f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="company-name"]/a/text()').extract_first()
        #company_href  # 公司链接
        company_href = select.xpath(f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="company-name"]/a/@href').extract_first()
        #company_tag  # 公司标签
        company_tag = select.xpath(
            f'//*[@id="sm-offer-list"]/div[{i}]//div[@class="common-company-tag"]//text()').extract_first()

        all_desc=[wd,title_name,img_url,desc_href,price,sales_num,company_name,company_href,company_tag,shop_repurchase_rate]
        print(all_desc)
        save_csv(all_desc)



def main():
    """
    각 페이지에 대해 반복
    """
    run=Chrome_drive()
    run.get_login() # 로그인하려면 코드를 스캔

    wd=['小型毛巾加热柜']
    for w in wd:
        for i in range(1, 6): # 1688 총 6페이지가 표시되었으며 처음 5페이지의 내용이 크롤링
            run.index_page(i,w)


if __name__ == '__main__':
    csv_head = 'word,title_name,img_url,desc_href,price,sales_num,company_name,company_href,company_tag,shop_repurchase_rate'.split(
        ',')
    save_csv(csv_head)
    main()
