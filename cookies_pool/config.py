# Redis数据库地址、端口、密码
REDIS_HOST =  "localhost"               # 注意本地就写字符串形式的"localhost"
REDIS_PORT = 6379
REDIS_PASSWORD =  None                  # 密码没有的话，就写None

# 产生器使用的浏览器
BROSER_TYPE = "chrome"                  # 注意浏览器类型，是字符串形式的

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {                       # 注意字典后的类名也是字符串形式的
    "1688":"1688CookiesGenerator"
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP ={
    "1688": "1688ValidTester"
}

TESTER_URL_MAP = {
    '1688': 'https://www.1688.com'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '127.0.0.1'                  # host是字符串
API_PORT = 5000                         # port不是字符串

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True

# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
TESTER_PROCESS = True

# API接口服务
API_PROCESS = True
