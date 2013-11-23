'''
Created on Nov 17, 2013

@author: nicodjimenez
'''

#from skimage.filter import gaussian_filter
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure
import numpy as np
import pickle
import os

from read_data import load_feature_file
from process_strokes import FULL_DIM

def HOG_image(img):
    # old values of pixels per cell 5,10,20
    fd_0 = hog(img, orientations=16, pixels_per_cell=(5, 5),
                            cells_per_block=(1, 1), normalise=False,visualise=False)
    
    fd_1 = hog(img, orientations=16, pixels_per_cell=(12, 12),
                            cells_per_block=(1, 1), normalise=False,visualise=False)

    fd_2 = hog(img, orientations=16, pixels_per_cell=(25, 25),
                            cells_per_block=(1, 1), normalise=False,visualise=False)
    
    
    
    fd = np.hstack((fd_0,fd_1,fd_2))
    #fd = fd / np.linalg.norm(fd)
    #fd = hog(img, orientations=8, pixels_per_cell=(5, 5),        
                            #cells_per_block=(1, 1), normalise=False,visualise=False)
    
    return fd

def HOG_dataset(file_name = "clean_symbols_45"):
    [f,data] = load_feature_file(file_name)
    (X,symbol_ind,symbol_list) = data
    fd_list = []
    
    for x in X:
        img = x.reshape((FULL_DIM,FULL_DIM)) * 1.0
        #img = gaussian_filter(img, sigma=1.0)
        #two_norm = np.linalg.norm(img)
        #img = img * (1.0 / two_norm)
        
        #print np.linalg.norm(img)
        #plt.imshow(img)
        #plt.show()
        
        fd = HOG_image(img)
        fd_list.append(fd)
        dataset = (fd_list,symbol_ind,symbol_list)
        
    filename = "XL_HOG_" + file_name + ".p"
    save_filename = os.path.join("../pickle_files/features",filename)
    
    with open(save_filename,'wb') as f:
        pickle.dump(dataset, f, protocol=0)
        print "Successfully saved pickle file to: " + str(save_filename)
    
if __name__ == "__main__":
    file_name = "clean_symbols_45"
    HOG_dataset(file_name)