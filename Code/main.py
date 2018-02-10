# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other modules. 
At the minute most of the code is for testing what works and what doesn't.
"""
#All the imported modules
import os
import time
from datetime import datetime
import inputs 
import corners
import lengths
import sys
import numpy as np


#Variables and Constants
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored
DEBUGGING = False
OVERWRITE = False
RANDOM = False #Whether or not to generate random images
FIBRE_WIDTH = 25 #fibre width
MIN_LENGTH = 4 * FIBRE_WIDTH #Minimum fibre length minimum ratio is approximately 4:1


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



#Get input file
while True:
    imageSource = input("Please input filename to be analysed, input \"Random #\" to generate and analyse # random images (case sensitive): ")
    if imageSource.find("Random") != -1:
        RANDOM = True
        try:
            rand, numRand = imageSource.lower().split(" ")
            numAnalyse = int(numRand) #Number of images to be analysed
        except:
            print("The format you have given is incorrect please try again. \n If you would like random images type \"random #\" (case sensitive)")
            continue
        print("Generating and analysing " + str(numRand) + " random images.")
        imageSource = "Generated Random Image."
        break
    elif not os.path.isfile(IMAGEFOLDER + imageSource):
        print("Could not find \"" + imageSource + "\" in " + IMAGEFOLDER + "\nPlease try again.")
        continue
    else:
        RANDOM = False
        numAnalyse = 1 #Number of images to be analysed
        print("Analysing " + IMAGEFOLDER + imageSource)
        break
        
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
if RANDOM:
    print("Log file for " + imageSource + " " + str(numRand) + " images to be generated and analysed.")
else:
    print("Log file for " + IMAGEFOLDER + imageSource)
print("\nSave location: " + saveLocation + "\nStarted at: " + str(start) + "s\n")

#Loop to allow mulitple images to be analysed at without extra input
numDone = 1
originalSaveLoc = saveLocation #Keep the unedited saveLocation 
while numDone <= numAnalyse:
    #Create the grayscale numpy array of the image or generate an image array
    print("\n\n***********************************************************************************\nStarting image " + 
          str(numDone) + " out of " + str(numAnalyse))
    if RANDOM:
        imageGray = inputs.generateImage(FIBRE_WIDTH, MIN_LENGTH, 10, 10000)
        saveLocation = originalSaveLoc + " (Random Image " + str(numDone) + ") "
        print("Generated random image " + str(numDone) + " out of " + str(numAnalyse) + "\n")
    else:
        imageGray = inputs.openImage(IMAGEFOLDER + imageSource, DEBUGGING, saveLocation)
        print("Opened image " + str(numDone) + " out of " + str(numAnalyse))
    
    #Find the corners and then the edges on the image
    cornersCoords = corners.findCorners(imageGray, saveLocation, DEBUGGING)
    edgeCoords = corners.averageEdges(cornersCoords, FIBRE_WIDTH)
    
    #Finding the fibre lengths
    fibreLengths = lengths.findLengths(edgeCoords, MIN_LENGTH, FIBRE_WIDTH, imageGray)
    np.savetxt(saveLocation + "Fibre_Lengths.txt", fibreLengths, header = "Fibre lengths: [x0, y0, x1, y1, length01, angle01]")
    
    #Draw found fibres
    lengths.drawFound(fibreLengths, imageGray, saveLocation)
    
    #Update number done
    print("Analysed image " + str(numDone) + " out of " + str(numAnalyse) + 
          "\n***********************************************************************************")
    numDone += 1


#Finished
end = time.clock()
print("\nTime taken: " + str(end-start))

#Set standard out back to its original
sys.stdout = orignal