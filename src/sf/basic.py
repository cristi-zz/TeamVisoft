__author__ = 'visoft'
"""
Basic data manipulation

"""

import pandas as pd

NON_NUMERIC  = ['Id','Dates','Descript','PdDistrict','DayOfWeek','Resolution','Address']
CLASS_COLUMN = 'Category'


def get_X_Y_class_labels_from_dataframe(dataframe,features_to_remove = None, target_column = None):
    if features_to_remove is None:
        features_to_remove = NON_NUMERIC
    if target_column is None:
        target_column = CLASS_COLUMN

    #Get sorted class labels and in Y use only indexes

    class_labels = dataframe[target_column].unique()
    class_labels.sort()
    class_labels_dict = {class_labels[i]:i for i in range(len(class_labels)) }
    Y_lables = dataframe[target_column]
    Y = Y_lables.map(lambda x: class_labels_dict[x])

    dataframe = dataframe.drop(target_column,axis=1,errors='ignore')

    X = get_X_from_dataframe(dataframe,features_to_remove)
    return X, Y,class_labels

def get_X_from_dataframe(dataframe,features_to_remove = None):
    """
    Remove everything that can't be used (i.e. non numeric values)
    :param dataframe:
    :param features_to_remove:
    :return:
    """
    if features_to_remove is None:
        features_to_remove = NON_NUMERIC

    X = dataframe.drop(features_to_remove, axis=1,errors='ignore')

    return X
def get_Id_from_test_dataframe(dataframe):
    Id = dataframe['Id'].values
    return Id

def build_pandas_output(id,predicted,class_labels):
    output = pd.DataFrame({'Id':id})
    for i in range(predicted.shape[1]):
        column = predicted[:,i]
        key = class_labels[i]
        output[key] = column
    return output