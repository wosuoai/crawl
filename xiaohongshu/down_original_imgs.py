import requests
import os


def fetchUrl(url):
    #获取网页源码
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    r = requests.get(url, headers=headers)
    return r.text


def parsing_link(html):
    #解析html文本，提取无水印图片的 url

    beginPos = html.find('imageList') + 11
    endPos = html.find(',"atUserList"')
    print(beginPos,endPos)
    imageList = eval(html[beginPos:endPos])

    for i in imageList:
        picUrl = f"https://sns-img-hw.xhscdn.com/{i['traceId']}?imageView2/2/w/1920/format/webp|imageMogr2/strip"
        yield picUrl, i['traceId']


def download(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    with open(f'{filename}.jpg', 'wb') as v:
        try:
            r = requests.get(url, headers=headers)
            v.write(r.content)
        except Exception as error:
            print('图片下载错误！')


if __name__ == '__main__':
    original_link = 'https://www.xiaohongshu.com/explore/632bc3950000000009008a62'
    html = fetchUrl(original_link)
    for url, traceId in parsing_link(html):
        print(f"download image {url}")
        download(url, traceId)

    print("Finished!")
