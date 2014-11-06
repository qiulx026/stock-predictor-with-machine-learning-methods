import numpy as np
import numpy
import math
import copy
import datetime as dt

class RandomForestLearner(object):


    def __init__(self, k=3):
        self.k = k
        self.trees = list()

    def addEvidence(self, Xtrain, Ytrain):
        self.xdata = Xtrain
        self.ydata = Ytrain
        self.data = np.column_stack((self.xdata, self.ydata))
        ceiling = math.ceil(self.ydata.size*.6)
        indeces = np.arange(self.ydata.size)

        for i in range(0,self.k):
            numpy.random.shuffle(indeces)
            tree = generateTree(self.xdata[indeces[0:ceiling],:], self.ydata[indeces[0:ceiling]])
            self.trees.append(tree) 


    def query(self, xtest):
        self.ytest=np.zeros(xtest.shape[0])
        j=0
        for testp in xtest:
            sum = 0
            for i in range(0, self.k):
                sum += queryTree(self.trees[i], testp)
            self.ytest[j]=(sum/self.k)
            j+=1
        return self.ytest

    def getName(self):
        print ("====Random Forest Learner: K = %s====" %(self.k))
        pass
        

def generateTree(Xtrain, Ytrain):
        data = np.column_stack((Xtrain, Ytrain))
        if Xtrain.shape[0] == 1:
            return np.array([-1, Ytrain[0], 0,0])

        factor_indeces = np.arange(Xtrain.shape[1])
        element_indeces = np.arange(Xtrain.shape[0])
        numpy.random.shuffle(factor_indeces)
        numpy.random.shuffle(element_indeces)
       
        random_factor = factor_indeces[0]
        split_val = np.mean(Xtrain[element_indeces[0:2],random_factor])

        left_subtree = [data[i] for i,x in enumerate(Xtrain) if x[random_factor] < split_val]
        right_subtree = [data[i] for i,x in enumerate(Xtrain) if x[random_factor] >= split_val]

        left_dtree = generateTree(np.array(left_subtree)[:,0:Xtrain.shape[1]], np.array(left_subtree)[:,Xtrain.shape[1]])
        right_dtree = generateTree(np.array(right_subtree)[:,0:Xtrain.shape[1]], np.array(right_subtree)[:,Xtrain.shape[1]])

        if left_dtree[0].size > 1:
            node = np.array([random_factor, split_val, 1, 1+left_dtree.shape[0]])
        else:
            node = np.array([random_factor, split_val, 1, 2])
        tree = np.row_stack((node, left_dtree))
        tree = np.row_stack((tree, right_dtree))
        return tree

def queryTree(tree, Xtest):
        i=0
        while tree[i][0] != -1:
            factor = int(tree[i][0])
            splitval = tree[i][1]
            if Xtest[factor] < splitval:
                i = i + 1
            else:
                i = i + tree[i][3]
 
        return tree[i][1]

def getflatcsv(fname):
    inf = open(fname)
    return numpy.array([map(float,s.strip().split(',')) for s in inf.readlines()])

def testgendata():
    fname = 'data-classification-prob.csv'
    querys = 1000
    data = getflatcsv(fname)

    xpoints = np.array(data[0:100,0:2])
    ypoints = np.array(data[0:100,2])
    learner = RandomForestLearner(k=28)
    learner.addEvidence(xpoints,ypoints)
    tree = generateTree(xpoints,ypoints)  
    print tree
    res = learner.query(xpoints)
    print res
   

def test():
    testgendata()

if __name__=="__main__":
    test()
