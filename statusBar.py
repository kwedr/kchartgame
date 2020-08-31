import PySide2.QtWidgets as QtWidgets
from signalFactor import SignalFactor

class StatusBar ():
    def __init__ (self, parent):
        self.statusbar = parent.statusBar ()
        self.statusbar.setSizeGripEnabled(True)
        self.label_time = QtWidgets.QLabel ('00:00')
        self.label_time.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken);
        self.statusbar.addPermanentWidget (self.label_time)
        
        SignalFactor().sign_tick_update.connect (self.tick_update)
        SignalFactor().sign_time_update.connect (self.time_update)

    def tick_update (self, tick):
        self.label_time.setText (tick.Date_Time.strftime("%Y/%m/%d %H:%M:%S")) 

    def time_update (self, date_time):
        self.label_time.setText (date_time.strftime("%Y/%m/%d %H:%M:%S")) 
