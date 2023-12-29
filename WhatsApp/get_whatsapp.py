from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import logging
import random
import phonenumbers
import pandas as pd
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from WhatsApp.chaojiying import Chaojiying_Client
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码


'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='search_google.log', filemode='w')


option = webdriver.ChromeOptions()
#option.add_argument('--headless')
# 关闭开发者模式防止被检测
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option("detach",True)
driver=webdriver.Chrome(executable_path=r"C:\Users\admin\AppData\Local\Programs\Python\Python38\chromedriver.exe",chrome_options=option)
driver.maximize_window()

#定义一个xpath的捕获异常
def xpathExists(xpath):
   try:
      driver.find_element(By.XPATH,xpath)
      return True
   except:
      return False

#超级鹰处理recaptcha验证
def deal_recaptcha():
    # 保存大图
    driver.save_screenshot('main.png')
    img = driver.find_element(By.ID, 'login_img_checkcode')
    img_location = img.location
    img_size = img.size

    # 使用pillow扣除大图中的验证码
    img_points = (
        int(img_location['x']),
        int(img_location['y']),
        int(img_location['x'] + img_size['width']),
        int(img_location['y'] + img_size['height']),
    )
    # 打开页面大图
    im = Image.open('./main.png')
    # 剪切验证码图片
    fram = im.crop(img_points)
    # 保存验证码图片
    fram.save('code.png')
    # 打开验证码图片
    code_img = open('code.png', 'rb').read()
    # 调用超级鹰识别
    res = Chaojiying_Client.PostPic(code_img, 1902)
    code = res.get('pic_str')
    print(code)

phone_data=[]

#country_list = [60,63,66,81,84,852,855,880,91,93,95,961,963,965,968,973,975,977,62,65,673,82,850,853,856,886,90,92,94,960,962,964,966,972,974,976,98,7,31,33,350,352,354,356,358,336,338,223,40,4175,44,46,48,30,32,34,351,353,355,357,349,39,396,41,43,45,47,20,213,218,221,223,225,227,229,231,233,235,237,239,240,242,244,247,249,251,253,255,257,260,262,264,266,268,27,297,210,216,220,222,224,226,228,230,232,234,236,238,239,241,243,245,248,250,252,254,256,258,261,263,265,267,269,290,298,1,1808,1809,1907,299,500,502,504,506,509,52,54,56,58,592,594,596,598,501,503,505,507,51,53,55,57,591,593,595,597,61,671,6723,674,677,679,683,685,688,64,6722,6724,676,678,682,684,686]
site = {0:"facebook.com",1:"instagram.com",2:"twitter.com",3:"pinterest.com",4:"Linkedin.com"}
print("====================================================================================")
print("0:facebook.com","1:instagram.com","2:twitter.com","3:pinterest.com","4:Linkedin.com")
print("====================================================================================")
key_word = input("搜索关键词: ")
site_num = int(input("请输入site序号: "))

start=time.time()
country_list = [60,63,66]
for k in country_list:
    driver.get('https://www.google.com/search?q= "%2B{}" {} whatsapp AND site:{}/&num=100&hl=en'.format(k,key_word,site.get(site_num)))


    '''等待元素加载，且如果出现recaptcha人机验证，在等待时间内处理掉'''
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "before-appbar")))
    # page = driver.page_source
    # print(page)
    try:
        if xpathExists('//*[@id="botstuff"]/div/div[2]/table/tbody/tr/td'):
            page_num = driver.find_element(By.XPATH, '//*[@id="botstuff"]/div/div[2]/table/tbody/tr/td[last()-1]').text
            for page in range(int(page_num)):
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "before-appbar")))
                # 向下滚动
                count = 1000
                for i in range(25):
                    driver.execute_script("document.documentElement.scrollTop={}".format(count))
                    time.sleep(random.randint(1, 2))
                    count += 1000

                num = 1
                n=0
                '''xpath从2开始到100，搜索链接的"num=100"不要做修改，超过100之后xpath规则改变了
                这里只做翻页处理，虽然发现有些不能翻页，但是可以点击加载更多，但是xpath规则会随着加载后变动，以后再做处理'''
                for i in range(100):
                    num+=1
                    if num<=100:
                        try:
                            get_info = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[{}]/div/div/div[2]/div'.format(num)).text
                            match = phonenumbers.PhoneNumberMatcher(get_info, "")
                            m = list(match)
                            for phone in m:
                                phone_data.append(phone.raw_string.replace('(','').replace(')',''))
                                # 这里虽然做了异常处理，但print还是会引发Logging error，但对结果来说没有影响，估计是get_info没有电话号码
                                print(phone.raw_string.replace('(','').replace(')',''))
                            n+=1
                        except Exception as error:
                            logging.error("错误是%s" % error)
                    else:
                        break
                try:
                    driver.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]').click()
                except:
                    continue
        else:
            # 向下滚动
            count = 1000
            for i in range(25):
                driver.execute_script("document.documentElement.scrollTop={}".format(count))
                time.sleep(random.randint(1, 2))
                count += 1000

            num = 1
            n = 0
            '''xpath从2开始到100，搜索链接的"num=100"不要做修改，超过100之后xpath规则改变了
            这里只做翻页处理，虽然发现有些不能翻页，但是可以点击加载更多，但是xpath规则会随着加载后变动，以后再做处理'''
            for i in range(100):
                num += 1
                if num <= 100:
                    try:
                        get_info = driver.find_element(By.XPATH,'/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[{}]/div/div/div[2]/div'.format(num)).text
                        match = phonenumbers.PhoneNumberMatcher(get_info, "")
                        m = list(match)
                        for phone in m:
                            phone_data.append(phone.raw_string.replace('(', '').replace(')', ''))
                            # 这里虽然做了异常处理，但print还是会引发Logging error，但对结果来说没有影响，估计是get_info没有电话号码
                            print(phone.raw_string.replace('(', '').replace(')', ''))
                        n += 1
                    except Exception as error:
                        logging.error("错误是%s" % error)
    except Exception as error:
        print(error)
        logging.error("错误是%s" % error)
        # 如果出现人机验证 等待元素出现执行下一步
        #WebDriverWait(driver, 1000, poll_frequency=35, ignored_exceptions=None)

    logging.info("爬取结束的国家区号是%s,当前页共爬取了%s条WhatsApp" %(str(k),str(n)))
    print("============================================")
    print(k,n)
    print("============================================")

# 列表去重
all_whatsapp = sorted(list(set(phone_data)), key=phone_data.index)

'''
验证电话号码是否符合标准
如国内是+86 11位数字组成
并不能验证该电话号码能否正常使用
'''
for real in all_whatsapp:
    if phonenumbers.is_possible_number(phonenumbers.parse(real, None)):
        pass
    else:
        all_whatsapp.remove(real)


driver.quit()
end=time.time()
logging.info("总计耗时%s" %(end-start))
df = pd.DataFrame({"WhatsApp":all_whatsapp})  # 列表处理后DataFrame还是使用处理之前的，因此这里手动添加
df.to_excel('./{}.xlsx'.format(key_word))
