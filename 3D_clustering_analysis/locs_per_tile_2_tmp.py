"""
Function to create list of number of localization estimates (without nn average) from stormtiff image tile. 
        
Swapnil 1/22
"""
import numpy as np
import pickle
import itertools
import multiprocessing
import pandas as pd
import math

def locsPerTile2Tmp(tile_start_pix_y, tile_start_pix_x, tile_size, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name, locs_est_storm_tile_lin_fit, locs_est_storm_tile_quad_fit):
    
    # Process details.
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))    
    
    # Intitialize localizations per tile in raw image coordinates and tile coordinates. 
    num_locs_est_tile_lin_fit = []        
    num_locs_est_tile_quad_fit = []            
    
    # Convert list of localizations from dictionary to array of localizations.
    locs_est_storm_tile_lin_fit = np.array(locs_est_storm_tile_lin_fit)
    locs_est_storm_tile_quad_fit = np.array(locs_est_storm_tile_quad_fit)        
    
    # Make a dataframe of array of localizations.
    est_lin_fit_df = pd.DataFrame(locs_est_storm_tile_lin_fit, columns=["y","x"])
    est_quad_fit_df = pd.DataFrame(locs_est_storm_tile_quad_fit, columns=["y","x"])        
    
    # Add new column to dataframe with floor values of "y" column. This new column denotes y-coordinate of pixels within which localization lies.
    est_lin_fit_df["y_floor"] = est_lin_fit_df["y"].apply(math.floor)
    est_lin_fit_df["x_floor"] = est_lin_fit_df["x"].apply(math.floor)

    est_quad_fit_df["y_floor"] = est_quad_fit_df["y"].apply(math.floor)
    est_quad_fit_df["x_floor"] = est_quad_fit_df["x"].apply(math.floor)     

    # Finding the number of localizations in every pixel of the tile.
    for j, i in itertools.product(range(tile_start_pix_y, tile_start_pix_y+tile_size), range(tile_start_pix_x, tile_start_pix_x+tile_size)):
    
        num_locs_est_tile_lin_fit.append(len(est_lin_fit_df[(est_lin_fit_df["y_floor"] == j-tile_start_pix_y) & (est_lin_fit_df["x_floor"] == i-tile_start_pix_x)]))    
        num_locs_est_tile_quad_fit.append(len(est_quad_fit_df[(est_quad_fit_df["y_floor"] == j-tile_start_pix_y) & (est_quad_fit_df["x_floor"] == i-tile_start_pix_x)]))            

    # Convert list to numpy array.
    num_locs_est_tile_lin_fit = np.array(num_locs_est_tile_lin_fit)
    num_locs_est_tile_quad_fit = np.array(num_locs_est_tile_quad_fit)    
                   
    # Writting locs per tile to files. 
    with open(num_locs_est_tile_lin_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(num_locs_est_tile_lin_fit, filehandle)

    # Writting locs per tile to files. 
    with open(num_locs_est_tile_quad_fit_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(num_locs_est_tile_quad_fit, filehandle)        
