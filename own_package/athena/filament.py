'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

#%%

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr 
# from cmasher import * 
import sys
import os

style_lib  = '../plot/style_lib/' 
# pallette   = style_lib + 'cup_pallette.mplstyle'
pallette   = style_lib + 'dark_pallette.mplstyle'
# pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca
import coherence as ch

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu

#%%

file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
file_loc += 'Turb.out2.00600.athdf'

# file_loc1 = '../../../Turb.hydro.out2.00600.athdf'
# file_loc2 = '../../../Turb.mhd.out2.00600.athdf'


MHD_flag = True
MHD_flag = False 

wnd_list = []
coh_list = []

file_loc_list = [file_loc]

for file_loc in file_loc_list:

    out_dict = dr.get_array_athena(file_loc, fields=["rho"],MHD_flag=MHD_flag)

    rho = out_dict['rho']
    # prs = out_dict['P']

    # T = (prs/rho) * KELVIN * mu


    devices = 4*['cpu']
    parallel_flag = False
    coh_list_i, wnd_list_i = ch.frac_aniso_window_variation(inp_arr=rho, num=2, parallel_flag=parallel_flag, devices=devices)

    wnd_list.append(wnd_list_i)
    coh_list.append(coh_list_i)

#%% 
plt.figure()

plt.plot(wnd_list[0], coh_list[0], label='HD')
# plt.plot(wnd_list[1], coh_list[1], label='MHD')

plt.xlabel('Window (in grid cells)')
plt.ylabel('Anisotropy')

# plt.yscale('log')
# plt.xscale('log')
plt.legend()

# plt.show()
# plt.savefig('anisotropy.png')


# %%
