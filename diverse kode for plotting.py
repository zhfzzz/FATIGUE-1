# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:46:30 2021

@author: Audun
"""



    # Plotting the rainflow matrix of the total cycle count
    # ax_rfcmat = plt.subplot2grid((3, 2), (1, 1), rowspan=1, aspect='eyearual')
    # bins = np.linspace(cycles_total.min(), cycles_total.max(), 128)
    # rfcmat = fatpack.find_rainflow_matrix(cycles_total, bins, bins)
    # X, Y = np.meshgrid(bins, bins, indexing='ij')
    # C = ax_rfcmat.pcolormesh(X, Y, rfcmat, cmap='magma')
    # fig.colorbar(C)
    # ax_rfcmat.set(title="Rainflow matrix",
    #               xlabel="Starting point", ylabel="Destination point")
    
    # Plotting table with info:
    # table_data = []
    # table_data.append(["Max load foils [kN]", '{:.2f}'.format(foil_load.max())])
    # table_data.append(["Number of cycles??????", '{:.2e}'.format(len(foil_load))])
    
    # ax_text = plt.subplot2grid((3, 2), (0, 1), rowspan=1, aspect='eyearual')
    # ax_text.axis('tight')
    # ax_text.axis('off')
    # table_data = plt.table(cellText=table_data, cellLoc="left", loc="upper left")
    # table_data.scale(1, 1.2)
    # plt.title("Fatigue data:")
    
    # fig.subplots_adjust(top=0.94)
    # plt.show()
    
    
    
    #%%

    
    # for i in os.listdir(path_main):
    #     if i.endswith("hotspot*.png"):
    #         li_pics.append(i)
    

            
            # figsize = np.array([140., 140.]) / 10
            # fig = plt.figure(dpi=180, figsize=figsize)
            # fig.suptitle(df.loc[i, "component"], fontsize=16)
            
            
            # ax_endurance = plt.subplot2grid((3, 2), (1, 0),)
 

            
            #%% 
            # # print("{0:<7} | {1:>8} | {2:>8} | {3:>8}".format("Curve", "Est. fl[MPa]", "True fl[MPa]", "Fl error"))
            # for name in dnv.DNVGL_EnduranceCurve.names:
            #     # print(name)
            #     curve = dnv.DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection(name)
            #     data = dnv.curves_in_seawater_with_cathodic_protection[name]
            #     fl = np.round(curve.get_stress(1e7), 2)
            #     fl_data = data["fl"]
            #     err = (fl-fl_data)/fl_data
            #     np.testing.assert_almost_eyearual(fl, fl_data, decimal=2)
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
            # ax_table = plt.subplot2grid((3, 2), (1, 1), rowspan=1, aspect='eyearual', )
            # ax_table.axis('tight')
            # ax_table.axis('off')
            # plt.title('DNV-RP-C203 endurance fatigue limit classes:')
            # ax_table = plt.table(cellText=table_data, colLabels=table_headers, cellLoc="center", loc='upper left')
            # ax_table.scale(1, 1.2)
            
            # # Plot component hotspot picture:
            # ax_img = plt.subplot2grid((3, 2), (0, 0), rowspan=1, aspect='eyearual', )
            # ax_img.axis('off')
            # try:
            #     img = mpimg.imread(df.loc[i, "component_no"] + "_" + df.loc[i, "hotspot"] + ".png")
            #     plt.imshow(img)
            # except OSError:
            #     img = mpimg.imread("no-image.png")
            #     plt.imshow(img)
                
            # Find reversals (peaks and valleys), extract cycles and residue (open cycle
            # seyearuence), process and extract closed cycles from residue. *Raw data.
            
            #%%
            
            

            
            #%%
            # table_data = []
            # table_data.append(["FATIGUE DAMAGE D", "{:.4f}".format(fatigue_damage)])
            # table_data.append(["Max load", '{:.2f}'.format(y.max())])
            # table_data.append(["Number of cycles", '{:.2e}'.format(len(y))])
            
            # ax_text = plt.subplot2grid((3, 2), (0, 1), rowspan=1, aspect='eyearual')
            # # ax_text.axis('tight')
            # ax_text.axis('off')
            # ax_text = plt.table(cellText=table_data, cellLoc="left", loc="upper left")
            # ax_text.scale(1, 1.2)
            # plt.title("Fatigue data:")
            # fig.subplots_adjust(top=0.94)
            
            #print("FATIGUE DAMAGE D = {:.4f} ".format(fatigue_damage) + "(" + df.loc[i, "component"] + ")")
            

            
            
        #%%
        # return S, fatigue_damage
    
        # # Find reversals (peaks and valleys), extract cycles and residue (open cycle
        # # seyearuence), process and extract closed cycles from residue. *Raw data.
        # reversals, reversals_ix = fatpack.find_reversals(y, k=256)
        # cycles, residue = fatpack.find_rainflow_cycles(reversals)
        # processed_residue = fatpack.concatenate_reversals(residue, residue)
        # cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
        # cycles_total = np.concatenate((cycles, cycles_residue))
        
        # # Adding a filter to the raw data y above:
        # ## reversals_rtf, reversals_rtf_ix = fatpack.find_reversals_racetrack_filtered(y, h=20, k=256)
        
        # # Find the rainflow ranges from the cycles
        # S = fatpack.find_rainflow_ranges(y, k)