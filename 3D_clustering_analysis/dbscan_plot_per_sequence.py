"""
Function to plot 'dbscan' predictions for 3d(x,y,z) array of localizations from particular sequence.         

Swapnil 3/22
"""

import numpy as np
import pickle
import matplotlib.pyplot as plt
import multiprocessing

def dbPlotPerSeq(cluster_3d, save, i, locs_seq_file_name ,db_out_file_name, plots_directory, sema):
    
    # Process details.
    curr_process = multiprocessing.current_process()
    # parent_process = multiprocessing.parent_process()
    print("Process Name : {} (Daemon : {}), Process Identifier : {}\n".format(curr_process.name, curr_process.daemon, curr_process.pid))

    # Read from the file. 
    with open(locs_seq_file_name, 'rb') as filehandle:
        locs3d_seq_arr = pickle.load(filehandle)

    # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
    locs3d_seq_arr[:,[0,1]] = locs3d_seq_arr[:,[1,0]]    
    
    # Read from the file. 
    with open(db_out_file_name, 'rb') as filehandle:
        db = pickle.load(filehandle)      
    
    # Masking the core samples.
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    labels = db.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    # Initialize cluster count for filtered clusters.
    clst_ct = 0

    # # Print results.
    # print(" There are {} estimated number of clusters for tile sequence {}." .format(n_clusters_, i))
    # print("There are {} estimated number of noise points for tile sequence {}." .format(n_noise_, i))        
    # # print("Estimated number of clusters: %d" % n_clusters_)
    # # print("Estimated number of noise points: %d" % n_noise_)
    # # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    # # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    # # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    # # print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
    # # print(
        # # "Adjusted Mutual Information: %0.3f"
        # # % metrics.adjusted_mutual_info_score(labels_true, labels)
    # # )
    # # print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(locs_arr, labels))

    if cluster_3d:

        # Plot results.
        # Plot x,y,z coordinates for clusters.                
        ax = plt.axes(projection='3d')        
        
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k
            noise_mask = labels == -1
            
            # Set the value for cluster size filter.
            # The size limit for clusters is calculated from average size of clusters for random control experiment. 
            clst_sz_fltr = 6
            
            # If cluster size is greater than the cluster size filter.
            if (sum(class_member_mask) > clst_sz_fltr):

                # Update cluster count.
                clst_ct += 1             

                # # For plotting only core member points.            
                # xy = locs3d_seq_arr[class_member_mask & core_samples_mask]
                
                # # For plotting all class member points including noise points.
                # xy = locs3d_seq_arr[class_member_mask]

                # For plotting all class member points without noise points.
                xy = locs3d_seq_arr[class_member_mask & ~noise_mask]            
                            
                # Plot x,y,z coordinates for clusters.                
                # ax = plt.axes(projection='3d')
                ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple(col), linewidth=0.5, alpha=1) 

                # # Emphasize individual clusters with black markers.
                # if (clst_ct == 20): 
                    # # Plot x,y,z coordinates for clusters.                
                    # # ax = plt.axes(projection='3d')
                    # ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple([0, 0, 0, 1]), linewidth=1.5, alpha=1)

                # else:
                    # # Plot x,y,z coordinates for clusters.                
                    # # ax = plt.axes(projection='3d')
                    # ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c=tuple(col), linewidth=0.5, alpha=1)                
                
                # # Plot x,y coordinates for clusters.    
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 1],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # # markersize=14,
                    # markersize=4,
                # )    
                    
                # # Plot x,z coordinates for clusters.    
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 2],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # # markersize=14,
                    # markersize=4,        
                # )


                # xy = locs_arr[class_member_mask & ~core_samples_mask]
                # plt.plot(
                    # xy[:, 0],
                    # xy[:, 1],
                    # "o",
                    # markerfacecolor=tuple(col),
                    # markeredgecolor="k",
                    # markersize=6,
                # )
                # plt.gca().invert_yaxis()
                # plt.gca().xaxis.tick_top()
                # plt.gca().set_aspect('equal', adjustable='box')    

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}, # of clusters: {}, molecule_list" .format(i, clst_ct))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        file_name = "dbscan_out_sequence_{}_3d.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)            
        
        else:
            plt.show()

        if (i%10 == 0):
            print("{}th sequence is analyzed." .format(i))     

    else:
    
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k
            noise_mask = labels == -1                        

            # # For plotting only core member points.            
            # xy = locs3d_seq_arr[class_member_mask & core_samples_mask]
            
            # # For plotting all class member points.
            # xy = locs3d_seq_arr[class_member_mask]

            # For plotting all class member points without noise points.
            xy = locs3d_seq_arr[class_member_mask & ~noise_mask]             
            
            # xy = locs3d_seq_arr[class_member_mask]    # Applying only class member mask.                  
            
            # Plot x,y coordinates for clusters.    
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                # markersize=14,
                markersize=4,
            )    
                
            # # Plot x,z coordinates for clusters.    
            # plt.plot(
                # xy[:, 0],
                # xy[:, 2],
                # "o",
                # markerfacecolor=tuple(col),
                # markeredgecolor="k",
                # # markersize=14,
                # markersize=4,        
            # )


            # xy = locs_arr[class_member_mask & ~core_samples_mask]
            # plt.plot(
                # xy[:, 0],
                # xy[:, 1],
                # "o",
                # markerfacecolor=tuple(col),
                # markeredgecolor="k",
                # markersize=6,
            # )
            # plt.gca().invert_yaxis()
            # plt.gca().xaxis.tick_top()
            # plt.gca().set_aspect('equal', adjustable='box')    

        plt.gca().invert_yaxis()
        # plt.gca().xaxis.tick_top()
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Sequence: {}, # of clusters: {}, molecule_list" .format(i, n_clusters_))        
        # plt.title("Estimated number of clusters: %d" % n_clusters_)
        file_name = "dbscan_out_sequence_{}_2d_core.jpg" .format(i)
        
        if save:
            # plt.savefig(locs_pred_directory + file_name, dpi = 300)
            plt.savefig(plots_directory + file_name)            
        
        plt.show()                       
        
    # `release` will add 1 to `sema`, allowing other 
    # processes blocked on it to continue
    sema.release()         



            
    

    



        
        

