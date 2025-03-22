"""
This script converts the localizations stored in localization dictionary to 2d localizations for given tile 
in both pixel and cartesian coordinates (with respect to stormtiff image frame). The x and y coordinates are the same values as in the dictionary and 
the z coordinate is same as the image number of given image slice.   

Swapnil 08/24
"""

import numpy as np
import glob
import math
import pickle
import itertools
import os
import matplotlib.pyplot as plt
import random
import pandas as pd

# Are you collecting training data or test data?
# training = True
training = False

# Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

accuracy_directory = expfolder + "Clustering_accuracy\\"

exp_name = "experiment_12"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'

# storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"

# tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv_8k.csv"
# tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_8k.csv"
# tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_8k.csv"

tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv.csv"

# Give pixel size in nano-meters.
nm_per_pixel_x = 15.5
nm_per_pixel_y = 15.5
nm_per_pixel_z = 70.0

# Specify the tile-size of storm image section for training data.
tile_size = 72

# Set percentage of total data used for training.
training_data_pctg = 90

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles.
tiles_num = len(df)

# Get number of tiles for training out of all tiles.
tiles_train_num = math.ceil(tiles_num*(training_data_pctg/100))    

# Create training and testing dataframes.
# Splitting dataframe by row index.
if training: tiles_df = df.iloc[:tiles_train_num,:]
else: tiles_df = df.iloc[tiles_train_num+1:,:]

# Get the localizations dictionary directory.
locs_dict_directory = storm_exp_directory + "locs_dictionary_tilesize_72_ROIs\\"

data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_ROIs\\"

# # Create new directory for 3d localizations per tile.
# if not os.path.exists(storm_exp_directory + data_directory_str):
    # os.mkdir(storm_exp_directory + data_directory_str)

if not os.path.exists(accuracy_experiment_directory + "locs2d_mol_list\\"):
    os.mkdir(accuracy_experiment_directory + "locs2d_mol_list\\")
    
locs_2d_directory = accuracy_experiment_directory + "locs2d_mol_list\\"

# Remove previously present files. 
files = glob.glob(locs_2d_directory + "*")
for f in files:
    os.remove(f)   

# Initialize tile count.
tile_count = 0 

# Initialize list of tiles with zero localizations.
tile_list_no_locs2d = []

tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_" + exp_name + ".data"    

# Iterate over individual image numbers.
for img_num in tiles_df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = tiles_df[tiles_df["Num_image"]==img_num]
    
    # get the dictionary file name.
    locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"

    # Read from the file and save it to a dictionary.    
    with open(locs_dict_file_name, 'rb') as filehandle:
        locs_storm = pickle.load(filehandle)    
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

        # Get the tile ID.
        tile_id = img_df.loc[idx, 'Tile_ID']           
 
        # Form a key from tile coordinates for given tile.
        key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
        
        # From the localizations dictionary get list of localizations for given key.
        locs_storm_tile = locs_storm[key]
        
        # Print if locs_3d list is empty.
        if not locs_storm_tile:
            # print("locs_rd list for tile {} is empty." .format(tile_id))
            tile_list_no_locs2d.append(tile_id)        

        # Convert list of localizations from dictionary to array of localizations.
        locs_storm_tile = np.array(locs_storm_tile)

        # Add third column to array of localizations for z coordinate as random value  between image_number and image_number - 1.
        # Choose number of floating points for random value.
        fl_pt = 3        
        
        
        # Make a copy of locs array for cartesian coordinates.
        locs_storm_tile_cart = locs_storm_tile.copy()
        
        # Convert x,y and z pixel coordinates to cartesian coordinates.
        locs_storm_tile_cart[:,0] = nm_per_pixel_y*locs_storm_tile[:,0]
        locs_storm_tile_cart[:,1] = nm_per_pixel_x*locs_storm_tile[:,1]

        # Get 3d localizations array in pixel and cartesian coordinates.
        locs2d_pixel_arr = locs_storm_tile
        locs2d_cart_arr = locs_storm_tile_cart        

        # locs3d_pred_file = locs_pred_directory + "tile_" + str(img_num) + str(tile_count+1) + ".data"
        locs2d_pixel_file = locs_2d_directory + "locs2d_molecule_list_pixel_tile_" + str(tile_id) + ".data"
        locs2d_cart_file = locs_2d_directory + "locs2d_molecule_list_cart_tile_" + str(tile_id) + ".data"                    
        
        # Writting the input and output lists to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
        with open(locs2d_pixel_file, 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(locs2d_pixel_arr, filehandle)
            
        with open(locs2d_cart_file, 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(locs2d_cart_arr, filehandle)
            
        if (tile_count%100 == 0):
            print("2d localizations for tile {} are created." .format(tile_id))            

        tile_count += 1
        
# Writting the input and output lists to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
with open(tile_list_no_locs2d_file, 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(tile_list_no_locs2d, filehandle)        
                
            
    

    



        
        

