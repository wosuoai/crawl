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
cookiesList = [{
                   'tfstk': 'dflHfMs2tvyQ-oukq6FB9ZsvfUptRMN720C827EyQlrsJ8rJd02o2cwr9W3Kjb0KC_LQ9LNoqlmFwJhoP_4rz0TQ2e9tR2N7anKAZI3IR7G2DnIE3jx0N7-vDIdxR2NS0CtlWtvn8hf16s5Oqw_T7_5r_Qw3m2WRa_lg-JXI8O7cQt7NO_awyfW5FJz_SoUxNwdG.',
                   'l': 'fBg6RSc4N3uVhiVzBOfaFurza77OSIRYYuPzaNbMi9fP_Y1B59C1W19MSrL6C3GVF67HR38PiVPBBeYBqQAonxv9w8VMULkmndLHR35..',
                   'uc1': 'cookie15=URm48syIIVrSKA%3D%3D&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7oPIg&cookie14=Uoe9b6l2BvrXiQ%3D%3D&pas=0',
                   '_nk_': 'tb82043229', '_l_g_': 'Ug%3D%3D',
                   'cookie1': 'UoMzgezpddPRRNA%2BCOjq9bWgwscNZZWmPolL71wcS1M%3D', 'dnk': 'tb82043229',
                   'cancelledSubSites': 'empty', 'sg': '92b', 'mt': 'ci=0_1', 'lgc': 'tb82043229', 'csg': '572b1c04',
                   'uc3': 'vt3=F8dCsGd%2BGfx1LDRranw%3D&id2=UUpgQEvwuxBfi25wxA%3D%3D&nk2=F5RNZ%2BB4f8h9FA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D',
                   'unb': '2216225431902', 'cookie2': '2c326e050e664659b49d2d71975da22d',
                   'uc4': 'id4=0%40U2gqz6QafAOV0MtvTNM1aQ3RgHN9vKjA&nk4=0%40FY4GsEDQgJWFAvgKMhdW03KKzNQL',
                   '_tb_token_': '55b05b51e58e3', '_samesite_flag_': 'true', '_cc_': 'URm48syIZQ%3D%3D',
                   'cookie17': 'UUpgQEvwuxBfi25wxA%3D%3D', 'xlly_s': '1', 'existShop': 'MTY5MjA4MjQzMg%3D%3D',
                   '_m_h5_tk_enc': 'b41950ace76b04c46ffb112dc1602ace',
                   '_m_h5_tk': '2b5857e8d948ce3aeaeea6f814055fd2_1691750466570',
                   'isg': 'BJKSSdxEIvbY6l7ofy_M_oR041h0o5Y9Q9KTS1zrv8UwbzNpUDbCTDed2cvTBA7V', 'skt': '1d59b0cc87f1c69d',
                   'sgcookie': 'E100i0ZCNejMZHhc%2BG4sK8aBKp9azMzB%2Fqxfq9to%2BLD4qHDpdvHRyqVDQFUpQlDaR5pZDAxYDq4dCOKHRTQZp8ZzXbeoxr0pr652logjoc0hiHVtTjdJ%2BmEqMv0wZFILN90Q',
                   'tracknick': 'tb82043229', 'cna': 'duFAHTR2tzYCAX158qGMeKOh', 'thw': 'cn',
                   't': 'be650f779bda6984ae19184e3075c83c'}]


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