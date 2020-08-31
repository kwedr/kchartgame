import PySide2.QtCore as QtCore
import PySide2.QtCharts as QtCharts
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from signalFactor import SignalFactor

class RecordTradeWidget (QtWidgets.QWidget):

    df_header_buy_sell = 0
    df_header_date = 1
    df_header_price = 2
    df_header_count = 3
    df_header_profit = 4
    df_header_note = 5

    def __init__ (self, parent = None):
        super().__init__(parent)
        self.row_index = 0
        
        self.tablewidget = QtWidgets.QTableWidget(0, 6, self)
        header = ["買賣", "時間", "價格", "數量", "損益", "註解"]
        self.tablewidget.setHorizontalHeaderLabels(header)
        self.tablewidget.setStyleSheet("::section { background-color: #646464; padding: 4px; border: 1px solid #fffff8; color: #D3D3D3; }")
        self.tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tablewidget.setAutoScroll(True)
        #self.tablewidget.cellClicked.connect (self.cellClicked)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tablewidget)

        SignalFactor ().sign_run_init.connect (self.run_init)
        SignalFactor().sign_trade_deal.connect (self.trade_deal)
        
    def add_item (self, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        flag = QtCore.Qt.ItemIsEnabled
        if column == self.df_header_note:
            flag = flag | QtCore.Qt.ItemIsEditable
        item.setFlags (flag) 
        self.tablewidget.setItem(self.row_index-1, column, item)
        self.tablewidget.scrollToItem (item, QtWidgets.QAbstractItemView.PositionAtBottom)

    def run_init (self):
        self.tablewidget.setRowCount(0)
        self.row_index = 0

    def trade_deal (self, tick, long_short, count, gain):
        self.setUpdatesEnabled(False)
        self.tablewidget.insertRow(self.row_index)
        self.row_index = self.row_index + 1
        
        self.add_item (self.df_header_buy_sell, "買" if long_short else "賣")
        self.add_item (self.df_header_date, tick.Date_Time.strftime ('%H:%M'))
        self.add_item (self.df_header_count, str(count))
        self.add_item (self.df_header_price, str(tick.Close))
        self.add_item (self.df_header_profit, str(gain) if gain != 0 else "")
        self.add_item (self.df_header_note, "")

        self.setUpdatesEnabled(True)
