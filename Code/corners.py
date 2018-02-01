# -*- coding: utf-8 -*-
"""
@author: Matthew
This module contains all the functions that will find the corners and edges of the fibres, once given an image array.
"""
#Imports
import numpy as np


#Functions

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



#Harris corner detection
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
