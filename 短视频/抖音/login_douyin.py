from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

shieldJsText = requests.get("https://gitcode.net/mirrors/requireCool/stealth.min.js/-/raw/main/stealth.min.js?inline=false").text

option = webdriver.ChromeOptions()
# 允许root模式允许google浏览器
option.add_argument('--no-sandbox')
option.add_argument("--incognito") #开启隐身模式
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
#option.add_argument("--user-data-dir=C:/Users/15256/AppData/Local/Google/Chrome/User Data")  # 指定一个 Chrome 用户配置文件目录
option.add_argument("--profile-directory=Default")
# 关闭开发者模式
option.add_argument('--disable-blink-features=AutomationControlled')
# 屏蔽保存密码提示框
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
option.add_experimental_option('prefs', prefs)
# 关闭webrtc 避免找到真实IP地址
preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
option.add_experimental_option("prefs", preferences)
service = ChromeService(executable_path=r'E:\元宇宙\f83ry87fg.exe') # 配置谷歌操作驱动路径

driver = webdriver.Chrome(options=option,service=service)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': shieldJsText})  # 屏蔽selenium参数
script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
driver.execute_script(script)

driver.get('https://www.douyin.com/')
time.sleep(40)

# driver.get("https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
# WebDriverWait(driver, 60, 2).until(EC.presence_of_element_located((By.ID, 'J_Title')))
# driver.implicitly_wait(10)

cookies = {}
for cookieDict in driver.get_cookies():
    cookies[cookieDict["name"]] = cookieDict["value"]

print(driver.get_cookies())
with open("douyin.json", "a") as f:
    f.write(str(cookies) + '\n')
driver.close()
