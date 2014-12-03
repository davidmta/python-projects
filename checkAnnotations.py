#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from Tkinter import *
from PIL import Image, ImageTk
from sets import Set

# CONSTANTS

CANVAS_HEIGHT = 750
CANVAS_WIDTH = 1200
Y_WHITE_SPACE_OFFSET = 30
Y_TEXT_OFFSET = 10

def parseXML(soup):
    nameTagList = re.findall('(<name>)(\w+)(</name>)', str(soup))
    truncationTagList = re.findall('(<truncated>)(\d)(</truncated>)',str(soup))
    occludedTagList = re.findall('(<occluded>)(\d)(</occluded>)',str(soup))
    poseTagList = re.findall('(<pose>)(\w+)(</pose>)',str(soup))
    xminTagList = re.findall('(<xmin>)(\d+)(</xmin>)',str(soup))
    yminTagList = re.findall('(<ymin>)(\d+)(</ymin>)',str(soup))
    xmaxTagList = re.findall('(<xmax>)(\d+)(</xmax>)',str(soup))
    ymaxTagList = re.findall('(<ymax>)(\d+)(</ymax>)',str(soup))
    return nameTagList,truncationTagList,occludedTagList,poseTagList,xminTagList,yminTagList,xmaxTagList, ymaxTagList

def determinePhotoSize(classes,orientation):
    if classes.lower() == 'person':
        size = 150, 300
    elif classes.lower() in ('car', 'bicycle') and orientation.lower() in ('frontal','rear'):
        size = 200, 150
    else:
        size = 300, 150
    return size

def organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,photoFullPath, classes, orientation, tags):
    size = determinePhotoSize(classes,orientation)
    imageDict = {}
    root = Tk()

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
                nameTagList,truncationTagList,occludedTagList,poseTagList,xminTagList,yminTagList,xmaxTagList,ymaxTagList = parseXML(soup)
                for name,truncation,occluded,pose,xmin,ymin,xmax,ymax in zip(nameTagList,truncationTagList,occludedTagList,poseTagList,xminTagList,yminTagList,xmaxTagList,ymaxTagList):
                    print "Processing file: " + xml
                    if classes.lower() == name[1]:
                        if orientation.lower() in (pose[1].lower(),'all'):
                            if tags.lower() == 'all' or tags.lower() == 'none' and int(truncation[1]) == 0 and int(occluded[1]) == 0 or tags.lower() == 'occluded' and int(occluded[1]) or tags.lower() == 'truncated' and int(truncation[1]) or tags.lower() == 'occluded and truncated' and int(occluded[1]) and int(truncation[1]):
                                print "Match found in: " + photo
                                photoPath = os.path.join(photoFullPath, photo)
                                image = Image.open(photoPath)
                                image = image.crop((int(xmin[1]),int(ymin[1]),int(xmax[1]),int(ymax[1])))
                                image = image.resize(size)
                                image = ImageTk.PhotoImage(image)
                                imageDict[image] = xml
    return imageDict,root,size

def determineTitle(positionDict,classes,tags,orientation):
    title = 'Showing ' + str(len(positionDict)) + ' ' + classes + ' objects' + ' in orientation: ' + orientation
    if tags != 'none':
        title += ' with in tag: ' + tags
    return title

def createCanvas(imageDict,classes,root,size,orientation,tags):
    print "Creating Canvas."
    xCoordinate = 0
    yCoordinate = 0
    positionDict = {}
    frame=Frame(root, height=300, width=150)
    frame.grid(row=0,column=0)
    canvas=Canvas(frame,width=CANVAS_WIDTH,height=CANVAS_HEIGHT)
    # could another function. determine increment.
    for photo in imageDict:
        if xCoordinate >= CANVAS_WIDTH:
            xCoordinate = 0
            yCoordinate += (size[1] + Y_WHITE_SPACE_OFFSET)
        canvas.create_image(xCoordinate, yCoordinate, image=photo, anchor='nw')
        canvas.create_text(xCoordinate + size[0]/2, yCoordinate + size[1] + Y_TEXT_OFFSET,text=imageDict[photo],justify=RIGHT)
        xCoordinate += size[0]
        positionDict[imageDict[photo]] = (xCoordinate,yCoordinate + size[1])
    canvas.config(scrollregion=(0,0,CANVAS_WIDTH,yCoordinate + size[1]+ Y_WHITE_SPACE_OFFSET))

    root.wm_title(determineTitle(positionDict,classes,tags,orientation))

    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
    root.mainloop()

def acceptUserInput():
    classes, orientation, tags = getCategoriesInfo()
    annotationsPath = raw_input("Path to the annotations?: ")
    annotationsFullPath = os.path.abspath(annotationsPath)
    photoPath = raw_input("Path to the photos in png format?: ")
    photoFullPath = os.path.abspath(photoPath)
    return classes, orientation, tags, os.listdir(annotationsFullPath),annotationsFullPath,os.listdir(photoFullPath),photoFullPath

def getCategoriesInfo():
    while(1):
        classes = raw_input("Which class? (car/person/bicycle): ")
        if classes.lower() in ('car','person','bicycle'):
            break
        else:
            print "Please enter a valid response. You entered " + classes
    while(1):
        orientation = raw_input("Which orientation? (left/right/frontal/rear/unspecified/all): ")
        if orientation.lower() in ('left','right','frontal','rear','all','unspecified'):
            break
        else:
            print "Please enter a valid response. You entered " + orientation
    while(1):
        tags = raw_input("Which tag? (all/none/occluded/truncated/occluded and truncated): ")
        if tags.lower() in ('all','none','occluded','truncated','occluded and truncated'):
            break
        else:
            print "Please enter a valid response. You entered " + tags
    return classes, orientation, tags

def main():
    classes, orientation, tags,annotationsFileList,annotationsFullPath,photoFileList,photoFullPath = acceptUserInput()
    imageDict,root,size = organizeImageInfo(annotationsFileList,photoFileList,annotationsFullPath,photoFullPath,classes, orientation, tags)
    createCanvas(imageDict,classes,root,size,orientation,tags)

if __name__ == '__main__':
    main()
