"""
Script to implement 'dbscan' clustering algorithm  on 2d(x,y) or 3d(x,y,z) array of localizations.   

Swapnil 1/22
"""

"""
Script to implement 'dbscan' clustering algorithm  on 2d(x,y) or 3d(x,y,z) array of localizations.   

Swapnil 1/22
"""

import numpy as np
import glob
import pickle
import os
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn import metrics

# Are you analyzing 2d or 3d data?
cluster_3d = False

# Are you sequencing 3d localizations from molecule list or from neural network prediction?
mol_list = False

# Are you doing control analysis for randomized clusters?
randm = False

# # Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

exp_name = 'experiment_12'

accuracy_directory = expfolder + "Clustering_accuracy\\"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'

# If not present create a new directory for 3d localizations. 
if not os.path.exists(accuracy_experiment_directory + "dbscan_output\\"):
    os.mkdir(accuracy_experiment_directory + "dbscan_output\\")

dbscan_directory = accuracy_experiment_directory + "dbscan_output\\"

if mol_list:
    locs_2d_directory = accuracy_experiment_directory + "locs2d_mol_list\\"
    
    # Get list of tiles with no localizations.
    tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_" + exp_name + ".data"     
    

else: 
    locs_2d_directory = accuracy_experiment_directory + "locs2d_predictions\\"
    
    # Get list of tiles with no localizations.
    tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_pred_" + exp_name + ".data" 

with open(tile_list_no_locs2d_file, 'rb') as filehandle:
    tile_list_no_locs2d = pickle.load(filehandle)
    
print(type(tile_list_no_locs2d[8]))    
 
    
    