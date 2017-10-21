import os

from jason_tellis_job_agent import Agent


class Environment:
    k = 10
    searchString = "Computer Science"
    resultsJobs = []
    agent = None
    ifContinue = "y"

    def __init__(self):
        self.ifContinue = "y"
        self.k = 10
        self.searchString = "Computer Science"
        self.agent = Agent()
        self.resultsJobs = []

    def main(self):
        while (self.ifContinue.lower() == 'y'):
            self.searchString = raw_input("\nGreetings " + os.getlogin() + "! What are you looking for?: ")
            self.k = int(raw_input("Kindly enter how many results you want(k): "))
            self.agent.sensor(self)
            self.__printJobs__()

            self.ifContinue = raw_input("Do you wish to continue? y to continue, press any other key to exit")
        print ("Goodbye")
        quit()

    def setResultFromAgent(self, resultJobs):

        self.resultsJobs = resultJobs

    def getK(self):
        return self.k

    def getSearchString(self):
        return self.searchString

    def __printJobs__(self):

        for job in self.resultsJobs:
            # print("\nWebsite: " + job["website"])
            # print("\nJob Title: " + job["title"])
            # print("\nCompany: " + job["company"])
            # print("\nLocation: " + job["loc"])
            print("\nURL: " + job["url"])
            # print("\nDescription: " + job["desc"])
            # print ("\nVector",job["vector"])
            # print("\n*******************************")


env = Environment()
env.main()
