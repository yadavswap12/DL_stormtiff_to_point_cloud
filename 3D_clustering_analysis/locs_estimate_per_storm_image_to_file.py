"""
Script to create parallel processes for estimating localizations in specified image tiles of stormtiff image list.
        
Swapnil 2/22
"""

import os
import glob
import pandas as pd
# import matplotlib
# from matplotlib.offsetbox import AnchoredText
import multiprocessing
from multiprocessing import Semaphore

from locs_estimate_per_storm_image import locsEstimatePerStormImage

if __name__ == "__main__":

    # Set path to data files.
    expfolder = "analysis_path\\experiment_name\\"
    
    # storm_exp_name = "561storm"
    # storm_exp_name = "647storm"    
    storm_exp_name = "750storm"
    storm_exp_directory = expfolder + storm_exp_name + "\\"

    # If does not exists, create new directory for localization estimation with nearest neighbor averaging.      
    if not os.path.exists(storm_exp_directory + "locs_estimate_dictionary\\"):
        os.mkdir(storm_exp_directory + "locs_estimate_dictionary\\")

    # Set directory for localization estimation with nearest neighbor averaging.
    locs_est_dict_directory = storm_exp_directory + "locs_estimate_dictionary\\"

    # Get stormtiff directory.
    stormtiff_directory = storm_exp_directory + "stormtiff_tiles\\"

    # Get tile-list file.
    tile_list_file = storm_exp_directory + "tile_list\\" + "750_ROIs_to_csv_no_empty_tiles_sorted.csv"
        
    # Remove previously present files in given directory.
    files = glob.glob(locs_est_dict_directory + "*")
    for file in files:
        os.remove(file)     

    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    print("total tiles are {}" .format(len(df)))

    # Set tile size for square shaped tile.
    tile_size = 86
    
    # Remove previously present files. 
    files = glob.glob(locs_est_dict_directory + "*")
    for f in files:
        os.remove(f)
        
    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 1                
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()  
    sema = Semaphore(max_processes)        
    
    # Iterate over individual image numbers in dataframe.
    for img_num in df["z(Num_image)"].unique():

        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["z(Num_image)"]==img_num]
        
        # Create a dictionary filename.
        locs_est_dict_file_name_lin_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_lin_fit.data"
        locs_est_dict_file_name_quad_fit = locs_est_dict_directory + "locs_dict_img_" + str(img_num) + "_quad_fit.data"
        
        # Create a tupple of file names.
        locs_est_dict_file_name = (locs_est_dict_file_name_lin_fit, locs_est_dict_file_name_quad_fit)  

        # Once max_processes are running, block the main process.
        # the main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()                
        
        # Assign process for each tile.
        # Process for localization estimation with nearest neighbor averaging.         
        process = multiprocessing.Process(target = locsEstimatePerStormImage, args=(stormtiff_directory, tile_size, img_df, locs_est_dict_file_name, sema))

        # # Process for localization estimation without nearest neighbor averaging. 
        # process = multiprocessing.Process(target = locsEstimatePerStormImage2, args=(stormtiff_file, tile_size, img_df, locs_est_dict_file_name))
        
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the process are terminated.         
    for job in jobs:
        
        job.join()        