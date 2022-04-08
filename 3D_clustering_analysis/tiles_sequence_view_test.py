"""
Test script to view entries of tile sequence files. 

Swapnil 1/22
"""

import glob
import math
import pickle
import pandas as pd

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

exp_name = "experiment_1"

storm_exp_directory = expfolder + storm_exp_name + "\\"
experiment_directory = storm_exp_directory + "experiment1\\"

tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_no_empty_locs3d_" + exp_name + "_sorted.csv"

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles.
tiles_num = len(df)

# Get tile sequences directory.
# tile_sequences_directory = storm_exp_directory + "tile_sequences\\"
tile_sequences_directory = experiment_directory + "tile_sequences\\"

# Get number of files present in 3d localizations directory.
total_files = len(glob.glob(tile_sequences_directory + "*.data"))
        
# Give the tile sequence number.         
i = 289

# Get the tile sequence filename.
tile_seq_file_name = tile_sequences_directory + "sequence_" + str(i) + ".data"

# Read from the file. 
with open(tile_seq_file_name, 'rb') as filehandle:
    tile_seq = pickle.load(filehandle)

print("There are {} tiles in this sequence." .format(len(tile_seq)))    
                    
for tile in tile_seq:

    tile_counter = 1
        
    # Iterate over individual image numbers.
    for img_num in df["z(Num_image)"].unique():

        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["z(Num_image)"]==img_num]
        
        # Iterate over all rows in dataframe for given image number.
        for idx in img_df.index:
        
            # Get the tile ID.
            tile_id = img_df.loc[idx, 'Tile_ID']   

            # if (tile == tile_counter):
            if (tile == tile_id):            
            
                # Get the tile coordinates.
                tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
                tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

                print("for tile {}, coordinates are {} and image number is {}." .format(tile, (tile_start_pix_y, tile_start_pix_x), img_num))
                
            tile_counter += 1    
                

    










