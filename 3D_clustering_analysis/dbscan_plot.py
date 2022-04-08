"""
Script to plot 'dbscan' predictions for 3d(x,y,z) array of localizations. 
If cluster_3d is True then script gives 3d plot, if False, then script gives 2d plot (top view of 3d plot).     

Swapnil 1/22
"""

import numpy as np
import glob
import pickle
import os
import matplotlib.pyplot as plt

# Are you ploting 2d or 3d data?
cluster_3d = True

# Are you ploting 3d localizations from molecule list or from neural network prediction?
mol_list = False

# Do you want to save the plot or just view it?
save = False

# Are you doing control analysis for randomized clusters?
randm = False

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

# Set directory for dbscan output of 3d localization sequences.
if mol_list: 
    if randm:
        dbscan_seq_directory = storm_exp_directory + "dbscan_output_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    
    else:
        dbscan_seq_directory = storm_exp_directory + "dbscan_output_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
 
else: 
    if randm:
        dbscan_seq_directory = experiment_directory + "dbscan_output_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     
    
    else:
        dbscan_seq_directory = experiment_directory + "dbscan_output_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     

# Create directory to save plots.
if not os.path.exists(dbscan_seq_directory + "plots\\" ):
    os.mkdir(dbscan_seq_directory + "plots\\" )

plots_directory =  dbscan_seq_directory + "plots\\"

# # Remove previously present files. 
# files = glob.glob(plots_directory + "*.jpg")
# for f in files:
    # os.remove(f)       

# # Set starting tile and end tile to get localizations from tile sequence for 2D clustering.
# tile_start = 1
# tile_end = 1

# # Or give tile sequence number and list of tile numbers in that tile sequence.
# # tile_seq = 2
# # tile_list = [2, 252, 408]
# tile_seq = 1
# tile_list = [1]

seq_start = 571
seq_end = 571
    
# Get number of 3d dbscan result files present in dbscan_seq_directory.
total_seqs = len(glob.glob(dbscan_seq_directory + "*.data"))

# Get localizations sequences directory.
if mol_list: 
    if randm:
        locs_sequences_directory = storm_exp_directory + "random_cluster_sequences_mol_list\\"
    
    else:
        locs_sequences_directory = storm_exp_directory + "locs3d_molecule_list_sequences\\"
    
else: 
    if randm:
        locs_sequences_directory = experiment_directory + "random_cluster_sequences\\"    
    
    else:
        locs_sequences_directory = experiment_directory + "locs3d_pred_sequences\\"    

# Iterate over sequences.
# for i in range(1, total_seqs+1):
for i in range(seq_start, seq_end+1):

    # Get the 3d localization sequence filename.
    if mol_list: 
        if randm:
            locs_seq_file_name = locs_sequences_directory + "random_cluster_mol_list_sequence_" + str(i) + ".data"
        
        else:
            locs_seq_file_name = locs_sequences_directory + "locs3d_molecule_list_sequence_" + str(i) + ".data"

    else: 
        if randm:
            locs_seq_file_name = locs_sequences_directory + "random_cluster_sequence_" + str(i) + ".data" 
        
        else:
            locs_seq_file_name = locs_sequences_directory + "locs3d_pred_sequence_" + str(i) + ".data" 

    # Read from the file. 
    with open(locs_seq_file_name, 'rb') as filehandle:
        locs3d_seq_arr = pickle.load(filehandle)

    # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
    locs3d_seq_arr[:,[0,1]] = locs3d_seq_arr[:,[1,0]]
    
    # Get the DBSCAN result filename for given 3d localization sequence.
    db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(i) + ".data"            
    
    # Read from the file. 
    with open(db_out_file_name, 'rb') as filehandle:
        db = pickle.load(filehandle)      
    
    # Masking the core samples.
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    labels = db.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    # Initialize cluster count for filtered clusters.
    clst_ct = 0

    # # Print results.
    # print(" There are {} estimated number of clusters for tile sequence {}." .format(n_clusters_, i))
    # print("There are {} estimated number of noise points for tile sequence {}." .format(n_noise_, i))        
    # # print("Estimated number of clusters: %d" % n_clusters_)
    # # print("Estimated number of noise points: %d" % n_noise_)
    # # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    # # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    # # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    # # print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
    # # print(
        # # "Adjusted Mutual Information: %0.3f"
        # # % metrics.adjusted_mutual_info_score(labels_true, labels)
    # # )
    # # print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(locs_arr, labels))

    if cluster_3d:

        # Plot results.
        # Plot x,y,z coordinates for clusters.                
        ax = plt.axes(projection='3d')        
        
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k
            noise_mask = labels == -1
            
            # Set the value for cluster size filter.
            # The size limit for clusters is calculated from average size of clusters for random control experiment (See cluster_randomization.py). 
            clst_sz_fltr = 6
            
            # If cluster size is greater than the cluster size filter.
            if (sum(class_member_mask) > clst_sz_fltr):

                # Update cluster count.
                clst_ct += 1             

                # # For plotting only core member points.            
                # xy = locs3d_seq_arr[class_member_mask & core_samples_mask]
                
                # # For plotting all class member points including noise points.
                # xy = locs3d_seq_arr[class_member_mask]

                # For plotting all class member points without noise points.
                xy = locs3d_seq_arr[class_member_mask & ~noise_mask]            
                            
                # Plot x,y,z coordinates for clusters.                
                # ax = plt.axes(projection='3d')
                ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple(col), linewidth=0.5, alpha=1) 

                # # Emphasize individual clusters with black markers.
                # if (clst_ct == 20): 
                    # # Plot x,y,z coordinates for clusters.                
                    # # ax = plt.axes(projection='3d')
                    # ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple([0, 0, 0, 1]), linewidth=1.5, alpha=1)

                # else:
                    # # Plot x,y,z coordinates for clusters.                
                    # # ax = plt.axes(projection='3d')
                    # ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple(col), linewidth=0.5, alpha=1)                
                
                # # Plot x,y coordinates for clusters.    
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 1],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # # markersize=14,
                    # markersize=4,
                # )    
                    
                # # Plot x,z coordinates for clusters.    
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 2],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # # markersize=14,
                    # markersize=4,        
                # )


                # xy = locs_arr[class_member_mask & ~core_samples_mask]
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 1],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # markersize=6,
                # )
                # plt.gca().invert_yaxis()
                # plt.gca().xaxis.tick_top()
                # plt.gca().set_aspect('equal', adjustable='box')    

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}, # of clusters: {}, molecule_list" .format(i, clst_ct-1))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        file_name = "dbscan_out_sequence_{}_3d.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)            
        
        else:
            plt.show()

        if (i%10 == 0):
            print("{}th sequence is analyzed." .format(i))     

    else:
    
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k
            noise_mask = labels == -1                        

            # # For plotting only core member points.            
            # xy = locs3d_seq_arr[class_member_mask & core_samples_mask]
            
            # # For plotting all class member points.
            # xy = locs3d_seq_arr[class_member_mask]

            # For plotting all class member points without noise points.
            xy = locs3d_seq_arr[class_member_mask & ~noise_mask]             
            
            # xy = locs3d_seq_arr[class_member_mask]    # Applying only class member mask.                  
            
            # Plot x,y coordinates for clusters.    
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                # markersize=14,
                markersize=4,
            )    
                
            # # Plot x,z coordinates for clusters.    
            # plt.plot(
                # xy[:, 0],
                # xy[:, 2],
                # "o",
                # markerfacecolor=tuple(col),
                # markeredgecolor="k",
                # # markersize=14,
                # markersize=4,        
            # )


            # xy = locs_arr[class_member_mask & ~core_samples_mask]
            # plt.plot(
                # xy[:, 0],
                # xy[:, 1],
                # "o",
                # markerfacecolor=tuple(col),
                # markeredgecolor="k",
                # markersize=6,
            # )
            # plt.gca().invert_yaxis()
            # plt.gca().xaxis.tick_top()
            # plt.gca().set_aspect('equal', adjustable='box')    

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}, # of clusters: {}, molecule_list" .format(i, n_clusters_))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        file_name = "dbscan_out_sequence_{}_2d_core.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)            
        
        plt.show()                       




            
    

    



        
        

