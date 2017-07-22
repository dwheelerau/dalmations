#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        exitAction = QtGui.QAction(QtGui.QIcon('web.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit app')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu = menubar.addMenu('&Help')

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        # pass string and widget, in this case self ie QtGui.QPushButton
        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 20)

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.setToolTip('Click to quit')
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 20)


        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        self.center()

        self.show()

    def center(self):
        '''set the window in the center of the desktop'''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # the above is getting the coord of the center, now we move
        self.move(qr.topLeft())



def main():

    app = QtGui.QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
