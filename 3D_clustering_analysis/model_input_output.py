"""
This function collects tiles from makeTiles() and number of localizations per pixel from locsFromTiles() functions.

Swapnil 12/21
"""

from make_tiles import makeTiles

def modelInputOutput(storm_exp_directory, storm_exp_name, channel, tile_size, storm_image_scale, df, locsPerTile2, locsPerTile2Tmp, sorted):
    
    tile_input = []      
        
    # Make individual tiles from stormtiff image. 
    total_tiles = makeTiles(storm_exp_directory, storm_exp_name, tile_size, df, tile_input, sorted)
    
    # # Make localization files for individual tiles             
    # total_loc_files = locsFromTiles(storm_exp_directory, storm_exp_name, tile_size, storm_image_scale, df, locsPerTile2, sorted)            
    # # total_loc_files = locsFromTilesTmp(storm_exp_directory, storm_exp_name, tile_size, storm_image_scale, df, locsPerTile2Tmp, filtered)

    total_loc_files = None
        
    return (total_tiles, total_loc_files)        
            
            
            
            
            
            
        
        
        

    

