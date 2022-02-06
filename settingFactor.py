

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
        self.HWND = self.mainwindow.winId ()
        self.KBarInterval = int(self.getKBarInterval ())

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

    def getFreePosFreeOrderEnable (self):
        return self.setting.value("FreePosFreeOrder", "True")

    def setFreePosFreeOrderEnable (self, value):
        self.setting.setValue("FreePosFreeOrder", value)

    def getRunStopLoss (self):
        return self.setting.value("RunStopLoss ", "0")

    def setRunStopLoss  (self, value):
        self.setting.setValue("RunStopLoss ", value)

    def getYahooEnable (self):
        return self.setting.value("YahooEnable", "")

    def setYahooEnable (self, value):
        self.setting.setValue("YahooEnable", value)

    def getYahooProdId (self):
        return self.setting.value("YahooProdId", "")

    def setYahooProdId (self, value):
        self.setting.setValue("YahooProdId", value)       

    def getKBarInterval (self):
        #return self.setting.value("KBarInterval", "60")
        if hasattr(self, "KBarInterval") == False:
            return 60
        return self.KBarInterval 

    def setKBarInterval (self, value):
        number = 60
        if value[-1] == 's':
            number = int (value[:-1])
        elif value[-1] == 'm':
            number = int (value[:-1]) * 60
        self.KBarInterval = number
        #self.setting.setValue("KBarInterval", number) 