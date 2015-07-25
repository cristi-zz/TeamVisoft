__author__ = 'Amalia'

# read config file to get path of dataset

def getPathOfDataset():
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('properties.cfg')
    path = config.get("Properties", "datasetPath")
    return path

if __name__ == "__main__":
    print getPathOfDataset()