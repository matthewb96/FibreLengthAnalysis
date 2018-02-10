# -*- coding: utf-8 -*-
"""
@author: Matthew
Input module to control the image being inputted or generate a random image for testing.
"""
#Imports
import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage import draw

#Functions
def openImage(imageSource, debug = False, filename = ""):
    """
    This function will open the given image using openCV and convert it to grayscale. 
    It will show the images in the console and produces histograms if debug = True.
    It will return the grayscale image as a numpy array.
    
    arg[0] imageSource - a string containg the source for the image file to be opened.
    arg[1] debug - a boolean that will allow extra code to be run for debugging.
    arg[2] filename - a string containing the source for where the debugging images should be saved.
    
    Returns a numpy array containing the grayscale image data.
    """
    image = cv2.imread(imageSource)
    cv2.imwrite(filename + ".jpg", image)
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if debug: #Printing the images and some histograms to the console for debugging purposes
        img = plt.figure()
        #Plot images
        plt.subplot(2,2,1)
        plt.imshow(image) #Shows the image in the IPython console test purposes
        plt.title("Original Image"), plt.yticks([]), plt.xticks([])
        plt.subplot(2,2,2)
        plt.imshow(imageGray)
        plt.title("Grayscale Image"), plt.yticks([]), plt.xticks([])
        #Plot histograms
        plt.subplot(2,2,3)
        n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(image))) #Plot histogram of the orignal image array
        plt.title("Original Hist"), plt.yticks([])
        plt.subplot(2,2,4)
        n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(imageGray))) #Plot histogram of the grayscale image array
        plt.title("Grayscale Hist"), plt.yticks([])
        #Show and save the plots
        plt.show()
        try:
            img.savefig(filename + " GrayScale(DEBUG).jpg")
        except TypeError as error:
            print(error)
            print("Debugging images could not be saved. In input.openFile().")
        plt.close(img)
    
    return imageGray


def generateImage(fibreWidth, minLength, numFibres, arraySize):
    """
    This function will randomly generate an image array for testing.
    
    arg[0] fibreWidth - int value stating the width all the fibres should be.
    arg[1] minLength - int value for the minimum length a fibre can be.
    arg[2] numFibres - int value for the amount of fibres that should be generated.
    arg[3] arraySize - int value stating the size of the array, e.g. 10 would be a 10*10 array.
    
    Returns a tuple containing two numpy arrays, one containing the image array and the other containing the fibre lengths and positions.
    """
    #Inititate the image array with all white pixels
    imageArray = np.full((arraySize, arraySize), 255, dtype = np.uint8)
    fibresGen = 0 #Amount of fibres generated
    #Continue generating fibres until enough are generated
    while fibresGen < numFibres:
        #Randomly generate the fibre
        length = np.random.randint(minLength, (minLength * 10), size = 1)
        corner1 = np.random.randint(arraySize, size = 2)
        angle = np.random.randint(360, size = 1)
        lengths = trig(length, angle)
        corner2 = np.array([corner1[0] + lengths[0], corner1[1] + lengths[1]])
        if np.all(corner2 < arraySize) and np.all(corner2 > 0): 
            #If corner2 is within boundries then generate corner 3 and 4 at 90degrees and the width of the fibre away
            lengths = trig(fibreWidth, angle + 90)
            corner3 = np.array([(corner1[0] + lengths[0]), (corner1[1] + lengths[1])])
            corner4 = np.array([(corner2[0] + lengths[0]), (corner2[1] + lengths[1])])
            if np.all(corner3 < arraySize) and np.all(corner3 > 0) and np.all(corner4 < arraySize) and np.all(corner4 > 0):
                #If corner 3 and 4 are within boundries then the whole fibre is so it can be drawn
                #Round all corners to nearest int
                corner2 = np.rint(corner2).astype(int)
                corner3 = np.rint(corner3).astype(int)
                corner4 = np.rint(corner4).astype(int)
                #Create two arrays containing the coordinates for the rows and the columns
                rows = np.array([corner1[0], corner3[0], corner4[0], corner2[0]])
                cols = np.array([corner1[1], corner3[1], corner4[1], corner2[1]])
                #Returns the coordinates that are part of the polygone (fibre)
                rr, cc = draw.polygon(rows, cols)
                imageArray[rr, cc] = 0
                fibresGen += 1
                print("Generated " + str(fibresGen) + " out of " + str(numFibres) + " fibres.")
                
    return imageArray

    
def trig(length, angle):
    """
    This function will take an angle and a hipotenuse of a triangle and find the other two lines.
    
    arg[0] length - int value for the length of the hipotenuse.
    arg[1] angle - int value for the angle in degrees next to the hipotenuse.
    
    Returns a numpy array containing lengths of the other two lines.
    """
    lengths = np.array([(length * (np.cos(np.deg2rad(angle))))[0], (length * (np.sin(np.deg2rad(angle))))[0]])
    return lengths

