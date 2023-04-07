#from inspect import _void
from numpy import void
from selenium import webdriver
#from lxml import etree
from selenium.webdriver.common.by import By
import time
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import base64
import uuid
import urllib.request

## 解码 url 图片
def decodeUrlImage(src:str)->void:
    res = urllib.request.urlopen(src, timeout=3).read()
    filename = "{}.{}".format(uuid.uuid4(),"jpg")
    with open("target/"+filename, "wb") as file:
        file.write(res)

## 解码base64图片
def decode_image(src:str)->void:
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")

    img = base64.urlsafe_b64decode(data)
    filename = "{}.{}".format(uuid.uuid4(), ext)
    with open("target/"+filename, "wb") as f:
        f.write(img)

def ChromeSimulation(chromeUrl:str)->void:

    driver = webdriver.Chrome("C:/Users/admin/Anaconda3/chromedriver.exe",chrome_options=option)
    driver.get(chromeUrl)
    #source = driver.page_source

    searchBox=driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    searchInput=input("请输入你想搜索的图片名称: ")
    searchBox.send_keys(searchInput)
    searchBox.send_keys(Keys.ENTER)

    driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
    #selenium报错，click后强制sleep
    time.sleep(2)

    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        imgContent=driver.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img')
        for imgSrc in imgContent:
            try:
                imgUrl=imgSrc.get_attribute("src")
                if "data" in imgUrl:
                    # base64图片链接保存
                    decode_image(imgUrl)
                if "http" in imgUrl:
                    # Unicode图片链接保存
                    decodeUrlImage(imgUrl)
            except Exception as error:
                print("this is error")

        #网页按照显示尺寸大小向下滚动
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')

        try:
            driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        except:
            pass
        #点击显示更多搜索结果
        if new_height == last_height:
            try:
                driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
            except:
                break
        last_height = new_height


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    #打开开发者模式防止被网页识别，并过滤无用日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    #打开无界面浏览模式，但需要设置sleep，否则容易被网页的反爬机制所限制
    #option.add_argument('--headless')
    ChromeSimulation("https://www.google.com/")
