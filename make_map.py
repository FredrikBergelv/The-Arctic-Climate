import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

plt.close("all")

# Arctic Circle latitude
arctic_circle_lat = 66.5622

# Create figure and projection
fig = plt.figure(figsize=(6, 6))
ax = plt.axes(projection=ccrs.NorthPolarStereo())

# Land and ocean

ax.add_feature(cfeature.LAND, facecolor="beige", alpha=1)
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.COASTLINE.with_scale("50m"), edgecolor='gray')

# Draw Arctic Circle
lons = np.linspace(0, 360, 1000)
lats = np.full_like(lons, arctic_circle_lat)
ax.plot(lons, lats, transform=ccrs.PlateCarree(),
        color='red', linewidth=2, linestyle='--')

# Map extent
ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())

# Gridlines
gl = ax.gridlines(draw_labels=False, linewidth=0.5, color='black', alpha=0.5, linestyle='--')

# --- Locations from text with approximate lat/lon ---
locations = {
    #"Arctic Ocean": (90, 0),
    "Greenland Sea": (75, -10),
    "Labrador Sea": (61, -55),
    "Baffin Bay": (70, -65),
    "Bering Strait": (66.5, -168),
    "Canadian Archipelago": (75, -100),
    "Barents Sea": (75, 40),
    "Fram Strait": (79, -10),
    "Beaufort Sea": (73, -145),
    "Kara Sea": (75, 70),
    "Nordenskiöld Sea": (75, 125),
    "East Siberian Sea": (72, 170),
    "Norwegian Sea": (68, 5),
    }

# Plot blue dots and names
for name, (lat, lon) in locations.items():
    print(name)
    ax.plot(lon, lat, 'o', color='blue', markersize=5, transform=ccrs.PlateCarree())

    if name == "Bering Strait":
        ax.text(lon, lat+2.4, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
    
    elif name == "Greenland Sea":
        ax.text(lon, lat-3, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
  
    elif name == "Barents Sea":
        ax.text(lon, lat-1, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
    
    elif name == "Arctic Ocean":
        ax.text(lon, lat-3, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
        
    elif name == "Norwegian Sea":
         ax.text(lon, lat-2.2, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
    
    elif name == "Nordenskiöld Sea":
         ax.text(lon+38, lat+5, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
  
    elif name == "Kara Sea":
       ax.text(lon, lat+2, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
    
    elif name == "East Siberian Sea":
       ax.text(lon-2, lat, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
     
       
    else:
        ax.text(lon, lat+1, name, color='darkblue', fontsize=16, transform=ccrs.PlateCarree())
    

# Title
plt.title("Map of the Arctic", fontsize=16)
plt.savefig("Arctic-project-report/Figures/map.png", dpi=400)
plt.show()