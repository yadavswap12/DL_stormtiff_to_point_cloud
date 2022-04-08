"""
Script to predict localizations from pixel intensities in stormtiff images 
using previously trained models.

Swapnil 2/22
"""

import numpy as np
import glob
import pickle
import os
import pandas as pd

import tensorflow as tf

from get_data_2 import getData

# Limiting GPU memory growth.
gpus = tf.config.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e) 

# Are you analyzing data with nearest neighbor averaging of pixel intensities for predicting localizations from fit?
nn_avg = True

# Are you using lin_fit for estimating localizations from fit?
lin_fit = True

# Get test data.
# Set path to data files.
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"    
# storm_exp_name = "750storm"
storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Get the tile-list file.
tile_list_file = storm_exp_directory + "tile_list\\" + "647_ROIs_to_csv_no_empty_tiles_sorted.csv"

# Make a dataframe from csv file containing list of tile coordinates.
df = pd.read_csv(tile_list_file)

# Give the experiment name and experiment model name as a string.
exp_name = "experiment_1"
exp_mod = "experiment1_model"

# Set path for prediction files.
if not os.path.exists(experiment_directory + "model_predictions\\"):
    os.mkdir(experiment_directory + "model_predictions\\")  
    
prediction_directory = experiment_directory + "model_predictions\\"

# Remove previously present files from the directory.
files = glob.glob(prediction_directory + "*")
for file in files:
    os.remove(file)

# Get the path of the previously trained model for this experiment.
model_file = experiment_directory + exp_mod

# Get number of epochs for which the model was trained.
epochs = 1000

# Specify the tile-size of storm image section for training data.
tile_size = 72

data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_sorted\\"

data_path = storm_exp_directory + data_directory_str
tiles_data_path = data_path + "tiles\\"
# tiles_data_path = data_path + "tiles_flattened\\"

if nn_avg: num_locs_est_data_path = data_path + "num_locs_estimate\\"
else: num_locs_est_data_path = data_path + "num_locs_estimate_no_nn_avg\\"

if os.path.exists(tiles_data_path): tiles = getData(tiles_data_path, data_type="tiles", df=df)
    
else: print("Tiles data for this tile-size, tile-step and storm image section does not exist.")

if os.path.exists(num_locs_est_data_path): num_locs_est_lin_fit = getData(num_locs_est_data_path, data_type="num_locs_est_lin_fit", df=df)

else: print("Locs_estimate data for this tile-size, tile-step and storm image section does not exist.")

if os.path.exists(num_locs_est_data_path): num_locs_est_quad_fit = getData(num_locs_est_data_path, data_type="num_locs_est_quad_fit", df=df)

else: print("Locs_estimate data for this tile-size, tile-step and storm image section does not exist.")   

# total number of input tiles for training
num_tiles = len(tiles)

# total number of locs estimate files for training
num_num_locs_est = len(num_locs_est_lin_fit)
    
print("total number tiles created for testing are {}\n" .format(num_tiles))
print("total number of localization estimation files created for testing are {}\n" .format(num_num_locs_est))

# Convert tiles and locs lists to arrays.
tiles_test = np.array(tiles)
print("Testing input from tiles has shape {}\n" .format(tiles_test.shape))

num_locs_est_lin_fit_test = np.array(num_locs_est_lin_fit)
num_locs_est_quad_fit_test = np.array(num_locs_est_quad_fit)

# If necessary reshape input data from tiles to a shape the sequential model expects.
tiles_test = np.reshape(tiles_test, (num_tiles, tile_size, tile_size, 1))    # If image data is greyscale.

# # Convert 1 channel greyscale image array into repeated 3 channel greyscale image array.
# # This is done so that the most pretrained models like resnet50 can be used with single channel greyscale images.
# tiles_test = np.repeat(tiles_test[..., np.newaxis], 3, -1)

# Reshape output data from locs to 1D array.
num_locs_est_lin_fit_test = np.reshape(num_locs_est_lin_fit_test, (num_tiles, tile_size*tile_size, 1))
num_locs_est_quad_fit_test = np.reshape(num_locs_est_quad_fit_test, (num_tiles, tile_size*tile_size, 1))

print("Testing input to model has shape {}\n" .format(tiles_test.shape))
print("Testing output from model has shape {}\n" .format(num_locs_est_lin_fit_test.shape))

# Scale the pixel intensities to range [0,1]. 
tiles_test = tiles_test/255.0

# Loading the model back.
model = tf.keras.models.load_model(model_file)

for i in range(num_tiles):

    # Get the tile-id from tile-list dataframe.
    tile_id = df["Tile_ID"][i]    

    # # Use following lines for 1D flattened tiles.
    # tile_test = tiles_test[i,:]
    # tile_test = np.reshape(tile_test, (1, tile_size*tile_size))

    # Use following lines for 2D tiles.
    tile_test = tiles_test[i,:,:,:]
    tile_test = np.reshape(tile_test, (1, tile_size, tile_size, 1))
    
    # # Use following lines for resnet50 predicitions.
    # tile_test = tiles_test[i,:,:,:]
    # tile_test = np.reshape(tile_test, (1, tile_size, tile_size, 3))    

    num_loc_est_lin_fit_test = num_locs_est_lin_fit_test[i,:,:]
    num_loc_est_lin_fit_test = np.reshape(num_loc_est_lin_fit_test, (1, tile_size*tile_size, 1))    

    num_loc_est_quad_fit_test = num_locs_est_quad_fit_test[i,:,:]
    num_loc_est_quad_fit_test = np.reshape(num_loc_est_quad_fit_test, (1, tile_size*tile_size, 1))      
    
    # locs_pred_storm_file = prediction_directory + "storm_pred_locs_tile_" + str(i) + ".data"
    # num_locs_pred_tile_file = prediction_directory + "tile_pred_num_locs_tile_" + str(i) + ".data"    
    num_locs_pred_tile_file = prediction_directory + "tile_pred_num_locs_tile_" + str(tile_id) + ".data"
    
    # Make predictions with trained model.
    pred = model.predict(tile_test)
    
    # Reshaping predictions.
    pred = np.reshape(pred, (1, tile_size*tile_size, 1))    
    
    # Find localization prediction from localization error prediction.
    if lin_fit: pred_num_loc = pred + num_loc_est_lin_fit_test
    else: pred_num_loc = pred + num_loc_est_quad_fit_test    

    # Reshaping predictions.
    pred_num_loc = np.reshape(pred_num_loc, (1, tile_size*tile_size))        

    # Writing the model predictions. 
    with open(num_locs_pred_tile_file, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(pred_num_loc, filehandle)

    if (i%100 == 0):
        print("{}th tile is analyzed." .format(i))        


