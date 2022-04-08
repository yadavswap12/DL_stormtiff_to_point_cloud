"""
Script to write sequences of overlapping tiles in consecutive image slices to file. The 
sequences of overlapping tiles are found from tiles-list provided.     

Swapnil 1/22
"""

import glob
import pickle
import os
import pandas as pd

from tile_sequencer_class_new import TileSequencer

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

exp_name = "experiment_1"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_no_empty_locs3d_" + exp_name + "_sorted.csv"

# Create new directory for tile sequence.
if not os.path.exists(experiment_directory + "tile_sequences\\"):
    os.mkdir(experiment_directory + "tile_sequences\\")
    
tile_sequences_directory = experiment_directory + "tile_sequences\\"

# Remove previously present files. 
files = glob.glob(tile_sequences_directory + "*")
for f in files:
    os.remove(f)

# Set tile size for square shaped tile.
tile_size = 72

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Get total number of tiles.
tiles_num = len(df)

# Print first few rows from dataframe.
print(df.head())

# Initialize sequence counter.
seq_count = 1

while (len(df) != 0):

    # Get the tile coordinates, image number and tile number from the top row of dataframe.
    tile_start_pix_y = df.iloc[0]["y(row)"]
    tile_start_pix_x = df.iloc[0]["x(column)"]
    image_num = df.iloc[0]["z(Num_image)"]
    tile_num = int(df.iloc[0]["Tile_ID"])        

    (tile_num_seq, df) = TileSequencer().tileSequence(df, tile_start_pix_y, tile_start_pix_x, tile_size, image_num, tile_num)
    
    # Create a sequence filename.
    seq_file_name = tile_sequences_directory + "sequence_" + str(seq_count) + ".data"

    # Writing sequences to files.
    with open(seq_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(tile_num_seq, filehandle)
    
    if (seq_count%100 == 0):
        print("{}th tile sequence is created." .format(seq_count))    

    seq_count += 1

    










