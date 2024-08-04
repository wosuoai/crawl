import requests
import re
from bs4 import BeautifulSoup
import pymysql
import time
from urllib.request import quote, unquote

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

cookies = {
    'session-id': '141-4364040-7657710',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'ubid-main': '131-9022662-9037352',
    'lc-main': 'zh_CN',
    'sp-cdn': '"L5Z9:CN"',
    'session-token': '58G6XXN8VLKUmACK+9AuIS1iyO/WOwxnp/YLe2v/ER4gjPSO5wLvoHee9QewT5QN3+ZUAfy5i/Np3EmXKByMvQUdFEpUSymK3JRobJOginvaf52p3nyTnX2vA/+gVBRRR0fE1CaH3zjQUhrjklYCDw6Ck4+vFEAiBjzQEdfwAA4VI/iayGKNGhutej2nqEHLdibm/OAc9iHZPtWsdbGSMOU0Fxi5czB2Wd6wJVeAAHfv9qKhIKytddhdAPPE/5yh731EmQTTXaE+0VgNn8Jbxmf4/0Ixu4hwgL9rGv/gEpg3sy3NF1eXvuIRlZE8LH5D/ZIMaMQs6mFg/Hwglrt6DKv7OfHJ4qYR',
    'csm-hit': 'tb:P81XG46AYH64J3ECB9AV+s-9VPPMDWQBCEC2HQ7GN20|1719501628885&t:1719501628885&adb:adblk_yes',
}


def sort_links(page:str) -> list:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'session-id=130-9954836-8963410; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:CN"; ubid-main=131-7919419-5952225; session-token=ooAwVOkeuxWYz6ViHG71/RNG2fKnl1AjHc6HM7GugdJLZWxdN95qc3cZuhy7ImQSYuo4nRef8jktPRAIDDTJm3S6kpLo2UgrhjoP0drSUQ2Ua93RKC7WTJtvIIJARjz0VSM2uKhIqB71/HlwCbHsU/LSDrQgP1hnBRKsdrCQoEEUOfQtlJcdhUDfSArbFnEJ8aKSDH8T40al+SgEJQjFxKX5aiAPuVGR8F9BFLSNVn40m8FN6DHnS7iXSjd75VJcBZ6RkaCC/WV705g461wgj3/37c9nujuaR3frCydxzlsilMtYTZhaLnG51lxl+c+yjGPxoKsUIkpfJvVKyMi/JT1mWwPSM2HK; csm-hit=tb:B81P2ZB5DSBRK39SQ0MH+s-B81P2ZB5DSBRK39SQ0MH|1719386788676&t:1719386788676&adb:adblk_no',
        'device-memory': '8',
        'downlink': '9.35',
        'dpr': '1',
        'ect': '4g',
        'priority': 'u=0, i',
        'referer': 'https://www.amazon.com/s?k=lilly+pulitzer+outlet&hvadid=557209755028&hvdev=c&hvlocphy=1013802&hvnetw=g&hvqmt=b&hvrand=11915583993827380783&hvtargid=kwd-27201913&hydadcr=7472_13183978&tag=googhydr-20&ref=pd_sl_3k37yrfqp0_b',
        'rtt': '200',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1920',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'viewport-width': '1920',
    }

    params = {
        'k': 'lilly pulitzer outlet',
        'page': page,
        'language': 'zh',
        'hvadid': '557209755028',
        'hvdev': 'c',
        'hvlocphy': '1013802',
        'hvnetw': 'g',
        'hvqmt': 'b',
        'hvrand': '11915583993827380783',
        'hvtargid': 'kwd-27201913',
        'hydadcr': '7472_13183978',
        'qid': '1719386703',
        'ref': 'sr_pg_2',
    }

    response = requests.get('https://www.amazon.com/s', params=params, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    sort_urls = []
    for a_tag in soup.find_all('a', href=True,class_='a-link-normal s-no-outline'):
        data_value = a_tag.get('href')
        if data_value:
            sort_urls.append("https://www.amazon.com"+data_value)
    return sort_urls

def data_html(referer:str,url:str) -> str:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'session-id=130-9954836-8963410; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:CN"; ubid-main=131-7919419-5952225; session-token=z2rJDON+B7tV5oSxkwf4KqTANuQarUmcn1UiXqjs0W0RU5ilzNN0CuNjPTxJrou2ksrWON8JpXLkJz5gmrSpA32vnoOXq0IzCBc/p6w2YpGQqkHuIQUVReIT9mBIFimTS8ehvjDTywxlzVJCHbgNqREjSY+c0A7SGTFjYfdCKuiAbwtGzmUdhSDIYqFJ9JcaKg4eNek6uFqX82oekE/1ITfBp4DMgyUgqMKpvdo3apxlUSJLrPzR6So7eiTjHA38OsVk7fV+EzX7d7mDYJpRfkeBMgoIj66wNcbWZp4Y7/0qCLHZ/KghyxOn2rt3qBc2X12KRnOUImAQhk0geMRqDyzWEEJAcm0k; csm-hit=tb:8EKYSZHPS4A8QT5YXJTG+s-8EKYSZHPS4A8QT5YXJTG|1719387247509&t:1719387247509&adb:adblk_no',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1',
        'ect': '4g',
        'priority': 'u=0, i',
        'referer': referer,
        'rtt': '200',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1920',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'viewport-width': '1920',
    }
    response = requests.get(url, cookies=cookies, headers=headers).text
    return response

if __name__ == "__main__":
    sorts = "lilly|pulitzer|outlet"
    for i in range(1,7):
        print(f"当前爬取的页数是：{i}")
        all_sort_links = sort_links(str(i))
        referfer_url = "https://www.amazon.com/s?k=lilly+pulitzer+outlet&page={}&language=zh&hvadid=557209755028&hvdev=c&hvlocphy=1013802&hvnetw=g&hvqmt=b&hvrand=11915583993827380783&hvtargid=kwd-27201913&hydadcr=7472_13183978&qid=1719386794&ref=sr_pg_{}".format(i,i)
        for data_link in all_sort_links[2:]:
            print(f"当前爬取的是：{data_link}")
            response = data_html(referfer_url,data_link)

            #try:
            data_id = data_link.split("?")[0].split("/")[-2]
            title = re.search('<title>(.*?)</title>',response).group(1).replace("Amazon.com: ","").split(",")[0]
            mark = re.search('<span class="a-icon-alt">(.*?)</span>',response).group(1).split(" ")[0]
            price = re.search('<span aria-hidden="true">.*?</span>',response).group(1).replace("US$","")
            talk = re.search('<span id="acrCustomerReviewText" class="a-size-base">(.*?)</span>',response).group(1).split(" ")[0]
            soup = BeautifulSoup(response, 'html.parser')
            #price = soup.find("span",class_="a-offscreen").text.replace("US$","")
            print(price)
            colors = ""
            color_imgs = ""
            for a_tag in soup.find_all('img', src=True,class_='imgSwatch'):
                colors += a_tag.get('alt') + "|"
                color_imgs += a_tag.get('src') + "|"
            des = ""
            des_list = re.findall('<span class="a-list-item a-size-base a-color-base">(.*?)</span>',response)
            for i in des_list:
                des += i.replace("'","").replace('"','')
            main_imgs = ""
            for li_tag in soup.find_all('li', class_='a-spacing-small item'):
                main_imgs += li_tag.find("img").get("src").replace("._AC_SR38,50_","") + "|"
            detail_imgs = ""
            for div_tag in soup.find_all('div', class_='a-section a-spacing-none background-image'):
                detail_imgs += div_tag.find("img",class_="a-lazy-loaded").get("data-src") + "|"

            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            run_sql = 'insert into amazon (`link`, `title`, `sort`, `num`, `price`, `color`, `color_img`, `intro`, `main_img`, `detail_img`, `evaluate_num`, `mark`, `create_time`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                data_link, title, sorts, data_id, price, colors[:-1], color_imgs[:-1], des, main_imgs[:-1], detail_imgs[:-1], talk, mark, t)
            print(run_sql)
            try:
                MysqlDb(host='127.0.0.1', user='root', password='', database='').executeCommit(sql=run_sql)
            except Exception as error:
                print(error)
            print(f"当前爬取的{data_link}完成！")
            time.sleep(3)
            # except Exception as error:
            #     print(error)

    print("当前爬取完成")
    MysqlDb(host='127.0.0.1', user='root', password='', database='').closeConnect()