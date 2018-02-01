# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other modules. 
At the minute most of the code is for testing what works and what doesn't.
"""
#All the imported modules
import os #Used in saveImg()
import time

#All the global constants that are needed
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored
DEBUGGING = False

#All the global variables that are needed
imageSource = input("Please input filename to be analysed: ")
start = time.clock() #Time the program from this point so that waiting for user input isnt included
#Some functions are defined that will be used later

def saveImg(filename, overwrite = False):
    """
    This function will save the images that have been created into a file with the name "filename", by default it will not overwrite existing images.
    Currently not working as planned as plt.saveFig() won't work inside the function so instead this function just finds the next free filename and returns it.
    
    Arguments:
        filename - This is the name and source of the file to be saved and should be a string.
        overwrite - This defines whether or not an image can be overwrited, it is a boolean. (Default = False)
        
    Returns a string of an edited version of the filename that won't overwrite anything.
    
    """
    if overwrite or not os.path.isfile(filename) : #Check if overwrite is enabled or if the file doesn't exist and save the image and exit function.
        return filename
    else: #The file does exist so add a number to the filename and save it
        pos = filename.rfind(".") #Find the position of the start of the file type to put a number before it
        num = 1
        filename = filename[:pos] + " [" + str(num) + "]" + filename[pos:] 
        while os.path.isfile(filename): #While the filename is being used replace the number until the filename isn't in use
            digits = len(str(num))
            num += 1
            filename = filename[:(pos+2)] + str(num) + filename[(pos+2+digits):]
        return filename



           
   





#Find fibre length
edges = averageEdges(cornersSubPix)
print("# Endpoints: " + str(edges.shape[0]))
fibresLength = findLengths(edges)
print("Lengths Found: " + str(fibresLength.shape[0]))
print("Fibre lengths: [x0, y0, x1, y1, length01]\n")

end = time.clock()
print("Time taken: " + str(end-start))