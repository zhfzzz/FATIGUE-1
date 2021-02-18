# -*- coding: utf-8 -*-
import fatpack
import numpy as np
import matplotlib.pyplot as plt

curves_in_air = dict(
    reference = "DNVGL-RP-C203 - Edition April 2016, Table 2-1 S-N curves in air",
    B1= dict(m1=4.0, loga1=15.117, m2=5, Nd=1e7, loga2=17.146, fl=106.97),
    B2= dict(m1=4.0, loga1=14.885, m2=5, Nd=1e7, loga2=16.856, fl= 93.59),
    C = dict(m1=3.0, loga1=12.592, m2=5, Nd=1e7, loga2=16.320, fl= 73.10),
    C1= dict(m1=3.0, loga1=12.449, m2=5, Nd=1e7, loga2=16.081, fl= 65.50),
    C2= dict(m1=3.0, loga1=12.301, m2=5, Nd=1e7, loga2=15.835, fl= 58.48),
    D = dict(m1=3.0, loga1=12.164, m2=5, Nd=1e7, loga2=15.606, fl= 52.63),
    E = dict(m1=3.0, loga1=12.010, m2=5, Nd=1e7, loga2=15.350, fl= 46.78),
    F = dict(m1=3.0, loga1=11.855, m2=5, Nd=1e7, loga2=15.091, fl= 41.52),
    F1= dict(m1=3.0, loga1=11.699, m2=5, Nd=1e7, loga2=14.832, fl= 36.84),
    F3= dict(m1=3.0, loga1=11.546, m2=5, Nd=1e7, loga2=14.576, fl= 32.75),
    G = dict(m1=3.0, loga1=11.398, m2=5, Nd=1e7, loga2=14.330, fl= 29.24),
    W1= dict(m1=3.0, loga1=11.261, m2=5, Nd=1e7, loga2=14.101, fl= 26.32),
    W2= dict(m1=3.0, loga1=11.107, m2=5, Nd=1e7, loga2=13.845, fl= 23.39),
    W3= dict(m1=3.0, loga1=10.970, m2=5, Nd=1e7, loga2=13.617, fl= 21.05),
)

curves_in_seawater_with_cathodic_protection = dict(
    reference = "DNVGL-RP-C203 - Edition April 2016, Table 2-2 S-N curves in seawater with cathodic protection",
    B1= dict(m1=4.0, loga1=14.917, m2=5, Nd=1e6, loga2=17.146, fl=106.97),
    B2= dict(m1=4.0, loga1=14.685, m2=5, Nd=1e6, loga2=16.856, fl= 93.59),
    C = dict(m1=3.0, loga1=12.192, m2=5, Nd=1e6, loga2=16.320, fl= 73.10),
    C1= dict(m1=3.0, loga1=12.049, m2=5, Nd=1e6, loga2=16.081, fl= 65.50),
    C2= dict(m1=3.0, loga1=11.901, m2=5, Nd=1e6, loga2=15.835, fl= 58.48),
    D = dict(m1=3.0, loga1=11.764, m2=5, Nd=1e6, loga2=15.606, fl= 52.63),
    E = dict(m1=3.0, loga1=11.610, m2=5, Nd=1e6, loga2=15.350, fl= 46.78),
    F = dict(m1=3.0, loga1=11.455, m2=5, Nd=1e6, loga2=15.091, fl= 41.52),
    F1= dict(m1=3.0, loga1=11.299, m2=5, Nd=1e6, loga2=14.832, fl= 36.84),
    F3= dict(m1=3.0, loga1=11.146, m2=5, Nd=1e6, loga2=14.576, fl= 32.75),
    G = dict(m1=3.0, loga1=10.998, m2=5, Nd=1e6, loga2=14.330, fl= 29.24),
    W1= dict(m1=3.0, loga1=10.861, m2=5, Nd=1e6, loga2=14.101, fl= 26.32),
    W2= dict(m1=3.0, loga1=10.707, m2=5, Nd=1e6, loga2=13.845, fl= 23.39),
    W3= dict(m1=3.0, loga1=10.570, m2=5, Nd=1e6, loga2=13.617, fl= 21.05),
)

curves_in_seawater_for_free_corrosion = dict(
    reference = "DNVGL-RP-C203 - Edition April 2016, Table 2-3 S-N curves in seawater for free corrosion",
    B1= dict(m=3.0, loga=12.436),
    B2= dict(m=3.0, loga=12.262),
    C = dict(m=3.0, loga=12.115),
    C1= dict(m=3.0, loga=11.972),
    C2= dict(m=3.0, loga=11.824),
    D = dict(m=3.0, loga=11.687),
    E = dict(m=3.0, loga=11.533),
    F = dict(m=3.0, loga=11.378),
    F1= dict(m=3.0, loga=11.222),
    F3= dict(m=3.0, loga=11.068),
    G = dict(m=3.0, loga=10.921),
    W1= dict(m=3.0, loga=10.784),
    W2= dict(m=3.0, loga=10.630),
    W3= dict(m=3.0, loga=10.493),
)

curve_bolts = dict(
    reference = "DNVGL-RP-C203 - Edition April 2016, 2.9.3 Bolts in shear loading",
    BOLT= dict(m=5.0, loga=16.301),
    )


class DNVGL_EnduranceCurve:
    """Return a DNVGL C203 endurance curve.
    
    Use the following methods to access endurance curves 
    for different structural types and in different environments
        - DNVGL_EnduranceCurve.in_air
        - DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection
        - DNVGL_EnduranceCurve.in_seawater_for_free_corrosion
        
    """
    names = [c for c in curves_in_air.keys() if c != "reference"]
    @staticmethod
    def in_air(name):
        """Returns a DNVGL endurance curve (SN curve)
        
        This method returns an endurance curve in air according to 
        table 2-1 in DNVGL RP-C203.
        
        Arguments
        ---------
        name : str
            Name of the endurance curve.
            
        Returns
        -------
        fatpack.BiLinearEnduranceCurve
            Endurance curve corresponding to `name` in DNVGL RP-C203
            
        Example
        -------
        >>>curve = DNVGL_EnduranceCurve.in_air("D")
        >>>N = curve.get_endurance(90.0)
        
        """
        
        data = curves_in_air[name]
        curve = fatpack.BiLinearEnduranceCurve(1.0)
        curve.Nc = 10 ** data["loga1"]
        curve.Nd = data["Nd"]
        curve.m1 = data["m1"]
        curve.m2 = data["m2"]
        curve.reference = curves_in_air["reference"]
        return curve
    
    @staticmethod
    def in_seawater_with_cathodic_protection(name):
        """Returns a DNVGL endurance curve (SN curve)
        
        This method returns an endurance curve in seawater with 
        cathodic protection according to table 2-2 in DNVGL RP-C203.
        
        Arguments
        ---------
        name : str
            Name of the endurance curve.
            
        Returns
        -------
        fatpack.BiLinearEnduranceCurve
            Endurance curve corresponding to `name` in DNVGL RP-C203
            
        Example
        -------
        >>>curve = DNVGL_EnduranceCurve.in_seawater_with_cathodic_protection("D")
        >>>N = curve.get_endurance(90.0)
        
        """
        data = curves_in_seawater_with_cathodic_protection[name]
        curve = fatpack.BiLinearEnduranceCurve(1.0)
        curve.Nc = 10 ** data["loga1"]
        curve.Nd = data["Nd"]
        curve.m1 = data["m1"]
        curve.m2 = data["m2"]
        ref = curves_in_seawater_with_cathodic_protection["reference"]
        curve.reference = ref
        return curve
    
    @staticmethod
    def in_seawater_for_free_corrosion(name):
        """Returns a DNVGL endurance curve (SN curve)
        
        This method returns an endurance curve in seawater for 
        free corrosion according to table 2-4 in DNVGL RP-C203.
        
        Arguments
        ---------
        name : str
            Name of the endurance curve.
            
        Returns
        -------
        fatpack.LinearEnduranceCurve
            Endurance curve corresponding to `name` in DNVGL RP-C203
            
        Example
        -------
        >>>curve = DNVGL_EnduranceCurve.in_seawater_for_free_corrosion("D")
        >>>N = curve.get_endurance(90.0)
        
        """
        data = curves_in_seawater_for_free_corrosion[name]
        curve = fatpack.LinearEnduranceCurve(1.0)
        curve.Nc = 10 ** data["loga"]
        curve.m = data["m"]
        ref = curves_in_seawater_for_free_corrosion["reference"]
        curve.reference = ref
        return curve    


