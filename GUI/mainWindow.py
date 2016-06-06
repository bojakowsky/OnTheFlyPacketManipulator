import sys
import gtk

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from GUI.insertRuleWindow import *
from GUI.packetEditWindow import *

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


class MyListWidget(QtGui.QListWidget, QtGui.QListWidgetItem):
    pass


class MainView(QtGui.QWidget):

    def __init__(self, packetQueue, packetQueueRaw):
        super(MainView, self).__init__()
        self.table = MyTable(50, 12)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.initUI()
        self.packetQueue = packetQueue
        self.packetQueueRaw = packetQueueRaw;
        self.timer = QTimer()
        self.timer.timeout.connect(self.packetQueueRefresher)
        self.timer.start(500)
        self.packetEditWindow = PacketEditWindow(self, mWidth + mWidth, mHeight, self.packetQueue, self.packetQueueRaw, 0)
        self.table.cellDoubleClicked.connect(self.rowClicked)

    @pyqtSlot(int, int)
    def rowClicked(self, item1, y):
        print(x, y)
        if (x <= 0) and (x < len(self.packetQueue)):
            self.packetEditWindow.index = x
            self.packetEditWindow.show()
            self.packetEditWindow.addPacketToTable()


    def packetQueueRefresher(self):
        j = 0
        for queList in self.packetQueue:
            i = 0
            for key, value in queList.iteritems():
                newItem = QtGui.QTableWidgetItem(key + ": " + str(value))
                self.table.setItem(j, i, newItem)
                i = i + 1
            j = j + 1

        if len(self.packetQueue) > 0:
            self.table.resizeColumnsToContents()

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


        insertButton.clicked.connect(insertRuleModalShow)

        rulesLabel = QtGui.QLabel()
        rulesLabel.setText("Rules")
        buttonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        verticalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        verticalSplitter.addWidget(rulesLabel)
        verticalSplitter.addWidget(list)
        buttonSplitter.addWidget(insertButton)
        buttonSplitter.addWidget(removeButton)
        verticalSplitter.addWidget(buttonSplitter)

        removeTableRow = QtGui.QPushButton("Delete table row")
        nextButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        removeAllRows = QtGui.QPushButton("Delete all table rows")
        nextButtonSplitter.addWidget(removeAllRows)
        nextButtonSplitter.addWidget(removeTableRow)
        #removeTableRow.connect(deleteTableRow)
        #removeAllRows.conn

        verticalSplitter.addWidget(nextButtonSplitter)
        verticalSplitter.addWidget(self.table)

        hbox.addWidget(verticalSplitter)

        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, mWidth/2, mHeight)
        self.setWindowTitle('OnTheFlyPacketManipulator')
        self.show()

