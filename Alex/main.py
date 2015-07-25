__author__ = 'Amalia'

# read config file to get path of dataset

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
