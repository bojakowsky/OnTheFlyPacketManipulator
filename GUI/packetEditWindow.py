from PyQt4 import QtGui, QtCore
from LOGIC.PacketManager import get_packet_from_raw, get_hexdump_from_packet, build_packet_layer, send_packet_based_on_layers

class PacketTable(QtGui.QTableWidget):
    def __init__(self, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.setGeometry(600, 600, 600, 600)
        self.data = {}


class PacketEditWindow(QtGui.QWidget):

    def __init__(self, appWindow, mWidth, mHeight, queue, queueRaw, index):
        super(PacketEditWindow, self).__init__()
        self.appWindow = appWindow
        self.setWindowTitle("Packet edit")
        self.setGeometry(0, mHeight / 4, mWidth/4, mHeight / 2)
        self.standardLayout = QtGui.QHBoxLayout()

        self.table = PacketTable(1, 1)
        self.verticalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        self.verticalSplitter.addWidget(self.getTopSection())
        self.verticalSplitter.addWidget(self.table)

        self.standardLayout.addWidget(self.verticalSplitter)
        self.setLayout(self.standardLayout)

        self.queue = queue
        self.queueRaw = queueRaw
        self.index = index

        self.SendButton = QtGui.QPushButton('Send')
        self.CancelButton = QtGui.QPushButton('Cancel')

        self.ButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.ButtonSplitter.addWidget(self.SendButton)
        self.ButtonSplitter.addWidget(self.CancelButton)
        self.verticalSplitter.addWidget(self.ButtonSplitter)

        def hide_modal():
            self.table.clear()
            self.deleteLater()



        def send_data():
            layers = []
            for i in range(0, self.table.rowCount()):
                layers.append(self.table.item(i, 0).text())
            send_packet_based_on_layers(layers, self.queueRaw[self.index],
                self.srcAndDstCheckbox.isChecked(), self.sportAndDportCheckbox.isChecked(), self.chksumAndLenCheckbox.isChecked())
            #Removing existing
            self.queueRaw.remove(self.queueRaw[self.index])
            self.queue.remove(self.queue[self.index])
            self.appWindow.table.removeRow(self.index)
            hide_modal()

        #Slots
        self.SendButton.clicked.connect(send_data)  # Save button event
        self.CancelButton.clicked.connect(hide_modal)  # Cancel button event

    def getTopSection(self):
        self.hexdump = QtGui.QLabel(self)
        self.srcAndDstCheckbox = QtGui.QCheckBox()
        self.srcAndDstCheckbox.setText("Handle src and dst")
        self.sportAndDportCheckbox = QtGui.QCheckBox()
        self.sportAndDportCheckbox.setText("Handle sport and dport")
        self.chksumAndLenCheckbox = QtGui.QCheckBox()
        self.chksumAndLenCheckbox.setText("Handle chksum and len")

        checkboxSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        checkboxSplitter.addWidget(self.srcAndDstCheckbox)
        checkboxSplitter.addWidget(self.sportAndDportCheckbox)
        checkboxSplitter.addWidget(self.chksumAndLenCheckbox)
        commonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.hexdump.setFixedWidth(commonSplitter.width())
        checkboxSplitter.setFixedWidth(commonSplitter.width())
        commonSplitter.addWidget(self.hexdump)
        commonSplitter.addWidget(checkboxSplitter)
        return commonSplitter

    def addPacketToTable(self):
        if len(self.queueRaw) == 0:
            self.hexdump.setText("Not initialized")
            return

        pkt = get_packet_from_raw(self.queueRaw[self.index])
        self.hexdump.setText(get_hexdump_from_packet(pkt))

        layers = build_packet_layer(pkt)
        dictToDisplay = {}
        for layer in layers:
            dictToDisplay[layer.name] = layer.fields

        self.table.clear()
        i = 0
        for key, value in dictToDisplay.iteritems():
            newItem = QtGui.QTableWidgetItem(str(value))
            self.table.removeRow(i)
            self.table.insertRow(i)
            self.table.setItem(i, 0, newItem)
            i = i + 1
        while self.table.rowCount() > i+1:
            i = i + 1
            self.table.removeRow(i)

        if len(self.queueRaw) > 0:
            self.table.resizeColumnsToContents()
