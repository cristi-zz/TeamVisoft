__author__ = 'Cristi'

# read config file to get path of dataset
import sf.fh as fh
import pandas as pd
import sf.basic as basic
import sklearn.naive_bayes as bayes

#Mainly taken from kaggle scripts

if __name__ == "__main__":
    #This is how you get the file name
    train_file_name = fh.get_src_path(fh.TRAIN_FILE_NAME)
    train_set = pd.read_csv(train_file_name)
    test_file_name =fh.get_src_path(fh.TEST_FILE_NAME)
    test_set = pd.read_csv(test_file_name)

    X,Y = basic.get_X_Y_from_dataframe(train_set)
    T = basic.get_X_from_dataframe(test_set)
    Id = basic.get_Id_from_test_dataframe(test_set)


    #Get a classifier. Later, it will be a pipeline
    pipeline = bayes.GaussianNB()
    pipeline.fit(X,Y)

    predicted = pipeline.predict_proba(T)
    classes = pipeline.classes_
    print "Done"





