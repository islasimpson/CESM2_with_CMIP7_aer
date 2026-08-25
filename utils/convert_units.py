import xarray as xr
import numpy as np
import sys

from CASutils import calendar_utils as cal

avog = 6.022e23 # Avogadro's number
re = 6.3712e8 # Radius of the earth in cm

def convert_molecules_to_tg(dat,varname=None):
    """ Convert surface emissions in molecules/cm2/s to Tg

    """
    # Start with moleculre/cm2/s.  Convert from molecules to grams.
    # Divide by Avogadro's number to convert from molecules to moles.
    #Multiply by molcular weight in g/mol to end up with g/cm2/s
    if varname is not None:
        dat = dat[varname]
    else:
        dat = dat
    dat_g = dat.molecular_weight*dat/avog

    # convert from per s to per year
    dat_g_y = dat_g*365.*86400.

    if "altitude" in dat.dims:
        print('you have altitudes')
         # Compute dz for each altitude
        altitude = dat.altitude
        dz = altitude*0
        altitude = np.concatenate(([0],np.array(altitude)))
        dz[0] = (altitude[1]) + (altitude[2]-altitude[1])/2.
        dz[1:len(altitude)-2] = (
                             ((altitude[2:len(altitude)-1] - altitude[1:len(altitude)-2])/2.) +
                             ((altitude[3::] - altitude[2:len(altitude)-1])/2.)
                            )
        dz[len(altitude)-2] = 2*( (altitude[len(altitude)-1] - altitude[len(altitude)-2] ) / 2.) # assuming same dz in going above the top level


        #dz = dat.altitude_int[1:dat.altitude_int.size].values - dat.altitude_int[0:dat.altitude_int.size-1].values
        dz = xr.DataArray(dz, coords=[dat.altitude], dims=['altitude'], name='dz')
        dz = dz*1000.*100. # convert to cm
        dat_g_y = (dat_g_y*dz).sum('altitude')


    # Integrate over space
    dlon = np.deg2rad( (dat.lon[2] - dat.lon[1]))
    dlat = np.deg2rad( (dat.lat[2] - dat.lat[1]))
    area = xr.ones_like(dat.isel(time=0))
    weights = np.cos(np.deg2rad(area.lat))*dlat*dlon*re**2. # area in cm2
    dat_g_y_w = dat_g_y.weighted(weights)
    dattot = dat_g_y_w.sum(("lon","lat"))

    # Convert from grams to terra grams
    dattot = dattot/1e12

    return dattot

def convert_molecules_to_tg_specifywgt(dat,molecular_weight,varname=None):
    """ Convert surface emissions in molecules/cm2/s to Tg

    """
    alldat = dat # alldat also contains weights if needed

    if varname is not None:
        dat = dat[varname]
    else:
        dat = dat
    # Start with moleculre/cm2/s.  Convert from molecules to grams.
    # Divide by Avogadro's number to convert from molecules to moles.
    #Multiply by molcular weight in g/mol to end up with g/cm2/s
    dat_g = molecular_weight*dat/avog

    # convert from per s to per year
    dat_g_y = dat_g*365.*86400.

    if "altitude" in dat.dims:
        print('you have altitudes')
        altitude = dat.altitude
        dz = altitude*0
        altitude = np.concatenate(([0],np.array(altitude)))
        dz[0] = (altitude[1]) + (altitude[2]-altitude[1])/2.
        dz[1:len(altitude)-2] = (
                             ((altitude[2:len(altitude)-1] - altitude[1:len(altitude)-2])/2.) +
                             ((altitude[3::] - altitude[2:len(altitude)-1])/2.)
                            )
        dz[len(altitude)-2] = 2*( (altitude[len(altitude)-1] - altitude[len(altitude)-2] ) / 2.) # assuming same dz in going above the top level




        #dz = dat.altitude_int[1:dat.altitude_int.size].values - dat.altitude_int[0:dat.altitude_int.size-1].values
        dz = xr.DataArray(dz, coords=[dat.altitude], dims=['altitude'], name='dz')
        dz = dz*1000.*100. # convert to cm
        dat_g_y = (dat_g_y*dz).sum('altitude')


    # Integrate over space
    if "ncol" in dat.dims: # using spectral element
        weights = alldat.area*re**2
        dat_g_y_w = dat_g_y.weighted(weights)
        dattot = dat_g_y_w.sum('ncol')
    else:
        dlon = np.deg2rad( (dat.lon[2] - dat.lon[1]))
        dlat = np.deg2rad( (dat.lat[2] - dat.lat[1]))
        area = xr.ones_like(dat.isel(time=0))
        weights = np.cos(np.deg2rad(area.lat))*dlat*dlon*re**2. # area in cm2
        dat_g_y_w = dat_g_y.weighted(weights)
        dattot = dat_g_y_w.sum(("lon","lat"))

    # Convert from grams to terra grams
    dattot = dattot/1e12

    return dattot



