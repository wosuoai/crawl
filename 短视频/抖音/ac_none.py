import requests
sess = requests.session()
headers_base = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"no-cache",
    "pragma":"no-cache",
    "sec-ch-ua":"\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"\"Windows\"",
    "sec-fetch-dest":"document",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"none",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
sess.headers = headers_base
url = 'https://www.douyin.com'
__ac_nonce = sess.get(url,headers=headers_base).cookies.get('__ac_nonce')
print(__ac_nonce)