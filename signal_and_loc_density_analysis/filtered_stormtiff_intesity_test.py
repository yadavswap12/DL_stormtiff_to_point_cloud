"""
Script to count pixels with non-zero intensity for a 
particular tile or image section from filtered stormtiff image.

Swapnil 2/22
"""

import math
import itertools
import pandas as pd
from tifffile import tifffile

# Set path to data files
expfolder = "analysis_path\\signal_and_loc_density_analysis\\"
data_directory = expfolder + "make_data\\"
# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "750storm"
storm_exp_directory = data_directory + storm_exp_name + "\\"

# Get stormtiff images for corresponding .hdf5 file
stormtiff_file = storm_exp_directory + "001_uint8.tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
stormtiff_image_size = stormtiff_image_array.shape

# Set tile size for square shaped tile.
tile_size = 82

# Set image number of of stormtiff image to be analyzed.
img_num = 1

# Get tile-list file.
tile_list_file = storm_exp_directory + "750_ROIs_to_csv_img1_trunc_2.csv"

# Make a dataframe from csv file containing list of tile coordinates.
tile_list_df = pd.read_csv(tile_list_file)

# Create a dataframe for particular "Num_img" entry.
img_df = tile_list_df[tile_list_df["Num_image"]==img_num]

idx = 1

# Get the tile coordinates.
tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])

print("image intensity is {}" .format(stormtiff_image_array[tile_start_pix_y,tile_start_pix_x]))
print(tile_start_pix_y, tile_start_pix_x)
# print("image intensity is {}" .format(stormtiff_image_array[3482,66]))

# Initialize intensity counter.
counter = 0

# Iterate over pixels from selected tile of stormtiff image.
for j, i in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size)):

    if (stormtiff_image_array[j,i] != 0): counter += 1

print("there are {} pixels with non-zero intensity." .format(counter))    

