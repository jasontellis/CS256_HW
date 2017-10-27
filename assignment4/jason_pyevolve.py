import datetime  # JT+
import os  # JT+
import random
import time

from pyevolve import Consts
from pyevolve import Crossovers
from pyevolve import G1DList
from pyevolve import GSimpleGA

from DistanceMatrix import DistanceMatrix

random.seed(1024)
PIL_SUPPORT = None

try:
    from PIL import Image, ImageFont, ImageDraw

    PIL_SUPPORT = True
except:
    PIL_SUPPORT = False

distanceMatrix = []
coords = []

CITIES = 0  # JT+
DM = None

WIDTH = 1024
HEIGHT = 768
LAST_SCORE = -1


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    global DM
    total = 0
    t = tour.getInternalList()
    for i in range(CITIES):
        j = (i + 1) % CITIES
        total += DM.getDistanceBetweenCities(t[i], t[j])
        # total += matrix[t[i], t[j]]
    return total


def write_tour_to_text_file(coords, tour, distanceMatrix):
    """
    Writes output of TSP to a file

    :param coords: Co-ordinates of the city
    :param tour: Sequence of cities to visit

    :return: None
    """

    global DM
    textFileName = "Tour_"
    tempTimestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(tempTimestamp).strftime('%Y-%m-%d_%H%M%S')
    textFileName += timestamp

    with open(textFileName, 'w') as fileHandle:
        fileHandle.write("TOUR_SECTION\n")
        distance = 0.0

        num_cities = len(tour)
        fileHandle.write(str(tour[0]) + "\n")
        for i in range(num_cities):
            j = (i + 1) % num_cities
            city_i = tour[i]
            city_j = tour[j]
            currDistance = DM.getDistanceBetweenCities(city_i, city_j)
            print("%i,%i,%f\n" % (city_i, city_j, currDistance))
            distance += currDistance
            fileHandle.write(str(city_j) + "\n")

    print("The distance travelled is %f" % tour_length(distanceMatrix, tour))
    print "The tour was written to %s" % (textFileName)
    shouldOpen = raw_input("Do you wish to open the file?  y: Yes, any other key to continue:")
    if shouldOpen.lower() == 'y':
        osCommandString = "open -t " + textFileName
        os.system(osCommandString)


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


def main_run(filename):
    global distanceMatrix, coords, WIDTH, HEIGHT, CITIES

    # coords = [(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    #               for i in xrange(CITIES)]  #JT-

    global DM
    DM = DistanceMatrix(filename)

    CITIES = DM.cityCount  # JT+
    coords = DM.coordinates
    # distanceMatrix = cartesian_matrix(coords)#JT-
    distanceMatrix = DM.matrix
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
    write_tour_to_text_file(coords, best, distanceMatrix)

    if PIL_SUPPORT:
        write_tour_to_img(coords, best, "./tsp/tsp_result.png")
    else:
        print "No PIL detected, cannot plot the graph !"


if __name__ == "__main__":
    main_run("./att48.tsp")
