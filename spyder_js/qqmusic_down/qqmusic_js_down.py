import requests
import re
import execjs
import os

"""
只能下载免费的歌曲，VIP歌曲有识别号暂不做处理
"""

class QQmusic(object):
    def __init__(self):
            self.headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                'Referer': 'https://y.qq.com/portal/singer_list.html',
            }

    def run(self):
        data='{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":-100,"sin":0,"cur_page":1}}}'

        sign=self.get_sign(data)
        #0,1是下一页的歌手号如下一页是80,2
        #解析歌手的名字和id号
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI20079930333012497&g_tk=1541691288&' \
              'sign={}&loginUin=3320795610&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22' \
              'sin%22%3A{}%2C%22' \
              'cur_page%22%3A{}%7D%7D%7D'.format(sign, 0, 1)
        response=self.parse_url(url)

        #歌手id
        data_id_list,name_list=self.parse_data(response)
        n=0
        s=1
        for name in name_list:
            print("%d  %s  "%(n,name),end=' ')
            if n==10*s:
                print('\n')
                s=s+1
            n=n+1
        n=int(input("\n请输入歌手的序列号:"))
        print("你选择了"+name_list[n])
        url_data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList","param":{"order":1,"singerMid":"%s","begin":0,"num":10},"module":"musichall.song_list_server"}}'%str(data_id_list[n])
        url_html = self.get_sign(url_data)
        music_html='https://u.y.qq.com/cgi-bin/musics.fcg?-=getSingerSong9337150917069357&g_tk=1541691288&sign={}&' \
                   'loginUin=3320795610&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&' \
                   'data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{}%22%2C%22begin%22%3A0%2C%22num%22%3A10%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D'.format(url_html,data_id_list[n])

        #歌手的歌名
        html_list=self.parse_url(music_html)
        music,title=self.music_list(html_list,name_list[n])
        music_data='{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1399367235","calltype":0,"userip":""}},"req_0"' \
                 ':{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1399367235",' \
                 '"songmid":["%s"],"songtype":[0],"uin":"3320795610","loginflag":1,"platform":"20"}},"comm":{"uin":3320795610,"format":"json","ct":24,"cv":0}}'%(str(music))

        #获取音乐的钥匙
        url_html=self.get_sign(music_data)
        
        #最后钥匙的链接
        html='https://u.y.qq.com/cgi-bin/musics.fcg?-=getplaysongvkey37572959288093255&g_tk=1541691288&sign={}&' \
             'loginUin=3320795610&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer' \
             '%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%221399367235%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%221399367235%22%2C%22' \
             'songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%223320795610%22%2C%22loginflag%22%3A1%2C%22platform%' \
             '22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A3320795610%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'.format(url_html,music)
        data_key=self.parse_url(html)
        link=self.html_key(data_key)
        print(link)
        print("下载结束啦！！！")
        #保存
        self.with_open(link,title)

    #js加密
    def get_sign(self,data):
        with open('get_sign.js', 'r', encoding='utf-8') as f:
            text = f.read()
        js_data = execjs.compile(text)
        sign_id = js_data.call('get_sign', data)
        #清洗数据获取真正的sign
        sign = re.sub("finedunde", "", sign_id).replace("zzaundefined", "")
        sign = "zzaundefinedunde" + sign
        return sign
    #解析url
    def parse_url(self,url):

        reponse=requests.get(url=url,headers=self.headers).json()

        return reponse
    #清洗数据获取想要的参数
    def parse_data(self,response):
        music_name=[]
        music_id=[]
        #歌手的名字,这是第一页，可以通过scrapy全局爬取
        for i in range(0,80):
            music_name.append(response['singerList']['data']['singerlist'][i]['singer_name'])
            # print(music_name)
            #歌手的id
            music_id.append(response['singerList']['data']['singerlist'][i]['singer_mid'])
            # print(music_id)
        return music_id,music_name
    #歌名清洗
    def music_list(self,html_list,name):
        print("------------------------------------"+name+"的歌单------------------------------------")
        for i in range(0,10):
            print(str(i)+"  "+html_list['singerSongList']['data']['songList'][i]['songInfo']['name'])
        n=int(input("请选择歌单序列号:"))
        music=html_list['singerSongList']['data']['songList'][n]['songInfo']['mid']
        music_name=html_list['singerSongList']['data']['songList'][n]['songInfo']['name']
        return music,music_name
    #链接获取
    def html_key(self,data_key):
        req=data_key['req_0']['data']['midurlinfo'][0]['purl']
        req="https://ws.stream.qqmusic.qq.com/"+req
      # print(req)
        return req
    #保存
    def with_open(self,link,title):
        root = './download'
        if not os.path.exists(root):
            os.mkdir(root)
        res=requests.get(link, headers=self.headers).content
        with open(os.path.join(root, '{}.mp3'.format(title)),'wb') as f:
            f.write(res)
            print(title+' 下载成功')

if __name__ == '__main__':
    qq_music=QQmusic()
    qq_music.run()
