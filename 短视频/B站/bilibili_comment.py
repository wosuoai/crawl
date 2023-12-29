import requests
from fake_useragent import UserAgent
from bilibili_data import get_oid

#comment = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=279857984&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=1996e56b8e83b4115e19e1c5a0933b76&wts=1703237148'

def bili_comment_oid(share_url: str) -> str:
    """
    评论接口参数 -> oid -> aid -> 可通过静态接口直接提取
    :return:
    """
    headers = {
        'authority': 'www.bilibili.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': UserAgent().random,
    }

    bilibili_html = requests.get(share_url, headers=headers).text.replace("\n", "").replace(" ", "")
    return get_oid(bilibili_html)

def bili_comment_rid() -> str:
    """
    评论接口参数 -> w_rid
    :return:
    """
    pass

def bili_comment_wts() -> str:
    """
    评论接口参数 -> wts(时间戳)
    :return:
    """
    pass

def bili_comment_url(oid: str, rid: str, wts: str) -> str:
    """
    :issue -> w_rid,wts
    :return:
    """
    comment_url = f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid={rid}&wts={wts}'
    return comment_url

def bili_comment_details(share_url: str, comment_url: str) -> dict:
    """
    B站评论信息
    """
    headers = {
        'authority': 'api.bilibili.com',
        'origin': 'https://www.bilibili.com',
        'referer': share_url,
        'user-agent': UserAgent().random,
    }

    bili_comment = requests.get(comment_url, headers=headers).json()
    return bili_comment