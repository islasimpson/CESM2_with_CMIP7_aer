# Dealing with so4_a1 directly from input4MIPS

This is necessary because there was a difference in the diameter that was used for calculating the particle emissions number between the sub-components of so4_a1 between CMIP6 and CMIP7.

| Sector | CMIP6 diameter (µm) | CMIP7 diameter (µm) |
|--------|---------------------|---------------------|
| Agriculture | 0.134 | 0.134 |
| Solvents | 0.134 | 0.261 |
| Waste | 0.134 | 0.261 |
| Shipping | 0.261 | 0.261 |

This means that in order to calculate the particle number emissions they need to be treated separately as [Agriculture], [Solvents+Waste],[Shipping].

So, I'm getting so4_a1 from the SO2 from input4MIPs directly here.

# Order of operations:

<ol>
<li>Obtain the different components of so4_a1 using
  - `output_so4_a1_CMIP7.ipynb`
  - `output_so4_a1_CMIP6.ipynb`
</li>
<li>Make a scrip file for the native CEDS input4MIPs emissions grid
  - `make_CEDS_scripfile_CMIP6.py`
  - `make_CEDS_scripfile_CMIP7.py`
</li>
</li>Make a weight file to regrid from CEDS to the desired grid
  - `make_CEDS_to_ne30_weightfile_CMIP7.sh`
  - `make_CEDS_to_f09_weightfile_CMIP6.sh`
</li>
<li>Remap to the desired grid.  For CMIP7 I'm going via the ne30 grid since that's how I'm doing the other emissions
  - `remap_ceds_to_ne30pg3.sh`
  - `remap_ceds_to_f09.sh`
</li>
<li>Check the sum of the components generated add up to the original emissions
  - `./checking/compare_mine_bens.ipynb` - for CMIP7
  - `./checking/compare_mine_louisas.ipynb` - for CMIP6
</li>

</ol>




