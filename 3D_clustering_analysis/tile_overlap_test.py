"""
Script to check the tile-list for overlapping tiles with same image number.
Specifically it gives list of all overlapping tiles for a given tile. 

Swapnil 2/22
"""

import math
import pandas as pd

# Are you analyzing filtered images?
filtered = True

# Do you want to sort the tile-list according to image number?
sorted =  True

# Set path to data files
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"         

if filtered:
    if sorted: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_v2_to_csv_no_empty_tiles_filtered_sorted.csv"
    else: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_v2_to_csv_no_empty_tiles_filtered.csv"

else: 
    if sorted: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_v2_to_csv_no_empty_tiles_sorted.csv"
    else: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_v2_to_csv_no_empty_tiles.csv" 

# Which channel do you want to analyze? Set experiment name.
# channel = "561storm"
# channel = "647storm"    
channel = "750storm"
base = str(channel)

# Set tile size for square shaped tile.
tile_size = 100

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file_updt)

# Initialize overlap counter.
ovrlp_count = 0

# # Get total number of tiles.
# tiles_num = len(df)

# # Initialize tile count.
# tile_count = 0

# # Part 1: Find and print overlapping sequence for particular tile.

# # Get the image number for the tiles to be analyzed.
# img_num = 1

# # Create a dataframe for particular "Num_img" entry.
# img_df = df[df["Num_image"]==img_num]

# # Get the index of the tile to be checked for overlap.
# tile_idx = img_df.index[1]

# # Get the tile coordinates and tile-number of the tile to be checked for overlap.
# tile_start_pix_y = math.floor(img_df.loc[tile_idx, 'y(row)'])
# tile_start_pix_x = math.floor(img_df.loc[tile_idx, 'x(column)'])
# tile_num = img_df.loc[tile_idx, 'tile_num']

# print("tile number is {}" .format(tile_num))

# # Initialize overlapping tile-number sequence list with first tile number.
# tile_num_seq = [tile_num] 
    
# # Iterate over all rows in dataframe for given image number.
# for idx in img_df.index:

    # # Get the coordinates for other possibly overlapping tiles with givebn image number.
    # ovrlp_tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
    # ovrlp_tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
    # ovrlp_tile_num = img_df.loc[idx, 'tile_num']

    # # Create tile overlap conditions. 
    # cond1 = ((tile_start_pix_y+tile_size>ovrlp_tile_start_pix_y) & (tile_start_pix_y<ovrlp_tile_start_pix_y)) & ((tile_start_pix_x+tile_size>ovrlp_tile_start_pix_x) & (tile_start_pix_x<ovrlp_tile_start_pix_x))
    # cond2 = ((tile_start_pix_y+tile_size>ovrlp_tile_start_pix_y) & (tile_start_pix_y<ovrlp_tile_start_pix_y)) & ((tile_start_pix_x-tile_size<ovrlp_tile_start_pix_x) & (tile_start_pix_x>ovrlp_tile_start_pix_x))
    # cond3 = ((tile_start_pix_y-tile_size<ovrlp_tile_start_pix_y) & (tile_start_pix_y>ovrlp_tile_start_pix_y)) & ((tile_start_pix_x-tile_size<ovrlp_tile_start_pix_x) & (tile_start_pix_x>ovrlp_tile_start_pix_x))
    # cond4 = ((tile_start_pix_y-tile_size<ovrlp_tile_start_pix_y) & (tile_start_pix_y>ovrlp_tile_start_pix_y)) & ((tile_start_pix_x+tile_size>ovrlp_tile_start_pix_x) & (tile_start_pix_x<ovrlp_tile_start_pix_x))                                    
    
    # if (cond1 | cond2 | cond3 | cond4):
        # tile_num_seq.append(ovrlp_tile_num)
        
# print(tile_num_seq)

# Part 2: Find and print overlapping sequences for all the tiles in tile-list.

# Iterate over individual image numbers.
for img_num in df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = df[df["Num_image"]==img_num]
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:    
    
        # Get the tile coordinates and tile-number of the tile to be checked for overlap.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
        tile_num = img_df.loc[idx, 'tile_num']
        
        # Initialize overlap sequence length.
        seq_len = 1
        
        # Initialize overlapping tile-number sequence list with first tile number.
        tile_num_seq = [tile_num]         
        
        for idx_nxt in img_df[img_df.index > idx].index:

            # Get the coordinates for other possibly overlapping tiles with givebn image number.
            ovrlp_tile_start_pix_y = math.floor(img_df.loc[idx_nxt, 'y(row)'])
            ovrlp_tile_start_pix_x = math.floor(img_df.loc[idx_nxt, 'x(column)'])
            ovrlp_tile_num = img_df.loc[idx_nxt, 'tile_num']

            # Create tile overlap conditions. 
            cond1 = ((tile_start_pix_y+tile_size>ovrlp_tile_start_pix_y) & (tile_start_pix_y<ovrlp_tile_start_pix_y)) & ((tile_start_pix_x+tile_size>ovrlp_tile_start_pix_x) & (tile_start_pix_x<ovrlp_tile_start_pix_x))
            cond2 = ((tile_start_pix_y+tile_size>ovrlp_tile_start_pix_y) & (tile_start_pix_y<ovrlp_tile_start_pix_y)) & ((tile_start_pix_x-tile_size<ovrlp_tile_start_pix_x) & (tile_start_pix_x>ovrlp_tile_start_pix_x))
            cond3 = ((tile_start_pix_y-tile_size<ovrlp_tile_start_pix_y) & (tile_start_pix_y>ovrlp_tile_start_pix_y)) & ((tile_start_pix_x-tile_size<ovrlp_tile_start_pix_x) & (tile_start_pix_x>ovrlp_tile_start_pix_x))
            cond4 = ((tile_start_pix_y-tile_size<ovrlp_tile_start_pix_y) & (tile_start_pix_y>ovrlp_tile_start_pix_y)) & ((tile_start_pix_x+tile_size>ovrlp_tile_start_pix_x) & (tile_start_pix_x<ovrlp_tile_start_pix_x))                                    
            
            if (cond1 | cond2 | cond3 | cond4):
                seq_len += 1
                ovrlp_count += 1 
                tile_num_seq.append(ovrlp_tile_num)
                print(tile_num_seq)
                
print("There are {} number of overlaps in tiles" .format(ovrlp_count))                


    
