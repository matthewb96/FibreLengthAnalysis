# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other files and house a lot of the important functions. 
At the minute most of the code is for testing what works and what doesn't.
"""
#All the imported modules
import cv2
import numpy as np
from matplotlib import pyplot as plt, image as mpimg #mimg was previously used for imread
import os #Used in saveImg()

#All the global constants that are needed
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored

#All the global variables that are needed
imageSource = input("Please input filename to be analysed: ")

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
            num += 1
            filename = filename[:(pos+2)] + str(num) + filename[(pos+3):]
        return filename


#First bit of test code opening the image and showing it in the console can't read png when using cv2.imread() instead of mimg.imread()
image = cv2.imread(IMAGEFOLDER + imageSource) #Opens the image and converts it to an array of floating point data between 0 and 1.
img = plt.figure()
plt.subplot(2,3,1)
plt.imshow(image) #Shows the image in the IPython console test purposes
plt.title("Original Image"), plt.yticks([]), plt.xticks([])


#Convert to grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.subplot(2,3,2)
plt.imshow(imageGray)
plt.title("Grayscale Image"), plt.yticks([]), plt.xticks([])


#Finding the edges of the image using Canny Edge detection from opencv
imageUint8 = np.uint8(image) #Converts the image from CV_8U to uint8 so it can be used by Canny()
edges = cv2.Canny(imageUint8, 0, 0) #Finds the edges in the image, the arguments are image, minVal and maxVal
plt.subplot(2,3,3)
plt.imshow(edges, cmap="gray")
plt.title("Edge Image"), plt.yticks([]), plt.xticks([])


#Trying Harris corner detection
imageFloat = np.float32(imageGray)
corners = cv2.cornerHarris(imageFloat, 2, 3, 0.04)
corners = cv2.dilate(corners, None) #Used to mark the corners
plt.subplot(2,3,4)
plt.imshow(corners)
plt.title("Corner Image"), plt.yticks([]), plt.xticks([])


"""
#Trying Line Detection using Hough Line Transform
ret, imageThres = cv2.threshold(imageUint8, 127, 255, cv2.THRESH_BINARY)
lines = cv2.HoughLines(imageThres, 1, np.pi/180, 200)
plt.subplot(2,3,5)
plt.imshow(lines)
plt.title("Line Image"), plt.yticks([]), plt.xticks([])
"""

#Show and save the images
plt.show()
plt.savefig(saveImg(PROCESSEDFOLDER + imageSource))
plt.close(img)