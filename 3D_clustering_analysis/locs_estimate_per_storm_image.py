"""
Function for making dictionary of localization estimations in specified image tiles of stormtiff image list.
        
Swapnil 12/21
"""
import numpy as np
import pickle
import itertools
import math
import multiprocessing
from tifffile import tifffile
from scipy.stats import truncnorm 

def locsEstimatePerStormImage(stormtiff_directory, tile_size, img_df, locs_est_dict_file_name, sema):

    # Process details
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))
    
    # Get dictionary file-names from tupple.
    (locs_est_dict_file_name_lin_fit, locs_est_dict_file_name_quad_fit) = locs_est_dict_file_name       
    
    # Initialize dictionary of localizations in storm image section
    locs_est_storm_lin_fit = {}
    locs_est_storm_quad_fit = {}

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
    for idx in img_df.index:

        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
        
        # Get the tile ID.
        tile_id = img_df.loc[idx, 'Tile_ID']        

        # For post-aligned and filtered stormtiff images. 
        if ((tile_id)//10 == 0): stormtiff_file = stormtiff_directory + "00000" + str(tile_id) + ".tif"
        
        elif (((tile_id)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0000" + str(tile_id) + ".tif"
        
        elif ((((tile_id)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "000" + str(tile_id) + ".tif"
        
        elif (((((tile_id)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "00" + str(tile_id) + ".tif"
        
        elif ((((((tile_id)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + "0" + str(tile_id) + ".tif"

        elif (((((((tile_id)//10)//10)//10)//10)//10)//10 == 0): stormtiff_file = stormtiff_directory + str(tile_id) + ".tif"
        
        tile = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
        
        # To dictionary of localizations in storm image, add pixel ids as key 
        # and initialize a list for localizations in given pixel as value for the key.
        locs_est_storm_lin_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []
        locs_est_storm_quad_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)] = []        
        
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
            
            # Get number of localizations from fit to signal intensity.
            if (sig_nn_avg < 20.0):
            
                # Define truncated normal distribution function.
                def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
                    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
                
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
            locs_est_storm_lin_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)].extend(locs_est_pix_lin)
            locs_est_storm_quad_fit["locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)].extend(locs_est_pix_quad)
            
    # Writting locs per tile to files. 
    with open(locs_est_dict_file_name_lin_fit, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_lin_fit, filehandle) 

    # Writting locs per tile to files. 
    with open(locs_est_dict_file_name_quad_fit, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_est_storm_quad_fit, filehandle)   

    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue
    sema.release()        
                
        
        
        
        
        
        
        
        
        
        

 