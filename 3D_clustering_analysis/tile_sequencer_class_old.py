"""
This script contains TileSequencer class.     

Swapnil 1/22
"""

import numpy as np
import pickle

class TileSequencer(object):
    """
    The superclass containing functions for making sequence of 
    overlapping tiles from a list of tiles in the form of dataframe.

    """
    def __init__(self, tiles_df):
        super(TileSequencer, self).__init__()
        self.tiles_df = tiles_df

    def tileSequence(self, tile_start_pix_y, tile_start_pix_x, tile_size, image_num, tile_num):
        """
        Find sequence of overlapping tiles for a tile with given parameters. 
        """
        # Initialize tile number sequence list with first tile number.
        tile_num_seq = [tile_num]
        
        # remove the tile added to sequence from tile list.
        # Get the index of the tile to be removed from dataframe.
        drop_idx = self.tiles_df[self.tiles_df["tile_num"]==tile_num].index
        
        self.tiles_df.drop(labels=drop_idx, inplace=True)        
        
        # Initialize the sequence status (True if sequence is ongoing, False if sequence has come to an end).
        seq = True
        
        while seq:
        
            # Create a dataframe for tiles with next image number.
            img_df = self.tiles_df[self.tiles_df["Num_image"]==image_num+1]        

            # Iterate over all rows in dataframe with next image number.
            for idx in img_df.index:
            
                # Get the tile coordinates.
                tile_start_pix_y_next = img_df.loc[idx, 'y(row)']
                tile_start_pix_x_next = img_df.loc[idx, 'x(column)']
                tile_num_next = img_df.loc[idx, 'tile_num']

                # Create tile overlap conditions. 
                cond1 = (tile_start_pix_y+tile_size>tile_start_pix_y_next) & (tile_start_pix_x+tile_size>tile_start_pix_x_next)
                cond2 = (tile_start_pix_y+tile_size>tile_start_pix_y_next) & (tile_start_pix_x-tile_size<tile_start_pix_x_next)
                cond3 = (tile_start_pix_y-tile_size<tile_start_pix_y_next) & (tile_start_pix_x-tile_size<tile_start_pix_x_next)
                cond4 = (tile_start_pix_y-tile_size<tile_start_pix_y_next) & (tile_start_pix_x+tile_size>tile_start_pix_x_next)                                    
                
                if(cond1 | cond2 | cond3 | cond4):
                
                    # Add next tile number to the sequence.
                    tile_num_seq.append(tile_num_next)
                    
                    # remove the tile added to sequence from tile list dataframe.
                    # Get the index of the tile to be removed from dataframe.
                    drop_idx = self.tiles_df[self.tiles_df["tile_num"]==tile_num_next].index
                    
                    self.tiles_df.drop(labels=drop_idx, inplace=True)
                    
                    # Replace the old tile start coordinates with those of the tile added to sequence. 
                    tile_start_pix_y = tile_start_pix_y_next
                    tile_start_pix_x = tile_start_pix_x_next
                    
                    # Increment the image number to look for overlapping tiles in next image slice.
                    image_num += 1
                    
                    # Break the loop as the overlapping tile is found. A tile in sequence can overlap only with single tile from next slice. 
                    break
            
            # If no overlapping tile is found break the sequence. 
            seq = False        
        
        # Return the tupple of tile number sequence and updated tile-list dataframe.            
        return (tile_num_seq, self.tiles_df)
        
    def locs3dSequence(self, tile_num_seq, locs_3d_directory):
        """
        Make sequence of 3d localizations for a given list with tile sequence. 
        """
        
        for j in len(tile_num_seq):

            # Get the tile number from the sequence.
            tile_num = tile_num_seq[j]
            
            # Get 3d localizations for given tile number.
            # Create a sequence filename.
            locs3d_file_name = locs_3d_directory + "locs3d_pred_tile_" + str(tile_num) + ".data"

            # Read from the localization file. 
            with open(locs3d_file_name, 'rb') as filehandle:
                locs3d = pickle.load(filehandle)        
            
            if (j == 0): locs_3d_seq = locs3d
                
            else: locs_3d_seq = np.concatenate((locs_3d_seq, locs3d)) 

        # Return the 3d localization sequence.            
        return locs_3d_seq            

        
                    