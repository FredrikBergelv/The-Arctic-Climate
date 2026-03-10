"""
Created on Sun Feb 22 19:29:09 2026

@author: fredrik
"""
import xarray as xr

atm_files = [
    "data/ERA5.nc",
    "data/ERA5_precip.nc",
    "data/ERA5_seaice.nc",
]

atm = xr.open_mfdataset(
    atm_files,
    combine="by_coords",
    chunks="auto"
)

atm.to_netcdf("data/ERA52.nc")