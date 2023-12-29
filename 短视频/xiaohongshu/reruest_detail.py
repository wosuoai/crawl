import requests
import execjs
import random

def register_Id(c=32):
    s = "abcdef0123456789"
    webId = ''
    for i in range(c):
        webId += random.choice(s)
    return webId

def register_session():
    url = 'https://edith.xiaohongshu.com/api/sns/web/v1/login/activate'
    headers = {
        'authority': 'edith.xiaohongshu.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'xhsTrackerId=0aa97c49-0ecc-4519-9561-6c2a9b001960; xhsTrackerId.sig=AloePOx9ItgsrrdnH1g1uJdSZDXEWWbNzpRe5jF2e3U; xsecappid=xhs-pc-web; a1=187b334463dcaf4kzy8em3ycw3ev8sttn58p4y6mn50000381150; webId=b2cbb36a757bd1aa33ae163698242f5f; gid=yYWDqq44q8I0yYWDqq44K2vKqfS0i4TuvYd6Y6IqvSEqdU28hYM994888qYyy288Y42qDjJf; gid.sign=Ui/aW0yA8k/tuCiM1e44knL0uxg=; xhsTracker=url=explore&searchengine=baidu; xhsTracker.sig=u1cFYHAwm89lKbFLL1Y8vp9JcskioXWTa56RKaAB2ys; webBuild=2.3.1; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=f3a71ba5-8311-442a-bb3a-e0fb3db04226; extra_exp_ids=yamcha_0327_exp,h5_1208_exp3,ques_clt2; extra_exp_ids.sig=ETM51AFqVyLPOioG2x0qNaEzMLVwrEIN37uTpfkLqxc; web_session=040069b147824957be304a847e364bd6f33ca6',
        'origin': 'https://www.xiaohongshu.com',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-b3-traceid': '97bc1c22d46aed7c',
        'x-s': 'OgAb12O6OBM+Z2w6Z6FG1gcCs25GZgw6sB1K121LOg13',
        'x-s-common': '2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0P1PjhIHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHUN0P1PaHVHdWMH0ijP/W7G0PA+ec9P9z0GnGFy7kEwBpTP7S04A+S40YA4oz1+/YI+oD9JnhMPeZIPePhP/rMPsHVHdW9H0il+0WU+0WEP/LhP/rhNsQh+UHCHDRdcnHlPDu9/FQ+tMiU4A8y+D8oPn40c7PU+L4y87q9qFHlaArUPLlO8ArAHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafpr8bQhqgb78rS9cg+gcf+i4MmF4B4T+e8NpgkhanWIqAmPa7+xqg412/4rnDS9J7+hGSmx2n+McLSia9prG/4A8fzIJbmM4FFUpd49q9RMqrSe4nMwpAYN2S87LFSe89p3pdzH47b7zrSb/g+QyemS2rl88rShLA+Q4d8Ap7p7LjV72SmCGFEA8BIA8n8c4MzQyg8ApSmFaFRn4obAqgzgaBI68pzga/zQ40zGanSnPURn49qFqgzLa/P3LBRr+fpkqgziag8Sq7Yc4MmQyMz7anSbqnRScnp/+AYGqfhIq98M49+UGfRSPr8BpFlsa9LIngbwagY68n8n4B+QzaRSzobFyBQ8aLMwwpm7agWM8/bl4e+jJ/8S+fhh/rSbzBpQypmTPSpTcLS9pFh3/L4EaLp08Skn4M+Q2rSez9uAq9kC/9LApdzGagYOq9zmP9pD8biRHjIj2eDjw0qA+0G7+AP9+UIj2erIH0iAP0SR',
        'x-t': '1682689158118',
    }
    session = requests.post(url,data='{}',headers=headers,cookies={}).json()['data']['session']
    return session

def feed(source_note_id):
    headers = {
        'authority': 'edith.xiaohongshu.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'xhsTrackerId=0aa97c49-0ecc-4519-9561-6c2a9b001960; xhsTrackerId.sig=AloePOx9ItgsrrdnH1g1uJdSZDXEWWbNzpRe5jF2e3U; xsecappid=xhs-pc-web; a1=187b334463dcaf4kzy8em3ycw3ev8sttn58p4y6mn50000381150; webId=b2cbb36a757bd1aa33ae163698242f5f; gid=yYWDqq44q8I0yYWDqq44K2vKqfS0i4TuvYd6Y6IqvSEqdU28hYM994888qYyy288Y42qDjJf; gid.sign=Ui/aW0yA8k/tuCiM1e44knL0uxg=; xhsTracker=url=explore&searchengine=baidu; xhsTracker.sig=u1cFYHAwm89lKbFLL1Y8vp9JcskioXWTa56RKaAB2ys; webBuild=2.3.1; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=f3a71ba5-8311-442a-bb3a-e0fb3db04226; extra_exp_ids=yamcha_0327_exp,h5_1208_exp3,ques_clt2; extra_exp_ids.sig=ETM51AFqVyLPOioG2x0qNaEzMLVwrEIN37uTpfkLqxc; web_session=040069b147824957be304a847e364bd6f33ca6',
        'origin': 'https://www.xiaohongshu.com',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-b3-traceid': '97bc1c22d46aed7c',
        'x-s': 'OgAb12O6OBM+Z2w6Z6FG1gcCs25GZgw6sB1K121LOg13',
        'x-s-common': '2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0P1PjhIHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHUN0P1PaHVHdWMH0ijP/W7G0PA+ec9P9z0GnGFy7kEwBpTP7S04A+S40YA4oz1+/YI+oD9JnhMPeZIPePhP/rMPsHVHdW9H0il+0WU+0WEP/LhP/rhNsQh+UHCHDRdcnHlPDu9/FQ+tMiU4A8y+D8oPn40c7PU+L4y87q9qFHlaArUPLlO8ArAHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafpr8bQhqgb78rS9cg+gcf+i4MmF4B4T+e8NpgkhanWIqAmPa7+xqg412/4rnDS9J7+hGSmx2n+McLSia9prG/4A8fzIJbmM4FFUpd49q9RMqrSe4nMwpAYN2S87LFSe89p3pdzH47b7zrSb/g+QyemS2rl88rShLA+Q4d8Ap7p7LjV72SmCGFEA8BIA8n8c4MzQyg8ApSmFaFRn4obAqgzgaBI68pzga/zQ40zGanSnPURn49qFqgzLa/P3LBRr+fpkqgziag8Sq7Yc4MmQyMz7anSbqnRScnp/+AYGqfhIq98M49+UGfRSPr8BpFlsa9LIngbwagY68n8n4B+QzaRSzobFyBQ8aLMwwpm7agWM8/bl4e+jJ/8S+fhh/rSbzBpQypmTPSpTcLS9pFh3/L4EaLp08Skn4M+Q2rSez9uAq9kC/9LApdzGagYOq9zmP9pD8biRHjIj2eDjw0qA+0G7+AP9+UIj2erIH0iAP0SR',
        'x-t': '1682689158118',
    }
    with open('x-s-t.js', 'r', encoding='utf-8') as f:
        js = f.read()
    crt = execjs.compile(js)
    data = '{"source_note_id":"%s"}'%source_note_id
    #print(data)
    result = crt.call('sign','/api/sns/web/v1/feed',{"source_note_id":"%s"%source_note_id})
    x_s = result["X-s"]
    x_t = result["X-t"]
    headers["x-s"]=x_s
    headers["x-t"]=str(x_t)
    # print(headers)
    feed = 'https://edith.xiaohongshu.com/api/sns/web/v1/feed'
    print(requests.post(url=feed, data=data, headers=headers).json())

if __name__ == '__main__':
    #print(register_session())
    result=feed("64106122000000001203d2fb")
