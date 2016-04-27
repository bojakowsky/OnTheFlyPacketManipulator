import sys
import gtk
from PyQt4 import QtGui, QtCore

lista = ['aa', 'ab', 'ac']
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

class myListWidget(QtGui.QListWidget, QtGui.QListWidgetItem):

    def Clicked(self, item):
        self.removeItemWidget(item)
        QtGui.QMessageBox.warning(self, "ListWidget", "You clicked: "+item.text())

class myRemoveButton(QtGui.QPushButton, QtGui.QListWidget):

    def Clicked(self, listToEdit):
        print listToEdit

class mainView(QtGui.QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.initUI()



    def initUI(self):
        insertRuleWidget = QtGui.QWidget()
        insertRuleLayout = QtGui.QHBoxLayout()
        insertRuleTextbox = QtGui.QLineEdit()
        insertRuleButton = QtGui.QPushButton('Save')
        insertRuleCancelButton = QtGui.QPushButton('Cancel')
        insertRuleLabel = QtGui.QLabel()
        insertRuleLabel.setText("Insert new rule")
        insertRuleWidget.setLayout(insertRuleLayout)
        insertRuleLayout.addWidget(insertRuleLabel)
        insertRuleLayout.addWidget(insertRuleTextbox)
        insertRuleButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        insertRuleButtonSplitter.addWidget(insertRuleButton)
        insertRuleButtonSplitter.addWidget(insertRuleCancelButton)
        insertRuleLayout.addWidget(insertRuleButtonSplitter)

        def insertRuleModalClearAndHide():
            insertRuleTextbox.clear()
            insertRuleWidget.hide()


        def insertRule():
            insertItemRule = QtGui.QListWidgetItem(insertRuleTextbox.text())
            list.addItem(insertItemRule)
            insertRuleModalClearAndHide()

        insertRuleButton.clicked.connect(insertRule)

        def insertRuleModalHide():
            insertRuleModalClearAndHide()

        insertRuleCancelButton.clicked.connect(insertRuleModalHide)

        hbox = QtGui.QHBoxLayout(self)
        list = myListWidget()
        insertButton = QtGui.QPushButton('New rule')
        removeButton = QtGui.QPushButton('Remove selected')
        table = MyTable(mystruct, 5, 3)

        def removeRule():
            for SelectedItem in list.selectedItems():
                list.takeItem(list.row(SelectedItem))

        removeButton.clicked.connect(removeRule)

        def insertRuleModalShow():
            insertRuleWidget.show()

        insertButton.clicked.connect(insertRuleModalShow)


        for i in range(10):
            item = QtGui.QListWidgetItem("Rule %i" % i)
            list.addItem(item)
        label1 = QtGui.QLabel()
        label1.setText("Rules")
        buttonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(label1)
        splitter1.addWidget(list)
        buttonSplitter.addWidget(insertButton)
        buttonSplitter.addWidget(removeButton)
        splitter1.addWidget(buttonSplitter)
        splitter1.addWidget(table)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, mWidth/2, mHeight)
        self.setWindowTitle('')
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = mainView()

    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()