import random

import numpy as np

from ImageVectorExtractor import ImageVectorExtractor


class Cluster:
    def __init__(self, centroid):
        self.centroid = centroid
        self.updatedCentroid = np.zeros(len(centroid))
        self.members = []
        self.sse = 0.0

    def addMember(self, element, distance=0.0):
        """
        Adds element with distance from centroid = 'distance' to cluster
        and updates the sum of squared errors

        :param element: Element to be added to cluster
        :param distance: Distance of element from centroid
        :return: None
        """
        self.members.append(element)

        # Updated centroid is the vector sum of all memeber vectors and is calculated every time a member is added
        # In the recompute step, this vector is simply divided by no. of members to get the mean which will be set as new centroid

        self.updatedCentroid += element.imageVector
        self.sse += distance ** 2

    def getDistanceFromCentroid(self, element):
        """
        Returns distance of given element from cluster's centroid

        :param element: element to be compared with cluster centroid
        :return: Distance of element from cluster's centroid
        """
        distance = ImageVectorExtractor.__calculateDistance__(self.centroid, element.imageVector)
        return distance

    def reComputeCentroid(self):
        self.centroid = self.updatedCentroid / len(self.members)  # Divide vector sum by length of members to get mean
        self.members = []
        self.sse = 0
        self.updatedCentroid = np.zeros(len(self.centroid))


class KMeansClusteringAgent:
    def __init__(self, imageTable=[], clusterCount=2):
        self.clusters = []
        random.seed(0)
        self.imageTable = imageTable
        dataCount = len(self.imageTable) - 1

        print("\nClassifying " + str(len(self.imageTable)) + " images....")

        # Randomly select two centroids
        for index in range(clusterCount):
            selectedCentroidIndex = random.randint(0, dataCount)
            print("Randomly Selected Centroid Index: " + str(selectedCentroidIndex) + " " + imageTable[
                selectedCentroidIndex].imageFileName)
            self.clusters.append(Cluster(imageTable[selectedCentroidIndex].imageVector))

        self.cluster(self.imageTable)

    def getClusters(self):
        return self.clusters

    def cluster(self, imageTable):

        currentSSE = np.inf
        previousSSE = np.inf
        iterations = 0
        while True:
            iterations += 1
            currentSSE = 0
            for image in imageTable:

                closestCluster = None
                distanceFromClosestCluster = np.inf  # Initialize to infinity
                for cluster in self.clusters:

                    distanceFromCluster = cluster.getDistanceFromCentroid(image)

                    if distanceFromCluster < distanceFromClosestCluster:
                        distanceFromClosestCluster = distanceFromCluster
                        closestCluster = cluster

                closestCluster.addMember(image, distanceFromClosestCluster)
                currentSSE += closestCluster.sse

            if previousSSE <= currentSSE:
                break
            previousSSE = currentSSE
            for cluster in self.clusters:
                cluster.reComputeCentroid()

        # self.output()
        return self.clusters

    def output(self):
        for (clusterIndex, cluster) in enumerate(self.clusters):
            print("\n")
            print ("Cluster#: " + str(clusterIndex + 1))
            for member in cluster.members:
                print("\n" + member.imageFileName)
