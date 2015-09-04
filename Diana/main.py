__author__ = 'Diana'

import pandas as pd
import matplotlib.pyplot as plt
import datetime as df
import numpy as np
import sf.fh as fh
import sklearn.neighbors as ngh
import math
import sf.knn as knn
import sklearn.pipeline as pipe
import sklearn.datasets as dts
import time
import sf.kd_tree as kd_tree

# iris = dts.load_iris()
# X = iris.data[:, :2]
# y = iris.target
#
# #sklearn knn
# x_test = np.array([[5., 3.5], [5., 1.], [5., 3.2], [5.1, 3.5]])
# neigh = ngh.KNeighborsClassifier(n_neighbors=3)
# t1 = time.time()
# neigh.fit(X, y)
# print(neigh.predict(x_test))
# print "Sklearn knn: %.2f" % (time.time() - t1)
# print neigh.predict_proba(x_test)
#
# #custom knn
# classifier = pipe.Pipeline([
#     ('clf', knn.KNeighborsClassifier(n_neighbors=3))
# ])
# t1 = time.time()
# classifier.fit(X, y)
# print classifier.predict(x_test)
# print "Custom knn: %.2f" % (time.time() - t1)
#
# #another set of data
X = [[0], [1], [2], [3]]
y = [1, 2, 0, 0]
neigh = ngh.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree')
neigh.fit(X, y)

print(neigh.predict([[2], [1.1]]))
print(neigh.predict_proba([[2], [1.1]]))

print "Custom"

classifier = pipe.Pipeline([
    ('clf', knn.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree'))
])
classifier.fit(X, y)
print classifier.predict([[2], [1.1]])
print classifier.predict_proba([[2], [1.1]])

# points = [(7,2), (8, 1), (4, 7), (9, 6), (5, 7), (3, 7)]
# print points
# kneighbors = []
#
# for i in range(0, 3):
#     tree = kd_tree.KdTree(points)
#     kdtree = tree.build_tree()
#     (nearest, best_dist) = tree.nearest_neighbor(kdtree, (3, 7), float("inf"), 0)
#     kneighbors.append(nearest)
#     points.remove(nearest)
#
# print(kneighbors)
#
# X = [[7,2], [8, 1], [4, 7], [3, 7]]
# y = [1, 2, 0, 0]
# tree = kd_tree.KdTree(X)
# kdtree = tree.build_tree()
# print tree.nearest_neighbor(kdtree, [3,7], float("inf"), 0)