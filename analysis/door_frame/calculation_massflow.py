"""
Functions used to calculate the mass flow at the door from pressure probes and temperature data


"""

from scipy.signal import savgol_filter
import numpy as np

def calculation_area(number_of_heights = 9, delta_height = 0.2, door_width = 0.8):
    """
    Returns a list with the equivalent area fraction of the door for each probe.
    
    The list provides a number of areas equal to the number of heights measured. Some heights (0.4 m and 1.6 m) have three pressure probes.
    
    Parameters:
    ----------
    number_of_heights: number of heights at which pressure probes were located
        int
    
    delta_height: fraction of the door corresponding to a single pressure probe
        float
        
    door_width: width of the door
        float
        
    Returns:
    -------
    areas = list with the corresponding door area for each pressure probe height
        list
    """
    areas = [delta_height * door_width] * number_of_heights
    
    return areas


def calculation_velocity(df, gamma = 0.94, omega_factor = 2.49, gems_factor = 10, window_length = 21, polyorder = 2):
    """
    Calculates gas flow velocity from the pressure probe readings
    
    Parameters:
    ----------
    df: pandas DataFrame with the raw test data
        pd.DataFrame
        
    gamma: calibration constant for the pressure probe
        float
        
    omega_factor: conversion factor for the omega pressure transducers
        float
        
    gems_factor: conversion factor for the gems pressure transducers
        int
        
    window_length: the length of the filter window for the Savitsky-Golay filter
        int
        
    polyorder: the order of the polynomial used to fit the samples with the Savitsky-Golay filter    
        
    Returns:
    -------
    df: pandas DataFrame with the formatted and calculated data
        pd.DataFrame
    """
    # create a mask to access values before start test
    mask_prestart = df.loc[:, "testing_time"] < 0
    
    # calculate ambient temperature as mean value of all temperatures before start and assing to h = 20 cm.
    temperature_columns = []
    for column in df:
        if "TDD" in column:
            temperature_columns.append(column)
    temperature_ambient = df.loc[mask_prestart, temperature_columns].mean().mean()
    df["TDD.20"] = temperature_ambient

    # calculate mean value reported by the pressure probes before start test
    pressure_columns = [x for x in df.columns if "P" in x]
    pressure_prestart_mean = df.loc[mask_prestart, pressure_columns].mean()
    
    # calculate the zeroed values for the pressure channels (value - mean_prestart)
    for column in pressure_prestart_mean.index:
        df.loc[:, f"{column}_zeroed"] = df.loc[:, column] - pressure_prestart_mean[column]
    
    # determine which pressure transducers were used for each sensor
    omega = ["P1.20", "P2.40", "P3.40", "P4.40", "P5.60", "P6.80"]
    gems = ["P7.100", "P8.120", "P9.140", "P10.160", "P11.160", "P12.160", "P13.180"]
    
    # calculate the pressure difference from the zeroed values
    for column in df:
        if "zeroed" not in column:
            pass
        else:
            probe = column.split("_")[0]
            if probe in omega:
                df.loc[:, f"{probe}_DeltaP"] = df.loc[:, column] * omega_factor
            elif probe in gems:
                df.loc[:, f"{probe}_DeltaP"] = df.loc[:, column] * gems_factor
    
    # drop all nan values before continuing with smoothing (raises LinAlgError)
    df.dropna(axis = 0, inplace = True)
    
    # smooth the pressure readings using a savitsky-golay filter
    for column in df:
        if "DeltaP" in column:
            df.loc[:, f"{column}_smooth"] = savgol_filter(df.loc[:, column],window_length, polyorder)
    
    # drop all other pressure columns (except for pressure smooth)
    PP_drop = []
    for column in df:
        if ("P." in column) and not ("smooth" in column):
            PP_drop.append(column)
    df.drop(columns = PP_drop, inplace = True)
    
    # average those probes which are at the same height
    df.loc[:, "PP_40"] = df.loc[:, ["P2.40_DeltaP_smooth", "P3.40_DeltaP_smooth", "P4.40_DeltaP_smooth"]].mean(axis = 1)
    df.loc[:, "PP_160"] = df.loc[:, ["P10.160_DeltaP_smooth", "P11.160_DeltaP_smooth", "P12.160_DeltaP_smooth"]].mean(axis = 1)

    # rename columns to their respective height
    df.rename(columns = {"P1.20_DeltaP_smooth": "PP_20", "P5.60_DeltaP_smooth": "PP_60", 
                        "P6.80_DeltaP_smooth": "PP_80", "P7.100_DeltaP_smooth": "PP_100", 
                        "P8.120_DeltaP_smooth": "PP_120", "P9.140_DeltaP_smooth": "PP_140", 
                        "P13.180_DeltaP_smooth": "PP_180"}, inplace = True)
    
    # for a given height, if delta p is positive then temperature equals ambient temperature
    for column in df:
        if "PP" in column:
            mask_positives = df.loc[:, column] > 0
            height = column.split("_")[1]
            df.loc[:, f"TC_{height}"] = df.loc[:, f"TDD.{height}"]
            df.loc[mask_positives, f"TC_{height}"] = temperature_ambient
            
    # drop the old temperature columns
    df.drop(columns = [f"TDD.{x}" for x in range(20,200,20)], inplace = True)
    
    # calculate density
    for column in df:
        if "TC" in column:
            height = column.split("_")[1]
            df.loc[:, f"Rho_{height}"] = 353 / (df.loc[:,column] + 273)
    
    # calculate velocities
    for height in range(20,200,20):
        df.loc[:,f"V_{height}"] = gamma * np.sqrt(2 * np.abs(df.loc[:, f"PP_{height}"]) / 
               df.loc[:, f"Rho_{height}"])
        
        # np.abs used for calculation but now negative delta P should give a negative (outward) velocity
        mask_negatives = df.loc[:, f"PP_{height}"] < 0
        df.loc[mask_negatives,f"V_{height}"] = df.loc[mask_negatives,f"V_{height}"] * -1
        
    return

def calculation_massflow(df, areas, Cd = 0.68):
    """
    Calculates the mass flow from the velocities and areas already determined.
    
    Also determines the total inflow and outflow of gases to and from the compartment
    
    Parameters:
    ----------
    df: pandas DataFrame containing all the time dependant data
        pd.DataFrame
    
    areas: fraction of the door area to which each pressure probe corresponds
        list
        
    Cd: discharge coefficient (0.68 according to SFPE and 0.7 according to Prahl and Emmons, 1975)
    
    Returns:
    -------
    df: pandas DataFrame containing all the data.
    """
    
    for i, height in enumerate(list(range(20,200,20))):
        df.loc[:, f"M_{height}"] = Cd * df.loc[:, f"Rho_{height}"] * df.loc[:,f"V_{height}"] * areas[i]
    
    mass_columns = [x for x in df.columns if "M_" in x]
            
    # sum positives and negatives to obtain mass_in and mass_out (slow and dirty implementation)
    for index, row in df.loc[:, mass_columns].iterrows():
        positives = 0
        negatives = 0
        for item in row:
            if item > 0:
                positives += item
            else:
                negatives += np.abs(item)
        df.loc[index, "mass_in"] = positives
        df.loc[index, "mass_out"] = negatives
    df.loc[:, "mass_average"] = df.loc[:, ["mass_in", "mass_out"]].mean(axis = 1)
            
    return None

def calculation_HRR(df, XO2_0 = 0.2095, alpha = 1.105, E_02 = 13.1, ECO_CO2 = 17.6, E_CO2 = 13.3, 
                    E_CO = 12.3, M_a = 29, M_O2 = 32, M_CO2 = 44, M_CO = 28):
    """
    Calculates the HRR from the a
    
    """
    
    return None
