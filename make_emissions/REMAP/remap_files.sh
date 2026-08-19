#!/bin/bash
module load nco
pathout="/glade/campaign/cgd/cas/islas/python_savs/CESM2_with_CMIP7_aer/make_emissions/REMAP/f09/"

python list_files.py | while IFS="|" read species cmip exp path remap wgtfile
do
    echo "$species $cmip $exp"
    if [[ $remap == "yes" ]]; then 
        echo "$path"
        fname=$(basename "$path")
        fout=$pathout$fname
        echo $fout
        echo $wgtfile
        ncremap -m $wgtfile -i $path -o $fout
    fi
done
