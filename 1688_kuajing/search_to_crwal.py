from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib import parse
import random
import logging

'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='1688spider.log', filemode='w')

import pandas as pd

# option.add_argument('--headless')
# 无头模式
option = webdriver.ChromeOptions()
# 允许root模式允许google浏览器
option.add_argument('--no-sandbox')
# option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# 打开无痕浏览模式
#option.add_argument("--incognito")
# 关闭开发者模式
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(
    executable_path=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",
    chrome_options=option)


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
def getImgUrl(imgStr: str) -> str:
    try:
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        return re.findall(p1, imgStr)[0]
    except:
        return ""


if __name__ == "__main__":
    # 构建信息列表
    titelList = []
    priceList = []
    companyNameList = []
    goodNameList = []
    dealList = []
    goodsUrlList = []
    pinjiaList = []

    # 构建dataFrame
    data = {
        '商品类型': goodNameList,
        '标题': titelList,
        '商品详情地址': goodsUrlList,
        '商品价格': priceList,
        '成交量': dealList,
        '公司名称': companyNameList,
        '商品评价': pinjiaList
    }
    goodName = input("请输入需要爬取的商品名称：")
    page = int(input("请输入需要爬取的页码数："))

    fistWindows = driver.current_window_handle
    driver.get(
        "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Ftheme%25253Dfactory&style=tao_custom&from=1688web")
    time.sleep(25)

    # page=3 就是从3开始爬取
    for i in range(28, page + 1):
        try:
            #fistWindows = driver.current_window_handle
            # driver.get(
            #     "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Ftheme%25253Dfactory&style=tao_custom&from=1688web")
            # time.sleep(25)
            driver.get(
                "https://s.1688.com/selloffer/offer_search.htm?keywords={}&spm=a26352.13672862.searchbox.input&beginPage={}#sm-filtbar".format(
                    parse.quote(goodName.encode('gbk')), i))
            # 在这段延迟时间里进行淘宝扫描登陆
            #time.sleep(25)
            # 一直到变化的div
            items = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[7]/div[4]/div/div/ul/div")
            print("该页面获取全部对象成功,对象数量%s" % len(items))

            for itemIndex in range(len(items)):
                # 初始化部分数值
                titel = ""
                goodsurl = ""
                price = ""
                deal = ""
                companyName = ""
                pinjia = "未获取到评价"

                # 标题
                titel = items[itemIndex].find_element(By.XPATH, './div/div[2]/a/div').text
                titelList.append(titel)
                # 详情地址
                goodsurl = items[itemIndex].find_element(By.XPATH, './div/div[2]/a').get_attribute("href")
                goodsUrlList.append(goodsurl)
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

                try:
                    try:
                        toDetail = items[itemIndex].find_element(By.XPATH, './div/div[2]/a/div')
                        # 点击详情
                        toDetail.click()
                        time.sleep(random.randint(1, 3))
                        #  切换到新窗口新链接
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(random.randint(1, 3))
                    except Exception as error:
                        pinjiaList.append(pinjia)
                        goodNameList.append(goodName)
                        print("----------")
                        print(titel, goodsurl, price, deal, companyName, pinjia)
                        print("----------")
                        time.sleep(random.randint(1, 3))
                        # 回到首页
                        driver.switch_to.window(fistWindows)
                        continue

                    try:
                        # 这里可能出现错误
                        # pageSource=driver.page_source
                        pinjia = driver.find_element(By.XPATH,
                                                     '/html/body/div[3]/div/div[1]/div/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div').text
                        # 评价添加
                        pinjiaList.append(pinjia)
                        # 添加商品名称
                        goodNameList.append(goodName)
                        print("----------")
                        print(titel, goodsurl, price, deal, companyName, pinjia)
                        print("----------")
                        try:
                            # 关闭新的窗口
                            driver.close()
                            # time.sleep(random.randint(1,3))
                            # 重新切换到第一个窗口 回到首页
                            driver.switch_to.window(fistWindows)
                            time.sleep(random.randint(1, 3))
                        except Exception as error:
                            # 回到首页
                            driver.switch_to.window(fistWindows)
                            time.sleep(random.randint(1, 3))
                            continue
                    except Exception as error:
                        # 获取拼接
                        pinjiaList.append(pinjia)
                        # 添加商品名称
                        goodNameList.append(goodName)
                        print("----------")
                        print(titel, goodsurl, price, deal, companyName, pinjia)
                        print("----------")
                        continue

                except Exception as error:
                    continue

        except Exception as error:
            print(error)
            logging.error("错误是%s" % error)
        logging.info("爬完了第%s页" % page)
        # 每次爬完一页就写入一页，防止最终什么数据都没有
        df = pd.DataFrame(data)
        df.to_excel('./{}.xlsx'.format(goodName))
