from dbm import dumb
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pyautogui
import chromedriver_autoinstaller
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO
import os
import time, random

## https://www.youtube.com/watch?v=lDY-J-sUzPA
## 슬라이드 캡챠 해칭 봇 만들기 튜토리얼 (빵형의 개발도상국)
BROWSER_MENU_HEIGHT = 58

def connectDriver(tool):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)
    time.sleep(1)
    
    if tool == 'chrome':
        options = webdriver.ChromeOptions() 
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_argument("user-data-dir={}".format(userProfile))
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        #options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        browser = webdriver.Chrome(executable_path=driver_path, options=options) 
        #크롤링 방지 설정을 undefined로 변경 
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ }) 

    elif tool == 'chrome_secret':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')  
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        
    elif tool == 'chrome_service':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2}) 
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")

        #desired_capabilities = options.to_capabilities()
        #desired_capabilities['pageLoadStrategy'] = 'none'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

    elif tool == 'chrome_service_secret':
        service = Service.Service(driver_path)
        service.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled") 
        user_ag = UserAgent().random 
        options.add_argument('user-agent=%s'%user_ag) 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2})
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito") # 시크릿 모드
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(
                random.random()) + " Safari/537.36, 'Referer': 'https://s.taobao.com/'")

        #desired_capabilities = options.to_capabilities()
        #desired_capabilities['pageLoadStrategy'] = 'none'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options, desired_capabilities=capa)

    elif tool == 'brave':
        #path = "C:\\Project\\chromedriver.exe"
        username = os.getenv("USERNAME")
        userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options = webdriver.ChromeOptions()
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_argument("window-size=1400x1080")  # 화면크기(전체화면)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('--no-sandbox')
        options.add_argument("user-data-dir={}".format(userProfile))
        options.binary_location = brave_path
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

        # brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        # options = webdriver.ChromeOptions()
        # options.binary_location = brave_path

        # # Create new automated instance of Brave
        # browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    elif tool == 'Firefox':
        path = "C:\Project\cgeckodriver.exe"
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9150)
        profile.update_preferences()
        browser = webdriver.Firefox(profile, executable_path=path)

    return browser

connect_mode = "chrome_secret"
driver = connectDriver(connect_mode)
wait = WebDriverWait(driver, 20)

driver.get('https://detail.1688.com/offer/557259693146.html')
driver.set_window_size(1400, 1000)
driver.set_window_position(0, 0, windowHandle='current')
time.sleep(3)


# 퍼즐 위치 찾기 (퍼즐 이미지와 완성된퍼즐 이미지 rgb 값 비교해서 위치알아내기)
def get_distance(img1, img2):
    for x in range(60, img1.size[0]):
        for y in range(img1.size[1]):
            rgb1 = img1.getpixel((x,y))
            rgb2 = img2.getpixel((x,y))

            diff_r = abs(rgb1[0] - rgb2[0])
            diff_g = abs(rgb1[1] - rgb2[1])
            diff_b = abs(rgb1[2] - rgb2[2])

            if diff_r > 100 or diff_g > 100 or diff_b > 100:
                return x

#distance = get_distance(puzzel_img, compleate_img)
#print(distance)
cnt = 0
distance = 257
flg = "0"
while flg == "0":
    #sliderA = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    sliderA = driver.find_element_by_css_selector('#nc_1_n1z')
    time.sleep(1)
    if sliderA:
        xpos = sliderA.location['x'] + random.randint(32,33)
        ypos = sliderA.location['y'] + random.randint(100,101)
        print(" xpos: {}  ypos: {} ".format(xpos,ypos))
        pyautogui.moveTo(xpos, ypos, duration=random.uniform(1.0,3.0), tween=pyautogui.easeInBounce)
        pyautogui.click()
        pyautogui.mouseDown()
        #time.sleep(0.2)
        current_x = 0
        while True:
            if current_x >= 158:
                dx = distance - 158
            else:
                dx = random.randint(100,150)
            dy = random.randint(-5,5)
            dt = random.randint(100,150) / 150
            print("[1] dx: {}  dy: {} current_x : {}".format(dx,dy,current_x))
            pyautogui.moveRel(dx, dy, dt, tween=pyautogui.easeInOutSine)
            current_x += dx
            print("[0] current_x : {}".format(current_x))
            if current_x >= distance:
                dx = distance - current_x
                dy = random.randint(-5,5)
                print("[2] dx: {}  dy: {} current_x : {}".format(dx,dy,current_x))
                pyautogui.moveRel(dx, dy, 0.2, tween=pyautogui.easeInOutSine)
                time.sleep(1)
                break

        pyautogui.mouseUp()

    if cnt > 5:
        break
    driver.refresh()
    time.sleep(2)
    cnt = cnt + 1

input("KEY : ")