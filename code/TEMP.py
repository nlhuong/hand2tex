import cPickle as pickle
import glob
import os
from space_features import *
import numpy as np

DEBUG0 = False
DEBUG = False

DUMP_LOCATION = "../pickle_files/"
full_file_str = os.path.join(DUMP_LOCATION,"clean_files_spaceLabels_bounds.p")
with open(full_file_str,'rb') as f: 
    data = pickle.load(f)
    
file2 = os.path.join(DUMP_LOCATION,"corrupted_files.p")    
with open(file2,'rb') as f2: 
    faulty_files = pickle.load(f2)

(file_names, symbols, relations, bounds) = data

file_names = file_names.tolist()
file_names.append('end')
list_symbols = []
list_features = []
list_labels = []
list_files = []
bars_x = []
bars_y = []

cur_file = file_names[0]
file_beginning = 0 
end_symbols = 0

for k in range(len(symbols)+1):
    if file_names[k] == cur_file:
        if relations[k] == 6:
            bars_x.append([bounds[k][0], bounds[k][2]])
            bars_y.append((bounds[k][1]+bounds[k][3])/2)
    else:
        bar_info = [bars_x, bars_y]
        if DEBUG:
            print cur_file
            print 'file_beginning', file_beginning
        for i in range(file_beginning, k):
            if relations[i] != 7:
                list_features.append(features(bar_info, bounds[i], bounds[i+1]))
                list_files.append(file_names[i])
                list_symbols.append(symbols[i])
                list_labels.append(relations[i])                    

            else:
                end_symbols += 1
        if DEBUG: print 'file_end', i
                    
        cur_file = file_names[k]
        file_beginning = k
        bars_x = []
        bars_y = []  


dataset = (np.array(list_files), np.array(list_symbols), \
        np.array(list_labels), np.array(list_features))  


save_filename = os.path.join(DUMP_LOCATION,"features_and_labels.p")
with open(save_filename,'wb') as f:
    pickle.dump(dataset, f, protocol=0)
    print "Successfully saved pickle file to: " + str(save_filename)

############
if DEBUG0:
    
    print 'file_names', file_names
    print 'faulty files', faulty_files
    print 'num_unq_files', len(set(file_names))
    print len(file_names)
    print len(symbols)   
    
    print list_files[1402:1420]
    print list_symbols[1402:1420]
    print list_labels[1402:1420]
    print list_features[1402:1420]
    print bounds[1402:1420]
    
    print file_names[1402:1420]
    print symbols[1402:1420]
    print relations[1402:1420]
    print bounds[1402:1420]   
    
    print 'len_files', len(set(list_files))
    print 'len list_symbols', len(list_symbols)
    
    """import cPickle as pickle
    import glob
    import os
    
    DUMP_LOCATION = "../pickle_files/"
    full_file_str = os.path.join(DUMP_LOCATION,"clean_files_spaceLabels_bounds.p")
    with open(full_file_str,'rb') as f: 
        data = pickle.load(f)
    
    file2 = os.path.join(DUMP_LOCATION,"corrupted_files.p")    
    with open(file2,'rb') as f2: 
        faulty_files = pickle.load(f2)
    
    (file_names, symbols, relations, bounds) = data
    print 'faulty files', faulty_files
    print 'num_unq_files', len(set(file_names))
    print len(file_names)
    print len(symbols)
    print file_names[15000:15010]
    print symbols[15000:15010]
    print relations[15000:15010]
    print bounds[15000:15010]"""