#!/user/bin/env python
#coding=utf-8

import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# -----------------------自定义myWidget类，实现鼠标拖动-------------------
#这个自定义myWidget里面必须有自节点，否则无法定义样式，参见下面的测试代码
class myWidget(QWidget):
	def __init__(self,window):   #window参数是要被移动的窗口
		super(myWidget,self).__init__()
		self.window = window
	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.m_drag=True
			self.window.m_DragPosition=event.globalPos()-self.window.pos()
			print event.globalPos()
			print self.window.pos()
			event.accept()
	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() and Qt.LeftButton and self.m_drag:
			self.window.move(QMouseEvent.globalPos()-self.window.m_DragPosition)
			QMouseEvent.accept()
	def mouseReleaseEvent(self, QMouseEvent):
		self.m_drag=False

# ----------------测试-------------------
class window(QWidget):
	def __init__(self):
		super(window,self).__init__()
		self.resize(200,200)
		self.dropWd()
		self.staticWd()
	def dropWd(self):
		dp = QWidget(self);
		dp.setGeometry(150,150,50,50)
		dp.setStyleSheet("QWidget{background:red}")
		dp.show()
	def staticWd(self):
		sp = myWidget(self)   #这里的self就是被移动的窗口
		sp.setParent (self)  #这里的self是所属父级
		sp.setStyleSheet("QWidget{background:blue}")
		sp.resize(50,50)
		label = QLabel("haha",sp)  #这个自定义myWidget里面必须有东西 不能为空，否则无法定义样式
		label.resize(50,50)
		label.show()
		sp.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	demo = window()
	demo.show()
	sys.exit(app.exec_())