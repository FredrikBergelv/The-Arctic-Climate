#!/usr/bin/env python3
"""
Created on Wed Dec 17 18:14:23 2025

@author: Fredrik Bergelv
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from matplotlib import colors
from matplotlib.gridspec import GridSpec
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
import matplotlib.patches as mpatches
from shapely.geometry import Point
from time import time


def ocean(data, lon360=True):
    """
    Filters an Xarray so only data on ocean remains. 

    Parameters
    ----------
    data : xarray, tuple, list
        The data which you want to filter..
        
    lon360 : Bool, optional
        Is the longitudinal data from 0-360deg or -180-180deg. The default is True.

    Returns
    -------
    data_ocean : xarray
        The filtered data.
    """

    time_start = time()

    # allow tuple/list input
    if not isinstance(data, (tuple, list)):
        data = (data,)
        single = True
    else:
        single = False

    lons = data[0].longitude.values
    lats = data[0].latitude.values

    land_geoms = list(cfeature.LAND.geometries())
    land_mask = np.ones((len(lats), len(lons)), dtype=bool)

    for i, lon in enumerate(lons):
        for j, lat in enumerate(lats):

            lon180 = ((lon + 180) % 360) - 180 if lon360 else lon

            point = Point(lon180, lat)

            for geom in land_geoms:
                if geom.contains(point):
                    land_mask[j, i] = False
                    break

    results = tuple(d.where(land_mask) for d in data)

    elapsed_time = time() - time_start
    print(f"Ocean filter execution time: {elapsed_time/60:.0f}:{elapsed_time%60:.0f} min")

    return results[0] if single else results



def land(data, lon360=True):
    """
    Filters an Xarray so only data on land remains. 

    Parameters
    ----------
    data : xarray, tuple, list
        The data which you want to filter..
        
    lon360 : Bool, optional
        Is the longitudinal data from 0-360deg or -180-180deg. The default is True.

    Returns
    -------
    data_land : xarray
        The filtered data.

    """
    time_start = time()

    if not isinstance(data, (tuple, list)):
        data = (data,)
        single = True
    else:
        single = False

    lons = data[0].longitude.values
    lats = data[0].latitude.values

    ocean_geoms = list(cfeature.OCEAN.geometries())
    ocean_mask = np.ones((len(lats), len(lons)), dtype=bool)

    for i, lon in enumerate(lons):
        for j, lat in enumerate(lats):

            lon180 = ((lon + 180) % 360) - 180 if lon360 else lon

            point = Point(lon180, lat)

            for geom in ocean_geoms:
                if geom.contains(point):
                    ocean_mask[j, i] = False
                    break

    results = tuple(d.where(ocean_mask) for d in data)

    elapsed_time = time() - time_start
    print(f"Land filter execution time: {elapsed_time/60:.0f}:{elapsed_time%60:.0f} min")

    return results[0] if single else results


def xarray(
    data,
    outputdir=None,
    lat_range=None,
    lon_range=None,
    size=1,
    valuescale=20,
    center=None,
    projection="flat",     # "flat", "lambert", "robinson"
    cmap="RdBu_r",
    title="",
    bartitle="",
    isobars=None,          # xarray.DataArray
    isobar_levels=None,
    isobar_color="white",
    wind=None,             # (u_da, v_da)
    wind_step=5,
    wind_scale=400,
    wind_thickness=0.002,
    polar_wind=False,
    mapscale="10m",
    gridlines=True,
    gridlinecolor="white", 
    colorbar=True,
    clim=None,
    show=True,
    ):
     """
    Plot a 2D geophysical field stored in an xarray.DataArray on a map using Cartopy.

    This function supports global and regional map projections, automatic domain
    subsetting, aspect-aware figure sizing, optional isobar contours, and wind
    vector overlays. It is designed for meteorological and geophysical data
    on regular latitude–longitude grids.

    Parameters
    ----------
    data : xarray.DataArray
        2D data field to plot. Must contain latitude and longitude coordinates.
        Coordinate names may vary (e.g. 'lat', 'latitude', 'lon', 'longitude').

    outputdir : str or None, optional
        Directory where the figure will be saved. If the string ends with '.pdf' or 'png',
        it is treated as a full output filename. If None, the figure is not saved.

    lat_range : tuple(float, float) or None, optional
        Latitude range to plot as (lat_min, lat_max). If None, the full latitude
        extent of the data is used. Not allowed with Robinson projection.

    lon_range : tuple(float, float) or None, optional
        Longitude range to plot as (lon_min, lon_max). If None, the full longitude
        extent of the data is used. Not allowed with Robinson projection.

    size : float, optional
        Overall scaling factor for the figure size. Default is 1.

    valuescale : int, optional
        Number of contour levels used in the filled contour plot.

    center : tuple(float, float) or None, optional
        Required for the orthographic projection. Centers the map as (lat,lon).

    projection : {"flat", "lambert", "robinson", "azimuthal", "orthographic"}, optional
        Map projection to use:
        - "flat"        : PlateCarree (no distortion, best for small regions)
        - "lambert"     : Lambert Conformal Conic (best for mid-latitude regions)
        - "azimuthal"   : Azimuthal equidistant projection (best for Arctic)
        - "robinson"    : Robinson projection (best for global view)
        - "orthographic": Orthographic globe view (uses `center` argument)

    cmap : str or matplotlib Colormap, optional
        Colormap used for the filled contours.

    title : str, optional
        Title shown above the plot. If empty, the DataArray name is used.

    bartitle : str, optional
        Label for the colorbar. If empty, the DataArray name is used.

    isobars : xarray.DataArray or None, optional
        2D DataArray containing a scalar field (e.g. pressure) to be drawn as
        contour lines on top of the filled contours.

    isobar_levels : sequence of float or None, optional
        Contour levels for the isobars. Required if `isobars` is provided.
    
    isobar_color  : str, optional
        color of isobar levels, if left empty than "white"

    wind : tuple(xarray.DataArray, xarray.DataArray) or None, optional
        Tuple of (u, v) wind components. Each must be a 2D DataArray on the same
        grid as `data`.

    wind_step : int, optional
        Subsampling step for wind vectors. Larger values produce fewer arrows.

    wind_scale : float, optional
        Scaling factor for wind arrows passed to matplotlib quiver.

    wind_thickness : float, optional
        Thickness for wind arrows passed to matplotlib quiver. Default set to 0.002.

    polar_wind : Bool, optional
        Should wind density decrease towards the pole?

    mapscale    : string, optional
        Scale for borders and coastlines. Default set to "10m". 

    gridlines   : Bool, optional
        True or False if gridlines is wanted

    gridlinecolor   : String, optional
        Color of the gridline. Default set to "white". 

    colorbar   : Bool, optional
        True or False if colorbar is wanted

    clim    : tuple(float, float), optional
        Tuple to set limits

    show    : Bool, optional
        True or False if figure should be shown.

    Raises
    ------
    TypeError
        If `data` is not an xarray.DataArray.

    ValueError
        If Robinson projection is used with regional bounds,
        if isobars are given without levels,
        if orthographic is used without `center`,
        or if `center` is used with another projection.

    Notes
    -----
    - Robinson projection is global-only and does not support regional zooming.
    - For full control over spatial extent and distortion, use "flat" or "lambert".
    - Figure size is automatically adjusted to the latitude/longitude aspect ratio
      for regional plots.

    """

    # -------------------------
    # Checks
    # -------------------------
     if center is not None and projection != "orthographic":
        raise ValueError("`center` can only be used with projection='orthographic'.")
    
     if not isinstance(data, xr.DataArray):
        raise TypeError("data must be an xarray.DataArray")

     if projection == "robinson" and (lat_range or lon_range):
        raise ValueError(
            "Robinson projection is global only. "
            "Use 'flat' or 'lambert' for regional plots."
        )
    
     if projection == "azimuthal" and (lon_range):
       raise ValueError(
           "Azimuthal projection always views all longitudes. "
           "Use 'flat' or 'lambert' for regional plots."
       )
     
     if projection == "azimuthal":
         if lon_range is not None:
             raise ValueError(
                 "Azimuthal Lambert projection does not support lon_range. "
                 "All longitudes are included."
                 )
         if lat_range is not None:
             if max(lat_range) != 90:
                 raise ValueError(
                     "Azimuthal Lambert projection must have lat_range upper limit = 90."
                     )
    
     if "lats" in data.coords:
         lat_name = "lats"
     elif "lat" in data.coords:
         lat_name = "lat"
     else:
         # fallback: search for any coordinate containing "lat"
         lat_name = [c for c in data.coords if "lat" in c.lower()][0]

     if "lons" in data.coords:
         lon_name = "lons"
     elif "lon" in data.coords:
        lon_name = "lon"
     else:
        # fallback: search for any coordinate containing "lon"
        lon_name = [c for c in data.coords if "lon" in c.lower()][0]

     # -------------------------
     # Subset domain
     # -------------------------
     if lat_range:
        data = data.sel({lat_name: slice(*lat_range)})
        if isobars is not None:
            isobars = isobars.sel({lat_name: slice(*lat_range)})
        if wind is not None:
            wind = (
                wind[0].sel({lat_name: slice(*lat_range)}),
                wind[1].sel({lat_name: slice(*lat_range)}),
            )

     # --- Normalize longitudes to [-180, 180] if needed ---
     if data[lon_name].max() > 180:
         data = data.assign_coords(
             {lon_name: (((data[lon_name] + 180) % 360) - 180)}
             ).sortby(lon_name)

         if isobars is not None:
            isobars = isobars.assign_coords(
                {lon_name: (((isobars[lon_name] + 180) % 360) - 180)}
                ).sortby(lon_name)

         if wind is not None:
            wind = (
                wind[0].assign_coords(
                    {lon_name: (((wind[0][lon_name] + 180) % 360) - 180)}
                    ).sortby(lon_name),
                wind[1].assign_coords(
                    {lon_name: (((wind[1][lon_name] + 180) % 360) - 180)}
                    ).sortby(lon_name),
                )

     if lon_range:
         lon_min, lon_max = lon_range

         # Convert user input from 0–360 to -180–180 if needed
         if lon_min > 180:
             lon_min -= 360
         if lon_max > 180:
             lon_max -= 360

         data = data.sel({lon_name: slice(lon_min, lon_max)})

         if isobars is not None:
             isobars = isobars.sel({lon_name: slice(lon_min, lon_max)})

         if wind is not None:
             wind = (
                 wind[0].sel({lon_name: slice(lon_min, lon_max)}),
                 wind[1].sel({lon_name: slice(lon_min, lon_max)}),
             )

     lats = data[lat_name].values
     lons = data[lon_name].values
     south, north = float(lats.min()), float(lats.max())


     # --- Optional cyclic longitude ---
     if projection in ("azimuthal", "orthographic"):
        data_vals, lons_cyclic = add_cyclic_point(data.values, coord=lons)
        # Isobars
        if isobars is not None:
            isobars_vals, _ = add_cyclic_point(isobars.values, coord=lons)
        # Wind
        if wind is not None:
            u_vals, _ = add_cyclic_point(wind[0].values, coord=lons)
            v_vals, _ = add_cyclic_point(wind[1].values, coord=lons)

        # Create 2D meshgrid for plotting
        lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
        west, east = float(lons_cyclic.min()), float(lons_cyclic.max())
        

     else:
         data_vals = data.values
         if isobars is not None:
             isobars_vals = isobars.values
         if wind is not None:
             u_vals = wind[0].values
             v_vals = wind[1].values

         lon2d, lat2d = np.meshgrid(lons, lats)
         west, east = float(lons.min()), float(lons.max())
         
     

    # -------------------------
    # Projection
    # -------------------------
     if projection == "flat":
        proj = ccrs.PlateCarree()
        proj_name = "PlateCarree"

     elif projection == "lambert":
        proj = ccrs.LambertConformal(
            central_longitude=(west + east) / 2,
            central_latitude=(south + north) / 2
        )
        proj_name = "LambertConformal"
        
        
     elif projection == "azimuthal":
         proj = ccrs.AzimuthalEquidistant(
             central_longitude=0,
             central_latitude=90
             )
         proj_name = "AzimuthalEquidistant"
         
     elif projection == "orthographic":
        proj = ccrs.Orthographic(
            central_longitude=center[1],
            central_latitude=center[0],
        )
        proj_name = "Orthographic"


     elif projection == "robinson":
        proj = ccrs.Robinson()
        proj_name = "Robinson"

     else:
        raise ValueError("projection must be 'flat', 'lambert','azimuthal' or 'robinson'")

    # -------------------------
    # Figure size (aspect-aware)
    # -------------------------
     lat_span = max(north - south, 1e-6)
     lon_span = max(east - west, 1e-6)

     fig_width = 7 * size
     fig_height = fig_width * (lat_span / lon_span)
     
     if projection == "lambert":
        fig_height = 6 * size
    
     if projection == "azimuthal":
        fig_height = 5 * size
        fig_width = 6.5 * size


     fig = plt.figure(figsize=(fig_width, fig_height))
     #gs = GridSpec(1, 2, width_ratios=[30, 1], wspace=0.05) 
     if projection == "orthographic":
         gs = GridSpec(1, 2, width_ratios=[40, 1], wspace=0.01)
     else:
         gs = GridSpec(1, 2, width_ratios=[30, 1], wspace=0.05)
 

     ax = fig.add_subplot(gs[0], projection=proj)
     if colorbar:
         cax = fig.add_subplot(gs[1])

        
    # -------------------------
    # Map extent & clipping
    # -------------------------
     if projection not in ("azimuthal", "robinson", "orthographic"):
        ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())

        n = 200
        aoi = mpath.Path(
            np.vstack([
                np.column_stack([np.linspace(west, east, n), np.full(n, north)]),
                np.column_stack([np.full(n, east), np.linspace(north, south, n)]),
                np.column_stack([np.linspace(east, west, n), np.full(n, south)]),
                np.column_stack([np.full(n, west), np.linspace(south, north, n)]),
            ])
        )
        ax.set_boundary(aoi, transform=ccrs.PlateCarree())
        
     elif projection == "azimuthal":
         ax.set_extent([-180, 180, south, 90], ccrs.PlateCarree())
         theta = np.linspace(0, 2*np.pi, 100)
         center, radius = [0.5, 0.5], 0.5
         verts = np.vstack([np.sin(theta), np.cos(theta)]).T
         circle = mpath.Path(verts * radius + center)
         ax.set_boundary(circle, transform=ax.transAxes)
 

     else:
        ax.set_global()
        
         
        

    # -------------------------
    # Colorbar
    # -------------------------
     if clim is not None:
         vmin, vmax = clim
         levels = np.linspace(vmin, vmax, valuescale)
         norm = colors.Normalize(vmin=vmin, vmax=vmax)

     cf = ax.contourf(
        lon2d,
        lat2d,
        data_vals,
        levels=levels if clim else valuescale,
        cmap=cmap,
        norm=norm if clim else None,
        extend="both" if clim else None,
        transform=ccrs.PlateCarree(),
        )

     if isobars is not None:
         cs = ax.contour(
             lon2d,
             lat2d,
             isobars_vals,
             levels=isobar_levels,
             colors=isobar_color,
             linewidths=1,
             transform=ccrs.PlateCarree()
             )
         
       

     if colorbar:
         cb = plt.colorbar(cf, cax=cax)
         cb.set_label(bartitle if bartitle else data.name)
         
     # Move colorbar closer for orthographic
     if projection == "orthographic" and colorbar:
      pos = cax.get_position()
      cax.set_position([
        pos.x0 - 0.15,   # shift left
        pos.y0,
        pos.width,
        pos.height
        ])

     if clim is not None:
        ticks = np.linspace(clim[0], clim[1], 6)
        if colorbar:
            cb.set_ticks(ticks)


    # Adjust position for specific projections
     if projection in ("flat", "robinson") and cax is not None:
        pos = cax.get_position()
        cax.set_position([
            pos.x0,
            pos.y0 + pos.height * 0.1,
            pos.width * 0.8,
            pos.height * 0.8,
        ])

    # -------------------------
    # Isobars
    # -------------------------
     if isobars is not None:
        if isobar_levels is None:
            raise ValueError("isobar_levels must be provided")
    
        ax.clabel(
            cs,
            fmt="%d",          # format of labels (e.g. 1000, 1010)
            fontsize=9,
            inline=True,
            inline_spacing=5)

    # -------------------------
    # Wind
    # -------------------------
     if wind is not None:
        u_da, v_da = wind

        if polar_wind:
            lon_plot = []
            lat_plot = []
            u_plot = []
            v_plot = []

            for j in range(0, lat2d.shape[0], wind_step):

               lat = lat2d[j, 0]
               lon_step = max(1, int(wind_step / np.cos(np.deg2rad(lat))))

               for i in range(0, lon2d.shape[1], lon_step):
                  lon_plot.append(lon2d[j, i])
                  lat_plot.append(lat2d[j, i])
                  u_plot.append(u_vals[j, i])
                  v_plot.append(v_vals[j, i])

            lon_plot = np.array(lon_plot)
            lat_plot = np.array(lat_plot)
            u_plot = np.array(u_plot)
            v_plot = np.array(v_plot)

            ax.quiver(
                lon_plot,
                lat_plot,
                u_plot,
                v_plot,
                transform=ccrs.PlateCarree(),
                scale=wind_scale,
                width=wind_thickness,
                color="black"
                )
        else:
            ax.quiver(
                lon2d[::wind_step, ::wind_step],
                lat2d[::wind_step, ::wind_step],
                u_vals[::wind_step, ::wind_step],
                v_vals[::wind_step, ::wind_step],
                transform=ccrs.PlateCarree(),
                scale=wind_scale,
                width=wind_thickness,
                color="black"
            )


    # -------------------------
    # Features
    # -------------------------
     ax.add_feature(cfeature.COASTLINE.with_scale(mapscale), linewidth=0.8)
     ax.add_feature(cfeature.BORDERS.with_scale(mapscale), linewidth=0.6)

    # -------------------------
    # Gridlines
    # -------------------------
     if gridlines:
         gl = ax.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=0.6,
            color=gridlinecolor,
            alpha=0.7,
            linestyle="--",
            x_inline=False,
            y_inline=False
            )

         gl.left_labels = True
         gl.bottom_labels = True
         gl.right_labels = False
         gl.top_labels = False
         gl.xlabel_style = {"size": 9}
         gl.ylabel_style = {"size": 9}

    # -------------------------
    # Title
    # -------------------------
     ax.set_title(title if title else data.name, fontsize=13)

    # -------------------------
    # Save
    # -------------------------
     if outputdir:
         if outputdir.endswith(".pdf"):
            save_path = outputdir
         elif outputdir.endswith(".png"):
            save_path = outputdir
         else:
            os.makedirs(outputdir, exist_ok=True)
            save_path = os.path.join(outputdir, f"{proj_name}_{data.name}.pdf")

         fig.savefig(save_path, bbox_inches="tight")
         print(f"Saved: {save_path}")

     if show:
        plt.show()


"""
SOME EXAMPLE USAGE 


#%%%%


# Create latitude & longitude
lats = np.linspace(30, 75, 91)     # 30–75°N
lons = np.linspace(-30, 40, 141)   # -30–40°E

lon2d, lat2d = np.meshgrid(lons, lats)

# Fake field (e.g. temperature anomaly)
data = np.sin(np.deg2rad(lat2d)) * np.cos(np.deg2rad(lon2d))

data = xr.DataArray(
    data,
    coords={"lat": lats, "lon": lons},
    dims=("lat", "lon"),
    name="temperature_anomaly",
    attrs={
        "long_name": "Temperature anomaly",
        "units": "K",}
    )


mp.xarray(data)

#%%%%


lats = np.linspace(-90, 90, 180)
lons = np.linspace(-180, 180, 180)

lon2d, lat2d = np.meshgrid(lons, lats)

data = np.sin(np.deg2rad(lat2d)) * np.cos(np.deg2rad(lon2d))



numpy(data,
      projection="flat",
      size=1,
         lats=lats,
         lons=lons)

numpy(data,
      projection="robinson",
      size=1,
         lats=lats,
         lons=lons)

numpy(data,
      projection="lambert",
      size=1,
         lats=lats,
         lons=lons,
         lat_range=(25, 80),
         lon_range=(-40, 40),)

#%%
p_tot = 1000 + 10 * np.sin(np.deg2rad(lat2d)) * 10 * np.cos(np.deg2rad(lon2d))

u_wind = 10 * np.cos(np.deg2rad(lat2d))  
v_wind = 5 * np.sin(np.deg2rad(lon2d))   


numpy(data,
         lats=lats,
         lons=lons,
         outputdir=None,
         lat_range=(25, 80),
         lon_range=(-40, 40),
         size=2,
         projection="lambert",
         cmap="RdBu_r",
         title="Title",
         bartitle="Bar title",
         isobars=p_tot,
         isobar_levels=np.arange(990, 1030, 5),
         wind=(u_wind, v_wind),              # (u_da, v_da)
         wind_step=5,
         wind_scale=300)

"""



