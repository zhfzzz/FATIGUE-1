# -*- coding: utf-8 -*-

# Import libraries:
import numpy as np
import os
from pathlib import Path
import json
import pandas as pd
from pandas import DataFrame
import append2excel

from scipy import interpolate

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import fatpack #Download from: pip install fatpack
import fnmatch

# Import additional py-files:
import DNV_endurance_curves as dnv
import compoundTimeseries as annual

# Prints full
pd.options.display.max_columns = None
# pd.reset_option('max_columns')

# # Finding the path to Dropboxfolder
# def resource_path():
#     try:
#         json_path = (Path(os.getenv('LOCALAPPDATA'))/'Dropbox'/'info.json').resolve()
#     except FileNotFoundError:
#         json_path = (Path(os.getenv('APPDATA'))/'Dropbox'/'info.json').resolve()
    
#     with open(str(json_path)) as f:
#         return json.load(f)
# db_location = resource_path()
# db_location = db_location["business"]["path"]

db_location = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Wavefoil AS/Wavefoil AS - Dropbox Arkiv\Teknisk utvikling')
g=-9.81 #m/s^2
mass = 78000 #kg

def fatigueLoad(foil_load, FN_interpolated, k=None, foilmodule=None, outputfolder=None, iteration=None, V=None):
    
    # Set global variables:
    global curve, category, S, fatigue_damage, path_main, y, df, li_img, li_fd

    # System paths
    path_main = db_location +  "\\" + foilmodule[0:2] + ' ' + foilmodule[2:] + "\FEM ANALYSE\RAPPORT"
    os.chdir(path_main)
    print(path_main)

    df = pd.read_excel (path_main + '\\Input til FATIGUE.xlsx', sheet_name=foilmodule)
    # print (df.iloc[:, [0,1]])
 
     # Generates overview of the loads acting on the foil:
    #%%
    reversals, reversals_ix = fatpack.find_reversals(foil_load)#, k)
    cycles, residue = fatpack.find_rainflow_cycles(reversals)
    processed_residue = fatpack.concatenate_reversals(residue, residue)
    cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
    cycles_total = np.concatenate((cycles, cycles_residue))
    
    # Find the rainflow ranges from the cycles
    force_range = fatpack.find_rainflow_ranges(foil_load)#, k)
    
    figsize = np.array([140., 140.]) / 10
    fig = plt.figure(dpi=180, figsize=figsize)
    fig.suptitle("Foil load data:", fontsize=16)
    
    # Plotting signal with reversals.
    ax_signal = plt.subplot2grid((3, 2), (0, 0))
    ax_signal.plot(foil_load/1000)
    ax_signal.plot(reversals_ix, foil_load[reversals_ix]/1000, 'ro', fillstyle='none',
                    label='reversal')
    # ax_signal.legend()
    ax_signal.set(title="Signal", ylabel="Foil normal force [kN]", xlabel="Index", xlim=[0, 5000])
    
    # Plotting the cumulative distribution of the cycle count
    ax_cumdist = plt.subplot2grid((3, 2), (1, 0))
    N, force_distribution = fatpack.find_range_count(force_range, 25)
    Ncum = N.sum() - np.cumsum(N)
    ax_cumdist.semilogx(Ncum, force_distribution/1000)
    ax_cumdist.set(title="Cumulative distribution, rainflow ranges",
                   xlabel="Count, N", ylabel="Foil normal force range [kN]")
    
    # Interpolate for a fixed range of forces
    df_FN_interpolated = DataFrame (FN_interpolated,columns=['Foil normal force range [N]'])   
    f = interpolate.interp1d(force_distribution, Ncum, fill_value=0, bounds_error=False)
    Ncum_normalized = np.round(f(FN_interpolated))     
    df_Ncum = DataFrame (Ncum_normalized,columns=['Year ' + str(iteration) + ': Number of cycles [-]'])   

    # Save distribution to excel file
    filename= outputfolder + '\FOIL FORCE STATISTICS ' + str(int(V/0.5144)) + ' knots.xlsx'
    append2excel.append_df_to_excel(filename, df_FN_interpolated, sheet_name='Sheet1', startcol=0, startrow = 5, truncate_sheet=None, index=False)
    append2excel.append_df_to_excel(filename, df_Ncum, sheet_name='Sheet1', startcol=iteration+4, startrow = 5,  truncate_sheet=None, index=False)

    return force_range, force_distribution

    #%%
def predictLifetime(force_range, foil_time, db_location, foilmodule=None):
    """
    Predicts lifetime for each critical hotspot in the foil module
    Ncum =  Number of cycles during life time [-]
    force_distribution =    Force range [N]   
    """
    # System paths
    path_main = db_location +  "\\" + foilmodule[0:2] + ' ' + foilmodule[2:] + "\FEM ANALYSE\RAPPORT"

    df_lifetime = pd.read_excel (path_main + '\\Input til FATIGUE.xlsx', sheet_name=foilmodule)
    
    li_img = fnmatch.filter(os.listdir(path_main), '*hotspot*')
    li_fd = []           
    table_data = []
    table_headers = ("Curve", "Est. fl", "True fl", "Fl error")
    
    N = np.logspace(4, 8)
    
    for i in df_lifetime.index:
        # Find stresses acting on component in hotspot from foil load y (scale):
        stress_range = force_range * df_lifetime.loc[i,"stress_per_load[MPa/N]"]
        print(df_lifetime.loc[i, "component"] + ': ' +df_lifetime.loc[i, "hotspot"])
        print('   Mean stress range: ' + str(np.mean(stress_range)))
        print('   Max stress range: ' + str(max(stress_range)))
        print('   Max stress level: ' + str(max(stress_range)/2))
                
        curve = dnv.DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection(df_lifetime.loc[i, "DNV_category"])
        fatigue_damage = curve.find_miner_sum(stress_range)
        df_lifetime.loc[i, "fatigue_damage"] = fatigue_damage
        
        #Hvor mange år er komponenten testet?
        time_simulated = foil_time[-1]/(60*60*24*365)

        #Hvor mye lenger tåler komponentet?
        ratio = 1/fatigue_damage

        #Estimated lifetime
        lifetime = time_simulated * ratio
        df_lifetime.loc[i, "lifetime"] = lifetime

        print("   FATIGUE DAMAGE D = {:.4f} ".format(fatigue_damage) + ", estimated lifetime:  " + str(int(lifetime)) + " years\n")
            

    return df_lifetime

#%% Fatigue analysis 
database = r'D:\FATIGUE\WF5910'
n_seconds = round(60*60*24*365.2425)
n_years = 1
for year in range(1, int(np.ceil(n_years)+1) ):
    #%% Create realistic time series for a period
    import time
    t = time.time()

    if n_years < 1:
        total_time_series, total_FN_series, total_Zacc_series, V = annual.createTimeseries(database, n_seconds*n_years)
    else:
        total_time_series, total_FN_series, total_Zacc_series, V = annual.createTimeseries(database, n_seconds)
        
    foil_time = total_time_series[0::10] #dt=2s instead of 0.2s from simulations.
    foil_load = total_FN_series[0::10] # LOAD PER FOIL  
    a = g - total_Zacc_series[0::10] #Positive if foilmodule accelerates upwards
    support_load = foil_load + mass*a


    #%%Fatique loads
    FN_interpolated = np.arange(50000, 4000000, 50000) 
    force_range, force_distributiion = fatigueLoad(foil_load, FN_interpolated, k=32, foilmodule="WF5910", outputfolder = database, iteration = year, V=V)
    
    t2 = time.time() 
    elapsed = t2 - t
    print('    Brukte ' + str(elapsed) + ' sekunder på år ' + str(year) + '\n\n')


# #%% Bruker force_range fra siste år til å estimere levetider.
df_lifetime = predictLifetime(force_range, foil_time, db_location,foilmodule="WF5910")
