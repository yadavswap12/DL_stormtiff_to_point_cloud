"""
Script to get tile-list parameters and tile-number for empty tile(zero intensity everywhere) among tiles created from tile-list.

Swapnil 2/22
"""

import numpy as np
import math
import pandas as pd
from tifffile import tifffile 

# Set path to data files
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

list_filename = storm_exp_directory + "empty_tile_list_750_ROIs_v2_to_csv.csv"

stormtiff_directory = storm_exp_directory + "stormtiffs\\"         

tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_v2_to_csv.csv"

# Set tile size for square shaped tile.
tile_size = 100

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles
tiles_num = len(df)

# Initialize tile count.
tile_count = 0 

# Iterate over individual image numbers.
for img_num in df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = df[df["Num_image"]==img_num]

    # # For post-aligned and filtered stormtiff images.
    # if ((img_num)//10 == 0): stormtiff_file = stormtiff_directory + "Gs" + "00" + str(img_num) + ".tif"
    
    # elif (((img_num)//10)//10 == 0): stormtiff_file = stormtiff_directory + "Gs" + "0" + str(img_num) + ".tif"
    
    # elif ((((img_num)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "Gs" + str(img_num) + ".tif"
    
    # For post-aligned stormtiff images.        
    if ((img_num-1)//10 == 0): stormtiff_file = stormtiff_directory + storm_exp_name[:3] + "_" + storm_exp_name[3:] + "000" + str(img_num-1) + ".tif"
    
    elif (((img_num-1)//10)//10 == 0): stormtiff_file = stormtiff_directory + storm_exp_name[:3] + "_" + storm_exp_name[3:] + "00" + str(img_num-1) + ".tif"
    
    elif ((((img_num-1)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + storm_exp_name[:3] + "_" + storm_exp_name[3:] + "0" + str(img_num-1) + ".tif"

    elif (((((img_num-1)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + storm_exp_name[:3] + "_" + storm_exp_name[3:] + str(img_num-1) + ".tif"           
    
    stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:
    
        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

        # Slicing the image array according to the tile position.
        # If tile extends more than stormtiff image.
        cond1 = ((tile_start_pix_y+tile_size-1) > stormtiff_image_array.shape[0]-1) & ((tile_start_pix_x+tile_size-1) <= stormtiff_image_array.shape[1]-1)
        cond2 = ((tile_start_pix_y+tile_size-1) <= stormtiff_image_array.shape[0]-1) & ((tile_start_pix_x+tile_size-1) > stormtiff_image_array.shape[1]-1)
        cond3 = ((tile_start_pix_y+tile_size-1) > stormtiff_image_array.shape[0]-1) & ((tile_start_pix_x+tile_size-1) > stormtiff_image_array.shape[1]-1)         
        
        if cond1:
            
            tile = np.zeros((tile_size,tile_size))
            tile[:stormtiff_image_array.shape[0]-tile_start_pix_y, :] = stormtiff_image_array[tile_start_pix_y: , tile_start_pix_x:tile_start_pix_x+tile_size]
            
        elif cond2:

            tile = np.zeros((tile_size,tile_size))
            # print("tile broadcast shape is {}" .format(tile[: , :stormtiff_image_array.shape[1]-tile_start_pix_x].shape))
            # print("tile_start_pix_x is  {}" .format(tile_start_pix_x))
            # print("stormtiff_image_array.shape_1 is {}" .format(stormtiff_image_array.shape[1]))
            
            tile[: , :stormtiff_image_array.shape[1]-tile_start_pix_x] = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size , tile_start_pix_x:]

        elif cond3:

            tile = np.zeros((tile_size,tile_size))
            tile[:stormtiff_image_array.shape[0]-tile_start_pix_y, :stormtiff_image_array.shape[1]-tile_start_pix_x] = stormtiff_image_array[tile_start_pix_y: , tile_start_pix_x:]

        else:     
        
            tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size, tile_start_pix_x:tile_start_pix_x+tile_size]
        
        # If the tile is empty
        if np.all((tile == 0)):            
            # Write tile_start_pix_y, tile_start_pix_x and image number to a .csv file.
            with open(list_filename,"a") as f_out:
                f_out.write("{},{},{},{}\n" .format(tile_start_pix_y, tile_start_pix_x, img_num, tile_count+1))

        div = tiles_num//10
        # div = 1000
        
        if ((tile_count+1)%div==0):
            print("{}th tile is analyzed\n" .format(tile_count+1))                
        
        tile_count += 1







   