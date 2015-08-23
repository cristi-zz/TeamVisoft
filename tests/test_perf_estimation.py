__author__ = 'visoft'
"""
Example on how to build, run and analyse a random search job list.

The scorer and CV generator can be replaced with different options.

For SF data, you want to use something like train/test splitting, randomized at first, and then, one week at a time

"""

import sklearn.metrics as metrics
import sklearn.cross_validation as cross_validation
import sklearn.datasets
import sklearn.metrics.scorer

import sf.perf_estimation as perf_estimation
import sf.estimators as estimators


def generate_jobs_with_two_estimators(Y):

    scorer = sklearn.metrics.scorer.get_scorer('log_loss') #Because sklearn
    cv_gen = cross_validation.StratifiedKFold(Y,n_folds=5)

    pipe,meta = estimators.get_classic_svm()
    jobs1 = perf_estimation.get_random_search_cv_job_list(pipe,scorer,cv_gen,True,meta,10,1,True)

    pipe,meta = estimators.get_random_forest()
    jobs2 = perf_estimation.get_random_search_cv_job_list(pipe,scorer,cv_gen,True,meta,10,2,True)

    jobs = jobs1 + jobs2

    return jobs

def test_jobs_on_iris():
    iris = sklearn.datasets.load_iris()
    X = iris.data
    Y = iris.target

    jobs = generate_jobs_with_two_estimators(Y)

    results = perf_estimation.run_jobs_serial(jobs,X,Y)  #TODO Implement something in parallel

    aggregation = perf_estimation.accumulate_results(results)
    print "\n"
    for k,v in aggregation.items():
        print "set {0} train {1} test {2} time {3}\n".format(k,v[0],v[1],v[2])









