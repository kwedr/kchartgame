
from types import SimpleNamespace
import PySide2.QtCore as QtCore
import PySide2.QtCharts as QtCharts
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from signalFactor import SignalFactor
import re

def is_digit(str):
    return str.lstrip('-').replace('.', '').isdigit()

class PriceLadderWidget (QtWidgets.QWidget):
    df_max_volumn = 2000

    df_header_mit_buy = 0
    df_header_bid = 1
    df_header_price = 2
    df_header_ask = 3
    df_header_mit_sell = 4

    class BackgroundDelegate(QtWidgets.QStyledItemDelegate):
        def paint(self, painter, option, index):
            super(PriceLadderWidget.BackgroundDelegate, self).paint(painter, option, index)

            if option.state & QtWidgets.QStyle.State_Selected:
                painter.save()
                #painter.fillRect(option.rect, index.data(Qt.BackgroundRole))
                # Changed to Green
                pen = QtGui.QPen(QtCore.Qt.darkGreen, 2, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
                myrect = option.rect.adjusted(1, 1, 0, 0)
                painter.setPen(pen)
                painter.drawLine(myrect.topLeft(), myrect.topRight())
                painter.drawLine(option.rect.bottomRight() , option.rect.bottomLeft())
                painter.drawLine(myrect.topLeft(), myrect.bottomLeft())
                painter.drawLine(option.rect.topRight() + QtCore.QPoint(0, 2), option.rect.bottomRight() + QtCore.QPoint(0, -2))
                painter.restore()
                return
            
            background = index.data (QtCore.Qt.BackgroundRole)
            if background == QtWidgets.QStyle.State_UpArrow:
                painter.save()
                #painter.fillRect(option.rect, index.data(Qt.BackgroundRole))
                # Changed to Green
                pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
                myrect = option.rect.adjusted(1, 1, 0, 0)
                painter.setPen(pen)
                painter.drawLine(myrect.topLeft(), myrect.topRight())
                painter.drawLine(option.rect.bottomRight() , option.rect.bottomLeft())
                painter.drawLine(myrect.topLeft(), myrect.bottomLeft())
                painter.drawLine(option.rect.topRight() + QtCore.QPoint(0, 2), option.rect.bottomRight() + QtCore.QPoint(0, -2))
                painter.restore()
                return
            elif background == QtWidgets.QStyle.State_DownArrow:
                painter.save()
                #painter.fillRect(option.rect, index.data(Qt.BackgroundRole))
                # Changed to Green
                pen = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
                myrect = option.rect.adjusted(1, 1, 0, 0)
                painter.setPen(pen)
                painter.drawLine(myrect.topLeft(), myrect.topRight())
                painter.drawLine(option.rect.bottomRight() , option.rect.bottomLeft())
                painter.drawLine(myrect.topLeft(), myrect.bottomLeft())
                painter.drawLine(option.rect.topRight() + QtCore.QPoint(0, 2), option.rect.bottomRight() + QtCore.QPoint(0, -2))
                painter.restore()
                return

    class PLTableWidget (QtWidgets.QTableWidget):
        rightClicked = QtCore.Signal(object)
        leftClicked = QtCore.Signal(object)

        def mousePressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.leftClicked.emit (event)
            elif event.button() == QtCore.Qt.RightButton:
                self.rightClicked.emit (event)

    def __init__ (self, parent = None):
        super().__init__(parent)

        self.init_price = False
        self.run_mit_item_list = {}
        self.run_best_bid_item_list = {}
        self.run_best_ask_item_list = {}
        self.run_position = 1
        self.run_better_size = 0
        self.options = SimpleNamespace(keep_center = True)
        self.params = SimpleNamespace(position = 0, average = 0, profit = 0, mit_buy_count = 0, mit_sell_count = 0)
        self.params.trade = []

        self.topwidget = QtWidgets.QWidget (self)
        self.top_radio_keep_center = QtWidgets.QCheckBox ("報價置中")
        self.top_radio_keep_center.setChecked(True)
        self.top_radio_keep_center.stateChanged.connect(self.change_keep_center)

        spingroup = QtWidgets.QHBoxLayout()
        self.top_label_position = QtWidgets.QLabel("口數:")
        self.top_spin_position = QtWidgets.QSpinBox ()
        self.top_spin_position.setMinimum (1)
        self.top_spin_position.setMaximumSize(100, 100)
        self.top_spin_position.valueChanged.connect(self.change_run_position)
        spingroup.addWidget (self.top_label_position)
        spingroup.addWidget (self.top_spin_position)

        hlay = QtWidgets.QHBoxLayout()
        hlay.addLayout (spingroup)
        hlay.addWidget (self.top_radio_keep_center)

        vlay = QtWidgets.QVBoxLayout(self.topwidget)
        vlay.addLayout(hlay)

        hlay = QtWidgets.QHBoxLayout()
        self.top_label_position = QtWidgets.QLabel ("庫存: 0", self)
        self.top_label_average = QtWidgets.QLabel ("均價: 0", self)
        self.top_label_floating_profit = QtWidgets.QLabel ("浮動損益: 0", self)
        self.top_label_net_profit = QtWidgets.QLabel ("淨損益: 0", self)
        for w in (self.top_label_position, self.top_label_average, self.top_label_floating_profit, self.top_label_net_profit):
            hlay.addWidget(w)
        vlay.addLayout (hlay)

        self.bottom_btn_buy = QtWidgets.QPushButton ("市價買進", self.topwidget)
        self.bottom_btn_buy.clicked.connect (self.btn_buy)
        self.bottom_btn_sell = QtWidgets.QPushButton ("市價賣出", self.topwidget)
        self.bottom_btn_sell.clicked.connect (self.btn_sell)
        self.bottom_btn_market_buy_clear = QtWidgets.QPushButton ("買單全清", self.topwidget)
        self.bottom_btn_market_buy_clear.clicked.connect (self.btn_market_buy_clear)
        self.bottom_btn_market_sell_clear = QtWidgets.QPushButton ("賣單全清", self.topwidget)
        self.bottom_btn_market_sell_clear.clicked.connect (self.btn_market_sell_clear)        
        self.bottom_btn_mit_buy_clear = QtWidgets.QPushButton ("觸買全清", self.topwidget)
        self.bottom_btn_mit_buy_clear.clicked.connect (self.btn_mit_buy_clear)
        self.bottom_btn_mit_sell_clear = QtWidgets.QPushButton ("觸賣全清", self.topwidget)
        self.bottom_btn_mit_sell_clear.clicked.connect (self.btn_mit_sell_clear)
        self.bottom_btn_trade_clear = QtWidgets.QPushButton ("全部清倉", self.topwidget)
        self.bottom_btn_trade_clear.clicked.connect (self.btn_trade_clear)
        
        vlay = QtWidgets.QVBoxLayout()
        hlay = QtWidgets.QHBoxLayout()
        for w in (self.bottom_btn_buy, self.bottom_btn_sell):
            hlay.addWidget(w)
        vlay.addLayout (hlay)

        hlay = QtWidgets.QHBoxLayout()
        for w in (self.bottom_btn_mit_buy_clear, self.bottom_btn_market_buy_clear, self.bottom_btn_trade_clear, self.bottom_btn_market_sell_clear, self.bottom_btn_mit_sell_clear):
            hlay.addWidget(w)
        vlay.addLayout (hlay)

        self.tablewidget = PriceLadderWidget.PLTableWidget(self.df_max_volumn, 5, self)
        header = ["觸買:0", "委買", "價格", "委賣", "觸賣:0"]
        self.tablewidget.setHorizontalHeaderLabels(header)
        self.tablewidget.setStyleSheet("::section { background-color: #646464; padding: 4px; border: 1px solid #fffff8; color: #D3D3D3; }")
        self.tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tablewidget.verticalHeader().hide()
        self.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tablewidget.setItemDelegate(self.BackgroundDelegate())
        self.tablewidget.rightClicked.connect (self.rightClicked)
        self.tablewidget.leftClicked.connect (self.leftClicked)
        self.tableheader_bid = self.tablewidget.horizontalHeaderItem(self.df_header_bid)
        self.tableheader_ask = self.tablewidget.horizontalHeaderItem(self.df_header_ask)
        self.tableheader_mit_buy = self.tablewidget.horizontalHeaderItem(self.df_header_mit_buy)
        self.tableheader_mit_sell = self.tablewidget.horizontalHeaderItem(self.df_header_mit_sell)
        self.tablewidgetitem = []
        for i in range(5):
            self.tablewidgetitem.append([])
            for j in range (self.df_max_volumn):
                #text = "{}.{}".format (i, j)
                text = ""
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tablewidget.setItem(j, i, item)
                item = self.tablewidget.item(j, i)
                self.tablewidgetitem[i].append (item)
        
        lay = QtWidgets.QVBoxLayout(self)
        for w in (self.topwidget, self.tablewidget):
            lay.addWidget(w)
        lay.addLayout(vlay)
        
        item = self.tablewidgetitem[2][0]
        self.tablewidget.scrollToItem (item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.shortcuts ()

        SignalFactor ().sign_run_init.connect (self.run_init)
        SignalFactor().sign_tick_update.connect (self.tick_update)
        SignalFactor().sign_trade_order_market_ret.connect (self.trade_order_market_ret)
        SignalFactor().sign_trade_order_mit_ret.connect (self.trade_order_mit_ret)
        SignalFactor().sign_trade_deal.connect (self.trade_deal)
        SignalFactor().sign_best_bid_update.connect (self.best_bid_update)
        SignalFactor().sign_best_ask_update.connect (self.best_ask_update)

    def shortcuts (self):
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        shortcut.activated.connect(self.action_buy) 
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_D), self)
        shortcut.activated.connect(self.action_sell)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W), self)
        shortcut.activated.connect(self.better_price_size_add)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S), self)
        shortcut.activated.connect(self.better_price_size_dec)
        
    def action_buy (self):
        price = self.tick.Close + self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, True)

    def action_sell (self):
        price = self.tick.Close - self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, False)

    def run_init (self, value):
        for row in self.run_mit_item_list:
            for column in self.run_mit_item_list[row]:
                if not self.run_mit_item_list[row][column] is None:
                    if not self.run_mit_item_list[row][column].item is None:
                        self.run_mit_item_list[row][column].item.setText ("")

        for row in self.run_best_bid_item_list:
            for column in self.run_best_bid_item_list[row]:
                if not self.run_best_bid_item_list[row][column] is None:
                    if not self.run_best_bid_item_list[row][column].item is None:
                        self.run_best_bid_item_list[row][column].item.setText ("")

        for row in self.run_best_ask_item_list:
            for column in self.run_best_ask_item_list[row]:
                if not self.run_best_ask_item_list[row][column] is None:
                    if not self.run_best_ask_item_list[row][column].item is None:
                        self.run_best_ask_item_list[row][column].item.setText ("")
                        
        self.init_price = False
        self.run_position = 1
        self.run_high_price = 0
        self.run_curr_item = None
        self.run_better_up_item = None
        self.run_better_dn_item = None
        self.run_mit_item_list = {}
        self.run_best_bid_item_list = {}
        self.run_best_ask_item_list = {}
        self.params = SimpleNamespace(position = 0, average = 0, profit = 0, mit_buy_count = 0, mit_sell_count = 0)
        self.params.trade = []
        self.top_spin_position.setValue(self.run_position)
        self.update_mit_header ()
        self.top_label_position.setText("庫存: {}".format (0))
        self.top_label_average.setText("均價: {:.02f}".format (0))
        self.top_label_net_profit.setText("淨損益: {:.02f}".format (0))
        self.top_label_floating_profit.setText("浮動損益: {:.02f}".format (0))

    def tick_update (self, tick):
        self.setUpdatesEnabled(False)

        if self.init_price == False:
            self.init_price = True
            #center_price = tick.Close
            self.run_high_price = tick.Close + int(self.df_max_volumn / 2)
            for i in range (self.df_max_volumn):
                scrollitem =  self.tablewidgetitem[2][i]
                scrollitem.setText (str(self.run_high_price - i))

        if self.run_curr_item:
            self.run_curr_item.setSelected (False)
            self.run_curr_item = None

        if self.run_better_up_item:
            self.run_better_up_item.setData (QtCore.Qt.BackgroundRole, None)
            self.run_better_up_item = None

        if self.run_better_dn_item:
            self.run_better_dn_item.setData (QtCore.Qt.BackgroundRole, None)
            self.run_better_dn_item = None

        
        index = self.run_high_price - tick.Close
        try:
            self.run_curr_item = self.tablewidgetitem[2][int(index)]
        except:
            return
        self.tick = tick
        self.run_curr_item.setSelected (True)

        if self.run_better_size != 0 :
            self.run_better_up_item = self.tablewidgetitem[2][int(index) - self.run_better_size]
            self.run_better_up_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_UpArrow)
            self.run_better_dn_item = self.tablewidgetitem[2][int(index) + self.run_better_size]
            self.run_better_dn_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_DownArrow)

        if self.options.keep_center:
            self.tablewidget.scrollToItem (self.run_curr_item, QtWidgets.QAbstractItemView.PositionAtCenter)

        self.update_float_profit ()

        self.setUpdatesEnabled(True)

    def get_mit_item (self, price, long_short):
        row = int(self.run_high_price - price)
        column = PriceLadderWidget.df_header_mit_buy
        if long_short == False:
            column = PriceLadderWidget.df_header_mit_sell

        if not row in self.run_mit_item_list:
            self.run_mit_item_list[row] = {}

        if not column in self.run_mit_item_list[row]:
            self.run_mit_item_list[row][column] = {}
        
        if not self.run_mit_item_list[row][column] or self.run_mit_item_list[row][column] is None:
            self.run_mit_item_list[row][column] = SimpleNamespace () 
            self.run_mit_item_list[row][column].item = self.tablewidget.item (row, column)

        return self.run_mit_item_list[row][column].item, row, column

    def get_bid_item (self, price):
        row = int(self.run_high_price - price)
        if row < 0:
            return None
        column = PriceLadderWidget.df_header_bid
        if not row in self.run_best_bid_item_list:
            self.run_best_bid_item_list[row] = {}

        if not column in self.run_best_bid_item_list[row]:
            self.run_best_bid_item_list[row][column] = {}
        
        if not self.run_best_bid_item_list[row][column] or self.run_best_bid_item_list[row][column] is None:
            self.run_best_bid_item_list[row][column] = SimpleNamespace (item = None, best = 0, market = 0) 
            self.run_best_bid_item_list[row][column].item = self.tablewidget.item (row, column)

        return self.run_best_bid_item_list[row][column]

    def get_ask_item (self, price):
        row = int(self.run_high_price - price)
        if row < 0:
            return None
        column = PriceLadderWidget.df_header_ask
        if not row in self.run_best_ask_item_list:
            self.run_best_ask_item_list[row] = {}

        if not column in self.run_best_ask_item_list[row]:
            self.run_best_ask_item_list[row][column] = {}
        
        if not self.run_best_ask_item_list[row][column] or self.run_best_ask_item_list[row][column] is None:
            self.run_best_ask_item_list[row][column] = SimpleNamespace (item = None, best = 0, market = 0) 
            self.run_best_ask_item_list[row][column].item = self.tablewidget.item (row, column)

        return self.run_best_ask_item_list[row][column]

    @QtCore.Slot(object)
    def rightClicked (self, e):
        pos = e.pos ()
        item = self.tablewidget.itemAt (pos)
        if item is None:
            return
        row = item.row ()
        column = item.column() 
        if column != PriceLadderWidget.df_header_mit_buy and column != PriceLadderWidget.df_header_mit_sell:
            return

        price_tiem = self.tablewidget.item (row, PriceLadderWidget.df_header_price)
        if is_digit(price_tiem.text ()) == False:
            return

        value = 0
        if str.isdigit(item.text ()):
            value = int(item.text ())
        value = value - 1
        if (value <= 0):
            value = 0
            item.setText ("")
        else:
            item.setText (str(value))
        price = float (price_tiem.text ())
        if not row in self.run_mit_item_list:
            self.run_mit_item_list[row] = {}
        if not column in self.run_mit_item_list[row]:
            self.run_mit_item_list[row][column] = SimpleNamespace () 
            self.run_mit_item_list[row][column].item = item
        if value <= 0:
            del self.run_mit_item_list[row][column]
        SignalFactor().sign_trade_order_mit.emit (price, value, column == PriceLadderWidget.df_header_mit_buy)
        self.update_mit_header ()

    @QtCore.Slot(object)
    def leftClicked (self, e):
        pos = e.pos ()
        item = self.tablewidget.itemAt (pos)
        if item is None:
            return
        row = item.row ()
        column = item.column() 
        if column != PriceLadderWidget.df_header_mit_buy and column != PriceLadderWidget.df_header_mit_sell:
            return

        price_tiem = self.tablewidget.item (row, PriceLadderWidget.df_header_price)
        if is_digit(price_tiem.text ()) == False:
            return
            
        value = 0
        if str.isdigit(item.text ()):
            value = int(item.text ())

        value = value + 1
        item.setText (str(value))
        price = float (price_tiem.text ())

        if not row in self.run_mit_item_list:
            self.run_mit_item_list[row] = {}
        if not column in self.run_mit_item_list[row]:
            self.run_mit_item_list[row][column] = SimpleNamespace () 
            self.run_mit_item_list[row][column].item = item

        SignalFactor().sign_trade_order_mit.emit (price, value, column == PriceLadderWidget.df_header_mit_buy)
        self.update_mit_header ()

    def update_order_header (self):
        bid = 0
        for row in self.run_best_bid_item_list:
            for column in self.run_best_bid_item_list[row]:
                if not self.run_best_bid_item_list[row][column] is None:
                    if not self.run_best_bid_item_list[row][column].item is None:
                        bid = bid + self.run_best_bid_item_list[row][column].market

        ask = 0
        for row in self.run_best_ask_item_list:
            for column in self.run_best_ask_item_list[row]:
                if not self.run_best_ask_item_list[row][column] is None:
                    if not self.run_best_ask_item_list[row][column].item is None:
                        ask = ask + self.run_best_ask_item_list[row][column].market

        bid_str = "委買:{}".format (bid) if bid > 0 else "委買"
        self.tableheader_bid.setText (bid_str)
        ask_str = "委賣:{}".format (ask) if ask > 0 else "委賣"
        self.tableheader_ask.setText (ask_str)

    def update_mit_header (self):
        buy_count = 0
        sell_count = 0
        for row in self.run_mit_item_list:
            if self.df_header_mit_buy in self.run_mit_item_list[row]:
                data = self.run_mit_item_list[row][self.df_header_mit_buy]
                if not data is None:
                    buy_count = buy_count + int(data.item.text ())
            if self.df_header_mit_sell in self.run_mit_item_list[row]:
                data = self.run_mit_item_list[row][self.df_header_mit_sell]
                if not data is None:
                    sell_count = sell_count + int(data.item.text ())

        self.tableheader_mit_buy.setText ("觸買:{}".format (buy_count))
        self.tableheader_mit_sell.setText ("觸賣:{}".format (sell_count))

    def trade_order_market_ret(self, price, long_short, count):
        item = None
        if long_short:
            item = self.get_bid_item (price)
        else:
            item = self.get_ask_item (price)

        item.market = count
        self.update_best_item_text (item)
        self.update_order_header ()

    def trade_order_mit_ret (self, price, long_short, count):
        item, row , column = self.get_mit_item (price, long_short)
        if not item is None:
            if count > 0:
                item.setText (str(count))
            else:
                item.setText ("")
                self.run_mit_item_list[row][column] = None
        self.update_mit_header ()

    def trade_deal (self, tick, long_short, count, gain):
        self.setUpdatesEnabled(False)

        position = count if long_short else -count
        self.params.position = self.params.position + position
        self.params.profit = self.params.profit + gain

        if self.params.position != 0:
            trade = SimpleNamespace(price = tick.Close, count = count, long_short = long_short)
            if self.params.trade:
                if self.params.trade[0].long_short != trade.long_short:
                    trade_list = []
                    for t in self.params.trade:
                        if trade.count <= 0:
                            trade_list.append (t)
                            continue
                        if t.count > trade.count:
                            t.count = t.count - trade.count
                            trade.count = 0
                            trade_list.append (t)
                        elif t.count < trade.count:
                            trade.count = trade.count - t.count
                        elif t.count == trade.count:
                            trade.count = 0
                    if trade.count > 0:
                        trade_list.append (trade)
                    self.params.trade = trade_list
                else:
                    self.params.trade.append (trade)
                price_list = []
                for t in self.params.trade:
                    price_list = price_list + [t.price] * t.count
                self.params.average = sum(price_list) / len(price_list)
            else:
                self.params.trade.append (trade)
                self.params.average = trade.price
        else:
            self.params.trade.clear ()
            self.params.average = 0
        
        self.top_label_position.setText("庫存: {}".format (self.params.position))
        self.top_label_average.setText("均價: {:.02f}".format (self.params.average))
        self.top_label_net_profit.setText("淨損益: {:.02f}".format (self.params.profit))
        self.update_float_profit ()
        self.setUpdatesEnabled(True)

    def change_keep_center (self):
        enable = self.top_radio_keep_center.checkState() == QtCore.Qt.Checked
        self.options.keep_center = enable

    def btn_market_buy_clear (self):
        SignalFactor().sign_trade_order_market_buy_clear.emit ()

    def btn_market_sell_clear (self):
        SignalFactor().sign_trade_order_market_sell_clear.emit ()

    def btn_mit_buy_clear (self):
        SignalFactor().sign_trade_order_mit_buy_clear.emit ()

    def btn_mit_sell_clear (self):
        SignalFactor().sign_trade_order_mit_sell_clear.emit ()

    def btn_trade_clear (self):
        SignalFactor().sign_trade_clear.emit ()

    def update_float_profit (self):
        floating_profit = 0
        for t in self.params.trade:
            if t.long_short:
                floating_profit = floating_profit + (self.tick.Close - t.price) * t.count
            else:
                floating_profit = floating_profit + (t.price - self.tick.Close) * t.count
        self.top_label_floating_profit.setText("浮動損益: {:.02f}".format (floating_profit))

    def change_run_position (self):
        self.run_position = self.top_spin_position.value ()

    def btn_buy (self):
        price = self.tick.Close + self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, True)

    def btn_sell (self):
        price = self.tick.Close - self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, False)

    def update_best_item_text (self, item):
        if item.item is None:
            return
        if item.best > 0 and item.market > 0:
            item.item.setText (str(item.best) + "(" + str(item.market) + ")")
        elif item.best > 0:
            item.item.setText (str(item.best))
        elif item.market > 0:
            item.item.setText ("(" + str(item.market) + ")")
        else:
            item.item.setText ("")

    def best_bid_update (self, value):
        for row in self.run_best_bid_item_list:
            for column in self.run_best_bid_item_list[row]:
                if not self.run_best_bid_item_list[row][column] is None:
                    if not self.run_best_bid_item_list[row][column].item is None:
                        self.run_best_bid_item_list[row][column].best = 0
                        self.update_best_item_text (self.run_best_bid_item_list[row][column])

        cnt = len (value)
        idx = 0
        while idx < cnt:
            bid = self.get_bid_item (float(value[idx]))
            if bid is None:
                return
            count = re.match ('[+-]?([0-9]*[.])?[0-9]+', value[idx+1]).group ()
            bid.best = int(float(count))
            self.update_best_item_text (bid)
            idx = idx + 2

    def best_ask_update (self, value):
        for row in self.run_best_ask_item_list:
            for column in self.run_best_ask_item_list[row]:
                if not self.run_best_ask_item_list[row][column] is None:
                    if not self.run_best_ask_item_list[row][column].item is None:
                        self.run_best_ask_item_list[row][column].best = 0
                        self.update_best_item_text (self.run_best_ask_item_list[row][column])

        cnt = len (value)
        idx = 0
        while idx < cnt:
            ask = self.get_ask_item (float(value[idx]))
            if ask is None:
                return
            count = re.match ('[+-]?([0-9]*[.])?[0-9]+', value[idx+1]).group ()
            ask.best = int(float(count))
            self.update_best_item_text (ask)
            idx = idx + 2
        
    def better_price_size_add (self):
        self.run_better_size = self.run_better_size + 1

    def better_price_size_dec (self):
        self.run_better_size = self.run_better_size - 1