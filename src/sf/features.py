__author__ = 'visoft'

"""
Various feature generators
Each function take a pandas dataset and adds new columns to it.
It first checks if the source column is present.


todo:
1) Generate week and month number continuously by ignoring the year passing. Ex:
1 ian 2000  week 1
8 ian 2000   week 2
2 feb 2000   week 5
1 ian 2001  week 53
etc

the idea is to take from test set month 48 and look only at crimes from month 47 and 49 without worrying  that 48 is jan and 47 is dec last year.


2) extract day of week (values 1-7)

3) extract day label as "one hot encoding" : working day, weekend, holiday. For holiday I don;t know how to do it automatically

4) extract the season (values 1-4)

5) extract one hot encoding the time of day: night, morning rush hour, morning, noon,afternoon rush hour, everning.


"""



