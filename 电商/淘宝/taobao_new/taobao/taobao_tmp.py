from taobao_dp import DP
import time
from taobao_item_img import TaobaoItemImg
import random
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
from setting import redisHost, redisPort, redisPassword
import hashlib
import pymysql


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="wosuoai8279",
    database="item_imgs"
)
cursor = conn.cursor()

def item_main(shopUrl: str, shopName: str, cookiesList: list = []):
    # 创建对象
    dp = DP(host=redisHost, port=redisPort, password=redisPassword)  # 创建一个店铺对象
    taobaoItemImg = TaobaoItemImg()  # 创建一个item爬取对象

    # 进行是否使用ip代理池和cookies池配置
    taobaoItemImg.enableIpProxy = False  # 图片下载不使用ip代理池
    dp.enableCookiesPool = True  # 获取店铺是否使用cookies池
    taobaoItemImg.enableCookiesPool = True  # 获取详情页图片是否使用cookies池

    # 先提取某个搜索页的店铺 第一页
    # 传入cookiesList
    shopList = dp.search_shop_item(shopUrl, cookiesList, shopName)  # 获取一个唯一的店铺

    for shopItem in shopList:
        # 提取店铺的名称和店铺全部商品页html
        for shopName in shopItem:
            shopUrl = shopItem[shopName]
            asynSearchMaxPage = 22  # 获取店铺全部商品页最大页码
            page = 6
            # 进行店铺全部商品页的循环
            while page <= asynSearchMaxPage:
                shopUrl = shopUrl.split("pageNo")[0] + "pageNo={}".format(page)
                print("当前店铺全部商品页url是{}".format(shopUrl))
                asynSearchHeaders = dp.set_shop_item_search_headers(shopUrl)  # 获取请求asynSearch.htm页面的headers

                # 传入cookiesList
                asynSearchText = dp.get_shop_item_search_text(asynSearchHeaders, shopUrl, cookiesList=cookiesList)

                asynSearchMaxPage = int(dp.get_max_goods_page_from_dp(asynSearchText))  # 更新全部商品页html最大页码
                page = page + 1

                # 进行店铺全部商品页的每个商品提取
                itemUrlList = dp.get_itemUrl_from_dp(asynSearchText)
                for itemUrl in itemUrlList:
                    # 基于商品url进行去重处理
                    if dp.is_url_exist(itemUrl) == True:
                        print("该商品url已经爬取过,对url进行跳过")
                        continue

                    # 传入cookiesList
                    result = taobaoItemImg.get_item_imgs(cookiesList=cookiesList, requestUrl=itemUrl)

                    skuImgList = result["skuImgList"]  # sku图片列表
                    lbImgList = result["lbImgList"]  # 轮播图列表
                    detailImgList = result["detailImgList"]  # 详情图列表
                    allImgList = skuImgList + lbImgList + detailImgList

                    if allImgList == []:
                        time.sleep(3)  # 没有提取到图片，跳过
                        dp.redisClient.delete(hashlib.md5(itemUrl.encode()).hexdigest())  # 没有提取到图片删除redis中这个已爬取的记录
                        print(f"跳过商品详情页url是{itemUrl}")
                        continue

                    title = result["title"]  # 店铺的名字
                    for img in allImgList:
                        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        sql = "insert into all_imgs_copy2 (`shop_name`, `item_name`, `img_link`, `create_time`) values ('%s', '%s', '%s', '%s')" % (shopName, title, img, t)
                        cursor.execute(sql)
                        conn.commit()
                    print(f"店铺{shopName}共计{len(allImgList)}张关于{title}商品的图片已全部保存！")
                    print("------------提取item详情页{}完成------------".format(itemUrl))
                    time.sleep(random.randint(20, 40))

                # 手动使用cookies爬取，每次爬取完商品列表页做个延迟处理
                if cookiesList != []:
                    time.sleep(random.randint(20, 40))

            # 如果手动使用cookies，爬取整个店铺完整，做个延时
            if cookiesList != []:
                time.sleep(random.randint(20, 40))


# 这份代码没有优化跳过
# def main():
#     cookiesList=[{'l': 'fB_vR164NC-3uSP9BOfaFurza77OSIRYYuPzaNbMi9fPsHfB5_7NW1_FO_86C3GVF6WHR3lDK4dwBeYBqQAonxv9w8VMULkmndLHR35..', 'tfstk': 'cYp5BPOmhz4572D3Eai2GDrRRQ6dwzcfDb_2VVpZAZ8heN1clR71KUd3l9Sdc', 'uc1': 'cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie14=Uoe9bfwIymDKzQ%3D%3D&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C', 'dnk': 'tb80111606', 'cancelledSubSites': 'empty', 'cookie1': 'U%2BGWz3AsFiX%2BQb4KVw17j51DAUP9jxfiN9Dd%2FomAUJ8%3D', '_l_g_': 'Ug%3D%3D', '_nk_': 'tb80111606', 'existShop': 'MTY5MDE4NjUwNQ%3D%3D', 'csg': '6f22e8fb', 'uc3': 'lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCsGGr97fmeDmc8Rg%3D&nk2=F5RNZTse5XZpwA%3D%3D&id2=UNQyQxMqUdx1nQ%3D%3D', 'unb': '3451510054', 'cna': 'Nf9EHZfSwxoCAW8CWybl9Yqd', 'tracknick': 'tb80111606', 'cookie2': '1b759ff838c77b0ec651827884720b0b', 'uc4': 'id4=0%40UgP5GPE5h%2FvopPV87sjzIkKz1%2Ft8&nk4=0%40FY4GsvRHfRNKE%2BdeKAjFMKHJQZFs', '_tb_token_': 'f4b5b9599eb15', '_samesite_flag_': 'true', 'isg': 'BFFRjByX0d7s6T3KsqM2Xp6oYF3rvsUwEe5K7TPmQ5g32nAseQ0xAUYoeq48SV1o', 'skt': 'e8208d91d9b98c38', 'sgcookie': 'E100VIk3OL1IpbuPA6y6tak88kmv3ZhMj4Bddtkc4%2F6gABALxPltLYiGkncS0kRzVRUoVD0MK2oRnd0D%2FspajWld4EyIXCzOxQZ6YJEm7S%2Fao48HdML4pUgFkMKlh8ds4KCd', 'lgc': 'tb80111606', 'sg': '641', '_cc_': 'Vq8l%2BKCLiw%3D%3D', 'cookie17': 'UNQyQxMqUdx1nQ%3D%3D', 'xlly_s': '1', 't': 'a170703abdc55c9694b8dcc5bd3a0e4a'}  ]
#     dp=DP(host="127.0.0.1",password="") # 创建一个店铺对象
#     taobaoItemImg=TaobaoItemImg() # 创建一个item爬取对象
#     taobaoItemImg.enableIpProxy=False # 图片下载不使用ip代理池

#     # 先提取某个搜索页的店铺 第一页
#     # 传入cookiesList
#     shopList = dp.serach_shop_list("女装",2,cookiesList=cookiesList)  # 根据搜索页获取所有店铺
#     # shopList = dp.search_shop_item("https://shop306580388.taobao.com",cookiesList,"店铺的名字") # 获取一个唯一的店铺

#     for shopItem in shopList:
#         # 提取店铺的名称和店铺全部商品页html
#         for shopName in shopItem:
#             shopUrl = shopItem[shopName]
#             print("店铺全部商品页的url是{}".format(shopUrl))
#             asynSearchMaxPage=1 # 获取店铺全部商品页最大页码
#             page=1
#             # 进行店铺全部商品页的循环
#             while page<=asynSearchMaxPage:
#                 shopUrl = shopUrl.split("pageNo")[0]+"pageNo={}".format(page)
#                 print("当前店铺全部商品页url是{}".format(shopUrl))
#                 asynSearchHeaders=dp.set_shop_item_search_headers(shopUrl) # 获取请求asynSearch.htm页面的headers

#                 # 传入cookiesList
#                 asynSearchText=dp.get_shop_item_search_text(asynSearchHeaders,shopUrl,cookiesList=cookiesList)

#                 asynSearchMaxPage=int(dp.get_max_goods_page_from_dp(asynSearchText)) # 更新全部商品页html最大页码
#                 page=page+1

#                 # 进行店铺全部商品页的每个商品提取
#                 itemUrlList = dp.get_itemUrl_from_dp(asynSearchText)
#                 for itemUrl in itemUrlList:
#                     # 基于商品url进行去重处理
#                     if dp.is_url_exist(itemUrl)==True:
#                         print("该商品url已经爬取过,对url进行跳过")
#                         continue

#                     # 传入cookiesList
#                     result = taobaoItemImg.get_item_imgs(cookiesList=cookiesList,requestUrl=itemUrl)

#                     skuImgList = result["skuImgList"] # sku图片列表
#                     lbImgList = result["lbImgList"] # 轮播图列表
#                     detailImgList = result["detailImgList"] # 详情图列表
#                     title= result["title"] # 店铺的名字
#                     taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/sku",skuImgList)
#                     taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/lb",lbImgList)
#                     taobaoItemImg.write_imgList_to_dir(shopName+"/"+title+"/detail",detailImgList)
#                     print("------------提取item详情页{}完成------------".format(itemUrl))
#                     time.sleep(22) # 每个详情页图片下载完成后等待一段时间
#                 time.sleep(random.randint(30,60)) # 店铺每页爬取完成后等待一段时间
#             time.sleep(random.randint(10,30)) # 爬完一个店铺后等待一段时间

if __name__ == '__main__':
    # item_main("https://shop306580388.taobao.com","店铺名字",cookiesList=[{"_cc_":"U%2BGCWk%2F7og%3D%3D","_l_g_":"Ug%3D%3D","_nk_":"tb117416292","_samesite_flag_":"true","_tb_token_":"eeee6e1759b73","cancelledSubSites":"empty","cna":"4zdRHYIYAioCASQYc6rJ5G+f","cookie1":"BYXLDujz7cMf5qXWf0wpvtl2XoqRpayhoOHj22O2chc%3D","cookie17":"UUphzOV4ZmtYf4ZcQA%3D%3D","cookie2":"141d7d2d0c9719cc68e3487d8693615d","csg":"e1cfd189","dnk":"tb117416292","existShop":"MTY5MDk3ODgwMA%3D%3D","isg":"BBMTRsmuc_AYZT-k_LwTEN8xopc9yKeK6inylMUwbjJoRDLmW5rN294GeLQqf_-C","l":"fBgWNgXqNek_vrCDBOfaFurza77OSIRYYuPzaNbMi9fPOwCB5Ul5W1ONiuL6C3GVFs_HR38PiVPBBeYBq7Vonxv9w8VMULkmndLHR35..","lgc":"tb117416292","sg":"258","sgcookie":"E100AcrFa%2BtaMmSJitMFoSzvRC6DkfwPZc4nFR3DQUgx2PTr0ip0jLnpzjTTCgf9UPjHFxXBMqBFPRajiTPD9kM7JfcnLisW4B1p%2BKZMvJJnxqeb%2Fw%2BwiivR%2BtVRATe7EOOE","skt":"be4c5c3f2939a181","t":"74df446e826e16608b11a525d6ffdf6a","tfstk":"dTB6fkaR2V01ew9ByfZFO3ILeppbzNwzGmtAqiHZDdpTh6sllFr0sd5BlwQBWClaInpfJZrM7iB2Dt9GL1k27PvfDaJbzzyzUdjMEKUzztPdjGxT7BpLU8SGjKvYzzyzo72n7tAcdlOyPmNiDO62JCTRf7Dxh9My1UI9RxKhdO5rUU1_RjiBZxtBzkZIijVcQUpd.","tracknick":"tb117416292","uc1":"pas=0&cookie14=Uoe9bfSDjYeQGg%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&cookie21=URm48syIYB3rzvI4Dim4","uc3":"id2=UUphzOV4ZmtYf4ZcQA%3D%3D&vt3=F8dCsGCkNagY%2FqXoJ%2BI%3D&nk2=F5REP7sBUHYX1vY%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D","uc4":"id4=0%40U2grF8636cbIDpmfqxXgrXyJqUF9kM3s&nk4=0%40FY4Pba8SP%2Fxz1We3n%2B84Qyh5%2F2PTXw%3D%3D","unb":"2206799874005","xlly_s":"1"}])
    item_main("https://shop170638374.taobao.com/", "知否原创汉服")
    # 多进程启动如果cookies够多
    # processPool = ProcessPoolExecutor()
    # processPool.submit(item_main,"url","店铺名字")
    # processPool.submit(item_main,"url1","店铺名字")



