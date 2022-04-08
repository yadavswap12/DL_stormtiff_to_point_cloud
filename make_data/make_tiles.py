"""
Function to create image tiles from a subsection of stromtiff image. 

Swapnil 10/21
"""

import os
import pickle
import glob
from tifffile import tifffile
import math

def makeTiles(storm_exp_directory, storm_exp_name, tile_size, tiles_df, tile_input, uint8, roi):
    
    if uint8: 
    
        data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_uint8" + roi + "\\"
        stormtiff_directory = storm_exp_directory + "stormtiff_tiles_uint8\\"

    else: 
    
        data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + roi + "\\"
        stormtiff_directory = storm_exp_directory + "stormtiff_tiles\\"  

    # Create new directory for tiles of stormtiff file.
    if not os.path.exists(storm_exp_directory + data_directory_str):
        os.mkdir(storm_exp_directory + data_directory_str)
        # os.mkdir(storm_exp_directory + data_directory_str + "locs\\")           

    if not os.path.exists(storm_exp_directory + data_directory_str + "tiles\\"):
        os.mkdir(storm_exp_directory + data_directory_str + "tiles\\")
        # os.mkdir(storm_exp_directory + data_directory_str + "locs\\")        

    tiles_directory = storm_exp_directory + data_directory_str + "tiles\\"
    # locs_directory = storm_exp_directory + data_directory_str + "locs\\"
    
    # Remove previously present files. 
    files = glob.glob(tiles_directory + "*")
    for f in files:
        os.remove(f)         
    
    # Initialize tile count.
    tile_count = 0    
    
    # Iterate over individual image numbers.
    for img_num in tiles_df["Num_image"].unique():
    
        # Create a dataframe for particular "Num_img" entry.
        img_df = tiles_df[tiles_df["Num_image"]==img_num]
        
        # stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
        
        # Iterate over all rows in dataframe for given image number.
        for idx in img_df.index:
        
            # Get the tile coordinates and tile ID.
            tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])
            
            # # For pre-aligned and filtered 750 channel stormtiff images. 
            # if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "00000" + str(tile_id) + ".tif"
            
            # elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
            
            # elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
            
            # elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
            
            # elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"

            # elif (((((((tile_id)//10)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"
            
            # For pre-aligned and filtered 647 channel stormtiff images. 
            if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
            
            elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
            
            elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
            
            elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"
            
            elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"        
            
            tile = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray

            tile_file = tiles_directory + "tile_" + str(tile_id) + ".data"                                          
            
            # Writting the input and output lists to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
            with open(tile_file, 'wb') as filehandle:
                # store the data as binary data stream
                pickle.dump(tile, filehandle)
            
            # div = tiles_num//10
            # div = 1            
            div = 1000
            
            if ((tile_count+1)%div==0):
                print("{}th tile is created\n" .format(tile_count+1))
                
            tile_count += 1

    total_tiles = tile_count

    return total_tiles    
    