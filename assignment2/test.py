fname = "jason_tellis_lookup.dat"
import os.path
import pickle

jobsLookupTable = [{"1": 1, "2":2},
                   {"3": 3, "4":4}]


# _lookUpTableFileName = "test.dat"
# with open(_lookUpTableFileName, 'a') as fileHandle:
#     # for job in jobsLookupTable:
#     pickle.dump(jobsLookupTable, fileHandle)
#     print("\nLookup file " + _lookUpTableFileName + " written to disk")
#
# with open(_lookUpTableFileName, 'r') as fileHandle:
#     # for job in jobsLookupTable:
#     jobsLookupTable = pickle.load(fileHandle)
#
#     print(repr(jobsLookupTable))

# def __calculateDistance__(searchVector={}, lookUpVector={}):
#     intersection, union, distance = 0.0, 0.0, 0.0
#     for lookUpVectorWord  in lookUpVector:
#         if lookUpVectorWord in searchVector:
#             intersection += 1
#     union = len(lookUpVector) + len(searchVector) - intersection
#     if intersection == 0:
#         distance = 5000.0
#     else:
#         distance = 1.0 - float(intersection)/union
#     print("LookUp Vector", lookUpVector)
#     print("Search Vector", searchVector)
#     print ("Union", union)
#     print ("Intersection", intersection)
#     print ("Distance", distance)

# __calculateDistance__({"a":1,"b":1,"c":1}, {"a":1, "b":1, "c":1, "e":1})
#

# import re
# text = "Hi-?!@'.eI    am a boy"
# text = re.sub("[^\w\s]", " ", "Hi-?!@'.eI    am a boy   ")
# print text
# print  re.sub("\s+", " ", text).strip()

import time
def __getTimeStamp__():
    timestamp = time.strftime('%Y%m%d%H%M%S')
    return timestamp

print __getTimeStamp__()

