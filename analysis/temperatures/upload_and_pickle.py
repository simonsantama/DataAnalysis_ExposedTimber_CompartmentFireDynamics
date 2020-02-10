"""
This script uploads temperatures from each test and distributes them by thermocouple tree.

It also creates plots of the raw temperatures to visualize the data.

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

all_raw_data = {}
all_processed_data = {}

# plotting parameters
linestyles = ["-", "--", "-.", ":"]*3
colors = ["black", "royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan"]*2

# iterate over all tests
for test_name in ["Alpha2", "Beta2", "Gamma"]:
    
    # upload the data from both data loggers
    file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/temperature/{test_name}_Thermocouple_tree_analysis.xlsx"
    df_A = pd.read_excel(file_address, sheet_name = "LoggerA", skiprows = 1)
    df_B = pd.read_excel(file_address, sheet_name = "LoggerB", skiprows = 1)
    
    # two data loggers means two different data frames
    for df in [df_A, df_B]:
        df.loc[:, "testing_time"] = df.loc[:, "Time [min]"]*60
    
    # add new columns to include the name of the TC tree
    if test_name == "Alpha1":
        pass
    
    elif test_name == "Alpha2":
        # centre T22
        c_cols = []
        for column in df_A.columns[1:13]:
            df_A.loc[:, f"centre_{column.split('m')[0]}"] = df_A.loc[:, column]
            c_cols.append(f"centre_{column.split('m')[0]}")
        # left door T11
        ld_cols = []
        for column in df_A.columns[13:25]:
            df_A.loc[:, f"leftdoor_{column.split('m')[0]}"] = df_A.loc[:, column]
            ld_cols.append(f"leftdoor_{column.split('m')[0]}")
        # right wall T33
        rw_cols = []
        for column in df_A.columns[25:36]:
            df_A.loc[:, f"rightwall_{column.split('m')[0]}"] = df_A.loc[:, column]
            rw_cols.append(f"rightwall_{column.split('m')[0]}")
        # right door T31
        rd_cols = []
        for column in df_A.columns[36:46]:
            df_A.loc[:, f"rightdoor_{column.split('m')[0]}"] = df_A.loc[:, column]
            rd_cols.append(f"rightdoor_{column.split('m')[0]}")
        # left wall wall
        lw_cols = []
        for column in df_A.columns[46:58]:
            df_A.loc[:, f"rightdoor_{column.split('m')[0]}"] = df_A.loc[:, column]
            lw_cols.append(f"rightdoor_{column.split('m')[0]}")
        
    elif test_name == "Beta1":
        pass
    
    elif test_name == "Beta2":
        pass
    
    elif test_name == "Gamma":
        pass
    
    
    # create a temperature plot that shows ALL thermocouple for ALL thermocouple trees
    fig = plt.figure(figsize = (8,11), constrained_layout = True)
    gs = fig.add_gridspec(3,2)
    
    # create subplots to populate the gridspec
    ax0 = fig.add_subplot(gs[2,0])
    ax0.set_title("Left_Door. T11")
    ax1 = fig.add_subplot(gs[2,1])
    ax1.set_title("Right_Door. T31")
    ax2 = fig.add_subplot(gs[1,:])
    ax2.set_title("Centre. T22")
    ax3 = fig.add_subplot(gs[0,0])
    ax3.set_title("Left_Wall. T13")
    ax4 = fig.add_subplot(gs[0,1])
    ax4.set_title("Right_Wall. T33")
    all_axes = [ax0, ax1, ax2, ax3, ax4]
    
    # format the axes
    for axis in all_axes:
        axis.set_xlabel("Time [min]")
        axis.set_xlim([0,60])
        axis.set_xticks(np.linspace(0,60,7))
        
        axis.set_ylabel("Temperature [$^\circ$C]")
        axis.set_ylim([0,1400])
        axis.set_yticks(np.linspace(0,1400,5))

        axis.grid(True, linestyle = "--", color = "gainsboro", linewidth = 0.75)
        
    # plot
    for j, column_list in enumerate([ld_cols, rd_cols, c_cols, lw_cols, rw_cols]):
        
        mask = (df.loc[:, "testing_time"] > 0) & (df.loc[:, "testing_time"]/60 < 60)
        for k,column in enumerate(column_list):
            all_axes[j].plot(df_A.loc[mask, "testing_time"]/60,
                    df_A.loc[mask, column],
                    linestyle = linestyles[k],
                    color = colors[k],
                    linewidth = 2,
                    label = f"{int(column.split('_')[1])/100} m")
                    
        all_axes[j].legend(fancybox = True, loc = "lower right", ncol = 3, fontsize = 8)
                    
    
    fig.savefig(f"{test_name}_allTCs_raw.png", dpi = 300)
    plt.close(fig)
    
    break

