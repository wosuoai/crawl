from cookies_process.cookies_redis import RedisClient
from setting import REDIS_CONFIG,ACCOUNT_MAP
import requests
import logging
import sys
import re
import json
import time
from fake_useragent import UserAgent

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
                                'accept-language': 'zh-CN,zh;q=0.9',
                                'cache-control': 'max-age=0',
                                # 'cookie': 'thw=cn; _uetvid=17f9e27029e711eeb5600b32a025baed; _ga=GA1.2.1168878322.1690178300; _ga_YFVFB9JLVB=GS1.1.1690537650.3.1.1690537823.0.0.0; _ga_JBTWV3NHSY=GS1.1.1690537650.3.1.1690537823.56.0.0; t=2b9286dd549d9887768496a17733007b; lLtC1_=1; xlly_s=1; cna=hS2QHXCurFkCAXPDTAjtBsQO; cookie2=1c420c586b03bdc619a00eaf91899663; _samesite_flag_=true; sgcookie=E100TtNtvJCGWsK2k%2Bd0k%2FJbO8JfIY2eALoLcIHIVlfqljnRSAj0OxiC5kqTDnUXjcZNv0hyJgssJCq%2Bratqm6JdjoWWcakMYV8w8haGWol5AZ4%3D; unb=2206799874005; uc3=id2=UUphzOV4ZmtYf4ZcQA%3D%3D&nk2=F5REP7sBUHYX1vY%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dD3CAUcD%2Fb2BYM98k%3D; csg=93ad6539; lgc=tb117416292; cancelledSubSites=empty; cookie17=UUphzOV4ZmtYf4ZcQA%3D%3D; dnk=tb117416292; skt=bf7c8d01b9de4cc1; existShop=MTY5ODM3Mzc0NA%3D%3D; uc4=id4=0%40U2grF8636cbIDpmfqxXgrXyBkDJ7QOGe&nk4=0%40FY4Pba8SP%2Fxz1We3n%2B84SwqOktztiQ%3D%3D; tracknick=tb117416292; _cc_=U%2BGCWk%2F7og%3D%3D; _l_g_=Ug%3D%3D; sg=258; _nk_=tb117416292; cookie1=BYXLDujz7cMf5qXWf0wpvtl2XoqRpayhoOHj22O2chc%3D; mt=ci=6_1; uc1=cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie14=Uoe9ZYWgozAscQ%3D%3D; v=0; miid=1404226906216772041; _tb_token_=6bf5e83e3f6b; _m_h5_tk=6eb21c08fce3a3297a6a6a0a4f93d45f_1698391709576; _m_h5_tk_enc=7f185db28b5ae5a87a9030cb82aaf16e; tfstk=dEW6EfZg6V06TdOxQRZFRdyxWqpflNwzhmtAqiHZDdpThnQPRIH4sdRXhwLFQFSwB-tAzwOAuESZj6bP2AWasKkXIKvYzzyzUcSMnKHap8yzfbnzfzzzU8PtvKa_z1uTM5XrhxqUS-ILRvDEU_7xg52m3xWBvrYRfU-Hx9t91UdpROWjUU1_RjiBZxtBzkZIij46HYeG.; l=fBTeheEqNfLFpdtCXOfwPurza77tSIRAguPzaNbMi9fP9gCM5mUAW13g5_YHCnGVF6zDR3RpoAReBeYBq3xonxvte5DDwIMmnmOk-Wf..; isg=BCoqiarnO96ShbZBKFCGc0EQe5DMm671ESDbNLTj2n0I58qhnCj-B_wVcxN7FyaN',
                                'referer': 'https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu',
                                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"Windows"',
                                'sec-fetch-dest': 'document',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-site': 'none',
                                'sec-fetch-user': '?1',
                                'upgrade-insecure-requests': '1',
                                #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                                'user-agent': UserAgent().random,
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


#
# headers={
#         'authority': 'item.taobao.com',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'zh-CN,zh;q=0.9',
#         'cache-control': 'max-age=0',
#         # 'cookie': 'thw=cn; _uetvid=17f9e27029e711eeb5600b32a025baed; _ga=GA1.2.1168878322.1690178300; _ga_YFVFB9JLVB=GS1.1.1690537650.3.1.1690537823.0.0.0; _ga_JBTWV3NHSY=GS1.1.1690537650.3.1.1690537823.56.0.0; t=98981d3e4a62b41419b40bc69f134ce2; xlly_s=1; _tb_token_=fe3e5ee7f6b5d; cookie2=22f36ae8cbacaf6f893eceb812204f50; _samesite_flag_=true; cna=TWFvHZYSPU8CAXPE9gvUad+5; sgcookie=E100y1SC%2B10XJiD0Q%2BWsUMiVOilL8DFzuUc0N0a0lCelHgDe6EmkUHDEYxUw3lXFFc5WK4q8gG31XWRvc1A6RZAc%2BUezfmJDNY1uEIpG90TqjKY%3D; unb=2216174043397; uc3=id2=UUpgQEjzHDCO8qJu5A%3D%3D&nk2=F5RGNs1XxWX0fG0hWno%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dCsGZGWjLj7TC98jQ%3D; csg=f1766a1a; lgc=tb307480725849; cancelledSubSites=empty; cookie17=UUpgQEjzHDCO8qJu5A%3D%3D; dnk=tb307480725849; skt=816e68c8a99ed245; existShop=MTY5MzI3NzcwNQ%3D%3D; uc4=id4=0%40U2gqz6fdB8BAmddT2A222ZWLgyIc%2B9TA&nk4=0%40FY4NA1sR8gQBPMyWtH%2BMB28r6lb%2F8VWxeQ%3D%3D; tracknick=tb307480725849; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=97c; _nk_=tb307480725849; cookie1=WvSbIa6wl3AGlpLstYQlbgWvDm8z4axn9U%2FjMCGa9ck%3D; mt=ci=0_1; uc1=cookie14=Uoe9bjCfV16CTg%3D%3D&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=false&cookie21=W5iHLLyFfoaZ&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0; x5sec=7b22617365727665723b32223a223734363934313264303135353930303138616236646661343231653131343735434e65517471634745503767395a33342f2f2f2f2f774561447a49794d5459784e7a51774e444d7a4f5463374d6a43516f6357652b2f2f2f2f2f384251414d3d222c22733b32223a2261636264356637356433386438633931227d; _m_h5_tk=f4f4122fe6c558b5ee6f2053982406aa_1693297907046; _m_h5_tk_enc=70df50763aabf59ec5d7489df6eced30; v=0; tfstk=duGME1jysAy_6ggDm1F6syO7z7ppCGNb0mCYDSE2LkrIWsLsWv4qDDTX5534mmmLAVCv5VHho4inm-T_DormDqk9JQd-5VNbgixJwQKjOSN49TzdLVg_GS7d0LHE5rjp_h6rZZJZ_slBS8Elk-eevexTBuuaYV3tTPj84VrhgsrgSOPdLT7F1saekXWfhRzQ-uEufiVF.; isg=BO3tssZ4daGTcRHoU6EZKhoR_IlnSiEcM3CLWy_yKQTzpg1Y95ox7Dt0lHpAJjnU; l=fBTeheEqNfLFpGNEBOfwPurza77OSIRAguPzaNbMi9fPOd5k5vjGW1tQVK8DC3GVF6P9R3-WjmOpBeYBqI4DXGYme5DDwQHmnmOk-Wf..',
#         'referer': 'https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu',
#         'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#         'user-agent': UserAgent().random,
#     }