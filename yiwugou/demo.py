import re
import time
import requests
import html


proxies = {
    "http": None,
    "https": None,
}


def update_pro(pro_id, work_cookie, add_info: list):
    header = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.40 '
            'Safari/537.36 Edg/87.0.664.24',
        'cookie': work_cookie
    }
    url = 'https://work.yiwubuy.com/product_en/product_edit.htm?productId=' + str(pro_id) + '&&cpage=1'

    resp = requests.get(url=url, headers=header, verify=False, proxies=proxies)
    resp = resp.text
    p_id = re.findall(r'\"id\" value\=\"(\d+)\"', resp)

    n_p_id = ''
    bbscode = re.findall(r'bbscode\" value\=\"(.*?)\" \/\>', resp)
    entitle = re.findall(r'entitle\" value\=\"(.*?)\"\s*placeholder', resp)
    goodscode = ''
    x = 1
    images = []
    while x <= 10:
        image = re.findall(r'image' + str(x) + '\" value\=\"(.*?)\" ', resp)
        images.append(image)
        x += 1

    content = ''
    videoId = re.findall(r'videoId\" value\=\"(\d+)\" \/\>', resp)
    metric = re.findall(r'selected\"\>(.*?)\<\/option\>', resp)
    customMetric = re.findall(r'customMetric\" type\=\"text\" '
                              r'class\=\"input\_text w70 hide ml10\"\s*value\=\"(.*?)\" max', resp)
    priceType = re.findall(r'priceType\" checked value\=\"(\d+)\" class', resp)
    if not priceType:
        priceType = re.findall(r'priceType\" value\=\"(\d+)\" checked class', resp)
    startPrice = ''
    endPrice = ''
    prices = [['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']]
    if priceType[0] == '0':
        startPrice = re.findall(r'startPrice\" numonly\=\"\d\" maxlength\=\"\d\" value\=\"(.*?)\" \/\>', resp)
        endPrice = re.findall(r'endPrice\" numonly\=\"\d\" maxlength\=\"\d\" value\=\"(.*?)\" \/\>', resp)
        startPrice = startPrice[0]
        endPrice = endPrice[0]
    else:
        prices = [['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']]
        for k, v in enumerate(prices):
            p_s = 'price00'
            if k == 1:
                p_s = 'price10'
            elif k == 2:
                p_s = 'price20'
            elif k == 3:
                p_s = 'price03'
            elif k == 4:
                p_s = 'price13'
            elif k == 5:
                p_s = 'price23'
            p_s_re = p_s + '\"\\s*value=\\"(.*?)\\"'
            price = re.findall(p_s_re, resp)
            v[1] = price[0]
            v[0] = p_s
    enbrief = ''
    enintroduction = re.findall(r'<textarea.*?class="introduction requisite">([\s\S]*?)</textarea>', resp)
    enintroduction = html.unescape(enintroduction[0])
    for info in add_info:
        enintroduction = info + enintroduction

    length = re.findall(r'length\" value\=\"(\d+)\" maxlength', resp)
    if not length:
        length = ''
    width = re.findall(r'width\" value\=\"(\d+)\" maxlength', resp)
    if not width:
        width = ''
    height = re.findall(r'height\" value\=\"(\d+)\" maxlength', resp)
    if not height:
        height = ''
    shippingWeight = re.findall(r'shippingWeight\" value\=\"(\d+)\" maxlength\=\"', resp)
    if not shippingWeight:
        shippingWeight = ''
    packingQuantity = re.findall(r'packingQuantity\" value\=\"(\d+)\" maxlength\=\"', resp)
    if not packingQuantity:
        packingQuantity = ''
    onlineOrderFlag = re.findall(r'onlineOrderFlag\" checked value\=\"(\d)\" \/\>', resp)
    if not onlineOrderFlag:
        onlineOrderFlag = re.findall(r'onlineOrderFlag\" value\=\"(\d)\" checked \/\>', resp)
    if onlineOrderFlag == '1':
        salenum = re.findall(r'salenum\"\s*value\=\"(\d+)\" type', resp)
        deliveryPromise = re.findall(r'deliveryPromise\"\s*value\=\"(.*?)\" maxlength', resp)
        freightTemplateIdradio = re.findall(r'freightTemplateIdradio\" value\=\"(\d+)\" checked', resp)
        freightTemplateId = re.findall(r'请选择运费模板\<\/option\>\s*\<option value\=\"(\d+)\" data\-type', resp)
        freedelivery = re.findall(r'freedelivery\"\s*value\=\"(\d+)\"\s*numOnly', resp)
        freight = re.findall(r'freight\"\s*numOnly\=\d\s*maxlength\=\d+\s*value\=\"(.*?)\" \/\>', resp)
    else:
        salenum = deliveryPromise = freightTemplateIdradio = freightTemplateId = freedelivery = freight = ''
    date = {
        'id': p_id[0],
        'newProductId': n_p_id,
        'bbscode': bbscode[0],
        'entitle': entitle[0],
        'goodscode': goodscode,
        'image1': images[0][0],
        'smallpic1': images[0][0],
        'image2': images[1][0],
        'smallpic2': images[1][0],
        'image3': images[2][0],
        'smallpic3': images[2][0],
        'image4': images[3][0],
        'smallpic4': images[3][0],
        'image5': images[4][0],
        'smallpic5': images[4][0],
        'image6': images[5][0],
        'smallpic6': images[5][0],
        'image7': images[6][0],
        'smallpic7': images[6][0],
        'image8': images[7][0],
        'smallpic8': images[7][0],
        'image9': images[8][0],
        'smallpic9': images[8][0],
        'image10': images[9][0],
        'smallpic10': images[9][0],
        'proimg3d': '0',
        'type': '0',
        'content': '',
        'videoId': videoId[0],
        'metric': metric[0],
        'customMetric': customMetric[0],
        'priceType': priceType[0],
        'startPrice': startPrice,
        'endPrice': endPrice,
        'price00': prices[0][1],
        'price03': prices[3][1],
        'price10': prices[1][1],
        'price13': prices[4][1],
        'price20': prices[2][1],
        'price23': prices[5][1],
        'enbrief': enbrief,
        'enintroduction': enintroduction,
        'length': length,
        'width': width,
        'height': height,
        'shippingWeight': shippingWeight,
        'packingQuantity': packingQuantity,
        'onlineOrderFlag': onlineOrderFlag,
        'salenum': salenum,
        'deliveryPromise': deliveryPromise,
        'freightTemplateIdradio': freightTemplateIdradio,
        'freightTemplateId': freightTemplateId,
        'freedelivery': freedelivery,
        'freight': freight
    }
    url = 'https://work.yiwubuy.com/product_en/ajax_insert.htm?cpage=1'
    insert_info = requests.post(url=url, headers=header, data=date, verify=False, proxies=proxies)
    print(pro_id, insert_info.text)


def get_pro_id(work_cookie: str, page_index: int, all_pro: list):
    header = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.40 '
            'Safari/537.36 Edg/87.0.664.24',
        'cookie': work_cookie
    }
    url = 'https://work.yiwubuy.com/product_en/productlist/' + str(page_index) + '.htm?t=1&pageSize=100'
    res = requests.get(url=url, headers=header, verify=False, proxies=proxies)
    pro_id = re.findall(r'name\=\"checkname\" value\=\"(\d+)\" \/\>', res.text)
    if len(pro_id) == 100:
        page_index += 1
        all_pro.append(pro_id)
        if page_index == 11:
            return all_pro
        get_pro_id(work_cookie, page_index, all_pro)

        time.sleep(2)
    return all_pro


if __name__ == '__main__':
    cookie = 'syncPicZone=; u_c_c_a=1089gkcgkyoderUrTRyy9KZKPbInddHuMhzCdQ4ikNhRhftj6oZI97gCSPJRnHDpHSo04uTYUxpcWUkHYg;' \
             ' yiwugouuauth=55baf4s+Zgq1zP11eqvyonRmuS3V/zbYTv62O98Z+5cjmpBO8rNvq535Xf/bqhcvNzIHez6Wt9ffHMvr4oK8; ' \
             'c_u_i=244cc07d7c75a56573db7fbec4d26b1e; JSESSIONID=056698B76293E7F9E40768E722D9C46F'

    add_info = [
        '<img alt="主图.jpg" height="790" '
        'src="http://ywgimg.yiwugo.com/product/shop_273700/en/946439929/20230509/69IbfQb6b792aDWI.jpg" width="790" />',
        '<img alt="主图.jpg" height="790" '
        'src="http://ywgimg.yiwugo.com/product/shop_273700/en/946439929/20230509/b9RXIo9klAa3o6Ap.jpg" width="790" />',
    ]
    pro_ids = get_pro_id(work_cookie=cookie, page_index=1, all_pro=[])
    for k, i in enumerate(pro_ids):
        if k == 0:
            print('第一组跳过')
            continue
        for x in i:
            update_pro(x, cookie, add_info)
            time.sleep(1.5)
