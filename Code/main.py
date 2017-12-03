# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other files and house a lot of the important functions. 
At the minute most of the code is for testing what works and what doesn't.
"""
#All the imported modules
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os #Used in saveImg()
import time

#All the global constants that are needed
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored

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

def averageEdges(cornerPos, FIBREWIDTH = 25):
    """
    Finds the corners that are close enough together to be considered part of the short edge 
    and averages them to return one position for each edge.
    """
    averageCoords = np.array([[0,0]]) #Initiate array with temp values
    arrayLength, width = cornerPos.shape #Find length of axis 0
    for i in range(arrayLength):
        for j in range(i, arrayLength): #Generates list of numbers starts at i so to not repeat numbers already compared
            distance = coordDist(cornerPos[i], cornerPos[j])
            if  distance <= FIBREWIDTH and distance != 0:
                average = np.array([(cornerPos[i] + cornerPos[j])/2])
                averageCoords = np.vstack((averageCoords, average))
    
    averageCoords = np.delete(averageCoords, 0, 0) #Delete temp values
    return averageCoords

def coordDist(pos1, pos2):
    """
    Takes two arrays of length 2 and will find the length between them.
    """
    xDiff, yDiff = abs(pos1 - pos2)
    hippotenuse = np.sqrt(xDiff**2 + yDiff**2)
    return hippotenuse

def checkLine(pos1, pos2):
    """
    This function takes two sets of coordinates and checks there is a solid line of pixels between them.
    
    Returns boolean value for if there is a solid line between them or not.
    """
    return True

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
    for i in range(arrayLength):
        for j in range(i, arrayLength): #Generates list of numbers starts at i so to not repeat numbers already compared
            if not checkLine(coords[i], coords[j]):
                continue #Skip loop if corners not joined by solid black pixels ie not part of the same fibre
            distance = coordDist(coords[i], coords[j])
            if distance == 0:
                continue #Skip this loop if the distance is zero ie same corners are being measured
            arrayRow = np.array([coords[i][0], coords[i][1], coords[j][0], coords[j][1], distance])
            lineLengths = np.vstack((lineLengths, arrayRow))
    
    lineLengths = np.delete(lineLengths, 0, 0)
    return lineLengths
            
   


#Opening the image and showing it in the console can't read png when using cv2.imread() instead of mimg.imread()
image = cv2.imread(IMAGEFOLDER + imageSource) #Opens the image and converts it to an array of floating point data between 0 and 1.
img = plt.figure()
plt.subplot(3,4,1)
plt.imshow(image) #Shows the image in the IPython console test purposes
plt.title("Original Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,2)
n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(image))) #Plot histogram of the image array
plt.title("Original Hist"), plt.yticks([])

#Convert to grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.subplot(3,4,3)
plt.imshow(imageGray)
plt.title("Grayscale Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,4)
n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(imageGray))) #Plot histogram of the image array
plt.title("Grayscale Hist"), plt.yticks([])


#Trying Harris corner detection
imageFloat = np.float32(imageGray)
corners = cv2.cornerHarris(imageFloat.copy(), 10, 15, 0.04)
corners = cv2.dilate(corners, None) #Used to mark the corners
plt.subplot(3,4,5)
plt.imshow(corners)
plt.title("Corner Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,6)
plt.hist(np.ndarray.flatten(np.uint8(corners))) #Plot histogram of the image array
plt.title("Corner Hist"), plt.yticks([])


# Find the corners more accurately using cornerSubPix
thresVal, cornersThres = cv2.threshold(corners, 0.7*corners.max(), 255, 0)
cornersThres = np.uint8(cornersThres)
retval, labels, stats, centroids = cv2.connectedComponentsWithStats(cornersThres)
centroids = np.delete(centroids, 0, 0) #Delete the first row in the array because it does not refer to a corner
#Plot cornersThres
plt.subplot(3,4,9)
plt.imshow(cornersThres)
plt.title("CornerThres Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,10)
plt.hist(np.ndarray.flatten(np.uint8(cornersThres))) #Plot histogram of the image array
plt.title("Corner Thres Hist"), plt.yticks([])

#Sub Pixel Function
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
cornersSubPix = cv2.cornerSubPix(imageFloat,            #Input image
                                 np.float32(centroids), #Initial coordinates of the original corners
                                (5,5),                  #Size of search window        
                                (-1,-1),                #Size of dead region (-1,-1) is no dead region
                                criteria)               #Criteria to stop the iteration
print("Subpix Corners: " + str(cornersSubPix.shape[0]))

#Find fibre length
edges = averageEdges(cornersSubPix)
print("# Endpoints: " + str(edges.shape[0]))
fibresLength = findLengths(edges)
print("Lengths Found: " + str(fibresLength.shape[0]))
print("Fibre lengths: [x0, y0, x1, y1, length01]\n")


#Show and save the images
plt.show()
saveName = saveImg(PROCESSEDFOLDER + imageSource)
img.savefig(saveName)
plt.close(img)

# Now draw orginal image with corners plotted
res = np.hstack((centroids,cornersSubPix))
res = np.int0(res)
image[res[:,1],res[:,0]]=[0,0,255]
image[res[:,3],res[:,2]] = [0,255,0]

cv2.imwrite(saveName + " subpix.jpg",image)
cv2.imwrite(saveName + " Harris.jpg",corners)
cv2.imwrite(saveName + " HarrisThres.jpg",cornersThres)

end = time.clock()
print("Time taken: " + str(end-start))