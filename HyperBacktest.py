import pandas as pd
import numpy as np
from datetime import datetime

class HyperBacktest:
    def __init__(self,target,sl,calculator,df,max_time=1*24*60,long=True,short=True
                ,fees=0.1,leverage=1,simultaneous_trades=2):
        self.target = target/100
        self.sl = sl/100
        self.calculator = calculator
        self.df = df.copy()
        self.max_time = max_time
        self.fees = fees
        self.long = long
        self.short = short
        self.leverage = leverage
        self.simultaneous_trades = simultaneous_trades
        self.df["End"] = 0

    def run(self):
        if self.long:
            self.long_trades()
        if self.short:
            self.short_trades()
        
        # self.df["Gap"] = 0
        # self.df[ (self.df["End"] != 0) & (self.df["Returns"] != 0) ]["Gap"] = (self.df[ (self.df["End"] != 0) & (self.df["Returns"] != 0) ]["Open Time"] - self.df[ (self.df["End"] != 0) & (self.df["Returns"] != 0) ]["End"].shift(self.simultaneous_trades).fillna(datetime.now())).apply(lambda x: x.total_seconds()/60)
        # for i in range(self.simultaneous_trades):
        #     self.df["Gap"][i] = 0

        self.df = self.df[ self.df["Returns"] != 0 ]
        self.df["Gap"] = (self.df["Open Time"] - self.df["End"].shift(self.simultaneous_trades).fillna(datetime.now())).apply(lambda x: x.total_seconds()/60)
        print(f"Before Drop: {len(self.df)}")
        self.df = self.df.drop( self.df[ self.df["Gap"] < 0 ].index )
        print(f"After Drop: {len(self.df)}")

    def long_trades(self):
        wins = 0
        losses = 0
        for i in np.where( (self.df["Buy"] == 1) )[0]:
            target_price = self.df["Close"][i] * (1+self.target)
            sl_price = self.df["Close"][i] * (1+self.sl)
            from_time = self.df["Open Time"][i]
            to_time = min(self.df["Open Time"][i] + pd.Timedelta(minutes=self.max_time),self.df["Open Time"][len(self.df) - 1])
            # print(f"From: {from_time} \nTo: {to_time}")
            # print("------------------")
            self.df["Returns"][i] = self.calculator.calculate(from_time,to_time,target_price,sl_price) * self.leverage - self.fees # Fees
            # print(self.calculator.end)
            self.df["End"][i] = self.calculator.end
            if type(self.calculator.end) != pd.Timestamp:
                self.tmp = self.calculator.df_main
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
            self.df["Returns"][i] = self.calculator.calculate(from_time,to_time,target_price,sl_price,trade="short") * self.leverage - self.fees # Fees
            # print(self.calculator.end)
            self.df["End"][i] = self.calculator.end
            if type(self.calculator.end) != pd.Timestamp:
                self.tmp = self.calculator.df_main
            if self.df["Returns"][i] > 0:
                wins += 1
            else:
                losses += 1