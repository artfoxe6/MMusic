#coding=utf-8
"""
为了更加灵活的扩展和修改程序逻辑,
我不直接使用一部分Qt的组件,而是去继承这些组件封装一些自己的逻辑
所以你在其他文件中看到一些莫名其妙的名称的组件,请到这里面查找
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
#播放器外框
class windowWidget(QWidget):
	def __init__(self):
		super(windowWidget,self).__init__()

# 播放器头部Widget
class headWidget(QWidget):
	def __init__(self,window):
		super(headWidget,self).__init__()
		self.window = window
	#重写三个方法使头部支持拖动,上面参数window就是拖动对象
	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.m_drag=True
			self.window.m_DragPosition=event.globalPos()-self.window.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))
	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() and Qt.LeftButton and self.m_drag:
			self.window.move(QMouseEvent.globalPos()-self.window.m_DragPosition)
			QMouseEvent.accept()
	def mouseReleaseEvent(self, QMouseEvent):
		self.m_drag=False
		self.setCursor(QCursor(Qt.ArrowCursor))


# ================自定义QLabel类=====================

class myLabel(QLabel):
	def __init__(self,action,player):
		super(myLabel,self).__init__()
		self.action = action;
		self.player = player;

	def mousePressEvent(self,event):
		if self.action == 'presong':
			self.player.pre()
		elif self.action == 'nextsong':
			self.player.next()
		elif self.action == "playsong":
			self.player.playsong()
