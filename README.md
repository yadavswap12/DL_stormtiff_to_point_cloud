# DL_stormtiff_to_point_cloud
Deep Learning based localization prediction for STORMTIFF images.

This repository hosts the source code for a Deep Learning-based framework to predict from STORMTIFF images, the localizations and their 3D clustering. This 
framework faciliates prediciton of otherwise missing point-cloud data for aligned STORMTIFF images.

Instructions:
To implement this framework follow the steps mentioned below and run the scripts in same order as listed under 'Main' section. The 'Supplimentary' section 
either contains scripts for modules used in scripts from 'Main' section or has scripts that may help in additional analysis but are not needed for primary 
implementation of the framework. The script filenames are prefixed with the folder path to store them.      

Step 1: Correct stormtiff image saturation.

        To facilitate the alignment process, the Stormtiff images are artifically saturated to some extent. Due to this saturation of most of the bright 
	pixels in clusters, the pixel intensity gradients are lost. To get rid of the saturation effects we introduce a soft-saturation alternative which 
	produces training images that look very similar to aligned stormtiff images on which the neural network model will be making predictions.

	Main:
	1) analysis_path\\make_data\\pixel_intensity_transformation.py - To introduce soft-saturation to raw stormtiff images and then do the Gaussian blurring.
	2) analysis_path\\make_data\\storm_save_out_no_transformation.py - (FIJI Macro) To convert images to uint8 format, to be run in FIJI.
	

Step 2: Prepare or edit a list of regions of interests (ROIs) from stormtiff image.
	
	A previously established STORM experiment analysis pipeline segments synapses from background in saturation-corrected stormtiff image and provides 
	a list of ROIs in it. These ROIs are a squared shaped regions within stormtiff images and contain a segmented synapse. The list of ROIs provides 
	coordinates of each ROI, ROI ID and Stormtiff image number. For further analysis, ROIs can be chosen from this extensive list in many different ways.        	


	Main:
	1) analysis_path\\make_data\\make_df_shuffled_tile_list.py - To randomly shuffle the list of ROIs.

	Supplimentary:
	1) analysis_path\\make_data\\make_df_mixed_tile_list.py - To make a list of first few fixed number of ROIs for each image number.

Step 3: Signal intensity vs localization density analysis.

	We plot nearest-neighbor (nn) averaged pixel intensity vs nearest-neighbor-averaged localization density which helps in initial estimation of 
	localization density from stormtiff image tile.

	Main:
	1) analysis_path\\signal_and_loc_density_analysis\\locs_per_storm_image_to_file.py - To collect ground-truth localizations from image tiles containing segmented synapses.
	2) analysis_path\\signal_and_loc_density_analysis\\full_pixel_list.py - To create a single pixel list of all the pixels from the clusters (connected components) in given list of ROIs.		            
	3) analysis_path\\signal_and_loc_density_analysis\\sig_intesity_vs_loc_density_segmented_img.py - To plot (for stormtiff image with segmented clusters) nn-averaged signal intensity vs nn-averaged number of localizations per pixel. Fit the plot with polynomial function and save the fit parameters.
	
	Supplimentary:
	1) analysis_path\\signal_and_loc_density_analysis\\sig_intesity_vs_loc_density.py - To plot nn-averaged signal intensity vs nn-averaged number of localizations per pixel. Fit the plot with polynomial function and save the fit parameters. 
        2) analysis_path\\signal_and_loc_density_analysis\\filtered_stormtiff_intesity_test.py - To count pixels with non-zero intensity.
	3) analysis_path\\signal_and_loc_density_analysis\\max_sig_test.py - To compute maximum pixel intensity signal for given stormtiff image or a section of the image.    

Step 4: Prepare training data for the network.

        Main:
	1) analysis_path\\make_data\\full_pixel_list.py - To create a single pixel list of all the pixels from the clusters (connected components) in given list of ROIs.
	2) analysis_path\\make_data\\locs_per_storm_image_to_file.py - To collect ground-truth localizations for ROIs.
	3) analysis_path\\make_data\\locs_estimate_per_storm_image_to_file.py - To collect estimated localizations for ROIs.  
        4) analysis_path\\make_data\\make_data.py - To make input-output pairs to train or validate the network.

	Supplimentary:
	1) analysis_path\\make_data\\get_list_empty_tiles.py - To get tile-list parameters and tile-number for empty tile(zero intensity everywhere).
        2) analysis_path\\make_data\\locs_estimate_per_storm_image.py - Module used for making estimations of localizations from stormtiff image tiles.
	3) analysis_path\\make_data\\locs_estimate_per_storm_image_2.py - Module used for making estimations of localizations (wihtout nn-averaging) from stormtiff image tiles.  
	4) analysis_path\\make_data\\locs_from_tiles.py - Module to create list of localizations and localization estimates from stormtiff image tile. 
	5) analysis_path\\make_data\\locs_from_tiles_tmp.py - Module to create list of localizations and localization estimates (without nn average) from stormtiff image tile. 
	6) analysis_path\\make_data\\locs_per_storm_image.py - Module to collect number of localizations per pixel in specified image tile.
	7) analysis_path\\make_data\\locs_per_tile_2.py - Module to create list of localizations and localization estimates from given tile of stormtiff image.                                      
	8) analysis_path\\make_data\\locs_per_tile_2_tmp.py - Module to create list of localizations and localization estimates (without nn average) from given tile of stormtiff image.
	9) analysis_path\\make_data\\make_tiles.py - Module to create image tiles from a subsection of stormtiff image.
	10) analysis_path\\make_data\\max_sig_test_storm_image.py - To compute maximum pixel intensity signal for given stormtiff image or a section of the image.
	11) analysis_path\\make_data\\max_sig_test_storm_image_list.py - To compute maximum pixel intensity signal for list of stormtiff images. 
	12) analysis_path\\make_data\\max_sig_test_storm_tile.py - To compute maximum pixel intensity signal for given stormtiff image tile.  
	13) analysis_path\\make_data\\model_input_output.py - Module to collect input-output pairs for training or validation data.
	14) analysis_path\\make_data\\tile_and_num_locs_plot.py - To plot estimated, predicted or ground-truth localizations found in tiles from given image section.

Step 5: Training and validation experiments.

        Main:
	1) analysis_path\\experiments\\experiment_train.py - To build the neural network model and train it.
	2) analysis_path\\experiments\\experiment_pred_to_file.py - To load previously trained model and test it on validation data.

	Supplimentary:
	1) analysis_path\\experiments\\get_data.py - Module to collect and combine the data from all data files in given path.
	2) analysis_path\\experiments\\locs_pred_random_plot.py - To plot the predicted localizations for a particular tile.
	3) analysis_path\\experiments\\models.py - Module with classes to build neural network models using sequential() module in keras.
	4) analysis_path\\experiments\\training_plot.py - To plot training history (training error vs epoch) for given experiment.

Step 5: Deploy the model to make localization predictions and perform 3D clustering analysis.

	Main:
	1) analysis_path\\3D_clustering_analysis\\remove_empty_tiles_tile_list.py - To remove empty ROIs from list, if present.
	2) analysis_path\\3D_clustering_analysis\\make_num_locs_estimate_per_tile_parallel.py - To make localization estimates on ROIs.
	3) analysis_path\\3D_clustering_analysis\\make_data.py - To make ROI image tiles as input to the model.
	4) analysis_path\\3D_clustering_analysis\\experiment_pred_to_file.py - To make localization predictions on ROIs.
	5) analysis_path\\3D_clustering_analysis\\nn_pred_to_locs3d.py - To convert model predictions into 3D pixel and cartesian coordinates.
	6) analysis_path\\3D_clustering_analysis\\remove_empty_locs3d_tile_list.py - To remove ROIs that have no localizations predicted.
	7) analysis_path\\3D_clustering_analysis\\tiles_sequence.py - To create sequence of overlapping tiles from consecutive image slices.
	8) analysis_path\\3D_clustering_analysis\\locs_3d_sequence.py - To collect 3D localizations from sequences of overlapping tiles.
	9) analysis_path\\3D_clustering_analysis\\dbscan.py - To perform 'DBSCAN' clustering analysis on 3D localization sequences.
	10) analysis_path\\3D_clustering_analysis\\get_cluster_properties.py - Get cluster properties for predicted clusters.

	Supplimentary:
	1) analysis_path\\3D_clustering_analysis\\cluster_properties_class.py - Module that has 'ClusterProperties' class.  
	2) analysis_path\\3D_clustering_analysis\\cluster_properties_plot.py - To plot histograms of different properties of clusters predicted by 'DBSCAN'
	3) analysis_path\\3D_clustering_analysis\\cluster_properties_to_csv.py - To write clusters properties to csv file.
	4) analysis_path\\3D_clustering_analysis\\cluster_randomization.py - To randomize the location of points in a cluster, to be used in determining average cluster size for random distribution.
	5) analysis_path\\3D_clustering_analysis\\dbscan_plot.py - To plot 'dbscan' cluster predictions for 2D or 3D array of localizations.
	6) analysis_path\\3D_clustering_analysis\\dbscan_plot_parallel.py - To plot 'dbscan' predictions for many sequences in parallel.
	7) analysis_path\\3D_clustering_analysis\\dbscan_plot_per_sequence.py - Module to plot 'dbscan' predictions.
	8) analysis_path\\3D_clustering_analysis\\experiment_pred_to_file_data_generator.py - To predict localizations from pixel intensities in stormtiff image tiles normalized with ImageDataGenerator module.
	9) analysis_path\\3D_clustering_analysis\\find_sequence_from_tile_ids.py - To get tile sequence files consisting of given tile ids.
	10) analysis_path\\3D_clustering_analysis\\get_data.py - Module to collect and combine the data from all the files in given path.
	11) analysis_path\\3D_clustering_analysis\\get_data_2.py - Module to collect and combine the data from all the files in given path (it collects files in the order their ROIs appear in tile-list).
	12) analysis_path\\3D_clustering_analysis\\get_list_empty_tiles.py - To get tile-list parameters and tile-number for empty tiles(zero intensity everywhere) among tiles created from tile-list.
	13) analysis_path\\3D_clustering_analysis\\locs_2d_3d_sequence_plot.py - To plot 2D or 3D array of localizations from 3D localization sequences.
	14) analysis_path\\3D_clustering_analysis\\locs_dict_to_locs3d.py - To convert the 2D localizations from dictionary to 3D localizations.
	15) analysis_path\\3D_clustering_analysis\\locs_estimate_per_storm_image.py - Module to get localization estimations in specified image tiles of stormtiff image list.
	16) analysis_path\\3D_clustering_analysis\\locs_estimate_per_storm_image_2.py - Module to get localization estimations (without nn averaging) in specified image tiles of stormtiff image list.
	17) analysis_path\\3D_clustering_analysis\\locs_from_tiles.py - Module to create list of localization estimates from stormtiff image tile.
	18) analysis_path\\3D_clustering_analysis\\locs_from_tiles_tmp.py - Module to create list of number of localization estimates (without nn average) from stormtiff image tile. 
	19) analysis_path\\3D_clustering_analysis\\locs_per_tile_2.py - Module to create list of localizations and localization estimates from given tile of stormtiff image.
	20) analysis_path\\3D_clustering_analysis\\locs_per_tile_2_tmp.py - Module to create list of number of localization estimates (without nn average) from stormtiff image tile. 
	21) analysis_path\\3D_clustering_analysis\\locs_pred_random_plot.py - To plot the predicted localizations for a particular tile.
	22) analysis_path\\3D_clustering_analysis\\make_num_locs_estimate_per_tile.py - To make estimated number of localizations file for each stormtiff tile. 
	23) analysis_path\\3D_clustering_analysis\\make_tiles_2.py - Alternate script (uses full dataframe) to create image tiles from a subsection of stromtiff image.
	24) analysis_path\\3D_clustering_analysis\\model_input_output.py - Module to collect input-output pairs for training or validation data.
	25) analysis_path\\3D_clustering_analysis\\num_locs_per_tile.py - Module to create number of localization estimates from given tile of stormtiff image.
	26) analysis_path\\3D_clustering_analysis\\random_cluster_sequence_plot.py - To plot 3D localizations in randomized clusters for 3d localization sequences.   
	27) analysis_path\\3D_clustering_analysis\\tile_and_num_locs_random_plot.py - To plot the predicted localizations for a particular tile. 
	28) analysis_path\\3D_clustering_analysis\\tile_list_df_test.py - To get information about list of tiles. 
	29) analysis_path\\3D_clustering_analysis\\tile_overlap_test.py - To check the tile-list for overlapping tiles with same image number.
	30) analysis_path\\3D_clustering_analysis\\tile_sequencer_class.py - Module that contains TileSequencer class that does not accept any external inputs.
	31) analysis_path\\3D_clustering_analysis\\tile_sequencer_class_new.py - Module that contains TileSequencer class that handles multiple overlap cases. 
	32) analysis_path\\3D_clustering_analysis\\tile_sequencer_class_old.py - Module that contains TileSequencer class.
	33) analysis_path\\3D_clustering_analysis\\tiles_sequence_test.py - To check if correct sequence of overlapping tiles in consecutive image slices is returned for a particular ROI from tiles-list provided.   
	34) analysis_path\\3D_clustering_analysis\\tiles_sequence_view_test.py - To view entries of tile sequence files. 
