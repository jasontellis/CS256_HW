import numpy as np

from ImageVectorExtractor import ImageVectorExtractor


class DistanceMatrix:
    def __init__(self, dataTable):
        """
        :param dataTable: Data table to be used to compute distance matrix
        """
        self.dataTable = dataTable
        self.matrix = []
        dtype = [('rowIndex', int), ('colIndex', int), ('distance', float)]  # Data Type of tuple in Distance Matrix
        self.nextMinPairIndex = 0
        tempMatrix = []
        self.mergedClustersList = []
        self.mergedCluster = set()
        self.pointCount = len(dataTable)

        tempMatrix = self.__computeDistanceMatrix__()

        # Sort distance matrix in ascending order
        self.matrix = np.array(tempMatrix, dtype=dtype)
        self.matrix = np.sort(self.matrix, order='distance')

    def __computeDistanceMatrix__(self):
        """
        Computes distance matrix for data table
        :return: DistanceMatrix
        """

        distanceMatrix = []

        for (rowIndex, outerDataRow) in enumerate(self.dataTable):

            for (colIndex, innerDataRow) in enumerate(self.dataTable):
                if colIndex >= rowIndex:  # Compute distances only along lower diagonal
                    break
                distance = ImageVectorExtractor.__calculateDistance__(outerDataRow.imageVector,
                                                                      innerDataRow.imageVector)
                distanceMatrix.append(
                    (rowIndex, colIndex, distance))  # Store distances between points( x, y) as (x,y, distance)

        return distanceMatrix

    def getClusterOfPoint(self, point):
        """
        If point is already part of a cluster, return the cluster else return point

        :param point: Data Point
        :return: Cluster to which point belongs
        """
        cluster = point
        for mergedCluster in self.mergedClustersList:
            if point & mergedCluster[2]:  # If point is part of a cluster
                cluster = cluster | mergedCluster[2]  # Return the cluster
        return cluster

    def merge(self, cluster1, cluster2, distance):
        """

        :param cluster1: Cluster1 to be merged
        :param cluster2: Cluster2 to be merged
        :param distance: Distance between clusters
        :return:
        """

        cluster1ToBeMerged = set([cluster1])
        cluster2ToBeMerged = set([cluster2]) - cluster1ToBeMerged

        cluster1ToBeMerged = self.getClusterOfPoint(cluster1ToBeMerged)
        cluster2ToBeMerged = self.getClusterOfPoint(cluster2ToBeMerged)

        if cluster1ToBeMerged != cluster2ToBeMerged:
            self.mergedCluster = cluster1ToBeMerged | cluster2ToBeMerged
            mergedClustersRow = [cluster1ToBeMerged, cluster2ToBeMerged, self.mergedCluster, distance]
            self.mergedClustersList.append(mergedClustersRow)

    def hasUnclusteredPairs(self):
        """
        Returns true if all pairs are not yet clustered

        :return: True if all pairs are not clustered
        """
        hasUnclusteredPairs = False

        if len(self.mergedCluster) < self.pointCount:
            hasUnclusteredPairs = True
        return hasUnclusteredPairs

    def printClusters(self, level=1):
        """
        Prints clusters mereged at specified level

        :param level: Level of merging at which clusters are to be printed
        :return: None
        """

        if len(self.mergedClustersList) >= level:
            index = -1 * level
            clusterToPrint = self.mergedClustersList[index]
            self.printCluster(clusterToPrint, 0)
            self.printCluster(clusterToPrint, 1)

    def printCluster(self, cluster, clusterIndex):
        """

        :param cluster: Cluster to be printed
        :param clusterIndex: Index of the cluster
        :return:
        """

        print ("\n************************************************************")
        print ("Cluster" + str(clusterIndex + 1) + " with " + str(len(cluster[clusterIndex])) + " members")
        print ("************************************************************\n")
        for member in cluster[clusterIndex]:
            print(self.dataTable[member].imageFileName)

    def getNextMinPair(self):
        """

        :return: Returns a pair of clusters from distance table with minimum distances
        """
        nextMinPair = None
        if self.nextMinPairIndex < len(self.matrix):
            nextMinPair = self.matrix[self.nextMinPairIndex]
            self.nextMinPairIndex += 1

        return nextMinPair


class HierarchicalClusteringAgent:
    def __init__(self, dataTable):
        print ("Clustering " + str(len(dataTable)) + " files using Single Link Hierarchical Clustering")
        self.distanceMatrix = DistanceMatrix(dataTable)
        while self.distanceMatrix.hasUnclusteredPairs():
            pair = self.distanceMatrix.getNextMinPair()
            self.distanceMatrix.merge(pair[0], pair[1], pair[2])

        self.distanceMatrix.printClusters(1)
