"""
This is a script for non-linear transformation of pixel intensities (soft-saturation) in raw stormtiff image.
 
Swapnil 4/22
"""

import numpy as np
import glob
import os
from tifffile import tifffile
import cv2

# Are you analyzing uint8 data?
uint8 = True

# Are you collecting training data or test data?
training = True

# Set path to training data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm_no_saturation"    
# storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"

stormtiff_directory = storm_exp_directory + "stormtiffs\\"

# Create new directory for transformed images.
if not os.path.exists(storm_exp_directory + "stormtiffs_transformed\\"):
    os.mkdir(storm_exp_directory + "stormtiffs_transformed\\")
    
stormtiff_transformed_directory = storm_exp_directory + "stormtiffs_transformed\\"   

# Create new directory for transformed images.
if not os.path.exists(storm_exp_directory + "stormtiffs_transformed_blurred\\"):
    os.mkdir(storm_exp_directory + "stormtiffs_transformed_blurred\\")
    
stormtiff_transformed_blurred_directory = storm_exp_directory + "stormtiffs_transformed_blurred\\"         
    

# Set transformation parameters.
# This parameter is chosen such that the pixel intensity distribution (as seen in fiji) for transformed and blurred uint8 images 
# looks very similar to aligned uint8 images.
c = 0.38    

# The maximum intensity for raw stormtiff images is found out from 'max_sig_test_storm_image_list.py'
max_sig = 1142.524658203125

counter = 0
 
# Get image files. 
files = glob.glob(stormtiff_directory + "*.tiff")

for file in files:
    # Get image tile.
    tile = tifffile.imread(file)    # type(stormtiff_image_array) = numpy.ndarray
    
    # Get the transformed tile.
    # Converting to 32-bit float format to be able to read by ImageJ.
    tile = (max_sig/np.tanh(c*max_sig))*np.tanh(c*tile).astype(np.float32)
    
    # Get the filename.
    # Note that raw data tiles are in .tif format (integer-valued intensity) and transformed files to be saved in .tiff format (float-valued intensity).
    # filename = stormtiff_transformed_directory + os.path.basename(file)[:-4] + ".tiff"
    filename = stormtiff_transformed_directory + os.path.basename(file)    
    
    # Save the transformed tile.
    tifffile.imsave(filename, tile)    
    # tifffile.imsave(filename, tile, frames.astype(np.uint16))
    
    # Apply guassian blur on image tile.
    tile = cv2.GaussianBlur(tile, ksize=[0,0], sigmaX=0.6, sigmaY=0.6, borderType=cv2.BORDER_DEFAULT)

    # Get the filename.
    # Note that raw data tiles are in .tif format (integer-valued intensity) and transformed files to be saved in .tiff format (float-valued intensity).
    # filename = stormtiff_transformed_blurred_directory + os.path.basename(file)[:-4] + ".tiff"
    filename = stormtiff_transformed_blurred_directory + os.path.basename(file)        
    
    # Save the transformed tile.
    tifffile.imsave(filename, tile)    
    # tifffile.imsave(filename, tile, frames.astype(np.uint16))    

    counter += 1
    
    # if counter%100 == 0:
        # print("{}th tile is transformed." .format(counter))
        
    if counter%10 == 0:
        print("{}th tile is transformed." .format(counter))        
    
