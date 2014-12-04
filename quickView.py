from Tkinter import *
from PIL import Image, ImageTk, ImageOps
import sys
import os
import glob
import json
import re
# CONSTANTS FOR KEYBOARD CONTROLS
GOOD_PHOTO_BUTTON = "<a>"
BAD_PHOTO_BUTTON = "<s>"

"""
    Checks the last 4 digits to find files containing JPG files. Opens files with formats such as 140000-1231 or DCM0001.
"""

def checkIfInt(filename):
    try:
        int(filename[-4:])
        return True
    except ValueError:
        return False

"""
    Parses through link to search for the photos. If selected, will ignore already categorized photos.
"""

def parseFiles(ignoreCategorizedPhotos,JSONcategories):
    jpegList = []
    photoPath = raw_input('Path to JPG photos: ')
    
    fileList = glob.glob(photoPath + '/*')
    
    for file in fileList:
        if checkIfInt(file):
            DCMList = glob.glob(file + '/*')
            for DCMFile in DCMList:
                if (checkIfInt(DCMFile)):
                    photoList = glob.glob(DCMFile + '/*')
                    for photo in photoList:
                        if photo.endswith('.JPG') or photo.endswith('.jpg'):
                            if str(ignoreCategorizedPhotos) == "n":
                                print "n"
                                jpegList.append(os.path.abspath(photo))
                            else:
                                if os.path.abspath(photo) not in JSONcategories:
                                    jpegList.append(os.path.abspath(photo))
    return jpegList

"""
    Opens photos with Tkinter. Anti-Aliasing is not done when resizing photos to fit them in the Canvas.
    If you want Anti-Aliasing, include image.ANTIALIAS as a parameter for ImageOps. Be advisied, anti-aliasing doubles the time it takes to open up a photo
"""

def viewPhotos(jpegList,JSONcategories,createPhotoCategories,ignoreCategorizedPhotos):
    for jpegPosition in range(len(jpegList)):

        root = Tk()
        root.geometry('+0+0')
        root.wm_title(jpegList[jpegPosition])
        
        # Makes sure that photos that are already categorized, are labelled as such when Tkinter brings up the photos to be viewed.
        if str(ignoreCategorizedPhotos) == "n":
            root.wm_title(jpegList[jpegPosition] + " - " + JSONcategories[jpegList[jpegPosition]])

        image = Image.open(jpegList[jpegPosition])
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = screen_width, screen_height
        image = ImageOps.fit(image, size)
        canvas = Canvas(root,width=image.size[0],height=image.size[1], bd=0, highlightthickness=0)
        
        # Keyboard commands for the photoviewer. User can add more categories or alter pre-existing commands.
        def rightKeyPress(event):
            root.destroy()
        root.bind("<Right>", rightKeyPress)
        def categorizeBadPhoto(event):
            JSONcategories[jpegList[jpegPosition]] = "bad"
            root.wm_title(jpegList[jpegPosition] + " - bad")
        root.bind(BAD_PHOTO_BUTTON, categorizeBadPhoto)
        def categorizeGoodPhoto(event):
            JSONcategories[jpegList[jpegPosition]] = "good"
            root.wm_title(jpegList[jpegPosition] + " - good")
        root.bind(GOOD_PHOTO_BUTTON, categorizeGoodPhoto)
        def quitProgram(event):
            organizePhotos(createPhotoCategories,JSONcategories)
            quit(root)
        root.bind("<Escape>", quitProgram)
        
        canvas.pack()

        imageTk = ImageTk.PhotoImage(image)
        canvasImage = canvas.create_image(0,0,image=imageTk,anchor='nw')
        root.mainloop()

"""
    Opens photos with Tkinter.
"""

def organizePhotos(createPhotoCategories,JSONcategories):
    if str(createPhotoCategories) == "y":
        with open('categorizedQuickViewPhotos.txt', 'w') as outfile:
            json.dump(JSONcategories, outfile)

def convertTxtToDict(txt,JSONcategories):
    photoLinkList = re.findall('\d+-\d+/DCM\d+/\d+_\d+....',txt)
    categoryList = re.findall(': "\w+"',txt)

    for x in range(0,len(photoLinkList)):
        category = categoryList[x][3:]
        category = category[:-1]
        JSONcategories[os.path.abspath(photoLinkList[x])] = category




def main():
    JSONcategories = {}
    createPhotoCategories = raw_input('Would you like to categorize the photos and write to a file? (y/n): ')
    acceptPreviousPhotoCategorizations = raw_input('Would you like to use classifications that you have previously created? (y/n): ')
    if str(acceptPreviousPhotoCategorizations) == "y":
        oldCategorizationPath = "";
        while not os.path.exists(oldCategorizationPath):
            processPreviousPhotoCategorizations = raw_input('Where are previous classications located? ')
            oldCategorizationPath = os.path.abspath(processPreviousPhotoCategorizations)
            if not os.path.exists(oldCategorizationPath):
                print "Old Categorization File Not Found."

    oldCategorizationTxt = open(oldCategorizationPath, 'r')

    convertTxtToDict(oldCategorizationTxt.read(), JSONcategories)
    ignoreCategorizedPhotos = raw_input('Ignore Categorized Photos? (y/n): ')
    jpegList = parseFiles(ignoreCategorizedPhotos,JSONcategories);
    viewPhotos(jpegList,JSONcategories,createPhotoCategories,ignoreCategorizedPhotos);
    organizePhotos(createPhotoCategories,JSONcategories);

if __name__ == '__main__':
    main()


