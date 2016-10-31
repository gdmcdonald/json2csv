import json
import csv
import gzip
import time

#input .json.gz file
inputFileName='aggressive_dedup.json.gz'

#remove last 8 charachters to get file name without extentions
fileNameRoot=inputFileName[:-8]

#max lines to output in a single csv file
maxLines=3000000

fileNumber=0

#count lines and read in field names on first pass
with gzip.open (inputFileName,'r') as jsonfile:
    linecounter=0
    t0 = time.time()
    for line in jsonfile:
        lineDictionary=eval(line)
        linecounter+=1
        break
    #fieldnames=[key for key, value in lineDictionary.items()] #random order, let's go back to hard coded
    for line in jsonfile:
        linecounter+=1
    t1 = time.time()
    #print(str(t1-t0)+" seconds")
    print(str(linecounter)+" lines to convert to csv.")

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

    while 1==1:
        fileNumber+=1
        outputFileName=inputFileName+'_output'+str(fileNumber)+'.csv'
        counter=0
        totalLines=counter+(fileNumber-1)*maxLines
        if totalLines<linecounter:
            with open(outputFileName, 'w') as csvfile:
                spamwriter = csv.DictWriter(csvfile,
                                            fieldnames=fieldnames)
                spamwriter.writeheader()

                t0 = time.time()
                for line in jsonfile:
                    lineDictionary=eval(line)
                    spamwriter.writerow(lineDictionary)
                    counter+=1
                    totalLines=counter+(fileNumber-1)*maxLines
                    print(str(totalLines)+" lines converted, %0.0f" % (totalLines/linecounter*100) +"% done.", end='\r')
                    if counter==maxLines:
                        break
                t1 = time.time()
                print("File number "+str(fileNumber)+ " took %.2f" % (t1-t0)+ " seconds.                                ")
        else:
            break
