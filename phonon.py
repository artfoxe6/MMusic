#!/usr/bin/env python
#coding=utf-8
"""
播放相关逻辑
"""
from __future__ import unicode_literals   #防止乱码
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import os,sys
from threading import Timer
from mutagen import File
import time

class player():
	# =========================初始化播放组件=============================================
	def __init__(self,window):  #参数window为播放器父框对象
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.window = window
		self.mediaObject = Phonon.MediaObject(self.window)   #实例化一个媒体对象
		self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self.window)   #实例化音频输出
		Phonon.createPath(self.mediaObject, self.audioOutput)   #将上面的媒体对象作为音频来源并对接到音频输出
		self.mediaObject.stateChanged.connect(self.stateChange)  #播放状态改变触发事件
		self.mediaObject.finished.connect(self.Finished)  #播放状态改变触发事件
		#----------加载进度条----------
		self.seek = Phonon.SeekSlider(self.mediaObject,window.proWgt) 
		self.seek.setIconVisible(False)
		# -----------加载音量条----------
		self.vlu = Phonon.VolumeSlider (self.audioOutput,window.vluWgt) 
		self.vlu.setMuteVisible(False)
		self.vlu.setMaximumVolume(1.5)
		self.vlu.setStyleSheet("""
			QSlider::sub-page:horizontal{ background:QLinearGradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #9EEAFD, 
              stop:0.25 #5FF199, stop:0.5 #5FF199, stop:1 #9EEAFD);    }
	            	QSlider::add-page:horizontal{background: QLinearGradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 orange, stop:0.25 
              orange, stop:0.5 orange, stop:1 orange);}
			""")
		#----------加载播放列表--------
		self.playlist()
	def playlist(self):
		# -------加载播放列表----------
		self.window.songList.clear()
		self.songlist = {}
		self.songing = -5   #当前播放的歌曲编号
		songpath = open("local.py","r").read().split("+++")[0]
		if songpath == "":
			songpath = "music"
		listfile = []
		try:
			listfile=os.listdir(songpath)
		except Exception, e:
			print e
		index = 0
		for value in listfile:
		# for index ,value in enumerate (listfile): 
			if os.path.getsize(songpath+"/"+value) < 10:
				continue
			if value == '' or value[-3:] != 'mp3':
				continue
			self.songlist[index] = songpath+"/"+value
			# print self.songlist[index]
			item = QListWidgetItem ("   "+str(index+1)+"   "+os.path.basename(value)[0:-4])
			item.setSizeHint (QSize(250,35))
			self.window.songList.addItem(item)
			index+=1

    # ==============================指定播放======================================
	def playit(self,songUrl=''):    
		# print str(songUrl).decode('utf-8')
		songUrl = songUrl.split("  ")[1]
		songNum = (int)(songUrl)-1
		songUrl = self.songlist[songNum]
		self.songing = int(songNum)
		# print u""+songUrl+""
		self.mediaObject.setCurrentSource(Phonon.MediaSource(songUrl))
		self.mediaObject.play()  

		# print files.tags['APIC:e'].data
		# print dir(files.tags)
		# self.window.songName.setText( os.path.basename(songUrl)[:-4] )
		
	# def delayrun(self,strs):
		# print u'延迟执行'
		# print strs
		
	# ==============================下一曲====================================
	def next(self):
		lens = len(self.songlist)
		if self.songing == -5:
			self.songing = lens-1
		if lens-self.songing>1:
			songUrl = self.songlist[self.songing+1]
			self.mediaObject.setCurrentSource(Phonon.MediaSource(songUrl))
			self.mediaObject.play()
			self.songing = self.songing+1
		else:
			songUrl = self.songlist[0]
			self.mediaObject.setCurrentSource(Phonon.MediaSource(songUrl))
			self.mediaObject.play()
			self.songing = 0
		# self.window.songName.setText( os.path.basename(songUrl)[:-4] )
		
	# ===============================上一曲=====================================
	def pre(self):
		if self.songing == -5:
			self.songing = 0
		if self.songing != 0:
			self.songing-=1
		else:
			self.songing = len(self.songlist)-1
		songUrl = self.songlist[self.songing]
		self.mediaObject.setCurrentSource(Phonon.MediaSource(songUrl))
		self.mediaObject.play()
		# self.window.songName.setText( os.path.basename(songUrl)[:-4] )
		
	#============================播放暂停=====================================
	def pause(self):
		if self.mediaObject.state() == Phonon.PlayingState:
			self.mediaObject.pause()
			
		elif self.mediaObject.state() == Phonon.PausedState:
			self.mediaObject.play() 
		else:
			self.next()
			
# ============================回调函数============================================
	# ------------播放状态发生改变-----------------------
	def stateChange(self, newstate, oldstate):

		if newstate == Phonon.PlayingState:  
			#解析mp3 meta信息
			metDict = self.mediaObject.metaData()
			try:
				songName = metDict[QString(u'TITLE')][0]
			except Exception, e:
				songName = self.mediaObject.currentSource().fileName() 
				songName = os.path.basename(str(songName))[:-4]
				songName = unicode(songName)
			#刷新当前歌曲的歌名
			self.window.songName.setText(songName)
			#解析mp3文件得到歌曲专辑图片
			files = File(str(self.mediaObject.currentSource().fileName()) )
			# print files.tags
			fc = open("src/temp.jpg","wb")
			try:
				jpg = files.tags['APIC:e'].data
				fc.write(jpg)
				fc.close()
			except Exception, e:
				pass
			# Timer(2,self.tupian).start() 
			
				
			#改变播放按钮状态
			img = QImage("src/pause11.png")
			img = img.scaled(48,48,Qt.KeepAspectRatio)
			self.window.play.setPixmap(QPixmap.fromImage(img))
			#把正在播放的歌曲标记未选择状态
			self.window.songList.setCurrentItem(self.window.songList.item(self.songing))
			#刷新专辑图片
			# time.sleep(3)
			# try:
			if os.path.getsize("src/temp.jpg") <10:
				img = QImage("src/tray.jpg").scaled(70,120,Qt.KeepAspectRatio)
			else:
				img = QImage("src/temp.jpg").scaled(70,120,Qt.KeepAspectRatio)
			self.window.songerPic.setPixmap(QPixmap.fromImage(img))
		elif newstate == Phonon.StoppedState:
			pass
		elif newstate == Phonon.PausedState:
			img = QImage("src/play11.png")
			img = img.scaled(48,48,Qt.KeepAspectRatio)
			self.window.play.setPixmap(QPixmap.fromImage(img))
		elif newstate == Phonon.ErrorState:  
			source = self.mediaObject.currentSource().fileName()   #抛出播放出错的文件名
			print 'ERROR: could not play:', source.toLocal8Bit().data()
		else:
			self.next()
	def Finished(self):
		self.next()
  # ========================事件集合========================================



# =================================================================================
# +++++++++++++++++++++++++++++++++( video player )+++++++++++++++++++++++++++
# ==============================================================================
class mvplayer:
	def __init__(self,window):
		self.window = window






if __name__ == "__main__":
	pass