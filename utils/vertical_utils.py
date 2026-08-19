import xarray as xr
import numpy as np


def vertically_integrate(dat):
    """ Convert vertically distributed emissions in molecules/cm3/s to molecules/cm2 """
    altitude = dat.altitude.values
    dz = altitude * 0 # arrat for dz values
    altitude = np.concatenate(([0],altitude))

    # Compute dz for each altitude
    dz[0] = (altitude[1]) + (altitude[2]-altitude[1])/2.
    dz[1:len(altitude)-2] = (
                             ((altitude[2:len(altitude)-1] - altitude[1:len(altitude)-2])/2.) + 
                             ((altitude[3::] - altitude[2:len(altitude)-1])/2.)
                            )
    dz[len(altitude)-2] = 2*( (altitude[len(altitude)-1] - altitude[len(altitude)-2] ) / 2.) # assuming same dz in going above the top level

    # Convert dz from km to cm
    dz_cm = dz*1e5
    dz_cm = xr.DataArray(dz_cm, coords=[dat.altitude], dims=['altitude'])

    # Vertically integrate the emissions
    dat_column = (dat*dz_cm).sum('altitude')
    return dat_column
    
def vertically_distribute_as_cmip6(dat, altitude):
    """ Vertically distribut column integrated emissions in molecules/cm2 as was done for CMIP6
        Spread evenly over a 200m (2e4cm) layer from indices 3 to 6
    """
    dat_vertical = dat.expand_dims(altitude=altitude).transpose("time","altitude","lat","lon")*0
    dat_vertical[:,3:7,:,:] = dat / 2e4
    return dat_vertical   
