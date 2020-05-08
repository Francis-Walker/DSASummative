from Node import *
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio

import matplotlib.image as mpimg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def is_within(node1, node2):
    x1 = node1.x
    y1 = node1.y
    x2 = node2.x
    y2 = node2.y

    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    print(type(distance))
    print(type(node1.rad))
    if distance > node1.rad:
        return False
    else:
        return True


def is_within_xy(x1, y1, x2, y2, r):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    if distance > r:
        return False
    else:
        return True


class Zone:
    #

    @property
    def prob_inf(self):
        return self.__prob_inf

    @property
    def prob_safely_recover(self):
        return self.__prob_safely_recover

    @property
    def current_iteration(self):
        return self.__current_iteration

    @current_iteration.setter
    def current_iteration(self, new_value):
        self.__current_iteration = new_value

    @property
    def prop_safely_recover(self):
        return self.prob_safely_recover

    @property
    def node_inf_dur(self):
        return self.__node_inf_dur

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def node_r(self):
        return self.__node_r

    @property
    def numNode(self):
        raise Exception("Local variable accessed outside class")

    @numNode.setter
    def numNode(self, val):
        raise Exception("Local variable assigned outside class")
 
    @property
    def sus_list(self):
        raise Exception("Local variable accessed outside class")

    @sus_list.setter
    def sus_list(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def inf_list(self):
        raise Exception("Local variable accessed outside class")

    @inf_list.setter
    def inf_list(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def rec_list(self):
        raise Exception("Local variable accessed outside class")

    @rec_list.setter
    def rec_list(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def title(self):
        raise Exception("Local variable accessed outside class")

    @title.setter
    def title(self, val):
        raise Exception("Local variable assigned outside class")

    def __init__(self, num_nodes=100, node_radius=5, infected_duration=(14, 48),
                 size_y=100, size_x=100, infection_prob=35, recover_safely_prob=50, title="Default"):

        # varibles used outside class
        self.__node_r = node_radius
        self.__node_inf_dur = infected_duration
        self.__current_iteration = 0
        self.__height = size_y
        self.__width = size_x
        self.__prob_inf = infection_prob
        self.__prob_safely_recover = recover_safely_prob

        # varibles used inside class
        self.__numNode = num_nodes
        self.__sus_list = []
        self.__inf_list = []
        self.__rec_list = []
        self.__title = title

        for i in range(0, self.__numNode):
            self.__sus_list.append(Node(self))

        ran_index = random.randint(0, len(self.__sus_list) + 1)
        node = self.__sus_list.pop(ran_index)
        # print(node.status)
        node.exposed(True)
        # print(node.status)

        self.__inf_list.append(node)

    # each node makes a move and applies sus to inf to rec logic and swaps where needed
    def iteration(self):

        infection_map = {}
        swap_index = []

        # check infected list and map infection zone and recovers node if possible

        # if node can recover it does else node dies
        for i in self.__inf_list:
            if i.can_recover():
                i.recovered()

            if i.get_rec():
                if not i.get_dead():
                    i.step()

                # Helper list to swap infected and recovered node so they are in the correct list
                swap_index.append(self.__inf_list.index(i))
            else:
                i.step()

                # adds all xy within radius of infected to infection map
                for x in range(i.x - i.rad, i.x + i.rad):
                    for y in range(i.y - i.rad, i.y + i.rad):
                        if is_within_xy(i.x, i.y, x, y, i.rad):
                            infection_map["" + str(x) + "," + str(y)] = True

        swap_index.sort()
        swap_index.reverse()
        # Swap inf to rec
        if self.__inf_list:
            for index_to_remove in swap_index:
                node = self.__inf_list.pop(index_to_remove)
                self.__rec_list.append(node)

        # node in infection map exposed and populate swap indexs
        swap_index = []

        # for each suseptiable node, check if in infection map
        for i in range(len(self.__sus_list)):

            self.__sus_list[i].step()

            key_test = "" + str(self.__sus_list[i].x) + "," + str(self.__sus_list[i].y)

            # if in infection map node is exposed
            if key_test in infection_map:
                self.__sus_list[i].exposed()
                # if node is infected prepares to swap
                if self.__sus_list[i].get_inf():
                    swap_index.append(i)

        # Reverses order top avoid integrity lapse
        swap_index.sort()
        swap_index.reverse()
        # Swap sus to inf
        if self.__sus_list:
            for index_to_remove in swap_index:
                node = self.__sus_list.pop(index_to_remove)
                self.__inf_list.append(node)

            # i.display_postion()
        # if recovered node is not dead it moves
        for i in self.__rec_list:
            if not i.get_dead():
                i.step()

        self.current_iteration = self.current_iteration + 1

    # gets x/y postions for all nodes
    def gen_xy_lists(self):

        s_x_arr = []
        s_y_arr = []
        i_x_arr = []
        i_y_arr = []
        i_r_arr = []
        r_x_arr = []
        r_y_arr = []
        d_x_arr = []
        d_y_arr = []
        xy = []

        for i in self.__sus_list:
            s_x_arr.append(i.x)
            s_y_arr.append(i.y)

        for i in self.__inf_list:
            i_x_arr.append(i.x)
            i_y_arr.append(i.y)
            i_r_arr.append(i.rad)

        for i in self.__rec_list:
            if i.get_dead():
                d_x_arr.append(i.x)
                d_y_arr.append(i.y)
            else:
                r_x_arr.append(i.x)
                r_y_arr.append(i.y)

        return (np.array(s_x_arr), np.array(s_y_arr)), (np.array(i_x_arr), np.array(i_y_arr), np.array(i_r_arr)), (
            np.array(r_x_arr), np.array(r_y_arr)), (np.array(d_x_arr), np.array(d_y_arr))
        # returns current postions of all nodes

    # makes plots
    def map(self, ax=None):
        # gets coordinates of all nodes based on status
        co_ords = self.gen_xy_lists()

        # clears axes
        ax = ax or plt.gca()
        ax.cla()

        # paints axis
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_ylim(0, self.height)
        ax.set_xlim(0, self.width)
        ax.set_yticklabels("")
        ax.set_xticklabels("")
        ax.title.set_text(self.__title)

        # paints each node on plot
        ax.plot(co_ords[0][0], co_ords[0][1], 'bo', label="Susceptible")
        ax.plot(co_ords[1][0], co_ords[1][1], 'ro', label="Infected")
        ax.plot(co_ords[2][0], co_ords[2][1], 'ko', label="Recovered")
        ax.plot(co_ords[3][0], co_ords[3][1], 'kx', label="Dead")
        # ax.axis("off")

        # paints red circle around each inf node based on zone radious
        for i in range(len(co_ords[1][0])):
            circle = plt.Circle((co_ords[1][0][i], co_ords[1][1][i]), co_ords[1][2][i], color='r', fill=False)
            ax.add_artist(circle)

        # plt.savefig('figure.png')

        # img = imageio.imread('figure.png')

        subplot = ax

        return subplot

    # returns images of plots
    def map_img(self):

        fig = self.map()
        fig.savefig('figure.png')
        img = imageio.imread('figure.png')
        return img

    # return data of current iteration
    def map_data(self):
        size_s = len(self.__sus_list)
        size_i = len(self.__inf_list)

        size_r = 0
        size_d = 0
        for i in self.__rec_list:
            if i.get_dead():
                size_d += 1
            else:
                size_r += 1

        return [size_s, size_i, size_r, size_d, self.current_iteration]

    # randomly select n nodes to export.
    def node_export(self, total_export):
        # list of nodes to export from zone
        output = []

        # break point of random node selected to export to ensure node is pulled from correct list
        breakpoint_sus_list = len(self.__sus_list)
        breakpoint_inf_list = breakpoint_sus_list + len(self.__inf_list)
        breakpoint_rec_list = breakpoint_inf_list + len(self.__rec_list)

        for i in range(total_export):
            random_index = random.randint(0, self.__numNode)
            if random_index < breakpoint_sus_list and random_index < breakpoint_inf_list:
                if self.__sus_list:
                    node = random.choice(self.__sus_list)
                    self.__sus_list.remove(node)
                    output.append(node)
                    self.__numNode -= 1

            elif random_index < breakpoint_inf_list and random_index < breakpoint_rec_list:
                if self.__inf_list:
                    node = random.choice(self.__inf_list)
                    self.__inf_list.remove(node)
                    output.append(node)
                    self.__numNode -= 1
            else:
                if self.__rec_list:
                    node = random.choice(self.__rec_list)
                    self.__rec_list.remove(node)
                    output.append(node)
                    self.__numNode -= 1

        return output

    # import n  nodes and assign them to respective list based on status
    def node_import(self, node):

        node.zone_update(self)
        if node.get_rec():
            self.__rec_list.append(node)
        elif node.get_inf():
            self.__inf_list.append(node)
        else:
            self.__sus_list.append(node)
        self.__numNode += 1
