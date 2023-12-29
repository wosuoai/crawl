"""
去重复做了个简单的店铺
"""

from taobao_item_img import TaobaoItemImg # 导入淘宝详情页图片提取类
import requests
import random
import lxml
import json
import lxml.etree
import time
from urllib.request import quote, unquote
from urllib.parse import urlparse
import redis
import hashlib
import re
import datetime
from setting import cookiesPoolUrl

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

class DP:
    def __init__(self,host,port,password) -> None:
        self.redisClient = MyRedis(host,password,port,db=6)
        self.enableCookiesPool=True

    # 基于url的md5实现url去重
    def is_url_exist(self,url:str):
        urlMd5Str = hashlib.md5(url.encode()).hexdigest()
        if self.redisClient.str_get(urlMd5Str):
            return True
        self.redisClient.str_set(urlMd5Str,1)
        return False

    # 从cookies池中取cookies
    def get_cookiesList_from_cookiesPool(self,appName:str="taobao")->dict:
        cookies={}
        if self.enableCookiesPool:
            while cookies=={}:
                try:
                    cookies=requests.get(url=f"{cookiesPoolUrl}/{appName}/cookies",timeout=15).json()
                except Exception as error:
                    print(f"请求cookies错误是{error}")
                time.sleep(3)
            return cookies

    # 从店铺全部商品页中提取每页的item
    def get_itemUrl_from_dp(self,responseText:str)->list:
        itemUrlList=[]
        selector = lxml.etree.HTML(responseText)

        urlList=[]
        try:
            urlList = set(selector.xpath('//a/@href'))
        except Exception as error:
            print("从店铺全部商品页中提取每页的item错误,错误原因是{}".format(error))

        for url in urlList:
            url=str(url).replace("\\","")
            if 'item.taobao.com' in url:
                # 怀疑spm和风控有关所以随机拼了一个spm
                if eval(url).startswith("//"):
                    itemUrlList.append("https:"+eval(url)+"&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
                    continue
                itemUrlList.append(eval(url)+"spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
        return itemUrlList

    # 获取店铺全部商品页的最大页码
    def get_max_goods_page_from_dp(self,responseText:str)->int:
        responseText=responseText.replace("\n","").replace(" ","").replace("\\","")
        pattern= r'(?<=<spanclass="page-info">)\d+/\d+(?=</span>)'
        result = re.findall(pattern, responseText)
        if len(result)>0:
            return int(str(result[0]).split("/")[1])

        # 如果获取不到就返回1
        return 1

    # 获取店铺搜索页的最大页面
    def get_max_shop_page_from_dp(self):
        return 100

    # 生成asynSearch.htm网页的headers
    def set_shop_item_search_headers(self,shopUrl:str)->dict:
        headers = {
            'authority': '{}'.format(urlparse(shopUrl).netloc),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://{}/category.htm?spm=a1z10.5-c-s.w4010-23122658377.2.4bf9329cQyz293&search=y'.format(urlparse(shopUrl).netloc),
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        return headers

    # 请求asynSearch.htm网页的所有内容
    def get_shop_item_search_text(self,headers:dict,requestUrl:str,cookiesList:list)->str:
        # 如果cookies为空就使用cookies池
        if cookiesList==[]:
            cookiesList=[self.get_cookiesList_from_cookiesPool()]
        try:
            return requests.get(url=requestUrl,headers=headers,cookies=random.choice(cookiesList)).text
        except Exception as error:
            print("请求asynSearch.htm网页的所有内容失败,失败的原因是{}".format(error))
            return ""

    # 提取店铺相关url
    def pattern_shop_list_information(self,responseText:str,cookiesList:list)->list:
        # 如果cookies为空就使用cookies池
        if cookiesList==[]:
            cookiesList=self.cookiesList
        shopInformationList = []
        try:
            pattern = r"g_page_config = {(.*?)};"
            result = re.search(pattern, responseText, re.S)
            if result:
                dictionaryText = result.group(1)
                jsonText = "{" + dictionaryText + "}"
                jsonData = json.loads(jsonText)["mods"]["shoplist"]["data"]["shopItems"]
                for itemShopInformation in jsonData:
                    itemShopUrl = "https:"+itemShopInformation["shopUrl"]
                    # 基于itemShopUrl实现店铺全部商品页面去重
                    # if self.is_url_exist(itemShopUrl)==True:
                    #     print("店铺url已经爬取过,对url进行跳过")
                    #     continue
                    # 提取asynSearch.htm链接
                    shopSearchUrl = itemShopUrl+'/search.htm?spm=a1z10.3-c-s.w4002-22856179752.1.504449ddtvXPWj&search=y' # 拼接一个searchUrl
                    shopSearchHeaders=self.set_shop_item_search_headers(shopSearchUrl)
                    shopSearchText=""
                    try:
                        shopSearchText = requests.get(url=shopSearchUrl,headers=shopSearchHeaders,cookies=random.choice(cookiesList)).text
                    except Exception as error:
                        print("提取asynSearch.htm链接失败,失败原因是{}".format(error))

                    shopSearchLink=""
                    result1 = re.findall('value="([^"]+)"', shopSearchText)
                    if result1:
                        shopSearchLink = result1[-1]
                    if shopSearchLink=="":
                        print("提取店铺全部商品链接后部分链接失败,失败的店铺链接是{}".format(shopSearchUrl))
                    shopInformationList.append({
                        itemShopInformation["title"]: itemShopUrl+shopSearchLink+"&pageNo=1"
                    })
                    print("-------提取店铺全部商品url链接等待中,提取的链接是{}------".format(itemShopUrl))
                    time.sleep(random.randint(20,30)) # 请求随机延迟
            return shopInformationList
        except Exception as error:
            print("提取店铺相关url失败,错误是 {}".format(error))
            return shopInformationList

    # 根据店铺的shopUrl提取店铺所有商品的图片
    # 例子 https://shop306580388.taobao.com/?spm=a230r.7195193.1997079397.452.770c6831luUGSc
    #  https://shop306580388.taobao.com
    def search_shop_item(self,shopUrl:str,cookiesList:list,shopName)->list:
        # 如果cookies为空就使用cookies池
        if cookiesList==[]:
            cookiesList=[self.get_cookiesList_from_cookiesPool()]

        shopInformationList=[]
        itemShopUrl = shopUrl

        # 提取asynSearch.htm链接
        shopSearchUrl = itemShopUrl+'search.htm?spm=a1z10.1-c-s.w5002-23472267900.1.64ad2199w4hGCP&search=y' # 拼接一个searchUrl
        shopSearchHeaders=self.set_shop_item_search_headers(shopSearchUrl)
        shopSearchText=""
        try:
            shopSearchText = requests.get(url=shopSearchUrl,headers=shopSearchHeaders,cookies=random.choice(cookiesList)).text
        except Exception as error:
            print("提取asynSearch.htm链接失败,失败原因是{}".format(error))

        shopSearchLink=""
        result1 = re.findall('value="([^"]+)"', shopSearchText)
        if result1:
            shopSearchLink = result1[-1]
        if shopSearchLink=="":
            print("提取店铺全部商品链接后部分链接失败,失败的店铺链接是{}".format(shopSearchUrl))
        shopInformationList.append({
           shopName: itemShopUrl+shopSearchLink+"&pageNo=1"
        })
        return shopInformationList

    # 根据商品搜索所有匹配店铺
    def serach_shop_list(self,goodsName:str,page:int,cookiesList:list)->list:
        headers = {
            'authority': 'shopsearch.taobao.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'thw=cn; _uetvid=17f9e27029e711eeb5600b32a025baed; _ga=GA1.2.1168878322.1690178300; _ga_YFVFB9JLVB=GS1.1.1690537650.3.1.1690537823.0.0.0; _ga_JBTWV3NHSY=GS1.1.1690537650.3.1.1690537823.56.0.0; miid=129979361131112765; cna=h0tXHbWjLXACASQYc3J+yrmz; lgc=t-3110751053-1; tracknick=t-3110751053-1; sgcookie=E100T%2BBhrfFpR5PWh%2FAynyHTIB4b1z0M5t5FBGXkhMzgX%2FZqTaMTY1JPTlVxccR5hBxG1MVLtXEqWNy05kWtaKFhJ9rWlrWkNe%2FMXk5jZf0pbkM%3D; uc3=id2=UNGXErL6DPTPew%3D%3D&nk2=F9vlEhVtaAUXKX4c3Mk%3D&vt3=F8dCsGZMnqqhKKeyhQU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; uc4=id4=0%40UgbvDH8R6%2BaCqcdPWfZcUffHXK4Q&nk4=0%40FcEKYMKi8FTUUKLwv4FV6FiCmtaIumyj5Q%3D%3D; _cc_=URm48syIZQ%3D%3D; mt=ci=-1_0; lLtC1_=1; _samesite_flag_=true; cookie2=1bed9df7aac5c15c1812a7378427c11c; t=c2c73e06766f7836a8138c3ce2f0134c; _tb_token_=fe7e1593516b8; _m_h5_tk=3d721adf74a266560abe25ab43b491c5_1692852732277; _m_h5_tk_enc=d5aa7f2443f8b7e99a768941c02d3682; xlly_s=1; v=0; uc1=cookie14=Uoe9b6GjxMxrVQ%3D%3D; JSESSIONID=0514358691364A541CD0AAC892FBCB50; isg=BDg4U17MqH1oYcTX7pq0_a86CebKoZwrZgt-BHKp8nMmjdl3GrPIu6PsQYU93VQD; l=fBTeheEqNfLFpsMYBOfwnurza77tHIRfguPzaNbMi9fPObfe5_ahW1trDATwCnGVEsKBR3-WjmOpBRYtsyUB7xv9-egxnLBEldLnwpzHU; tfstk=dzZJfBtbjsfu343LAYQc8neQWEXciuezH7y6xXckRSFYd7Got3iIliMZBvOQdXmL9WFKZ21rqkFx4o4kxbfrvJNiv1fGjG2zU4oCs1vQcAKyiDLZ-oJuU8oEAKACSrwrpCKMXGMpZ1INPHq3xY_Ev0ySBn9IN4h_HN-BvY-iPfNiMH1_DOoLjlHwbCctKU6AHe8EPx5tN9u5.',
            'referer': 'https://shopsearch.taobao.com/search?q=SimpleRetro+%E5%AE%98%E6%96%B9%E5%BA%97&js=1&initiative_id=staobaoz_20230824&ie=utf8',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        # 如果没有传入cookies就使用cookies池
        if cookiesList==[]:
            cookiesList=self.cookiesList

        requestUrl = self.name_quote(goodsName,page)

        responseText=""
        try:
            responseText = requests.get(url=requestUrl,cookies=random.choice(cookiesList),headers=headers).text # 返回搜索到的每页店铺列表
        except Exception as error:
            print("根据商品搜索所有匹配店铺出现错误,错误是{}".format(error))

        return self.pattern_shop_list_information(responseText,cookiesList=cookiesList) # 获取店铺列表

    # 搜索名称编码为新的url
    def name_quote(self,goodsName:str,page:int):
        # currentDate = datetime.datetime.now().strftime('%Y%m%d')
        initiative_id="staobaoz_20120515"
        # 编码名称
        return "https://shopsearch.taobao.com/search?q={}&initiative_id={}&s={}".format(quote(goodsName,encoding="gbk"),initiative_id,page*19)
        # return "https://shopsearch.taobao.com/search?q={}&js=1&initiative_id=staobaoz_{}&ie=utf8&s={}".format(quote(goodsName,encoding="utf8"),currentDate,page*19)

if __name__ == '__main__':
    pass
    # cookiesList=[{'uc1': 'pas=0&cookie14=Uoe9bfwIyfvD4w%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C', 'l': 'fB_vR164NC-3uLSbBO5Cnurza77OVIRb8sPzaNbMiIEGa14f9FsWHNC18tdJWdtjgT5cNetrip0J_dFX-laLRKNEXRN6dL4w9Ip68eM3N7AN.', 'tfstk': 'cIyPBQv1wTBPJMrdWxDU057TPMkRanhn_KoKZZ-XUapOcHho7sVDJmXL3mo90ecl.', 'dnk': 'tb80111606', 'cancelledSubSites': 'empty', 'cookie1': 'U%2BGWz3AsFiX%2BQb4KVw17j51DAUP9jxfiN9Dd%2FomAUJ8%3D', '_l_g_': 'Ug%3D%3D', '_nk_': 'tb80111606', 'existShop': 'MTY5MDE4NTI2Mg%3D%3D', 'csg': 'dcc5f4fe', 'uc3': 'lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dCsGGr97iqzZWVKK0%3D&id2=UNQyQxMqUdx1nQ%3D%3D&nk2=F5RNZTse5XZpwA%3D%3D', 'unb': '3451510054', 'cna': 'Nf9EHZfSwxoCAW8CWybl9Yqd', 'tracknick': 'tb80111606', 'cookie2': '11561734f07d830a0352f8a51044481e', 'uc4': 'id4=0%40UgP5GPE5h%2FvopPV87sjzIkKwKLBr&nk4=0%40FY4GsvRHfRNKE%2BdeKAjFMKHKIoLM', '_tb_token_': '77bde33180b3f', '_samesite_flag_': 'true', 'isg': 'BJiYNjZvSMUgnGRBk0wfVQ9_acYqgfwLIDnzJtKJVVOGbTlXepDymyFPoaXd_bTj', 'skt': 'a50b5a664603ab51', 'sgcookie': 'E100Ee%2FMymHS2ljzrJ%2FpCZ7eN8WEYDGKjJPxVqJIuexRsu5asq6oRX%2FTgh3%2BfMRd34j%2Fy1B7jVbWR506PQ%2BvYnrHYAOu2hzlMsI2xtmxKqGac%2Bbl9toKemB3DMhtbmZACIrf', 'lgc': 'tb80111606', 'sg': '641', '_cc_': 'WqG3DMC9EA%3D%3D', 'cookie17': 'UNQyQxMqUdx1nQ%3D%3D', 'xlly_s': '1', 't': 'a170703abdc55c9694b8dcc5bd3a0e4a'}]
    # # 创建一个店铺对象
    # dp=DP(host="127.0.0.1",password="")

    # # 先提取某个搜索页的店铺 第一页
    # # 传入cookiesList
    # # shopList = dp.serach_shop_list("女装",2,cookiesList=cookiesList)  # 根据搜索页获取所有店铺
    # shopList = dp.search_shop_item("https://shop306580388.taobao.com",cookiesList,"店铺的名字") # 获取一个唯一的店铺

    # for shopItem in shopList:
    #     # 提取店铺的名称和店铺全部商品页html
    #     for shopName in shopItem:
    #         shopUrl = shopItem[shopName]
    #         print("店铺全部商品页的url是{}".format(shopUrl))
    #         asynSearchMaxPage=1 # 获取店铺全部商品页最大页码
    #         page=1
    #         # 进行店铺全部商品页的循环
    #         while page<=asynSearchMaxPage:
    #             shopUrl = shopUrl.split("pageNo")[0]+"pageNo={}".format(page)
    #             asynSearchHeaders=dp.set_shop_item_search_headers(shopUrl) # 获取请求asynSearch.htm页面的headers

    #             # 传入cookiesList
    #             asynSearchText=dp.get_shop_item_search_text(asynSearchHeaders,shopUrl,cookiesList=cookiesList)

    #             asynSearchMaxPage=dp.get_max_goods_page_from_dp(asynSearchText) # 更新全部商品页html最大页码
    #             page=page+1

    #             # 进行店铺全部商品页的每个商品提取
    #             itemUrlList = dp.get_itemUrl_from_dp(asynSearchText)
    #             for itemUrl in itemUrlList:
    #                 taobaoItemImg=TaobaoItemImg() # 创建一个item爬取对象

    #                 # 传入cookiesList
    #                 result = taobaoItemImg.get_item_imgs(cookiesList=cookiesList,requestUrl=itemUrl)

    #                 skuImgList = result["skuImgList"] # sku图片列表
    #                 lbImgList = result["lbImgList"] # 轮播图列表
    #                 detailImgList = result["detailImgList"] # 详情图列表
    #                 title= result["title"] # 店铺的名字
    #                 taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/sku",skuImgList)
    #                 taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/lb",lbImgList)
    #                 taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/detail",detailImgList)
    #                 print("------------提取item详情页等待中------------")
    #                 time.sleep(random.randint(30,60))

    #         time.sleep(random.randint(10,30)) # itemUrlList为空防止频繁使用cookies请求









    # with open("search.html","r") as f:
    #     pass
    #     print(dp.pattern_shop_information(f.read()))

    # print(dp.serach_shop())
    # with open("dp.html","r") as f:
    #     print(dp.get_max_page_from_dp(f.read()))
    # # 从店铺页面里提取item.htm产品url
    # def get_itemUrl_from_dp(responseText:str)->list:
    #     itemUrlList=[]
    #     selector = lxml.etree.HTML(responseText)
    #     urlList = set(selector.xpath('//a/@href'))
    #     for url in urlList:
    #         url=str(url).replace("\\","")
    #         if 'item.taobao.com' in url:
    #             # 怀疑spm和风控有关所以随机拼了一个spm
    #             if eval(url).startswith("//"):
    #                 itemUrlList.append("https:"+eval(url)+"&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
    #                 continue
    #             itemUrlList.append(eval(url)+"spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu")
    #     return itemUrlList



    # 根据店铺爬取url爬取(店铺url提取规则摆烂了)
    # 类都不想写了。。。。
    # name=input("请输入需要保存的店铺名字: ")
    # for i in range(1):
    #     cookies=random.choice(cookiesList)
    #     dpUrl="https://shop225848760.taobao.com/i/asynSearch.htm?_ksTS=1690033079036_285&callback=jsonp286&input_charset=gbk&mid=w-23122658373-0&wid=23122658373&path=/category.htm&spm=a1z10.3-c-s.w4002-23122658373.66.787a658d4Ys1Sy&input_charset=gbk&search=y&pageNo={}".format(i)
    #     # 不同店铺headers的authority值和referer值需要修改
    #     headers = {
    #         'authority': 'shop225848760.taobao.com',
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #         'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    #         'cache-control': 'no-cache',
    #         # 'cookie': '_uetvid=9da4f4d0249311eea044195e64d33b67; _ga_JBTWV3NHSY=GS1.1.1689592698.1.1.1689592747.11.0.0; _ga=GA1.2.208439145.1689592688; _ga_YFVFB9JLVB=GS1.1.1689592688.1.1.1689592747.0.0.0; thw=cn; cna=su2QHDAXHR4BASQJiijj0y+z; lgc=tb80111606; tracknick=tb80111606; mt=ci=-1_0; xlly_s=1; t=4e400d43fbdf02c4e5bb6812c6d18547; sgcookie=E100Kh2ecfBhEfYAZCBNf24clCvW0bVFNlQeWYa0%2FwMHFlebBtGZxb265UH3tOXai5vi9fOPbD%2Fnm2z4Zr5akc13bVdkM0dNqX7KrGrPjFvpxuKRfRwMLpTHzwYupZSQk27u; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dCsGGp77F2o5L8jF0%3D&nk2=F5RNZTse5XZpwA%3D%3D&id2=UNQyQxMqUdx1nQ%3D%3D; uc4=id4=0%40UgP5GPE5h%2FvopPV87sjzI3bYxkOy&nk4=0%40FY4GsvRHfRNKE%2BdeKAjFMdIApg%2BY; _cc_=V32FPkk%2Fhw%3D%3D; cookie2=1c60aec452b901be98fbfa4f5030b792; _tb_token_=e7335eb393b53; _m_h5_tk=9fa1146a56b5ea3b51273b0ea5797318_1690032219148; _m_h5_tk_enc=fa28bfe55312c1d2c58a954cf03c6a57; uc1=cookie14=Uoe9bf26APEbgA%3D%3D; pnm_cku822=098%23E1hvJpvUvbZvUvCkvvvvvjiWnLsvsjiWnLFWzjthPmPhsj3WnLdwsjDPRLFpsjY8i9hvCvvvpZpRvpvhvv2MMQvCvvOv9hCvvvmgvpvIvvCvpPMMvPQvvh8YvvvCOpvvByOvvUhQvvCVB9vv9BQvvhnnvvmC5T9Cvv9vvhjUYNOBHU9CvvwCvhnm1Wo4mvhvLvmdjB6a%2Bb8rVX9aUhzBRfpz%2B0gUAf00ILoQW5VYyfUZ%2BulABz7yHd8rejOdYE7reCKK4QtrAEkKHdBYBnFZeBOqrADn9Wma%2BfmtEpZgvpvhvvCvpv%3D%3D; tfstk=cHcOBJ0NuHxMfVK0T5pHgjTI_4YlZH_TmNZAMfaXZxfhckfAitcow5IkCrrzXeC..; l=fBElX6hPT7nkkiT2BOfwPurza77OSIRAguPzaNbMi9fPOI5H5idlW1_gA-TMC3GVFsCvR38PiVPBBeYBqoxJa5wv9w8mWVHmnmOk-Wf..; isg=BJubrHFle5lPaIA8TIIc1HkhKv8FcK9yIvFqDI3YdxqxbLtOFUA_wrluAsxizAdq',
    #         'pragma': 'no-cache',
    #         'referer': 'https://shop225848760.taobao.com/category.htm?spm=a1z10.5-c-s.w4010-23122658377.2.4bf9329cQyz293&search=y',
    #         'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"Windows"',
    #         'sec-fetch-dest': 'document',
    #         'sec-fetch-mode': 'navigate',
    #         'sec-fetch-site': 'same-origin',
    #         'sec-fetch-user': '?1',
    #         'upgrade-insecure-requests': '1',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    #     }
    #     htmlText=requests.get(url=dpUrl,headers=headers,cookies=cookies).text
    #     print("{}店铺第{}页获取所有详情页成功".format(name,i+1))
    #     time.sleep(random.randint(20,40))
    #     itemUrlList =get_itemUrl_from_dp(htmlText)
    #     print(itemUrlList)
        # for itemUrl in itemUrlList:
        #     # 调用 TaobaoItemImg 进行爬取item并保存图片
        #     taobaoItemImg=TaobaoItemImg() # 创建一个item爬取对象
        #     cookies1=random.choice(cookiesList)
        #     cookies2=random.choice(cookiesList)
        #     result = taobaoItemImg.get_item_imgs(cookies1=cookies1,cookies2=cookies2,requestUrl=itemUrl)
        #     skuImgList = result["skuImgList"]
        #     lbImgList = result["lbImgList"]
        #     detailImgList = result["detailImgList"]
        #     taobaoItemImg.write_imgList_to_dir(name+"/sku",skuImgList)
        #     taobaoItemImg.write_imgList_to_dir(name+"/lb",lbImgList)
        #     taobaoItemImg.write_imgList_to_dir(name+"/detail",detailImgList)
        #     time.sleep(random.randint(30,60))







