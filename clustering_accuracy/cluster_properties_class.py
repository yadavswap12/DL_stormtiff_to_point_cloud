"""
Script for ClusterProperties class to compute different properties of 
clusters of localizations.     

Swapnil 1/22
"""

import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d

class ClusterProperties(object):
    """
    The superclass containing functions to compute different properties of
    cluster of localizations.

    """
    def __init__(self, db):
        super(ClusterProperties, self).__init__()
        self.db = db

        # Get cluster labels.
        self.labels = self.db.labels_        

    def numOfClusters(self):
        """
        Get the number of clusters predicted by dbscan. 
        """
        
        # # Get cluster labels.
        # self.labels = self.db.labels_

        # Number of clusters in labels, ignoring noise if present.
        num_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)            
        
        # Return the number of clusters.            
        return (num_clusters)
        
    def numOfNoise(self):
        """
        Get the number of Noise points (not part of any cluster) predicted by dbscan. 
        """
        
        # # Get cluster labels.
        # self.labels = self.db.labels_

        # Number of noise points in labels.
        num_noise = list(self.labels).count(-1)
        
        # Return the number of clusters.            
        return (num_noise)        
        
    def clusterStats(self, locs3d_seq_arr):
        """
        Get dictionaries for cluster centers, cluster size and cluster volume. 
        Dictionaries have cluster labels as keys. 
        """
        
        # Initialize dictionaries.
        clust_cent_dict = {}
        clust_size_dict = {}
        clust_area_dict = {}                
        clust_vol_dict = {}        

        # Get unique labels for each cluster and noise points
        unique_labels = set(self.labels)

        # Iterate over all unique cluster labels except noise label.
        # for l in unique_labels:        
        for l in [i for i in unique_labels if i!=-1]:        
            # Get a mask for cluster with given label.
            clust_mask = (self.labels == l)

            # Get coordinates of points with given cluster label.   
            clust_xyz = locs3d_seq_arr[clust_mask]
            
            # Get cluster center.
            clust_cen = np.mean(clust_xyz, axis=0)

            # Include cluster center in dictionary with cluster label as key.
            # clust_cent_dict["l"] = clust_cen
            clust_cent_dict[l] = clust_cen            

            # Get cluster size.
            clust_sz = len(clust_xyz)

            # Include cluster size in dictionary with cluster label as key.
            # clust_size_dict["l"] = clust_sz
            clust_size_dict[l] = clust_sz            

            # hull calculation needs more than 3 cluster points.
            if (len(clust_xyz)>3):
                # Find convex hull for given cluster.
                hull = ConvexHull(clust_xyz)

                # Find surface area of convex hull.
                clust_hull_area = hull.area
                
                # Find volume of convex hull.
                clust_hull_vol = hull.volume

            else:
                # Set surface area of convex hull to zero.            
                clust_hull_area = 0

                # Set volume of convex hull to zero.                            
                clust_hull_vol = 0                            
            
            # Include cluster area in dictionary with cluster label as key.
            # clust_area_dict["l"] = clust_hull_area
            clust_area_dict[l] = clust_hull_area                                    

            # Include cluster volume in dictionary with cluster label as key.
            # clust_vol_dict["l"] = clust_hull_vol
            clust_vol_dict[l] = clust_hull_vol                        

        # Return the 3d localization sequence.            
        return clust_cent_dict, clust_size_dict, clust_area_dict, clust_vol_dict            

        
                    