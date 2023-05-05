from selenium import webdriver
from urllib import parse
import time
from selenium.webdriver.common.by import By
import re
import pandas as pd
import logging
import random
import json
import requests
from bs4 import BeautifulSoup
import ast


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
driver=webdriver.Chrome(executable_path=r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()

#定义一个xpath的捕获异常
def xpathExists(xpath):
   try:
      driver.find_element(By.XPATH,xpath)
      return True
   except:
      return False

driver.get("https://www.yiwugo.com/")
driver.delete_all_cookies()

# 读取cookies
with open(r"E:\义乌购商铺信息\cookies\73333197.txt", mode="r", encoding="utf-8") as f:
    ck = f.read()

b=json.dumps(ck).replace("work.yiwugo.com",".yiwugo.com")
#cookies=json.loads(b)

# ast强制转换str--->list
cookies=ast.literal_eval(json.loads(b))
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']  # 删除报错的expiry字段
    driver.add_cookie(cookie)
driver.refresh()
driver.implicitly_wait(2)

#义乌购是点击链接后新开一个窗口
driver.get("https://www.yiwugo.com/product/detail/934247243.html")
handle = driver.current_window_handle   #获取当前窗口句柄
driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div[3]/div[1]/span[2]/a[1]").click()
handles = driver.window_handles #获取所有窗口句柄
driver.switch_to.window(handles[1]) #进入新窗口


#获取该商品每个款式的价格，并上调价格做限时秒杀
priceList = []
try:
    items = driver.find_elements(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[15]/td/div/table/tbody/tr")
    print(len(items))
    for item in range(1,len(items)-1):
        old_price = items[item].find_element(By.XPATH, './td[4]/input').get_attribute("value")
        priceList.append(old_price)
    print(priceList)

    for i in range(len(priceList)):
        new_price = round(float(priceList[i])/0.8,2)
        print(new_price)
        #价格调整
        clean=driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[15]/td/div/table/tbody/tr[{}]/td[4]/input".format(i+2))
        clean.clear()
        clean.send_keys(str(new_price))
        #调整商品数量为零的情况
        goods_num = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[15]/td/div/table/tbody/tr[{}]/td[5]/input".format(i+2)).get_attribute("value")
        num_clean = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[15]/td/div/table/tbody/tr[{}]/td[5]/input".format(i+2))
        if str(goods_num)=='0':
            num_clean.clear()
            num_clean.send_keys(str(random.randint(10,100)))
        else:
            continue
except:
    pass
finally:
    #这是另外一个商品价格的模板
    if priceList==[]:
        items = driver.find_elements(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[11]/td/table[2]/tbody/tr")
        print(len(items))
        try:
            for item in range(1, len(items)):
                old_price = items[item].find_element(By.XPATH, './td[1]/input[2]').get_attribute("value")
                priceList.append(old_price)
            print(priceList)
        except:
            pass

        for i in range(len(priceList)):
            new_price = round(float(priceList[i])/0.8, 2)
            print(new_price)
            clean = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[11]/td/table[2]/tbody/tr[{}]/td[1]/input[2]".format(i + 2))
            clean.clear()
            clean.send_keys(str(new_price))
    else:
        pass
