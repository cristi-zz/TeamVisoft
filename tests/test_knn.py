__author__ = 'Diana'

import sf.knn as knn
import sklearn.datasets as dts
import numpy as np
import sklearn.neighbors as ngh
import sklearn.pipeline as pipe

def test_load_datasets():
    iris = dts.load_iris()
    X = iris.data[:, :2]
    y = iris.target
    assert X is not None
    assert y is not None

def test_custom_knn():
    iris = dts.load_iris()
    X = iris.data[:, :2]
    y = iris.target
    x_test = np.array([[5., 3.5], [5., 1.], [5., 3.2], [5.1, 3.5]])

    neigh = ngh.KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X, y)
    result = neigh.predict(x_test)

    classifier = pipe.Pipeline([
        ('clf', knn.KNeighborsClassifier(n_neighbors=3))
    ])
    classifier.fit(X, y)
    custom_result = classifier.predict(x_test)

    assert np.array_equal(result, custom_result)
