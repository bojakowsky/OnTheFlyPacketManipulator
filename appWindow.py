import sys
from PyQt4 import QtGui, QtCore

lista = ['aa', 'ab', 'ac']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A': lista, 'B': listb, 'C': listc}

class MyTable(QtGui.QTableWidget):
    def __init__(self, thestruct, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.setGeometry(600,600,600,600)
        self.data = thestruct
        self.setmydata()

    def setmydata(self):
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(m, n, newitem)
                m += 1
            n += 1

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        hbox = QtGui.QHBoxLayout(self)
        list = QtGui.QListWidget()

        table = MyTable(mystruct, 5, 3)

        for i in range(10):
            item = QtGui.QListWidgetItem("Item %i" % i)
            list.addItem(item)


        splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(list)
        splitter1.addWidget(table)


        hbox.addWidget(splitter1)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(300, 300, 600, 800)
        self.setWindowTitle('')
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()