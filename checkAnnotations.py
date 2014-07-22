#!/usr/bin/python
import os
import sys
import re
from BeautifulSoup import BeautifulSoup as bsoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Accept inputs for certain types of photos
# Returns photos.
# Opens all the photos in a reasonable manner
# Can somehow mark photos.
# Allow changing the brightness of photos.
# Allows user not to have to open marked photos.
# Allows user to make changes to marked photos.

from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
    
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        
        self.QUIT.pack({"side": "right"})
        
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        
        self.hi_there.pack({"side": "right"})
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

if __name__ == '__main__':
    main()
