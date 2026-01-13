import random
import os
import socket
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from collections import Counter
import chromedriver_autoinstaller
import datetime
import pyperclip
import pyautogui
import func_ali
from dbCon import DBmodule_FR


def chrom_click(selector, driver):
    driver.find_element_by_css_selector(selector).click()
    time.sleep(1)
    print(selector,"클릭")
    
def chrom_write(selector, driver, write):
    lst = list(write)
    for i in lst:
        driver.find_element_by_css_selector(selector).send_keys(i)
        time.sleep(random.uniform(0.2,0.3))
    time.sleep(1)

def loginProcNew(browser, loginId, loginPw):
    # 마우스 커서 어카운트 (계정)에 위치
    ActionChains(browser).move_to_element(browser.find_element_by_css_selector("#nav-user-account > span > a")).perform()
    # sign in 클릭
    time.sleep(1)
    try:
        # 계정 -> 로그인 버튼 클릭
        chrom_click("#nav-user-account > div > div > p.flyout-bottons > a.sign-btn", browser)
        # 아이디, 패스워드 입력
        chrom_click("#fm-login-id", browser)    
        chrom_write("#fm-login-id", browser, loginId)
        chrom_write("#fm-login-password", browser, loginPw)
        try:
            chrom_click("#batman-dialog-wrap > div > div > div.cosmos-tabs > div.cosmos-tabs-container > div > div > button.cosmos-btn.cosmos-btn-primary.cosmos-btn-large.cosmos-btn-block.login-submit > span", browser)
        except:
            chrom_click("#batman-dialog-wrap > div > div.fm-tabs-content > div > div > button", browser)
    except:
        print("로그인 중")
        time.sleep(1)

    order_url="https://www.aliexpress.com/p/order/index.html"
    try:
        browser.get(order_url)
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "comet-tabs-nav-item")))
        print(">> 주문 내역 Page Ok ")
        time.sleep(1)
    except:
        browser.get("https://ko.aliexpress.com/")
        time.sleep(1)

    browser.get("https://ko.aliexpress.com/")
    time.sleep(1)

    account_check = browser.find_element_by_class_name('account-main')
    if str(account_check.text).find('로그인') > -1 or str(account_check.text).find('Sign in') > -1:
        print(">> 로그인 실패 ")
        return "1"
    else:
        print(">> 로그인 OK ")
        return "0"


if __name__ == '__main__':

    connect_mode = "chrome"
    browser = func_ali.connectDriver(connect_mode)
    time.sleep(2)
    link_url="https://ko.aliexpress.com/"
    browser.get(link_url)
    element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "index-page")))
    time.sleep(2)

    loginProcNew(browser, "koiforever0526@gmail.com", "uiop7890")

    time.sleep(2)
