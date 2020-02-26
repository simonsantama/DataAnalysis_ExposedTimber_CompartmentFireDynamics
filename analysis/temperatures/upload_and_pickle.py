"""
This script uploads temperatures from each test and distributes them by thermocouple tree.

It also creates plots of the raw temperatures to visualize the data.

"""

import pandas as pd
import pickle

all_raw_data = {}

# plotting parameters
linestyles = ["-", "--", "-.", ":"]*3
colors = ["black", "royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan"]*2

# iterate over all tests
for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:
    
    all_raw_data[test_name] = {}
    
    # upload the data from both data loggers
    file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/temperature/{test_name}_GasPhaseTemperatures.xlsx"
    
    # two data loggers means two different data frames
    df_A = pd.read_excel(file_address, sheet_name = "LoggerA")
    df_B = pd.read_excel(file_address, sheet_name = "LoggerB")
    
    # parse the data
    for df in [df_A, df_B]:
        # convert time to seconds
        df.loc[:, "testing_time"] = df.loc[:, "testing_time"]*60
        
        # iterate over all columns and apply meaningful names
        for column in df.columns[1:]:
            new_col_name = column.split("<")[1].split(">")[0]
            df.loc[:, new_col_name] = df.loc[:, column]
            
    all_raw_data[test_name]["LoggerA"] = df_A
    all_raw_data[test_name]["LoggerB"] = df_B
    
file_address = "Temperatures_Raw.pkl"
with open(file_address, "wb") as handle:
    pickle.dump(all_raw_data, handle)
        
        
        


