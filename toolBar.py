
import sys
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
from actionFactor import ActionFactor
from signalFactor import SignalFactor
from settingFactor import SettingFactor

class Time24Edit(QtWidgets.QTimeEdit):
    minTime = QtCore.QTime(0, 0, 0)
    maxTime = QtCore.QTime(23, 59, 59)
    _timeChanged = QtCore.Signal(QtCore.QTime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDisplayFormat('hh:mm:ss')
        self.setMinimumTime(self.minTime)
        self.setMaximumTime(self.maxTime)

        # "substitute" the base timeChanged signal with the custom one so that
        # we emit the correct HH:MM time
        self._baseTimeChanged = self.timeChanged
        self._baseTimeChanged.connect(self._checkTime)
        self.timeChanged = self._timeChanged

    def _checkTime(self, time):
        self.timeChanged.emit(self.time())

    def stepBy(self, step):
        fakeTime = super().time()
        seconds = fakeTime.second() + (fakeTime.minute() * 60) + (fakeTime.hour() * 3600)
        if self.currentSection() == self.SecondSection:
            seconds += step
        elif self.currentSection() == self.MinuteSection:
            seconds += step * 60
        elif self.currentSection() == self.HourSection:
            seconds += step * 3600
        # "sanitize" the value to 0-1440 "minutes"
        minutes, seconds = divmod(seconds, 60)
        hour, minutes =  divmod(minutes, 60)
        super().setTime(QtCore.QTime(hour, minutes, seconds))

    def stepEnabled(self):
        fakeTime = super().time()
        steps = 0
        if fakeTime > self.minTime:
            steps |= self.StepDownEnabled
        if fakeTime < self.maxTime:
            steps |= self.StepUpEnabled
        return steps

    def time(self):
        fakeTime = super().time()
        return QtCore.QTime(fakeTime.hour(), fakeTime.minute(), fakeTime.second())

    def setTime(self, time):
        super().setTime(QtCore.QTime(time.hour(), time.minute(), time.second()))

class ToolBar ():
    df_btn_open = 0
    df_btn_save = 1
    df_btn_connect_config = 2
    df_btn_reviewconfig = 3
    df_btn_reveiwrun = 4
    df_btn_reveiwsuspend = 5
    df_btn_reveiwstop = 6
    df_btn_reveiwslower = 7
    df_btn_reveiwfaster = 8
    df_btn_zoom_x = 9
    df_btn_zoom_y = 10
    df_btn_mark = 11
    df_btn_max = 12

    df_btn_review_start = df_btn_reviewconfig
    df_btn_review_end = df_btn_reveiwfaster +1

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.toolbar = QtWidgets.QToolBar()
        self.mainwindow.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(16,16))
        
        self.btn = [None] * ToolBar.df_btn_max

        action_factor = ActionFactor()
       
        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.openfile)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_open] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.savefile)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_save] = btn

        self.toolbar.addSeparator ()

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.connectconfig)
        btn.setCheckable (True)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_connect_config] = btn

        self.toolbar.addSeparator ()

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reviewconfig)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reviewconfig] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reveiwrun)
        btn.setCheckable (True)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reveiwrun] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reveiwsuspend)
        btn.setCheckable (True)
        action_factor.reveiwsuspend.triggered.connect (self.click_btn_reveiwsuspend)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reveiwsuspend] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reveiwstop)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reveiwstop] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reveiwslower)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reveiwslower] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.reveiwfaster)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_reveiwfaster] = btn

        self.reviewspeed = QtWidgets.QLabel("1x")
        self.toolbar.addWidget (self.reviewspeed)

        self.toolbar.addSeparator ()
        self.timeedit = Time24Edit ()
        self.timeedit.setMaximumWidth (150)
        self.toolbar.addWidget(self.timeedit)

        btn = QtWidgets.QPushButton ()
        btn.clicked.connect (action_factor.reviewgoto.triggered)
        btn.setMaximumWidth (30)
        btn.setText('Go')
        self.toolbar.addWidget(btn)
        action_factor.reviewgoto.triggered.connect (self.click_btn_reviewgoto)

        self.toolbar.addSeparator ()

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.zome_x)
        btn.setCheckable (True)
        action_factor.zome_x.triggered.connect (self.click_btn_zome_x)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_zoom_x] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.zome_y)
        btn.setCheckable (True)
        action_factor.zome_y.triggered.connect (self.click_btn_zome_y)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_zoom_y] = btn

        btn = QtWidgets.QToolButton ()
        btn.setDefaultAction (action_factor.mark)
        btn.setCheckable (True)
        action_factor.mark.triggered.connect (self.click_btn_mark)
        self.toolbar.addWidget(btn)
        self.btn[ToolBar.df_btn_mark] = btn

        SignalFactor ().sign_run_init.connect (self.run_init)
        SignalFactor ().sign_review_speed_change.connect (self.review_speed_change)
        SignalFactor ().sign_dde_config_done.connect (self.dde_config_done)
    
    def run_init (self):
        self.reviewspeed.setText ("{}x".format(1))

    def review_speed_change (self, speed):
        self.reviewspeed.setText ("{}x".format(speed))

    def click_btn_reveiwsuspend (self):
        btn = self.btn[ToolBar.df_btn_reveiwsuspend]
        checked = btn.isChecked() 
        btn.setChecked (not checked)

        for idx in range (ToolBar.df_btn_review_start, ToolBar.df_btn_review_end):
            if idx == ToolBar.df_btn_reveiwsuspend:
                continue
            self.btn[idx].setDisabled (not checked)
    
    def click_btn_zome_x (self):
        btn = self.btn[ToolBar.df_btn_zoom_x]
        checked = btn.isChecked() 
        btn.setChecked (not checked)

    def click_btn_zome_y (self):
        btn = self.btn[ToolBar.df_btn_zoom_y]
        checked = btn.isChecked() 
        btn.setChecked (not checked)

    def click_btn_mark (self):
        btn = self.btn[ToolBar.df_btn_mark]
        checked = btn.isChecked() 
        btn.setChecked (not checked)

    def dde_config_done  (self):
        enable = True if SettingFactor().getDDEEnable () != "" else False
        btn = self.btn[ToolBar.df_btn_connect_config]
        btn.setChecked (enable)

    def click_btn_reviewgoto (self):
        go_time = self.timeedit.time ()
        SignalFactor().sign_review_goto.emit (go_time)