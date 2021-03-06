__author__ = 'visoft'
"""
Module that is used to estimate the performace. It reproduces sklearn tools but with a twist.
Exposes some intermediate steps so one can easily distribute the experiment using whatever infrastructure

Basically, takes RandomizedSearchCV from sklearn and explodes it.

"""

from sklearn.cross_validation import _fit_and_score
from sklearn.grid_search import ParameterSampler
from operator import attrgetter,itemgetter

__all__ = ['Job','get_random_search_cv_job_list','run_jobs_serial','accumulate_results']


class Job:
    """
    Class that holds details about a job that has to be run.
    Run it on some remote worker or another thread.
    Once the job is run, a Result object is returned that can be passed back

    A job is identified by a token formed by:
    tok_id: passed as is to the result,
    iteration_no: have the same meaning as RandomizedSearch. That is, the metaparameter set number that is curently tested
    fold_no: the CV fold that is currently fitted and predicted. For each meta set you run a CV loop.
    In the results, all three numbers are packed into a tuple
    """
    def __init__(self, tok_id, iteration_no, fold_no, estimator, scorer, meta_parameter_set, eval_on_training,
                 train_index, test_index,
                 verbose
                 ):
        """
        :param tok_id:
        :param iteration_no:
        :param fold_no:
        :param estimator:
        :param scorer:
        :param meta_parameter_set:
        :param eval_on_training:
        :param train_index:
        :param test_index:
        :param verbose:
        :return:
        """
        self.tok_id = tok_id
        self.iteration_no = iteration_no
        self.fold_no = fold_no
        self.estimator = estimator
        self.scorer = scorer
        self.meta_parameter_set = meta_parameter_set
        self.eval_on_training = eval_on_training
        self.train_index = train_index
        self.test_index = test_index
        self.verbose = verbose


    def run(self,X, Y):
        """
        Lengthly and compute intensive part.
        Returns a Result object
        """
        train_score, test_score, n_test_samples, scoring_time = _fit_and_score(self.estimator, X, Y, self.scorer,
                                                                                       self.train_index, self.test_index,
                                                                                       self.verbose,
                                                                                       self.meta_parameter_set,
                                                                                               None, self.eval_on_training)
        return Result(self.get_unique_token(),train_score,test_score,scoring_time,self.meta_parameter_set)

    def get_unique_token(self):
        return (self.tok_id, self.iteration_no, self.fold_no)



class Result:
    """
    Keeps the results of a job. The token packs all the information passed in the job (tok_id, iteration_no, fold_no)
    """
    def __init__(self,token,train_score,test_score,scoring_time,meta_parameter_set):
        self.token = token
        self.train_score = train_score
        self.test_score = test_score
        self.scoring_time = scoring_time
        self.meta_parameter_set = meta_parameter_set


def get_random_search_cv_job_list(estimator,scorer,cv_generator,eval_on_training,meta_parameter_dist,no_samples,token,verbose=True):
    """

    The intent of the token is to allow one to run several random searches simultaneously. You can test several estimators,
    or several cv generation methods or repeat the random cv search several times etc.
    Each of these tasks can have an unique token. The results will be aggregated wrt to these tokens.

    :param estimator:
    :param scorer:
    :param cv_generator:
    :param eval_on_training:
    :param meta_parameter_dist:
    :param no_samples:
    :param token: A numeric ID or tuple that uniquely identifies this random search.
    :param verbose:
    :return:
    """
    meta_param_list = list(ParameterSampler(meta_parameter_dist,no_samples))
    train_test_pairs = list(cv_generator)
    jobs = list()
    for i in range(len(meta_param_list)):
        for j in range(len(train_test_pairs)):
            train,test = train_test_pairs[j]
            job = Job(token,i,j,estimator,scorer,meta_param_list[i],eval_on_training,train,test,verbose)
            jobs.append(job)
    return jobs


def run_jobs_serial(jobs,X,Y):
    """
    Just takes each job and runs it. Mainly for testing purposes.
    Returns a list of results.

    This behavior must be kept by other implementations too

    :param jobs:
    :param X:
    :param Y:
    :return:
    """
    results = list()
    for job in jobs:
        r = job.run(X,Y)
        results.append(r)
    return results


def accumulate_results(results):
    """
    Aggregate the results and for each tok_id find the best metaparameter set (the best iteration_no)
    All performance metrics are supposed to be "greater is better" and for those that are "less is better" the sklearn negates the results.
    So for log_loss, you get a negative result.

    :param results:
    :return: dictionary with tokens as keys tuple values containing in order train, test performances, total time and meta parameter set
    """
    #Get an unique set of tokens
    tokens = set(map(lambda r:r.token[0],results))
    aggregation = {}
    for token in tokens:
        #filter only those jobs having the right token
        result_list = filter(lambda r:r.token[0] == token, results)
        #find unique iteration numbers (each iteration have one meta parameter)
        iterations = set(map(lambda r:r.token[1], result_list))
        performances = list()
        for iteration in iterations:
            results_one_cv_loop = filter(lambda r:r.token[1] == iteration, result_list)
            train_perf = 0
            test_perf = 0
            total_time = 0
            for job in results_one_cv_loop:
                train_perf += job.train_score
                test_perf += job.test_score
                total_time += job.scoring_time
            count = len(results_one_cv_loop)
            result = results_one_cv_loop[0]
            performances.append((train_perf/count,test_perf/count,total_time,result.meta_parameter_set))
        bp = max(performances,key = lambda p:p[1])
        aggregation[token] = bp
    return aggregation