__author__ = 'visoft'
"""
Module that is used to estimate the performace. It reproduces sklearn tools but with a twist.
Exposes some intermediate steps so one can easily distribute the experiment using whatever infrastructure

Basically, takes RandomizedSearchCV from sklearn and explodes it.

"""

from sklearn.cross_validation import _fit_and_score
from sklearn.grid_search import ParameterSampler
from operator import attrgetter,itemgetter

class Job:
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
        train_score, test_score, n_test_samples, scoring_time, params = _fit_and_score(self.estimator, X, Y, self.scorer,
                                                                                       self.train_index, self.test_index,
                                                                                       self.verbose,
                                                                                       self.meta_parameter_set,
                                                                                       None, self.eval_on_training)
        self.train_score = train_score
        self.test_score = test_score
        self.scoring_time = scoring_time

    def get_unique_token(self):
        return (self.tok_id, self.iteration_no, self.fold_no)



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
    for i in range(meta_param_list):
        for j in range(train_test_pairs):
            train,test = train_test_pairs[j]
            job = Job(token,i,j,estimator,scorer,meta_param_list[i],eval_on_training,train,test,verbose)
            jobs.append(job)
    return jobs


def run_jobs_serial(jobs,X,Y):
    for job in jobs:
        job.run(X,Y)


def accumulate_results(jobs, is_loss=False):
    """

    :param jobs:
    :param is_loss: if True, will return the parameter set that minimizes the test performance
    :return: dictionary with tokens as keys tuple values containing in order train, test performances, total time and meta parameter set
    """
    #Get an unique set of tokens
    tokens = set(map(lambda job:job.tok_id,jobs))
    result = {}
    for token in tokens:
        #filter only those jobs having the right token
        job_list = filter(lambda job:job.tok_id == token, jobs)
        #find unique iteration numbers (each iteration have one meta parameter)
        iterations = set(map(lambda job:job.iteration_no), job_list)
        performances = list()
        for iteration in iterations:
            jobs_one_cv_loop = filter(lambda job:job.iteration_no == iteration, job_list)
            train_perf = 0
            test_perf = 0
            total_time = 0
            for job in jobs_one_cv_loop:
                train_perf += job.train_score
                test_perf += job.test_score
                total_time += job.scoring_time
            job = jobs_one_cv_loop[0]
            performances.append((train_perf,test_perf,total_time,job.meta_parameter_set))
        #Get the best iteration
        if is_loss:
            bp = min(performances,itemgetter(1))
        else:
            bp = max(performances,itemgetter(1))
        result[token] = bp
    return result