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
import pyperclip
from selenium.webdriver.common.keys import Keys

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
with open(r"E:\义乌购商铺信息\cookies\73333406.txt", mode="r", encoding="utf-8") as f:
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

    for i in range(2,21):
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr[{}]/td[10]/a[1]".format(i)).click()
        time.sleep(2)
        if xpathExists("/html/body/div[7]/div[3]/button"):
            driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/button").click()
        try:
            # 修改详细描述中上传错误的图片
            comfirmdel=driver.find_element(By.XPATH,'/html/body/div[2]/div/form/table/tbody/tr[22]/td/div[1]/div[1]/div[1]/span[1]')
            driver.execute_script("arguments[0].click();", comfirmdel)
            textarea=driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[22]/td/div[1]/div[1]/div[2]/textarea").get_attribute("value")
            """
            <img src="http://ywgimg.yiwugo.com/product/shop_270384/normal/945165535/20230509/wtT7Y6bQvaRCKYUq.jpg" alt="" />
            这里面有两个一直变化的量：945165535，wtT7Y6bQvaRCKYUq
            预计是根据前面的数字，来对图片名称进行加密得
            """
            html_list=textarea.split("\n")
            for img in html_list:
                if "img" in html_list[0]:
                    del html_list[0]
                else:
                    pass
            true_html='<img src="http://ywgimg.yiwugo.com/product/shop_270384/normal/945165535/20230509/wtT7Y6bQvaRCKYUq.jpg" alt="" />'
            for element in html_list:
                true_html+="\n"+element
            driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[22]/td/div[1]/div[1]/div[1]/span[27]/span").click()
            tmp=driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/textarea")
            tmp.clear()
            pyperclip.copy(true_html)   # 将长文本复制到剪切板
            tmp.send_keys(Keys.CONTROL,"v") # 模拟组合键Control+v
            driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/span[27]/span").click()

            # 判断是否选择运费模板
            freight = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[26]/td/table/tbody/tr[1]/td/select/option[1]").text
            if freight == "请选择运费模板":
                # 定位下拉框,实例化select方法
                ele = driver.find_element(By.ID, "freightTemplateId")
                select_ele = Select(ele)
                select_ele.select_by_visible_text("运费")
                time.sleep(1)

            # 判断商品重量
            weight_num = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[27]/td/table/tbody/tr/td/div/input").text
            if weight_num == "" or weight_num == "0":
                weight = driver.find_element(By.XPATH,"/html/body/div[2]/div/form/table/tbody/tr[27]/td/table/tbody/tr/td/div/input")
                weight.clear()
                weight.send_keys("0.2")

            try:
                driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > input").click()
            except:
                driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(3) > div > form > table > tbody > tr.p_b_h > td > input").click()

            time.sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[1]/div/div[2]/p/a").click()
            time.sleep(0.5)
        except:
            # 不能正常修改下架该商品
            title = driver.find_element(By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[1]/td/div/input").get_attribute("value")
            driver.get("https://work.yiwugo.com/product_s/productlist/1.htm?t=1")
            input_title = driver.find_element(By.ID, "title")
            input_title.clear()
            input_title.send_keys(title)
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/form/ul/li[9]/input").click()
            time.sleep(0.5)

            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr[2]/td[10]/a[2]").click()
            time.sleep(2)
            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/button").click()
            driver.get("https://work.yiwugo.com/product_s/productlist/{}.htm?t=1".format(int(page_num) - 1))
            time.sleep(0.5)

    driver.refresh()

print("该店铺所有商品二维码已全部添加")
driver.close()
