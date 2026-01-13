import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
import subprocess
import os, sys
import datetime
import webbrowser
import func_user
import DBmodule_FR
import func
import parsing_source


db_FS = DBmodule_FR.Database('freeship')

if __name__ == '__main__':
  now = datetime.datetime.now()
  print('>> 작업 시작 :' + str(now))

  sp_main_cate = parsing_source.main_cate.split('data-web-log-event=')
  for ea_cate in sp_main_cate:
    cate_url = func_user.getparse(ea_cate,'href="','"')
    if cate_url.find('https://') == -1:
      cate_url = "https://www.coupang.com" + str(cate_url)
    cate_name = func_user.getparse(ea_cate,'alt="','"')
    if cate_name != "":
      print(">> [{}] {}".format(cate_name,cate_url))

  print(">>")