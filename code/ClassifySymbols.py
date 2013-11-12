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
    The labels are list of nested spatial relations, i.e. for values 0, -1, 1, 0.5, -0.5, 2 denoting
    base, subscript, superscript, numerator, denominator and square root respectively, we can have for x in
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
                b = label+ [2]
                for child in mathML:
                      loop_ML(child, b, list_sym_label)
            
            else:
                  for child in mathML:
                      loop_ML(child, label, list_sym_label)
    
    return list_sym_label


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
    List_labels = loop_ML(mathML, [], [])
    
               
    return Symbols, Syms_bounds, List_labels
    

def loop_over_data():
    
    # get the list of .inkml files
    xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
    p = os.listdir(REL_PATH)
    list_filenames = [file for file in p  if file.endswith('.inkml')]
    
    for k, cur_file in enumerate(xml_file_list):
        Symbols, Syms_bounds, List_labels = file_parser(cur_file)
        

####

xml_file = glob.glob(os.path.join(REL_PATH,"TrainData2_4_sub_9.inkml"))
print file_parser(xml_file[0])
loop_over_data()

        
   

