import os.path  # Used for file R/W
import pickle  # Used for File R/W
import time

class Utilities:




    # //List of Stopwords from http://www.ranks.nl/stopwords
    stopWords = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act",
                 "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again",
                 "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am",
                 "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore",
                 "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren",
                 "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away",
                 "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before",
                 "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below",
                 "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca",
                 "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come",
                 "comes", "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't",
                 "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during",
                 "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end",
                 "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody",
                 "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first",
                 "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found",
                 "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given",
                 "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has",
                 "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby",
                 "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his",
                 "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im",
                 "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information",
                 "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've",
                 "j", "just", "k", "keep", "keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely",
                 "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like",
                 "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly",
                 "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely",
                 "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much",
                 "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly",
                 "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine",
                 "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not",
                 "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often",
                 "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord",
                 "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
                 "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per",
                 "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp",
                 "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides",
                 "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really",
                 "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively",
                 "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same",
                 "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming",
                 "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll",
                 "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant",
                 "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody",
                 "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere",
                 "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly",
                 "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "t", "take",
                 "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll",
                 "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there",
                 "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres",
                 "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think",
                 "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru",
                 "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly",
                 "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike",
                 "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully",
                 "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol",
                 "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went",
                 "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever",
                 "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether",
                 "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever",
                 "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words",
                 "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre",
                 "yours", "yourself", "yourselves", "you've", "z", "zero"]

    # A new lookup file is generated everyday with time stamp
    lookupTableFileName = "jason_tellis_hw2_lookuptable" + time.strftime('%Y%m%d') + ".dat"

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




    @staticmethod
    def __removeSpecialCharactersFromStr__(str=""):
        """
        Removes all special characters except single spaces and alphanumeric characters

        :param str: String
        :return: String with only single spaces and alphanumeric chasracters
        """
        # returnStr = re.sub("[^\w\s]", " ", str)
        # returnStr = re.sub()

        returnStr = ''.join(char for char in str if
                            char.isalnum() or char == " ")  # Consider alphanumeric characters and spaces only in job description

        return returnStr

    @staticmethod
    def __getStringVector__(str=""):
        """
        Converts a string of words into a feature vector
        :param jobDesc:
        :return: A Dictionary vector with normalized word counts
        """

        vector = {}
        strippedStr = Utilities.__removeSpecialCharactersFromStr__(str)
        strWordList = strippedStr.lower().split(" ")
        strWordList = Utilities.__removeStopWords__(strWordList)
        vector = Utilities.__convertWordListToVector__(strWordList)

        return vector

    @staticmethod
    def __convertWordListToVector__(wordList=[]):
        """
        Converts given list of words to a dictionary with words and their associated frequency

        :param wordList: A list of strings
        :return: Dictonary of the form {"word": "count"}
        """
        total = len(wordList)
        wordVector = {}

        if total > 0:
            for word in wordList:
                if word in wordVector:
                    ++wordVector[word]
                else:
                    wordVector[word] = 1

        return wordVector

    @staticmethod
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
                jobURL = jobPage["baseUrl"] + url;

        return jobURL

    @staticmethod
    def __removeStopWords__(wordList=[]):
        """
        Removes stop words from a list of words
        :param wordList: A list of words
        :return: List with stopWords removed
        """



        jobDescWords = [jobDescWord for jobDescWord in wordList if jobDescWord not in Utilities.stopWords and jobDescWord != " "]
        return jobDescWords;

    @staticmethod
    def __readLookUpTableFromFile__(fileName=lookupTableFileName):
        """
        Reads lookup table file if it was generated today, else returns blank so that new look up table will be built

        :param fileName: Name of lookupfile stored on disk
        :return: Dictionary of the form {<searchString": ["list of jobs"]>}
        """

        jobsLookupTable = {}
        if os.path.isfile(fileName):  # Checks if file was written today
            print("\nFound lookup file " + fileName + " on disk for today. Reading Lookup Table from Disk...")
            with open(fileName, "r") as fileHandle:
                tempLookupTable = pickle.load(fileHandle)
                jobsLookupTable = tempLookupTable

        if not jobsLookupTable:
            print ("No data in lookup file for today on disk. Lookup table will be pre-built from web")
            jobsLookupTable = {}

        return jobsLookupTable

    @staticmethod
    def __writeLookupTableToFile__(jobsLookupTable={}, fileName=lookupTableFileName):
        """
        Writes LookUpTable to disk
        :param jobsLookupTable:
        :param fileName:
        :return: none
        """

        print("\nWriting Lookup file to Disk")

        with open(fileName, 'w') as fileHandle:
            pickle.dump(jobsLookupTable, fileHandle)

        print("\nLookup file " + fileName + " written to disk")

    @staticmethod
    def __calculateDistance__(lookUpVector={}, searchVector={}):
        """Calculates Jaccard distance between two vectors
        :param lookUpVector:
        :param searchVector:
        :return: Jaccard  distance between vectors as  a floaing point no.
        """
        intersection, union, distance = 0.0, 0.0, 0.0
        for lookUpVectorWord in lookUpVector:
            if lookUpVectorWord in searchVector:
                intersection += 1
        union = len(lookUpVector) + len(searchVector) - intersection
        if intersection == 0:  # If intersection is 0, distance is maximum
            distance = 1.0
        else:
            distance = 1.0 - float(intersection) / union

        # print("LookUp Vector", lookUpVector)
        # print("Search Vector", searchVector)
        # print ("Union", union)
        # print ("Intersection", intersection)
        # print ("Distance", distance)
        return distance


