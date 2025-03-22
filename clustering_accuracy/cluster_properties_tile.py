"""
Script to get print cluster properties for given tile of localizations.

Swapnil 08/24
"""

import glob
import pickle
import os


# Are you sequencing 3d localizations from molecule list or from neural network prediction?
mol_list = True

# Are you doing control analysis for randomized clusters?
randm = False

# # Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

exp_name = 'experiment_12'

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
if mol_list: 
    if randm:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_random_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    
    else:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
 
else: 
    if randm:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_random_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     
    
    else:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     

# Create directory to save plots.
if not os.path.exists(dbscan_seq_directory + "stats\\" ):
    os.mkdir(dbscan_seq_directory + "stats\\" )

stats_directory =  dbscan_seq_directory + "stats\\"

# Get tile number.
tile_num = 18131

# Set the filename for cluster stats from given 3d localization sequence.
cl_stats_file_name = stats_directory + "cluster_stats_tile_" + str(tile_num) + ".data" 
   
# Read from the file. 
with open(cl_stats_file_name, 'rb') as filehandle:
    cl_stats = pickle.load(filehandle)
    
print(f"Number of clusters is {cl_stats[0]}.")    
      
print(f"Number of noise points is {cl_stats[1]}.")

i=1
for key in cl_stats[2][0].keys():
    print(f"Cluster center of {i}th cluster is {cl_stats[2][0][key]}")
    i+=1
    
i=1
for key in cl_stats[2][1].keys():
    print(f"Cluster size of {i}th cluster is {cl_stats[2][1][key]}")
    i+=1  

i=1
for key in cl_stats[2][2].keys():
    print(f"Cluster area of {i}th cluster is {cl_stats[2][2][key]}")
    i+=1 

i=1
for key in cl_stats[2][3].keys():
    print(f"Cluster volume of {i}th cluster is {cl_stats[2][3][key]}")
    i+=1     
