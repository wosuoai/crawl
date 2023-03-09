from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib import parse

import pandas as pd
# option.add_argument('--headless')
# 无头模式
option = webdriver.ChromeOptions()
# 允许root模式允许google浏览器
option.add_argument('--no-sandbox')
# option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# 关闭开发者模式
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=r"C:\Users\wosuoai\.cache\selenium\chromedriver\win32\110.0.5481.77\chromedriver.exe",chrome_options=option)
# 隐藏对selenium的检测
# //滑块解决
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })

# 正则提取1688图片url
def getImgUrl(imgStr:str)->str:
    try:
        p1=re.compile(r'[(](.*?)[)]', re.S) 
        return re.findall(p1,imgStr)[0]
    except:
        return ""

if __name__=="__main__":
    # 构建信息列表
    urlList=[]
    priceList=[]
    companyNameList=[]
    goodNameList=[]
    # 构建dataFrame
    data = {
        '商品类型':goodNameList,
        '图片地址': urlList,
        '商品价格': priceList,
        '公司名称': companyNameList
        }
    goodName=input("请输入需要爬取的商品名称：")
    page=int(input("请输入需要爬取的页码数："))

    for i in range(1,page):
        try:
            driver.get("https://s.1688.com/selloffer/offer_search.htm?keywords={}&spm=a26352.13672862.searchbox.input&beginPage={}#sm-filtbar".format(parse.quote(goodName.encode('gbk')),i))
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            # 一直到变化的div
            items=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[7]/div[4]/div/div/ul/div")
            print("该页面获取全部对象成功")
            print(len(items))

            for itemIndex in range(len(items)):
                # 图片地址
                imgUrl=getImgUrl(items[itemIndex].find_element(By.XPATH,'./div/div[1]/div/a/div').get_attribute("style"))
                urlList.append(imgUrl)
                # 价格
                price=items[itemIndex].find_element(By.XPATH,'./div/div[5]/div[1]/div[2]').text
                priceList.append(price)
                # 公司名称
                companyName=items[itemIndex].find_element(By.XPATH,'./div/div[6]/div[2]/a/div').text
                companyNameList.append(companyName)
                # 添加商品名称
                goodNameList.append(goodName)
                # print(price,companyName,imgUrl)
        except Exception as error:
            print(error)
    # 最终完成
    df = pd.DataFrame(data)
    df.to_excel('./{}.xlsx'.format(goodName))
