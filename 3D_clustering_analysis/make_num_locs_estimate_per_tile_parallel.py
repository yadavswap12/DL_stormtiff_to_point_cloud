"""
Script to make estimated number of localizations file for each stormtiff tile.
This script uses multiprocessing module for parallel processing.
        
Swapnil 3/22
"""

import math
import os
import glob
import pandas as pd
import multiprocessing
from multiprocessing import Semaphore

from num_locs_per_tile import numLocsPerTile

if __name__ == "__main__": 

    # Do you want to sort the tile-list according to image number?
    sorted =  True

    # Set path to data files.
    expfolder = "analysis_path\\experiment_name\\"

    # storm_exp_name = "561storm"
    storm_exp_name = "647storm"    
    # storm_exp_name = "750storm"
    storm_exp_directory = expfolder + storm_exp_name + "\\"

    # Get tile-list file.
    tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_sorted.csv"        

    # Set tile size for square shaped tile.
    tile_size = 72     

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

    # Remove previously present files. 
    files = glob.glob(num_locs_est_directory + "*")
    for f in files:
        os.remove(f)        

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
    
    # # Coefficients for 647 channel and uint8 datatype with 0.01 saturation.
    # coef1 = [0.21772410421209096, -0.015225682234650812]
    # coef2 = [0.0005799012459515905, 0.15711056495319434, 0.018844083337277072]

    # Coefficients for 647 channel and uint8 datatype with transform.
    coef1 = [0.046628958810424864, -0.03730664340399158]
    coef2 = [0.0002316377928535721, 0.021220177212217008, 0.0031084989948440907]        

    # # Coefficients for 750 channel and uint8 datatype.
    # coef1 = [0.048444465641161706, -0.08657427333332146]
    # coef2 = [0.00011772590610813693, 0.03178708473681607, 0.012119446304195071]

    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 1        
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)       

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

        # Create output files to store the number of localizations per pixel.
        # Note -  The localization estimates are given only in tile frame coordinates.
        num_locs_est_tile_lin_fit_file_name = num_locs_est_directory + "storm_num_locs_est_lin_fit_tile_" + str(tile_id) + ".data"            
        num_locs_est_tile_quad_fit_file_name = num_locs_est_directory + "storm_num_locs_est_quad_fit_tile_" + str(tile_id) + ".data"              

        # Once max_processes are running, block the main process.
        # the main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()

        # Assign process for each tile.        
        # Process for localization estimation with nearest neighbor averaging. 
        process = multiprocessing.Process(target = numLocsPerTile, args=(tile_size, tile_id, coef1, coef2, stormtiff_file, locs_est_storm_lin_fit, locs_est_storm_quad_fit, num_locs_est_tile_lin_fit_file_name, num_locs_est_tile_quad_fit_file_name, sema))        
            
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the processes are terminated.       
    for job in jobs:
        
        job.join()
       
                
        
        
        
        
        
        
        
        
        
        

 