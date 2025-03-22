"""
Script to get properties clusters predicted by dbscan algorithm on 2d(x,y) tiles of localizations.

Swapnil 08/24
"""

import glob
import pickle
import os

from cluster_properties_class import ClusterProperties

# Are you sequencing 3d localizations from molecule list or from neural network prediction?
mol_list = False

# Are you doing control analysis for randomized clusters?
randm = False

# # Set path to data files.
expfolder = "C:\\Users\\Swapnil\\Research\\loc_prediction\\storm\\project_17\\"

exp_name = 'experiment_12'
# exp_name = 'experiment_9'
# exp_name = 'experiment_10'
# exp_name = 'experiment_11'


# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

accuracy_directory = expfolder + "Clustering_accuracy\\"

accuracy_experiment_directory = accuracy_directory + exp_name + '\\'

dbscan_directory = accuracy_experiment_directory + "dbscan_output\\"

if mol_list:
    locs_2d_directory = accuracy_experiment_directory + "locs2d_mol_list\\"
    
    # Get list of tiles with no localizations.
    tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_" + exp_name + ".data"     
    

else: 
    locs_2d_directory = accuracy_experiment_directory + "locs2d_predictions\\"
    
    # Get list of tiles with no localizations.
    tile_list_no_locs2d_file = accuracy_experiment_directory + "tile_list_no_locs2d_pred_" + exp_name + ".data" 

with open(tile_list_no_locs2d_file, 'rb') as filehandle:
    tile_list_no_locs2d = pickle.load(filehandle)        

# Get dbscan parameters.

# For 647 channel.
eps = 2.0
min_samples = 8

# # For 750 channel.
# eps = 2.0
# min_samples = 16

# Set directory for dbscan output of 2d localizations.
if mol_list: 
    if randm:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_random_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    
    else:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
 
else: 
    if randm:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_random_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     
    
    else:
        dbscan_seq_directory = dbscan_directory + "dbscan_output_tiles_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"     

# Create directory to save plots.
if not os.path.exists(dbscan_seq_directory + "stats\\" ):
    os.mkdir(dbscan_seq_directory + "stats\\" )

stats_directory =  dbscan_seq_directory + "stats\\"

# Remove previously present files in the folder.
files = glob.glob(stats_directory + "*.data") 
for file in files:
    os.remove(file)
    
    
# files = glob.glob(locs_2d_directory + "*pixel*")
files = glob.glob(dbscan_seq_directory + "*.data") 

# Initialize tile counter.
tl_ct = 1 

# Initialize cluster property value.
clust_sz = 0
clust_ar = 0
clust_vl = 0    

# Initialize cluster property counter.
clust_count = 0          

# Iterate over sequences.
for file in files:

    locs_tile_file_name = file
    
    # Get the sequence number present in the filename.
    tile_num = int(locs_tile_file_name.split("_")[-1][:-5])

    if tile_num not in tile_list_no_locs2d:        

        # Get 2d localizations directory.
        if mol_list: 
        
            locs2d_file_name = locs_2d_directory + "locs2d_molecule_list_pixel_tile_" + str(tile_num) + ".data"            

        else: 
        
            locs2d_file_name = locs_2d_directory + "locs2d_pred_pixel_tile_" + str(tile_num) + ".data"             
                             
        with open(locs2d_file_name, 'rb') as filehandle:
            locs_2d = pickle.load(filehandle)
           
        # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs_arr. 
        locs_2d[:,[0,1]] = locs_2d[:,[1,0]]



        # Get the DBSCAN result filename for given 3d localization sequence.
        db_out_file_name = dbscan_seq_directory + "dbscan_out_tile_" + str(tile_num) + ".data"           
        
        # Read from the file. 
        with open(db_out_file_name, 'rb') as filehandle:
            db = pickle.load(filehandle)

        # Set the filename for cluster stats from given 3d localization sequence.
        cl_stats_file_name = stats_directory + "cluster_stats_tile_" + str(tile_num) + ".data" 

        # Create an empty list for cluster stats.
        cl_stats = []

        # Get the cluster properties from dbscan output and add them to cluster stat list.
        # Get the number of clusters predicted.
        num_cl = ClusterProperties(db).numOfClusters()
        cl_stats.append(num_cl)
        
        # Get the number of noise points predicted.
        num_ns = ClusterProperties(db).numOfNoise()
        cl_stats.append(num_ns)         

        # Get tupple of dictionaries (with unique cluster labels as key) for different cluster stats.
        dicts = ClusterProperties(db).clusterStats(locs_2d)
        cl_stats.append(dicts)

        # Writting the cluster stats list to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
        with open(cl_stats_file_name, 'wb') as filehandle:
            # store the data as binary data stream.
            pickle.dump(cl_stats, filehandle)         
        
        # Get dictionary for cluster centers.
        cl_cntr_dict = dicts[0]  

        # Get dictionary for cluster sizes.
        cl_sz_dict = dicts[1]

        # Get dictionary for cluster areas.
        cl_ar_dict = dicts[2] 

        # Get dictionary for cluster volumes.
        cl_vl_dict = dicts[3]

        # Iterate over all values in dictionary.
        for key in cl_sz_dict.keys():
            clust_sz += cl_sz_dict[key]
            clust_ar += cl_ar_dict[key]
            clust_vl += cl_vl_dict[key]            
            clust_count += 1
            
        if (tl_ct%100 == 0):
            print("{}th sequence is analyzed." .format(tl_ct))

    tl_ct += 1            



clust_sz_avg = clust_sz/clust_count
clust_ar_avg = clust_ar/clust_count       
clust_vl_avg = clust_vl/clust_count

print("average cluster size: {}, average cluster area: {}, average cluster volume: {}" .format(clust_sz_avg, clust_ar_avg, clust_vl_avg))            

            
       
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



    



        
        

