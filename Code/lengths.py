# -*- coding: utf-8 -*-
"""
@author: Matthew
This module will contain all the functions for finding the lengths of the fibres.
"""

#Imports
import numpy as np
import time
import cv2
from skimage import draw

#Functions
def coordDist(pos1, pos2):
    """
    Takes two arrays of length 2 and will find the length between them.
    
    arg[0] pos1 - a numpy array containing the first set of coordinates.
    arg[1] pos2 - a numpy array containing the second set of coordinates.
    
    Returns a float that is the distance between the two sets of coordinates.
    """
    xDiff, yDiff = abs(pos1 - pos2)
    hippotenuse = np.sqrt(xDiff**2 + yDiff**2)
    return hippotenuse


def findLengths(coords, minLength, fibreWidth, imageArray):
    """
    Accepts a 2D numpy array of coordinates and finds the length between all combinations of coordinates that have a line between them.
    
    arg[0] coords - numpy array containing the end of fibre coordinates that should be analysed.
    arg[1] minLength - integer value of the minimum distance apart the coordinates can be to be part of a fibre.
    arg[2] fibreWidth - int value for the maximum width of a fibre.
    arg[2] imageArray - a numpy array containing the image data for checking two coordinates are part of a single fibre.
    
    Returns array containing the coordinates of the line and the line length 
    [[x0, y0, x1, y1, length01]
     [x0, y0, x2, y2, length02] 
     ...]
    """
    lineLengths = np.array([[0, 0, 0, 0, 0, 0]]) #For each line in the array [x, y, x1, y1, length, angle]
    arrayLength, width = coords.shape #Find length of axis 0
    lengthsChecked = 0
    coordsChecked = np.full(arrayLength, False) #Array corresponding to coords that will be set to true once a corner has been connected so none are found twice
    for i in range(arrayLength):
        if coordsChecked[i]: #if corner is already part of a fibre
            continue
        for j in range(i + 1, arrayLength): #Generates list of numbers starts at i so to not to repeat numbers already compared
            if coordsChecked[j]: #if corner is already part of a fibre
                continue
            numChecked = np.count_nonzero(coordsChecked == True)
            if numChecked % 4 == 0:
                print("Current clock "+ str(time.clock()) + "s. " + str(numChecked) + " out of " + str(arrayLength) + " coordinates found.")
            distance = coordDist(coords[i], coords[j])
            if distance < minLength:
                continue #Skip this loop if the distance is less than the minimum length of a fibre
            lengthsChecked += 1 #Amount of lengths needed to be checked by checkLine()
            if not checkLine(coords[i], coords[j], fibreWidth, imageArray):
                continue #Skip loop if corners not joined by solid black pixels ie not part of the same fibre
            
            #Found a fibre so add all data to the array
            angle = findAngle(coords[i], coords[j])
            arrayRow = np.array([coords[i][0], coords[i][1], coords[j][0], coords[j][1], distance, angle])
            lineLengths = np.vstack((lineLengths, arrayRow))
            coordsChecked[i] = True
            coordsChecked[j] = True
            break #If the code reaches this then a joined fibre is found so there is no need to carry on checking all other corners against this one
    
    #Print info and remove the empty first line of the array before returning it
    numChecked = np.count_nonzero(coordsChecked == True)
    print("Final: " + str(numChecked) + " out of " + str(arrayLength) + " coordinates found.")
    lineLengths = np.delete(lineLengths, 0, 0)
    print("Lengths checked: " + str(lengthsChecked))
    print("Lengths Found: " + str(lineLengths.shape[0]))
    return lineLengths
 

def checkLineOld(pos1, pos2, imageArray):
    """
    This function takes two sets of coordinates and checks there is a solid line of pixels between them.
    This function checks every single pixel between the two coordinates which is why it is so slow.
    This is the older less efficient algorithm a new function has been written.
    
    arg[0] pos1 - numpy array containing the first set of coordinates.
    arg[1] pos2 - numpy array containing the second set of coordinates.
    arg[2] imageArray - numpy array containing the image data that should be checked.
    
    Returns boolean value for if there is a solid line between them or not.
    """
    #Create two booleans to allow for a for either for loop to be ignored
    horizontal = False
    vertical = False
    #Round the coords to integers
    pos1 = np.rint(pos1)
    pos2 = np.rint(pos2)
    #Check they aren't same corners or that the line isn't vertical
    #Find an equation for the line between the two postions y = mx + c
    if pos1[0] == pos2[0] and pos1[1] == pos2[1] : #Same corner
        return False
    elif pos1[0] == pos2[0]: #Completely vertical line 
        xVal = pos1[0]
        vertical = True
    elif pos1[1] == pos2[1]: #Completely horizontal line
        gradient = 0
        yIntercept = pos1[1]
        horizontal = True
    else: #The line has a gradient
        gradient = (pos1[1]-pos2[1])/(pos1[0]-pos2[0])
        yIntercept = pos1[1] - (gradient*pos1[0])
        if np.rint(yIntercept) != np.rint(pos2[1] - (gradient*pos2[0])): #Rounding errors can cause these to not be equal so rounded to int for checking
            print("Cannot find the equation for the line between " + str(pos1) + " and " + str(pos2))
            return False
    
    #Loop through equation checking each postion is black
    if not vertical: #If the line is vertical all x will be the same so no need to loop through x
        #First loop through the x postions calculating corresponding y
        for i in range(int(min(pos1[0], pos2[0])), int(max(pos1[0], pos2[0])) + 1):
            yVal = (gradient * i) + yIntercept
            pos = np.array([i, yVal])
            if not checkBlack(pos, imageArray):
                return False
    
    if not horizontal: #If line is horizontal all y will be the same 
        #Next loop through the y positions calculating corresponding x
        for i in range(int(min(pos1[1], pos2[1])), int(max(pos1[1], pos2[1])) + 1):
            if vertical: 
                pass #Do nothing x is constant
            else:
                xVal = (i - yIntercept)/gradient
            pos = np.array([xVal, i])
            if not checkBlack(pos, imageArray):
                return False
            
    #If both loops make it all the way through then the postions must be connected by a fibre so return True
    return True

def checkLine(pos1, pos2, fibreWidth, imageArray):
    """
    This function is a rewrite of checkLineOld() and uses a more efficient algorithm. This algorithm works be finding the midpoint of the two fibre ends and checking it is black,
    then finding the next midpoint and checking that. It does this until the midpoint is less than the width of a fibre.
    
    arg[0] pos1 - numpy array containing the first set of coordinates.
    arg[1] pos2 - numpy array containing the second set of coordinates.
    arg[2] fibreWidth - int value for the width of a fibre
    arg[3] imageArray - numpy array containing the image data that should be checked.
    
    Returns boolean value True if the line is part of a fibre and False if not.
    """
    mid1 = midpoint(pos1, pos2)
    mid2 = midpoint(pos1, pos2)
    #Check to within half of fibre width
    while int(coordDist(mid1, pos1)) > (fibreWidth/2) and int(coordDist(mid2, pos2)) > (fibreWidth/2):
        partOf = False #Set to true when midpoint is part of a fibre
        #Check the midpoint is part of a fibre, check all pixels within one pixel of midpoint
        for i in [(0,0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            check1 = np.array([(mid1[0] + i[0]), mid1[1] + i[1]])
            check2 = np.array([(mid2[0] + i[0]), mid2[1] + i[1]])
            if checkBlack(check1, imageArray) and checkBlack(check2, imageArray):
                #If one of the pixels next to the midpoint is black then consider it part of a fibre
                mid1 = midpoint(pos1, mid1)
                mid2 = midpoint(pos2, mid2)
                partOf = True
                break
        #Only false if midpoint or surrounding pixels aren't part of a fibre    
        if not partOf:
            return False
        
    #If the loop has suceeded then pos1 and pos2 are part of the same fibre
    return True
    

def midpoint(pos1, pos2):
    """
    This function will find the midpoint between two given coordinates.
    
    arg[0] pos1 - numpy array containing first set of coordinates.
    arg[1] pos2 - numpy array conataing second set of coordinates.
    
    Returns a numpy array containing the coordinates of the midpoint between pos1 and pos2
    """
    middle = (pos1 + pos2)/2
    return middle


def checkBlack(pos, image):
    """
    This function checks if the pixel at the given position is black and therefore part of a fibre.
    
    arg[0] pos - a numpy array containing the coordinates for the pixel that should be checked.
    arg[1] image - a numpy array containing the image data that should be checked.
    
    Returns boolean value of True if the pixel is part of a fibre and False if it is not.
    """
    pixel = image[int(pos[1])][int(pos[0])]
    if pixel <= (0.5*np.amax(image)):
        return True 
    else:
        return False


def findAngle(pos1, pos2):
    """
    This function will find the angle between two given sets of coordinates.
    
    arg[0] pos1 - numpy array containing the first set of coordinates.
    arg[1] pos2 - numpy array containing the second set of coordinates.
    
    Returns the angle in radians between the two coordinates as a float.
    """
    diff = abs(pos1 - pos2)
    angle = np.arctan(diff[0]/diff[1])
    return angle
    
    
def drawFound(fibreLengths, imageArray, filename):
    """
    This function will draw a red line on the found fibres, and save a new image containing the drawn lines.
    
    arg[0] fibreLengths - the numpy array containing the fibre coordinates and lengths.
    arg[1] imageArray - numpy array containing the image data for a grayscale image.
    arg[2] saveLocation - string containing the source for where the image will be saved.
    
    Returns nothing.
    """
    #Draw on the found fibres
    print("\nDrawing found fibres.")
    image = cv2.cvtColor(imageArray, cv2.COLOR_GRAY2BGR)
    for i in range(fibreLengths.shape[0]):
        print("Drawing " + str(i + 1) + " out of " + str(fibreLengths.shape[0]))
        lineCoords = np.rint(fibreLengths[i])
        lineCoords = lineCoords.astype(int)
        print("Line coords: " + str((lineCoords[1], lineCoords[0], lineCoords[3], lineCoords[2])))
        rr, cc = draw.line(lineCoords[1], lineCoords[0], lineCoords[3], lineCoords[2])
        image[rr, cc] = np.array([0, 0, 255])
        
    cv2.imwrite(filename + "Drawn Lines.jpg", image)
    print("Drawn found fibres on the image: " + filename + "Drawn Lines.jpg\n")
    return
