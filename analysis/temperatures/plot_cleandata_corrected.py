"""
Corrects the data for radiation. Plots the corrected and clean data and saves the corrected temperatures
to a pickle file.

"""

import pickle
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

# upload the processed and corrected data
file_address = "Temperatures_Processed_Uncorrected.pkl"
with open(file_address, "rb") as handle:
    all_data = pickle.load(handle)

# plotting parameters
colors = ["royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan", "black"]*3
linestyles = ["-", "--", "-.", ":"]*4
location_plot = {"TXX": (0,1),
                 "T13": (1,0), "T23": (1,1), "T33": (1,2),
                 "T12": (2,0), "T22": (2,1), "T32": (2,2),
                 "T11": (3,0), "T21": (3,1), "T31": (3,2),
                 "TDD": (4,1)}

# c