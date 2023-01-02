import pandas as pd
import numpy as np
from datetime import datetime

'''
All operations on the dataframe are done in the utc context, time needs to be converted to utc before passing to the functions.
BinanceSync takes an exisiting dataframe and asynchronously updates it to the latest candlestick data
'''

class BinanceSync:
    def __init__(self,df):
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        df["Close Time"] = pd.to_datetime(df["Close Time"]+1, unit="ms")
        self.df = df

    def sync(self):
        last = self.df.iloc[-1]
        last_time = last["Close Time"]
        cur_time = datetime.utcnow()

        # Already synced
        if cur_time.day < last_time.day:
            return self.df
        
        

