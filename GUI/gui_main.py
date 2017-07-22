#!/usr/bin/env python2


import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *


class Outer(QtGui.QMainWindow):

    def __init__(self):
        super(Outer, self).__init__()

        self.initUI()


    def initUI(self):

        exitAction = QtGui.QAction(QtGui.QIcon('web.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(exitAction)

        self.resize(640, 480)
        self.center()
        self.block = Block(self)
        self.setCentralWidget(self.block)

        self.setWindowTitle('Caller')
        self.show()

    def center(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
                  (screen.height()-size.height())/2)

class Block(QtGui.QWidget):

    def __init__(self, parent):
        super(Block, self).__init__(parent)

        self.initBlock()


    def initBlock(self):

        demultLab = QtGui.QLabel('De-multiplex')
        demultLab.setAlignment(Qt.AlignCenter)
        loadLab = QtGui.QLabel('Load')
        loadLab.setAlignment(Qt.AlignCenter)
        dataLab = QtGui.QLabel('Data')
        dataLab.setAlignment(Qt.AlignCenter)
        logLab = QtGui.QLabel('Log')
        logLab.setAlignment(Qt.AlignCenter)

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        #grid.setColumnStretch(0,1)

        grid.addWidget(demultLab, 0, 0)
        # grid.addWidget(titleEdit, 1, 1)
        demultButton = QtGui.QPushButton('De-multiplex')
        grid.addWidget(demultButton, 1, 0)

        grid.addWidget(loadLab, 0, 1)
        #grid.addWidget(authorEdit, 2, 1)
        loadButton = QtGui.QPushButton('Load')
        grid.addWidget(loadButton, 1, 1)

        grid.addWidget(dataLab, 0, 2)
        dataButton = QtGui.QPushButton('Data')
        grid.addWidget(dataButton, 1, 2)

        grid.addWidget(logLab, 0, 3)
        logButton = QtGui.QPushButton('Log')
        grid.addWidget(logButton, 1, 3)

        # this stredtches over 5 rows
        #grid.addWidget(review, 3, 0)
        #grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Outer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
