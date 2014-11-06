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


def main():
    ''' Main Function'''
    ls_symbols = ["AAPL","GOOG" ,"IBM" ,"MSFT"]
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
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
    na_price = d_data['actual_close'].values

    band=na_price.copy()


    for j in range(0,len(ls_symbols)):    
        band_mean=pd.rolling_mean(na_price,20)
        band_std=pd.rolling_std(na_price,20)
        for i in range(0,len(ldt_timestamps)):
            band[i,j]=(na_price[i,j]-band_mean[i,j])/band_std[i,j]
    for i in range(0,len(ldt_timestamps)):
        print ldt_timestamps[i],band[i]
        
if __name__ == '__main__':
    main()













