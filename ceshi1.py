<<<<<<< HEAD
import multiprocessing
import time

def worker(d, key, value):
    # print key,value
    d[key] = value

if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [ multiprocessing.Process(target=worker, args=(d, i, i*2))
             for i in range(10) 
             ]
    # print jobs
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print ('Results:' )
    for key , value in dict(d).items():
       print key , value
=======
#coding=utf-8

import os
import sys
import subprocess
import os.path

from PyQt4 import QtGui
from PyQt4 import QtCore

class MyWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setWindowTitle("My Window")
        self.setWindowIcon(QtGui.QIcon('play.png'))
        self.show()

def main(args):
    app = QtGui.QApplication([])

    ww= MyWin()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv[1:])
>>>>>>> b19a5e93d5021d9d9b4383f0ab2c45970c2ea5aa
