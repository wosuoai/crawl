import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import warnings
import urllib3
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


option = uc.ChromeOptions()
# 允许root模式允许google浏览器
option.add_argument('--no-sandbox')
option.add_argument('--disable-gpu')
option.add_argument("--incognito")  # 开启隐身模式
# 屏蔽保存密码提示框
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
option.add_experimental_option('prefs', prefs)
# 关闭webrtc 避免找到真实IP地址
preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
option.add_experimental_option("prefs", preferences)
# 关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")
driver = uc.Chrome(option=option,version_main=119)

time.sleep(random.randint(3, 7))
driver.get(url="https://login.tmall.com/")
driver.switch_to.frame("J_loginIframe") #登录框在iframe里，打开页面后，需要切换到iframe

time.sleep(5)
name_input_element = driver.find_element(By.ID,'fm-login-id')
time.sleep(1)
name_input_element.clear()
account = ""
for s in account:
    name_input_element.send_keys(s)
    time.sleep(random.randint(1, 4) * 0.1)

time.sleep(2)
password_input_element = driver.find_element(By.ID,'fm-login-password')
time.sleep(1)
password_input_element.clear()
password = ""
for s in password:
    password_input_element.send_keys(s)
    time.sleep(random.randint(1, 4) * 0.1)

time.sleep(10)

# 点击登陆按钮
button = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button')
button.click()
time.sleep(15)

driver.get("https://detail.tmall.com/item.htm?abbucket=20&id=716249068289&ns=1")
WebDriverWait(driver, 60, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/h1')))
driver.implicitly_wait(10)

cookies = {}
for cookieDict in driver.get_cookies():
    cookies[cookieDict["name"]] = cookieDict["value"]

print(cookies)
with open("tmallCookies.json", "a") as f:
    f.write(str(cookies) + '\n')
driver.close()

