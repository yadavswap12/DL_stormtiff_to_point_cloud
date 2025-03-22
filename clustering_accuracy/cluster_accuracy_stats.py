"""
Script to compute differences in cluster properties of molecule-list and NN-predicted localizations.

Swapnil 08/24
"""

import numpy as np
import glob
import pickle
import os
import math

# Are you plotting only single cluster results?
single_cluster = False

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

storm_exp_directory = expfolder + storm_exp_name + "\\"

# experiment_directory = storm_exp_directory + "experiment1\\"

# Get dbscan parameters.

# For 647 channel.
eps = 2.0
min_samples = 8

dbscan_accuracy_directory = accuracy_experiment_directory + "dbscan_accuracy\\"

# Set the filename for cluster stats from given 3d localization sequence.

if single_cluster:
    cl_acc_file_name = dbscan_accuracy_directory + "cluster_accuracy_single_clusters_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".data"       
else:
    cl_acc_file_name = dbscan_accuracy_directory + "cluster_accuracy_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".data"       

# Read from the file. 
with open(cl_acc_file_name, 'rb') as filehandle:
    cl_acc_dict = pickle.load(filehandle)
    
    
    
if not single_cluster: 

    # Get mean of the distribution.
    clust_loc_diff_mean = np.mean(cl_acc_dict['clust_loc_diff_list'])
    rel_clust_size_diff_mean = np.mean(cl_acc_dict['rel_clust_size_diff_list'])
    rel_clust_area_diff_mean = np.mean(cl_acc_dict['rel_clust_area_diff_list'])
    
    
    # Get standard-deviation of the distribution.    
    clust_loc_diff_std = np.std(cl_acc_dict['clust_loc_diff_list'])
    rel_clust_size_diff_std = np.std(cl_acc_dict['rel_clust_size_diff_list'])
    rel_clust_area_diff_std = np.std(cl_acc_dict['rel_clust_area_diff_list'])
    
    
    # Get 10th percentile of distribution.    
    clust_loc_diff_10_pctl = np.percentile(cl_acc_dict['clust_loc_diff_list'],10)
    rel_clust_size_diff_10_pctl = np.percentile(cl_acc_dict['rel_clust_size_diff_list'],10)    
    rel_clust_area_diff_10_pctl = np.percentile(cl_acc_dict['rel_clust_area_diff_list'],10)    
    
    
    # Get 90th percentile of distribution.    
    clust_loc_diff_90_pctl = np.percentile(cl_acc_dict['clust_loc_diff_list'],90)
    rel_clust_size_diff_90_pctl = np.percentile(cl_acc_dict['rel_clust_size_diff_list'],90)
    rel_clust_area_diff_90_pctl = np.percentile(cl_acc_dict['rel_clust_area_diff_list'],90)
    
    
    
    out_file_name = dbscan_accuracy_directory + "cluster_accuracy_stats_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".csv"       
    
    with open(out_file_name,"a") as f_out:
        f_out.write(f"Mean of cluster location difference is {clust_loc_diff_mean}.\n") 
        f_out.write(f"Mean of relative cluster size difference is {rel_clust_size_diff_mean}.\n")
        f_out.write(f"Mean of relative cluster area difference is {rel_clust_area_diff_mean}.\n") 
        
        f_out.write("\n") 
        
        f_out.write(f"standard deviation of cluster location difference is {clust_loc_diff_std}.\n") 
        f_out.write(f"standard deviation of relative cluster size difference is {rel_clust_size_diff_std}.\n")
        f_out.write(f"standard deviation of relative cluster area difference is {rel_clust_area_diff_std}.\n")

        f_out.write("\n") 
        
        f_out.write(f"10th percentile of cluster location difference is {clust_loc_diff_10_pctl}.\n") 
        f_out.write(f"10th percentile of relative cluster size difference is {rel_clust_size_diff_10_pctl}.\n")
        f_out.write(f"10th percentile of relative cluster area difference is {rel_clust_area_diff_10_pctl}.\n")
        
        f_out.write("\n") 
        
        f_out.write(f"90th percentile of cluster location difference is {clust_loc_diff_90_pctl}.\n") 
        f_out.write(f"90th percentile of relative cluster size difference is {rel_clust_size_diff_90_pctl}.\n")
        f_out.write(f"90th percentile of relative cluster area difference is {rel_clust_area_diff_90_pctl}.\n")
        
        
        
        
        
        
    
    
    
    





        
        
            
            




















































        
