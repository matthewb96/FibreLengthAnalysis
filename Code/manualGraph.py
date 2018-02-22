# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 13:11:34 2018

@author: Matthew
Temporary file for creating a graph manually.
"""

import numpy as np
from matplotlib import pyplot as plt

#Data for the 100 random image tests before fixing the one away check 
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataOrig = np.array([[10000, 698, 271, 27],
                     [9000, 703, 255, 35],
                     [8000, 675, 281, 27],
                     [7000, 680, 270, 36],
                     [6000, 629, 272, 70],
                     [5000, 620, 269, 87],
                     [4000, 540, 327, 104],
                     [3000, 505, 263, 167],
                     [2500, 442, 302, 181],
                     [2000, 222, 338, 309],
                     [1500, 190, 378, 251],
                     [1000, 128, 322, 326]
                     ])

#Forgot to add 1 to incorrect data for every fibre that wasn't found have edited code now but this data doesn't include it
#Adding to incorrect to make total for each test to 1000
for i in range(dataOrig.shape[0]):
    totFibres = np.sum(dataOrig[i, 1:])
    dataOrig[i,3] += (1000 - totFibres)
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataOrig[i, 1:])))
    
#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataOrig[:, 0], dataOrig[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images\nbefore fixing the one away check")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()

#Data for the 100 random image tests after fixing the one away check 
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataNew = np.array([[10000, 720, 221, 59],
                     [9000, 665, 213, 122],
                     [8000, 669, 271, 60],
                     [7000, 626, 242, 132],
                     [6000, 671, 223, 106],
                     [5000, 652, 184, 164],
                     [4000, 593, 225, 182],
                     [3000, 417, 135, 448],
                     [2500, 355, 125, 520],
                     [2000, 267, 114, 619],
                     [1500, 187, 64, 749],
                     [1000, 105, 50, 845]
                     ])
    
#Checking the total fibres
for i in range(dataNew.shape[0]):
    totFibres = np.sum(dataNew[i, 1:])
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataNew[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataNew[:, 0], dataNew[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images\nafter fixing the one away check")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()

#Data for the 100 random image tests after getting fibres to check further down the array when some are missing 
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataCheckDown = np.array([[10000, 744, 219, 37],
                         [9000, 707, 274, 19],
                         [8000, 705, 259, 36],
                         [7000, 722, 245, 33],
                         [6000, 674, 254, 72],
                         [5000, 667, 249, 84],
                         [4000, 619, 222, 159],
                         [3000, 582, 212, 206],
                         [2500, 499, 197, 304],
                         [2000, 435, 163, 402],
                         [1500, 320, 124, 556],
                         [1000, 200, 86, 714]
                         ])
    
#Checking the total fibres
for i in range(dataCheckDown.shape[0]):
    totFibres = np.sum(dataCheckDown[i, 1:])
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataCheckDown[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataCheckDown[:, 0], dataCheckDown[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images after having\nfibres check further down array, to account for missing fibres.")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()

#Data for the 100 random image tests after edits for checking the midpoint is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataCentroid = np.array([[10000, 692, 287, 21],
                         [9000, 726, 246, 28],
                         [8000, 698, 280, 22],
                         [7000, 710, 258, 32],
                         [6000, 689, 258, 53],
                         [5000, 609, 221, 170],
                         [4000, 590, 209, 201],
                         [3000, 535, 173, 292],
                         [2500, 480, 174, 346],
                         [2000, 324, 120, 556],
                         [1500, 244, 86, 670],
                         [1000, 169, 81, 750]
                         ])
    
#Checking the total fibres
for i in range(dataCentroid.shape[0]):
    totFibres = np.sum(dataCentroid[i, 1:])
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataCentroid[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataCentroid[:, 0], dataCentroid[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images after edits\nfor checking the midpoint is part of a fibre.")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()

#Data for the 100 random image tests after edits for checking centroid position is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataMidpoint = np.array([[10000, 709, 281, 10],
                         [9000, 726, 246, 28],
                         [8000, 725, 264, 11],
                         [7000, 705, 280, 15],
                         [6000, 718, 258, 24],
                         [5000, 712, 253, 35],
                         [4000, 668, 280, 52],
                         [3000, 662, 245, 93],
                         [2500, 648, 205, 147],
                         [2000, 626, 199, 175],
                         [1500, 506, 181, 313],
                         [1000, 400, 123, 477]
                         ])
    
#Checking the total fibres
for i in range(dataMidpoint.shape[0]):
    totFibres = np.sum(dataMidpoint[i, 1:])
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataMidpoint[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataMidpoint[:, 0], dataMidpoint[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images after edits\nfor checking centroid position is part of a fibre.")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()
"""
#Data for the 100 random image tests after fixing checking the line is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataLineFix = np.array([[10000, , , ],
                         [9000, , , ],
                         [8000, , , ],
                         [7000, , , ],
                         [6000, , , ],
                         [5000, , , ],
                         [4000, , , ],
                         [3000, , , ],
                         [2500, , , ],
                         [2000, , , ],
                         [1500, , , ],
                         [1000, , , ]
                         ])
    
#Checking the total fibres
for i in range(dataLineFix.shape[0]):
    totFibres = np.sum(dataLineFix[i, 1:])
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataLineFix[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataLineFix[:, 0], dataLineFix[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
plt.title("Graph showing the data for 100 random images after fixing\nthe check that the line is part of a fibre.")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()
"""