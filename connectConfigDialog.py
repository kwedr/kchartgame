import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from tickFactor import TickFactor
from settingFactor import SettingFactor
from signalFactor import SignalFactor
from ddeConfigDialog import DDEConfigDlg
from plugin.yahooConfigDialog import YahooConfigDlg

class ConnectConfigDlg (QtWidgets.QDialog):
    PAGE_DDE = 0
    PAGE_Yahoo = 1

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

        btn_Yahoo = QtWidgets.QPushButton("Yahoo")
        btn_Yahoo.clicked.connect(self.clickYahoo)
        item_Yahoo = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item_Yahoo)
        self.listWidget.setItemWidget(item_Yahoo, btn_Yahoo)

    def updateContent (self):
        dlg = DDEConfigDlg (self)
        dlg.updateBySettings ()
        dlg.ok.clicked.connect (self.clickedOK)
        self.contentWidget.addWidget(dlg)

        dlg = YahooConfigDlg (self)
        dlg.ok.clicked.connect (self.clickedOK)
        self.contentWidget.addWidget(dlg)

    def clickDDE (self):
        self.contentWidget.setCurrentIndex (self.PAGE_DDE)
        widget = self.contentWidget.currentWidget()
        widget.updateBySettings ()

    def clickYahoo (self):
        self.contentWidget.setCurrentIndex (self.PAGE_Yahoo)
        widget = self.contentWidget.currentWidget()
        widget.updateBySettings ()

    def clickedOK (self):
        SignalFactor ().sign_connect_config_done.emit ()
        self.close ()

