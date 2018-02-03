# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other modules. 
At the minute most of the code is for testing what works and what doesn't.
"""
#All the imported modules
import os #Used in saveImg()
import time
from datetime import datetime
import inputs 
import corners
import lengths
import sys
import numpy as np


#Constants
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored
DEBUGGING = False
OVERWRITE = False
MIN_LENGTH = 25 #Minimum fibre length
FIBRE_WIDTH = 25 #fibre width


#Functions
def saveImg(filename, overwrite = False):
    """
    This function will save the images that have been created into a file with the name "filename", by default it will not overwrite existing images.
    Currently not working as planned as plt.saveFig() won't work inside the function so instead this function just finds the next free filename and returns it.
    
    Arguments:
        filename - This is the name and source of the file to be saved and should be a string.
        overwrite - This defines whether or not an image can be overwrited, it is a boolean. (Default = False)
        
    Returns a string of an edited version of the filename that won't overwrite anything.
    """
    pos = filename.rfind(".") #Find the position of the start of the file type to put a number before it 
    filename = filename[:pos] + "[" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) +  "]" #Add the date and time to the filename, and then it will probably not need to overwrite anything
    if overwrite or not os.path.isfile(filename + ".jpg") : #Check if overwrite is enabled or if the file doesn't exist and save the image and exit function.
        return filename
    else: #The file does exist so add a number to the filename and save it
        num = 1
        newFilename = filename + " [" + str(num) + "]"
        while os.path.isfile(newFilename + ".jpg"): #While the filename is being used replace the number until the filename isn't in use
            num += 1
            newFilename = filename + " [" + str(num) + "]"
        return newFilename



#Main Code
imageSource = input("Please input filename to be analysed: ")
while not os.path.isfile(IMAGEFOLDER + imageSource): #Loop to check file exists before continuing
    imageSource = input("Could not find \"" + imageSource + "\" in " + IMAGEFOLDER + "\nPlease input filename to be analysed: ")

start = time.clock() #Time the program from this point so that waiting for user input isnt included
saveLocation = saveImg(PROCESSEDFOLDER + imageSource, OVERWRITE)

#Redirecting Standard output of python terminal to a log file
#This class will allow the stdout to be duplicated into the log file so it is also seen in the terminal
#This piece of code was found online at stackoverflow.com by Jacob Gabrielson
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(saveLocation + "(LOG).txt", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
        
orignal = sys.stdout
sys.stdout = Logger()

#Log file info
print("Log file for " + IMAGEFOLDER + imageSource + "\nStarted at: " + str(start) + "s\n")

#Create the grayscale numpy array of the image
imageGray = inputs.openImage(IMAGEFOLDER + imageSource, DEBUGGING, saveLocation)

#Find the corners and then the edges on the image
cornersCoords = corners.findCorners(imageGray, saveLocation, DEBUGGING)
edgeCoords = corners.averageEdges(cornersCoords, FIBRE_WIDTH)

#Finding the fibre lengths
fibreLengths = lengths.findLengths(edgeCoords, MIN_LENGTH, FIBRE_WIDTH, imageGray)
np.savetxt(saveLocation + "Fibre_Lengths.txt", fibreLengths, header = "Fibre lengths: [x0, y0, x1, y1, length01, angle01]")

#Finished
end = time.clock()
print("Time taken: " + str(end-start))

#Set standard out back to its original
sys.stdout = orignal