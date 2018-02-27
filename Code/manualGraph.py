# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 13:11:34 2018

@author: Matthew
Temporary file for creating a graph manually.
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Functions
def plot3LineGraph(data, title):
    """
    Plots a graph containing the correct, incorrect and one away data for the 100 random image tests.
    
    arg[0] data - numpy array containing the data to be plotted.
    arg[1] title - string containing the title for the graph.
    """
    #Plot the graph
    labels = ("Correct", "One Away", "Incorrect")
    graph = plt.figure()
    [y1, y2, y3] = plt.plot(data[:, 0], data[:, 1:])
    plt.xlabel("Array Size (pixels)"); plt.ylabel("Number of fibres")
    plt.title(title)
    plt.legend([y1, y2, y3], labels, loc = (0.7, 0.5))
    graph.show()
    
    
def plotPercentError(data, title):
    """
    Plot a graph for the average percentage incorrect fibres for 100 random images tests.
    
    arg[0] data - numpy array containing the data to be plotted.
    arg[1] title - string containing the title for the graph.
    """
    graph = plt.figure()
    x = data[:, 0]
    #Divide the data by 100 to get average per image, then divide by 10 and multiply by 100 to get percentage so just divide by 10
    y = data[:, 3] / 10
    y1 = np.ones(y.shape)
    yErr = np.sqrt(y) #Error is the square root of the value for counting stats
    
    #Exponential fit
    global popt
    popt, pcov = curve_fit(expFunc, x, y, sigma = yErr, p0 = (100., (0.01), 1.))
    percentile = expFuncX(1, *popt)
    
    #Plots
    plt.errorbar(x, y, yerr = yErr, fmt = "r.", label = "% Incorrect")
    plt.plot(x, expFunc(x, *popt), label = "Exponential fit")
    plt.plot(x, y1, label = "1%")
    plt.xlabel("Array Size (pixels)"); plt.ylabel("Percentage of Incorrect Fibres")
    plt.title(title)
    plt.text(6000, 25, "1% Incorrect at x = " + str(np.rint(percentile)) + "\nb = -" + str(np.round(popt[1], 8)))
    plt.legend()
    graph.show()
    
    
def expFunc(x, a, b, c):
    """
    Exponential function for curve_fit.
    """
    return a * np.exp(-b * x) + c


def expFuncX(y, a, b, c):
    """
    Rearrangement of the exponential function to find y.
    """
    return -(np.log((y - c)/a))/b


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
#Plot graphs 
plot3LineGraph(dataOrig, "Graph showing the data for 100 random images\nbefore fixing the one away check")
plotPercentError(dataOrig, "Graph showing the percentage error for 100 random images\nbefore fixing the one away check")


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
#Plot the graphs
plot3LineGraph(dataNew, "Graph showing the data for 100 random images\nafter fixing the one away check")
plotPercentError(dataNew, "Graph showing the percentage error for 100 random images\nafter fixing the one away check")


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

#Plot the graph
plot3LineGraph(dataCheckDown, "Graph showing the data for 100 random images after having\nfibres check further down array, to account for missing fibres.")
plotPercentError(dataCheckDown, "Graph showing the percentage error for 100 random images after having\nfibres check further down array, to account for missing fibres.")


#Data for the 100 random image tests after edits for checking the midpoint is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataMidpoint = np.array([[10000, 692, 287, 21],
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

#Plot the graphs
plot3LineGraph(dataMidpoint, "Graph showing the data for 100 random images after edits\nfor checking the midpoint is part of a fibre.")
plotPercentError(dataMidpoint, "Graph showing the percentage error for 100 random images after edits\nfor checking the midpoint is part of a fibre.")


#Data for the 100 random image tests after edits for checking centroid position is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataCentroid = np.array([[10000, 709, 281, 10],
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
#Plot the graphs
plot3LineGraph(dataCentroid, "Graph showing the data for 100 random images after edits\nfor checking centroid position is part of a fibre.")
plotPercentError(dataCentroid, "Graph showing the percentage error for 100 random images after edits\nfor checking centroid position is part of a fibre.")


#Data for the 100 random image tests after fixing checking the line is part of a fibre
#10 fibres per image between 100-1000 pixels long and 25 pixels wide
#[Array Size, correct, one away, incorrect]
dataLineFix = np.array([[10000, 737, 256, 7],
                         [9000, 739, 257, 4],
                         [8000, 736, 255, 9],
                         [7000, 722, 265, 13],
                         [6000, 735, 248, 17],
                         [5000, 747, 240, 13],
                         [4000, 717, 247, 36],
                         [3000, 673, 251, 76],
                         [2500, 658, 240, 102],
                         [2000, 624, 247, 129],
                         [1500, 561, 201, 238],
                         [1000, 466, 180, 354]
                         ])

#Plot the graphs
plot3LineGraph(dataLineFix, "Graph showing the data for 100 random images after fixing\nthe check that the line is part of a fibre.")
plotPercentError(dataLineFix, "Graph showing the percentage error for 100 random images after fixing\nthe check that the line is part of a fibre.")