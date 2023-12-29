# from fake_useragent import UserAgent
# import requests
#
# headers = {'User-Agent': UserAgent().random}
# r = requests.get("https://gd4.alicdn.com/imgextra/i4/381329993/O1CN012Ar07Y2NgqhfMgUI8_!!381329993.jpg", headers=headers)
# # 下载图片
# with open("images/1111.jpg", mode="wb") as f:
#     f.write(r.content)  # 图片内容写入文件

import pymysql
import requests
from urllib.parse import urlparse
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import queue
import time
import random
from PIL import Image
from io import BytesIO
import os
import uuid
from typing import Tuple
from warnings import filterwarnings  # 忽略操作mysql时的一些警告

# 忽略mysql告警信息
filterwarnings("ignore", category=pymysql.Warning)

headers = {'User-Agent': 'ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

title_erList = ["|", "】", "【", "/", "\t", ":", "*", "?", '"', ">", "<", "'", "\\"]  # Windows文件夹命名规则不包含的字符
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

def down_imgs():
    while True:
        try:
            # 使用游标对象执行SQL查询语句
            results = MysqlDb(host='127.0.0.1', user='', password='', database='').executeSql('SELECT id,shop_name, item_name, img_link FROM all_imgs_copy4 WHERE (status = 0 AND id >= 1202287) order by id asc LIMIT 100')
            for result in results:
                #if len(result) == 0:
                if result == ():
                    print("当前数据库没有可下载的图片链接")
                    break
                else:
                    result = result[1:]
                    item_title = result[1]
                    for i in title_erList:
                        item_title = item_title.replace(i, "")
                    dirPath = "E:\\shop_imgs\\" + result[0] + "\\" + item_title
                    imgUrl = result[2]
                    # 如果文件夹不存在创建文件夹
                    if os.path.exists(dirPath) == False:
                        os.makedirs(dirPath)

                    filename = uuid.uuid4().hex
                    try:
                        # with open("{}/{}.png".format(dirPath, filename), "wb") as f:
                        #     f.write(requests.get(imgUrl, headers=headers).content)
                        img = Image.open(BytesIO(requests.get(imgUrl, headers=headers).content))
                        img.save("{}/{}.png".format(dirPath, filename))
                        print(dirPath + "图片{}下载成功".format(imgUrl))
                        # 图片下载成功更新status状态
                        MysqlDb(host='127.0.0.1', user='root', password='wosuoai8279', database='item_imgs').executeCommit("UPDATE all_imgs_copy4 SET status = 1 WHERE img_link = '{}'".format(imgUrl))
                        time.sleep(1)
                    except Exception as error:
                        print("图片下载出现错误%s" % error)
                        # if "RGBA" in error:
                        #     img = Image.open(BytesIO(requests.get(imgUrl, headers=headers).content))
                        #     img.save("{}/{}.png".format(dirPath, filename))
                        #     print(dirPath + "图片{}下载成功".format(imgUrl))
                        #     # 图片下载成功更新status状态
                        #     MysqlDb(host='127.0.0.1', user='root', password='wosuoai8279',database='item_imgs').executeCommit("UPDATE all_imgs_copy4 SET status = 1 WHERE img_link = '{}'".format(imgUrl))
                        #     time.sleep(1)
        except Exception as error:
            print("出现错误")
            print(error)

if __name__ == "__main__":
    down_imgs()