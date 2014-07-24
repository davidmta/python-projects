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

# Accept inputs for certain types of photos
# Returns photos.
# Opens all the photos in a reasonable manner
# Can somehow mark photos.
# Allow changing the brightness of photos.
# Allows user not to have to open marked photos.
# Allows user to make changes to marked photos.


def createImageDict(annotationsFileList,photoFileList):
    imageDict = {}
    annotationsSet = Set(annotationsFileList)
    for photo in photoFileList:
        photoMatch = re.search('(2014_)(\w+)(.png)',photo)
        if photoMatch:
            xml = str(photoMatch.group(1)) + str(photoMatch.group(2)) + '.xml'
            if xml in annotationsSet:
                print "Processing file: " + photo
                imageDict[photo] = xml

def createImages():
    
    root = Tkinter.Tk()
    root.title("Reviewing Annotations")
    root.maxsize(1200, 750)
    imageList = []
    for file in photoFileList:
        photoMatch = re.search('(2014_)(\w+)(.png)',file)
        if photoMatch:
#            annotationMatch = re.search(str((photoMatch.group(2))+'.xml'),fileList)
#            if annotationMatch:
            image = Image.open(file)
            tk_image = ImageTk.PhotoImage(image)
            imageList.append(tk_image)


    print imageList
    canvas = Tkinter.Canvas(root, bd=0, highlightthickness=0,width=1000,height=750)
    canvas.pack()
    canvas.create_image(0, 0, image=tk_image, anchor='nw')


    #    image = image.crop((0, 0, 200, 200))
    
    
    doneButton = Tkinter.Button(root, text="done")
    doneButton.pack(side='left', expand='true')

    root.mainloop()


def main():
    photoPath = raw_input("Path to the photos?: ")
    annotationsPath = raw_input("Path to the annotations?: ")
        
    annotationsFullPath = os.path.abspath(annotationsPath)
    photoFullPath = os.path.abspath(photoPath)
    
    annotationsFileList = os.listdir(annotationsFullPath)
    photoFileList = os.listdir(photoFullPath)

    createImageDict(annotationsFileList,photoFileList)



if __name__ == '__main__':
    main()
