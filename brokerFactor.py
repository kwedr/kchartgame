from types import SimpleNamespace
from signalFactor import SignalFactor
from singleton import Singleton
from settingFactor import SettingFactor

class BrokerFactor (Singleton):
    def __init__ (self):
        pass

    def init (self, mainwindow):
        self.mainwindow = mainwindow
        self.mit = {}
        self.market = {}
        self.trade = []
        self.account =  SimpleNamespace (profit =  0, fee = 0)

        SignalFactor().sign_run_init.connect (self.run_init)
        SignalFactor().sign_tick_update.connect (self.tick_update)
        SignalFactor().sign_trade_order_market.connect (self.trade_order_market)
        SignalFactor().sign_trade_order_limit_market.connect (self.trade_order_limit_market)
        SignalFactor().sign_trade_order_market_buy_clear.connect (self.trade_order_market_buy_clear)
        SignalFactor().sign_trade_order_market_sell_clear.connect (self.trade_order_market_sell_clear)
        SignalFactor().sign_trade_order_mit.connect (self.trade_order_mit)
        SignalFactor().sign_trade_order_mit_buy_clear.connect  (self.trade_order_mit_buy_clear)
        SignalFactor().sign_trade_order_mit_sell_clear.connect  (self.trade_order_mit_sell_clear)
        SignalFactor().sign_trade_clear.connect  (self.trade_clear)

    def deactive (self):
        SignalFactor().sign_run_init.disconnect (self.run_init)
        SignalFactor().sign_tick_update.disconnect (self.tick_update)
        SignalFactor().sign_trade_order_market.disconnect (self.trade_order_market)
        SignalFactor().sign_trade_order_limit_market.disconnect (self.trade_order_limit_market)
        SignalFactor().sign_trade_order_market_buy_clear.disconnect (self.trade_order_market_buy_clear)
        SignalFactor().sign_trade_order_market_sell_clear.disconnect (self.trade_order_market_sell_clear)
        SignalFactor().sign_trade_order_mit.disconnect (self.trade_order_mit)
        SignalFactor().sign_trade_order_mit_buy_clear.disconnect  (self.trade_order_mit_buy_clear)
        SignalFactor().sign_trade_order_mit_sell_clear.disconnect  (self.trade_order_mit_sell_clear)
        SignalFactor().sign_trade_clear.disconnect  (self.trade_clear)

    def tick_update (self, tick):
        self.tick = tick
        self.trade_exec ()

    def run_init (self, count):
        self.mit = {}
        self.trade = []
        self.account =  SimpleNamespace( profit =  0, fee = 0 )

    def trade_order_market (self, price, count, long_short):
        #"""
        if not self.trade or self.trade[-1].long_short == long_short:
            trade = SimpleNamespace()
            trade.price = self.tick.Close
            trade.long_short = long_short
            trade.count = count
            self.trade.append (trade)
            SignalFactor().sign_trade_deal.emit (self.tick, long_short, trade.count, 0)
        else:
            tmp_trade = []
            market_count = count
            for t in self.trade:
                if market_count <= 0:
                    tmp_trade.append(t)
                    continue
                if t.count > market_count:
                    if long_short:
                        gain = (t.price - self.tick.Close) * market_count
                    else:
                        gain = (self.tick.Close - t.price) * market_count
                    self.account.profit = self.account.profit + gain
                    SignalFactor().sign_trade_deal.emit (self.tick, long_short, market_count, gain)
                    self.account.fee = self.account.fee + market_count
                    t.count = t.count - market_count
                    market_count = 0
                    tmp_trade.append(t)
                else:
                    if long_short:
                        gain = (t.price - self.tick.Close) * t.count
                    else:
                        gain = (self.tick.Close - t.price) * t.count
                    self.account.profit = self.account.profit + gain
                    self.account.fee = self.account.fee + t.count
                    SignalFactor().sign_trade_deal.emit (self.tick, long_short, t.count, gain)
                    market_count = market_count - t.count
            self.trade = tmp_trade

        """
        if count > 0:
            if not price in self.market:
                self.market[price] = {}
            if not long_short in self.market[price]:
                self.market[price][long_short] = SimpleNamespace(count = 0)
            self.market[price][long_short].count = self.market[price][long_short].count + count
            SignalFactor().sign_trade_order_market_ret.emit (price, long_short, self.market[price][long_short].count)
        else:
            if price in self.market and long_short in self.market[price]:
                if self.market[price][long_short].count > 0:
                    self.market[price][long_short].count = self.market[price][long_short].count + count
                    SignalFactor().sign_trade_order_market_ret.emit (price, long_short, self.market[price][long_short].count)
                    if self.market[price][long_short].count == 0:
                        del self.market[price][long_short]

        #"""
    
    def trade_order_limit_market (self, price, count, long_short):
        is_trade = False
        if count > 0:
            if long_short == True and price >= self.tick.Close:
                is_trade = True
            elif long_short == False and price <= self.tick.Close:
                is_trade = True

        if is_trade:
            if not self.trade or self.trade[-1].long_short == long_short:
                trade = SimpleNamespace()
                trade.price = self.tick.Close
                trade.long_short = long_short
                trade.count = count
                self.trade.append (trade)
                SignalFactor().sign_trade_deal.emit (self.tick, long_short, trade.count, 0)
            else:
                tmp_trade = []
                market_count = count
                for t in self.trade:
                    if market_count <= 0:
                        tmp_trade.append(t)
                        continue
                    if t.count > market_count:
                        if long_short:
                            gain = (t.price - self.tick.Close) * market_count
                        else:
                            gain = (self.tick.Close - t.price) * market_count
                        self.account.profit = self.account.profit + gain
                        SignalFactor().sign_trade_deal.emit (self.tick, long_short, market_count, gain)
                        self.account.fee = self.account.fee + market_count
                        t.count = t.count - market_count
                        market_count = 0
                        tmp_trade.append(t)
                    else:
                        if long_short:
                            gain = (t.price - self.tick.Close) * t.count
                        else:
                            gain = (self.tick.Close - t.price) * t.count
                        self.account.profit = self.account.profit + gain
                        self.account.fee = self.account.fee + t.count
                        SignalFactor().sign_trade_deal.emit (self.tick, long_short, t.count, gain)
                        market_count = market_count - t.count
                self.trade = tmp_trade
        else:
            if count > 0:
                if not price in self.market:
                    self.market[price] = {}
                if not long_short in self.market[price]:
                    self.market[price][long_short] = SimpleNamespace(count = 0)
                self.market[price][long_short].count = self.market[price][long_short].count + count
                SignalFactor().sign_trade_order_market_ret.emit (price, long_short, self.market[price][long_short].count)
            else:
                if price in self.market and long_short in self.market[price]:
                    if self.market[price][long_short].count > 0:
                        self.market[price][long_short].count = self.market[price][long_short].count + count
                        SignalFactor().sign_trade_order_market_ret.emit (price, long_short, self.market[price][long_short].count)
                        if self.market[price][long_short].count == 0:
                            del self.market[price][long_short]


    def trade_order_mit (self, price, count, long_short):
        if not price in self.mit:
            self.mit[price] = {}
        if not long_short in self.mit[price]:
            self.mit[price][long_short] = SimpleNamespace()
            self.mit[price][long_short].count = 0
        self.mit[price][long_short].count = count
        if count <= 0:
            del self.mit[price][long_short]

    def trade_exec (self):
        if not self.tick.Close in self.mit and not self.tick.Close in self.market:
            return

        market = None
        if self.tick.Close in self.market:
            market = self.market[self.tick.Close]
        else:
            self.market[self.tick.Close] = {}
            self.market[self.tick.Close][True] = SimpleNamespace(count = 0)
            self.market[self.tick.Close][False] = SimpleNamespace(count = 0)
            market = self.market[self.tick.Close]

        mit = None
        if self.tick.Close in self.mit:
            mit = self.mit[self.tick.Close]

        if mit:
            for long_short in [True, False]:
                if not long_short in mit:
                    continue
                if market is None or not long_short in market:
                    market[long_short] = SimpleNamespace(count = 0)
                market[long_short].count = market[long_short].count + mit[long_short].count
                SignalFactor().sign_trade_order_mit_ret.emit (self.tick.Close, long_short, 0)
            del self.mit[self.tick.Close]

        for long_short in [True, False]:
            if not long_short in market:
                continue
            if market[long_short].count <= 0:
                continue

            if not self.trade or self.trade[-1].long_short == long_short:
                trade = SimpleNamespace()
                trade.price = self.tick.Close
                trade.long_short = long_short
                trade.count = market[long_short].count
                self.trade.append (trade)
                
                del self.market[self.tick.Close][long_short]
                SignalFactor().sign_trade_order_market_ret.emit (self.tick.Close, long_short, 0)
                SignalFactor().sign_trade_order_mit_ret.emit (self.tick.Close, long_short, 0)
                SignalFactor().sign_trade_deal.emit (self.tick, long_short, trade.count, 0)
            else:
                tmp_trade = []
                for t in self.trade:
                    if market[long_short].count <= 0:
                        tmp_trade.append(t)
                        continue
                    if t.count > market[long_short].count:
                        if long_short:
                            gain = (t.price - self.tick.Close) * market[long_short].count
                        else:
                            gain = (self.tick.Close - t.price) * market[long_short].count
                        self.account.profit = self.account.profit + gain
                        SignalFactor().sign_trade_deal.emit (self.tick, long_short, market[long_short].count, gain)
                        self.account.fee = self.account.fee + market[long_short].count
                        t.count = t.count - market[long_short].count
                        market[long_short].count = 0
                        tmp_trade.append(t)
                    else:
                        if long_short:
                            gain = (t.price - self.tick.Close) * t.count
                        else:
                            gain = (self.tick.Close - t.price) * t.count
                        self.account.profit = self.account.profit + gain
                        self.account.fee = self.account.fee + t.count
                        SignalFactor().sign_trade_deal.emit (self.tick, long_short, t.count, gain)
                        market[long_short].count = market[long_short].count - t.count
                self.trade = tmp_trade

                SignalFactor().sign_trade_order_market_ret.emit (self.tick.Close, long_short, market[long_short].count)
                if market[long_short].count <= 0:
                    del self.market[self.tick.Close][long_short]

                if len(self.trade) <= 0 and SettingFactor().getFreePosFreeOrderEnable () == 'True':
                    self.trade_order_market_buy_clear ()
                    self.trade_order_market_sell_clear ()
                    self.trade_order_mit_buy_clear ()
                    self.trade_order_mit_sell_clear ()

    def trade_order_market_buy_clear (self):
        for price in self.market:
            if True in self.market[price]:
                del self.market[price][True]
                SignalFactor().sign_trade_order_market_ret.emit (price, True, 0)

    def trade_order_market_sell_clear (self):
        for price in self.market:
            if False in self.market[price]:
                del self.market[price][False]
                SignalFactor().sign_trade_order_market_ret.emit (price, False, 0)

    def trade_order_mit_buy_clear (self):
        for price in self.mit:
            if True in self.mit[price]:
                 del self.mit[price][True]
                 SignalFactor().sign_trade_order_mit_ret.emit (price, True, 0)

    def trade_order_mit_sell_clear (self):
        for price in self.mit:
            if False in self.mit[price]:
                 del self.mit[price][False]
                 SignalFactor().sign_trade_order_mit_ret.emit (price, False, 0)

    def trade_clear (self):
        gain = 0
        count = 0
        long_short = True
        for t in self.trade:
            if t.long_short:
                long_short = t.long_short
                gain = gain + (self.tick.Close - t.price) * t.count
                self.account.fee = self.account.fee + t.count
            else:
                long_short = t.long_short
                gain = gain + (t.price - self.tick.Close) * t.count
                self.account.fee = self.account.fee + t.count
            count = count + t.count

        if gain != 0:
            self.account.profit = self.account.profit + gain
        if count > 0:
            SignalFactor().sign_trade_deal.emit (self.tick, not long_short, count, gain)

        self.trade_order_mit_buy_clear()
        self.trade_order_mit_sell_clear()
        self.mit = {}
        self.marekt = {}
        self.trade = []






                    
