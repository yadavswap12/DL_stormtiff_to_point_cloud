"""
This is a test script to compute maximum pixel intensity signal for list of stormtiff images.  

Swapnil 1/22
"""

import numpy as np
import glob
import os
from tifffile import tifffile

# Are you analyzing training tiles or test tiles?
training = True

# Set path to data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
testing_data_directory = data_directory + "testing_data\\"

#storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"

if training: storm_exp_directory = training_data_directory + storm_exp_name + "\\"

else: storm_exp_directory = testing_data_directory + storm_exp_name + "\\"        

# Get stormtiff directory.
stormtiffs_directory = storm_exp_directory + "stormtiffs\\"
# stormtiffs_directory = storm_exp_directory + "stormtiffs_uint8\\"

# Get all the images present in stormtiff folder. 
img_files = glob.glob(stormtiffs_directory + "*")

# Initialize maximum intensity.
max_int = 0

# Iterate over individual image files.
for img_file in img_files:

    # Load the image in the form of an array.
    stormtiff_image_array = tifffile.imread(img_file)    # type(stormtiff_image_array) = numpy.ndarray
    
    # Get stormtiff image number from file name.
    img_filename = os.path.basename(img_file)
    img_num = int(img_filename[9:12])    # 9th, 10th and 11th places in storm image file name denote image number.  

    # # Following lines also give image number from file name.
    # img_filename_copy = os.path.basename(img_file)    
    # img_filename_copy.replace("750storm_",'')    # Remove given string from filename. 
    # img_filename_copy.replace("_mlist",'')    # # Remove given string from filename.
    # img_num = int(img_filename_copy)

    max_int_img = np.amax(stormtiff_image_array)  

    if (max_int_img > max_int):
        max_int = max_int_img
        img_num_max_int = img_num

    # Write image number and corresponding maximum intensity for that image to a .csv file.
    with open(stormtiffs_directory + "max_sig_stormtiff_list.csv","a") as f_out:
        f_out.write("{},{}\n" .format(img_num, max_int_img))
        
    print("Maximum intensity for stormtiff image {} is written to file." .format(img_num))    
        
# Write maximum intensity for the whole stormtiff list and corresponding stormtiff image number to a final line of .csv file.
with open(stormtiffs_directory + "max_sig_stormtiff_list.csv","a") as f_out:
    f_out.write("Maximum intensity for the whole stormtiff image list is {} and is from stormtiff image {}\n" .format(max_int, img_num_max_int))        
    