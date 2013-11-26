'''
Created on Nov 10, 2013

@author: nlhuong

This file classifies recognized symbols into spatial relation categories. 
It organizes the symbols read into an expression, and is the final step of
the reading process.
'''

import glob
import os 
import numpy as np
from StringIO import StringIO
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import dump as xml_dump

from space_labels import *
from space_features import *

import cPickle as pickle

DEBUG = True
DEBUG2 = False

# where is the data relative to current directory
REL_PATH = "../data/CROHME2012_data/trainData"

DUMP_LOCATION = "../pickle_files/"

# where data is dumped
DUMP_LOCATION = "../pickle_files/"

def stroke_to_arr(stroke):
    """
    Takes in stroke text and returns stroke array.
    """
    stroke = stroke.replace(',', '\n')
    stroke_IO = StringIO(stroke)
    stroke_arr = np.loadtxt(stroke_IO)
    #stroke_arr[1,:] = -1 * stroke_arr[1,:]
    return stroke_arr



def file_parser(curfile):
    tree = ET.parse(curfile)
    root = tree.getroot()
    
    # save the full LaTeX expression
    latex_ME =  root.find("*[@type='truth']")
    latex_ME = latex_ME.text
    
    if DEBUG2:
        print latex_ME
        
    # gather list of all strokes
    full_trace_list = root.findall("{http://www.w3.org/2003/InkML}trace")
        
    # this is a group of a group of strokes which make up the whole expression
    traceGroup_parent = root.find("{http://www.w3.org/2003/InkML}traceGroup")
     # for each subgroup of strokes in the expression corresponding to a symbol
    
    # List of symbols in the expression
    Symbols = [] 
    
    # List of bounding boxes for each symbol
    Syms_bounds =[]
    
    for traceGroup in traceGroup_parent: 
        part = traceGroup.find("{http://www.w3.org/2003/InkML}annotation")
    
        if part == None:
            continue
            
        symbol = part.text
        Symbols.append(symbol)
            
        # get the indices of the single strokes which comprise the current symbol
        cur_trace_list = traceGroup.findall("{http://www.w3.org/2003/InkML}traceView")
        trace_id_list = [int(elem.attrib.get('traceDataRef')) for elem in cur_trace_list]
        new_cur_data = None
            
        for trace_id in trace_id_list:
            stroke = full_trace_list[trace_id].text
            stroke_arr = stroke_to_arr(stroke)

            if new_cur_data == None:
                new_cur_data = stroke_arr
            else:
                new_cur_data = np.vstack((new_cur_data,stroke_arr))
    
        if DEBUG2:
            print 'symbol', symbol
            print 'length', len(new_cur_data)
            print 'new_curr_data', new_cur_data 
        
        # the bounding box of a symbol [xmin, ymin, xmax, ymax]
        bounds = [new_cur_data[:, 0].min(), new_cur_data[:, 1].min(), \
                  new_cur_data[:, 0].max(), new_cur_data[:, 1].max()]
        Syms_bounds.append(bounds)
        
    mathML = root.find("{http://www.w3.org/2003/InkML}annotationXML/*")
    list_labels = loop_ML(mathML, [], [])
    
    if DEBUG:
        print list_labels
    list_space_relations = space_relations(list_labels)
    
    if DEBUG:
        print 'Symbols', Symbols
        print 'Syms_bounds', Syms_bounds
        print 'list_space_relations', list_space_relations
    
    
    final_list_relations = []
    final_list_symbols = []
    final_list_bounds = []
    
    faulty_file = []
    
    for i in range(len(list_space_relations)):
        try:
            symbol = list_space_relations[i][0]            
            k = Symbols.index(symbol)
            final_list_symbols.append(symbol)
            final_list_bounds.append(Syms_bounds[k])
            final_list_relations.append(list_space_relations[i][1])
            
            Symbols.remove(symbol)            
            Syms_bounds.remove(Syms_bounds[k])            
            
                         
        except:
            print "List of symbols does not match traces."
            faulty_file = curfile[34:]
            
    dataset = (final_list_symbols, final_list_relations, final_list_bounds)
    return dataset, faulty_file
    

def loop_over_data():
    
    # get the list of .inkml files
    xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
    p = os.listdir(REL_PATH)
    list_filenames = [file for file in p  if file.endswith('.inkml')]
    
    file_names = []
    final_list_symbols = []
    final_list_relations = []
    final_list_bounds = []
    faulty_files = []    
    data = []
    
    for k, cur_file in enumerate(xml_file_list):
        file_name = cur_file[34:]
        if DEBUG:
            print file_name
        
        data_k, faulty_file = file_parser(cur_file)
        
        if faulty_file == []:
            file_names += [file_name]*len(data_k[0])
            final_list_symbols += data_k[0]
            final_list_relations += data_k[1]
            final_list_bounds += data_k[2]
             
        else:
            faulty_files.append(faulty_file)

    dataset = (np.array(file_names), np.array(final_list_symbols), \
               np.array(final_list_relations), np.array(final_list_bounds))    
    save_filename = os.path.join(DUMP_LOCATION,"clean_files_spaceLabels_bounds.p")
    with open(save_filename,'wb') as f:
        pickle.dump(dataset, f, protocol=0)
        print "Successfully saved pickle file to: " + str(save_filename)
    
    save_filename2 = os.path.join(DUMP_LOCATION,"corrupted_files.p")
    with open(save_filename2,'wb') as f2:
        pickle.dump(faulty_files, f2, protocol=0)
        print "Successfully saved pickle file to: " + str(save_filename)
    
####

if DEBUG:
    xml_file = glob.glob(os.path.join(REL_PATH,"KME2G3_20_sub_30.inkml"))
    #dataset = loop_over_data()
    (final_list_symbols, final_list_relations, final_list_bounds), faulty_file = file_parser(xml_file[0])
    file_name = xml_file[0]
    print file_name[34:]
    print final_list_symbols
    print final_list_relations
    print final_list_bounds
    print len(final_list_bounds)
    print len(final_list_relations)
    loop_over_data()
 
        
   

