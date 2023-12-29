from taobao_dp import DP
import time
from taobao_item_img import TaobaoItemImg
import random
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from threading import Thread
from setting import redisHost,redisPort,redisPassword
import hashlib

def item_main(shopUrl:str,shopName:str,cookiesList:list=[]):
    # 创建对象
    dp=DP(host=redisHost,port=redisPort,password=redisPassword) # 创建一个店铺对象
    taobaoItemImg=TaobaoItemImg() # 创建一个item爬取对象
    
    # 进行是否使用ip代理池和cookies池配置
    taobaoItemImg.enableIpProxy=False # 图片下载不使用ip代理池
    dp.enableCookiesPool=True # 获取店铺是否使用cookies池
    taobaoItemImg.enableCookiesPool=True # 获取详情页图片是否使用cookies池
    
    # 先提取某个搜索页的店铺 第一页
    # 传入cookiesList
    shopList = dp.search_shop_item(shopUrl,cookiesList,shopName) # 获取一个唯一的店铺
    
    for shopItem in shopList:
        # 提取店铺的名称和店铺全部商品页html
        for shopName in shopItem:
            shopUrl = shopItem[shopName]
            asynSearchMaxPage=1 # 获取店铺全部商品页最大页码
            page=1
            # 进行店铺全部商品页的循环
            while page<=asynSearchMaxPage:
                shopUrl = shopUrl.split("pageNo")[0]+"pageNo={}".format(page)
                print("当前店铺全部商品页url是{}".format(shopUrl))
                asynSearchHeaders=dp.set_shop_item_search_headers(shopUrl) # 获取请求asynSearch.htm页面的headers
                
                # 传入cookiesList
                asynSearchText=dp.get_shop_item_search_text(asynSearchHeaders,shopUrl,cookiesList=cookiesList)
                
                asynSearchMaxPage=int(dp.get_max_goods_page_from_dp(asynSearchText)) # 更新全部商品页html最大页码
                page=page+1
                
                # 进行店铺全部商品页的每个商品提取
                itemUrlList = dp.get_itemUrl_from_dp(asynSearchText)
                for itemUrl in itemUrlList:
                    # 基于商品url进行去重处理
                    if dp.is_url_exist(itemUrl)==True:
                        print("该商品url已经爬取过,对url进行跳过")
                        continue
                    
                    # 传入cookiesList
                    result = taobaoItemImg.get_item_imgs(cookiesList=cookiesList,requestUrl=itemUrl)
                    
                    allImgList=[]
                    skuImgList = result["skuImgList"] # sku图片列表
                    lbImgList = result["lbImgList"] # 轮播图列表
                    detailImgList = result["detailImgList"] # 详情图列表
                    allImgList=skuImgList+lbImgList+detailImgList
                    
                    if allImgList==[]:
                        time.sleep(3) # 没有提取到图片，跳过
                        dp.redisClient.delete(hashlib.md5(itemUrl.encode()).hexdigest()) # 没有提取到图片删除redis中这个已爬取的记录
                        print(f"跳过商品详情页url是{itemUrl}")
                        continue
                     
                    title= result["title"] # 店铺的名字
                    taobaoItemImg.write_imgList_to_dir(shopName+"/"+title,skuImgList)
                    taobaoItemImg.write_imgList_to_dir(shopName+"/"+title,lbImgList)
                    taobaoItemImg.write_imgList_to_dir(shopName+"/"+title,detailImgList)
                    print("------------提取item详情页{}完成------------".format(itemUrl))
                    # 如果使用了手动cookies,每次爬取完item详情页做延迟，防止cookies被ban
                    if cookiesList!=[]:
                        time.sleep(random.randint(20,40))

                # 手动使用cookies爬取，每次爬取完商品列表页做个延迟处理
                if cookiesList!=[]:
                    time.sleep(random.randint(20,40))
            
            # 如果手动使用cookies，爬取整个店铺完整，做个延时
            if cookiesList!=[]:
                time.sleep(random.randint(20,40))

# 这份代码没有优化跳过
# def main():
#     cookiesList=[]
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
    # item_main("https://shop306580388.taobao.com","店铺名字",cookiesList=[])
    item_main("https://shop258347922.taobao.com/","陈佳楠 NN's")
    # 多进程启动如果cookies够多
    # processPool = ProcessPoolExecutor()
    # processPool.submit(item_main,"url","店铺名字")
    # processPool.submit(item_main,"url1","店铺名字")