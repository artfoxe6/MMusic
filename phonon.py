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
		for index ,value in enumerate (listfile): 
			if value == '' or value[-3:] != 'mp3':
				continue
			self.songlist[index] = songpath+"/"+value
			# print self.songlist[index]
			item = QListWidgetItem ("   "+str(index+1)+"   "+os.path.basename(value)[0:-4])
			item.setSizeHint (QSize(250,35))
			self.window.songList.addItem(item)

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
		self.window.songName.setText( os.path.basename(songUrl)[:-4] )
		
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
		
	#============================播放暂停=====================================
	def pause(self):
		if self.mediaObject.state() == Phonon.PlayingState:
			self.mediaObject.pause()
			
		elif self.mediaObject.state() == Phonon.PausedState:
			self.mediaObject.play() 
		elif self.mediaObject.state() == Phonon.StoppedState:
			self.next()
			
# ============================回调函数============================================
	# ------------播放状态发生改变-----------------------
	def stateChange(self, newstate, oldstate):
		if newstate == Phonon.PlayingState:  
			#改变播放按钮状态
			img = QImage("src/pause.png")
			img = img.scaled(48,48,Qt.KeepAspectRatio)
			self.window.play.setPixmap(QPixmap.fromImage(img))
			#把正在播放的歌曲标记未选择状态
			self.window.songList.setCurrentItem(self.window.songList.item(self.songing))
		elif newstate == Phonon.StoppedState:
			pass
		elif newstate == Phonon.PausedState:
			img = QImage("src/play.png")
			img = img.scaled(48,48,Qt.KeepAspectRatio)
			self.window.play.setPixmap(QPixmap.fromImage(img))
		elif newstate == Phonon.ErrorState:  
			source = self.mediaObject.currentSource().fileName()   #抛出播放出错的文件名
			print 'ERROR: could not play:', source.toLocal8Bit().data()
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