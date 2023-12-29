"""
去重复做了个简单的店铺
"""

from taobao_item_img import TaobaoItemImg # 导入淘宝详情页图片提取类
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from urllib.request import quote, unquote
from selenium.webdriver.common.by import By
import random
import requests
import os
import re
import lxml
import lxml.etree
import uuid
import hashlib
import redis
from setting import redisHost, redisPort, redisPassword


from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driverPath = ChromeDriverManager().install()

class MyRedis():
    def __init__(self,ip,password,port=6379,db=6):#构造函数
        try:
            self.r = redis.Redis(host=ip,password=password,port=port,db=db)  #连接redis固定方法,这里的值必须固定写死
        except Exception as e:
            print('redis连接失败,错误信息%s'%e)
    def str_get(self,k):
        res = self.r.get(k)   #会从服务器传对应的值过来，性能慢
        if res:
            return res.decode()   #从redis里面拿到的是bytes类型的数据，需要转换一下

    def str_set(self,k,v,time=None): #time默认失效时间
        self.r.set(k,v,time)

    def delete(self,k):
        tag = self.r.exists(k)
        #判断这个key是否存在,相对于get到这个key他只是传回一个存在火灾不存在的信息，
        # 而不用将整个k值传过来（如果k里面存的东西比较多，那么传输很耗时）
        if tag:
            self.r.delete(k)
        else:
            print('这个key不存在')

    def hash_get(self,name,k):  #哈希类型存储的是多层字典（嵌套字典）
        res = self.r.hget(name,k)
        if res:
            return res.decode()  #因为get不到值得话也不会报错所以需要判断一下

    def hash_set(self,name,k,v): #哈希类型的是多层
        self.r.hset(name,k,v)   #set也不会报错

    def hash_getall(self,name):
        res = self.r.hgetall(name)   #得到的是字典类型的，里面的k,v都是bytes类型的
        data={}
        if res:
            for k,v in res.items(): #循环取出字典里面的k,v，在进行decode
                k = k.decode()
                v = v.decode()
                data[k]=v
        return data

    def hash_del(self,name,k):
        res = self.r.hdel(name,k)
        if res:
            print('删除成功')
            return 1
        else:
            print('删除失败,该key不存在')
            return 0

    @property   #属性方法，
                # 使用的时候和变量一个用法就好比实例，A=MyRedis(), A.clean_redis使用，
                # 如果不加这个@property,使用时A=MyRedis(), A.clean_redis()   后面需要加这个函数的括号
    def clean_redis(self):
        self.r.flushdb()   #清空 redis
        print('清空redis成功!')
        return 0


class DP:
    def __init__(self, host=redisHost, port=redisPort, password=redisPassword):
        self.redisClient = MyRedis(host, password, port, db=6)

        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.option.add_experimental_option("detach", True)
        self.service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe')  # 配置谷歌操作驱动路径
        # option.add_argument('--headless')
        # option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
        # option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
        self.driver = webdriver.Chrome(options=self.option, service=self.service)
        script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        self.driver.execute_script(script)

        self.tbHeaders = {
            'authority': 's.taobao.com',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.taobao.com/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        self.cookiesList = []
        self.enableIpProxy = True

    # 添加反爬js
    def add_js_to_driver(self, driver):
        shieldJsText = requests.get("https://gitcode.net/mirrors/requireCool/stealth.min.js/-/raw/main/stealth.min.js?inline=false", proxies=self.set_proxy()).text
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': shieldJsText})  # 屏蔽selenim参数

    # 基于url的md5实现url去重
    def is_url_exist(self, url: str):
        urlMd5Str = hashlib.md5(url.encode()).hexdigest()
        if self.redisClient.str_get(urlMd5Str):
            return True
        self.redisClient.str_set(urlMd5Str, 1)
        return False

    def set_proxy(self):
        """
        set proxy for requests
        :param proxy_dict
        :return:
        """
        if self.enableIpProxy:
            res = requests.get(url="http://api.haiwaidaili.net/abroad?token=afdf84f97f18dd40bfb083bad1c05d12&num=1&format=1&protocol=http&country=tw&state=&city=&sep=1&csep=&area=").text.strip()
            print(res)
            return {
                "http": "http://{}".format(res),
                "https": "http://{}".format(res)
            }
        else:
            return None

    def dict_cookies_to_browser_taobao(self, cookies: dict) -> list:
        cookiesBrowserList = []
        for key in cookies:
            cookiesBrowserList.append({
                "domain": ".taobao.com",
                "name": key,
                "value": cookies[key]
            })

        return cookiesBrowserList

    # 获取每个商品页面js渲染后的HTML数据
    def get_item_links(self, cookies: dict, shopLink: str) -> list:
        self.driver.get('https://www.taobao.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser_taobao(cookies):
            self.driver.add_cookie(item)
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        self.driver.get(shopLink)
        # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        time.sleep(5)

        page_num = self.driver.find_element(By.XPATH, '//*[@id="J_ShopSearchResult"]/div/div[2]/div[1]/div[3]/span').text.replace("/", "")[1:]  # 该店铺总共有多少页的商品
        shop_name = self.driver.find_element(By.XPATH, '//*[@id="header-content"]/div[2]/div[1]/div[1]/a').text  # 该店铺的名称
        for page in range(2, int(page_num) + 2):
            print("当前获取的数据是来自第{}页".format(page - 1))
            # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
            for i in range(5):
                self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
                time.sleep(1)

            shop_body = self.driver.execute_script("return document.documentElement.outerHTML")
            time.sleep(random.randint(5, 8))

            result = re.findall(r'itemIds=([\d,]+)', shop_body)
            str_a = result[0].split(',')
            item_list = [int(x) for x in str_a] # 店铺每页商品的所有productid
            print(item_list)
            url_list = []
            for item in item_list:
                requestUrl = 'https://item.taobao.com/item.htm?id={}&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu'.format(item)
                url_list.append(requestUrl)

            yield url_list, shop_name

            self.driver.get(target_shopLink.split("pageNo")[0] + "pageNo={}".format(page))
            time.sleep(random.randint(2, 3))
            # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
            self.driver.refresh()
            self.driver.implicitly_wait(2)

        return [], shop_name

    def get_product_body(self,item_url:str)->str:
        start=time.time()
        self.driver.get(url=item_url)
        time.sleep(random.randint(1, 2))
        # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
        self.driver.refresh()
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_Title"]/h3')))
        self.driver.implicitly_wait(10)

        # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
        for i in range(15):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(0.5)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.randint(5, 8))

        item_body = self.driver.execute_script("return document.documentElement.outerHTML")
        time.sleep(random.randint(3, 5))
        print("单个商品图片下载共计耗时%s" % (time.time() - start))
        # time.sleep(random.randint(10, 20))
        return item_body

    # 解析轮播图
    def lb_pattern_links(self, item_body: str) -> list:
        lbImgList = []
        jsonText = item_body.replace("\n", "").replace(" ", "")
        match = re.search(r'auctionImages:\[(.*?)\]', jsonText)
        if match:
            item_link = match.group(1).split(',')
            group_list = [item.replace('"', "") for item in item_link]
            for item in group_list:
                if item.startswith("//"):
                    lbImgList.append("https:" + item)
                else:
                    lbImgList.append(item)

            return lbImgList
        else:
            return []

    # 解析sku
    def sku_pattern_links(self, item_body: str) -> list:
        imageLinks = re.findall(r'background:url\((.*?\.jpg)\)', item_body)
        skuImgList = []
        for itemUrl in imageLinks:
            if itemUrl.endswith("_30x30.jpg"):
                skuImgList.append("https:" + itemUrl.replace("_30x30.jpg",""))

        return skuImgList

    # 解析详情图
    def detail_pattern_links(self, item_body: str) -> list:
        detailImgList = []
        jsonText = item_body.replace("\n", "").replace(" ", "")
        ImgList = re.findall(r"data-src=['\"]([^'\"]+)['\"]", jsonText) + re.findall(r"imgsrc=['\"]([^'\"]+)['\"]", jsonText)
        dirty_imgs = [".png","_180x180.jpg","_120x120.jpg","_300x300.jpg",".gif",";"]
        for img in ImgList:
            if img.startswith("//"):
                img="https:"+img.replace("_50x50.jpg","")
            for dirty_str in dirty_imgs:
                if dirty_str not in img:
                    detailImgList.append(img)

        #ImgList = [img for img in ImgList if img.endswith('.jpg')]
        # for img in ImgList:
        #     if "https:" not in img:
        #         detailImgList.append("https:" + img.replace("_50x50.jpg",""))
        #     else:
        #         detailImgList.append(img.replace("_50x50.jpg",""))
        print(set(detailImgList))

        return detailImgList

    def make_dirPath(self, item_body: str, shop_name: str) -> str:
        # 解析商品标题
        title = lxml.etree.HTML(item_body).xpath("//title/text()")
        end_title = title[0]
        title_erList = ["|", "】", "【", "/", "\\", ":", "*", "?", '"', ">", "<"]  # Windows文件夹命名规则不包含的字符
        for i in title_erList:
            end_title = end_title.replace(i, "")
        save_path = "E:\\shop_imgs\\" + shop_name + "\\" + end_title

        return save_path

    # 将图片列表写入到文件夹
    def save_imgs(self, dirPath: str, imgList: list):
        # 如果文件夹不存在创建文件夹
        if os.path.exists(dirPath) == False:
            os.makedirs(dirPath)

        if len(imgList) > 0:
            for imgUrl in imgList:
                if str(imgUrl).startswith("http"):
                    filename = uuid.uuid4().hex
                    try:
                        with open("{}/{}.jpg".format(dirPath, filename), "wb") as f:
                            print(dirPath + "图片{}下载成功".format(imgUrl))
                            f.write(requests.get(imgUrl, headers=self.tbHeaders, proxies=self.set_proxy()).content)
                    except Exception as error:
                        print("图片下载出现错误%s" % error)

if __name__ == "__main__":
    cookiesList = []

    # 直接复制店铺链接，注意加上pageNo
    target_shopLink = 'https://shop356744483.taobao.com/search.htm?spm=a1z10.3-c.w4002-21168156062.9.6368628d5bFtDf&_ksTS=1693297542641_241&callback=jsonp242&input_charset=gbk&mid=w-21168156062-0&wid=21168156062&path=%2Fsearch.htm&search=y&pageNo=1'

    # 创建一个爬取天猫详情的
    taobaoItemImg = DP()
    result = taobaoItemImg.get_item_links(cookies=random.choice(cookiesList), shopLink=target_shopLink)

    for url_list, shop_name in result:

        if url_list == []:
            print("爬取完成")
            break
        else:
            for url in url_list:
                # 判断是否需要进行去重
                if taobaoItemImg.is_url_exist(url) == True:
                    print("该商品url已经爬取过,对url进行跳过")
                    continue

                item_body=taobaoItemImg.get_product_body(item_url=url)

                # 通过item_body通过参数解析图片内容
                lb_list = taobaoItemImg.lb_pattern_links(item_body)
                sku_list = taobaoItemImg.sku_pattern_links(item_body)
                detail_list = taobaoItemImg.detail_pattern_links(item_body)
                img_list = lb_list + sku_list + detail_list

                # 没有爬取到内容清除redis里信息
                # if img_list == []:
                #     time.sleep(3)  # 没有提取到图片，跳过
                #     taobaoItemImg.redisClient.delete(hashlib.md5(url.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                #     print(f"跳过商品详情页url是{url}")
                #     break
                # img_path = taobaoItemImg.make_dirPath(item_body, shop_name)
                #taobaoItemImg.save_imgs(img_path, img_list)