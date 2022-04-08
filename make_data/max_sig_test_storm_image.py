"""
This is a test script to compute maximum pixel intensity signal for given stormtiff image or 
a section of the image.  

Swapnil 11/21
"""

import itertools
from tifffile import tifffile

# Set path to data files
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
# testing_data_directory = data_directory + "testing_data\\"

#storm_exp_name = "561storm"
# storm_exp_name = "647storm"    
storm_exp_name = "750storm"

storm_exp_directory = training_data_directory + storm_exp_name + "\\"
# storm_exp_directory = testing_data_directory + storm_exp_name + "\\"

# Get stormtiff directory.
stormtiffs_directory = storm_exp_directory + "stormtiffs_uint8\\"

# Get stormtiff image number (for image number 000 img_num starts from 1).
img_num = 1

# Get stromtiff images for corresponding image number.
if ((img_num)//10 == 0): stormtiff_file = stormtiffs_directory + "00" + str(img_num) + ".tiff"

elif (((img_num)//10)//10 == 0): stormtiff_file = stormtiffs_directory + "0" + str(img_num) + ".tiff"

elif ((((img_num)//10)//10)//10 == 0): stormtiff_file = stormtiffs_directory + str(img_num) + ".tiff"

stormtiff_image_array = tifffile.imread(stormtiff_file)    # type(stormtiff_image_array) = numpy.ndarray
stormtiff_image_size = stormtiff_image_array.shape

full_image_analysis = True
# image_section  = (2000, 2000, 3000, 3000)
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

    