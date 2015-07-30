__author__ = 'visoft'
"""
Basic data manipulation

"""

NON_NUMERIC  = ['Id','Dates','Descript','PdDistrict','DayOfWeek','Resolution','Address']
CLASS_COLUMN = 'Category'


def get_X_Y_from_dataframe(dataframe,features_to_remove = None, target_column = None):
    if features_to_remove is None:
        features_to_remove = NON_NUMERIC
    if target_column is None:
        target_column = CLASS_COLUMN

    Y = dataframe[target_column].values
    dataframe = dataframe.drop(target_column,axis=1,errors='ignore')

    X = get_X_from_dataframe(dataframe,features_to_remove)
    return X, Y

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