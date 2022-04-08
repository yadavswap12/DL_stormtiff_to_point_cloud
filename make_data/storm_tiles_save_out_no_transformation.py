"""
This fiji macro is based on macro 'storm_save_out.py'. It converts Stormtiff image from 'single' data 
format to 'unit16' (maximum intensity 65535) data format or 'unit8' (maximum intensity 255) data format without applying any alignment transformations.

Swapnil 1/22
"""

import os,sys
import glob
import shutil
from ij import IJ  
from ij.process import ImageStatistics as IS
from ij import Prefs
import time

# get experiment folder from python
expfolder = "analysis_path\\"
# set paths
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
# testing_data_directory = data_directory + "testing_data\\"

# storm_exp_name = "561storm"
# storm_exp_name = "647storm"
storm_exp_name = "647storm_no_saturation"
# storm_exp_name = "750storm"

storm_exp_directory = training_data_directory + storm_exp_name + "\\"
# storm_exp_directory = testing_data_directory + storm_exp_name + "\\"    
stormtiffs_directory = storm_exp_directory + "stormtiff_tiles_transformed_blurred\\"

# If does not exists, create new directory for uint8 stormtiff images.
if not os.path.exists(storm_exp_directory + "stormtiff_tiles_transformed_blurred_uint8\\"):
    os.mkdir(storm_exp_directory + "stormtiff_tiles_transformed_blurred_uint8\\")
    
stormtiffs_directory_uint8 = storm_exp_directory + "stormtiff_tiles_transformed_blurred_uint8\\"

# Get all the images present in stormtiff folder. 
img_files = glob.glob(stormtiffs_directory + "*")

# Iterate over individual image files.
for img_file in img_files:

    # Get image file name.
    img_filename = os.path.basename(img_file)

    print(img_filename)

    imp = IJ.openImage((img_file))
    IJ.run(imp, "16-bit", "")
    imp.show()
    # IJ.run("Enhance Contrast", "saturated=0.3")
    IJ.run("Enhance Contrast", "saturated=0.0")    
    IJ.run("Apply LUT")
    # IJ.run(imp, "16-bit", "")
    IJ.run(imp, "8-bit", "")    
    IJ.saveAs(imp, "Tiff", (stormtiffs_directory_uint8 + img_filename))
    imp.close();
    
IJ.run("Close All", "");

