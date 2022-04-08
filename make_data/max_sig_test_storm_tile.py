"""
This is a test script to compute maximum pixel intensity signal for given stormtiff image tile.  

Swapnil 1/22
"""

import numpy as np
import math
import pandas as pd
from tifffile import tifffile

# Are you analyzing training tiles or test tiles?
training = True

# Set path to data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

#storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"        

# Get stormtiff directory.
stormtiffs_directory = storm_exp_directory + "stormtiffs\\"

# tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv_8k.csv"
# tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_8k.csv"
tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_8k.csv"

# Specify the tile-size of storm image section for training data.
tile_size = 100

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

# Get stormtiff tile number (tile number starts from 1).
tile_num = 4

# Initialize tile count.
tile_count = 1

# Iterate over individual image numbers in dataframe.
for img_num in tiles_df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = tiles_df[tiles_df["Num_image"]==img_num]
    
    # print("Number of tiles in image {} are {}" .format(img_num, len(img_df)))
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:
        
        if (tile_count == tile_num):
        
            # Get stormtiff images for corresponding image number.
            if ((img_num-1)//10 == 0): stormtiff_file = stormtiffs_directory + storm_exp_name + "_00" + str(img_num-1) + "_mlist" + ".tiff"

            elif (((img_num-1)//10)//10 == 0): stormtiff_file = stormtiffs_directory + storm_exp_name + "_0" + str(img_num-1) + "_mlist" + ".tiff"

            elif ((((img_num-1)//10)//10)//10 == 0): stormtiff_file = stormtiffs_directory + storm_exp_name + "_" + str(img_num-1) + "_mlist" + ".tiff"

            stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
            
            # Get the tile coordinates.
            tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
            tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
            
            # Slicing the image array according to the tile position
            tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size, tile_start_pix_x:tile_start_pix_x+tile_size]

            break_status = True
            break
                    
        tile_count += 1

    if break_status: break
        
max_int = np.amax(tile)        

print("maximum intensity is {}" .format(max_int))    
    