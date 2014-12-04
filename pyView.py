from Tkinter import *
from PIL import Image, ImageTk, ImageOps
import sys
import os
import glob
import json
from timeit import default_timer

# create a check to see if the photo is already

GOOD_PHOTO_BUTTON = "<a>"
BAD_PHOTO_BUTTON = "<s>"

def checkIfInt(filename):
    try:
        int(filename[-4:])
        return True
    except ValueError:
        return False

# This makes the assumption that there are DCM files.
# Remove hard code for final edit.

def parseFiles():
    jpegList = []
    photoPath = '/Users/davidta/Desktop'
    

#    photoPath = raw_input("Path to the jpeg photos?: ")
    fileList = glob.glob(photoPath + '/*')
    
    for file in fileList:
        if checkIfInt(file):
            DCMList = glob.glob(file + '/*')
            for DCMFile in DCMList:
                if (checkIfInt(DCMFile)):
                    photoList = glob.glob(DCMFile + '/*')
                    for photo in photoList:
                        if photo.endswith('.JPG') or photo.endswith('.jpg'):
                            jpegList.append(photo)

    return jpegList


def viewPhotos(jpegList,JSONcategories,createPhotoCategories):
    
    for jpegPosition in range(len(jpegList)):
        
        root = Tk()
        root.geometry('+0+0')
        root.wm_title(jpegList[jpegPosition])
        image = Image.open(jpegList[jpegPosition])
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = screen_width, screen_height
        image = ImageOps.fit(image, size)
        canvas = Canvas(root,width=image.size[0],height=image.size[1], bd=0, highlightthickness=0)
        def rightKeyPress(event):
            root.destroy()
        root.bind("<Right>", rightKeyPress)
        
        def categorizeBadPhoto(event):
            JSONcategories[jpegList[jpegPosition]] = 'bad'
            root.wm_title(jpegList[jpegPosition] + " - Bad")
        root.bind(BAD_PHOTO_BUTTON, categorizeBadPhoto)
        
        def categorizeGoodPhoto(event):
            JSONcategories[jpegList[jpegPosition]] = 'good'
            root.wm_title(jpegList[jpegPosition] + " - Good")
        root.bind(GOOD_PHOTO_BUTTON, categorizeGoodPhoto)
        
        def quitProgram(event):
            organizePhotos(createPhotoCategories,JSONcategories)
            quit(root)
        root.bind("<Escape>", quitProgram)

        canvas.pack()

        imageTk = ImageTk.PhotoImage(image)
        canvasImage = canvas.create_image(0,0,image=imageTk,anchor='nw')
        root.mainloop()

def organizePhotos(createPhotoCategories,JSONcategories):
    if createPhotoCategories == 'y' or 'Y':
        with open('orderedqVPhotos.txt', 'w') as outfile:
            json.dump(JSONcategories, outfile)

def main():
    createPhotoCategories = raw_input('Organize the photos into a JSON file? (y/n): ')
    JSONcategories = {}
    jpegList = parseFiles();
    
    viewPhotos(jpegList,JSONcategories,createPhotoCategories);
    organizePhotos(createPhotoCategories,JSONcategories)

if __name__ == '__main__':
    main()


