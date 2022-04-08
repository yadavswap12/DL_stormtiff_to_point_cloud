"""
Test script to check if correct sequence of overlapping tiles in consecutive image slices is 
returned for a particular ROI from tiles-list provided.     

Swapnil 2/22
"""

import pandas as pd

from tile_sequencer_class_new import TileSequencer

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_no_empty_tiles_sorted.csv"

# Set tile size for square shaped tile.
tile_size = 86

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles.
tiles_num = len(df)

# Get the tile coordinates, image number and tile number for the ROI.
tile_start_pix_y = 79
tile_start_pix_x = 258
image_num = 2
tile_num = 59

(tile_num_seq, df) = TileSequencer().tileSequence(df, tile_start_pix_y, tile_start_pix_x, tile_size, image_num, tile_num)

print("The tile sequence is {}." .format(tile_num_seq))    
    










