"""
This is a test script to compute maximum pixel intensity signal for given stormtiff image or 
a section of the image.  

Swapnil 11/21
"""

import itertools
import os
from tifffile import tifffile

# Set path to data files
expfolder = "analysis_path\\signal_and_loc_density_analysis\\"
data_directory = expfolder + "make_data\\"
storm_exp_name = "750storm"
storm_exp_directory = data_directory + storm_exp_name + "\\"

# Get molecule-list file.
h5_file = storm_exp_directory + os.path.basename(os.path.normpath(storm_exp_directory)) + "_000_mlist.hdf5" 

# Get stromtiff images for corresponding .hdf5 file
h5_filename = os.path.basename(h5_file)
stormtiff_file = storm_exp_directory + h5_filename[:-5] + ".tiff"
stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
stormtiff_image_size = stormtiff_image_array.shape

full_image_analysis = True
image_section  = (13, 3432, 113, 3532)

if full_image_analysis:

    # Get full image coordinates.
    start_pix_x = 0
    start_pix_y = 0
    stop_pix_x = stormtiff_image_size[1] - 1
    stop_pix_y = stormtiff_image_size[0] - 1

else:

    # Get image section coordinates
    start_pix_x, start_pix_y, stop_pix_x, stop_pix_y = image_section
    
max_int = 0

# Iterate over pixels from selected section of stormtiff image.
for j, i in itertools.product(range(start_pix_y, stop_pix_y+1), range(start_pix_x, stop_pix_x+1)):

    # plt.scatter(stormtiff_image_array[j,i], len(locs_storm["locs_"+str(j)+"_"+str(i)]), c='r', marker="o", s=1)
    if (stormtiff_image_array[j,i] > max_int):
        max_int = stormtiff_image_array[j,i]

print("maximum intensity is {}" .format(max_int))        

    