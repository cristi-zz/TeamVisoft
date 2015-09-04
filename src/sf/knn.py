__author__ = 'Diana'

import math
import collections
import numpy as np
import sf.kd_tree as kd_tree

#distance between p1 and p2
def get_distance( p1, p2 ):
 sum = 0
 for index in range(0, len(p2)):
     sum += (p2[index] - p1[index]) ** 2
 return math.sqrt(sum)

class KNeighborsClassifier():
    n_neighbors = 1
    #training data
    x = []
    #target values
    y = []
    #algorithm
    algorithm = '';

    def __init__(self):
        self.n_neighbors = 1

    def __init__(self, n_neighbors):
        self.n_neighbors = n_neighbors

    def __init__(self, n_neighbors, algorithm):
        self.n_neighbors = n_neighbors
        self.algorithm = algorithm

    def fit(self, x, y):
        self.x = x
        self.y = y

    #returns the distances list between the transmitted value and each element of training data set
    def distances(self, val):
        dist = []
        for elem in self.x :
            dist.append(get_distance(elem, val))
        return dist

    #returns the distances and the corresponding indexes
    def kneighbors(self, val):
        indices = []

        if self.algorithm == 'kd_tree':
            distances = []
            tree = kd_tree.KdTree(self.x)
            kdtree = tree.build_tree()
            (point, index, distance) = tree.nearest_neighbor(kdtree, val, float("inf"), 0)
            indices.append(index)
            distances.append(distance)
        else:
            #algorithm = auto
            distances = self.distances(val)
            sorted_indexes = sorted(range(len(distances)), key=lambda k: distances[k])
            for index in range(0, self.n_neighbors):
                indices.append(sorted_indexes[index])

        return np.array(distances), np.array(indices)

    #returns the predicted values list for the transmitted value
    def predict(self, val):
        predicted = []
        for elem in val:
            distances, indices = self.kneighbors(elem)
            frequencies = self.get_frequencies_of_target_values(indices)
            #sort target values by frequency
            frequencies = sorted(frequencies.items(), key=lambda x: x[1])
            #add most frequent target value to the result
            predicted.append(frequencies[-1][0])
        return np.array(predicted)

    def get_frequencies_of_target_values(self, indices):
        #used to store the frequency of each target value found in neighbors
        #collections - used in order to keep the data structure ordered
        frequencies = collections.OrderedDict()
        for index in indices:
            if frequencies.has_key(self.y[index]):
                frequencies[self.y[index]] += 1
            else:
                frequencies[self.y[index]] = 1
        return frequencies

    def predict_proba(self, val):
        predict_proba = []
        #get unique target values
        target_values = set(self.y)
        for elem in val:
            predict_proba_aux = []
            distances, indices = self.kneighbors(elem)
            frequencies = self.get_frequencies_of_target_values(indices)
            for target_value in target_values:
                found = 0
                for value in frequencies.items():
                    if target_value == value[0]:
                        found = 1
                        predict_proba_aux.append(float(value[1])/self.n_neighbors)
                        break
                if found == 0:
                    predict_proba_aux.append(0.0)
            predict_proba.append(predict_proba_aux)
        return np.array(predict_proba)






