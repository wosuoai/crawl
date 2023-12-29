from cookies_process.cookies_redis import RedisClient
from cookies_process.account_login import login as logins
from setting import REDIS_CONFIG,ACCOUNT_MAP,LOGIN_MAP
import logging
import sys
import json
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cookies_pool_tmall.log')
    ]
)
class BaseGenerator(object):
    def __init__(self,website:str) -> None:
        self.website=website
        self.accountOperator = RedisClient(type="account",website=self.website,host=REDIS_CONFIG["host"],port=REDIS_CONFIG["port"],password=REDIS_CONFIG["password"]) # 账号
        self.credentialOperator = RedisClient(type="credential",website=self.website,host=REDIS_CONFIG["host"],port=REDIS_CONFIG["port"],password=REDIS_CONFIG["password"]) # 凭证
        accountList = ACCOUNT_MAP["taobao"]
        self.accountOperator.deleteHashKey()
        for account in accountList:
            self.accountOperator.set(account["username"],account["password"])
                    
            
            
    
    # 通过账号密码生成认证信息
    def generate(self,username,password):
        raise NotImplementedError
    
    # run 方法
    def run(self):
        logging.info("开始运行账号池生成")
        for username, password in self.accountOperator.all().items():
            # 如果认证信息已经存在就跳过账号认证生成
            if self.credentialOperator.get(username):
                continue
            logging.info("开始生成账号认证")
            try:
                self.generate(username,password)
            except Exception as error:
                logging.error("{}账号生成cookies出错,错误原因是{}".format(username,error))
            
class TBGenerator(BaseGenerator):
    def __init__(self, website: str) -> None:
        super().__init__(website)
        
    def generate(self,username:str,password:str):
        loginOperator = getattr(logins,LOGIN_MAP[self.website])()
        cookies=loginOperator.login(username,password) # 使用selenium登陆
        self.credentialOperator.set(username,json.dumps(cookies)) # 设置cookies到redis
        
            
    
if __name__ == "__main__":
    pass