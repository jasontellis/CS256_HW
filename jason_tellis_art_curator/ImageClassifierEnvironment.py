import os

from ImageClassifierAgent import ImageClassifierAgent
from Trainer import Trainer


class ImageClassifierEnvironment:
    def __init__(self):
        self.imagePath = ""
        self.agent = ImageClassifierAgent(self)
        self.k = 10
        self.isContinue = "y"

    def percept(self):

        while self.isContinue.lower() == "y":
            fileList = []

            self.imagePath = raw_input("\nGreetings " + os.getlogin() + "! Which image woud you like to classify?"
                                                                        "\n(Please enter path to JPEG image  "
                                                                        "\ne.g. /Users/jasontellis/Desktop/testImage.jpg"
                                                                        "\nor directory containing images to be classified"
                                                                        "\ne.g. /Users/jasontellis/Desktop/)\n")

            if os.path.isfile(self.imagePath):
                fileList.append(self.imagePath)
            elif os.path.isdir(self.imagePath):
                fileList = Trainer.__getFileList__(self.imagePath)
            else:
                print ("Uh oh! The path you entered seems to be invalid. Please try again")
                continue

            self.k = raw_input("\nHow many neighbors would you like to poll for classfication?"
                               "\nPlease enter an odd number between 1 & 20\n")

            if isinstance((int)(self.k), int) and (int)(self.k) % 2 != 0:
                self.k = (int)(self.k)
            else:
                print("The no. of neighbors you entered does not seem to be a valid odd number. Please try again")
                continue

            print ("Classifying " + str(len(fileList)) + " images")
            for file in fileList:
                self.agent.sensor(file, self.k)
                print(file + " is a " + self.response)

            self.isContinue = raw_input("\nDo you wish to continue? Press Y to continue, any other key to exit").lower()

        print ("Goodbye...")
        quit()

    def setResponseFromAgent(self, response):
        self.response = response
