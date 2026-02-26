"""
Created on Sun Feb 23 13:16:09 2026

@author: fredrik
"""
"""
Auto-generate LaTeX figure blocks
Matches current plotting script
"""
"""
Created on Thu Feb 26 18:22:03 2026

@author: fredrik
"""


"""
Auto-generate LaTeX figure blocks
and save to figures.tex
"""

output_file = "Arctic-project-report/Textfiles/2.Figures.tex"

# --- Seasonal variables ---
seasonal_variables = {
    "BoundaryLayerHeight": "Seasonal mean boundary layer height (m)",
    "SeaLevelPressure": "Seasonal mean sea level pressure (hPa)",
    "SeaIce": "Seasonal mean sea ice concentration (-)",
    "Temperature": "Seasonal mean 2m air temperature (°C)",
}

seasons = ["DJF", "MAM", "JJA", "SON"]

with open(output_file, "w", encoding="utf-8") as f:

    # --- Seasonal figures ---
    for var, caption_text in seasonal_variables.items():
        
        f.write("\\begin{figure}[H]\n")
        
        for i, season in enumerate(seasons):
            f.write("    \\begin{subfigure}[b]{0.49\\textwidth}\n")
            
            # Alignment: right, left, right, left
            if i % 2 == 0:
                f.write("        \\raggedleft\n")
            else:
                f.write("        \\raggedright\n")
            
            f.write(
                f"        \\includegraphics[height=0.23\\textheight,keepaspectratio]"
                f"{{Figures/{var}_2012_2021_mean_{season}.png}}\n"
            )
            f.write(f"        \\caption{{{season}}}\n")
            f.write(f"        \\label{{fig:{var}_2012_2021_mean_{season}}}\n")
            f.write("    \\end{subfigure}\n")
            
            if i % 2 == 0:
                f.write("    \\hfill\n")
            else:
                f.write("    \\\\[0.6em]\n")
        
        f.write(
            f"    \\caption{{{caption_text} for 2012--2021 for DJF, MAM, JJA, and SON.}}\n"
        )
        f.write(f"    \\label{{fig:{var}_2012_2021_mean}}\n")
        f.write("\\end{figure}\n\n\n")


    # --- Annual mean block ---
    f.write("\\begin{figure}[H]\n")
    f.write("    \\centering\n")

    f.write("    \\begin{subfigure}[b]{0.49\\textwidth}\n")
    f.write("        \\centering\n")
    f.write(
        "        \\includegraphics[height=0.23\\textheight,keepaspectratio]"
        "{Figures/TotalPrecipitation_2012_2021_annual.png}\n"
    )
    f.write("        \\caption{Total Precipitation}\n")
    f.write("        \\label{fig:TotalPrecipitation_2012_2021_annual}\n")
    f.write("    \\end{subfigure}\n")
    f.write("    \\hfill\n")

    f.write("    \\begin{subfigure}[b]{0.49\\textwidth}\n")
    f.write("        \\centering\n")
    f.write(
        "        \\includegraphics[height=0.23\\textheight,keepaspectratio]"
        "{Figures/SeaSurfaceTemperature_2012_2021_annual.png}\n"
    )
    f.write("        \\caption{Sea Surface Temperature}\n")
    f.write("        \\label{fig:SeaSurfaceTemperature_2012_2021_annual}\n")
    f.write("    \\end{subfigure}\n")

    f.write(
        "    \\caption{Annual mean total precipitation and sea surface temperature for 2012--2021.}\n"
    )
    f.write("    \\label{fig:annual_means}\n")
    f.write("\\end{figure}\n\n")

print(f"LaTeX file saved as: {output_file}")