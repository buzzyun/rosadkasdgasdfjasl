import urllib
import urllib
from urllib.request import Request, urlopen
import cv2
from PIL import Image
from io import BytesIO
import datetime
import time
import requests
import os

def imgComp(fs_url, ali_url):

    file_path = os.path.dirname(os.path.abspath(__file__)) 
    if os.path.exists(file_path+ "\\img_fs.jpg"):
        os.remove(file_path+ "\\img_fs.jpg")
    if os.path.exists(file_path+ "\\img_ali.jpg"):
        os.remove(file_path+ "\\img_ali.jpg")

    time.sleep(1)
    # 프리쉽 상품 URL 이미지 다운로드
    #url = "https://office2.freeship.co.kr/goodsimg/56403\\2021-03-29/big/4000041507449.jpg"
    urllib.request.urlretrieve(str(fs_url), file_path+"\\img_fs.jpg")
    time.sleep(2)

    # 알리 상품 이미지 다운로드
    #urllib.request.urlretrieve(str(ali_url), "test_ali.jpg")
    r = requests.get(ali_url)
    with open(file_path+"\\img_ali.jpg", "wb") as outfile:
        outfile.write(r.content)
    time.sleep(2)

    # 프리쉽 상품 이미지와 알리 상품 이미지 비교 
    imageA = cv2.imread(file_path+"\\img_fs.jpg")
    imageB = cv2.imread(file_path+"\\img_ali.jpg")
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    if len(grayA) == 0 or len(grayB) == 0:
        return "-1"

    # 이미지의 구조 비교
    if len(grayA)==len(grayB):
        print(" 이미지 구조 같음 ")
        return "0"
    else:
        print(" 이미지 구조 다름 ")
        return "1"
    

fs_url = "https://electron2.freeship.co.kr/goodsimg/56209/2021-04-10/big/32768900465.jpg"
ali_url = "http://ae01.alicdn.com/kf/HTB1jyafOpXXXXXBapXXq6xXFXXXT/PS2-90000.jpg"


rtn_img = imgComp(fs_url, ali_url)
print(" rtn_img : "+ str(rtn_img))