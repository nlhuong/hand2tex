'''
Created on Oct 22, 2013

@author: nicodjimenez

This file handles requests for stored data.  For example, 
saved classifiers or saved pre-processed data.  
'''

import cv2
import glob
import os 
import cPickle as pickle
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import dump as xml_dump
import numpy as np
from pylab import *
from settings import * 

from process_strokes import *
from data_vis import view_bitmap

features_file_list = glob.glob("../pickle_files/features/*.p")

def load_feature_file(file_name):
    full_file_str = os.path.join("../pickle_files/features/",file_name + ".p")
    
    with open(full_file_str,'rb') as f: 
        data = pickle.load(f)
            
    return [f,data]
    

def load_data(data_type="clean"):
    
    if data_type == "clean":
        with open("../pickle_files/features/clean_symbols_45.p",'rb') as f: 
            data = pickle.load(f)
            
    if data_type == "HOG":
        with open("../pickle_files/features/HOG.p",'rb') as f: 
            data = pickle.load(f)
        
    return [f,data]

def data_iterator(substring=""):
    """
    Iterates over all feature maps whose filenames contain a certain substring. 
    
    Returns: 
        [filename_str,data] - name of feature map, and the data
    """
    
    for feature_file in features_file_list:
        if substring in feature_file: 
            with open(feature_file,'rb') as f:
                data = pickle.load(f)
                yield [f,data]
        



    


    

