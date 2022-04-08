"""
Function to collect and combine the data from all the files in given path.
Returns a list with each element of list being data from single file in given file path.

data_path - full path of directory where data is located.

data_type = A string argument specifying the data type.
data_type = "tiles" for image tile data.
data_type = "locs" for localization data.

This script is different from get_data.py in that, instead of collecting files in ascending order of number 
in the filename, it collects files in the order their ROIs appear in tile-list.   

Swapnil 2/22
"""

import pickle

def getData(data_path, data_type, df):

    if (data_type == "tiles"):
    
        data = []
            
        # Iterate over all rows in dataframe.
        for idx in df.index:
            
            # Get the tile ID.
            tile_id = df.loc[idx, 'Tile_ID'] 

            tile_file = data_path + "tile_" + str(tile_id) + ".data" 

            # Read from the file and save it to an array 
            with open(tile_file, 'rb') as filehandle:
                tile = pickle.load(filehandle)                
            
            data.append(tile)                           
            
            
    elif (data_type == "num_locs"):

        data = []
            
        # Iterate over all rows in dataframe.
        for idx in df.index:
            
            # Get the tile ID.
            tile_id = df.loc[idx, 'Tile_ID'] 

            num_locs_tile_file = data_path + "storm_num_locs_tile_" + str(tile_id) + ".data"    

            # Read from the file and save it to an array 
            with open(num_locs_tile_file, 'rb') as filehandle:
                num_locs_tile = pickle.load(filehandle)                
            
            data.append(num_locs_tile)                        
            
    elif (data_type == "num_locs_est_lin_fit"):

        data = []
            
        # Iterate over all rows in dataframe.
        for idx in df.index:
            
            # Get the tile ID.
            tile_id = df.loc[idx, 'Tile_ID'] 

            num_locs_est_tile_file = data_path + "storm_num_locs_est_lin_fit_tile_" + str(tile_id) + ".data"  
                
            # Read from the file and save it to an array 
            with open(num_locs_est_tile_file, 'rb') as filehandle:
                num_locs_est_tile = pickle.load(filehandle)            
        
            data.append(num_locs_est_tile)

    elif (data_type == "num_locs_est_quad_fit"):

        data = []
            
        # Iterate over all rows in dataframe.
        for idx in df.index:
            
            # Get the tile ID.
            tile_id = df.loc[idx, 'Tile_ID'] 

            num_locs_est_tile_file = data_path + "storm_num_locs_est_quad_fit_tile_" + str(tile_id) + ".data"  
                
            # Read from the file and save it to an array 
            with open(num_locs_est_tile_file, 'rb') as filehandle:
                num_locs_est_tile = pickle.load(filehandle)            
        
            data.append(num_locs_est_tile)
            
    return data        
    
        