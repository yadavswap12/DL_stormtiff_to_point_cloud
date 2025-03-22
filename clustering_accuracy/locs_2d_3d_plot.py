"""
Script to plot 2d(x,y)3d or (x,y,z) array of localizations.   

Swapnil 08/24
"""

import glob
import pickle
import os
import matplotlib.pyplot as plt

# Are you plotting 2d or 3d data?
plot_3d = False

# Are you plotting 3d localizations from molecule list or from neural network prediction?
mol_list = True

# Do you want to save the plot or just view it?
save = False

# # Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

accuracy_directory = expfolder + "Clustering_accuracy\\"

exp_name = "experiment_12"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"


if mol_list: 
    locs_2d_directory = accuracy_experiment_directory + "locs2d_mol_list\\"
else:
    locs_2d_directory = accuracy_experiment_directory + "locs2d_predictions\\"    


# storm_exp_directory = expfolder + storm_exp_name + "\\"

# experiment_directory = storm_exp_directory + "experiment1\\"  

tile_id_list = [18139]       

if save: 

    # Create directory to save plots.
    if not os.path.exists(locs_sequences_directory + "plots\\" ):
        os.mkdir(locs_sequences_directory + "plots\\" )
        # os.mkdir(storm_exp_directory + data_directory_str + "locs\\")

    plots_directory =  locs_sequences_directory + "plots\\"    

# Iterate over tiles list.
for num in range(len(tile_id_list)):   

    
    # Get the 3d localization sequence filename.
    # if mol_list: locs_tile_file_name = locs_2d_directory + "locs2d_molecule_list_cart_tile_" + str(tile_id_list[num]) + ".data"
    # else: locs_tile_file_name = locs_2d_directory + "locs2d_pred_cart_tile_" + str(tile_id_list[num]) + ".data"

    if mol_list: locs_tile_file_name = locs_2d_directory + "locs2d_molecule_list_pixel_tile_" + str(tile_id_list[num]) + ".data"
    else: locs_tile_file_name = locs_2d_directory + "locs2d_pred_pixel_tile_" + str(tile_id_list[num]) + ".data"          
    
    
    
    # Read from the file. 
    with open(locs_tile_file_name, 'rb') as filehandle:
        locs2d_tile_arr = pickle.load(filehandle)

    print("shape of random cluster is {}" .format(locs2d_tile_arr.shape))

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
        
        file_name = "locs3d_pred_sequence_{}.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)       
        
        plt.show()

    else:
    
        # get 2d localization array.
        xy = locs2d_tile_arr    

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
        plt.title("Tile: {}" .format(tile_id_list[num]))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)        
        
        
        
        # if mol_list: file_name = "locs2d_molecule_list_cart_tile_{}.jpg" .format(tile_id_list[num])
        # else: file_name = "locs2d_pred_cart_tile_{}.jpg" .format(tile_id_list[num]) 
        
        if mol_list: file_name = "locs2d_molecule_list_pixel_tile_{}.jpg" .format(tile_id_list[num])
        else: file_name = "locs2d_pred_pixel_tile_{}.jpg" .format(tile_id_list[num])         
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)       
        
        plt.show()        

            
    

    



        
        

