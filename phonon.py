#!/usr/bin/env python
#coding=utf-8
"""
播放相关逻辑
"""

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
		# -------加载播放列表----------
		self.songlist = {}
		self.songing = -1   #当前播放的歌曲编号
		fp = open("songs.list")
		s = fp.read()
		arr = s.split("\n")
		for index ,value in enumerate (arr): 
			self.songlist[index] = value
			item = QListWidgetItem (" "+str(index+1)+"   "+u""+os.path.basename(value)+"")
			item.setSizeHint (QSize(250,35))
			window.songList.addItem(item)
		#----------加载进度条----------
		self.seek = Phonon.SeekSlider(self.mediaObject,window.proWgt) 
    # ==============================播放、暂停======================================
	def playit(self,songUrl=''):
		songNum = (int)(songUrl[1])-1
		songUrl = self.songlist[songNum]
		print u""+songUrl+""
		self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
		self.mediaObject.play()  
	# ==============================下一曲====================================
	def next(self):
		pass
	# ===============================上一曲=====================================
	def pre(self):
		pass

# ============================回调函数============================================
	# ------------播放状态发生改变-----------------------
	def handleButton(self):   
		if self.mediaObject.state() == Phonon.PlayingState:
			pass
		elif  self.mediaObject.state() == Phonon.PausedState:
			pass
		elif  self.mediaObject.state() == Phonon.StoppedState:
			pass
		elif  self.mediaObject.state() == Phonon.ErrorState:
			pass

            

	def handleStateChanged(self, newstate, oldstate):
		if newstate == Phonon.PlayingState:  
			pass
		elif newstate == Phonon.StoppedState:
			pass
		elif newstate == Phonon.PausedState:
			pass
		elif newstate == Phonon.ErrorState:  
			pass
  # ========================事件集合========================================

  	def evt(self):
  		self.mediaObject.stateChanged.connect(self.handleStateChanged)  #播放状态改变触发事件

if __name__ == "__main__":
	fp = open("songs.list")
	s = fp.read()
	arr = s.split("\n")
	for v in arr:
		print v