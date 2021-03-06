"""
Plot the raw data for all tests.
This script also uploads the data from the doorway and plots that with the other data.

Saves the parsed data to a pickle.
"""
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pickle
import time

# import data
file_address = "Temperatures_Raw.pkl"
with open(file_address, "rb") as handle:
    all_raw_data = pickle.load(handle)
    
# import doorway data (this is processed in the Door Frame script. It is assumed that air coming - from pressure probe
# data - is at ambient temperature)
file_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Door_Temperatures.pkl"
with open(file_address, "rb") as handle:
    door_temperatures = pickle.load(handle)
    
list_useful_cols = [f"T{x}" for x in [11,12,13,21,22,23,31,32,33,"XX"]]
all_useful_cols = {name:[] for name in list_useful_cols}

# plot location equivalence
location_plot = {"TXX": (0,1),
                 "T13": (1,0), "T23": (1,1), "T33": (1,2),
                 "T12": (2,0), "T22": (2,1), "T32": (2,2),
                 "T11": (3,0), "T21": (3,1), "T31": (3,2)}

colors = cm.get_cmap('cividis', len(list_useful_cols))
linestyles = ["-", "--", "-.", ":"]*3

# plot
for test_name in ["Alpha1","Alpha2", "Beta1", "Beta2", "Gamma"]:
    start = time.time()
    
    print(f"Creating plot for {test_name}")
    data_dict = all_raw_data[test_name]
#    if test_name not in ["Alpha1"]:
#        data_door = door_temperatures[test_name]
    data_door = door_temperatures[test_name]
    
    fig, ax = plt.subplots(5,3,figsize = (11,11), sharex = True, sharey = True)
    fig.subplots_adjust(top = 0.9, left = 0.1, bottom = 0.1,
                        hspace = 0.20, wspace = 0.075)
    fig.suptitle(test_name, fontsize = 14)
    
    # remove the axis and frames from plots that are not part of the actual TC tree grid
    for axis in [ax[0,0], ax[0,2], ax[4,0], ax[4,2]]:
        axis.axis("off")
    
    
    # format plots
    for j,axis in enumerate(ax.flatten()):
        axis.grid(True, color = "gainsboro", linestyle = "--", linewidth = 0.75)
        axis.set_title(["","TXX_Centre_Wall","",
                        "T13_Left_Far","T23_Centre_Far","T33_Right_Far",
                        "T12_Left_Midle","T22_Centre_Midle","T32_Right_Midle",
                        "T11_Left_Near","T21_Centre_Near","T31_Right_Near",
                        "", "TDD_Door", ""][j],
                       fontsize = 12)
    for axis in ax[:,0]:
        axis.set_ylabel("Temperature [$^\circ$C]", fontsize = 10)
        axis.set_ylim([-75,1500])
        axis.set_yticks(np.linspace(0,1500,6))
    for axis in [ax[3,0], ax[4,1], ax[3,2]]:
        axis.set_xlabel("Time [min]", fontsize = 10)
        axis.set_xlim([0,60])
        axis.set_xticks(np.linspace(0,60,5))
        
    # plot
    for logger in data_dict:
        df = data_dict[logger]
        
        # getting rid of the columns with non-formatted names
        drop_columns = [col for col in df.columns if "<" in col]
        df.drop(columns = drop_columns, inplace = True)
        
        # iterate over the different TC trees
        for useful_col in list_useful_cols:
            
            # extract the name of hte TC tree
            TC_tree_name = useful_col.split("-")[0]
            location = location_plot[TC_tree_name]
            
            # create a list of columns that correspond to this TC tree
            TC_tree_columns = [x for x in df.columns[1:] if useful_col in x]
            TC_tree_columns.append("testing_time")
            
            # created reduced data frame
            df_reduced = df.loc[:, TC_tree_columns]
            
            # plot
            axis = ax[location[0], [location[1]]][0]
            mask = (df_reduced.loc[:, "testing_time"]/60 > 0) & (df_reduced.loc[:, "testing_time"]/60 < 60)
            
            for j,column in enumerate(df_reduced):
                if "testing_time" in column:
                    pass
                else:
                    axis.plot(df.loc[mask, "testing_time"]/60,
                              df.loc[mask, column],
                              color = colors(j/len(list_useful_cols)),
                              linestyle = linestyles[j])
    
    # plot the door temperatures
    for j,column in enumerate(data_door):
        axis = ax[4,1]
        mask = (data_door.loc[:,"testing_time"]/60 > 0) & (data_door.loc[:, "testing_time"]/60 < 60)
        if "testing_" in column:
            pass
        else:
            axis.plot(data_door.loc[mask, "testing_time"]/60,
              data_door.loc[mask, column],
              color = colors(j/len(list_useful_cols)),
              linestyle = linestyles[j])
    
    # funny plot to add a legend in the first subplot
    for j in range(12):
        ax[0,0].plot([],
          [],
          linestyle = linestyles[j],
          color = colors(j/len(list_useful_cols)),
          label = f"{np.linspace(40,260,12)[j]/100} m")
        ax[0,0].legend(fancybox = True, loc = "center", fontsize = 10, title = "TC Height", ncol = 3)
    
    print(f" time taken: {np.round(time.time() - start,2)} seconds")

    # save and close
    fig.savefig(f"raw_data/{test_name}_temperatures_raw.png", dpi = 600)
    plt.close(fig)
    

