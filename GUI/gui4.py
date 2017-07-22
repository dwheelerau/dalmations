#!/usr/bin/env python

import sys
from PyQt4 import QtGui

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)


        #positions = [(i, j) for i in range(5) for j in range(5)]
        #print positions

        #for position, name in zip(positions, names):

        #    if name == '':
        #        continue
        button = QtGui.QPushButton('test')
        grid.addWidget(button, *(0,0))

        button = QtGui.QPushButton('test2')
        grid.addWidget(button, *(0,1))

        button = QtGui.QPushButton('test4')
        grid.addWidget(button, *(0,3))

        button = QtGui.QPushButton('test3')
        grid.addWidget(button, *(1,2))


        self.setWindowTitle('Calculator')
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
