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

def viewPhotos(jpegList):
    for jpeg in jpegList:
#        class App():
#            def __init__(self):
#            self.root = Tkinter.Tk()
#            button = Tkinter.Button(self.root, text = 'root quit', command = self.quit)
#            button.pack()
#            self.root.mainloop()
#            def quit(self):
#                self.root.destroy()
#        app = App()

        root = Tk(className=jpeg)
        
        def rightKeyPress(event):
            print "het"
        def quit(self):
            self.root.destroy()
        root.geometry('+0+0')
        
        image = Image.open(jpeg)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()


        size = screen_width/2, screen_height/2
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        canvas = Canvas(root,width=image.size[0],height=image.size[1], bd=0, highlightthickness=0)
        root.bind("<Right>", rightKeyPress)

        canvas.pack()

        imageTk = ImageTk.PhotoImage(image)
        imagesprite = canvas.create_image(0,0,image=imageTk,anchor='nw')
        root.mainloop()


def main():
    jpegList = parseFiles();
    viewPhotos(jpegList);

if __name__ == '__main__':
    main()


