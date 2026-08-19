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

# Order of operations:

(1) populate the yaml files with details on filenames, variables an remapping information following the example yml files.
(2) If SOAG is needed and you are computing it from the components, do that using the script in ./SOAG
(3) Remap any ne30 files to f09 or between any other grid options (a wgt file for the relevant grid remapping should simply be provided in the yml file)
  (a) make sure `./REMAP/list_files.py` is pointing to the correct yml file
  (b) run `./REMAP/remap_files.sh`
 

