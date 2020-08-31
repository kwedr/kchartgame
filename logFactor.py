

import logging, os
from logging import handlers

from singleton import Singleton

class LogFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.mainwindow = mainwindow

        self.logger = logging.getLogger('app')
        #self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        hdlr = logging.FileHandler(os.path.join("./", 'app.log'), encoding="utf-8")
        hdlr.setFormatter(logFormatter)
        self.logger.addHandler(hdlr)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug (msg, *args, **kwargs)
