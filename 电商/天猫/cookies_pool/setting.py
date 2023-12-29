# redis 配置
REDIS_CONFIG={
    "host":"127.0.0.1",
    "password":"",
    "port":6379
}

# 检测类
TESTER_MAP={
    "tmall": "TMTest"
}

# 生成类
GENERATOR_MAP={
    "tmall": "TMGenerator"
}

# 登陆认证类
LOGIN_MAP={
    "tmall": "TMLogin"
}

# 账号配置类
ACCOUNT_MAP={
    "tmall":[]
}

# 每个cookies的冷却时间
SLEEP_MAP={
    "taobao": 22,
    "tmall":20
}

# 配置谷歌浏览器路径和驱动路径 这部分实现了自动匹配大法
# CHROME_CONFIG={
#     "chromePath":"D:/Google/Chrome/Application/chrome.exe",
#     "driverPath":"D:/Google/Chrome/Application/chromedriver.exe"
# }