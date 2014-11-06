# -*- coding: cp936 -*-
'''
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
import csv as csv
import sys as sys

    
def simulater(dt_start, dt_end, money, filename1, filename2):
    cash = float(money)
    value_everyday = dict()    
    symbols_equity = dict()
    
    reader= csv.reader(open(filename1,'rU'),delimiter=',')
    for elements in reader:      
        symbols_equity[(elements[3])]=0
        
    ls_symbols= symbols_equity.keys()

    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    price_data = d_data['close']
   
    for daytime in ldt_timestamps:
        value_everyday[daytime]=0
        reader= csv.reader(open(filename1,'rU'),delimiter=',') 
        for elements in reader:
            dt_time=dt.datetime(int(elements[0]),int(elements[1]),int(elements[2]),16)
            if daytime == dt_time:
                if elements[4]=="Buy":
                    symbols_equity[(elements[3])] += int(elements[5])
                    cash -= int(elements[5]) * price_data[elements[3]][daytime]
                if elements[4]=="Sell":
                    symbols_equity[(elements[3])] -= int(elements[5])
                    cash += int(elements[5]) * price_data[elements[3]][daytime]
        for symbol in ls_symbols:
            value_everyday[daytime] += symbols_equity[symbol] * price_data[symbol][daytime]
        value_everyday[daytime]+= cash

    writer = csv.writer(open(filename2,'wb'),delimiter=',')
    for daytime in ldt_timestamps:
        row_to_enter = [daytime,value_everyday[daytime]]
        writer.writerow(row_to_enter)

def sharpratio(dt_start, dt_end, ls_symbols, ls_allocation):
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

    #print na_normalized_price

    multy_price = na_normalized_price.copy()
    sum_price = 0
    
    for i  in range(0,len(ls_symbols)):
        sum_price  += multy_price[ : ,i ] * ls_allocation[i]
        i=i+1

    sum_daily_return=sum_price.copy()
    tsu.returnize0(sum_daily_return)
    sum_mean_daily_return=np.mean(sum_daily_return)
    sum_std_daily_return=np.std(sum_daily_return)
    k=np.sqrt(252)
    sharpratio=k*sum_mean_daily_return/sum_std_daily_return

    cum_daily_return=sum_daily_return.copy()
    cum_daily_return[0]=1
    for i in range(1,len(cum_daily_return)):
        cum_daily_return[i]=cum_daily_return[i-1]*(1+cum_daily_return[i])
    return sharpratio,cum_daily_return[len(cum_daily_return)-1],sum_std_daily_return,sum_mean_daily_return
        
def valuesharp(dt_start, dt_end, arg4 ):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ls_symbols = ['$SPX']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols,ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    na_price = d_data['actual_close'].values

    reader= csv.reader(open(arg4,'rb'),delimiter=',')
    i=0
    for key in reader:
        daytime=dt.datetime.strptime(key[0],"%Y-%m-%d %H:%M:%S")
        na_price[i]=[float(key[1])]
        i+=1
    sum_daily_return=na_price/na_price[0]
    tsu.returnize0(sum_daily_return)
    sum_mean_daily_return=np.mean(sum_daily_return)
    sum_std_daily_return=np.std(sum_daily_return)
    k=np.sqrt(252)
    sharpratio=k*sum_mean_daily_return/sum_std_daily_return
    cum_daily_return=sum_daily_return.copy()
    cum_daily_return[0]=1
    for i in range(1,len(cum_daily_return)):
        cum_daily_return[i]=cum_daily_return[i-1]*(1+cum_daily_return[i])
    return sharpratio,float(cum_daily_return[len(cum_daily_return)-1]),sum_std_daily_return,sum_mean_daily_return

def main():
    ''' Main Function'''
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    arg4 = sys.argv[4]

    value_ed=list()
    value_edd=list()
    value_price=dict()
    value_daily_return=list()

    dt_start = dt.datetime(2008, 2, 25)
    dt_end = dt.datetime(2009, 12, 30)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    simulater(dt_start,dt_end,arg1,arg2,arg3)

    sharpr_spx=sharpratio(dt_start,dt_end,['$SPX'],[1.0])

    sharp_value=valuesharp(dt_start, dt_end, arg4)

    print "\nsharp ratio of Fund:\t",sharp_value[0],"\nsharp ratio of $SPX:\t",sharpr_spx[0]
    print "\n\nTotal Return of Fund:\t",sharp_value[1],"\nTotal Return of $SPX:\t",sharpr_spx[1]
    print "\n\nStandard Deviation of Fund:\t",sharp_value[2],"\nStandard Deviation of $SPX:\t",sharpr_spx[2]
    print "\n\nAverage Daily Return of Fund:\t",sharp_value[3],"\nAverage Daily Return of $SPX:\t",sharpr_spx[3]

if __name__ == '__main__':
    main()
