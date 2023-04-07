import requests
from lxml import etree
page = input('请输入要爬取多少页：')
page = int(page) + 1
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
n = 0
pn = 1
#pn是从第几张图片获取 百度图片下滑时默认一次性显示30张
for m in range(1,page):
    url = 'https://image.baidu.com/search/acjson?'

    param = {
        'tn': 'resultjson_com',
        'logid': '8846269338939606587',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': '水果',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z':'' ,
        'ic':'' ,
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': '水果',
        's':'' ,
        'se':'' ,
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': 'girl',
        'pn': pn,#从第几张图片开始
        'rn': '30',
        'gsm': '1e',
    }
    page_text = requests.get(url=url,headers=header,params=param)
    page_text.encoding = 'utf-8'
    page_text = page_text.json()
    info_list = page_text['data']
    del info_list[-1]
    img_path_list = []
    for i in info_list:
        img_path_list.append(i['thumbURL'])
    
    for img_path in img_path_list:
        img_data = requests.get(url=img_path,headers=header).content
        img_path = 'images/' + str(n) + '.jpg'
        with open(img_path,'wb') as fp:
            fp.write(img_data)
        n = n + 1
        
    pn += 29
