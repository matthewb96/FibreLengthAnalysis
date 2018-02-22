# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other modules. 
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
import cv2


#Variables and Constants
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source where output files are stored
#IMAGEFOLDER = "..\\Real Images Test\\Real Images Taken\\"
#PROCESSEDFOLDER = "..\\Real Images Test\\ProcessedData\\"
PROCESSEDIMAGES = PROCESSEDFOLDER + "Images\\" #Source for where processed images are stored
PROCESSEDDATA = PROCESSEDFOLDER + "LogDataFiles\\" #Source for where log and data files are stored
DEBUGGING = False
OVERWRITE = False
#Fibre variables
FIBRE_WIDTH = 25 #fibre width
MIN_LENGTH = 4 * FIBRE_WIDTH #Minimum fibre length minimum ratio is approximately 4:1
#Varibles for random generated images
randArraySize = 10000
randFibreNum = 10


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
    if overwrite or not os.path.isfile(PROCESSEDIMAGES + filename + ".jpg") : #Check if overwrite is enabled or if the file doesn't exist and save the image and exit function.
        return filename
    else: #The file does exist so add a number to the filename and save it
        num = 1
        newFilename = filename + " [" + str(num) + "]"
        while os.path.isfile(PROCESSEDIMAGES + newFilename + ".jpg"): #While the filename is being used replace the number until the filename isn't in use
            num += 1
            newFilename = filename + " [" + str(num) + "]"
        return newFilename


def checkRandom(fibreLengths, knownPositions, incorrectFile):
    """
    This function will check the fibre lengths found against the known fibre lengths generated and return a value for the amount correct, incorrect and one away.
    
    arg[0] fibreLengths - numpy array containing the found fibre lengths.
    arg[1] knownPositions - numpy array containing the known positions of fibres.
    arg[2] incorrectFile - file object for saving incorrect fibre data.
    
    Returns three int values for the correct number of fibres, the incorrect number of fibres and the number of fibres that are one away.
    """
    print("Checking found fibres with known fibre positions.")
    #Convert found angle to degrees
    fibreLengths[:,5] = np.rad2deg(fibreLengths[:,5])
    #Round the arrays to int
    knownPositions = np.rint(knownPositions)
    fibreLengths = np.rint(fibreLengths)
    #Sort the two arrays based on length
    knownPositions = knownPositions[knownPositions[:, 4].argsort()]
    fibreLengths = fibreLengths[fibreLengths[:, 4].argsort()]
    
    #Check the lengths are the same
    incorrect = 0
    correct = 0
    oneAway = 0
    diff = knownPositions.shape[0] - fibreLengths.shape[0]
    for i in range(knownPositions.shape[0]):
        try: #In case not all fibres have been found use try statement so the program doesn't crash
            if fibreLengths[i, 4] == knownPositions[i, 4]:
                print("CORRECT: " + str(fibreLengths[i]))
                correct += 1
            elif abs(fibreLengths[i, 4] - knownPositions[i, 4]) <= 1:
                print("One away: Known Data: "+ str(knownPositions[i]) + " Found Data: " + str(fibreLengths[i]))
                oneAway += 1
            else:
                #If there are less fibres found than generated loop through all the missing fibres and check
                if diff > 0:
                    found = False
                    for j in range(diff):
                        j += 1
                        #Check if next one is correct then break 
                        if fibreLengths[i, 4] == knownPositions[i + j, 4]:
                            print("CORRECT: " + str(fibreLengths[i]) + " Skipped " + str(j))
                            correct += 1
                            found = True
                            break
                        elif abs(fibreLengths[i, 4] - knownPositions[i + j, 4]) <= 1:
                            print("One away: Known Data: "+ str(knownPositions[i + j]) + " Found Data: " + str(fibreLengths[i]) + " Skipped " + str(j))
                            oneAway += 1
                            found = True
                            break
                    if found:
                        continue 
                #Fibre is incorrect      
                string = "INCORRECT: Known Data: " + str(knownPositions[i]) + " Found Data: " + str(fibreLengths[i])
                print(string)
                incorrectFile.write(string + "\n")
                incorrect += 1
        except:
            string = ("There are " + str(knownPositions.shape[0]) + " generated fibres but only " + str(fibreLengths.shape[0]) + 
                  " have been found.")
            print(string)
            incorrectFile.write(string + "\n")
            incorrect += 1

    return correct, incorrect, oneAway 


#Get input file
RANDOM = False #Whether or not to generate random images
while True:
    imageSource = input("Please input filename to be analysed, input \"Random #\" to generate and analyse # random images (case sensitive): ")
    if imageSource.find("Random") == 0:
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
saveName = saveImg(imageSource, OVERWRITE)

#Redirecting Standard output of python terminal to a log file
#This class will allow the stdout to be duplicated into the log file so it is also seen in the terminal
#This piece of code was found online at https://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python and edited
class Logger(object):
    def __init__(self, standard):
        self.type = standard
        self.terminal = sys.stdout
        if self.type == "Out":
            self.log = open(PROCESSEDDATA + saveName + "(LOG).txt", "w")

    def write(self, message):
        self.terminal.write(message)
        if self.type == "Out":
            self.log.write(message)
        
    def flush(self):
        self.terminal.flush()
        if self.type == "Out":
            self.log.flush()
        
orignalOut = sys.stdout
originalErr = sys.stderr
sys.stdout = Logger("Out")
sys.stderr = Logger("Error")


#Log file info
if RANDOM:
    print("Log file for " + imageSource + " " + str(numRand) + " images to be generated and analysed.")
    #Initiate variables for random fibre checks
    totCorrect = 0
    totIncorrect = 0
    totOneAway = 0
else:
    print("Log file for " + IMAGEFOLDER + imageSource)
print("\nSave location: " + PROCESSEDIMAGES + saveName + "\nStarted at: " + str(start) + "s\n")


#Loop to allow mulitple images to be analysed at without extra input
numDone = 1
originalSaveName = saveName #Keep the unedited saveLocation 
while numDone <= numAnalyse:
    #Create the grayscale numpy array of the image or generate an image array
    print("\n\n***********************************************************************************\nStarting image " + 
          str(numDone) + " out of " + str(numAnalyse))
    if RANDOM:
        imageGray, knownPositions = inputs.generateImage(FIBRE_WIDTH, MIN_LENGTH, randFibreNum, randArraySize)
        saveName = originalSaveName + " (Random Image " + str(numDone) + ") "
        cv2.imwrite(PROCESSEDIMAGES + saveName + ".jpg", imageGray)
        print("Generated random image " + str(numDone) + " out of " + str(numAnalyse) + "\n")
    else:
        imageGray = inputs.openImage(IMAGEFOLDER + imageSource, DEBUGGING, PROCESSEDIMAGES + saveName)
        print("Opened image " + str(numDone) + " out of " + str(numAnalyse))
    
    #Find the corners and then the edges on the image
    cornersCoords, subpixArray = corners.findCorners(imageGray, PROCESSEDIMAGES + saveName, DEBUGGING)
    edgeCoords = corners.averageEdges(cornersCoords, FIBRE_WIDTH, imageGray)
    
    #Add the edge positions to the subpixArray and then saved the image
    subpixArray[np.rint(edgeCoords[:,1]).astype(int) , np.rint(edgeCoords[:, 0]).astype(int)] = np.array([255, 255, 0])
    #Save a copy of the orginal image given with the corner and edge positions saved on
    cv2.imwrite(PROCESSEDIMAGES + saveName + "Corners and Edges.jpg",subpixArray)
    
    #Finding the fibre lengths
    fibreLengths = lengths.findLengths(edgeCoords, MIN_LENGTH, FIBRE_WIDTH, imageGray)
    np.savetxt(PROCESSEDDATA + saveName + "Fibre_Lengths.txt", fibreLengths, header = "Fibre lengths: [x0, y0, x1, y1, length01, angle01]")
    
    #Draw found fibres
    lengths.drawFound(fibreLengths, imageGray, PROCESSEDIMAGES + saveName)
    
    #If randomly generated image check found fibres against known fibre positions
    if RANDOM:
        with open(PROCESSEDDATA + originalSaveName + " Incorrect Data.txt", "a") as incorrectFile:
            correct, incorrect, oneAway = checkRandom(fibreLengths, knownPositions, incorrectFile)
            #If there is incorrect data in this image then state the image number
            if incorrect != 0: 
                incorrectFile.write("Incorrect Data for Random Image " + str(numDone) + 
                                    "\n\n************************************************\n")

        #Print the data found
        print("Found " + str(incorrect) + " incorrect fibres and " + str(correct) + " correct fibres and " + str(oneAway) + " fibres that are one away.")
        #Add to the total numbers
        totCorrect += correct
        totIncorrect += incorrect
        totOneAway += oneAway
        
    #Update number done
    print("Analysed image " + str(numDone) + " out of " + str(numAnalyse) + 
          "\n***********************************************************************************")
    numDone += 1

#Print values for generated image checks
if RANDOM:
    print("A total of " + str(totCorrect) + " correct fibres have been found, with " + str(totOneAway) + " fibres only one away. " 
          + str(totIncorrect) + " have been incorrectly found.")
    #Remove the incorrect data file if it is empty
    if os.path.getsize(PROCESSEDDATA + originalSaveName + " Incorrect Data.txt") == 0:
        os.remove(PROCESSEDDATA + originalSaveName + " Incorrect Data.txt")

#Finished
end = time.clock()
print("\nTime taken: " + str(end-start))

#Set standard out back to its original
sys.stdout = orignalOut
sys.stderr = originalErr