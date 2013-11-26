'''
Created on Nov 18, 2013

@author: nicodjimenez

Looks at SVM classifier and sees where it goes wrong.  
'''

import matplotlib.pyplot as plt
import os
import cPickle as pickle
from sklearn import svm,grid_search

from skimage.feature import hog
from skimage import data, color, exposure

from read_data import load_data, load_feature_file
from process_strokes import FULL_DIM
from sklearn.externals import joblib

hog_file_name = "HOG_clean_symbols_45"

# load SVM
print "Loading SVM..."
file_output = "../pickle_files/classifiers/SVM_" +  hog_file_name + ".p" 
clf = joblib.load(file_output)

# load features
print "Loading features..."
[f_hog,data_hog] = load_feature_file(hog_file_name)
(X_HOG,Y,symbol) = data_hog

# construct dictionary
ind_to_sym = dict(zip(Y,symbol))
#print ind_to_sym.keys()

# load original data 
print "Loading original data..."
file_name = "clean_symbols_45"
[f,data] = load_feature_file(file_name)
(X,Y,symbol) = data

print "Starting iteration!!!"
for (ind,X_HOG_cur) in enumerate(X_HOG):
    Y_predict = clf.predict(X_HOG_cur)[0]
    #dec = clf.decision_function(X_HOG_cur)
    
    #if True == True:
    if Y_predict != Y[ind]:
        print "Index: ", ind
        
        # get top other classes
        log_prob = clf.predict_proba(X_HOG_cur)[0]
        #print log_prob
        
        top_index_list = [1 + i[0] for i in sorted(enumerate(log_prob), key=lambda x:x[1])]
        top_index_list.reverse()
        #print log_prob[top_index_list[0:5]]
        
        for guess_ind in top_index_list[0:5]: 
            print ind_to_sym[guess_ind]
        
        # get wrong label 
        sym_wrong = ind_to_sym[Y_predict]
        sym_right = ind_to_sym[Y[ind]]
        sym_str = sym_wrong + " instead of " + sym_right
        
        # plot figure
        x = X[ind]
        img = x.reshape((FULL_DIM,FULL_DIM)) * 1.0
        plt.imshow(img)
        plt.title(sym_str)
        plt.show()
        