import cPickle as pickle
import glob
import os

DUMP_LOCATION = "../pickle_files/"
full_file_str = os.path.join(DUMP_LOCATION,"clean_files_spaceLabels_bounds.p")
file2 = os.path.join(DUMP_LOCATION,"corrupted_files.p")

with open(full_file_str,'rb') as f: 
    data = pickle.load(f)
    
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
print bounds[15000:15010]