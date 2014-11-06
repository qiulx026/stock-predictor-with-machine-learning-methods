
import numpy as np
import copy

class KNNLearner:
    def __init__(self, k):
        self.k=k
               

    def addEvidence(self, Xin, Yin):
        if (len(Xin)!= len(Yin)):
            print ' error: data_X_train is not matched with data_Y_train'
            exit(0)
        else:
            self.x=Xin.copy()
            self.y=Yin.copy()

            
    def query(self, xtest):
        self.data=np.column_stack((self.x, self.y))
        self.ytest=np.zeros(xtest.shape[0])
        i=0
        for testp in xtest:
            distance=np.zeros(self.x.shape[0])
            j=0
            for trainp in self.x:
                distance[j]=np.sum((trainp-testp)**2)
                j=j+1
            distance_data = np.column_stack((self.data, np.array(distance)))
            distance_data = distance_data[distance_data[:,3].argsort()]
            self.ytest[i]=np.mean(distance_data[0:self.k,2])
            i=i+1
        return self.ytest




                                  
