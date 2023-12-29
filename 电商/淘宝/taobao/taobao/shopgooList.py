import requests

cookies = {'tfstk': 'dlPWfDxYb3x7OFljXL_4C6IvJIcCbu1NdegLSydyJbhRO-agA07hEbyjAoEj2YJPZ2hQDk7o4yFEJWGug8RE4gcQJllCbG5N_z4oEXINb4qurz0R4xhA_1zurXcdbG5Nx8a1AtYTGaMZferXr6fI2YiTPOApOSOZFcU-cB30GOue_cw5cpTjIBgjbZ_XKpfKR2ff.', 'l': 'fBg6RSc4N3uVhQtDBOfaFurza77OSIRYYuPzaNbMi9fPOTCB5gINW1tQODL6C3GVF609R3-WjmOpBeYBqQAonxv9w8VMULkmndLHR35..', 'uc1': 'pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie21=VT5L2FSpdiBh&existShop=false&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie14=Uoe9bjCRCwpbgg%3D%3D', '_nk_': 'tb539911461186', '_l_g_': 'Ug%3D%3D', 'cookie1': 'VFCsDnfbj2W0HSQ1IYxUhPCpRlWMdi9NDzEb9OnLyMY%3D', 'dnk': 'tb539911461186', 'cancelledSubSites': 'empty', 'sg': '684', 'mt': 'ci=0_1', 'lgc': 'tb539911461186', 'csg': '8d600ce3', 'uc3': 'id2=UUpgQEvzZtFYxW785g%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCsGZGVMVQQJrk59g%3D&nk2=F5RAQUDDgWyfX4761mw%3D', 'unb': '2216216378928', 'cookie2': '2c90ce0a6163b2419983c8030ce68ed2', 'uc4': 'id4=0%40U2gqz6QZKRM7HGaO1puEMtf5g5PAPAOe&nk4=0%40FY4L7Q88XzzMISuYV%2BJR4ZwuO%2BxsHSH11w%3D%3D', '_tb_token_': 'f18b903e4f710', '_samesite_flag_': 'true', 'existShop': 'MTY5MzI5NDc1Ng%3D%3D', '_m_h5_tk_enc': 'bff1111896685fae7d1c827bf15cd0ed', '_m_h5_tk': 'a08175a5fb37d5ac1dafad46b74fc229_1693195978200', '_cc_': 'VFC%2FuZ9ajQ%3D%3D', 'cookie17': 'UUpgQEvzZtFYxW785g%3D%3D', 'xlly_s': '1', 'isg': 'BHt7DpJhm2_ZtaePrhxlYWVXCl_l0I_SEepdLW04VnqRzJqu4aU7IzYe4GyCd-fK', 'skt': '6418098a7fce3e40', 'sgcookie': 'E100lBsLZE9fWiQHedFB6mof9SAxsXpozgjLr4uhE2oxhutlZ3SgXYIERvYbjQz9WuIcwhkZHNxhqbHU1dsWm8be%2B5wTHQ5cXXxEv6wVack6kww%3D', 't': 'be650f779bda6984ae19184e3075c83c', 'cna': 'duFAHTR2tzYCAX158qGMeKOh', 'thw': 'cn', 'tracknick': 'tb539911461186'}

headers = {
    'authority': 'shop114791417.taobao.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    # 'cookie': 'thw=cn; cna=AbGRHJxN6koCAW8CWyaOFU9H; lgc=tb80111606; tracknick=tb80111606; t=a2fbed6ac298d9add775152474982d05; xlly_s=1; sgcookie=E100SYKotXAF5Z4hSeDFiWucBWoG4cD4PXUQQSksIrE0jzii6fefO1a1lQZlw0DxviCUkJV85IGPMWzWfQ8om7gUyXZAqejDMufSXBOsp8SjuZh%2B%2B5ZI9Ff6%2FKsBH%2BY%2FgIPo; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&nk2=F5RNZTse5XZpwA%3D%3D&vt3=F8dCsGGr97%2FSV4zQRi0%3D&id2=UNQyQxMqUdx1nQ%3D%3D; uc4=nk4=0%40FY4GsvRHfRNKE%2BdeKAjFMK4XROY0&id4=0%40UgP5GPE5h%2FvopPV87sjzIk3lA3%2Bp; _cc_=URm48syIZQ%3D%3D; mt=ci=-1_0; _m_h5_tk=8e85ca8f961b60be669b665a8bbe8a51_1690188914170; _m_h5_tk_enc=68f434bb860736dc0d298384a4080901; cookie2=1ca0aad2f0923006292c74d6b587996e; _tb_token_=ee33353675b33; arms_uid=1d59dbee-62ec-4c71-ad51-e8a63cb052fc; uc1=cookie14=Uoe9bfwIyf8Yog%3D%3D; isg=BHl5Fqj5Odboh-Vrsc3WJbNeiOVThm04KaayZZuvzKB8Ipi04tb1Cb0zoCbUmgVw; l=fBSck9QeNgpDv8D5BO5Clurza77TwIOb8sPzaNbMiIEGa1yF9p9uwNC18tivWdtjgT5c1eKrip0J_dUkJ2U38FkDBeYQtkbd_Up6-eM3N7AN.; tfstk=dMdvXBg720m09xW91ZHo_RrD2x3oEILVwn8QsGj0C3KJ5nscjt6fPu_cW5_bGF_163tiuiYs0hdOVs6wnGjcX1Lwv4mntXY2u15IxDchBF4Ns-0HPOIr6E5N1D4u1vcpuHulcTsG6Vz0loVDiB7jCcD918K8DZXAAUHU65aCukjpl7VT6QpRyORHtBB9NkjdS-g-yRyNhaRaoYbF.',
    'referer': 'https://shop114791417.taobao.com/?spm=a230r.7195193.1997079397.2.50af6831gaOAhw',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

params = {
    'pageSize': '20',
    'shopId': '114791417',
    'page': '1',
    'sortType': 'des',
    # 'orderType': 'popular',
    'appUid': 'RAzN8BQwukorVdqYGeiXsjZbVA5Xw',
}

response = requests.get('https://shop114791417.taobao.com/getShopItemList.htm', params=params, cookies=cookies, headers=headers)
print(response.text)