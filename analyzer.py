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
import math
import copy

    
def simulater(ldt_timestamps, money, filename1, filename2):
    cash = float(money)
    value_everyday = dict()    
    symbols_equity = dict()
    
    reader= csv.reader(open(filename1,'rU'),delimiter=',')
    for elements in reader:      
        symbols_equity[(elements[3])]=0
        
    ls_symbols= symbols_equity.keys()
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    price_data = d_data['close']

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
        
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

def sharpratio(ldt_timestamps, ls_symbols, ls_allocation):
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
        
def valuesharp(ldt_timestamps, arg4 ):
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ls_symbols = ['$SPX']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols,ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    na_price = d_data['close'].values

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

def eventfund(ldt_timestamps, arg2):
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
        
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    ldt_timestamps = df_close.index

    writer = csv.writer(open(arg2,'wb'),delimiter=',')
    for i in range(1, len(ldt_timestamps)):
        for s_sym in ls_symbols:
            if df_close[s_sym].ix[ldt_timestamps[i]]<7.0 and df_close[s_sym].ix[ldt_timestamps[i-1]]>=7.0 :
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                if i< (len(ldt_timestamps) -5):
                    date_time_split=ldt_timestamps[i].timetuple()
                    row_to_enter = [date_time_split[0],date_time_split[1],date_time_split[2],s_sym,'Buy',100]
                    writer.writerow(row_to_enter)
                    date_time_split=ldt_timestamps[i+5].timetuple()
                    row_to_enter = [date_time_split[0],date_time_split[1],date_time_split[2],s_sym,'Sell',100]
                    writer.writerow(row_to_enter)
                else:
                    date_time_split=ldt_timestamps[i].timetuple()
                    row_to_enter = [date_time_split[0],date_time_split[1],date_time_split[2],s_sym,'buy',100]
                    writer.writerow(row_to_enter)
                    date_time_split=ldt_timestamps[len(ldt_timestamps)-1].timetuple()
                    row_to_enter = [date_time_split[0],date_time_split[1],date_time_split[2],s_sym,'sell',100]
                    writer.writerow(row_to_enter)      
       
    
def main():
    ''' Main Function'''
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]

    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    eventfund(ldt_timestamps,arg2)
    
    simulater(ldt_timestamps,arg1,arg2,arg3)

    sharpr_spx=sharpratio(ldt_timestamps,['$SPX'],[1.0])

    sharp_value=valuesharp(ldt_timestamps, arg3)

    print "\nsharp ratio of Fund:\t",sharp_value[0],"\nsharp ratio of $SPX:\t",sharpr_spx[0]
    print "\n\nTotal Return of Fund:\t",sharp_value[1],"\nTotal Return of $SPX:\t",sharpr_spx[1]
    print "\n\nStandard Deviation of Fund:\t",sharp_value[2],"\nStandard Deviation of $SPX:\t",sharpr_spx[2]
    print "\n\nAverage Daily Return of Fund:\t",sharp_value[3],"\nAverage Daily Return of $SPX:\t",sharpr_spx[3]      
    

if __name__ == '__main__':
    main()
