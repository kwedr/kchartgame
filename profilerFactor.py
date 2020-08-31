
from singleton import Singleton
from PySide2.QtCore import Qt, QTimer, QElapsedTimer
from logFactor import LogFactor

class ProfilerFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.factor_init = True
        self.mainwindow = mainwindow
        self.timer = None

    def timer_start (self):
        self.timer = QElapsedTimer ()
        self.timer.start()

    def timer_elapsed (self):
        elapsed = self.timer.elapsed()
        LogFactor().debug ("timer elapsed：{}".format (elapsed))
        self.timer.restart()

    def timer_finish (self):
        elapsed = self.timer.elapsed()
        LogFactor().debug ("timer elapsed：{}".format (elapsed))
        self.timer = None