"""
Function to collect number of localizations per pixel in specified image tiles of stormtiff image list.
        
Swapnil 11/21
"""
import numpy as np
import storm_analysis.sa_library.sa_h5py as saH5Py
import pickle
import math
import multiprocessing 

def locsPerStormImage(h5_file, tile_size, storm_image_scale, img_df, locs_dict_file_name, sema):

    # Process details
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))    
    
    # Initialize dictionary of localizations in storm image section.
    locs_storm = {}
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])

        # To dictionary of localizations in storm image, add pixel ids as key 
        # and initialize a list for localizations in given pixel as value for the key.
        locs_storm["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []

    # To read localizations from given hdf5 file.
    h5 = saH5Py.SAH5Py(h5_file)
    
    # Note: Add fields for amplitude and sigma (or any other useful properties) later.
    # fields = ["x", "y", "xsigma", "ysigma"].
    fields = ["x", "y"]

    for fnum, locs in h5.localizationsIterator(fields = fields):
    
        if ((fnum%1000)==0):
            print("Analyzing frame {}" .format(fnum))
            
        locs_copy = locs.copy()

        # Iterate over number of localizations in given frame.
        for k in range(len(locs_copy["x"])):
        
            # Get raw image coordinates of localization found.
            x_raw = locs_copy["x"][k]
            y_raw = locs_copy["y"][k]

            # Get storm image coordinates of localization found.            
            x_storm = x_raw*storm_image_scale
            y_storm = y_raw*storm_image_scale
            
            # Iterate over keys to find tile for the localization. 
            for key in locs_storm.keys():
            
                # Get the tile coordinates.
                tile_start_pix_y = int(key.split("_")[1])
                tile_start_pix_x = int(key.split("_")[2])
                
                if(((y_storm<=tile_start_pix_y+tile_size-1) & (tile_start_pix_y<=y_storm)) & ((x_storm<=tile_start_pix_x+tile_size-1) & (tile_start_pix_x<=x_storm))):
            
                    # Add the localization to dictionary of localizations in storm image section with
                    # key specified by pixel id.
                    locs_storm[key].append(np.array([y_storm, x_storm]))
            
    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(locs_dict_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_storm, filehandle)

    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue.
    sema.release()        