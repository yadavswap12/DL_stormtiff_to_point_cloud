"""
Script to get tile-list parameters and tile-number for empty tile(zero intensity everywhere).

Swapnil 2/22
"""

import numpy as np
import math
import pandas as pd
from tifffile import tifffile 

# Are you analyzing training data or testing data?
training = True

# Set path to data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "750storm"

# Specify ROI extension string for data directory.
# roi = "_ROIs_mixed_first_70"    
# roi = "_ROIs_mixed_first_100"
roi = "_ROIs_14k" 

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"   

list_filename = storm_exp_directory + "tile_list\\" + "empty_tile_list_750_ROIs_to_csv.csv"

stormtiff_directory = storm_exp_directory + "stormtiffs_uint8\\"         

tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_14k.csv"    

# Specify ROI extension string for data directory.
# roi = "_ROIs_mixed_first_70"    
# roi = "_ROIs_mixed_first_100"
roi = "_ROIs_14k"            

# Set tile size for square shaped tile.
tile_size = 86

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

    if ((img_num)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(img_num) + ".tiff"
    
    elif (((img_num)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(img_num) + ".tiff"
    
    elif ((((img_num)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(img_num) + ".tiff"         
    
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
            tile[: , :stormtiff_image_array.shape[1]-tile_start_pix_x] = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size , tile_start_pix_x:]

        elif cond3:

            tile = np.zeros((tile_size,tile_size))
            tile[:stormtiff_image_array.shape[0]-tile_start_pix_y, :stormtiff_image_array.shape[1]-tile_start_pix_x] = stormtiff_image_array[tile_start_pix_y: , tile_start_pix_x:]

        else:     
        
            tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size, tile_start_pix_x:tile_start_pix_x+tile_size]
        
        # If the tile is empty.
        if np.all((tile == 0)):
            print("empty tile found.")
            # Write tile_start_pix_y, tile_start_pix_x and image number to a .csv file.
            with open(list_filename,"a") as f_out:
                f_out.write("{},{},{},{}\n" .format(tile_start_pix_y, tile_start_pix_x, img_num, tile_count+1))

        div = tiles_num//10
        # div = 1000
        
        if ((tile_count+1)%div==0):
            print("{}th tile is analyzed\n" .format(tile_count+1))                
        
        tile_count += 1







   