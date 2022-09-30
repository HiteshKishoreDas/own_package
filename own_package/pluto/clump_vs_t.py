#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created Date: Thursday, June 24th 2021, 5:58:07 pm
Author: Hitesh
'''

import numpy as np
import json as js

import pyPLUTO
import pyPLUTO.pload as pp

# import workdir_2 as wdir
# import workdir_2_dept as wdir
import workdir_2_drish as wdir

import clump_count_MG20 as ccmg
# import plot_fn as pf
import lamfn as lf
# import curl as cl
# import bash_run as br

CONST_amu = 1.66053886e-24
UNIT_DENSITY = 1.66053886e-24
UNIT_VELOCITY = 1.e8
UNIT_LENGTH = 3.0856775807e18  * 1.e5
CONST_kB = 1.3806505e-16
KELVIN = UNIT_VELOCITY*UNIT_VELOCITY*CONST_amu/CONST_kB

ul = 100 # in kpc
uv = 1.0E+8 # in cm/s
ut = ((ul * 3.086E+21)/uv)  # in s
ut = (ut / 3.154e+13)    # in Myr

uv = 1.022  # in kpc/Myr

# dt = 5.0*1e-2*ut  # in Myr ############################

# wdir_list = [wdir.wdir38,wdir.wdir39,wdir.wdir40,wdir.wdir41,wdir.wdir42,wdir.wdir43,wdir.wdir44]
# dt_list = [5.0*1e-4*ut,  1.0*1e-3*ut,  5.0*1e-2*ut, 5.0*1e-2*ut, 5.0*ut,5.0*1e-4*ut, 5.0*1e-4*ut]
# file_list = ['R1','R2','R3', 'R3_highres', 'R4','R1_assym', 'R1_lowres']

# wdir_list = [wdir.wdir38,wdir.wdir42]
# dt_list = [5.0*1e-4*ut, 5.0*ut]
# file_list = ['R1', 'R4']

wdir_list = ["/home/hitesh/Project/MultiD_TI/PLUTO_4_4/TI/2D_nl_parascan_MG21_assym_heat_R0/"]#[wdir.wdir47]
dt_list = [5.0*1e-5*ut]
file_list = ['assym_heat_R0']


# wdir_list = [wdir.wdir41]
# dt_list = [5.0*ut]
# file_list = ['R4']


# wdir_list = [wdir.wdir22]
# dt_list = [5.0*1e-4*ut]
# file_list = ['R1']


for i_wd,wd in enumerate(wdir_list):

    nlinf = pyPLUTO.nlast_info(w_dir=wd+'output/')

    clump_rho_list = []
    clump_T_list = []
    t_list = []

    min_cstc = []
    size_hist_list = []
    mass_hist_list = []

    for n in range(nlinf['nlast']):

        print(n)

        t_list.append(n*dt_list[i_wd])

        D = pp.pload(n, w_dir=wd+'output/')

        T = D.prs/D.rho*KELVIN*lf.MMWt_mu(D.tr1,D.tr2)

        rho_cut = 10

        clump_n,label_arr = ccmg.clump_MG20(D.rho,rho_cut,True)

        clump_rho_list.append(clump_n)

        T_cut = 1.0*1e6

        clump_n,label_arr = ccmg.clump_MG20(T,T_cut,False)

        clump_T_list.append(clump_n)

        nbins = 30

        #size_hist, mass_hist = ccmg.clump_hist(label_arr,D,nbins,2)

        #min_cstc.append(np.min(lf.cs_data(D)*lf.tcool_data(D))*ul)

        #size_hist_list.append(size_hist)
        #mass_hist_list.append(mass_hist)
            
    save_arr = np.zeros((len(t_list),4),dtype=float)
    save_arr[:,0] = np.array(t_list)
    save_arr[:,1] = np.array(clump_rho_list)
    save_arr[:,2] = np.array(clump_T_list)
    #save_arr[:,3] = np.array(min_cstc)

    np.savetxt("save_arr/clump_vs_t_"+file_list[i_wd], save_arr)

    with open("save_arr/clump_size_hist_"+file_list[i_wd],"w") as filehandle:

        js.dump(size_hist_list,filehandle)

    with open("save_arr/clump_mass_hist_"+file_list[i_wd],"w") as filehandle:

        js.dump(mass_hist_list,filehandle)