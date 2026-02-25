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
    


    mp.xarray(
    data=mean_tp,
    lat_range=(90, 60),
    bartitle="Precipitation [mm]",
    title=f"Total precipitation ({season})",
    cmap=cmocean.cm.rain,
    projection="azimuthal",
    mapscale="50m",
    isobars=None if not isobar_YN else mean_msl,
    isobar_levels=None if not isobar_YN else [970,980,990,1000,1010,1020,1030,1040,1050],
    isobar_color=None if not isobar_YN else "white",
    size=figsize,
    clim=(0, 15),
    colorbar=isobar_YN,
    outputdir=f"{folder}/TotalPrecipitation_2012_2021_mean_{season}.png",
    show=False
    )

elapsed_time = time() - time_start
print(f"Execution time: {elapsed_time/60:.0f} minutes and {elapsed_time%60:.0f} seconds")
