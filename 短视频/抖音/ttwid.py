import requests,re

def get_ttwid():
    try:
        url = 'https://ttwid.bytedance.com/ttwid/union/register/'
        data = {
            "region": "cn",
            "aid": 1768,
            "needFid": False,
            "service": "www.ixigua.com",
            "migrate_info": {"ticket": "", "source": "node"},
            "cbUrlProtocol": "https",
            "union": True
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        set_cookie = response.headers.get('set-cookie', '')
        regex = re.compile(r'ttwid=([^;]+)')
        match = regex.search(set_cookie)

        return "ttwid=" + match.group(1) if match else ''
    except Exception as error:
        print(error)
        return ''

print(get_ttwid())