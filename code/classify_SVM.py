'''
Created on Nov 17, 2013

@author: nicodjimenez
'''

import os
import pickle
from sklearn import svm, grid_search
from read_data import load_data, load_feature_file
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors, datasets
from sklearn.externals import joblib
from sklearn import preprocessing

file_name = "HOG_clean_symbols_45"
[f,data] = load_feature_file(file_name)
(X,Y,symbol) = data

#X = preprocessing.scale(X)


X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=0)

# parameter search for best SVM 
#param_grid = [
#   {'C': [1,100,10000], 'kernel': ['linear']},
#   #{'C': [1], 'gamma': [0.001,0.0001], 'kernel': ['rbf']},
#  ]

clf = svm.SVC(kernel="linear",C=1,probability=True)
#clf = grid_search.GridSearchCV(svr, param_grid)

clf.fit(X_train, Y_train)

###############################################################################
# Evaluation
print("SVM regression using HOG features:\n%s\n" % (
    metrics.classification_report(
        Y_test,
        clf.predict(X_test))))

print clf.get_params()
###############################################################################
# Storage 
file_output = "../pickle_files/classifiers/SVM_" +  file_name + ".p" 
joblib.dump(clf,file_output)
print "Successfully saved pickle file to: " + str(file_output)

# with open(file_output,'wb') as f:
#     pickle.dump(clf, f, protocol=0)  
#     print "Successfully saved pickle file to: " + str(file_output)
