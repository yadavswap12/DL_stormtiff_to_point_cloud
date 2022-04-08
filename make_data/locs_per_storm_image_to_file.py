"""
Script to create parallel processes for making dictionary of localizations in specified image tiles of 
stormtiff image list.
        
Swapnil 2/22
"""

import os
import pandas as pd
# import matplotlib
# from matplotlib.offsetbox import AnchoredText
import multiprocessing

from locs_per_storm_image import locsPerStormImage
from multiprocessing import Semaphore

if __name__ == "__main__":

    # Set path to data files.
    expfolder = "analysis_path\\"
    data_directory = expfolder + "make_data\\"
    training_data_directory = data_directory + "training_data\\"
    # testing_data_directory = data_directory + "testing_data\\"
    storm_exp_name = "647storm"  
    storm_exp_directory = training_data_directory + storm_exp_name + "\\"
    # storm_exp_directory = testing_data_directory + storm_exp_name + "\\"    
    molecule_lists_directory = storm_exp_directory + "molecule_lists\\"
    
    tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv.csv"                   

    # Set tile size for square shaped tile. 
    tile_size = 72        

    # Specify ROI extension string for data directory.
    # roi = "_ROIs_mixed_first_70"        
    # roi = "_ROIs_mixed_first_100"
    # roi = "_ROIs_14k" 
    # roi = "_ROIs_from_3k_14k_shuffled"
    roi = "_ROIs"                
    
    # If does not exists, create a directory for localization dictionary.
    if not os.path.exists(storm_exp_directory + "locs_dictionary_tilesize_" + str(tile_size) + roi + "\\"):
        os.mkdir(storm_exp_directory + "locs_dictionary_tilesize_" + str(tile_size) + roi + "\\")
        
    locs_dict_directory = storm_exp_directory + "locs_dictionary_tilesize_" + str(tile_size) + roi + "\\"

    # Make a dataframe from csv file containing list of tile coordinates.
    df = pd.read_csv(tile_list_file)

    print("total tiles are {}" .format(len(df)))

    # Initialize maximum localizations per tile.
    max_locs_per_tile = 0

    # Set scaling factor between raw image and stormtiff image.
    storm_image_scale = int(10)
    
    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 1    
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)        
    
    # Iterate over individual image numbers in dataframe.
    for img_num in df["Num_image"].unique():

        # Create a dataframe for particular "Num_img" entry.
        img_df = df[df["Num_image"]==img_num]

        # Get molecule list file for given image number.        
        if ((img_num-1)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_00" + str(img_num-1) + "_mlist" + ".hdf5"
        
        elif (((img_num-1)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_0" + str(img_num-1) + "_mlist" + ".hdf5"
        
        elif ((((img_num-1)//10)//10)//10 == 0): h5_file = molecule_lists_directory + storm_exp_name + "_" + str(img_num-1) + "_mlist" + ".hdf5"
        
        # Create a dictionary filename.
        locs_dict_file_name = locs_dict_directory + "locs_dict_img_" + str(img_num) + ".data"
        
        # once max_processes are running, block the main process
        # The main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()         
        
        # Assign process for each tile.
        process = multiprocessing.Process(target = locsPerStormImage, args=(h5_file, tile_size, storm_image_scale, img_df, locs_dict_file_name, sema))
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the process are terminated.     
    for job in jobs:
        
        job.join()        