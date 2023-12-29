import json
import re
import time
import requests
import hashlib
from pygments import highlight, lexers, formatters


"""
if (!0 === r.H5Request) {
    var i = "//" + (r.prefix ? r.prefix + "." : "") + (r.subDomain ? r.subDomain + "." : "") + r.mainDomain + "/h5/" + n.api.toLowerCase() + "/" + n.v.toLowerCase() + "/"
      , a = n.appKey || ("waptest" === r.subDomain ? "4272" : "12574478")
      , s = (new Date).getTime()
      , l = u(r.token + "&" + s + "&" + a + "&" + n.data)
      , c = {
        jsv: k,
        appKey: a,
        t: s,
        sign: l
    }
      , f = {
        data: n.data,
        ua: n.ua
    };
"""

def get_sign(string):
    return hashlib.md5(string.encode()).hexdigest()


def req(sign,now,data):
    cookies = {
        #添加你自己的cookies
    }

    headers = {
        'authority': 'h5api.m.tmall.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'referer': 'https://detail.tmall.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'jsv': '2.7.0',
        'appKey': '12574478',
        't': now,
        'sign': sign,
        'api': 'mtop.alibaba.review.list.for.new.pc.detail',
        'v': '1.0',
        'isSec': '0',
        'ecode': '0',
        'timeout': '10000',
        'ttid': '2022@taobao_litepc_9.17.0',
        'AntiFlood': 'true',
        'AntiCreep': 'true',
        'preventFallback': 'true',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp3',
        'data': data,
    }

    response = requests.get(
        'https://h5api.m.tmall.com/h5/mtop.alibaba.review.list.for.new.pc.detail/1.0/',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    json_str = re.findall(r'mtopjsonp3\((.*?)\)',response.text)
    content = json.loads(json_str[0])
    formatted_json = json.dumps(content, indent = 4, ensure_ascii = False, sort_keys = True)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

def get_time_13():
    return int(time.time()*1000)


s=time.time()*1000  #13位数时间戳
a='12574478' #appkey
token = "0978c19acf33059456da04eb34559867" #_m_h5_tk
#token = re.findall('_m_h5_tk=(.*?)_', cookie)[0]
#请求参数data
data='{"appId":"34385","params":"{\"device\":\"HMA-AL00\",\"isBeta\":\"false\",\"grayHair\":\"false\",\"from\":\"nt_history\",\"brand\":\"HUAWEI\",\"info\":\"wifi\",\"index\":\"4\",\"rainbow\":\"\",\"schemaType\":\"auction\",\"elderHome\":\"false\",\"isEnterSrpSearch\":\"true\",\"newSearch\":\"false\",\"network\":\"wifi\",\"subtype\":\"\",\"hasPreposeFilter\":\"false\",\"prepositionVersion\":\"v2\",\"client_os\":\"Android\",\"gpsEnabled\":\"false\",\"searchDoorFrom\":\"srp\",\"debug_rerankNewOpenCard\":\"false\",\"homePageVersion\":\"v7\",\"searchElderHomeOpen\":\"false\",\"search_action\":\"initiative\",\"sugg\":\"_4_1\",\"sversion\":\"13.6\",\"style\":\"list\",\"ttid\":\"600000@taobao_pc_10.7.0\",\"needTabs\":\"true\",\"areaCode\":\"CN\",\"vm\":\"nw\",\"countryNum\":\"156\",\"m\":\"pc\",\"page\":1,\"n\":48,\"q\":\"%E8%BF%9E%E8%A1%A3%E8%A3%99\",\"tab\":\"all\",\"pageSize\":48,\"totalPage\":100,\"totalResults\":4800,\"sourceS\":\"0\",\"sort\":\"_coefp\",\"bcoffset\":\"\",\"ntoffset\":\"\",\"filterTag\":\"\",\"service\":\"\",\"prop\":\"\",\"loc\":\"\",\"start_price\":null,\"end_price\":null,\"startPrice\":null,\"endPrice\":null,\"itemIds\":null,\"p4pIds\":null}"}'

# 结果比对不上 说明魔改过
str_data = token + "&" + str(1693280731070) + "&" + a + "&" + data
sign = hashlib.md5(str_data.encode(encoding='utf-8')).hexdigest()
print(sign)