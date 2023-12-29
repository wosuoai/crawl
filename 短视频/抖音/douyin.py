import http.client
import re
import requests
import secrets
from fake_useragent import UserAgent

def parse_share_url(share_url: str) -> str:
    """
        解析分享的url指向的网页视频url
    """
    path = share_url.split("v.douyin.com")[1]
    conn = http.client.HTTPSConnection('v.douyin.com')
    headers = {
        'Host': 'v.douyin.com',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    conn.request('GET', '%s' % path, headers=headers)
    response = conn.getresponse()
    response_text = response.read().decode('utf-8')
    # 使用正则表达式提取href属性
    href_match = re.search(r'href="([^"]+)"', response_text)
    try:
        if href_match:
            href_value = href_match.group(1)
            video_id_match = re.search(r'/video/(\d+)/', href_value)
            return "https://www.douyin.com/video/" + video_id_match.group(1)
        else:
            return ""
    except:
        return ""


def return_detail_url(web_video_url: str) -> str:
    """
        解析实际有用的接口链接
    """
    web_video_id = web_video_url.split("video/")[1]
    detail_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={web_video_id}"

    return detail_url

def parse_real_video(web_video_url: str, detail_url: str, cookie: str) -> str:
    """
        解析无水印的url链接
    """
    try:
        headers = {
            "accept": "application/json, text/plain, */*",
            "cookie": cookie,
            "referer": web_video_url,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

        response = requests.post(detail_url, headers=headers)
        real_video_id = response.json()['aweme_detail']['video']['play_addr']['uri']
        return "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + real_video_id + "&ratio=720p&line=0"
    except Exception as error:
        return ""

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

def get_real_down_url(share_url:str)->str:
    """
        如果返回为空字符串表示没有成功解析
    """
    web_url = parse_share_url(share_url)
    detail_url = return_detail_url(web_url)
    cookie = get_ttwid(detail_url)
    real_download_url = parse_real_video(web_url, detail_url, cookie)
    return real_download_url
    
if __name__ == "__main__":
    # cookie = 'ttwid=1%7CG1TS9FeQ3OC4MIuEsRlACKjAHWUseFC9I-cAErCorDs%7C1685626204%7C2f77d48479c4448be7bbbdf751dea434a8f8fca503539f80c1fbee136a7a9d32; xgplayer_device_id=97270984555; xgplayer_user_id=980450083250; passport_csrf_token=8df3e07ff183ff9cea173be85da37d45; passport_csrf_token_default=8df3e07ff183ff9cea173be85da37d45; s_v_web_id=verify_loijf1lw_Ce6TnMrh_j583_4jQ9_9nFa_AINoHatIjSww; passport_assist_user=CkG1-viGXMVqjveYwV1jDlOuIlOkSNmCA1g82uBH5OoDs9ode1OEz3YYljrdwIihbYwZJ-EhSqnhQB_FaptEj2ChAhpKCjzocE5kWc79GPHfuBp7P3dLq6OAS8E7yloutEjOuBH5D8LJ2wCPVBLuhuzzkY-QT4FIcg8bir2u5QFv2OAQ0rXADRiJr9ZUIAEiAQPMvA6p; n_mh=imFUQe7lisct_mqRlyHY6nH48nYtSM886xeMvaj_EDQ; sso_uid_tt=ee59efb27e28b24ba61c41d41e899754; sso_uid_tt_ss=ee59efb27e28b24ba61c41d41e899754; toutiao_sso_user=2a8ffd6b25951f5096e29569180b4b94; toutiao_sso_user_ss=2a8ffd6b25951f5096e29569180b4b94; passport_auth_status=1c4f9e391b40df1ed4ccdd12af82eaa2%2C; passport_auth_status_ss=1c4f9e391b40df1ed4ccdd12af82eaa2%2C; uid_tt=6181cff231ca7f675b78a94a75708b6d; uid_tt_ss=6181cff231ca7f675b78a94a75708b6d; sid_tt=abc5a5a8a0d8b7d4ec147c9f1430d005; sessionid=abc5a5a8a0d8b7d4ec147c9f1430d005; sessionid_ss=abc5a5a8a0d8b7d4ec147c9f1430d005; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=52c21ee9e04462ea8be379f9fac3c566; __security_server_data_status=1; LOGIN_STATUS=1; store-region=cn-zj; store-region-src=uid; csrf_session_id=bedb5fd1221df14d178779fe41f91306; douyin.com; xg_device_score=18.705882352941178; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; __live_version__=%221.1.1.5614%22; live_use_vvc=%22false%22; webcast_leading_last_show_time=1700570611837; webcast_leading_total_show_times=1; webcast_local_quality=ld; publish_badge_show_info=%220%2C0%2C0%2C1701344792599%22; dy_swidth=1536; dy_sheight=864; strategyABtestKey=%221701344793.636%22; bd_ticket_guard_client_web_domain=2; sid_ucp_sso_v1=1.0.0-KDc5ZDI3OTQwZTIzNjMyMGUyMmM4ZDA4ZDRhZDVkYjRiYWRiMmRiODIKHwiU9LCO5PXYBBCb7KGrBhjvMSAMMPi5kOcFOAZA9AcaAmxmIiAyYThmZmQ2YjI1OTUxZjUwOTZlMjk1NjkxODBiNGI5NA; ssid_ucp_sso_v1=1.0.0-KDc5ZDI3OTQwZTIzNjMyMGUyMmM4ZDA4ZDRhZDVkYjRiYWRiMmRiODIKHwiU9LCO5PXYBBCb7KGrBhjvMSAMMPi5kOcFOAZA9AcaAmxmIiAyYThmZmQ2YjI1OTUxZjUwOTZlMjk1NjkxODBiNGI5NA; sid_guard=abc5a5a8a0d8b7d4ec147c9f1430d005%7C1701344796%7C5184000%7CMon%2C+29-Jan-2024+11%3A46%3A36+GMT; sid_ucp_v1=1.0.0-KGUxZTBiYjI0NjZhNzI3ZDE4Y2ExNjIxYjY2NzJmYzBmN2ZiN2RiMDcKGwiU9LCO5PXYBBCc7KGrBhjvMSAMOAZA9AdIBBoCbHEiIGFiYzVhNWE4YTBkOGI3ZDRlYzE0N2M5ZjE0MzBkMDA1; ssid_ucp_v1=1.0.0-KGUxZTBiYjI0NjZhNzI3ZDE4Y2ExNjIxYjY2NzJmYzBmN2ZiN2RiMDcKGwiU9LCO5PXYBBCc7KGrBhjvMSAMOAZA9AdIBBoCbHEiIGFiYzVhNWE4YTBkOGI3ZDRlYzE0N2M5ZjE0MzBkMDA1; passport_fe_beating_status=true; download_guide=%223%2F20231130%2F0%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.4%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRjVQM25GUmZzeEtLUWx6ZGM2MFJ6a3gzMFRZSmt0TGp6UWVMMGcvUnNmRnZqekVXeTZWS2VkaXdNQy9SbVZzanFHNTF0aUY4ci9OMkFsbE9VbTM3VDA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=hGSAKJhdERKQP_c2mDGFg7YSTnY4gCkd9ysfBqqN1Or9p4REVGKSCheasVm3ESX3DLfOgDUxDxceo2xcbifvwyw3RXLwjL5asQ-xMjjAunr7agXPp2qa4leVdztsA8iT; msToken=yni4BQCIeX5BDQ_0UEkBkUEw-tec95XTZQY5qrrVT5SFIetbETnl_3hxX1hSYe37BZeVFebDlnxN-_w_Li7t5tzWDJ3UTXYt7OGNOAl5Gjy_O94m6c2YEHLszebLp4re; tt_scid=LQefsipmF0chDXw-PnND.kbawiTLE-v72KvlxuF0IviUgB.bRKfhwxDL3IpvT3VS0609; odin_tt=fbd0c6046a2d3c419824af48665ce1ca8aa63218c64473ba3bb40137b149f74f5ca3a39ecbf2255f1d228a3006e9395b; __ac_nonce=06568aad000e89bf8d220; __ac_signature=_02B4Z6wo00f01ylIQOgAAIDCAsIbLbQj1T8paERAAK9FF1MIEerwjkr-s8AaGRGS6gLRCFBkbrUCaT8K9mhDH2OajDydcIilPfi7nXOBkv4MulBVV4TLwQyveuYrRcafeKM-Mb4PltR3hs2Y07; home_can_add_dy_2_desktop=%220%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAATwSj50ihoR3vhi9aJArsPYE_IZg3aibiUAbPmayYT4-YJKxn62394tVYn8gXbjDr%2F1701360000000%2F0%2F0%2F1701358890193%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAATwSj50ihoR3vhi9aJArsPYE_IZg3aibiUAbPmayYT4-YJKxn62394tVYn8gXbjDr%2F1701360000000%2F0%2F1701358290194%2F0%22; IsDouyinActive=false'
    # cookie = get_ttwid()
    # cookie = 'douyin.com; xgplayer_device_id=97270984555; xgplayer_user_id=980450083250; passport_csrf_token=8df3e07ff183ff9cea173be85da37d45; passport_csrf_token_default=8df3e07ff183ff9cea173be85da37d45; s_v_web_id=verify_loijf1lw_Ce6TnMrh_j583_4jQ9_9nFa_AINoHatIjSww; passport_assist_user=CkG1-viGXMVqjveYwV1jDlOuIlOkSNmCA1g82uBH5OoDs9ode1OEz3YYljrdwIihbYwZJ-EhSqnhQB_FaptEj2ChAhpKCjzocE5kWc79GPHfuBp7P3dLq6OAS8E7yloutEjOuBH5D8LJ2wCPVBLuhuzzkY-QT4FIcg8bir2u5QFv2OAQ0rXADRiJr9ZUIAEiAQPMvA6p; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=52c21ee9e04462ea8be379f9fac3c566; __security_server_data_status=1; LOGIN_STATUS=1; csrf_session_id=bedb5fd1221df14d178779fe41f91306; douyin.com; xg_device_score=18.705882352941178; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; __live_version__=%221.1.1.5614%22; live_use_vvc=%22false%22; webcast_leading_last_show_time=1700570611837; webcast_leading_total_show_times=1; webcast_local_quality=ld; publish_badge_show_info=%220%2C0%2C0%2C1701344792599%22; dy_swidth=1536; dy_sheight=864; strategyABtestKey=%221701344793.636%22; bd_ticket_guard_client_web_domain=2; passport_fe_beating_status=true; download_guide=%223%2F20231130%2F0%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.4%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; __ac_nonce=06568aad000e89bf8d220; __ac_signature=_02B4Z6wo00f01ylIQOgAAIDCAsIbLbQj1T8paERAAK9FF1MIEerwjkr-s8AaGRGS6gLRCFBkbrUCaT8K9mhDH2OajDydcIilPfi7nXOBkv4MulBVV4TLwQyveuYrRcafeKM-Mb4PltR3hs2Y07; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAATwSj50ihoR3vhi9aJArsPYE_IZg3aibiUAbPmayYT4-YJKxn62394tVYn8gXbjDr%2F1701360000000%2F0%2F0%2F1701358890193%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAATwSj50ihoR3vhi9aJArsPYE_IZg3aibiUAbPmayYT4-YJKxn62394tVYn8gXbjDr%2F1701360000000%2F0%2F1701358290194%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRjVQM25GUmZzeEtLUWx6ZGM2MFJ6a3gzMFRZSmt0TGp6UWVMMGcvUnNmRnZqekVXeTZWS2VkaXdNQy9SbVZzanFHNTF0aUY4ci9OMkFsbE9VbTM3VDA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=C-CzGuFEYlty3nyErjamdce4CoI3VB5EjkHkhjmna-8AyAEB6Qv8XTCjQGB0-Nizqv7q0lRLG1V_YiXrGbJ_KXKOvYIs9G6H2XectvGI7M3TCYYKiBrN246cd2w0q2bj; home_can_add_dy_2_desktop=%221%22; tt_scid=Kkz13ty1u9U-kxzw-ibP5M.5eAbPKLh.b8lJovuIXr8AFWYblfNHEx4QjJmL2TMY1e6d; IsDouyinActive=true; msToken=dId4MwojCoW7LW2G1t7ql75QRupRQunXjgp6kYvCyfiSS443L7Kb2xGb_2JkprF1JMcyzIbCx6KrDwKsyRltsuNKYVJtbAM9XoPgfLJEeslIP59wnIsEzYtnM87TtATh'
    print(get_real_down_url("https://v.douyin.com/iR7f3njW/"))
    # print(parse_share_url("https://v.douyin.com/iRvk7Abb/"))
    # print(parse_real_video("https://www.douyin.com/video/7299767272908868883"))
    # print(parse_real_video("https://www.douyin.com/video/7306891498358934838"))