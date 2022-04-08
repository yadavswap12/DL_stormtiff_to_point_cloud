"""
This script removes empty tiles(zero intensity everywhere) and returns updated tile-list. 
'Sorted' option if chosen, sorts the updated tile-list according to image number.

Swapnil 2/22
"""

import numpy as np
import pandas as pd
from tifffile import tifffile 

# Do you want to sort the tile-list according to image number?
sorted =  True

# Set path to data files
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

stormtiff_directory = storm_exp_directory + "stormtiff_tiles\\"

# Convert text to csv.
tile_list_file = pd.read_csv (storm_exp_directory + "tile_list\\" + "647_ROIs.txt")
tile_list_file.to_csv (storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv.csv", index=None)          

tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv.csv"

# Get the filename for updated tile-list.
if sorted: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_sorted.csv"
else: tile_list_file_updt = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles.csv" 

# Set tile size for square shaped tile.
tile_size = 72

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles
tiles_num = len(df)

# Initialize tile count.
tile_count = 0

# Iterate over all rows in the dataframe.
for idx in df.index:

    # Get the tile ID.
    tile_id = df.loc[idx, 'Tile_ID']

    # For post-aligned and filtered stormtiff images. 
    if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "00000" + str(tile_id) + ".tif"
    
    elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
    
    elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
    
    elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
    
    elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"

    elif (((((((tile_id)//10)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"
    
    tile = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray 

    # If the tile is empty
    if np.all((tile == 0)):            
        # Remove the row from the dataframe.
        df.drop(index=idx, inplace=True) 

    # Print analysis status.
    div = tiles_num//10
    # div = 1000
    
    if ((tile_id)%div==0):
        print("{}th tile is analyzed\n" .format(tile_id))         

# Save the updated dataframe to .csv file. 
if sorted:
    df_sorted = df.sort_values(["z(Num_image)"], ascending=True)
    df_sorted.to_csv(tile_list_file_updt, index=False)
else:
    df.to_csv(tile_list_file_updt, index=False)    








   