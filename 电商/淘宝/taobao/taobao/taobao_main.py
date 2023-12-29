from taobao_dp import DP
import time
from taobao_item_img import TaobaoItemImg
import random
import hashlib
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def item_main(shopUrl: str, shopName):
    cookiesList = []
    dp = DP(host="127.0.0.1", password="")  # 创建一个店铺对象
    taobaoItemImg = TaobaoItemImg()  # 创建一个item爬取对象
    taobaoItemImg.enableIpProxy = False  # 图片下载不使用ip代理池

    # 先提取某个搜索页的店铺 第一页
    # 传入cookiesList
    shopList = dp.search_shop_item(shopUrl, cookiesList, shopName)  # 获取一个唯一的店铺

    for shopItem in shopList:
        # 提取店铺的名称和店铺全部商品页html
        for shopName in shopItem:
            shopUrl = shopItem[shopName]
            print("店铺全部商品页的url是{}".format(shopUrl))
            asynSearchMaxPage = 1  # 获取店铺全部商品页最大页码
            page = 1
            # 进行店铺全部商品页的循环
            while page <= asynSearchMaxPage:
                shopUrl = shopUrl.split("pageNo")[0] + "pageNo={}".format(page)
                print("当前店铺全部商品页url是{}".format(shopUrl))
                asynSearchHeaders = dp.set_shop_item_search_headers(shopUrl)  # 获取请求asynSearch.htm页面的headers

                # 传入cookiesList
                asynSearchText = dp.get_shop_item_search_text(asynSearchHeaders, shopUrl, cookiesList=cookiesList)

                asynSearchMaxPage = int(dp.get_max_goods_page_from_dp(asynSearchText))  # 更新全部商品页html最大页码
                page = page + 1

                try:
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
                            break

                        title = result["title"]  # 店铺的名字
                        start = time.time()
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, skuImgList)
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, lbImgList)
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, detailImgList)
                        print("单个商品图片下载共计耗时%s" % (time.time() - start))
                        print("------------提取item详情页{}完成------------".format(itemUrl))
                    time.sleep(random.randint(5, 10))  # 每个详情页图片下载完成后等待一段时间
                except:
                    pass
            time.sleep(random.randint(10, 20))  # 爬完一个店铺后等待一段时间


def main():
    cookiesList = []
    dp = DP(host="127.0.0.1", password="")  # 创建一个店铺对象
    taobaoItemImg = TaobaoItemImg()  # 创建一个item爬取对象
    taobaoItemImg.enableIpProxy = False  # 图片下载不使用ip代理池

    # 先提取某个搜索页的店铺 第一页
    # 传入cookiesList
    shopList = dp.serach_shop_list("女装", 2, cookiesList=cookiesList)  # 根据搜索页获取所有店铺
    # shopList = dp.search_shop_item("https://shop306580388.taobao.com",cookiesList,"店铺的名字") # 获取一个唯一的店铺

    for shopItem in shopList:
        # 提取店铺的名称和店铺全部商品页html
        for shopName in shopItem:
            shopUrl = shopItem[shopName]
            print("店铺全部商品页的url是{}".format(shopUrl))
            asynSearchMaxPage = 1  # 获取店铺全部商品页最大页码
            page = 1
            # 进行店铺全部商品页的循环
            while page <= asynSearchMaxPage:
                shopUrl = shopUrl.split("pageNo")[0] + "pageNo={}".format(page)
                print("当前店铺全部商品页url是{}".format(shopUrl))
                asynSearchHeaders = dp.set_shop_item_search_headers(shopUrl)  # 获取请求asynSearch.htm页面的headers

                # 传入cookiesList
                asynSearchText = dp.get_shop_item_search_text(asynSearchHeaders, shopUrl, cookiesList=cookiesList)

                asynSearchMaxPage = int(dp.get_max_goods_page_from_dp(asynSearchText))  # 更新全部商品页html最大页码
                page = page + 1

                try:
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
                        title = result["title"]  # 店铺的名字
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, skuImgList)
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, lbImgList)
                        taobaoItemImg.write_imgList_to_dir(shopName + "/" + title, detailImgList)
                        print("------------提取item详情页{}完成------------".format(itemUrl))
                    time.sleep(random.randint(20, 30))  # 每个详情页图片下载完成后等待一段时间
                except:
                    pass
            time.sleep(random.randint(10, 20))  # 爬完一个店铺后等待一段时间


if __name__ == '__main__':
    item_main("https://shop60785920.taobao.com/", "羊城故事 cantonstory")
    # 多进程启动如果cookies够多
    # processPool = ProcessPoolExecutor()
    # processPool.submit(item_main,"url","店铺名字")
    # processPool.submit(item_main,"url1","店铺名字")