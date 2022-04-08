"""
Experiment to train the neural network model.

Swapnil 1/22
"""

import numpy as np
import os

import tensorflow as tf

import models
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

# Get training data.
# Set path to data files.
expfolder = "analysis_path\\"
data_directory = expfolder + "make_data\\"
training_data_directory = data_directory + "training_data\\"
# testing_data_directory = data_directory + "testing_data\\"
storm_exp_name = "647storm"
storm_exp_directory = training_data_directory + storm_exp_name + "\\"
experiment_directory = expfolder + "experiments\\"

# Specify the tile-size of storm image section for training data.
tile_size = 72

# Choose fit for the estimated localizations.
linear_fit = True
quadratic_fit = False

data_directory_str = "chenghang_list_" + "tilesize_" + str(tile_size) + "_uint8_ROIs_from_3k_14k_shuffled\\"

data_path = storm_exp_directory + data_directory_str
tiles_data_path = data_path + "tiles\\"
num_locs_data_path = data_path + "num_locs\\"
num_locs_est_data_path = data_path + "num_locs_estimate\\"

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
    
print("total number of tiles created for training are {}\n" .format(num_tiles))
print("total number of localization files created for training are {}\n" .format(num_num_locs))

# Convert tiles and locs lists to arrays.
tiles_train = np.array(tiles)
print("Training input from tiles has shape {}\n" .format(tiles_train.shape))

num_locs_train = np.array(num_locs)
print("Training output from files has shape {}\n" .format(num_locs_train.shape))

num_locs_est_lin_fit_train = np.array(num_locs_est_lin_fit)
print("Training output from files has shape {}\n" .format(num_locs_est_lin_fit_train.shape))

num_locs_est_quad_fit_train = np.array(num_locs_est_quad_fit)
print("Training output from files has shape {}\n" .format(num_locs_est_quad_fit_train.shape))

# If necessary reshape input data from tiles to a shape the sequential model expects
tiles_train = np.reshape(tiles_train, (num_tiles, tile_size, tile_size, 1))

# Get the localization error as the output of the network.
if linear_fit: num_locs_error_train = num_locs_train - num_locs_est_lin_fit_train

if quadratic_fit: num_locs_error_train = num_locs_train - num_locs_est_quad_fit_train        

# Reshape output data from locs to 1D array.
num_locs_error_train = np.reshape(num_locs_error_train, (num_tiles, tile_size*tile_size, 1))

print("Training input to model has shape {}\n" .format(tiles_train.shape))
print("Training output from model has shape {}\n" .format(num_locs_error_train.shape))

# Scale the pixel intensities to range [0,1]. 
tiles_train = tiles_train/255.0

# Set model parameters.
conv_input_shape = tiles_train.shape
output_nodes = num_locs_error_train.shape[1]

# Set number of Conv2D layers in model.
conv_layers = 6

# Set number of fully-connected layers after Conv2D layers in model.
fc_layers = 2

params = (conv_input_shape, output_nodes, conv_layers, fc_layers)

# Choose model from models.py and initialize it with parameters. 
model_class = models.cnnRegression(parameters=params)

# Build convolutional part of the model.
# Set stride for Conv2D layers.
stride = (1,1)

# Set padding for Conv2D layers.
pad = "same"

# Set activation function for Conv2D layers.
activ = "relu"

# Set regularization method for Conv2D layers.
reg = None

# Set initialization method for Conv2D layers.
init = "glorot_uniform"

# Set dropout probability for Conv2D layers.
# If no dropout then set these to None. 
drop = None

# Want to include batch normalization for Conv2D layers? Set Boolean value (True or False).
BN = False

# Set pooling window size for Conv2D layers.
pool_sz = (2,2)

# Set pooling window stride for Conv2D layers.
pool_st = 2

# Set padding for pooling in Conv2D layers.
pool_pd = "valid"

model = model_class.cnnBuild(conv_stride=stride, conv_pad=pad, conv_activ=activ, conv_reg=reg, conv_init=init, conv_drop=drop, conv_BN=BN , pool_size=pool_sz, pool_stride=pool_st, pool_pad=pool_pd)

# Build and attach fully-connected network to convolutional network.
# Set the list of number of nodes in each fully-connected layer.
# If you want use default list, set it to an empty list.
# lyr = []
lyr = [100, 100]

# Set activation function for fully-connected layers.
activ = "relu"

# Set regularization method for fully-connected layers.
reg = None

# Set initialization method for fully-connected layers.
init = "glorot_uniform"

# Set dropout probability for fully-connected layers.
# If no dropout then set these to None. 
drop = None

# Want to include batch normalization for fully-connected layers? Set Boolean value (True or False).
BN = False

model  = model_class.fcBuild(model, fc_layers=lyr, fc_activ=activ, fc_reg=reg, fc_init=init, fc_drop=drop, fc_BN=BN, fc_output_layer_units=output_nodes)

# Set the optimizer, learning rate and rate decay.
opt = tf.keras.optimizers.Adam(learning_rate=1e-3)

# Set the loss function.
mse = tf.keras.losses.MeanSquaredError()

# Compiling the model
model.compile(optimizer=opt, loss=mse)

# Choose number of epochs for training.
# Epochs for initial training.
init_epo = 1000
# Epochs for further training on saved model.
epo = 1000

# Choose mini-batch size.
# To use default batch size of 32 set it to None. 
bs = None
# bs  = num_tiles

# To get the summary of the model.
model.summary()

# Log the training history.
# Path to saved training history.
# Create new directory for training history if it does not exist.
if not os.path.exists(experiment_directory + "saved_training_history\\"):
    os.mkdir(experiment_directory + "saved_training_history\\")
 
history_directory = experiment_directory + "saved_training_history\\"
history_file = history_directory + "experiment1_history.csv"

training_history_log = tf.keras.callbacks.CSVLogger(filename=history_file, separator=",", append=True)

# Path to saved model.
# Create new directory for saved models if it does not exist.
if not os.path.exists(experiment_directory + "saved_models\\"):
    os.mkdir(experiment_directory + "saved_models\\")
    
model_directory = experiment_directory + "saved_models\\"
model_file = model_directory + "experiment1_model"

if os.path.exists(model_file):

    # Load previously trained model.
    model = tf.keras.models.load_model(model_file)
    
    # The previously trained model is already compiled and has retained the optimizer
    # state, so its training can resume. Also save the model.
    model.fit(tiles_train, num_locs_error_train, epochs=epo, batch_size=bs, callbacks=[training_history_log])
    model.save(model_file)
    
else:

    # Train the model and save.
    model.fit(tiles_train, num_locs_error_train, epochs=init_epo, batch_size=bs, callbacks=[training_history_log])
    model.save(model_file)

# # Checkpoint method.
# # Note- Either use model.save() method or checkpoint method to save or reload trained models. 
# checkpoint_directory = experiment_directory + "saved_checkpoints\\"
# checkpoint_file = checkpoint_directory + "experiment1_checkpoint"

# model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
                                # filepath=checkpoint_file,
                                # monitor="val_loss",
                                # verbose=0,
                                # save_best_only=False,
                                # save_weights_only=False,
                                # mode="auto",
                                # save_freq="epoch",
                                # options=None,
                                # **kwargs
                            # )                            

# if os.path.exists(checkpoint_file):
    
    # # Load previously trained model.
    # model = load_model(checkpoint_file)
    
    # # Find the epoch index from which the training should be resumed.
    # initial_epoch = get_init_epoch(checkpoint_file)
    
    # # Resume training the model.
    # model.fit(tiles_train, locs_train, epochs=epo, batch_size=bs, callbacks=[model_checkpoint_callback, training_history_log], initial_epoch=initial_epoch)

# else:
    
    # initial_epoch = 0
    
    # # Start training the model.
    # model.fit(tiles_train, locs_train, epochs=epo, batch_size=bs, callbacks=[model_checkpoint_callback, training_history_log], initial_epoch=initial_epoch)



