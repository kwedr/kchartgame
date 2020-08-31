from PySide2.QtCore import QObject, Signal
from singleton import Singleton

class SignalFactor (Singleton, QObject):
    sign_loadfile = Signal(object)
    sign_loadfile_rand = Signal(object)
    sign_savefile = Signal(object)
    sign_run_init = Signal(object)
    sign_review_run = Signal(object, object, object, object, object)
    sign_tick_update = Signal(object)
    sign_time_update = Signal(object)
    sign_best_bid_update = Signal(object)
    sign_best_ask_update = Signal(object)
    sign_trade_order_market = Signal(object, object, object)
    sign_trade_order_market_ret = Signal(object, object, object)
    sign_trade_order_market_buy_clear = Signal()
    sign_trade_order_market_sell_clear = Signal()
    sign_trade_order_mit = Signal(object, object, object)
    sign_trade_order_mit_ret = Signal(object, object, object)
    sign_trade_order_mit_buy_clear = Signal()
    sign_trade_order_mit_sell_clear = Signal()
    sign_trade_clear = Signal()
    sign_trade_deal = Signal(object, object, object, object)
    sign_review_speed_change = Signal(object)
    sign_review_config = Signal()
    sign_review_suspend = Signal ()
    sign_zoom_x_visible = Signal ()
    sign_zoom_y_visible = Signal ()
    sign_mark = Signal ()
    sign_connect_config = Signal ()
    sign_dde_config_done = Signal (object)
    sign_review_goto = Signal(object)
    sign_review_goto_init = Signal()
    sign_review_goto_done = Signal()
    sign_yuanta_config_done = Signal ()

    factor_init = False
    
    def __init__ (self):
        if self.factor_init == False:
            super().__init__()

    def init (self, mainwindow):
        self.factor_init = True
        self.mainwindow = mainwindow

