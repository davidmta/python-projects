#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def countList(tagList):
    countedList = [0,0,0,0]
    for tag in tagList:
        if tag == 'none':
            countedList[0] += 1
        if tag == 'truncated':
            countedList[1] += 1
        if tag == 'truncated and occluded':
            countedList[2] += 1
        if tag == 'occluded':
            countedList[3] += 1
    return countedList

def addToTagList(soup):
    truncation = int(soup.truncated.string)
    occlusion = int(soup.occluded.string)
    if truncation and occlusion:
        return('truncated and occluded')
    elif occlusion:
        return('occluded')
    elif truncation:
        return('truncated')
    else:
        return('none')

def parseFiles(annotationsPath,objectType):
    tagList = []
    # Retrieves all the files in a directory and checks if they are xml
    fileList = os.listdir(annotationsPath)
    for file in fileList:
        fileTypeMatch = re.search('.xml',file)
        if fileTypeMatch:
            try:
                f = open(file)
                soup = bsoup(f)
                f.close()
                # Finds the object of all xml files and places the objects into a list
                # and returns it.
                parsedXML = (soup.findAll('name'))
                if objectType == 'all':
                    tagList.append(addToTagList(soup))
                elif objectType in ('car','person','bicycle'):
                    for object in parsedXML:
                        match = re.search('(<name>)(\w+)(</name>)', str(object))
                        if match.group(2) == objectType:
                            tagList.append(addToTagList(soup))
            except IOError:
                sys.stderr.write('There was a problem with file: ' + file)
    return tagList

def calculatePercentage(countedList):
    percentageList = []
    sum = 0.0
    for category in countedList:
        sum += category
    for objectTag in countedList:
        quotient = (objectTag/sum)*100
        percentageList.append(round(quotient,4))
    return percentageList

def createPieChart(countedList,objectType,percentageList,outputPath):
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'None', 'Truncated', 'Truncated and Occluded', 'Occluded'
    sizes = percentageList
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    plt.title('The Distribution of ' + objectType + ' Object by Tag',fontsize=16, fontweight='bold')
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=0)
            # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.axis('equal')
            
            # Asks the user if he or she wants to save the file
            userInput = ''
            while userInput is not 'y' or 'n':
                userInput = raw_input("Would you like to save the figure? (y/n) ")
                userInput = userInput.lower()
                if userInput == 'y':
                    path = os.path.abspath(outputPath)
                    filename = 'objectTagsFigure_1.png'
                    fullpath = os.path.join(path, filename)
                    plt.savefig(fullpath)
                    break
                elif userInput == 'n':
                    break
                else:
                    print "Please answer y or n. " '\n'
            plt.show()


def graphObjectTags(annotationsPath,outputPath,objectType='all'):
    tagList = parseFiles(annotationsPath,objectType)
    countedList = countList(tagList)
    percentageList = calculatePercentage(countedList)
    createPieChart(countedList,objectType,percentageList,outputPath)

"""
    Given the path, it opens the all the xml files.
    Use matlab to create a graph to a certain locations.
    Create your own directory if not present.
    Accepting the argument.
    """

def main():
    annotationsPath = raw_input("Path to the annotations?: ")
    outputPath = raw_input("Output Path?: ")
    objecttype = raw_input("Which object tags would you like? (all/car/person/bicycle): ")
    if objectType in ('car','person','bicycle'):
        graphObjectTags(annotationsPath,outputPath,objectType=objectType)
    else if objectType is 'all':
        graphObjectTags(annotationsPath,outputPath)

if __name__ == '__main__':
    main()
