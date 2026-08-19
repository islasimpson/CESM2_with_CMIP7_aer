# CESM2_with_CMIP7_aer
Repository for generating and checking emissions files to run CESM2 with CMIP7 aerosol emissions.

To avoid changing the piControl baseline and necessitating re-tuning the CMIP7 aerosol emission anomalies relative to 1850 are added onto the CMIP6 piControl baseline.  This is done on a month-by-month basis over the case of the seasonal cycle.  If the CMIP6 piControl baseline is substantially smaller than the CMIP7 baseline in particular locations, the possibility could arise that the emissions go negative when the CMIP7 anomalies are added onto the CMIP6 baseline.  To handle this, the emissions deficit is spread out to adjacent grid cells evenly in concentric squares, to the extent sufficient positive emissions remain in those grid cells to carry the deficit.

# Contents of this repo:

- yaml files that contain the information on the CMIP6 and CMIP7 source files and regridding needs 
  - `emission_file_anthro_sfc_info.yml` 
  - `emission_file_anthro_elev_info.yml` 
  - `emission_file_bmb_sfc_info.yml`

- script for computing the anomalies relative to the CMIP6 piControl and spreading emissions deficits
  - `./make_emissions/anthro/sfc/CMIP7/make_anthro_sfc_emissions.ipynb`




