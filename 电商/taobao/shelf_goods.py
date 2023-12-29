from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
driver=webdriver.Chrome(executable_path=r"C:\Users\wosuoai\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()


driver.get('https://www.taobao.com')
time.sleep(3)
cookies=[]
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']  # 删除报错的expiry字段
    driver.add_cookie(cookie)
driver.refresh()
driver.implicitly_wait(2)
# if driver.find_element(By.PARTIAL_LINK_TEXT,'亲，请登录'):
#     driver.find_element(By.PARTIAL_LINK_TEXT,'亲，请登录').click()

#点击购物车
if driver.find_element(By.PARTIAL_LINK_TEXT,'购物车'):
    driver.find_element(By.PARTIAL_LINK_TEXT,'购物车').click()

#全选商品
if driver.find_element(By.ID,"J_SelectAll1"):
    driver.find_element(By.ID,"J_SelectAll1").click()
#需要勾选的商品
# if driver.find_element(By.ID,'J_CheckBox_4955335596583'):
#     driver.find_element(By.ID,'J_CheckBox_4955335596583').click()

time.sleep(5)
def buy(buy_time):  # buy_time 购买时间
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('当前时间:%s' % now)
        now=datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

        # 判断是否到达抢购时间
        if now > buy_time:
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT,'结 算').click()
            except:
                pass

        # 对比时间，循环提交订单
        while True:
            try:
                if driver.find_element(By.LINK_TEXT,'提交订单'):
                    driver.find_element(By.LINK_TEXT,'提交订单').click()
                    print(f"抢购成功，请尽快付款")
            except:
                print(f"再次尝试提交订单")
        time.sleep(0.01)

if __name__ == '__main__':
    shelf_time="2023-05-25 20:00:00"
    buy(datetime.strptime(shelf_time,'%Y-%m-%d %H:%M:%S'))
