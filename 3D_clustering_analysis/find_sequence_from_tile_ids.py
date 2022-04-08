"""
Script to get tile sequence files consisting of given tile ids. 

Swapnil 1/22
"""

import glob
import pickle
import re

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Get tile sequences directory.
tile_sequences_directory = experiment_directory + "tile_sequences\\"

# Get the files present in tile_sequences_directory.
files = glob.glob1(tile_sequences_directory, "*.data")

# Get the list of tile ids for 647 channel forming a sequence.         
tile_ids = [22,23,24,25]

# Initialize the sequence status.
seq_sts = False

for file in files:

    # Read from the file. 
    with open(tile_sequences_directory + file, 'rb') as filehandle:
        tile_seq = pickle.load(filehandle)
    
    # If tile ids are subset or superset of the sequence. Any of the two conditions below work.
    # if (set(tile_ids).issubset(set(tile_seq)) | set(tile_seq).issubset(set(tile_ids))):
    if (all(x in tile_seq for x in tile_ids) | all(x in tile_ids for x in tile_seq)):
    
        # Change the sequence status to True.
        seq_sts = True
    
        # Get the sequence number present in filename. 
        seq_num = re.search(r'\d+', file).group(0)
        
        print("The sequence number for given list of tile ids is {}." .format(seq_num))
        
        break

if not seq_sts:        
    print("There is no sequence for given list of tile ids.")
        
                    







