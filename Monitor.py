import pandas as pd
import numpy as np
from tensorflow import keras
from BinanceCollector import BinanceCollector
from TradeBook import TradeBook
import warnings
warnings.filterwarnings("ignore")
from BreakdownCalculator import BreakdownCalculator
from BinanceSync import BinanceSync
from HyperBacktest import HyperBacktest
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from SlackCron import SlackCron

start = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
end = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
symbol = "ETHUSDT"
interval = "15m"

collector = BinanceCollector(symbol,start,end,interval)
collector.start_collect()
collector.df.columns = ["Open Time","Open","High","Low","Close","Volume","Close Time",
             "Quote asset volumne","Total Trades","Buyer Base Volume",
             "Taker buy quote asset volume","Ignore"]
df = collector.df
df["Open Time"] = pd.to_datetime(df["Open Time"],unit="ms")
df["Close Time"] = pd.to_datetime(df["Close Time"],unit="ms")
target = 4
sl = 2

cron = SlackCron()

done = False
while True:
    # Change according to interval
    if (datetime.now().minute-1)%15 != 0:
        done = False
        continue
    if done:
        continue
    print("Startng sync...")
    sync = BinanceSync(df,symbol,interval)
    sync.sync()
    df = sync.df
    df["EMA_20"] = df["Close"].ewm(span=20,adjust=False).mean()
    df["EMA_50"] = df["Close"].ewm(span=50,adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200,adjust=False).mean()
    df["Buy"] = np.where( (df["EMA_20"] > df["EMA_50"]) & (df["EMA_20"].shift(1) <= df["EMA_50"].shift(1) ),1,0 )
    df["Sell"] = np.where( (df["EMA_20"] < df["EMA_50"]) & (df["EMA_20"].shift(1) >= df["EMA_50"].shift(1) ),1,0 )
    print(df.iloc[-1])
    print("Synced!")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'time':time
    }
    if df.iloc[-1]["Buy"] == 1:
        print(f"Buy Signal at {df.iloc[-1]['Close Time']}")
        data['Signal'] = "Buy"
        data["Close Price"] = df.iloc[-1]["Close"]
        data["Target"] = df.iloc[-1]["Close Price"] + target*df.iloc[-1]["Close Price"]
        data["Stop Loss"] = df.iloc[-1]["Close Price"] - sl*df.iloc[-1]["Close Price"]
        cron.send(data)
    if df.iloc[-1]["Sell"] == 1:
        print(f"Sell Signal at {df.iloc[-1]['Close Time']}")
        data['Signal'] = "Sell"
        data["Close Price"] = df.iloc[-1]["Close"]
        data["Target"] = df.iloc[-1]["Close Price"] - target*df.iloc[-1]["Close Price"]
        data["Stop Loss"] = df.iloc[-1]["Close Price"] + sl*df.iloc[-1]["Close Price"]
        cron.send(data)
    done = True