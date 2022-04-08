"""
Script to plot 3d(x,y,z) array of localizationsin randomized clusters for 3d localization sequences.   

Swapnil 2/22
"""

import glob
import pickle
import os
import matplotlib.pyplot as plt

# Are you plotting 2d or 3d data?
plot_3d = True

# Are you plotting 3d localizations from molecule list or from neural network prediction?
mol_list = False

# Do you want to save the plot or just view it?
save = True

# # Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"  

# # Set starting tile and end tile to get localizations from tile sequence for 2D clustering.
# tile_start = 1
# tile_end = 1

# Or give tile sequence number and list of tile numbers in that tile sequence.
# tile_seq = 2
# tile_list = [2, 252, 408]
tile_seq = 1
tile_list = [1]

# Set starting sequence and end sequence to get localizations from tile sequence for 3D clustering.
seq_start = 359
seq_end = 359

# Get localizations sequences directory.
if mol_list: locs_sequences_directory = storm_exp_directory + "random_cluster_sequences_mol_list\\"
    
else: locs_sequences_directory = experiment_directory + "random_cluster_sequences\\"

# Create directory to save plots.
if not os.path.exists(locs_sequences_directory + "plots\\" ):
    os.mkdir(locs_sequences_directory + "plots\\" )
    # os.mkdir(storm_exp_directory + data_directory_str + "locs\\")

plots_directory =  locs_sequences_directory + "plots\\"    

# Get number of 3d localization sequences present in locs_sequences_directory.
total_seqs = len(glob.glob(locs_sequences_directory + "*.data"))

# Iterate over sequences.
# for i in range(1, total_seqs+1):
for i in range(seq_start, seq_end+1):    
    
    # Get the 3d localization sequence filename.
    if mol_list: locs_seq_file_name = locs_sequences_directory + "random_cluster_mol_list_sequence_" + str(i) + ".data"

    else: locs_seq_file_name = locs_sequences_directory + "random_cluster_sequence_" + str(i) + ".data"          
    
    # Read from the file. 
    with open(locs_seq_file_name, 'rb') as filehandle:
        locs3d_seq_arr = pickle.load(filehandle)

    print("shape of random cluster is {}" .format(locs3d_seq_arr.shape))

    # Plot results.
    
    if plot_3d:     
    
        # For 3d plot.                
        ax = plt.axes(projection='3d')        

        # get 3d localization array.
        xy = locs3d_seq_arr
            
        # Plot x,y,z coordinates for 3d localizations.                
        ax.scatter(xy[:, 1], xy[:, 0], xy[:, 2])           

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}" .format(i))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        
        file_name = "locs3d_pred_sequence__{}.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)       
        
        plt.show()

    else:
    
        # get 2d localization array.
        xy = locs3d_seq_arr[:,:2]    

        # Plot x,y coordinates for clusters.    
        plt.plot(
            xy[:, 1],
            xy[:, 0],
            "o",
            # markeredgecolor="k",
            # markersize=14,
            # markersize=4,
        ) 

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}" .format(i))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        
        file_name = "locs2d_pred_sequence__{}.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)       
        
        plt.show()        

            
    

    



        
        

