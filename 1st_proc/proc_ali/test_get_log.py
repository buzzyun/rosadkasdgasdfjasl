import json, os, time, random
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

service = Service()
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--enable-logging')
options.add_argument('--log-level=0')
options.add_argument("user-data-dir={}".format(userProfile))
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + str(random.random()) + " Safari/537.36, 'Referer': 'https://ko.aliexpress.com/'")
driver = webdriver.Chrome(service=service, options=options)

onurl = "https://ko.aliexpress.com/item/1005005750878861.html"
driver.get(onurl)
time.sleep(2)

logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

# def log_filter(log_):
#     return (
#         # is an actual response
#         log_["method"] == "Network.responseReceived"
#         # and json
#         and "json" in log_["params"]["response"]["mimeType"]
#     )

def log_filter(log_):
    return (
        log_["method"] == "Network.requestWillBeSent"
    )

for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["request"]["url"]
    if str(resp_url).find('mtop.aliexpress.itemdetail.pc.asyncpcdetail') > 0:
        print(f"Caught {resp_url}")
        print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))

print(">> ")