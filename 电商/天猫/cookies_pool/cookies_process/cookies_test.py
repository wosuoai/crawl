from cookies_process.cookies_redis import RedisClient
from setting import REDIS_CONFIG,ACCOUNT_MAP
import requests
import logging
import sys
import re
import json
import time
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cookies_pool_tmall.log')
    ]
)
class BaseTest(object):
    def __init__(self,website:str) -> None:
        self.website=website
        self.accountOperator = RedisClient(type="account",website=self.website,host=REDIS_CONFIG["host"],port=REDIS_CONFIG["port"],password=REDIS_CONFIG["password"]) # 账号
        self.credentialOperator = RedisClient(type="credential",website=self.website,host=REDIS_CONFIG["host"],port=REDIS_CONFIG["port"],password=REDIS_CONFIG["password"]) # 凭证
    # 子类必须要写测试方法
    def test(self,username:str,credential:str):
        raise NotImplementedError
    # run 方法
    def run(self):
        credentials=self.credentialOperator.all()
        # print(credentials)
        for username,credintial in credentials.items():
            try:
                self.test(username,credintial)
            except Exception as error:
                logging.error("{}账号测试出现错误,错误是{}".format(username,error))

class TBTest(BaseTest):
    def __init__(self, website: str) -> None:
        super().__init__(website)
    
    # 做个解析测试
    def pattern_lb_response(self,returnText:str)->list:
        auctionImagesList = []
        try:
            pattern = r"var g_config = {(.*?)};"
            result = re.search(pattern, returnText, re.S)
            if result:
                dictionaryText = result.group(1)
                jsonText = "{" + dictionaryText + "}"
                jsonText=jsonText.replace("\n","").replace(" ","")
                auctionImagesRe = re.search(r"auctionImages:(\[.*?\])", jsonText)
                for itemUrl in eval(auctionImagesRe.group(1)):
                    sItemUrl= str(itemUrl)
                    if sItemUrl.startswith("//"):
                        auctionImagesList.append("https:"+sItemUrl)
                        continue
                    auctionImagesList.append(sItemUrl)
            return auctionImagesList
        
        except Exception as error:
            return auctionImagesList
        
    def test(self,username:str,credential:str):
        text = requests.get(url='https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu',
                            headers={
                                'authority': 'item.taobao.com',
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                                'cache-control': 'max-age=0',
                                # 'cookie': 'thw=cn; cna=AbGRHJxN6koCAW8CWyaOFU9H; t=5c0e77b79ca30999a50febac43117b48; lgc=tb80111606; tracknick=tb80111606; _cc_=VT5L2FSpdA%3D%3D; sgcookie=E100w%2Bvajo%2B06VFgv76h5cODFFyv%2Bsyt1j2kmGOG0X%2BR9qk1aujLoXjzlwvaAI21V6eRs4tVN1rGqG5CR9WixyPmLuxrmpvpnggWGtFIP1Xu4y4zhgbjye5CwPmjupe6CyyC; uc3=id2=UNQyQxMqUdx1nQ%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=F5RNZTse5XZpwA%3D%3D&vt3=F8dCsGO7WCQXYRbBmfQ%3D; uc4=nk4=0%40FY4GsvRHfRNKE%2BdeKAlPibDvG5zy&id4=0%40UgP5GPE5h%2FvopPV87slT5h%2Btp8Ez; mt=ci=-1_0; cookie2=1543732a315fefad0f05b7d93ba61d92; _tb_token_=e93eeeb8177fe; xlly_s=1; _m_h5_tk=87b0be7f3547a1f72d92e1ade99f7d42_1689565190413; _m_h5_tk_enc=eb782c9f0f0a7b0250133ffaaf8d1722; uc1=cookie14=Uoe8g0xRHxRTFg%3D%3D; isg=BNzcaDMS1FsWIaAk3F4rQmZ9rfqOVYB_fCW36rbdo0eqAXyL3mVjD1LwZWn5ibjX; l=fBSck9QeNgpDvjnZBOfZPurza77TxIRAguPzaNbMi9fPObCH5RvNW1_-H7TMCnGVFsBJR3lDK4dwBeYBq_C-nxvt5mhSG5kmne_7Qn5..; tfstk=c53FBO_XveLUnNlJHP4r_Bpa7mZdZbhnZNPbxdre5VKymzZhiHB8sU3a_71NEkf..',
                                'referer': 'https://uland.taobao.com/',
                                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"Windows"',
                                'sec-fetch-dest': 'document',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-site': 'same-site',
                                'sec-fetch-user': '?1',
                                'upgrade-insecure-requests': '1',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                            },
                            cookies=json.loads(credential)).text
        res=self.pattern_lb_response(text)
        if res==[]:
            logging.info(f"{username}账号过期了,从存储池中移除cookies")
            self.credentialOperator.delete(username)
        if res!=[]:
            logging.info(f"{username}账号验证是有效的")
            
        time.sleep(30)
        
if __name__ == "__main__":
    bt = BaseTest("taobao")
    bt.run()