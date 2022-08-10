import re
import time
import requests
from urllib import parse
import os
from fake_useragent import UserAgent #随机生成一个user-agent,模拟有多个浏览器访问
import urllib3

dicPattern={'bing':r'<img class="mimg vi.*src="(.*?)"','baidu':r'"middleURL":"(.*?)"','sogou':r'img.*src="(.*?)"','360':r'"img":"(.*?)"'}
dicUrl={'bing':'https://cn.bing.com/images/search?q={}&form=HDRSC2&first={}&tsc=ImageHoverTitle','baidu':'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7542812996841482750&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&{}='}

def writeHtml(outfile,html):
    with open(outfile,'w',encoding='utf-8') as f:
        f.write(str(html))


def geturls(baseurl,enginPattern):
    ImgUrlPattern = re.compile(enginPattern)

    # 响应头，假装我是浏览器访问的网页
    headers ={'User-Agent':UserAgent().random}
    urllib3.disable_warnings()                         #忽略警告
    response = requests.get(baseurl, headers=headers)  # 获取网页信息

    html = response.text                  # 将网页信息转化为text形式
    data=re.findall(ImgUrlPattern, html)  # 得到图片超链接的列表
    return data

def DownloadImg(imgUrls):
    global i
    headers={'User-Agent':UserAgent().random}

    for ImgUrl in imgUrls:
        if i < imgNum:
            # 如果url是无效的，则查看下一个url
            try:
                resp = requests.get(ImgUrl, headers=headers)# 获取网页信息
            except requests.ConnectionError as error:
                continue
            byte = resp.content# 转化为content二进制
            with open("{:0>4d}.jpg".format(i + 1), "wb") as f:
                if resp.status_code==200 and len(str(byte)) > 1000 :
                    f.write(byte)
                    i = i + 1
                    time.sleep(1)  #设置间隔，避免访问过快认为我在DDS攻击服务器
                    print("第{}张与{}有关的图片爬取成功!".format(i, search))
        else:
            break

#print('有效的引擎有：bing,baidu')
engine=input('请输入引擎：')
search=input('请输入检索词：')
imgNum=int(input('请输入爬取图片数量：'))

i=0

def main():
    if not os.path.isdir("./{}_{}".format(search,engine)):#判断文件夹是否存在，不存在创建文件夹
        os.mkdir("./{}_{}".format(search,engine))
    os.chdir("./{}_{}".format(search,engine))

    global i
    while(i<imgNum):
        for index in range(1000):
            if engine=='baidu':
                decteUrl=dicUrl[engine].format(parse.quote(search),parse.quote(search),index*30,str(int(time.time()*1000)))
            elif engine=='bing':
                decteUrl=dicUrl[engine].format(search,index*35) #dicUrl保存引擎与搜索地址的映射
            imgUrls=geturls(decteUrl,dicPattern[engine])#获取网页中所有图片地址
            DownloadImg(imgUrls)
            if i>=imgNum:
                break
    if(i==imgNum):
        print("已基于搜索引擎{}爬取了{}张与{}相关的图片，保存在文件夹{}".format(engine,imgNum,search,os.getcwd()))


if __name__ == '__main__':
    main()