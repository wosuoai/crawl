from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib import parse
import random
from curl_cffi import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Edge
from fake_useragent import UserAgent
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driverPath = ChromeDriverManager().install()

def get_cookies():
    option = webdriver.ChromeOptions()
    #option.add_argument('--proxy-server=socks5://127.0.0.1:8888')
    #option = EdgeOptions()
    # 无头模式
    # option.add_argument('--headless')
    # proxy_ip = '115.207.170.185:4231'
    # option.add_argument('--proxy-server={}'.format(proxy_ip))
    # 允许root模式允许google浏览器
    option.add_argument("--incognito")  # 开启隐身模式
    option.add_argument('--no-sandbox')
    # option.add_argument('--headless')
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    #option.add_argument("--user-data-dir=C:/Users/15256/AppData/Local/Google/Chrome/User Data")  # 指定一个 Chrome 用户配置文件目录
    option.add_argument("--profile-directory=Default")
    # 打开无痕浏览模式
    # option.add_argument("--incognito")
    # 关闭开发者模式
    option.add_argument('--disable-blink-features=AutomationControlled')
    service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe')  # 配置谷歌操作驱动路径
    #service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\msedgedriver.exe')  # 配置谷歌操作驱动路径
    driver = webdriver.Chrome(options=option, service=service)

    driver.get("https://login.taobao.com/member/login.jhtml")
    #driver.get("https://login.tmall.com/")
    time.sleep(30)
    # print(driver.get_cookies())
    # with open("taobao_cookies.json","a",encoding="utf-8") as f:
    #     f.write(str(driver.get_cookies()))
    # driver.get("https://detail.tmall.com/item.htm?abbucket=20&id=716249068289&ns=1")
    # WebDriverWait(driver, 60, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/h1')))
    # driver.implicitly_wait(10)
    response = requests.get("https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu", impersonate="chrome110")

    if 'Just a moment' in response.text:  # tls指纹被检测到，会返回这个信息
        print('被检测')
    else:
        print('成功绕过')
    driver.get("https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
    WebDriverWait(driver, 60, 2).until(EC.presence_of_element_located((By.ID, 'J_Title')))
    driver.implicitly_wait(10)


    driver_cookies=str(driver.get_cookies())
    print(driver_cookies)


    cookies = {}
    for cookieDict in driver.get_cookies():
        cookies[cookieDict["name"]] = cookieDict["value"]
    with open("taobao_cookies.json","a",encoding="utf-8") as f:
        f.write(str(driver.get_cookies()))

    print(cookies)

if __name__ == '__main__':
    get_cookies()