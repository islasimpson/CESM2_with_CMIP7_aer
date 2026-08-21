import xarray as xr
import numpy as np

ds = xr.open_dataset("/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/input4MIPs/CMIP6/PNNL-JGCRI/"
                     "SO2-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18_gn_185001-185012.nc")

lon = ds.lon.values
lat = ds.lat.values

lon_bnds = ds.lon_bnds.values
lat_bnds = ds.lat_bnds.values

nlon = lon.size
nlat = lat.size
grid_size = nlon*nlat

lon2d, lat2d = np.meshgrid(lon,lat)

corner_lon = np.empty((nlat,nlon,4))
corner_lat = np.empty((nlat,nlon,4))

for j in range(nlat):
    for i in range(nlon):
        corner_lon[j, i, :] = [
            lon_bnds[i,0],
            lon_bnds[i,1],
            lon_bnds[i,1],
            lon_bnds[i,0]
        ]

        corner_lat[j, i, :] = [
            lat_bnds[j,0],
            lat_bnds[j,0],
            lat_bnds[j,1],
            lat_bnds[j,1]
        ]

scrip = xr.Dataset()

scrip["grid_dims"] = xr.DataArray(
    np.array([nlon, nlat], dtype="int32"),
    dims=["grid_rank"]
)

scrip["grid_center_lon"] = xr.DataArray(
    lon2d.ravel(),
    dims=["grid_size"]
)

scrip["grid_center_lat"] = xr.DataArray(
    lat2d.ravel(),
    dims=["grid_size"]
)

scrip["grid_corner_lon"] = xr.DataArray(
    corner_lon.reshape(grid_size,4),
    dims=["grid_size","grid_corners"]
)

scrip["grid_corner_lat"] = xr.DataArray(
    corner_lat.reshape(grid_size,4),
    dims=["grid_size","grid_corners"]
)

scrip["grid_imask"] = xr.DataArray(
    np.ones(grid_size, dtype="int32"),
    dims=["grid_size"]
)

scrip["grid_center_lon"].attrs["units"] = "degrees"
scrip["grid_center_lat"].attrs["units"] = "degrees"
scrip["grid_corner_lon"].attrs["units"] = "degrees"
scrip["grid_corner_lat"].attrs["units"] = "degrees"

scrip["grid_imask"].attrs["units"] = "unitless"
scrip.attrs["title"] = "CEDS 0.5x0.5 degree SCRIP grid"

encoding = {
    "grid_center_lon": {"_FillValue": None},
    "grid_center_lat": {"_FillValue": None},
    "grid_corner_lon": {"_FillValue": None},
    "grid_corner_lat": {"_FillValue": None},
    "grid_dims": {"_FillValue": None},
    "grid_imask": {"_FillValue": None},
}

scrip.to_netcdf("/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/from_CEDS/CMIP6/CEDS_scrip.nc", encoding = encoding)



