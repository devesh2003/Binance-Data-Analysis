import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import requests
import warnings
warnings.filterwarnings("ignore")

'''
All operations on the dataframe are done in the utc context, time needs to be converted to utc before passing to the functions.
BinanceSync takes an exisiting dataframe and asynchronously updates it to the latest candlestick data
'''

class BinanceSync:
    def __init__(self,df,symbol,interval):
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        try:
            df["Close Time"] = pd.to_datetime(df["Close Time"], unit="ms")
        except:
            # df["Close Time"] = pd.to_datetime(df["Close Time"]+1, unit="ms")
            pass
        self.df = df
        self.symbol = symbol
        self.interval = interval

    '''
    Sample response from API
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
    '''
    def get_candlestick(self,start,end):
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={self.symbol}&interval={self.interval}&limit=1&starttime={int(start)}"
        r = requests.get(url,verify=False)
        data = r.json()
        df = {
            "Open Time": datetime.fromtimestamp(data[0][0]/1000),
            "Open": float(data[0][1]),
            "High": float(data[0][2]),
            "Low": float(data[0][3]),
            "Close": float(data[0][4]),
            "Volume": float(data[0][5]),
            "Close Time": datetime.fromtimestamp(data[0][6]/1000),
            "Quote Asset Volume": float(data[0][7]),
            "Number of Trades": int(data[0][8]),
            "Taker Buy Base Asset Volume": float(data[0][9]),
            "Taker Buy Quote Asset Volume": float(data[0][10]),
            "Ignore": float(data[0][11])
        }
        print(url)
        print(r.text)
        print("-----------------------")
        return pd.DataFrame(df,index=[0])

    def get_current_time(self):
        url = "https://fapi.binance.com/fapi/v1/time"
        r = requests.get(url,verify=False,allow_redirects=True)
        data = r.json()
        return datetime.fromtimestamp(data["serverTime"]/1000)

    def sync(self):
        last = self.df.iloc[-1]
        last_time = last["Close Time"]
        cur_time = self.get_current_time()

        # Already synced
        if cur_time < last_time:
            return self.df
        
        sync_start = last_time.timestamp()*1000
        sync_end = cur_time.timestamp()*1000
        sync_date = last_time

        while sync_start < sync_end:
            df = self.get_candlestick(sync_start,sync_end)
            self.df = self.df.append(df,ignore_index=True)
            sync_date += timedelta(minutes=15)
            sync_start = sync_date.timestamp()*1000
        
        

