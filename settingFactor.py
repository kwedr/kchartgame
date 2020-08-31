

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
from singleton import Singleton

class SettingFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.mainwindow = mainwindow
        ini_file = QtCore.QDir.currentPath() + "/" + QtWidgets.QApplication.applicationName() + ".ini"
        self.setting = QtCore.QSettings (ini_file, QtCore.QSettings.IniFormat)

    def getReviewConfigID (self):
        return self.setting.value("ReviewConfigID", "TX")

    def setReviewConfigID (self, value):
        self.setting.setValue("ReviewConfigID", value)

    def getReviewConfigMonth (self):
        return self.setting.value("ReviewConfigMonth", "")

    def setReviewConfigMonth (self, value):
        self.setting.setValue("ReviewConfigMonth", value)

    def setReviewConfigStartDate (self, value):
        self.setting.setValue("ReviewConfigStartDate", value)
    
    def getReviewConfigStartDate (self):
        return self.setting.value("ReviewConfigStartDate", "")

    def setReviewConfigStartTime (self, value):
        self.setting.setValue("ReviewConfigStartTime", value)

    def getReviewConfigStartTime (self):
        return self.setting.value("ReviewConfigStartTime", "")

    def setReviewConfigEndDate (self, value):
        self.setting.setValue("ReviewConfigEndDate", value)
    
    def getReviewConfigEndDate (self):
        return self.setting.value("ReviewConfigEndDate", "")

    def setReviewConfigEndTime (self, value):
        self.setting.setValue("ReviewConfigEndTime", value)

    def getReviewConfigEndTime (self):
        return self.setting.value("ReviewConfigEndTime", "")

    def getDDEEnable (self):
        return self.setting.value("DDEEnable", "")

    def setDDEEnable (self, value):
        self.setting.setValue("DDEEnable", value)

    def getDDEService (self):
        return self.setting.value("DDEService", "")

    def setDDEService (self, value):
        self.setting.setValue("DDEService", value)

    def getDDETopic (self):
        return self.setting.value("DDETopic", "")

    def setDDETopic (self, value):
        self.setting.setValue("DDETopic", value)

    def getDDEAdvisePrice (self):
        return self.setting.value("DDEAdvisePrice", "")

    def setDDEAdvisePrice (self, value):
        self.setting.setValue("DDEAdvisePrice", value)

    def getDDEAdviseAsk (self):
        return self.setting.value("DDEAdviseAsk", "")

    def setDDEAdviseAsk (self, value):
        self.setting.setValue("DDEAdviseAsk", value)

    def getDDEAdviseBid (self):
        return self.setting.value("DDEAdviseBid", "")

    def setDDEAdviseBid (self, value):
        self.setting.setValue("DDEAdviseBid", value)        