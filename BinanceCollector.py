#!/usr/bin/env python
# coding: utf-8

# In[16]:


import os
import requests
from datetime import datetime,timedelta,date
import shutil
import numpy as np
import pandas as pd


# In[74]:


class BinanceCollector:
    def __init__(self,asset,start_date,end_date,interval):
        self.start = start_date
        self.end = end_date
        self.asset = asset
        self.interval = interval
        self.url = f"https://data.binance.vision/data/spot/daily/klines/{self.asset}/{self.interval}/"
        tmp = start_date.split("-")
        self.date = date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
        
        if not os.path.isdir("Data"):
            os.mkdir("Data")
    
    def make_url(self,date):
        return self.url+f"{self.asset}-{self.interval}-{date}.zip"
    
    def check(self,date):
        if os.path.isfile(f"Data/{self.asset}-{self.interval}-{date}.zip"):
            return True
        else:
            return False
    
    def construct_date(self,date_obj):
        year = 0
        month = 0
        day = 0
        if len(str(date_obj.month)) == 2:
            month = date_obj.month
        else:
            month = "0"+str(date_obj.month)

        if len(str(date_obj.day)) == 2:
            day = date_obj.day
        else:
            day = "0"+str(date_obj.day)
        
        return f"{date_obj.year}-{month}-{day}"
        
    def start_collect(self):
        self.df = []
        date = self.construct_date(self.date)
        while date != self.end:
            name = f"./Data/{self.asset}-{self.interval}-{date}.zip"
            url = self.make_url(date)
#             print(url)
            if not self.check(date):
                r = requests.get(url,verify=False,allow_redirects=True)
                with open(name,"wb") as f:
                    f.write(r.content)
                shutil.unpack_archive(name,"./Data")
#                 print(name)
            tmp = pd.read_csv(f"./Data/{self.asset}-{self.interval}-{date}.csv")
#             print(tmp)
            self.df.append(np.array(tmp))
            self.date += timedelta(days=1)
            date = self.construct_date(self.date)
            
        self.df = np.concatenate(self.df)
        self.df = pd.DataFrame(self.df)

# In[78]:


# obj = BinanceCollector("APEUSDT","2022-12-16","2022-12-18","15m")


# In[79]:


# obj.start_collect()
# https://data.binance.vision/data/spot/daily/klines/APEUSDT/15m/APEUSDT-15m-2022-12-17.zip
# https://data.binance.vision/?prefix=data/spot/daily/klines/APEUSDT/15m/APEUSDT-15m-2022-12-16.zip


# In[80]:


# shutil.unpack_archive("./Data/APEUSDT-15m-2022-12-17.zip","./Data")


# In[ ]:





# In[ ]:




