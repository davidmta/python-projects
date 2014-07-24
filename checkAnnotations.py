#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import Tkinter
from PIL import Image, ImageTk
from sets import Set
import collections


# Accept inputs for certain types of photos
# Returns photos.
# Opens all the photos in a reasonable manner
# Can somehow mark photos.
# Allow changing the brightness of photos.
# Allows user not to have to open marked photos.
# Allows user to make changes to marked photos.


def organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,classes, orientation, tags):
    imageDict = collections.OrderedDict()
    imageDimension = []
    annotationsSet = Set(annotationsFileList)
    for photo in photoFileList:
        photoMatch = re.search('(2014_)(\w+)(.png)',photo)
        if photoMatch:
            xml = str(photoMatch.group(1)) + str(photoMatch.group(2)) + '.xml'
            if xml in annotationsSet:
                xmlPath = os.path.join(annotationsFullPath, xml)
                f = open(xmlPath)
                soup = bsoup(f)
                f.close()
                parsedXML = soup.findAll('name')
                nameMatch = re.search('(<name>)(\w+)(</name>)', str(parsedXML))
                for name in parsedXML:
                    if classes.lower() == nameMatch.group(2):
                        if orientation.lower() in (soup.pose.string.lower(),'all'):
                            if tags.lower() in ('none',soup.truncated.string.lower(), soup.occluded.string.lower()) or tags.lower() == 'occluded and truncated' and int(soup.occluded.string) and int(soup.truncated.string):
                                print "Processing file: " + photo
                                imageDict[photo] = xml
                                imageDimension.append([int(soup.xmin.string),int(soup.ymin.string),int(soup.xmax.string),int(soup.ymax.string)])
    return imageDict,imageDimension

def createCanvas(imageDict,imageDimension):
    photoList = []
    root = Tkinter.Tk()
    root.title("Reviewing Annotations")
    root.maxsize(1200, 750)
    
    for photo, dimension in zip(imageDict,imageDimension):
        image = Image.open(photo)
        image = image.crop((dimension[0], dimension[1], dimension[2], dimension[3]))
        tk_image = ImageTk.PhotoImage(image)
        photoList.append(tk_image)
    canvas = Tkinter.Canvas(root, bd=0, highlightthickness=0,width=1000,height=750)
    canvas.pack()
    canvas.create_image(0, 0, image=tk_image, anchor='nw')

    root.mainloop()

def createAnnotationsFileList():
    annotationsPath = raw_input("Path to the annotations?: ")
    annotationsFullPath = os.path.abspath(annotationsPath)
    return os.listdir(annotationsFullPath),annotationsFullPath

def createPhotoFileList():
    photoPath = raw_input("Path to the photos?: ")
    photoFullPath = os.path.abspath(photoPath)
    return os.listdir(photoFullPath)

def getDesiredObjects():
    while(1):
        classes = raw_input("Which class? (car/person/bicycle): ")
        if classes.lower() in ('car','person','bicycle'):
            break
        else:
            print "Please enter a valid response. You entered " + classes
    while(1):
        orientation = raw_input("Which orientation? (left/right/frontal/rear/all): ")
        if orientation.lower() in ('left','right','frontal','rear','all'):
            break
        else:
            print "Please enter a valid response. You entered " + orientation
    while(1):
        tags = raw_input("Which tag? (none/occluded/truncated/occluded and truncated): ")
        if tags.lower() in ('none','occluded','truncated','occluded and truncated'):
            break
        else:
            print "Please enter a valid response. You entered " + tags
    return classes, orientation,tags


def main():
    classes, orientation, tags = getDesiredObjects()
    annotationsFileList,annotationsFullPath = createAnnotationsFileList()
    photoFileList = createPhotoFileList()
    imageDict,imageDimension = organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,classes, orientation, tags)
    createCanvas(imageDict,imageDimension)

if __name__ == '__main__':
    main()
