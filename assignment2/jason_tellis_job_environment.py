from jason_tellis_job_agent import Agent
import os
import webbrowser
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
        while(self.ifContinue.lower() == 'y'):
            self.resultsJobs = []
            self.searchString = raw_input("\nGreetings "+os.getlogin()+"! \nWhat are you looking for? ")
            self.k = int(raw_input("How many results would you like? "))
            self.agent.sensor(self)
            self.__printJobs__()

            self.ifContinue = raw_input("\nDo you wish to continue? y to continue, press any other key to exit: ")
        print ("Goodbye")
        quit()


    def setResultFromAgent(self, resultJobs):

        self.resultsJobs = resultJobs


    def getK(self):
        return  self.k

    def getSearchString(self):
        return self.searchString

    # def cluster(self):
    #     clusterCount = 0
    #     clusterCentres= []
    #     clusterMember = []  # Membership matrix
    #     distance = []  # Distance matrix
    #     clusterIndex = 0
    #     jobIndex = 0
    #
    #     if len(self.resultsJobs) >=3:
    #         clusterCentres[0] = self.resultsJobs[0]
    #         clusterCentres[1] = self.resultsJobs[1]
    #         clusterCentres[2] = self.resultsJobs[2]
    #     else:
    #         print("\nInadequate data! Could not cluster")
    #
    #     clusterIndex = 0
    #     for clusterCentre in clusterCentres:
    #         jobIndex = 0
    #         for job in self.resultsJobs:

    @staticmethod
    def __getHTMLRow(title, url, location, description):
        htmlRow = '<tr>' \
              '<td><a href="'+url+'" target="_blank">'+title+'</a></td>' \
               '<td>'+description+'</td>' \
               '<td>'+location+'</td></tr>'
        return htmlRow


    def __printJobs__(self):

        htmlPrefix = '<!DOCTYPE html><html lang="en">' \
                     '<head><title>'+str(self.k)+'Jobs for '+self.searchString+'</title>' \
                     '<meta charset="utf-8">' \
                     '<meta name="viewport" content="width=device-width, initial-scale=1">' \
                     '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">' \
                     '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">' \
                     '</script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">' \
                     '</script>' \
                     '</head>' \
                     '<body>  ' \
                      '<div><h1>'+str(len(self.resultsJobs))+' jobs found for '+self.searchString+'</h1></div>' \
                      '<table class="table table-bordered table-striped"">' \
                     '<thead>' \
                     '<tr><th>Job Title</th>' \
                     '<th>Job Description</th>' \
                     '<th>Location</th></tr></thead>'\
                     '<tbody>'
        htmlSuffix = '</tbody></table></body></html>'
        htmlRows = ""




        for job in self.resultsJobs:

            htmlRows = htmlRows + Environment.__getHTMLRow(job["title"],job["url"], job["loc"], job["desc"])
            # print("\nWebsite: " + job["website"])
            # print("\nJob Title: " + job["title"])
            # print("\nCompany: " + job["company"])
            # print("\nLocation: " + job["loc"])
            print("\nURL: " + job["url"])
            # print("\nDescription: " + job["desc"])
            # print ("\nVector",job["vector"])
            # print("\n*******************************")

        html = htmlPrefix+htmlRows+htmlSuffix
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
        print("Results written to "+fileName)
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
        argParser = argparse.ArgumentParser(description="Job Search ImageClassifierAgent Using K-Nearest Neighbours.",
                                            formatter_class=argparse.RawTextHelpFormatter)

        # Add parameter -k for k
        argParser.add_argument("-k", "--k",
                               type=int,
                               default=10,
                               help="Description: No. of job entries to retrieve. "
                                    "\nType: Integer"
                                    "\nDefault: 10"
                                    "\nExample: python " + sys.argv[0] + " -k 10")

        # Add argument -q for keywords
        argParser.add_argument("-q", "--query",
                               type=str,
                               default="The Computer Science",
                               help="Description: List of Keywords for job search. "
                                    "\nType: String"
                                    "\nDefault: None "
                                    "\nExample: python " + sys.argv[0] + " -q Computer Science")

        # Add argument -l for location
        argParser.add_argument("-l", "--loc",
                               type=str,
                               default="",
                               help="Description: Location for Job Search. "
                                    "\nType: String"
                                    "\nDefault: San Jose"
                                    "\nExample: python " + sys.argv[0] + " -l San Jose")

        args = argParser.parse_args()  # Object holding command-line arguments
        return args




env = Environment()
env.main()
