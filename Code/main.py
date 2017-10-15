# -*- coding: utf-8 -*-
"""
@author: Matthew
This main file will control all other files and house a lot of the important functions. 
"""
#All the imported modules
import cv2
import numpy as np
from matplotlib import pyplot as plt, image as mpimg

#All the global constants that are needed
IMAGEFOLDER = "..\\FibreImages\\" #Source where images to be analysed are stored. Backslash is special character used to ignore special characters so 2 are needed
PROCESSEDFOLDER = "..\\ProcessedData\\" #Source for where processed data is stored

#All the global variables that are needed
imageSource = input("Please input filename to be analysed: ")


#First bit of test code opening the image and showing it in the console
image = mpimg.imread(IMAGEFOLDER + imageSource) #Opens the image and converts it to an array of floating point data between 0 and 1. Could use cv2.imread but that nwon't read png files
img = plt.figure()
plt.subplot(131)
plt.imshow(image) #Shows the image in the IPython console test purposes
plt.title("Original Image")

#Finding the edges of the image using Canny Edge detection from opencv
imageConverted = np.uint8(image) #Converts the image from CV_8U to uint8 so it can be used by Canny()
edges = cv2.Canny(imageConverted, 0, 0) #Finds the edges in the image, the arguments are image, minVal and maxVal
plt.subplot(132)
plt.imshow(edges, cmap="gray")
plt.title("Edge Detected Image"), plt.yticks([])


plt.subplot(133)
plt.imshow(imageConverted)
plt.title("Converted Image"), plt.yticks([])

"""
#Trying Harris corner detection
imageConverted = np.float32(image)
print(imageConverted)
corners = cv2.cornerHarris(imageConverted, 2, 3, 0.04)
plt.subplot(132)
plt.imshow(corners)
plt.title("Corner Detected Image"), plt.yaxis([])
"""

"""
#Trying Line Detection using Hough Line Transform
imageConverted = np.uint8(image)
imageConverted = cv2.cvtColor(imageConverted, cv2.COLOR_BGR2GRAY)
ret, imageThres = cv2.threshold(imageConverted, 127, 255, cv2.THRESH_BINARY)
lines = cv2.HoughLines(imageThres, 1, np.pi/180, 200)
plt.subplot(133)
plt.imshow(lines, cmap="gray")
plt.title("Line Detected Image"), plt.yticks([])
"""

#Show and save the images
plt.show()
img.savefig(PROCESSEDFOLDER + imageSource)
plt.close(img)