import os  # JT+
import time, datetime #JT+
import random

from pyevolve import Consts
from pyevolve import Crossovers
from pyevolve import G1DList
from pyevolve import GSimpleGA

random.seed(1024)
from math import sqrt

PIL_SUPPORT = None

try:
    from PIL import Image, ImageFont, ImageDraw
    PIL_SUPPORT = True
except:
    PIL_SUPPORT = False

distanceMatrix = []
coords = []
# CITIES = 100
CITIES = 48  # JT+

WIDTH = 1024
HEIGHT = 768
LAST_SCORE = -1


def cartesian_matrix(coords):
    """

    :param coords:
    :return:
    """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)

            matrix[i, j] = dist
    return matrix


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(CITIES):
        j = (i + 1) % CITIES
        total += matrix[t[i], t[j]]
    return total


def write_tour_to_text_file(coords, tour, distanceMatrix):
    """
    Writes output of TSP to a file

    :param coords: Co-ordinates of the city
    :param tour: Sequence of cities to visit
    :param textFileName: Name of file to write output to

    :return: None
    """

    textFileName = "Tour"
    tempTimestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(tempTimestamp).strftime('%Y-%m-%d_%H%M%S')
    textFileName +=  timestamp


    with open(textFileName, 'w') as fileHandle:
        fileHandle.write("TOUR_SECTION\n")
        distance = 0.0

        num_cities = len(tour)
        for i in range(num_cities):
            j = (i + 1) % num_cities
            city_i = tour[i]
            city_j = tour[j]
            currDistance = distanceMatrix[( city_i, city_j)]
            print( "%i,%i,%f\n" % ( city_i, city_j, currDistance))
            distance += currDistance
            fileHandle.write(str(city_i) + "\n")
            fileHandle.write(str(city_j) + "\n")

    print("The distance of shortest path is %f" % tour_length(distanceMatrix,tour))
    print "The plot was written to %s" % (textFileName)




def write_tour_to_img(coords, tour, img_file):
    """ The function to plot the graph """
    padding = 20
    coords = [(x + padding, y + padding) for (x, y) in coords]
    maxx, maxy = 0, 0
    for x, y in coords:
        maxx, maxy = max(x, maxx), max(y, maxy)
    maxx += padding
    maxy += padding
    img = Image.new("RGB", (int(maxx), int(maxy)), color=(255, 255, 255))
    font = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        x1, y1 = coords[city_i]
        x2, y2 = coords[city_j]
        d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
        d.text((int(x1) + 7, int(y1) - 5), str(i), font=font, fill=(32, 32, 32))

    for x, y in coords:
        x, y = int(x), int(y)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0), fill=(196, 196, 196))
    del d
    img.save(img_file, "PNG")
    print "The plot was saved into the %s file." % (img_file,)


def G1DListTSPInitializator(genome, **args):
    """ The initializator for the TSP """
    lst = [i for i in xrange(genome.getListSize())]
    random.shuffle(lst)
    genome.setInternalList(lst)


def readCityCoordinatesFromFile(fileName="/Users/jasontellis/Google Drive/cs256/hw/assignment4/att48.tsp"):
    """
    Read cities' Co-ordinates from given file

    :param fileName: Name of file
    :return: A list of co-ordinates
    """

    DATASET_START_INDEX = 7  # First 6 lines of file are metadata
    cityCoordinates = []
    lineIndex = 0

    if os.path.isfile(fileName):

        with open(fileName, 'rb') as fileHandle:

            for line in fileHandle:

                lineIndex += 1
                if lineIndex >= DATASET_START_INDEX:  # Skip copying first 6 lines of metadata
                    cityIndex, xCoord, yCoord = line.split()
                    xCoord = (int)(xCoord)
                    yCoord = (int)(yCoord)
                    cityCoordinates.append((xCoord, yCoord))

    else:
        print("Invalid filename")
    return cityCoordinates


def main_run():
    global distanceMatrix, coords, WIDTH, HEIGHT

    # coords = [(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    #               for i in xrange(CITIES)]  #JT-

    coords = readCityCoordinatesFromFile()  # JT+

    # distanceMatrix = cartesian_matrix(coords)#JT-
    distanceMatrix = cartesian_matrix(coords)  # JT+
    genome = G1DList.G1DList(len(coords))

    genome.evaluator.set(lambda chromosome: tour_length(distanceMatrix, chromosome))
    genome.crossover.set(Crossovers.G1DListCrossoverEdge)
    genome.initializator.set(G1DListTSPInitializator)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(1000)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)

    ga.evolve(freq_stats=500)
    best = ga.bestIndividual()

    if PIL_SUPPORT:
        write_tour_to_img(coords, best, "tsp_result.png")
        write_tour_to_text_file(coords,best, distanceMatrix)
    else:
        print "No PIL detected, cannot plot the graph !"


if __name__ == "__main__":
    main_run()