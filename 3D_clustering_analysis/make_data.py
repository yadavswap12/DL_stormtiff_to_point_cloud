"""
Main function to collect input data for the previously trained model.

Swapnil 1/22
"""

import pandas as pd

from model_input_output import modelInputOutput
# from locs_from_tiles import locsFromTiles
from locs_per_tile_2 import locsPerTile2
from locs_per_tile_2_tmp import locsPerTile2Tmp

if __name__ == "__main__":

    # Do you want to sort the tile-list according to image number?
    sorted =  True

    # Set path to data files
    expfolder = "analysis_path\\experiment_name\\"
    
    # storm_exp_name = "561storm"
    storm_exp_name = "647storm"    
    # storm_exp_name = "750storm"
    
    storm_exp_directory = expfolder + storm_exp_name + "\\"         

    if sorted: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_sorted.csv"
    else: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles.csv" 

    # if sorted: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_no_empty_tiles_sorted.csv"
    # else: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_no_empty_tiles.csv" 

    # Set scaling factor between raw image and stormtiff image.
    storm_image_scale = int(10)

    # Which channel do you want to analyze? Set experiment name.
    # channel = "561storm"
    channel = "647storm"    
    # channel = "750storm"
    base = str(channel)

    # Set tile size for square shaped tile.
    tile_size = 72    
    
    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file_updt)
    
    # Create input and output files from tiles.
    total_tiles, total_loc_files = modelInputOutput(storm_exp_directory, storm_exp_name, channel, tile_size, storm_image_scale, df, locsPerTile2, locsPerTile2Tmp, sorted)

    # print("total number of training tiles created are {}\n" .format(total_tiles))
    print("total number of testing tiles created are {}\n" .format(total_tiles))
    
    
