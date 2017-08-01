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
        # file paths
        self.sdir = None
        self.fPairPath = None

        self.initBlock()

    def initBlock(self):
        # labels
        loadLab = QtGui.QLabel('<b>1. </b>Please provide a folder of samples')
        loadLab.setAlignment(Qt.AlignCenter)
        alnLab = QtGui.QLabel('<b>2. </b>Run alignment')
        alnLab.setAlignment(Qt.AlignCenter)
        pairLab = QtGui.QLabel(
            '<b>3. </b>Please provide a file of sample pairs')
        pairLab.setAlignment(Qt.AlignCenter)
        seqLab = QtGui.QLabel('<b>4. </b>Create sequences')
        seqLab.setAlignment(Qt.AlignCenter)
        dataLab = QtGui.QLabel('<b>5. </b>Data')
        dataLab.setAlignment(Qt.AlignCenter)
        logLab = QtGui.QLabel('<b>6. </b>Log')
        logLab.setAlignment(Qt.AlignCenter)

        # layout
        grid = QtGui.QGridLayout()
        # some options for spacing of elements
        # grid.setSpacing(10)
        # grid.setColumnStretch(0,1)

        # add objects
        grid.addWidget(loadLab, 0, 0)
        loadButton = QtGui.QPushButton('Samples directory')
        grid.addWidget(loadButton, 1, 0)
        loadButton.clicked.connect(self.loadButtonClk)

        self.sampleFileLab = QtGui.QLabel('')
        grid.addWidget(self.sampleFileLab, 2, 0)

        grid.addWidget(alnLab, 3, 0)
        loadGoButton = QtGui.QPushButton('Run alignment!')
        grid.addWidget(loadGoButton, 4, 0)
        loadGoButton.clicked.connect(self.loadGoButtonClk)
        self.alignLab = QtGui.QLabel('')
        grid.addWidget(self.alignLab, 5, 0)

        grid.addWidget(pairLab, 0, 1)
        pairButton = QtGui.QPushButton('Pairs file')
        grid.addWidget(pairButton, 1, 1)
        pairButton.clicked.connect(self.pairButtonClk)
        self.pairFileLab = QtGui.QLabel('')
        self.pairProgLab = QtGui.QLabel('')
        grid.addWidget(self.pairFileLab, 2, 1)
        grid.addWidget(self.pairProgLab, 3, 1)

        grid.addWidget(seqLab, 0, 2)
        seqButton = QtGui.QPushButton('Make sequences')
        grid.addWidget(seqButton, 1, 2)
        seqButton.clicked.connect(self.seqButtonClk)
        self.seqProgLab = QtGui.QLabel('')
        grid.addWidget(self.seqProgLab, 2, 2)

        grid.addWidget(dataLab, 0, 3)
        dataButton = QtGui.QPushButton('View data')
        grid.addWidget(dataButton, 1, 3)
        dataButton.clicked.connect(self.dataButtonClk)

        grid.addWidget(logLab, 2, 3)
        logButton = QtGui.QPushButton('Log')
        grid.addWidget(logButton, 3, 3)
        logButton.clicked.connect(self.logButtonClk)

        # this stretches over 5 rows
        # grid.addWidget(review, 3, 0)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

    def loadButtonClk(self):
        # I need to pop up a dialog saying 'running'
        self.sdir = QtGui.QFileDialog.getExistingDirectory(
            self, "Samples directory")
        self.sampleFileLab.setText(
            'Samples dir: ' + os.path.basename(str(self.sdir)))

    def loadGoButtonClk(self):
        # this part runs step 1
        if self.sdir:
            self.alignLab.setText('Running...')
            args_step1 = ' '.join([os.path.join(sys.path[0],
                                                'run_aligner.py'),
                                   str(self.sdir)])
            print('running step1')
            p = Popen(args_step1, shell=True)
            # this waits until process is finished
            p.wait()
            self.alignLab.setText('Done with alignment!')
        else:
            print("need to handle an error here")
            sys.exit(1)

    def pairButtonClk(self):
        # need to handle this error with a message saying please select
        # a valid file to continue.
        # IOError: [Errno 2] No such file or directory:
        self.fPairPath = QtGui.QFileDialog.getOpenFileName(self, "Pairs file")
        self.pairFileLab.setText(
            'Pairs file: ' + os.path.basename(str(self.fPairPath)))
        with open(str(self.fPairPath)) as f:
            targets = []
            for line in f:
                bits = line.strip().split('\t')
                targets.append((bits[0], bits[1]))
        print('running step2')
        for pair in targets:
            args_step2 = ' '.join([os.path.join(sys.path[0],
                                                'genotyper_iter.py'),
                                   pair[0], pair[1]])

            p = Popen(args_step2, shell=True)
            p.wait()
        self.pairProgLab.setText('Done processing pairs!')

    def seqButtonClk(self):
        args_step3 = ' '.join([os.path.join(sys.path[0],
                                            'create_sequences.py')])
        p = Popen(args_step3, shell=True)
        p.wait()
        self.seqProgLab.setText('Sequences saved in final_sequences directory')

    def dataButtonClk(self):
        # subprocess.Popen("./test.py", arg)
        print('starting script')
        p = Popen(os.path.join(sys.path[0], 'test.py'))
        p.wait()
        print('finished function this should be last')

    def logButtonClk(self):
        # subprocess.Popen("./test.py", arg)
        Popen(os.path.join(sys.path[0], 'test.py'))


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Outer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
