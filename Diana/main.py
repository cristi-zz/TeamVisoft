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

iris = dts.load_iris()
X = iris.data[:, :2]
y = iris.target

#sklearn knn
x_test = np.array([[5., 3.5], [5., 1.], [5., 3.2], [5.1, 3.5]])
neigh = ngh.KNeighborsClassifier(n_neighbors=3)
t1 = time.time()
neigh.fit(X, y)
print(neigh.predict(x_test))
print "Sklearn knn: %.2f" % (time.time() - t1)
print neigh.predict_proba(x_test)

#custom knn
classifier = pipe.Pipeline([
    ('clf', knn.KNeighborsClassifier(n_neighbors=3))
])
t1 = time.time()
classifier.fit(X, y)
print classifier.predict(x_test)
print "Custom knn: %.2f" % (time.time() - t1)

#another set of data 
X = [[0], [1], [2], [3]]
y = [1, 2, 0, 0]
neigh = ngh.KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)

print(neigh.predict([[2], [1.1]]))
print(neigh.predict_proba([[2], [1.1]]))

print "Custom"

classifier = pipe.Pipeline([
    ('clf', knn.KNeighborsClassifier(n_neighbors=3))
])
classifier.fit(X, y)
print classifier.predict([[2], [1.1]])
print classifier.predict_proba([[2], [1.1]])