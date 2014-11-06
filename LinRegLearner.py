import numpy as np
import math, copy



class LinRegLearner:

    def __init__(self):
        print 'hi'
        
    def addEvidence(self, Xin, Yin):
        if (len(Xin)!= len(Yin)):
            print ' error: data_X_train is not matched with data_Y_train'
            exit(0)
        else:
            self.x = Xin.copy()
            self.y = Yin.copy()
            lin_x =np.column_stack((self.x,np.ones(self.x.shape[0])))
            self.parameter = np.linalg.lstsq(lin_x, self.y)[0]
                
                
    def query(self, Xtest):
        lin_xtest=np.column_stack((Xtest,np.ones(Xtest.shape[0])))
        ytest=np.dot(lin_xtest, self.parameter)
        return ytest


