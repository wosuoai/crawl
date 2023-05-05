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
from selenium.webdriver.support.select import Select

option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("--disable-javascript")
driver=webdriver.Chrome(executable_path=r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()

#定义一个xpath的捕获异常
def xpathExists(xpath):
   try:
      driver.find_element(By.XPATH,xpath)
      return True
   except:
      return False

def set_element_value(driver, xpath, value):
    """ Xpath中使用双引号，则拼接js时要使用单引号包裹双引号，否则会出现missing)after argument list """
    js = f'var ele = document.evaluate(\'{xpath}\', document).iterateNext(); ele.value = arguments[0];'
    driver.execute_script(js, value)

driver.get("https://www.yiwugo.com/")
driver.delete_all_cookies()

# 读取cookies
with open(r"E:\义乌购商铺信息\hot_cookies\Y4005301.txt", mode="r", encoding="utf-8") as f:
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


driver.get("https://work.yiwugo.com/product_s/productlist/1.htm?t=1")
time.sleep(1)

page_num=driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/ul/li[10]/a").text
for page in range(int(page_num)):
    driver.get("https://work.yiwugo.com/product_s/productlist/{}.htm?t=1".format(int(page_num)-1))
    time.sleep(0.5)

    # 一直到变化的div
    for i in range(2,21):
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr[{}]/td[10]/a[1]".format(i)).click()
        time.sleep(2)
        if xpathExists("/html/body/div[7]/div[3]/button"):
            driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/button").click()
        #上传图片修改详细描述
        driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[22]/td/div[1]/div[1]/div[1]/span[41]/input").send_keys("C:\\Users\\Administrator\\Desktop\\尹.png")
        freight=driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[26]/td/table/tbody/tr[1]/td/select/option[1]").text
        #判断是否选择运费模板
        if freight=="请选择运费模板":
            # 定位下拉框,实例化select方法
            ele = driver.find_element(By.ID, "freightTemplateId")
            select_ele = Select(ele)
            select_ele.select_by_value("111997")
            time.sleep(1)

        save=''
        try:
            save=driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[30]/td/input").get_attribute("value")
            print(save)
        except:
            pass
        if save=="发布商品":
            driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[30]/td/input").click()
        else:
            driver.find_element(By.XPATH, "/html/body/div[5]/input").click()

        time.sleep(0.5)
        driver.get("https://work.yiwugo.com/product_s/productlist/{}.htm?t=1".format(int(page_num)-1))
        time.sleep(0.5)

    driver.refresh()

print("该店铺所有商品二维码已全部添加")
driver.close()
