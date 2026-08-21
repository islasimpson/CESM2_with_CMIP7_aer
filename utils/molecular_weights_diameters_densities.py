# list of molecular weights
# so4_a1 here is the anthropogenic vertically distributed so4_a1 (doesn't atter for weights but does for analogous
# dictionaries of particle diameter.
mol_weights={'bc_a4':12,
             'SO2':64,
             'so4_a1_ene_ind': 115,
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
particle_diams_cmip7={'bc_a4': 0.134e-6,
                 'so4_a1_ene_ind': 0.261e-6, # energy + industry vertically distributed
                 'so4_a1_ag': 0.134e-6, # agriculture
                 'so4_a1_ship': 0.261e-6, # shipping
                 'so4_a1_slv_was': 0.261e-6, # solvents + waste
                 'so4_a1_bmb': 0.134e-6, # biomass burning  
                 'so4_a2': 0.0504e-6, # residential + transport
                 'pom_a4': 0.134e-6}

particle_diams_cmip6={'bc_a4': 0.134e-6,
                 'so4_a1_ene_ind': 0.261e-6, # energy + industry vertically distributed
                 'so4_a1_ag': 0.134e-6, # agriculture
                 'so4_a1_ship': 0.261e-6, # shipping
                 'so4_a1_slv_was': 0.134e-6, # solvents + waste
                 'so4_a1_bmb': 0.134e-6, # biomass burning
                 'so4_a2': 0.0504e-6, # residential + transport
                 'pom_a4': 0.134e-6}

# list of particle densities
particle_dens = {'bc_a4': 1700.,
            'so4_a1_ene_ind': 1770., # energy + industry vertically distributed
            'so4_a1_ag': 1770., # agriculture
            'so4_a1_ship': 1770. , # shipping
            'so4_a1_slv_was': 1770. , # solvents + waste
            'so4_a1_bmb': 1770, # biomass burning
            'so4_a2': 1770., # residential + transport
            'pom_a4': 1000.}
