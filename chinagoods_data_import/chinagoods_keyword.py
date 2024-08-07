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


key = ["船袜","袜子"]

for keyword in key:
    time.sleep(3)
    driver.get('https://www.chinagoods.com/search/product/{}'.format(parse.quote(keyword.encode('utf-8'))))
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPagination"]/button[2]/span')))

    count=300
    for i in range(6):
        driver.execute_script("document.documentElement.scrollTop={}".format(count))
        time.sleep(random.randint(1,2))
        count+=300

    goodsUrlList=[]
    for i in range(1,60):
        if driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[{}]/div/div[1]/div[1]'.format(i)).text=="广告":
            pass
        else:
            goodsurl = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[{}]/div/a'.format(i)).get_attribute("href")
            goodsUrlList.append(goodsurl)
    #print('该页面总共有%s个可用链接'%(len(goodsUrlList)))

    for url in goodsUrlList:
        driver.get(url)
        driver.set_page_load_timeout(45)
        driver.implicitly_wait(2)
        html_elements=driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div[1]/div[2]/div[1]/div[1]/span[2]/span/a')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'product_description')))
        for element in html_elements:
            #print(element.text)
            print("%s属于%s类目"%(keyword,element.text))
        time.sleep(random.randint(1,2))

driver.quit()
