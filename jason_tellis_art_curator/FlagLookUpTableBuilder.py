import os

from Trainer import Trainer


class FlagLookUpTableBuilder(Trainer):
    """
    Build LookUpTable for Flags Clustering

    """

    def __buildLookUpTable__(self):
        for flagFile in self.flagFileList:
            self.__addFileToLookUpTable__(flagFile, "")

    def __init__(self):
        self.classCounts = {}
        self.lookUpTable = []
        self.flagsDirectory = os.path.join(os.getcwd(), 'flags')
        self.flagFileList = self.__getFileList__(self.flagsDirectory)
        self.__buildLookUpTable__()
