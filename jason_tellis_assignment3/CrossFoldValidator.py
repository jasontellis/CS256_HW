import random

from AccuracyPlotter import AccuracyPlotter
from ImageClassifierAgent import ImageClassifierAgent
from  Trainer import Trainer


class CrossFoldValidator:
    """
    Implements cross-fold validation for the K-NN Image Classifier for values of k upto maxK

    """

    def __init__(self, foldCount=3, maxK=10):
        random.seed(0)
        self.maxK = maxK
        self.folds = []
        self.agent = ImageClassifierAgent(self)
        self.imageClass = ""
        trainer = Trainer()
        self.lookUpTable = trainer.getLookUpTable()
        self.sampleCount = trainer.getSampleCount()
        self.folded = {}
        self.foldCount = foldCount
        self.foldElementCount = self.sampleCount / self.foldCount  # Count of elements in each fold
        self.foldCounts = {}
        self.sampleDataClassCounts = trainer.getClassDataCounts()
        self.__createFolds__()

    def validate(self):
        """
        :return:
        """
        kList = []
        accuraciesForK = []
        accuracyList = []

        for k_knn in range(1, self.maxK, 2):  # For odd values of K from KNN
            accuraciesForK = []
            accuracyForK = 0.0
            print ("\n************************************************")
            print("\nFor k = " + str(k_knn))

            for foldIndexStart in range(self.foldCount):

                validationFoldIndex = (foldIndexStart + self.foldCount - 1) % self.foldCount
                validationDataTable = self.folds[validationFoldIndex]
                trainingLookUpTable = []
                # logging.info("Validation Fold Index " + str(validationFoldIndex + 1))

                for trainingFoldNextIndex in range(
                                self.foldCount - 1):  # For foldCount - 1 folds of data as training data

                    trainingDataFoldIndex = (foldIndexStart + trainingFoldNextIndex) % self.foldCount
                    # logging.info("Training Fold Index " + str(trainingDataFoldIndex + 1))
                    trainingLookUpTable.extend(self.folds[trainingDataFoldIndex])
                self.agent.setLookUpTable(trainingLookUpTable)

                foldAccuracy = 0.0
                for validationDataRow in validationDataTable:
                    self.agent.sensor(validationDataRow.imageFileName, k_knn)
                    # logging.info("Filename: "+validationDataRow.imageFileName+ " Predicted Class: "+ self.imageClass+" Actual Class: "+validationDataRow.imageClass)
                    if self.imageClass == validationDataRow.imageClass:
                        foldAccuracy += 1

                foldAccuracy /= (float)(len(validationDataTable))
                foldAccuracy = round(foldAccuracy, 4) * 100

                print ("Accuracy for fold " + str(validationFoldIndex + 1) + ": " + str(foldAccuracy) + "\n")
                accuraciesForK.append(foldAccuracy)
                accuracyForK += foldAccuracy

            accuracyForK /= (float)(self.foldCount)
            accuracyForK = round(accuracyForK, 4)
            accuraciesForK.append(accuracyForK)
            print ("Average Accuracy for k = " + str(k_knn) + " : " + str(accuracyForK))
            kList.append(k_knn)
            accuracyList.append(accuraciesForK)

        AccuracyPlotter.plot(kList, accuracyList)

    def setResponseFromAgent(self, imageClass):
        """

        :param imageClass:
        :return:
        """
        self.imageClass = imageClass

    def __createFolds__(self):
        """
        :return:
        """
        print(str(len(self.lookUpTable)) + " elements found for cross-folding")
        for foldIndex in range(self.foldCount):
            print("\nCreating fold " + str(foldIndex + 1) + "....")

            foldClassCounts = {}  # Tracks count of classes in each fold to ensure balanced folds
            fold = set({})

            while len(fold) < self.foldElementCount:
                foldRowIndex = self.__selectRandomLookUpTableRow__(foldClassCounts)
                foldRow = self.lookUpTable[foldRowIndex]
                foldClassCounts = Trainer.incrementImageClassCount(foldClassCounts, foldRow.imageClass)
                fold.add(foldRow)
                self.folded[str(foldRowIndex)] = True
            print("Fold " + str(foldIndex + 1) + " created with " + str(len(fold)) + " elements")
            self.folds.append(fold)

    def __selectRandomLookUpTableRow__(self, foldClassCounts):
        """
        Selects a random LookUpTable row without replacement while checking
         1. Row has not already been selected
         2. The count of rows for each class in the fold is balanced


        :param foldClassCounts: Count of elements of each class in current fold
        :return: Row Index from LookUpTable
        """

        selected = None

        while selected is None:

            rowIndex = random.randint(0, self.sampleCount - 1)  # Randomly select a row
            if self.__isRowUnselected__(rowIndex):  # Check that row has not already been selected in some fold

                imageClass = self.lookUpTable[rowIndex].imageClass
                if self.__isBalanced__(imageClass,
                                       foldClassCounts):  # Check fold will not be unbalanced by adding row of this class to it
                    selected = rowIndex

        return selected

    def __isRowUnselected__(self, rowIndex):
        """
        Checks whether randomly selected row has already been included in some fold

        :param rowIndex: roewIndex of LookUp Table
        :return: True if row has not already been selected
        """
        rowUnselected = True
        if self.folded.has_key(str(rowIndex)):
            rowUnselected = False

        return rowUnselected

    def __isBalanced__(self, imageClass, foldClassCounts):
        """
        Checks whether adding an element having given class will unbalance the  fold
        by comparing proportion of images of given class in lookuptable to proportion of images of given class
        in fold

        :param self:
        :return:
        """

        isBalanced = True
        if foldClassCounts.has_key(imageClass) and foldClassCounts[imageClass] / self.foldElementCount >= \
                        self.sampleDataClassCounts[imageClass] / self.foldCount:
            isBalanced = False
        return isBalanced


maxK = raw_input("Please enter maximum value of 'K' upto which cross validation should be run e.g. 10\n")
try:
    maxK = (int)(maxK)
except:
    print("Invalid value for K, Default of 10 will be assumed")
    maxK = 10

cfv = CrossFoldValidator(3, maxK)
cfv.validate()
