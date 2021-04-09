# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:24:31 2021

@author: lenna
"""

import numpy as np

# fname = r"C:\Users\Audun\Wavefoil AS\Wavefoil AS - Dokumenter\Hydrodynamikk\Utviklingsarbeid\dynamisk stall modell testcase\Output\Fatigue\FoilForce_simtime-10800 heading-1 Tp-1 Hs-1 vel-1.out"




def readwavefoilforces(fname):
    """
    Reads binary result files from the wavefoil dynamic stall program in Julia
   
    Parameters
    ----------
    fname : str
        Path to the .out file located in Output/Fatigue subfolder of a given case
    Returns
    -------
    time : Array of Float64
        Array of timestamps of the simulation
    FC : Array of Float64
        Chordwise force on foil at given timeinstance
    FN : Array of Float64
        Normal force on foil at given timeinstance
    FX : Array of Float64
        Force in global x coordinate
    FZ : Array of Float64
        Force in global z coordinate
    Zacc : Array of Float64
        Local acceleration at foil module
    """
    tmp = np.fromfile(fname,dtype=float)
    N = int(len(tmp)/6)
    # time, FC, FN, FX, FZ, Zacc
    return tmp[0:N], tmp[N:2*N], tmp[2*N:3*N], tmp[3*N:4*N], tmp[4*N:5*N], tmp[5*N:6*N]
