import xarray as xr
import numpy as np
import pandas as pd
import yaml
from pathlib import Path
import sys

# Utilities for parsing emission_file_info.yml and reading the relevant emissions files
def read_emissions(infofile, species, cmip, exp, dstgrid='f09'):
    """ 
    infofile = yaml file containing emissions file information
    species = the chemical species to be read
    cmip = the CMIP era (either "cmip6" or "cmip7"
    exp = the experiment name (either "piControl" or "hist")
    dstgrid = the destination grid when using remapped files (currently only "f09")
    """
  
    with open(infofile) as f:
        info = yaml.safe_load(f)
    species_info = info[species]

    # loop over files that correspond to the species/cmip/exp
    files = species_info[cmip][exp]['files']
    allvars=[]
    for ifile in files:
        # change the filename if it has been remapped
        if "remap" in ifile:
            fname = Path(ifile['path']).name
            if dstgrid != 'f09':
                print('the only valid dstgrid right now is f09')
                sys.exit()
            fpath="/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/REMAP/"+dstgrid+"/"+fname
        else:
            fpath = ifile['path']

        print(fpath)
        dat = xr.open_dataset(fpath)

        if exp == 'piControl':
            dat = dat.sel(time=slice("1850-01-01","1850-12-31"))

        for ivar in ifile['vars']:
            print(ivar)
            allvars.append(dat[ivar])
    allvars = xr.concat(allvars, dim='emiss_type')
    return allvars
