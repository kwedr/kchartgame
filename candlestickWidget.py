import time, math, sys
from datetime import datetime
import pandas as pd
import PySide2.QtCore as QtCore
import PySide2.QtCharts as QtCharts
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from signalFactor import SignalFactor
from pandasModel import PandasModel
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
from types import SimpleNamespace

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.series = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        w = 0.4
        self.offset = 0
        self.low = 0
        self.high = 1
        self.pictures = []
        self.wPen = pg.mkPen(color='w', width=w * 2)
        self.wBrush = pg.mkBrush('w')
        self.bPen = pg.mkPen(color='g', width=w * 2)
        self.bBrush = pg.mkBrush('g')
        self.rPen = pg.mkPen(color='r', width=w * 2)
        self.rBrush = pg.mkBrush('r')
        #self.rBrush.setStyle(QtCore.Qt.NoBrush)

    def generatePicture(self, redraw=False):
        if redraw:
            self.pictures = []
        elif self.pictures:
            obj = self.pictures.pop()

        w = 0.3
        bPen = self.bPen
        bBrush = self.bBrush
        rPen = self.rPen
        rBrush = self.rBrush
        low, high = (self.series[0].low(), self.series[0].high ()) if len(self.series) > 0 else (sys.maxsize, 1)
        for data in self.series:
            t = int (data.timestamp())
            if t >= len(self.pictures):
                tShift = t

                low, high = (min(low, data.low()), max(high, data.high()))
                picture = QtGui.QPicture()
                p = QtGui.QPainter(picture)
                pen, brush, pmin, pmax = (bPen, bBrush, data.close(), data.open()) \
                    if data.open() > data.close() else (rPen, rBrush, data.open(), data.close())

                p.setPen(self.wPen)
                p.setBrush(self.wBrush)
                
                if pmin > data.low():
                    p.drawLine(QtCore.QPointF(tShift, data.low()), QtCore.QPointF(tShift, pmin))
                if data.high() > pmax:
                    p.drawLine(QtCore.QPointF(tShift, pmax), QtCore.QPointF(tShift, data.high()))

                p.setPen(self.wPen)
                #p.setPen(QtCore.Qt.NoPen)
                p.setBrush(brush)                    
                p.drawRect(QtCore.QRectF(tShift - w, data.open(), w * 2, data.close() - data.open()))
                p.end()
                self.pictures.append(picture)
        self.low, self.high = low, high

    def append (self, data, draw=True, redraw=False):
        self.series.append (data)
        if draw:
            self.generatePicture (redraw)

    def pop (self):
        data = self.series[-1]
        del self.series[-1]
        return data

    def update(self):
        if not self.scene() is None:
            self.scene().update()

    def paint(self, p, o, w):
        rect = o.exposedRect
        xmin, xmax = (max(0, int(rect.left())), min(len(self.pictures), int(rect.right())))
        [p.drawPicture(0, 0, pic) for pic in self.pictures[xmin:xmax]]

    def boundingRect(self):
        return QtCore.QRectF(0, self.low, len(self.pictures), (self.high - self.low))

    def clear (self):
        self.series = []
        self.pictures = []

class CenteredTextItem(QtGui.QGraphicsTextItem):
    def __init__(
        self,
        text='',
        parent=None,
        pos=(0, 0),
        pen=None,
        brush=None,
        valign=None,
        opacity=0.1,
    ):
        super().__init__(text, parent)

        self.pen = pen
        self.brush = brush
        self.opacity = opacity
        self.valign = valign
        self.text_flags = QtCore.Qt.AlignCenter
        self.setPos(*pos)
        self.setFlag(self.ItemIgnoresTransformations)
        self.visible = False
    
    def isvisible (self):
        return self.visible

    def setvisible (self, visible):
        self.visible = visible

    def boundingRect(self):  # noqa
        r = super().boundingRect()
        if self.valign == QtCore.Qt.AlignTop:
            return QtCore.QRectF(-r.width() / 2, -37, r.width(), r.height())
        elif self.valign == QtCore.Qt.AlignBottom:
            return QtCore.QRectF(-r.width() / 2, 15, r.width(), r.height())
        elif self.valign == QtCore.Qt.AlignCenter:
            return QtCore.QRectF(-r.width() / 2, -11, r.width(), r.height())

    def paint(self, p, option, widget):
        if self.visible == False:
            return
        p.setRenderHint(p.Antialiasing, False)
        p.setRenderHint(p.TextAntialiasing, True)
        p.setPen(self.pen)
        if self.brush.style() != QtCore.Qt.NoBrush:
            p.setOpacity(self.opacity)
            p.fillRect(option.rect, self.brush)
            p.setOpacity(1)
        p.drawText(option.rect, self.text_flags, self.toPlainText())

class PricePositionItem:
    def __init__(self, parent):
        self.parent = parent
        self.series = []
        self.items = []
        self.rcbounding = QtCore.QRectF (0, 0, 0, 0)
        #self.setFlag(self.ItemUsesExtendedStyleOption)
        self.wPen = pg.mkPen(color='w')
        self.wBrush = pg.mkBrush('w')
        self.visible = False

    def append (self, data):
        item = CenteredTextItem (data.text, self.parent, [data.posx, data.Close], self.wPen, self.wBrush, QtCore.Qt.AlignCenter)
        item.setvisible (self.visible)
        self.items.append (item)
        self.rcbounding = self.rcbounding.united (item.boundingRect())

    def pop (self):
        data = self.series[-1]
        del self.series[-1]
        del self.items[-1]
        return data

    def last (self):
        if len(self.series) > 0:
            return self.series[-1]
        return None

    def paint(self, p, option, widget):
        return

    def boundingRect(self):
        return self.rcbounding

    def clear (self):
        self.series = []
        for item in self.items:
            item.setvisible (False)
        self.items = []

    def setvisible (self, visible):
        self.visible = visible
        for item in self.items:
            item.setvisible (self.visible)

    def isvisible (self):
        return self.visible

class TimeStringAxis (pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.setPen(color=(255, 255, 255, 255), width=0.8)
        self.setStyle(tickFont=QtGui.QFont("Roman times", 10, QtGui.QFont.Bold), autoExpandTextSpace=True)
        self.x_values = []
        self.x_strings = {}

    def clear (self):
        self.x_values = []
        self.x_strings = {}
        
    def append (self, values):
        self.x_values.append (values[0])
        self.x_strings[values[0]] = values[1]

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            if vs in self.x_values:
                vstr = self.x_strings[vs]
            else:
                vstr = ""
            strings.append(vstr)
        return strings

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.PanMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        pass
        #if ev.button() == QtCore.Qt.RightButton:
        #    self.autoRange()

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

        #if ev.button() == QtCore.Qt.RightButton:
        #    ev.ignore()
        #else:
        #    pg.ViewBox.mouseDragEvent(self, ev)

class CandlestickChartWidget (QtWidgets.QWidget):
    df_max_bar = 300
    df_show_bar = 50
    df_left_bar = 5
    df_right_bar = 5
    df_top_volumn = 100
    df_bottom_volumn = 80

    def __init__(self, parent = None):
        super().__init__(parent)
        self.run_left_bar = 0
        self.run_show_bar = self.df_show_bar
        self.run_tick_range_left = 0
        self.trade = SimpleNamespace (count = 0, long_short = True)
        self.candlesTick = CandlestickItem ()
        self.pricePosition = PricePositionItem (self.candlesTick)
        self.axis_x_datetime = TimeStringAxis(orientation='bottom')
        self.axis_x_datetime.setTickSpacing(10, 5)
        vb = CustomViewBox()
        self.plotwidget = pg.PlotWidget(viewBox=vb, axisItems={'bottom': self.axis_x_datetime}, enableMenu=False)
        self.plotwidget.addItem (self.candlesTick)
        #self.plotwidget.addItem (self.pricePosition)
        self.plotwidget.showGrid (x=True, y=True)

        self.axis_volumn_left = self.plotwidget.getAxis('left')
        self.axis_volumn_left.setTickSpacing(10, 1)

        self.top_line = pg.InfiniteLine(angle=0, movable=False, )
        self.bottom_line = pg.InfiniteLine(angle=0, movable=False, )
        self.plotwidget.addItem (self.top_line, ignoreBounds=True)
        self.plotwidget.addItem (self.bottom_line, ignoreBounds=True)

        self.top_label = pg.TextItem (anchor = (0,1))
        self.bottom_label = pg.TextItem ()
        self.plotwidget.addItem (self.top_label, ignoreBounds=True)
        self.plotwidget.addItem (self.bottom_label, ignoreBounds=True)

        self.scrollbar_x = QtWidgets.QScrollBar(QtCore.Qt.Horizontal)
        self.scrollbar_x.setMinimum(0)
        self.scrollbar_x.setMaximum(self.df_max_bar-self.df_show_bar-1)
        self.scrollbar_x.sliderMoved.connect (self.onAxisSliderMoved)
        
        self.slider_x = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_x.setRange(-self.df_left_bar, self.df_max_bar-self.df_show_bar)
        self.slider_x.setValue(0)
        self.slider_x.sliderMoved.connect (self.onZoomSliderXMoved)
        self.slider_x.setVisible (False)

        self.slider_y = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.slider_y.setRange(-100, 100)
        self.slider_y.setValue(0)
        self.slider_y.sliderMoved.connect (self.onZoomSliderYMoved)
        self.slider_y.setVisible (False)

        hlay = QtWidgets.QHBoxLayout()
        
        for w in (self.plotwidget, self.slider_y):
            hlay.addWidget(w)

        vlay = QtWidgets.QVBoxLayout(self)
        vlay.addLayout (hlay)
        for w in (self.scrollbar_x, self.slider_x):
            vlay.addWidget(w)

        self.info_lable = pg.TextItem()
        self.plotwidget.addItem(self.info_lable)
        self.vLine = pg.InfiniteLine(angle=90, movable=False, )
        self.hLine = pg.InfiniteLine(angle=0, movable=False, )
        self.plotwidget.addItem(self.vLine, ignoreBounds=True)
        self.plotwidget.addItem(self.hLine, ignoreBounds=True)
        self.line_label = pg.TextItem (anchor = (0,1))
        self.plotwidget.addItem(self.line_label, ignoreBounds=True)
        self.move_slot = pg.SignalProxy(self.plotwidget.scene().sigMouseMoved, rateLimit=60, slot=self.print_slot)

        SignalFactor ().sign_savefile.connect (self.savefile)
        SignalFactor ().sign_run_init.connect (self.run_init)
        SignalFactor ().sign_tick_update.connect (self.update_tick)
        SignalFactor ().sign_zoom_x_visible.connect (self.zoom_x_visible)
        SignalFactor ().sign_zoom_y_visible.connect (self.zoom_y_visible)
        SignalFactor ().sign_mark.connect (self.mark)
        SignalFactor ().sign_trade_deal.connect (self.trade_deal)
        SignalFactor ().sign_review_goto_init.connect (self.review_goto_init)
        SignalFactor ().sign_review_goto_done.connect (self.review_goto_done)

    def savefile (self, filename):
        import pyqtgraph.exporters
        exporter = pg.exporters.ImageExporter(self.plotwidget.plotItem)
        exporter.parameters()['width'] = 1024
        exporter.parameters()['height'] = 768
        exporter.export(filename)

    def run_init (self, value):
        self.candle = {}
        self.candlesTick.clear ()
        self.pricePosition.clear ()
        self.trade = SimpleNamespace (count = 0, long_short = True)

        start_time = QtCore.QDateTime.fromString(value['start_time'], 'yyyyMMddhhmm')
        self.run_left_bar = int((start_time.toSecsSinceEpoch() % 600) / 60)
        if self.run_left_bar <= 0:
            self.run_left_bar = 10

        
        self.run_idx = self.run_left_bar-1
        self.run_tick_datetime_start = start_time.addSecs(self.run_left_bar * -60)
        #self.run_tick_datetime_end = QtCore.QDateTime.fromString(value['end_time'], 'yyyyMMddhhmm').addSecs(self.df_right_bar * 60)
        self.run_volumn_max = 0
        self.run_volumn_min = 1000000
        self.run_volumn_range = 0
        self.run_tick_range_left = 0
        self.run_tick_range_right = self.df_show_bar-1
        self.run_show_bar = self.df_show_bar
        self.run_goto = False

        axis_x_time = self.run_tick_datetime_start
        for i in range (self.df_max_bar):
            self.axis_x_datetime.append ([i, axis_x_time.toString('hh:mm')])
            axis_x_time = axis_x_time.addSecs(60)
        self.axis_x_datetime.setRange (0, self.run_show_bar)
        self.axis_x_datetime.setStyle (tickLength = self.run_show_bar)
        self.plotwidget.setXRange (0, self.run_show_bar)

        self.onAxisSliderMoved (0)

    def update_tick (self, tick):
        self.setUpdatesEnabled(False)
        candle = None
        o, h, l, c = tick.Open, tick.High, tick.Low, tick.Close
        tick_date_time = QtCore.QDateTime()
        tick_date_time.setDate(QtCore.QDate(tick.Date_Time.year, tick.Date_Time.month, tick.Date_Time.day))
        tick_date_time.setTime (QtCore.QTime(tick.Date_Time.hour, tick.Date_Time.minute))
        #tick_date_time = tick.Date_Time
        if tick_date_time in self.candle:
            candle = self.candle[tick_date_time]
            o = candle.open()
            h = max (h, candle.high())
            l = min (l, candle.low())

        if candle != None:
            candle = self.candlesTick.pop ()
            candle.setOpen(o)
            candle.setHigh(h)
            candle.setLow(l)
            candle.setClose(c)
            self.candlesTick.append (candle, not self.run_goto)

        else:
            self.run_idx = self.run_idx +1
            #self.run_num_list.append (str(tick.Date_Time))
            candle = QtCharts.QtCharts.QCandlestickSet(o, h, l, c, self.run_idx)
            self.candle[tick_date_time] = candle
            self.candlesTick.append (candle, not self.run_goto)
            if (self.run_idx >= self.run_show_bar):
                if (self.run_idx - self.run_tick_range_left) + self.run_show_bar >= self.run_tick_range_right:
                    self.onAxisSliderMoved (self.run_tick_range_left+1)
                    self.scrollbar_x.setSliderPosition(self.run_tick_range_left)
        
        self.adjust_axes_y (l, h)
        self.setUpdatesEnabled(True)

    def adjust_axes_y (self, value_min, value_max):
        vmax = max (self.run_volumn_max, value_max)
        vmin = min (self.run_volumn_min, value_min)
        if vmax != self.run_volumn_max or vmin != self.run_volumn_min:
            self.run_volumn_max = vmax
            self.run_volumn_min = vmin
            self.top_label.setText(str(self.run_volumn_max))
            self.top_label.setPos (0, self.run_volumn_max)
            self.top_line.setPos (self.run_volumn_max)
            self.bottom_label.setText(str(self.run_volumn_min))
            self.bottom_label.setPos (0, self.run_volumn_min)
            self.bottom_line.setPos (self.run_volumn_min)
            value_max = int((vmax + self.df_top_volumn) / 10) * 10
            value_min = int((vmin - self.df_bottom_volumn) / 10) * 10
            vmin = value_min - self.run_volumn_range
            vmax = value_max + self.run_volumn_range
            count = (vmax-vmin) / 10
            self.plotwidget.setYRange (vmin, vmax)

    def adjust_axes_x (self, value_min, value_max):
        vmin = max (value_min, 0)
        vmax = min (value_max, self.df_max_bar-1)
        if (value_max - value_min) < 80:
            self.axis_x_datetime.setTickSpacing (10, 5)
        elif (value_max - value_min) < 150:
            self.axis_x_datetime.setTickSpacing (30, 10)
        else:
            self.axis_x_datetime.setTickSpacing (60, 30)
        self.run_tick_range_left = vmin
        self.run_tick_range_right = vmax
        self.axis_x_datetime.setRange (vmin, vmax)
        self.plotwidget.setXRange (vmin, vmax)
        label_pos = self.line_label.pos ()
        label_pos[0] = vmin
        self.line_label.setPos (label_pos)
        label_pos = self.top_label.pos ()
        label_pos[0] = vmin
        self.top_label.setPos (label_pos)
        label_pos = self.bottom_label.pos ()
        label_pos[0] = vmin
        self.bottom_label.setPos (label_pos)


    @QtCore.Slot(int)
    def onAxisSliderMoved(self, value):
        r = value / self.df_max_bar * self.df_max_bar
        self.adjust_axes_x(math.floor(r), math.ceil(r + self.run_show_bar-1))

    @QtCore.Slot(int)
    def onZoomSliderXMoved(self, value):
        self.run_show_bar = self.df_show_bar + value
        self.adjust_axes_x (self.run_tick_range_left, self.run_tick_range_left + self.run_show_bar)

    @QtCore.Slot(int)
    def onZoomSliderYMoved(self, value):
        self.run_volumn_range = value
        value_max = int((self.run_volumn_max + self.df_top_volumn) / 10) * 10
        value_min = int((self.run_volumn_min - self.df_bottom_volumn) / 10) * 10
        vmin = value_min - self.run_volumn_range
        vmax = value_max + self.run_volumn_range
        count = (vmax-vmin) / 10
        self.plotwidget.setYRange (vmin, vmax)

    def zoom_x_visible (self):
        is_visible = self.slider_x.isVisible ()
        self.slider_x.setVisible (not is_visible)

    def zoom_y_visible (self):
        is_visible = self.slider_y.isVisible ()
        self.slider_y.setVisible (not is_visible)

    def print_slot(self, event=None):
        if event is None:
            return
        else:
            self.info_lable.setVisible (False)
            self.vLine.setVisible (False)
            self.hLine.setVisible (False)
            self.line_label.setVisible (False)
            pos = event[0]
            try:
                if self.plotwidget.sceneBoundingRect().contains(pos):
                    self.vLine.setVisible (True)
                    self.hLine.setVisible (True)
                    self.line_label.setVisible (True)
                    mousePoint = self.plotwidget.plotItem.vb.mapSceneToView(pos)
                    index = int(mousePoint.x())
                    pos_y = int(mousePoint.y())
                    index = index - self.run_left_bar 
                    if -1 < index < len(self.candlesTick.series):
                        data = self.candlesTick.series[index]
                        time = self.run_tick_datetime_start.addSecs((self.run_left_bar + index) *60).toString ('hh:mm')
                        self.info_lable.setVisible (True)
                        self.info_lable.setHtml(
                            "<p style='color:white'><strong>{0}</strong></p><p style='color:white'>開：{1}</p><p style='color:white'>收：{2}</p><p style='color:white'>高：<span style='color:red;'>{3}</span></p><p style='color:white'>低：<span style='color:green;'>{4}</span></p>".format(
                                time, data.open(), data.close(), data.high(),data.low()))
                        self.info_lable.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                    
                    # 设置垂直线条和水平线条的位置组成十字光标
                    self.vLine.setPos(mousePoint.x())
                    self.hLine.setPos(mousePoint.y())
                    self.line_label.setText (str(int(mousePoint.y())))
                    self.line_label.setPos (self.run_tick_range_left, mousePoint.y())
            except Exception as e:
                pass
    
    def mark (self):
        visible =  not self.pricePosition.isvisible ()
        self.pricePosition.setvisible (visible)

    def trade_deal (self, tick, long_short, count, gain):
        go = 1 if long_short else -1
        count = count if go > 0 else -count
        if self.trade.long_short == long_short:
            self.trade.count = self.trade.count + (count * go)
        else:
            self.trade.count = self.trade.count - (count * go)

        if self.trade.count == 0:
            self.trade.long_short =  True
        
        mark = self.pricePosition.last ()
        if mark != None and mark.Date_Time == tick.Date_Time and mark.long_short == long_short and mark.Close == tick.Close:
            mark.count = self.trade.count
            if self.trade.count > 0:
                mark.text = "+" + str(self.trade.count)
            else:
                mark.text = str(self.trade.count)
            self.pricePosition.pop ()
            self.pricePosition.append (mark)
        else:
            tick_date_time = QtCore.QDateTime()
            tick_date_time.setDate(QtCore.QDate(tick.Date_Time.year, tick.Date_Time.month, tick.Date_Time.day))
            tick_date_time.setTime (QtCore.QTime(tick.Date_Time.hour, tick.Date_Time.minute))

            loc = int((tick_date_time.toTime_t() - self.run_tick_datetime_start.toTime_t()) / 60)
            mark = SimpleNamespace (idx = 0, posx = loc, count = self.trade.count, long_short = long_short, Date_Time = tick.Date_Time, Close = tick.Close)
            if self.trade.count > 0:
                mark.text = "+" + str(self.trade.count)
            else:
                mark.text = str(self.trade.count)
            self.pricePosition.append (mark)

    def review_goto_init (self):
        self.candle = {}
        self.candlesTick.clear ()
        self.run_idx = self.run_left_bar-1
        self.run_goto = True
        self.run_volumn_max = 0
        self.run_volumn_min = 1000000
        self.top_label.setText(str(self.run_volumn_max))
        self.top_label.setPos (0, self.run_volumn_max)
        self.top_line.setPos (self.run_volumn_max)
        self.bottom_label.setText(str(self.run_volumn_min))
        self.bottom_label.setPos (0, self.run_volumn_min)
        self.bottom_line.setPos (self.run_volumn_min)

    def review_goto_done (self):
        self.candlesTick.generatePicture (True)
        self.run_goto = False




