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
from urllib.parse import urlparse

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driverPath = ChromeDriverManager().install()


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
        self.redisClient = MyRedis(host, password, port, db=7)
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.service = ChromeService(executable_path=driverPath)  # 配置谷歌操作驱动路径
        #self.service = ChromeService(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver.exe')  # 配置谷歌操作驱动路径
        # option.add_argument('--headless')
        # option.add_argument("--user-data-dir="+r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")  #调用本地浏览器，需确认本地没有浏览器窗口打开
        # option.add_argument("load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/nnjjahlikiabnchcpehcpkdeckfgnohf/5.11.7_0")
        self.driver = webdriver.Chrome(options=self.option,service=self.service)

        self.tmHeaders = {
            'authority': 'h5api.m.tmall.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'hng=GLOBAL%7Czh-CN%7CUSD%7C999; cna=MNdAHfe9xi4CAX158qFb1dM7; xlly_s=1; _l_g_=Ug%3D%3D; login=true; cookie2=1ce22af1f33454e5ebcd62a6b9c18251; cancelledSubSites=empty; t=8b9f5ca0b00c1255cf95c94a4df9e2dc; _tb_token_=e9097593338e; _m_h5_tk=fb6ba51b908d0db8a2975b4babaeb6c2_1690436820208; _m_h5_tk_enc=46d71c13b4e953f6be4c4509adb626b6; dnk=tb059498881; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0&existShop=false&cookie21=WqG3DMC9FxUx&cookie14=Uoe9bflPZ45TVg%3D%3D; uc3=id2=UUphzWMtKnyS0KGk8A%3D%3D&nk2=F5RFhSJ6PeUkEmM%3D&lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCsGChuJ1Z9kalthw%3D; tracknick=tb059498881; lid=tb059498881; uc4=nk4=0%40FY4O7F8GgqcDx1UqdvM4BEZCpFytSg%3D%3D&id4=0%40U2grFnyQBWe%2BzdGRiBTguy3gzwcIMkfU; unb=2207414953300; lgc=tb059498881; cookie1=Vqt28cypSWtYAKpxiLTGaHhnR2wNPpQUvCKlwCjFB8k%3D; cookie17=UUphzWMtKnyS0KGk8A%3D%3D; _nk_=tb059498881; sgcookie=E100EJhoKNP1KW0BBy85z45voCsrxzUdZGWwel%2F2Trb6loL6UscnGpNCg%2FmfDGyITZuqkNvug7%2BeJllNcPiwYN0lXbDlw5JIONXPv16PcyMJUZ70%2BKagSxnBTpdfgWKS2KlT; sg=107; csg=9c5fd64c; isg=BHV1JKDFffWJEJkxl8020eoghPEv8ikEeNMUcvea1uw7zpXAv0JP1INPGJJ4jkG8; l=fBE_0FalN3u2-cY-BO5Cnurza77t5IRb4sPzaNbMiIEGa6tC1FT8pNC6GcAMRdtjgTCU8etyzs0aOdLHR3AJwxDDB_5LaCkE3xv9QaVb5; tfstk=c1BNBgqoSReaHqsYypvVYXljPZKOZgjGmv-WsyuFwHqxQiOGiYgvxflXYniEoCf..',
            'referer': 'https://detail.tmall.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
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
            res = requests.get(
                url="http://api.haiwaidaili.net/abroad?num=1&format=1&protocol=http&country=&state=&city=&sep=1&csep=&type=datacenter").text.strip()
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

    # 店铺链接时淘宝的页面
    def request_toget_items(self, cookies: dict, shopLink: str, appUid: str) -> list:
        # 通过tmall.com刷入cookies
        self.driver.get('https://www.tmall.com')
        time.sleep(3)
        for item in self.dict_cookies_to_browser(cookies):
            self.driver.add_cookie(item)
        self.driver.refresh()
        time.sleep(3)

        itemList = []
        headers = {
            'authority': f'{urlparse(shopLink).netloc}',
            # 'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'cna=sjhOHRNw0GcCAW8CWybrYdHu; t=0926a07aea9547d618996a01e818b79c; lgc=tb80111606; tracknick=tb80111606; mt=ci=55_1; thw=cn; cookie2=175794a13305956e39fa359140593694; _tb_token_=fjWYZmThk3Op7; _m_h5_tk=e9d9e5fbf6069cc675c52bdab141ab4a_1691128471404; _m_h5_tk_enc=c0ec13280ec104072290da32ce1d4672; xlly_s=1; _samesite_flag_=true; unb=3451510054; cancelledSubSites=empty; cookie17=UNQyQxMqUdx1nQ%3D%3D; dnk=tb80111606; _l_g_=Ug%3D%3D; sg=641; _nk_=tb80111606; cookie1=U%2BGWz3AsFiX%2BQb4KVw17j51DAUP9jxfiN9Dd%2FomAUJ8%3D; sgcookie=E100fWOQXZpwbu8bxeHM%2F7xosmJ4z3Nmt4hGQ14IilppBFvHk18qbWXRKd9UQBoDd0k0Vrpow7VKQVHeOXvZ1gHF69G4cpByUShb6v7gQ0%2BPtkAsYao6ziiqknffNDusAHtS; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&pas=0&cookie21=Vq8l%2BKCLjhS4UhJVbhgU&existShop=false&cookie14=Uoe9bFvE91m3kg%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D; uc3=lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dCsGCm5ifMPjLwOVs%3D&nk2=F5RNZTse5XZpwA%3D%3D&id2=UNQyQxMqUdx1nQ%3D%3D; csg=43b07397; skt=60037f7028f1cafe; existShop=MTY5MTEyMDMwNg%3D%3D; uc4=id4=0%40UgP5GPE5h%2FvopPV87sjyaL0nrTBJ&nk4=0%40FY4GsvRHfRNKE%2BdeKAjEmuMUbSWH; _cc_=VFC%2FuZ9ajQ%3D%3D; arms_uid=97dafeb8-7574-4664-96cd-50a8f1316654; isg=BPHxqft3MUzdqZ1TCQf7OM1DAH2L3mVQhCcQTtMHMLhE-hNMGijvIQFbGI6cMv2I; l=fBOyr01lNftbuGYGBO5aourza77OaIdbzsPzaNbMiIEGa6GA9pKDJNC69koyWdtjgT5V1eKyzs0aOdEWkPUU-AkDBeYISZ39sApw8eM3N7AN.; tfstk=dMWHXIDby6RQesIurvpQpli7c_V9d29WraHJyLLz_F8spappeAlwA3KrYYRUQ1jfreE7OpCMrN7M8aj7A38PzaYR95eAAM9WUrBuH-ICYAFptS4tfti7RLzYk-htbBapUTpbiNSMDl3dvf67xILmq7FdYtZ4IEIeSxj1QHk2l-TsUnB6YBXPsO-E_jzAgYta2OlSNB-6jEKAFDeG.',
            'referer': f'https://{urlparse(shopLink).netloc}/?spm=a230r.7195193.1997079397.2.348e692cXTXGqa',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        state = 1
        page = 1
        while state:
            params = {
                'pageSize': '200',
                'shopId': urlparse(shopLink).netloc.split(".")[0][4::],
                'page': f'{page}',
                'sortType': 'des',
                'orderType': 'popular',
                'appUid': appUid
            }
            print("当前页信息是来自{}页".format(page))
            if state == 1:
                response = requests.get(f'https://{urlparse(shopLink).netloc}/getShopItemList.htm', params=params,cookies=cookies, headers=headers).json()
                state = int(response["state"])
                if state == 1:
                    for i in response['data']['module']:
                        itemList.append(i["itemUrl"])
                else:
                    break
                yield itemList
                # 迭代后清空
                itemList = []

            page = page + 1
            time.sleep(3)

        yield []

    def get_product_by_taobao_to_tm(self, cookies: dict, item_url: str) -> str:
        start = time.time()

        self.driver.get(url=item_url)
        time.sleep(random.randint(1, 2))
        # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
        self.driver.refresh()
        time.sleep(random.randint(1, 2))
        self.driver.implicitly_wait(2)

        # 设置页面滚动，防止下方的商品没有加载出来导致没有数据返回
        for i in range(15):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(0.5)
        time.sleep(random.randint(5, 8))

        item_body = self.driver.execute_script("return document.documentElement.outerHTML")
        time.sleep(random.randint(5, 8))
        print("单个商品图片下载共计耗时%s" % (time.time() - start))

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
        item_body.replace(" ", "").replace("\n", "")
        detailImgList = []
        outImgList = re.findall(r"src=['\"]([^'\"]+)['\"]", item_body) + re.findall(r"data-src=['\"]([^'\"]+)['\"]",item_body)
        for itemUrl in outImgList:
            if str(itemUrl).startswith("//"):
                detailImgList.append("https:" + itemUrl)
            else:
                detailImgList.append(itemUrl)
        # item_body.replace(" ", "").replace("\n", "")
        # detailImgList = re.findall(r"src=['\"]([^'\"]+)['\"]", item_body) + re.findall(r"data-src=['\"]([^'\"]+)['\"]",item_body)
        detailImgList = [img for img in detailImgList if img.endswith('.jpg')]

        return detailImgList

    def make_dirPath(self, item_body: str) -> str:
        shop_name = "赐律旗舰店"
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
                    except Exception as error:
                        print("图片下载出现错误%s" % error)


if __name__ == "__main__":
    cookiesList = []

    # 直接复制店铺链接，注意加上pageNo
    target_shopLink = 'https://shop201511688.taobao.com//getShopItemList.htm'

    # 创建一个爬取天猫详情的
    tmallItemImg = TmallItemImg()

    # 根据迭代器创建生成器
    items = tmallItemImg.request_toget_items(cookies=random.choice(cookiesList), shopLink=target_shopLink,appUid='RAzN8BQmXpyNR3ymRbFEi2g6tJ6BK')  # 创建一个生成器对象
    for items_list in items:
        if items_list==[]:
            print("爬取完成")
            break
        else:
            for link in items_list:
                if tmallItemImg.is_url_exist(link) == True:
                    print(f"{link}链接重复跳过")
                    continue

                item_body = tmallItemImg.get_product_by_taobao_to_tm(cookies=random.choice(cookiesList), item_url=link)

                lb_list = tmallItemImg.lb_pattern_links(item_body)
                sku_list = tmallItemImg.sku_pattern_links(item_body)
                detail_list = tmallItemImg.detail_pattern_links(item_body)
                img_list = lb_list + sku_list + detail_list

                # 没有爬取到内容清除redis里信息
                if img_list == []:
                    time.sleep(3)  # 没有提取到图片，跳过
                    tmallItemImg.redisClient.delete(hashlib.md5(link.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                    print(f"跳过商品详情页url是{link}")
                    continue
                img_path = tmallItemImg.make_dirPath(item_body)
                tmallItemImg.save_imgs(img_path, img_list)