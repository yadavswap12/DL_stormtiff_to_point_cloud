"""
Script to predict localizations from pixel intensities in stormtiff images 
using previously trained models.

Swapnil 11/21
"""

import numpy as np
import pickle
import os

import tensorflow as tf

from get_data import getData

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
    
# Are you analyzing uint8 data?
uint8 = True
    
# Are you analyzing training data?
train = False

# Are you analyzing data with nearest neighbor averaging of pixel intensities for predicting localizations from fit?
nn_avg = True

# Are you using lin_fit for estimating localizations from fit?
lin_fit = True

# Specify ROI extension string for data directory.
roi = "_ROIs_from_10k_shuffled"                                                                                                                                                                                                                                                                                                                                                                                              

# Get test data.
# Set path to data files.
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
testing_data_directory = data_directory + "testing_data\\"
# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"
storm_exp_directory = testing_data_directory + storm_exp_name + "\\"
experiment_directory = expfolder + "experiments\\"

# Give the experiment name and experiment model name as a string.
exp_name = "experiment_1"
exp_mod = "experiment1_model"

# Set path for prediction files.
if train:
    if not os.path.exists(experiment_directory + "model_predictions_training_data\\"):
        os.mkdir(experiment_directory + "model_predictions_training_data\\")
        
    if not os.path.exists(experiment_directory + "model_predictions_training_data\\" + exp_name + "\\"):
        os.mkdir(experiment_directory + "model_predictions_training_data\\" + exp_name + "\\")    
        
    prediction_directory = experiment_directory + "model_predictions_training_data\\" + exp_name + "\\"
    
else:
    if not os.path.exists(experiment_directory + "model_predictions\\"):
        os.mkdir(experiment_directory + "model_predictions\\")
        
    if not os.path.exists(experiment_directory + "model_predictions\\" + exp_name + "\\"):
        os.mkdir(experiment_directory + "model_predictions\\" + exp_name + "\\")    
        
    prediction_directory = experiment_directory + "model_predictions\\" + exp_name + "\\"

# Get the path of the previously trained model for this experiment.
model_directory = experiment_directory + "saved_models\\"
model_file = model_directory + exp_mod

# Get number of epochs for which the model was trained.
epochs = 1000

# Specify the tile-size of storm image section for training data.
tile_size = 72

if uint8: 
    if train: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_train_uint8" + roi + "\\"
    else: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_uint8" + roi + "\\"

else:
    if train: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_train" + roi + "\\"
    else: data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + roi + "\\"

data_path = storm_exp_directory + data_directory_str
tiles_data_path = data_path + "tiles\\"
# tiles_data_path = data_path + "tiles_flattened\\"
num_locs_data_path = data_path + "num_locs\\"

if nn_avg: num_locs_est_data_path = data_path + "num_locs_estimate\\"
else: num_locs_est_data_path = data_path + "num_locs_estimate_no_nn_avg\\"

if os.path.exists(tiles_data_path): tiles, tile_id_list = getData(tiles_data_path, data_type="tiles")
    
else: print("Tiles data for this tile-size, tile-step and storm image section does not exist.")

if os.path.exists(num_locs_data_path): num_locs, num_locs_tile_id_list = getData(num_locs_data_path, data_type="num_locs")

else: print("Locs data for this tile-size, tile-step and storm image section does not exist.")

if os.path.exists(num_locs_est_data_path): num_locs_est_lin_fit, num_locs_est_lin_fit_tile_id_list = getData(num_locs_est_data_path, data_type="num_locs_est_lin_fit")

else: print("Locs_estimate data for this tile-size, tile-step and storm image section does not exist.")

if os.path.exists(num_locs_est_data_path): num_locs_est_quad_fit, num_locs_est_quad_fit_tile_id_list = getData(num_locs_est_data_path, data_type="num_locs_est_quad_fit")

else: print("Locs_estimate data for this tile-size, tile-step and storm image section does not exist.")   

# total number of input tiles for training
num_tiles = len(tiles)

# total number of locs files for training
num_num_locs = len(num_locs)
    
print("total number tiles created for testing are {}\n" .format(num_tiles))
print("total number of localization files created for testing are {}\n" .format(num_num_locs))

# Convert tiles and locs lists to arrays.
tiles_test = np.array(tiles)
print("Testing input from tiles has shape {}\n" .format(tiles_test.shape))

num_locs_test = np.array(num_locs)
print("Testing output from locs files has shape {}\n" .format(num_locs_test.shape))

num_locs_est_lin_fit_test = np.array(num_locs_est_lin_fit)
num_locs_est_quad_fit_test = np.array(num_locs_est_quad_fit)

# If necessary reshape input data from tiles to a shape the sequential model expects.
tiles_test = np.reshape(tiles_test, (num_tiles, tile_size, tile_size, 1))    # If image data is greyscale.

# # Convert 1 channel greyscale image array into repeated 3 channel greyscale image array.
# # This is done so that the most pretrained models like resnet50 can be used with single channel greyscale images.
# tiles_test = np.repeat(tiles_test[..., np.newaxis], 3, -1)

# Reshape output data from locs to 1D array.
num_locs_test = np.reshape(num_locs_test, (num_tiles, tile_size*tile_size, 1))
num_locs_est_lin_fit_test = np.reshape(num_locs_est_lin_fit_test, (num_tiles, tile_size*tile_size, 1))
num_locs_est_quad_fit_test = np.reshape(num_locs_est_quad_fit_test, (num_tiles, tile_size*tile_size, 1))

print("Testing input to model has shape {}\n" .format(tiles_test.shape))
print("Testing output from model has shape {}\n" .format(num_locs_test.shape))

# # Get the maximum pixel intensity from all stormtiff images.
# # The maximum intensity is found out from 'max_sig_test_storm_image_list.py'
# max_sig = 1142.524658203125 

# # Scale the pixel intensities to range [0,1]. 
# tiles_test = tiles_test/max_sig

# Scale the pixel intensities to range [0,1] for unit8 images. 
tiles_test = tiles_test/255.0

# Loading the trained model.
model = tf.keras.models.load_model(model_file)

# Initialize squared error
squared_error = 0.0

for i in range(len(tile_id_list)): 

    # # Use following lines for 1D flattened tiles.
    # tile_test = tiles_test[i,:]
    # tile_test = np.reshape(tile_test, (1, tile_size*tile_size))

    # Use following lines for 2D tiles.
    tile_test = tiles_test[i,:,:,:]
    tile_test = np.reshape(tile_test, (1, tile_size, tile_size, 1))
    
    # # Use following lines for resnet50 predicitions.
    # tile_test = tiles_test[i,:,:,:]
    # tile_test = np.reshape(tile_test, (1, tile_size, tile_size, 3))    

    num_loc_test = num_locs_test[i,:,:]
    num_loc_test = np.reshape(num_loc_test, (1, tile_size*tile_size, 1))

    num_loc_est_lin_fit_test = num_locs_est_lin_fit_test[i,:,:]
    num_loc_est_lin_fit_test = np.reshape(num_loc_est_lin_fit_test, (1, tile_size*tile_size, 1))    

    num_loc_est_quad_fit_test = num_locs_est_quad_fit_test[i,:,:]
    num_loc_est_quad_fit_test = np.reshape(num_loc_est_quad_fit_test, (1, tile_size*tile_size, 1))      
    
    # locs_pred_storm_file = prediction_directory + "storm_pred_locs_tile_" + str(i) + ".data"
    # num_locs_pred_tile_file = prediction_directory + "tile_pred_num_locs_tile_" + str(i+1) + ".data"
    num_locs_pred_tile_file = prediction_directory + "tile_pred_num_locs_tile_" + str(tile_id_list[i]) + ".data"    
    
    # Make predictions with trained model.
    pred = model.predict(tile_test)
    
    # Reshaping predictions.
    pred = np.reshape(pred, (1, tile_size*tile_size, 1))    
    
    # Find localization prediction from localization error prediction.
    if lin_fit: pred_num_loc = pred + num_loc_est_lin_fit_test
    else: pred_num_loc = pred + num_loc_est_quad_fit_test    

    # Reshaping predictions.
    pred_num_loc = np.reshape(pred_num_loc, (1, tile_size*tile_size))        
    
    # Add squared error
    squared_error += np.mean((pred_num_loc.flatten() - num_loc_test.flatten())**2)

    # Writing the model predictions. 
    with open(num_locs_pred_tile_file, 'wb') as filehandle:
        # store the data as binary data stream.
        pickle.dump(pred_num_loc, filehandle)      

# Compute mean-squared error in predicted localizations and print. 
mean_squared_error = squared_error/num_num_locs
print ("The mean-squared error in predicted localizations is: {}" .format(mean_squared_error))
#print("The mean-squared error in predicted localizations is: %.3f" %(mean_squared_error))

# Save prediction error to file
with open(prediction_directory + "prediction_error.csv","a") as f_out:
    f_out.write("prediction error after {} epochs is {}\n" .format(epochs, mean_squared_error))
    f_out.write("normalized-by-tile-size prediction error after {} epochs is {}\n" .format(epochs, mean_squared_error/(tile_size*tile_size)))
    


