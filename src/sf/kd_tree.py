from collections import namedtuple
from operator import itemgetter
from pprint import pformat

__author__ = 'Diana'

import collections
import pprint
import operator

class Node(namedtuple('Node', 'root left right')):
    def __repr__(self):
        return pformat(tuple(self))

class KdTree():
    points = []

    def __init__(self, points_list):
        self.points = points_list

    def build_tree(self):
        tree = self.kd_tree(self.points, 0)
        return tree

    def kd_tree(self, points, depth):
        try:
            dim = len(points[0]) # dim = 2 for points like (x, y)
        except IndexError as er:
            return None

        #determine which axis to use
        x_y = depth % dim

        #sort points by corresponding axis
        points.sort(key = itemgetter(x_y))
        median = len(points) / 2

        return Node(
            root = points[median],
            left = self.kd_tree([points[i] for i in range (0, median)], depth+1),
            right = self.kd_tree([points[i] for i in range (median+1, len(points))], depth+1)
        )

    def nearest_neighbor(self, tree, target, best_dist, depth):

        #stop condition
        if tree is None:
           return ((float("inf"),float("inf")), float("inf"))

        dim = len(tree.root)
        #find corresponding axis
        x_y = depth % dim

        #find the subtree for the recursive call by comparing the root and the target
        if target[x_y] < tree.root[x_y]:
            next_tree = tree.left
            possible_tree = tree.right
        else:
            next_tree = tree.right
            possible_tree = tree.left

        #nearest neighbor and its corresponding distance from the subtree
        (nearest, best_dist) = self.nearest_neighbor(next_tree, target, best_dist, depth+1)

        #find distance from root to target point
        current_distance = self.get_distance(target, tree.root)

        if current_distance < best_dist:
            best_dist = current_distance
            nearest = tree.root

        #check if it's possible that a nearest point will be found in the other subtree
        d = (target[x_y] - tree.root[x_y]) ** 2

        if d > best_dist:
            return (nearest, best_dist)

        #check the other subtree
        (nearest2, best_dist2) = self.nearest_neighbor(possible_tree, target, best_dist, depth+1)

        #return the best result
        if best_dist2 < best_dist:
            return (nearest2, best_dist2)

        return (nearest, best_dist)

    def get_distance( self, p1, p2 ):
        sum = 0
        for index in range(0, len(p2)):
            sum += (p2[index] - p1[index]) ** 2
        return sum

