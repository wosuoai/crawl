import re
import requests
from fake_useragent import UserAgent
import logging

def redbook_real_weburl(share_url: str) -> str:
    """
        处理及判断用户传入的url
    """
    if "复制本条信息，打开【小红书】App查看精彩内容！" in share_url:
        url_match = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', share_url)
        target_url = url_match[0]
        return target_url
    else:
        return share_url

def redbook_real_imgurl(target_url: str) -> list:
    """
        调取静态接口解析无水印的url链接
    """
    headers = {
        'authority': 'www.xiaohongshu.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': UserAgent().random,
    }

    img_html = requests.get(target_url, headers=headers).text.replace("\\u002F", "/").replace("\n", "").replace(" ","")  # 调取静态接口
    url_pattern = re.compile(r'"url":"(.*?)"')
    img_url = url_pattern.findall(img_html)
    if len(img_url) > 0:
        img_url = list(set([url for url in img_url if 'wm_1' in url]))
    return img_url

def analyze_redbook(redbook_share_url: str):
    try:
        # 传入参数 --> 小红书分享的url
        user_input_url = redbook_share_url

        target_url = redbook_real_weburl(user_input_url)
        real_img_url = redbook_real_imgurl(target_url)

        logging.info(f"用户传入url解析成功：{real_img_url}")
        return {'exist': real_img_url}
    except Exception as error:
        logging.error(f"解析错误：{error}")