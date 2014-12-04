from Tkinter import *
from PIL import Image, ImageTk, ImageOps
import sys
import os
import glob
import json

def checkIfInt(filename):
    try:
        int(filename[-4:])
        return True
    except ValueError:
        return False

# This makes the assumption that there are DCM files.

def parseFiles():
    jpegList = []
    photoPath = raw_input("Path to the jpeg photos?: ")
    fileList = glob.glob(photoPath + '/*')
    
    for file in fileList:
        if checkIfInt(file):
            DCMList = glob.glob(file + '/*')
            for DCMFile in DCMList:
                if (checkIfInt(DCMFile)):
                    photoList = glob.glob(DCMFile + '/*')
                    for photo in photoList:
                        if photo.endswith('.JPG'):
                            jpegList.append(photo)
    return jpegList

# Option to quit

def viewPhotos(jpegList):
    for jpegPosition in range(0,len(jpegList)):
        
        root = Tk(className=jpegList[jpegPosition])
        root.geometry('+0+0')
        image = Image.open(jpegList[jpegPosition])
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        size = screen_width/2, screen_height/2
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        canvas = Canvas(root,width=image.size[0],height=image.size[1], bd=0, highlightthickness=0)
        def rightKeyPress(event):
            root.destroy()
        
        root.bind("<Right>", rightKeyPress)
        canvas.pack()


        imageTk = ImageTk.PhotoImage(image)
        imagesprite = canvas.create_image(0,0,image=imageTk,anchor='nw')
                

        
        root.mainloop()


#        class Window():
#            def __init__(self):
#                self.root = Tk(className=jpegList[jpegPosition])
#
#                
#                self.root.geometry('+0+0')
#                image = Image.open(jpegList[jpegPosition])
#                screen_width = self.root.winfo_screenwidth()
#                screen_height = self.root.winfo_screenheight()
#                size = screen_width/2, screen_height/2
#                image = ImageOps.fit(image, size, Image.ANTIALIAS)
#                canvas = Canvas(self.root,width=image.size[0],height=image.size[1], bd=0, highlightthickness=0)
#                canvas.pack()
#                
#                imageTk = ImageTk.PhotoImage(image)
#                imagesprite = canvas.create_image(0,0,image=imageTk,anchor='nw')
#                
#                def escapeKeyPress(self):
#                    quit(self)
#                self.root.bind("<Escape>", escapeKeyPress)
#                def rightKeyPress(self):
#                    print "right"
#                    root.destroy()
#
#                self.root.bind("<Right>", rightKeyPress)
#                def leftKeyPress(self):
#                    quit(self)
#                self.root.bind("<Left>", leftKeyPress)
#                self.root.mainloop()
#            
#            def quit(self):
#                self.destroy()
#        window = Window()

#/Users/davidta/Desktop

def main():
    jpegList = parseFiles();
    viewPhotos(jpegList);

if __name__ == '__main__':
    main()


