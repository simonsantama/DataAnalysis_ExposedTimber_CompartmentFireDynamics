"""
Plots all the data in independent figures for analysis (not plots for the paper)
This is useful to see the data as a time series before creating the plots for the paper

"""
import matplotlib.pyplot as plt
import numpy as np
import pickle

figsize_fullpage = (8,11)

fontsize_labels = 14
fontsize_ticks = 12
fontsize_legends = 12

colors = ["royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan"]

lw_plots = 2
lw_grid = 0.75
linestyles = ["-", "--", "-.", ":"]*3


# --- FIGURE 1A. FLAME DIMENSIONS (HEIGHT AND DEPTH)
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Flame_Dimensions.pkl"
with open(data_address, "rb") as handle:
    Flame_Dimensions = pickle.load(handle)
    
fig, ax = plt.subplots(4,2,figsize = figsize_fullpage, sharex = True, sharey = "col")

# format each subplot
for i, axis in enumerate(ax[:,0]):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Length [m]", fontsize = fontsize_labels)
    axis.set_ylim([-0.5,5])
    axis.set_yticks(np.linspace(0,5,6))
    
for i, axis in enumerate(ax[:,1]):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Length [m]", fontsize = fontsize_labels)
    axis.set_ylim([-0.2,2])
    axis.set_yticks(np.linspace(0,2,6))
    
for axis in ax.flatten():
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
        
for i, axis in enumerate(ax[3,:]):
    axis.set_xlabel("Time [min]", fontsize = fontsize_labels)
    axis.set_xlim([0,60])
    axis.set_xticks(np.linspace(0,60,7))

# plot
for i, key in enumerate(Flame_Dimensions):
    flame_dimensions_data = Flame_Dimensions[key]
    
    for axis in ax[i,:]:
        axis.set_title(key, fontsize = fontsize_labels)
    
    # plot height
    for j, column in enumerate(flame_dimensions_data.columns[11:13]):
        ax[i,0].plot(flame_dimensions_data.loc[:, "testing_time"]/60,
                flame_dimensions_data.loc[:, column],
                linewidth = lw_plots, 
                color = colors[j],
                linestyle = linestyles[j],
                alpha = 0.75,
                label = f"{column.split('_')[1]}_{column.split('_')[2]}")
    
    # plot flame depth
    for j, column in enumerate(flame_dimensions_data.columns[13:16]):
        ax[i,1].plot(flame_dimensions_data.loc[:, "testing_time"]/60,
                flame_dimensions_data.loc[:, column],
                linewidth = lw_plots, 
                color = colors[j],
                linestyle = linestyles[j],
                alpha = 0.75,
                label = f"{column.split('_')[1]}_{column.split('_')[2]}")

# add legends
for axis in ax.flatten():
    axis.legend(fancybox = True, fontsize = fontsize_legends - 4, loc = "upper right")

# save and close figure   
fig.tight_layout()
fig.savefig("FlameDimensionsA.png", dpi = 600)
plt.close(fig)
# --- FIGURE 1A. FLAME DIMENSIONS (HEIGHT AND DEPTH)

# --- FIGURE 1B. FLAME DIMENSIONS (HEIGHT AND DEPTH)
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Flame_Dimensions.pkl"
with open(data_address, "rb") as handle:
    Flame_Dimensions = pickle.load(handle)
    
fig, ax = plt.subplots(4,2,figsize = figsize_fullpage, sharex = True, sharey = "col")

# format each subplot
for i, axis in enumerate(ax[:,0]):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Length [m]", fontsize = fontsize_labels)
    axis.set_ylim([-0.5,5])
    axis.set_yticks(np.linspace(0,5,6))
    
for i, axis in enumerate(ax[:,1]):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Area [m$^2$]", fontsize = fontsize_labels)
    axis.set_ylim([-0.25,2.5])
    axis.set_yticks(np.linspace(0,2.5,6))
    
for axis in ax.flatten():
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
        
for i, axis in enumerate(ax[3,:]):
    axis.set_xlabel("Time [min]", fontsize = fontsize_labels)
    axis.set_xlim([0,60])
    axis.set_xticks(np.linspace(0,60,7))

# plot
for i, key in enumerate(Flame_Dimensions):
    flame_dimensions_data = Flame_Dimensions[key]
    
    for axis in ax[i,:]:
        axis.set_title(key, fontsize = fontsize_labels)
    
    # plot height
    for j, column in enumerate(["flame_ellipse_length_smooth"]):
        ax[i,0].plot(flame_dimensions_data.loc[:, "testing_time"]/60,
                flame_dimensions_data.loc[:, column],
                linewidth = lw_plots, 
                color = colors[j],
                linestyle = linestyles[j],
                alpha = 0.75,
                label = f"{column.split('_')[1]}_{column.split('_')[2]}")
    
    # plot flame depth
    ax[i,1].plot(flame_dimensions_data.loc[:, "testing_time"]/60,
            flame_dimensions_data.loc[:, "flame_area_smooth"],
            linewidth = lw_plots, 
            color = colors[0],
            linestyle = linestyles[0],
            alpha = 0.75,
            label = "flame_area")
    # plot flame depth
    ax2 = ax[i,1].twinx()
    ax2.set_ylabel("Flame Angle [deg]")
    ax2.set_ylim([0,180])
    ax2.set_yticks(np.linspace(0,180,5))
    ax2.plot(flame_dimensions_data.loc[:, "testing_time"]/60,
            flame_dimensions_data.loc[:, "flame_ellipse_angle_smooth"],
            linewidth = lw_plots, 
            color = colors[1],
            linestyle = linestyles[1],
            alpha = 0.75,
            label = "flame_angle")
    ax2.legend(fancybox = True, fontsize = fontsize_legends - 4, loc = "lower right")

# add legends
for axis in ax.flatten():
    axis.legend(fancybox = True, fontsize = fontsize_legends - 4, loc = "upper right")

# save and close figure   
fig.tight_layout()
fig.savefig("FlameDimensionsB.png", dpi = 600)
plt.close(fig)
# --- FIGURE 1B. FLAME DIMENSIONS (HEIGHT AND DEPTH)

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

# --- FIGURE 2. HEAT RELEASE RATE
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/HRR_total.pkl"
with open(data_address, "rb") as handle:
    HRR_total = pickle.load(handle)
    
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/HRR_internal.pkl"
with open(data_address, "rb") as handle:
    HRR_internal = pickle.load(handle)
    
fig, ax = plt.subplots(4,1,figsize = figsize_fullpage, sharex = True, sharey = True)

# format each subplot
for i, axis in enumerate(ax):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("HRR [MW]", fontsize = fontsize_labels)
    axis.set_ylim([-0.8,8])
    axis.set_yticks(np.linspace(0,8,5))
    
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    
ax[3].set_xlabel("Time [min]", fontsize = fontsize_labels)
ax[3].set_xlim([0,60])
ax[3].set_xticks(np.linspace(0,60,7))

# plot
for i, key in enumerate(HRR_total):
    hrr_total = HRR_total[key]
    hrr_internal = HRR_internal[key]
    
    ax[i].set_title(key, fontsize = fontsize_labels)
    
    ax[i].plot(hrr_total.loc[:, "testing_time"]/60,
            hrr_total.loc[:, "THRR"]/1000,
            linewidth = lw_plots, 
            color = colors[0],
            linestyle = linestyles[0],
            alpha = 0.75,
            label = "Total HRR")
    
    ax[i].plot(hrr_internal.loc[:, "testing_time"]/60,
            hrr_internal.loc[:, "hrr_internal"]/1000,
            linewidth = lw_plots, 
            color = colors[1],
            linestyle = linestyles[1],
            alpha = 0.75,
            label = "Internal HRR")

    # add legends
    ax[i].legend(fancybox = True, fontsize = fontsize_legends, loc = "upper right")



# save and close figure   
fig.tight_layout()
fig.savefig("HRRvsTime.png", dpi = 600)
plt.close(fig)
# --- FIGURE 2. HEAT RELEASE RATE

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #


# ---- FIGURE 3. TSC
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/TSC.pkl"
with open(data_address, "rb") as handle:
    TSC = pickle.load(handle)
    
fig, ax = plt.subplots(2,1,figsize = figsize_fullpage, sharex = True, sharey = True)

# format each subplot
for i, axis in enumerate(ax):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Heat Flux [kW/m$^2$]", fontsize = fontsize_labels)
    axis.set_ylim([-4,40])
    axis.set_yticks(np.linspace(0,40,5))
    axis.text(30, 36,  f"{[2,4][i]} meters from the opening", 
                bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'),
                ha = "center", fontsize = fontsize_legends)
    
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    
ax[1].set_xlabel("Time [min]", fontsize = fontsize_labels)
ax[1].set_xlim([0,60])
ax[1].set_xticks(np.linspace(0,60,7))

# create an extra axis to add the additional legend
ax2 = ax[1].twinx()

# plot
for i, key in enumerate(TSC):
    ihf_data = TSC[key]
    
    for height in range(4):
        ax[0].plot(ihf_data.loc[:, "testing_time"]/60,
                ihf_data.loc[:, f"sIHF_{height}"]/1000,
                linewidth = lw_plots, 
                color = colors[i],
                linestyle = linestyles[height],
                alpha = 0.75)
        
    for height in range(4,8):
        ax[1].plot(ihf_data.loc[:, "testing_time"]/60,
                ihf_data.loc[:, f"sIHF_{height}"]/1000,
                linewidth = lw_plots, 
                color = colors[i],
                linestyle = linestyles[height-4],
                alpha = 0.75)

    # create dummy plot for using wiht the legends
    ax[1].plot([],[],
      color = colors[i],
      label = ["Alpha 2", "Beta 2", "Gamma"][i])

# create dummy plots to have two legends
for j in range(4):
    ax2.plot([],[],
         color = "black",
         linestyle = linestyles[j],
         label = ["0.6 m", "1.1 m", "1.6 m", "2.1 m"][j])

# add legends
ax[1].legend(fancybox = True, fontsize = fontsize_legends, loc = "upper left", title = "Experiment")
ax2.legend(fancybox = True, fontsize = fontsize_legends, loc = "upper right", title = "Sensor Height")
# remove all ticks and labels from axis 2
ax2.set_yticks([]) 

# save and close figure   
fig.tight_layout()
fig.savefig("HFvsTime.png", dpi = 600)
plt.close(fig)
# ---- FIGURE 3. TSC

# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

# ---- FIGURE 4. Velocities
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Velocities.pkl"
with open(data_address, "rb") as handle:
    Velocities = pickle.load(handle)
    
fig, ax = plt.subplots(4,1,figsize = figsize_fullpage, sharex = True, sharey = True)

# format each subplot
for i, axis in enumerate(ax):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Velocity [m/s]", fontsize = fontsize_labels)
    axis.set_ylim([-10,10])
    axis.set_yticks(np.linspace(-10,10,5))
    
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    
ax[1].set_xlabel("Time [min]", fontsize = fontsize_labels)
ax[1].set_xlim([0,60])
ax[1].set_xticks(np.linspace(0,60,7))

# plot
for i, key in enumerate(Velocities):
    velocities_data = Velocities[key]
    
    # add plot title
    ax[i].set_title(key, fontsize = fontsize_labels)
    
    for j, column in enumerate(velocities_data.columns[1:]):
        ax[i].plot(velocities_data.loc[:, "testing_time"]/60,
                velocities_data.loc[:, column],
                linewidth = lw_plots, 
                alpha = 0.75,
                label = column)
    
    # add legend
    ax[i].legend(fancybox = True, fontsize = fontsize_legends - 3, loc = "upper right", ncol = 3)

# save and close figure   
fig.tight_layout()
fig.savefig("VelocitiesvsTime.png", dpi = 600)
plt.close(fig)
# ---- FIGURE 4. Velocities


# ---------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------- #

# ---- FIGURE 4. Neutral Plane
data_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Neutral_Plane.pkl"
with open(data_address, "rb") as handle:
    Neutral_Plane= pickle.load(handle)
    
fig, ax = plt.subplots(4,1,figsize = figsize_fullpage, sharex = True, sharey = True)
#
# format each subplot
for i, axis in enumerate(ax):
    axis.grid(True, color = "gainsboro", linewidth = lw_grid, linestyle = "--")
    axis.set_ylabel("Neutral Plane [m]", fontsize = fontsize_labels)
    axis.set_ylim([0,2])
    axis.set_yticks(np.linspace(0,2,5))
    
    for tick in axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    for tick in axis.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_ticks)
    
ax[1].set_xlabel("Time [min]", fontsize = fontsize_labels)
ax[1].set_xlim([0,60])
ax[1].set_xticks(np.linspace(0,60,7))

# plot
for i, key in enumerate(Velocities):
    np_data = Neutral_Plane[key]
    
    # add plot title
    ax[i].set_title(key, fontsize = fontsize_labels)
    
    for j, column in enumerate(np_data.columns[1:]):
        ax[i].plot(np_data.loc[:, "testing_time"]/60,
                np_data.loc[:, column],
                linewidth = lw_plots, 
                alpha = 0.75)

# save and close figure   
fig.tight_layout()
fig.savefig("NeutralPlanevsTime.png", dpi = 600)
plt.close(fig)
# ---- FIGURE 4. Neutral Plane