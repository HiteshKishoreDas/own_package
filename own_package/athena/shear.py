'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cr 
import sys
import os


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
from units import KELVIN, mu



file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
file_loc += 'Turb.out2.00600.athdf'

# MHD_flag = True
MHD_flag = False 

out_dict = dr.get_array(file_loc,MHD_flag=MHD_flag)

rho = out_dict['rho']
prs = out_dict['P']

T = (prs/rho) * KELVIN * mu

cut = 5e4

n_blob_sp, label_arr_sp = ca.clump_finder_scipy(T, cut, above_cut=False)

vel = out_dict['vel']

shear_dict, shear_map = ca.shear_calc(label_arr_sp, vel)
  
#%%
plt.style.use('dark_background') 

import matplotlib as mt

y_data = np.copy(np.array(shear_dict['clump_vol']))  # [1:]
x_data = np.copy(np.array(shear_dict['shear_vmag'])) # [1:]

# x_data = x_data[y_data<1e2]
# y_data = y_data[y_data<1e2]

N_bin = 30

x_bin = np.linspace(x_data.min(), x_data.max(), num = N_bin)
y_bin = np.logspace(np.log10(y_data.min()), np.log10(y_data.max()), num = N_bin)

plt.hist2d( x_data, y_data,\
    bins=[x_bin,y_bin], norm=mt.colors.LogNorm() )
plt.yscale('log')
# plt.xscale('log')

plt.xlabel(r'$v_{\rm shear}$ (kpc/Myr)')
plt.ylabel('Clump volume (cells)')

plt.colorbar()

plt.savefig('size_shear_hist2d_mhd.png')
# plt.savefig('size_shear_hist2d_hydro.png')

# %%
