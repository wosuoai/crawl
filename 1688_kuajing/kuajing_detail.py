from selenium import webdriver
# 基于requests的方案
# https://blog.csdn.net/weixin_42216028/article/details/107701421
from urllib.parse import urlparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains   
import logging
import time
import re
import pandas as pd
import os

# set log config
logging.basicConfig(level=logging.INFO,filename="./kuajing_detail.log",
                    format='%(asctime)s-%(levelname)s-%(message)s')

# 定义解析链接的类，实现任意网站的链接解析，支持登陆渲染
class ParseLink:
    def __init__(   
                self,
                url:str,
                cookies:list,
                executablePath:str,
                sourceUrl:str,
                timeOut:int=5,
                EnableLinuxRoot=False,
                Enableincogniton=False,
                EnableHeadless=False,
                EnableCookies=True
                ) -> None:
        # 创建一个option对象
        self.option = webdriver.ChromeOptions()
        
        # 设置爬取页面超市时间
        self.timeOut=timeOut
        
        # 指定的webdriver路径
        self.executablePath=executablePath
        
        # linux下允许root运行
        if EnableLinuxRoot:
            self.option.add_argument('--no-sandbox')
        # 设置无头模式
        if EnableHeadless:
            self.option.add_argument('--headless')
        # 开启无痕模式
        if Enableincogniton:
            self.option.add_argument("--incognito")
       
        # 设置关闭开发者模式防止被检测
        self.option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.browser=webdriver.Chrome(executable_path=self.executablePath,options=self.option)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        # 定义一个wait对象
        self.wait=WebDriverWait(self.browser,self.timeOut)
        # cookies
        self.cookies=cookies
        # 传入url
        self.url=url
        # print(urlparse(self.url).scheme+"//"+urlparse(self.url).netloc)
        # 手动设置cookies在主域名刷新，解决淘宝直接在detail页面设置cookie需要滑块认证
        if sourceUrl=="":
            self.browser.get(self.url)
        else:
            self.browser.get(sourceUrl)
            print("触发")
        # 允许使用cookies
        if EnableCookies:
            # 添加cookies
            for cookie in self.cookies:
                self.browser.add_cookie(cookie_dict=cookie)
            # 刷新页面
            self.scrape_refresh()
            
    # 刷新页面
    def scrape_refresh(self):
        self.browser.refresh()
    # 定义一个解析页面的方法
    # condition 页面加载成功判断条件
    # locator 是定位器，通过配置查询条件和参数来获取一个或者多个节点
    # 每次爬取页面至少有一个标签需要验证一次
    def scrape_page(self,condition,locator)->bool:
        logging.info("scraping %s"%self.url)
        try:
            self.browser.get(self.url)
            self.wait.until(condition(locator))
            return True
        except TimeoutException:
            logging.error("error occurred while scraping %s",self.url,exc_info=True)
            return False
    
    def scrape_items_by_css_select(self,selectCss):
        return self.browser.find_elements(By.CSS_SELECTOR,selectCss)
    
    def scrape_item_by_css_select(self,selectCss):
        return self.browser.find_element(By.CSS_SELECTOR,selectCss)
    
    def scrape_items_by_css_name(self,selectCss):
        return self.browser.find_elements(By.CLASS_NAME,selectCss)
    
    def scrape_item_by_css_name(self,selectCss):
        return self.browser.find_element(By.CLASS_NAME,selectCss)
    
    def scrape_items_by_path(self,selectXpath):
        return self.browser.find_elements(By.XPATH,selectXpath)
    
    def scrape_item_by_path(self,selectXpath):
        return self.browser.find_element(By.XPATH,selectXpath)
    
    # 传出浏览器窗口对象，方便外部实现操作
    def get_browser(self):
        return self.browser
    
    def close_browser(self):
        self.browser.close()
    
    def huadong(self):
        spider = self.browser.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
        self.move_to_gap(spider,self.get_track(300))
    
    # 定义一共滑块随机移动步长函数
    # https://blog.csdn.net/qq_39377418/article/details/106954643 
    # https://www.jb51.net/article/261758.htm
    def get_track(self,distance):
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
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(self.browser).release().perform()

if __name__ == '__main__':
    #url_list = ["https://detail.1688.com/offer/550577800329.html", "https://detail.1688.com/offer/683377277181.html", "https://detail.1688.com/offer/684920897688.html", "https://detail.1688.com/offer/643688910607.html"]
    #print((urlparse("https://detail.1688.com/offer/699297425649.html").scheme))
    print("开始")
    count=0

    # 获取存放商品链接地址文件夹的所有文件
    all_files = []
    for root, dirs, files in os.walk("C:\跨境专供链接地址"):
        for file in files:
            if os.path.splitext(file)[1] == '.xls':
                all_files.append(os.path.join(root, file))

    # 提取所有文件中产品链接
    all_links = []
    for file in all_files:
        data_frame_1 = pd.read_excel(file, sheet_name='Sheet1')
        good_links = data_frame_1["产品链接"]
        for link in good_links:
            all_links.append(link)

    for i in range(len(all_links)):
    #for ul in url_list:
        try:
            count=count+1
            obj=ParseLink(url=all_links[i],
                        cookies=[{'domain': '.1688.com', 'expiry': 1695437549, 'httpOnly': False, 'name': 'tfstk', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'cbhGBQjlqAy12edxAcN6aoRp0AeNZC_UXmosTeUGdPlrI-GFiVBFUiIyKkxWbt1..'}, {'domain': '.1688.com', 'expiry': 1680490353, 'httpOnly': False, 'name': 'is_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'buyer'}, {'domain': '.1688.com', 'expiry': 1680490353, 'httpOnly': False, 'name': 'aliwwLastRefresh', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1679885553764'}, {'domain': '.1688.com', 'expiry': 1695437549, 'httpOnly': False, 'name': 'l', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'fBQ0RcqPNEz9sFpBBOfCFurza779jIRYSuPzaNbMi9fP9M7p5CnNW1ijVPR9CnGVFsvyR3o-P8F6BeYBqsVidj4KuQIXdpMmngzr905..'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '__mwb_logon_id__', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'tb059498881'}, {'domain': '.1688.com', 'expiry': 1679957548, 'httpOnly': False, 'name': 'last_mid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b2b-220741495330082be5'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '__cn_logon_id__', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'tb059498881'}, {'domain': '.1688.com', 'expiry': 1679892754, 'httpOnly': False, 'name': '_show_user_unbind_div_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'b2b-220741495330082be5_false'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'unb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2207414953300'}, {'domain': '.1688.com', 'expiry': 1680490292, 'httpOnly': False, 'name': '_m_h5_tk', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '57a4561ff01f3878e2df53f261cfbe2f_1679894495295'}, {'domain': '.1688.com', 'expiry': 1714445548, 'httpOnly': False, 'name': 'ali_apache_track', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'c_mid=b2b-220741495330082be5|c_lid=tb059498881|c_ms=1'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'csg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1084add3'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'sgcookie', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'E100OFusavE%2BiEREFQMece4kTeq8OS6ikMzGA%2FJAnmoOCo4lCknmizuM6JD6l6%2FaxLfc%2FmrMAqVdnl3jyopt0jtS4WZd2U1jVo5AEfohFII6kv8%3D'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'UUphzWMtKnyS0KGk8A%3D%3D'}, {'domain': '.1688.com', 'expiry': 1679892754, 'httpOnly': False, 'name': '_show_force_unbind_div_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'b2b-220741495330082be5_false'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Vqt28cypSWtYAKpxiLTGaHhnR2wNPpQUvCKlwCjFB8k%3D'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'uc4', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'id4=0%40U2grFnyQBWe%2BzdGRiBTguyMvKS%2FS7Ubj&nk4=0%40FY4O7F8GgqcDx1UqdvM2XRmSQRyapQ%3D%3D'}, {'domain': '.1688.com', 'expiry': 1680490352, 'httpOnly': False, 'name': 'firstRefresh', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1679885552938'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'mwb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ng'}, {'domain': '.1688.com', 'expiry': 1714445559, 'httpOnly': False, 'name': 'alicnweb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'touch_tb_at%3D1679885498424%7Clastlogonid%3Dtb059498881'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_csrf_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1679885551222'}, {'domain': '.1688.com', 'expiry': 1679892754, 'httpOnly': False, 'name': '__rn_alert__', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'false'}, {'domain': '.1688.com', 'expiry': 1679892754, 'httpOnly': False, 'name': '_show_sys_unbind_div_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'b2b-220741495330082be5_false'}, {'domain': '.1688.com', 'expiry': 1679892753, 'httpOnly': False, 'name': '_is_show_loginId_change_block_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'b2b-220741495330082be5_false'}, {'domain': '.1688.com', 'expiry': 1714445493, 'httpOnly': False, 'name': 'cna', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 't/KnHGmGjj8CAX1w83riKERc'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '38533eee70fd6'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '__cn_logon__', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'true'}, {'domain': '.1688.com', 'expiry': 1711421548, 'httpOnly': False, 'name': 'lid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb059498881'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '107'}, {'domain': '.1688.com', 'expiry': 1679971892, 'httpOnly': False, 'name': 'xlly_s', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1'}, {'domain': '.1688.com', 'expiry': 1695437553, 'httpOnly': False, 'name': 'isg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'BFlZaAWNWemjfQV97wgg6fEUaEUz5k2YbssyCnsO1gD_gnkUwzMUaPvQgEb0P-XQ'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'ali_apache_tracktmp', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'c_w_signed=Y'}, {'domain': '.1688.com', 'expiry': 1680490292, 'httpOnly': False, 'name': '_m_h5_tk_enc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '4323f41640932f9e358156dee4f00ac8'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 't', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '754e036d3f9104b114697b4fc75f1878'}, {'domain': '.1688.com', 'expiry': 1680490352, 'httpOnly': False, 'name': 'lastRefresh', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1679885552938'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb059498881'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1000d3179c711914f6cd54159a178ee2'}],
                        executablePath=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",
                        sourceUrl="https://www.1688.com/")
            # obj.scrape_page(condition=EC.visibility_of_element_located,locator=(By.XPATH,'//*[@id="hd_0_container_0"]/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/a/div'))
            # 等待买家评价加载完成说明所有的信息都加载完成了
            if obj.scrape_page(condition=EC.visibility_of_element_located,locator=(By.XPATH,'//*[@id="nc_1_n1z"]')):
                obj.huadong()
            # print("滑动成功")

            # time.sleep(600)
            if obj.scrape_page(condition=EC.visibility_of_element_located,locator=(By.XPATH,'//*[@id="10811813010580"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div/div/ul/li[2]/div')):
                print("加载成功")
                # 公司经营年数
                #print(obj.scrape_item_by_path('//*[@id="hd_0_container_0"]/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/a/div').text)
                # 公司名称
                print(obj.scrape_item_by_path('//*[@id="hd_0_container_0"]/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/span').text)
                # 买家评价数
                print(obj.scrape_item_by_path('//*[@id="1081181308831"]/div/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div/span[1]').text)
                # 公司90天成交量                //*[@id="10811813010580"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div/div/ul/li[2]/div
                print(obj.scrape_item_by_path('//*[@id="1081181308831"]/div/div/div[2]/div[1]/div/div[3]/div[1]/div[3]/span[2]').text)
                # 收藏数
                aaa = obj.scrape_item_by_path('//div[@class="no-affix-wrapper"]/div[2]/div[2]/div/div/div[4]/span').text
                aaa = re.sub("\D", "", aaa)
                print(aaa)
            # 关闭窗口
            obj.close_browser()
            print("已爬取详情页的数量是%s"%count)

        except Exception as error:
            print(error)
            print("已爬取详情页的数量是%s"%count)
            continue
    # select 是 css节点
    # obj.scrape_page(condition=EC.visibility_of_element_located,locator=(By.CSS_SELECTOR,'#hd_0_container_0 > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(2) > a > div'))
    # print(obj.scrape_item_by_css_select('#hd_0_container_0 > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(2) > a > div').text)
    #hd_0_container_0 > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(2) > a > div
