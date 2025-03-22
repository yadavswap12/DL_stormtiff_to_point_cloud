"""
This script converts the predicted number of localizations per pixel for a given tile to 2D 
localizations. 

Swapnil 08/24
"""

import numpy as np
import glob
import math
import pickle
import itertools
import os
import random
import pandas as pd

# Set path to data files.
# expfolder = "analysis_path\\experiment_name\\"
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

accuracy_directory = expfolder + "Clustering_accuracy\\"

exp_name = "experiment_12"
# exp_name = "experiment_9"
# exp_name = "experiment_10"
# exp_name = "experiment_11"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'


data_directory = expfolder + "experiments\\"


# storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"

storm_exp_directory = data_directory + "model_predictions\\"

tile_list_file = accuracy_experiment_directory + "647_ROIs_to_csv_no_empty_tiles_sorted.csv"
# tile_list_file = accuracy_experiment_directory + "750_ROIs_to_csv_no_empty_tiles_sorted.csv"


# Give pixel size in nano-meters.
nm_per_pixel_x = 15.5
nm_per_pixel_y = 15.5
nm_per_pixel_z = 70.0

# Specify the tile-size of storm image section for training data.
tile_size = 72
# tile_size = 86

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles.
tiles_num = len(df)

# Get localization prediction directory.
locs_pred_directory = storm_exp_directory + "experiment_12\\"
# locs_pred_directory = storm_exp_directory + "experiment_9\\"
# locs_pred_directory = storm_exp_directory + "experiment_10\\"
# locs_pred_directory = storm_exp_directory + "experiment_11\\"

# If not present create a new directory for 3d localizations. 
if not os.path.exists(accuracy_experiment_directory + "locs2d_predictions\\"):
    os.mkdir(accuracy_experiment_directory + "locs2d_predictions\\")
    
locs2d_pred_directory = accuracy_experiment_directory + "locs2d_predictions\\"

# Remove previously present files.
files = glob.glob(locs2d_pred_directory + "*")
for f in files:
    os.remove(f)

# Initialize tile counter.
tl_ct = 1

# Initialize list of tiles with zero localizations.
tile_list_no_locs2d = []

tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_pred_" + exp_name + ".data"    

# Iterate over individual image numbers.
for img_num in df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = df[df["Num_image"]==img_num]
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)']) 

        # Get the tile ID.
        tile_id = img_df.loc[idx, 'Tile_ID']           
 
        num_loc_pred_file = locs_pred_directory + "tile_pred_num_locs_tile_" + str(tile_id) + ".data"        
            
        with open(num_loc_pred_file, 'rb') as filehandle:
            num_locs_pred_tile = pickle.load(filehandle)

        # print("shape of num_locs_tile is {}" .format(num_locs_pred_tile.shape))
        
        # Initialize localizations lists.
        loc2d_pred_pixel_list = []
        loc2d_pred_cart_list = []        

        counter = 0      
            
        for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):

            # num_locs_pred_tile.append(len(df[(df["y_floor"] == j) & (df["x_floor"] == i)]))
            num_locs_pred = num_locs_pred_tile[0, counter]              

            # Assign the number of localizations to pixel center or randomly within pixel and make a list.  
            # num_loc_pred_pixel = round(num_locs_pred)*[np.array([j+1/2, i+1/2])]
            # Choose number of floating points for random floats.
            fl_pt = 3
                        
            # Assign all localizations a different random position within pixel.
            # Initialize localizations list for random positions within pixel. 
            num_loc_pred_pixel = []
            num_loc_pred_cart = []            
            
            # For every localization in given pixel.
            for num in range(round(num_locs_pred)):
                
                num_loc_pred_pixel.append(np.array([random.randint((j+tile_start_pix_y)*10**fl_pt, (j+tile_start_pix_y+1)*10**fl_pt)/10**fl_pt, random.randint((i+tile_start_pix_x)*10**fl_pt, (i+tile_start_pix_x+1)*10**fl_pt)/10**fl_pt]))
                num_loc_pred_cart.append(np.array([nm_per_pixel_y*random.randint((j+tile_start_pix_y)*10**fl_pt, (j+tile_start_pix_y+1)*10**fl_pt)/10**fl_pt, nm_per_pixel_x*random.randint((i+tile_start_pix_x)*10**fl_pt, (i+tile_start_pix_x+1)*10**fl_pt)/10**fl_pt]))            
            
            # Add the pixel list to final localizations list.
            loc2d_pred_pixel_list.extend(num_loc_pred_pixel)
            loc2d_pred_cart_list.extend(num_loc_pred_cart)
            
            counter += 1
            
        # Print if locs_3d list is empty.
        if not loc2d_pred_pixel_list:
            # print("locs_rd list for tile {} is empty." .format(tile_id))
            tile_list_no_locs2d.append(tile_id)

        # Convert list to numpy array.
        locs2d_pred_pixel_arr = np.array(loc2d_pred_pixel_list)
        locs2d_pred_cart_arr = np.array(loc2d_pred_cart_list)        

        # locs2d_pred_file = locs_pred_directory + "tile_" + str(img_num) + str(tile_count+1) + ".data"
        locs2d_pred_pixel_file = locs2d_pred_directory + "locs2d_pred_pixel_tile_" + str(tile_id) + ".data"
        locs2d_pred_cart_file = locs2d_pred_directory + "locs2d_pred_cart_tile_" + str(tile_id) + ".data"                    
        
        # Writting the input and output lists to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
        with open(locs2d_pred_pixel_file, 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(locs2d_pred_pixel_arr, filehandle)
            
        with open(locs2d_pred_cart_file, 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(locs2d_pred_cart_arr, filehandle)

        if (tl_ct%100 == 0):
            print("{}th tile is analyzed." .format(tl_ct))    

        tl_ct += 1

# Writting the input and output lists to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
with open(tile_list_no_locs2d_file, 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(tile_list_no_locs2d, filehandle)
        
            
    

    



        
        

