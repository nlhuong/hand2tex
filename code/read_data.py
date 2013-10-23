'''
Created on Oct 22, 2013

@author: nicodjimenez
'''

import glob
import os 
#from lxml import etree
import xml.etree.ElementTree as ET
# used for debugging only
from xml.etree.ElementTree import dump as xml_dump
import numpy as np
from StringIO import StringIO
from pylab import *

REL_PATH = "../data/CROHME2012_data/trainData"
xml_file_list = glob.glob(os.path.join(REL_PATH,"*.inkml"))
symbol_dict = {}
ct = 0

for cur_file in xml_file_list:
    tree = ET.parse(cur_file)
    root = tree.getroot()
    full_trace_list = root.findall("{http://www.w3.org/2003/InkML}trace")
    traceGroup_parent = root.find("{http://www.w3.org/2003/InkML}traceGroup")
    
    for traceGroup in traceGroup_parent: 
        part = traceGroup.find("{http://www.w3.org/2003/InkML}annotation")
        
        if part == None:
            continue
        
        ct += 1
        symbol = part.text
        cur_trace_list = traceGroup.findall("{http://www.w3.org/2003/InkML}traceView")
        trace_id_list = [int(elem.attrib.get('traceDataRef')) for elem in cur_trace_list]
        new_cur_data = ""
        
        for trace_id in trace_id_list:
            new_cur_data += full_trace_list[trace_id].text
            
        new_cur_data = new_cur_data.replace(',', '\n')
        new_cur_data = StringIO(new_cur_data)
        new_cur_data_arr = np.loadtxt(new_cur_data)
        scatter(new_cur_data_arr[:,0],-new_cur_data_arr[:,1])
        xlim([0,20000])
        ylim([-10000,0])
        title(symbol)
        show()
        
        if symbol in symbol_dict:
            symbol_dict[symbol].append(new_cur_data_arr)
        else:
            symbol_dict.update({symbol:[new_cur_data_arr]})
    
for symbol in symbol_dict:
    print symbol, len(symbol_dict[symbol])
    

print "Total number of example characters: ", ct



    

