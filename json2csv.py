import csv
import gzip
import time

#input .json.gz file, in the same folder as this python script.
inputFileName='reviews_Electronics_5.json.gz'

#remove last 8 charachters (".json.gz") to get file name without extentions
fileNameRoot=inputFileName[:-8]

#max lines to output in a single csv file
linesPerOutputFile=3000000

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

fieldnames=['reviewTime',
             'overall',
             'reviewerID',
             'reviewerName',
             'unixReviewTime',
             'asin',
             'reviewText',
             'summary',
             'helpful']



#convert to multiple csv files on second pass
with gzip.open (inputFileName,'r') as jsonfile:

    while 1 == 1:
        fileNumber += 1
        outputFileName = inputFileName + '_output' + str(fileNumber) + '.csv'
        countOfLinesInThisFile = 0
        linesDoneSoFar = countOfLinesInThisFile + (fileNumber - 1) * linesPerOutputFile
        if linesDoneSoFar < totalLinesInInputFile:
            with open(outputFileName, 'w') as csvfile:
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
