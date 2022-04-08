"""
Test code to plot localizations found in tiles from given image section.
Each localization is assigned a random position inside the pixel.

Swapnil 10/21
"""

import numpy as np
import glob
import pickle
import itertools
import matplotlib.pyplot as plt
import random

# Set path to training data files
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Specify the tile-size of storm image section for training data.
tile_size = 72

data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_sorted\\"

# num_locs_directory = storm_exp_directory + data_directory_str + "num_locs\\"
num_locs_pred_directory = experiment_directory + "model_predictions\\"
# num_locs_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"
# num_locs_directory = storm_exp_directory + data_directory_str + "num_locs_estimate_no_nn_avg\\"
tiles_directory = storm_exp_directory + data_directory_str + "tiles\\"    

# Get number of tiles.
total_tiles = len(glob.glob(tiles_directory + "*.data"))

# Which tile localizations do you want to plot?
tile_num = 41

# Get the ith tile.
tile_file = tiles_directory + "tile_" + str(tile_num) + ".data"

# Read from .data files. 
with open(tile_file, 'rb') as filehandle:
    tile = pickle.load(filehandle)

# Get the files where the number of localizations for ith tile is stored.    
# num_locs_tile_file_name = num_locs_directory + "storm_num_locs_tile_" + str(tile_num) + ".data"
num_locs_pred_tile_file_name = num_locs_pred_directory + "tile_pred_num_locs_tile_" + str(tile_num) + ".data"
# num_locs_tile_file_name = num_locs_directory + "storm_num_locs_est_lin_fit_tile_" + str(tile_num) + ".data"
# num_locs_tile_file_name = num_locs_directory + "storm_num_locs_est_quad_fit_tile_" + str(tile_num) + ".data"

# # Read the localizations from file for number of localizations for ith tile.      
# with open(num_locs_tile_file_name, 'rb') as filehandle:
    # num_locs_tile = pickle.load(filehandle)
 
# Read the localizations from file for number of localizations for ith tile.      
with open(num_locs_pred_tile_file_name, 'rb') as filehandle:
    num_locs_pred_tile = pickle.load(filehandle) 
    
# Initialize localizations list.
a = []

counter = 0      
    
for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):

    # num_locs_tile.append(len(df[(df["y_floor"] == j) & (df["x_floor"] == i)]))
    # num_locs = num_locs_tile[counter]
    num_locs = num_locs_pred_tile[0, counter] 

    # Choose number of floating points for random floats.
    fl_pt = 3

    # New version which assigns all localizations different random position within pixel.
    # Initialize localizations list for random positions within pixel. 
    num_loc_pred_pixel = []
    num_loc_est_pixel = []
    num_loc_pixel = []    

    # For every localization in given pixel.
    for num_loc in range(round(num_locs)):
        num_loc_pixel.append(np.array([random.randint((j)*10**fl_pt, (j+1)*10**fl_pt)/10**fl_pt, random.randint((i)*10**fl_pt, (i+1)*10**fl_pt)/10**fl_pt]))                    

    # # Take care of zero localizations case so that number of localization estimates array and image tile has same shape.
    # if (num_locs==0): num_locs = -1

    # # Assign the number of localizations to pixel centre and make a list.  
    # a_pixel = round(num_locs)*[np.array([j+1/2, i+1/2])]
    
    # Add the pixel list to final localizations list.
    # a.extend(a_pixel)
    a.extend(num_loc_pixel)    

    counter += 1

# Convert list to numpy array.
a = np.array(a)     

print("length of locs_est is {}" .format(len(a)))
print("shape of locs_est is {}" .format(a.shape))             
    
# Plot ith tile.
plt.subplot(1, 2, 1)
plt.imshow(tile, cmap='gray')
plt.colorbar()
plt.gca().xaxis.tick_top()
# plt.legend(labels=['tile'])
# plt.title("tile_{}" .format(tile_num), pad=30.0)
plt.title("tile_{}" .format(tile_num), pad=30.0)
# plt.title("tile_{}" .format(i), y=1.08)
# plt.show()

# Choose colormap to denote different scatter points in different color.
cmap = np.arange(len(a))

# Plot predicted localizations from ith tile.
plt.subplot(1, 2, 2) 
# plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker=".", s=0.1)
# plt.scatter(loc[(loc[:,0]>0)&(loc[:,1]>0)][:,1], loc[(loc[:,0]>0)&(loc[:,1]>0)][:,0], c='r', marker="o", s=1)
# plt.scatter(a[(a[:,0]>0)&(a[:,1]>0)][:,1], a[(a[:,0]>0)&(a[:,1]>0)][:,0], c='r', marker=".", s=1)
#plt.scatter(a[(a[:,0]>0)&(a[:,1]>0)][:,1], a[(a[:,0]>0)&(a[:,1]>0)][:,0], c=cmap, marker=".", s=1)
# plt.scatter(a[:,1], a[:,0], c=cmap, marker=".", s=1)
plt.scatter(a[:,1], a[:,0], c='r', marker="o", s=1)

plt.xlim(0, 72)
plt.ylim(0, 72)
plt.gca().invert_yaxis()
plt.gca().xaxis.tick_top()
plt.gca().set_aspect('equal', adjustable='box')
# plt.ylabel("y")
# plt.xlabel("x")
# plt.legend(labels=['prediction'])
# plt.title("pred_tile_{}" .format(tile_num), pad=30.0)
plt.title("tile: {}" .format(tile_num), pad=30.0)
# plt.title("pred_tile_{}" .format(i), y=1.08)

# To stop axis labels from overlapping with neighboring plot.
plt.tight_layout()

# file_name = "pred_train_tile_{}.jpg" .format(i)
# plt.savefig(locs_pred_directory + file_name)
plt.show()    
        

