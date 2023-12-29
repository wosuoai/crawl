# -*- coding: utf-8 -*-
from selenium import webdriver
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
from setting import redisHost, redisPort, redisPassword
import redis
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Edge
from fake_useragent import UserAgent
from selenium.webdriver.edge.options import Options as EdgeOptions
import concurrent.futures

from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driverPath = ChromeDriverManager().install()
#driverPath = r'C:\\Users\\15256\\.cache\\selenium\\chromedriver\\win64\\115.0.5790.170\\chromedriver.exe'

#指纹绕过
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import warnings
import urllib3

script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''

from concurrent.futures import ThreadPoolExecutor
import queue


# 重新封装线程池类
class ThreadPool_Executor(ThreadPoolExecutor):
    """
    重写线程池修改队列数
    """

    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        # 队列大小为最大线程数的两倍
        self._work_queue = queue.Queue(self._max_workers * 2)

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


class TmallItemImg:
    def __init__(self, host=redisHost, port=redisPort, password=redisPassword):
        self.redisClient = MyRedis(host, password, port, db=5)
        self.option = EdgeOptions()
        # # 设置代理IP
        # proxy_ip = '125.124.201.220:1234'
        # self.option.add_argument('--proxy-server={}'.format(proxy_ip))
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        #self.option.add_argument("--incognito")  # 开启隐身模式
        self.option.add_argument("--inprivate")
        # 关闭警告
        urllib3.disable_warnings()
        warnings.filterwarnings("ignore")
        #self.service = ChromeService(executable_path=driverPath)  # 配置谷歌操作驱动路径
        self.service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\msedgedriver.exe') # 配置谷歌操作驱动路径
        # option.add_argument('--headless')
        # option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
        # option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
        self.driver = Edge(options=self.option,service=self.service)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

        self.tmHeaders = {
            'authority': 'h5api.m.tmall.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'cna=oagQHJX9ghUCAbaOb348Rp8T; ariaDefaultTheme=undefined; hng=GLOBAL%7Czh-CN%7CUSD%7C999; miid=435332491841349282; lid=tb117416292; xlly_s=1; sgcookie=E100SBCAN08%2BgskwonVlc29WkBj104g71oTTgKSTrfxhcdm8X%2FwWx4sfvvTi6Y%2FjA30T%2Fn0hmcEN4A7gVpL9vAk2ThTYH297Qci5jTQaUdMv0FE%3D; uc1=cookie14=Uoe9aOGZ58%2F%2BkQ%3D%3D; t=e73098be23d1e6971fd7ec8b8226d1c4; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&nk2=F5REP7sBUHYX1vY%3D&vt3=F8dCsGSHRAgtLaGYRQI%3D&id2=UUphzOV4ZmtYf4ZcQA%3D%3D; tracknick=tb117416292; uc4=id4=0%40U2grF8636cbIDpmfqxXgrXyMKXCE9Wp1&nk4=0%40FY4Pba8SP%2Fxz1We3n%2B84Rgoi4rtoew%3D%3D; lgc=tb117416292; _tb_token_=eeeeea17fbefe; cookie2=1b42a56a5589ea0faac2113ae58d9008; _m_h5_tk=b410c95a1d36f96d4dba5b499164ca38_1695724068822; _m_h5_tk_enc=edffede86addf81698c5b5f6218143c6; tfstk=d6RyUdOXhbhyzHmfFT5e7GCVLX1RT1nszBsC-eYhPgjov4QhT3tcKWTSe2uF0HI5F_v5-W-fcHNBPBJYTFLpN4CIy_LR96msffNeyUCdrmms181H7VfnfcG_hrX-V6v58iPhU45uYygF3cYOmQM7OghndUS4tWzOzTji6iP3tI7yuGXwlkQD7XOpUk2FEZQVfqu2ovhwT; l=fBIbldWmNkCzReLWKOfwPurza77OSIRAguPzaNbMi9fP_x1p5HLAW1HVGaT9C3GVF6VMR3-P4wWXBeYBqnmsAd8Aa6Fy_CkmnmOk-Wf..; isg=BJKSSxvcIz9rL17-AOo0mrfd41h0o5Y9U-cXH1zrvsUwbzJpRDPmTZiJ38vTHw7V',
            'origin': 'https://detail.tmall.com',
            'referer': 'https://detail.tmall.com/',
            'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent().random,
        }
        self.cookiesList = []
        self.enableIpProxy = False
        self.max_workers=1
        self.threadsPool = ThreadPool_Executor(max_workers=self.max_workers)  # 定义线程数量

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
            #res=requests.get(url="http://proxy.siyetian.com/apis_get.html?token=gHbi1yTUVUNPR1Zy4EVNJTT31STqFUeNpXR31ERjBTTqFlMORVS31kaVpnTUN2M.QNxQzM1cjN5YTM&limit=1&type=0&time=&split=0&split_text=&repeat=0&isp=0").text
            # ip_list=res.split("\r\n")
            # ip_list = ['58.209.192.141', '49.72.171.122', '49.72.171.61', '49.72.171.118', '49.72.171.137']
            # res=random.choice(ip_list)
            return {
                "http": "http://{}".format('220.187.129.188:12261'),
                "https": "http://{}".format('220.187.129.188:12261')
            }
            # url="https://www.baidu.com"
            # try:
            #     response = requests.get(url, proxies=proxies)
            #     # 判断代理IP是否可用
            #     if response.status_code == 200:
            #         return proxies
            # except:
            #     print("代理ip失效")
            #     return None

    def dict_cookies_to_browser(self, cookies: dict) -> list:
        cookiesBrowserList = []
        for key in cookies:
            cookiesBrowserList.append({
                "domain": ".tmall.com",
                "name": key,
                "value": cookies[key]
            })
        return cookiesBrowserList

    def get_cookiesList_from_cookiesPool(sleepTime: int = 2, cookiesPoolUrl="") -> dict:
        cookies = {}
        while cookies == {}:
            time.sleep(sleepTime)
            cookies = requests.get(url="http://www.baidu.com").json()
        return [cookies]

    # 定义一个xpath的捕获异常
    def xpathExists(self, xpath):
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

    def handle_vertify(self):
        iframe = self.driver.find_element(By.XPATH,'/html/body/div[4]/iframe')
        # iframe = self.driver.find_elements(By.XPATH,'//div[@class="J_MIDDLEWARE_FRAME_WIDGET"]//iframe')
        # print(iframe)
        # if len(iframe) == 0:
        #     return
        self.driver.switch_to.frame(iframe)
        trys = 0
        # 需要多次尝试
        while trys < 5:
            trys += 1
            slider = self.driver.find_element(By.XPATH,"//*[@id='nc_1_n1t']/span")  # 需要滑动的元素
            ActionChains(self.driver).click_and_hold(slider).perform()
            # 大概滑动３００就可以通过验证
            trace = [10, 20, 30, 40, 40, 40, 30, 30, 30, 30]
            for i in range(len(trace)):
                ActionChains(self.driver).move_by_offset(xoffset=trace[i], yoffset=0).perform()
            ActionChains(self.driver).release().perform()
            # move_to_gap2(driver,slider,get_track(270))
            refresh = self.driver.find_elements(By.XPATH,"//span[@class='nc-lang-cnt']/a")
            if len(refresh) > 0:
                refresh[0].click()
                continue
            time.sleep(random.randint(2, 5))
            if self.driver.page_source.find("nc_1_n1t") == -1:
                self.driver.switch_to.parent_frame()
                break
        if trys >= 5:
            print("[Error]:vertify code error")
        else:
            print("[Success]:vertify code error")

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
            time.sleep(random.randint(2, 5))
            if self.driver.page_source.find("nc_1_n1z") == -1:
                self.driver.switch_to.parent_frame()
                break

    # 页面滚动到底部
    def scroll(self):
        for i in range(5):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(1)

    #定义curl_cffi库中支持的三种浏览器，隐藏指纹信息
    def which_Browser(self):
        browser_list=['edge99','chrome110','safari15_3']
        browser=random.choice(browser_list)

        return browser

    # 获取每个商品页面js渲染后的HTML数据
    def get_item_links(self, cookies: dict, shopLink: str) -> list:
        self.driver.get('https://www.tmall.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser(cookies):
            self.driver.add_cookie(item)
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        self.driver.get(shopLink)
        # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
        self.driver.refresh()
        self.driver.implicitly_wait(2)

        time.sleep(5)

        page_num = self.driver.find_element(By.XPATH, '//*[@id="J_ShopSearchResult"]/div/div[2]/p/b').text.replace("/","")[1:]  # 该店铺总共有多少页的商品
        shop_name = self.driver.find_element(By.XPATH, '//*[@id="shopExtra"]/div[1]/a/strong').text  # 该店铺的名称
        for page in range(19,int(page_num) + 2):
            print("当前获取的数据是来自第{}页".format(page-1))
            # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
            self.scroll()

            shop_body = self.driver.execute_script("return document.documentElement.outerHTML")
            time.sleep(random.randint(5, 8))

            result = re.findall(r"\d{12}\|", shop_body)
            content = '|'.join(result).strip('|')
            item_list = content.split("||")  # 店铺每页商品的所有productid
            url_list = []
            for item in item_list:
                requestUrl = 'https://detail.tmall.com/item.htm?abbucket=10&id={}&rn=6a87064040bd23dd8bd942e848f59683&sku_properties=1627207:24946378100&spm=a1z10.5-b-s.w4011-18694600216.97.702a1fc6hLdih0'.format(item)
                url_list.append(requestUrl)

            yield url_list,shop_name

            self.driver.get(target_shopLink.split("pageNo")[0] + "pageNo={}#anchor".format(page))
            time.sleep(random.randint(2, 3))
            # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
            self.driver.refresh()
            self.driver.implicitly_wait(2)

        return [],shop_name

    def get_product_body(self,item_url:str)->str:
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        # 关闭警告
        urllib3.disable_warnings()
        warnings.filterwarnings("ignore")
        self.driver.get(url=item_url)
        time.sleep(random.randint(1, 2))

        try:
            self.outside_slide()
            self.insideTM_slide()
        except:
            pass

        # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
        self.scroll()
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.randint(5, 8))

        item_body = self.driver.execute_script("return document.documentElement.outerHTML")
        time.sleep(random.randint(3, 5))
        # time.sleep(random.randint(10, 20))
        return item_body

    # 解析轮播图
    def lb_pattern_links(self, item_body: str) -> list:
        lbImgList = []
        pattern = r"//gw.alicdn.com/imgextra.*?\.webp"
        matches = re.findall(pattern, item_body)

        for match in matches:
            if ";" in match:
                del match
            elif "110x10000Q75.jpg" in match:
                lb_link = "https:" + match.replace("_110x10000Q75.jpg_.webp", "")
                lbImgList.append(lb_link)

        return lbImgList

    # 解析sku
    def sku_pattern_links(self, item_body: str) -> list:
        skuImgList = []
        pattern = r"//gw.alicdn.com/bao/uploaded.*?\.webp"
        matches = re.findall(pattern, item_body)

        for match in matches:
            if "src" in match:
                del match
            else:
                if "60x60q50.jpg" in match:
                    sku_link = "https:" + match.replace("_60x60q50.jpg_.webp", "")
                    skuImgList.append(sku_link)

        return skuImgList

    # 解析详情图
    def detail_pattern_links(self, item_body: str) -> list:
        detailImgList=[]
        item_body.replace(" ", "").replace("\n", "")
        ImgList = re.findall(r"src=['\"]([^'\"]+)['\"]", item_body) + re.findall(r"data-src=['\"]([^'\"]+)['\"]", item_body)
        ImgList=[img for img in ImgList if img.endswith('.jpg')]
        for img in ImgList:
            if "https:" not in img:
                detailImgList.append("https:"+img)
            else:
                detailImgList.append(img)

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

    # 多线程下载
    def _threads_download(self, dirPath: str, filename: str, imgUrl: str, headers: dict):
        try:
            proxies = self.set_proxy()
            if proxies:
                with open("{}/{}.jpg".format(dirPath, filename), "wb") as f:
                    f.write(requests.get(imgUrl, headers=headers, proxies=proxies).content)
                    print(dirPath + "图片{}下载成功".format(imgUrl))
            return
        except Exception as error:
            print("图片下载出现错误%s" % error)
            return

    # 将图片列表写入到文件夹
    def save_imgs(self, dirPath: str, imgList: list):
        from curl_cffi import requests
        # 如果文件夹不存在创建文件夹
        if os.path.exists(dirPath) == False:
            os.makedirs(dirPath)

        if len(imgList) > 0:
            for imgUrl in imgList:
                if str(imgUrl).startswith("http"):
                    filename = uuid.uuid4().hex
                    # 走代理下载
                    if self.enableIpProxy:
                        self.threadsPool.submit(self._threads_download,dirPath, filename, imgUrl, self.tmHeaders)

                    # 不走代理下载
                    else:
                        try:
                            with open("{}/{}.jpg".format(dirPath, filename), "wb") as f:
                                print(dirPath + "图片{}下载成功".format(imgUrl))
                                f.write(requests.get(imgUrl, headers=self.tmHeaders, proxies=self.set_proxy()).content)
                        except Exception as error:
                            print("图片下载出现错误%s" % error)

if __name__ == "__main__":
    cookiesList = []

    # 直接复制店铺链接，注意加上pageNo
    target_shopLink = 'https://bokaqi.tmall.com/search.htm?spm=a1z10.1-b-s.w5002-16088423282.1.1fd5249emV5Qgr&search=y&pageNo=18#anchor'

    # 创建一个爬取天猫详情的
    tmallItemImg = TmallItemImg()
    result = tmallItemImg.get_item_links(cookies=random.choice(cookiesList), shopLink=target_shopLink)

    for url_list, shop_name in result:

        if url_list == []:
            print("爬取完成")
            break
        else:
            for url in url_list:
                # 判断是否需要进行去重
                if tmallItemImg.is_url_exist(url) == True:
                    print("该商品url已经爬取过,对url进行跳过")
                    continue

                item_body=tmallItemImg.get_product_body(item_url=url)

                # 通过item_body通过参数解析图片内容
                lb_list = tmallItemImg.lb_pattern_links(item_body)
                sku_list = tmallItemImg.sku_pattern_links(item_body)
                detail_list = tmallItemImg.detail_pattern_links(item_body)
                img_list = lb_list + sku_list + detail_list

                # 没有爬取到内容清除redis里信息
                if img_list == []:
                    time.sleep(3)  # 没有提取到图片，跳过
                    tmallItemImg.redisClient.delete(hashlib.md5(url.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                    print(f"跳过商品详情页url是{url}")
                    break
                img_path = tmallItemImg.make_dirPath(item_body, shop_name)
                start=time.time()
                tmallItemImg.save_imgs(img_path, img_list)
                downimg_time=time.time() - start
                print("单个商品图片下载共计耗时%s" % downimg_time)
                #如果下载图片时间不足5s，等待延迟后在继续
                if int(downimg_time) < 5:
                    time.sleep(3)