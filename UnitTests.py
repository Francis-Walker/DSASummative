import unittest
from Zone import *
from Node import *

#check the constraint that the number of nodes remains constant
def zone_size_test():
    zone = Zone(num_nodes=50)
    check = True
    for i in range(1000):
        zone.iteration()
        data = zone.map_data()
        if not data[0] + data[1] + data[2] + data[3] == 50:
            check = False
    return check

#check the constraint that a node can't move outside a zones area
def zone_node_constrained():
    x = 10
    y = 10
    zone = Zone(size_x=x, size_y=y)
    node = Node(zone)
    check = True
    for i in range(1000):
        node.step()
        if (node.print_postion()[0] < 0 or node.print_postion()[0] > x) or (
                node.print_postion()[1] < 0 or node.print_postion()[1] > y):
            check = False
    return check


class Test(unittest.TestCase):

    #check that no node can exist with out zone
    def node_with_no_zone(self):
        with self.assertRaises(Exception): node = Node()

    def checkConstraint(self):
        self.assertEqual(zone_size_test(),True)
        self.assertEqual(zone_node_constrained(),True)


# outer_check = True
# for i in range(50):
#     outer_check*=zone_size_test()
# print(outer_check)

# outer_check = True
# for i in range(50):
#     outer_check*=zone_node_constrained()
# print(outer_check)


if __name__ == "__main__":
    test = Test()
    test.checkConstraint()
    test.node_with_no_zone()