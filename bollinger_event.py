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
import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
import math

print "Pandas Version", pd.__version__

def band_value(ls_symbols, ldt_timestamps):
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    band=na_price.copy()

    for j in range(0,len(ls_symbols)):    
        band_mean=pd.rolling_mean(na_price,20)
        band_std=pd.rolling_std(na_price,20)
        for i in range(0,len(ldt_timestamps)):
            band[i,j]=(na_price[i,j]-band_mean[i,j])/band_std[i,j]
            
    return band


def find_events(ls_symbols, d_data,ldt_timestamps ):
    df_close = d_data['close']
    ts_market = df_close['SPY']
    count=0
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    
    spy_band=band_value(['SPY'],ldt_timestamps)
    
    for s_sym in ls_symbols:
        sym_band=band_value([s_sym],ldt_timestamps)
        for i in range(20, len(ldt_timestamps)):           
            if sym_band[i] < -2.0 and sym_band[i-1] >= -2.0 and spy_band[i] >= 1.5:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                count = count+1
    print count       

    return df_events
    
def main():
    ''' Main Function'''
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    #ls_symbols = ["AAPL","GOOG" ,"IBM" ,"MSFT"]
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events=find_events(ls_symbols, d_data, ldt_timestamps)
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,s_filename='bollinger_1.5_2012.pdf', b_market_neutral=True, b_errorbars=True, s_market_sym='SPY')

    
    
        
if __name__ == '__main__':
    main()













