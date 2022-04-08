"""
Script to get information about list of tiles. 
        
Swapnil 11/21
"""

import math
import pandas as pd 

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"
data_directory = expfolder + "make_data\\"
# training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"
storm_exp_name = "750storm"
# storm_exp_directory = training_data_directory + storm_exp_name + "\\"
storm_exp_directory = testing_data_directory + storm_exp_name + "\\"

tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_trunc_2.csv"

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Print first few rows in dataframe.
print(df.head())

print("total tiles are {}" .format(len(df)))

# Set the tile number for which the information is needed.
tile = 24

# Initialize tile count.
tile_count = 0

# Iterate over individual image numbers in dataframe.
for img_num in df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = df[df["Num_image"]==img_num]
    
    # print("Number of tiles in image {} are {}" .format(img_num, len(img_df)))
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:
    
        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

        tile_num = tile_count + 1
        
        if (tile_num == tile):
            
            print("For tile {}, img_num is {}, tile_start_y is {} and tile_start_x is {}." .format(tile, img_num, tile_start_pix_y, tile_start_pix_x))
        
        tile_count += 1

    
    
    
    
    
    
    
    