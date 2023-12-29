import pymysql
import requests
from urllib.parse import urlparse
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import queue
import time
import random
import os
import uuid
from warnings import filterwarnings  # 忽略操作mysql时的一些警告

# 忽略mysql告警信息
filterwarnings("ignore", category=pymysql.Warning)

title_erList = ["|", "】", "【", "/", "\\", ":", "*", "?", '"', ">", "<", "'"]  # Windows文件夹命名规则不包含的字符
class MysqlDb:
    """
    初始化数据库，连接数据库、获取操作游标
    :return:
    """

    def __init__(self, host, user, password, database, selectReturnType='one') -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.selectReturnType = selectReturnType
        # 创建对象连接
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        # 创建连接数据库游标
        self.cursor = self.conn.cursor()

    # 定义一个关闭数据库连接的方法
    def closeConnect(self):
        self.cursor.close()
        self.conn.close()

    def executeSql(self, sql):
        """
            执行sql语句，针对读操作返回结果集
            args：
                sql  ：sql语句
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有列表记录
            results = self.cursor.fetchall()
            # 关闭数据库连接
            self.closeConnect()
            return results
        except pymysql.Error as e:
            error = '执行sql语句失败(%s): %s' % (e.args[0], e.args[1])
            print(error)

    def executeCommit(self, sql):
        """
        执行数据库sql语句，针对更新,删除,事务等操作失败时回滚
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库
            self.conn.commit()
            # 关闭连接
            self.closeConnect()
        except pymysql.Error as e:
            self.conn.rollback()
            error = '执行数据库sql语句失败(%s): %s' % (e.args[0], e.args[1])
            print("error:", error)


# 重新封装线程池类
class ThreadPool_Executor(ThreadPoolExecutor):
    """
    重写线程池修改队列数
    """

    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        # 队列大小为最大线程数的两倍
        self._work_queue = queue.Queue(self._max_workers * 2)


class TmallItemImg:
    def __init__(self):
        self.Headers = {'user-agent': UserAgent().random, }
        self.enableIpProxy = True
        self.max_workers = 5
        self.threadsPool = ThreadPool_Executor(max_workers=self.max_workers)  # 定义线程数量

        self.proxyIpList = []

        # 打开最后保存的ip
        with open("ip.txt", "r", encoding='utf-8') as f:
            ipList = f.readlines()
            if len(ipList) > 1:
                self.proxyIpList = eval(ipList[-1])

    def set_proxy(self):
        """
        set proxy for requests
        :param proxy_dict
        :return:
        """
        if self.enableIpProxy:
            proxies = None
            while True:
                try:
                    if len(self.proxyIpList) <= self.max_workers * 2:
                        time.sleep(5)
                        # 每日签到
                        #get_ip = requests.get(url=f"http://proxy.siyetian.com/apis_get.html?token=gHbi1STUlkeOpWT65kaZBTTn1STqFUeNpXR31ERrh3TUlENORVV31kaVBzTE1EN.QM1ETO5MDO5YTM&limit=1&type=0&time=&split=0&split_text=").text.split('\r\n')
                        # 包月套餐
                        get_ip = requests.get(url=f"http://proxy.siyetian.com/apis_get.html?token=AesJWLOR1Z45EVJdXTq1EeNRUR35kajhnTR1STqFUeNpXR31ERrh3TUlENORVV31kaVBzTE1EN.QM3cjNzITO5YTM&limit=5&type=0&time=&split=0&split_text=").text.split('\r\n')
                        if get_ip == '{"code":10019,"info":"�Ѵﵽʹ������","data":[]}':
                            time.sleep(2)
                            continue

                        get_ip = [item for item in get_ip if item != ""]

                        self.proxyIpList = self.proxyIpList + get_ip

                        # 每次获取的一批ip追加到文本里
                        with open("ip.txt", "a+") as f:
                            f.write(str(self.proxyIpList) + "\n")
                            print("------ip追加到ip.txt--------")

                    else:
                        ip = random.choice(self.proxyIpList)
                        proxies = {
                            "http": "http://{}".format(ip),
                            "https": "http://{}".format(ip)
                        }

                        url = "https://www.baidu.com/abcd"
                        try:
                            response = requests.get(url, proxies=proxies, timeout=3)

                            if response.status_code != 404:
                                proxies = None

                        # 这里的异常只存在超时的情况
                        except Exception as error:
                            proxies = None
                            if ip in self.proxyIpList:
                                self.proxyIpList.remove(ip)
                            print(f"------代理ip池还剩下ip数量为{len(self.proxyIpList)}------")
                            print(f"------代理ip列表中移除ip-------{ip}")
                            print(error)

                except Exception as error:
                    proxies = None
                    print("出现异常是")
                    print(error)

                finally:
                    time.sleep(random.uniform(0.2, 0.5))
                    return proxies

    # 图片下载
    def dowm_imgs(self):
        while True:
            try:
                # 使用游标对象执行SQL查询语句
                results = MysqlDb(host='127.0.0.1', user='root', password='wosuoai8279',database='item_imgs').executeSql('SELECT shop_name, item_name, img_link FROM all_imgs_copy1 WHERE status = 0 order by id asc LIMIT 100')
                start = time.time()
                task_list = []
                for result in results:
                    if len(result) <= 0:
                        print("当前数据库没有可下载的图片链接")
                        break
                    else:
                        item_title=result[1]
                        for i in title_erList:
                            item_title = item_title.replace(i, "")
                        dirPath = "E:\\shop_imgs\\" + result[0] + "\\" + item_title
                        imgUrl = result[2]
                        # 如果文件夹不存在创建文件夹
                        if os.path.exists(dirPath) == False:
                            os.makedirs(dirPath)
                        task = self.threadsPool.submit(self._threads_download, dirPath, imgUrl)
                        task_list.append(task)
                concurrent.futures.wait(task_list, return_when=concurrent.futures.ALL_COMPLETED)

                print("一轮下载完成")
                print(f"一轮下载的时长为{time.time() - start}")
            except Exception as error:
                print("出现错误")
                print(error)

    # 多线程下载
    def _threads_download(self, dirPath: str, imgUrl: str):
        try:
            filename = uuid.uuid4().hex
            with open("{}/{}.jpg".format(dirPath, filename), "wb") as f:
                proxies = self.set_proxy()

                if proxies is None:
                    print("------------------没有提取到代理跳过下载------------------")
                else:
                    f.write(requests.get(imgUrl, headers=self.Headers, proxies=proxies, timeout=(2, 3)).content)
                    print(dirPath + "图片{}下载成功".format(imgUrl))
                    # 图片下载成功更新status状态
                    MysqlDb(host='127.0.0.1', user='root', password='wosuoai8279', database='item_imgs').executeCommit("UPDATE all_imgs_copy1 SET status = 1 WHERE img_link = '{}'".format(imgUrl))
        except Exception as error:
            print("图片下载出现错误%s" % error)


if __name__ == "__main__":
    # 创建一个爬取天猫详情的
    tmallItemImg = TmallItemImg()
    tmallItemImg.dowm_imgs()
