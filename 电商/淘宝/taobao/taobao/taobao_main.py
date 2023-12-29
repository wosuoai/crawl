from taobao_dp import DP
import time
from taobao_item_img import TaobaoItemImg
import random
import hashlib
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def item_main(shopUrl: str, shopName):
    cookiesList = [{'v': '0', 'l': 'fBSyexXIPxP-CN0CKOfwPurza77OSIRAguPzaNbMi9fP_8fk5M35W1nJF6LDC3GVFse9R3J_8YVHBeYBq7Vonxvte5DDwQHmnmOk-Wf..', 'tfstk': 'd0DkEm_wEbP5kv77tQeWU7PSv-RvPawQ82BLJJUegrzj29KS2jqEJqtBV8nU-20Yl0BpV0hcxcgm-Wt7JyznJDlJDdptV0wQLwY9BdFHrJwUH1rAg0i7dJSA8ChqV941xnBPII8KKFkJq5UGAlvc5wBuwPozu0n-3ubT70zcL9zuqO7Rg1SVF9Z2vx5CO7rbmPFkD19f.', 'uc1': 'cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=Uoe9a7Je%2B0q77w%3D%3D&cookie21=V32FPkk%2FhSg%2F&pas=0&existShop=false&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D', '_m_h5_tk_enc': 'f26335dc6656961610809fe6ed9ca804', '_m_h5_tk': '6d09afeedd6351c7f8b6744bee3b8865_1696930252139', 'dnk': 'tb675900152750', 'cancelledSubSites': 'empty', 'cookie1': 'AHmARbUtDQf0ukZ86Lb%2B1T8d6lvSen3LOaBTFr0vJxE%3D', '_l_g_': 'Ug%3D%3D', 'cookie2': '14036b05c361b5ee4b1d4d44a59c0cdb', 'uc4': 'nk4=0%40FY4I6FUnZTj%2BCtAGblpRX8MTjiMHqZKUDA%3D%3D&id4=0%40U2gqz6QY%2BuLQ6lct5m54rey7kDqoPvKL', '_nk_': 'tb675900152750', 'existShop': 'MTY5NjkxOTc5OA%3D%3D', 'csg': 'ebce3070', 'tracknick': 'tb675900152750', 'thw': 'cn', 'cna': '0t6rHX11RU4CAXPBe+oirVOA', 'uc3': 'id2=UUpgQEvyiMFol7r9dg%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&nk2=F5RDK1aMEME8kyIMKUM%3D&vt3=F8dCsGrN2NWJO%2FpMOWs%3D', 'unb': '2216208669787', 'mt': 'ci=0_1', 'sg': '070', 'lgc': 'tb675900152750', 'isg': 'BMjIrLmLOc9PxFVLwqed98LdmTbacSx7qnIE04J5FMM2XWjHKoH8C17f0TUt7eRT', 'skt': '719d4762a51751a6', '_tb_token_': '7e53e7e3646e4', 'sgcookie': 'E100w6wdH8fqmRcnqsBFHfn%2FVJ9xtlpJmaWRS0WDe1KWv%2FOJbpaYRPkcEpnLqdJDjtjGT9Dlrmi6P%2BWCfVuhqtmexs5layK4cN24sf16uyP2pvU%3D', '_cc_': 'Vq8l%2BKCLiw%3D%3D', 'cookie17': 'UUpgQEvyiMFol7r9dg%3D%3D', 'xlly_s': '1', 't': 'daaf0164bf82f635c431690f4123f3b3', '_samesite_flag_': 'true'}]
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
    cookiesList = [{'tfstk': 'dNee3IsD-9BFvANKbjMzbOPjNKMKFxQfL8gSquqoA20nRumoUP45v2ZlJzyrSuFCvb_p4HeauL9CJ6EkUYMllZ6fhkKIeYbjnkvX9IHr9Ns65tZLvYKeriNGh0uAwYWr-f6w_OGhoo3gLQ_Ypdbu1VJk3nnEt-XxSLvuQDrZcOkyycAeN8FerQlnXcufbGzghYlV.', 'l': 'fBg6RSc4N3uVhr_9BOfwourza77OlIRfguPzaNbMi9fP_7fpj46FW1O0n6L9CnGVEsd9R38PiVPBBbYiDy4Fmxv9-eTCgsDKndLnwpzHU', 'uc1': 'cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=false&pas=0&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie21=U%2BGCWk%2F7oPIg&cookie14=Uoe9bfibBTJJNQ%3D%3D', '_nk_': 'tb190299083298', '_l_g_': 'Ug%3D%3D', 'cookie2': '1ea26f2366b8c7016e6b2e7d1c165603', 'uc4': 'nk4=0%40FY4PZdb%2Bd5L%2B34Qv%2Fa5cvO6Bl7SvPQ5Etg%3D%3D&id4=0%40U2gqz6fTwYfR056JIWg0jpNSkJYftW95', 'cookie1': 'W8rvz2ilfARm%2BgIV2uEja%2BoORUSU4B9RxHi0RpERwZw%3D', 'dnk': 'tb190299083298', 'cancelledSubSites': 'empty', 'mt': 'ci=0_1', 'sg': '876', 'lgc': 'tb190299083298', 'csg': 'feef3be1', 'isg': 'BJeXuGTyvy2l4TvbKoCBXVnjJgvh3Gs-zsX2mOnE02b1GLZa8a-DjxMwfrgG8EO2', 'skt': 'e2654b9acb270c13', 'sgcookie': 'E100m7bAUKRZI7y22GXKTk7bPyTPM%2BHgneAlwjNOx6esmp%2FOB6b%2BNZsjGk00M3x%2FqnyhecfWVplER3Eeg0sWB2NQlPKPrEcMbBlJYflpYXhwNJ0SSav0Mu74qVuZjLamUj%2BZ', '_tb_token_': 'f01e1773895ee', '_samesite_flag_': 'true', 'existShop': 'MTY5MDUzNzk3OA%3D%3D', '_m_h5_tk': 'dd5808338f75b4fd5ee78865a997c2c3_1690545633662', '_m_h5_tk_enc': 'e5fe73f0f59c0dd3ad3ec4554f17f7ae', 'uc3': 'lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=F5REN0TzpuIpquvrAXs%3D&id2=UUpgQEj92dq3JiruyQ%3D%3D&vt3=F8dCsGCg2jA36x9DgBw%3D', 'unb': '2216199918737', '_cc_': 'UtASsssmfA%3D%3D', 'cookie17': 'UUpgQEj92dq3JiruyQ%3D%3D', 'xlly_s': '1', 't': 'be650f779bda6984ae19184e3075c83c', 'cna': 'duFAHTR2tzYCAX158qGMeKOh', 'thw': 'cn', 'tracknick': 'tb190299083298'}]
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