'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cr 
import sys
import os

CONST_pc  = 3.086e18
CONST_yr  = 3.154e7
CONST_amu = 1.66053886e-24
CONST_kB  = 1.3806505e-16

unit_length = CONST_pc*1e3  # 1 kpc
unit_time   = CONST_yr*1e6  # 1 Myr
unit_density = CONST_amu    # 1 mp/cm-3
unit_velocity = unit_length/unit_time

KELVIN = unit_velocity*unit_velocity*CONST_amu/CONST_kB

Xsol = 1.0
Zsol = 1.0

X = Xsol * 0.7381
Z = Zsol * 0.0134
Y = 1 - X - Z

mu  = 1.0/(2.*X+ 3.*(1.-X-Z)/4.+ Z/2.);
mue = 2.0/(1.0+X);
muH = 1.0/X;

mH = 1.0


cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as p3d
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 


file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
file_loc += 'Turb.out2.00681.athdf'

MHD_flag = True

out_dict = dr.get_array(file_loc,MHD_flag=MHD_flag)

rho = out_dict['rho']
prs = out_dict['P']

T = (prs/rho) * KELVIN * mu

cut = 5e4

n_blob_sp, label_arr_sp = ca.clump_finder_scipy(T, cut, above_cut=False)

vel = out_dict['vel']

shear_dict, shear_map = ca.shear_calc(label_arr_sp, vel)
  

plt.style.use('dark_background') 

plt.hist(np.array(shear_dict['shear_vmag']))
plt.show()