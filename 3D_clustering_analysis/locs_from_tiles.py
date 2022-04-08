"""
Function to create list of localization estimates from stormtiff image tile.
        
Swapnil 1/22
"""

import os
import multiprocessing
import glob
import pickle
import math

def locsFromTiles(storm_exp_directory, storm_exp_name, tile_size, storm_image_scale, df, locsPerTile2, sorted):
        
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
    
    # Remove previously present files. 
    files = glob.glob(num_locs_est_directory + "*")
    for f in files:
        os.remove(f)            
    
    # Get total number of tiles
    tiles_num = len(df)
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()

    # Initialize tile count.
    tile_count = 0
    
    # Iterate over individual image numbers.
    for img_num in df["z(Num_image)"].unique():
    
        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["z(Num_image)"]==img_num]
        
        # Get locs estimate dictionary directory. 
        locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary\\"
        
        locs_est_dict_file_name_lin_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_lin_fit.data"
        locs_est_dict_file_name_quad_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_quad_fit.data"        
        
        # Read from the file and save it to a dictionary.
        print("Reading localizations dictionary from file ...\n")

        with open(locs_est_dict_file_name_lin_fit, 'rb') as filehandle:
            locs_est_storm_lin_fit = pickle.load(filehandle)

        with open(locs_est_dict_file_name_quad_fit, 'rb') as filehandle:
            locs_est_storm_quad_fit = pickle.load(filehandle)                    
    
        # Iterate over all rows in dataframe for given image number.
        for idx in img_df.index:
        
            # Get the tile coordinates.
            tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
            tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
            
            # Get the tile ID.
            tile_id = img_df.loc[idx, 'Tile_ID']               
            
            # Form a key from tile coordinates for given tile.
            key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
            
            # From the localizations dictionary get list of localizations for given key.
            locs_est_storm_tile_lin_fit = locs_est_storm_lin_fit[key]            
            locs_est_storm_tile_quad_fit = locs_est_storm_quad_fit[key]                     

            # Create output files to store the number of localizations per pixel.
            # Note -  The localization estimates are given only in tile frame coordinates.
            num_locs_est_tile_lin_fit_file_name = num_locs_est_directory + "storm_num_locs_est_lin_fit_tile_" + str(tile_id) + ".data"            
            num_locs_est_tile_quad_fit_file_name = num_locs_est_directory + "storm_num_locs_est_quad_fit_tile_" + str(tile_id) + ".data"              

            # Assign process for each tile.
            # process = multiprocessing.Process(target = locsPerTile, args=(tile_start_pix_y, tile_start_pix_x, tile_size, max_locs_per_pixel, nm_per_pixel, storm_image_scale, locs_storm_file_name, locs_tile_file_name, locs_storm))
            process = multiprocessing.Process(target = locsPerTile2, args=(tile_start_pix_y, tile_start_pix_x, tile_size, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name, locs_est_storm_tile_lin_fit, locs_est_storm_tile_quad_fit))                
            jobs.append(process)
            process.start()
                        
            tile_count += 1
            
    total_loc_files = tile_count        

    return total_loc_files            














         



        

