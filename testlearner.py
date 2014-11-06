from KNNLearner import KNNLearner as knn
from RandomForestLearner import RandomForestLearner as Ran

import numpy as np
import math, copy, time
import matplotlib.pyplot as plt
from pylab import *


def getflatcsv(fname):
    inf = open(fname)
    return np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

def filetest(fname):

    data = getflatcsv(fname)
    print data.shape
    test_length = .6*data.shape[0]
    RandomError =  np.zeros(101)
    RandomCorre =  np.zeros(101)
    KnnError = np.zeros(101)
    KnnCorre = np.zeros(101)
    
    xpoints = data[0:test_length,0:2]
    ypoints = data[0:test_length,2]

    Xtestset = data[test_length: ,0:2]
    Ytestset = data[test_length: ,2]
    
    set_length = Xtestset.shape[0]
    
    for k in range(2,3):
    
        learner1=Ran(k)        
        learner1.addEvidence(xpoints,ypoints)             
        y = learner1.query(Xtestset)         

        corrcoeff1 = np.corrcoef(np.array(y),Ytestset)
        RandomCorre[k] = corrcoeff1[0,1]
        RandomError[k] =  np.sqrt(np.mean((np.array(y) - Ytestset)**2))

        learner2=knn(k)
        learner2.addEvidence(xpoints,ypoints)             
        y = learner2.query(Xtestset)         

        corrcoeff1 = np.corrcoef(np.array(y),Ytestset)
        KnnCorre[k] = corrcoeff1[0,1]
        KnnError[k] =  np.sqrt(np.mean((np.array(y) - Ytestset)**2))
        
    plt.clf()
    plt.plot(np.column_stack((RandomError,KnnError)))
    plt.legend(['random','knn'])
    plt.ylabel('%s RMSE' %fname)
    plt.xlabel("k values")
    plt.axis([1, 99, 0, 1])
    plt.savefig('%s RFRMSE.pdf' %fname,format='pdf')
    
    plt.clf()
    plt.plot(np.column_stack((RandomCorre,KnnCorre)))
    plt.legend(['random','knn'])
    plt.ylabel('%s Correlation' %fname)
    plt.xlabel("k values")
    plt.axis([1, 99, 0, 1])
    plt.savefig('%s RFcorrelation.pdf' %fname,format='pdf')
    




filetest("data-classification-prob.csv" )
filetest("data-ripple-prob.csv")
