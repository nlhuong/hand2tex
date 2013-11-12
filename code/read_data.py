'''
Created on Oct 22, 2013

@author: nicodjimenez

This file will process data for symbol recognizer. 
It will create list of flattened bitmaps along with corresponding labels.
These will be saved as a tuple in a pickle file.

TODO: cubic interpolation fcn
'''

import cv2
from scipy.interpolate import interp1d
import glob
import os 
import cPickle as pickle
import xml.etree.ElementTree as ET
# used for debugging only
from xml.etree.ElementTree import dump as xml_dump
import numpy as np
from StringIO import StringIO
from pylab import *
#from skimage import morphology

import settings

# are we plotting all the image transformations
DEBUG = False

# pixel dimensions to which we are going to downsample
FULL_DIM = 28

# pixel resolution at the point we do segmentation 
BOUND_DIM = 20.0

# are we going to plot all the symbmols as they come along? (just for debugging)
PLOT_ME = False

# where is the data relative to current directory
REL_PATH = "../data/CROHME2012_data/trainData"

# where are we saving the outputs to
DUMP_LOCATION = "../pickle_files/"

SYMBOL_LIST_FILENAME = "symbol_list.txt"

# x resolution which will be used to interpolate between data points
INTERP_RES = 1

# special symbols that contain more than one component
MULT_COMP_SYMBOLS = settings.mult_comp_symbols.keys()

def xy_to_bitmap(data_arr):
    """
    Converts xy pairs to a bit mat formatted array for easy processing 
    by LeNet5.  
    
    First: scale xy coordinates so that everything is between 0 and 20. 
    Second: shift these coordinates so that center of mass is at 14 
    Third: overlay image on top of a 28 x 28  bitmap
    
    If we have a single point, then just put this point smack in the middle 
    and we are done.  
    """
    
    # if we have a dot, for example 
    if (len(data_arr) == 1) or (data_arr.ndim == 1): 
        vis = np.zeros((FULL_DIM, FULL_DIM),np.uint8)
        mid_pt = int(FULL_DIM * 0.5)
        vis[mid_pt,mid_pt] = 1
        
        return vis
    
    max_x = max(data_arr[:,0])
    max_y = max(data_arr[:,1])
    max_xy = max([max_x,max_y])
    dim_stretch = (BOUND_DIM ) / max_xy
    
    # make it fit in 20 x 20 box
    data_arr = data_arr * dim_stretch
    
    # now translate this box to middle part of 28 x 28 
    data_arr = data_arr + (FULL_DIM - BOUND_DIM) * 0.5
    
    vis = np.zeros((FULL_DIM, FULL_DIM),np.uint8)
    
    # this code is in case you want to center using COM
#     avg_x = data_arr[:,0].mean()
#     avg_y = data_arr[:,1].mean()
#     min_xy = data_arr.min()
#     max_xy = data_arr.max()
#     x_diff = FULL_DIM * 0.5 - avg_x 
#     y_diff = FULL_DIM * 0.5 - avg_y
#     data_arr[:,0] += x_diff 
#     data_arr[:,1] += y_diff
    
    # place all values in binary image
    for elem in data_arr: 
        vis[FULL_DIM - int(elem[1]) ,int(elem[0])] = 1
        
#     if DEBUG: 
#         vis_2 = cv2.cvtColor(vis,cv2.COLOR_GRAY2BGR)
#         cv2.imshow('thresh',vis_2)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

    return vis

def xy_to_cv(data_arr):
    """
    Converts xy pairs to a openCV formatted matrix.
    """
    SEG_DIM = 100 
    max_x = max(data_arr[:,0])
    max_y = max(data_arr[:,1])
    max_xy = max([max_x,max_y])
    dim_stretch = SEG_DIM / max_xy
    data_arr = data_arr * dim_stretch
    
    vis = 255 * np.ones((SEG_DIM+1, SEG_DIM+1),np.uint8)
    
    # place all values in binary image
    for elem in data_arr: 
        vis[SEG_DIM - int(elem[1]) ,int(elem[0])] = 0
    
    return vis

def gen_opencv_mat(data_arr):
    """
    Some experimentation with segmenting symbols.
    """
    bin_mat = xy_to_cv(data_arr)
    
    vis_2 = cv2.cvtColor(bin_mat,cv2.COLOR_GRAY2BGR)
    cv2.imwrite('sof2.png',vis_2)
        
    # Load the image
    img = cv2.imread('sof2.png')
    #img = cv2.imread('test_case.png')
    
    # convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # smooth the image to avoid noises
    gray = cv2.medianBlur(gray,0)
    
    if DEBUG:
        cv2.imshow('gray_img',gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    
    if DEBUG:
        cv2.imshow('thresh',thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    # apply some dilation and erosion to join the gaps
    thresh = cv2.dilate(thresh,None,iterations = 1)
    
    if DEBUG:
        cv2.imshow('thresh_after_dilation',thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
#     thresh = cv2.erode(thresh,None,iterations = 1)
#         
#     if DEBUG:
#         cv2.imshow('thresh_after_erode',thresh)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
    
    # Find the contours
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # For each contour, find the bounding rectangle and draw it
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.rectangle(thresh_color,(x,y),(x+w,y+h),(0,255,0),2)
    
    if DEBUG:
        # Finally show the image
        #cv2.imshow('img',img)
        cv2.imshow('res',thresh_color)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
#     
#     label_number = 0
#     
#     for label_number in range(np.max(labels)):
#         temp = np.uint8(labels==label_number) * 255
#         if not cv2.countNonZero(temp):
#             break
#         cv2.imshow('result', temp), cv2.waitKey(0)

    return None

def normalize_symbol(data_arr):
    """
    Takes symbols and aligns them at the bottom left corner. 
    """
    
    # must flip this dimension (it's f-ed up in the inkml files)
    data_arr[:,1] = -1 * data_arr[:,1]
    #print len(data_arr)
    #print data_arr
    min_x = min(data_arr[:,0]) 
    min_y = min(data_arr[:,1]) 
    
    sub_vec = np.array([min_x,min_y])
    
    for (ind,elem) in enumerate(data_arr): 
        data_arr[ind] = elem - sub_vec
        
    return data_arr

def lin_interp_stroke(data_arr):
    """
    Takes stroke array as input and returns linearly interpolated
    stroke array. 
    """
    
    KIND = 'linear'
    interp_data_arr = None
    data_len = len(data_arr)
    
    # don't try to interpolate if we only have one point!
    if (len(data_arr) == 1) or (data_arr.ndim == 1):
        return data_arr
    
    for ind in range(data_len-1):  
        
        #print data_arr[ind:ind+2,:]
        x_diff = abs(data_arr[ind,0] - data_arr[ind+1,0])
        y_diff = abs(data_arr[ind,1] - data_arr[ind+1,1])
        
        # if two points between which we are interpolating is 'flat'
        if x_diff > y_diff: 
            
            if data_arr[ind,0] < data_arr[ind+1,0]:
                g = interp1d([data_arr[ind,0],data_arr[ind+1,0]] ,[data_arr[ind,1],data_arr[ind+1,1]],kind=KIND)
            else:
                g = interp1d([data_arr[ind+1,0],data_arr[ind,0]] ,[data_arr[ind+1,1],data_arr[ind,1]],kind=KIND)
                     
            #g = interp1d(data_arr[ind:ind+2,0], data_arr[ind:ind+2,1])
            
            x_new = np.arange(min(data_arr[ind:ind+2,0]),max(data_arr[ind:ind+2,0]),INTERP_RES)
            y_new = g(x_new)
            
        # if the two points between which we are interpolating is tall
        else: 
            if data_arr[ind,1] < data_arr[ind+1,1]:
                g = interp1d([data_arr[ind,1],data_arr[ind+1,1]] ,[data_arr[ind,0],data_arr[ind+1,0]],kind=KIND)
            else:
                g = interp1d([data_arr[ind+1,1],data_arr[ind,1]] ,[data_arr[ind+1,0],data_arr[ind,0]],kind=KIND)
                     
            #g = interp1d(data_arr[ind:ind+2,0], data_arr[ind:ind+2,1])
            
            y_new = np.arange(min(data_arr[ind:ind+2,1]),max(data_arr[ind:ind+2,1]),INTERP_RES)
            x_new = g(y_new)
            
        
        new_data_arr = np.vstack((x_new,y_new)).T
        
        if interp_data_arr == None: 
            interp_data_arr = new_data_arr
        else:
            interp_data_arr = np.vstack((interp_data_arr,new_data_arr))
            
    return interp_data_arr
    
def remove_outliers(data_arr):
    """
    Takes array as input and deletes garbage indices.
    """
    ind_delete = []
    for (ind,val) in enumerate(data_arr[:,1]):
        if abs(val) > 1E6:
            ind_delete.append(ind)
    
    data_arr = np.delete(data_arr, ind_delete,0)
    
    return data_arr

def stroke_to_arr(stroke):
    """
    Takes in stroke text and returns stroke array.
    """
    
    stroke = stroke.replace(',', '\n')
    stroke_IO = StringIO(stroke)
    stroke_arr = np.loadtxt(stroke_IO)
    #stroke_arr[1,:] = -1 * stroke_arr[1,:]
    
    return stroke_arr

def special_treatment(symbol,trace_list,bitmap_list,symbol_list):
    """
    Takes in list of strokes corresponding to a 'special' character, 
    breaks up the character into constituents, and then appends that 
    to the training set.
    """
    
    #bitmap_list = []
    #symbol_list = []
    
    if symbol == "=":
        if len(trace_list) != 2: 
            return 
        
        normal_treatment('-',[trace_list[0]],bitmap_list,symbol_list)
        normal_treatment('-',[trace_list[1]],bitmap_list,symbol_list)
    
    if symbol == "i" or "!":
        if len(trace_list) != 2: 
            return 
        
        len_0 = len(trace_list[0])
        len_1 = len(trace_list[1])
        ind = np.array([len_0,len_1]).argmin()
        
        normal_treatment('.',[trace_list[ind]],bitmap_list,symbol_list,plot_me=True)
        normal_treatment('|',[trace_list[1-ind]],bitmap_list,symbol_list,plot_me=True)
        
    if symbol == "\ldots":
        [normal_treatment('.',[trace],bitmap_list,symbol_list) for trace in trace_list]
        
    if symbol == "\leq":
        if len(trace_list) != 2: 
            return 
        
        avg_y0 = trace_list[0][:,1].mean() 
        avg_y1 = trace_list[1][:,1].mean()
        ind = np.array([avg_y0,avg_y1]).argmin()
        
        normal_treatment('=',[trace_list[ind]],bitmap_list,symbol_list)
        normal_treatment('\lt',[trace_list[1-ind]],bitmap_list,symbol_list)
    
    if symbol == "\geq":
        if len(trace_list) != 2: 
            return 
        
        avg_y0 = trace_list[0][:,1].mean() 
        avg_y1 = trace_list[1][:,1].mean()
        ind = np.array([avg_y0,avg_y1]).argmin()
        
        normal_treatment('=',[trace_list[ind]],bitmap_list,symbol_list)
        normal_treatment('\gt',[trace_list[1-ind]],bitmap_list,symbol_list)
        
    if symbol == "\div":
        if len(trace_list) != 3: 
            return 
        
        avg_y0 = trace_list[0][:,1].mean() 
        avg_y1 = trace_list[1][:,1].mean()
        avg_y2 = trace_list[2][:,1].mean()
        
        myList = [avg_y0,avg_y1,avg_y2]
        
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        symbol_ascending = [".","-","."]
        
        for cur_ind in range(3):
            normal_treatment(symbol_ascending[cur_ind],[trace_list[ind_ascending[cur_ind]]],bitmap_list,symbol_list)
            
    if symbol == "\sin":
        if len(trace_list) != 4: 
            return 
        
        dot_ind = np.array([len(arr) for arr in trace_list]).argmin()
        normal_treatment(".",[trace_list[dot_ind]],bitmap_list,symbol_list)
        
        trace_list.pop(dot_ind)
        
        myList = [trace[:,0].mean() for trace in trace_list]
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        symbol_ascending = ["s","|","n"]
        
        for (cur_ind,cur_symbol) in enumerate(symbol_ascending):
            normal_treatment(cur_symbol,[trace_list[ind_ascending[cur_ind]]],bitmap_list,symbol_list)
            
    if symbol == "\tan":
        if len(trace_list) != 4: 
            return 
        
        # first group the strokes making up the 't'
        myList = [trace[:,0].mean() for trace in trace_list]
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        normal_treatment("t",trace_list[ind_ascending[0:2]],bitmap_list,symbol_list)
        
        normal_treatment("a",trace_list[ind_ascending[2]],bitmap_list,symbol_list)
        normal_treatment("n",trace_list[ind_ascending[3]],bitmap_list,symbol_list)
        
    if symbol == "\cos":
        if len(trace_list) != 3: 
            return 
        
        # first group the strokes making up the 't'
        myList = [trace[:,0].mean() for trace in trace_list]
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        normal_treatment("c",trace_list[ind_ascending[0]],bitmap_list,symbol_list)
        normal_treatment("o",trace_list[ind_ascending[1]],bitmap_list,symbol_list)
        normal_treatment("s",trace_list[ind_ascending[2]],bitmap_list,symbol_list)
        
    if symbol == "\log":
        if len(trace_list) != 3: 
            return 
        
        # first group the strokes making up the 't'
        myList = [trace[:,0].mean() for trace in trace_list]
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        normal_treatment("l",trace_list[ind_ascending[0]],bitmap_list,symbol_list)
        normal_treatment("o",trace_list[ind_ascending[1]],bitmap_list,symbol_list)
        normal_treatment("g",trace_list[ind_ascending[2]],bitmap_list,symbol_list)
    
    if symbol == "\lim":
        if len(trace_list) != 4: 
            return 
        
        dot_ind = np.array([len(arr) for arr in trace_list]).argmin()
        normal_treatment(".",[trace_list[dot_ind]],bitmap_list,symbol_list)
        
        trace_list.pop(dot_ind)
        
        myList = [trace[:,0].mean() for trace in trace_list]
        ind_ascending = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
        symbol_ascending = ["l","|","m"]
        
        for (cur_ind,cur_symbol) in enumerate(symbol_ascending):
            normal_treatment(cur_symbol,[trace_list[ind_ascending[cur_ind]]],bitmap_list,symbol_list)
        
    return 

def normal_treatment(symbol,trace_list,bitmap_list,symbol_list,plot_me=False):
    """
    Takes a new set of strokes and saves it in the right format for the classifier.
    
    Note: the values of bitmap_list and symbol_list will be modified in
    the function.
    """
    
    # now we build a string with comma separated fields that will contain all the 
    # positions of the sybmol, aggregated from all the constituent stokes
    new_cur_data = None
    # concatenate all traces into one 
    for stroke_arr in trace_list:
        
        if new_cur_data == None:
            new_cur_data = stroke_arr
        else: 
            new_cur_data = np.vstack((new_cur_data,stroke_arr))
                        
    # flip the symbol and shift coordinates to lower left of bounding box
    if len(new_cur_data) == 0: 
        return 
    
    new_cur_data = normalize_symbol(new_cur_data)
    
    if plot_me: 
        if new_cur_data.ndim == 2:
            scatter(new_cur_data[:,0],new_cur_data[:,1])
        else: 
            scatter(new_cur_data[0],new_cur_data[1])
        
        title(symbol)
        show()
        
    #gen_opencv_mat(new_cur_data)
    
    # convert xy coordinates to bitmap
    new_cur_data = xy_to_bitmap(new_cur_data)
    
    # flatten the bitmap (to make it compatible with mnist)
    new_cur_data = new_cur_data.reshape(FULL_DIM * FULL_DIM)
    
    bitmap_list.append(new_cur_data)
    symbol_list.append(symbol)
    


def loop_over_data():
    # get the list of .inkml files
    xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
    
    symbol_list = [] 
    bitmap_list = []
    
    #symbol_dict = {}
    ct = 0
    
    for cur_file in xml_file_list:
        tree = ET.parse(cur_file)
        root = tree.getroot()
        
        # gather list of all strokes
        full_trace_list = root.findall("{http://www.w3.org/2003/InkML}trace")
        
        # this is a group of a group of strokes which make up the whole expression
        traceGroup_parent = root.find("{http://www.w3.org/2003/InkML}traceGroup")
        
        # for each subgroup of strokes in the expression corresponding to a symbol
        for traceGroup in traceGroup_parent: 
            
            # look for the annotation of the current group of strokes which will contain
            # the truth value of the stroke
            part = traceGroup.find("{http://www.w3.org/2003/InkML}annotation")
            
            if part == None:
                #TODO: add special function here 
                continue
            
            ct += 1
            symbol = part.text
            
            # get the indices of the single strokes which comprise the current symbol
            trace_id_list_pre = traceGroup.findall("{http://www.w3.org/2003/InkML}traceView")
            trace_id_list = [int(elem.attrib.get('traceDataRef')) for elem in trace_id_list_pre]
            trace_list = [lin_interp_stroke(stroke_to_arr(full_trace_list[trace_id].text)) for trace_id in trace_id_list]
            
            if symbol in MULT_COMP_SYMBOLS: 
                # we'll get back to these symbols later... 
                #print symbol
                continue
                #special_treatment(symbol,trace_list,bitmap_list,symbol_list) 
                
            else: 
                normal_treatment(symbol,trace_list,bitmap_list,symbol_list) 
                
    print "Total number of example characters: ", ct
    
    dataset = (np.array(bitmap_list),np.array(symbol_list))
    
    save_filename = os.path.join(DUMP_LOCATION,"clean_symbols.p")
    with open(save_filename,'wb') as f:
        pickle.dump(dataset, f, protocol=0)   
        print "Successfully saved pickle file to: " + str(save_filename)
        
#     with open(SYMBOL_LIST_FILENAME,'wb') as f: 
#         for key in symbol_dict.keys():
#             f.write(key + "\n")
#         print "Successfully list of symbols to: " + str(SYMBOL_LIST_FILENAME)
        
if __name__ == "__main__":
    loop_over_data()
    
#for symbol in symbol_dict:
#    print symbol, len(symbol_dict[symbol])
#print "Total number of example characters: ", ct



    

