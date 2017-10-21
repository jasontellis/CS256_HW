"""Job search agent using K-NN for CS256-02

Author: Jason Tellis

Prints a list of 'k' specified jobs based on following user input:
 1. 'K'
 2. Job Keywords
 3. Job Location
__
"""
import argparse
import os
import sys
import webbrowser

from jason_tellis_job_agent import Agent


class Cluster:
    mode = {"a", "b", "c", "d"}
    members = [{"a"},
               {"b"}
               ]#List of member vectors
    distanceOfAllMembersFromMode = 0.0

    def __init__(self):


    def __init__(self, mode = {}, members = [{}]):
        self.mode = mode
        self.members = members

    def __getDistance__(self, vector = {}):
        return Agent.__calculateDistance__(self.mode, vector)

    def addMember(self, vector = {}):
        self.members.add(vector)

    def reComputeMode(self):

        memberSet = ()
        for member in self.members:
            memberSet = set(self.members.keys())
            modeSet = modeSet.intersection(memberSet)


class Environment:
    k = 10
    searchString = "Computer Science"
    resultsJobs = []
    agent = None
    ifContinue = "y"

    def __init__(self):
        CHOICE_SEARCH = 1
        CHOICE_CLUSTER = 2
        self.__buildCLI__()
        self.ifContinue = "y"
        self.choice = CHOICE_SEARCH
        self.k = 10
        self.searchString = "Computer Science"
        self.agent = Agent()
        self.resultsJobs = []

    def main(self):
        while (self.ifContinue.lower() == 'y'):
            self.resultsJobs = []
            self.searchString = raw_input("\nGreetings " + os.getlogin() + "! \nWhat are you looking for? ")
            # self.choice = raw_input("\nEnter any key to search or enter 2 to tocluster")
            # if self.choice != self.choice.s
            self.k = int(raw_input("How many results would you like to see? "))
            self.agent.sensor(self)
            self.__printJobs__()

            self.ifContinue = raw_input("\nDo you wish to continue? y to continue, press any other key to exit: ")
        print ("Bye, have a nice day!")
        quit()

    def setResultFromAgent(self, resultJobs):

        self.resultsJobs = resultJobs

    def getK(self):
        return self.k

    def getSearchString(self):
        return self.searchString

    def cluster(self):
        """

        :return:
        """

        jobs = self.resultsJobs[:15]
        clusterCount = 3
        clusteringIterationCount = 10
        clusterCentres= []
        jobMemberOf = []  # Membership matrix
        distance = []  # Distance matrix
        clusterIndex = 0
        jobIndex = 0

        # Initialize 3 centroids to be vectors of first 3 jobs returned by agent
        if len(self.resultsJobs) >=3:
            clusterCentres[0]["vector"] = self.resultsJobs[0]["vector"]
            clusterCentres[1]["vector"] = self.resultsJobs[1]["vector"]
            clusterCentres[2]["vector"] = self.resultsJobs[2]["vector"]
        else:
            print("\nInadequate data! Could not cluster")

        iterationCount = 0
        while iterationCount < clusteringIterationCount
            iterationCount += 1


            for jobIndex, job in enumerate(self.resultsJobs):
                jobVector = job["vector"]
                minDist = 1.0
                jobMemberOfCluster = 0
                for clusterIndex, clusterCentre in enumerate(clusterCentres):
                    clusterVector = clusterCentre["vector"]
                    dist = Agent.__calculateDistance__(clusterVector, jobVector)
                    if dist < minDist:
                        minDist = dist
                        jobMemberOfCluster = clusterIndex

                clusterCentres[jobMemberOfCluster]["members"].add(jobVector)









    @staticmethod
    def __getHTMLRow(title, url, location, description):
        htmlRow = '<tr>' \
                  '<td><a href="' + url + '" target="_blank">' + title + '</a></td>' \
                                                                         '<td>' + description + '</td>' \
                                                                                                '<td>' + location + '</td></tr>'
        return htmlRow

    def __printJobs__(self):

        htmlPrefix = '<!DOCTYPE html><html lang="en">' \
                     '<head><title>' + str(self.k) + 'Jobs for ' + self.searchString + '</title>' \
                                                                                       '<meta charset="utf-8">' \
                                                                                       '<meta name="viewport" content="width=device-width, initial-scale=1">' \
                                                                                       '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">' \
                                                                                       '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">' \
                                                                                       '</script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">' \
                                                                                       '</script>' \
                                                                                       '</head>' \
                                                                                       '<body>  ' \
                                                                                       '<div><h1>' + str(
            len(self.resultsJobs)) + ' jobs found for ' + self.searchString + '</h1></div>' \
                                                                              '<table class="table table-bordered table-striped"">' \
                                                                              '<thead>' \
                                                                              '<tr><th>Job Title</th>' \
                                                                              '<th>Job Description</th>' \
                                                                              '<th>Location</th></tr></thead>' \
                                                                              '<tbody>'
        htmlSuffix = '</tbody></table></body></html>'
        htmlRows = ""

        for job in self.resultsJobs:
            htmlRows = htmlRows + Environment.__getHTMLRow(job["title"], job["url"], job["loc"], job["desc"])
            # print("\nWebsite: " + job["website"])
            # print("\nJob Title: " + job["title"])
            # print("\nCompany: " + job["company"])
            # print("\nLocation: " + job["loc"])
            print("\nURL: " + job["url"])
            # print("\nDescription: " + job["desc"])
            # print ("\nVector",job["vector"])
            # print("\n*******************************")

        html = htmlPrefix + htmlRows + htmlSuffix
        try:
            from urllib import pathname2url  # Python 2.x
        except:
            from urllib.request import pathname2url  # Python 3.x

        fileName = self.searchString + "_jobs.htm"
        try:
            with open(fileName, 'w') as fileHandle:
                fileHandle.write(html.encode('utf-8'))
        except:
            print("Unable to write results to file")

        resultsUrl = 'file:{}'.format(pathname2url(os.path.abspath(fileName)))
        print("Results written to " + fileName)
        webbrowser.open(resultsUrl)

    @staticmethod
    def moduleCheck(moduleName):
        if moduleName not in sys.modules:
            print("\nPlease Install " + moduleName + " library and re-run. Program will exit")

    @staticmethod
    def __buildCLI__():
        """Builds the Command-Line interface

        :return: Object containing command line arguments entered by user
        """
        argParser = argparse.ArgumentParser(description="Job Search ImageClassifierAgent Using K-Nearest Neighbours. " +
                                                        "\nImplements k-nearest neighbors using Jaccard Distances on search string and documents as binary word count vectors" +
                                                        "\nOnly supports searching and no clustering",

                                            formatter_class=argparse.RawTextHelpFormatter)

        args = argParser.parse_args()  # Object holding command-line arguments


env = Environment()
env.main()
