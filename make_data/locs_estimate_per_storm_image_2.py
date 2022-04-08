"""
Function for making estimations for number of localizations per pixel from stormtiff image tiles.

This script is different from locs_estimate_per_storm_image.py as it does not average over nearest neighbors while 
predicting the number of localizations from stormtiff image.    
        
Swapnil 1/22
"""
import numpy as np
import pickle
import itertools
import math
import multiprocessing
from tifffile import tifffile

def locsEstimatePerStormImage2(stormtiff_directory, tile_size, storm_image_scale, img_df, locs_est_dict_file_name, channel, uint8, sema):

    # Process details.
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))

    # # Get stormtiff image.
    # stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
    
    # Get dictionary file-names from tupple.
    (locs_est_dict_file_name_lin_fit, locs_est_dict_file_name_quad_fit) = locs_est_dict_file_name       
    
    # Initialize dictionary of localizations in storm image section.
    locs_est_storm_lin_fit = {}
    locs_est_storm_quad_fit = {}

    # List of coefficients from highest to lowest degree for polynomial fit (f(x) = coef[0]*x**n + coef[1]*x**(n-1) + ... + coef[n])
    # The list is found from sig_intesity_vs_loc_density.py 
    if (channel == "561storm"):
    
        if uint8:
        
            # pass
            # Coefficients for 561 channel and uint8 datatype.
            coef1 = [0.045472407327056284, -0.1318786631018805]
            coef2 = [0.00037214381469885684, -0.031098925558799454, 0.07589720917078603]

        else: 
        
            # Coefficients for 561 channel.
            coef1 = [1.3058884319927422, -0.012829047546426713]
            coef2 = [0.006895699692032262, 1.0509767817272098, 0.0011626601969680055]

    elif (channel == "647storm"):
    
        if uint8:
        
            # pass
            # # Coefficients for 647 channel and uint8 datatype with 0.3 saturation.
            # coef1 = [0.020566544735555848, -0.0002843564651092773]
            # coef2 = [3.9396307058006944e-05, 0.013017080650862363, 0.010744420497577395]
            
            # # Coefficients for 647 channel and uint8 datatype with 0.01 saturation.
            # coef1 = [0.21772410421209096, -0.015225682234650812]
            # coef2 = [0.0005799012459515905, 0.15711056495319434, 0.018844083337277072]

            # Coefficients for 647 channel and uint8 datatype with intensity-transform.
            coef1 = [0.046628958810424864, -0.03730664340399158]
            coef2 = [0.0002316377928535721, 0.021220177212217008, 0.0031084989948440907]                   

        else: 
        
            # Coefficients for 647 channel.
            coef1 = [1.2291747698187308, 0.015945786321955428]
            coef2 = [-0.10895379029017836, 1.8095791618225017, 0.007008934071100023]

    elif (channel == "750storm"):
    
        if uint8:
        
            # Coefficients for 750 channel and uint8 datatype.
            coef1 = [0.048444465641161706, -0.08657427333332146]    # fit from project 14.
            coef2 = [0.00011772590610813693, 0.03178708473681607, 0.012119446304195071]    # fit from project 14.
            # coef1 = [0.057119309596473294, -0.05900190175286056]    # fit from project 15.
            # coef2 = [0.00028923150976019026, 0.009569265138515536, 0.021079449352223403]    # fit from project 15.                

        else: 
        
            # Coefficients for 750 channel.
            coef1 = [0.4795187198928817, -0.05356505718095568]
            coef2 = [0.005899245913286556, 0.4008079724468171, -0.011281064571405939]       
    
    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
        
        # Get the tile ID.
        tile_id = img_df.loc[idx, 'Tile_ID']          
        
        # # For pre-aligned and filtered 750 channel stormtiff images. 
        # if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "00000" + str(tile_id) + ".tif"
        
        # elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
        
        # elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
        
        # elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
        
        # elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"

        # elif (((((((tile_id)//10)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"
        
        # For pre-aligned and filtered 647 channel stormtiff images. 
        if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
        
        elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
        
        elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
        
        elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"
        
        elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"        
        
        tile = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray      

        # # Slicing the image array according to the tile position
        # tile = stormtiff_image_array[tile_start_pix_y:tile_start_pix_y+tile_size, tile_start_pix_x:tile_start_pix_x+tile_size]
        
        # To dictionary of localizations in storm image, add pixel ids as key 
        # and initialize a list for localizations in given pixel as value for the key.
        locs_est_storm_lin_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []
        locs_est_storm_quad_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []        
        
        # Iterate over pixels from selected tile.
        for j, i in itertools.product(range(0, tile_size), range(0, tile_size)):
            
            # Get signal intensity for given pixel in tile.
            sig = tile[j,i]
            
            # Assign zero signal intensity of zero localizations else get number of localizations from fit coefficients and signal intensity.
            if (sig == 0):
                num_loc_lin_fit = 0
                num_loc_quad_fit = 0

            else: 
                num_loc_lin_fit = np.poly1d(coef1)(sig)
                num_loc_quad_fit = np.poly1d(coef2)(sig)                        
                
            # Add list of estimated number of localizations to center of the tile pixel.
            # If estimated number of localizations are a positive integer.
            if math.ceil(num_loc_lin_fit) > 0:
                locs_est_pix_lin = math.ceil(num_loc_lin_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
            # Else create list of array with default value -1 for coordinates.
            else:
                locs_est_pix_lin = [np.array([-1, -1])]
                
            # if round(num_loc_lin_fit) > 0:
                # locs_est_pix_lin = round(num_loc_lin_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
            # # Else create list of array with default value -1 for coordinates.
            # else:
                # locs_est_pix_lin = [np.array([-1, -1])]                

            # If estimated number of localizations are a positive integer.            
            if math.ceil(num_loc_quad_fit) > 0:
                locs_est_pix_quad = math.ceil(num_loc_quad_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
            # Else create list of array with default value -1 for coordinates.    
            else:
                locs_est_pix_quad = [np.array([-1, -1])]

            # if round(num_loc_quad_fit) > 0:
                # locs_est_pix_quad = round(num_loc_quad_fit)*[np.array([(j+1.0/2),(i+1.0/2)])]
            # # Else create list of array with default value -1 for coordinates.    
            # else:
                # locs_est_pix_quad = [np.array([-1, -1])]                                
            
            # Add the list to final dictionary of lists.
            locs_est_storm_lin_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)].extend(locs_est_pix_lin)
            locs_est_storm_quad_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)].extend(locs_est_pix_quad)
            
    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(locs_est_dict_file_name_lin_fit, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_lin_fit, filehandle) 

    # Writting locs per tile to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(locs_est_dict_file_name_quad_fit, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_quad_fit, filehandle) 

    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue
    sema.release()        
                
        
        
        
        
        
        
        
        
        
        

 