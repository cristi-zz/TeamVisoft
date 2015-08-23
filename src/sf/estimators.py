__author__ = 'visoft'
"""
  Keeps track of the pipelines.
  Each pipeline generator should return the actual pipeline and the dictionary with the tunable metaparameters.
"""
import sklearn.svm
import sklearn.pipeline
import sklearn.ensemble
import scipy.stats as stats


def get_classic_svm():
    """
    Builds a normalizer+SVM

    :return pipeline: constructed pipeline
    :return meta_dict: dictionary with tunable metaparameters and random generators for their range
    """
    # Normalize the data
    scaler = sklearn.preprocessing.MinMaxScaler((0, 1), False)
    classifier = sklearn.svm.SVC(C=100, kernel='rbf', gamma=0.11, probability=True, class_weight={0: 1, 1: 1},)
    pipeline = sklearn.pipeline.Pipeline(
        [('standardization', scaler), ('SVC_rbf', classifier)])

    meta_dict = {'SVC_rbf__C':stats.uniform(1,100),
                   'SVC_rbf__gamma':stats.expon()}

    return pipeline,meta_dict


def get_random_forest():
    classifier = sklearn.ensemble.RandomForestClassifier(max_features=None,oob_score=False,n_jobs=1)
    pipeline = sklearn.pipeline.Pipeline([('RF',classifier)])

    meta_dict={'RF__n_estimators':stats.randint(5,100),'RF__max_features':['sqrt','log2','auto',None],
               'RF__max_depth':stats.randint(2,10)}

    return pipeline,meta_dict

