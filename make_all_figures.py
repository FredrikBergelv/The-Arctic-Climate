"""
Created on Sun Feb 23 13:16:09 2026

@author: fredrik
"""

from time import time
import xarray as xr
import mypy.mapplot as mp
import cmocean

time_start = time()
folder     = "Arctic-project-report/Figures"
figsize    = 0.8
isobar_YN  = False


#open the data
data    = xr.open_dataset("data/totdata.nc")
data_tp = xr.open_dataset("data/total_precip_2012_2021.nc")
data_sd = xr.open_dataset("data/snowdepth_2012_2021.nc")

# Select variable
blh     = data["blh"] 
msl     = data["msl"] / 100
tclw    = data["tclw"] 
tisr    = data["tisr"] 
tp      = data_tp["tp"] * 1000
siconc  = data["siconc"] 
sst     = data["sst"] - 273.15
sd      = data_sd["sd"] 
t2m     = data["t2m"] - 273.15
tsr     = data["tsr"] 
skt     = data["tclw"] 


# Group by season
seasonal_blh    = blh.groupby("time.season")
seasonal_msl    = msl.groupby("time.season")
seasonal_tclw   = tclw.groupby("time.season")
seasonal_tisr   = tisr.groupby("time.season")
seasonal_tp     = tp.groupby("time.season")
seasonal_siconc = siconc.groupby("time.season")
seasonal_sst    = sst.groupby("time.season")
seasonal_sd     = sd.groupby("time.season")
seasonal_t2m    = t2m.groupby("time.season")
seasonal_tsr    = tsr.groupby("time.season")
seasonal_skt    = skt.groupby("time.season")



# Loop over seasons
for season in ["DJF", "MAM", "JJA", "SON"]:
    
    # Take the mean of each season
    mean_blh      = seasonal_blh.mean(dim="time").sel(season=season)
    mean_msl      = seasonal_msl.mean(dim="time").sel(season=season)
    mean_tclw     = seasonal_tclw.mean(dim="time").sel(season=season)
    mean_tisr     = seasonal_tisr.mean(dim="time").sel(season=season)
    mean_tp       = seasonal_tp.mean(dim="time").sel(season=season)
    mean_siconc   = seasonal_siconc.mean(dim="time").sel(season=season)
    mean_sst      = seasonal_sst.mean(dim="time").sel(season=season)
    mean_sd       = seasonal_sd.mean(dim="time").sel(season=season)
    mean_t2m      = seasonal_t2m.mean(dim="time").sel(season=season)
    mean_tsr      = seasonal_tsr.mean(dim="time").sel(season=season)
    mean_skt      = seasonal_skt.mean(dim="time").sel(season=season)
    
    #Only show colorbar for "SON", since all use the same
    if season ==  "SON":
        bar_YN = True
    else :
        bar_YN = False
    
    # Boundary layer height
    mp.xarray(
        data=mean_blh,
        lat_range=(90, 60),
        bartitle="Height [m]",
        title=f"Boundary layer height ({season})",
        cmap=cmocean.cm.dense,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "black",
        size=figsize,
        clim=(0,1050),
        colorbar=bar_YN,
        outputdir=f"{folder}/BoundaryLayerHeight_2012_2021_mean_{season}.png",
        show=False
    )
    
    # Mean sea level pressure
    mp.xarray(
        data=mean_msl,
        lat_range=(90, 60),
        bartitle="Pressure [hPa]",
        title=f"Sea Level Pressure ({season})",
        cmap=cmocean.cm.diff,
        projection="azimuthal",
        mapscale="50m",
        isobars=mean_msl,
        isobar_levels=[970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color="red",
        size=figsize,
        clim=( 995, 1030),
        valuescale=35,
        colorbar=bar_YN,
        outputdir=f"{folder}/SeaLevelPressure_2012_2021_mean_{season}.png",
        show=False
    )

    # Total column cloud liquid water 
    mp.xarray(
        data=mean_tclw,
        lat_range=(90, 60),
        bartitle="Water column [kg/m²]",
        title=f"Total column cloud liquid water ({season})",
        cmap=cmocean.cm.deep,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "black",
        size=figsize,
        clim=( 0,0.3),
        colorbar=bar_YN,
        outputdir=f"{folder}/TotalColumnCloudLiquidWater_2012_2021_mean_{season}.png",
        show=False
    )

    # Solar radiation 
    mp.xarray(
        data=mean_tisr,
        lat_range=(90, 60),
        bartitle="Solar radiation [W/m²]",
        title=f"Solar Radiation ({season})",
        cmap=cmocean.cm.solar,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( 0, 5*10**7),
        colorbar=bar_YN,
        outputdir=f"{folder}/SolarRadiation_2012_2021_mean_{season}.png",
        show=False
    )

    # Total precipitation
    mp.xarray(
        data=mean_tp,
        lat_range=(90, 60),
        bartitle="Precipitation [mm]",
        title=f"Total precipitation ({season})",
        cmap=cmocean.cm.rain,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=(0,10),
        colorbar=bar_YN,
        outputdir=f"{folder}/TotalPrecipitation_2012_2021_mean_{season}.png",
        show=False
    )

    # Sea Ice Concentration
    mp.xarray(
        data=mean_siconc,
        lat_range=(90, 60),
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
        colorbar=bar_YN,
        outputdir=f"{folder}/SeaIce_2012_2021_mean_{season}.png",
        show=False
    )

    # Sea surface temperature
    mp.xarray(
        data=mean_sst,
        lat_range=(90, 60),
        bartitle="Temperature [°C]",
        title=f"Sea Surface Temperature ({season})",
        cmap=cmocean.cm.thermal,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( 0, 20),
        colorbar=bar_YN,
        outputdir=f"{folder}/SeaSurfaceTemperature_2012_2021_mean_{season}.png",
        show=False
    )

    # Snow depth
    mp.xarray(
        data=mean_sd,
        lat_range=(90, 60),
        bartitle="Snow depth [m]",
        title=f"Snow depth ({season})",
        cmap=cmocean.cm.ice,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( 0,1),
        colorbar=bar_YN,
        outputdir=f"{folder}/SnowDepth_2012_2021_mean_{season}.png",
        show=False
    )

    # Mean 2m Air Temperature
    mp.xarray(
        data=mean_t2m,
        lat_range=(90, 60),
        bartitle="Temperature [°C]",
        title=f"2m Air Temperature ({season})",
        cmap=cmocean.cm.thermal,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( -30, 30),
        colorbar=bar_YN,
        outputdir=f"{folder}/Temperature_2012_2021_mean_{season}.png",
        show=False
    )

    # Top net solar radiation
    mp.xarray(
        data=mean_tsr,
        lat_range=(90, 60),
        bartitle="Radiation [W/m²]",
        title=f"Top Net Solar Radiation ({season})",
        cmap=cmocean.cm.solar,
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "white",
        size=figsize,
        clim=( 0, 5*10**7),
        colorbar=bar_YN,
        outputdir=f"{folder}/TopNetSolarRadiation_2012_2021_mean_{season}.png",
        show=False
    )
    
    # Total cloud cover
    mp.xarray(
        data=mean_skt,
        lat_range=(90, 60),
        bartitle="Cloud cover [-]",
        title=f"Total cloud cover ({season})",
        cmap="Greys",
        projection="azimuthal",
        mapscale="50m",
        isobars=None if isobar_YN == False else mean_msl,
        isobar_levels=None if isobar_YN == False else [970,980,990,1000,1010,1020,1030,1040,1050],
        isobar_color=None if isobar_YN == False else "red",
        size=figsize,
        clim=( 0,0.5),
        colorbar=bar_YN,
        outputdir=f"{folder}/TotalCloudCover_2012_2021_mean_{season}.png",
        show=False
    )

elapsed_time = time() - time_start
print(f"Execution time: {elapsed_time/60:.0f} minutes and {elapsed_time%60:.0f} seconds")
