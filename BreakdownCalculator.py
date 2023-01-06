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
        df = self.df.copy()
        start_index = df[ df["Open Time"] == _from ].index[0]
        open_price = df["Close"][start_index]
        end_index = df[ df["Open Time"] == _to ].index[0]
        last_price = df["Open"][end_index]
        df = df[start_index:end_index]
        df.reset_index(inplace=True)
        if trade == "buy":
            df["TP_Diff"] = target - df["High"]
            df["SL_Diff"] = df["Low"] - sl
            tp_time = np.append(np.where( df["TP_Diff"] <= 0 )[0],99999999)[0]
            sl_time = np.append(np.where( df["SL_Diff"] <= 0 )[0],99999999)[0]
            self.df_main = df
            # Profit
            if tp_time < sl_time:
                self.end = df["Open Time"][tp_time]
                # print(f"Profit\n{self.end}")
                # print("------------------")
                return ( (target - open_price)*100/open_price )
            # Loss
            elif tp_time > sl_time:
                self.end = df["Open Time"][sl_time]
                # print(f"Loss\n{self.end}")
                # print("------------------")
                return ( (sl - open_price)*100/open_price  )
            
            self.end = df["Open Time"][len(df) - 1]
            # print(f"Force Close\n{self.end}")
            # print("------------------")
            return ( (last_price - open_price)*100/open_price )
        else:
            df["TP_Diff"] = df["Low"] - target
            df["SL_Diff"] = sl - df["High"]
            tp_time = np.append(np.where( df["TP_Diff"] <= 0 )[0],99999999)[0]
            sl_time = np.append(np.where( df["SL_Diff"] <= 0 )[0],99999999)[0]
            self.df_main = df
            # Profit
            if tp_time < sl_time:
                self.end = df["Open Time"][tp_time]
                # print(f"Profit\n{self.end}")
                # print("------------------")
                return ( (open_price - target)*100/open_price )
            # Loss
            elif tp_time > sl_time:
                self.end = df["Open Time"][sl_time]
                # print(f"Loss\n{self.end}")
                # print("------------------")
                return ( (open_price - sl)*100/open_price  )
            
            self.end = df["Open Time"][len(df) - 1]
            # print(f"Force Close\n{self.end}")
            # print("------------------")
            return ( (open_price - last_price)*100/open_price )