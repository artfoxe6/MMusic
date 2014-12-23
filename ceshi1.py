#coding=utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon

class Window(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self, 'Choose File')   #将一个按钮作为主窗口，谁说不可以。你试试
        self.mediaObject = Phonon.MediaObject(self)   #实例化一个媒体对象
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)   #实例化音频输出
        Phonon.createPath(self.mediaObject, self.audioOutput)   #将上面的媒体对象作为音频来源并对接到音频输出
        self.mediaObject.stateChanged.connect(self.handleStateChanged)  #播放状态改变触发事件
        self.clicked.connect(self.handleButton) #单击按钮事件

    def handleButton(self):   #按下按钮后检测当前的播放状态，如果为播放状态，那么停止
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()
        else:   #如果状态本身就是停止的那么就打开文件对话框选择媒体
            path = QtGui.QFileDialog.getOpenFileName(self, self.text())  #第二个参数是设置打开文件对话框默认在当前工作目录
            if path:
                self.mediaObject.setCurrentSource(Phonon.MediaSource(path))  #把这个文件放到当前的播放队列的第一个位置（这个位置不是我们看到的列表里面的位置，而是播放位置）
                self.mediaObject.play()  #开始播放

    def handleStateChanged(self, newstate, oldstate):   #当播放状态该表时触发这个函数
        if newstate == Phonon.PlayingState:  #检查播放状态
            self.setText('Stop')
        elif newstate == Phonon.StoppedState:
            self.setText('Choose File')
        elif newstate == Phonon.ErrorState:  #判断播放异常，这个很实用
            source = self.mediaObject.currentSource().fileName()   #抛出播放出错的文件名
            print 'ERROR: could not play:', source.toLocal8Bit().data()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Phonon')
    win = Window()
    win.resize(200, 100)
    win.show()
    sys.exit(app.exec_())