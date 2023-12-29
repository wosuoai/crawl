from selenium import webdriver
from urllib.parse import quote
import requests
import random
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging

'''
format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间
'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='../crawl_weibo.log', filemode='w')


# 构建信息列表
idList = []
usernameList = []
timeList = []
titleList = []
transpondList = []
commentList = []
praiseList = []

# 构建dataFrame
data = {
    "用户id": idList,
    '用户名': usernameList,
    '发布时间': timeList,
    '正文': titleList,
    '转发量': transpondList,
    '评论量': commentList,
    '点赞量': praiseList
}

topic=input("需要搜索的话题：")
print("搜索时间段的格式：2023-06-16-23")
start_time=input("开始时间：")
end_time=input("结束时间：")
page_num=int(input("需要爬取的页数："))


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
#option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 通过端口号接管已打开的浏览器
option.add_argument('--disable-infobars')  # 不显示chrome正受到自动测试软件的控制
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')    #去掉webdriver痕迹
driver=webdriver.Chrome(executable_path=r"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()

start=time.time()
driver.get('https://weibo.com/login.php')
time.sleep(random.randint(2,3))
cookies=[{'domain': '微博.com', 'expiry': 1687080427, 'httpOnly': True, 'name': 'WBPSESS', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'FH255CAr_cfIbZ29-Y520Qb7G8HcFtCUf6RrIKf_gdtWqE1sdtABmxP3vqzxZPrtJdc3dSP2b4tX_BW49o9k4s_F56vbv5GuDgoeVs_DhZCVbHKlWBSXmT93duvJBI-oagyPRELC5paCsWFCYb78HA=='}, {'domain': '.微博.com', 'httpOnly': False, 'name': 'SSOLoginState', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1686994027'}, {'domain': '.微博.com', 'expiry': 1718530027, 'httpOnly': False, 'name': 'SUBP', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWM6.Fq-hhEyGMpwasJ-pSf5JpX5KzhUgL.FoMNSh2RSo241h.2dJLoIEBLxKnLB.qL12-LxK.LBKeL12-LxKBLB.zL12zLxK-LBo5L1Knt'}, {'domain': '.微博.com', 'expiry': 1718530027, 'httpOnly': False, 'name': 'ALF', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1718530027'}, {'domain': '.微博.com', 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '_2A25JiQw7DeRhGeFJ71MZ9i_FwzWIHXVq_3rzrDV8PUNbmtANLVXWkW9Nf-zUNWQbgpypUYqrvMGYflzMalfxhZNQ'}, {'domain': '.微博.com', 'httpOnly': False, 'name': 'Apache', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5453398494087.913.1686994017189'}, {'domain': '.微博.com', 'httpOnly': False, 'name': '_s_tentry', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'passport.微博.com'}, {'domain': '微博.com', 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'GeE52wbzYXjPyF30XRAdm1fV'}, {'domain': '.微博.com', 'expiry': 1721554017, 'httpOnly': False, 'name': 'SINAGLOBAL', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5453398494087.913.1686994017189'}, {'domain': '.微博.com', 'httpOnly': False, 'name': 'login_sid_t', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '161128118c56a9fc1a06183ff8059d3d'}, {'domain': '.微博.com', 'expiry': 1686995827, 'httpOnly': False, 'name': 'PC_TOKEN', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'fde6d2030c'}, {'domain': '微博.com', 'expiry': 1686994616, 'httpOnly': False, 'name': 'WBStorage', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '4d96c54e|undefined'}, {'domain': '.微博.com', 'expiry': 1718098017, 'httpOnly': False, 'name': 'ULV', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1686994017192:1:1:1:5453398494087.913.1686994017189:'}, {'domain': '.微博.com', 'httpOnly': False, 'name': 'cross_origin_proto', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'SSL'}, {'domain': '微博.com', 'expiry': 1687017417, 'httpOnly': False, 'name': 'wb_view_log', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1536*8641.25'}]
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']  # 删除报错的expiry字段
    driver.add_cookie(cookie)
driver.refresh()
time.sleep(random.randint(2,3))
driver.implicitly_wait(2)

for pagenum in range(1,page_num+1):
    driver.get('https://s.weibo.com/weibo?q=%23{}%23&typeall=1&suball=1&timescope=custom%3A{}%3A{}&Refer=g&page={}'.format(quote(topic),start_time,end_time,pagenum))
    time.sleep(random.randint(2,3))

    cookies = {
        'SINAGLOBAL': '1334474547233.9126.1686990056382',
        'UOR': ',,login.sina.com.cn',
        'PC_TOKEN': '0bb76e42e2',
        '_s_tentry': '微博.com',
        'appkey': '',
        'Apache': '1851321542079.456.1687013215092',
        'ULV': '1687013215094:3:3:3:1851321542079.456.1687013215092:1687012039383',
        'SUB': '_2A25JibfTDeRhGeFJ71MZ9i_FwzWIHXVq_q4brDV8PUNbmtANLU7akW9Nf-zUNTvuwPyBSOGx7S3KNh3pIgMCzmXw',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWM6.Fq-hhEyGMpwasJ-pSf5JpX5KzhUgL.FoMNSh2RSo241h.2dJLoIEBLxKnLB.qL12-LxK.LBKeL12-LxKBLB.zL12zLxK-LBo5L1Knt',
        'ALF': '1718549250',
        'SSOLoginState': '1687013251',
    }

    headers = {
        'authority': 's.微博.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'SINAGLOBAL=1334474547233.9126.1686990056382; UOR=,,login.sina.com.cn; PC_TOKEN=0bb76e42e2; _s_tentry=微博.com; appkey=; Apache=1851321542079.456.1687013215092; ULV=1687013215094:3:3:3:1851321542079.456.1687013215092:1687012039383; SUB=_2A25JibfTDeRhGeFJ71MZ9i_FwzWIHXVq_q4brDV8PUNbmtANLU7akW9Nf-zUNTvuwPyBSOGx7S3KNh3pIgMCzmXw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWM6.Fq-hhEyGMpwasJ-pSf5JpX5KzhUgL.FoMNSh2RSo241h.2dJLoIEBLxKnLB.qL12-LxK.LBKeL12-LxKBLB.zL12zLxK-LBo5L1Knt; ALF=1718549250; SSOLoginState=1687013251',
        'referer': 'https://s.weibo.com/weibo?q=%23%E5%9B%BD%E6%B3%B0%E8%88%AA%E7%A9%BA%E8%87%B4%E6%AD%89%23&typeall=1&suball=1&timescope=custom%3A2023-05-24-0%3A2023-06-16-23&Refer=g',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'q': '#国泰航空致歉#',
        'typeall': '1',
        'suball': '1',
        'timescope': 'custom:2023-05-24-0:2023-06-16-23',
        'Refer': 'g',
        'page': '2',
    }

    params['q']='#{}#'.format(topic)
    params['timescope']='custom:{}:{}'.format(start_time,end_time)
    params['page']=pagenum

    response = requests.get('https://s.weibo.com/weibo', params=params, cookies=cookies, headers=headers)
    response.encoding = 'utf-8' #处理乱码
    page = BeautifulSoup(response.text,"html.parser")

    #ID、datatime
    id_time = page.find_all("div",class_="from")
    for text in id_time:
        idList.append(re.search(r'\d+', str(text))[0])
        timeList.append(re.findall(r'\d+月\d+日\s\d+:\d+', str(text))[0])
        print(re.search(r'\d+', str(text))[0],re.findall(r'\d+月\d+日\s\d+:\d+', str(text))[0])
        logging.info("用户id：%s，发布时间：%s"%(re.search(r'\d+', str(text))[0],re.findall(r'\d+月\d+日\s\d+:\d+', str(text))[0]))

    #作者、正文
    name_title = page.find_all("p",class_="txt")
    for elements in name_title:
        usernameList.append(elements.get("nick-name"))
        titleList.append(elements.text)
        print(elements.get("nick-name"),elements.text)
        logging.info("用户名：%s，正文内容：%s"%(elements.get("nick-name"),elements.text))

    #转发、评论、赞
    all_num = page.find_all("div",class_="card-act")
    for num_elements in all_num:
        num_list=num_elements.text.strip().split('\n')
        num = [i for i in num_list if i != '']
        logging.info("原数据量：%s"%num)

        if num[0]=="转发":
            num[0]='0'

        if num[1]==" 评论":
            num[1]='0'

        if num[2]=="赞":
            num[2]='0'

        transpondList.append(num[0])
        commentList.append(num[1])
        praiseList.append(num[2])

        print(num[0],num[1],num[2])
        logging.info("文章转发量：%s，评论量：%s，点赞量：%s"%(num[0],num[1],num[2]))

# df = pd.DataFrame(data)
# df.to_excel('./{}.xlsx'.format("国泰航空致歉"))
# logging.info("累计耗时%s" %(time.time()-start))