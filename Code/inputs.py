# -*- coding: utf-8 -*-
"""
@author: Matthew
Input module to control the image being inputted or generate a random image for testing.
"""
#Imports
import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage import draw, morphology
from lengths import midpoint

#Functions
def openImage(imageSource, minSize, debug = False, filename = ""):
    """
    This function will open the given image using openCV and convert it to grayscale. 
    It will show the images in the console and produces histograms if debug = True.
    It will return the grayscale image as a numpy array.
    
    arg[0] imageSource - a string containg the source for the image file to be opened.
    arg[1] minSize - int for the minimum amount of pixels to be counted as a fibre.
    arg[2] debug - a boolean that will allow extra code to be run for debugging.
    arg[3] filename - a string containing the source for where the debugging images should be saved.
    
    Returns a numpy array containing the grayscale image data, with small object removed.
    """
    image = cv2.imread(imageSource)
    cv2.imwrite(filename + ".jpg", image)
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Threshold the image
    thresVal, imageGray = cv2.threshold(imageGray, 180, 255, 0)
    
    #Remove small objects using morphology
    morph = morphology.remove_small_holes(imageGray, min_size = minSize, connectivity = 1)
    morphedImage = np.zeros_like(imageGray)
    morphedImage[np.where(morph)] = 255
    
    if debug: #Printing the images and some histograms to the console for debugging purposes
        img = plt.figure()
        #Plot images
        plt.subplot(2,3,1)
        plt.imshow(image) #Shows the image in the IPython console test purposes
        plt.title("Original Image"), plt.yticks([]), plt.xticks([])
        plt.subplot(2,3,2)
        plt.imshow(imageGray)
        plt.title("Grayscale Image"), plt.yticks([]), plt.xticks([])
        plt.subplot(2,3,3)
        plt.imshow(morphedImage)
        plt.title("Morphed Image"), plt.yticks([]), plt.xticks([])
        #Plot histograms
        plt.subplot(2,3,4)
        n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(image))) #Plot histogram of the orignal image array
        plt.title("Original Hist"), plt.yticks([])
        plt.subplot(2,3,5)
        n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(imageGray))) #Plot histogram of the grayscale image array
        plt.title("Grayscale Hist"), plt.yticks([])
        plt.subplot(2,3,6)
        n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(morphedImage))) #Plot histogram of the grayscale image array
        plt.title("Morphed Hist"), plt.yticks([])
        #Show and save the plots
        plt.show()
        try:
            img.savefig(filename + " GrayScale(DEBUG).png")
        except TypeError as error:
            print(error)
            print("Debugging images could not be saved. In input.openFile().")
        plt.close(img)
    
    return morphedImage


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
    print("Generating random image with " + str(numFibres) + " fibres and an array size of " + str(arraySize) + 
          " pixels.\nThe fibre widths are " + str(fibreWidth) + " with lengths between " + str(minLength) + " and " + str(minLength*10) + " pixels.")
    imageArray = np.full((arraySize, arraySize), 255, dtype = np.uint8)
    fibresGen = 0 #Amount of fibres generated
    fibrePositions = np.array([[0, 0, 0, 0, 0, 0]]) #Initiate array for fibre data [x0, y0, x1, y1, length, angle]
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
                
                #Find midpoint for fibre data
                pos1 = midpoint(corner1, corner3)
                pos2 = midpoint(corner2, corner4)
                #Add generated fibre position data
                arrayRow = np.array([pos1[0], pos1[1], pos2[0], pos2[1], length, angle])
                fibrePositions = np.vstack((fibrePositions, arrayRow))
                print("Generated " + str(fibresGen) + " out of " + str(numFibres) + " fibres.")
    
    fibrePositions = np.delete(fibrePositions, 0, 0)          
    return imageArray, fibrePositions

    
def trig(length, angle):
    """
    This function will take an angle and a hipotenuse of a triangle and find the other two lines.
    
    arg[0] length - int value for the length of the hipotenuse.
    arg[1] angle - int value for the angle in degrees next to the hipotenuse.
    
    Returns a numpy array containing lengths of the other two lines.
    """
    lengths = np.array([(length * (np.cos(np.deg2rad(angle))))[0], (length * (np.sin(np.deg2rad(angle))))[0]])
    return lengths

