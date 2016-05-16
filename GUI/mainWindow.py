import sys
import gtk

from PyQt4 import QtGui, QtCore
#from PyQt4.QtCore import QThreadPool, pyqtSignal, QObject, QRunnable
from GUI.insertRuleWindow import *
from LOGIC.PacketManager import *
from LOGIC.IPTables import *


# lista = ['aa', 'ab', 'ac', 'ba', 'eds', 'ol']
# listb = ['ba', 'bb', 'bc']
# listc = ['ca', 'cb', 'cc']
# 'A': lista, 'B': listb, 'C': listc

window = gtk.Window()
screen = window.get_screen()
monitors = []
nmons = screen.get_n_monitors()
for m in range(nmons):
    mg = screen.get_monitor_geometry(m)
    monitors.append(mg)

# current monitor
curmon = screen.get_monitor_at_window(screen.get_active_window())
x, y, mWidth, mHeight = monitors[curmon]

ipTablesManager = IPTablesManager()


class MyTable(QtGui.QTableWidget):
    def __init__(self, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.setGeometry(600, 600, 600, 600)
        self.data = {}
        self.setItem(9999, 9999, QtGui.QTableWidgetItem(":)"))
        #self.set_table_data()
        

    def set_table_data(self):
        n = 0
        if self.data:
            for key in self.data:
                m = 0
                for item in self.data[key]:
                    newitem = QtGui.QTableWidgetItem(item)
                    self.setItem(n, m, newitem)
                    m += 1
                n += 1


class MyListWidget(QtGui.QListWidget, QtGui.QListWidgetItem):
    pass


class MainView(QtGui.QWidget):

    def __init__(self, packetQueue):
        super(MainView, self).__init__()
        self.table = MyTable(50, 20)
        self.initUI()
        self.packetQueue = packetQueue


    def initUI(self):
        list = MyListWidget()
        hbox = QtGui.QHBoxLayout(self)

        insertButton = QtGui.QPushButton('New rule')
        removeButton = QtGui.QPushButton('Remove selected')


        def removeRule():
            for SelectedItem in list.selectedItems():
                print("Removing id: " + str(list.row(SelectedItem)))
                ipTablesManager.remove_rule(list.row(SelectedItem))
                list.takeItem(list.row(SelectedItem))

        removeButton.clicked.connect(removeRule)

        def insertRuleModalShow():
            insertRuleWindow = InsertRuleWindow(self, mWidth, mHeight, list, ipTablesManager)
            insertRuleWindow.show()
            print(self.packetQueue)
            j = 0
            for queList in self.packetQueue:
                i = 0
                for key, value in queList.iteritems():
                    newItem = QtGui.QTableWidgetItem(key + ": " + str(value))
                    self.table.setItem(j, i, newItem)
                    i = i + 1
                j = j + 1

        insertButton.clicked.connect(insertRuleModalShow)

        rulesLabel = QtGui.QLabel()
        rulesLabel.setText("Rules")
        buttonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        vericalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        vericalSplitter.addWidget(rulesLabel)
        vericalSplitter.addWidget(list)
        buttonSplitter.addWidget(insertButton)
        buttonSplitter.addWidget(removeButton)
        vericalSplitter.addWidget(buttonSplitter)
        vericalSplitter.addWidget(self.table)

        hbox.addWidget(vericalSplitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, mWidth/2, mHeight)
        self.setWindowTitle('OnTheFlyPacketManipulator')
        self.show()

