import re
import random
import requests
import http.client
from fake_useragent import UserAgent

def parse_share_url(share_url: str) -> str:
    """
        解析分享的url指向的网页视频url
    """
    path = share_url.split("v.douyin.com")[1]
    conn = http.client.HTTPSConnection('v.douyin.com')
    headers = {
        'Host': 'v.douyin.com',
        'user-agent': UserAgent().random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    conn.request('GET', '%s' % path, headers=headers)
    response = conn.getresponse()
    response_text = response.read().decode('utf-8')
    # 使用正则表达式提取href属性
    href_match = re.search(r'href="([^"]+)"', response_text)

    try:
        # 抖音笔记链接
        href_value = href_match.group(1)
        note_id_match = re.search(r'/note/(\d+)/', href_value)
        return "https://www.douyin.com/note/" + note_id_match.group(1)
    except:
        # 抖音视频链接
        href_value = href_match.group(1)
        video_id_match = re.search(r'/video/(\d+)/', href_value)
        return "https://www.douyin.com/video/" + video_id_match.group(1)

def get_ac_nonce() -> str:
    """
        抖音__ac_nonce参数
    """
    sess = requests.session()
    headers_base = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    sess.headers = headers_base
    url = 'https://www.douyin.com'
    __ac_nonce = sess.get(url, headers=headers_base).cookies.get('__ac_nonce')
    return __ac_nonce

def parse_real_imgurl(web_img_url: str) -> list:
    """
        解析抖音无水印的图片url链接
    """
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie': '__ac_nonce=06192fe1600efd2f548a4; __ac_signature=_02B4Z6wo00f010oZ.OAAAIDDSL4VSgFGbQNKOPhAALMfzkcLVN8kvHY8F8.4A5amrjhSxq1fBh5cV3Mb3lmu6n1vBZEZ7g2-OJbAE0HGGN.q9D4vlb32.SAnb8XjxYYKuIgSkmi4eQazA1DF9a',
        'user-agent': UserAgent().random,
    }

    response = requests.get(web_img_url, headers=headers)
    pattern = re.compile(r'src="(https\:\/\/[^"]+?tplv\-dy\-aweme\-images:[^"]+)"')

    # 提取所有的图片并去重
    img_links = pattern.findall(response.text.replace("amp;", ""))
    img_links = list(set(img_links))
    return img_links

def return_detail_url(web_video_url: str) -> str:
    """
        解析实际有用的接口链接
    """
    web_video_id = web_video_url.split("video/")[1]
    detail_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={web_video_id}"

    return detail_url

def get_ttwid(detail_url: str) -> str:
    """
        # 通过接口拿到随机的ttwid
    """
    conn = http.client.HTTPSConnection("tk.nsapps.cn")

    payload = '{\n  \"url\": \"%s\",\n  \"userAgent\": \"%s\"\n}' %(detail_url,UserAgent().random)

    headers = {'content-type': "application/json"}

    conn.request("POST", "/", payload, headers)

    res = conn.getresponse()
    data = res.read()
    ttwid_value = "ttwid=" + re.search(r'"ttwid":"(.*?)"', data.decode("utf-8")).group(1)
    return ttwid_value

def parse_real_video(web_video_url: str, detail_url: str, cookie: str) -> str:
    """
        解析无水印的url链接
    """
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "cookie": cookie,
            "referer": web_video_url,
            "user-agent": UserAgent().random,
        }

        response = requests.post(detail_url, headers=headers)
        real_video_id = response.json()['aweme_detail']['video']['play_addr']['uri']
        return "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + real_video_id + "&ratio=720p&line=0"
    except Exception as error:
        return ""

def analyze_douyin(douyin_share_url: str):
    """
        如果返回为空字符串表示没有成功解析
    """
    try:
        # 传入参数 --> 抖音分享的url
        share_url = re.search(r'https?://\S+', douyin_share_url).group()
        web_url = parse_share_url(share_url)
        if "video" in web_url:
            detail_url = return_detail_url(web_url)
            cookie = get_ttwid(detail_url)
            real_download_url = parse_real_video(web_url, detail_url, cookie)
        else:
            real_download_url = parse_real_imgurl(web_url)
        return {'exist': real_download_url}
    except Exception as error:
        return ""