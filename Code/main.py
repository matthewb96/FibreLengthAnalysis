# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other modules. 
"""
####Imports####

import os
import time
from datetime import datetime
import inputs 
import corners
import lengths
import sys
import numpy as np
import cv2
import graphing


####Variables####
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source where output files are stored
PROCESSEDIMAGES = PROCESSEDFOLDER + "Images\\" #Source for where processed images are stored
PROCESSEDDATA = PROCESSEDFOLDER + "LogDataFiles\\" #Source for where log and data files are stored
DEBUGGING = False
OVERWRITE = False
global imageStats
imageStats = [["Objects Found", "Fibres Found", "Coordinates Missed"]]
#Fibre variables
FIBRE_WIDTH = 10
MIN_LENGTH = 30


####Functions####

def saveImg(directory, filename, timeAndDate, overwrite = False):
    """
    This function will save the images that have been created into a file with the name "filename", by default it will not overwrite existing images.
    Currently not working as planned as plt.saveFig() won't work inside the function so instead this function just finds the next free filename and returns it.
    
    Arguments:
        directory - this is the directory the file should be saved in.
        filename - This is the name and source of the file to be saved and should be a string.
        overwrite - This defines whether or not an image can be overwrited, it is a boolean. (Default = False)
        
    Returns a string of an edited version of the filename that won't overwrite anything.
    """
    pos = filename.rfind(".") #Find the position of the start of the file type to put a number before it 
    filename = filename[:pos] + timeAndDate #Add the date and time to the filename, and then it will probably not need to overwrite anything
    if overwrite or not os.path.isfile(directory + filename + ".jpg") : #Check if overwrite is enabled or if the file doesn't exist and save the image and exit function.
        return filename
    else: #The file does exist so add a number to the filename and save it
        num = 1
        newFilename = filename + " [" + str(num) + "]"
        while os.path.isfile(directory + newFilename + ".jpg"): #While the filename is being used replace the number until the filename isn't in use
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


def analyseImage(saveData, loadData, FIBRE_WIDTH, MIN_LENGTH, numDone, numAnalyse, DEBUGGING = False, RANDOM = False, randData = None):
    """
    Function that contains all the calls to other functions to fully analyse a single image.
    
    arg[0] saveData - tuple containg 3 strings first being path to processed data folder, second path to processed images folder and third being the save filename.
    arg[1] loadData - tuple containing 2 strings first being path to image folder and second being the filename for image to be anlysed.
    arg[2] FIBRE_WIDTH - int value for the fibre width.
    arg[3] MIN_LENGTH - int value for the minimum length of a fibre.
    arg[4] numDone - int value for number of images analysed.
    arg[5] numAnalyse - int value for the total number of images to analyse.
    arg[6] DEBUGGING - boolean value for whether in debugging mode or not.
    arg[7] RANDOM - boolean value for whether random image generation or not.
    arg[8] randData - tuple containing the random fibre number and array size to be generated.
    """
    #Extract save data from tuple
    PROCESSEDDATA, PROCESSEDIMAGES, originalSaveName = saveData
    IMAGEFOLDER, imageSource = loadData
    #Create the grayscale numpy array of the image or generate an image array
    if RANDOM:
        randFibreNum, randArraySize = randData
        imageGray, knownPositions = inputs.generateImage(FIBRE_WIDTH, MIN_LENGTH, randFibreNum, randArraySize)
        saveName = originalSaveName + " (Random Image " + str(numDone) + ") "
        cv2.imwrite(PROCESSEDIMAGES + saveName + ".jpg", imageGray)
        print("Generated random image " + str(numDone) + " out of " + str(numAnalyse) + "\n")
    else:
        saveName = originalSaveName
        imageGray, numObjects = inputs.openImage(IMAGEFOLDER + imageSource, int(FIBRE_WIDTH * MIN_LENGTH * 0.9), DEBUGGING, PROCESSEDIMAGES + saveName)
        print("Opened image " + str(numDone) + " out of " + str(numAnalyse))
        print(str(numObjects) + " objects found in the image.")
        knownPositions = None
    
    #Find the corners and then the edges on the image
    cornersCoords, subpixArray = corners.findCorners(imageGray, PROCESSEDIMAGES + saveName, DEBUGGING)
    edgeCoords = corners.averageEdges(cornersCoords, FIBRE_WIDTH, imageGray)
    
    #Add the edge positions to the subpixArray and then saved the image
    subpixArray[np.rint(edgeCoords[:,1]).astype(int) , np.rint(edgeCoords[:, 0]).astype(int)] = np.array([255, 255, 0])
    #Save a copy of the orginal image given with the corner and edge positions saved on
    cv2.imwrite(PROCESSEDIMAGES + saveName + "Corners and Edges.jpg", subpixArray)
    
    #Finding the fibre lengths
    fibreLengths, coordsNotFound = lengths.findLengths(edgeCoords, MIN_LENGTH, FIBRE_WIDTH, imageGray)
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
        #Variables to be returned
        correctness = (correct, oneAway, incorrect)
    else:
        correctness = None
    
    if DEBUGGING:
        #Produce graphs
        graphing.lengthDistribution(fibreLengths, PROCESSEDIMAGES + saveName, title = "Length Distribution of the Found Fibres")
        if RANDOM:
            graphing.lengthDistribution(knownPositions, PROCESSEDIMAGES + saveName, title = "Length Distribution of the Known Fibres")
            
    print("Image data:\nThere are " + str(numObjects) + " objects found in the image, " + str(len(fibreLengths)) + " of which are found to be fibres. " + str(coordsNotFound) + " endpoints were not found to be part of a fibre.")
    imageStats.append([numObjects, len(fibreLengths), coordsNotFound])
    
    return correctness, knownPositions, fibreLengths


####Main Code####
    
#Get input file
RANDOM = False #Whether or not to generate random images
MULTI_IMAGES = False #Whether or not analysing multiple images
originalImageFolder = IMAGEFOLDER #Keep original image folder if error in input
while True:
    IMAGEFOLDER = originalImageFolder
    inputString = input("Please input filename(s) to be analysed (no spaces in filenames, spaces between each file), input \"Random (loop number) (fibre number) (array size)\" to" + 
                        """ generate and analyse # random images (case sensitive) or input "Dir directory path" to analyse a full directory e.g. "Dir C:\\\ Users \\\ Directory":""")
    try:
        temp = str(inputString).split(" ")
        source = []
        #Remove whitespace and any blank elements
        for i in temp:
            i.strip()
            if i != "":
                source.append(i)    
        del temp
    except Exception as error:
        print("Error: " + str(error) + """\nThe format you have given is incorrect please try again. 
              \nIf you would like random images type \"random (loop number) (fibre number) (array size)\" (case sensitive).
              \nIf you would like to input one or multiple files leave a space between separate files
              and the filenames must not contain spaces.""")
        continue
    
    if source[0] == "Random":
        RANDOM = True
        temp = source
        source = []
        try:
            i = 1
            while i < len(temp):
                source.append((int(temp[i]), int(temp[i + 1]), int(temp[i + 2])))
                i += 3
        except Exception as error:
            print("The format you have given is incorrect please try again. \n If you would like random images type \"random (loop number) (fibre number) (array size)\" (case sensitive)")
            print(error)
            continue
        #Ask user if correct
        print("Random image with (number of loops, number of fibres, array size)" + str(source))
        check = input("Are these the correct values(y/n): ")
        if check == "y":
            break
        else:
            print("Please try again.")
            continue
    elif source[0] == "Dir":
        #Get a list of all image files in directory
        MULTI_IMAGES = True
        directory = source[1]
        source.clear()
        IMAGEFOLDER = directory + "\\"
        PROCESSEDFOLDER = directory + "\\"
        PROCESSEDDATA = PROCESSEDFOLDER + "LogDataFiles\\"
        PROCESSEDIMAGES = PROCESSEDFOLDER + "Images\\"
        #Create data folders
        if not os.path.exists(PROCESSEDDATA):
            os.mkdir(PROCESSEDDATA)
        if not os.path.exists(PROCESSEDIMAGES):
            os.mkdir(PROCESSEDIMAGES)
        for i in os.listdir(IMAGEFOLDER):
            pos = i.rfind(".")
            if i[pos:] == ".jpg" or i[pos:] == ".bmp":
                source.append(i)
    #Check all images exist
    if len(source) > 1:
        MULTI_IMAGES = True
    for i in source:
        if not os.path.isfile(IMAGEFOLDER + i):
            print("Could not find \"" + i + "\" in " + IMAGEFOLDER + "\nPlease try again.")
            continue
    #Ask user if correct
    print(source)
    check = input("Are these the correct files(y/n): ")
    if check == "y":
        break
    else:
        print("Please try again.")
        continue

     
start = time.clock() #Time the program from this point so that waiting for user input isnt included
timeAndDate = "[" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) +  "]" #Date and time to be used on filenames
if RANDOM:
    logName = saveImg(PROCESSEDIMAGES, "Generating_Random_Images", timeAndDate, OVERWRITE)
elif MULTI_IMAGES:
    logName = saveImg(PROCESSEDIMAGES, "Multiple_Images", timeAndDate, OVERWRITE)
else:
    logName = saveImg(PROCESSEDIMAGES, source[0], timeAndDate, OVERWRITE)

#Redirecting Standard output of python terminal to a log file
#This class will allow the stdout to be duplicated into the log file so it is also seen in the terminal
#This piece of code was found online at https://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python and edited
class Logger(object):
    def __init__(self, standard):
        self.type = standard
        self.terminal = sys.stdout
        if self.type == "Out":
            self.log = open(PROCESSEDDATA + logName + "(LOG).txt", "w")

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
    print("Log file for " + str(timeAndDate) + " random image with (number of loops, number of fibres, array size)" + str(source))
    #Initiate variables for random fibre checks
    totCorrect = 0
    totIncorrect = 0
    totOneAway = 0
else:
    if MULTI_IMAGES:
        print("Log file for " + IMAGEFOLDER + " containing multiple images:\n" + str(source))
    else:
        print("Log file for " + IMAGEFOLDER + source[0])
print("\nStarted at: " + str(start) + "s\n")
totFibreLengths = np.array([[0,0,0,0,0,0]])
totKnownPositions = np.array([[0,0,0,0,0,0]])

#Loop to allow mulitple images to be analysed at without extra input
for image in source:
    if RANDOM:
        name = "RandomSettings(" + str(image[0]) + "loops," + str(image[1]) + "fibres," + str(image[2]) + "arraySize) "
        saveName = saveImg(PROCESSEDIMAGES, name, timeAndDate, OVERWRITE)
        randData = int(image[1]), int(image[2])
    else:
        saveName = saveImg(PROCESSEDIMAGES, image, timeAndDate, OVERWRITE)
    saveData = PROCESSEDDATA, PROCESSEDIMAGES, saveName
    loadData = IMAGEFOLDER, image
    imageNum = source.index(image) + 1
    print("\n\n###################################################################################\nAnalysing image " + str(image) 
          + ", number " + str(imageNum) + " out of " + str(len(source)) + 
          "\n###################################################################################\n")
    if RANDOM:        
        #Loop for random images
        numDone = 1
        numAnalyse = image[0]
        while numDone <= numAnalyse:
            print("\n\n***********************************************************************************\nLoop " + 
              str(numDone) + " out of " + str(numAnalyse))
            #Analyse image
            correctness, knownPositions, fibreLengths = analyseImage(saveData, loadData, FIBRE_WIDTH, MIN_LENGTH, numDone, numAnalyse, DEBUGGING, RANDOM, randData)
            totCorrect += correctness[0]; totOneAway += correctness[1]; totIncorrect += correctness[2]
            totFibreLengths = np.concatenate((totFibreLengths, fibreLengths))
            totKnownPositions = np.concatenate((totKnownPositions, knownPositions))
            #Update number done
            print("Analysed image loop " + str(numDone) + " out of " + str(numAnalyse) + 
                  "\n***********************************************************************************")
            numDone += 1
    else:
        correctness, knownPositions, fibreLengths = analyseImage(saveData, loadData, FIBRE_WIDTH, MIN_LENGTH, imageNum, len(source), DEBUGGING)
        totFibreLengths = np.concatenate((totFibreLengths, fibreLengths))
    #Print values for generated image checks
    if RANDOM:
        print("A total of " + str(totCorrect) + " correct fibres have been found, with " + str(totOneAway) + " fibres only one away. " 
              + str(totIncorrect) + " have been incorrectly found.")
        #Remove the incorrect data file if it is empty
        if os.path.getsize(PROCESSEDDATA + saveName + " Incorrect Data.txt") == 0:
            os.remove(PROCESSEDDATA + saveName + " Incorrect Data.txt")
    
    #End of this image analysis
    print("\n\n###################################################################################\nAnalysed image " + str(image) 
          + ", number " + str(imageNum) + " out of " + str(len(source)) + 
          "\n###################################################################################\n")


totFibreLengths = np.delete(totFibreLengths, 0, 0)
totKnownPositions = np.delete(totKnownPositions, 0, 0)
#Producing graphs for combined data
#Length Distribution
np.savetxt(PROCESSEDDATA + saveName + "Total_Fibre_Lengths.txt", totFibreLengths, header = "Fibre lengths: [x0, y0, x1, y1, length01, angle01]")
print("Producing length distribution graphs for total data.")
graphing.lengthDistribution(totFibreLengths, PROCESSEDIMAGES + saveName, title = "Length Distribution of the Found Fibres for the Total Data")
if RANDOM:
    graphing.lengthDistribution(totKnownPositions, PROCESSEDIMAGES + saveName, title = "Length Distribution of the Known Fibres for the Total Data")

#Finished
end = time.clock()
print("\nTime taken: " + str(end-start))
print("Log file location: " + PROCESSEDDATA + logName + "(LOG).txt")
#Set standard out back to its original
sys.stdout = orignalOut
sys.stderr = originalErr