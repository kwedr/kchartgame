
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
from tickFactor import TickFactor
from signalFactor import SignalFactor
from singleton import Singleton
from settingFactor import SettingFactor

class ActionFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.mainwindow = mainwindow
        
        self.openfile = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/046.png"), "&Open", mainwindow)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip("Open")
        self.openfile.triggered.connect(self.action_openFile)

        self.openfile_rand = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/046.png"), "Open &Rand File", mainwindow)
        self.openfile_rand.setShortcut('Ctrl+R')
        self.openfile_rand.setStatusTip("Open Rand File")
        self.openfile_rand.triggered.connect(self.action_openFileRand)

        self.savefile = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/095.png"), "&Save", mainwindow)
        self.savefile.setShortcut('Ctrl+S')
        self.savefile.setStatusTip("Save")
        self.savefile.triggered.connect(self.action_saveFile)

        self.exit = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/101.png"), '&Exit', mainwindow)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit')
        self.exit.triggered.connect(mainwindow.close)

        self.reveiwspeed = 1
        self.reveiwspeedlist = [0.5, 1, 2, 4, 8, 16]
        self.reveiwrun = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/131.png"), '&Run', mainwindow)
        self.reveiwrun.setShortcut('F5')
        self.reveiwrun.setStatusTip('RUN')
        self.reveiwrun.triggered.connect(self.action_reveiwRun)

        self.reveiwsuspend = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/141.png"), '&Suspend', mainwindow)
        self.reveiwsuspend.setShortcut('Ctrl+M')
        self.reveiwsuspend.setStatusTip('Suspend')
        self.reveiwsuspend.triggered.connect(self.action_reveiwSuspend)

        self.reveiwstop = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/142.png"), '&Stop', mainwindow)
        self.reveiwstop.setShortcut('Ctrl+E')
        self.reveiwstop.setStatusTip('Stop')
        self.reveiwstop.triggered.connect(self.action_reveiwStop)

        self.reveiwprev = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/136.png"), '&Prev', mainwindow)
        self.reveiwprev.setShortcut('Ctrl+Left')
        self.reveiwprev.setStatusTip('Prev')
        self.reveiwprev.triggered.connect(self.action_reveiwPrev)

        self.reveiwnext= QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/135.png"), '&Next', mainwindow)
        self.reveiwnext.setShortcut('Ctrl+Right')
        self.reveiwnext.setStatusTip('Next')
        self.reveiwnext.triggered.connect(self.action_reveiwNext)

        self.reveiwfaster = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/129.png"), '&Faster', mainwindow)
        self.reveiwfaster.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Plus))
        self.reveiwfaster.setStatusTip('Faster')
        self.reveiwfaster.triggered.connect(self.action_reveiwFaster)

        self.reveiwslower = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/130.png"), '&Slower', mainwindow)
        self.reveiwslower.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Minus))
        self.reveiwslower.setStatusTip('Slower')
        self.reveiwslower.triggered.connect(self.action_reveiwSlower)

        self.reviewconfig = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/087.png"), '&Config', mainwindow)
        self.reviewconfig.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_K))
        self.reviewconfig.setStatusTip('Config')
        self.reviewconfig.triggered.connect(self.action_reveiwConfig)

        self.zome_x = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/201.png"), '&ZoomX', mainwindow)
        self.zome_x.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_Plus))
        self.zome_x.setStatusTip('ZoomX')
        self.zome_x.triggered.connect(self.action_zoomX)

        self.zome_y = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/202.png"), '&ZoomY', mainwindow)
        self.zome_y.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT | QtCore.Qt.Key_Minus))
        self.zome_y.setStatusTip('ZoomY')
        self.zome_y.triggered.connect(self.action_zoomY)

        self.mark = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/083.png"), '&Mark', mainwindow)
        self.mark.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_M))
        self.mark.setStatusTip('Mark')
        self.mark.triggered.connect(self.action_mark)

        self.hline = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/203.png"), '&HLine', mainwindow)
        self.hline.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_H))
        self.hline.setStatusTip('HLine')
        self.hline.triggered.connect(self.action_hline_config)

        self.connectconfig = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/041.png"), '&Connect', mainwindow)
        self.connectconfig.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_E))
        self.connectconfig.setStatusTip('ConnectConfig')
        self.connectconfig.triggered.connect(self.action_connect_config)

        self.reviewgoto = QtWidgets.QAction(None, '&Goto', mainwindow)
        self.reviewgoto.triggered.connect(self.action_reveiwgoto)

        self.reconnect = QtWidgets.QAction(QtGui.QIcon("icon/diagona-icons-1.0/icons/16/125.png"), '&ReConnect', mainwindow)
        self.reconnect.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_R))
        self.reconnect.setStatusTip('ReConnect')
        self.reconnect.triggered.connect(self.action_reconnect)

        self.k30s = QtWidgets.QAction("30s", mainwindow)
        self.k30s.setStatusTip('30s')
        self.k30s.triggered.connect(self.action_k30s)

        self.k1m = QtWidgets.QAction("1m", mainwindow)
        self.k1m.setStatusTip('1m')
        self.k1m.triggered.connect(self.action_k1m)

        self.k5m = QtWidgets.QAction("5m", mainwindow)
        self.k5m.setStatusTip('5m')
        self.k5m.triggered.connect(self.action_k5m)

    def action_openFile (self):
        filters = ('default (*.rpt *.csv);;'
                   'all file (*.*);;')

        filename = QtWidgets.QFileDialog.getOpenFileName(self.mainwindow, 'Open File', './', filter=filters)[0]
        SignalFactor().sign_loadfile.emit (filename)
        QtWidgets.QMessageBox.about(self.mainwindow, "Message", "Open File Finish")

    def action_openFileRand (self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "", "./")
        SignalFactor().sign_loadfile_rand.emit (folder)
        QtWidgets.QMessageBox.about(self.mainwindow, "Message", "Open File Finish")

    def action_saveFile (self):
        filters = ('PNG (*.png);;')
        filename = QtWidgets.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', './', filter=filters)[0]
        SignalFactor().sign_savefile.emit (filename)
        QtWidgets.QMessageBox.about(self.mainwindow, "Message", "Save File Finish")

    def action_reveiwRun (self):
        self.reveiwspeed = 1
        id = SettingFactor().getReviewConfigID()
        month = SettingFactor().getReviewConfigMonth()
        start_time = SettingFactor().getReviewConfigStartDate() + SettingFactor().getReviewConfigStartTime()
        end_time = SettingFactor().getReviewConfigEndDate() + SettingFactor().getReviewConfigEndTime()

        SignalFactor().sign_run_init.emit ({'start_time' : start_time, 'end_time':end_time})
        SignalFactor().sign_review_run.emit (id, month, 1000, start_time, end_time)

        #SignalFactor().sign_run_init.emit ({'start_time' : '202003310845', 'end_time':'202003311345'})
        #SignalFactor().sign_review_run.emit ('TX', '202004', 1000, '202003310845', '202003311345')

    def action_reveiwSuspend (self):
        SignalFactor().sign_review_suspend.emit ()

    def action_reveiwStop (self):
        pass

    def action_reveiwPrev (self):
        SignalFactor().sign_review_prev.emit ()

    def action_reveiwNext (self):
        SignalFactor().sign_review_next.emit ()

    def action_reveiwFaster (self):
        self.reveiwspeed = self.reveiwspeed + 1
        if (self.reveiwspeed >= len(self.reveiwspeedlist)):
            self.reveiwspeed = len(self.reveiwspeedlist)-1
        SignalFactor().sign_review_speed_change.emit (self.reveiwspeedlist[self.reveiwspeed])

    def action_reveiwSlower (self):
        self.reveiwspeed = self.reveiwspeed -  1
        if (self.reveiwspeed < 0):
            self.reveiwspeed = 0
        SignalFactor().sign_review_speed_change.emit (self.reveiwspeedlist[self.reveiwspeed])

    def action_reveiwConfig (self):
        SignalFactor().sign_review_config.emit ()

    def action_zoomX (self):
        SignalFactor().sign_zoom_x_visible.emit ()

    def action_zoomY (self):
        SignalFactor().sign_zoom_y_visible.emit ()

    def action_mark (self):
        SignalFactor().sign_mark.emit ()

    def action_hline_config (self):
        SignalFactor().sign_hline_config.emit ()

    def action_connect_config (self):
        SignalFactor().sign_connect_config.emit ()

    def action_reveiwgoto (self):
        pass
    
    def action_reconnect (self):
        SignalFactor().sign_reconnect.emit ()
        SignalFactor().sign_reconnect_done.emit ()

    def action_k30s (self):
        SettingFactor().setKBarInterval ('30s')
        SignalFactor().sign_kbar_interval_change_init.emit ()
        SignalFactor().sign_kbar_interval_change.emit ()

    def action_k1m (self):
        SettingFactor().setKBarInterval ('1m')
        SignalFactor().sign_kbar_interval_change_init.emit ()
        SignalFactor().sign_kbar_interval_change.emit ()

    def action_k5m (self):
        SettingFactor().setKBarInterval ('5m')
        SignalFactor().sign_kbar_interval_change_init.emit ()
        SignalFactor().sign_kbar_interval_change.emit ()
