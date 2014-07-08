#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
"""
    Assumes that areList has already been sorted.
"""

def createBin(areaList):
    binList = []
    roundingFactor = int(len(str(123)))
    for area in areaList:
        area = round(area,-roundingFactor)
        binList.append(area)
    return binList

def createGraph(areaList,outputPath,objectClass,noTruncated,noOcclusion):
    # CONSTANTS
    MAX_AREA = 400*600
    
    # Creates the bins for the histogram.
    areaList.sort()
    binList = createBin(areaList)
    
    # Creates the histogram.
    areaList.sort()
    fig, ax = plt.subplots()
    plt.hist(areaList,range = (0,MAX_AREA), bins = binList)
    
    plt.title(r'The Distribution of '+ objectClass + ' Object by Area of the Bounding Box', fontsize=16, fontweight='bold')
    plt.xlabel('Area of a Bounding Box',fontweight='bold')
    plt.ylabel('Amount In Each Bin',fontweight='bold')
    ax.set_xticks(binList,minor=1)
    
    # Creates the legend.
    ax.bar([0], [0], width=0.4, label = 'noTruncated = ' + str(noTruncated), align='center')
    ax.bar([0], [0], width=0.4, label = 'noOcclusion = ' + str(noOcclusion), align='center')
    ax.legend(loc='upper right',title = 'Optional Parameters',fancybox = True,shadow = True,frameon = True)

    
    # Prompts the user whether he or she wants to save the figure.
    userInput = ''
    while userInput is not 'y' or 'n':
        userInput = raw_input("Would you like to save the figure? (y/n) ")
        userInput = userInput.lower()
        if userInput == 'y':
            path = os.path.abspath(outputPath)
            filename = 'objectAreaFigure_1.png'
            fullpath = os.path.join(path, filename)
            plt.savefig(fullpath)
            break
        elif userInput == 'n':
            break
        else:
            print "Please answer y or n. " '\n'
    # Shows the histogram.
    plt.show()

def calculateArea(soup,list):
        xLength = int(soup.xmax.string) - int(soup.xmin.string)
        yLength = int(soup.ymax.string) - int(soup.ymin.string)
        area = xLength*yLength
        list.append(area)

"""
    Finds of the area of all bounding boxes in xml files and
    returns a list of the areas.
"""

def collectObjectArea(annotationsPath,objectClass,noTruncated,noOcclusion):
    
    areaList = []
    truncationArea = []
    occlusionArea = []
        # Retrieves all the files in a directory and checks if they are xml
    fileList = os.listdir(annotationsPath)
    for file in fileList:
        fileTypeMatch = re.search('.xml',file)
        if fileTypeMatch:
            try:
                f = open(file)
                soup = bsoup(f)
                f.close()
                parsedXML = (soup.findAll('name'))
                # Finds the object of all xml files and checks if it is a part of objectClass.
                if objectClass == 'all':
                    for object in parsedXML:
                        truncatedMatch = int(soup.truncated.string)
                        occlusionMatch = int(soup.occluded.string)
                        if not truncatedMatch and not occlusionMatch:
                            calculateArea(soup,areaList)
                        if truncatedMatch and not occlusionMatch:
                            calculateArea(soup,truncationArea)
                        if occlusionMatch and not truncatedMatch:
                            calculateArea(soup,occlusionArea)
                else:
                    for object in parsedXML:
                        match = re.search('(<name>)(\w+)(</name>)', str(object))
                        truncatedMatch = int(soup.truncated.string)
                        occlusionMatch = int(soup.occluded.string)
                        # For all objects of the type that the user specifies, area is
                        # calculated and added to a list.
                        if match.group(2) == objectClass:
                            if not truncatedMatch and not occlusionMatch:
                                calculateArea(soup,areaList)
                            if truncatedMatch and not occlusionMatch:
                                calculateArea(soup,truncationArea)
                            if occlusionMatch and not truncatedMatch:
                                calculateArea(soup,occlusionArea)
            except IOError:
                sys.stderr.write('There was a problem with file: ' + file +'\n')
    if noTruncated:
        areaList += truncationArea
    if noOcclusion:
        areaList += occlusionArea
    return areaList

"""
    Parses all xml annotation files in annotationsPath using BeautifulSoup. Creates and displays a simple histogram showing the distribution of bounding box area (in pixels), for objects with class objectClass. The number of histogram bins should be chosen to optimize readability of the graph. The graph should have a descriptive title and labeled axes.
    
    Args:
    annotationsPath: a string that specifies the directory containing the xml annotation files.
    objectClass: a string that specifies the PASCAL VOC object class of interest.
    outputPath: a string that specifies the directory in which to write the output graph file.
    Returns:
    
    Raises:
    
"""
def graphObjectAreas(annotationsPath,outputPath, objectClass='all',noTruncated=False,noOcclusion=False):
    areaList = collectObjectArea(annotationsPath,objectClass,noTruncated,noOcclusion)
    createGraph(areaList,outputPath,objectClass,noTruncated,noOcclusion)

"""
 Given the path, it opens the all the xml files.
 Use matlab to create a graph to a certain locations.
 Create your own directory if not present.
 Accepting the argument.
"""

def main():
    
    objectType='all'
    noOcclusion=0
    noTruncated=0
    
    args = sys.argv[1:]
    if not args:
      sys.stderr.write("Error - usage: [annotationsPath][outputPath]")
      sys.exit(1)
    else:
      annotationsPath = args[0]
      outputPath = args[1]
  
      # Checks args for optional parameter,objectClass, noTruncatedMatch, noOcclusionMatch
      for arg in args:
        objectMatch = re.search('(objectType)(=)(\w+)',arg)
        noTruncatedMatch = re.search('(noTruncated=)(True)',arg)
        noOcclusionMatch = re.search('(noOcclusion=)(True)',arg)
        if objectMatch:
          objectType = objectMatch.group(3).lower()
        if noOcclusionMatch:
          noOcclusion = noOcclusionMatch.group(2)
        if noTruncatedMatch:
          noTruncated = noTruncatedMatch.group(2)

      # Determines what type of graph to create based on the optional parameters declared.
      if os.path.exists(annotationsPath) and os.path.exists(outputPath):
        if objectType in ('car', 'person', 'bicycle') and noOcclusion and noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noOcclusion=True,noTruncated=True)
        if objectType in ('car', 'person', 'bicycle') and noOcclusion and not noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noOcclusion=True)
        if objectType in ('car', 'person', 'bicycle') and not noOcclusion and noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noTruncated=True)
        if objectType in ('car', 'person', 'bicycle') and not noOcclusion and not noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType)

        if objectType == 'all' and noOcclusion and noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noOcclusion=True,noTruncated=True)
        if objectType == 'all' and noOcclusion and not noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noOcclusion=True)
        if objectType == 'all' and not noOcclusion and noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType,noTruncated=True)
        if objectType == 'all' and not noOcclusion and not noTruncated:
          graphObjectAreas(annotationsPath,outputPath,objectClass=objectType)

      # Error mssages for broken paths.
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