"""
Function to create list of localizations and localization estimates from stormtiff image tile to be used as 
output of a neural network.
        
Swapnil 12/21
"""

import os
import multiprocessing
import glob
import pickle
import pandas as pd
import math
from multiprocessing import Semaphore

def locsFromTiles(storm_exp_directory, storm_exp_name, tile_size, num_locs_output, num_locs_est_lin_fit_output, num_locs_est_quad_fit_output, max_processes, storm_image_scale, tiles_df, locsPerTile2, uint8, roi, clust_pix_list_full_file):
    
    
    if uint8: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_uint8" + roi + "\\"
    
    else: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + roi + "\\"
    
    molecule_lists_directory = storm_exp_directory + "molecule_lists\\"

    # Create new directory for num_locs from tiles.
    if not os.path.exists(storm_exp_directory + data_directory_str):
        os.mkdir(storm_exp_directory + data_directory_str)

    if not os.path.exists(storm_exp_directory + data_directory_str + "num_locs\\"):
        os.mkdir(storm_exp_directory + data_directory_str + "num_locs\\")

    num_locs_directory = storm_exp_directory + data_directory_str + "num_locs\\"
    
    if not os.path.exists(storm_exp_directory + data_directory_str + "num_locs_estimate\\"):
        os.mkdir(storm_exp_directory + data_directory_str + "num_locs_estimate\\")
        
    num_locs_est_directory = storm_exp_directory + data_directory_str + "num_locs_estimate\\"        
    
    # Remove previously present files. 
    files = glob.glob(num_locs_directory + "*")
    for f in files:
        os.remove(f)

    files = glob.glob(num_locs_est_directory + "*")
    for f in files:
        os.remove(f)            
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()

    # Initialize tile count.
    tile_count = 0
    
    # Make a dataframe from list of pixel coordinates.
    clstr_pix_list_full_df = pd.read_csv(clust_pix_list_full_file)
    
    # Coordinates in pixel list start from 1 so subtract 1 from all coordinates.
    clstr_pix_list_full_df[["x(row)","y(column)"]] = clstr_pix_list_full_df[["x(row)","y(column)"]].subtract(1)    

    # Create a new column for tuple of row and column coordinates.
    clstr_pix_list_full_df['row_col_tup'] = clstr_pix_list_full_df[['x(row)', 'y(column)']].apply(tuple, axis=1)

    # # Convert the tuple column to list.            
    # clstr_pix_list = clstr_pix_list_full_df['row_col_tup'].tolist()

    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)     
    
    # Iterate over individual image numbers.
    for img_num in tiles_df["Num_image"].unique():
    
        # Create a dataframe for particular "Num_img" entry.
        img_df = tiles_df[tiles_df["Num_image"]==img_num]
        
        # Get molecule list file for given image number.        
        if ((img_num-1)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_00" + str(img_num-1) + "_mlist" + ".hdf5"
        
        elif (((img_num-1)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_0" + str(img_num-1) + "_mlist" + ".hdf5"
        
        elif ((((img_num-1)//10)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_" + str(img_num-1) + "_mlist" + ".hdf5"

        # Get file for dictionary of localizations from all tiles in tiles_list for given image number.        
        locs_dict_directory = storm_exp_directory + "locs_dictionary_tilesize_" + str(tile_size) + "_ROIs\\"
        locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"        
        
        if uint8: locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary_uint8_tilesize_" + str(tile_size) + "_ROIs\\"
        
        else: locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary_tilesize_" + str(tile_size) + "_ROIs\\"            
        
        locs_est_dict_file_name_lin_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_lin_fit.data"
        locs_est_dict_file_name_quad_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_quad_fit.data"        
        
        # Read from the file and save it to a dictionary.
        print("Reading localizations dictionary from file ...\n")
        
        with open(locs_dict_file_name, 'rb') as filehandle:
            locs_storm = pickle.load(filehandle)

        with open(locs_est_dict_file_name_lin_fit, 'rb') as filehandle:
            locs_est_storm_lin_fit = pickle.load(filehandle)

        with open(locs_est_dict_file_name_quad_fit, 'rb') as filehandle:
            locs_est_storm_quad_fit = pickle.load(filehandle)                    
    
        # Iterate over all rows in dataframe for given image number.
        for idx in img_df.index:
        
            # Get the tile coordinates.
            tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
            tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
            tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])            
            
            # Form a key from tile coordinates for given tile.
            key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
            
            # From the localizations dictionary get list of localizations for given key.
            locs_storm_tile = locs_storm[key]
            locs_est_storm_tile_lin_fit = locs_est_storm_lin_fit[key]            
            locs_est_storm_tile_quad_fit = locs_est_storm_quad_fit[key]                     

            # Create output files to store the number of localizations per pixel.
            # Note -  The localization estimates are given only in tile frame coordinates.
            num_locs_file_name = num_locs_directory + "storm_num_locs_tile_" + str(tile_id) + ".data"            
            num_locs_est_tile_lin_fit_file_name = num_locs_est_directory + "storm_num_locs_est_lin_fit_tile_" + str(tile_id) + ".data"                       
            num_locs_est_tile_quad_fit_file_name = num_locs_est_directory + "storm_num_locs_est_quad_fit_tile_" + str(tile_id) + ".data"              
  
            # From dataframe of full pixel list, create a dataframe of pixel-list coordinates that lie within given tile.
            cond = clstr_pix_list_full_df["TileID"] == tile_id             

            clstr_pix_list_df = clstr_pix_list_full_df[cond]

            # Convert the tuple column to list.            
            clstr_pix_list = clstr_pix_list_df['row_col_tup'].tolist()
            
            # Once max_processes are running, block the main process.
            # This loop will continue only after one or more 
            # previously created processes complete.
            sema.acquire()            

            # Assign process for each tile.
            # process = multiprocessing.Process(target = locsPerTile, args=(h5_file, tile_start_pix_y, tile_start_pix_x, tile_size, max_locs_per_pixel, nm_per_pixel, storm_image_scale, locs_storm_file_name, locs_tile_file_name, locs_storm))
            process = multiprocessing.Process(target = locsPerTile2, args=(h5_file, tile_start_pix_y, tile_start_pix_x, tile_size, num_locs_file_name, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name, locs_storm_tile, locs_est_storm_tile_lin_fit, locs_est_storm_tile_quad_fit, clstr_pix_list, sema))                
            jobs.append(process)
            process.start()
            
            tile_count += 1
        
    # Block the execution of next lines in the main script.       
    for job in jobs:
        
        job.join()                       
            
    total_loc_files = tile_count        

    return total_loc_files            














         



        

