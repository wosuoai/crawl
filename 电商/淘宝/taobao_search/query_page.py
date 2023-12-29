# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
import re
import time
import random
import lxml
import lxml.etree
import json
import os
import uuid
import hashlib
from urllib.request import quote, unquote
from setting import redisHost, redisPort, redisPassword
import redis
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService
#
# driverPath = ChromeDriverManager().install()

option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("--disable-javascript") #屏蔽js
#service = ChromeService(executable_path=driverPath)  # 配置谷歌操作驱动路径
# option.add_argument('--headless')
# option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
# option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
driver = webdriver.Chrome(options=option)
cookiesList = []


def dict_cookies_to_browser_taobao(cookies: dict) -> list:
    cookiesBrowserList = []
    for key in cookies:
        cookiesBrowserList.append({
            "domain": ".taobao.com",
            "name": key,
            "value": cookies[key]
        })

    return cookiesBrowserList


driver.get('https://www.taobao.com')
time.sleep(3)
for item in dict_cookies_to_browser_taobao(random.choice(cookiesList)):
    driver.add_cookie(item)
driver.refresh()
driver.implicitly_wait(2)


def scroll(driver):
    for i in range(5):
        driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
        time.sleep(1)


if __name__ == "__main__":
    key_word = "水貂皮草"
    driver.get('https://s.taobao.com/search')
    search_element = driver.find_element(By.CSS_SELECTOR, '#q')
    # 默认就是第一页
    search_element.send_keys("水貂皮草")
    search_element.send_keys(Keys.ENTER) # 输入页码后进行回车
    scroll(driver)
    time.sleep(5)

    """
    该页面上的选项点击后不会对地址栏中的链接造成改变
    因此这里如果要做筛选 需要模拟点击后在进行链接跳转 之前的操作会默认记录
    """
    product_links = "https://s.taobao.com/search?bcoffset=0&commend=all&ie=utf8&initiative_id=staobaoz_20230828&p4ppushleft=%2C44&page={}&q={}&s=0&search_type=item&sort=sale-desc&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ssid=s5-e".format(1, quote(key_word, encoding="utf-8"))
    driver.get(product_links)
    time.sleep(5)
    # 选择性别
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').click()
    time.sleep(5)

    # 判断商品搜索页数，如果不是100页，则切换到销量排序
    total_page = driver.find_element(By.XPATH,'//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/span').text.replace("/","")[1:]
    if int(total_page) != 100:
        driver.find_element(By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[1]/div/div[1]/div/div/div/ul/li[2]').click()
        time.sleep(5)

    # 选择货源地址，时间尽量长一点，太短会触发风控
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[1]')).perform()
    time.sleep(2)
    # 上海
    driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(2) > button").click()
    time.sleep(10)
    # 广州
    driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(3) > button").click()
    time.sleep(10)
    # 深圳
    driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(4) > button").click()
    time.sleep(10)
    # 杭州
    driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(5) > button").click()
    time.sleep(10)
    # 嘉兴
    driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(2) > div:nth-child(13) > button").click()
    time.sleep(10)

    scroll(driver=driver)
    time.sleep(5)

    item_html = driver.execute_script("return document.documentElement.outerHTML").encode('utf-8').decode('raw_unicode_escape').replace(" ",'').replace("/n","")
    comment_urls = re.findall(r'//item\.taobao\.com/item\.htm\?id=\d+', item_html) + re.findall(r'//(detail\.tmall\.com/item\.htm\?id=[\d]+)', item_html)
    print(len(comment_urls))
    item_links = []  # 定义一个存放每页商品的列表
    for url in comment_urls:
        if "item.taobao.com" in url:
            item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1#detail"
            item_links.append(item_link)
        else:
            item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1"
            item_links.append(item_link)
    item_links = item_links[3:]  # 去除广告商品
    print(len(item_links))
    print(item_links)


    for i in range(99):
        # 直接定位到输入框输入页数
        # js_scr = 'document.getElementsByClassName("next-input next-medium next-pagination-jump-input")[0].value="5";'
        js_scr = 'document.querySelector("#root > div > div:nth-child(3) > div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Pagination--pgWrap--kfPsaVv > div > div > span.next-input.next-medium.next-pagination-jump-input > input").value="5";'
        driver.execute_script(js_scr)
        time.sleep(5)
        # 确认按钮
        js_scr1 = 'document.querySelector("#root > div > div:nth-child(3) > div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Pagination--pgWrap--kfPsaVv > div > div > button.next-btn.next-medium.next-btn-normal.next-pagination-jump-go").click();'
        driver.execute_script(js_scr1)
        time.sleep(10)

        # 点击下一页的操作放在JavaScript里面的，需要js执行
        js_scr = 'document.querySelector("#sortBarWrap > div.SortBar--sortBarWrapTop--VgqKGi6 > div.SortBar--otherSelector--AGGxGw3 > div:nth-child(2) > div.next-pagination.next-small.next-simple.next-no-border > div > button.next-btn.next-small.next-btn-normal.next-pagination-item.next-next").click();'
        driver.execute_script(js_scr)
        time.sleep(random.randint(5, 8))

        item_html = driver.execute_script("return document.documentElement.outerHTML").encode('utf-8').decode('raw_unicode_escape').replace(" ", '').replace("/n", "")
        comment_urls = re.findall(r'//item\.taobao\.com/item\.htm\?id=\d+', item_html) + re.findall(r'//(detail\.tmall\.com/item\.htm\?id=[\d]+)', item_html)
        print(len(comment_urls))
        item_links = []  # 定义一个存放每页商品的列表
        for url in comment_urls:
            if "item.taobao.com" in url:
                item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1#detail"
                item_links.append(item_link)
            else:
                item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1"
                item_links.append(item_link)
        item_links = item_links[3:]  # 去除广告商品
        print(len(item_links))
        print(item_links)