import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QDockWidget, QListWidget)
import PySide2.QtCore as QtCore
from candlestickWidget import CandlestickChartWidget
from menuBar import MenuBar
from toolBar import ToolBar
from actionFactor import ActionFactor
from signalFactor import SignalFactor
from logFactor import LogFactor
from profilerFactor import ProfilerFactor
from priceLadderWidget import PriceLadderWidget
from recordTradeWidget import RecordTradeWidget
from brokerFactor import BrokerFactor
from tickFactor import TickFactor
from reviewConfigDialog import ReviewConfigDlg
from connectConfigDialog import ConnectConfigDlg
from statusBar import StatusBar
from settingFactor import SettingFactor
from hlineConfigDialog import HLineConfigDlg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1024, 768)

        self.init_factor ()
        
        self.menubar = MenuBar (self)
        self.toolbar = ToolBar (self)
        self.statusbar = StatusBar (self)

        self.dockWidgetCandle = QDockWidget('CandleView', self)
        #self.dockWidgetCandle.setMinimumSize(QtCore.QSize(600, 400))
        self.dockWidgetCandle.resize(QtCore.QSize(800, 400))
        self.WidgetCandle = CandlestickChartWidget()
        self.dockWidgetCandle.setWidget(self.WidgetCandle)
        self.dockWidgetCandle.setFloating(False)

        self.dockWidgetPriceLadder = QDockWidget('PriceLadder', self)
        self.dockWidgetPriceLadder.setMinimumWidth(200)
        self.dockWidgetPriceLadder.setMaximumWidth(500)
        #self.dockWidgetPriceLadder.resize(QtCore.QSize(200, 500))
        self.WidgetPriceLadder = PriceLadderWidget(self)
        self.dockWidgetPriceLadder.setWidget(self.WidgetPriceLadder)
        self.dockWidgetPriceLadder.setFloating(False)

        self.dockWidgetRecordTrade = QDockWidget('RecordTrade', self)
        self.dockWidgetRecordTrade.setMinimumWidth(200)
        self.dockWidgetRecordTrade.setMaximumWidth(500)
        #self.dockWidgetRecordTrade.resize(QtCore.QSize(200, 500))
        self.WidgeRecordTrade = RecordTradeWidget(self)
        self.dockWidgetRecordTrade.setWidget(self.WidgeRecordTrade)
        self.dockWidgetRecordTrade.setFloating(False)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidgetCandle)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWidgetPriceLadder)
        self.tabifyDockWidget (self.dockWidgetPriceLadder, self.dockWidgetRecordTrade)
        self.dockWidgetPriceLadder.raise_()

        #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWidgetRecordTrade)

        #self.setCorner(QtCore.Qt.TopLeftCorner,     QtCore.Qt.LeftDockWidgetArea)
        #self.setCorner(QtCore.Qt.BottomLeftCorner,  QtCore.Qt.LeftDockWidgetArea)
        #self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        SignalFactor ().sign_tick_update.connect (self.debug_tick_update)
        SignalFactor ().sign_connect_config.connect (self.connect_config)
        SignalFactor ().sign_review_config.connect (self.review_config)
        SignalFactor ().sign_hline_config.connect (self.hline_config)

    def init_factor (self):
        LogFactor ().init (self)
        SignalFactor ().init (self)
        ActionFactor ().init (self)
        ProfilerFactor ().init (self)
        BrokerFactor (). init (self)
        TickFactor ().init (self)
        SettingFactor().init (self)

    def connect_config(self):
        dlg = ConnectConfigDlg (self)
        dlg.run ()

    def review_config(self):
        dlg = ReviewConfigDlg (self)
        dlg.run ()

    def debug_tick_update (self, tick):
        #LogFactor().debug ("tick: {} close:{} volumn:{}".format (tick.Date_Time, tick.Close, tick.Volumn))
        pass

    def hline_config(self):
        dlg = HLineConfigDlg (self)
        dlg.run ()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("kchartgame")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())