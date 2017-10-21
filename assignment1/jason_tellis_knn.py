# -*- coding: utf-8 -*-
'''

K-NN Algorithm implementation for CS 256-02 by Jason Tellis


Citation:

This algorithm has been implemented using the reference at
https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
and
https://matplotlib.org/users/pyplot_tutorial.html
'''

# %%
import csv
import os
import operator
import matplotlib.pyplot as plt
import numpy as np

'''
The Environment Class
'''


class Environment:
    def __init__(self, k, trainingFilename, testFilename, attributeCount):

        self.k = k
        self.trainingFilename = trainingFilename
        self.testFilename = testFilename
        self.attributeCount = attributeCount

        self.trainingDataSet = self.__readFile__(trainingFilename)
        self.testDataSet = self.__readFile__(testFilename)

    # Read file and return dataSet as a list
    def __readFile__(self, filename):

        dataSetStartIndex = self.attributeCount + 5  #attributeCount + 5 lines contain metadata about dataset

        with open(filename, 'rb') as dataFile:
            dataRows = csv.reader(dataFile)

            # Truncate first (attributeCount + 5) lines from file containing dataset metadata
            dataSet = list(dataRows)[dataSetStartIndex:]



            #           Convert string attribute values from file to float
            for dataRow in dataSet:
                for attributeIndex in range(self.attributeCount):
                    dataRow[attributeIndex] = float(dataRow[attributeIndex])

            return dataSet

    # Gets accuracy in % for given k and training-test file pair
    def getAccuracy(self):

        correctCounter = 0  # Initialize correct predictions to 0
        testDataCount = len(self.testDataSet)
        agent = Agent(self)  # Initialize agent with Environment knowledge
        for testRow in self.testDataSet:
            predictedClass = agent.sensor(testRow)
            # print("\nActual Class: "+testRow[-1]+" Predicted Class "+predictedClass)

            # If predicted class = actual class, increment correct coiunter
            if testRow[-1] == predictedClass:
                correctCounter += 1

        accuracy = (correctCounter / float(testDataCount)) * 100.0
        return round(accuracy,2)


class Agent:
    def __init__(self, environment):
        self.env = environment

    #    Sensor senses environment iand gets k
    def sensor(self, testRow):
        return self.__actuator__(testRow)

    #   Get k nearest neighbors based on Euclidean distance
    def __function__(self, testRow):

        distances = []  # Initialize list of distances to be empty

        #       For given test row, iterate over entire training set to compute Euclidean distance and store
        #       along with corresponding training data row
        for trainingDataRow in self.env.trainingDataSet:
            dist = self.__euclideanDistance__(trainingDataRow, testRow)
            distances.append((trainingDataRow, dist))

        distances.sort(key=operator.itemgetter(1))  # Sort Array of distances in ascending order of distance
        neighbors = []  # Initialize neighbours
        for distancesIndex in range(self.env.k):  # Save first 'k' nearest neighbors to neighbors
            neighbors.append(distances[distancesIndex][0])
            # print(repr(testRow)+" neighbor: "+repr(distances[distancesIndex][0])+repr(distances[distancesIndex][1])+"\n")
        return neighbors

    #   Return class of testRow
    def __actuator__(self, testRow):
        neighbors = self.__function__(testRow)

        classVotes = {}  # Define classVotes as a blank hash

        for neighborRow in neighbors:  # Iterate over each of the k nerest neighbours and compute count of each class
            response = neighborRow[-1]  # Set response to last attribute of neighbor i.e. class of neighbor

            # If class of neighbor present in hash, increment count of class, else set count of class to 1
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1

        # Sort class counts in descending order and return class with max count as class
        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
        classification = sortedVotes[0][0]
        return classification

    #    Compute Euclidean distance between trainingRow & testRow having attributeCount attributes
    def __euclideanDistance__(self, trainingRow, testRow):

        # Initialize distance to zero
        distance = 0.0

        # Distance is sum of squares of differences of attributes; root not computed to optimize unnecessary operation
        for attributeIndex in range(self.env.attributeCount):
            distance += pow( (testRow[attributeIndex] - trainingRow[attributeIndex]), 2)
            # print("Distance: "+str(distance)+"\n")
        # print(repr(trainingRow)+" - "+repr(testRow)+" = "+str(distance)+" \n")
        return distance


# Function to start program execution
def main():

    foldCount = 10  # Count of folds
    kStart = 1  # Start Value of k
    kEnd = 10  # Maximum value of K
    kStepSize = 2  # Only odd 'k' to be considered
    filenamePrefix = "banana-10-"
    testFileNameSuffix = "tst.dat"
    trainingFileNameSuffix = "tra.dat"
    avgAccuracyList = []
    kList = []

    # filepath = "/Users/jasontellis/Downloads/banana-10-fold/"
    filepath = raw_input("Kindly enter directory path containing banana dataset including trailing '/' "
                         "(Example: '/Users/jasontellis/Downloads/banana-10-fold/' ) :"
                         "\n")

    attributeCount = int(raw_input("Kindly enter count of attributes in file excluding class: (Example: For banana data set 2) \n"))



    for k in range(kStart, kEnd + 1, kStepSize):  # Iterate for odd values of 'k' between 1-10 as even k may cause classification tie
        totalAccuracy = 0.0
        fileAccuracies = []
        print("\n****************For k= " + str(k) + "***************")

        for fileIndex in range(1, (foldCount + 1)):
            trainingFilename = filepath + filenamePrefix + str(fileIndex) + trainingFileNameSuffix
            testFilename = filepath + filenamePrefix + str(fileIndex) + testFileNameSuffix
            # print("\nTraining Filename: " + trainingFilename+ " Test Filename: " + testFilename )

            env = Environment(k, trainingFilename, testFilename, attributeCount)
            accuracy = env.getAccuracy()
            fileAccuracies.append(accuracy)
            totalAccuracy += accuracy

            # print("\nAccuracy for k = " + str(k) + " : " + str(accuracy))
        print("\n Accuracies for the 10 files when k = " + str(k) + " : " + repr(fileAccuracies))
        avgAccuracy = (totalAccuracy / 10.0)
        kList.append(k)
        avgAccuracyList.append(avgAccuracy)
        print ("\n\n Average accuracy for k= " + str(k) + ": " + str(avgAccuracy))
        print("***************End of k= " + str(k) + "******************\n\n")

    __plotAccuracyGraph__(kList, avgAccuracyList)



#   Takes 2 lists containing k and corresponding prediction accuracy as input and plots graph
def __plotAccuracyGraph__(kList, accuracyList):

    fig = plt.figure(figsize=(11,8))
    plt.axis([0,10, 0, 100.0])
    plt.xlabel("k (nearest neighbors)")
    plt.ylabel("Accuracy in %")
    plt.xticks(np.arange(0, 10, 1.0))
    plt.yticks(np.arange(0, 110.0, 10.0))
    plt.title('Accuracy % vs k for k Nearest Neighbours on Banana dataset')
    plt.plot(kList, accuracyList)
    plt.show()

main()
# %%
