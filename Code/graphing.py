# -*- coding: utf-8 -*-
"""
@author: Matthew
This module will contain the functions to produce graphs and analysis of the data found.
"""

#Imports
from matplotlib import pyplot as plt
import numpy as np

#Functions
def lengthDistribution(data):
    """
    Produces a histogram showing the length distribution.
    """
    graph = plt.figure()
    x = data[:, 4]
    plt.hist(x)
    plt.ylabel("Number of fibres"), plt.xlabel("Fibre Length (pixels)")
    plt.title("Length Distribution of the Fibres")
    graph.show()
    
"""
data = np.array([[0,0,0,0,0,0]], dtype = np.float)
for i in range(100):
    temp = np.loadtxt("..\\ProcessedData\\LogDataFiles\\Generated Random Image[2018-02-22_21-29-49] (Random Image " + str(i + 1) + ") Fibre_Lengths.txt")
    data = np.concatenate((data, temp))
    
data = np.delete(data, 0, 0)

lengthDistribution(data)
"""