import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QApplication, QLabel, QStatusBar, QPushButton
from crawl_imgdown import reptile

class qt_view(QWidget):
    def __init__(self):
        super(qt_view, self).__init__()

        #self.resize(445, 400)
        #self.setFixedSize(445,400)
        self.setGeometry(300, 300, 445, 400)#绝对布局
        self.setWindowTitle("图片爬取")

        self.classlabel = QLabel(self)
        self.classlabel.setText("欢迎使用图片爬取程序")
        self.classlabel.move(90, 30)
        self.classlabel.setStyleSheet("QLabel{color:blue;font-size:25px;font-weight:bold;font-family:YaHei;}")

        self.setWindowIcon(QIcon("1.ico"))#加载任务栏图标
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("images/2.jpg")))#加载背景图片
        self.setPalette(window_pale)

        #搜索框
        self.classlabel = QLabel(self)
        self.classlabel.setText("请填写需要爬取的图片名：")
        self.classlabel.move(10, 100)
        self.classlabel.setStyleSheet("QLabel{color:green;font-size:18px;font-weight:bold;font-family:YaHei;}")

        self.le0 = QLineEdit(self)
        self.le0.move(15, 130)
        self.le0.resize(300, 28)
        self.le0.setPlaceholderText("eg：水果图片")
        self.le0.setClearButtonEnabled(True)#清除输入框显示
        #保存路径框
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("请填写图片存储的路径：")
        self.pathlabel.move(10, 175)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:18px;font-weight:bold;font-family:YaHei;}")

        self.le1 = QLineEdit(self)
        self.le1.move(15, 205)
        self.le1.resize(300, 28)
        self.le1.setPlaceholderText("eg：F:/images")
        self.le1.setClearButtonEnabled(True)
        #下载数量框
        self.pathlabel = QLabel(self)
        self.pathlabel.setText("请填写图片下载页数(不超过1000)：")
        self.pathlabel.move(10, 250)
        self.pathlabel.setStyleSheet("QLabel{color:green;font-size:18px;font-weight:bold;font-family:YaHei;}")

        self.le2 = QLineEdit(self)
        self.le2.move(15, 275)
        self.le2.resize(300, 28)
        self.le2.setPlaceholderText("eg：200")
        self.le2.setClearButtonEnabled(True)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(6)
        #搜索框按钮
        le0btn = QPushButton(self)
        le0btn.setText("√")
        le0btn.setFont(font)
        le0btn.move(320, 129)
        le0btn.resize(30, 28)
        le0btn.clicked.connect(self.doAction)
        #路径框按钮
        le1btn = QPushButton(self)
        le1btn.setText("...")
        le1btn.setFont(font)
        le1btn.move(320, 205)
        le1btn.resize(30, 28)
        le1btn.clicked.connect(self.select_folder)
        #数量框按钮
        le2btn = QPushButton(self)
        le2btn.setText("√")
        le2btn.setFont(font)
        le2btn.move(320, 275)
        le2btn.resize(30, 28)
        le2btn.clicked.connect(self.DownpageSize)

        self.textlabel = QLabel(self)
        self.textlabel.setFixedSize(388, 352)
        self.textlabel.move(30, 352)#鼠标操作范围
        self.textlabel.setScaledContents(True)#自适应窗口大小

        button_detect_img = QPushButton(self)
        button_detect_img.setText("start")
        button_detect_img.move(376, 180)
        button_detect_img.setFixedSize(55, 90)
        button_detect_img.clicked.connect(self.detectimage)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(15, 320, 445, 25)

        self.timer = QBasicTimer()
        self.step = 0

    def timerEvent(self, e):
        if self.step >= 100:
            #self.step = 0
            self.pbar.setValue(self.step)
            self.timer.stop()
        else:
            self.step = self.step + 1/2
            self.pbar.setValue(self.step)

    def doAction(self, value):
        if self.timer.isActive():#如果定时器被激活-处于执行状态
            self.timer.stop()
        else:
            self.timer.start(100, self)


    def break_value(self):
        if (self.le0.isModified()):
            print(self.le0.text())
        if (self.le1.isModified()):
            print(self.le1.text())
        if (self.le2.isModified()):
            print(self.le2.text())

    def select_folder(self):#文件夹选取，默认是G盘
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "G:/")
        print(self.directory)
        directory = str(self.directory)
        self.le1.setText(directory)

    def DownpageSize(self):
        #文本框输入内容不在范围内，清除输入的内容
        if int(self.le2.text())>1000:
            QMessageBox.information(self, "提示", "请输入有效范围！")
            self.le2.clear()

    def detectimage(self):
        if int(self.le2.text())>1000:
            QMessageBox.information(self, "提示", "请输入有效范围！")
            self.le2.clear()
        if self.le0.text()=='' or self.le1.text()=='' or self.le2.text()=='':
            QMessageBox.information(self, "提示", "请输入有效字符！")
        else:
            save_name = self.le0.text()
            save_path = self.le1.text()
            pageSize = self.le2.text()
            values = reptile(save_name, save_path, pageSize)


    def closeEvent(self, event):#关闭程序前，弹出消息提示框

        reply = QMessageBox.question(self, '警告', '退出后程序将停止,\n你确认要退出吗？', QMessageBox.Yes,QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = qt_view()
    main.show()
    sys.exit(app.exec_())