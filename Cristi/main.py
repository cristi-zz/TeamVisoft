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

    X,Y,class_labels = basic.get_X_Y_class_labels_from_dataframe(train_set)
    T = basic.get_X_from_dataframe(test_set)
    Id = basic.get_Id_from_test_dataframe(test_set)


    #Get a classifier. Later, it will be a pipeline
    pipeline = bayes.GaussianNB()

    #TODO tune pipeline metaparameters.
    #The most time consuming part! We have to be really creative here!


    #Once the metaparameters were found, set them and fit ("learn") the training set
    pipeline.fit(X,Y)

    #Sometimes a little time consuming but not very much
    predicted_proba = pipeline.predict_proba(T)

    #Build nicely the pandas so we can write a nice csv
    output = basic.build_pandas_output(Id,predicted_proba,class_labels)

    output_file_name = fh.get_out_path("cv_Prediction_Attempt_01.08.2015.csv")
    output.to_csv(output_file_name,index=False)

    #Write the file, ready to be submitted
    print "Done"





