import requests
import hashlib
import time
from flask import Flask,jsonify
import json
import sys
from cookies_process.cookies_redis import RedisClient
from threading import Thread
from setting import REDIS_CONFIG,SLEEP_MAP
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cookies_pool_tmall.log')
    ]
)

app = Flask(__name__)
sleepCookies={}

class Server:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_cookies_from_redis(website:str)->dict:
        global sleepCookies
        credentialOperator = RedisClient(type="credential",website=website,host=REDIS_CONFIG["host"],port=REDIS_CONFIG["port"],password=REDIS_CONFIG["password"]) # 凭证对象
        try:
            cookies=credentialOperator.random() # 随机取一个cookies
        except:
            return json.loads("{}")
        # 一直等待到有cookies再返回
        while cookies in sleepCookies.keys():
            cookies=credentialOperator.random()
            time.sleep(0.1)
        sleepCookies[cookies]=SLEEP_MAP[website]
        return json.loads(cookies)
    
    @staticmethod
    def remove_cookies_from_sleep():
        global sleepCookies
        while True:
            logging.info("进行cookies冷却检测中")
            try:
                for cookies in sleepCookies.copy().keys():
                    sleepCookies[cookies]=sleepCookies[cookies]-2
                    t = sleepCookies[cookies]
                    if t<=0:
                        del sleepCookies[cookies]
            except Exception as error:
                print("出现错误{},跳过".format(error))
            time.sleep(2)
    
    @staticmethod
    @app.route('/')
    def index():
        return '<h2>亦知基于python构建的cookies池</h2>'

    @staticmethod
    @app.route("/<website>/cookies")
    def get_cookies(website):
        return Server.get_cookies_from_redis(website)
    
    @staticmethod
    def run():
        Thread(target=Server.remove_cookies_from_sleep,args=()).start() 
        app.run()
        
if __name__ == '__main__':
    pass