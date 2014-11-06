# -*- coding: cp936 -*-
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, csv, sys
from RandomForestLearner import RandomForestLearner as Ran

DAYS_LOOKBACK = 21
DAYS_PREDICT = 5

def readCSV(filename):
  with open(filename, 'r') as f:
    a = [float(s.strip().split(',')[-1]) for s in f.readlines()[1:]]
    a.reverse()
    return np.array(a)

def getflatcsv(fname):
    inf = open(fname)
    return np.array([map(float,s.strip().split(',')) for s in inf.readlines()])  
  
def getMean(data):
  return [(data[i-DAYS_LOOKBACK:i].mean()-data[i]) for i in range(DAYS_LOOKBACK, data.size)]

def getStdDev(data):
  return [np.std(data[i-DAYS_LOOKBACK:i]) for i in range(DAYS_LOOKBACK, data.size)]

def getFreqeuncy(data):
  cnts = []
  for i in range(DAYS_LOOKBACK, data.size):
    data1 = data[i-DAYS_LOOKBACK:i]
    mean = data1.mean()
    cnt = 0
    for j in range(1, len(data1)):
      if (data1[j] > mean and data1[j-1] <= mean) or (data1[j] <= mean and data1[j-1] > mean):
        cnt += 1
    cnts.append(cnt)
  return cnts

def getSlop(data):
  return [(data[i] - data[i-1]) for i in range(DAYS_LOOKBACK, data.size)]

def getSlope20(data):
  return [(data[i] - data[i-20]) for i in range(DAYS_LOOKBACK, data.size)]


def getDelta(data):
  deltas = []
  for i in range(DAYS_LOOKBACK, data.size):
    data1 = data[i-DAYS_LOOKBACK:i]
    mean = data1.mean()
    total = 0.0
    for datum in data1:
      total += abs(datum)
    deltas.append(total)
  return deltas

def getPrice(data):
  return [(data[i+5] - data[i]) for i in range(DAYS_LOOKBACK, data.size-5)]

def getRealPrice(data):
  return [(data[i+5]) for i in range(DAYS_LOOKBACK, data.size-5)]

def process(filename):
  data = readCSV(filename)
  #mean = getMean(data)
  stddev = getStdDev(data)
  #freqency = getFreqeuncy(data)
  slop = getSlop(data)
  #slope20 = getSlope20(data)
  price = getPrice(data)
  X = []
  for i in range(len(price)):
    X.append(tuple([ stddev[i], slop[i]]) )
  return X, price



def filetest(trainfname, testfname, testfname1):

    print trainfname
    data = getflatcsv(trainfname)
    print data.shape
    test_length = data.shape[0]
    RandomError =  np.zeros(101)
    RandomCorre =  np.zeros(101)
    
    xpoints = data[0:test_length,0:2]
    ypoints = data[0:test_length,2]
    print 'train set'

    data1 = getflatcsv(testfname)
    print data1.shape
    test_length = data1.shape[0]
    Xtestset = data1[0:test_length,0:2]
    Ytestset = data1[0:test_length,2]
    print 'test set'    
    data2 = readCSV('proj3-data/ML4T-292.csv')  
    bench = getRealPrice(data2)
    f1=getStdDev(data2)
    f2=getSlop(data2)  
    learner = Ran(40)
    learner.addEvidence(xpoints,ypoints)
    
    print 'learned'
    y = learner.query(Xtestset)         
    print 'queryed'
    Ytestset+=bench
    y+=bench
    print len(bench),len(Ytestset),len(y)
    corrcoeff1 = np.corrcoef(np.array(y),Ytestset)
    RandomCorre[0] = corrcoeff1[0,1]
    RandomError[0] =  np.sqrt(np.mean((np.array(y) - Ytestset)**2))
    print RandomCorre[0]
    print RandomError[0]


    data3 = getflatcsv(testfname1)
    print data3.shape
    test_length = data3.shape[0]
    Xtestset1 = data3[0:test_length,0:2]
    Ytestset1 = data3[0:test_length,2]
    print 'test set1'    
    data4 = readCSV('proj3-data/ML4T-129.csv')
    bench1 = getRealPrice(data4)
    f3=getStdDev(data4)    
    f4=slop = getSlop(data4)


    y1 = learner.query(Xtestset1)         
    Ytestset1+=bench1
    y1+=bench1
    print len(bench1),len(Ytestset1),len(y1)
    corrcoeff1 = np.corrcoef(np.array(y1),Ytestset1)
    RandomCorre[1] = corrcoeff1[0,1]
    RandomError[1] =  np.sqrt(np.mean((np.array(y1) - Ytestset1)**2))
    print RandomCorre[1]
    print RandomError[1]

    days = [i for i in range(100)]    
    plt.clf()
    plt.plot(days, y[:100], 'r', label='Ypredict')
    plt.plot(days, Ytestset[:100], 'b', label='Yactual')
    plt.legend()
    plt.title('ML4T-292.csv-first-100days')
    plt.savefig('ML4T-292.csv-first-100days' ,format='pdf')

    days = [i for i in range(100)]    
    plt.clf()
    plt.plot(days, y[len(y)-100:len(y)], 'r', label='Ypredict')
    plt.plot(days, Ytestset[len(y)-100:len(y)], 'b', label='Yactual')
    plt.legend()
    plt.title('ML4T-292.csv-last-100days')
    plt.savefig('ML4T-292.csv-last-100days' ,format='pdf')
            
    plt.clf()
    plt.plot(days, y1[:100], 'r', label='Ypredict')
    plt.plot(days, Ytestset1[:100], 'b', label='Yactual')
    plt.legend()
    plt.title('ML4T-129.csv-first-100days')
    plt.savefig('ML4T-129.csv-first-100days' ,format='pdf')
          
    plt.clf()
    plt.plot(days, y1[len(y)-100:len(y)], 'r', label='Ypredict')
    plt.plot(days, Ytestset1[len(y)-100:len(y)], 'b', label='Yactual')
    plt.legend()
    plt.title('ML4T-129.csv-last-100days')
    plt.savefig('ML4T-129.csv-last-100days' ,format='pdf')

    plt.clf()
    plt.plot(days, y1[len(y)-100:len(y)], 'r', label='Ypredict')
    plt.plot(days, Ytestset1[len(y)-100:len(y)], 'b', label='Yactual')
    plt.legend()
    plt.title('ML4T-129.csv-last-100days')
    plt.savefig('ML4T-129.csv-last-100days' ,format='pdf')
    
 
    plt.clf()
    plt.plot(days, f1[:100], 'r', label='stdev')
    plt.plot(days, f2[:100], 'b', label='slope')
    plt.legend()
    plt.title('ML4T-292.csv-features')
    plt.savefig('ML4T-292.csv-features',format='pdf')

    plt.clf()
    plt.plot(days, f3[:100], 'r', label='stdev')
    plt.plot(days, f4[:100], 'b', label='slope')
    plt.legend()
    plt.title('ML4T-129.csv-features')
    plt.savefig('ML4T-129.csv-features',format='pdf')

    plt.clf()
    plt.plot(y, Ytestset, 'r', label='Ypredict versus Yactual')
    plt.legend()
    plt.title('Ypredict versus Yactual')
    plt.ylabel('Ypredict')
    plt.xlabel("Yactual")
    plt.savefig('ML4T-292.csv-Ypredict versus Yactual',format='pdf')

    plt.clf()
    plt.plot(y1, Ytestset1, 'r', label='Ypredict versus Yactual')
    plt.legend()
    plt.title('Ypredict versus Yactual')
    plt.ylabel('Ypredict')
    plt.xlabel("Yactual")
    plt.savefig('ML4T-129.csv-Ypredict versus Yactual',format='pdf')

    
if __name__ == '__main__':
  filepathprefix = 'proj3-data/ML4T-%03d.csv'
  outfile = 'features-train.csv'  
  writer = csv.writer(open (outfile, 'wb'), delimiter=',')
  #writer.writerow(['mean', 'stddev', 'freqency', 'slop', 'delta', '5dayprice'])
  for i in range(100):
    filename = filepathprefix % i
    print filename
    X, Y = process(filename)
    for i in range(len(Y)):
      l = [str(x) for x in list(X[i])]
      l.append(str(Y[i]))
      writer.writerow(l)
  #outfile = 'features-test~.csv'  
  #writer = csv.writer(open (outfile, 'wb'), delimiter=',')
  outfile = 'features-test1.csv'  
  writer = csv.writer(open (outfile, 'wb'), delimiter=',')
  filename = 'proj3-data/ML4T-129.csv'
  print filename
  X, Y = process(filename)
  for i in range(len(Y)):
    l = [str(x) for x in list(X[i])]
    l.append(str(Y[i]))
    writer.writerow(l)
  filetest("features-train.csv","features-test.csv","features-test1.csv")

  
