# -*- coding: utf-8 -*-

# Import libraries:
import numpy as np
import os
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import fatpack
import fnmatch

# Import additional py-files:
import DNV_endurance_curves as dnv

# Prints full
pd.options.display.max_columns = None
# pd.reset_option('max_columns')

# Finding the path to Dropboxfolder
def resource_path():
    try:
        json_path = (Path(os.getenv('LOCALAPPDATA'))/'Dropbox'/'info.json').resolve()
    except FileNotFoundError:
        json_path = (Path(os.getenv('APPDATA'))/'Dropbox'/'info.json').resolve()
    
    with open(str(json_path)) as f:
        return json.load(f)
db_location = resource_path()
db_location = db_location["business"]["path"]


def fatigueDamage(foil_load, k=64, foilmodule=None):
    
    # Set global variables:
    global curve, category, S, fatigue_damage, path_main, y, df, li_img, li_fd

    # System paths
    path_main = db_location + "\Wavefoil Team Folder\Teknisk utvikling" + "\\" + foilmodule[0:2] + ' ' + foilmodule[2:] + "\FEM ANALYSE\RAPPORT"
    os.chdir(path_main)
    print(path_main)

    df = pd.read_excel (path_main + '\\Input til FATIGUE.xlsx', sheet_name=foilmodule)
    print (df.iloc[:, [0,1]])
 
        # Generates overview of the loads acting on the foil:
    #%%
    reversals, reversals_ix = fatpack.find_reversals(foil_load/1000, k)
    cycles, residue = fatpack.find_rainflow_cycles(reversals)
    processed_residue = fatpack.concatenate_reversals(residue, residue)
    cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
    cycles_total = np.concatenate((cycles, cycles_residue))
    
    # Find the rainflow ranges from the cycles
    S = fatpack.find_rainflow_ranges(foil_load/1000, k)
    
    figsize = np.array([140., 140.]) / 10
    fig = plt.figure(dpi=180, figsize=figsize)
    fig.suptitle("Foil load data:", fontsize=16)
    
    # Plotting signal with reversals.
    ax_signal = plt.subplot2grid((3, 2), (0, 0))
    ax_signal.plot(foil_load/1000)
    ax_signal.plot(reversals_ix, foil_load[reversals_ix]/1000, 'ro', fillstyle='none',
                   label='reversal')
    ax_signal.legend()
    ax_signal.set(title="Signal", ylabel="Foil load [kN]", xlabel="Index", xlim=[200, 500])
    
    # Plotting the cumulative distribution of the cycle count
    ax_cumdist = plt.subplot2grid((3, 2), (1, 0))
    N, Sr = fatpack.find_range_count(S, 100)
    Ncum = N.sum() - np.cumsum(N)
    ax_cumdist.semilogx(Ncum, Sr)
    ax_cumdist.set(title="Cumulative distribution, rainflow ranges",
                   xlabel="Count, N", ylabel="Range, Sr")
    
    # Plotting the rainflow matrix of the total cycle count
    ax_rfcmat = plt.subplot2grid((3, 2), (1, 1), rowspan=1, aspect='equal')
    bins = np.linspace(cycles_total.min(), cycles_total.max(), 128)
    rfcmat = fatpack.find_rainflow_matrix(cycles_total, bins, bins)
    X, Y = np.meshgrid(bins, bins, indexing='ij')
    C = ax_rfcmat.pcolormesh(X, Y, rfcmat, cmap='magma')
    fig.colorbar(C)
    ax_rfcmat.set(title="Rainflow matrix",
                  xlabel="Starting point", ylabel="Destination point")
    
    # Plotting table with info:
    table_data = []
    table_data.append(["Max load foils [kN]", '{:.2f}'.format(foil_load.max())])
    table_data.append(["Number of cycles", '{:.2e}'.format(len(foil_load))])
    
    ax_text = plt.subplot2grid((3, 2), (0, 1), rowspan=1, aspect='equal')
    ax_text.axis('tight')
    ax_text.axis('off')
    table_data = plt.table(cellText=table_data, cellLoc="left", loc="upper left")
    table_data.scale(1, 1.2)
    plt.title("Fatigue data:")
    
    fig.subplots_adjust(top=0.94)
    plt.show()
    
    
    
    #%%
    li_img = fnmatch.filter(os.listdir(path_main), '*hotspot*')
    li_fd = []
    
    # for i in os.listdir(path_main):
    #     if i.endswith("hotspot*.png"):
    #         li_pics.append(i)
    
    for i in df.index:
        # Find stresses acting on component in hotspor from foil load y (scale):
        y = foil_load * df.loc[i,"stress_per_load[MPa/N]"]
        
        # figsize = np.array([140., 140.]) / 10
        # fig = plt.figure(dpi=180, figsize=figsize)
        # fig.suptitle(df.loc[i, "component"], fontsize=16)
        
        
        # ax_endurance = plt.subplot2grid((3, 2), (1, 0),)
        
        table_data = []
        table_headers = ("Curve", "Est. fl", "True fl", "Fl error")
        
        N = np.logspace(4, 8)
        # # print("{0:<7} | {1:>8} | {2:>8} | {3:>8}".format("Curve", "Est. fl[MPa]", "True fl[MPa]", "Fl error"))
        # for name in dnv.DNVGL_EnduranceCurve.names:
        #     # print(name)
        #     curve = dnv.DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection(name)
        #     data = dnv.curves_in_seawater_with_cathodic_protection[name]
        #     fl = np.round(curve.get_stress(1e7), 2)
        #     fl_data = data["fl"]
        #     err = (fl-fl_data)/fl_data
        #     np.testing.assert_almost_equal(fl, fl_data, decimal=2)
        #     # print(f"{name:<7} | {fl:8.2f} | {fl_data:8.2f} | {err:8.2%}")
        #     table_data.append([name, fl, fl_data, "{:.2%}".format(err)])
        #     Sr = curve.get_stress(N)
        #     if name == df.loc[i, "DNV_category"]:
        #         plt.loglog(N, Sr, "k", lw=2)
        #     else:
        #         plt.loglog(N, Sr, "k", lw=0.5)
        #     plt.text(2e6, curve.get_stress(2e6), "{0:2}".format(name), fontsize=5.5, 
        #               ha='center', va='center', bbox={'fc':'w', 'ec':(0, 0, 0, 0), 'pad':1})
        # plt.grid(which='both')
        # plt.title("S-N curves in seawater with cathodic protection")
        # plt.xlabel("Number of cycles")
        # plt.ylabel("Stress range (MPa)")
        # plt.ylim(10, 1000)
        # plt.xlim(1e4, 1e8)
        # fig.tight_layout()
        
        # # print(table_data)
        # ax_table = plt.subplot2grid((3, 2), (1, 1), rowspan=1, aspect='equal', )
        # ax_table.axis('tight')
        # ax_table.axis('off')
        # plt.title('DNV-RP-C203 endurance fatigue limit classes:')
        # ax_table = plt.table(cellText=table_data, colLabels=table_headers, cellLoc="center", loc='upper left')
        # ax_table.scale(1, 1.2)
        
        # # Plot component hotspot picture:
        # ax_img = plt.subplot2grid((3, 2), (0, 0), rowspan=1, aspect='equal', )
        # ax_img.axis('off')
        # try:
        #     img = mpimg.imread(df.loc[i, "component_no"] + "_" + df.loc[i, "hotspot"] + ".png")
        #     plt.imshow(img)
        # except OSError:
        #     img = mpimg.imread("no-image.png")
        #     plt.imshow(img)
            
        # Find reversals (peaks and valleys), extract cycles and residue (open cycle
        # sequence), process and extract closed cycles from residue. *Raw data.
        reversals, reversals_ix = fatpack.find_reversals(y, k)
        cycles, residue = fatpack.find_rainflow_cycles(reversals)
        processed_residue = fatpack.concatenate_reversals(residue, residue)
        cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
        cycles_total = np.concatenate((cycles, cycles_residue))
        
        # Find the rainflow ranges from the cycles
        S = fatpack.find_rainflow_ranges(y, k)
        
        curve = dnv.DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection(df.loc[i, "DNV_category"])
        fatigue_damage = curve.find_miner_sum(S)
        
        # table_data = []
        # table_data.append(["FATIGUE DAMAGE D", "{:.4f}".format(fatigue_damage)])
        # table_data.append(["Max load", '{:.2f}'.format(y.max())])
        # table_data.append(["Number of cycles", '{:.2e}'.format(len(y))])
        
        # ax_text = plt.subplot2grid((3, 2), (0, 1), rowspan=1, aspect='equal')
        # # ax_text.axis('tight')
        # ax_text.axis('off')
        # ax_text = plt.table(cellText=table_data, cellLoc="left", loc="upper left")
        # ax_text.scale(1, 1.2)
        # plt.title("Fatigue data:")
        # fig.subplots_adjust(top=0.94)
        
        print("FATIGUE DAMAGE D = {:.4f} ".format(fatigue_damage) + "(" + df.loc[i, "component"] + ")")
        
        df.loc[i, "fatigue_damage"] = fatigue_damage
        
        
    
    # return S, fatigue_damage

    # # Find reversals (peaks and valleys), extract cycles and residue (open cycle
    # # sequence), process and extract closed cycles from residue. *Raw data.
    # reversals, reversals_ix = fatpack.find_reversals(y, k=256)
    # cycles, residue = fatpack.find_rainflow_cycles(reversals)
    # processed_residue = fatpack.concatenate_reversals(residue, residue)
    # cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
    # cycles_total = np.concatenate((cycles, cycles_residue))
    
    # # Adding a filter to the raw data y above:
    # ## reversals_rtf, reversals_rtf_ix = fatpack.find_reversals_racetrack_filtered(y, h=20, k=256)
    
    # # Find the rainflow ranges from the cycles
    # S = fatpack.find_rainflow_ranges(y, k)
    


    #%%
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
    """
    tmp = np.fromfile(fname,dtype=float)
    N = int(len(tmp)/3)
    # time, FC, FN
    return tmp[0:N], tmp[N:2*N], tmp[2*N:3*N]

fname = db_location + "\Wavefoil Team Folder\Teknisk utvikling\WF 5910\FEM ANALYSE\RAPPORT\FoilForce_simtime-10800 heading-1 Tp-14 Hs-3 vel-7.out"

time, FC, FN = readwavefoilforces(fname)

foil_load = FN

fatigueDamage(foil_load, k=500, foilmodule="WF5910")

