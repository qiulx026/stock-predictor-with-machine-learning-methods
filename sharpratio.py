# -*- coding: cp936 -*-
'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Example tutorial code.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

print "Pandas Version", pd.__version__

def simulate(dt_start, dt_end, ls_symbols, ls_allocation):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    na_price = d_data['close'].values

    na_normalized_price = na_price / na_price[0, :]

    multy_price = na_normalized_price.copy()
    sum_price = multy_price[ : , ] * ls_allocation
    sum_daily_return=sum_price.copy()
    tsu.returnize0(sum_daily_return)
    sum_mean_daily_return=np.mean(sum_daily_return)
    sum_std_daily_return=np.std(sum_daily_return)
    k=np.sqrt(252)
    sharpratio=k*sum_mean_daily_return/sum_std_daily_return

    #na_rets = na_normalized_price.copy()
    cum_daily_return=sum_daily_return.copy()
    cum_daily_return[0]=1
    for i in range(1,len(cum_daily_return)):
        cum_daily_return[i]=cum_daily_return[i-1]*(1+cum_daily_return[i])  

    #print "normalized price \n",na_normalized_price,"\nmean daily return\n",sum_mean_daily_return,"\nsum daily return\n",sum_daily_return,"\nsharpratio\n",sharpratio,"\ncumdaily\n",cum_daily_return
    return sharpratio

sharpratio=-1;
ls_symbols =     ['BRCM', 'TXN', 'IBM', 'HNZ'] 
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
for i in range (0,11):
    for j in range (0,11-i):
        for k in range (0,11-i-j):
            l=10-i-j-k
            sharpratio1=simulate(dt_start,dt_end,ls_symbols,(0.1*i,0.1*j,0.1*k,0.1*l))
            if sharpratio1>sharpratio:
                sharpratio=sharpratio1
                ls_allocation=[0.1*i,0.1*j,0.1*k,0.1*l]

print "sharpratio\n",sharpratio,"\nallocation\n",ls_allocation,ls_symbols

                    


