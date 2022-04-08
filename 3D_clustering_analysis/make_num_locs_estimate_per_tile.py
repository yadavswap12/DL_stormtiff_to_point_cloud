"""
Script to make estimated number of localizations file for each stormtiff tile.
        
Swapnil 3/22
"""
import numpy as np
import pickle
import itertools
import math
import os
import pandas as pd
from tifffile import tifffile
import random
from scipy.stats import truncnorm 

# Do you want to sort the tile-list according to image number?
sorted =  True

# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"
storm_exp_directory = expfolder + storm_exp_name + "\\"

# Get tile-list file.
tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_no_empty_tiles_sorted.csv"    

# Set tile size for square shaped tile.
tile_size = 86 

# Get stormtiff directory.
stormtiff_directory = storm_exp_directory + "stormtiff_tiles\\"

if sorted: 
    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_sorted\\"
else:
    data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "\\"              
    
# Create new directory for num_locs from tiles.
if not os.path.exists(storm_exp_directory + data_directory_str):
    os.mkdir(storm_exp_directory + data_directory_str)

if not os.path.exists(storm_exp_directory + data_directory_str + "num_locs_estimate\\"):
    os.mkdir(storm_exp_directory + data_directory_str + "num_locs_estimate\\")
    
num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"      

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

print("total tiles are {}" .format(len(df)))   

# List of coefficients from highest to lowest degree for polynomial fit (f(x) = coef[0]*x**n + coef[1]*x**(n-1) + ... + coef[n])
# The list is found from sig_intesity_vs_loc_density.py
# # Coefficients for 561 channel and uint8 datatype.
# coef1 = [0.045472407327056284, -0.1318786631018805]
# coef2 = [0.00037214381469885684, -0.031098925558799454, 0.07589720917078603]

# # Coefficients for 647 channel and uint8 datatype.
# coef1 = [0.020566544735555848, -0.0002843564651092773]
# coef2 = [3.9396307058006944e-05, 0.013017080650862363, 0.010744420497577395]

# Coefficients for 750 channel and uint8 datatype.
coef1 = [0.048444465641161706, -0.08657427333332146]
coef2 = [0.00011772590610813693, 0.03178708473681607, 0.012119446304195071]   

# Iterate over all rows in dataframe for given image number.
for idx in df.index:

    # Get the tile coordinates.
    tile_start_pix_y = math.floor(df.loc[idx, 'y(row)'])
    tile_start_pix_x = math.floor(df.loc[idx, 'x(column)'])
    
    # Get the tile ID.
    tile_id = df.loc[idx, 'Tile_ID']

    # Initialize a list for localizations in given tile.
    locs_est_storm_lin_fit = []
    locs_est_storm_quad_fit = []    

    # For post-aligned and filtered stormtiff images. 
    if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "00000" + str(tile_id) + ".tif"
    
    elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
    
    elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
    
    elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
    
    elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"

    elif (((((((tile_id)//10)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"
    
    tile = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray

    # Create output files to store the number of localizations per pixel.
    # Note -  The localization estimates are given only in tile frame coordinates.
    num_locs_est_tile_lin_fit_file_name = num_locs_est_directory + "storm_num_locs_est_lin_fit_tile_" + str(tile_id) + ".data"            
    num_locs_est_tile_quad_fit_file_name = num_locs_est_directory + "storm_num_locs_est_quad_fit_tile_" + str(tile_id) + ".data"          
    
    # Iterate over pixels from selected tile.
    for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):
        
        # Begin nn-average computations.
        # Initialize signal intensity and nn-counter.
        sig = 0
        nn_counter = 0
        
        # Iterating over 8 nearest neighbors.
        for m, n in itertools.product(range(j-1, j+2), range(i-1, i+2)):

        # # Iterating over 24 nearest neighbors.
        # for m, n in itertools.product(range(j-2, j+3), range(i-2, i+3)):    

            if ((m, n) in itertools.product(range(0, tile_size), range(0, tile_size))):
                
                sig += tile[m,n]
                nn_counter += 1
        
        sig_nn_avg = (sig/nn_counter)
        
        # Define truncated normal distribution function.
        def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
            return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)            
        
        # Get number of localizations from fit to signal intensity.
        if (sig_nn_avg < 20.0):
            
            # # With truncated normal distribution function calculate spread following truncated normal distribution. The 3-sigma of gaussian = range. 
            # spread = round(get_truncated_normal(mean=0, sd=math.ceil(0.5*sig_nn_avg*(3.0/5))/3, low=math.floor(-0.5*sig_nn_avg*(3.0/5)), upp=math.ceil(0.5*sig_nn_avg*(3.0/5))).rvs())    
            
            # Get the random spread around the fit value.
            # The factor of (3.0/5) is determined from plots for the fits.
            # spread = random.randint(math.floor(-0.5*sig_nn_avg*(3.0/5)), math.ceil(0.5*sig_nn_avg*(3.0/5)))
            
            # Or set the spread to zero. 
            spread = 0
            
            # Assign zero signal intensity of zero localizations else use fit to estimate localizations.
            if (sig_nn_avg == 0):
                num_loc_nn_avg_lin_fit = 0
                num_loc_nn_avg_quad_fit = 0

            else: 
                num_loc_nn_avg_lin_fit = np.poly1d(coef1)(sig_nn_avg) + spread
                num_loc_nn_avg_quad_fit = np.poly1d(coef2)(sig_nn_avg) + spread                
            
        else:
        
            # # With truncated normal distribution function calculate spread following truncated normal distribution. The 3-sigma of gaussian = range. 
            # spread = round(get_truncated_normal(mean=0, sd=math.ceil(0.5*5)/3, low=math.floor(-0.5*5), upp=math.ceil(0.5*5)).rvs())                

            # Get the random spread around the fit value.
            # Here factor of 5 is for width of the random spread which remains constant for signal intensities greater than sig_nn_avg = 20.
            # spread = random.randint(math.floor(-0.5*5), math.ceil(0.5*5))
           
            # Or set the spread to zero.             
            spread = 0

            # Assign zero signal intensity of zero localizations else use fit to estimate localizations.
            if (sig_nn_avg == 0):
                num_loc_nn_avg_lin_fit = 0
                num_loc_nn_avg_quad_fit = 0

            else: 
                num_loc_nn_avg_lin_fit = np.poly1d(coef1)(sig_nn_avg) + spread
                num_loc_nn_avg_quad_fit = np.poly1d(coef2)(sig_nn_avg) + spread     
            
        # Add list of estimated number of localizations to center of the tile pixel.
        # If estimated number of localizations are a positive integer.
        if math.ceil(num_loc_nn_avg_lin_fit) > 0:
            locs_est_pix_lin = math.ceil(num_loc_nn_avg_lin_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
        # Else create list of array with default value -1 for coordinates.    
        else:
            locs_est_pix_lin = [np.array([-1, -1])]
        
        # If estimated number of localizations are a positive integer.            
        if math.ceil(num_loc_nn_avg_quad_fit) > 0:
            locs_est_pix_quad = math.ceil(num_loc_nn_avg_quad_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
        # Else create list of array with default value -1 for coordinates.    
        else:
            locs_est_pix_quad = [np.array([-1, -1])]
        
        # Add the list to final dictionary of lists.
        locs_est_storm_lin_fit.extend(locs_est_pix_lin)
        locs_est_storm_quad_fit.extend(locs_est_pix_quad)
        
    # Convert list of localizations to array of localizations.
    locs_est_storm_lin_fit = np.array(locs_est_storm_lin_fit)
    locs_est_storm_quad_fit = np.array(locs_est_storm_quad_fit)               
        
    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(num_locs_est_tile_lin_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_lin_fit, filehandle) 

    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(num_locs_est_tile_quad_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_quad_fit, filehandle)

    if (idx % 100 == 0):
        print("num_locs_estimate file for {}th tile is created" .format(idx))
                
        
        
        
        
        
        
        
        
        
        

 