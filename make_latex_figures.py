"""
Created on Sun Feb 23 13:16:09 2026

@author: fredrik
"""
# Script to auto-generate LaTeX seasonal figure blocks


###############################################################


variables = {
    "BoundaryLayerHeight": "Seasonal mean boundary layer height (m)",
    "SeaLevelPressure": "Seasonal mean sea level pressure (hPa)",
    "TotalColumnCloudLiquidWater": "Seasonal mean total column cloud liquid water (kg m$^{-2}$)",
    "SolarRadiation": "Seasonal mean incoming solar radiation (W m$^{-2}$)",
    "TotalPrecipitation": "Seasonal monthly mean total precipitation (mm)",
    "SeaIce": "Seasonal mean sea ice concentration (-)",
    "SeaSurfaceTemperature": "Seasonal mean sea surface temperature (°C)",
    "SnowDepth": "Seasonal mean monthly snow depth (m)",
    "Temperature": "Seasonal mean 2m air temperature (°C)",
    "TopNetSolarRadiation": "Seasonal mean top net solar radiation (W m$^{-2}$)",
    "TotalCloudCover": "Seasonal mean total cloud cover (-)"
}

seasons = ["DJF", "MAM", "JJA", "SON"]

for var, caption_text in variables.items():
    
    print(r"\begin{figure}[H]")
    print(r"    \centering")
    
    for i, season in enumerate(seasons):
        print(rf"    \begin{{subfigure}}[b]{{0.49\textwidth}}")
        
        # (a) and (c) -> right aligned
        if i % 2 == 0:
            print(r"        \raggedleft")
        # (b) and (d) -> left aligned
        else:
            print(r"        \raggedright")
        
        print(rf"        \includegraphics[height=0.22\textheight,keepaspectratio]{{Figures/{var}_2012_2021_mean_{season}.png}}")
        print(rf"        \caption{{{season}}}")
        print(rf"        \label{{fig:{var}_2012_2021_mean_{season}}}")
        print(r"    \end{subfigure}")
        
        # Layout: two per row
        if i % 2 == 0:
            print(r"    \hfill")
        else:
            print(r"    \\[0.5em]")
    
    print(rf"    \caption{{{caption_text} for 2012--2021 for DJF, MAM, JJA, and SON. }}")
    print(rf"    \label{{fig:{var}_2012_2021_mean}}")
    print(r"\end{figure}")
    print("\n\n")
    
    
    
    #########################################################
    
    
    
    
variables = {
    "BoundaryLayerHeight": "Seasonal mean boundary layer height (m)",
    "SeaLevelPressure": "Seasonal mean sea level pressure (hPa)",
    "TotalColumnCloudLiquidWater": "Seasonal mean total column cloud liquid water (kg m$^{-2}$)",
    "SolarRadiation": "Seasonal mean incoming solar radiation (W m$^{-2}$)",
    "TotalPrecipitation": "Seasonal mean total precipitation (kg m$^{-2}$)",
    "SeaIce": "Seasonal mean sea ice concentration",
    "SeaSurfaceTemperature": "Seasonal mean sea surface temperature (°C)",
    "SnowDepth": "Seasonal mean snow depth (m)",
    "Temperature": "Seasonal mean 2m air temperature (°C)",
    "TopNetSolarRadiation": "Seasonal mean top net solar radiation (W m$^{-2}$)",
    "TotalCloudCover": "Seasonal mean total cloud cover"
}

seasons = ["DJF", "MAM", "JJA", "SON"]

"""
for var, caption_text in variables.items():
    
    print(r"\begin{figure}[H]")
    print(r"    \centering")
    
    for i, season in enumerate(seasons):
        print(rf"    \begin{{subfigure}}[b]{{0.24\textwidth}}")
        print(r"        \centering")
        print(rf"        \includegraphics[height=0.125\textheight,keepaspectratio]{{Figures/{var}_2012_2021_mean_{season}.png}}")
        print(rf"        \caption{{{season}}}")
        print(rf"        \label{{fig:{var}_2012_2021_mean_{season}}}")
        print(r"    \end{subfigure}")
        
        if i < 3:
            print(r"    \hfill")
    
    print(rf"    \caption{{{caption_text} for 2012–2021 for DJF, MAM, JJA, and SON.}}")
    print(rf"    \label{{fig:{var}_2012_2021_mean}}")
    print(r"\end{figure}")
    print("\n\n")
"""