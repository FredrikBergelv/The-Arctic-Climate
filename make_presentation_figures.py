"""
Created on Sun Feb 23 13:16:09 2026

@author: fredrik
"""

from time import time
import xarray as xr
import mypy.mapplot as mp
import cmocean

time_start = time()
folder     = "Arctic-presentation/Figures"
figsize    = 0.9
isobar_YN  = False
lats = (90, 55)

#open the data
data    = xr.open_dataset("data/ERA5_(2015-2025).nc")


# Select variable
msl     = data["msl"] / 100     # Mean sea level pressure
tp      = data["tp"] * 1000  # Total precipitation
siconc  = data["siconc"]        # Sea Ice Concentration
sst     = data["sst"] - 273.15  # Sea surface temperature
t2m     = data["t2m"] - 273.15  # 2m temperature


# Group by season
seasonal_msl    = msl.groupby("valid_time.season")
seasonal_siconc = siconc.groupby("valid_time.season")
seasonal_sst    = sst.groupby("valid_time.season")
seasonal_t2m    = t2m.groupby("valid_time.season")


# Here we make seasonal plots
# Loop over seasons
for season in ["DJF", "MAM", "JJA", "SON"]:
    
    # Take the mean of each season
    mean_msl      = seasonal_msl.mean(dim="valid_time").sel(season=season)
    mean_siconc   = seasonal_siconc.mean(dim="valid_time").sel(season=season)
    mean_sst      = seasonal_sst.mean(dim="valid_time").sel(season=season)
    mean_t2m      = seasonal_t2m.mean(dim="valid_time").sel(season=season)
    
    #Only show colorbar for "SON", since all use the same
    if season ==  "JJA":
        bar_YN = True
    else :
        bar_YN = False
        
   # Mean sea level pressure
    mp.xarray(
       data=mean_msl,
       lat_range=lats,
       bartitle="Pressure [hPa]",
       title=f"Sea Level Pressure ({season})",
       cmap=cmocean.cm.diff,
       projection="azimuthal",
       mapscale="50m",
       isobars=mean_msl,
       isobar_levels=[970,980,990,1000,1010,1020,1030,1040,1050],
       isobar_color="red",
       size=figsize,
       clim=(995, 1030),
       valuescale=35,
       colorbar=bar_YN,
       gridlinecolor="white",
       outputdir=f"{folder}/SeaLevelPressure_mean_{season}.pdf",
       show=False
    )


    # Sea Ice Concentration
    mp.xarray(
        data=mean_siconc,
        lat_range=lats,
        bartitle="Ice Cover [-]",
        title=f"Sea Ice Concentration ({season})",
        cmap=cmocean.cm.ice,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "red",
        size=figsize,
        clim=( 0, 1),
        colorbar=True,
        gridlinecolor="white",
        outputdir=f"{folder}/SeaIce_mean_{season}.pdf",
        show=False
    )

    # Mean 2m Air Temperature
    mp.xarray(
        data=mean_t2m,
        lat_range=lats,
        bartitle="Temperature [°C]",
        title=f"2m Air Temperature ({season})",
        cmap=cmocean.cm.balance,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( -30, 30),
        colorbar=True,
        gridlinecolor="white",
        outputdir=f"{folder}/Temperature_mean_{season}.pdf",
        show=False
    )

# Here we make annual mean plots 
annual_tp  = tp.mean(dim="valid_time")
annual_sst = sst.mean(dim="valid_time")
annual_msl = msl.mean(dim="valid_time")


# Total precipitation
mp.xarray(
    data=annual_tp,
    lat_range=lats,
    bartitle="Precipitation [mm/d]",
    title=f"Total precipitation",
    cmap=cmocean.cm.rain,
    projection="azimuthal",
    mapscale="50m",
    isobars=None if isobar_YN == False else mean_msl,
    isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
    isobar_color=None if isobar_YN == False else "white",
    size=figsize,
    clim=(0,10),
    colorbar=True,
    gridlinecolor="white",
    outputdir=f"{folder}/TotalPrecipitation_annual.pdf",
    show=False
    )

# Sea surface temperature
mp.xarray(
    data=annual_sst,
    lat_range=lats,
    bartitle="Temperature [°C]",
    title=f"Sea Surface Temperature",
    cmap=cmocean.cm.thermal,
    projection="azimuthal",
    mapscale="50m",
    isobars=None if isobar_YN == False else mean_msl,
    isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
    isobar_color=None if isobar_YN == False else "white",
    size=figsize,
    clim=(0, 10),
    colorbar=True,
    gridlinecolor="white",
    outputdir=f"{folder}/SeaSurfaceTemperature_annual.pdf",
    show=False
    )


    
    # Mean sea level pressure
mp.xarray(
        data=mean_msl,
        lat_range=lats,
        bartitle="Pressure [hPa]",
        title=f"Sea Level Pressure ",
        cmap=cmocean.cm.diff,
        projection="azimuthal",
        mapscale="50m",
        isobars=mean_msl,
        isobar_levels=[970,980,990,1000,1005,1010,1015,1020,1030,1040,1050],
        isobar_color="red",
        size=figsize,
        clim=( 995, 1030),
        valuescale=35,
        colorbar=True,
        gridlinecolor="white",
        outputdir=f"{folder}/SeaLevelPressure_annual.pdf",
        show=False
    )


u = data["u10"]
v = data["v10"]

# seasonal means
u_mean = u.mean("valid_time")
v_mean = v.mean("valid_time")

speed = (u_mean**2 + v_mean**2)**0.5

u_ocean, v_ocean = mp.ocean((u_mean, v_mean))

mp.xarray(
        data=speed,
        center=(81,-10),
        bartitle="Speed [m/s]",
        title=f"Sea Surface Winds",
        cmap=cmocean.cm.tempo,
        projection="orthographic",
        mapscale="110m",
        size=figsize,
        clim=(0, 15),
        colorbar=True,
        gridlines=False,
        wind=(u_ocean, v_ocean), 
        wind_step=20, 
        wind_scale=45, 
        wind_thickness=0.005, 
        polar_wind=True,
        outputdir=f"{folder}/SurfaceWind_annual.pdf",
        show=False
    )

elapsed_time = time() - time_start
print(f"Execution time: {elapsed_time/60:.0f} minutes and {elapsed_time%60:.0f} seconds")
