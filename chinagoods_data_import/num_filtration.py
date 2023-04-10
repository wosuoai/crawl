import pandas as pd
from selenium import webdriver
from urllib import parse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_argument('lang=zh_CN.UTF-8')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
driver  =  webdriver.Chrome(executable_path=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)


all_word=[]
all_link=[]
data_frame_1 = pd.read_csv("C:\\Users\\admin\\PycharmProjects\\袜子.csv")
for word in data_frame_1["关键词"]:
    if len(word)<=4:
        link = "https://www.yiwugo.com/keyword_more.html?keyword={}".format(parse.quote(word.encode('utf-8')))
        all_word.append(word)
        all_link.append(link)
    else:
        pass

search_keyList=[]
search_numList=[]
for search in all_link:
    driver.get(search)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'frame')))
    search_key=driver.find_element(By.XPATH,'//*[@id="word"]/ul[2]/li[2]/span[1]/a').text
    search_num=driver.find_element(By.XPATH, '//*[@id="word"]/ul[2]/li[2]/span[2]/a').text
    if search_num=="< 100":
        pass
    else:
        print(search_key,search_num)
        search_keyList.append(search_key)
        search_numList.append(search_num)
    time.sleep(random.randint(2,3))

driver.quit()
df = pd.DataFrame({"关键词":search_keyList,"搜索次数":search_numList})
df.to_excel('./{}.xlsx'.format('search_keyword'))
