from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib import parse
from selenium.webdriver.chrome.service import Service as ChromeService
import random
import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
driverPath = ChromeDriverManager().install()
# from setting import CHROME_CONFIG
import sys
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cookies_pool_tmall.log')
    ]
)
"""
防止被检测js https://gitcode.net/mirrors/requireCool/stealth.min.js?utm_source=csdn_github_accelerator
user_accounts_data 要设置管理员权限,不只是能读权限
突破selenium淘宝 https://blog.51cto.com/csnd/5983926
"""

shieldJsText = requests.get("https://gitcode.net/mirrors/requireCool/stealth.min.js/-/raw/main/stealth.min.js?inline=false").text

class BaseLogin:
    def __init__(self) -> None:
        global driverPath
        self.options = webdriver.ChromeOptions() # 实列化option
        self.options.add_argument('--no-sandbox') # 允许root模式允许google浏览器
        # self.options.add_argument('--incognito') # 开启无痕模式
        self.options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging']) # 设置开发者模式启动，该模式下webdriver属性为正常值
        # self.options.add_argument('--disable-web-security') # 关闭浏览器安全认证
        self.options.add_argument('--disable-blink-features=AutomationControlled') # 屏蔽检测
        # self.options.add_argument("--remote-debugging-port=9222")
        # self.options.add_experimental_option("remoteDebuggingPort","9222")
        # self.options.add_argument("C:\\Users\\15256\\Desktop\\nowTime\\sxhCrawler\\商城\\淘宝国内商城\\taobao\\taobao_cookies_pool\\taobao_login\\user_accounts_data\\{}".format(userData))  # 指定一个 Chrome 用户配置文件目录
        # self.options.add_argument("--profile-directory=Default")
        # self.options.binary_location=CHROME_CONFIG["chromePath"] # 配置谷歌浏览器路径
        service = ChromeService(executable_path=driverPath) # 配置谷歌操作驱动路径
        
        self.driver = webdriver.Chrome(options=self.options,service=service) # 初始化操作对象
        
        self.wait=WebDriverWait(self.driver,1) # 定义一个wait对象
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': shieldJsText})  # 屏蔽selenim参数
        
    def login(self,username:str,password:str)->dict:
        raise NotImplementedError
            
class TMLogin(BaseLogin):
    def __init__(self) -> None:
        super().__init__()
        
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
            ActionChains(self.driver).move_to_element_with_offset()
            time.sleep(1)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(self.driver).release().perform()
    
    # 生成滑动距离列表
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
    
    # 检测页面标签是否存在  
    def detection_element(self,condition,locator)->bool:
        logging.info("detection element ")
        try:
            self.wait.until(condition(locator))
            return True
        except TimeoutException:
            logging.error("error find element",exc_info=True)
            return False
    
    def login(self,username:str,password:str)->dict:
        print("登陆代码")
        self.driver.get(url="https://login.tmall.com/")
        self.driver.switch_to.frame("J_loginIframe")  # 登录框在iframe里，打开页面后，需要切换到iframe
        time.sleep(random.randint(3,5)) # 等待3-5秒
        name_input_element = self.driver.find_element(By.ID,'fm-login-id')
        name_input_element.clear()
        # 延迟输入用户名
        for s in username:
            name_input_element.send_keys(s)
            time.sleep(random.randint(1,4)*0.1)
        # 延迟输入密码
        password_input_element = self.driver.find_element(By.ID,'fm-login-password')
        password_input_element.clear()
        for s in password:
            password_input_element.send_keys(s)
            time.sleep(random.randint(1,4)*0.1)
            
        # 进行是否要滑动滑块判断
        if self.detection_element(condition=EC.visibility_of_element_located,locator=(By.XPATH, '//*[@id="nc_1_n1z"]')):
            slider=self.driver.find_element(By.XPATH,'//*[@id="nc_1_n1z"]')
            self.move_to_gap(slider,self.get_track(300))
            time.sleep(1)
            
        # 再点击按钮前做个随机延迟
        time.sleep(random.randint(5,15)*0.1)

        # 点击登陆按钮
        # //*[@id="login-form"]/div[4]/button
        button=self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button')
        button.click()
        time.sleep(3)
        cookies={}
        for cookieDict in self.driver.get_cookies():
            cookies[cookieDict["name"]]=cookieDict["value"]

        self.driver.close()
        return cookies
if __name__ == "__main__":
    tmLogin=TMLogin()
    tmLogin.login()
    


# # 添加UA
# options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# # 指定浏览器分辨率
# options.add_argument('window-size=1920x3000') 

# # 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--disable-gpu') 

#  # 隐藏滚动条, 应对一些特殊页面
# options.add_argument('--hide-scrollbars')

# # 不加载图片, 提升速度
# options.add_argument('blink-settings=imagesEnabled=false') 

# # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# options.add_argument('--headless') 

# # 以最高权限运行
# options.add_argument('--no-sandbox')

# # 手动指定使用的浏览器位置
# options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" 

# #添加crx插件
# option.add_extension('d:\crx\AdBlock_v2.17.crx') 

# # 禁用JavaScript
# option.add_argument("--disable-javascript") 

# # 设置开发者模式启动，该模式下webdriver属性为正常值
# options.add_experimental_option('excludeSwitches', ['enable-automation']) 

# # 禁用浏览器弹窗
# prefs = {  
#     'profile.default_content_setting_values' :  {  
#         'notifications' : 2  
#      }  
# }  
# options.add_experimental_option('prefs',prefs)


# driver=webdriver.Chrome(chrome_options=chrome_options)

'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
#                     datefmt='%a %d %b %Y %H:%M:%S', filename='1688spider.log', filemode='w')

# option = webdriver.ChromeOptions()
# 无头模式
# option.add_argument('--headless')
# 允许root模式允许google浏览器
# option.add_argument('--no-sandbox')
# option.add_argument('--headless')
# option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# 打开无痕浏览模式
# option.add_argument("--incognito")
# 关闭开发者模式
# option.add_argument('--disable-blink-features=AutomationControlled')
# option.add_argument("--user-data-dir=C:/Users/15256/AppData/Local/Google/Chrome/User Data")  # 指定一个 Chrome 用户配置文件目录
# option.add_argument("--profile-directory=Default")
# driver = webdriver.Chrome(
#     options=option)

# driver.get("https://login.taobao.com/member/login.jhtml")
# # driver.get("https://login.taobao.com/?spm=pc_detail.27183998.0.0.7f727dd6r9HYlM&redirectURL=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fid%3D685066395791%26pvid%3Db1545104-22bc-456f-b81e-44c4bae077fc%26scm%3D1007.40986.276750.0%26spm%3Da21bo.jianhua.201876.1.3e562a89zYxY7Y")
# time.sleep(30)
# # print(driver.get_cookies())
# with open("taobao_cookies.json","w",encoding="utf-8") as f:
#     f.write(str(driver.get_cookies()))


