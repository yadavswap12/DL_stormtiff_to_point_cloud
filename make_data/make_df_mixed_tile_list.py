"""
This script creates a mixed version of original tile-list such that it takes only fixed number of 
first few tiles for every image number in original tile-list.  

Swapnil 2/22
"""

import pandas as pd

# Are you analyzing uint8 data?
uint8 = True

# Are you collecting training data or test data?
training = True

# Set path to training data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"        

# Which channel do you want to analyze? Set experiment name.
# channel = "561storm"
# channel = "647storm"    
channel = "750storm"

# Get number of tiles(ROIs) to be selected for every image number in tile-list.
num_tiles = 100 

# Get the original tile_list file.
if (channel == "561storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv.csv"

elif (channel == "647storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv.csv"

elif (channel == "750storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_full.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Initialize dataframe list.
df_mixed_tile_list = []

# Iterate over individual image numbers in dataframe.
for img_num in df["Num_image"].unique():

    # Create a dataframe for particular "Num_img" entry.
    img_df = df[df["Num_image"]==img_num]
    
    # Create a temporary dataframe with only first fixed number of rows from img_df.
    df_temp = img_df.iloc[:num_tiles]
    df_mixed_tile_list.append(df_temp)


# Create a concatenated dataframe form dataframe list. 
df_mixed = pd.concat(df_mixed_tile_list, ignore_index=True)

# Get the output file for the concatenated dataframe.
df_out_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_mixed_first_" + str(num_tiles) + ".csv" 

# Write the concatenated dataframe to .csv file.
df_mixed.to_csv(df_out_file)        
    
