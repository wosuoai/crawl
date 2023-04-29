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
import os


'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='yiwugou.log', filemode='w')

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

start = time.time()

cookies_file = os.listdir(r'E:\义乌购商铺信息\cookies')
for filename in cookies_file:
    # 构建信息列表
    shopidList = ["{}".format(filename[:-4])] #店铺id
    limit_shelfnumList = [] #限时秒杀已上架数量
    limit_offnumList = [] #限时秒杀已下架数量
    limit_titelList = [] #限时秒杀已上架商品标题
    start_timeList = [] #限时秒杀已上架商品开团时间
    end_timeList = [] #限时秒杀已上架商品结束时间
    regist_timeList = [] #限时秒杀已上架商品报名时间
    deal_titleList = [] #限时秒杀未上架但是能上架的商品标题
    #sellList = [] #限时秒杀未上架但是能上架的商品销量
    clear_shelfnumList = [] #尾货清仓已上架数量
    clear_offnumList = [] #尾货清仓已下架数量
    clear_titelList = [] #尾货清仓已上架商品标题
    update_timeList = [] #尾货清仓已上架商品更新时间
    priceList = []  #尾货清仓已上架商品价格
    scoreList = []  #尾货清仓已上架商品得分

    print("当前执行的账户是%s"%filename[:-4])
    logging.info("当前执行的账户是%s"%filename[:-4])
    driver.get("https://www.yiwugo.com/")
    driver.delete_all_cookies()

    # 读取cookies
    with open(r"E:\义乌购商铺信息\cookies\{}".format(filename), "r", encoding="utf-8") as f:
        ck = f.read()

    """
    获取到的cookies都是登录后重定向到work.yiwugo.com的
    直接使用，在登录时会重定向到user.yiwugou.com上，导致domain错误
    因此将work.yiwugo.com替换成.yiwugo.com
    """
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


    driver.get("https://work.yiwugo.com/")
    time.sleep(1)
    #提取当前网页cookie，即热cookie
    new_cookies=driver.get_cookies()
    with open(r"E:\义乌购商铺信息\hot_cookies\{}".format(filename), "w", encoding="utf-8") as f:
        f.write(str(new_cookies))
    time.sleep(1)

    try:
        #判断是否有弹窗
        if xpathExists("/html/body/div[6]/div[3]/button"):
            driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/button").click()
    except Exception as error:
        logging.error("错误是%s" % error)
    finally:
        driver.find_element(By.ID, "juCheap").click()
        applyNum = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/a[2]").text
        print("限时秒杀：已上架%s个商品，可上架%s个商品"%(applyNum[5],applyNum[-2]))
        logging.info("限时秒杀：已上架%s个商品，可上架%s个商品"%(applyNum[5],applyNum[-2]))
        limit_shelfnumList.append(applyNum[5])
        limit_offnumList.append(applyNum[-2])

        limit_titel1 = ""
        start_time1 = ""
        end_time1 = ""
        regist_time1 = ""
        if int(applyNum[5])>0:
            # 一直到变化的div
            items = driver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr")
            print("检测到%s个商品信息" % (len(items) - 1))

            for item in range(1, len(items)):
                # 标题
                limit_titel = items[item].find_element(By.XPATH, './td[2]/a').text
                # 开团时间
                start_time = items[item].find_element(By.XPATH, './td[3]').text
                # 结束时间
                end_time = items[item].find_element(By.XPATH, './td[4]').text
                # 报名时间
                regist_time = items[item].find_element(By.XPATH, './td[5]').text
                # 状态
                state = items[item].find_element(By.XPATH, './td[6]').text
                if state=="已通过":
                    print(limit_titel,start_time,end_time,regist_time)
                    limit_titel1 += limit_titel + "\n"
                    start_time1 += start_time + "\n"
                    end_time1 += end_time + "\n"
                    regist_time1 += regist_time + "\n"
                else:
                    continue
            limit_titelList.append(limit_titel1)
            start_timeList.append(start_time1)
            end_timeList.append(end_time1)
            regist_timeList.append(regist_time1)
        else:
            limit_titelList.append(limit_titel1)
            start_timeList.append(start_time1)
            end_timeList.append(end_time1)
            regist_timeList.append(regist_time1)

        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/a[2]").click()
        time.sleep(1)

    #构建requests所需要的cookie格式
    dict = {}
    for cookie in new_cookies:
        if ("name" in cookie) and ("value" in cookie):
            dict[cookie["name"]] = cookie["value"]

    #字典去重
    keys = list(set(dict.values()))
    cookie_dict = {k: dict[k] for k in dict if dict[k] in keys}

    """
    使用https://curlconverter.com/
    分析https://work.yiwugo.com/marketing/product_select/1.htm
    拿到headers
    最后requests.get返回html
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://work.yiwugo.com/marketing/product_select.htm',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 限时秒杀页面html
    response = requests.get('https://work.yiwugo.com/marketing/product_select/1.htm', cookies=cookie_dict, headers=headers).text
    #print(response)
    soup= BeautifulSoup(response,"lxml")
    #处理商品标题
    deal_title = ""
    elements=soup.find_all("a", class_='c36c')
    print("检测到%s个商品信息"%len(elements))
    if len(elements)>0:
        for element in elements:
            element.getText()
            print(element.getText())
            deal_title += element.getText() + "\n"
        deal_titleList.append(deal_title)
    else:
        deal_titleList.append(deal_title)

    #处理商品90天销售金额
    sales = soup.find_all("p")
    for sale in sales:
        try:
            if "90天销量" in sale.getText():
                salenum=sale.getText()[6:-1]
                #print(salenum)
            else:
                pass
        except:
            continue

    time.sleep(1)
    #切换到尾货清仓
    driver.get("https://work.yiwugo.com/product_s/productlist/1.htm?type=leftover&t=1")
    shelfNum = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/a[1]/span").text
    unshelfNum = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/a[2]/span").text
    print("尾货清仓：已上架%s个商品，已下架%s个商品"%(shelfNum[1:-2],unshelfNum[1:-2]))
    logging.info("尾货清仓：已上架%s个商品，已下架%s个商品"%(shelfNum[1:-2],unshelfNum[1:-2]))
    clear_shelfnumList.append(shelfNum[1:-2])
    clear_offnumList.append(unshelfNum[1:-2])

    clear_titel1 = ""
    update_time1 = ""
    price1 = ""
    score1 = ""
    if int(shelfNum[1:-2])>0:
        # 一直到变化的div
        items = driver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr")
        print("检测到%s个商品信息"%(len(items)-1))

        for item in range(1,len(items)):
            #标题
            clear_titel = items[item].find_element(By.XPATH, './td[3]/a').text
            #更新时间
            update_time = items[item].find_element(By.XPATH, './td[4]/span').text
            #价格
            price = items[item].find_element(By.XPATH, './td[5]').text
            #产品分值
            score = items[item].find_element(By.XPATH, './td[6]').text
            print(clear_titel,update_time,price,score)

            clear_titel1 += clear_titel + "\n"
            update_time1 += update_time + "\n"
            price1 += price + "\n"
            score1 += score + "\n"

        clear_titelList.append(clear_titel1)
        update_timeList.append(update_time1)
        priceList.append(price1)
        scoreList.append(score1)
    else:
        clear_titelList.append(clear_titel1)
        update_timeList.append(update_time1)
        priceList.append(price1)
        scoreList.append(score1)

    print("当前帐号%s数据处理完成"%filename[:-4])
    logging.info("当前帐号%s数据处理完成"%filename[:-4])

    # 构造ExcelWriter
    excel_writer = pd.ExcelWriter('./1688有效数据/{}.xlsx'.format(filename[:-4]))
    df1 = pd.DataFrame({"店铺id": shopidList,"已上架数量": limit_shelfnumList ,"已下架数量": limit_offnumList ,"已上架商品标题": limit_titelList ,"商品开团时间": start_timeList ,"商品结束时间": end_timeList ,"商品报名时间": regist_timeList,"能上架的商品标题": deal_titleList})
    df2 = pd.DataFrame({"店铺id": shopidList,"已上架数量": clear_shelfnumList ,"已下架数量": clear_offnumList ,"商品标题": clear_titelList ,"商品更新时间": update_timeList ,"商品价格": priceList ,"商品得分": scoreList})
    df1.to_excel(excel_writer,sheet_name = '限时秒杀')
    df2.to_excel(excel_writer, sheet_name='尾货清仓')
    #excel_writer.save()
    excel_writer.close()

driver.close()
logging.info("累计耗时%s" %(time.time()-start))
