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
from mv import *

class main(QWidget):
	def __init__(self):
		super(main,self).__init__()
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setGeometry(300, 30, 300,600)
		self.addLayout()
		self.player = player(self)
		self.slowLayout()
	def  addLayout(self):
		# ==========================头部=================================
		self.head = headWidget(self)   #这里的self就是被移动的窗口
		self.head.setParent (self)  #这里的self是所属父级
		self.setStyleSheet("QWidget{background:#7FAEE4;border:1px solid #5FB9FA;border-top:none;border-bottom:none}QLabel{color:white;border:none}\
			QSlider{width:300px;height:10px}\
			QPushButton{border:none;color:white}QPushButton:hover{color:blue}\
			QSlider::groove:horizontal { border: 1px solid #999999;height: 10px; margin: 0px 0;    }\
	            QSlider::handle:horizontal  { border: 1px solid #5c5c5c;border-image:url(src/ico.png);width: 18px;margin: -7px -7px -7px -7px; }\
	            QSlider::sub-page:horizontal{ background: QLinearGradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #9EEAFD, stop:0.25 \
	                #627BF3, stop:0.5 #627BF3, stop:1 #9EEAFD);    }\
	            QSlider::add-page:horizontal{background:QLinearGradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #9EEAFD, \
	                stop:0.25 #E6E6E6, stop:0.5 #E6E6E6, stop:1 #9EEAFD);}\
	        VolumeSlider{background:red}\
			")
		#滚动条样式参见：http://blog.sina.com.cn/s/blog_791f544a0100s2ml.html
		self.head.setGeometry(0,0,300,200)
		QLabel(self.head).resize(300,120)  #这个自定义myWidget里面必须有东西 不能为空，否则无法定义样式
		# label.resize(300,120)
		# ----------------头部内部组件-------------------------
		#------播放器名字
		QLabel(u"～梦音乐v1.0～",self.head) .setGeometry(10,5,100,20)
		#------关闭按钮
		closeBtn = QPushButton(u"关闭",self.head) 
		closeBtn.setGeometry(260,5,30,20)
		closeBtn.clicked.connect(self.quitit)
		#------隐藏到托盘
		hideBtn = QPushButton(u"隐藏",self.head) 
		hideBtn.setGeometry(220,5,30,20)
		hideBtn.clicked.connect(self.hideit)
		# ------歌手头像
		self.songerPic = QLabel(self.head)
		self.songerPic.setGeometry(10,30,72,72)
		img = QImage("src/songer.png")
		img = img.scaled(70,120,Qt.KeepAspectRatio)
		self.songerPic.setPixmap(QPixmap.fromImage(img))
		# ------当前播放的歌名
		self.songName = QLabel(u"我可以抱你吗-张惠妹",self.head)
		self.songName.setAlignment(Qt.AlignHCenter)
		self.songName.setGeometry(110,25,150,20)
		# ===========================进度条==============================
		self.proWgt = QWidget(self)
		self.proWgt.setGeometry(0, 110, 300,10)
		self.proWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# ===========================歌曲列表==============================
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 120, 300,430)
		listWgt.setStyleSheet("QWidget{color:white;background:white;border:1px solid #5FB9FA;border-top:none;border-bottom:none}")
		self.songList = QListWidget(listWgt)
		self.songList.resize(260,430)   
		self.songList.setStyleSheet("QListWidget{color:gray;font-size:12px;background:#FAFAFD;}\
		    QScrollBar{width:0;height:0}\
		    ")
		self.songList.itemDoubleClicked.connect(self.playit)
		# ================================音量========================
		self.vluWgt = QWidget(self)
		self.vluWgt.setGeometry(0, 550, 300,10)
		self.vluWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# =============================底部=============================
		foot = QWidget(self)
		foot.setGeometry(0, 560, 300,40)
		foot.setStyleSheet("QWidget{color:white;background:#7FAEE4;border:1px solid #5FB9FA;border-top:none;border-bottom:none}\
		QPushButton{border:none;color:white}QPushButton:hover{color:red}")
		setBtn = QPushButton(u"设置",foot)
		setBtn.setGeometry(0,0,60,40)
		setBtn.clicked.connect(self.setFunc)
		mvBtn = QPushButton(u"MV",foot)
		mvBtn.setGeometry(60,0,60,40)
		mvBtn.clicked.connect(self.mvFunc)

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
		tray.activated.connect(self.trayIcon_DoubleClicked)
	# -----------------由于组件之间逻辑先后调用，把一部分组件延后加载-----------------
	def slowLayout(self):
		#-------上一曲
		self.preSong = myLabel('presong',self.player) 
		self.preSong.setParent(self.head)
		self.preSong.setGeometry(120,60,24,24)
		img = QImage("src/pre.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.preSong.setPixmap(QPixmap.fromImage(img))
		#--------下一曲
		self.nextSong = myLabel('nextsong',self.player) 
		self.nextSong.setParent(self.head)
		self.nextSong.setGeometry(225,60,24,24)
		img = QImage("src/next.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.nextSong.setPixmap(QPixmap.fromImage(img))
		#--------播放
		self.play = myLabel('playsong',self.player) 
		self.play.setParent(self.head)
		self.play.setGeometry(160,48,50,50)
		img = QImage("src/play.png")
		img = img.scaled(48,48,Qt.KeepAspectRatio)
		self.play.setPixmap(QPixmap.fromImage(img))
	# ===========================回调函数===========================
	def quitit(self):
		self.close()
	def showit(self):
		self.show()
	def hideit(self):
		self.hide()
	def playit(self,item):
		self.player.playit(item.text())
	def selectDir(self):
		path = QFileDialog.getExistingDirectory(self.popSetWg)
		self.popSetWg.line.setText(path)
		fil = open("local.py","r").read().split("+++")
		if path:
			fil[0] = str(path)
			open("local.py","w").write("+++".join(fil))
			self.player.playlist()
	def trayIcon_DoubleClicked(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			self.show()
	#打开设置窗口
	def setFunc(self):
		self.move(100,30)
		self.popSetWg = popWindow (self.pos())
		self.popSetWg.setStyleSheet("QLabel{color:blue}QPushButton{border:1px solid blue;color:blue}")
		self.popSetWg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		lab = QLabel(u"默认歌曲路径",self.popSetWg)
		lab.setGeometry(10,40,200,25)
		self.popSetWg.line = QLineEdit(self.popSetWg)
		self.popSetWg.line.setGeometry(10,65,400,30)
		btn = QPushButton(u"选择文件夹",self.popSetWg)
		btn.setGeometry(410,65,100,30)
		btn.clicked.connect(self.selectDir)
		self.popSetWg.show()
	#打开mv窗口
	def mvFunc(self):
		self.move(100,30)
		self.popMvWg = popWindow (self.pos())
		self.popMvWg.setStyleSheet("QLabel{color:white}QPushButton{border:none}")
		self.popMvWg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		lab = QLabel(u" MV频道测试",self.popMvWg)
		lab.setAlignment(Qt.AlignHCenter)
		lab.setGeometry(10,10,100,25)
		self.popMvWg.line = QLineEdit(self.popMvWg)
		self.popMvWg.line.setGeometry(10,35,600,30)
		btn = QPushButton(u"搜索",self.popMvWg)
		btn.setGeometry(630,35,100,30)
		btn.clicked.connect(self.showMv)
		
		self.mvbox = QWidget(self.popMvWg)
		self.mvbox.setGeometry(0,70,800,380)
		self.mvbox.setStyleSheet("QWidget{background:#DCECFF}")
		self.popMvWg.show()
		# -----mv位置布局-----------
		mvs = BaiDuMV()
		recs = mvs.recommend()
		arr = recs.split("|||")
		arr.pop()
		listfile=os.listdir("icon")
		print listfile
		hbox1  = QHBoxLayout()
		for img in range(5):
			item = QLabel("") 
			item.resize(140,140)
			x = arr.pop()
			img = QImage(x.split("+++")[1])
			img = img.scaled(140,80,Qt.KeepAspectRatio)
			item.setPixmap(QPixmap.fromImage(img))
			hbox1.addWidget(item)
		hbox2  = QHBoxLayout()
		for img in range(5):
			item = QLabel("") 
			item.resize(140,140)
			x = arr.pop()
			img = QImage(x.split("+++")[1])
			img = img.scaled(140,80,Qt.KeepAspectRatio)
			item.setPixmap(QPixmap.fromImage(img))
			hbox2.addWidget(item)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox1)
		self.mvbox.setLayout(vbox)

		
	#加载MV
	def showMv(self):
		pass
	# ========================================================



if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = main()
	demo.show()
	sys.exit(app.exec_())