"""
Plots for proposal. Rory. July 2020.
This script takes the data from Alpha2, Beta 1 and Gamma.
Plots the data at a height of two meters for different tests
"""
#import libraries
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pickle

# import data
file_address = "condensed_data.pickle"
with open(file_address, "rb") as handle:
    all_condensed_data = pickle.load(handle)


# iterate over different experiments
for experiment in all_condensed_data:
    temperatures = all_condensed_data[experiment]
    
    list_columns_at_desiredheight = []    
    for column in temperatures:
        if column != "testing_time":
            height = int(column.split("-")[1])
            if height == 200:
                list_colu
#    
#    print(f"Condensing data of {experiment} into a single data frame")
#    all_condensed_data[experiment] = pd.DataFrame()
#    new_time = np.linspace(0,3600,3601)
#    all_condensed_data[experiment].loc[:,"testing_time"] = new_time
#    
#    # interpolate door data to 1 Hz frequency
#    door_temperatures = door_data[experiment]
#    for column in door_temperatures:
#        if column != "testing_time":
#            old_time = door_temperatures["testing_time"]
#            old_temperature = door_temperatures[column]
#            new_temperature = np.interp(new_time, old_time, old_temperature)
#            
#            # save the interpolated data in the condensed data frame
#            new_column_name = "TD" + column.split("_")[1]
#            all_condensed_data[experiment][new_column_name] = new_temperature
#    
#    # interpolate the compartment data to 1Hz frequency
#    compartment_temperatures = all_raw_data[experiment]
#    for logger in compartment_temperatures:
#        for column in compartment_temperatures[logger]:
#            if column != "testing_time":
#                if "<" not in column:
#                    old_time = compartment_temperatures[logger]["testing_time"]
#                    old_temperature = compartment_temperatures[logger][column]
#                    new_temperature = np.interp(new_time, old_time, old_temperature)
#                    
#                    # save the interpolated data in the condensed data frame
#                    all_condensed_data[experiment][column] = new_temperature
#    
#
#    
#    break
#
##    
##list_useful_cols = [f"T{x}" for x in [11,12,13,21,22,23,31,32,33,"XX"]]
##all_useful_cols = {name:[] for name in list_useful_cols}
##
### plot location equivalence
##location_plot = {"TXX": (0,1),
##                 "T13": (1,0), "T23": (1,1), "T33": (1,2),
##                 "T12": (2,0), "T22": (2,1), "T32": (2,2),
##                 "T11": (3,0), "T21": (3,1), "T31": (3,2)}
##
##colors = cm.get_cmap('cividis', len(list_useful_cols))
##linestyles = ["-", "--", "-.", ":"]*3
##
### plot
##for test_name in ["Alpha1","Alpha2", "Beta1", "Beta2", "Gamma"]:
##    start = time.time()
##    
##    print(f"Creating plot for {test_name}")
##    data_dict = all_raw_data[test_name]
###    if test_name not in ["Alpha1"]:
###        data_door = door_temperatures[test_name]
##    data_door = door_temperatures[test_name]
##    
##    fig, ax = plt.subplots(5,3,figsize = (11,11), sharex = True, sharey = True)
##    fig.subplots_adjust(top = 0.9, left = 0.1, bottom = 0.1,
##                        hspace = 0.20, wspace = 0.075)
##    fig.suptitle(test_name, fontsize = 14)
##    
##    # remove the axis and frames from plots that are not part of the actual TC tree grid
##    for axis in [ax[0,0], ax[0,2], ax[4,0], ax[4,2]]:
##        axis.axis("off")
##    
##    
##    # format plots
##    for j,axis in enumerate(ax.flatten()):
##        axis.grid(True, color = "gainsboro", linestyle = "--", linewidth = 0.75)
##        axis.set_title(["","TXX_Centre_Wall","",
##                        "T13_Left_Far","T23_Centre_Far","T33_Right_Far",
##                        "T12_Left_Midle","T22_Centre_Midle","T32_Right_Midle",
##                        "T11_Left_Near","T21_Centre_Near","T31_Right_Near",
##                        "", "TDD_Door", ""][j],
##                       fontsize = 12)
##    for axis in ax[:,0]:
##        axis.set_ylabel("Temperature [$^\circ$C]", fontsize = 10)
##        axis.set_ylim([-75,1500])
##        axis.set_yticks(np.linspace(0,1500,6))
##    for axis in [ax[3,0], ax[4,1], ax[3,2]]:
##        axis.set_xlabel("Time [min]", fontsize = 10)
##        axis.set_xlim([0,60])
##        axis.set_xticks(np.linspace(0,60,5))
##        
##    # plot
##    for logger in data_dict:
##        df = data_dict[logger]
##        
##        # getting rid of the columns with non-formatted names
##        drop_columns = [col for col in df.columns if "<" in col]
##        df.drop(columns = drop_columns, inplace = True)
##        
##        # iterate over the different TC trees
##        for useful_col in list_useful_cols:
##            
##            # extract the name of hte TC tree
##            TC_tree_name = useful_col.split("-")[0]
##            location = location_plot[TC_tree_name]
##            
##            # create a list of columns that correspond to this TC tree
##            TC_tree_columns = [x for x in df.columns[1:] if useful_col in x]
##            TC_tree_columns.append("testing_time")
##            
##            # created reduced data frame
##            df_reduced = df.loc[:, TC_tree_columns]
##            
##            # plot
##            axis = ax[location[0], [location[1]]][0]
##            mask = (df_reduced.loc[:, "testing_time"]/60 > 0) & (df_reduced.loc[:, "testing_time"]/60 < 60)
##            
##            for j,column in enumerate(df_reduced):
##                if "testing_time" in column:
##                    pass
##                else:
##                    axis.plot(df.loc[mask, "testing_time"]/60,
##                              df.loc[mask, column],
##                              color = colors(j/len(list_useful_cols)),
##                              linestyle = linestyles[j])
##    
##    # plot the door temperatures
##    for j,column in enumerate(data_door):
##        axis = ax[4,1]
##        mask = (data_door.loc[:,"testing_time"]/60 > 0) & (data_door.loc[:, "testing_time"]/60 < 60)
##        if "testing_" in column:
##            pass
##        else:
##            axis.plot(data_door.loc[mask, "testing_time"]/60,
##              data_door.loc[mask, column],
##              color = colors(j/len(list_useful_cols)),
##              linestyle = linestyles[j])
##    
##    # funny plot to add a legend in the first subplot
##    for j in range(12):
##        ax[0,0].plot([],
##          [],
##          linestyle = linestyles[j],
##          color = colors(j/len(list_useful_cols)),
##          label = f"{np.linspace(40,260,12)[j]/100} m")
##        ax[0,0].legend(fancybox = True, loc = "center", fontsize = 10, title = "TC Height", ncol = 3)
##    
##    print(f" time taken: {np.round(time.time() - start,2)} seconds")
##
##    # save and close
##    fig.savefig(f"raw_data/{test_name}_temperatures_raw.png", dpi = 600)
##    plt.close(fig)
##    
#
