import pandas as pd
import numpy as np

class HyperBacktest:
    def __init__(self,target,sl,calculator,df,max_time=1*24*60,long=True,short=True
                ,fees=0.1):
        self.target = target/100
        self.sl = sl/100
        self.calculator = calculator
        self.df = df.copy()
        self.max_time = max_time
        self.fees = fees
        self.long = long
        self.short = short

    def run(self):
        if self.long:
            self.long_trades()
        if self.short:
            self.short_trades()

    def long_trades(self):
        wins = 0
        losses = 0
        for i in np.where( (self.df["Buy"] == 1) )[0]:
            target_price = self.df["Close"][i] * (1+self.target)
            sl_price = self.df["Close"][i] * (1+self.sl)
            from_time = self.df["Open Time"][i]
            to_time = min(self.df["Open Time"][i] + pd.Timedelta(minutes=self.max_time),self.df["Open Time"][len(self.df) - 1])
            self.df["Returns"][i] = self.calculator.calculate(from_time,to_time,target_price,sl_price) - self.fees # Fees
            if self.df["Returns"][i] > 0:
                wins += 1
            else:
                losses += 1

    def short_trades(self):
        wins = 0 
        losses = 0
        for i in np.where( (self.df["Sell"] == 1) )[0]:
            target_price = self.df["Close"][i] * (1-self.target)
            sl_price = self.df["Close"][i] * (1-self.sl)
            from_time = self.df["Open Time"][i]
            to_time = min(self.df["Open Time"][i] + pd.Timedelta(minutes=self.max_time),self.df["Open Time"][len(self.df) - 1])
            self.df["Returns"][i] = self.calculator.calculate(from_time,to_time,target_price,sl_price,trade="short") - self.fees # Fees
            if self.df["Returns"][i] > 0:
                wins += 1
            else:
                losses += 1