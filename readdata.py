"""
Created on Sun Feb 22 19:29:09 2026

@author: fredrik
"""
import xarray as xr

atm_files = [
    "data/2012.nc",
    "data/2013.nc",
    "data/2014.nc",
    "data/2015.nc",
    "data/2016.nc",
    "data/2017.nc",
    "data/2018.nc",
    "data/2019.nc",
    "data/2020.nc",
    "data/2021.nc",
    "snowdepth_2012_2021.nc",
    "total_precip_2012_2021.nc"
]

atm = xr.open_mfdataset(
    atm_files,
    combine="by_coords",
    chunks="auto"
)

atm.to_netcdf("data/totdata.nc")