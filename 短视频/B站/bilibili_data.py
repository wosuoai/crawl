import requests
from fake_useragent import UserAgent
import re

def bilibili_real_weburl(share_url: str) -> str:
    """
    正则提取用户的分享链接
    :param share_url:
    :return:
    """
    if "【" in share_url:
        url_value = re.search(r'https://[^?]+\?', share_url)
        return url_value.group(0)[:-1]
    else:
        return share_url

def get_real_html(real_url: str) -> str:
    """
    调取B站静态接口
    :param real_url:
    :return:
    """
    headers = {
        'authority': 'www.bilibili.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': UserAgent().random,
    }

    bilibili_html = requests.get(real_url, headers=headers).text.replace("\n","").replace(" ","")
    return bilibili_html

def get_video_link(html_body: str) -> dict:
    """
    正则提取需要的有效信息
    :param html_body:
    :return:
    """
    author = re.search(r'name="author"content="(.*?)">', html_body).group(1)  # 作者
    title = re.search(r'name="title"content="(.*?)">', html_body).group(1).replace("_哔哩哔哩_bilibili","")  # 标题
    desc = re.search(r'name="description"content="(.*?)">', html_body).group(1).split(",视频播放量")[0]  # 正文
    tags = re.search(r'name="keywords"content="(.*?)">', html_body).group(1).split(",")[1:-4]  # 标签
    real_video_url = re.search(r'"base_url":"(.*?)"', html_body).group(1)  # B站视频链接
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "music": "", "video_without_mp3": "", "first_img": "", "real_video_url": real_video_url, "link_type": 1, "method_code": 0})
    return detail_dict

def get_oid(html_body: str) -> str:
    """
    aid是评论接口的一个必要参数
    :param html_body:
    :return:
    """
    oid = re.search(r'"aid":(\d+)', html_body).group(1)
    return oid

def analyze_bilibili():
    share_url = "https://www.bilibili.com/video/BV1xc411m7x2/"
    return get_video_link(get_real_html(bilibili_real_weburl(share_url)))

print(analyze_bilibili())