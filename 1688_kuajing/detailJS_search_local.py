from selenium import webdriver
from urllib import parse
import time
from selenium.webdriver.common.by import By
import re
import pandas as pd
import logging
import random

'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='1688_search_local.log', filemode='w')


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_argument('lang=zh_CN.UTF-8')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
driver  =  webdriver.Chrome(executable_path=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)


# 构建信息列表
goodNameList = []
companyNameList = []
titelList = []
goodsUrlList = []
repurchaseList = []
priceList = []
dealList = []
pinjiaList = []
evaluateList = []
collectList = []

# 构建dataFrame
data = {
    "关键词": goodNameList,
    '公司名称': companyNameList,
    '标题': titelList,
    '商品详情地址': goodsUrlList,
    '复购率': repurchaseList,
    '商品价格': priceList,
    '成交量': dealList,
    '商品评价': evaluateList,
    '收藏数': collectList
}

goodName = input("请输入需要爬取的商品名称：")
fistWindows = driver.current_window_handle
driver.get(
    "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Ftheme%25253Dfactory&style=tao_custom&from=1688web")
time.sleep(15)

start = time.time()
for page in range(1,6):
    driver.get("https://s.1688.com/selloffer/offer_search.htm?keywords={}&spm=a260k.dacugeneral.search.0&beginPage={}#sm-filtbar".format(parse.quote(goodName.encode('gbk')),page))
    time.sleep(5)

    count=1000
    for i in range(6):
        driver.execute_script("document.documentElement.scrollTop={}".format(count))
        time.sleep(random.randint(3,4))
        count+=1000

    with open('file.js') as f:
        js = f.read()
        js_string = '{}'.format(js)

    driver.execute_script(js_string)
    time.sleep(random.randint(3,4))
    driver.find_element(By.ID,'ywg-alibaba-list-btn').click()
    # 一直到变化的div
    items = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[7]/div[4]/div/div/ul/div")
    print(len(items))
    logging.info("当前页有%s个数据条列"%len(items))
    num=0

    try:
        for itemIndex in range(len(items)):
            # 添加商品名称
            goodNameList.append(goodName)
            # 标题
            titel = items[itemIndex].find_element(By.XPATH, './div/div[2]/a/div').text
            titelList.append(titel)
            # 详情地址
            goodsurl = items[itemIndex].find_element(By.XPATH, './div/div[2]/a').get_attribute("href")
            goodsUrlList.append(goodsurl)
            try:
                # 复购率
                repurchase = items[itemIndex].find_element(By.XPATH, './div/div[4]/div/span').text
                repurchaseList.append(repurchase)
            except Exception as error:
                logging.error("错误是%s" % error)
                repurchase = "暂无复购率"
                repurchaseList.append(repurchase)
            # 价格
            price = items[itemIndex].find_element(By.XPATH, './div/div[5]/div[1]/div[2]').text + "元"
            priceList.append(price)
            # 成交量
            deal = items[itemIndex].find_element(By.XPATH, './div/div[5]/div[2]/div').text
            if deal == "":
                deal = "暂无成交量"
            dealList.append(deal)
            # 公司名称
            companyName = items[itemIndex].find_element(By.XPATH, './div/div[6]/div[2]/a/div').text
            companyNameList.append(companyName)
            # 评价和收藏
            pinjia = items[itemIndex].find_element(By.XPATH, './span').text
            if "璇勪环" in pinjia:
                pinjia = pinjia.replace("璇勪环", "评价").replace("鏀惰棌", "收藏")
                # 正则分离
                matches = re.findall(r'评价:(\d+),收藏:(\d+)', pinjia)
                evaluate = matches[0][0]
                collect = matches[0][1]
                print(evaluate, collect)
            evaluateList.append(evaluate)
            collectList.append(collect)
            num += 1
    except Exception as error:
        print(error)
        logging.error("错误是%s" % error)

    time.sleep(random.randint(5, 8))

    print("爬到了%s条商品信息" % num)
    driver.refresh()
    time.sleep(random.randint(5, 8))

    logging.info("爬完了第%s页" % page)
    logging.info("爬到了%s条商品信息" % num)

driver.quit()
end = time.time()
logging.info("累计耗时%s" %(end-start))
df = pd.DataFrame(data)
df.to_excel('./{}.xlsx'.format(goodName))
