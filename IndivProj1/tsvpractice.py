# Author: Artiom Dolghi
# TSV Practice
# Due 2/20/2020

from csv import writer
from csv import reader

with open('freqs.tsv', 'r') as readFile, \
        open('freqs-mean.tsv', 'w', newline='') as writeFile:

    csv_reader = reader(readFile, delimiter = '\t')

    csv_writer = writer(writeFile, delimiter = '\t')
    
    for row in csv_reader:
        
        rowList = list(row)
        
        rowList.pop(0) # removing the word
        
        while (" " in rowList): # removing unnecessary characters
            rowList.remove(" ")
        while ("" in rowList):
            rowList.remove("")
        
        sumRow = 0.0
        
        for element in rowList:
            sumRow += float(element)
        
        try:
            mean = sumRow / len(rowList)
        except:
            mean = 0.0

        row.append(mean)

        csv_writer.writerow(row)