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