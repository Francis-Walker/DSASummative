from Zone import *
from Node import *
import csv
from math import sqrt, floor, ceil
from PIL import Image
import imageio
from enum import Enum


# Takes number of zones n and return sutible grid size (number of col and row)
def grid_size(n):
    sqrt_n = sqrt(n)
    row = floor(sqrt_n)
    col = ceil(sqrt_n)
    check = False
    while not check:
        if row * col < n:
            row += 1
        else:
            check = True

    return row, col


# enum of zone types
class ZoneType(Enum):
    HighAwarenessUrbanArea = 1
    MedAwarenessUrbanArea = 2
    LowAwarenessUrbanArea = 3
    HighAwarenessRuralArea = 4
    MedAwarenessRuralArea = 5
    LowAwarenessRuralArea = 6


# takes in zone type value and returns unique zone based on zoneType init variables
def zoneFactory(type):
    if type == ZoneType.HighAwarenessUrbanArea.value:
        return Zone(num_nodes=200, node_radius=2, infection_prob=10, recover_safely_prob=98,
                    title="HighAwareness_UrbanArea")
    elif type == ZoneType.MedAwarenessUrbanArea.value:
        return Zone(num_nodes=200, node_radius=4, infection_prob=20, recover_safely_prob=85,
                    title="MedAwareness_UrbanArea")
    elif type == ZoneType.LowAwarenessUrbanArea.value:
        return Zone(num_nodes=200, node_radius=6, infection_prob=30, recover_safely_prob=70,
                    title="LowAwareness_UrbanArea")
    elif type == ZoneType.HighAwarenessRuralArea.value:
        return Zone(num_nodes=50, node_radius=2, infection_prob=10, recover_safely_prob=98,
                    title="HighAwareness_RuralArea")
    elif type == ZoneType.MedAwarenessRuralArea.value:
        return Zone(num_nodes=50, node_radius=4, infection_prob=20, recover_safely_prob=85,
                    title="MedAwareness_RuralArea")
    elif type == ZoneType.LowAwarenessUrbanArea.value:
        return Zone(num_nodes=50, node_radius=6, infection_prob=30, recover_safely_prob=70,
                    title="LowAwareness_RuralArea")
    else:
        return Zone()


class Universe:
    __zones = []

    # private getters and setters to ensure local varibles are not accessed outside of class
    @property
    def zones(self):
        raise Exception("Local variable accessed outside class")

    @zones.setter
    def zones(self, val):
        raise Exception("Local variable assigned  outside class")

    @property
    def num_iterations(self):
        raise Exception("Local variable accessed outside class")

    @num_iterations.setter
    def num_iterations(self, val):
        raise Exception("Local variable assigned  outside class")

    @property
    def num_zones(self):
        raise Exception("Local variable accessed outside class")

    @num_zones.setter
    def num_zones(self, val):
        raise Exception("Local variable assigned  outside class")

    @property
    def num_nodes_move(self):
        raise Exception("Local variable accessed outside class")

    @num_nodes_move.setter
    def num_nodes_move(self, val):
        raise Exception("Local variable assigned  outside class")

    # init for universe
    def __init__(self):
        # number of iteration simulation will run
        self.__num_iterations = 500

        # number of zones in simulation
        self.__num_zones = 10

        # number of zone that move from each zone to another random zone at each iteration
        self.__num_nodes_move = 1

        # generate number of random zones to be used in simulation
        for i in range(self.__num_zones):
            # To generate choicen zones types parse 1-6 inclusive to zone factory.
            self.__zones.append(zoneFactory(4))

    # moves nodes between zones at each iteration
    def node_move(self):
        # local varible used to store all exported node before new zone assignment
        node_list = []

        # extracts nodes from zones
        for i in self.__zones:
            node_list += i.node_export(self.__num_nodes_move)

        # place each exported node into new zone if new zone is not previous zone
        for i in node_list:
            check = True
            while check:
                zone = random.choice(self.__zones)
                if not zone == i.zone:
                    zone.node_import(i)
                    check = False

    # export simulation to csv
    def export_csv(self):
        # varible to store all simulation data before exporting to csv
        write_data = []
        for j in range(self.__num_iterations):
            # moves nodes
            self.node_move()

            # get zone data and iterates each zone
            for i in range(len(self.__zones)):
                self.__zones[i].iteration()
                i_data = self.__zones[i].map_data()
                i_data += [i]
                write_data.append(i_data)

        # opens or creates csv to write to
        csvO = open('dataHighPopLowAwareness5.csv', 'w')
        with csvO:
            writer = csv.writer(csvO)
            # write colomn headers
            writer.writerow(["Susceptible", "Infected", "Recover", "Dead", "Iter", "Zone"])
            # writes all data to csv
            writer.writerows(write_data)

    #generates gif of simulation
    def map_universe_gif(self):
        #dynamically creates grid size to plot all zones
        gridSize = grid_size(self.__num_zones)

        #creates plot
        fig, axis = plt.subplots(ncols=gridSize[1], nrows=gridSize[0], figsize=(5 * gridSize[1], 5 * gridSize[0]))

        #list to store img of each iterations plot before gif conversion
        img_list = []

        #generates subplots for each iteration of simulation
        for iter in range(self.__num_iterations):


            plt.suptitle(str("Low Population High awareness\nIteration") + ": " + str(iter))
            nz = 0
            for i in range(gridSize[0]):
                for j in  range(gridSize[1]):
                    if nz < self.__num_zones:
                        self.__zones[nz].map(axis[i][j])
                        self.__zones[nz].iteration()
                        nz += 1
                    else:
                        axis[i][j].axis('off')
                self.node_move()

            plt.savefig('figure.png')
            #appends image of plot to imglist
            img_list.append(imageio.imread('figure.png'))

        #takes img list and saves it as gif
        imageio.mimsave("imgChache/universe.gif", img_list)



uni = Universe()
uni.map_universe_gif()
