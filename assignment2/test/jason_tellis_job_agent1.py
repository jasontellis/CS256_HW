"""Job search agent using K-NN for CS256-02

Author: Jason Tellis

Prints a list of 'k' specified jobs based on following user input:
 1. 'K'
 2. Job Keywords
 3. Job Location
__
"""
import argparse  # Used for creating Command Line Interface
import os.path  # Used for file R/W
import pickle  # Used for File R/W
import sys  # Used to access script name in CLI help
# Imported Internal Libraries
import time  # Used to calculate runtime
import urllib2  # Used to open URL
from operator import itemgetter
from  urllib import urlencode, quote_plus

# Imported External Libraries
from bs4 import BeautifulSoup


def __getTimeStamp__():
    timestamp = time.strftime('%Y%m%d')
    return timestamp


# //List of Stopwords from http://www.ranks.nl/stopwords
stopWords = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act",
             "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against",
             "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst",
             "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway",
             "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as",
             "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became",
             "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning",
             "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond",
             "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause",
             "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains",
             "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done",
             "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty",
             "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even",
             "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few",
             "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly",
             "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give",
             "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has",
             "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby",
             "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither",
             "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate",
             "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into",
             "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k",
             "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later",
             "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little",
             "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe",
             "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more",
             "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name",
             "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never",
             "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone",
             "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained",
             "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones",
             "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out",
             "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly",
             "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially",
             "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides",
             "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really",
             "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively",
             "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw",
             "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen",
             "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should",
             "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar",
             "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan",
             "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically",
             "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully",
             "such", "sufficiently", "suggest", "sup", "sure", "t", "take", "taken", "taking", "tell", "tends", "th",
             "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs",
             "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein",
             "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd",
             "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand",
             "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward",
             "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under",
             "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used",
             "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very",
             "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome",
             "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence",
             "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever",
             "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom",
             "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont",
             "words", "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your",
             "youre", "yours", "yourself", "yourselves", "you've", "z", "zero"]
lookupTableFileName = "jason_tellis_hw2_lookuptable" + __getTimeStamp__() + ".dat"

# The below dictionaries are used to modularize logic for fetching jobs from the three websites, can easily be ectended to
# fetch jobs from multiple websites
# This needed deep understanding of Beautiful Soup to handle the inconsistent ways in which classes are labelled on the three websites
acm = {"website": "acm",
       "baseUrl": "http://jobs.acm.org/jobs",
       "rowTag": "div",
       "rowAttr": {"class": "aiResultsMainDiv"},
       "rowSelector": {"name": "div", "attrs": {"class": "aiResultsMainDiv"}},
       "titleTag": "div",
       "titleAttr": {"class": "aiResultTitle"},
       "locTag": "span",
       "locAttr": {"class": "aiResultsLocationSpan"},
       "compTag": "li",
       "compAttr": {"class": "aiResultsCompanyName"},
       "descTag": "div",  # Job Descripton Selector
       "descAttr": {"class": ["aiResultsDescriptionNoAdvert", "aiResultsDescription"]},
       }

ieee = {"website": "ieee",
        "baseUrl": "http://jobs.ieee.org/jobs",
        "rowTag": "div",
        "rowAttr": {"class": "aiResultsWrapper"},
        "rowSelector": {"name": "div", "attrs": {"class": "aiResultsWrapper"}},
        "titleTag": "div",
        "titleAttr": {"class": "aiResultTitle"},
        "locTag": "span",
        "locAttr": {"class": "aiResultsLocationSpan"},
        "compTag": "li",
        "compAttr": {"class": "aiResultsCompanyName"},
        "descTag": "div",  # Job Descripton Selector
        "descAttr": {"class": ["aiResultsDescriptionNoAdvert", "aiResultsDescription"]},
        }
indeed = {"website": "indeed",
          "baseUrl": "https://www.indeed.com",  # /jobs?",
          "rowTag": "div",
          "rowAttr": {"class": "row"},
          "rowSelector": {"name": "div", "attrs": {"class": "row"}},
          "titleTag": "",  # "["a", "h2"],
          "titleAttr": {"class": "jobtitle"},
          "locTag": "span",
          "locAttr": {"class": "location"},
          "compTag": "span",
          "compAttr": {"class": "company"},
          "descTag": "span",  # Job Descripton Selector
          "descAttr": {"class": "summary"}
          }

jobPagesToSearch = (acm,
                    ieee,
                    indeed)
jobsLookupTable = {}  # Initialize Lookup table


def moduleCheck(moduleName):
    if moduleName not in sys.modules:
        print("\nPlease Install " + moduleName + " library and re-run. Program will exit")


# Build the Command Line Interface and Retrieve entered arguments
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


def __preBuildLookUp__():
    """

    :return:
    """

    print("\nPre-Building LookUp Table...")

    preBuildQueries = [
        {"searchString": "computer science", "searchLoc": ""},
        {"searchString": "artificial intelligence", "searchLoc": ""},
        {"searchString": "machine learning", "searchLoc": ""},
        {"searchString": "data scientist", "searchLoc": ""},
        {"searchString": "developer", "searchLoc": ""}
    ]

    global jobsLookupTable
    jobsLookupTable = {}
    jobsLookupTable = __readLookUpTableFromFile__(lookupTableFileName)

    if not jobsLookupTable:
        print("Pre-building Lookup Table from Web")
        for preBuildQuery in preBuildQueries:
            jobsLookupTable[preBuildQuery["searchString"]] = __buildLookupTable__(preBuildQuery["searchString"],
                                                                                  preBuildQuery["searchLoc"])
        print("\nPre-building Completed")


def main():
    """

    :return:
    """
    args = __buildCLI__()  # User's Command Line Arguments
    __preBuildLookUp__()

    k = args.k
    searchString = args.query.lower()
    searchString = __removeSpecialCharactersFromStr__(searchString)
    searchLoc = args.loc.lower()

    global jobsLookupTable
    # If look up table jobs for search string simply return k nearest jobs
    if jobsLookupTable.has_key(searchString):
        return jobsLookupTable[searchString][:k]
    else:
        jobsLookupTable[searchString] = __buildLookupTable__(searchString, searchLoc)

    neighbors = __findNearestNeighbours__(jobsLookupTable[searchString], 3)
    for neighbor in neighbors:
        print neighbor["dist"]



        # __writeLookupTableToFile__(jobsLookupTable)


def __buildLookupTable__(searchString="", searchLoc=""):
    """
    Fills job lookup table with a list of jobs sorted by distance from ACM, IEEE & Indeed for jobs matching given searchString & searchLoc
    along with corresponding distance from search string

    :param searchString: Keywords in  Job
    :param searchLoc: Job Location
    :return: List of jobs
    """

    jobsFromAllPages = []
    jobsFromPage = []
    jobsLookupTable = {}
    for jobPage in jobPagesToSearch:
        try:
            jobsFromPage = __scrapeJobsFromPage__(jobPage, searchString, searchLoc)
            jobsFromAllPages.extend(jobsFromPage)
        except:
            print("Could not read all jobs from" + jobPage["website"] + " due to unforeseen inconsistencies")

    jobsFromAllPages = sorted(jobsFromAllPages[0:5],
                              key=itemgetter('dist'))  # Sort the pages by distnce from search vector

    return jobsFromAllPages


def __printJobs__(jobsLookUpTable={}):
    for searchKey in jobsLookupTable:
        for job in jobsLookupTable[searchKey]:
            print("\nWebsite: " + job["website"])
            # print("\nJob Title: " + job["title"])
            # print("\nCompany: " + job["company"])
            # print("\nLocation: " + job["loc"])
            # print("\nURL: " + job["url"])
            # print("\nDescription: " + job["desc"])
            # print ("\nVector",job["vector"])
            # print("\n*******************************")


def __getSearchURL__(jobPage={}, searchString="", searchLoc=""):
    """
    Returns the URL to be used for searching a job page based on search String

    :param jobPage:
    :param searchString:
    :param searchLoc:
    :return:
    """

    maxResultCount = 50
    url = jobPage['baseUrl']
    prefix = ""  # Prefix appended to start of Base URl
    quotedSearchLoc = ""  # Encoded Search Loc for URL
    quotedSearchString = ""  # Encoded Search String for URL
    separator = ""  # Separator between searchString and searchLocation
    suffix = ""  # Suffix to be added to end of URL

    if jobPage["website"] == "acm" or jobPage["website"] == "ieee":

        # <sourceURL>/<searchString>/<searchLoc>
        if searchString or searchLoc:
            prefix = "/results/keyword/"
            suffix = "?rows=" + str(maxResultCount)
            if searchString:
                prefix = "/results/keyword/"
                quotedSearchString = quote_plus(searchString)

            if searchLoc:
                separator = "/"
                prefix = "/results/keyword/"
                quotedSearchLoc = quote_plus(searchLoc)

    elif jobPage["website"] == "indeed":
        prefix = "/jobs?"
        quotedSearchString = urlencode({"q": searchString, "l": searchLoc})

    url = url + prefix + quotedSearchString + separator + quotedSearchLoc + suffix
    return url


def __scrapeJobsFromPage__(jobPage={}, searchString="", searchLoc=""):
    """
    Scrapes jobs from a given website based on entered searchString & searchLocation

    :return: List of jobs from page
    """

    # print("\n*************************"+jobPage["website"])
    jobs = []
    url = __getSearchURL__(jobPage, searchString, searchLoc)
    print ("Retrieving jobs for '" + searchString + "' from : " + url)
    jobsHTMLTable = __extractJobsTableFromPage__(jobPage, url)
    # print(repr(jobsHTMLTable))
    for jobRow in jobsHTMLTable:
        job = __extractJobFromRow__(jobRow, jobPage, searchString)
        job["searchLoc"] = searchLoc
        job["searchString"] = searchString
        # print(job)
        jobs.append(job)
    print (str(len(jobs)) + " jobs found for " + searchString + " on " + jobPage["website"])
    return jobs


def __extractJobsTableFromPage__(jobPage={}, url=""):
    """
    Extracts HTML table of jobs from given URL and job page attributes passed in jobPage

    :param jobPage:
    :param url: URL of the WebPage
    :return: Job Dictionary with attributes
    """
    page = urllib2.urlopen(url)
    bsParser = BeautifulSoup(page, 'html.parser')
    # jobsHTMLTable = bsParser.find_all(name=jobPage["rowTag"], attrs=jobPage["rowAttr"])
    jobsHTMLTable = bsParser.find_all(**jobPage["rowSelector"])
    return jobsHTMLTable


def __extractJobFromRow__(jobRow, jobPage, searchString):
    """
    Extracts job attributes from given jobRow and returns a dictonary with a job
    :param jobRow: an HTML row holding a job from page specified in jobPage
    :param jobPage: jobPage attributes
    :return: A job with attributes such as title, description etc represented as a dictionary.
    """

    jobTitle = jobRow.find(name=jobPage["titleTag"], attrs=jobPage["titleAttr"])
    # print("row" + "jobTitle" + repr(jobTitle))
    jobTitle = jobTitle.get_text().strip()
    # jobTitle = jobTitle.encode('ascii')
    jobURL = jobRow.find("a")["href"].strip()
    jobURL = __formatJobURL__(jobPage, jobURL)
    jobCompany = jobRow.find(name=jobPage["compTag"], attrs=jobPage["compAttr"]).get_text().strip()
    jobDesc = jobRow.find(name=jobPage["descTag"], attrs=jobPage["descAttr"]).get_text().strip()

    searchVector = __getStringVector__(searchString)
    jobDescVector = __getStringVector__(jobDesc)
    jobLoc = jobRow.find(name=jobPage["locTag"], attrs=jobPage["locAttr"]).get_text().strip()

    searchVector = __getStringVector__(searchString)
    jobDescVector = __getStringVector__(jobDesc)
    distance = 0.0
    distance = __calculateDistance__(jobDescVector, searchVector)
    job = {
        "website": jobPage["website"],
        "title": jobTitle,
        "company": jobCompany,
        "desc": jobDesc,
        "loc": jobLoc,
        "url": jobURL,
        "vector": jobDescVector,
        "dist": distance
    }
    # print(job)
    return job


def __removeSpecialCharactersFromStr__(str=""):
    """
    Removes all special characters except spaces and alphanumeric chasracters

    :param str: String
    :return: String removing all special characters except spaces and alphanumeric chasracters
    """
    returnStr = ''.join(char for char in str if
                        char.isalnum() or char == " ")  # Consider alphanumeric characters and spaces only in job description

    return returnStr


def __getStringVector__(str=""):
    """
    Converts a string of words into a feature vector
    :param jobDesc:
    :return: A Dictionary vector with normalized word counts
    """

    vector = {}
    strippedStr = __removeSpecialCharactersFromStr__(str)
    strWordList = strippedStr.lower().split(" ")
    strWordList = __removeStopWords__(strWordList)
    vector = __convertWordListToVector__(strWordList)

    return vector


def __convertWordListToVector__(wordList=[]):
    """
    Converts given list of words to a vector with words and their associated frequency

    :param wordList: A list of strings
    :return: Dictonary of the form {"word": "count"}
    """
    total = len(wordList)
    wordVector = {}

    if total > 0:
        for word in wordList:
            if word in wordVector:
                wordVector[word] += wordVector[word]
            else:
                wordVector[word] = 1

    return wordVector


def __formatJobURL__(jobPage={}, url=""):
    """
    Converts the relative URL from a job into absolute URL

    :param jobPage:
    :param url:
    :return: an absolute URL as a string
    """
    jobURL = url
    if len(url) > 0:
        if url[0] == "/":  # If first character is  /, it is relative URL not absolute: prepend base URL to it
            jobURL = jobPage["baseUrl"] + url

    return jobURL


def __removeStopWords__(wordList=[]):
    """
    Removes stop words from a list of words
    :param wordList: A list of words
    :return: List with stopWords removed
    """
    jobDescWords = [jobDescWord for jobDescWord in wordList if jobDescWord not in stopWords and jobDescWord != " "]
    return jobDescWords


def __readLookUpTableFromFile__(fileName=lookupTableFileName):
    """

    :param fileName: Name of lookupfile stored on disk
    :return: Dictionary of the form {<searchString": ["list of jobs"]>}
    """

    jobsLookupTable = {}
    if os.path.isfile(fileName):
        print("\nFound lookup file " + lookupTableFileName + " on disk for today. Reading Lookup Table from Disk...")
        with open(fileName, "r") as fileHandle:
            tempLookupTable = pickle.load(fileHandle)
            jobsLookupTable = tempLookupTable

    if not jobsLookupTable:
        print ("No data in lookup file for today on disk. Lookup table will be pre-built from web")
        jobsLookupTable = {}

    return jobsLookupTable


def __writeLookupTableToFile__(jobsLookupTable={}, fileName=lookupTableFileName):
    print("\nWriting Lookup file to Disk")

    with open(fileName, 'w') as fileHandle:
        pickle.dump(jobsLookupTable, fileHandle)

    print("\nLookup file " + fileName + " written to disk")


def __calculateDistance__(lookUpVector={}, searchVector={}):
    """

    :param lookUpVector:
    :param searchVector:
    :return: Distance between vectors as  a floaing point no.
    """
    intersection, union, distance = 0.0, 0.0, 0.0
    for lookUpVectorWord in lookUpVector:
        if lookUpVectorWord in searchVector:
            intersection += 1
    union = len(lookUpVector) + len(searchVector) - intersection
    if intersection == 0:
        distance = 5000.0
    else:
        distance = 1.0 - float(intersection) / union

    # print("LookUp Vector", lookUpVector)
    # print("Search Vector", searchVector)
    # print ("Union", union)
    # print ("Intersection", intersection)
    # print ("Distance", distance)
    return distance


def __findNearestNeighbours__(jobsLookupTable=[], k=10):
    print("Finding " + str(k) + " nearest neighbours")
    return jobsLookupTable[:k]


main()
