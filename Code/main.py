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
            digits = len(str(num))
            num += 1
            filename = filename[:(pos+2)] + str(num) + filename[(pos+2+digits):]
        return filename


#First bit of test code opening the image and showing it in the console can't read png when using cv2.imread() instead of mimg.imread()
image = cv2.imread(IMAGEFOLDER + imageSource) #Opens the image and converts it to an array of floating point data between 0 and 1.
img = plt.figure()
plt.subplot(3,4,1)
plt.imshow(image) #Shows the image in the IPython console test purposes
plt.title("Original Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,2)
n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(image))) #Plot histogram of the image array
plt.title("Original Hist"), plt.yticks([])
print("Original Hist Data")
print(n)
print(bins)
print(np.sum(n))

#Convert to grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.subplot(3,4,3)
plt.imshow(imageGray)
plt.title("Grayscale Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,4)
n, bins, patches = plt.hist(np.ndarray.flatten(np.uint8(imageGray))) #Plot histogram of the image array
plt.title("Grayscale Hist"), plt.yticks([])
print("Grayscale Hist Data")
print(n)
print(bins)
print(np.sum(n))

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
#cornersThres = cv2.threshold(corners, 0.01*corners.max(), 255, 0)
cornersThres = np.uint8(corners)
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(cornersThres)
print(centroids)
#Plot cornersThres
plt.subplot(3,4,7)
plt.imshow(cornersThres)
plt.title("CornerThres Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,8)
plt.hist(np.ndarray.flatten(np.uint8(cornersThres))) #Plot histogram of the image array
plt.title("Corner Thres Hist"), plt.yticks([])


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
cornersSubPix = cv2.cornerSubPix(imageFloat,            #Input image
                                 np.float32(centroids), #Initial coordinates of the original corners
                                (5,5),                  #Size of search window        
                                (-1,-1),                #Size of dead region (-1,-1) is no dead region
                                criteria)               #Criteria to stop the iteration

print(cornersSubPix)


"""
#Try to find the indices of the coloured corners
corners = np.uint8(corners)
ret, threshold = cv2.threshold(corners,254,255,cv2.THRESH_BINARY)
plt.subplot(3,4,9)
plt.imshow(threshold)
plt.title("Threshold Image"), plt.yticks([]), plt.xticks([])
#Plot histogram
plt.subplot(3,4,10)
plt.hist(np.ndarray.flatten(np.uint8(threshold))) #Plot histogram of the image array
plt.title("Threshold Hist"), plt.yticks([])

positions = np.array(np.nonzero(corners)) #Returns the indices of any non-zero values of the array
#positions = np.transpose(positions)
print(positions[0].size)
x1 = np.average(positions[0, :int(positions[0].size/2)])
x2 = np.average(positions[0, int(positions[0].size/2):])
print(x1)
print(x2)
print("length = "+ str(np.absolute(x1-x2)))
np.savetxt(saveImg(imageSource) + ".txt", corners)
np.savetxt(saveImg(imageSource) + "(positions).txt", positions)
"""

"""
#Trying Line Detection using Hough Line Transform
#ret, imageThres = cv2.threshold(imageUint8, 127, 255, cv2.THRESH_BINARY)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200) #Using Hough line transform on canny edge detected image
#plt.subplot(2,3,6)
cv2.imshow("image",lines)
cv2.waitKey(0)
#plt.title("Line Image"), plt.yticks([]), plt.xticks([])
"""

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