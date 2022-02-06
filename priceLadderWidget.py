
from types import SimpleNamespace
import PySide2.QtCore as QtCore
import PySide2.QtCharts as QtCharts
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from signalFactor import SignalFactor
import re, time
from settingFactor import SettingFactor

def is_digit(str):
    return str.lstrip('-').replace('.', '').isdigit()

class PriceLadderWidget (QtWidgets.QWidget):
    df_max_volumn = 500

    df_header_mit_buy = 0
    df_header_bid = 1
    df_header_price = 2
    df_header_ask = 3
    df_header_mit_sell = 4
    de_header_max = 5

    class BackgroundDelegate(QtWidgets.QStyledItemDelegate):
        def paint(self, painter, option, index):
            super(PriceLadderWidget.BackgroundDelegate, self).paint(painter, option, index)

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
            elif background == QtWidgets.QStyle.State_MouseOver:
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

            foreground = index.data (QtCore.Qt.ForegroundRole)
            if foreground == QtWidgets.QStyle.State_Active:
                painter.save()
                #painter.fillRect(option.rect, index.data(Qt.BackgroundRole))
                # Changed to Green
                pen = QtGui.QPen(QtCore.Qt.magenta, 3, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
                myrect = option.rect.adjusted(1, 1, 0, 0)
                painter.setPen(pen)
                painter.drawLine(option.rect.bottomRight() , option.rect.bottomLeft())
                painter.restore()
            elif foreground == QtWidgets.QStyle.State_MouseOver:
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

    class PLTableWidget (QtWidgets.QTableWidget):
        rightClicked = QtCore.Signal(object)
        leftClicked = QtCore.Signal(object)
        mouseOver = QtCore.Signal(object)
        mouseWheel = QtCore.Signal(object)
        resizeChange = QtCore.Signal(object)

        def mouseMoveEvent (self, event):
            self.mouseOver.emit (event)

        def mousePressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.leftClicked.emit (event)
            elif event.button() == QtCore.Qt.RightButton:
                self.rightClicked.emit (event)

        def wheelEvent (self, event):
            self.mouseWheel.emit (event)

        def resizeEvent(self, event):
            self.resizeChange.emit (event)
            super().resizeEvent(event)

    def __init__ (self, parent = None):
        super().__init__(parent)

        self.init_price = False
        self.run_mit_item_list = {}
        self.run_mit_list = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_buy] = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_sell] = {}
        self.run_best_bid_item_list = {}
        self.run_best_ask_item_list = {}
        self.run_position = 1
        self.run_market_list = {}
        self.run_market_list[PriceLadderWidget.df_header_bid] = {}
        self.run_market_list[PriceLadderWidget.df_header_ask] = {}
        self.run_market_item_list = {}
        self.run_the_fifth_order_list = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid] = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask] = {}
        self.run_mouse_over_item = None
        self.run_stop_loss = int (SettingFactor().getRunStopLoss())
        self.options = SimpleNamespace(keep_center = True, mouse_wheel = False, mouse_wheel_time = 0)
        self.params = SimpleNamespace(position = 0, average = 0, profit = 0, mit_buy_count = 0, mit_sell_count = 0)
        self.params.trade = []

        self.topwidget = QtWidgets.QWidget (self)
        self.top_radio_keep_center = QtWidgets.QCheckBox ("報價置中")
        self.top_radio_keep_center.setChecked(True)
        self.top_radio_keep_center.stateChanged.connect(self.change_keep_center)

        self.top_radio_free_pos_free_order = QtWidgets.QCheckBox ("空手清單")
        self.top_radio_free_pos_free_order.setChecked(True)
        self.top_radio_free_pos_free_order.stateChanged.connect(self.change_free_pos_free_order)

        spingroup = QtWidgets.QHBoxLayout()
        self.top_label_position = QtWidgets.QLabel("口數:")
        self.top_spin_position = QtWidgets.QSpinBox ()
        self.top_spin_position.setMinimum (1)
        self.top_spin_position.setMaximumSize(100, 100)
        self.top_spin_position.valueChanged.connect(self.change_run_position)
        spingroup.addWidget (self.top_label_position)
        spingroup.addWidget (self.top_spin_position)

        stoplossgroup = QtWidgets.QHBoxLayout()
        self.top_label_stop_loss = QtWidgets.QLabel("自動停損:")
        self.top_spin_stop_loss = QtWidgets.QSpinBox ()
        self.top_spin_stop_loss.setMinimum (0)
        self.top_spin_stop_loss.setValue(self.run_stop_loss)
        self.top_spin_stop_loss.setMaximumSize(100, 100)
        self.top_spin_stop_loss.valueChanged.connect(self.change_stop_loss)
        stoplossgroup.addWidget (self.top_label_stop_loss)
        stoplossgroup.addWidget (self.top_spin_stop_loss)

        hlay = QtWidgets.QHBoxLayout()
        hlay.addLayout (spingroup)
        hlay.addWidget (self.top_radio_keep_center)
        hlay.addWidget (self.top_radio_free_pos_free_order)
        hlay.addLayout (stoplossgroup)

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
        self.tablewidget.verticalScrollBar().setDisabled(True)
        self.tablewidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);
        self.tablewidget.setMouseTracking(True)
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
        self.tablewidget.mouseOver.connect (self.mouseOver)
        self.tablewidget.mouseWheel.connect (self.mouseWheel)
        self.tablewidget.resizeChange.connect (self.resizeChange)
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
        self.itemShowCount = 0
        self.itemShowCountDiv2 = 0
        self.run_curr_item = None
        self.shortcuts ()

        SignalFactor().sign_run_init.connect (self.run_init)
        SignalFactor().sign_tick_update.connect (self.tick_update)
        SignalFactor().sign_trade_order_market_ret.connect (self.trade_order_market_ret)
        SignalFactor().sign_trade_order_mit_ret.connect (self.trade_order_mit_ret)
        SignalFactor().sign_trade_deal.connect (self.trade_deal)
        SignalFactor().sign_best_bid_update.connect (self.best_bid_update)
        SignalFactor().sign_best_ask_update.connect (self.best_ask_update)
        SignalFactor().sign_reconnect.connect  (self.reconnect)
        SignalFactor().sign_get_account.connect  (self.get_account)
        SignalFactor().sign_get_account_done.connect  (self.get_account_done)
        SignalFactor().sign_reconnect_trade_order_deal.connect (self.trade_deal)

    def shortcuts (self):
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self)
        shortcut.activated.connect(self.btn_trade_clear)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        shortcut.activated.connect(self.action_buy) 
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_D), self)
        shortcut.activated.connect(self.action_sell)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W), self)
        shortcut.activated.connect(self.better_price_size_add)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S), self)
        shortcut.activated.connect(self.better_price_size_dec)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_C), self)
        shortcut.activated.connect(self.inverse_keep_center)

    def action_buy (self):
        price = self.tick.Close + self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, True)

    def action_sell (self):
        price = self.tick.Close - self.run_better_size
        SignalFactor().sign_trade_order_market.emit (price, self.run_position, False)

    def run_init (self, value):
        self.tick = None
        for item in self.run_mit_item_list:
            item.setText ("")

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

        for row in self.tablewidgetitem:
            for item in row:
                item.setData (QtCore.Qt.ForegroundRole, None)
                item.setData (QtCore.Qt.BackgroundRole, None)
                        
        self.init_price = False
        self.run_position = 1
        self.run_high_price = 0
        self.run_price_row = 0
        self.run_average_item = None
        self.run_better_size = 0
        self.run_better_up_item = None        
        self.run_better_dn_item = None
        self.run_mouse_over_item = None
        self.run_get_account_done = True
        self.run_mit_item_list = {}
        self.run_mit_list = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_buy] = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_sell] = {}
        self.run_market_list = {}
        self.run_market_list[PriceLadderWidget.df_header_bid] = {}
        self.run_market_list[PriceLadderWidget.df_header_ask] = {}
        self.run_market_item_list = {}
        self.run_the_fifth_order_list = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid] = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask] = {}
        self.run_marekt_list = {}
        self.params = SimpleNamespace(position = 0, average = 0, profit = 0, mit_buy_count = 0, mit_sell_count = 0)
        self.params.trade = []
        self.top_spin_position.setValue(self.run_position)
        self.update_mit_header ()
        self.top_label_position.setText("庫存: {}".format (0))
        self.top_label_average.setText("均價: {:.02f}".format (0))
        self.top_label_net_profit.setText("淨損益: {:.02f}".format (0))
        self.top_label_floating_profit.setText("浮動損益: {:.02f}".format (0))
        self.update_curr_item ()

    def tick_update (self, tick):
        self.setUpdatesEnabled(False)
        self.tick = tick
        is_center = self.is_keep_center ()
        if self.init_price == False:
            self.init_price = True
            is_center = True
        self.update_tablewidget_item (is_center)
        self.update_float_profit ()

        self.setUpdatesEnabled(True)

    @QtCore.Slot(object)
    def rightClicked (self, e):
        pos = e.pos ()
        item = self.tablewidget.itemAt (pos)
        if item is None:
            return
        row = item.row ()
        column = item.column() 

        header = [
            PriceLadderWidget.df_header_bid,
            PriceLadderWidget.df_header_ask,
            PriceLadderWidget.df_header_mit_buy,
            PriceLadderWidget.df_header_mit_sell
        ]

        if not column in header:
            return

        price_tiem = self.tablewidget.item (row, PriceLadderWidget.df_header_price)
        if is_digit(price_tiem.text ()) == False:
            return
        price = float (price_tiem.text ())

        if column == PriceLadderWidget.df_header_bid or column == PriceLadderWidget.df_header_ask:
            SignalFactor().sign_trade_order_limit_market.emit (price, -self.run_position, column == PriceLadderWidget.df_header_bid)

        elif column == PriceLadderWidget.df_header_mit_buy or column == PriceLadderWidget.df_header_mit_sell:
            if not price in self.run_mit_list[column]:
                self.run_mit_list[column][price] = 0
                return

            value = self.run_mit_list[column][price] = self.run_mit_list[column][price] - self.run_position
            if self.run_mit_list[column][price] < 0:
                self.run_mit_list[column][price] = 0
                value = 0

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
        header = [
            PriceLadderWidget.df_header_bid,
            PriceLadderWidget.df_header_ask,
            PriceLadderWidget.df_header_mit_buy,
            PriceLadderWidget.df_header_mit_sell
        ]
        if not column in header:
            return

        price_tiem = self.tablewidget.item (row, PriceLadderWidget.df_header_price)
        if is_digit(price_tiem.text ()) == False:
            return

        price = float (price_tiem.text ())

        if column == PriceLadderWidget.df_header_bid or column == PriceLadderWidget.df_header_ask:
            SignalFactor().sign_trade_order_limit_market.emit (price, self.run_position, column == PriceLadderWidget.df_header_bid)
        
        elif column == PriceLadderWidget.df_header_mit_buy or column == PriceLadderWidget.df_header_mit_sell:
            if not price in self.run_mit_list[column]:
                self.run_mit_list[column][price] = 0
            value = self.run_mit_list[column][price] = self.run_mit_list[column][price] + self.run_position
            
            SignalFactor().sign_trade_order_mit.emit (price, value, column == PriceLadderWidget.df_header_mit_buy)
            self.update_mit_header ()

    def mouseOver (self, e):
        pos = e.pos ()
        item = self.tablewidget.itemAt (pos)
        if item is None:
            return
        row = item.row ()
        column = item.column() 
        header = [
            PriceLadderWidget.df_header_bid,
            PriceLadderWidget.df_header_ask,
            PriceLadderWidget.df_header_mit_buy,
            PriceLadderWidget.df_header_mit_sell
        ]
        if not column in header:
            return
        if not self.run_mouse_over_item is None:
            self.run_mouse_over_item.setData (QtCore.Qt.ForegroundRole, None)
        self.run_mouse_over_item = item
        self.run_mouse_over_item.setData (QtCore.Qt.ForegroundRole, QtWidgets.QStyle.State_MouseOver)

    def mouseWheel (self, e):
        if not self.init_price:
            return

        self.options.mouse_wheel = True
        self.options.mouse_wheel_time = time.time()

        y = e.angleDelta().y()
        self.run_high_price = self.run_high_price + (1 if y > 0 else -1)
        self.update_tablewidget_item (False, True)

    def update_order_header (self):
        bid_count = 0
        ask_count = 0
        for price in self.run_market_list[self.df_header_bid]:
            bid_count = bid_count + self.run_market_list[self.df_header_bid][price]

        for price in self.run_market_list[self.df_header_ask]:
            ask_count = ask_count + self.run_market_list[self.df_header_ask][price]

        bid_str = "委買:{}".format (bid_count) if bid_count > 0 else "委買"
        self.tableheader_bid.setText (bid_str)
        ask_str = "委賣:{}".format (ask_count) if ask_count > 0 else "委賣"
        self.tableheader_ask.setText (ask_str)

    def update_mit_header (self):
        buy_count = 0
        sell_count = 0
        for price in self.run_mit_list[self.df_header_mit_buy]:
            buy_count = buy_count + self.run_mit_list[self.df_header_mit_buy][price]

        for price in self.run_mit_list[self.df_header_mit_sell]:
            sell_count = sell_count + self.run_mit_list[self.df_header_mit_sell][price]

        buy_str = "觸買:{}".format (buy_count) if buy_count > 0 else "委買"
        self.tableheader_mit_buy.setText (buy_str)
        sell_str = "觸賣:{}".format (sell_count) if sell_count > 0 else "委賣"
        self.tableheader_mit_sell.setText (sell_str)

    def trade_order_market_ret(self, price, long_short, count):
        column = PriceLadderWidget.df_header_bid if long_short else PriceLadderWidget.df_header_ask
        if not price in self.run_market_list[column]:
            self.run_market_list[column][price] = 0
        self.run_market_list[column][price] = count
        self.update_order_header ()

    def trade_order_mit_ret (self, price, long_short, count):
        column = PriceLadderWidget.df_header_mit_buy if long_short else PriceLadderWidget.df_header_mit_sell
        if not price in self.run_mit_list[column]:
            self.run_mit_list[column][price] = 0
        self.run_mit_list[column][price] = count
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

        if gain == 0 and self.run_stop_loss > 0 and self.run_get_account_done:
            not_long_short = not long_short
            column = self.df_header_mit_buy if not_long_short else self.df_header_mit_sell
            price = tick.Close - self.run_stop_loss if long_short else tick.Close + self.run_stop_loss
            if not price in self.run_mit_list[column]:
                self.run_mit_list[column][price] = 0
            value = self.run_mit_list[column][price] = self.run_mit_list[column][price] + count
            SignalFactor().sign_trade_order_mit.emit (price, value, not_long_short)
            self.update_mit_header ()

        self.top_label_position.setText("庫存: {}".format (self.params.position))
        self.top_label_average.setText("均價: {:.02f}".format (self.params.average))
        self.top_label_net_profit.setText("淨損益: {:.02f}".format (self.params.profit))
        self.update_float_profit ()
        self.setUpdatesEnabled(True)

    def inverse_keep_center (self):
        enable = self.top_radio_keep_center.checkState() == QtCore.Qt.Checked
        self.top_radio_keep_center.setChecked (not enable)

    def change_keep_center (self):
        enable = self.top_radio_keep_center.checkState() == QtCore.Qt.Checked
        self.options.keep_center = enable
        if self.options.keep_center:
            self.options.mouse_wheel = False
            self.update_curr_item ()
            self.update_better_price_size ()

    def change_free_pos_free_order (self):
        enable = self.top_radio_free_and_skip.checkState() == QtCore.Qt.Checked
        SettingFactor().setFreePosFreeOrderEnable("True" if enable else "")

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
        if self.tick is None:
            return
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

    def best_bid_update (self, value):
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid] = {}
        
        cnt = len (value)
        idx = 0
        while idx < cnt:
            price = float(value[idx])
            count = re.match ('[+-]?([0-9]*[.])?[0-9]+', value[idx+1]).group ()
            self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid][price] = int(float(count))
            idx = idx + 2

    def best_ask_update (self, value):
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask] = {}
        cnt = len (value)
        idx = 0
        while idx < cnt:
            price = float(value[idx])
            count = re.match ('[+-]?([0-9]*[.])?[0-9]+', value[idx+1]).group ()
            self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask][price] = int(float(count))
            idx = idx + 2

    def better_price_size_add (self):
        self.run_better_size = self.run_better_size + 1
        self.update_better_price_size ()

    def better_price_size_dec (self):
        self.run_better_size = self.run_better_size - 1
        self.update_better_price_size ()

    def resizeChange (self, event):
        h = self.tablewidget.viewport().height()
        self.itemShowCount = self.tablewidget.itemAt(0, h).row () + 1
        self.itemShowCountDiv2 = int (self.itemShowCount/2)
        self.update_tablewidget_item_price ()
        self.update_curr_item ()

    def update_curr_item (self):
        if self.run_curr_item:
            self.run_curr_item.setData (QtCore.Qt.BackgroundRole, None)
            self.run_curr_item = None

        is_center = self.is_keep_center ()
        if is_center:
            self.run_curr_item = self.tablewidgetitem[PriceLadderWidget.df_header_price][self.itemShowCountDiv2]
            self.run_curr_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_MouseOver)

    def update_tablewidget_item (self, is_center, update_price = False):
        if not self.init_price:
            return

        if is_center:
            self.run_high_price = self.tick.Close + self.itemShowCountDiv2
            self.update_tablewidget_item_price ()
        else:
            curr_price = self.run_high_price - self.tick.Close
            if self.run_price_row != curr_price:
                self.run_price_row = curr_price
                if self.run_curr_item:
                    self.run_curr_item.setData (QtCore.Qt.BackgroundRole, None)
                    self.run_curr_item = None

                if curr_price >= 0 and curr_price <= self.itemShowCount:
                    row = int (self.run_high_price - self.tick.Close)
                    self.run_curr_item = self.tablewidgetitem[PriceLadderWidget.df_header_price][row]
                    self.run_curr_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_MouseOver)

            if update_price:
                self.update_tablewidget_item_price ()
            self.update_better_price_size ()
        self.update_mit_item ()
        self.update_market_item ()
        
        if self.run_average_item:
            self.run_average_item.setData (QtCore.Qt.ForegroundRole, None)

        if self.params.average > 0:
            row = int(self.run_high_price - self.params.average)
            if row >= 0 and row <= self.itemShowCount:
                self.run_average_item = self.tablewidgetitem[2][row]
                self.run_average_item.setData (QtCore.Qt.ForegroundRole, QtWidgets.QStyle.State_Active)

    def update_tablewidget_item_price (self):
        if not self.init_price:
            return
        for i in range (0, self.itemShowCount):
            item = self.tablewidgetitem[PriceLadderWidget.df_header_price][i]
            item.setText (str (self.run_high_price-i))

    def update_better_price_size (self):
        if self.run_better_up_item:
            self.run_better_up_item.setData (QtCore.Qt.BackgroundRole, None)
        if self.run_better_dn_item:
            self.run_better_dn_item.setData (QtCore.Qt.BackgroundRole, None)
        if self.run_better_size != 0:
            curr_price = int(self.run_high_price - self.tick.Close)
            up_row = curr_price - self.run_better_size
            if up_row >= 0 and up_row <= self.itemShowCount:
                self.run_better_up_item = self.tablewidgetitem[2][up_row]
                self.run_better_up_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_UpArrow)
            dn_row = curr_price + self.run_better_size
            if dn_row >= 0 and dn_row <= self.itemShowCount:
                self.run_better_dn_item = self.tablewidgetitem[2][dn_row]
                self.run_better_dn_item.setData (QtCore.Qt.BackgroundRole, QtWidgets.QStyle.State_DownArrow)

    def update_mit_item (self):
        for item in self.run_mit_item_list:
            item.setText ("")
        self.run_mit_item_list = []
        for buy_sell in self.run_mit_list:
            for price in self.run_mit_list[buy_sell]:
                row = int(self.run_high_price - price)
                if row >= 0 and row <= self.itemShowCount:
                    item = self.tablewidgetitem[buy_sell][row]
                    count = self.run_mit_list[buy_sell][price]
                    if count != 0:
                        item.setText (str(count))
                        self.run_mit_item_list.append (item)
                    else:
                        item.setText ("")

    def update_market_item (self):
        for item in self.run_market_item_list:
            item.setText ("")
        self.run_market_item_list = []
        
        bid_list = {}
        ask_list = {}
        for price in self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid]:
            row = int(self.run_high_price - price)
            if row >= 0 and row <= self.itemShowCount:
                if not price in bid_list:
                    bid_list[row] = str(self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid][price])

        for price in self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask]:
            row = int(self.run_high_price - price)
            if row >= 0 and row <= self.itemShowCount:
                if not price in ask_list:
                    ask_list[row] = str(self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask][price])

        for price in self.run_market_list[PriceLadderWidget.df_header_bid]:
            row = int(self.run_high_price - price)
            if row >= 0 and row <= self.itemShowCount:
                count = self.run_market_list[PriceLadderWidget.df_header_bid][price]
                if count <= 0:
                    continue
                if not row in bid_list:
                    bid_list[row] = "({})".format (count)
                else:
                    bid_list[row] = "{}({})".format (bid_list[row], count)
        
        for price in self.run_market_list[PriceLadderWidget.df_header_ask]:
            row = int(self.run_high_price - price)
            if row >= 0 and row <= self.itemShowCount:
                count = self.run_market_list[PriceLadderWidget.df_header_ask][price]
                if count <= 0:
                    continue
                if not row in ask_list:
                    ask_list[row] = "({})".format (count)
                else:
                    ask_list[row] = "{}({})".format (ask_list[row], count)

        for row in bid_list:
            item = self.tablewidgetitem[PriceLadderWidget.df_header_bid][row]
            item.setText (bid_list[row])
            self.run_market_item_list.append (item)

        for row in ask_list:
            item = self.tablewidgetitem[PriceLadderWidget.df_header_ask][row]
            item.setText (ask_list[row])
            self.run_market_item_list.append (item)

    def is_keep_center (self):
        if not self.options.keep_center:
            return False

        if self.options.mouse_wheel:
            now = time.time()
            if now - self.options.mouse_wheel_time > 20:
                self.options.mouse_wheel = False
                self.update_curr_item ()
                self.update_better_price_size ()
            else:
                return False
        return True

    def change_stop_loss (self):
        self.run_stop_loss = self.top_spin_stop_loss.value ()
        SettingFactor().setRunStopLoss(self.run_stop_loss)

    def reconnect (self):
        for item in self.run_mit_item_list:
            item.setText ("")

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
                        
        self.run_position = 1
        self.run_high_price = 0
        self.run_price_row = 0
        self.run_average_item = None
        self.run_better_size = 0
        self.run_better_up_item = None
        self.run_better_dn_item = None
        self.run_mouse_over_item = None
        self.run_mit_item_list = {}
        self.run_mit_list = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_buy] = {}
        self.run_mit_list[PriceLadderWidget.df_header_mit_sell] = {}
        self.run_market_list = {}
        self.run_market_list[PriceLadderWidget.df_header_bid] = {}
        self.run_market_list[PriceLadderWidget.df_header_ask] = {}
        self.run_market_item_list = {}
        self.run_the_fifth_order_list = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_bid] = {}
        self.run_the_fifth_order_list[PriceLadderWidget.df_header_ask] = {}
        self.run_marekt_list = {}
        self.params = SimpleNamespace(position = 0, average = 0, profit = 0, mit_buy_count = 0, mit_sell_count = 0)
        self.params.trade = []
        self.top_spin_position.setValue(self.run_position)
        self.update_mit_header ()
        self.top_label_position.setText("庫存: {}".format (0))
        self.top_label_average.setText("均價: {:.02f}".format (0))
        self.top_label_net_profit.setText("淨損益: {:.02f}".format (0))
        self.top_label_floating_profit.setText("浮動損益: {:.02f}".format (0))
        self.run_get_account_done = True

    def get_account (self):
        self.run_get_account_done = False

    def get_account_done (self):
        self.run_get_account_done = True




