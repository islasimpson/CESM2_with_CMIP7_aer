import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from math import nan
import pandas as pd
from matplotlib.colors import BoundaryNorm

from CASutils import mapplot_utils as mymaps
from CASutils import averaging_utils as avg
from CASutils import plotposition_utils as plotpos
from CASutils import calendar_utils as cal
from CASutils import colormap_utils as mycolors
from CASutils import averaging_utils as avg
from CASutils import colorbar_utils as cbars
import cartopy.feature as cfeature
import cartopy.crs as ccrs

import spread_emissions_func as spread
import importlib
importlib.reload(spread)

def compute_edges(coord):
    coord = np.array(coord)
    midpoints = (coord[:-1] + coord[1:]) / 2
    edges = np.empty(len(coord) + 1)
    edges[1:-1] = midpoints
    edges[0] = coord[0] - (midpoints[0] - coord[0])
    edges[-1] = coord[-1] + (coord[-1] - midpoints[-1])
    return edges

def plot_map(fig, dat, ci, cmin, cmax, titlestr, x1, x2, y1, y2):
    ax = fig.add_axes([x1, y1, (x2-x1), (y2-y1)], projection = ccrs.PlateCarree())
    nlevs = (cmax - cmin)/ci + 1
    clevs = np.arange(cmin, cmax+ci, ci)
    mymap = mycolors.blue2red_cmap(nlevs)
    norm = BoundaryNorm(clevs, ncolors=mymap.N, clip=True)

    lon_edges = compute_edges(dat.lon)
    lat_edges = compute_edges(dat.lat)

    ax.pcolormesh(lon_edges, lat_edges, dat, cmap=mymap, norm=norm)
    ax.add_feature(cfeature.COASTLINE, zorder=100)
    ax.set_title(titlestr)
    return ax

def plot_map_limits(dat, ci, cmin, cmax, titlestr, x1, x2, y1, y2, xlim1, xlim2, ylim1, ylim2):
    ax = fig.add_axes([x1, y1, (x2-x1), (y2-y1)], projection = ccrs.PlateCarree())
    nlevs = (cmax - cmin)/ci + 1
    clevs = np.arange(cmin, cmax+ci, ci)
    mymap = mycolors.blue2red_cmap(nlevs)
    norm = BoundaryNorm(clevs, ncolors=mymap.N, clip=True)

    lon_edges = compute_edges(dat.lon)
    lat_edges = compute_edges(dat.lat)

    ax.pcolormesh(lon_edges, lat_edges, dat, cmap=mymap, norm=norm)
    ax.add_feature(cfeature.COASTLINE, zorder=100)
    ax.set_title(titlestr)
    ax.set_extent([xlim1, xlim2, ylim1, ylim2], crs = ccrs.PlateCarree())
    return ax
