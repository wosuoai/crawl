import requests
import json
import random
import re
import uuid
import os
import time
import lxml
import lxml.etree
from setting import cookiesPoolUrl

class TaobaoItemImg:
    def __init__(self):
        self.tbHeaders = {
            'authority': 'item.taobao.com',
            #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        self.enableIpProxy=False
        self.enableCookiesPool=True

    def set_proxy(self):
        """
        set proxy for requests
        :param proxy_dict
        :return:
        """
        if self.enableIpProxy:
            res=requests.get(url="").text.strip()
            return {
                    "http": "http://{}".format(res),
                    "https": "http://{}".format(res)
                    }
        else:
            return None

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

    # 实现将图片列表写入到文件夹的功能
    def write_imgList_to_dir(self,dirPath:str,imgList:list):
        headers = {
            'authority': 'img.alicdn.com',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'if-modified-since': 'Fri, 11 Aug 2023 10:05:11 GMT',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        # 如果文件夹不存在创建新的文件夹
        if os.path.exists(dirPath)==False:
            os.makedirs(dirPath)

        if len(imgList) > 0:
            for imgUrl in imgList:
                if str(imgUrl).startswith("http"):
                    if str(imgUrl).endswith(".gif"):
                        print("该图片是gif图片跳过%s"%imgUrl)
                        continue
                    filename = uuid.uuid4().hex
                    try:
                        hz=os.path.splitext(imgUrl)[-1] # 获取图片名称后缀
                        with open("{}/{}{}".format(dirPath,filename,hz),"wb") as f:
                            print(dirPath + "图片{}下载成功".format(imgUrl))
                            f.write(requests.get(imgUrl,headers=headers,proxies=self.set_proxy()).content)
                        if self.enableIpProxy==False:
                            time.sleep(random.randint(2,4)*0.1)
                    except Exception as error:
                        print("图片下载出现错误%s"%error)

    # 获取网页item.html原始txt数据
    def get_item_html_text(self,cookies:dict,requestUrl:str)->str:
        responseText=""
        if 'item.taobao.com' in requestUrl:
            try:
                responseText = requests.get(url=requestUrl,headers=self.tbHeaders,cookies=cookies).text
            except Exception as error:
                print("获取网页item.html原始text数据失败,错误是{}".format(error))
        return responseText

    # 获取淘宝商品轮播图片列表
    def get_lb_url_list(self,responseText:str)->list:
        return self.pattern_lb_response(responseText)

    # 获取sku轮播图列表
    def get_sku_url_list(self,responseText:str)->list:
        return self.pattern_sk_response(responseText)

    # 获取详情图链接
    def get_detail_url(self,responseText:str)->str:
        pattern = r"apiImgInfo:'([^']+)'"
        url=""
        match = re.search(pattern, responseText.replace("\n","").replace(" ",""))
        if match:
            url = match.group(1)
        if url!="":
            return "https:"+url
        return url

    # 获取详情图文本
    def get_detail_img_text(self,detailImgUrl:str,cookies2:dict)->str:
        try:
            return requests.get(url=detailImgUrl,cookies=cookies2,headers=self.tbHeaders).text
        except Exception as error:
            print("获取获取详情图文本失败,失败原因是{}".format(error))
            return ""

    # 获取详情图列表
    def get_detail_img_url_list(self,responseText:str)->list:
        return self.pattern_detail_img_response(responseText)

    # 解析轮播图结果
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

    # 解析sku轮播图结果
    def pattern_sk_response(self,returnText:str)->list:
        # r'background:url\((.*?)\)'
        pattern = r'background:url\((.*?)\)'
        jsonText=returnText.replace("\n","").replace(" ","")
        imageLinks = re.findall(pattern, jsonText)
        skuImgList=[]
        for itemUrl in imageLinks:
            sItemUrl = str(itemUrl)
            sItemUrl=sItemUrl.replace("_30x30.jpg","")
            if sItemUrl.startswith("//"):
                skuImgList.append("https:"+sItemUrl)
                continue
            skuImgList.append(sItemUrl)
        return skuImgList

    # 解析详情图结果
    def pattern_detail_img_response(self,returnText:str)->list:
        detailImgList=[]
        result = returnText.replace("\n","").replace(" ","").replace("$callback(","").replace(")","")
        if result=="":
            return detailImgList
        jsonResult=json.loads(result)
        for key in jsonResult:
            value=jsonResult[key]
            if isinstance(value, dict) and "w" in value and "h" in value:
                detailImgList.append("https://gd3.alicdn.com/imgextra/i2/2207245700365/"+key)
        return detailImgList

    # 返回统计返回所有结果
    def get_item_imgs(self,cookiesList:list,requestUrl:str)->dict:
        isUse=False  # 是否使用cookis池
        # 如果没有传入cookies就使用cookies池
        if cookiesList==[]:
            cookiesList=[self.get_cookiesList_from_cookiesPool()]
            isUse=True

        # 如果调用接口cookies已经使用过，设置cookies为空重新获取cookies
        if isUse:
            cookiesList=[]
            cookiesList=[self.get_cookiesList_from_cookiesPool()]

        # 获取item.html文本
        htmlText = self.get_item_html_text(cookies=random.choice(cookiesList),requestUrl=requestUrl)

        # 获取商品名字
        title = "未知"
        titleList=lxml.etree.HTML(htmlText).xpath("//title/text()")
        if len(titleList)>0:
            title=str(titleList[0]).replace(" ","")
        title_erList = ["|", "】", "【", "/", "\\", ":", "*", "?", '"', ">", "<", "'"]  # Windows文件夹命名规则不包含的字符
        for i in title_erList:
            title = title.replace(i, "")

        # 获取轮播图列表
        lbImgList=self.get_lb_url_list(htmlText)

        # 获取sku列表
        skuImgList=self.get_sku_url_list(htmlText)

        # 获取详情图列表
        detailImgText=""
        detailImgUrl = self.get_detail_url(htmlText) # 详情图url
        if detailImgUrl != "":
            if cookiesList==[]:
                cookiesList=[self.get_cookiesList_from_cookiesPool()]
            detailImgText = self.get_detail_img_text(detailImgUrl,random.choice(cookiesList)) # 详情图页面文本
        detailImgList=self.get_detail_img_url_list(detailImgText) # 详情图页面的图片列表
        return {
            "title":title,
            "skuImgList":skuImgList,
            "lbImgList":lbImgList,
            "detailImgList":detailImgList
        }


if __name__ == "__main__":
    # cookies列表
    cookiesList=[]

    # 创建一个爬取淘宝详情的
    taobaoItemImg= TaobaoItemImg()
    # print(getIp())
    # count=0
    # url="https://detail.tmall.com/item.htm?ali_refid=a3_431358_1007:583780033:U:251836915_0_6373557982:a96eed9f9ef944739f14118d2cd3577e&ali_trackid=149_a96eed9f9ef944739f14118d2cd3577e&id=656852524774&scm=1007.40986.276750.0&spm=a21bo.jianhua.201876.61&sku_properties=147956252:75366378"
    url1="https://item.taobao.com/item.htm?spm=a211oj.24780012.3690372280.ditem3.127636dcFJq5uV&id=706709723784&utparam=%7B%22ald_res%22%3A%2228320006%22%2C%22ald_solution%22%3A%22SmartHorseRace%22%2C%22ald_biz%22%3A1234%2C%22ump_item_price%22%3A%22808%22%2C%22traceId%22%3A%222147b50016900221406546227ef31f%22%2C%22ald_st%22%3A%221690022140749%22%2C%22item_price%22%3A%22808%22%2C%22ald_price_field%22%3A%22itemActPrice%22%2C%22ump_invoke%22%3A%222%22%2C%22ump_sku_id%22%3A%225011134284858%22%2C%22ump_price_stage%22%3A%220%22%7D"
    # htmlText= taobaoItemImg.get_item_html_text(cookies=random.choice(cookiesList),requestUrl=url1)
    # print(taobaoItemImg.get_lb_url_list(htmlText))
    # print(taobaoItemImg.get_sku_url_list(htmlText))
    # imgUrl="https://tds.alicdn.com/json/item_imgs.htm?t=desc/icoss21734163593a1d75c0edf5072&sid=2207245700365&id=707947099148&s=0e1c9da6ec5a098736bb5d9e4101bc76&v=2&m=1"
    result = taobaoItemImg.get_item_imgs(cookiesList,requestUrl=url1)

    skuImgList = result["skuImgList"]
    lbImgList = result["lbImgList"]
    detailImgList = result["detailImgList"]
    print(result['title'])
    # print(lbImgList)
    # print("-----------")
    # print(skuImgList)
    # print("------------")
    # print(detailImgList)
    taobaoItemImg.write_imgList_to_dir("a/sku",skuImgList)
    taobaoItemImg.write_imgList_to_dir("a/lb",lbImgList)
    taobaoItemImg.write_imgList_to_dir("a/detail",detailImgList)


    # print(taobaoItemImg.)
    # url_tm="https://item.taobao.com/item.htm?id=656852524774"
    # for i in range(100000):
    #     count=count+1
    #     print("爬取了多少次%s"%count)
    #     time.sleep(random.randint(20,40))
    #     print(taobaoLB.get_lb_url(random.choice(cookiesList),requestUrl=url1))
    # callback: jsonp286
    # input_charset: gbk
    # mid: w-23122658373-0
    # wid: 23122658373
    # path: /category.htm
    # spm: a1z10.3-c-s.w4002-23122658373.66.787a658d4Ys1Sy
    # input_charset: gbk
    # search: y
    # pageNo: 2




