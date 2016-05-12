import sys
import gtk
from PyQt4 import QtGui, QtCore
from LOGIC.SupportedProtocols import *
from LOGIC.IPTables.IPTableRule import *
from LOGIC.IPTables.IPTableRuleTCP import *
from LOGIC.IPTables.IPTablesManager import *
from LOGIC.IPTables.IPTableRuleUDP import *
from LOGIC.IPTables.IPTableRuleICMP import *

class InsertRuleWindow(QtGui.QWidget):
    previousProtocolSelected = 'None'
    def __init__(self, appWindow, mWidth, mHeight, list, ipTablesManager):
        super(InsertRuleWindow, self).__init__()
        InsertRuleWindow.previousProtocolSelected = 'None'
        self.insertRuleWidget = QtGui.QWidget()
        self.insertRuleWidget.setGeometry(mWidth / 8, mHeight / 8, mWidth / 4, mHeight / 2)
        self.insertRuleWidget.setWindowTitle('Insert new rule')
        self.StandardLayout = QtGui.QHBoxLayout()

        #Buttons
        self.SaveButton = QtGui.QPushButton('Save')
        self.CancelButton = QtGui.QPushButton('Cancel')

        #Rule name
        self.RuleNameTextBox = QtGui.QLineEdit() # textbox
        self.RuleNameLabel = QtGui.QLabel() # label
        self.RuleNameLabel.setText("Rule Name") # setText

        #Table type
        self.TableTypeCombobox = QtGui.QComboBox(appWindow)
        self.TableTypeLabel = QtGui.QLabel()
        self.TableTypeLabel.setText("Table type")

        #Chain type
        self.ChainTypeCombobox = QtGui.QComboBox(appWindow)
        self.ChainTypeLabel = QtGui.QLabel()
        self.ChainTypeLabel.setText("Chain type")

        #Target chain type
        self.ChainTargetTypeCombobox = QtGui.QComboBox(appWindow)
        self.ChainTargetTypeLabel = QtGui.QLabel()
        self.ChainTargetTypeLabel.setText("Chain target type")

        #source
        self.SourceTextBox = QtGui.QLineEdit()
        self.SourceLabel = QtGui.QLabel()
        self.SourceLabel.setText("Source IP address")

        #destination
        self.DestinationTextBox = QtGui.QLineEdit()
        self.DestinationLabel = QtGui.QLabel()
        self.DestinationLabel.setText("Destination IP address")

        #limit
        self.LimitTextBox = QtGui.QLineEdit()
        self.LimitLabel = QtGui.QLabel()
        self.LimitLabel.setText("Limits")

        #Supported protocols
        self.ProtocolCombobox = QtGui.QComboBox(appWindow)
        self.ProtocolLabel = QtGui.QLabel()
        self.ProtocolLabel.setText("Protocol")

        #Init layout
        self.insertRuleWidget.setLayout(self.StandardLayout)
        self.RuleSpliterStandard = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.StandardLayout.addWidget(self.RuleSpliterStandard)

        #Rule name layout
        self.RuleSpliterStandard.addWidget(self.RuleNameLabel)
        self.RuleSpliterStandard.addWidget(self.RuleNameTextBox)

        #Table type layout
        self.RuleSpliterStandard.addWidget(self.TableTypeLabel)
        for tableType in TableTypeEnum:
            self.TableTypeCombobox.addItem(tableType.value)
        self.TableTypeCombobox.currentIndexChanged[QtCore.QString].connect(
            self.tableTypeComboboxSelectionChanged)  # EVENT
        self.RuleSpliterStandard.addWidget(self.TableTypeCombobox)

        #Chain rule layout
        self.RuleSpliterStandard.addWidget(self.ChainTypeLabel)
        chains = [chain.value for chain in FilterEnum]
        chainsValue = [c.value for c in chains]
        self.ChainTypeCombobox.addItems(chainsValue)
        #for chainRule in ChainEnum:
        #    self.ChainTypeCombobox.addItem(chainRule.value)

        self.RuleSpliterStandard.addWidget(self.ChainTypeCombobox)

        #Chain target rule layout
        self.RuleSpliterStandard.addWidget(self.ChainTargetTypeLabel)
        chainTargets = [chainTarget.value for chainTarget in ChainTargetEnum]
        self.ChainTargetTypeCombobox.addItems(chainTargets)
        #for chainTargetRule in ChainTargetEnum:
        #    self.ChainTargetTypeCombobox.addItem(chainTargetRule.value)
        self.RuleSpliterStandard.addWidget(self.ChainTargetTypeCombobox)

        #Source layout
        self.RuleSpliterStandard.addWidget(self.SourceLabel)
        self.RuleSpliterStandard.addWidget(self.SourceTextBox)

        #Destination layout
        self.RuleSpliterStandard.addWidget(self.DestinationLabel)
        self.RuleSpliterStandard.addWidget(self.DestinationTextBox)

        #Limit layout
        self.RuleSpliterStandard.addWidget(self.LimitLabel)
        self.RuleSpliterStandard.addWidget(self.LimitTextBox)

        #Supported protocols layout
        self.RuleSpliterStandard.addWidget(self.ProtocolLabel)
        protocolsList = [protocol.value for protocol in SupportedProtocols]
        self.ProtocolCombobox.addItems(protocolsList)
        self.ProtocolCombobox.setCurrentIndex(protocolsList.index(SupportedProtocols.NONE.value))
        self.RuleSpliterStandard.addWidget(self.ProtocolCombobox)
        self.ProtocolCombobox.currentIndexChanged[QtCore.QString].connect(self.protocolComboboxSelectionChanged)  # EVENT

        #extension splitter
        self.RuleSpliterExtended = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.RuleSpliterStandard.addWidget(self.RuleSpliterExtended)

        #button splitter
        self.ButtonSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.ButtonSplitter.addWidget(self.SaveButton)
        self.ButtonSplitter.addWidget(self.CancelButton)

        self.RuleSpliterStandard.addWidget(self.ButtonSplitter)

        #Events
        def ClearAndCloseModal():
            self.insertRuleWidget.deleteLater()
            self.deleteLater()

        def passInsertRule(ipTable):
            self.insertItemRule = QtGui.QListWidgetItem(
                self.RuleNameTextBox.text() + " :: " + ipTablesManager.return_table_as_string(ipTable))
            list.addItem(self.insertItemRule)
            ClearAndCloseModal()

        def insertRule():
            prev = InsertRuleWindow.previousProtocolSelected
            if prev == 'TCP':
                ipTable = IPTableRuleTCP(
                    self.TableTypeCombobox.currentText(),
                    self.ChainTypeCombobox.currentText(),
                    self.ChainTargetTypeCombobox.currentText(),
                    self.SourceTextBox.text() if self.SourceTextBox.text() != '' else None,
                    self.DestinationTextBox.text() if self.DestinationTextBox.text() != '' else None,
                    self.LimitTextBox.text() if self.LimitTextBox.text() != '' else None,
                    self.ConsideredFlagsTextBox.text() if self.ConsideredFlagsTextBox.text() != '' else None,
                    self.MatchedFlagsTextBox.text() if self.MatchedFlagsTextBox.text() != '' else None,
                    self.SourcePortTextBox.text() if self.SourcePortTextBox.text() != '' else None,
                    self.DestinationPortTextBox.text() if self.DestinationPortTextBox.text() != '' else None)
                try:
                    ipTablesManager.add_rule_TCP(ipTable)
                    passInsertRule(ipTable)
                except:
                    pass
            elif prev == 'UDP':
                ipTable = IPTableRuleUDP(
                    self.TableTypeCombobox.currentText(),
                    self.ChainTypeCombobox.currentText(),
                    self.ChainTargetTypeCombobox.currentText(),
                    self.SourceTextBox.text() if self.SourceTextBox.text() != '' else None,
                    self.DestinationTextBox.text() if self.DestinationTextBox.text() != '' else None,
                    self.LimitTextBox.text() if self.LimitTextBox.text() != '' else None,
                    self.SourcePortTextBox.text() if self.SourcePortTextBox.text() != '' else None,
                    self.DestinationPortTextBox.text() if self.DestinationPortTextBox.text() != '' else None)
                ipTablesManager.add_rule_UDP(ipTable)
                passInsertRule(ipTable)
            elif prev == 'ICMP':
                ipTable = IPTableRuleICMP(
                    self.TableTypeCombobox.currentText(),
                    self.ChainTypeCombobox.currentText(),
                    self.ChainTargetTypeCombobox.currentText(),
                    self.SourceTextBox.text() if self.SourceTextBox.text() != '' else None,
                    self.DestinationTextBox.text() if self.DestinationTextBox.text() != '' else None,
                    self.LimitTextBox.text() if self.LimitTextBox.text() != '' else None,
                    self.IcmpTypeTextBox.text() if self.IcmpTypeTextBox.text() != '' else None )
                ipTablesManager.add_rule_ICMP(ipTable)
                passInsertRule(ipTable)
            elif prev == 'None':
                ipTable = IPTableRule(
                    self.TableTypeCombobox.currentText(),
                    self.ChainTypeCombobox.currentText(),
                    self.ChainTargetTypeCombobox.currentText(),
                    self.SourceTextBox.text() if self.SourceTextBox.text() != '' else None,
                    self.DestinationTextBox.text() if self.DestinationTextBox.text() != '' else None,
                    self.LimitTextBox.text() if self.LimitTextBox.text() != '' else None)
                ipTablesManager.add_rule(ipTable)
                passInsertRule(ipTable)

        def insertRuleModalHide():
            ClearAndCloseModal()


        self.SaveButton.clicked.connect(insertRule) #Save button event
        self.CancelButton.clicked.connect(insertRuleModalHide) #Cancel button event

    def tableTypeComboboxSelectionChanged(self, item):
        if item == 'nat':
            self.ChainTypeCombobox.clear()
            buf = [items.value for items in NatEnum]
            items = [i.value for i in buf]
            self.ChainTypeCombobox.addItems(items)
        elif item == 'raw':
            self.ChainTypeCombobox.clear()
            buf = [items.value for items in RawEnum]
            items = [i.value for i in buf]
            self.ChainTypeCombobox.addItems(items)
        elif item == 'mangle':
            self.ChainTypeCombobox.clear()
            buf = [items.value for items in MangleEnum]
            items = [i.value for i in buf]
            self.ChainTypeCombobox.addItems(items)
        elif item == 'filter':
            self.ChainTypeCombobox.clear()
            buf = [items.value for items in FilterEnum]
            items = [i.value for i in buf]
            self.ChainTypeCombobox.addItems(items)

    def protocolComboboxSelectionChanged(self, item):
        prev = InsertRuleWindow.previousProtocolSelected
        if prev == 'TCP':
            self.DeleteTCPFields()
        elif prev == 'UDP':
            self.DeleteUDPFields()
        elif prev == 'ICMP':
            self.DeleteICMPFields()
        elif prev == 'None':
            pass

        if item == 'TCP':
            InsertRuleWindow.previousProtocolSelected = 'TCP'
            self.LoadTCPFields()
        elif item == 'UDP':
            InsertRuleWindow.previousProtocolSelected = 'UDP'
            self.LoadUDPFields()
        elif item == 'ICMP':
            InsertRuleWindow.previousProtocolSelected = 'ICMP'
            self.LoadICMPFields()
        elif item == 'None':
            InsertRuleWindow.previousProtocolSelected = 'None'
            pass

    def LoadTCPFields(self):
        # source port
        self.SourcePortTextBox = QtGui.QLineEdit()
        self.SourcePortLabel = QtGui.QLabel()
        self.SourcePortLabel.setText("Source Port")

        # source port layout
        self.RuleSpliterExtended.addWidget(self.SourcePortLabel)
        self.RuleSpliterExtended.addWidget(self.SourcePortTextBox)

        # destination port
        self.DestinationPortTextBox = QtGui.QLineEdit()
        self.DestinationPortLabel = QtGui.QLabel()
        self.DestinationPortLabel.setText("Destination Port")

        # destination port layout
        self.RuleSpliterExtended.addWidget(self.DestinationPortLabel)
        self.RuleSpliterExtended.addWidget(self.DestinationPortTextBox)

        # flags
        #self.FlagsCombobox = QtGui.QComboBox(self)
        self.ConsideredFlagsTextBox = QtGui.QLineEdit()
        self.ConsideredFlagsLabel = QtGui.QLabel()
        self.ConsideredFlagsLabel.setText("Considered flags")

        self.MatchedFlagsTextBox = QtGui.QLineEdit()
        self.MatchedFlagsLabel = QtGui.QLabel()
        self.MatchedFlagsLabel.setText("Matched flags")

        # flags layout
        self.RuleSpliterExtended.addWidget(self.ConsideredFlagsLabel)
        #a = [flag.value for flag in TcpFlags]
        #self.FlagsCombobox.addItems(a)
        #self.FlagsCombobox.setCurrentIndex(a.index(TcpFlags.NONE.value))
        self.RuleSpliterExtended.addWidget(self.ConsideredFlagsTextBox)

        self.RuleSpliterExtended.addWidget(self.MatchedFlagsLabel)
        self.RuleSpliterExtended.addWidget(self.MatchedFlagsTextBox)

    def DeleteTCPFields(self):
        self.SourcePortTextBox.close()
        self.SourcePortLabel.close()
        self.DestinationPortLabel.close()
        self.DestinationPortTextBox.close()
        self.ConsideredFlagsLabel.close()
        self.ConsideredFlagsTextBox.close()
        self.MatchedFlagsTextBox.close()
        self.MatchedFlagsLabel.close()

    def LoadUDPFields(self):
        # source port
        self.SourcePortTextBox = QtGui.QLineEdit()
        self.SourcePortLabel = QtGui.QLabel()
        self.SourcePortLabel.setText("Source Port")

        # source port layout
        self.RuleSpliterExtended.addWidget(self.SourcePortLabel)
        self.RuleSpliterExtended.addWidget(self.SourcePortTextBox)

        # destination port
        self.DestinationPortTextBox = QtGui.QLineEdit()
        self.DestinationPortLabel = QtGui.QLabel()
        self.DestinationPortLabel.setText("Destination Port")

        # destination port layout
        self.RuleSpliterExtended.addWidget(self.DestinationPortLabel)
        self.RuleSpliterExtended.addWidget(self.DestinationPortTextBox)

    def DeleteUDPFields(self):
        self.SourcePortTextBox.close()
        self.SourcePortLabel.close()
        self.DestinationPortLabel.close()
        self.DestinationPortTextBox.close()

    def DeleteICMPFields(self):
        self.IcmpTypeTextBox.close()
        self.IcmpTypeLabel.close()

    def LoadICMPFields(self):
        # ICMP type
        self.IcmpTypeTextBox = QtGui.QLineEdit()
        self.IcmpTypeLabel = QtGui.QLabel()
        self.IcmpTypeLabel.setText("Icmp type")

        #layout
        self.RuleSpliterExtended.addWidget(self.IcmpTypeLabel)
        self.RuleSpliterExtended.addWidget(self.IcmpTypeTextBox)


    def show(self):
        self.insertRuleWidget.show()