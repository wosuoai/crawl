# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.request import quote, unquote
from selenium.webdriver.common.by import By
import random
import re
import hashlib
from setting import redisHost, redisPort, redisPassword
import redis
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService


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
        self.option.add_extension(r"C:\Users\admin\Downloads\push_item_imgs.crx") #给当前浏览器安装插件
        self.option.add_experimental_option('prefs', {"extensions.ui.developer_mode": True, }) #启用扩展程序的开发者模式
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--lang=zh-CN")
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.service = ChromeService(executable_path=r'C:\Users\admin\.wdm\drivers\chromedriver\win64\118.0.5993.70\chromedriver-win32\chromedriver.exe') # 配置谷歌操作驱动路径
        self.driver = webdriver.Chrome(options=self.option,service=self.service)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    # 基于url的md5实现url去重
    def is_url_exist(self, url: str):
        urlMd5Str = hashlib.md5(url.encode()).hexdigest()
        if self.redisClient.str_get(urlMd5Str):
            return True
        self.redisClient.str_set(urlMd5Str, 1)
        return False

    def dict_cookies_to_browser(self, cookies: dict) -> list:
        cookiesBrowserList = []
        for key in cookies:
            cookiesBrowserList.append({
                "domain": ".tmall.com",
                "name": key,
                "value": cookies[key]
            })
        return cookiesBrowserList

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

    # 页面滚动到底部
    def scroll(self):
        for i in range(5):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(1)

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

    def login_tmall(self):
        self.driver.get(url="https://login.tmall.com/")
        self.driver.switch_to.frame("J_loginIframe")  # 登录框在iframe里，打开页面后，需要切换到iframe

        time.sleep(5)
        name_input_element = self.driver.find_element(By.ID, 'fm-login-id')
        time.sleep(1)
        name_input_element.clear()
        account = "13175523170"
        for s in account:
            name_input_element.send_keys(s)
            time.sleep(random.randint(1, 4) * 0.1)

        time.sleep(2)
        password_input_element = self.driver.find_element(By.ID, 'fm-login-password')
        time.sleep(1)
        password_input_element.clear()
        password = "dejavu8279"
        for s in password:
            password_input_element.send_keys(s)
            time.sleep(random.randint(1, 4) * 0.1)

        time.sleep(10)

        # 点击登陆按钮
        button = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button')
        button.click()
        time.sleep(3)

        self.driver.get("https://detail.tmall.com/item.htm?abbucket=20&id=716249068289&ns=1")
        WebDriverWait(self.driver, 60, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/h1')))
        self.driver.implicitly_wait(10)

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

        page_num = self.driver.find_element(By.XPATH, '//*[@id="J_ShopSearchResult"]/div/div[2]/p/b').text.replace("/", "")[1:]  # 该店铺总共有多少页的商品
        for page in range(2, int(page_num) + 2):
            print("当前获取的数据是来自第{}页".format(page - 1))
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

            yield url_list

            self.driver.get(target_shopLink.split("pageNo")[0] + "pageNo={}#anchor".format(page))
            time.sleep(random.randint(2, 3))
            # 这里一定要刷新页面 否则会出现页面加载不出内容的情况
            self.driver.refresh()
            self.driver.implicitly_wait(2)

        return []

    def down_img_by_crx(self):
        try:
            self.scroll()
            time.sleep(random.randint(5,8))
            handles = self.driver.window_handles  # 获取所有窗口,如果定位插件按钮错误，直接回退到原来窗口

            cj = self.driver.find_element(By.CSS_SELECTOR, '#fatkun-view-wrapper > div > button:nth-child(1)')  # 定位插件按钮
            cj.click()  # 点击插件下载按钮
            time.sleep(3)

            handles = self.driver.window_handles  # 获取所有窗口
            self.driver.switch_to.window(handles[1])  # 切换到下载窗口
            time.sleep(random.randint(2, 3))

            download_button = self.driver.find_element(By.CSS_SELECTOR, '#header-slot > button:nth-child(1)')  # 获取下载按钮
            download_button.click()  # 点击下载按钮
            time.sleep(random.randint(2, 3))

            bctu_button = self.driver.find_element(By.CSS_SELECTOR,'#app > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.el-button--primary > span')  # 点击保存图片按钮
            bctu_button.click()  # 点击保存图片按钮
            time.sleep(random.randint(8, 12))

            self.driver.close()  # 关闭当前窗口
            self.driver.switch_to.window(handles[0])  # 切换回一窗口
        except Exception as error:
            self.driver.switch_to.window(handles[0])
            print("失败是：%s" % error)

    def down_item_imgs(self, item_url: str):
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.driver.get(url=item_url)
        time.sleep(random.randint(2, 3))

        self.outside_slide()
        self.insideTM_slide()

        self.down_img_by_crx()
        time.sleep(random.randint(15,25))

if __name__ == "__main__":
    cookiesList = [{'tfstk': 'deo9U7sIqBAGGhYbpNLHuQe77_JHKcHavfk5mSVGlXhKabIDQVcmJ-GnMoqmhClxDWGOmVDihtejtlaqSSVgMoHqwpAkq3DZQoz6ZQxoGsMa0AeMwMtoQArVBs9oR3jvbo_hUxTPINWhXcn0CE-EY841ocwTWSI09iCynRUTZANpNQ6aw0m8Ug5uw-b6ppQVuPwew5945', '_m_h5_tk': '8d0c3c6597512c79b023b25fbf4c4ffe_1695097531852', 'uc1': 'existShop=true&pas=0&cookie21=WqG3DMC9Fbk9noNn0ySw&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie14=Uoe9aOayj60c2w%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D', 'cancelledSubSites': 'empty', 'uc4': 'nk4=0%40FcEKYMKi8FTUUKLwv4FV6FiCnbGM5zR%2FMQ%3D%3D&id4=0%40UgbvDH8R6%2BaCqcdPWfZb%2FrtJSGmA', 'sgcookie': 'E100WD7Sy9oGe8WiGYa4BhrNtNEok%2BkzUHv2YXVm76xCzOekCOx%2FMMfoyWvZDImnSHFt4DryH%2FdUcaRWDjJQDjmjVoSDZo7%2BTWUFwoUvvywW9Pg%3D', 'tracknick': 't-3110751053-1', '_nk_': 't-3110751053-1', 'sg': '134', '_tb_token_': 'e4eee13e8eeeb', 'csg': 'f94e526f', 'cookie2': '1af51697c5f6eb0487bce5d00aac08f6', 'xlly_s': '1', 'isg': 'BD09zYQIBFXoYKHyXD_M7PhkTJk32nEs4wDbq_-CXhTDNl1oxy7g_ork5Gpwtonk', 'unb': '3110751053', 'uc3': 'vt3=F8dCsGSJTipiV2%2B%2BdZs%3D&lg2=UIHiLt3xD8xYTw%3D%3D&id2=UNGXErL6DPTPew%3D%3D&nk2=F9vlEhVtaAUXKX4c3Mk%3D', 'cookie17': 'UNGXErL6DPTPew%3D%3D', '_l_g_': 'Ug%3D%3D', 't': 'e2a17efc8e2b20df90213c81e2e04ed2', 'lid': 't-3110751053-1', 'login': 'true', 'dnk': 't-3110751053-1', 'l': 'fBIMmS5RNZnWlM9sKOfZourza779RIRAguPzaNbMi9fPOLC65hbNW1hs_-YBCnGVF62XR3-WjmOpBeYBqIvTUEGCa6Fy_QkmnmOk-Wf..', 'lgc': 't-3110751053-1', '_m_h5_tk_enc': '5eefecd7efa1042b7a360535b0c3cf56', 'cookie1': 'Wqajzt427CkD7%2BKUaBPrkLCOKT2Ni0o1cMo4O%2B22aM4%3D', 'cna': 'duFAHTR2tzYCAX158qGMeKOh'}]

    # 直接复制店铺链接，注意加上pageNo
    target_shopLink = 'https://mixiufushi.tmall.com/search.htm?spm=a1z10.1-b-s.w5001-23642529525.3.47a96f565wY4tT&search=y&orderType=newOn_desc&tsearch=y&scene=taobao_shop&pageNo=1#anchor'

    # 创建一个爬取天猫详情的
    tmallItemImg = TmallItemImg()
    result = tmallItemImg.get_item_links(cookies=random.choice(cookiesList), shopLink=target_shopLink)

    for url_list in result:

        if url_list == []:
            print("爬取完成")
            break
        else:
            for url in url_list:
                # 判断是否需要进行去重
                if tmallItemImg.is_url_exist(url) == True:
                    print("该商品url已经爬取过,对url进行跳过")
                    continue

                tmallItemImg.down_item_imgs(item_url=url)
                print(f'------------提取item详情页{url}完成------------')