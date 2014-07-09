#!/usr/bin/env python
# a stacked bar plot with errorbars
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

"""
    Parses through all the xml files to return a list of objects within the file.
    Returns a dict of lists which contains the number of orientations an object has. [Left, Right, Frontal, Rear, Unspecified]
    """

def parseFiles(annotationsPath,objectType):
    orientationDict = {'car':[0,0,0,0,0],'person':[0,0,0,0,0],'bicycle':[0,0,0,0,0]}
    # Creates two lists and an object in one list corresponds to the orientation in the other list based on position.
    parsedObjectXMLList = []
    parsedOrientationXMLList = []
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
                parsedObjectXML = (soup.findAll('name'))
                parsedOrientationXML = soup.pose.string
                
                for object in parsedObjectXML:
                    match = re.search('(<name>)(\w+)(</name>)', str(object))
                    object = match.group(2)
                    if objectType == 'all':
                        parsedObjectXMLList += object,
                        parsedOrientationXMLList += str(parsedOrientationXML),
                    elif objectType == 'car' and object == 'car':
                        parsedObjectXMLList += object,
                        parsedOrientationXMLList += str(parsedOrientationXML),
                    elif objectType == 'person' and object == 'person':
                        parsedObjectXMLList += object,
                        parsedOrientationXMLList += str(parsedOrientationXML),
                    elif objectType == 'bicycle' and object == 'bicycle':
                        parsedObjectXMLList += object,
                        parsedOrientationXMLList += str(parsedOrientationXML),
            except IOError:
                sys.stderr.write('There was a problem with file: ' + file + '/n')
    print parsedObjectXMLList, parsedOrientationXMLList
    print len(parsedObjectXMLList)
    print len(parsedOrientationXMLList)
    return

    for x in range (0,len(parsedObjectXMLList)):
        if parsedObjectXMLList[x] == 'car':
            if parsedOrientationXMLList[x] == 'Left':
                (orientationDict['car'])[0]+=1
            elif parsedOrientationXMLList[x] == 'Right':
                (orientationDict['car'])[1]+=1
            elif parsedOrientationXMLList[x] == 'Frontal':
                (orientationDict['car'])[2]+=1
            elif parsedOrientationXMLList[x] == 'Rear':
                (orientationDict['car'])[3]+=1
            elif parsedOrientationXMLList[x] == 'Unspecified':
                (orientationDict['car'])[4]+=1
        elif parsedObjectXMLList[x] == 'person':
            if parsedOrientationXMLList[x] == 'Left':
                (orientationDict['person'])[0]+=1
            elif parsedOrientationXMLList[x] == 'Right':
                (orientationDict['person'])[1]+=1
            elif parsedOrientationXMLList[x] == 'Frontal':
                (orientationDict['person'])[2]+=1
            elif parsedOrientationXMLList[x] == 'Rear':
                (orientationDict['person'])[3]+=1
            elif parsedOrientationXMLList[x] == 'Unspecified':
                (orientationDict['person'])[4]+=1
        elif parsedObjectXMLList[x] == 'bicycle':
            if parsedOrientationXMLList[x] == 'Left':
                (orientationDict['bicycle'])[0]+=1
            elif parsedOrientationXMLList[x] == 'Right':
                (orientationDict['bicycle'])[1]+=1
            elif parsedOrientationXMLList[x] == 'Frontal':
                (orientationDict['bicycle'])[2]+=1
            elif parsedOrientationXMLList[x] == 'Rear':
                (orientationDict['bicycle'])[3]+=1
            elif parsedOrientationXMLList[x] == 'Unspecified':
                (orientationDict['bicycle'])[4]+=1
    return orientationDict

"""
    Counts the number of objects and returns a list.
    The list is organized as these lines:
    [Number of Cars, Number of Persons, Number of Bicycles]
    """

def createGraph(objectOrientationDict,outputPath):
    
    N = 5
    carOrientation   = objectOrientationDict['car']
    personOrientation = objectOrientationDict['person']
    bicycleOrientation = objectOrientationDict['bicycle']
    
    bicycleBarHeight = [0,0,0,0,0]
    
    orientationNumber = [0,0,0,0,0]
    for x in range (0,5):
        height = (carOrientation[x] + personOrientation[x])
        bicycleBarHeight[x] = height
        orientationNumber[x] = (carOrientation[x] + personOrientation[x] + bicycleOrientation[x])
    
    ind = np.arange(N)    # the x locations for the groups
    width = 0.50       # the width of the bars: can also be len(x) sequence
    
    p1 = plt.bar(ind, carOrientation, width, color='r')
    p2 = plt.bar(ind, personOrientation, width, color='#FFD700',bottom=carOrientation)
    p3 = plt.bar(ind, bicycleOrientation, width, color='g',bottom=bicycleBarHeight)
    
    plt.ylabel('The Number of Objects', fontsize=12, fontweight='bold')
    plt.title('The Distribution of Objects in the Database by Orientation.', fontsize=16, fontweight='bold')
    plt.xticks(ind+width/2., ('Left - ' + str(orientationNumber[0]), 'Right - ' + str(orientationNumber[1]), 'Frontal - ' + str(orientationNumber[2]),'Rear - ' + str(orientationNumber[3]),'Unspecified - ' + str(orientationNumber[4])),fontsize=12, fontweight='bold' )
    plt.legend( (p1[0], p2[0],p3[0]), ('Cars', 'Persons','Bicycles'),fancybox = True,shadow = True,frameon = True)
    
    # Asks the user if he or she wants to save the file
    userInput = ''
    while userInput is not 'y' or 'n':
        userInput = raw_input("Would you like to save the figure? (y/n) ")
        userInput = userInput.lower()
        if userInput == 'y':
            path = os.path.abspath(outputPath)
            filename = 'graphObjectOrientation_1.png'
            fullpath = os.path.join(path, filename)
            plt.savefig(fullpath)
            break
        elif userInput == 'n':
            break
        else:
            print "Please answer y or n. " '\n'
    
    plt.show()


"""
    Creates a graph of object classes by reading files from the
    directory,annotationsPath and outputs it to outputPath
    """

def graphObjectOrientation(annotationsPath, outputPath,objectType):
    objectOrientationDict = parseFiles(annotationsPath,objectType)
    createGraph(objectOrientationDict,outputPath)

"""
    Given the path, it opens the all the xml files.
    Use matlab to create a graph to a certain locations.
    Create your own directory if not present.
    Accepting the argument.
    """

def main():
    annotationsPath = raw_input("Path to the annotations?: ")
    outputPath = raw_input("Output Path?: ")
    objectType = raw_input("What type of object would you like? (car/person/bicycle/all)")
    
    if os.path.exists(annotationsPath) and os.path.exists(outputPath):
        graphObjectOrientation(annotationsPath,outputPath,objectType)
    
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
