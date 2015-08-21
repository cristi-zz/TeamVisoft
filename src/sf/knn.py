__author__ = 'Diana'

import math
import collections

#distance between p1 and p2
def getDistance( p1, p2 ):
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

    def __init__(self):
        self.n_neighbors = 1

    def __init__(self, n_neighbors):
        self.n_neighbors = n_neighbors

    def fit(self, x, y):
        self.x = x
        self.y = y

    #returns the distances list between the transmitted value and each element of training data set
    def distances(self, val):
        dist = []
        for elem in self.x :
            dist.append(getDistance(elem, val))
        return dist

    #returns the distances and the corresponding indexes
    def kneighbors(self, val):
        indices = []
        distances = self.distances(val)
        sorted_indexes = sorted(range(len(distances)), key=lambda k: distances[k])
        for index in range(0, self.n_neighbors):
            indices.append(sorted_indexes[index])
        return distances, indices

    #returns the predicted values list for the transmitted value
    def predict(self, val):
        predicted = []
        for elem in val:
            distances, indices = self.kneighbors(elem)
            #used to store the frequency of each target value found in neighbors
            #collections - used in order to keep the data structure ordered
            frequencies = collections.OrderedDict()
            for index in indices:
                if frequencies.has_key(self.y[index]):
                    frequencies[self.y[index]] += 1
                else:
                    frequencies[self.y[index]] = 0

            #sort target values by frequency
            frequencies = sorted(frequencies.items(), key=lambda x: x[1])
            #add most frequent target value to the result
            predicted.append(frequencies[-1][0])
        return predicted







