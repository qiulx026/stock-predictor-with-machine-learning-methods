import numpy as np
import numpy
import math
import copy
import datetime as dt

def buildtrees(Xtrain, Ytrain):
        data = np.column_stack((Xtrain, Ytrain))
        if Xtrain.shape[0] == 1:
            return np.array([-1, Ytrain[0], 0,0])

        f = np.arange(Xtrain.shape[1])
        e = np.arange(Xtrain.shape[0])
        numpy.random.shuffle(f)
        numpy.random.shuffle(e)
       
        f= f[0]
        split_val = np.mean(Xtrain[e[0:2],f])

        left_data = [data[i] for i,x in enumerate(Xtrain) if x[f] < split_val]
        right_data = [data[i] for i,x in enumerate(Xtrain) if x[f] >= split_val]

        left_dtree = buildtrees(np.array(left_data)[:,0:Xtrain.shape[1]], np.array(left_data)[:,Xtrain.shape[1]])
        right_dtree = buildtrees(np.array(right_data)[:,0:Xtrain.shape[1]], np.array(right_data)[:,Xtrain.shape[1]])

        if left_dtree[0].size > 1:
            node = np.array([f, split_val, 1, 1+left_dtree.shape[0]])
        else:
            node = np.array([f, split_val, 1, 2])
        tree = np.row_stack((node, left_dtree))
        tree = np.row_stack((tree, right_dtree))
        return tree

class RandomForestLearner():
    def __init__(self, k=3):
        self.k = k
        self.forest = list()

    def addEvidence(self, Xtrain, Ytrain):
        self.xdata = Xtrain
        self.ydata = Ytrain
        self.data = np.column_stack((self.xdata, self.ydata))
        length = math.ceil(self.ydata.size*.001)
        indeces = np.arange(self.ydata.size)

        for i in range(0,self.k):
            numpy.random.shuffle(indeces)
            tree = buildtrees(self.xdata[indeces[0:length],:], self.ydata[indeces[0:length]])
            self.forest.append(tree) 


    def query(self, xtest):
        self.ytest=np.zeros(xtest.shape[0])
        j=0
        for testp in xtest:
            sum = 0
            for i in range(0, self.k):
                t=self.forest[i]
                p=0
                while t[p][0]!= -1:
                        f = int(t[p][0])
                        splitval = t[p][1]
                        if testp[f] < splitval:
                                p = p + 1
                        else:
                                p = p + t[p][3]
                        sum += t[i][1]
            self.ytest[j]=(sum/self.k)
            j+=1
        return self.ytest
        




