import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from tickFactor import TickFactor
from settingFactor import SettingFactor
from signalFactor import SignalFactor
from ddeConfigDialog import DDEConfigDlg

class ConnectConfigDlg (QtWidgets.QDialog):
    def __init__ (self, parent):
        super().__init__ (parent)
        self.setWindowTitle ("Connect Config")
        self.resize(600,600)

        self.listWidget = QtWidgets.QListWidget ()
        self.listWidget.setMaximumWidth(100)

        self.updateListWidget ()

        self.contentWidget = QtWidgets.QStackedLayout ()
        self.updateContent ()

        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.addWidget(self.listWidget)
        self.hlay.addLayout(self.contentWidget)

    def change_run_enable (self):
        pass

    def run (self):
        #self.setUpdatesEnabled (False)
        #self.updateBySettings ()
        #self.setUpdatesEnabled (True)
        self.show ()

    def updateListWidget (self):
        btn_dde = QtWidgets.QPushButton("DDE")
        btn_dde.clicked.connect(self.clickDDE)
        item_dde = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item_dde)
        self.listWidget.setItemWidget(item_dde, btn_dde)

        btn_Yuanta = QtWidgets.QPushButton("Yuanta")
        btn_Yuanta.clicked.connect(self.clickYuanta)
        item_Yuanta = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item_Yuanta)
        self.listWidget.setItemWidget(item_Yuanta, btn_Yuanta)

    def updateContent (self):
        dlg = DDEConfigDlg (self)
        dlg.ok.clicked.connect (self.clickedOK)
        self.contentWidget.addWidget(dlg)
        

    def clickDDE (self):
        pass

    def clickYuanta (self):
        pass

    def clickedOK (self):
        self.close ()

