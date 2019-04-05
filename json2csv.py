#--
# json2csv version 0.2
# Description: This script converts compressed json .json.gz files into
# compressed csv .csv.gz files
#
# Example usage:
# >python  json2csv.py mybigfile.json.gz 1000000
# converts the gzipped json file "mybigfile.json.gz" into multiple gzipped csv files of length 1000000 rows
#
# Caveat: to avoid random column order, field names are hardcoded below.
#
# Author: Gordon McDonald
# gordon.mcdonald@sydney.edu.au
#
# Date last modified: 5/Apr/2019
#
# If you use this script towards a publication, please acknowledge the
# Sydney Informatics Hub.
#
# Suggested acknowledgement:
# “This research was supported by the Sydney Informatics Hub, a Core Research Facility of the University of Sydney.”
#--



import csv
import gzip
import time
import sys
from pathlib import Path

#input .json.gz file, in the same folder as this python script.
inputFileName=sys.argv[1]

#remove last 8 charachters (".json.gz") to get file name without extentions
fileNameRoot=Path(inputFileName).stem

#max lines to output in a single csv file
if (len(sys.argv)>2):
    linesPerOutputFile= int(sys.argv[2])
else:
    linesPerOutputFile=1000000

#hardcoded field names.....sob
fieldnames=['reviewTime',
             'overall',
             'reviewerID',
             'reviewerName',
             'unixReviewTime',
             'asin',
             'reviewText',
             'summary',
             'helpful']

#initialize the output file number at zero
fileNumber=0

#count lines and read in field names on first pass
with gzip.open (inputFileName,'r') as jsonfile:
    totalLinesInInputFile=0
    t0 = time.time()
    for line in jsonfile:
        lineDictionary=eval(line)
        totalLinesInInputFile+=1
        break
    #fieldnames=[key for key, value in lineDictionary.items()]
    #this makes the fields save in random order in the output csv, let's go back to hard coded
    for line in jsonfile:
        totalLinesInInputFile+=1
    t1 = time.time()
    #print(str(t1-t0)+" seconds")
    print(str(totalLinesInInputFile)+" lines to convert to csv.")


#convert to multiple csv files on second pass
with gzip.open (inputFileName,'r') as jsonfile:

    while 1 == 1:
        fileNumber += 1
        outputFileName = fileNameRoot + str(fileNumber) + '.csv.gz'
        countOfLinesInThisFile = 0
        linesDoneSoFar = countOfLinesInThisFile + (fileNumber - 1) * linesPerOutputFile
        if linesDoneSoFar < totalLinesInInputFile:
            with gzip.open(outputFileName, 'wt') as csvfile:
                OutputCsvFileWriter = csv.DictWriter(csvfile,
                                            fieldnames=fieldnames)
                OutputCsvFileWriter.writeheader()

                t0 = time.time()
                for line in jsonfile:
                    #evaluate the line of json, which will make it a python dictionary.
                    lineDictionary=eval(line)
                    OutputCsvFileWriter.writerow(lineDictionary)
                    countOfLinesInThisFile+=1
                    linesDoneSoFar = countOfLinesInThisFile + (fileNumber - 1) * linesPerOutputFile
                    print(str(linesDoneSoFar) + " lines converted, %0.0f" % (linesDoneSoFar / totalLinesInInputFile * 100) + "% done.", end='\r')
                    if countOfLinesInThisFile == linesPerOutputFile:
                        break
                t1 = time.time()
                print("File number " + str(fileNumber) + " took %.2f" % (t1-t0) + " seconds.                                ")
        else:
            break
