import execjs
from fake_useragent import UserAgent

douyin_js_obj = execjs.compile(open('douyin.js').read())
web_id = douyin_js_obj.call("get_web_id")

params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "cookie_enabled": "true",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Firefox",
        "browser_version": "110.0",
        "browser_online": "true",
        "engine_name": "Gecko",
        "os_name": "Windows",
        "os_version": "10",
        "engine_version": "109.0",
        "platform": "PC",
        "screen_width": "1920",
        "screen_height": "1200",
        # " webid": douyin_js_obj.call("get_web_id"),
        # "msToken": local_storage.get("xmst"),
        # "msToken": "abL8SeUTPa9-EToD8qfC7toScSADxpg6yLh2dbNcpWHzE0bT04txM_4UwquIcRvkRb9IU8sifwgM1Kwf1Lsld81o9Irt2_yNyUbbQPSUO8EfVlZJ_78FckDFnwVBVUVK",
    }

query = '&'.join([f'{k}={v}' for k, v in params.items()])
x_bogus = douyin_js_obj.call('sign', query, UserAgent().random)
print(web_id,x_bogus)