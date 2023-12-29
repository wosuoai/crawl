# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
import re
import time
import random
import lxml
import lxml.etree
import json
import os
import uuid
import hashlib
from urllib.request import quote, unquote
from setting import redisHost, redisPort, redisPassword
import redis
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driverPath = ChromeDriverManager().install()

proxies = {
    'http': 'socks5://127.0.0.1:10808',
    'https': 'socks5://127.0.0.1:10808',
}
shieldJsText = requests.get("https://gitcode.net/mirrors/requireCool/stealth.min.js/-/raw/main/stealth.min.js?inline=false").text

script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''

class MyRedis():
    def __init__(self, ip, password, port=6379, db=6):  # 构造函数
        try:
            self.r = redis.Redis(host=ip, password=password, port=port, db=db)  # 连接redis固定方法,这里的值必须固定写死
        except Exception as e:
            print('redis连接失败,错误信息%s' % e)

    def str_get(self, k):
        res = self.r.get(k)  # 会从服务器传对应的值过来，性能慢
        if res:
            return res.decode()  # 从redis里面拿到的是bytes类型的数据，需要转换一下

    def str_set(self, k, v, time=None):  # time默认失效时间
        self.r.set(k, v, time)

    def delete(self, k):
        tag = self.r.exists(k)
        # 判断这个key是否存在,相对于get到这个key他只是传回一个存在火灾不存在的信息，
        # 而不用将整个k值传过来（如果k里面存的东西比较多，那么传输很耗时）
        if tag:
            self.r.delete(k)
        else:
            print('这个key不存在')

    def hash_get(self, name, k):  # 哈希类型存储的是多层字典（嵌套字典）
        res = self.r.hget(name, k)
        if res:
            return res.decode()  # 因为get不到值得话也不会报错所以需要判断一下

    def hash_set(self, name, k, v):  # 哈希类型的是多层
        self.r.hset(name, k, v)  # set也不会报错

    def hash_getall(self, name):
        res = self.r.hgetall(name)  # 得到的是字典类型的，里面的k,v都是bytes类型的
        data = {}
        if res:
            for k, v in res.items():  # 循环取出字典里面的k,v，在进行decode
                k = k.decode()
                v = v.decode()
                data[k] = v
        return data

    def hash_del(self, name, k):
        res = self.r.hdel(name, k)
        if res:
            print('删除成功')
            return 1
        else:
            print('删除失败,该key不存在')
            return 0

    @property  # 属性方法，
    # 使用的时候和变量一个用法就好比实例，A=MyRedis(), A.clean_redis使用，
    # 如果不加这个@property,使用时A=MyRedis(), A.clean_redis()   后面需要加这个函数的括号
    def clean_redis(self):
        self.r.flushdb()  # 清空 redis
        print('清空redis成功!')
        return 0


class SearchItemImg:
    def __init__(self, host=redisHost, port=redisPort, password=redisPassword):
        self.redisClient = MyRedis(host, password, port, db=4)
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.option.add_experimental_option("detach", True)
        self.option.add_argument("--incognito") #开启隐身模式
        # option.add_argument('--headless')
        # option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
        # option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
        self.service = ChromeService(executable_path=driverPath)  # 配置谷歌操作驱动路径
        #self.service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe')  # 配置谷歌操作驱动路径
        self.driver = webdriver.Chrome(options=self.option, service=self.service)
        # script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        # self.driver.execute_script(script)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

        self.Headers = {
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
        self.enableIpProxy = False

    # 添加反爬js
    def add_js_to_driver(self, driver):
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': shieldJsText})  # 屏蔽selenium参数

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
            res = requests.get(
                url="http://api.haiwaidaili.net/abroad?num=1&format=1&protocol=http&country=&state=&city=&sep=1&csep=&type=datacenter").text.strip()
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

    def dict_cookies_to_browser_tmall(self, cookies1: dict) -> list:
        cookiesBrowserList = []
        for key in cookies1:
            cookiesBrowserList.append({
                "domain": ".tmall.com",
                "name": key,
                "value": cookies1[key]
            })

        return cookiesBrowserList

    def get_cookiesList_from_cookiesPool(sleepTime: int = 2, cookiesPoolUrl="") -> dict:
        cookies = {}
        while cookies == {}:
            time.sleep(sleepTime)
            cookies = requests.get(url="http://www.baidu.com").json()
        return [cookies]

    def scrape_page(self, condition, locator) -> bool:
        print("scraping %s" % self.url)
        try:
            self.driver.get(self.url)
            self.wait.until(condition(locator))
            return True
        except TimeoutException:
            print("error occurred while scraping %s", self.url, exc_info=True)
            return False

    # 定义一个xpath的捕获异常
    def xpathExists(self,xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    # 定义一个css_select的捕获异常
    def cssSelectExists(self, css):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css)
            return True
        except:
            return False

    # def huadong(self):
    #     spider = self.driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
    #     self.move_to_gap(spider, self.get_track(300))
    def huadong(self, xpath: str):
        spider = self.driver.find_element(By.XPATH, xpath)
        self.move_to_gap(spider, self.get_track(300))

    # 定义一共滑块随机移动步长函数
    # https://cloud.tencent.com/developer/article/1095744 鼠标点击事件方法
    # https://blog.csdn.net/qq_39377418/article/details/106954643
    # https://www.jb51.net/article/261758.htm
    def get_track(self, distance):
        """ 模拟轨迹 假装是人在操作 """

        """ 1.设定长度比例 """
        pos = [0, 1, 2, 3, 3, 2, 1, 4, 2, 1]  # 滑动轨迹之间比例设定
        pos = [0, 5]  # 滑动轨迹之间比例设定

        """ 2. 正弦函数 """
        # pos = [random.randrange(0, 10) for i in range(10)]
        # pos.sort()
        # pos = [item / 10 * math.pi for item in pos]
        # pos = [math.sin(x) for x in pos]

        pos_sum = sum(pos)
        route = [int(int(distance) * (item / pos_sum)) for item in pos]  # 计算出移动路径

        route = route + [int(distance) - sum(route), ]
        # print('distance', distance)
        # print('sum route', sum(route))
        # print('route', route)
        return route

    # 极验滑块滑动
    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
        # to_element: The WebElement to move to.

        # Move the mouse by an offset of the specified element. Offsets are relative to the in-view center point of the element.
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in tracks:
            #ActionChains(self.driver).move_to_element_with_offset()
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(self.driver).release().perform()

    # 判断外层是否有滑块
    def outside_slide(self):
        if self.xpathExists('//*[@id="nc_1_n1z"]'):
            self.huadong('//*[@id="nc_1_n1z"]')
            time.sleep(3)

            self.slide_trys()

    # 判断内层天猫item是否有滑块
    def insideTM_slide(self):
        if self.cssSelectExists("iframe[src*='h5api.m.tmall.com']"):
            iframe_element = self.driver.find_element(By.CSS_SELECTOR, "iframe[src*='h5api.m.tmall.com']")
            self.driver.switch_to.frame(iframe_element)
            time.sleep(2)
            self.huadong('//*[@id="nc_1_n1z"]')
            time.sleep(3)

            self.slide_trys()

    # 判断内层淘宝item是否有滑块
    def insideTB_slide(self):
        if self.cssSelectExists("#baxia-dialog-content"):
            self.driver.switch_to.frame("baxia-dialog-content")
            time.sleep(2)
            self.huadong('//*[@id="nc_1_n1z"]')
            time.sleep(3)

            self.slide_trys()

    # 滑块第一次没有通过 多次尝试
    def slide_trys(self):
        out_try = 0
        while out_try < 5:
            out_try += 1

            refresh = self.driver.find_elements(By.XPATH, '//*[@id="`nc_1_refresh1`"]')
            if len(refresh) > 0:
                refresh[0].click()
                time.sleep(2)
                self.huadong('//*[@id="nc_1_n1z"]')
                continue
            time.sleep(random.randint(2, 3))
            # if self.driver.page_source.find("nc_1_n1z") == -1:
            #     self.driver.switch_to.parent_frame()
            #     break
            if self.xpathExists('//*[@id="nc_1_n1z"]')==False:
                break

    # 页面滚动到底部
    def scroll(self, driver):
        for i in range(5):
            driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(1)

    def choice_elements(self):
        """
        该页面上的选项点击后不会对地址栏中的链接造成改变
        因此这里如果要做筛选 需要模拟点击后在进行链接跳转 之前的操作会默认记录
        """
        product_links = "https://s.taobao.com/search?bcoffset=0&commend=all&ie=utf8&initiative_id=staobaoz_20230828&p4ppushleft=%2C44&page={}&q={}&s=0&search_type=item&sort=sale-desc&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ssid=s5-e".format(1,quote(key_word+"女",encoding="utf-8"))
        self.driver.get(product_links)
        time.sleep(3)
        # 选择性别
        self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').click()
        time.sleep(5)

        # 判断商品搜索页数，如果不是100页，则切换到销量排序
        total_page = self.driver.find_element(By.XPATH,'//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/span').text.replace("/", "")[1:]
        if int(total_page) != 100:
            self.driver.find_element(By.XPATH,'//*[@id="sortBarWrap"]/div[1]/div[1]/div/div[1]/div/div/div/ul/li[2]').click()
            time.sleep(5)

        # 选择货源地址，时间尽量长一点，太短会触发风控
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[1]')).perform()
        time.sleep(2)
        # 上海
        self.driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(2) > button").click()
        time.sleep(10)
        # 广州
        self.driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(3) > button").click()
        time.sleep(10)
        # 深圳
        self.driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(4) > button").click()
        time.sleep(10)
        # 杭州
        self.driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(1) > div:nth-child(5) > button").click()
        time.sleep(10)
        # 嘉兴
        self.driver.find_element(By.CSS_SELECTOR,"body > div.next-overlay-wrapper.v2.opened > div > div:nth-child(2) > div:nth-child(13) > button").click()
        time.sleep(10)

    def login_taobao(self,driver):
        driver.get("https://login.taobao.com/member/login.jhtml")
        # driver.get(url="https://login.tmall.com/?spm=a211oj.20831186.a2226mz.2.73c878e6VBInAM&redirectURL=https%3A%2F%2Fpages.tmall.com")

        time.sleep(5)
        name_input_element = driver.find_element(By.XPATH, '//*[@id="fm-login-id"]')
        time.sleep(1)
        name_input_element.clear()
        name_input_element.send_keys("19357188234")

        time.sleep(2)
        password_input_element = driver.find_element(By.XPATH, '//*[@id="fm-login-password"]')
        time.sleep(1)
        password_input_element.clear()
        password_input_element.send_keys("dejavu999")

        time.sleep(10)

        # 点击登陆按钮
        button = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button')
        button.click()
        time.sleep(3)

        driver.get("https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
        WebDriverWait(driver, 60, 2).until(EC.presence_of_element_located((By.ID, 'J_Title')))
        driver.implicitly_wait(10)

    # 刷入淘宝和天猫cookies到driver
    def init_cookies_to_driver(self, tmCookies: dict, tbCookies: dict):
        self.driver.get('https://www.tmall.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser_tmall(tmCookies):
            self.driver.add_cookie(item)
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        self.driver.get('https://www.taobao.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser_taobao(tbCookies):
            self.driver.add_cookie(item)
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        #self.login_taobao(driver=self.driver)

    # 通过requests返回每页搜索的信息
    def page_items(self, key_word: str, tbCookies: dict, startPage: int = 16, endPage: int = 100) -> list:
        driver = webdriver.Chrome(options=self.option, service=self.service)
        self.add_js_to_driver(driver=driver)  # 添加反屏蔽js

        driver.get('https://www.taobao.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser_taobao(tbCookies):
            driver.add_cookie(item)
        driver.refresh()
        driver.implicitly_wait(2)

        #self.login_taobao(driver=driver)

        driver.get('https://s.taobao.com')
        time.sleep(3)
        search_element = driver.find_element(By.CSS_SELECTOR, '#q')
        search_element.send_keys(key_word)  # 搜索
        search_element.send_keys(Keys.ENTER)  # 进行回车跳页

        #self.choice_elements()
        time.sleep(45)

        self.scroll(driver=driver)
        time.sleep(3)

        for i in range(startPage, endPage):
            print("当前页是来自第{}页的数据".format(i))
            item_html = driver.execute_script("return document.documentElement.outerHTML").encode('utf-8').decode('raw_unicode_escape')
            comment_urls = re.findall(r'//item\.taobao\.com/item\.htm\?id=\d+', item_html) + re.findall(r'//(detail\.tmall\.com/item\.htm\?id=[\d]+)', item_html)
            item_links = []
            for url in comment_urls:
                if "item.taobao.com" in url:
                    item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1#detail"
                    item_links.append(item_link)
                else:
                    item_link = "https:" + url + "&amp;ns=1&amp;abbucket=1"
                    item_links.append(item_link)
            # comment_urls = re.findall(r'detail_url":"(.*?)",', item_html)
            # item_links = []
            # for url in comment_urls:
            #     if "https:" not in url:
            #         item_link = "https:" + url
            #         item_links.append(item_link)
            item_links = item_links[3:] #去除每页商品列表的广告
            time.sleep(random.randint(5, 8))
            yield list(set(item_links))

            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            # 点击下一页的操作放在JavaScript里面的，需要js执行
            js_scr = 'document.querySelector("#sortBarWrap > div.SortBar--sortBarWrapTop--VgqKGi6 > div.SortBar--otherSelector--AGGxGw3 > div:nth-child(2) > div.next-pagination.next-small.next-simple.next-no-border > div > button.next-btn.next-small.next-btn-normal.next-pagination-item.next-next").click();'
            driver.execute_script(js_scr)
            time.sleep(random.randint(5, 8))
            self.scroll(driver=driver)  # 刷新页面后将页面滚动到最后
            time.sleep(random.randint(5, 8))

        return []

    # 获取每个商品页面js渲染后的HTML数据
    def get_item_html(self, items_list: list) -> str:
        self.add_js_to_driver(driver=self.driver)  # 添加反屏蔽js
        for item_link in items_list:
            requestUrl = item_link
            self.driver.get(requestUrl)
            time.sleep(3)

            self.outside_slide()
            self.insideTM_slide()
            #self.insideTB_slide()

            # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
            self.scroll(driver=self.driver)

            item_html = self.driver.execute_script("return document.documentElement.outerHTML")
            time.sleep(random.randint(2, 3))

            yield item_html, requestUrl

        return "当前商品信息成功返回"

    # 天猫和淘宝的图片保存路径
    def make_dirPath(self, htmlText: str, key_word: str) -> str:
        # 解析商品标题
        title = "未知"
        titleList = lxml.etree.HTML(htmlText).xpath("//title/text()")
        if len(titleList) > 0:
            title = str(titleList[0]).replace(" ", "")
        title_erList = ["|", "】", "【", "/", "\\", ":", "*", "?", '"', ">", "<"]  # Windows文件夹命名规则不包含的字符
        for i in title_erList:
            title = title.replace(i, "")
        # 解析店铺名称
        pattern = r"sellerNick\s*:\s*'([^']*)'"
        shopname = re.findall(pattern, item_html)
        save_path = "E:\\keyword\\" + key_word + "\\" + title + "{}".format(random.randint(111, 999))

        return save_path

    # 解析淘宝商品的轮播图
    def tb_get_lb_links(self, htmlText: str) -> list:
        lbImgList = []
        pattern = r'img src="(.*?)_120x120.jpg"'
        imgList = re.findall(pattern, htmlText)
        for img in imgList:
            link = "https:" + img.replace("_120x120.jpg", "")
            lbImgList.append(link)

        return lbImgList

    # 解析淘宝商品的sku
    def tb_get_sku_links(self, htmlText: str) -> list:
        skuImgList = []
        background_urls = re.findall(r'background:url\((.*?\.jpg)\)', htmlText)
        for url in background_urls:
            if "_30x30.jpg" in url:
                skuImgList.append("https:" + url.replace("_30x30.jpg", ""))
            elif "_80x80.jpg" in url:
                skuImgList.append("https:" + url.replace("_80x80.jpg", ""))
            elif "_300x300.jpg" in url:
                skuImgList.append("https:" + url.replace("_300x300.jpg", ""))

        return skuImgList

    # 解析淘宝商品的详情图
    def tb_get_detail_links(self, htmlText: str) -> list:
        detailImgList = []
        item_html.replace(" ", "").replace("\n", "")
        ImgList = re.findall(r"img src=['\"]([^'\"]+)['\"]", htmlText)
        ImgList1 = re.findall(r"img data-src=['\"]([^'\"]+)['\"]", htmlText)
        for img in ImgList:
            if "；" not in img:
                detailImgList.append(img)

        for img1 in ImgList1:
            if img1.startswith("//"):
                detailImgList.append("https:"+img1.replace("_50x50.jpg", ""))

        return detailImgList

    # 解析天猫商品的轮播图
    def tm_get_lb_links(self, htmlText: str) -> list:
        lbImgList = []
        pattern = r"//gw.alicdn.com/imgextra.*?\.webp"
        matches = re.findall(pattern, htmlText)

        for match in matches:
            if ";" in match:
                del match
            elif "110x10000Q75.jpg" in match:
                lb_link = "https:" + match.replace("_110x10000Q75.jpg_.webp", "")
                lbImgList.append(lb_link)

        return lbImgList

    # 解析天猫商品的sku
    def tm_get_sku_links(self, htmlText: str) -> list:
        skuImgList = []
        pattern = r"//gw.alicdn.com/bao/uploaded.*?\.webp"
        matches = re.findall(pattern, htmlText)

        for match in matches:
            if "src" in match:
                del match
            else:
                if "60x60q50.jpg" in match:
                    sku_link = "https:" + match.replace("_60x60q50.jpg_.webp", "")
                    skuImgList.append(sku_link)

        return skuImgList

    # 解析天猫商品的详情图
    def tm_get_detail_links(self, htmlText: str) -> list:
        detailImgList = []
        htmlText.replace(" ", "").replace("\n", "")
        ImgList = re.findall(r"src=['\"]([^'\"]+)['\"]", htmlText) + re.findall(r"data-src=['\"]([^'\"]+)['\"]",htmlText)
        ImgList = [img for img in ImgList if img.endswith('.jpg')]
        for img in ImgList:
            if "https:" not in img:
                detailImgList.append("https:" + img)
            else:
                detailImgList.append(img)

        return detailImgList

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
                            f.write(requests.get(imgUrl, headers=self.Headers, proxies=self.set_proxy()).content)
                            #f.write(requests.get(imgUrl, headers=self.Headers, proxies=proxies).content)
                    except Exception as error:
                        print("图片下载出现错误%s" % error)


if __name__ == "__main__":
    # 淘宝
    cookiesList = []
    # 天猫
    cookiesList1 = []

    # 输入商品关键词
    search_key = "新中式轻国风上衣"

    # 创建一个通过关键词爬取的图片
    searchItemImg = SearchItemImg()
    searchItemImg.init_cookies_to_driver(tmCookies=random.choice(cookiesList1),tbCookies=random.choice(cookiesList))  # 输入到cookies到driver

    # 定义一个生成器对象
    items_links_gen = searchItemImg.page_items(key_word=search_key,tbCookies=random.choice(cookiesList))  # 翻页刷入淘宝的cookies,另启动一个driver

    # 从生成器对象中遍历列表
    for items_links in items_links_gen:
        if items_links == []:
            print("爬取完成")
            break
        else:
            # 对原列表进行备份，遍历时遍历备份的列表
            new_links = items_links[:]
            # 判断是否需要进行去重
            for link in new_links:
                if searchItemImg.is_url_exist(link) == True:
                    items_links.remove(link)
                    print("该商品url已经爬取过,对url进行跳过")

            # 获取item页面的内容
            result = searchItemImg.get_item_html(items_list=items_links)

            for item_html, requestUrl in result:
                if "item.taobao.com" in requestUrl:
                    # 通过item_html通过参数解析图片内容
                    save_path = searchItemImg.make_dirPath(item_html, search_key)
                    tb_lb_list = searchItemImg.tb_get_lb_links(item_html)
                    tb_sku_list = searchItemImg.tb_get_sku_links(item_html)
                    tb_detail_list = searchItemImg.tb_get_detail_links(item_html)
                    tb_img_list = tb_lb_list + tb_sku_list + tb_detail_list

                    img_list = []
                    for img in tb_img_list:
                        if ";" not in img:
                            img_list.append(img)

                    # 没有爬取到内容清除redis里信息，还有风控滑块没有跳转过去下载的风控图片
                    if len(list(set(img_list)))<5:
                        time.sleep(3)  # 没有提取到图片，跳过
                        searchItemImg.redisClient.delete(hashlib.md5(requestUrl.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                        print(f"跳过商品详情页url是{requestUrl}")
                        continue

                    searchItemImg.save_imgs(save_path, img_list)
                else:
                    # 通过item_html通过参数解析图片内容
                    save_path = searchItemImg.make_dirPath(item_html, search_key)
                    tm_lb_list = searchItemImg.tm_get_lb_links(item_html)
                    tm_sku_list = searchItemImg.tm_get_sku_links(item_html)
                    tm_detail_list = searchItemImg.tm_get_detail_links(item_html)
                    tm_img_list = tm_lb_list + tm_sku_list + tm_detail_list

                    img_list = []
                    for img in tm_img_list:
                        if ";" not in img:
                            img_list.append(img)

                    # 没有爬取到内容清除redis里信息，还有风控滑块没有跳转过去下载的风控图片
                    if len(list(set(img_list)))<5:
                        time.sleep(3)  # 没有提取到图片，跳过
                        searchItemImg.redisClient.delete(hashlib.md5(requestUrl.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                        print(f"跳过商品详情页url是{requestUrl}")
                        continue

                    searchItemImg.save_imgs(save_path, img_list)