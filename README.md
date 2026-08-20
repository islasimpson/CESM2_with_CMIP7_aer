# CESM2_with_CMIP7_aer
Repository for generating and checking emissions files to run CESM2 with CMIP7 aerosol emissions.

To avoid changing the piControl baseline and necessitating re-tuning the CMIP7 aerosol emission anomalies relative to 1850 are added onto the CMIP6 piControl baseline.  This is done on a month-by-month basis over the case of the seasonal cycle.  If the CMIP6 piControl baseline is substantially smaller than the CMIP7 baseline in particular locations, the possibility could arise that the emissions go negative when the CMIP7 anomalies are added onto the CMIP6 baseline.  To handle this, the emissions deficit is spread out to adjacent grid cells evenly in concentric squares, to the extent sufficient positive emissions remain in those grid cells to carry the deficit.

# Contents of this repo:

- yaml files that contain the information on the CMIP6 and CMIP7 source files and regridding needs 
  - `emission_file_anthro_sfc_info.yml` - Specifies source files, variables and remapping needs for anthropogenic surface emissions 
  - `emission_file_anthro_elev_info.yml` - Specifies source files, variables and remapping needs for anthropogenic elevated emissions 
  - `emission_file_bmb_sfc_info.yml` - Specifies source files, variables and remapping needs for biomass surface emissions

- regridding scripts to convert from the ne30 grid to the f09 grid
  - `remap_files.sh` - bash script to be run to remap all the required files
  - `list_files.py` - python script used by `remap_files.sh` to read in the information from the yaml file (note, you'll need to edit the yml file being opened here depending on which kind of emissions you're wanting to regrid.


- scripts for computing the anomalies relative to the CMIP6 piControl and spreading emissions deficits
  - `./make_emissions/anthro/sfc/CMIP7/make_anthro_sfc_emissions.ipynb`
  - `./make_emissions/anthro/elev/CMIP7/make_anthro_elev_emissions.ipynb`
  - `./make_emissions/bmb/sfc/CMIP7/make_bmb_sfc_emissions.ipynb

# Order of operations:

<ol>
  <li>populate the yaml files with details on filenames, variables an remapping information following the example yml files.</li>
  <li>If SOAG is needed and you are computing it from the components, do that using the script in ./SOAG</li>
  <li>Remap any ne30 files to f09 or between any other grid options (a wgt file for the relevant grid remapping should simply be provided in the yml file)
    <ol type="a">
      <li>make sure `./REMAP/list_files.py` is pointing to the correct yml file</li>
      <li>run `./REMAP/remap_files.sh`</li>
    </ol>
  <li>Compute the anomalous emissions and spread out any deficits to nearby grid points using the appropriate scripts</li>
  <li>Check the output
    <ol, type="a">
      <li>`./verify_emissions/check_timeseries/check_emissions_timeseries.ipynb` - Check how the globally integrated timeseries are looking.
      <li>`./verify_emissions/check_spread/check_percentage_spread.ipynb` - Check the fraction of emissions being spread and how far
      <li>`./verify_emissions/check_maps/check_maps.ipynb` - Check how maps of the species are looking
    </ol>
</ol>
 
# Additional elements for biomass burning emissions:

- SOAGx1.5 was computed from its constituent components using
  - `./make_emissions/SOAG/make_SOAG.ipynb`
- SOAGx1.5 was checked against an existing SOAG file using 
  - `./make_emissions/SOAG/check_SOAG.ipynb`
- The computation of CMIP7 anomalies relative to the piControl and their addition onto the CMIP6 piControl was done on the unsmoothed emissions to avoid the differences between the piControl's that arise between unsmoothed (CMIP6) and smoothed (CMIP7).  The CMIP7 smoothed emissions provided in input4MIPs are smoothed all the way back so these are not being used.  Instead the emissions are smoothed after the anomaly computation.
- Smoothing of contructed biomass burning emissions was done following the CMIP7 protocol which is centered 5 year running means using
  - `./make_emissions/smooth_bmb/smooth_bmb.ipynb`
- Smoothing was checked at 
  - `./make_emissions/check_smoothed_bmb.ipynb`
