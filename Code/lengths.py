# -*- coding: utf-8 -*-
"""
@author: Matthew
This module will contain all the functions for finding the lengths of the fibres.
"""

#Imports
import numpy as np


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

def checkLine(pos1, pos2):
    """
    This function takes two sets of coordinates and checks there is a solid line of pixels between them.
    
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
            if not checkBlack(pos):
                return False
    
    if not horizontal: #If line is horizontal all y will be the same 
        #Next loop through the y positions calculating corresponding x
        for i in range(int(min(pos1[1], pos2[1])), int(max(pos1[1], pos2[1])) + 1):
            if vertical: 
                pass #Do nothing x is constant
            else:
                xVal = (i - yIntercept)/gradient
            pos = np.array([xVal, i])
            if not checkBlack(pos):
                return False
            
    #If both loops make it all the way through then the postions must be connected by a fibre so return True
    return True

def checkBlack(pos):
    """
    This function checks if the pixel at the given position is black ie part of a fibre.
    """
    pixel = imageGray[int(pos[1])][int(pos[0])]
    if pixel <= (0.5*np.amax(imageGray)):
        return True 
    else:
        return False

def findLengths(coords, minLength = 25):
    """
    Accepts a 2D numpy array of coordinates and finds the length between all combinations of coordinates that have a line between them.
    
    Returns array containing the coordinates of the line and the line length 
    [[x0, y0, x1, y1, length01]
     [x0, y0, x2, y2, length02] 
     ...]
    """
    lineLengths = np.array([[0, 0, 0, 0, 0]]) #For each line in the array [x, y, x1, y1, length]
    arrayLength, width = coords.shape #Find length of axis 0
    lengthsChecked = 0
    maxChecks = int((arrayLength * (arrayLength - 1))/2)
    for i in range(arrayLength):
        for j in range(i + 1, arrayLength): #Generates list of numbers starts at i so to not repeat numbers already compared
            if lengthsChecked % 20 == 0:
                now = time.clock()
                print("Running for "+ str(int(now-start)) + "s Lengths checked: " + str(lengthsChecked) + ". Maximum possible checks: " 
                      + str(maxChecks) + ". Lengths found: " + str(lineLengths.shape[0] - 1))
            lengthsChecked += 1
            if not checkLine(coords[i], coords[j]):
                continue #Skip loop if corners not joined by solid black pixels ie not part of the same fibre
            distance = coordDist(coords[i], coords[j])
            if distance == 0:
                continue #Skip this loop if the distance is zero ie same corners are being measured
            arrayRow = np.array([coords[i][0], coords[i][1], coords[j][0], coords[j][1], distance])
            lineLengths = np.vstack((lineLengths, arrayRow))
            break #If the code reaches this then a joined fibre is found so there is no need to carry on checking all other corners against this one
    
    print("Final lengths checked: " + str(lengthsChecked) + " Maximum possible checks: " + str(maxChecks))
    lineLengths = np.delete(lineLengths, 0, 0)
    return lineLengths
 