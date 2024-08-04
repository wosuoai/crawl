import requests
import re
import time
from bs4 import BeautifulSoup
import hashlib
from urllib.request import quote, unquote
from setting import redisHost,redisPort,redisPassword
import redis
from selenium.common.exceptions import TimeoutException

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


class JDItemImg:
    def __init__(self, host=redisHost, port=redisPort, password=redisPassword):
        self.redisClient = MyRedis(host, password, port, db=8)

        self.cookies = {
            'thor': 'CF1D7F0F9ECB5DF64473A3005EEC99E1A28F9E0A9B8502D92DD94C0CF8282ECC9072CB898985BA3BC3A07EDF8D30CB15F73BE6713FBC70B0FFC0FA548258989C74B285886EC59D342B0E52B5AD3A772D62621D7F11DCF1787FE81E10E2FD6600EF846334F6ACDD5A98F1AAD4536680D629B9D9C8BE4383F3E1F2A90D8D80A7853EFF049FD5A7C081412B766D47E869862F8453D2F43F61AA790EA00811BFEF9D',
        }

        self.Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://search.jd.com/Search?keyword=%E8%BF%9E%E8%A1%A3%E8%A3%99&pvid=42089aa2d7fd43faa74aa1c3e8e69d15&isList=0&page=7&s=116&click=0&log_id=1713452065257.6461',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
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

    def dict_cookies_to_browser_jingdong(self, cookies: dict) -> list:
        cookiesBrowserList = []
        for key in cookies:
            cookiesBrowserList.append({
                "domain": ".jd.com",
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

    def scrape_page(self, condition, locator) -> bool:
        print("scraping %s" % self.url)
        try:
            self.driver.get(self.url)
            self.wait.until(condition(locator))
            return True
        except TimeoutException:
            print("error occurred while scraping %s", self.url, exc_info=True)
            return False

    #通过requests返回每页搜索的信息
    def page_items(self, key_word: str) -> str:
        for page_num in range(1,5):
            print("来自第{}页的数据".format(page_num))
            url = 'https://search.jd.com/Search?keyword={}&suggest=1.his.0.0&wq={}&pvid=2825d697aba94a69a802181a40cc6a1e&isList=0&page={}&s=1&click=0&log_id=1713936900746.5227'.format(quote(key_word, encoding="utf-8"), quote(key_word, encoding="utf-8"), page_num * 2 - 1)
            time.sleep(3)

            html = requests.get(url=url, cookies=self.cookies, headers=self.Headers).text

            yield html

    # 单个商品的sku(图片链接和样式)
    def sku_imgurl_title(self, htmlText: str) -> list:
        soup = BeautifulSoup(htmlText, 'html.parser')
        goodsList = soup.find(id="J_goodsList")
        scroll_imgurl_list = []
        scroll_title_list = []
        scrolls = goodsList.find_all(class_="p-scroll")
        for scroll in scrolls:
            items = scroll.find_all(class_="ps-item")
            items_str = ''.join(map(str, items))
            # 单个商品的sku样式
            scroll_title = re.findall(r'title="(.*?)"', items_str)
            scroll_title_list.append(scroll_title)
            # 单个商品的sku图片链接
            img_links = re.findall(r'data-lazy-img="(.*?)"', items_str)
            if len(img_links) != 0:
                img_links = ['https:' + img_link.replace(".avif", "") for img_link in img_links]
                scroll_imgurl_list.append(img_links)
            else:
                scroll_imgurl_list.append(img_links)

        return scroll_imgurl_list, scroll_title_list

    # 单个商品的价格
    def items_prices(self, htmlText: str) -> list:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # 每页商品的所有数据
        goodsList = soup.find(id="J_goodsList")
        prices_list = [price.text for price in goodsList.find_all('i', {'data-price': True})]

        return prices_list

    # 单个商品的详情页链接和标题
    def items_url_title(self, htmlText: str) -> list:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # 每页商品的所有数据
        goodsList = soup.find(id="J_goodsList")
        url_list = []
        title_list = []
        url_title = goodsList.find_all(class_="p-name p-name-type-2")
        for elements in url_title:
            url_list.append("https:" + elements.find('a')['href'])
            title_list.append(elements.find('em').text)

        return url_list, title_list

    # 单个商品对应的店铺名
    def items_shopName(self, htmlText: str) -> list:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # 每页商品的所有数据
        goodsList = soup.find(id="J_goodsList")
        shopName_list = []
        shop_name = goodsList.find_all(class_="p-shop")
        for name in shop_name:
            shopName_list.append(name.find('a', {'class': 'curr-shop hd-shopname'}).text)

        return shopName_list

    # 单个商品参与的活动
    def items_icons(self, htmlText: str) -> list:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # 每页商品的所有数据
        goodsList = soup.find(id="J_goodsList")
        icons_list = []
        discounts = goodsList.find_all(class_="p-icons")
        for discount in discounts:
            icons = discount.find_all('i', {'class': 'goods-icons4 J-picon-tips'})
            item_icon = [icon.text for icon in icons]
            icons_list.append(item_icon)

        return icons_list

if __name__ == "__main__":
    # 京东
    #cookiesList = []

    # 输入商品关键词
    search_key="马面裙"

    # 创建一个通过关键词爬取
    jdItemImg = JDItemImg()

    for jd_html in jdItemImg.page_items(key_word=search_key):
        jd_sku_imgurl, jd_sku_title = jdItemImg.sku_imgurl_title(jd_html)
        jd_items_prices = jdItemImg.items_prices(jd_html)
        jd_items_url, jd_items_title = jdItemImg.items_url_title(jd_html)
        jd_items_shopName = jdItemImg.items_shopName(jd_html)
        jd_items_icons = jdItemImg.items_icons(jd_html)

        onsale_list = ["跨店每满", "官方立减", "券", "满"]
        for i in range(len(jd_items_icons)):
            final_price = int(jd_items_prices[i].split(".")[0])
            for icon in jd_items_icons[i]:
                for sale in onsale_list:
                    if sale in icon:
                        if sale == "券":
                            maxout = int(icon.split('-')[0].replace("券", ""))
                            discount = int(icon.split('-')[1])
                            if maxout <= int(jd_items_prices[i].split(".")[0]):
                                final_price = int(jd_items_prices[i].split(".")[0]) - discount
                        elif sale == "跨店每满":
                            maxout = int(icon.split('-')[0].replace("跨店每满", ""))
                            discount = int(icon.split('-')[1])
                            if maxout <= int(jd_items_prices[i].split(".")[0]):
                                int_more = int(jd_items_prices[i].split(".")[0]) // maxout
                                final_price = int(jd_items_prices[i].split(".")[0]) - discount * int_more
                        elif sale == "满":
                            try:
                                maxout = int(icon.split('-')[0].replace("满", ""))
                                discount = int(icon.split('-')[1])
                                if maxout <= int(jd_items_prices[i].split(".")[0]):
                                    final_price = int(jd_items_prices[i].split(".")[0]) - discount
                            except:
                                pass
                        elif sale == "官方立减":
                            maxout = int(icon.split('-')[0].replace("官方立减", "").replace("%", ""))
                            final_price = int(jd_items_prices[i].split(".")[0]) - int(jd_items_prices[i].split(".")[0]) * round(maxout / 100,2)
            print(jd_items_shopName[i], jd_items_title[i], jd_items_url[i], jd_items_prices[i], jd_sku_imgurl[i], jd_sku_title[i], jd_items_icons[i], final_price)