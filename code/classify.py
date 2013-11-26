'''
Created on Nov 12, 2013

@author: nicodjimenez

Classifies using SVM. 
'''

import os
import pickle
from sklearn import svm
from read_data import load_data

DUMP_LOCATION = "../pickle_files"

(X,symbol_ind,symbol) = load_data()

clf = svm.SVC(kernel='rbf',gamma=0.001)
clf.fit(X,symbol_ind)

save_filename = os.path.join(DUMP_LOCATION,"svm_clf.p")
with open(save_filename,'wb') as f:
    pickle.dump(clf, f, protocol=0)  
  
symbol_predict = clf.predict(X)

errors = 0
for ind in range(len(symbol_predict)):
    #print "Predicted: " + str(symbol_predict[ind])
    #print "Actual:  " + str(symbol_ind[ind])
    
    if symbol_predict[ind] != symbol_ind[ind]:
        errors += 1 
        
error_rate = errors * 1.0 / len(symbol_predict)
print "Error rate: " + str(error_rate) 



#SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
#gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
#shrinking=True, tol=0.001, verbose=False)