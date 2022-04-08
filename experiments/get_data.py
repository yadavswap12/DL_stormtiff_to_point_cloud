"""
Function to get and combine the data from all data files in given path.
Returns a list with each element of list being data from single file in given file path.

data_path - full path of directory where data is located.

data_type = A string argument specifying the data type.

Swapnil 10/21
"""

import glob
import pickle
import re

def getData(data_path, data_type):

    if (data_type == "tiles"):
    
        data = []

        # Initialize tile-id list.
        tile_id_list = []
        
        # Get number of files present in given path.
        total_files = len(glob.glob(data_path + "*.data"))
        
        # Get files in sorted order according to number in filename.
        tile_files = sorted(glob.glob1(data_path, "*.data"), key=lambda x:float(re.findall("(\d+)",x)[0]))        
            
        for tile_file in tile_files:
                    
            # Read from the file and save it to an array 
            with open(data_path + tile_file, 'rb') as filehandle:
                tile = pickle.load(filehandle)
            
            # Get the number present in the filename.
            tile_id = re.search(r'\d+', tile_file).group(0)                
            
            data.append(tile)
            tile_id_list.append(tile_id)
            
            
    elif (data_type == "num_locs"):

        data = []
        
        # Initialize tile-id list.
        tile_id_list = []        
        
        # Get number of files present in given path.
        total_files = len(glob.glob(data_path + "storm_num_locs_tile_" + "*.data"))
        
        # Get files in sorted order according to number in filename.
        num_locs_tile_files = sorted(glob.glob1(data_path, "storm_num_locs_tile_" + "*.data"), key=lambda x:float(re.findall("(\d+)",x)[0]))     
            
        for num_locs_tile_file in num_locs_tile_files:
                    
            # Read from the file and save it to an array 
            with open(data_path + num_locs_tile_file, 'rb') as filehandle:
                num_locs_tile = pickle.load(filehandle)
                
            # Get the number present in the filename.
            tile_id = re.search(r'\d+', num_locs_tile_file).group(0)                    
            
            data.append(num_locs_tile)
            tile_id_list.append(tile_id)            
            
    elif (data_type == "num_locs_est_lin_fit"):

        data = []
        
        # Initialize tile-id list.
        tile_id_list = []        
        
        # Get number of files present in given path.
        total_files = len(glob.glob(data_path + "storm_num_locs_est_lin_fit_tile_" + "*.data"))
        
        # Get files in sorted order according to number in filename.
        num_locs_est_tile_files = sorted(glob.glob1(data_path, "storm_num_locs_est_lin_fit_tile_" + "*.data"), key=lambda x:float(re.findall("(\d+)",x)[0]))      
            
        for num_locs_est_tile_file in num_locs_est_tile_files:
                    
            # Read from the file and save it to an array 
            with open(data_path + num_locs_est_tile_file, 'rb') as filehandle:
                num_locs_est_tile = pickle.load(filehandle)
               
            # Get the number present in the filename.
            tile_id = re.search(r'\d+', num_locs_est_tile_file).group(0)                   
            
            data.append(num_locs_est_tile)
            tile_id_list.append(tile_id)                        

    elif (data_type == "num_locs_est_quad_fit"):

        data = []
        
        # Initialize tile-id list.
        tile_id_list = []          
        
        # Get number of files present in given path.
        total_files = len(glob.glob(data_path + "storm_num_locs_est_quad_fit_tile_" + "*.data"))
        
        # Get files in sorted order according to number in filename.
        num_locs_est_tile_files = sorted(glob.glob1(data_path, "storm_num_locs_est_quad_fit_tile_" + "*.data"), key=lambda x:float(re.findall("(\d+)",x)[0]))        

        for num_locs_est_tile_file in num_locs_est_tile_files:
        
            # Read from the file and save it to an array 
            with open(data_path + num_locs_est_tile_file, 'rb') as filehandle:
                num_locs_est_tile = pickle.load(filehandle)
                
            # Get the number present in the filename.
            tile_id = re.search(r'\d+', num_locs_est_tile_file).group(0)                  
            
            data.append(num_locs_est_tile)
            tile_id_list.append(tile_id)                                    
            
    return data, tile_id_list         
    
        