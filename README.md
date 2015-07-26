# README #

First steps to set up your env and run the scripts

### Tools (Not carved in stone) ###
* Anaconda as python distribution
* Git extensions
* PyCharm as IDE

### How do I get set up? ###

* Install anaconda distribution
* Edit paths, reboot, etc. so that the python gets executed from anaconda distribution
* Run:
```
    conda update -f conda
    conda install scikit-learn
    conda install pandas
    conda install pytest
```
* Upload SSH keys to bitbucket (if not already there)
* Clone the repo
* Copy the sf_crime_properties.cfg.sample in your HOME directory, edit the paths accordingly and remove the .sample extension
* Edit PYTHONPATH env variable to include "teamvisoft\src" folder (ex: d:\ML\teamvisoft\src)
* Go to d:\ML\teamvisoft and write in a console: `py.test tests\test_fh.py`. It should be green


### Set up pycharm ###
Configure the interpreter to Anaconda distribution
Right click src folder and select Mark directory as Source Root
go to File/Settings, "Build,Exec,Deploy", console, python console and set working directory to teamvisoft\src. Also thick Add content roots to PYTHONPATH
Go to File/Settings, Tools, Python Integration Tools and select py.test as default test runner.
Go to tests/test_fh, right click and select "Run py.test in test_fh . . ." It should be green


### What is this repository for? ###
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)