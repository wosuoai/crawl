

# from cookies_process import cookies_test as test
# testObj=getattr(test,"BaseTest")("taobao")
# testObj.run()
# from cookies_process.cookies_api import Server
# server = Server()
# server.run()
# from cookies_process import cookies_generator  as generators
# from cookies_process.cookies_generator import TBGenerator

# from setting import *
# website="taobao"
# generator=getattr(generators,GENERATOR_MAP[website])(website)
# generator.run()
# generator = TBGenerator("taobao")
# generator.run()
# from cookies_process.account_login.login import TBLogin
# t=TBLogin()
# print(t.login("15256728901","sxh.200008"))"
# a='{"taobao":"{\"tfstk\": \"ddUk0HV1juo5KPzRv435yOBWjdSxVLgIFJLKp2HF0xkjJYU82kq01JDROgg8mv24nYoRN7nH-WDjJYU82kq0E88K2JU3ceV_OzCSJ_g7N2gFBsQOB7NSR-S8D13qFxntYPWOWNF5xaF1POBC_rShF9ofnE8D7iaO9FJTLJ4mZmSYFx8nMrloqAo4reWN4n-Z5YTIg6U2AHirGjDt6yORo\", \"xlly_s\": \"1\", \"isg\": \"BAoK4prdWoONhdYv-eQ0l95KW_Cs-45VCwob05RDt93pR6sBb4i7ZP81U7Obtwbt\", \"cna\": \"WCtNHc6KHhoBASQJiiimSJhh\", \"l\": \"fBQ10W1PNfnc86lCBOfZFurza779sIRfguPzaNbMi9fPOJ1H5uVPW1OyS3YMCnGVEsmDY38PiVPBBA8g1yz3dxv9-e_7XPQondBGEkcah\", \"_tb_token_\": \"3be5ebee0867e\", \"t\": \"93da827f61272d8826d74cba7dd81531\", \"_samesite_flag_\": \"true\", \"XSRF-TOKEN\": \"2f3e00b3-e43e-4f34-a965-0a29299de829\", \"arms_uid\": \"7079d8c3-815b-4dcb-8769-eaeeef6fba64\", \"cookie2\": \"119f48f550b7811aa72d676bed3c531d\", \"_uab_collina\": \"169071343049139666358673\"}"}'
# import json
# print(eval(a))
# import json
# import requests
# print(requests.get("http://127.0.0.1:5000/taobao/cookies").json()["arms_uid"])
# a={"c":1}
# print(a.get("c"))
# def a():
#     for i in range(3):
#         yield i


# t=a()
# for c in t:
#     print(c)
import requests
print(requests.get(url='https://item.taobao.com/item.htm?id=687674726313&spm=a1z10.3-c-s.w4002-23122658373.15.f673658dYDxNiu').status_code)




