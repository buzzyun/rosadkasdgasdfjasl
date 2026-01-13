*** 셀레니움 크롤링 속도 향상 ***

셀레니움 크롤링 속도 향상 시키는법 공유 드립니다

options.page_load_strategy = 'eager'

옵션에 지정함으로써 전체 사이트 다 뜰때까지 로딩을 기다릴 필요가 없어집니다.

필요한 부분까지의 로딩을 
        while 1:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            if str(soup).find('title--text--Otu0bLr') > 0:

루프를 돌려가며 소스 확인후 소스가 로딩된거 확인후 바로 break 시켜버리면 전체 로딩대기 시간을 줄일수 있습니다.

또한,options.add_argument("--blink-settings=imagesEnabled=false")

셀레니움 드라이브옵션에 이미지를 안불러 오도록 설정하면 속도 향상에 도음이 됩니다.

만약 options.add_argument("user-data-dir={}".format(userProfile))

유저 데이터를 사용할경우 위의 옵션은 안먹히고 이미지가 계속 불러와집니다

이럴경우

def disable_images(driver):
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.jpg", "*.jpeg", "*.png", "*.gif"]})
    driver.execute_cdp_cmd("Network.enable", {})

# 이미지 로딩 차단 활성화
disable_images(driver)

driver.get(aliurl)

네트워크단에서 이미지의 확장자를 차단해줌으로써 이미지를 안불러올수 있습니다.

로딩 속도 줄이고 이미지 로딩을 안하니 크롤링 속도가 많이 좋아졌습니다.
알리에서도 트래픽이 줄어서 그런지 막히는 횟수도 줄어드네요