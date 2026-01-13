# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:51:14 2023

@author: allin
"""

from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess

def open_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    # chromedriver_version = "114.0.5735.16"
    chromedriver_version = "114.0.5735.90"
    options.add_argument('--disable-loging')
    options.add_argument(r'user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data\Profile1')
    options.add_argument("lang=ko_KR") # 한국어!
    options.add_argument("language=ko") # 한국어!     
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(executable_path='C:\\project\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver  


def cutString(string,start_word,end_word):
    start_index = string.find(start_word)
    end_index = string.find(end_word,start_index)    
    outString = string[start_index+len(start_word):end_index]
    
    return outString

def chrom_drive():
    try:#CC:\Program Files (x86)\Google\Chrome\Application
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동  
    except:
        subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
    
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(service=f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(5) 
    driver.set_page_load_timeout(3600)
    return driver 

def ListToStr(lst):
    string = str(lst).replace("[", "").replace("]", "").replace("'", "")
    
    return string