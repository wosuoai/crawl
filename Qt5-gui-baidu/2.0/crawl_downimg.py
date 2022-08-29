import sys
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import QProgressBar, QApplication, QLabel, QPushButton
from PyQt5.QtCore import *
import threading
from threading import Thread
import time

class qt_view(QWidget):
    def __init__(self):
        super(qt_view, self).__init__()

        self.resize(455, 440)
        #self.setGeometry(700, 300, 445, 440)#绝对布局
        self.setWindowTitle("baidu&bing")
        #self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框

        self.classlabel = QLabel(self)
        self.classlabel.setText("欢迎使用图片爬取程序")
        self.classlabel.move(90, 30)
        self.classlabel.setStyleSheet("QLabel{color:blue;font-size:25px;font-weight:bold;font-family:YaHei;}")

        self.setWindowIcon(QIcon("1.ico"))  # 加载任务栏图标
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("images/2.jpg")))#加载背景图片
        self.setPalette(window_pale)

        #搜索引擎
        self.classlabel = QLabel(self)
        self.classlabel.setText("请选择搜索引擎：")
        self.classlabel.move(10, 75)
        self.classlabel.setStyleSheet("QLabel{color:green;font-size:15px;font-weight:bold;font-family:YaHei;}")

        self.le0 = QComboBox(self)
        self.le0.move(10, 105)
        self.le0.resize(300, 28)
        self.le0.addItems(['baidu', 'bing'])
        #self.le0.setClearButtonEnabled(True)  # 清除输入框显示


        #搜索内容
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("请输入需要爬取的图片：")
        self.pathlabel.move(10, 150)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:15px;font-weight:bold;font-family:YaHei;}")

        self.le1 = QLineEdit(self)
        self.le1.move(10, 180)
        self.le1.resize(300, 28)
        self.le1.setPlaceholderText("eg：水果")
        self.le1.setClearButtonEnabled(True)

        #下载数量
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("请输入图片下载数量：")
        self.pathlabel.move(10, 225)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:15px;font-weight:bold;font-family:YaHei;}")

        self.le2 = QLineEdit(self)
        self.le2.move(10, 255)
        self.le2.resize(300, 28)
        self.le2.setPlaceholderText("eg：1000")
        self.le2.setClearButtonEnabled(True)

        #保存路径
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("请选择图片保存路径：")
        self.pathlabel.move(10, 300)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:15px;font-weight:bold;font-family:YaHei;}")

        self.le3 = QLineEdit(self)
        self.le3.move(10, 330)
        self.le3.resize(300, 28)
        self.le3.setPlaceholderText("eg：F:/images")
        self.le3.setClearButtonEnabled(True)

        #下载进度
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("图片下载进度：")
        self.pathlabel.move(10, 375)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:15px;font-weight:bold;font-family:YaHei;}")

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(8)

        #搜索引擎按钮
        le0btn = QPushButton(self)
        le0btn.setText("√")
        le0btn.setFont(font)
        le0btn.move(320, 105)
        le0btn.resize(30, 28)
        le0btn.clicked.connect(self.doAction)

        #搜索内容按钮
        le1btn = QPushButton(self)
        le1btn.setText("===")
        le1btn.setFont(font)
        le1btn.move(320, 180)
        le1btn.resize(30, 28)
        le1btn.clicked.connect(self.target_img)

        #下载数量按钮
        le2btn = QPushButton(self)
        le2btn.setText("---")
        le2btn.setFont(font)
        le2btn.move(320, 255)
        le2btn.resize(30, 28)
        le2btn.clicked.connect(self.DownImgNum)

        #图片保存路径按钮
        le3btn = QPushButton(self)
        le3btn.setText("...")
        le3btn.setFont(font)
        le3btn.move(320, 330)
        le3btn.resize(30, 28)
        le3btn.clicked.connect(self.select_folder)

        self.textlabel = QLabel(self)
        self.textlabel.setFixedSize(388, 352)
        self.textlabel.move(30, 400)#允许光标操作范围
        self.textlabel.setScaledContents(True)#自适应窗口大小

        #开始按钮
        self.btn = QPushButton("start",self)
        self.btn.move(376, 110)
        self.btn.setFixedSize(55, 90)
        self.btn.clicked.connect(self.detectimage)

        #结束按钮
        self.btn1 = QPushButton("end",self)
        self.btn1.move(376, 260)
        self.btn1.setFixedSize(55, 90)
        self.btn1.clicked.connect(self.closeWindow)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(10, 405, 445, 25)

        self.timer = QBasicTimer()#构建计数器
        self.step = 0

        # 设置进度条的范围
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(1)
        self.pbar.setValue(self.step)

        self.pbar.setInvertedAppearance(True)#进度条从左到右

    #被编辑返回编辑状态
    def break_value(self):
        if (self.le0.currentText()):
            print(self.le0.currentText())
        if (self.le1.isModified()):
            print(self.le1.text())
        if (self.le2.isModified()):
            print(self.le2.text())
        if (self.le3.isModified()):
            print(self.le3.text())

    def select_engine(self):
        if self.le0.currentText() == "baidu":
            print("你选择的是baidu搜索引擎")
        else:
            print("你选择的是bing搜索引擎")

    def target_img(self):
        if self.le1.text() == "":
            QMessageBox.information(self, "提示", "请输入有效字符！")

    def DownImgNum(self):
        #文本框输入内容不在范围内，清除输入的内容
        if int(self.le2.text())>10000:
            QMessageBox.information(self, "提示", "请输入有效范围！")
            self.le2.clear()

    # 文件夹选取，默认是G盘
    def select_folder(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "G:/")
        print(self.directory)
        directory = str(self.directory)
        self.le3.setText(directory)

    def detectimage(self):

        if self.le0.currentText()=='' or self.le1.text()=='' or self.le2.text()=='' or self.le3.text()=='':
            QMessageBox.information(self, "提示", "请输入有效字符！")
        else:
            choice_engine = self.le0.currentText()#使用currentText()函数获取下拉框中选择的值
            print("你选择的是%s搜索引擎" %self.le0.currentText())
            find_img = self.le1.text()
            img_num = int(self.le2.text())
            save_path = self.le3.text()
            self.t1 = threading.Thread(target=self.DownImages, args=(choice_engine, find_img, img_num,save_path,))
            self.t1.start()
            self.t1.join()

    def DownImages(self,choice_engine, find_img, img_num,save_path):
        thread = Thread(target=crawl_images, args=(choice_engine, find_img, img_num,save_path,))
        thread.start()

    def closeWindow(self):
        qApp = QApplication.instance()#获取QApplication类的对象
        qApp.quit()
        self.t1.close()  # 设置异常，阻塞进程

    #设置爬虫下载进度条
    def timerEvent(self,e):
        global i
        for i in range(int(self.le2.text())):
            i+=1
            if self.step >= 1:
                self.pbar.setValue(self.step)
                self.timer.stop()
            else:
                self.step = i/int(self.le2.text())
                self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():#如果定时器被激活,处于执行状态
            self.timer.stop()
        else:
            self.timer.start(1, self)

    # 关闭程序前，弹出消息提示框
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '警告', '退出后程序将停止,\n你确认要退出吗？', QMessageBox.Yes,QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.t1.close()
        else:
            event.ignore()

i=0

#爬虫部分，放到主程序之外，避免耗时事件造成界面假死
def crawl_images(choice_engine, find_img, img_num,save_path):
    import re
    import time
    import requests
    from urllib import parse
    import os
    from fake_useragent import UserAgent  # 随机生成一个user-agent,模拟有多个浏览器访问
    import urllib3


    global i

    dicPattern = {'bing': r'<img class="mimg vi.*src="(.*?)"', 'baidu': r'"middleURL":"(.*?)"',
                  'sogou': r'img.*src="(.*?)"', '360': r'"img":"(.*?)"'}
    dicUrl = {'bing': 'https://cn.bing.com/images/search?q={}&form=HDRSC2&first={}&tsc=ImageHoverTitle',
              'baidu': 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7542812996841482750&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&{}='}

    def writeHtml(outfile, html):
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(str(html))

    def geturls(baseurl, enginPattern):
        ImgUrlPattern = re.compile(enginPattern)

        # 响应头，假装我是浏览器访问的网页
        headers = {'User-Agent': UserAgent().random}
        urllib3.disable_warnings()  # 忽略警告
        response = requests.get(baseurl, headers=headers)  # 获取网页信息

        html = response.text  # 将网页信息转化为text形式
        data = re.findall(ImgUrlPattern, html)  # 得到图片超链接的列表
        return data

    #i=0


    # 如果文件夹不存在就创建文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        pass

    while (i < img_num):
        for index in range(100):
            if choice_engine == 'baidu':
                decteUrl = dicUrl[choice_engine].format(parse.quote(find_img), parse.quote(find_img), index * 30,
                                                      str(int(time.time() * 1000)))
            elif choice_engine == 'bing':
                decteUrl = dicUrl[choice_engine].format(find_img, index * 35)  # dicUrl保存引擎与搜索地址的映射

            imgUrls = geturls(decteUrl, dicPattern[choice_engine])  # 获取网页中所有图片地址
            headers = {'User-Agent': UserAgent().random}

            for ImgUrl in imgUrls:
                if i < img_num and "http" in ImgUrl:  # 筛选非空列表
                    # 如果url是无效的，则查看下一个url
                    try:
                        resp = requests.get(ImgUrl, headers=headers)  # 获取网页信息
                    except requests.ConnectionError as error:
                        continue
                    byte = resp.content  # 转化为content二进制
                    with open("{}/{:0>4d}.jpg".format(save_path, (i + 1)), "wb") as f:
                        if resp.status_code == 200 and len(str(byte)) > 1000:
                            f.write(byte)
                            i = i + 1
                            time.sleep(1)  # 设置间隔，避免访问过快认为我在DDOS服务器
                            print("第{}张与{}有关的图片爬取成功!".format(i, find_img))
                else:
                    break

                status = round(i/img_num,2)
                print(status)

            if i >= img_num:
                break


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)#屏幕分辨率自适应
    #QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    #crawl_images()

    app = QApplication(sys.argv)
    main = qt_view()
    main.show()
    sys.exit(app.exec_())
