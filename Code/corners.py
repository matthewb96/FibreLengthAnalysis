# -*- coding: utf-8 -*-
"""
@author: Matthew
This module contains all the functions that will find the corners and edges of the fibres, once given an image array.
"""
#Imports
import numpy as np
from lengths import coordDist, checkBlack
import cv2
from matplotlib import pyplot as plt


#Functions
def averageEdges(cornerPos, FIBREWIDTH, imageArray):
    """
    Finds the corners that are close enough together to be considered part of the short edge 
    and averages them to return one position for each edge.
    
    arg[0] cornerPos - numpy array containing the coordinates for the corners.
    arg[1] FIBREWIDTH - int value for width of the fibres.
    arg[2] imageArray - numpy array containing the image data.
    """
    averageCoords = np.array([[0,0]]) #Initiate array with temp values
    arrayLength, width = cornerPos.shape #Find length of axis 0
    foundMidpoint = np.full(arrayLength, False, dtype = bool)
    for i in range(arrayLength):
        if foundMidpoint[i]: #If corner is already part of an edge
            continue
        for j in range(i, arrayLength): #Generates list of numbers starts at i so to not repeat numbers already compared
            if foundMidpoint[j]: #If corner is already part of an edge
                continue
            distance = coordDist(cornerPos[i], cornerPos[j])
            #Checking against a slightly larger number because if the corners are not exact due to blurring they might be slightly further apart than fibre width
            if  distance <= int(np.rint(FIBREWIDTH*1.1)) and distance != 0: 
                average = np.array([(cornerPos[i] + cornerPos[j])/2])
                #Check the midpoint is part of a fibre, check all pixels within one pixel of midpoint
                for k in [(0,0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    x = np.rint(average[0, 0] + k[0])
                    y = np.rint(average[0, 1] + k[1])
                    pos = np.array([x, y], dtype = int)
                    if checkBlack(pos, imageArray):
                        #If one of the pixels next to the midpoint is black then consider it part of a fibre and save the midpoint
                        averageCoords = np.vstack((averageCoords, average))
                        foundMidpoint[i] = True
                        foundMidpoint[j] = True
                        break
    
    #Add coordinates of corners where no midpoint has been found to the midpoint array
    if not foundMidpoint.all():
        elements = np.where(foundMidpoint == False)
        otherCorners = cornerPos[elements]
        averageCoords = np.concatenate((averageCoords, otherCorners))
    
    averageCoords = np.delete(averageCoords, 0, 0) #Delete temp values
    print("# Endpoints: " + str(averageCoords.shape[0]))
    return averageCoords

def findCorners(imageArray, filename, debug = False):
    """
    Finds the corners of the fibres in a given image array using Harris corner detection and returns an array of coordinates for the corners.
    Saves images showing the positions of the corners that are found on the original image. 
    Also plots the images being used and histograms showing the data if debug = True.
    
    arg[0] imageArray - a numpy array containing grayscale image data.
    arg[1] filename - a string giving the source for where outputs should be saved.
    arg[2] debug - a boolean that will allow extra code to be run for debugging.
    
    Returns a tuple containing two numpy arrays. The first containing the coordinates for every corner found and the second being the orignal image array
    with the subpixel and centroid points added to it.
    """
    #Harris corner detection
    imageFloat = np.float32(imageArray)
    corners = cv2.cornerHarris(imageFloat.copy(), 10, 15, 0.04)
    corners = cv2.dilate(corners, None) #Used to mark the corners
    
    # Find the corners more accurately using cornerSubPix
    thresVal, cornersThres = cv2.threshold(corners, 0.5*corners.max(), 255, 0)
    cornersThres = np.uint8(cornersThres)
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(cornersThres)
    centroids = np.delete(centroids, 0, 0) #Delete the first row in the array because it does not refer to a corner

    #Check centroid positions are on a fibre
    rowsDelete = []
    for i in range(centroids.shape[0]):
        if not checkBlack(centroids[i], imageArray):
            #Remove the centroid if it is not on a fibre
            rowsDelete.append(i)
    #Delete rows
    centroids = np.delete(centroids, rowsDelete, 0)
    
    #Sub Pixel Function
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    cornersSubPix = cv2.cornerSubPix(imageFloat,            #Input image
                                     np.float32(centroids), #Initial coordinates of the original corners
                                    (5,5),                  #Size of search window        
                                    (-1,-1),                #Size of dead region (-1,-1) is no dead region
                                    criteria)               #Criteria to stop the iteration
    print("# Corners Found: " + str(cornersSubPix.shape[0]))
    
    # Now draw orginal image array with corners plotted
    imageArray = cv2.cvtColor(imageArray, cv2.COLOR_GRAY2BGR)
    res = np.hstack((centroids,cornersSubPix))
    res = np.int0(res)
    imageArray[res[:,1],res[:,0]]=[0,0,255]
    imageArray[res[:,3],res[:,2]] = [0,255,0]
    
          
    if debug: #Plot images for debugging
        #Save images showing Harris corner detection outputs
        cv2.imwrite(filename + " Harris(DEBUG).jpg",corners)
        cv2.imwrite(filename + " HarrisThres(DEBUG).jpg",cornersThres)
        
        img = plt.figure()
        #Plot corners
        plt.subplot(2,2,1)
        plt.imshow(corners)
        plt.title("Corner Image"), plt.yticks([]), plt.xticks([])
        #Plot cornersThres
        plt.subplot(2,2,2)
        plt.imshow(cornersThres)
        plt.title("CornerThres Image"), plt.yticks([]), plt.xticks([])
        #Plot histograms
        plt.subplot(2,2,3)
        plt.hist(np.ndarray.flatten(np.uint8(corners))) #Plot histogram of the image array
        plt.title("Corner Hist"), plt.yticks([])
        plt.subplot(2,2,4)
        plt.hist(np.ndarray.flatten(np.uint8(cornersThres))) #Plot histogram of the image array
        plt.title("Corner Thres Hist"), plt.yticks([])
        #Show and save the plots
        plt.show()
        try:
            img.savefig(filename + " Corners(DEBUG).png")
        except TypeError as error:
            print(error)
            print("Debugging images could not be saved. In corners.findCorners().")
        plt.close(img)

    return cornersSubPix, imageArray

