"""
This is a script to randomize the location of points in a cluster.
For a given input cluster it returns a cluster with randomized locations of points within the original cluster volume.    

Swapnil 2/22
"""

import numpy as np
import glob
import pickle
import os
import random

from scipy.spatial import Delaunay

# Are you sequencing 3d localizations from molecule list or from neural network prediction?
mol_list = False

# # Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# If does not exist, create new directory for random-cluster output of 3d localization sequences.
if mol_list: 
    if not os.path.exists(storm_exp_directory + "random_cluster_sequences_mol_list\\"):
        os.mkdir(storm_exp_directory + "random_cluster_sequences_mol_list\\")
    
    rand_clust_directory = storm_exp_directory + "random_cluster_sequences_mol_list\\" 

else: 
    if not os.path.exists(experiment_directory + "random_cluster_sequences\\"):
        os.mkdir(experiment_directory + "random_cluster_sequences\\")
    
    rand_clust_directory = experiment_directory + "random_cluster_sequences\\" 

# Remove previously present files. 
files = glob.glob(rand_clust_directory + "*.data")
for f in files:
    os.remove(f)    

# Set starting sequence and end sequence to get localizations from tile sequence for 3D clustering.
seq_start = 359
seq_end = 359

# Get localizations sequences directory.
if mol_list: locs_sequences_directory = storm_exp_directory + "locs3d_molecule_list_sequences\\"
    
else: locs_sequences_directory = experiment_directory + "locs3d_pred_sequences\\"

# Get number of 3d localization sequences present in locs_sequences_directory.
total_seqs = len(glob.glob(locs_sequences_directory + "*.data"))

# Iterate over sequences.
for i in range(1, total_seqs+1):
# for i in range(seq_start, seq_end+1):    
    
    # Get the 3d localization sequence filename.
    if mol_list: locs_seq_file_name = locs_sequences_directory + "locs3d_molecule_list_sequence_" + str(i) + ".data"

    else: locs_seq_file_name = locs_sequences_directory + "locs3d_pred_sequence_" + str(i) + ".data"
    
    # Set the DBSCAN result filename for given 3d localization sequence.
    if mol_list: rand_clust_file_name = rand_clust_directory + "random_cluster_mol_list_sequence_" + str(i) + ".data"
    
    else: rand_clust_file_name = rand_clust_directory + "random_cluster_sequence_" + str(i) + ".data"              
    
    # Read from the file. 
    with open(locs_seq_file_name, 'rb') as filehandle:
        locs3d_seq_arr = pickle.load(filehandle)

    # Create a bounding box around the cluster.
    # Get min and max values for every dimension.
    y_min = np.amin(locs3d_seq_arr[:,0])
    y_max = np.amax(locs3d_seq_arr[:,0])

    x_min = np.amin(locs3d_seq_arr[:,1])
    x_max = np.amax(locs3d_seq_arr[:,1])

    z_min = np.amin(locs3d_seq_arr[:,2])
    z_max = np.amax(locs3d_seq_arr[:,2])
    
    # Hull needs atleast 5 points to construct initial simplex.
    if len(locs3d_seq_arr) >= 5:        
        # Get the delaunay triangulation for given sequence points.
        hull = Delaunay(locs3d_seq_arr)
        
    else:
        continue
    
    # Initialize random point counter.
    rand_count = 0
    
    # Initialize list of randomized localizations within the cluster.
    rand_loc_list = []
    
    while (rand_count <= len(locs3d_seq_arr)):

        # Get the random point within the bounding box.
        y_rand = random.uniform(y_min, y_max)
        x_rand = random.uniform(x_min, x_max)        
        z_rand = random.uniform(z_min, z_max)

        point = np.zeros(3)
        point[0] = y_rand
        point[1] = x_rand
        point[2] = z_rand
        
        # If the point is within hull volume.
        if (hull.find_simplex(point)>=0):
            
            # Add the point to random locs list. 
            rand_loc_list.append(point)
            rand_count += 1
        
    # Convert random localization list to array.
    rand_loc_arr = np.array(rand_loc_list)
    
    # Writting the random localization array to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(rand_clust_file_name, 'wb') as filehandle:
        # store the data as binary data stream.
        pickle.dump(rand_loc_arr, filehandle) 

    if (i%100 == 0):
        print("{}th random-cluster sequence is created." .format(i))               


            
    

    



        
        

