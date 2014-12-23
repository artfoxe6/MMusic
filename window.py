#!/user/bin/env python
#coding=utf-8
"""
播放器框架，只负责外观，不涉及逻辑
"""

import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from myClass import *
from phonon import *

class main(QWidget):
	def __init__(self):
		super(main,self).__init__()
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setGeometry(300, 30, 300,600)
		self.addLayout()
		self.player = player(self)
	def  addLayout(self):
		# ==========================头部=================================
		sp = headWidget(self)   #这里的self就是被移动的窗口
		sp.setParent (self)  #这里的self是所属父级
		self.setStyleSheet("QWidget{background:#7FAEE4;border:1px solid #5FB9FA;border-top:none;border-bottom:none}QLabel{color:white;border:none}\
			QPushButton{border:none;color:white}QPushButton:hover{color:blue}\
			QSlider{width:300px;height:20px}\
			QSlider::handle:horizontal{background:#2EB4FF;width:18px;}\
			QSlider::sub-page:horizontal{background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 pink, stop:0.25 blue, stop:0.5 blue, stop:1 pink)}\
			QSlider::add-page:horizontal{background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 orange, stop:0.25 white, stop:0.5 orange, stop:1 white)}\
			")
		#滚动条样式参见：http://blog.sina.com.cn/s/blog_791f544a0100s2ml.html
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
		self.songerPic = QLabel(sp)
		self.songerPic.setGeometry(10,30,72,72)
		img = QImage("src/songer.png")
		img = img.scaled(70,120,Qt.KeepAspectRatio)
		self.songerPic.setPixmap(QPixmap.fromImage(img))
		# ------当前播放的歌名
		self.songName = QLabel(u"我可以抱你吗-张惠妹",sp)
		self.songName.setGeometry(110,25,200,20)
		#-------上一曲
		self.preSong = QLabel(sp) 
		self.preSong.setGeometry(120,60,24,24)
		img = QImage("src/pre.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.preSong.setPixmap(QPixmap.fromImage(img))
		#--------播放
		self.play = QLabel(sp) 
		self.play.setGeometry(160,48,50,50)
		img = QImage("src/play.png")
		img = img.scaled(48,48,Qt.KeepAspectRatio)
		self.play.setPixmap(QPixmap.fromImage(img))
		#--------下一曲
		self.nextSong = QLabel(sp) 
		self.nextSong.setGeometry(225,60,24,24)
		img = QImage("src/next.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.nextSong.setPixmap(QPixmap.fromImage(img))
		# ===========================进度条==============================
		self.proWgt = QWidget(self)
		self.proWgt.setGeometry(0, 110, 300,10)
		self.proWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# ===========================歌曲列表==============================
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 120, 300,440)
		listWgt.setStyleSheet("QWidget{color:white;background:white;border:1px solid #5FB9FA;border-top:none;border-bottom:none}")
		self.songList = QListWidget(listWgt)
		self.songList.resize(260,440)   
		self.songList.setStyleSheet("QListWidget{color:gray;font-size:12px;background:#FAFAFD;}\
		    QScrollBar{width:0;height:0}\
		    ")
		self.songList.itemDoubleClicked.connect(self.playit)
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
	def playit(self,item):
		self.player.playit(item.text())
	# ========================================================
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = main()
	demo.show()
	sys.exit(app.exec_())