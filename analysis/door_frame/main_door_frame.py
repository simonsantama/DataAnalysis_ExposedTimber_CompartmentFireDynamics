"""
This code uploads analyses door frame data (pressure probes and temperatures) to calculate
mass flow, neutral plane height and internal HRR.

"""

import pickle

# import my own functions
from calculation_massflow import calculation_area, calculation_velocity, calculation_massflow

DoorFrame = {}

# store velocitie, mass flow and internal HRR separetely
Velocities = {}
MassFlow = {}
HRR_internal = {}


# upload the data from the excel spreadsheets
file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/door_frame/DoorFrame_unprocessed.pkl"
with open(file_address, "rb") as handle:
    DoorFrame = pickle.load(handle)

# iterate over the four tests to be analysed
for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:

    df = DoorFrame[test_name]
    df.rename(columns = {"Time [min]": "testing_time"}, inplace = True)
    df_juanalyser = df.loc[:, df.columns[23:]].copy()
    df.drop(columns = df.columns[22:], inplace = True)
    
    # modify testing time to show in seconds
    df.loc[:, "testing_time"] = df.loc[:, "testing_time"]*60
    
    # calculate areas
    areas = calculation_area()
    
    # calculate velocities
    calculation_velocity(df)
    
    # store the velocity data on it's own dictionary
    velocity_colums = ["testing_time"]
    for column in df:
        if "V_" in column:
            velocity_colums.append(column)
    Velocities[test_name] = df.loc[:, velocity_colums]
    
    # calculate massflow
    

# save velocitie, mass flow and internal HRR data
file_address_save = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Velocities.pkl"
with open(file_address_save, 'wb') as handle:
    pickle.dump(Velocities, handle)
