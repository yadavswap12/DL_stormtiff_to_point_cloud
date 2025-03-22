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
# exp_name = 'experiment_9'
# exp_name = 'experiment_10'
# exp_name = 'experiment_11'

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

        
# Set DBSCAN parameter.

# For 647 channel.

# eps = 1.0
# min_samples = 2    # Bad. Too many clusters.

# eps = 2.0
# min_samples = 2    # Okay. Too few clusters.

# eps = 2.0
# min_samples = 4    # Okay. Fewer clusters.

# eps = 2.0
# min_samples = 6    # Okay. Fewer clusters.

eps = 2.0
min_samples = 8    # Okay. Fewer clusters.

# eps = 2.0
# min_samples = 16    # Okay. Fewer clusters.


# If does not exist, create new directory for dbscan output of 3d localization sequences.
if mol_list:
    if randm:
        if not os.path.exists(dbscan_directory + "dbscan_output_random_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(dbscan_directory + "dbscan_output_random_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")

        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"             
    
    else:
        if not os.path.exists(dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
    
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 

else:
    if randm: 
        if not os.path.exists(dbscan_directory + "dbscan_output_random_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(dbscan_directory + "dbscan_output_random_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        dbscan_seq_directory = dbscan_directory + "dbscan_output_random_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 

    else: 
        if not os.path.exists(dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"         

# Remove previously present files. 
files = glob.glob(dbscan_seq_directory + "*.data")
for f in files:
    os.remove(f)    


# Initialize tile counter.
tl_ct = 1

if cluster_3d:

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
    
    # Get number of 3d localization sequences present in locs_sequences_directory.
    total_seqs = len(glob.glob(locs_sequences_directory + "*.data"))
    
    files = glob.glob(locs_sequences_directory + "*.data")    
    
    # Iterate over sequences.
    for file in files:
                     
        locs_seq_file_name = file
        
        # Get the sequence number present in the filename.
        i = int(locs_seq_file_name.split("_")[-1][:-5])         
        
        # Set the DBSCAN result filename for given 3d localization sequence.
        db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(i) + ".data"            
        
        # Read from the file. 
        with open(locs_seq_file_name, 'rb') as filehandle:
            locs3d_seq_arr = pickle.load(filehandle)

        # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
        locs3d_seq_arr[:,[0,1]] = locs3d_seq_arr[:,[1,0]]
        
        # print("There are total of {} points." .format(len(locs3d_seq_arr)))            
        
        # Compute dbscan.
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(locs3d_seq_arr)
        
        # Set the DBSCAN result filename for given 3d localization sequence.
        db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(i) + ".data"           

        # Writting the dbscan output to files. 
        with open(db_out_file_name, 'wb') as filehandle:
            # store the data as binary data stream.
            pickle.dump(db, filehandle)         
        
        # Masking the core samples.
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True

        labels = db.labels_
        
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        # Print results.
        print(" There are {} estimated number of clusters for tile sequence {}." .format(n_clusters_, i))
        print("There are {} estimated number of noise points for tile sequence {}." .format(n_noise_, i))        
        # print("Estimated number of clusters: %d" % n_clusters_)
        # print("Estimated number of noise points: %d" % n_noise_)
        # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
        # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
        # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
        # print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
        # print(
            # "Adjusted Mutual Information: %0.3f"
            # % metrics.adjusted_mutual_info_score(labels_true, labels)
        # )
        # print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(locs_arr, labels))

        # # Plot results.
        
        # # Plot x,y,z coordinates for clusters.                
        # ax = plt.axes(projection='3d')        
        
        # # Black removed and is used for noise instead.
        # unique_labels = set(labels)
        # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        # for k, col in zip(unique_labels, colors):
            # if k == -1:
                # # Black used for noise.
                # col = [0, 0, 0, 1]

            # class_member_mask = labels == k
            # noise_mask = labels == -1
            
            # # For plotting only core member points.            
            # xy = locs3d_seq_arr[class_member_mask & core_samples_mask]
            
            # # # For plotting all class member points.
            # # xy = locs3d_seq_arr[class_member_mask]

            # # # For plotting all class member points without noise points.
            # # xy = locs3d_seq_arr[class_member_mask & ~noise_mask]               
                        
            # # Plot x,y,z coordinates for clusters.                
            # # ax = plt.axes(projection='3d')
            # ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple(col), linewidth=0.5)        
            
            # # # Plot x,y coordinates for clusters.    
            # # plt.plot(
                # # xy[:, 0],
                # # xy[:, 1],
                # # "o",
                # # markerfacecolor=tuple(col),
                # # markeredgecolor="k",
                # # # markersize=14,
                # # markersize=4,
            # # )    
                
            # # # Plot x,z coordinates for clusters.    
            # # plt.plot(
                # # xy[:, 0],
                # # xy[:, 2],
                # # "o",
                # # markerfacecolor=tuple(col),
                # # markeredgecolor="k",
                # # # markersize=14,
                # # markersize=4,        
            # # )


            # # xy = locs_arr[class_member_mask & ~core_samples_mask]
            # # plt.plot(
                # # xy[:, 0],
                # # xy[:, 1],
                # # "o",
                # # markerfacecolor=tuple(col),
                # # markeredgecolor="k",
                # # markersize=6,
            # # )
            # # plt.gca().invert_yaxis()
            # # plt.gca().xaxis.tick_top()
            # # plt.gca().set_aspect('equal', adjustable='box')    

        # plt.gca().invert_yaxis()
        # # plt.gca().xaxis.tick_top()
        # # plt.gca().set_aspect('equal', adjustable='box')
        # plt.title("Sequence: {}, # of clusters: {}, molecule_list" .format(i, n_clusters_))        
        # # plt.title("Estimated number of clusters: %d" % n_clusters_)
        # plt.show()

        if (tl_ct%100 == 0):
            print("{}th tile is analyzed." .format(tl_ct))    

        tl_ct += 1        

else:

    
    # files = glob.glob(locs_2d_directory + "*.data")
    # files = glob.glob(locs_2d_directory + "*cart*")
    files = glob.glob(locs_2d_directory + "*pixel*")            
    
    # Iterate over tiles.
    for file in files:    
    # for file in files[:20]:
                     
        locs_tile_file_name = file
        
        # Get the sequence number present in the filename.
        tile_num = int(locs_tile_file_name.split("_")[-1][:-5])

        if tile_num not in tile_list_no_locs2d:        

    
    
            # Get 2d localizations directory.
            if mol_list: 
            
                locs2d_file_name = locs_2d_directory + "locs2d_molecule_list_pixel_tile_" + str(tile_num) + ".data"            

            else: 
            
                locs2d_file_name = locs_2d_directory + "locs2d_pred_pixel_tile_" + str(tile_num) + ".data"             
                                 
            with open(locs2d_file_name, 'rb') as filehandle:
                locs_2d = pickle.load(filehandle)
               
            # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs_arr. 
            locs_2d[:,[0,1]] = locs_2d[:,[1,0]]     

            # Compute dbscan.
            db = DBSCAN(eps=eps, min_samples=min_samples).fit(locs_2d)

            # Set the DBSCAN result filename for given 3d localization sequence.
            db_out_file_name = dbscan_seq_directory + "dbscan_out_tile_" + str(tile_num) + ".data"           

            # Writting the dbscan output to files. 
            with open(db_out_file_name, 'wb') as filehandle:
                # store the data as binary data stream.
                pickle.dump(db, filehandle)         
            
                                                                                
            # Masking the core samples.
            core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
            core_samples_mask[db.core_sample_indices_] = True

            labels = db.labels_

            # Number of clusters in labels, ignoring noise if present.
            n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise_ = list(labels).count(-1)

            # # Plot results.
            # # Black removed and is used for noise instead.
            # unique_labels = set(labels)
            # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
            # for k, col in zip(unique_labels, colors):
                # if k == -1:
                    # # Black used for noise.
                    # col = [0, 0, 0, 1]

                # class_member_mask = labels == k

                # xy = locs_arr[class_member_mask & core_samples_mask]
                
                # # Plot x,y coordinates for clusters.    
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 1],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # # markeredgecolor="k",
                    # # markersize=14,
                    # markersize=4,
                # )    

                # # xy = locs_arr[class_member_mask & ~core_samples_mask]
                # # plt.plot(
                    # # xy[:, 0],
                    # # xy[:, 1],
                    # # "o",
                    # # markerfacecolor=tuple(col),
                    # # markeredgecolor="k",
                    # # markersize=6,
                # # )
                # # plt.gca().invert_yaxis()
                # # plt.gca().xaxis.tick_top()
                # # plt.gca().set_aspect('equal', adjustable='box')    

            # plt.gca().invert_yaxis()
            # # plt.gca().xaxis.tick_top()
            # # plt.gca().set_aspect('equal', adjustable='box')
            # plt.title("Sequence: {}, # of clusters: {}" .format(tile_seq, n_clusters_))            
            # # plt.title("Estimated number of clusters: %d" % n_clusters_)
            # plt.show()
            
            
        if (tl_ct%100 == 0):
            print("{}th tile is analyzed." .format(tl_ct))    

        tl_ct += 1                  


            
    

    



        
        

