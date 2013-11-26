'''
Created on Nov 11, 2013

@author: nicodjimenez

Loads mnist data set.  

TODO: add MNIST dataset to InkML dataset.  
'''

import cPickle 
import cv2 
import numpy as np

DATA_LOC = "/home/nicodjimenez/Documents/hand2tex/deep_learning_code/DeepLearningTutorials/data/mnist.pkl"

with open(DATA_LOC,'rb') as f:
    train_set, valid_set, test_set = cPickle.load(f)
    
    for train_ind in range(100):
        text_example = train_set[0][train_ind]
        text_example = text_example * 255
        text_example = text_example.round()
        split_text = np.split(text_example, 28) 
        
        cv_mat = np.zeros( (28,28),np.uint8 )
        
        for ind in range(28):
            cv_mat[ind] = split_text[ind]
            
        
        vis_2 = cv2.cvtColor(cv_mat,cv2.COLOR_GRAY2BGR)
        cv2.imshow('gray_img',vis_2)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()
    