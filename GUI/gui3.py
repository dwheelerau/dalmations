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

        names = ['Cls', 'Bck', '', 'Close', 'ttt',
                 '7', '8', '9', '/','ttt',
                 '4', '5', '6', '*','ttt',
                 '1','2','3','-','ttt',
                 '0','.','=','+','ttt']


        positions = [(i, j) for i in range(5) for j in range(5)]
        print positions

        for position, name in zip(positions, names):

            print position
            if name == '':
                continue
            button = QtGui.QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
