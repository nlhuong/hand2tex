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

DEBUG = True
DEBUG2 = False

# where is the data relative to current directory
REL_PATH = "../data/CROHME2012_data/trainData"

def stroke_to_arr(stroke):
    """
    Takes in stroke text and returns stroke array.
    """
    stroke = stroke.replace(',', '\n')
    stroke_IO = StringIO(stroke)
    stroke_arr = np.loadtxt(stroke_IO)
    #stroke_arr[1,:] = -1 * stroke_arr[1,:]
    return stroke_arr

def loop_ML(mathML, label, list_sym_label):
    """
    Takes in the mathml object and a list of symbols, and outputs spatial labels for each symbol.
    The labels are list of nested spatial relations, i.e. for values 0, 0.1, -1, 1, 0.5, -0.5, 2, -2 denoting
    base, square root, subscript, superscript, numerator, denominator, over, and under respectively, we can have for x in
    $\frac{a+b}{\frac{2^x}{3+6}}$ we would have an output ['x', [-0.5, 0.5, 1]], for y in
    $a^{\frac{1}{\frac{b_y}{z+w}}}$ the output would be ['y', [1, -0.5, 0.5, -1]], for z in
    $\sqrt{b^{z} - 4 a c}$ the output would be ['z', [2, 1]].
    """
    
    if mathML == None:
        print 'list_sym_label', list_sym_label
        
    if mathML.findall('*') == []:
        if label == []: 
            label.append(0)
        list_sym_label.append([mathML.text, label])
        label = []
              
    else:
                
            if mathML.tag == '{http://www.w3.org/1998/Math/MathML}mfrac':
                
                a = label + [0]
                list_sym_label.append(['-', a])               
                a = label+ [0.5]
                b = label+ [-0.5]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
            
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msubsup':
                a = label + [0]
                b = label + [-1]
                c = label +[1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                loop_ML(mathML[2], c, list_sym_label)
    
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msup':
                a = label+ [0]
                b = label+ [1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                 
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msub':
                a = label+ [0]
                b = label+ [-1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msqrt':
                a = label + [0]
                list_sym_label.append(['\\sqrt', a])
                b = label+ [0.1]
                for child in mathML:
                      loop_ML(child, b, list_sym_label)
                      
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}munderover':
                a = label + [0]
                b = label + [-2]
                c = label +[2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                loop_ML(mathML[2], c, list_sym_label)
            
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}mover':
                a = label+ [0]
                b = label+ [2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                 
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}munder':
                a = label+ [0]
                b = label+ [-2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
    
                               
            else:
                  for child in mathML:
                      loop_ML(child, label, list_sym_label)
    
    return list_sym_label

def space_relations(list_sym_label):
    """Takes nested positions information from loop_ML() and converts into nearest neighbor relation-class.
    Returns list_space_relations, where list_space_relations[i] = [symbol, label]. Labels are integers
    denoting different classes of spatial relations."""
    
    list_space_relations = []
    
    horizontal = 0
    vertical_up = 1 
    vertical_down = 2 
    superscript = 3
    subscript = 4
    inside = 5
    horizontal_bar = 6
    end = 7
    label = 1000
                      
    for i in range(len(list_sym_label)):
        ele0 = list_sym_label[i]
        symbol0 = ele0[0]
        label0 = ele0[1]
                    
        if i != len(list_sym_label)-1:
            ele1 = list_sym_label[i+1]
            symbol1 = ele1[0]
            label1 = ele1[1]
                                  
            if len(label0) == len(label1): 
                index0 = -1
                index1 = -1
            
            elif len(label0) < len(label1):
                index0 = -1
                index1 = len(label0)-1
            
            elif len(label0) > len(label1):
                index0 = len(label1)-1
                index1 = -1
                
            if (label0[index0] != 2 and label1[index1] == 2) or (label0[index0] != 0.5 and label1[index1] == 0.5) or (label0[index0] == -1 and label1[index1] == 1):
                label = vertical_up
                
            elif (label0[index0] != -2 and label1[index1] == -2) or (label0[index0] != -0.5 and label1[index1] == -0.5) or (label0[index0] == 1 and label1[index1] == -1):
                label = vertical_down
                            
            elif (label0[index0] == 0 and label1[index1] == 1) or (label0[index0] <= -1 and label1[index1] == 0):
                label = superscript
                            
            elif (label0[index0] == 0 and label1[index1] == -1) or (label0[index0] >= 1 and label1[index1] == 0):
                label = subscript
                
            elif label0[index0] == label1[index1]:
                label = horizontal
            
            if symbol0 == '-' and label0[-1] == 0 and label1[len(label0) - 1] == 0.5:
                label = horizontal_bar
                                                                                        
            elif label0[-1] != label1[-1] and label1[-1] == 0.1:
                label = inside
            
            list_space_relations.append([symbol0, label])
                    
        else:
            list_space_relations.append([symbol0, end])
        
        label = 1000
        
    return list_space_relations


def features(bar_info, prev_label, prev_bounds, cur_bounds, next_bounds):
    """Takes the horizontal bar information, the bounds of previous(A), current (B) and next(C) symbol,
    and label of the previous symbol computes the features."""
    """
    TO DO: adjust centers according to previous symbols and the symbol type 
    
    if prev_label in [3, 4]: #if subscript or superscript modify vertical bounds so reflects the 
                            # previous symbol
        cur_bounds[3] = prev_bounds[3]
        cur_bounds[1] = prev_bounds[1]
    
    if prev_label == 0:
        cur_bounds[3] += prev_bounds[3]
        cur_bounds[1] += prev_bounds[1]
        cur_bounds[3] /= 2 
        cur_bounds[1] /= 2
    """
    ver_center_B = 0.5*(cur_bounds[3]+cur_bounds[1]) 
    ver_center_C = 0.5*(next_bounds[3]+next_bounds[1]) 
    hor_center_B = 0.5*(cur_bounds[2]+cur_bounds[0]) 
    hor_center_C = 0.5*(next_bounds[2]+next_bounds[0]) 
        
    hB = cur_bounds[3] - cur_bounds[1]
    hC = next_bounds[3] - next_bounds[1]
    
    H = hC/hB
    D = 0.5*(ver_center_B - ver_center_C)
    dhC = 0.5*(hor_center_B - hor_center_C)
    
    dx = (next_bounds[0] - cur_bounds[2])/hB
    dx1 = (next_bounds[0] - cur_bounds[0])/hB
    dx2 = (next_bounds[2] - cur_bounds[2])/hB

    dy = (next_bounds[3] - cur_bounds[1])/hB
    dy1 = (next_bounds[1] - cur_bounds[1])/hB
    dy2 = (next_bounds[3] - cur_bounds[3])/hB


#####################################################################################################

def file_parser(file):
    tree = ET.parse(file)
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
        bounds = [new_cur_data[:, 0].min(), new_cur_data[:, 1].min(), new_cur_data[:, 0].max(), new_cur_data[:, 1].max()]
        Syms_bounds.append(bounds)
        
    mathML = root.find("{http://www.w3.org/2003/InkML}annotationXML/*")
    list_labels = loop_ML(mathML, [], [])
    
    if DEBUG:
        print list_labels
    list_space_relations = space_relations(list_labels)
    
    final_list_relations = []
    final_list_symbols = []
    
    # TO DO
    # final_list_features = [[bounds], features from the paper, 
        # indicator{bar above}, indicator{bar below}] add some more later
    final_list_features = []  
    
    for i in range(len(list_space_relations)):
        final_list_symbols.append(list_space_relations[i][0])
        bounds = Syms_bounds[Symbols.index(list_space_relations[i][0])]
        
        # TO DO
        # Re-adjust centers for symbols types 
        # Hierarchical centers
        
                   
    
    dataset = (Symbols, Syms_bounds, list_space_relations)
    return dataset
    

def loop_over_data():
    
    # get the list of .inkml files
    xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
    p = os.listdir(REL_PATH)
    list_filenames = [file for file in p  if file.endswith('.inkml')]
    
    for k, cur_file in enumerate(xml_file_list):
        file_name = cur_file[34:]
        dataset = file_parser(cur_file)
        Symbols, Syms_bounds, list_space_relations = dataset
        

####

xml_file = glob.glob(os.path.join(REL_PATH,"KME2G3_20_sub_30.inkml"))
#dataset = loop_over_data()
(Symbols, Syms_bounds, list_space_relations) = file_parser(xml_file[0])
file_name = xml_file[0]
print file_name[34:]
print Symbols
print Syms_bounds
print list_space_relations
print len(Symbols)
print len(list_space_relations)
 
        
   

