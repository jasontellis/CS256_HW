import itertools
import logging
import os

from ImageVectorExtractor import ImageVectorExtractor
from LookUpTableRow import LookUpTableRow


class Trainer:
    """
    The training component of the ImageClassifierAgent
    
    
    """
    CLASS_HEADSHOT = "headshot"
    CLASS_LANDSCAPE = "landscape"
    imageClasses = [CLASS_HEADSHOT, CLASS_LANDSCAPE]
    trainingDirectory = os.getcwd()
    headshotsDirectory = os.path.join(trainingDirectory, CLASS_HEADSHOT)
    landscapesDirectory = os.path.join(trainingDirectory, CLASS_LANDSCAPE)

    def __init__(self):
        self.classCounts = {}
        self.lookUpTable = []
        self.__buildLookUpTable__()

    def getLookUpTable(self):
        return self.lookUpTable

    @staticmethod
    def incrementImageClassCount(classCounts={}, imageClass=""):
        """

        :param classCounts:
        :param imageClass:
        :return:
        """

        if classCounts.has_key(imageClass):
            classCounts[imageClass] += 1
        else:
            classCounts[imageClass] = 1
        return classCounts

    def getClassDataCounts(self):
        """
        Returns dictionary with imageClasses and no. of images associated with the classes

        :return:
        """
        return self.classCounts

    def getSampleCount(self):
        return len(self.lookUpTable)

    def getImageClassForRow(self, rowIndex):
        """

        :param rowIndex:
        :return:
        """
        imageClass = ""
        if 0 <= rowIndex and rowIndex < len(self.lookUpTable):
            imageClass = self.lookUpTable[rowIndex].imageClass

        return imageClass

    @staticmethod
    def __getFileList__(directory=os.path.join(os.getcwd(), CLASS_LANDSCAPE)):
        """

        :param directory: File Path
        :return: Returns a list of filenames of .JPG images in a directory
        """

        fileList = [os.path.join(directory, file) for file in os.listdir(directory) if
                    os.path.isfile(os.path.join(directory, file)) and (file.endswith(".jpg") or file.endswith(".jpeg"))]
        return fileList

    def __buildLookUpTable__(self):
        """
        :return: None
        """

        lookUpTable = []
        logging.info("Training...")
        headShotsFileList = Trainer.__getFileList__(Trainer.headshotsDirectory)
        logging.info(str(len(headShotsFileList)) + " files found of class " + Trainer.CLASS_HEADSHOT)
        landscapesFileList = Trainer.__getFileList__(Trainer.landscapesDirectory)
        logging.info(str(len(landscapesFileList)) + " files found of class " + Trainer.CLASS_LANDSCAPE)

        for (headshotFile, landscapeFile) in itertools.izip(headShotsFileList, landscapesFileList):
            self.__addFileToLookUpTable__(headshotFile, Trainer.CLASS_HEADSHOT)
            self.__addFileToLookUpTable__(landscapeFile, Trainer.CLASS_LANDSCAPE)
            # headShotFileImageVector = ImageVectorExtractor.extractVector(headshotFile)
            # landscapeFileImageVector = ImageVectorExtractor.extractVector(landscapeFile)
            #
            # headshotLookUpTableRow = LookUpTableRow(headshotFile, headShotFileImageVector, Trainer.CLASS_HEADSHOT)
            # landscapeLookUpTableRow = LookUpTableRow(landscapeFile, landscapeFileImageVector, Trainer.CLASS_LANDSCAPE)
            #
            # lookUpTable.append(headshotLookUpTableRow)
            # Trainer.incrementImageClassCount(self.classCounts, Trainer.CLASS_HEADSHOT)
            #
            # lookUpTable.append(landscapeLookUpTableRow)
            # Trainer.incrementImageClassCount(self.classCounts, Trainer.CLASS_LANDSCAPE)

    def __addFileToLookUpTable__(self, imageFileName="", imageClass=""):
        imageVector = ImageVectorExtractor.extractVector(imageFileName)
        lookUpTableRow = LookUpTableRow(imageFileName, imageVector, imageClass)
        self.lookUpTable.append(lookUpTableRow)
        Trainer.incrementImageClassCount(self.classCounts, imageClass)

# trainer = Trainer()
# print trainer.getLookUpTable()
