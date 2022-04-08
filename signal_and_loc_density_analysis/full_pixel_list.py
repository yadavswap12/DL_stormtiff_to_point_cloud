"""
This script creates a single pixel list of all the pixels from the clusters (connected components) in 
given set of image tiles.  

Swapnil 2/22
"""

import glob
import pandas as pd

# Are you analyzing uint8 data?
uint8 = True
# uint8 = False      

# Are you collecting training data?
training = True
# training = False    

# Set path to data files.
expfolder = "analysis_path\\signal_and_loc_density_analysis\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

storm_exp_name = "647storm"    

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"        

# Get path to the cluster pixel_list directory.
clust_pix_list_directory = storm_exp_directory + "cluster_pixel_lists\\"

# Initialize dataframe list.
df_list = []

# Get all the cluster pixel-list files. 
files = glob.glob(clust_pix_list_directory + "*")

for file in files:
    clstr_pix_list_df = pd.read_csv(file)
    
    df_list.append(clstr_pix_list_df)    

# Create a concatenated dataframe from dataframe list. 
df = pd.concat(df_list, ignore_index=True)

# Get the output file for the concatenated dataframe and save to a csv file.
df_out_file = clust_pix_list_directory + "pix_list_full.csv"
df.to_csv(df_out_file)        
    
