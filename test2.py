# -*- coding: utf-8 -*-
"""
Created on Sat Jul 06 13:10:25 2019

@author: RKUSHWAHA-W10
"""
import numpy as np
import pandas as pd
import sys
import os
import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime as dt
from datetime import date, timedelta
import os

os.system('. /sparkclient/prod/svc_client/current/bin/include.sh')
os.umask(000)

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
from datetime import date, timedelta
import pandas as pd
import networkx as nx

class Network(object):
    def __init__(self,date, Data, rel_types = ["CUSTOMER"]):
        self.graph = nx.DiGraph()
        self.date = pd.to_datetime(date)
        self.df = Data[(Data.start_date<self.date) & (Data.end_date.isnull() | (Data.end_date >self.date))]
        self.df = self.df[(self.df.uid_src.notnull()) & (self.df.uid_tgt.notnull())]
        self.edges =  []
        for rel in rel_types:
            if rel == "CUSTOMER":
                self.edges =  self.edges + list(self.df[['uid_tgt','uid_src']].itertuples(index=False,name=None))
            if rel == "SUPPLIER":
                self.edges =  self.edges + list(self.df[['uid_src','uid_tgt']].itertuples(index=False,name=None))

        self.graph.add_edges_from(self.edges)

    def draw(self):
        nx.draw(self.graph)

    def Get_Customers(self,src_uid):
        return self.graph.neighbors(src_uid)

    def Size(self):
        return len(self.df.uid_src.unique())


def Get_Dates(Start_Date,End_Date):
    Start_Date =  pd.to_datetime(Start_Date)
    End_Date =  pd.to_datetime(End_Date)
    return [Start_Date + timedelta(days=x) for x in range((End_Date-Start_Date).days + 1)]


def Get_Matric(Start_Date, End_Date, uid, country  = 'total_cust'):
    df0 = pd.DataFrame()
    for Date in Get_Dates(Start_Date,End_Date)[0:50]:
        try:
            df1 = Network(Date, Data,rel_types = ["CUSTOMER","SUPPLIER"]).df
            df1 = df1[(df1.uid_tgt == uid)]

            total_cust = len(df1.uid_src.unique())
            df1 = pd.DataFrame(df1.Country_src.value_counts()).transpose()

            df1.index.name = 'Date'
            df1.index  = [Date]
            df1['other'] =  total_cust - df1.sum(axis = 1)
            df1['total_cust'] =  total_cust
            df0 = df0.append(df1)
        except:
            continue
    if country == 'total_cust':
        return df0
    else:
        return df0[country]
