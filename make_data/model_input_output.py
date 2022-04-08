"""
This function collects tiles from makeTiles() and number of localizations per pixel from locsFromTiles() functions.

Swapnil 12/21
"""

from make_tiles import makeTiles
from locs_from_tiles import locsFromTiles
from locs_from_tiles_tmp import locsFromTilesTmp

def modelInputOutput(storm_exp_directory, storm_exp_name, channel, tile_size, max_processes, storm_image_scale, tiles_df, locsPerTile2, locsPerTile2Tmp, uint8, roi, clust_pix_list_full_file):
    
    tile_input = []
    num_locs_output = []
    num_locs_est_lin_fit_output = []
    num_locs_est_quad_fit_output = []           
        
    # Make individual tiles from stormtiff image. 
    total_tiles = makeTiles(storm_exp_directory, storm_exp_name, tile_size, tiles_df, tile_input, uint8, roi)
    
    # Make localization files for individual tiles.             
    total_loc_files = locsFromTiles(storm_exp_directory, storm_exp_name, tile_size, num_locs_output, num_locs_est_lin_fit_output, num_locs_est_quad_fit_output, max_processes, storm_image_scale, tiles_df, locsPerTile2, uint8, roi, clust_pix_list_full_file)            
    # total_loc_files = locsFromTilesTmp(storm_exp_directory, storm_exp_name, tile_size, max_processes, storm_image_scale, tiles_df, locsPerTile2Tmp, uint8, roi)            
        
    return (total_tiles, total_loc_files)
    # return total_tiles        
    
            
            
            
            
            
            
        
        
        

    

