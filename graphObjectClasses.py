#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

"""
    Main Program Function:
    Visually graphs the breakdown of objects by class in database and saves the graph to outputPath.

        Parses all xml annotation files in annotationsPath using BeautifulSoup. Creates and displays a simple graph (bar, pie, etc) showing the breakdown by class of all annotated objects in the database (e.g. 25% person, 25% bicycle, 50% car). Note that you are counting objects, not images. The graph should have a descriptive title and labeled axes.

        Args:
        annotationsPath: a string that specifies the directory containing the xml      annotation files.
        outputPath: a string that specifies the directory in which to write the output graph file.
        Returns:

        Raises:
"""

"""
 Parses through all the xml files to return a list of objects within the file.
"""

def parseFiles(annotationsPath):
  objectList = []
  # Retrieves all the files in a directory and checks if they are xml
  annotationsFullPath = os.path.abspath(annotationsPath)
  fileList = os.listdir(annotationsFullPath)
  
  if len(fileList) > 0:
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
                for object in parsedXML:
                    match = re.search('(<name>)(\w+)(</name>)', str(object))
                    objectList += match.group(2),
            except IOError:
                errorMessage = "There was a problem with file: " + file
                print
                sys.stderr.write(errorMessage)
  else:
    sys.stderr.write("Error - No xml files found.")
    sys.exit(1)
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

"""
  Calculates the percentage of an object type. Returns a list of floats rounded to the thousands.
"""
def calculatePercentage(countedList):
    sum = 0.0
    for float in countedList:
        sum += float
    percentageList = ['','','']
    for x in range(0,len(countedList)):
        percentageList[x] += str((round((countedList[x]/sum),3))*100) + '%'
    return percentageList
"""
   Creates the legend which will display how much each object type makes up of
   all the object types in the database as well as the total number of object types.
"""
def createLegend(ax,colors,countedList):
    percentageList = calculatePercentage(countedList)
    ax.bar([0], [0], width=0.4, label = percentageList[0] +' Cars', align='center', color = colors[0])
    ax.bar([0], [0], width=0.4, label = percentageList[1] +' Persons', align='center',color = colors[1])
    ax.bar([0], [0], width=0.4, label = percentageList[2] +' Bicycles',align='center',color = colors[2])
    ax.legend(loc='upper right',title = 'Object Types by Percentage',fancybox = True,shadow = True,frameon = True)

"""
 Creates a graph of object types and shows percentage of object type as well as 
 the number of object type.
"""
def createGraph(countedList,outputPath):
    
    # CONSTANTS
    CATEGORYNUM = len(countedList)
    MAXNUM = max(countedList)
    IND = np.arange(CATEGORYNUM)
    sum = 0
    for categoryNum in countedList:
        sum += int(categoryNum)
    WIDTH = 0.60
    
    fig, ax = plt.subplots()
    # Sets the colors for the 3 bars.
    colors = ['r','b','g']
    bars = ax.bar(IND, countedList, WIDTH, color=colors)
    
    # Graph Labels
    ax.set_ylabel(r'Number of Objects',fontsize=13, fontweight='bold')
    fig.suptitle(r'The Composition of ' + str(sum) + ' Annotated Objects in the Database by Type', fontsize=16, fontweight='bold')
    ax.set_xticks(IND + (WIDTH/2))
    ax.set_xticklabels( (r'Cars - ' + str(countedList[0]), r'Persons - ' + str(countedList[1]), r'Bicycles - ' + str(countedList[2])),fontweight='bold' )
    ax.set_ylim(0,MAXNUM*2)
    
    # Creates the legend.
    createLegend(ax,colors,countedList)

    # Asks the user if he or she wants to save the file
    userInput = ''
    while userInput is not 'y' or 'n':
      userInput = raw_input("Would you like to save the figure? (y/n) ")
      userInput = userInput.lower()
      if userInput == 'y':
        path = os.path.abspath(outputPath)
        filename = 'objectClassFigure_1.png'
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

def graphObjectClasses(annotationsPath, outputPath):
  objectList = parseFiles(annotationsPath)
  countedList = organizeObjectList(objectList)
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
        graphObjectClasses(annotationsPath,outputPath)
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
