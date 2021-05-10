import numpy as np

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
    AoA : Array of Float64
        Quasi static angle of attack
    alphaE : Array of Float64
        dynamic angle of attack 1
    alphaf : Array of Float64
        dynamic angle of attack 2
    """
    tmp = np.fromfile(fname,dtype=float)
    N = int(len(tmp)/9)
    # time, FC, FN, Zacc
    return tmp[0:N], tmp[N:2*N], tmp[2*N:3*N], tmp[3*N:4*N], tmp[4*N:5*N], tmp[5*N:6*N], tmp[6*N:7*N], tmp[7*N:8*N], tmp[8*N:9*N]