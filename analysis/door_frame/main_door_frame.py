"""
This code uploads analyses door frame data (pressure probes and temperatures) to calculate
mass flow, neutral plane height and internal HRR.

"""

import pickle
import matplotlib.pyplot as plt
import numpy as np

# import my own functions
from calculation_massflow import calculation_area, calculation_velocity, calculation_massflow, calculation_HRR

DoorFrame = {}
DoorFrame_full = {}

# dictionaries used to save the data separately in the data processed folder
Velocities = {}
Neutral_Plane = {}
Mass_Flow = {}
HRR_internal_massin = {}    
HRR_internal_juanalyser = {}

# upload the data from the excel spreadsheets
file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/door_frame/DoorFrame_unprocessed.pkl"
with open(file_address, "rb") as handle:
    DoorFrame = pickle.load(handle)

# iterate over the four tests to be analysed
for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:
    
    print(f"Analysing experiment {test_name}")
    
    # extract the data and divide into temperature/pressure_probe and gas analysis
    df_full = DoorFrame[test_name]
    df = df_full.iloc[:, :22].copy()
    
    
    # start with analysis of temperature/pressure_probe data
    df.rename(columns = {"Time [min]": "testing_time"}, inplace = True)
    
    # modify testing time to show in seconds
    df.loc[:, "testing_time"] = df.loc[:, "testing_time"]*60
    
    # calculate areas
    areas = calculation_area()
    
    # calculate velocities
    calculation_velocity(df, test_name)
    
    # calculate massflow
    calculation_massflow(df, areas)
    
    # store in DoorFrame_full for plotting below
    DoorFrame_full[test_name] = df
    
    # save data into independent dictionaries
    v_columns = [col for col in df.columns if "V_" in col]
    m_columns = [col for col in df.columns if "mass_" in col]
    for lst in [v_columns, m_columns]:
        lst.append("testing_time")
    np_columns = ["testing_time", "Neutral_Plane", "Neutral_Plane_Smooth"]
    hrr_massin_columns = ["testing_time", "hrr_internal_allmassin"]
    
    Velocities[test_name] = df.loc[:, v_columns]
    Mass_Flow[test_name] = df.loc[:, m_columns]
    Neutral_Plane[test_name] = df.loc[:, np_columns]
    HRR_internal_massin[test_name] = df.loc[:, hrr_massin_columns]
    
    # Heat Release Rate calculations
    df_juanalyser = df_full.iloc[:, 23:].copy()
    df_juanalyser.rename(columns = {"Time": "testing_time"}, inplace = True)
    df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[:, "testing_time"]*60
    
    # the ignition delay was not added to the spreadsheets for Beta1 and Beta2, So I am adding it manually.
    if test_name == "Beta1":
        df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[:, "testing_time"] - 4*60
    if test_name == "Beta2":
        df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[:, "testing_time"] - 18*60
    
    calculation_HRR(df_juanalyser, df)
    
    # save internal HRR data into independent dictionary
    HRR_internal_juanalyser[test_name] = df_juanalyser.loc[:, ["testing_time","hrr_internal"]]
    
# save velocities, neutral plane, mass flow and internal HRR to the processed data folder
data_to_save = [Velocities, Neutral_Plane, Mass_Flow, HRR_internal_massin, HRR_internal_juanalyser]

for i, data_type in enumerate(data_to_save):
    
    data_name = ["Velocities", "Neutral_Plane", "Mass_Flow", "HRR_internal_massin", "HRR_internal_juanalyser"][i]
    file_address_save = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/{data_name}.pkl"
    
    with open(file_address_save, 'wb') as handle:
        pickle.dump(data_type, handle)
    
# Plotting of the raw data to evaluate the algorithm and identify any broken sensors
test_name = ["Alpha2", 
               "Beta1", 
               "Beta2", 
               "Gamma"]
y_labels = ["Temperature [$^\circ$C]",
            "Transducers [V]",
            "Transducers [V]",
            "DeltaP [Pa]",
            "DeltaP [Pa]",
            "Temperature [$^\circ$C]",
            "Density [kg/m$^3$]",
            "Velocity [m/s]",
            "Neutral Plane [m]",
            "Neutral Plane Smooth [m]",
            "Mass Flow [kg/s]"]
y_limits = ([0,1200],
            [0,15],
            [-5,5],
            [-20,20],
            [-20,20],
            [0,1200],
            [0, 1.5],
            [-15,5],
            [0,2],
            [0,2],
            [0,1.5])
column_numbers = ([1,9],
                  [10,23],
                  [23,36],
                  [49,62],
                  [62,71],
                  [71,80],
                  [80,89],
                  [89,98],
                  [98, 99],
                  [99,100],
                  [109,112])

# iterate over all the parameters we wish to plot
fontsize_legend = 6
for j, parameter in enumerate(["Raw_Temperatures", "Raw_PressureProbes", "Zeroed_PressureProbes",
                               "DeltaPressure_Smooth", "DeltaPressure_Smooth_Clean", "Temperatures_Processed",
                               "Density", "Velocity", "Neutral Plane", "Neutral_Plane_Smooth", "Mass Flow"]):    

    fig, ax = plt.subplots(4,1,figsize = (8,11), sharex = True)
    fig.suptitle(parameter)
    fig.subplots_adjust(top = 0.9)
    
    ax[3].set_xlim([0,60])
    ax[3].set_xticks(np.linspace(0,60,13))
    ax[3].set_xlabel("Time [min]")
    
    for i,axis in enumerate(ax):
        
        # format the subplots
        axis.set_ylabel(y_labels[j])
        axis.set_ylim(y_limits[j])
        axis.grid(True, linestyle = "--", color = "gainsboro")
        axis.set_title(test_name[i])
        
        
        # extract data
        df = DoorFrame_full[test_name[i]]
        
        # plot
        mask = (df.loc[:, "testing_time"] > 0) & (df.loc[:,"testing_time"]/60 < 60)
        
        for column in df.columns[column_numbers[j][0]:column_numbers[j][1]]:
            axis.plot(df.loc[:, "testing_time"]/60,
                      df.loc[:, column],
                      label = column)
        axis.legend(fancybox = True, ncol = 4, fontsize = fontsize_legend)
    
    fig.savefig(f"{parameter}.png", dpi = 600)
    plt.close(fig)
    
# Additional plot to show the velocities as a function of time at different heights
fig, ax = plt.subplots(1,4,figsize = (11,8), sharex = True, sharey = True)
ax[0].set_ylim([0,2])
ax[0].set_yticks(np.linspace(0,2,6))
ax[0].set_ylabel("Height [m]")

for i,axis in enumerate(ax):
    
    # format the subplots
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])
    axis.set_xlim([-15,5])
    axis.set_xticks(np.linspace(-15,5,5))
    axis.set_xlabel("Velocity [m/s]")
    
    # extract data
    df = DoorFrame_full[test_name[i]]
    
    heights = [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]
    times_of_interest = [5,10,20,30]
    
    for j,t in enumerate(times_of_interest):
        mask = df.loc[:,"testing_time"]/60 > t
        index = df.loc[mask, :].index[0]
        
        velocity = df.loc[index, df.columns[89:98]].values
        
        # plot
        axis.plot(velocity,
                heights,
                label = f"{t} min",
                linestyle = ["-", "--", "-.", ":"][j])

    axis.legend(fancybox = True, ncol = 1, fontsize = fontsize_legend, title = "Time")

fig.savefig("Velocity_v_Height.png", dpi = 600)
plt.close(fig)


    
    
