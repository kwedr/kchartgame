import sys
from actionFactor import ActionFactor

class MenuBar ():
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.menubar = mainwindow.menuBar()

        action_factor = ActionFactor()

        fileMenu = self.menubar.addMenu("&File")
        fileMenu.addAction(action_factor.openfile)
        fileMenu.addAction(action_factor.openfile_rand)
        fileMenu.addAction(action_factor.savefile)
        fileMenu.addAction(action_factor.exit)


