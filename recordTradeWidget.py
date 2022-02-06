from datetime import datetime
from logging import info
from types import SimpleNamespace
import pandas as pd
import PySide2.QtCore as QtCore
import PySide2.QtCharts as QtCharts
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from signalFactor import SignalFactor

class RecordTradeWidget (QtWidgets.QWidget):

    df_page_deal = 0
    df_page_order = 1
    df_page_deal_record = 2

    df_deal_header_buy_sell = 0
    df_deal_header_date = 1
    df_deal_header_price = 2
    df_deal_header_count = 3
    df_deal_header_profit = 4
    df_deal_header_note = 5

    df_order_header_buy_sell = 1
    df_order_header_date = 2
    df_order_header_price = 3
    df_order_header_count = 4
    df_order_header_report = 5

    def __init__ (self, parent = None):
        super().__init__(parent)

        self.bottomlay = QtWidgets.QHBoxLayout()
        self.top_save = QtWidgets.QPushButton ("Save", self)
        self.top_save.clicked.connect (self.btn_save)
        self.top_load = QtWidgets.QPushButton ("Load", self)
        self.top_load.clicked.connect (self.btn_load)
        self.bottomlay.addWidget (self.top_save)
        self.bottomlay.addWidget (self.top_load)
        self.vlay = QtWidgets.QVBoxLayout(self)

        self.tab = QtWidgets.QTabWidget ()
        self.vlay.addWidget(self.tab)
        self.vlay.addLayout(self.bottomlay)
        
        self.tick = 0
        self.deal_row_index = 0
        self.order_row_index = 0
        self.deal_record_row_index = 0
        self.page = []
        self.create_page1 ()
        self.create_page2 ()
        self.order = {}
        self.deal = []
        self.deal_gain = 0
        self.deal_record = []

        SignalFactor ().sign_run_init.connect (self.run_init)
        SignalFactor ().sign_trade_deal.connect (self.trade_deal)
        SignalFactor ().sign_trade_order_ret.connect (self.trade_order)
        SignalFactor ().sign_reconnect.connect (self.reconnect)
        SignalFactor ().sign_tick_update.connect (self.tick_update)

    def create_page1 (self):
        tablewidget = QtWidgets.QTableWidget(0, 6, self)
        header = ["買賣", "時間", "價格", "數量", "損益", "註解"]
        tablewidget.setHorizontalHeaderLabels(header)
        tablewidget.setStyleSheet("::section { background-color: #646464; padding: 4px; border: 1px solid #fffff8; color: #D3D3D3; }")
        tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        tablewidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        #tablewidget.setAutoScroll(True)
        #tablewidget.cellClicked.connect (self.cellClicked)

        #layout = QtWidgets.QVBoxLayout(self)
        #layout.addWidget (tablewidget)
        #page = {"layout" : layout, "tablewidget" : tablewidget}
        self.page.append (tablewidget)
        self.tab.addTab(tablewidget, "Deal")

    def create_page2 (self):
        tablewidget = QtWidgets.QTableWidget(0, 6, self)
        header = ["操作", "買賣", "時間", "價格", "數量", "說明"]
        tablewidget.setHorizontalHeaderLabels(header)
        tablewidget.setStyleSheet("::section { background-color: #646464; padding: 4px; border: 1px solid #fffff8; color: #D3D3D3; }")
        tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        tablewidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        #tablewidget.setAutoScroll(True)
        #tablewidget.cellClicked.connect (self.cellClicked)

        #layout = QtWidgets.QVBoxLayout(self)
        #layout.addWidget (tablewidget)
        #page = {"layout" : layout, "tablewidget" : tablewidget}
        self.page.append (tablewidget)
        self.tab.addTab(tablewidget, "Order")

    def create_page3 (self):
        tablewidget = QtWidgets.QTableWidget(0, 6, self)
        header = ["買賣", "時間", "價格", "數量", "損益", "註解"]
        tablewidget.setHorizontalHeaderLabels(header)
        tablewidget.setStyleSheet("::section { background-color: #646464; padding: 4px; border: 1px solid #fffff8; color: #D3D3D3; }")
        tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        tablewidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        #tablewidget.setAutoScroll(True)
        #tablewidget.cellClicked.connect (self.cellClicked)

        #layout = QtWidgets.QVBoxLayout(self)
        #layout.addWidget (tablewidget)
        #page = {"layout" : layout, "tablewidget" : tablewidget}
        self.page.append (tablewidget)
        self.tab.addTab(tablewidget, "Deal Record")

    def add_deal_item (self, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        flag = QtCore.Qt.ItemIsEnabled
        if column == self.df_deal_header_note:
            flag = flag | QtCore.Qt.ItemIsEditable
        item.setFlags (flag) 
        self.page[self.df_page_deal].setItem(self.deal_row_index-1, column, item)
        self.page[self.df_page_deal].scrollToItem (item, QtWidgets.QAbstractItemView.PositionAtBottom)

    def add_order_item (self, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        if column == self.df_deal_header_note:
            item.setTextAlignment(QtCore.Qt.AlignLeft)
        else:
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        flag = QtCore.Qt.ItemIsEnabled
        if column == self.df_deal_header_note:
            flag = flag | QtCore.Qt.ItemIsEditable
        item.setFlags (flag) 
        self.page[self.df_page_order].setItem(self.order_row_index-1, column, item)
        self.page[self.df_page_order].scrollToItem (item, QtWidgets.QAbstractItemView.PositionAtBottom)
        self.page[self.df_page_order].horizontalScrollBar().setValue (0)
        
    def add_deal_record_item (self, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        #flag = QtCore.Qt.ItemIsEnabled
        #if column == self.df_deal_header_note:
        #    flag = flag | QtCore.Qt.ItemIsEditable
        #item.setFlags (flag) 
        self.page[self.df_page_deal_record].setItem(self.deal_record_row_index-1, column, item)
        self.page[self.df_page_deal_record].scrollToItem (item, QtWidgets.QAbstractItemView.PositionAtBottom)

    def run_init (self):
        if len(self.page) > self.df_page_order:
            self.page[self.df_page_deal].setRowCount(0)
            self.page[self.df_page_order].setRowCount(0)

        self.tick = 0
        self.deal_row_index = 0
        self.order_row_index = 0
        self.deal_record_row_index = 0
        self.order = {}
        self.deal = []
        self.deal_gain = 0

    def trade_deal (self, tick, long_short, count, gain):
        self.setUpdatesEnabled(False)
        self.page[self.df_page_deal].insertRow(self.deal_row_index)
        self.deal_row_index = self.deal_row_index + 1
        self.deal.append ([tick, long_short, count, gain])
        self.deal_gain = self.deal_gain + gain

        self.add_deal_item (self.df_deal_header_buy_sell, "買" if long_short else "賣")
        self.add_deal_item (self.df_deal_header_date, tick.Date_Time.strftime ('%H:%M:%S'))
        self.add_deal_item (self.df_deal_header_count, str(count))
        self.add_deal_item (self.df_deal_header_price, str(tick.Close))
        self.add_deal_item (self.df_deal_header_profit, str(gain) if gain != 0 else "")
        self.add_deal_item (self.df_deal_header_note, "")

        self.setUpdatesEnabled(True)

    def trade_order (self, order, report):
        if order.id in self.order:
            if self.order[order.id] == report:
                return

        self.setUpdatesEnabled(False)
        self.page[self.df_page_order].insertRow(self.order_row_index)
        self.order_row_index = self.order_row_index + 1

        self.add_order_item (self.df_order_header_buy_sell, order.long_short)
        self.add_order_item (self.df_order_header_date, order.date_time.strftime ('%H:%M:%S'))
        self.add_order_item (self.df_order_header_count, str(order.count))
        self.add_order_item (self.df_order_header_price, str(order.price))
        self.add_order_item (self.df_order_header_report, report)
        self.order[order.id] = report
        self.setUpdatesEnabled(True)

    def reconnect (self):
        self.run_init ()

    def tick_update (self, tick):
        self.tick = tick

        if self.deal_record:
            deal = self.deal_record [-1]
            if deal.Date_Time <= self.tick.Date_Time and deal.Close == self.tick.Close:
                SignalFactor().sign_kbar_deal_mark.emit (deal)
                self.deal_record.pop ()

    def btn_save (self):
        if len (self.deal) <= 0 :
            QtWidgets.QMessageBox.information(self, "Fail", "deal is empty")
            return

        fileName = self.deal [0][0].Date_Time.strftime("%Y%m%d") + "_" + "{0:+}".format (int(self.deal_gain))
        fileName = fileName + "_" + datetime.now().strftime("%Y%m%d%H%M") + ".deal"
        filters = ('all file (*.*);;')
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', fileName, filter=filters)[0]
        if not fileName:
            return

        out_file = QtCore.QFile(fileName)

        if not out_file.open(QtCore.QIODevice.WriteOnly):
            QtWidgets.QMessageBox.information(self, "Unable to open file",
                    out_file.errorString())
            return

        out_s = QtCore.QTextStream(out_file)
        out_s << 'VER:0.1' << '\n'     
        out_s << '//datetime, price, long_short, count' << '\n' 
        deal_row_index = 0
        for deal in (self.deal):
            out_s << deal[0].Date_Time.strftime("%Y%m%d%H%M%S")  << "," << deal[0].Close << "," << deal[1] << "," << deal[2] << "," << deal[3] << ","
            item = self.page[self.df_page_deal].item(deal_row_index, self.df_deal_header_note)
            out_s << item.text () << '\n'
            deal_row_index = deal_row_index + 1

        QtWidgets.QMessageBox.information(self, "Export Successful", fileName)

    def btn_load (self):
        filters = ('all file (*.*);;')
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', './', filter=filters)[0]
        if fileName:
            file = QtCore.QFile(fileName)
            if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                QtWidgets.QMessageBox.warning(self, "Application",
                        "Cannot read file %s:\n%s." % (fileName, file.errorString()))
                return
            self.deal_record = []
            if len(self.page) <= self.df_page_deal_record:
                self.create_page3 ()
            else:
                self.page[self.deal_record_row_index].setRowCount(0)
                self.deal_record_row_index = 0

            inf = QtCore.QTextStream(file)
            while not inf.atEnd():
                line = inf.readLine() #read one line at a time
                if line[0:2] == "//":
                    continue
                if 'VER' in line:
                    continue

                datas = line.split (',')
    
                Date_Time = pd.Timestamp(datas[0])
                deal = SimpleNamespace (Date_Time = Date_Time, Close = float(datas[1]), LongShort = True if int(datas[2]) > 0 else False, Count = int(datas[3]))

                self.setUpdatesEnabled(False)
                self.page[self.df_page_deal_record].insertRow(self.deal_record_row_index)
                self.deal_record_row_index = self.deal_record_row_index + 1
                self.add_deal_record_item (self.df_deal_header_buy_sell, "買" if int(datas[2]) else "賣")
                self.add_deal_record_item (self.df_deal_header_date, Date_Time.strftime ('%H:%M:%S'))
                self.add_deal_record_item (self.df_deal_header_count, datas[3])
                self.add_deal_record_item (self.df_deal_header_price, datas[1])
                self.add_deal_record_item (self.df_deal_header_profit, datas[4])
                self.add_deal_record_item (self.df_deal_header_note, datas[5])
                self.setUpdatesEnabled(True)
                
                if hasattr(self.tick, 'Date_Time') and self.tick.Date_Time >= deal.Date_Time:
                    SignalFactor().sign_kbar_deal_mark.emit (deal)
                else:
                    self.deal_record.append (deal)
            self.deal_record.reverse ()
            QtWidgets.QMessageBox.information(self, "Load Successful", fileName)
            





                