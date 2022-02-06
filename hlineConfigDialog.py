import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from signalFactor import SignalFactor

class HLineConfigDlg (QtWidgets.QDialog):
    def __init__ (self, parent):
        super().__init__ (parent)
        self.setWindowTitle ("HLine Config")
        self.line_label = QtWidgets.QLabel ("HLine:", self)
        self.line_number = QtWidgets.QLineEdit (self)
        self.line_number.setInputMask("9999999999")
        self.btn_add = QtWidgets.QPushButton (self)
        self.btn_add.setText ("Add")
        self.btn_add.clicked.connect (self.clickedAdd)
        self.btn_del = QtWidgets.QPushButton (self)
        self.btn_del.setText ("Del")
        self.btn_del.clicked.connect (self.clickedDel)

        vlay = QtWidgets.QVBoxLayout(self)
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget (self.line_label)
        hlay.addWidget (self.line_number)
        vlay.addLayout (hlay)
        vlay.addWidget (self.btn_add)
        vlay.addWidget (self.btn_del)

    def run (self):
        self.setUpdatesEnabled (False)
        self.setUpdatesEnabled (True)
        self.show ()

    def clickedAdd (self):
        value = self.line_number.text() 
        SignalFactor ().sign_hline_change.emit (value, 1)
        self.close ()

    def clickedDel (self):
        value = self.line_number.text() 
        SignalFactor ().sign_hline_change.emit (value, -1)
        self.close ()