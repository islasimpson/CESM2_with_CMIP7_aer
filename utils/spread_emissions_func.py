import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def spread_negative_emissions(dat,ilon,ilat):
    """Spread out negative emissions to the nearest grid pointsi
       dat = a 2D array of (nlat,nlon) containing the emissions
       ilon = the longitude index of the current negative grid point to be spread.
       ilat = the latitude index of the current negative grid point to be spread.
    """
    datnew = dat.copy(deep=True) # array that will have the emissions spread out
    deficit = np.abs(dat.isel(lon=ilon, lat=ilat).values) # the deficit at the current grid point

    thislat = float(dat.lat.isel(lat=ilat).item())
    thislon = float(dat.lon.isel(lon=ilon).item())

    # loop over concentric squares outward from the point with the deficit.  
    # Break out of this when the problem is resolved.
    # Maximum number of concentric squares is 20  
    for isq in np.arange(0,20,1):
        # get the longitude range of the concentric square
        ilon2 = np.arange(ilon-(isq+1),ilon+1+(isq+1),1)
        # flip the indices if they go negative west of the Greenwich Meridian.
        ilon2 = np.where(ilon2 >= 0, ilon2, ilon2+dat.lon.size)
        # flip the indices if they go above dat.lon.size
        ilon2 = np.where(ilon2 < dat.lon.size, ilon2, ilon2 - dat.lon.size)

        # get the latitude range of the concentric square
        lat1 = ilat - (isq+1) ; lat2 = ilat+1+(isq+1)
        if (lat1 < 0):
            lat1=0
        if (lat2 > dat.lat.size):
            lat2 = dat.lat.size
        ilat2 = np.arange(lat1,lat2,1)

        # pick out the concentric square grid points
        lons = [ datnew.lon[i].values for i in ilon2]
        lats = [ datnew.lat[i].values for i in ilat2]
        square = datnew.sel(lon=lons, lat=lats).copy(deep=True)

        # get the longitudes and latitudes of the points within the concentric square 
        # (single point for isq=0)
        lonsinner = lons[1:len(lons)-1] 
        latsinner = lats[1:len(lats)-1]

        # Stretch out the square
        square = square.stack(z=('lat','lon'))

        # Remove the inner square
        square = square.where( ~( square.lon.isin(lonsinner) & square.lat.isin(latsinner) ), drop=True)

        # Get rid of the cells of the square that already have negative emissions
        square = square.where(square > 0, drop=True)

        # Set up the area weights for the square (cos(thislat) / cos(lat))
        w = xr.DataArray( np.cos(np.deg2rad(thislat))/np.cos(np.deg2rad(square.lat)),
              dims="z", coords={"z":square.z} )

        # Initializing the array of emissions to add on
        addon = square.copy(deep=True)*0

        # iterate over the elements of the concentric square to fill up with the emissions deficit
        while deficit > 1e-14:
            # Check how many cells of the square still have emissions > 0
            cellsuse = xr.where( square > 0, 1, 0)
            nleft = np.sum(cellsuse).item()

            # If there are no cells left, then break out of this loop.
            if (nleft == 0):
                break

            # -- work out how much each remaining cell would have to take to get an equal share
            equaltake = (deficit / nleft)*w 

            # give the ones that don't have enough the max you can give them, giving the rest the equal share
            # scalling by cellsuse to not add more deficit onto cells that are already zero
            addontemp = xr.where( square < equaltake, -1.*square*cellsuse, -1.*equaltake)

            # add the addon to the overall addon array
            addon = addon + addontemp

            # workout how much of the deficit has been taken and reduce it by that much
            deficit_take = addontemp*(1./w)
            deficit = deficit + deficit_take.sum('z').values.item()

            # update the square
            square = square + addontemp

        # unstack the addon and reindex it.  Then add onto datnew.
        # set the problematic point to be equal to the current deficit
        addon = addon.unstack()
        addon = addon.where( ~np.isnan(addon), 0)
        addon = addon.reindex_like(datnew, fill_value=0)
        datnew = datnew + addon
        datnew[dict(lat=ilat,lon=ilon)] = deficit

        # Break out of the loop over concentric squares if you've reached a zero deficit (within machin precision)
        if (deficit < 1e-14):
            break
        
        # end of the loop over concentric squares
    if (deficit > 1e-14):
        print('ilon=',ilon,'ilat=',ilat)
        print('you still have a deficit after 15 concentric squares')
        sys.exit()
        
    return datnew



def spread_negative_emissions_np(datnew,lon,lat,ilon,ilat):
    """Spread out negative emissions to the nearest grid pointsi
       dat = a 2D array of (nlat,nlon) containing the emissions
       ilon = the longitude index of the current negative grid point to be spread.
       ilat = the latitude index of the current negative grid point to be spread.
       A numpy version of the above loop aiming for speed up
    """
    #datnew = dat.values.copy() # array that will have the emissions spread out
    nlat,nlon = datnew.shape
    deficit = abs(datnew[ilat,ilon])
    thislat = float(lat[ilat])
    #thislat = float(dat.lat.values[ilat])
    #thislon = float(dat.lon.values[ilon])


    # Amount of original deficit absorbed by each concentric ring
    spread_by_ring = np.zeros(60)


    # Set the original negative point to zero initially
    datnew[ilat,ilon] = 0.0

    # loop over concentric squares outward from the point with the deficit.  
    # Break out of this when the problem is resolved.
    # Maximum number of concentric squares is 20  
    for isq in range(60):

        # longitude indices of concentric square (wrapping around greenwich meridian)
        ilon2 = np.arange( ilon - (isq + 1), ilon + (isq + 1) + 1 ) % nlon

        # latitude indices of concentric squares clipped at poles (I'm not attempting to 
        # go over the top of the poles with the spreading
        lat1 = max(0, ilat - (isq + 1) )
        lat2 = min( nlat, ilat + (isq + 1) + 1)
        ilat2 = np.arange(lat1, lat2)

        # Make the rectangular square
        loninds2d, latinds2d = np.meshgrid(ilon2, ilat2)
        
        # Outer boundary of the rectangle
        ring = np.ones(latinds2d.shape, dtype=bool)
        
        # Remove the inner rectangle, exactly as in the xarray version
        if (len(ilat2) > 2) and (len(ilon2) > 2):
            ring[1:-1, 1:-1] = False
        
        latinds = latinds2d[ring]
        loninds = loninds2d[ring]


        # Only use the cells in the ring that have positive emissions
        positive = datnew[latinds,loninds] > 0.

        latinds = latinds[positive]
        loninds = loninds[positive]

        if latinds.size == 0:
            continue

        square = datnew[latinds,loninds].copy()

        # area weighting
        w = ( np.cos(np.deg2rad(thislat)) / np.cos(np.deg2rad(lat[latinds])) )

        # Keep track of the deficit in each concentric ring
        deficit_before_ring = deficit


        # iterate over concentric squares to fill up with the emissions deficit
        while deficit > 1e-14:
            cellsuse = square > 0 # only use grid cells that have emissions > 0
            nleft = cellsuse.sum()

            if nleft == 0:
              break

            equaltake = (deficit / nleft) * w
            addontemp = np.where( square < equaltake, -square, -equaltake)
           
            # can't fill cells that are already exhausted
            addontemp = np.where( cellsuse, addontemp, 0)
            
            deficit += np.sum(addontemp / w)

            square += addontemp

        spread_by_ring[isq] = deficit_before_ring - deficit

        # put the filled cells back into the array
        datnew[latinds,loninds] = square

        # remaining deficit at original point
        datnew[ilat,ilon] = -deficit

        if deficit < 1e-14:
            datnew[ilat,ilon] = 0.0
            break

    if deficit > 1e-14:
        raise RuntimeError(
          f"Still have deficit after 30 concentric squares"
          f"at ilon={ilon}, ilat={ilat}: {deficit}" )

    return datnew, spread_by_ring 
