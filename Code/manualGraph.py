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
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres (per image)")
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
    print("Total fibres: " + str(totFibres) + " New total: " + str(np.sum(dataOrig[i, 1:])))

#Plot the graph
labels = ("Correct", "One Away", "Incorrect")
graph = plt.figure()
[y1, y2, y3] = plt.plot(dataNew[:, 0], dataNew[:, 1:])
plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres (per image)")
plt.title("Graph showing the data for 100 random images\nafter fixing the one away check")
plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
graph.show()


