__author__ = 'visoft'
"""
File finding utility
File constants (names of the datasets, etc
Config object loading
"""
import ConfigParser
import os.path

DEFAULT_CONFIG_FILE_NAME='sf_crime_properties.cfg'
SOURCE_DIR_NAME='source_dir'
OUTPUT_DIR_NAME='out_dir'

#TODO to be moved in data generation
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

#TODO add here more constants with the file names (ex. training data, test data, generated data by us, etc)


def getUserFolder():
    return os.path.expanduser("~")

class LocalConfig():
    """
    Stores the local paths to the datasets
    """
    def __init__(self):
        pass

    def parseConfigFile(self):
        config = ConfigParser.ConfigParser()
        cfg_file = os.path.join(getUserFolder(),DEFAULT_CONFIG_FILE_NAME)
        config.read(cfg_file)
        self.source_dir = config.get("Properties", SOURCE_DIR_NAME)
        self.out_dir = config.get("Properties", OUTPUT_DIR_NAME)


#Just create an object
localConfigObject = LocalConfig()
localConfigObject.parseConfigFile()

#some shortcut functions
def get_src_path(relative_file_name):
    path = os.path.join(localConfigObject.source_dir,relative_file_name)
    return path

def get_out_path(relative_file_name,user=""):
    path = os.path.join(localConfigObject.out_dir,user,relative_file_name)
    return path
