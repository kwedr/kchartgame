import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from tickFactor import TickFactor
from settingFactor import SettingFactor
from signalFactor import SignalFactor

class YahooConfigDlg (QtWidgets.QWidget):
    def __init__ (self, parent):
        super().__init__ (parent)
        self.setWindowTitle ("Yahoo Config")
        self.prodid_label = QtWidgets.QLabel ("Prod Id:", self)
        self.prodid = QtWidgets.QLineEdit ("WTX%26", self)

        self.ok = QtWidgets.QPushButton (self)
        self.ok.setText ("OK")
        self.ok.clicked.connect (self.clickedOK)

        vlay = QtWidgets.QVBoxLayout(self)
        #hlay = QtWidgets.QHBoxLayout(self)
        vlay.addWidget (self.prodid_label)
        vlay.addWidget (self.prodid)
        vlay.addSpacing (500)
        vlay.addWidget (self.ok)

    def change_run_enable (self):
        pass

    def run (self):
        self.setUpdatesEnabled (False)
        self.updateBySettings ()
        self.setUpdatesEnabled (True)
        self.show ()

    def updateBySettings (self):
        st = SettingFactor()
        self.prodid.setText (st.getYahooProdId ())

    def clickedOK (self):
        prodid = self.prodid.text()
        SettingFactor().setYahooProdId(prodid)

        SignalFactor ().sign_yahoo_config_done.emit (True)