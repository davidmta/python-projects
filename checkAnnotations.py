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
# Add in failsafes.
# think about using descendants.
# 2 Tkinter.

def organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,classes, orientation, tags):
    imageDict = collections.OrderedDict()
    imageDimension = []
    root = Tkinter.Tk()
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
                nameTagList = re.findall('(<name>)(\w+)(</name>)', str(soup))
                truncationTagList = re.findall('(<truncated>)(\d)(</truncated>)',str(soup))
                occludedTagList = re.findall('(<occluded>)(\d)(</occluded>)',str(soup))
                poseTagList = re.findall('(<pose>)(\w+)(</pose>)',str(soup))
                xminTagList = re.findall('(<xmin>)(\d+)(</xmin>)',str(soup))
                yminTagList = re.findall('(<ymin>)(\d+)(</ymin>)',str(soup))
                xmaxTagList = re.findall('(<xmax>)(\d+)(</xmax>)',str(soup))
                ymaxTagList = re.findall('(<ymax>)(\d+)(</ymax>)',str(soup))
                for name,truncation,occluded,pose,xmin,ymin,xmax,ymax in zip(nameTagList,truncationTagList,occludedTagList,poseTagList,
                    xminTagList,yminTagList,xmaxTagList,ymaxTagList):
                    print truncation[1],occluded[1],pose[1],xmin[1],ymin[1],xmax[1],ymax[1]
                    
                    if classes.lower() == name[1]:
                        if orientation.lower() in (pose[1],'all'):
                            if tags.lower() == 'none' or tags.lower() == 'occluded' and int(occluded[1]) or tags.lower() == 'truncated' and int(truncation[1]) or tags.lower() == 'occluded and truncated' and int(occluded[1]) and int(truncation[1]):
                                print "Processing file: " + photo
                                if classes.lower() == 'person':
                                    size = 150, 300
                                else:
                                    size = 300, 150
                                image = Image.open(photo)
                                image = image.crop((int(xmin[1]),int(ymin[1]),int(xmax[1]),int(ymax[1])))

                                image = image.resize(size)
                                image = ImageTk.PhotoImage(image)
                                imageDict[image] = xml
#                                imageDimension.append([int(xmin[1]),int(ymin[1]),int(xmax[1]),int(ymax[1])])
    return imageDict,imageDimension,root,size

def createCanvas(imageDict,imageDimension,classes,root,size):
    print "Creating Canvas."
#    root = Tkinter.Tk()
#    root.title("Reviewing Annotations")
#    for photo, dimension in zip(imageDict,imageDimension):
#        photo = photo.crop((dimension[0], dimension[1], dimension[2], dimension[3]))

    X_COORDINATE = 0
    X_INCREMENT = 0
    Y_COORDINATE = 0
    Y_INCREMENT = 0
    canvas = Tkinter.Canvas(root, bd=0, highlightthickness=0,width=1050,height=750)
    canvas.pack()

    # could another function. determine increment.

    for photo in imageDict:
#        photo = ImageTk.PhotoImage(photo)

        if X_COORDINATE >= 1050:
            print X_COORDINATE,Y_COORDINATE
            X_COORDINATE = 0
            Y_COORDINATE += size[1]
        print X_COORDINATE,Y_COORDINATE
        canvas.create_image(X_COORDINATE, Y_COORDINATE, image=photo, anchor='nw')
        X_COORDINATE+=size[0]
    root.mainloop()

#Simplify.
def createAnnotationsFileList():
    annotationsPath = raw_input("Path to the annotations?: ")
    annotationsFullPath = os.path.abspath(annotationsPath)
    return os.listdir(annotationsFullPath),annotationsFullPath

def createPhotoFileList():
    photoPath = raw_input("Path to the photos in png format?: ")
    photoFullPath = os.path.abspath(photoPath)
    return os.listdir(photoFullPath)

# Reduce redundancy.
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
    imageDict,imageDimension,root,size = organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,classes, orientation, tags)
    createCanvas(imageDict,imageDimension,classes,root,size)

if __name__ == '__main__':
    main()
