"""
This code uploads analyses door frame data (pressure probes and temperatures) to calculate
mass flow, neutral plane height and internal HRR.

"""

import pandas as pd
import pickle

DoorFrame = {}


# iterate over the four tests to be analysed
for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:
    
    # upload the data from the excel spreadsheets
    file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/door_frame/Data_DoorAnalysis_Alltests.xlsx"
    
    # upload the raw data from the summary excel file
    with open(file_address, "rb") as handle:
        DoorFrame[test_name] = pd.read_excel(file_address, sheet_name = test_name)

# save all the external HRR data as a pickle in processed data
file_address_save = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/door_frame/DoorFrame_unprocessed.pkl"
with open(file_address_save, 'wb') as handle:
    pickle.dump(DoorFrame, handle)
