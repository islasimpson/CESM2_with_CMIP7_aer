#!/bin/bash
module load nco
basepath="/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/from_CEDS/CMIP7/"
mapping=$basepath'CEDS_to_ne30pg3_conserve.nc'

infile=$basepath'so4_a1_ag_emissions_native.nc'
outfile=$basepath'so4_a1_ag_emissions_ne30pg3.nc'

ncremap -m $mapping -i $infile -o $outfile

infile=$basepath'so4_a1_ship_emissions_native.nc'
outfile=$basepath'so4_a1_ship_emissions_ne30pg3.nc'

ncremap -m $mapping -i $infile -o $outfile

infile=$basepath'so4_a1_slv_was_emissions_native.nc'
outfile=$basepath'so4_a1_slv_was_emissions_ne30pg3.nc'

ncremap -m $mapping -i $infile -o $outfile
