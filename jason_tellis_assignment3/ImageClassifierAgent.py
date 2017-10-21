import numpy as np

from ImageVectorExtractor import ImageVectorExtractor
from Trainer import Trainer


class ImageClassifierAgent:
    def __init__(self, environment=None):
        self.img = ""
        self.k = 3
        self.trainer = Trainer()
        self.environment = environment
        self.lookUpTable = []
        self.path = ""
        self.lookUpTable = self.trainer.getLookUpTable()

    def sensor(self, imageFileName, k=3):
        self.k = k
        self.__function__(imageFileName)

    def __function__(self, imageFileName):
        self.__classifyUsingKNN__(imageFileName)

    def __classifyUsingKNN__(self, imageFileName):
        """
        Run K-nearest neighbors to predict class of given image

        :return:
        """

        distanceTable = self.__getKNN__(imageFileName)
        imageClass = self.__pollClassFromKNN(distanceTable)
        self.__actuator__(imageClass)

    def __getKNN__(self, imageFileName):
        """
        Returns table of 'k' nearest neighbors and their associated classes

        :param imageFileName:
        :return: Table of image classes with distances from input Image
        """
        dtype = [('imageClass', 'S10'), ('distance', float)]
        distanceTable = []
        inputImageVector = ImageVectorExtractor.extractVector(imageFileName)
        for lookupTableRow in self.lookUpTable:
            distance = ImageVectorExtractor.__calculateDistance__(lookupTableRow.imageVector, inputImageVector)
            disanceTableRow = (lookupTableRow.imageClass, distance)
            distanceTable.append(disanceTableRow)

        distanceTable = np.array(distanceTable, dtype=dtype)
        distanceTable.sort(order="distance")  # Sort LookUpTable in ascending order of distances

        distanceTable = distanceTable[:self.k]  # Return K Nearest Neighbors based on ascending order of distances

        return distanceTable

    def __pollClassFromKNN(self, distanceTable):
        """
        Polls K-Nearest Neighbors to classify given image

        :param distanceTable: Table of K Nearest neighbors
        :return: Predicted class of Image
        """
        headshotsCount = 0
        for distanceTableRow in distanceTable:
            if distanceTableRow[0] == Trainer.CLASS_HEADSHOT:
                headshotsCount += 1
        landscapesCount = self.k - headshotsCount

        imageClass = Trainer.CLASS_HEADSHOT

        if landscapesCount > headshotsCount:
            imageClass = Trainer.CLASS_LANDSCAPE

        return imageClass

    def __actuator__(self, imageClass):
        if self.environment is not None:
            self.environment.setResponseFromAgent(imageClass)

    def setLookUpTable(self, lookUpTable):
        self.lookUpTable = lookUpTable
