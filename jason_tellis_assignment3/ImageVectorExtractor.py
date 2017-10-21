import itertools
# from pylab import *
import logging

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import numpy as np
from PIL import Image


class ImageVectorExtractor:
    @staticmethod
    def extractVector(imageFileName="./landscape/white.jpg"):
        """
        Extracts a normalized histogram i.e. count of each value of RGB is divided by the
        no. of pixels and grouped in bands of 16 to get a vector with 48 features

        :return: List Normalized Histogram
        """

        # if os.path.isfile(imageFileName):
        image = Image.open(imageFileName)

        histogram = np.array(image.histogram())
        pixelCount = (float)(image.size[0] * image.size[1])

        normalizedHistogram = histogram / pixelCount  # Normalize frequencies by dividing by pixel count
        logging.debug("\nNormalized Histogram: ")
        logging.debug(normalizedHistogram)

        prevIndex = 0
        groupedHistogram = []
        for index in range(16, len(normalizedHistogram) + 16, 16):
            # Add normalized counts of 16 colors at a time to reduce vector dimensions from 768 to 48
            groupedHistogram.append(sum(normalizedHistogram[prevIndex: index]))
            prevIndex = index

        normalizedHistogram = groupedHistogram
        # [sum(normalizedHistogram[:256]), sum(normalizedHistogram[256:512]),sum(normalizedHistogram[512:768]) ]

        return normalizedHistogram

        # else:
        #     logging.error("I'm sorry, the file path you entered seems to be invalid")

    @staticmethod
    def __calculateDistance__(lookUpTableVector, inputVector):
        """

        :param lookUpTableVector:
        :param inputVector:
        :return:
        """

        manhattanDistance = 0.0
        for (lookUpVectorAttributeValue, inputVectorAttributeValue) in itertools.izip(lookUpTableVector, inputVector):
            manhattanDistance += abs(lookUpVectorAttributeValue - inputVectorAttributeValue)

        return manhattanDistance
