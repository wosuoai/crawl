import requests
from fake_useragent import UserAgent
import http.client
import json

def get_comment_param(detail_url: str) -> dict:
    """
        # 通过接口拿到随机的ttwid
    """
    conn = http.client.HTTPSConnection("tk.nsapps.cn")

    payload = '{\n  \"url\": \"%s\",\n  \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\"\n}' %(detail_url)

    headers = {'content-type': "application/json"}

    conn.request("POST", "/", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return eval(data)

def dy_comment_details(detail_url: str) -> dict:
    comment_param = get_comment_param(detail_url)["data"]
    headers = {
        'authority': 'www.douyin.com',
        'cookie': 'ttwid=' + comment_param["ttwid"],
        'referer': detail_url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(
        f'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={detail_url.split("video/")[-1]}&cursor=0&count=5&item_type=0&whale_cut_token=&cut_version=1&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=120.0.0.0&browser_online=true&engine_name=Blink&engine_version=120.0.0.0&os_name=Windows&os_version=10&cpu_core_num=24&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7288214080107677225&msToken={comment_param["mstoken"]}&X-Bogus={comment_param["xbogus"]}',
        headers=headers
    ).text.replace("null","None").replace("true", "True").replace("false", "False").replace('"{',"'{").replace('}"',"}'").replace("\n\n","")

    return eval(response)

print(dy_comment_details('https://www.douyin.com/video/7299767272908868883'))
