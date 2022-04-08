"""
Script to get properties clusters predicted by dbscan algorithm on 3d(x,y,z) sequences of localizations.

Swapnil 2/22
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
expfolder = "analysis_path\\experiment_name\\"

# storm_exp_name = "561storm"
storm_exp_name = "647storm"
# storm_exp_name = "750storm"

storm_exp_directory = expfolder + storm_exp_name + "\\"

experiment_directory = storm_exp_directory + "experiment1\\"

# Get dbscan parameters.
eps = 22.0
min_samples = 6

# Set directory for dbscan output of 3d localization sequences.
if mol_list: 
    if randm: 
        dbscan_seq_directory = storm_exp_directory + "dbscan_output_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    
    else:
        dbscan_seq_directory = storm_exp_directory + "dbscan_output_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
 
else: 
    if randm:
        dbscan_seq_directory = experiment_directory + "dbscan_output_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    
    else:
        dbscan_seq_directory = experiment_directory + "dbscan_output_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 

# If does not exist, create new directory for cluster stats from 3d localization sequences.
if mol_list:
    if randm:
        if not os.path.exists(storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = storm_exp_directory + "cluster_stats_random_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

    else:
        if not os.path.exists(storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = storm_exp_directory + "cluster_stats_sequences_mol_list_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 
    

else:
    if randm:
        if not os.path.exists(experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = experiment_directory + "cluster_stats_random_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"
    
    
    else:
        if not os.path.exists(experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"):
            os.mkdir(experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\")
        
        cl_stats_directory = experiment_directory + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"

# Remove previously present files in the folder.
files = glob.glob(cl_stats_directory + "*.data") 
for file in files:
    os.remove(file)

# Set starting sequence and end sequence to get localizations from tile sequence for 3D clustering.
seq_start = 1
seq_end = 1

# Get localizations sequences directory.
if mol_list: 
    if randm:
        locs_sequences_directory = storm_exp_directory + "random_cluster_sequences_mol_list\\"
    
    else:
        locs_sequences_directory = storm_exp_directory + "locs3d_molecule_list_sequences\\"
        
    
else: 
    if randm:
        locs_sequences_directory = experiment_directory + "random_cluster_sequences\\"        
    
    else:
        locs_sequences_directory = experiment_directory + "locs3d_pred_sequences\\"

# Get number of 3d localization sequences present in locs_sequences_directory.
total_seqs = len(glob.glob(locs_sequences_directory + "*.data"))

files = glob.glob(locs_sequences_directory + "*.data")        

# Initialize cluster property value.
clust_sz = 0
clust_ar = 0
clust_vl = 0    

# Initialize cluster property counter.
clust_count = 0    

# Iterate over sequences.
for file in files:
    
    # Get the 3d localization sequence filename.            
    locs_seq_file_name = file

    # Get the sequence number present in the filename.
    seq = int(locs_seq_file_name.split("_")[-1][:-5])             
    
    # Set the DBSCAN result filename for given 3d localization sequence.
    db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(seq) + ".data"   

    # Set the filename for cluster stats from given 3d localization sequence.
    cl_stats_file_name = cl_stats_directory + "cluster_stats_sequence_" + str(seq) + ".data"           
    
    # Read from the file. 
    with open(locs_seq_file_name, 'rb') as filehandle:
        locs3d_seq_arr = pickle.load(filehandle)

    # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
    locs3d_seq_arr[:,[0,1]] = locs3d_seq_arr[:,[1,0]]
   
    # Read dbscan output from the file. 
    with open(db_out_file_name, 'rb') as filehandle:
        db = pickle.load(filehandle)

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
    dicts = ClusterProperties(db).clusterStats(locs3d_seq_arr)
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
        
    if (seq%100 == 0):
        print("{}th sequence is analyzed." .format(seq))               
        
clust_sz_avg = clust_sz/clust_count
clust_ar_avg = clust_ar/clust_count       
clust_vl_avg = clust_vl/clust_count

print("average cluster size: {}, average cluster area: {}, average cluster volume: {}" .format(clust_sz_avg, clust_ar_avg, clust_vl_avg))

    



        
        

