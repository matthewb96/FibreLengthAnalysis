# -*- coding: utf-8 -*-
"""
@author: Matthew
This module will contain the functions to produce graphs and analysis of the data found.
"""

#Imports
from matplotlib import pyplot as plt
import numpy as np

#Functions
def lengthDistribution(data, filename = "", title = "Length Distribution of the Fibres"):
    """
    Produces a histogram showing the length distribution.
    """
    graph = plt.figure()
    #Generate Histogram
    vals, binEdges = np.histogram(data[:, 4], bins = 10)
    binCentres = 0.5 * (binEdges[1:] + binEdges[:-1])
    width = binEdges[1] - binEdges[0]
    stdErr = np.sqrt(vals)
    
    #Plot
    plt.bar(binCentres, vals, width, yerr = stdErr)
    plt.ylabel("Number of fibres"), plt.xlabel("Fibre Length (pixels)")
    plt.title(title)
    graph.show()
    
    #Save the plot
    if filename != "":
        graph.savefig(filename + " " + title + ".jpg") 
    
"""
data = np.array([[0,0,0,0,0,0]], dtype = np.float)
for i in range(100):
    temp = np.loadtxt("..\\ProcessedData\\LogDataFiles\\Generated Random Image[2018-02-22_23-28-49] (Random Image " + str(i + 1) + ") Fibre_Lengths.txt")
    data = np.concatenate((data, temp))
    
data = np.delete(data, 0, 0)

lengthDistribution(data)
"""