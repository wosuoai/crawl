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
from curl_cffi import requests


from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driverPath = ChromeDriverManager().install()
driverPath = r'C:\Users\Administrator\.wdm\drivers\chromedriver\win64\116.0.5845.97\chromedriver.exe'
chrome_path = r"D:\chrome-win64\chrome.exe" #指定浏览器的路径


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


class TmallItemImg:
    def __init__(self, host=redisHost, port=redisPort, password=redisPassword):
        self.redisClient = MyRedis(host, password, port, db=5)
        self.option = webdriver.ChromeOptions()
        #self.option.add_argument('--proxy-server=socks5://127.0.0.1:8080')
        self.option.binary_location = chrome_path
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.option.add_argument("--incognito")  # 开启隐身模式
        self.service = ChromeService(executable_path=driverPath)  # 配置谷歌操作驱动路径
        #self.service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe') # 配置谷歌操作驱动路径
        # option.add_argument('--headless')
        # option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
        # option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
        self.driver = webdriver.Chrome(options=self.option,service=self.service)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

        self.tmHeaders = {
            'authority': 'h5api.m.tmall.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'lid=tb82043229; xlly_s=1; dnk=tb82043229; uc1=cookie14=Uoe9aOewhJmsPg%3D%3D&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie21=V32FPkk%2FhSg%2F&pas=0&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&existShop=false; uc3=id2=UUpgQEvwuxBfi25wxA%3D%3D&vt3=F8dCsGSJT8wStc7iUd8%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&nk2=F5RNZ%2BB4f8h9FA%3D%3D; tracknick=tb82043229; _l_g_=Ug%3D%3D; uc4=nk4=0%40FY4GsEDQgJWFAvgKMhdRJAJDZ3eJ&id4=0%40U2gqz6QafAOV0MtvTNM1aQ3WctDsvdlH; unb=2216225431902; lgc=tb82043229; cookie1=UoMzgezpddPRRNA%2BCOjq9bWgwscNZZWmPolL71wcS1M%3D; login=true; cookie17=UUpgQEvwuxBfi25wxA%3D%3D; cookie2=14815f9859b8711213ab8a9f7c644905; _nk_=tb82043229; sgcookie=E100cB6coE9%2BSEJ%2F98W7xKqVFqNsm37IxtaQfiayXS0Y5bLjXQwshPgiBYlXzzuQ7xsWiRvES1PxHEqO15OPY7ot14Zi1yNiTdMFqmzmA9L4l8c%3D; cancelledSubSites=empty; sg=92b; t=9ad07e40fbff7f93e3b183060be0456d; csg=f7a50bdc; _tb_token_=fb3be966ab1ba; _m_h5_tk=808ca4b9a63ef3e8af5628525397c85b_1695114118676; _m_h5_tk_enc=de6cf74de094aec835a8ea44e8f30f07; cna=hS2QHXCurFkCAXPDTAjtBsQO; tfstk=d_J9Ug2BE20MYClfv5hng0QFikonZdKNpF-7nZbgGeLpzUembCYD9iTHktXDcV8vHwTTnCxMcoIX-O12sZbGktK2yD0oEYxwbt5sr4Dkk4KN3hIiyJMkbhW4XrikOY2xQKh5EskQDAmgdp9cfjk6NM59lpIO1Xx1R-sepGCOPh9ThOPJELIzUzbRm5iKvSPV1MuR5m51.; l=fBE_0FalN3u2-TLUKOfwPurza77OSIRAguPzaNbMi9fPOWfp5mvAW1h_sAT9C3GVF6W6R3-WjmOpBeYBqnmsAd8Aa6Fy_CkmnmOk-Wf..; isg=BNbWf3zPr6jev5q8gChlZMUtJ4zYdxqx9LVAvkA_wrlUA3adqAdqwTz1m5_vqxLJ',
            'origin': 'https://detail.tmall.com',
            'referer': 'https://detail.tmall.com/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        self.cookiesList = []
        self.enableIpProxy = False

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
            #res = requests.get(url="http://webapi.http.zhimacangku.com/getip_3h?num=1&type=1&pro=&city=0&yys=0&port=1&pack=336912&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=").text.strip()
            with open(file=r"C:\Users\Administrator\Desktop\1.txt", mode="r", encoding="utf-8") as f:
                data = f.read()
            ip_list = data.replace("\n", ",").split(",")
            res=random.choice(ip_list)
            print(res)
            return {
                "http": "http://{}".format(res),
                "https": "http://{}".format(res)
            }
        else:
            return None

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
        for page in range(2,int(page_num) + 2):
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
        self.driver.get(url=item_url)
        time.sleep(random.randint(1, 2))

        self.outside_slide()
        self.insideTM_slide()

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
                            f.write(requests.get(imgUrl, headers=self.tmHeaders, proxies=self.set_proxy()).content)
                            # f.write(requests.get(imgUrl, headers=self.Headers, proxies=proxies).content)
                    except Exception as error:
                        print("图片下载出现错误%s" % error)

if __name__ == "__main__":
    cookiesList = [{'tfstk': 'd9ZeUVXDtMIFQFfsR2orb8uetkmKcmCfLuGSE82odXchw9Ho4WNir3wCJTWr_7hIRD4IE3Ps17t7duz94-e8A9n5pDeK20ffGitzpJnRp95fceiu3tmlGssX5d0dO04CL7KPU1MViZQmls2xskEzS0O2xRlwq3JxL2ccDf-kqlkUQjXaXQHM8UZ88QYr-AHZGOWapQufo', '_m_h5_tk': '33bca8a9fd4f422443e2009d338aac11_1696689990045', 'uc1': 'cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&cookie21=W5iHLLyFfoaZ&cookie14=Uoe9a717fydHkQ%3D%3D&pas=0&cookie15=UtASsssmOIJ0bQ%3D%3D', 'cancelledSubSites': 'empty', 'uc4': 'id4=0%40U2gqz6QY%2BuLQ6lct5m54rey7n8Ktex9E&nk4=0%40FY4I6FUnZTj%2BCtAGblpRX8MTjizfov%2BxgQ%3D%3D', 'sgcookie': 'E1000c6aFE4mVGoLfNEH97VMcFW%2BrnMQZZr0%2Fmbr9ALsaINCRSJls4B6Yzvn63%2FqhmafLw1clEDLngs1Fh4DJqqsuoJ5W6o14MNEr3yfk5T1mBU%3D', 'tracknick': 'tb675900152750', '_nk_': 'tb675900152750', 'sg': '070', '_tb_token_': 'f0e6336b37dbb', 'csg': '91d9e603', 'cookie2': '1540b707a527e85f3fb8128cb6da86b3', 'xlly_s': '1', 'isg': 'BE5OEAlvp5gYGxO85AdAVvB1nyQQzxLJvJ3IBniXutEM2-414F9i2fQZFwe3Qwrh', 'unb': '2216208669787', 'uc3': 'nk2=F5RDK1aMEME8kyIMKUM%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUpgQEvyiMFol7r9dg%3D%3D&vt3=F8dCsGrKdAq7xAVVWIM%3D', 'cookie17': 'UUpgQEvyiMFol7r9dg%3D%3D', '_l_g_': 'Ug%3D%3D', 't': '9f8739346c760326c7d7805e3c073fef', 'lid': 'tb675900152750', 'login': 'true', 'dnk': 'tb675900152750', 'l': 'fBO0Uw9rPEyFXN_2BOfwPurza77OSIRAguPzaNbMi9fPO7C95hVlW1nbATTpC3GVF6PWR3-WjmOpBeYBqS2TUEGCa6Fy_CkmnmOk-Wf..', 'lgc': 'tb675900152750', '_m_h5_tk_enc': '62ae21122dadec3e055741b6881a2ef7', 'cookie1': 'AHmARbUtDQf0ukZ86Lb%2B1T8d6lvSen3LOaBTFr0vJxE%3D', 'cna': 'CTqoHXhVE3ACAXPBe+okzX3n'}]

    # 直接复制店铺链接，注意加上pageNo
    target_shopLink = 'https://plainpeople.tmall.com/category.htm?spm=a1z10.1-b-s.w15598761-23604912033.5.3b1f281eIoHHDj&search=y&pageNo=1#anchor'

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
                print("单个商品图片下载共计耗时%s" % (time.time() - start))
