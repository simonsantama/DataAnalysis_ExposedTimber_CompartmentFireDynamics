"""
Plots all the calculated data for each experiments.
Adds the video stills at the top of an experiment.

Outputs three figures that are saved in Allvariables_perexperiment/
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pickle

figsize_fullpage = (8,11)

fontsize_labels = 12
fontsize_ticks = 10
fontsize_legends = 8

colors = ["royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan"]

lw_plots = 2
lw_verticallines = 1
lw_grid = 0.75
linestyles = ["-", "--", "-.", ":"]*3

# dictionary with video still times used for marking the first subplots and for creating vertical lines   
videostill_times = {
    "Alpha2": [2, 5.13, 14, 35, 58],
    "Beta1": [2.3, 8.5, 9.9, 20, 30],
    "Beta2": [1.3, 4.2, 10, 18, 26],
    "Gamma": [1.5, 5.4, 17, 39, 59]}

# load processed data
all_processed_data = {}
data_address_folder = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data"
for variable in ["TSC", "Flame_Dimensions", "HRR_total", "Mass_Flow", "Neutral_Plane", "Velocities", 
                 "HRR_internal_massin"]:
    data_address_file = f"{data_address_folder}/{variable}.pkl"
    with open(data_address_file, "rb") as handle:
        all_processed_data[variable] = pickle.load(handle)

for i, test_name in enumerate(["Alpha2", "Beta1", "Beta2", "Gamma"]):
    
    fig, ax = plt.subplots(7,1,figsize = figsize_fullpage, sharex = True)
    fig.suptitle(test_name, fontsize = fontsize_labels)
    fig.subplots_adjust(bottom=0.1, left = 0.1, top = 0.95)
    
    # -----------------------------
    # --------- ax[0] video stills
    # -----------------------------
    
    # import images from video stills to show as first images
    img = mpimg.imread(f"VideoStills/{test_name}.png")
    
    # plot first row for all figures 
    ax[0].set_yticks([])
    ax[0].imshow(img, aspect = "auto", extent = [0,60,0,100])
    
    # create annotations with times for video stills
    for j, time in enumerate(videostill_times[test_name]):
        ax[0].text(x = [6,18,30,42,54][j],
                       y = 85, s = f"{time} min", ha="center", va="center", color="w", fontweight="bold")
        
    # -----------------------------
    # ---------  ax[1] radiation
    # -----------------------------
    
    if test_name in ["Alpha1", "Beta1"]:
        ax[1].set_yticks([])
        pass
    else:
        ax[1].set_ylabel("HF [kW/m$^2$]", fontsize = fontsize_labels)
        ax[1].set_ylim([0,40])
        ax[1].set_yticks(np.linspace(0,40,5))
        
        df = all_processed_data["TSC"][test_name]
        
        mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
        for j,column in enumerate(df.columns[1:5]):
            ax[1].plot(df.loc[mask, "testing_time"]/60,
              df.loc[mask, column]/1000,
              linestyle = linestyles[j],
              color = colors[j],
              linewidth = lw_plots,
              label = f"{[0.6, 1.1, 1.6, 2.1][j]} m")
            
        ax[1].legend(fancybox = True, loc = "upper right", title = "Height", fontsize = fontsize_legends,
          ncol = 2)
        
    
    # -----------------------------
    # ---------  ax[2] heat release rate
    # -----------------------------
    
    ax[2].set_ylabel("HRR [MW]", fontsize = fontsize_labels)
    ax[2].set_ylim([0,8])
    ax[2].set_yticks(np.linspace(0,8,5))
    
    df = all_processed_data["HRR_total"][test_name]
        
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    ax[2].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "THRR"]/1000,
      linestyle = linestyles[0],
      color = colors[0],
      linewidth = lw_plots,
      label = f"HRR total")

    df = all_processed_data["HRR_internal_massin"][test_name]
            
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    ax[2].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "hrr_internal_allmassin"]/1000,
      linestyle = linestyles[1],
      color = colors[1],
      linewidth = lw_plots,
      label = f"HRR internal")
        
    ax[2].legend(fancybox = True, loc = "upper right", fontsize = fontsize_legends,
      ncol = 2)
    
    # -----------------------------
    # --------- ax[3] flame dimensions
    # -----------------------------
    
    ax[3].set_ylabel("Length [m]", fontsize = fontsize_labels)
    ax[3].set_ylim([0,5])
    ax[3].set_yticks(np.linspace(0,5,5))
    
    df = all_processed_data["Flame_Dimensions"][test_name]
        
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    ax[3].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "flame_height_top_smooth"],
      linestyle = linestyles[0],
      color = "k",
      linewidth = lw_plots - 0.5,
      label = f"Flame max. height")
    
    ax[3].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "flame_height_bottom_smooth"],
      linestyle = linestyles[1],
      color = "k",
      linewidth = lw_plots - 0.5,
      label = f"Flame min. height")
    
    ax[3].fill_between(x = df.loc[mask, "testing_time"]/60,
      y1 = df.loc[mask, "flame_height_top_smooth"],
      y2 = df.loc[mask, "flame_height_bottom_smooth"],
      color = "grey",
      alpha = 0.5)
        
    ax[3].legend(fancybox = True, loc = "upper left", fontsize = fontsize_legends,
      ncol = 3)
    
    ax3_twin = ax[3].twinx()
    ax3_twin.set_ylabel("Projection [m]", fontsize = fontsize_labels)
    ax3_twin.set_ylim([0,2.4])
    ax3_twin.set_yticks(np.linspace(0,2.4,5))

    ax3_twin.plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "flame_projection_smooth"],
      linestyle = linestyles[2],
      color = colors[2],
      linewidth = lw_plots,
      label = f"Flame top projection")
        
    ax3_twin.legend(fancybox = True, loc = "lower right", fontsize = fontsize_legends,
      ncol = 3)
    
    # -----------------------------
    # --------- ax[4] mass flow and neutral plane
    # -----------------------------
    
    ax[4].set_ylabel("Mass flow [kg/s]", fontsize = fontsize_labels)
    ax[4].set_ylim([0,1.2])
    ax[4].set_yticks(np.linspace(0,1.2,5))
    
    df = all_processed_data["Mass_Flow"][test_name]
        
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    ax[4].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "mass_in"],
      linestyle = linestyles[0],
      color = colors[0],
      linewidth = lw_plots,
      label = f"Mass in")
    
    ax[4].plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "mass_out"] - df.loc[mask, "mass_in"],
      linestyle = linestyles[1],
      color = colors[1],
      linewidth = lw_plots,
      label = f"Mass pyrolyzates")

    ax[4].legend(fancybox = True, loc = "upper right", fontsize = fontsize_legends,
      ncol = 2) 
    
    # -----------------------------
    # --------- ax[5] Neutral plane and velocities
    # -----------------------------
    
    ax[5].set_ylabel("Velocity [m/s]", fontsize = fontsize_labels)
    ax[5].set_ylim([0,2])
    ax[5].set_yticks(np.linspace(0,12,5))
    
    df = all_processed_data["Velocities"][test_name]
    
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    for j, column in enumerate(df.columns[5:-1]):
    
        ax[5].plot(df.loc[mask, "testing_time"]/60,
          - df.loc[mask, column],
          linestyle = linestyles[j],
          color = colors[j],
          linewidth = lw_plots,
          label = f"{int(column.split('_')[1]) / 100} m")

    ax[5].legend(fancybox = True, loc = "upper right", fontsize = fontsize_legends, title = "Height",
              ncol = 4)

    # neutral plane
    ax5_twin = ax[5].twinx()
    ax5_twin.set_ylabel("Height [m]", fontsize = fontsize_labels)
    ax5_twin.set_ylim([0,1.6])
    ax5_twin.set_yticks(np.linspace(0,1.6,5))
    
    df = df = all_processed_data["Neutral_Plane"][test_name]
    
    mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
    ax5_twin.plot(df.loc[mask, "testing_time"]/60,
      df.loc[mask, "Neutral_Plane_Smooth"],
      linestyle = linestyles[0],
      color = "k",
      linewidth = lw_plots,
      label = f"Neutral Plane")
    
    ax5_twin.legend(fancybox = True, loc = "lower right", fontsize = fontsize_legends,
          ncol = 2)
    
    
    # -----------------------------
    # --------- ax[6] Temperatures
    # -----------------------------
    
    ax[6].set_ylabel("Temperature [$^\circ$C]", fontsize = fontsize_labels)
    ax[6].set_ylim([0,1200])
    ax[6].set_yticks(np.linspace(0,1200,5))

    # -----------------------------
    # --------- general plot formatting
    # -----------------------------
    
    # add grid, vertical lines and change size of y label for all plots
    for axis in ax[1:]:
        axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
        
        for tick in axis.yaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize_ticks)
            
        # draw vertical lines at the times highlighted by the video stills
        ylim = axis.get_ylim()
        for time in videostill_times[test_name]:
            axis.plot((time, time),ylim, linestyle = "--", color = "maroon", alpha = 0.35, linewidth = lw_verticallines)
    
    # format x label for the last plot
    for axis in ax[-1:]:
        axis.set_xlabel("Time [min]", fontsize = fontsize_labels)
        axis.set_xlim([0,60])
        axis.set_xticks(np.linspace(0,60,7))
        
        for tick in axis.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize_ticks)
    
    # save and close
    fig.savefig(f"Allvariables_perexperiment/{test_name}_alldata.png", dpi = 300)
    plt.close(fig)