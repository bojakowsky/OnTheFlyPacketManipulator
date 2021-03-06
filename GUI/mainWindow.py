import sys
import gtk
from wx.lib.agw.aui.aui_constants import vertical_border_padding

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from GUI.insertRuleWindow import *
from GUI.packetEditWindow import *
from LOGIC.PacketManager import send_fuzzed_packet_back, send_auto_packet_back, get_packet_from_raw

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
        self.table = MyTable(255, 12)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.initUI()
        self.packetQueue = packetQueue
        self.packetQueueRaw = packetQueueRaw;
        self.timer = QTimer()
        self.timer.timeout.connect(self.packetQueueRefresher)
        self.timer.start(500)
        self.packetEditWindow = None
        self.insertRuleWindow = None
        self.table.cellDoubleClicked.connect(self.rowClicked)

    def __del__(self):
        if self.packetEditWindow is not None:
            del self.packetEditWindow
        if self.insertRuleWindow is not None:
            del self.insertRuleWindow

    @pyqtSlot(int, int)
    def rowClicked(self, i, j):
        print(i, j)
        if (i >= 0) and (i < len(self.packetQueue)):
            self.packetEditWindow = PacketEditWindow(self, mWidth + mWidth, mHeight, self.packetQueue, self.packetQueueRaw, i)
            self.packetEditWindow.addPacketToTable()
            self.packetEditWindow.show()

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
            self.insertRuleWindow = InsertRuleWindow(self, mWidth, mHeight, list, ipTablesManager)
            self.insertRuleWindow.show()



        insertButton.clicked.connect(insertRuleModalShow)

        rulesLabel = QtGui.QLabel()
        rulesLabel.setText("Rules")
        buttonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        verticalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        verticalSplitter.addWidget(rulesLabel)
        verticalSplitter.addWidget(list)
        insertButton.setFixedWidth(buttonSplitter.width())
        removeButton.setFixedWidth(buttonSplitter.width())
        buttonSplitter.addWidget(insertButton)
        buttonSplitter.addWidget(removeButton)
        verticalSplitter.addWidget(buttonSplitter)


        #Buttons
        removeTableRowButton = QtGui.QPushButton("Delete table row")
        nextButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        removeAllRowsButton = QtGui.QPushButton("Delete all table rows")
        removeAllRowsButton.setFixedWidth(nextButtonSplitter.width())
        nextButtonSplitter.addWidget(removeAllRowsButton)
        removeTableRowButton.setFixedWidth(nextButtonSplitter.width())
        nextButtonSplitter.addWidget(removeTableRowButton)

        def deleteTableRow():
            index = self.table.currentRow()
            v = self.table.item(index, 0)
            if v is not None:
                self.packetQueue.remove(self.packetQueue[index])
                self.packetQueueRaw.remove(self.packetQueueRaw[index])
                self.table.removeRow(index)

        def deleteAllTableRows():
            self.packetQueue[:] = []
            self.packetQueueRaw[:] = []
            self.table.clearContents()

        removeTableRowButton.clicked.connect(deleteTableRow)
        removeAllRowsButton.clicked.connect(deleteAllTableRows)

        #Next line of buttons
        tryAutoReplyButton = QtGui.QPushButton("Try auto reply")
        lastButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        fuzzReplyButton = QtGui.QPushButton("Fuzz reply")
        tryAutoReplyButton.setFixedWidth(nextButtonSplitter.width())
        lastButtonSplitter.addWidget(tryAutoReplyButton)
        fuzzReplyButton.setFixedWidth(nextButtonSplitter.width())
        lastButtonSplitter.addWidget(fuzzReplyButton)

        def sendFuzzReply():
            index = self.table.currentRow()
            if (index >= 0) and (index < len(self.packetQueue)):
                pkt = get_packet_from_raw(self.packetQueueRaw[index])
                send_fuzzed_packet_back(pkt)
                self.packetQueue.remove(self.packetQueue[index])
                self.packetQueueRaw.remove(self.packetQueueRaw[index])
                self.table.removeRow(index)

        def sendAutoReply():
            index = self.table.currentRow()
            if (index >= 0) and (index < len(self.packetQueue)):
                pkt = get_packet_from_raw(self.packetQueueRaw[index])
                send_auto_packet_back(pkt)
                self.packetQueue.remove(self.packetQueue[index])
                self.packetQueueRaw.remove(self.packetQueueRaw[index])
                self.table.removeRow(index)

        fuzzReplyButton.clicked.connect(sendFuzzReply)
        tryAutoReplyButton.clicked.connect(sendAutoReply)

        horizontalLine = self.horizontalLine()
        verticalSplitter.addWidget(horizontalLine)
        verticalSplitter.addWidget(nextButtonSplitter)
        verticalSplitter.addWidget(lastButtonSplitter)
        verticalSplitter.addWidget(self.table)

        hbox.addWidget(verticalSplitter)

        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, mWidth/2, mHeight)
        self.setWindowTitle('OnTheFlyPacketManipulator')
        self.show()

    def horizontalLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedHeight(20)
        return line
