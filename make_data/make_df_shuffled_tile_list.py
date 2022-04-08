"""
This script creates a (randomly) shuffled version of original tile-list.

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
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"        

# Which channel do you want to analyze? Set experiment name.
# channel = "561storm"
channel = "647storm"    
# channel = "750storm"

# Get the tile_list file.
if (channel == "561storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv.csv"

elif (channel == "647storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_from_10k.csv"

elif (channel == "750storm"): tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_full.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# shuffle the DataFrame rows.
# df = df.sample(frac = 1).reset_index(inplace=True, drop=True)
df_shuffled = df.sample(frac = 1).reset_index(drop=True)

# Get the output file for the concatenated dataframe.
# df_out_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_full_shuffled.csv" 
df_out_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_from_10k_shuffled.csv"
# df_out_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_from_10k_shuffled.csv"  
# df_out_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_full_shuffled.csv" 

# Write the concatenated dataframe to .csv file.
df_shuffled.to_csv(df_out_file)        
    
