"""
This is a script to plot number of localizations vs the signal intensity for a 
particular tile or image section. It also fits the plot with different functions and saves the fit parameters.

Swapnil 2/22
"""

import numpy as np
import math
import itertools
import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from tifffile import tifffile

# Set path to data files
expfolder = "analysis_path\\signal_and_loc_density_analysis\\"
data_directory = expfolder + "make_data\\"
# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "647storm_transform"
# storm_exp_name = "750storm"
storm_exp_directory = data_directory + storm_exp_name + "\\"

# create new directory for plots.
if not os.path.exists(storm_exp_directory + "plots \\"):
    os.mkdir(storm_exp_directory + "plots \\")

plots_directory = storm_exp_directory + "plots \\"  

# Get molecule-list file.
h5_file = storm_exp_directory + "647storm_000_mlist.hdf5" 

# Get stormtiff images for corresponding .hdf5 file
stormtiff_file = storm_exp_directory + "647storm_000_mlist.tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
print("stormtiff image {} is loaded for analysis\n" .format(os.path.basename(stormtiff_file)))
stormtiff_image_size = stormtiff_image_array.shape

# Set tile size for square shaped tile.
tile_size = 72

# Set image number of of stormtiff image to be analyzed.
img_num = 1

# Get tile-list file.
# tile_list_file = storm_exp_directory + "tile_list\\" + "561_ROIs_to_csv_8k.csv"
tile_list_file = storm_exp_directory + "647_ROIs_to_csv_img1_shuffled.csv"
# tile_list_file = storm_exp_directory + "750_ROIs_to_csv_img1_trunc.csv" 

# Make a dataframe from csv file containing list of tile coordinates.
tile_list_df = pd.read_csv(tile_list_file)

# Create a dataframe for particular "Num_img" entry.
img_df = tile_list_df[tile_list_df["Num_image"]==img_num]  

# Get localization dictionary from file.
locs_dict_directory = storm_exp_directory + "locs_dictionary\\"
locs_dict_file_name = locs_dict_directory + "locs_dict_img_{}_trunc.data" .format(img_num)                                    

# Read from the file and save it to a dictionary.        
with open(locs_dict_file_name, 'rb') as filehandle:
    locs_storm = pickle.load(filehandle)    
    
# Initialize signal intensity and number of localizations lists.
sig_int = []
num_loc = []

# Initialize nn-average signal intensity and number of localizations lists.
sig_int_nn_avg = []
num_loc_nn_avg = []

num_loc_nn_avg_lin_fit_list = []
num_loc_nn_avg_quad_fit_list = []

# Iterate over all rows in dataframe for given image number.
for idx in img_df.index:

    # Get the tile coordinates.
    tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
    tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
    tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])
    
    tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size,tile_start_pix_x:tile_start_pix_x+tile_size]

    print("Analyzing {}th tile." .format(tile_id))
    
    # Form a key from tile coordinates for given tile.
    key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
    
    # From the localizations dictionary get list of localizations for given key.
    locs_storm_tile = locs_storm[key]

    # Make a dataframe of array of localizations.
    df = pd.DataFrame(locs_storm_tile, columns=["y","x"])    
    
    # Add new column to dataframe with floor values of "y" column. This new column denotes y-coordinate of pixels within which localization lies.
    df["y_floor"] = df["y"].apply(math.floor)
    df["x_floor"] = df["x"].apply(math.floor)    
    
    # Iterate over pixels from selected tile of stormtiff image.
    for j, i in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size)):
    
        sig_int.append(stormtiff_image_array[j,i])
        
        num_loc.append(len(df[(df["y_floor"] == j) & (df["x_floor"] == i)]))

        # Begin nn-average computations.
        # Initialize signal intensity, number of localizations and nn-counter.
        sig = 0
        num = 0
        nn_counter = 0
        
        # If empty part of tile then pass the nn calculation.
        if (np. all((stormtiff_image_array[j-1:j+2,i-1:i+2] == 0))):
            nn_counter += 1        
        else:    
            # Iterating over 8 nearest neighbors.
            for m, n in itertools.product(range(j-1, j+2), range(i-1, i+2)):

            # # Iterating over 24 nearest neighbors.
            # for m, n in itertools.product(range(j-2, j+3), range(i-2, i+3)):    

                if ((m, n) in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size))):
                    
                    sig += stormtiff_image_array[m,n]
                    
                    num += len(df[(df["y_floor"] == m) & (df["x_floor"] == n)])                                      
                    
                    nn_counter += 1
        
        sig_int_nn_avg.append(sig/nn_counter)
        num_loc_nn_avg.append(num/nn_counter)
      
# Linear fit to nn-average data.
coef1 = np.polyfit(sig_int_nn_avg, num_loc_nn_avg, 1)
coef2 = np.polyfit(sig_int_nn_avg, num_loc_nn_avg, 2)
# coef1 = np.polyfit(sig_int_nn_avg, num_loc, 1)
# coef2 = np.polyfit(sig_int_nn_avg, num_loc, 2)

# plt.scatter(sig_int, num_loc, c='r', marker="o", s=1)
plt.plot(sig_int_nn_avg, num_loc_nn_avg, 'yo', sig_int_nn_avg, np.poly1d(coef1)(sig_int_nn_avg), '--k')
# plt.plot(sig_int_nn_avg, num_loc, 'yo', sig_int_nn_avg, np.poly1d(coef1)(sig_int_nn_avg), '--k')
plt.ylabel("8nn average of # of localizations")
plt.xlabel("8nn average of signal intensity")
plt.title("img1_ROIs_trunc_8nn_average", pad=30.0)
file1_name = "img1_ROIs_trunc_8nn_average_lin_uint8"
# file1_name = "img1_ROIs_trunc_8nn_average_lin"
plt.savefig(plots_directory + file1_name)
plt.show()

# plt.scatter(sig_int, num_loc, c='r', marker="o", s=1)
plt.plot(sig_int_nn_avg, num_loc_nn_avg, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
# plt.plot(sig_int_nn_avg, num_loc, 'yo', sig_int_nn_avg, np.poly1d(coef2)(sig_int_nn_avg), '--k')
plt.ylabel("8nn average of # of localizations")
plt.xlabel("8nn average of signal intensity")
plt.title("img1_ROIs_trunc_8nn_average", pad=30.0)
file2_name = "img1_ROIs_trunc_8nn_average_quad_uint8" 
# file2_name = "img1_ROIs_trunc_8nn_average_quad" 
file_name = "img1_ROIs_trunc_8nn_average_2"
plt.savefig(plots_directory + file2_name)
plt.show()

# Save coefficients of the fit to file.
with open(plots_directory + "linear_fit_8nn_average_uint8.csv","a") as f_out:
    f_out.write("With linear fit for tiles in {} we have, # of localizations = {}*signal intensity + {},  \n" .format(os.path.basename(tile_list_file), coef1[0], coef1[1]))
    f_out.write("With quadratic fit for for tiles in {} we have, # of localizations = {}*signal intensity**2 + {}*signal intensity + {},  \n" .format(os.path.basename(tile_list_file), coef2[0], coef2[1], coef2[2]))     
        

