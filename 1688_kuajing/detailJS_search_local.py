from selenium import webdriver
from urllib import parse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import re
import pandas as pd
import logging
import random
import multiprocessing


'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='1688_wap.log', filemode='w')


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
#option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 通过端口号接管已打开的浏览器
option.add_argument('--disable-infobars')  # 不显示chrome正受到自动测试软件的控制
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')    #去掉webdriver痕迹
driver=webdriver.Chrome(executable_path=r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()


# 构建信息列表
goodNameList = []
titelList = []
goodsUrlList = []
dealList = []
evaluateList = []
collectList = []

# 构建dataFrame
data = {
    "关键词": goodNameList,
    '标题': titelList,
    '商品详情地址': goodsUrlList,
    '成交量': dealList,
    '商品评价': evaluateList,
    '收藏数': collectList
}

#定义一个xpath的捕获异常
def xpathExists(xpath):
   try:
      driver.find_element(By.XPATH,xpath)
      return True
   except:
      return False

#模拟拖动滑块
def move_to_gap(tracks):
    if xpathExists('//*[@id="nc_1_n1t"]/span'):
        # 找到滑块span
        need_move_span = driver.find_element(By.XPATH,'//*[@id="nc_1_n1t"]/span')
        # 模拟按住鼠标左键
        ActionChains(driver).click_and_hold(need_move_span).perform()
        for x in tracks: # 模拟人的拖动轨迹
            print(x)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=random.randint(1,3)).perform()
        time.sleep(1)
        ActionChains(driver).release().perform() # 释放左键
    else:
        pass


def get_track(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+(1/2)at²
    ③v²-v0²=2as

    :param distance: 需要移动的距离
    :return: 存放每0.2秒移动的距离
    '''
    # 初速度
    v = 0
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t = 0.1
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 4 / 5

    distance += 10  # 先滑过一点，最后再反着滑动回来

    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = 2  # 加速运动
        else:
            a = -3  # 减速运动

        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))

        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t

    # 反着滑动到大概准确位置
    for i in range(3):
        tracks.append(-2)
    for i in range(4):
        tracks.append(-1)
    return tracks

driver.get("https://www.1688.com/")
driver.delete_all_cookies()
cookies = []

for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']  # 删除报错的expiry字段
    driver.add_cookie(cookie)
driver.refresh()
time.sleep(2)

def get_data(goodName):
    for page in range(1,51):
        driver.get("https://s.1688.com/selloffer/offer_search.htm?keywords={}&spm=a260k.dacugeneral.search.0&beginPage={}#sm-filtbar".format(parse.quote(goodName.encode('gbk')),page))
        time.sleep(random.randint(2,3))

        # 页面异常处理
        if xpathExists('//*[@id="app"]/div/div[6]/div[4]/div/div/div[2]/h2')==False and xpathExists('//*[@id="sm-offer-list"]/div[4]/div/div[2]/a/div')==True:

            count=1000
            for i in range(6):
                driver.execute_script("document.documentElement.scrollTop={}".format(count))
                time.sleep(1)
                count+=1000

            with open('file.js') as f:
                js = f.read()
                js_string = '{}'.format(js)

            driver.execute_script(js_string)
            time.sleep(random.randint(2,3))
            try:
                driver.find_element(By.ID,'ywg-alibaba-list-btn').click()
            except Exception as error:
                logging.error("错误是%s" % error)
                move_to_gap(get_track(295))

            # 一直到变化的div
            items = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[7]/div[4]/div/div/ul/div")

            # 判断页面有多少广告位
            start_item = 0
            for i in range(1, len(items)):
                if xpathExists('//*[@id="sm-offer-list"]/div[{}]/div/a/div[3]/div[1]'.format(i)):
                    if driver.find_element(By.XPATH, '//*[@id="sm-offer-list"]/div[{}]/div/a/div[3]/div[1]'.format(i)).text == "广告":
                        start_item += 1
                else:
                    break
                start_item = start_item

            print("当前页有%s个数据条列" % (len(items) - start_item))
            logging.info("当前页有%s个数据条列" % (len(items) - start_item))
            num=0

            try:
                for itemIndex in range(start_item,len(items)):
                    # 标题
                    titel = items[itemIndex].find_element(By.XPATH, './div/div[2]/a/div').text
                    # 详情地址
                    goodsurl = items[itemIndex].find_element(By.XPATH, './div/div[2]/a').get_attribute("href")
                    if "detail" not in goodsurl:
                        goodsurl = ""
                    # 成交量
                    deal = items[itemIndex].find_element(By.XPATH, './div/div[5]/div[2]/div').text
                    if deal == "":
                        deal = "暂无成交量"
                    try:
                        # 评价和收藏
                        pinjia = items[itemIndex].find_element(By.XPATH, './span').text
                        if "璇勪环" in pinjia:
                            pinjia = pinjia.replace("璇勪环", "评价").replace("鏀惰棌", "收藏")
                            # 正则分离
                            matches = re.findall(r'评价:(\d+),收藏:(\d+)', pinjia)
                            evaluate = matches[0][0]
                            collect = matches[0][1]
                            #print(evaluate, collect)

                        # 只获取符合条件的信息
                        if (int(evaluate) >= 500 and int(collect) >= 500 and goodsurl != ""):
                            goodNameList.append(goodName)
                            titelList.append(titel)
                            goodsUrlList.append(goodsurl)
                            dealList.append(deal)
                            evaluateList.append(evaluate)
                            collectList.append(collect)

                        num += 1
                    except Exception as error:
                        logging.error("错误是%s" % error)

            except Exception as error:
                logging.error("错误是%s" % error)

            print("该页面共%s条信息" % num)
            driver.refresh()
            driver.implicitly_wait(2)

            logging.info("爬完了第%s页" % page)
            logging.info("该页面共%s条信息，%s条有效信息" % num)

        else:
            continue

    df = pd.DataFrame(data)
    df.to_excel('./test/{}.xlsx'.format(goodName))


if __name__ == '__main__':
    searchkey_data = pd.read_excel("C:\\Users\\Administrator\\Desktop\\订单管理总表.xlsx", sheet_name="Sheet4")
    #pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

    start = time.time()
    pool = multiprocessing.Pool(processes=5)
    for goods_name in searchkey_data["关键词"]:
        pool.apply_async(get_data, [goods_name])
    pool.close()
    pool.join()

logging.info("累计耗时%s" %(time.time()-start))
