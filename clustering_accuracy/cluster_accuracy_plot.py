"""
Script to plot histograms of different properties of clusters predicted by dbscan algorithm 3d(x,y,z) sequences of localizations.

Swapnil 2/22
"""

import glob
import pickle
import os
import matplotlib.pyplot as plt

# Do you want to save the plot or just view it?
save = True

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

# Create directory to save results.
if not os.path.exists(dbscan_accuracy_directory + "plots\\" ):
    os.mkdir(dbscan_accuracy_directory + "plots\\" )

dbscan_accuracy_plots_directory = dbscan_accuracy_directory + "plots\\"

# Set the filename for cluster stats from given 3d localization sequence.

if single_cluster:
    cl_acc_file_name = dbscan_accuracy_directory + "cluster_accuracy_single_clusters_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".data"       
else:
    cl_acc_file_name = dbscan_accuracy_directory + "cluster_accuracy_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".data"       

# Read from the file. 
with open(cl_acc_file_name, 'rb') as filehandle:
    cl_acc_dict = pickle.load(filehandle) 



    

if not single_cluster: 

    # Plot histogram for 'number of clusters' difference.
    # plt.hist(cl_acc_dict['num_clust_diff_list'],10000)
    
    # plt.hist(cl_acc_dict['num_clust_diff_list'], len(cl_acc_dict['num_clust_diff_list']))
    # plt.hist(cl_acc_dict['num_clust_diff_list'], len(cl_acc_dict['num_clust_diff_list'])//4)
    plt.hist(cl_acc_dict['num_clust_diff_list'], 100)
    
    
    # plt.hist(cl_acc_dict['num_clust_diff_list'])
    # plt.xlim([0, 40])
    # plt.ylim([0, 10])
    plt.title("'number of clusters' difference")        
    # plt.title("Estimated number of clusters: %d" % n_clusters_)

    if single_cluster:
        file_name = "single_clusters_number_of_clusters_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
    else:
        file_name = "number_of_clusters_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
       
    if save:
        # plt.savefig(locs_pred_directory + file_name, dpi = 300)
        plt.savefig(dbscan_accuracy_plots_directory + file_name)            

    plt.show()




# # Plot histogram for 'number of noise points' difference.
# # plt.hist(cl_acc_dict['num_noise_points_diff_list'],10000)
# plt.hist(cl_acc_dict['num_noise_points_diff_list'], len(cl_acc_dict['num_noise_points_diff_list']))
# # plt.hist(cl_acc_dict['num_noise_points_diff_list'])
# # plt.xlim([0, 40])
# # plt.ylim([0, 10])
# plt.title("'number of noise points' difference")        
# # plt.title("Estimated number of clusters: %d" % n_clusters_)
# file_name = "number_of_noise_points_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
   
# if save:
    # # plt.savefig(locs_pred_directory + file_name, dpi = 300)
    # plt.savefig(dbscan_accuracy_plots_directory + file_name)            

# plt.show()
 
 


# Plot histogram for 'cluster location' difference.
# plt.hist(cl_acc_dict['clust_loc_diff_list'],10000)

# plt.hist(cl_acc_dict['clust_loc_diff_list'], len(cl_acc_dict['clust_loc_diff_list']))
# plt.hist(cl_acc_dict['clust_loc_diff_list'], len(cl_acc_dict['clust_loc_diff_list'])//4)
plt.hist(cl_acc_dict['clust_loc_diff_list'], 100)

# plt.hist(cl_acc_dict['clust_loc_diff_list'])
# plt.xlim([0, 40])
# plt.ylim([0, 10])
plt.title("'cluster location' difference")        
# plt.title("Estimated number of clusters: %d" % n_clusters_)

if single_cluster:
    file_name = "single_clusters_cluster_location_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
else:
    file_name = "cluster_location_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
   
if save:
    # plt.savefig(locs_pred_directory + file_name, dpi = 300)
    plt.savefig(dbscan_accuracy_plots_directory + file_name)            

plt.show()




# Plot histogram for 'relative cluster size' difference.
# plt.hist(cl_acc_dict['clust_size_diff_list'],10000)

# plt.hist(cl_acc_dict['rel_clust_size_diff_list'], len(cl_acc_dict['rel_clust_size_diff_list']))
# plt.hist(cl_acc_dict['rel_clust_size_diff_list'], len(cl_acc_dict['rel_clust_size_diff_list'])//4)
plt.hist(cl_acc_dict['rel_clust_size_diff_list'], 100)


# plt.hist(cl_acc_dict['clust_size_diff_list'])
# plt.xlim([0, 40])
# plt.ylim([0, 10])
plt.title("'relative cluster size' difference")        
# plt.title("Estimated number of clusters: %d" % n_clusters_)

if single_cluster:
    file_name = "single_clusters_relative_cluster_size_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
else:
    file_name = "relative_cluster_size_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
   
if save:
    # plt.savefig(locs_pred_directory + file_name, dpi = 300)
    plt.savefig(dbscan_accuracy_plots_directory + file_name)            

plt.show()  




# Plot histogram for 'raltive cluster area' difference.
# plt.hist(cl_acc_dict['clust_area_diff_list'],10000)

# plt.hist(cl_acc_dict['rel_clust_area_diff_list'], len(cl_acc_dict['rel_clust_area_diff_list']))
# plt.hist(cl_acc_dict['rel_clust_area_diff_list'], len(cl_acc_dict['rel_clust_area_diff_list'])//4)
plt.hist(cl_acc_dict['rel_clust_area_diff_list'], 100)

# plt.hist(cl_acc_dict['clust_area_diff_list'])
# plt.xlim([0, 40])
# plt.ylim([0, 10])
plt.title("'raltive cluster area' difference")        
# plt.title("Estimated number of clusters: %d" % n_clusters_)

if single_cluster:
    file_name = "single_clusters_relative_cluster_area_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
else: 
    file_name = "relative_cluster_area_difference_hist_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + ".jpg" 
   
if save:
    # plt.savefig(locs_pred_directory + file_name, dpi = 300)
    plt.savefig(dbscan_accuracy_plots_directory + file_name)            

plt.show()  







            
    

    



        
        

