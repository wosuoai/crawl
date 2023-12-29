# redis 配置
REDIS_CONFIG={
    "host":"127.0.0.1",
    "password":"123456",
    "port":6379
}

# 检测类
TESTER_MAP={
    "taobao": "TBTest"
}

# 生成类
GENERATOR_MAP={
    "taobao": "TBGenerator"
}

# 登陆认证类
LOGIN_MAP={
    "taobao": "TBLogin"
}

# 账号配置类
ACCOUNT_MAP={
    "taobao":[
         {"username":"19357179344","password":"dejavu111"},
         {"username":"19357188234","password":"dejavu999"},
         {"username":"18067948834","password":"dejavu666"},
         {"username":"18072854747","password":"dejavu888"}
        
        ]
}

# 每个cookies的冷却时间
SLEEP_MAP={
    "taobao": 22,
    "tianmao":20
}

# 配置谷歌浏览器路径和驱动路径 这部分实现了自动匹配大法
# CHROME_CONFIG={
#     "chromePath":"D:/Google/Chrome/Application/chrome.exe",
#     "driverPath":"D:/Google/Chrome/Application/chromedriver.exe"
# }