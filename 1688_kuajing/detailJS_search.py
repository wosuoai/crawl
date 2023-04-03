from selenium import webdriver
from urllib import parse
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import re
import logging
import random
import pymysql

'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='1688test.log', filemode='w')

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="aifeibaihuo",
    database="new_goods"
)
cursor = conn.cursor()


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_argument('lang=zh_CN.UTF-8')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
driver  =  webdriver.Chrome(executable_path=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
# driver.get("https://www.1688.com/")
# time.sleep(3)
# cookies = 
# driver.delete_all_cookies()
# for cookie in cookies:
#     driver.add_cookie(cookie_dict=cookie)
# time.sleep(3)


goodName = input("请输入需要爬取的商品名称：")
fistWindows = driver.current_window_handle
driver.get(
    "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Ftheme%25253Dfactory&style=tao_custom&from=1688web")
time.sleep(15)

start = time.time()
for page in range(1,6):
    driver.get("https://s.1688.com/selloffer/offer_search.htm?keywords={}&spm=a260k.dacugeneral.search.0&beginPage={}#sm-filtbar".format(parse.quote(goodName.encode('gbk')),page))
    time.sleep(5)

    count=800
    for i in range(6):
        driver.execute_script("document.documentElement.scrollTop={}".format(count))
        time.sleep(random.randint(3,4))
        count+=800

    with open('file.js') as f:
        js = f.read()
        js_string = '{}'.format(js)

    driver.execute_script(js_string)
    time.sleep(random.randint(3,4))
    driver.find_element(By.ID,'ywg-alibaba-list-btn').click()
    num=0

    try:
        for j in range(1,61):
            # 标题
            titel = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[2]/a/div'.format(j)).text
            # 详情地址
            # goodsurl = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[2]/a'.format(j)).get_attribute("href")
            # goodsurl = goodsurl.replace('/\?.*/', '')
            # print(goodsurl)
            # goodsUrlList.append(goodsurl)
            try:
                # 复购率
                repurchase = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[4]/div/span'.format(j)).text
            except Exception as error:
                print(error)
                logging.error("错误是%s" % error)
                repurchase = "暂无复购率"
            # 价格
            price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[5]/div[1]/div[2]'.format(j)).text
            # 成交量
            deal = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[5]/div[2]/div'.format(j)).text
            # 公司名称
            companyName = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/div/div[6]/div[2]/a/div'.format(j)).text
            # 评价和收藏
            pinjia = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[4]/div/div/ul/div[{}]/span'.format(j)).text
            pinjia = pinjia.replace("璇勪环", "评价").replace("鏀惰棌", "收藏")
            # 正则分离
            match = re.findall(r'评价:(\d+),收藏:(\d+)',pinjia)
            evaluate = match[0][0]
            collect = match[0][1]
            print(evaluate,collect)

            num += 1
            createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            item = {
                "search_key": goodName,
                "company_name": companyName,
                "good_subject": titel,
                "price": price,
                "deal": deal,
                "buyback_rate": repurchase,
                "evaluate": evaluate,
                "collect": collect,
                "create_time": createdTime
            }

            sql = "insert into 1688_key_search (`search_key`, `company_name`, `good_subject`, `price`, `deal`, `buyback_rate`, `evaluate`, `collect`,`create_time`) \
                        values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')" % (item["search_key"], item["company_name"], item["good_subject"], item["price"],
                            item["deal"], item["buyback_rate"], item["evaluate"], item["collect"], item["create_time"])
            cursor.execute(sql)
            conn.commit()
    except Exception as error:
        print(error)
        logging.error("错误是%s" % error)

    time.sleep(random.randint(5, 8))

    driver.refresh()
    time.sleep(random.randint(3, 5))

    logging.info("爬完了第%s页" % page)
    logging.info("爬到了%s条商品信息" % num)

conn.close()
end = time.time()
total = end-start
print(total)
logging.info("累计耗时%s" % total)
