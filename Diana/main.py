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

#custom knn
classifier = pipe.Pipeline([
    ('clf', knn.KNeighborsClassifier(n_neighbors=3))
])
t1 = time.time()
classifier.fit(X, y)
print classifier.predict(x_test)
print "Custom knn: %.2f" % (time.time() - t1)
