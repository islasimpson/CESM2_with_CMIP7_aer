# list of molecular weights
# Note the options are kept here to treat agriculture + solvents + waste together 
# or separately because there was some confusion over whether the diameter shoudl have been changed
# for slv_was in CMIP7.  Turns out that was a mistake and the diameter should not have changed so 
# I'll be using the ag_slv_was option, but the _ag and _slv_was options are here in case
# they are needed in the future if the chemists change their mind


mol_weights={'bc_a4':12,
             'SO2':64,
             'so4_a1_ene_ind': 115,
             'so4_a1_ag_slv_was': 115,
             'so4_a1_ag': 115,
             'so4_a1_ship': 115,
             'so4_a1_slv_was': 115,
             'so4_a1_bmb': 115,
             'so4_a2': 115,
             'pom_a4': 12,
             'SOAG': 12,
             'BIGALK': 72,
             'BIGENE': 56,
             'TOLUENE': 92,
             'BENZENE': 78,
             'XYLENES': 106,
             'ISOP': 68,
             'MTERP': 136}

# list of molecular diameters
particle_diams={'bc_a4': 0.134e-6,
                 'so4_a1_ene_ind': 0.261e-6, # energy + industry vertically distributed
                 'so4_a1_ag_slv_was': 0.134e-6, # agriculture + solvents + waste
                 'so4_a1_ag': 0.134e-6, # agriculture
                 'so4_a1_ship': 0.261e-6, # shipping
                 'so4_a1_slv_was': 0.134e-6, # solvents + waste
                 'so4_a1_bmb': 0.134e-6, # biomass burning
                 'so4_a2': 0.0504e-6, # residential + transport
                 'pom_a4': 0.134e-6}

# list of particle densities
particle_dens = {'bc_a4': 1700.,
            'so4_a1_ene_ind': 1770., # energy + industry vertically distributed
            'so4_a1_sg_slv_was': 1770., # agriculture + solvents + waste
            'so4_a1_ag': 1770., # agriculture
            'so4_a1_ship': 1770. , # shipping
            'so4_a1_slv_was': 1770. , # solvents + waste
            'so4_a1_bmb': 1770, # biomass burning
            'so4_a2': 1770., # residential + transport
            'pom_a4': 1000.}
