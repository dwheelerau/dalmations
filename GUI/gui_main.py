#!/usr/bin/env python2

import sys
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from subprocess import Popen


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
        loadLab = QtGui.QLabel('Load')
        loadLab.setAlignment(Qt.AlignCenter)
        dataLab = QtGui.QLabel('Data')
        dataLab.setAlignment(Qt.AlignCenter)
        logLab = QtGui.QLabel('Log')
        logLab.setAlignment(Qt.AlignCenter)

        grid = QtGui.QGridLayout()
        # some options for spacing of elements
        # grid.setSpacing(10)
        # grid.setColumnStretch(0,1)

        grid.addWidget(loadLab, 0, 0)
        loadButton = QtGui.QPushButton('Load')
        grid.addWidget(loadButton, 1, 0)
        loadButton.clicked.connect(self.loadButtonClk)

        grid.addWidget(dataLab, 0, 1)
        dataButton = QtGui.QPushButton('Data')
        grid.addWidget(dataButton, 1, 1)
        dataButton.clicked.connect(self.dataButtonClk)

        grid.addWidget(logLab, 0, 2)
        logButton = QtGui.QPushButton('Log')
        grid.addWidget(logButton, 1, 2)
        logButton.clicked.connect(self.logButtonClk)

        # this stretches over 5 rows
        # grid.addWidget(review, 3, 0)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

    def loadButtonClk(self):
        # I need to pop up a dialog saying 'running'
        sdir = QtGui.QFileDialog.getExistingDirectory(
            self, "Samples directory")
        # get pairs file for processing step 2
        fPairPath = QtGui.QFileDialog.getOpenFileName(self, "Pairs file")
        with open(fPairPath) as f:
            targets = []
            for line in f:
                bits = line.strip().split('\t')
                targets.append((bits[0], bits[1]))
        # this part runs step 1
        args_step1 = ['../run_aligner.py', sdir]
        print 'running step1'
        p = Popen(args_step1)
        p.wait()
        print 'running step2'
        # this step runs before run_aligner has a chance to finish
        for pair in targets:
            args_step2 = ['../genotyper_iter.py', pair[0], pair[1]]
            p = Popen(args_step2)
            p.wait()
        print 'done step2'

    def dataButtonClk(self):
        # subprocess.Popen("./test.py", arg)
        print 'starting script'
        p = Popen('./test.py')
        p.wait()
        print 'finished function this should be last'

    def logButtonClk(self):
        # subprocess.Popen("./test.py", arg)
        Popen("./test.py")


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Outer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
