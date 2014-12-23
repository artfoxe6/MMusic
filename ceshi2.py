# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

class AudioPlayer(QtGui.QWidget):
    def __init__(self, url, parent = None):  
    #url参数就是你的MP3地址  

        self.url = url

        QtGui.QWidget.__init__(self, parent) 

        #设置一些窗口尺寸的策略，不用设置也会有默认策略，干脆注释了，无影响
        # self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)

	#创建一个音乐播放器  这是一种简单的方法，功能自然也是很单一，貌似只能实现简单的单首歌曲播放（希望我没有猜错，），更灵活的是使用AudioOutput，MediaObject等方法实现
        self.player = Phonon.createPlayer(Phonon.MusicCategory,Phonon.MediaSource(url))
        #下面这句话真没搞懂，谷歌了一下  多次尝试没反应  干脆把他注释了。。不影响程序
        # self.player.setTickInterval(100)
        self.player.tick.connect(self.tock)   #播放进度改变触发事件

        self.play_pause = QtGui.QPushButton(self)  #播放按钮
        self.play_pause.setIcon(QtGui.QIcon('icons/49heart.svg'))  #设置播放按钮图标，jpg，png都可以
        self.play_pause.clicked.connect(self.playClicked)  #播放按钮单击事件
        self.player.stateChanged.connect(self.stateChanged)  #播放状态改变触发事件

        self.slider = Phonon.SeekSlider(self.player , self)  #进度条

        self.status = QtGui.QLabel(self)  #Label组件用来显示播放的当前时间
        self.status.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter) #设置Label的对齐方式  左对齐或居中

        layout = QtGui.QHBoxLayout(self)  #水平布局
        layout.addWidget(self.play_pause)   #添加播放按钮
        layout.addWidget(self.slider)  #添加滑动条
        layout.addWidget(self.status)  #添加播放状态

    def playClicked(self):
        if self.player.state() == Phonon.PlayingState:  #如果为播放状态
            self.player.pause()   #暂停
        else:
            self.player.play()    #开始播放

    def stateChanged(self, new, old):
        if new == Phonon.PlayingState:   #根据改变后的状态更换播放图标
            self.play_pause.setIcon(QtGui.QIcon('icons/49heart.svg'))
        else:
            self.play_pause.setIcon(QtGui.QIcon('icons/49heart.svg'))

    def tock(self, time):  #播放进度改变时用来更新上面Label组件里面的当前播放时间time参数就是歌曲当前所在的时间刻，流中的媒体对象的当前位置是由时间参数给出  以毫秒为单位
        time = time/1000   #除以1000得到秒单位
        h = time/3600   #小时
        m = (time-3600*h) / 60  #分钟
        s = (time-3600*h-m*60)  #秒
        self.status.setText('%02d:%02d:%02d'%(h,m,s))  #更新Label显示的播放时间进度

def main():
    app = QtGui.QApplication(sys.argv)
    window=AudioPlayer(sys.argv[1])   #在命令行下的第二个参数 你的歌曲路径
    window.show()  #显示主窗口
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# 测试：  python mp3player.py  mymusic.mp3