# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:09:24 2021

@author: Audun
"Script to create dimensional time series for fatigue analysis.

Input:
    - 3 hour time series for each sea state/heading/speed (LOADS ARE MULTIPLIED BY TWO)
    - Probability tables for sea state/heading""

Output: 
    - 1 year time series

"""


import pandas as pd 
import readwavefoilforcesexample
import numpy as np
import random
            
def createTimeseries(database, total_seconds_in_period):
    total_FN_series = []
    total_Zacc_series = []
    
    heading_index=0
    V_index=0
    print("heading_index = " + str(heading_index))
    print("V_index = " + str(V_index))
    
    #%% Load simulation variables
    headings = pd.read_csv(database + '\FoilForce_variables-headings.csv' ,header=None)[0].to_numpy()
    periods = pd.read_csv(database + '\FoilForce_variables-Tp.csv' ,header=None)[0].to_numpy()
    heights = pd.read_csv(database + '\FoilForce_variables-Hs.csv' ,header=None)[0].to_numpy()
    velocities = pd.read_csv(database + '\FoilForce_variables-velocities.csv' ,header=None)[0].to_numpy()
    print('V=' + str(velocities[V_index])      )
                  
    #%% Find total number of observations
    observations = 0
    progression = 0
    for heading_index in range(len(headings)):             
        temp = pd.read_csv(database + '\\HsTpScatter - relative wave direction ' + str(heading_index+1) + '.csv',index_col=0)
        observations = observations + temp.sum().sum()

    #Go though all simulations and compose a representative time series
    for heading_index in range(len(headings)):   
        wave_stat = pd.read_csv(database + '\\HsTpScatter - relative wave direction ' + str(heading_index+1) + '.csv',index_col=0)
        print('heading_index = ' + str(heading_index))
        for Hs_index in range(len(heights)): # Python indexing
            print('    Hs_index = ' + str(Hs_index))
            for Tp_index in range(len(periods)): # Python indexing
                print('        Tp_index = ' + str(Tp_index))
                        
                if (heights[Hs_index]/periods[Tp_index] <= 0.75):
                    try:
                        # Import 3 hour time series
                        fname = database + '\PortFoilForce_simtime-10800 heading-' + str(heading_index+1) + ' Tp-' + str(Tp_index+1) + ' Hs-' + str(Hs_index+1) +' vel-' + str(V_index+1) +'.out'
                        time, FC, FN, Zacc = readwavefoilforcesexample.readwavefoilforces(fname)
    
                        probability = wave_stat.iloc[Hs_index,Tp_index] / observations
                    except:
                        print('        (File does not exist)')
                        probability = 0   
                        
                
                else:
                    # Wave combination doesn't exist
                    probability = 0          
                    print('        (Wave combination does not exist)')
                
                seconds_in_period = probability * total_seconds_in_period 
                
                number_of_3_hour_time_series = seconds_in_period / time[-1] #In period
        
                n = int(number_of_3_hour_time_series * len(time) ) #Number of time steps to be added to total time series
        
                FN_temp = np.tile(FN, int(np.floor(number_of_3_hour_time_series) + 1) ) # Temporary force series        
                Zacc_temp = np.tile(Zacc, int(np.floor(number_of_3_hour_time_series) + 1) ) # Temporary force series        

                
                start_index =  random.randint(0, len(FN_temp)-n) #Pick random slot in time series
    
                new_force_series = FN_temp[start_index : start_index + n]       
                total_FN_series = np.concatenate((total_FN_series,new_force_series)) 
                
                new_acc_series = Zacc_temp[start_index : start_index + n]
                total_Zacc_series = np.concatenate((total_Zacc_series,new_acc_series)) 
                
                progression = progression + probability
                
            print('        Progression: ' + str(int(progression*100)) + "%\n")
    
    #%% Create time
    total_time_series=np.arange(0, total_seconds_in_period, time[1]-time[0], dtype=None)     
    
    #%% Adjust time series for correct number of elements 
    ni = len(total_time_series) - len(total_FN_series)
    if ni > 0:
        total_FN_series =   np.concatenate( (total_FN_series,   np.zeros(ni)) )
        total_Zacc_series = np.concatenate( (total_Zacc_series, np.zeros(ni)) )
    
    return total_time_series, total_FN_series, total_Zacc_series, velocities[V_index]
                                                       
#%% Additional 

                                             