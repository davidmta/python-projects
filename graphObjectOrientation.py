#!/usr/bin/env python
# a stacked bar plot with errorbars
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#N = 5
#menMeans   = (20, 35, 30, 35, 27)
#womenMeans = (25, 32, 34, 20, 25)
#menStd     = (2, 3, 4, 1, 2)
#womenStd   = (3, 5, 2, 3, 3)
#ind = np.arange(N)    # the x locations for the groups
#width = 0.35       # the width of the bars: can also be len(x) sequence
#
#p1 = plt.bar(ind, menMeans,   width, color='r')
#p2 = plt.bar(ind, womenMeans, width, color='y',
#             bottom=menMeans)
#
#plt.ylabel('Scores')
#plt.title('Scores by group and gender')
#plt.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
#plt.yticks(np.arange(0,81,10))
#plt.legend( (p1[0], p2[0]), ('Men', 'Women') )
#
#plt.show()

"""
    Parses through all the xml files to return a list of objects within the file.
    """

def parseFiles(annotationsPath):
    objectList = []
    # Retrieves all the files in a directory and checks if they are xml
    fileList = os.listdir(annotationsPath)
    annotationsFullPath = os.path.abspath(annotationsPath)
    for file in fileList:
        fileTypeMatch = re.search('.xml',file)
        if fileTypeMatch:
            try:
                filePath = os.path.join(annotationsFullPath, file)
                f = open(filePath)
                soup = bsoup(f)
                f.close()
                # Finds the object of all xml files and places the objects into a list
                # and returns it.
                parsedXML = (soup.findAll('name'))
                for object in parsedXML:
                    match = re.search('(<name>)(\w+)(</name>)', str(object))
                    objectList += match.group(2),
            
            except IOError:
                sys.stderr.write('There was a problem with file: ' + file + '/n')
    return objectList

"""
    Counts the number of objects and returns a list.
    The list is organized as these lines:
    [Number of Cars, Number of Persons, Number of Bicycles]
    """

def organizeObjectList(objectList):
    
    countedObjects = [0,0,0]
    for objectType in objectList:
        if objectType == 'car':
            countedObjects[0] += 1
        if objectType == 'person':
            countedObjects[1] += 1
        if objectType == 'bicycle':
            countedObjects[2] += 1
    return countedObjects

def createGraph(countedList,outputPath):
    print countedList

"""
    Creates a graph of object classes by reading files from the
    directory,annotationsPath and outputs it to outputPath
    """

def graphObjectOrientation(annotationsPath, outputPath):
    objectList = parseFiles(annotationsPath)
    countedList = organizeObjectList(objectList)
    print "Nutmeg"
    createGraph(countedList,outputPath)

"""
    Given the path, it opens the all the xml files.
    Use matlab to create a graph to a certain locations.
    Create your own directory if not present.
    Accepting the argument.
    """

def main():
    annotationsPath = raw_input("Path to the annotations?: ")
    outputPath = raw_input("Output Path?: ")
    if os.path.exists(annotationsPath) and os.path.exists(outputPath):
        graphObjectOrientation(annotationsPath,outputPath)
    
    # Error messages for broken paths.
    elif not os.path.exists(annotationsPath):
        sys.stderr.write("Error - path does not exist" + '\n')
        sys.stderr.write("annotationsPath = " + annotationsPath + '\n')
        sys.exit(1)
    elif not os.path.exists(outputPath):
        sys.stderr.write("Error - path does not exist:" + '\n')
        sys.stderr.write("outputPath = " + outputPath + '\n')
        sys.exit(1)

if __name__ == '__main__':
    main()