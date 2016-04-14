import sys
import gtk
from PyQt4 import QtGui, QtCore

class InsertRuleWindow(QtGui.QWidget):
    def __init__(self, appWindow, mWidth, mHeight, list):
        self.insertRuleWidget = QtGui.QWidget()
        self.insertRuleWidget.setGeometry(mWidth / 8, mWidth / 8, mWidth / 4, mHeight / 4)
        self.insertRuleWidget.setWindowTitle('Insert new rule')
        self.insertRuleLayout = QtGui.QHBoxLayout()

        self.insertRuleTextbox = QtGui.QLineEdit()
        self.insertAttrsTextbox = QtGui.QLineEdit()
        self.insertVarsTextbox = QtGui.QLineEdit()

        self.insertRuleButton = QtGui.QPushButton('Save')
        self.insertRuleCancelButton = QtGui.QPushButton('Cancel')

        self.insertRuleNameLabel = QtGui.QLabel()
        self.insertRuleNameLabel.setText("Rule Name")
        self.insertRuleTypeLabel = QtGui.QLabel()
        self.insertRuleTypeLabel.setText("Packet type")
        self.insertRuleVarsLabel = QtGui.QLabel()
        self.insertRuleVarsLabel.setText("Variables")
        self.insertRuleAttrsLabel = QtGui.QLabel()
        self.insertRuleAttrsLabel.setText("Attributes")

        self.insertRuleWidget.setLayout(self.insertRuleLayout)

        self.insertRuleSplitterV = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.insertRuleLayout.addWidget(self.insertRuleSplitterV)

        self.insertRuleSplitterV.addWidget(self.insertRuleNameLabel)
        self.insertRuleSplitterV.addWidget(self.insertRuleTextbox)
        self.insertRuleSplitterV.addWidget(self.insertRuleTypeLabel)

        self.comboBox = QtGui.QComboBox(appWindow)
        self.comboBox.addItem("ICMP")
        self.comboBox.addItem("TCP")
        self.comboBox.addItem("UDP")

        self.insertRuleSplitterV.addWidget(self.comboBox)
        self.insertRuleSplitterV.addWidget(self.insertRuleAttrsLabel)
        self.insertRuleSplitterV.addWidget(self.insertAttrsTextbox)
        self.insertRuleSplitterV.addWidget(self.insertRuleVarsLabel)
        self.insertRuleSplitterV.addWidget(self.insertVarsTextbox)

        self.insertRuleButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.insertRuleButtonSplitter.addWidget(self.insertRuleButton)
        self.insertRuleButtonSplitter.addWidget(self.insertRuleCancelButton)
        self.insertRuleSplitterV.addWidget(self.insertRuleButtonSplitter)


        #Events
        def insertRuleModalClearAndHide():
            self.insertRuleTextbox.clear()
            self.insertRuleWidget.hide()

        def insertRule():
            self.insertItemRule = QtGui.QListWidgetItem(self.insertRuleTextbox.text())
            list.addItem(self.insertItemRule)
            insertRuleModalClearAndHide()

        self.insertRuleButton.clicked.connect(insertRule)


        def insertRuleModalHide():
            insertRuleModalClearAndHide()

        self.insertRuleCancelButton.clicked.connect(insertRuleModalHide)

    def show(self):
        self.insertRuleWidget.show()