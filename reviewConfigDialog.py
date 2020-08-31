import pandas as pd
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from tickFactor import TickFactor
from settingFactor import SettingFactor

class ReviewConfigDlg (QtWidgets.QDialog):
    def __init__ (self, parent):
        super().__init__ (parent)
        self.setWindowTitle ("Review Config")
        self.id_label = QtWidgets.QLabel ("商品:", self)
        self.id = QtWidgets.QComboBox (self)
        self.id.currentTextChanged.connect (self.idTextChanged)
        self.month_label = QtWidgets.QLabel ("合約:", self)
        self.month = QtWidgets.QComboBox (self)
        self.month.currentTextChanged.connect (self.monthTextChanged)
        self.start_date_label = QtWidgets.QLabel ("開始日期:", self)
        self.start_date = QtWidgets.QDateEdit (self)
        self.start_time_label = QtWidgets.QLabel ("開始時間:", self)
        self.start_time = QtWidgets.QTimeEdit (self)
        self.start_time.setDisplayFormat('HH:mm:ss')
        self.end_date_label = QtWidgets.QLabel ("結束日期:", self)
        self.end_date = QtWidgets.QDateEdit (self)
        self.end_time_label = QtWidgets.QLabel ("結束時間:", self)
        self.end_time = QtWidgets.QTimeEdit (self)
        self.end_time.setDisplayFormat('HH:mm:ss')
        self.ok = QtWidgets.QPushButton (self)
        self.ok.setText ("OK")
        self.ok.clicked.connect (self.clickedOK)

        vlay = QtWidgets.QVBoxLayout(self)
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget (self.id_label)
        hlay.addWidget (self.id)
        hlay.addWidget (self.month_label)
        hlay.addWidget (self.month)
        vlay.addLayout (hlay)
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget (self.start_date_label)
        hlay.addWidget (self.start_date)
        hlay.addWidget (self.start_time_label)
        hlay.addWidget (self.start_time)
        vlay.addLayout (hlay)
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget (self.end_date_label)
        hlay.addWidget (self.end_date)
        hlay.addWidget (self.end_time_label)
        hlay.addWidget (self.end_time)
        vlay.addLayout (hlay)
        vlay.addWidget (self.ok)

    def run (self):
        self.setUpdatesEnabled (False)
        self.df = TickFactor().data
        if not self.df is None and not self.df.empty:
            ids = self.df.index.get_level_values('ID').unique().tolist ()
            self.id.clear()
            self.id.addItems(ids)
            self.updateBySettings ()
        self.setUpdatesEnabled (True)
        self.show ()

    def updateBySettings (self):
        id = SettingFactor().getReviewConfigID()
        ids = self.df.index.get_level_values('ID').unique().tolist ()
        if not id in ids:
            return

        self.id.blockSignals(True)
        self.id.setCurrentText(id)
        self.updateMonth ()
        self.id.blockSignals(False)

        filter = self.df.index.get_level_values('ID') == self.id.currentText()
        df = self.df.iloc[filter]
        tmp_months = df.index.get_level_values('ContractMonth').unique().tolist ()
        max_month_num = 0
        month = SettingFactor().getReviewConfigMonth()
        if month == "":
            month = tmp_months[0]
            for tmp_month in tmp_months:
                filter = df.index.get_level_values('ContractMonth') == tmp_month
                df_num = df[filter].shape[0]
                if df_num > max_month_num:
                    max_month_num = df_num
                    month = tmp_month
        
        if month != "":
            if month in tmp_months:
                self.month.blockSignals(True)
                self.month.setCurrentText(month)
                self.updateDateTime ()
                self.month.blockSignals(False)

        start_date = SettingFactor().getReviewConfigStartDate()
        if start_date != "":
            self.start_date.setDate (QtCore.QDate.fromString(start_date, "yyyyMMdd"))
        start_time = SettingFactor().getReviewConfigStartTime()
        if start_time != "":
           self.start_time.setTime (QtCore.QTime.fromString(start_time, "hhmm"))
        end_date = SettingFactor().getReviewConfigEndDate()
        if end_date != "":
            self.end_date.setDate (QtCore.QDate.fromString(end_date, "yyyyMMdd"))
        end_time = SettingFactor().getReviewConfigEndTime()
        if end_time != "":
           self.end_time.setTime (QtCore.QTime.fromString(end_time, "hhmm"))

    def updateMonth (self):
        filter = self.df.index.get_level_values('ID') == self.id.currentText()
        df = self.df.iloc[filter]
        tmp_months = df.index.get_level_values('ContractMonth').unique().tolist ()
        months = []
        for m in tmp_months:
            if pd.isna(m) or m.find ('/') > 0:
                continue
            months.append (m)
        months = sorted(months)
        self.month.clear()
        self.month.addItems(months)
        self.month.setCurrentIndex(0)

    def updateDateTime (self):
        filter1 = self.df.index.get_level_values('ID') == self.id.currentText()
        filter2 = self.df.index.get_level_values('ContractMonth') == self.month.currentText()
        df = self.df.iloc[filter1 & filter2]
        df = df.sort_values ('Date_Time')
        if df.empty:
            return
        start = df['Date_Time'][0]
        end = df['Date_Time'][-1]

        self.start_date.setDate (QtCore.QDate (start.year, start.month, start.day))
        self.start_time.setTime (QtCore.QTime (start.hour, start.minute))
        self.end_date.setDate (QtCore.QDate (end.year, end.month, end.day))
        self.end_time.setTime (QtCore.QTime (end.hour, end.minute))

    def idTextChanged (self, txt):
        self.updateMonth ()

    def monthTextChanged (self, txt):
        self.updateDateTime ()

    def clickedOK (self):
        id = self.id.currentText()
        month = self.month.currentText ()
        start_date = self.start_date.date ().toString('yyyyMMdd')
        start_time  = self.start_time.time().toString('hhmm')
        end_date = self.end_date.date ().toString('yyyyMMdd')
        end_time  = self.end_time.time().toString('hhmm')

        SettingFactor().setReviewConfigID(id)
        SettingFactor().setReviewConfigMonth(month)
        SettingFactor().setReviewConfigStartDate(start_date)
        SettingFactor().setReviewConfigStartTime(start_time)
        SettingFactor().setReviewConfigEndDate(end_date)
        SettingFactor().setReviewConfigEndTime(end_time)

        self.close ()

