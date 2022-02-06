
import asyncio
import pandas as pd
import requests as req
from io import StringIO
import json
import datetime, os, time
from types import SimpleNamespace
from settingFactor import SettingFactor
from singleton import Singleton

class YahooAgent (Singleton):
    def __init__(self):
        pass

    def init (self):
        pass

    def getNowDate (self, diff = 0):
        if diff == 0:
            return datetime.date.today().strftime("%Y%m%d")
        else:
            nowdate = datetime.date.today() + datetime.timedelta(days=diff)
            return nowdate.strftime("%Y%m%d")
        
    def setCallback (self, callback_price):
        self.callback_price = callback_price

    def run_start (self):
        
        url = "https://tw.screener.finance.yahoo.net/future/q?type=ta&perd=1m&mkt=01&sym={}&callback=".format (SettingFactor().getYahooProdId())
        try:
            r = req.get(url)
        except:
            raise

        ta_idx = r.text.index ('"ta":')
        datas = json.load(StringIO('['+r.text[ta_idx+6:-4]+']'))
        for v in (datas):
            tick = SimpleNamespace (Date_Time = pd.to_datetime(v['t'], format= '%Y%m%d%H%M'), Close = v['c'], High = v['h'], Low = v['l'], Open = v['o'])
            self.callback_price (tick)

    def parse_text (self, txt):
        return txt.decode("big5").strip('\r\n')
