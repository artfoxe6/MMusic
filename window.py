#!/user/bin/env python
#coding=utf-8
"""
播放器框架，只负责外观，（基本）不涉及逻辑
"""
from __future__ import unicode_literals   #防止乱码
import sys,os
from multiprocessing import Process, Queue , Manager
import threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from myClass import *
from phonon import *
from mv import *
from search import *
import ctypes
#告诉windows我这个程序是单独的  不是python  否则设置任务栏图标无效
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class main(QWidget):
	def __init__(self):
		super(main,self).__init__()
		#隐藏边框
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setGeometry(300, 30, 300,600)
		self.addLayout()
		self.player = player(self)
		self.slowLayout()
	def  addLayout(self):
		# ==========================头部=================================
		self.head = headWidget(self)   #这里的self就是被移动的窗口
		self.head.setParent (self)  #这里的self是所属父级
		self.setStyleSheet("QWidget{background:#9B0069;font:Serif;border:1px solid #9B0069;border-top:none;border-bottom:none}QLabel{color:white;border:none}\
			QSlider{width:298px;height:10px}\
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
		QLabel(u" ♫ 梦音乐 ♫ ",self.head) .setGeometry(10,5,100,20)
		#------关闭按钮
		closeBtn = QPushButton(u"╳",self.head) 
		# closeBtn.setStyleSheet("QPushButton{border-image:url(src/close11.png)}")
		closeBtn.setGeometry(260,5,30,20)
		closeBtn.clicked.connect(self.quitit)
		#------隐藏到托盘
		hideBtn = QPushButton(u"一",self.head) 
		# hideBtn.setStyleSheet("QPushButton{border-image:url(src/sam11.png)}")
		hideBtn.setGeometry(220,5,30,20)
		hideBtn.clicked.connect(self.hideit)
		# ------歌手头像
		self.songerPic = QLabel(self.head)
		self.songerPic.setGeometry(10,30,72,72)
		img = QImage("src/tray.jpg")
		img = img.scaled(70,120,Qt.KeepAspectRatio)
		self.songerPic.setPixmap(QPixmap.fromImage(img))
		# ------当前播放的歌名
		self.songName = QLabel(u"",self.head)
		self.songName.setAlignment(Qt.AlignHCenter)
		self.songName.setGeometry(110,25,150,20)
		# ===========================进度条==============================
		self.proWgt = QWidget(self)
		self.proWgt.setGeometry(0, 110, 300,10)
		self.proWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #9B0069;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# ===========================歌曲列表==============================
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 120, 300,430)
		listWgt.setStyleSheet("QWidget{color:white;background:white;border:1px solid #9B0069;border-top:none;border-bottom:none}")
		self.songList = QListWidget(listWgt)
		self.songList.resize(260,430)   
		self.songList.setStyleSheet("QListWidget{color:gray;font-size:12px;background:#FAFAFD;}\
		    QScrollBar{width:0;height:0}\
		    ")
		self.songList.itemDoubleClicked.connect(self.playit)
		# ================================音量========================
		self.vluWgt = QWidget(self)
		self.vluWgt.setGeometry(0, 550, 300,10)
		self.vluWgt.setStyleSheet("QWidget{background-color:#C9C9C9;border:1px solid #9B0069;border-top:none;border-bottom:none}\
		    SeekSlider{width:300}")
		# =============================底部=============================
		foot = QWidget(self)
		foot.setGeometry(0, 560, 300,40)
		foot.setStyleSheet("""QWidget{color:white;background:#9B0069;border:1px solid #9B0069;border-top:none;border-bottom:none}
		QPushButton{border:none;color:white}QPushButton:hover{color:red}QPushButton#setBtnIcon{border-image:url(play.png)}
		QPushButton#setBtnIcon{background-image:url(src/001.png);background-repeat:no-repeat;background-position:center}
		QPushButton#mvBtn{background-image:url(src/002.png);background-repeat:no-repeat;background-position:center}
		QPushButton#hotBtn{background-image:url(src/003.png);background-repeat:no-repeat;background-position:center}
		QPushButton#newBtn{background-image:url(src/004.png);background-repeat:no-repeat;background-position:center}
		QPushButton#seaBtn{background-image:url(src/005.png);background-repeat:no-repeat;background-position:center}
		""")
		setBtn = QPushButton(u"",foot)
		setBtn.setObjectName("setBtnIcon")
		setBtn.setGeometry(0,0,60,40)
		setBtn.clicked.connect(self.setFunc)

		mvBtn = QPushButton(u"",foot)
		mvBtn.setObjectName("mvBtn")
		mvBtn.setGeometry(60,0,60,40)
		# mvBtn.clicked.connect(self.mvFunc)

		hotBtn = QPushButton(u"",foot)
		hotBtn.setGeometry(120,0,60,40)
		hotBtn.setObjectName("hotBtn")
		newBtn = QPushButton(u"",foot)
		newBtn.setGeometry(180,0,60,40)
		newBtn.setObjectName("newBtn")
		searchBtn = QPushButton(u"",foot)
		searchBtn.setGeometry(240,0,60,40)
		searchBtn.setObjectName("seaBtn")
		searchBtn.clicked.connect(self.searchSong)
		# ==========================托盘==================================
		tray = QSystemTrayIcon(self)
		icon = QIcon('src/tray.png')
		tray.setIcon(icon)
		trayIconMenu = QMenu(self)
		preAction = QAction(u"上一曲 ", self,triggered=self.preit)
		pauseAction = QAction(u"暂停|播放 ", self,triggered=self.pauseit)
		nextAction = QAction(u"下一曲 ", self,triggered=self.nextit)
		quitAction = QAction(u"退出 ", self,triggered=self.quitit)
		showAction = QAction(icon,u"显示主面板", self,triggered=self.showit)
		trayIconMenu.addAction(showAction)
		trayIconMenu.addAction(preAction)
		trayIconMenu.addAction(pauseAction)
		trayIconMenu.addAction(nextAction)
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
		img = QImage("src/pre11.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.preSong.setPixmap(QPixmap.fromImage(img))
		#--------下一曲
		self.nextSong = myLabel('nextsong',self.player) 
		self.nextSong.setParent(self.head)
		self.nextSong.setGeometry(225,60,24,24)
		img = QImage("src/next11.png")
		img = img.scaled(24,24,Qt.KeepAspectRatio)
		self.nextSong.setPixmap(QPixmap.fromImage(img))
		#--------播放
		self.play = myLabel('playsong',self.player) 
		self.play.setParent(self.head)
		self.play.setGeometry(160,48,50,50)
		img = QImage("src/play11.png")
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
	def nextit(self):
		self.player.next()
	def preit(self):
		self.player.pre()
	def pauseit(self):
		self.player.pause()
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
		self.move(150,50)
		self.popSetWg = popWindow (self.pos())
		self.popSetWg.setStyleSheet("QLabel{color:blue}QPushButton{border:1px solid blue;color:blue}")
		self.popSetWg.setWindowFlags(Qt.FramelessWindowHint)
		lab = QLabel(u"默认歌曲路径",self.popSetWg)
		lab.setGeometry(10,40,200,25)
		self.popSetWg.line = QLineEdit(self.popSetWg)
		self.popSetWg.line.setGeometry(10,65,400,30)
		btn = QPushButton(u"选择文件夹",self.popSetWg)
		btn.setGeometry(410,65,100,30)
		btn.clicked.connect(self.selectDir)
		self.popSetWg.show()

	# 歌曲搜索
	def searchSong(self):
		self.move(150,50)
		self.popSearch = popWindow (self.pos())
		self.popSearch.setStyleSheet("QWidget{background:#DCECFF}QLabel{background:none;color:white}QLineEdit{background:none}")
		self.popSearch.setWindowFlags(Qt.FramelessWindowHint )
		lab = QLabel(u" 在线音乐",self.popSearch)
		lab.setAlignment(Qt.AlignHCenter)
		lab.setGeometry(400,5,100,25)
		self.popSearch.line = QLineEdit(self.popSearch)
		self.popSearch.line.setGeometry(10,45,500,30)
		# self.popSearch.line.setText("冰 雨".decode('utf-8'))
		btn = QPushButton(u"搜索",self.popSearch)
		btn.setGeometry(530,45,100,30)
		btn.clicked.connect(self.search)
		# 结果列表----------------------------------------------------------------------------------------
		self.popSearch.myTable = QTableWidget(20,5,self.popSearch)
		self.popSearch.myTable.setStyleSheet("QPushButton{color:#9B0069;border:none}QScrollBar{width:0;height:0}")
		self.popSearch.myTable.setGeometry(0,90,700,450)
		# self.popSearch.myTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:pink;}")   #表头颜色
		# self.popSearch.myTable.horizontalHeader().setClickable(False)   #表头不可点击 (默认点击排序)
		self.popSearch.myTable.setFrameShape(QFrame.NoFrame)
		# self.popSearch.myTable.setShowGrid(False)   #隐藏格子线
		self.popSearch.myTable.setHorizontalHeaderLabels([u"歌名",u"歌手",u'操作',u"下载进度",u"下载链接"])
		self.popSearch.myTable.setColumnHidden(4,True)
		self.popSearch.myTable.horizontalHeader().setStretchLastSection(True)
		self.popSearch.myTable.verticalHeader().setDefaultSectionSize(25)
		self.popSearch.myTable.verticalHeader().setVisible(False)
		self.popSearch.myTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.popSearch.myTable.horizontalHeader().resizeSection(0,250)
		self.popSearch.myTable.horizontalHeader().resizeSection(1,150)
		self.popSearch.myTable.horizontalHeader().resizeSection(2,50)
		self.popSearch.myTable.cellClicked.connect(self.downit) 
		self.popSearch.show()
		
	#加载MV
	def showMv(self):
		pass
	def search(self):
		self.popSearch.myTable.clear()
		self.popSearch.myTable.setHorizontalHeaderLabels([u"歌名",u"歌手",u'操作',u"下载进度",u"下载链接"])
		song = unicode(self.popSearch.line.text())
		# print type(song)
		bMusic = BaiDuMusic()
		res_arr = bMusic.search(song)
		# # print res_arr
		for index ,x in enumerate (res_arr): 
			# -----歌名
			print x.split("+++")[2].decode("utf-8")
			item1 = QTableWidgetItem(x.split("+++")[2].decode("utf-8"))
			# item1.setBackgroundColor(QColor("blue"))
			item1.setTextColor(QColor(155,0,105))
			self.popSearch.myTable.setItem(index,0,item1)
			# -----歌手
			item2 = QTableWidgetItem(x.split("+++")[1].decode('utf-8'))
			# item2.setBackgroundColor(QColor("blue"))
			item2.setTextColor(QColor(155,0,105))
			self.popSearch.myTable.setItem(index,1,item2)
			# -----下载
			item3 = QTableWidgetItem(u"下载")
			item3.setTextColor(QColor(155,0,105))
			self.popSearch.myTable.setItem(index,2,item3)
			# -----进度条
			progressBar = QProgressBar()
			
			progressBar.setMaximum(100)
			# progressBar.setValue(20)
			progressBar.setStyleSheet('''QProgressBar {background:red;height:10px;width:10px} 
			                             QProgressBar::chunk {background:blue}''')
			self.popSearch.myTable.setCellWidget(index,3,progressBar)

			item4 = QTableWidgetItem(x.split("+++")[0].decode('utf-8'))
			# item2.setBackgroundColor(QColor("blue"))
			item4.setTextColor(QColor(155,0,105))
			self.popSearch.myTable.setItem(index,4,item4)
	def downit(self,x,y):
		if y!=2:
			return
		songid = self.popSearch.myTable.item(x,4).text()
		songname = self.popSearch.myTable.item(x,0).text()
		self.mgr = Manager()
		d = self.mgr.dict()
		bMusic = BaiDuMusic()
		obj = self.popSearch.myTable.cellWidget(x, 3)
		t = threading.Thread(target=bMusic.download, args=(str(songid),str(songname),obj))
		t.start()
		t.join()
		self.player.playlist()
		# Process(target=bMusic.download, args=(str(songid),str(songname),d)).start()
		# while int(d[0]) <=100:
				# self.popSearch.myTable.cellWidget(int(d[1]), 3).setValue(d[0])	
		# self.download(songid,str(songname))
		# Process(target=self.download, args=(),self.per).start()
	# ========================================================
	# #歌曲下载
	# def download(self,songid,songName,savePath="down/"):
	# 	# self.pids.put(os.getpid())
	# 	songNewUrl = "http://music.baidu.com/data/music/file?link=&song_id="+str(songid)
	# 	if not os.path.isdir(savePath):	
	# 		os.makedirs(savePath)
	# 	savemp3 = savePath.decode('utf-8')+songName.decode('utf-8')+u".mp3"
	# 	urllib.urlretrieve(songNewUrl, savemp3,self.cbk) 
	# #下载进度显示
	# def cbk(self,a, b, c):  
	# 	per = 100.0 * a * b / c
	# 	if per > 100:
	# 		per = 100
	# 	self.popSearch.myTable.cellWidget(int(self.index), 3).setValue(per)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = main()
	demo.setWindowIcon(QIcon("src/tray.png"))
	demo.show()
	sys.exit(app.exec_())

