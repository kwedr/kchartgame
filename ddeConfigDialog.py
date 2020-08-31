import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from tickFactor import TickFactor
from settingFactor import SettingFactor
from signalFactor import SignalFactor

class DDEConfigDlg (QtWidgets.QWidget):
    def __init__ (self, parent):
        super().__init__ (parent)
        self.setWindowTitle ("DDE Config")
        self.endable_checkbox = QtWidgets.QCheckBox ("Run With DDE")
        self.endable_checkbox.setChecked(False)
        self.endable_checkbox.stateChanged.connect(self.change_run_enable)
        self.service_label = QtWidgets.QLabel ("Service:", self)
        self.service = QtWidgets.QLineEdit ("XQLite", self)
        self.topic_label = QtWidgets.QLabel ("Topic:", self)
        self.topic = QtWidgets.QLineEdit ("Quote", self)
        self.advise_price_label = QtWidgets.QLabel ("Advise_Date_Time_Price:", self)
        self.advise_price = QtWidgets.QLineEdit ("FITXN*1.TF-TradingDate,Time,Price,Price", self)
        self.advise_ask_label = QtWidgets.QLabel ("Advise_Ask:", self)
        self.advise_ask = QtWidgets.QLineEdit ("FITXN*1.TF-BestAsk1,BestAskSize1,BestAsk2,BestAskSize2,BestAsk3,BestAskSize3,BestAsk4,BestAskSize4,BestAsk5,BestAskSize5", self)
        self.advise_bid_label = QtWidgets.QLabel ("Advise_Bid:", self)
        self.advise_bid = QtWidgets.QLineEdit ("FITXN*1.TF-BestBid1,BestBidSize1,BestBid2,BestBidSize2,BestBid3,BestBidSize3,BestBid4,BestBidSize4,BestBid5,BestBidSize5", self)

        self.ok = QtWidgets.QPushButton (self)
        self.ok.setText ("OK")
        self.ok.clicked.connect (self.clickedOK)

        vlay = QtWidgets.QVBoxLayout(self)
        #hlay = QtWidgets.QHBoxLayout(self)
        vlay.addWidget (self.endable_checkbox)
        vlay.addWidget (self.service_label)
        vlay.addWidget (self.service)
        vlay.addWidget (self.topic_label)
        vlay.addWidget (self.topic)
        vlay.addWidget (self.advise_price_label)
        vlay.addWidget (self.advise_price)
        vlay.addWidget (self.advise_ask_label)
        vlay.addWidget (self.advise_ask)
        vlay.addWidget (self.advise_bid_label)
        vlay.addWidget (self.advise_bid)
        vlay.addWidget (self.ok)

    def change_run_enable (self):
        pass

    def run (self):
        self.setUpdatesEnabled (False)
        self.updateBySettings ()
        self.setUpdatesEnabled (True)
        self.show ()

    def updateBySettings (self):
        enable = SettingFactor().getDDEEnable()
        if enable != "":
            self.endable_checkbox.setChecked(True)
        service = SettingFactor().getDDEService()
        if service != "":
            self.service.setText(service)
        topic = SettingFactor().getDDETopic()
        if topic != "":
            self.topic.setText(topic)
        advise = SettingFactor().getDDEAdvisePrice()
        if advise != "":
            self.advise_price.setText(advise)
        advise = SettingFactor().getDDEAdviseAsk()
        if advise != "":
            self.advise_ask.setText(advise)
        advise = SettingFactor().getDDEAdviseBid()
        if advise != "":
            self.advise_bid.setText(advise)

    def clickedOK (self):
        enable = self.endable_checkbox.isChecked()
        service = self.service.text()
        topic = self.topic.text ()
        advise_price = self.advise_price.text ()
        advise_ask = self.advise_ask.text ()
        advise_bid = self.advise_bid.text ()
        
        SettingFactor().setDDEEnable("True" if enable else "")
        SettingFactor().setDDEService(service)
        SettingFactor().setDDETopic(topic)
        SettingFactor().setDDEAdvisePrice(advise_price)
        SettingFactor().setDDEAdviseAsk(advise_ask)
        SettingFactor().setDDEAdviseBid(advise_bid)

        SignalFactor ().sign_dde_config_done.emit (enable)

