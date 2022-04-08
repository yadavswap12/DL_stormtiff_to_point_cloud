"""
This script contains TileSequencer class.

This script is different from tile_sequencer_class.py in that, in case of multiple overlapping tiles from next image section, 
the TileSequencer() class now looks for the tile with maximum overlap.     

Swapnil 2/22
"""

import numpy as np
import pickle

class TileSequencer(object):
    """
    The superclass containing functions for making sequence of 
    overlapping tiles from a list of tiles in the form of a dataframe.

    """
    def __init__(self):
        super(TileSequencer, self).__init__()

    def tileSequence(self, tiles_df, tile_start_pix_y, tile_start_pix_x, tile_size, image_num, tile_num):
        """
        Find sequence of overlapping tiles for a tile with given parameters. 
        """
        
        # Get the index of the final row of the 'tiles_df' data frame.
        tiles_df_last_idx = tiles_df.last_valid_index()

        # Get the image number of the final row of the 'tiles_df' data frame.
        img_num_last = tiles_df.loc[tiles_df_last_idx, 'z(Num_image)']
        
        # Initialize tile number sequence list with first tile number.
        tile_num_seq = [tile_num]
        
        # remove the tile added to sequence from tile list.
        # Get the index of the tile to be removed from dataframe.
        drop_idx = tiles_df[tiles_df["Tile_ID"]==tile_num].index
        
        tiles_df.drop(labels=drop_idx, inplace=True)        
        
        # If the first tile is in last image of image slice sequence, then there is no sequence.
        if (image_num == img_num_last):

            # Set the sequence status (True if sequence is ongoing, False if sequence has come to an end).
            seq = False            
        
        else: 
            
            # Initialize the sequence status (True if sequence is ongoing, False if sequence has come to an end).
            seq = True
        
        while seq:
        
            # Create a dataframe for tiles with next image number.
            img_df = tiles_df[tiles_df["z(Num_image)"]==image_num+1]

            # Get the index of the final row of the 'tiles_df' data frame.
            tiles_df_last_idx = tiles_df.last_valid_index()

            # Get the image number of the final row of the 'tiles_df' data frame.
            img_num_last = tiles_df.loc[tiles_df_last_idx, 'z(Num_image)']
            
            # Initialize the minimum distance between overlapping tiles as some large number.
            # Choose this to set minimum overlap required for consecutive tiles to be part of sequence.           
            ovrlp_dist_min = 0.02*tile_size

            # Initialize overlap status to False.
            ovrlp_sts = False           
            
            # Iterate over all rows in dataframe with next image number.
            for idx in img_df.index:
            
                # Get the tile coordinates.
                tile_start_pix_y_next = img_df.loc[idx, 'y(row)']
                tile_start_pix_x_next = img_df.loc[idx, 'x(column)']
                # tile_num_next = img_df.loc[idx, 'Tile_ID']

                # Create tile overlap conditions. 
                cond1 = ((tile_start_pix_y+tile_size>tile_start_pix_y_next) & (tile_start_pix_y<=tile_start_pix_y_next)) & ((tile_start_pix_x+tile_size>tile_start_pix_x_next) & (tile_start_pix_x<=tile_start_pix_x_next))
                cond2 = ((tile_start_pix_y+tile_size>tile_start_pix_y_next) & (tile_start_pix_y<=tile_start_pix_y_next)) & ((tile_start_pix_x-tile_size<tile_start_pix_x_next) & (tile_start_pix_x>=tile_start_pix_x_next))
                cond3 = ((tile_start_pix_y-tile_size<tile_start_pix_y_next) & (tile_start_pix_y>=tile_start_pix_y_next)) & ((tile_start_pix_x-tile_size<tile_start_pix_x_next) & (tile_start_pix_x>=tile_start_pix_x_next))
                cond4 = ((tile_start_pix_y-tile_size<tile_start_pix_y_next) & (tile_start_pix_y>=tile_start_pix_y_next)) & ((tile_start_pix_x+tile_size>tile_start_pix_x_next) & (tile_start_pix_x<=tile_start_pix_x_next))                                    
                
                if (cond1 | cond2 | cond3 | cond4):
                                    
                    # Calculate the distance between overlapping tiles.
                    ovrlp_dist = ((tile_start_pix_y-tile_start_pix_y_next)**2 + (tile_start_pix_x-tile_start_pix_x_next)**2)**(0.5)
                    
                    if (ovrlp_dist < ovrlp_dist_min):
                    
                        # Update the minimum distance for overlapping tiles.
                        ovrlp_dist_min = ovrlp_dist 
                    
                        tile_num_next = img_df.loc[idx, 'Tile_ID']
                                        
                        # remove the tile added to sequence from tile list dataframe.
                        # Get the index of the tile to be removed from dataframe.
                        drop_idx = idx                                                                    
                        
                        # Set the overlap status to true
                        ovrlp_sts = True                                                

            if (ovrlp_sts):

                # Add next tile number to the sequence.
                tile_num_seq.append(tile_num_next)
                
                # Replace the old tile start coordinates with those of the tile added to sequence. 
                tile_start_pix_y = img_df.loc[drop_idx, 'y(row)']
                tile_start_pix_x = img_df.loc[drop_idx, 'x(column)']                
                
                # tiles_df.drop(labels=drop_idx, inplace=True)
                tiles_df.drop(labels=drop_idx, inplace=True)
                
                # Increment the image number to look for overlapping tiles in next image slice.
                image_num += 1                               
                
            # If no overlapping tile is found, end the sequence.
            if not ovrlp_sts:
                seq = False                
                
            # If tile sequence reaches till the final image in image slice sequence, end the tile sequence.
            elif ((ovrlp_sts == True) & (image_num == img_num_last)):
                seq = False            
        
        # Return the tupple of tile number sequence and updated tile-list dataframe.            
        return (tile_num_seq, tiles_df)
        
    def locs3dSequence(self, tile_num_seq, locs_3d_directory, mol_list):
        """
        Make sequence of 3d localizations for a given list with tile sequence. 
        """
        
        for j in range(len(tile_num_seq)):

            # Get the tile number from the sequence.
            tile_num = tile_num_seq[j]
                        
            # Get 3d localizations for given tile number.
            # Create a sequence filename.            
            if mol_list: locs3d_file_name = locs_3d_directory + "locs3d_molecule_list_cart_tile_" + str(tile_num) + ".data"
            
            else: locs3d_file_name = locs_3d_directory + "locs3d_pred_cart_tile_" + str(tile_num) + ".data"                        

            # Read from the localization file. 
            with open(locs3d_file_name, 'rb') as filehandle:
                locs3d = pickle.load(filehandle)        
            
            if (j == 0): locs_3d_seq = locs3d
                
            else: locs_3d_seq = np.concatenate((locs_3d_seq, locs3d)) 

        # Return the 3d localization sequence.            
        return locs_3d_seq
        
                    