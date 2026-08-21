path="/glade/u/apps/casper/23.10/spack/opt/spack/esmf/8.5.0/mpi-serial/2.3.0/oneapi/2023.2.1/dfkx/bin/"
#Source grid
srcgrid="/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/from_CEDS/CEDS_scrip.nc"
#Destination grid
dstgrid="/glade/campaign/cesm/cesmdata/inputdata/share/scripgrids/ne30pg3_scrip_170417.nc"

$path/ESMF_RegridWeightGen -s $srcgrid -d $dstgrid --src_type SCRIP --dst_type SCRIP -m "conserve" -w "CEDS_to_ne30pg3_conserve.nc"
