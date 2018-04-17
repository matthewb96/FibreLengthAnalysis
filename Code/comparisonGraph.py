# -*- coding: utf-8 -*-
"""
@author: Matthew
Produce Comparison Graphs
"""
from matplotlib import pyplot as plt
import numpy as np

with open("..\FibreImages\DataCollectedByPeterHine\LogDataFiles\9[2018-04-17_04-11-02]Total_Fibre_Lengths.txt", "r") as file:
    autoData = np.loadtxt(file, delimiter = " ", skiprows = 1)



with open("..\FibreImages\DataCollectedByPeterHine\manualData.csv", "r") as file:
    manualData = np.loadtxt(file, delimiter = ",", skiprows = 1)

#Convert to Microns
autoLengths = autoData[:, 4] / 0.673

graph = plt.figure()
#Generate Histogram
vals, binEdges = np.histogram(autoLengths, bins = 30)
binCentres = 0.5 * (binEdges[1:] + binEdges[:-1])
width = binEdges[1] - binEdges[0]
stdErr = np.sqrt(vals)

#Plot
plt.bar(binCentres, vals, width, yerr = stdErr, label = "Image Analysis Collected Data")
plt.errorbar(manualData[:, 0], manualData[:, 1], yerr = manualData[:,2], fmt = "r+", label = "Manually Collected Data")
plt.ylabel("Number of fibres"), plt.xlabel("Fibre Length (microns)")
plt.title("Comparison of the Data Collected Manually by Peter Hine and Automatically by the Image Analysis Program.")
plt.legend()
graph.show()