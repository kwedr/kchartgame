import re
import math
import pandas as pd
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import datetime

from singleton import Singleton
from signalFactor import SignalFactor
from profilerFactor import ProfilerFactor
from signalFactor import SignalFactor
from PyWinDDE import DDEClient
from types import SimpleNamespace
from settingFactor import SettingFactor

class TickFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.mainwindow = mainwindow
        self.data = None
        self.dde = None
        self.review_timer = None
        SignalFactor ().sign_loadfile.connect (self.loadfile)
        SignalFactor ().sign_loadfile_rand.connect (self.loadfile_rand)
        SignalFactor ().sign_review_run.connect (self.review_run)
        SignalFactor ().sign_review_speed_change.connect (self.review_speed_change)
        SignalFactor ().sign_review_suspend.connect (self.review_suspend)
        SignalFactor ().sign_dde_config_done.connect (self.dde_config_done)
        SignalFactor ().sign_review_goto.connect (self.review_goto)

    def loadfile (self, filename):
        if filename.endswith (".rpt"):
            self.loadRPT (filename)
        elif filename.endswith (".cvs"):
            self.loadRPT (filename)
        pass

    def loadfile_rand (self, folder):
        file_list = []
        it = QtCore.QDirIterator (folder, ['*.rpt','*.csv'], QtCore.QDir.Files)
        while it.hasNext():
            file_list.append (it.next())
        
        from random import choice
        self.loadfile(choice(file_list))

    def loadRPT (self, filename):
        columns =['Date', 'ID', 'ContractMonth', 'Time', 'Close', 'Volumn', 'tmp1', 'tmp2', 'tmp3']
        self.data = pd.read_csv(filename, dtype=object, skiprows=1, names=columns, header=None, encoding = "ISO-8859-1").drop (['tmp1', 'tmp2', 'tmp3'], axis=1)
        self.data['ID'] = self.data['ID'].str.strip()
        self.data['ContractMonth'] = self.data['ContractMonth'].str.strip()
        self.data['Close'] = self.data['Close'].astype(float)
        self.data['Open'] = self.data['High'] = self.data['Low'] = self.data['Close']
        self.data['Volumn'] = self.data['Volumn'].astype(int) / 2
        self.data['Date'] = self.data['Date'].str.strip()
        self.data['Time'] = self.data['Time'].str.strip()
        self.data['Date_Time'] = pd.to_datetime(self.data['Date'] + ' ' + self.data['Time'])
        self.data.drop (['Date', 'Time'], axis=1, inplace = True)
        self.data.set_index (['ID','ContractMonth'], inplace = True)
        #self.data.to_csv (QtCore.QDir.currentPath() + "/test.csv")
        self.load_config ()

    def loadCVS (self, filename):
        pass

    def load_config (self):
        id = SettingFactor().getReviewConfigID()
        if id == "":
            id = "TX"
        filter = self.data.index.get_level_values('ID') == id
        df = self.data.iloc[filter]
        tmp_months = df.index.get_level_values('ContractMonth').unique().tolist ()
        max_month_num = 0
        month = tmp_months[0]
        for tmp_month in tmp_months:
            filter = df.index.get_level_values('ContractMonth') == tmp_month
            df_num = df[filter].shape[0]
            if df_num > max_month_num:
                max_month_num = df_num
                month = tmp_month
        SettingFactor().setReviewConfigMonth (month)
        filter = df.index.get_level_values('ContractMonth') == month
        df = df[filter]

        start_time = SettingFactor().getReviewConfigStartTime()
        if start_time == "":
            start_time = "0845"
            SettingFactor().setReviewConfigStartTime(start_time)

        end_time = SettingFactor().getReviewConfigEndTime()
        if end_time == "":
            end_time = "1345"
            SettingFactor().setReviewConfigEndTime(end_time)

        last_time = df['Date_Time'][-1]
        date = last_time.strftime('%Y%m%d')
        SettingFactor().setReviewConfigStartDate (date)
        SettingFactor().setReviewConfigEndDate (date)
        
    def review_run (self, id, contract_month, interval, start_time, end_time):
        self.review_timer = QtCore.QTimer()
        self.review_timer.timeout.connect(self.review_interval)
        self.review_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.review_timer_interval = interval
        self.review_timer_speed = 1
        self.review_timer_speed_change = False
        self.review_start_time = start_time
        self.review_end_time = end_time
        self.review_tick_idx = -1

        filter1 = self.data.index.get_level_values('ID') == id
        filter2 = self.data.index.get_level_values('ContractMonth') == contract_month

        self.review_tick = self.data.iloc[filter1 & filter2]
        self.review_tick = self.review_tick[self.review_tick['Date_Time'] >= start_time]
        self.review_tick = self.review_tick[self.review_tick['Date_Time'] <= end_time]

        self.curr_time = None
        self.next_time = None
        self.review_sec ()
        self.review_interval ()
        self.review_timer.start ()
        #ProfilerFactor().timer_start ()

    def review_sec (self):
        next_idx = self.review_tick_idx + 1
        tick = self.review_tick.iloc[next_idx]
        if self.next_time == None:
            self.next_time = tick.Date_Time
        self.curr_time = self.next_time
        delta = datetime.timedelta(seconds=1)
        self.next_time = self.curr_time + delta
        filter1 = self.review_tick['Date_Time'] >= self.curr_time
        filter2 = self.review_tick['Date_Time'] < self.next_time
        pd = self.review_tick[filter1 & filter2]
        pd_len = len(pd)
        self.review_timer_curr_interval = math.floor (self.review_timer_interval / self.review_timer_speed)
        if pd_len > 0:
            self.review_timer_curr_interval = math.floor (self.review_timer_curr_interval / pd_len)
        else:
            self.review_tick_idx = self.review_tick_idx -1
        self.review_timer.setInterval (self.review_timer_curr_interval)
        #self.review_timer.start (interval)
        
    def review_interval (self):
        old_tick_idx = self.review_tick_idx
        self.review_tick_idx = self.review_tick_idx + 1
        data_len = len(self.review_tick)
        if self.review_tick_idx >= data_len:
            self.review_timer.stop ()
            return

        new_tick = self.review_tick.iloc[self.review_tick_idx]

        if old_tick_idx >= 0:
            old_tick = self.review_tick.iloc[old_tick_idx]
            if new_tick.Date_Time != old_tick.Date_Time:
                #ProfilerFactor().timer_elapsed ()
                self.review_sec ()
        
        if old_tick_idx != self.review_tick_idx:
            SignalFactor().sign_tick_update.emit (new_tick)
        else:
            SignalFactor().sign_time_update.emit (self.curr_time)

    def review_speed_change (self, speed):
        if self.review_timer_speed == speed:
            return
        self.review_timer_speed = speed
        self.review_timer_speed_change = True

    def review_suspend (self):
        active = self.review_timer.isActive ()
        if active:
            self.review_timer.stop ()
        else:
            self.review_timer.start ()

    def dde_config_done (self, enable):
        if enable:
            self.dde_run ()
        else:
            del self.dde

    def dde_run (self):
        if self.dde:
            del self.dde
            self.dde = None

        #self.dde = DDEClient("XQLite", "Quote")
        #self.dde.advise("FITXN*1.TF-TradingDate,Time,Price", self.dde_callback_price)
        #self.dde.advise("FITXN*1.TF-BestBid1,BestBidSize1,BestBid2,BestBidSize2,BestBid3,BestBidSize3,BestBid4,BestBidSize4,BestBid5,BestBidSize5", self.dde_callback_best_bid)
        #self.dde.advise("FITXN*1.TF-BestAsk1,BestAskSize1,BestAsk2,BestAskSize2,BestAsk3,BestAskSize3,BestAsk4,BestAskSize4,BestAsk5,BestAskSize5", self.dde_callback_best_ask)

        self.dde = DDEClient(SettingFactor().getDDEService(), SettingFactor().getDDETopic())
        self.dde.advise(SettingFactor().getDDEAdvisePrice(), self.dde_callback_price)
        if SettingFactor().getDDEAdviseAsk() != "":
            self.dde.advise(SettingFactor().getDDEAdviseAsk(), self.dde_callback_best_ask)
        if SettingFactor().getDDEAdviseBid() != "":
            self.dde.advise(SettingFactor().getDDEAdviseBid(), self.dde_callback_best_bid)

        from datetime import datetime
        SignalFactor().sign_run_init.emit ({'start_time' : datetime.now().strftime("%Y%m%d%H%M")})

    def dde_callback_price (self, value, item):
        values = value.split (';')
        Open = High = Low = Close = float(re.match ('[+-]?([0-9]*[.])?[0-9]+', values[2]).group ())
        tick = SimpleNamespace (Date_Time = pd.Timestamp(values[0] + ' ' + values[1]), Close = Close, High = High, Low = Low, Open = Open)
        SignalFactor().sign_tick_update.emit (tick)

    def dde_callback_best_bid (self, value, item):
        bid = value.split (';')
        SignalFactor().sign_best_bid_update.emit (bid)

    def dde_callback_best_ask (self, value, item):
        ask = value.split (';')
        SignalFactor().sign_best_ask_update.emit (ask)

    def review_goto (self, time):
        import cProfile, pstats
        pr = cProfile.Profile()
        pr.enable ()
        self.run_review_goto(time)
        pr.disable()

        f = open('x.prof', 'a')
        sortby = 'cumulative'
        pstats.Stats(pr, stream=f).strip_dirs().sort_stats(sortby).print_stats()
        f.close()

    '''
    def review_goto (self, time):
        import cProfile

        pr = cProfile.Profile()
        pr.enable()
        self.run_review_goto (time)
        pr.disable()
        pr.print_stats(sort='cumtime')
    '''

    def review_goto (self, time):
        from actionFactor import ActionFactor
        SignalFactor().sign_review_goto_init.emit ()

        if self.review_timer is None or self.review_timer.isActive () == False:
            ActionFactor().reveiwrun.trigger ()

        is_suspend = False
        if ActionFactor().reveiwsuspend.isChecked () == False:
            ActionFactor().reveiwsuspend.trigger ()
            is_suspend = True

        start_time = self.review_tick['Date_Time'][0]
        tick_idx = -1
        tick = None

        check_time = pd.Timestamp (year=start_time.year, month=start_time.month, day=start_time.day, hour=time.hour(), minute=time.minute(), second=time.second())
        df = self.review_tick[self.review_tick['Date_Time'] < check_time]

        count = df.shape[0]
        progress = QtWidgets.QProgressDialog ("Progress...", "Cancel", 0, count)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.forceShow()

        start_idx = 0
        start_time = self.review_tick.iat[start_idx, 5]
        for i in range (0, count):
            tick_idx = tick_idx + 1
            progress.setValue(tick_idx)
            now_time = self.review_tick.iat[tick_idx, 5]

            if now_time - start_time >= pd.Timedelta(minutes=1):
                open = self.review_tick.iat[start_idx, 2]
                close = self.review_tick.iat[tick_idx-1, 0]
                ary = [self.review_tick.iat[i, 0] for i in range(start_idx, tick_idx) ]
                high = max (ary)
                low = min (ary)
                tick = SimpleNamespace (Date_Time = start_time, Close = close, High = high, Low = low, Open = open)
                SignalFactor().sign_tick_update.emit (tick)
                start_idx = tick_idx
                start_time = self.review_tick.iat[tick_idx, 5]

        open = self.review_tick.iat[start_idx, 2]
        close = self.review_tick.iat[tick_idx-1, 0]
        ary = [self.review_tick.iat[i, 0] for i in range(start_idx, tick_idx) ]
        high = max (ary)
        low = min (ary)
        tick = SimpleNamespace (Date_Time = start_time, Close = close, High = high, Low = low, Open = open)
        SignalFactor().sign_tick_update.emit (tick)
        self.review_tick_idx = tick_idx

        SignalFactor().sign_review_goto_done.emit ()

        if is_suspend == True:
            ActionFactor().reveiwsuspend.trigger ()



                
        
