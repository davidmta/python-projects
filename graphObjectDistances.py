#!/usr/bin/python
import os
import sys
import re
import subprocess
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np

# Determine actual height.
# Apply the formula

RAW_FORMAT = '.nef'
ANNOTATION_EXTENSION = '.xml'
#def calculatePhotoHeight()
"""
    Actual Height of a Person: 1.7 m for men while for women it is 1.6 m.
    We will take the average and use 1.65 m for all angles.
    From National Health Statistics Reports (http://www.cdc.gov/nchs/data/nhsr/nhsr010.pdf)
    
    Actual Height of a Bike:
    Left and Right of a bike is 1.5 m - 1.8 m
    We take the average: 1.65 m.
    
    From Wisconsin Department of Transportation: Wisconsin Bicycle Facility Design Handbook (http://www.dot.wisconsin.gov/projects/state/docs/bike-facility-chap1.pdf)
    
    Front and Back:
    I could not find this one so instead measure my bike from the handlebars to the ground and found that it was roughly 1 m.
    
"""
#def determineActualHeight(objectType,objectPose):
#    if objectType == 'car':
#    elif objectType == 'bicycle':
#        if objectPose in ('Rear','Front'):
#            return 1
#        elif objectPose in ('Left', 'Right'):
#            return 1.65
#    elif objectType == 'person' and objectPose is not 'Unspecified' :
#        print 'person objectPose: ' + objectPose
#        return 1.65

"""
    Converts Focal Length from millimeters to meters.
"""

def convertFocalLength(focalLength):
    return (float(focalLength)*(0.001))

def calculateAperture(rawFileFullPath,currentFile):
    proc = subprocess.Popen('dcraw -i -v ' + os.path.join(rawFileFullPath, currentFile), shell=True, stdout=subprocess.PIPE, )
    data = proc.communicate()[0]
    aperture = re.findall(r'Aperture: f/(.*)\n', data)[0]
    focalLength = re.findall(r'Focal length: (\d+).0 mm\n', data)[0]
    focalLength = convertFocalLength(focalLength)
    return aperture,focalLength

def calculateObjectDistance(rawFilePath,annotationsPath):
    rawFileFullPath = os.path.abspath(rawFilePath)
    annotationsPathFullPath = os.path.abspath(annotationsPath)
    for currentFile in os.listdir(rawFileFullPath):
        fileName, fileExtension = os.path.splitext(currentFile)
        if fileExtension == RAW_FORMAT:
            annotationFileName = fileName + ANNOTATION_EXTENSION
            if annotationFileName in os.listdir(annotationsPathFullPath):
                f = open(annotationFileName)
                soup = bsoup(f)
                f.close()
                aperture,focalLength = calculateAperture(rawFileFullPath,currentFile)
#                photoHeight = int(soup.ymax.string) - int(soup.ymin.string)
#                
#                objectTypesList = re.findall('(<name>)(\w+)',str(soup))
#                actualHeight = determineActualHeight(objectType)

"""
    Given the path, it opens the all the xml files.
    Use matlab to create a graph to a certain locations.
    Create your own directory if not present.
    Accepting the argument.
"""

def main():
    args = sys.argv[1:]
    rawFilePath = raw_input("Enter path for raw photos: ")
    annotationsPath = raw_input("Enter path for the Annotations: ")
    calculateObjectDistance(rawFilePath,annotationsPath)

if __name__ == '__main__':
    main()