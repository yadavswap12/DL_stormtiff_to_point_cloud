"""
Script to plot 'dbscan' predictions for 3d(x,y,z) array of localizations. 
If cluster_3d is True then script gives 3d plot, if False, then script gives 2d plot (top view of 3d plot). 

This script creates parallel processes for plots.    

Swapnil 3/22
"""

import glob
import os
import multiprocessing
from multiprocessing import Semaphore

from dbscan_plot_per_sequence import dbPlotPerSeq

if __name__ == "__main__": 

    # Are you ploting 2d or 3d data?
    cluster_3d = True

    # Are you ploting 3d localizations from molecule list or from neural network prediction?
    mol_list = False

    # Do you want to save the plot or just view it?
    save = True

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

    # Create directory to save plots.
    if not os.path.exists(dbscan_seq_directory + "plots\\" ):
        os.mkdir(dbscan_seq_directory + "plots\\" )

    plots_directory =  dbscan_seq_directory + "plots\\"

    # # Remove previously present files. 
    # files = glob.glob(plots_directory + "*.jpg")
    # for f in files:
        # os.remove(f)       

    # # Set starting tile and end tile to get localizations from tile sequence for 2D clustering.
    # tile_start = 1
    # tile_end = 1

    # # Or give tile sequence number and list of tile numbers in that tile sequence.
    # # tile_seq = 2
    # # tile_list = [2, 252, 408]
    # tile_seq = 1
    # tile_list = [1]

    seq_start = 377 
    seq_end = 377
        
    # Get number of 3d dbscan result files present in dbscan_seq_directory.
    total_seqs = len(glob.glob(dbscan_seq_directory + "*.data"))

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

    # Set Maximum number of parallel processes.
    # max_processes = 50
    max_processes = multiprocessing.cpu_count() - 1        
    
    # Setup process queue.
    jobs = []
    # process_count = 0
    # results = multiprocessing.Queue()
    sema = Semaphore(max_processes)              

    # Iterate over sequences.
    for i in range(1, total_seqs+1):
    # for i in range(seq_start, seq_end+1):
    
        # Get the DBSCAN result filename for given 3d localization sequence.
        db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(i) + ".data"        

        # Get the 3d localization sequence filename.
        if mol_list: 
            if randm:
                locs_seq_file_name = locs_sequences_directory + "random_cluster_mol_list_sequence_" + str(i) + ".data"
            
            else:
                locs_seq_file_name = locs_sequences_directory + "locs3d_molecule_list_sequence_" + str(i) + ".data"

        else: 
            if randm:
                locs_seq_file_name = locs_sequences_directory + "random_cluster_sequence_" + str(i) + ".data" 
            
            else:
                locs_seq_file_name = locs_sequences_directory + "locs3d_pred_sequence_" + str(i) + ".data"

        # Once max_processes are running, block the main process.
        # the main process will continue only after one or more 
        # previously created processes complete.
        sema.acquire()

        # Assign process for each tile.        
        # Process for localization estimation with nearest neighbor averaging. 
        process = multiprocessing.Process(target = dbPlotPerSeq, args=(cluster_3d, save, i, locs_seq_file_name ,db_out_file_name, plots_directory, sema))        
            
        jobs.append(process)
        process.start()
        
    # Block the execution of next lines in the main script until all the process are terminated.    
    for job in jobs:
        
        job.join()                






            
    

    



        
        

