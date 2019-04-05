# json2csv
Python script for converting .json.gz files to .csv.gz format

Specifically for converting the .json files available here:
http://jmcauley.ucsd.edu/data/amazon/
which are amazon reviews, into csv file format to make them compatible with common semantic analysis software.



### Example usage:

`>python json2csv.py mybigfile.json.gz 1000000`

converts the gzipped json file `mybigfile.json.gz` into multiple csv files of length 1000000 rows, called `mybigfile1.csv`, `mybigfile2.csv`, `mybigfile3.csv`...