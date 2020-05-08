import random
import numpy as np
import math
from enum import Enum


class Node:
    class Status(Enum):
        Susceptible = 'S'
        Infected = 'I'
        Recovered = 'R'
        Dead = 'D'

    __x = 0
    __y = 0
    __status = Status.Susceptible
    __speed = 2
    __rad = 7
    __max_h = 0
    __max_w = 0
    __inf_iter = None
    __rec_iter = None

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def rad(self):
        return self.__rad

    @property
    def status(self):
        return self.__status

    @property
    def move(self):
        raise Exception("Local variable accessed outside class")

    @move.setter
    def move(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def theta(self):
        raise Exception("Local variable accessed outside class")

    @theta.setter
    def theta(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def speed(self):
        raise Exception("Local variable accessed outside class")

    @speed.setter
    def speed(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def zone(self):
        return self.__zone

    @zone.setter
    def zone(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def max_h(self):
        raise Exception("Local variable accessed outside class")

    @max_h.setter
    def max_h(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def max_w(self):
        raise Exception("Local variable accessed outside class")

    @max_w.setter
    def max_w(self, val):
        raise Exception("Local variable assigned outside class")

    @property
    def infected_duration(self):
        raise Exception("Local variable accessed outside class")

    @infected_duration.setter
    def infected_duration(self, val):
        raise Exception("Local variable assigned outside class")

    def __init__(self, zone):
        # stores nodes current zone
        self.__zone = zone

        # varibles used internally

        # Boolean to dictate movement type of node
        self.__move = True

        # angle the node wil move on nexxt iteration
        self.__theta = random.randint(0, 360)

        # distance(in xy) node will move
        self.__speed = 1

        # nodes maximum width and height
        self.__max_h = self.__zone.height
        self.__max_w = self.__zone.width

        # infectious duration of each node
        self.__infected_duration = zone.node_inf_dur

        # varible access outside class

        # infectious radius of nodes in zone
        self.__rad = zone.node_r

        # stores xy postion of node
        # start at random position in node
        self.__x = random.randint(1, self.__max_w - 1)
        self.__y = random.randint(1, self.__max_h - 1)

    # When node moves between zones updates zone and set postion in middle
    def zone_update(self, zone):
        self.__zone = zone
        self.__x = zone.width // 2
        self.__y = zone.height // 2
        self.__max_h = zone.height
        self.__max_w = zone.width
        self.__rad = zone.node_r

    # Node moves
    def step(self):
        # move = True
        if self.__move:
            # new xy it found using angle of movement
            x = round(self.__x + (self.__speed * math.cos(math.radians(self.__theta))))
            y = round(self.__y + (self.__speed * math.sin(math.radians(self.__theta))))

            # if node is on zone boundry angle is reversed and zone postion is set to be on boundrey
            check = False
            if x > self.__zone.width:
                self.__x = self.__zone.width - 1
                check = True
            elif x < 1:
                self.__x = 1
                check = True
            else:
                self.__x = x

            if y > self.__zone.height:
                self.__y = self.__zone.height - 1
                check = True
            elif y < 1:
                self.__y = 1
                check = True
            else:
                self.__y = y

            # if not moving beyond  boundrey new angle is within 45 degrees of previous else reversed
            if not check:
                self.__theta += random.randint(-45, 45)
            else:
                self.__theta += 180

        else:

            # for each node assigns a direction and checks if direction is possible. if so moves node accordingly
            direction = random.randint(1, 4)
            usage_dict = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

            # print(usage_dict[direction])

            if (self.__x == 1 and direction == 1):
                pass
            elif (self.__x == self.__max_w - 1 and direction == 2):
                pass
            elif (self.__y == 1 and direction == 3):
                pass
            elif (self.__y == self.__max_h - 1 and direction == 4):
                pass
            else:
                self.__x += usage_dict[direction][0]
                self.__y += usage_dict[direction][1]

    def display_postion(self):
        print("x " + str(self.__x) + " y " + str(self.__y))

    # return true is node is infected else False
    def get_inf(self):
        if self.__status == self.Status.Infected:
            return True
        else:
            return False

    # return true is node is recovered else False
    def get_rec(self):
        if self.__status == self.Status.Recovered or self.__status == self.Status.Dead:
            return True
        else:
            return False

    # return true is node is dead else False
    def get_dead(self):
        if self.__status == self.Status.Dead:
            return True
        else:
            return False

    # sets node status to infect if node is infected
    def set_inf(self, f_t):
        if f_t:
            self.__status = self.Status.Infected

    # sets node status to recovered if input true else sets node to dead
    def set_rec(self, f_t):
        if f_t:
            self.__status = self.Status.Recovered
        else:
            self.__status = self.Status.Dead

    # exposes node
    def exposed(self, first=False):

        # random check to see if node is infected else not
        test_int = random.randint(0, 100)
        if test_int < self.__zone.prob_inf:
            first = True

        # if node is infected on zone init node
        if first:
            self.set_inf(True)
            self.inf_iter = self.__zone.current_iteration
            self.rec_iter = self.__zone.current_iteration + random.randint(self.__infected_duration[0],
                                                                           self.__infected_duration[1])

    # checks if node safly recovers or dies
    def recovered(self):
        test_int = random.randint(0, 100)
        if test_int < self.__zone.prob_safely_recover:
            self.set_rec(True)
        else:
            self.set_rec(False)

    # if zone has reached end of inf duration recovers node
    def can_recover(self):
        if self.__zone.current_iteration == self.rec_iter:
            return True
        else:
            return False
