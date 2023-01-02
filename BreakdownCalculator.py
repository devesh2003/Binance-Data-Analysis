import pandas as pd
import numpy as np

class BreakdownCalculator:
    def __init__(self,df):
        open_time = pd.to_datetime(df["Open Time"], unit="ms")
        df = df[["Open","High","Low","Close"]]
        # df = (df - df.mean())/df.std()
        df["Open Time"] = open_time
        self.df = df

    def calculate(self,_from,_to,target,sl,trade="buy"):
        df = self.df
        start_index = df[ df["Open Time"] == _from ].index[0]
        open_price = df["Close"][start_index]
        end_index = df[ df["Open Time"] == _to ].index[0]
        last_price = df["Open"][end_index]
        df = df[start_index:end_index]
        if trade == "buy":
            df["TP_Diff"] = target - df["High"]
            df["SL_Diff"] = df["Low"] - sl
            tp_time = np.append(np.where( df["TP_Diff"] <= 0 )[0],99999999)[0]
            sl_time = np.append(np.where( df["SL_Diff"] <= 0 )[0],99999999)[0]
            self.df_main = df
            # Profit
            if tp_time < sl_time:
                return ( (target - open_price)*100/open_price )
            # Loss
            elif tp_time > sl_time:
                return ( (sl - open_price)*100/open_price  )
            
            return ( (last_price - open_price)*100/open_price )
        else:
            df["TP_Diff"] = df["Low"] - target
            df["SL_Diff"] = sl - df["High"]
            tp_time = np.append(np.where( df["TP_Diff"] <= 0 )[0],99999999)[0]
            sl_time = np.append(np.where( df["SL_Diff"] <= 0 )[0],99999999)[0]
            self.df_main = df
            # Profit
            if tp_time < sl_time:
                return ( (open_price - target)*100/open_price )
            # Loss
            elif tp_time > sl_time:
                return ( (open_price - sl)*100/open_price  )
            
            return ( (open_price - last_price)*100/open_price )