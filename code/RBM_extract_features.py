'''
Created on Nov 17, 2013

@author: nicodjimenez

This file will extract features vectors from data and save them to pickle files.

So far only does RBM.
'''

import os
import numpy as np
from sklearn.neural_network import BernoulliRBM
from read_data import load_feature_file
import cPickle as pickle


file_name = "clean_symbols_45"
[f,data] = load_feature_file(file_name)
(X,symbol_ind,symbol_list) = data

#(X,symbol_ind,symbol_list) = load_data()
rbm = BernoulliRBM(random_state=0, verbose=True)
rbm.learning_rate = 0.06
rbm.n_iter = 10

#components_arr = [50,100,500]
components_arr = [250]
feature_file_name = ["rbm_" + str(comp_ct) + ".p" for comp_ct in components_arr]

for ind in range(len(components_arr)):
    rbm.n_components = components_arr[ind]
    print "Number of components: " + str(rbm.n_components)
    rbm.fit(X)
    X_new = rbm.transform(X)
    dataset = (X_new,symbol_ind,symbol_list)
    cur_file_name = feature_file_name[ind]
    
    # first save transformed dataset 
    save_filename = os.path.join("../pickle_files/features",cur_file_name)
    
    with open(save_filename,'wb') as f:
        pickle.dump(dataset, f, protocol=0)   
        print "Successfully saved pickle file to: " + str(save_filename)
        
    # now save the rbm itself 
    save_filename = os.path.join("../pickle_files/feature_maps",cur_file_name)
    with open(save_filename,'wb') as f:
        pickle.dump(rbm, f, protocol=0)
        print "Successfully saved pickle file to: " + str(save_filename)
        
        