# -*- coding: utf-8 -*-
"""
@author: Matthew
Input module to control the image being inputted or generate a random image for testing.
"""
#Imports
import cv2
from matplotlib import pyplot as plt
import numpy as np

#Functions
def openImage(imageSource, debug = False, filename = ""):
    """
    This function will open the given image using openCV and convert it to grayscale. 
    It will show the images in the console and produces histograms if debug = True.
    It will return the grayscale image as a numpy array.
    
    arg[0] imageSource - a string containg the source for the image file to be opened.
    arg[1] debug - a boolean that will allow extra code to be ran for debugging.
    arg[2] filename - a string containing the source for where the debugging images should be saved.
    
    Returns a numpy array containing the grayscale image data.
    """
    image = cv2.imread(imageSource)
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
            img.savefig(filename)
        except TypeError as error:
            print(error)
            print("Debugging images could not be saved. In openFile().")
        plt.close(img)
    
    return imageGray


def generateImage():
    """
    This function will randomly generate an image array for testing.
    """