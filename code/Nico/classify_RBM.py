'''
Created on Nov 17, 2013

@author: nicodjimenez
'''

import os
import pickle
from sklearn import svm, grid_search
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors, datasets

from read_data import load_feature_file

file_name = "rbm_250"
[f,data] = load_feature_file(file_name)
(X,Y,symbol) = data

X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=0)

# parameter search for best SVM 
# param_grid = [
#    {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#    {'C': [1, 10, 100, 1000], 'gamma': [0.001,0.0001], 'kernel': ['rbf']},
#   ]
# 
# svr = svm.SVC()
# clf = grid_search.GridSearchCV(svr, param_grid)

clf = svm.SVC(kernel="linear",C=10000)


# Training RBM-Logistic Pipeline
clf.fit(X_train, Y_train)

###############################################################################
# Evaluation
print("SVM regression using raw pixel features:\n%s\n" % (
    metrics.classification_report(
        Y_test,
        clf.predict(X_test))))

#print svr.get_params()

#with open("../pickle_files/RBM_classifier.p",'wb') as f:
#    pickle.dump(classifier, f, protocol=0)  

###############################################################################
