"""
Script to plot histograms of different properties of clusters predicted by dbscan algorithm 3d(x,y,z) sequences of localizations.

Swapnil 2/22
"""

import glob
import pickle
import os
import matplotlib.pyplot as plt

# Are you sequencing 3d localizations from molecule list or from neural network prediction?
mol_list = False

# Are you doing control analysis for randomized clusters?
randm = True

# Do you want to save the plot or just view it?
save = True

# # Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Get dbscan parameters.
eps = 22.0
min_samples = 6

# If does not exist, create new directory for cluster stats from 3d localization sequences.
if mol_list:
    if randm:
        if not os.path.exists(storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

    else:
        if not os.path.exists(storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    

else:
    if randm:
        if not os.path.exists(experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"
    
    
    else:
        if not os.path.exists(experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

# # Remove previously present files in the folder.
# files = glob.glob(cl_stats_directory + "*.data") 
# for file in files:
    # os.remove(file)

# Set starting sequence and end sequence to get localizations from tile sequence for 3D clustering.
seq_start = 1
seq_end = 1
    
# Get number of 3d localization sequences present in cluster_stats directory.
total_seqs = len(glob.glob(cl_stats_directory + "*.data"))

files = glob.glob(cl_stats_directory + "*.data")             

# Initialize cluster property value.
clust_sz = 0
clust_ar = 0
clust_vl = 0

# Initialize cluster property lists.
clust_sz_l = []
clust_ar_l = []
clust_vl_l = []       

# Initialize cluster property counter.
clust_count = 0    

# Iterate over sequences.
for file in files:        

    # Set the filename for cluster stats from given 3d localization sequence.
    cl_stats_file_name = file        
    
    # Read from the file. 
    with open(cl_stats_file_name, 'rb') as filehandle:
        cl_stats = pickle.load(filehandle)
        
    # Get the sequence number present in the filename.
    seq = int(cl_stats_file_name.split("_")[-1][:-5])                     
    
    # Get the cluster properties from cluster stat list.
    # Get the number of clusters predicted.        
    num_cl = cl_stats[0]
    
    # Get the number of noise points predicted.
    num_ns = cl_stats[1]         

    # Get tupple of dictionaries (with unique cluster labels as key) for different cluster stats.
    dicts = cl_stats[2]             
    
    # Get dictionary for cluster centers.
    cl_cntr_dict = dicts[0]  

    # Get dictionary for cluster sizes.
    cl_sz_dict = dicts[1]

    # Get dictionary for cluster areas.
    cl_ar_dict = dicts[2] 

    # Get dictionary for cluster volumes.
    cl_vl_dict = dicts[3]

    # Iterate over all values in dictionary.
    for key in cl_sz_dict.keys():
    
        # Compute averages.
        clust_sz += cl_sz_dict[key]
        clust_ar += cl_ar_dict[key]
        clust_vl += cl_vl_dict[key]            
        clust_count += 1
        
        # Update cluster property lists.
        clust_sz_l.append(cl_sz_dict[key])            
        
    if (seq%100 == 0):
        print("{}th sequence is analyzed." .format(seq))               
        
clust_sz_avg = clust_sz/clust_count
clust_ar_avg = clust_ar/clust_count       
clust_vl_avg = clust_vl/clust_count

print("average cluster size: {}, average cluster area: {}, average cluster volume: {}" .format(clust_sz_avg, clust_ar_avg, clust_vl_avg))

# Plot histogram of a cluster property.
plt.hist(clust_sz_l,10000)
plt.xlim([0, 40])
# plt.ylim([0, 10])
plt.title("Cluster size histogram")        
# plt.title("Estimated number of clusters: %d" % n_clusters_)
file_name = "cluster_size_hist.jpg"    
if save:
    # plt.savefig(locs_pred_directory + file_name, dpi = 300)
    plt.savefig(cl_stats_directory + file_name)            

plt.show()          

# Save averages to file
with open(cl_stats_directory + "cluster_stats_avg.csv","a") as f_out:
    f_out.write("average cluster size: {}, average cluster area: {}, average cluster volume: {}\n" .format(clust_sz_avg, clust_ar_avg, clust_vl_avg))



            
    

    



        
        

