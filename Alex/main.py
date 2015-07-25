__author__ = 'Amalia'

# read config file to get path of dataset
import pandas as pd
import matplotlib.pyplot as plt
import datetime as df

from enum import Enum
class Dataset(Enum):
    sample = 'sample'
    train = 'train'
    test = 'test'

def getPath(dataset):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('properties.cfg')
    path = config.get("Properties", dataset.value)
    return path

def getSamplePath():
    return getPath(Dataset.sample)
def getTestPath():
    return getPath(Dataset.test)
def getTrainPath():
    return getPath(Dataset.train)

if __name__ == "__main__":
    print getSamplePath()
    print getTrainPath()
    print getTestPath()

    train = pd.read_csv(getTrainPath(), parse_dates=['Dates'])
    train['DayOfYear'] = train['Dates'].map(lambda x: x.strftime("%m-%d"))
    df = train[['Category','DayOfYear']].groupby(['DayOfYear']).count()
    df.plot(y='Category', label='Number of events', figsize=(15,10))
    plt.title("Crimes occur with a regular pattern: two peaks per month")
    plt.ylabel('Number of crimes')
    plt.xlabel('Day of year')
    plt.grid(True)

    plt.savefig('Distribution_of_Crimes_by_DayofYear.png')
