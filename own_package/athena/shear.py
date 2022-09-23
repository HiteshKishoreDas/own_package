'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

#%%

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cr 
import sys

import os


cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca

sys.path.insert(0, f'{package_abs_path}cooling/')
import cooling_fn as cf

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as p3d
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu
import units as un
from v_turb import cs_calc


# TODO: Functionalise this script

file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'Turbulence/para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
file_loc += 'Turb.out2.00600.athdf'
# file_loc += 'Turb.out2.00501.athdf'

# file_loc = '../../../Turb.mhd.out2.00600.athdf'
file_loc = '../../../Turb.hydro.out2.00600.athdf'
#%%
# MHD_flag = True
MHD_flag = False 

out_dict = dr.get_array(file_loc, fields=['rho', 'prs', 'vel'],MHD_flag=MHD_flag)

rho = out_dict['rho']
prs = out_dict['prs']

T = (prs/rho) * KELVIN * mu

cut = 5e4
#%%
n_blob_sp, label_arr_sp = ca.clump_finder_scipy(T, cut, above_cut=False)

vel = out_dict['vel']

shear_dict, shear_map = ca.shear_calc(label_arr_sp, vel)
surface_dict          = ca.surface_area(label_arr_sp)
  
#%%
# plt.style.use('dark_background') 

# import matplotlib as mt

# y_data = np.copy(np.array(shear_dict['clump_vol']))  # [1:]
# x_data = np.copy(np.array(shear_dict['shear_vmag'])) # [1:]

# N_bin = 30

# # x_bin = np.linspace(x_data.min(), x_data.max(), num = N_bin)
# x_bin = np.linspace(0, 0.3, num = N_bin)
# y_bin = np.logspace(np.log10(y_data.min()), np.log10(y_data.max()), num = N_bin)

# plt.hist2d( x_data, y_data,\
#     bins=[x_bin,y_bin], norm=mt.colors.LogNorm() )
# plt.yscale('log')
# # plt.xscale('log')

# plt.xlabel(r'$v_{\rm shear}$ (kpc/Myr)')
# plt.ylabel('Clump volume (cells)')

# # plt.xlim(0,0.3)

# plt.colorbar()

# # plt.savefig('size_shear_hist2d_mhd.png')
# # plt.savefig('size_shear_hist2d_hydro.png')

#%%
amb_rho = 1.0  # in code units, amu/cc
T_floor = 4e4
Z_sol   = 1

# t_cool_cloud = 2.77e-5
cloud_chi = 100
t_cool_cloud = cf.tcool_calc(amb_rho*cloud_chi, T_floor, Z_sol)

cs = cs_calc(4e6, mu)
# l_shatter = 8.6e-7
l_shatter = cs*t_cool_cloud

print(f'{cs = }')
print(f'{cs*t_cool_cloud = }')


Rlsh  = 1000
Lbox  = Rlsh*40*l_shatter   # in kpc
M = 0.5
dx = Lbox/256
M0 = 4*np.pi/3 * (Rlsh*l_shatter)**3 * amb_rho * cloud_chi

t_eddy = Lbox/(cs*M)


# v_turb = M*cs*un.unit_velocity

v_shear = np.array(shear_dict['shear_vmag'])
R_clump = np.array(shear_dict['clump_vol'])
S_clump = np.array(surface_dict['clump_surface_area'])*dx*dx
R_clump = R_clump*3/(4*np.pi)
R_clump = R_clump**(1/3)

L = 4*R_clump*dx    # in kpc
M_shear = v_shear/cs
cs_cold = cs_calc(4e4, mu) * un.unit_velocity  # in cm/s

u_prime = 50 * (M_shear**(4/5)) * ((cs_cold/1.5e6)**(4/5)) * ((t_cool_cloud/0.03)**-0.1)
M_turb  = u_prime/cs_cold

v_in_slow_cool = 9.5  * (M_turb ** (3/4)) * ((L*1000/100)**(1/4)) * ((t_cool_cloud/0.03)**(-1/4))
v_in_fast_cool = 11.3 * (M_turb ** (1/2)) * ((L*1000/100)**(1/2)) * ((t_cool_cloud/0.03)**(-1/2))

t_turb = L/u_prime
Da_arr = t_turb/t_cool_cloud

v_in_slow_cool *= (Da_arr<=1) * 1e5 / un.unit_velocity
v_in_fast_cool *= (Da_arr>1)  * 1e5 / un.unit_velocity 

m_dot_slow = np.sum(v_in_slow_cool * S_clump * amb_rho)
m_dot_fast = np.sum(v_in_fast_cool * S_clump * amb_rho)
m_dot_total= m_dot_slow+m_dot_fast

m_m0_dot_tot = m_dot_total*t_eddy/M0

#%%

print(f'slow : {m_dot_slow}')
print(f'fast : {m_dot_fast}')
print(f'total: {m_dot_total}')
print(f'total in M/M0, t/t_eddy: {m_m0_dot_tot}')
print(f'total in log(M/M0), t/t_eddy: {m_m0_dot_tot/5}')
print(f'Mdot from figure: {8/1.75}')



# %%
