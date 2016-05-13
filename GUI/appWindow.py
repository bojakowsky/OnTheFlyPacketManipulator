import sys
import gtk
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, pyqtSignal, QObject, QRunnable
import threading
from insertRuleWindow import *
from LOGIC.IPTables.IPTableRule import *
from subprocess import call
from LOGIC.PacketManager import *

lista = ['aa', 'ab', 'ac', 'ba', 'eds', 'ol']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A': lista, 'B': listb, 'C': listc}

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
    def __init__(self, thestruct, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.setGeometry(600, 600, 600, 600)
        self.data = thestruct
        self.setmydata()

    def setmydata(self):
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(n, m, newitem)
                m += 1
            n += 1

class myListWidget(QtGui.QListWidget, QtGui.QListWidgetItem):
    pass



class mainView(QtGui.QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.initUI()


    def initUI(self):
        list = myListWidget()
        hbox = QtGui.QHBoxLayout(self)

        insertButton = QtGui.QPushButton('New rule')
        removeButton = QtGui.QPushButton('Remove selected')
        table = MyTable(mystruct, 50, 20)

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
        vericalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        vericalSplitter.addWidget(rulesLabel)
        vericalSplitter.addWidget(list)
        buttonSplitter.addWidget(insertButton)
        buttonSplitter.addWidget(removeButton)
        vericalSplitter.addWidget(buttonSplitter)
        vericalSplitter.addWidget(table)

        hbox.addWidget(vericalSplitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, mWidth/2, mHeight)
        self.setWindowTitle('OnTheFlyPacketManipulator')
        self.show()

def main():
    try:
        call("iptables-save > iptables-backup", shell=True)
        call("iptables -t filter --flush", shell=True)
        call("iptables -t nat --flush", shell=True)
        call("iptables -t raw --flush", shell=True)
        call("iptables -t mangle --flush", shell=True)

        app = QtGui.QApplication(sys.argv)
        view = mainView()
        sys.exit(app.exec_())

        t1 = threading.Thread(target=PacketManagerThread)
        t1.start()
    finally:
        print("closing..")
        call("iptables-restore < iptables-backup", shell=True)

def PacketManagerThread():
    pktMgr = PacketManager()

if __name__ == '__main__':
    main()

