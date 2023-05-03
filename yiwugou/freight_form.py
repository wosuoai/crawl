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
with open(r"E:\义乌购商铺信息\cookies\88800799.txt", mode="r", encoding="utf-8") as f:
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


driver.get("https://work.yiwugo.com/")
time.sleep(1)

try:
    #判断是否有弹窗
    if xpathExists("/html/body/div[6]/div[3]/button"):
        driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/button").click()
except:
    pass
finally:
    #运费模板
    driver.find_element(By.XPATH, "/html/body/div[2]/ul/li[2]/a[6]").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[1]/td/input").send_keys("限时秒杀")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[2]/td/label[2]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[1]/input[1]").send_keys("1")
    a=driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[1]/input[2]")
    a.clear()
    a.send_keys("5")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[1]/input[3]").send_keys("1")
    b=driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[1]/input[4]")
    b.clear()
    b.send_keys("1")
    
    #1
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[1]/span[1]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[1]/span[2]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[1]/span[3]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/div[2]/input[1]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[2]/td[3]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[2]/td[4]/input").send_keys("5")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[2]/td[5]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[2]/td[6]/input").send_keys("1.5")
    
    #2
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/a").click()
    for i in range(1,8):
        driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[2]/span[{}]/label".format(i)).click()
    for j in range(1, 5):
        driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[2]/span[{}]/label".format(j)).click()
    for k in range(1, 5):
        driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[2]/span[{}]/label".format(k)).click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[4]/span[6]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[4]/span[7]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[4]/span[8]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/div[2]/input[1]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td[3]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td[4]/input").send_keys("6")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td[5]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td[6]/input").send_keys("2")
    
    #3
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[4]/span[5]/label").click()
    for i in range(1,5):
        driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[5]/span[{}]/label".format(i)).click()
    for j in range(1, 4):
        driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[6]/span[{}]/label".format(j)).click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/div[2]/input[1]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[4]/td[3]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[4]/td[4]/input").send_keys("7")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[4]/td[5]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[4]/td[6]/input").send_keys("3")
    
    #4
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[7]/span[1]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[7]/span[2]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/div[2]/input[1]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[5]/td[3]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[5]/td[4]/input").send_keys("99")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[5]/td[5]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[5]/td[6]/input").send_keys("99")
    
    #5
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[7]/span[3]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[7]/span[4]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/ul/li[7]/span[5]/label").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/div[2]/div[2]/input[1]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[6]/td[3]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[6]/td[4]/input").send_keys("999")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[6]/td[5]/input").send_keys("1")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[3]/td/div[2]/table/tbody/tr[6]/td[6]/input").send_keys("999")
    
    driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[4]/td/input").click()
