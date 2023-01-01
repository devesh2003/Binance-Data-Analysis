import numpy as np
import pandas as pd
import os

class TradeBook:
    def __init__(self,symbol,timeframe,interval,custom_fields=[]):
        self.symbol = symbol
        self.timeframe = timeframe
        self.interval = interval
        self.create_file(custom_fields=custom_fields)

    def create_file(self,custom_fields=[]):
        name = f"{self.symbol}_{self.interval}_{self.timeframe}.csv"
        if (not os.path.isdir(self.symbol)) and (self.symbol not in os.getcwd()):
            os.mkdir(self.symbol)
        # if self.symbol not in os.getcwd():   
        #     os.chdir(self.symbol)
        self.name = name
        with open(os.path.join(".",self.symbol,name),"w") as f:
            f.write("Entry Time,Entry,Exit,Exit Time,Result,"+",".join(custom_fields)+"\n")

    def add_entry(self,data):
        with open(os.path.join(".",self.symbol,self.name),"a") as f:
            f.write( ",".join(data)+"\n" )
        

