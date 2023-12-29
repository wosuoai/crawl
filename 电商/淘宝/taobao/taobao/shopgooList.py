import requests

cookies = {}

headers = {
    'authority': 'shop114791417.taobao.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'referer': 'https://shop114791417.taobao.com/?spm=a230r.7195193.1997079397.2.50af6831gaOAhw',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

params = {
    'pageSize': '20',
    'shopId': '114791417',
    'page': '1',
    'sortType': 'des',
    # 'orderType': 'popular',
    'appUid': 'RAzN8BQwukorVdqYGeiXsjZbVA5Xw',
}

response = requests.get('https://shop114791417.taobao.com/getShopItemList.htm', params=params, cookies=cookies, headers=headers)
print(response.text)