'''
Created on Oct 22, 2013

@author: nicodjimenez

This file will save a dictionary mapping from symbols to lists of examples.
This dictionary is saved to a pickle file for easier access.
'''

import glob
import os 
import cPickle as pickle
import xml.etree.ElementTree as ET
# used for debugging only
from xml.etree.ElementTree import dump as xml_dump
import numpy as np
from StringIO import StringIO
from pylab import *

# are we going to plot all the symbmols as they come along? (just for debugging)
PLOT_ME = False

# where is the data relative to current directory
REL_PATH = "../data/CROHME2012_data/trainData"

# where are we saving the outputs to
DUMP_LOCATION = "../pickle_files/"
SAVE_FILENAME = os.path.join(DUMP_LOCATION,"raw_symbols.p")

def interp_stroke(stroke):
    stroke=1
    
def remove_outliers(stroke):
    stroke = stroke

def parse_data():
    # get the list of .inkml files
    xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
    symbol_dict = {}
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
                continue
            
            ct += 1
            symbol = part.text
            
            # get the indices of the single strokes which comprise the current symbol
            cur_trace_list = traceGroup.findall("{http://www.w3.org/2003/InkML}traceView")
            trace_id_list = [int(elem.attrib.get('traceDataRef')) for elem in cur_trace_list]
            
            # now we build a string with comma separated fields that will contain all the 
            # positions of the sybmol, aggregated from all the constituent stokes
            new_cur_data = ""
            
            for trace_id in trace_id_list:
                new_cur_data += full_trace_list[trace_id].text
                
            # a hack to enable easy parsing by numpy
            new_cur_data = new_cur_data.replace(',', '\n')
            new_cur_data = StringIO(new_cur_data)
            new_cur_data_arr = np.loadtxt(new_cur_data)
            
            # I delete strange feature in the data where some indices are ridiculously out 
            # of bounds 
            ind_delete = []
            for (ind,val) in enumerate(new_cur_data_arr[:,1]):
                if abs(val) > 1E6:
                    ind_delete.append(ind)
            
            new_cur_data_arr = np.delete(new_cur_data_arr, ind_delete,0)
            
            if PLOT_ME: 
                scatter(new_cur_data_arr[:,0],-new_cur_data_arr[:,1])
                #xlim([0,20000])
                #ylim([-10000,0])
                title(symbol)
                show()
            
            if symbol in symbol_dict:
                symbol_dict[symbol].append(new_cur_data_arr)
            else:
                symbol_dict.update({symbol:[new_cur_data_arr]})
    
    with open(SAVE_FILENAME,'wb') as f:
        pickle.dump(symbol_dict, f, protocol=0)   
        
    print "Successfully saved pickle file to: " + str(SAVE_FILENAME)
    
    
    
#for symbol in symbol_dict:
#    print symbol, len(symbol_dict[symbol])
#print "Total number of example characters: ", ct



    

