#!/usr/bin/env python3
# script for parsing yaml file and producing a list of files and whether they need to be remapped or not
import yaml

with open("../../emission_file_bmb_sfc_info.yml") as f:
    info = yaml.safe_load(f)
#with open("../../emission_file_info.yml") as f:
#    info = yaml.safe_load(f)

for species, species_info in info.items():
    for cmip, cmip_info in species_info.items():
        for exp, exp_info in cmip_info.items():
            for f in exp_info["files"]:
                remap = "yes" if "remap" in f else "no"
                wgtfile = weights=f["remap"]["wgtfile"] if "remap" in f else "NaN"
                print(
                     species,
                     cmip,
                     exp,
                     f["path"],
                     remap,
                     wgtfile,
                     sep="|"
                     )
