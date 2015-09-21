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
    X = [[0], [1], [2], [3]]
    y = sorted(['alb', 'alb', 'b', 'b'])
    x_test = np.array([[2]])

    neigh = ngh.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree')
    neigh.fit(X, y)
    result = neigh.predict(x_test)

    print result

    classifier = pipe.Pipeline([
        ('clf', knn.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree'))
    ])
    classifier.fit(X, y)
    custom_result = classifier.predict(x_test)

    print custom_result

    assert np.array_equal(result, custom_result)

def test_predict_proba():
    X = [[0], [1], [2], [3]]
    y = sorted(['alb', 'alb', 'b', 'b'])
    x_test = np.array([[2]])

    neigh = ngh.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree')
    neigh.fit(X, y)
    result = neigh.predict_proba(x_test)

    classifier = pipe.Pipeline([
        ('clf', knn.KNeighborsClassifier(n_neighbors=3, algorithm='kd_tree'))
    ])
    classifier.fit(X, y)
    custom_result = classifier.predict_proba(x_test)

    assert np.array_equal(result, custom_result)