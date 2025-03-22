"""
Script to compute differences in cluster properties of molecule-list and NN-predicted localizations.

Swapnil 08/24
"""

import glob
import pickle
import os
import math

# # Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

exp_name = 'experiment_12'
# exp_name = 'experiment_9'
# exp_name = 'experiment_10'
# exp_name = 'experiment_11'

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

accuracy_directory = expfolder + "Clustering_accuracy\\"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'

dbscan_directory = accuracy_experiment_directory + "dbscan_output\\"  

# Get dbscan parameters.

# For 647 channel.
eps = 2.0
min_samples = 8

# Set directory for dbscan output of 2d localizations.
dbscan_tile_mol_list_directory = dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
dbscan_tile_pred_directory = dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

# Get list of tiles with no localizations.
tile_list_no_locs2d_mol_list_file = accuracy_experiment_directory + "tile_list_no_locs2d_" + exp_name + ".data"
        
with open(tile_list_no_locs2d_mol_list_file, 'rb') as filehandle:
    tile_list_no_locs2d_mol_list = pickle.load(filehandle)

tile_list_no_locs2d_pred_file = accuracy_experiment_directory + "tile_list_no_locs2d_pred_" + exp_name + ".data"

with open(tile_list_no_locs2d_pred_file, 'rb') as filehandle:
    tile_list_no_locs2d_pred = pickle.load(filehandle)


stats_mol_list_directory =  dbscan_tile_mol_list_directory + "stats\\"      
stats_pred_directory =  dbscan_tile_pred_directory + "stats\\"      
     

# Create directory to save results.
if not os.path.exists(accuracy_experiment_directory + "dbscan_accuracy\\" ):
    os.mkdir(accuracy_experiment_directory + "dbscan_accuracy\\" )

dbscan_accuracy_directory = accuracy_experiment_directory + "dbscan_accuracy\\"

# Set the filename for cluster stats from given 3d localization sequence.
cl_acc_file_name = dbscan_accuracy_directory + "cluster_accuracy_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".data"       

# We will compute the accuracies only for dbscan output results common to molecule-list and NN-predictions.

# Get all files in molecule-list dbscan results.
# files = glob.glob(dbscan_tile_mol_list_directory + "*pixel*")
files = glob.glob(dbscan_tile_mol_list_directory + "*.data")

# Function to compute distance between two lists of (x,y) co-ordinates.
def get_dist(list1, list2):
    return math.sqrt((list1[0]-list2[0])**2 + (list1[1]-list2[1])**2)



# Initialize accuracy lists.
tile_list = []
num_clust_diff = []
# rel_num_noise_points_diff = [] 
clust_loc_diff = [] 
rel_clust_size_diff = []
rel_clust_area_diff = []



# Iterate over sequences.
for file in files:

    locs_tile_file_name = file
    
    # Get the sequence number present in the filename.
    tile_num = int(locs_tile_file_name.split("_")[-1][:-5])

    if (tile_num not in tile_list_no_locs2d_pred) and (tile_num not in tile_list_no_locs2d_mol_list):
    
        tile_list.append(tile_num)

        # Set the filename for cluster stats from given 3d localization sequence.
        cl_stats_mol_list_file_name = stats_mol_list_directory + "cluster_stats_tile_" + str(tile_num) + ".data"
        cl_stats_pred_file_name = stats_pred_directory + "cluster_stats_tile_" + str(tile_num) + ".data"         
           
        # Read from the file. 
        with open(cl_stats_mol_list_file_name, 'rb') as filehandle:
            cl_stats_mol_list = pickle.load(filehandle)

        with open(cl_stats_pred_file_name, 'rb') as filehandle:
            cl_stats_pred = pickle.load(filehandle)

        # Get number of cluster difference.
        num_clust_diff.append(cl_stats_pred[0]-cl_stats_mol_list[0])

        # # Get number of noise-points difference.
        # rel_num_noise_points_diff.append((cl_stats_pred[1]-cl_stats_mol_list[1])/max(cl_stats_pred[1], cl_stats_mol_list[1]))
        
        if cl_stats_pred[0] <= cl_stats_mol_list[0]:
            
            for key1 in cl_stats_pred[2][0].keys():
                
                # Initialize min_dist to a large value (larger than tile-diagonal length).
                min_dist = 100000000.0
                key_del = None
                
                for key2 in cl_stats_mol_list[2][0].keys():
                    
                    dist = get_dist(cl_stats_pred[2][0][key1], cl_stats_mol_list[2][0][key2])
                    
                    if dist < min_dist:
                        min_dist = dist
                        key_del = key2
                        
                        
                clust_loc_diff.append(min_dist)
                rel_clust_size_diff.append((cl_stats_pred[2][1][key1]-cl_stats_mol_list[2][1][key_del])/max(cl_stats_pred[2][1][key1], cl_stats_mol_list[2][1][key_del]))                
                rel_clust_area_diff.append((cl_stats_pred[2][2][key1]-cl_stats_mol_list[2][2][key_del])/max(cl_stats_pred[2][2][key1], cl_stats_mol_list[2][2][key_del])) 
                
                # Delete the cluster from inner loop which was already paired with cluster from outer loop.
                del cl_stats_mol_list[2][0][key_del]
                
        else:        

            for key1 in cl_stats_mol_list[2][0].keys():
                
                # Initialize min_dist to a large value (larger than tile-diagonal length).
                min_dist = 100000000.0
                key_del = None
                
                for key2 in cl_stats_pred[2][0].keys():
                    
                    dist = get_dist(cl_stats_pred[2][0][key2], cl_stats_mol_list[2][0][key1])
                    
                    if dist < min_dist:
                        min_dist = dist
                        key_del = key2
                        
                        
                clust_loc_diff.append(min_dist)
                rel_clust_size_diff.append((cl_stats_pred[2][1][key_del]-cl_stats_mol_list[2][1][key1])/max(cl_stats_pred[2][1][key_del], cl_stats_mol_list[2][1][key1]))                
                rel_clust_area_diff.append((cl_stats_pred[2][2][key_del]-cl_stats_mol_list[2][2][key1])/max(cl_stats_pred[2][2][key_del], cl_stats_mol_list[2][2][key1])) 
                
                # Delete the cluster from inner loop which was already paired with cluster from outer loop.
                del cl_stats_pred[2][0][key_del]                


# Define cluster accuracy dictionary and update it with lists of results
cl_acc_dict = {}
cl_acc_dict['tile_list'] = tile_list 
cl_acc_dict['num_clust_diff_list'] = num_clust_diff 
# cl_acc_dict['num_noise_points_diff_list'] = rel_num_noise_points_diff 
cl_acc_dict['clust_loc_diff_list'] = clust_loc_diff 
cl_acc_dict['rel_clust_size_diff_list'] = rel_clust_size_diff 
cl_acc_dict['rel_clust_area_diff_list'] = rel_clust_area_diff 

    
        
# Writting the cluster stats list to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
with open(cl_acc_file_name, 'wb') as filehandle:
    # store the data as binary data stream.
    pickle.dump(cl_acc_dict, filehandle)         

        
        
            
            




















































        
