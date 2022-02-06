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
    sign_trade_order_limit_market = Signal(object, object, object)
    sign_trade_clear = Signal()
    sign_trade_deal = Signal(object, object, object, object)
    sign_trade_order_ret = Signal(object, object)
    sign_review_speed_change = Signal(object)
    sign_review_config = Signal()
    sign_review_suspend = Signal ()
    sign_review_prev = Signal ()
    sign_review_prev_done = Signal (object)
    sign_review_next = Signal ()
    sign_review_next_done = Signal (object)
    sign_zoom_x_visible = Signal ()
    sign_zoom_y_visible = Signal ()
    sign_mark = Signal ()
    sign_connect_config = Signal ()
    sign_connect_config_done = Signal ()
    sign_dde_config_done = Signal (object)
    sign_review_goto = Signal(object)
    sign_review_goto_init = Signal()
    sign_review_goto_done = Signal()
    sign_hline_config = Signal ()
    sign_hline_change = Signal (object, object)
    sign_reconnect = Signal ()
    sign_reconnect_done = Signal ()
    sign_reconnect_trade_order_ret = Signal(object)
    sign_reconnect_trade_order_ret_done = Signal()
    sign_reconnect_trade_order_deal = Signal(object, object, object, object)
    sign_get_account = Signal ()
    sign_get_account_done = Signal ()
    sign_yahoo_config_done = Signal (object)
    sign_kbar_interval_change_init = Signal ()
    sign_kbar_interval_change = Signal ()
    sign_kbar_deal_mark = Signal (object)

    factor_init = False
    
    def __init__ (self):
        if self.factor_init == False:
            super().__init__()

    def init (self, mainwindow):
        self.factor_init = True
        self.mainwindow = mainwindow

