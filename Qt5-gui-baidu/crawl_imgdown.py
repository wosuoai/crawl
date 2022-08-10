import re
import os
import requests
import urllib3
from fake_useragent import UserAgent

def existDir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass


def reptile(reptileWord, savePath, downpageSize):
    # 如果文件夹不存在就创建文件夹
    existDir(savePath)

    count = 1
    for page in range(0, downpageSize):
        pn = page * 40

        # 获取百度页面url地址
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + reptileWord + '&pn={}'.format(pn)
        headers = {'User-Agent': UserAgent().random}
        urllib3.disable_warnings()
        response = requests.Session()
        response.headers = headers
        html = response.get(url, timeout=10, allow_redirects=False)

        # 正则表达式获取所有url
        pic_urls = re.findall('"objURL":"(.*?)",', html.text, re.S)

        # 遍历所有url
        t = 0
        for pic_url in pic_urls:
            download_value = '正在下载第' + str(count) + '张图片'
            string = savePath + r'\\' + reptileWord + '+' + str(count) + '.jpg'
            local_path = open(string, 'wb')
            photo = requests.get(pic_url, timeout=5)
            # 写入爬取成功的图片
            local_path.write(photo.content)
            local_path.close()
            count += 1
            t = t + 1
            if t > 40:
                t = 0
                break

            print(download_value)


if __name__ == '__main__':
    word = '图片'
    path = 'G:/spyder/code/111'
    pageSize = '2'
    pageSize = int(pageSize)
    values = reptile(word, path, pageSize)
