#!/user/bin/env python
#coding=utf-8

import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from myClass import *

class main(QWidget):
	def __init__(self):
		super(main,self).__init__()
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setGeometry(300, 30, 300,600)
		self.addLayout()
	def  addLayout(self):
		# ==========================头部=================================
		sp = headWidget(self)   #这里的self就是被移动的窗口
		sp.setParent (self)  #这里的self是所属父级
		sp.setStyleSheet("QWidget{background:#7FAEE4;border:1px solid #5FB9FA;border-top:none;border-bottom:none}QLabel{color:white;border:none}\
			QPushButton{border:none;color:white}QPushButton:hover{color:blue}")
		sp.setGeometry(0,0,300,200)
		QLabel(sp).resize(300,120)  #这个自定义myWidget里面必须有东西 不能为空，否则无法定义样式
		# label.resize(300,120)
		# ----------------头部内部组件-------------------------
		#------播放器名字
		QLabel(u"～梦音乐v1.0～",sp) .setGeometry(10,5,100,20)
		#------关闭按钮
		closeBtn = QPushButton(u"关闭",sp) 
		closeBtn.setGeometry(260,5,30,20)
		closeBtn.clicked.connect(self.quitit)
		#------隐藏到托盘
		hideBtn = QPushButton(u"隐藏",sp) 
		hideBtn.setGeometry(220,5,30,20)
		hideBtn.clicked.connect(self.hideit)
		# ------歌手头像
		songerPic = QLabel(sp)
		songerPic.setGeometry(10,30,72,72)
		img = QImage("src/songer.png")
		img = img.scaled(70,120,Qt.KeepAspectRatio)
		songerPic.setPixmap(QPixmap.fromImage(img))
		# ------当前播放的歌名
		QLabel(u"我可以抱你吗-张惠妹",sp).setGeometry(110,25,200,20)
		#-------上一曲
		preSong = QLabel(sp) 
		preSong.setGeometry(120,60,24,24)
		img = QImage("src/pre.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		preSong.setPixmap(QPixmap.fromImage(img))
		#--------播放
		preSong = QLabel(sp) 
		preSong.setGeometry(160,48,50,50)
		img = QImage("src/play.png")
		img = img.scaled(48,48,Qt.KeepAspectRatio)
		preSong.setPixmap(QPixmap.fromImage(img))
		#--------下一曲
		preSong = QLabel(sp) 
		preSong.setGeometry(225,60,24,24)
		img = QImage("src/next.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		preSong.setPixmap(QPixmap.fromImage(img))
		# ===========================滚动条==============================
		proWgt = QWidget(self)
		proWgt.setGeometry(0, 110, 300,10)
		proWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# ===========================歌曲列表==============================
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 120, 300,440)
		listWgt.setStyleSheet("QWidget{color:white;background:white;border:1px solid #5FB9FA;border-top:none;border-bottom:none}")
		songList = QListWidget(listWgt)
		songList.resize(260,440)   
		songList.setStyleSheet("QListWidget{color:gray;font-size:12px;background:#FAFAFD;}\
		    QScrollBar{width:0;height:0}\
		    ")
		# =============================底部=============================
		foot = QWidget(self)
		foot.setGeometry(0, 560, 300,40)
		foot.setStyleSheet("QWidget{color:white;background:#7FAEE4;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		QPushButton{border:none;color:white}QPushButton:hover{color:red}")
		QPushButton(u"addFile",foot).setGeometry(0,0,60,40)
		QPushButton(u"搜MV",foot).setGeometry(60,0,60,40)
		QPushButton(u"热榜",foot).setGeometry(120,0,60,40)
		QPushButton(u"新歌",foot).setGeometry(180,0,60,40)
		QPushButton(u"搜歌",foot).setGeometry(240,0,60,40)
		# ==========================托盘==================================
		tray = QSystemTrayIcon(self)
		icon = QIcon('src/tray.png')
		tray.setIcon(icon)
		trayIconMenu = QMenu(self)
		quitAction = QAction(u"退出 ", self,triggered=self.quitit)
		showAction = QAction(icon,u"显示主面板", self,triggered=self.showit)
		trayIconMenu.addAction(showAction)
		trayIconMenu.addAction(quitAction)
		tray.setContextMenu(trayIconMenu)
		tray.show()
	# ===========================回调函数===========================
	def quitit(self):
		self.close()
	def showit(self):
		self.show()
	def hideit(self):
		self.hide()
	# ========================================================
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = main()
	demo.show()
	sys.exit(app.exec_())